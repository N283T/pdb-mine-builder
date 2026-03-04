"""PDBj pipeline - main PDB structure data loader."""

import logging
import traceback
from pathlib import Path
from typing import Any

import gemmi
from rich.console import Console
from sqlalchemy import MetaData, Table

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import (
    Job,
    LoaderResult,
    bulk_copy_entry,
    get_all_tables,
    get_column_names,
    get_entry_pk,
    get_table_or_none,
    run_loader_streaming,
)
from mine2.parsers.cif import parse_cif_file, parse_mmjson_file
from mine2.parsers.mmjson import merge_data, normalize_column_name
from mine2.pipelines.base import BasePipeline, sync_entry_tables, transform_category
from mine2.utils.assembly import calculate_mw_for_bu, hex_sha256
from mine2.utils.brief_summary import generate_brief_summary
from mine2.utils.patches import apply_patches

console = Console()
_default_logger = logging.getLogger("mine2.pipelines.pdbj")


# =============================================================================
# Shared helper functions for both mmJSON and CIF pipelines
# =============================================================================


def _resolve_plus_path(directory: Path | None, entry_id: str) -> Path | None:
    """Return the plus file path for an entry if it exists, otherwise None."""
    if directory is None:
        return None
    candidate = directory.joinpath(f"{entry_id}-plus.json.gz")
    return candidate if candidate.exists() else None


def _validate_plus_dir(label: str, directory: Path | None) -> Path | None:
    """Validate a plus directory exists, warning and returning None if not."""
    if directory is None:
        return None
    if not directory.exists():
        console.print(
            f"  [yellow]Warning: {label} directory not found: {directory}[/yellow]"
        )
        _default_logger.warning(
            "Configured %s directory does not exist: %s", label, directory
        )
        return None
    return directory


def _merge_extra_paths(data: dict[str, Any], job: Job) -> dict[str, Any]:
    """Merge all extra plus files from job.extra into data, in order.

    Files are merged sequentially (plus_path first, then nextgen_plus_path),
    so later sources take precedence for overlapping categories via merge_data.
    """
    extra = job.extra or {}
    for key in ("plus_path", "nextgen_plus_path"):
        path = extra.get(key)
        if path is not None:
            _default_logger.debug("Merging %s: %s", key, path)
            data = merge_data(data, parse_mmjson_file(path))
    return data


def _transform_pdbj_data(
    data: dict[str, Any],
    entry_id: str,
    meta: MetaData,
    normalize_fn: Any | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Transform PDB data into table rows dict.

    Shared by both update and load modes.

    Warning:
        This function **mutates** ``data`` by popping processed keys.
        This is intentional for memory optimization on large entries.

    Args:
        data: Parsed data dictionary (mutated: processed keys are removed).
        entry_id: PDB entry ID
        meta: SQLAlchemy MetaData instance
        normalize_fn: Column name normalizer (for mmJSON) or None (for CIF)

    Returns:
        Dict mapping table names to lists of row dicts.
    """
    table_rows: dict[str, list[dict[str, Any]]] = {}

    # Transform entry table
    entry_rows = _transform_entry(data, entry_id)
    if entry_rows:
        table_rows["entry"] = entry_rows
    data.pop("entry", None)

    # Transform brief_summary with bu_mw calculation
    brief_table = get_table_or_none(meta, "brief_summary")
    if brief_table is not None:
        brief_rows = _transform_brief_summary(data, brief_table, entry_id)
        if brief_rows:
            table_rows["brief_summary"] = brief_rows
        data.pop("brief_summary", None)

    # Transform other categories
    pk_col = get_entry_pk(meta)
    for table in get_all_tables(meta):
        if table.name in ("entry", "brief_summary"):
            continue

        rows = data.get(table.name, [])
        if not rows:
            continue

        category_rows = transform_category(rows, table, entry_id, pk_col, normalize_fn)
        if category_rows:
            table_rows[table.name] = category_rows

        data.pop(table.name, None)

    return table_rows


def _load_pdbj_data(
    data: dict[str, Any],
    entry_id: str,
    meta: MetaData,
    conninfo: str,
    normalize_fn: Any | None = None,
) -> tuple[int, int, int]:
    """Load PDB data into database tables.

    Shared by both PdbjPipeline (mmJSON) and PdbjCifPipeline (CIF).

    Args:
        data: Parsed data dictionary
        entry_id: PDB entry ID
        meta: SQLAlchemy MetaData instance
        conninfo: Database connection string
        normalize_fn: Column name normalizer (for mmJSON) or None (for CIF)

    Returns:
        Tuple of (inserted_count, updated_count, deleted_count)
    """
    table_rows = _transform_pdbj_data(data, entry_id, meta, normalize_fn)

    return sync_entry_tables(
        conninfo=conninfo,
        meta=meta,
        entry_id=entry_id,
        table_rows=table_rows,
    )


def _transform_entry(data: dict[str, Any], entry_id: str) -> list[dict]:
    """Transform entry data."""
    rows = data.get("entry", [])
    if not rows:
        return [{"pdbid": entry_id, "id": entry_id.upper()}]

    result = []
    for row in rows:
        result.append(
            {
                "pdbid": entry_id,
                **{k: v for k, v in row.items() if v is not None},
            }
        )
    return result


def _transform_brief_summary(
    data: dict[str, Any],
    table: Table,
    entry_id: str,
) -> list[dict]:
    """Generate brief_summary from other categories.

    Generates all brief_summary fields from pdbx_database_status,
    pdbx_audit_revision_history, citation, entity_poly, and other categories.
    Also calculates bu_mw (biological unit molecular weight) and adds to plus_fields.
    """
    # Calculate bu_mw
    bu_mw = calculate_mw_for_bu(data)

    # Generate brief_summary from other categories
    row = generate_brief_summary(data, entry_id, bu_mw)

    # Filter to only columns defined in schema
    schema_columns = get_column_names(table)
    filtered_row = {k: v for k, v in row.items() if k in schema_columns}

    return [filtered_row]


class PdbjPipeline(BasePipeline):
    """Pipeline for loading PDB structure data."""

    name = "pdbj"
    file_pattern = "*-noatom.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract entry ID from filepath.

        Handles filenames like: 100d-noatom.json.gz -> 100d
        """
        name = filepath.name
        # Remove .json.gz
        if name.endswith(".json.gz"):
            name = name[:-8]
        # Remove -noatom suffix
        if name.endswith("-noatom"):
            name = name[:-7]
        return name

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find mmJSON files and pair with plus/nextgen-plus data if available."""
        data_dir = Path(self.config.data)
        plus_dir = _validate_plus_dir(
            "plus",
            Path(self.config.data_plus) if self.config.data_plus else None,
        )
        nextgen_plus_dir = _validate_plus_dir(
            "nextgen-plus",
            Path(self.config.data_nextgen_plus)
            if self.config.data_nextgen_plus
            else None,
        )

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath in data_dir.rglob(self.file_pattern):
            entry_id = self.extract_entry_id(filepath)
            jobs.append(
                Job(
                    entry_id=entry_id,
                    filepath=filepath,
                    extra={
                        "plus_path": _resolve_plus_path(plus_dir, entry_id),
                        "nextgen_plus_path": _resolve_plus_path(
                            nextgen_plus_dir, entry_id
                        ),
                    },
                )
            )

            if limit and len(jobs) >= limit:
                break

        if plus_dir:
            count = sum(1 for j in jobs if j.extra.get("plus_path") is not None)
            console.print(f"  Plus data matched: {count}/{len(jobs)}")
        if nextgen_plus_dir:
            count = sum(1 for j in jobs if j.extra.get("nextgen_plus_path") is not None)
            console.print(f"  Nextgen-plus (SIFTS) matched: {count}/{len(jobs)}")

        return jobs

    def process_job(
        self,
        job: Job,
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PDB entry."""
        try:
            from mine2.models import get_metadata

            meta = get_metadata(schema_name)

            # Load main data and merge any plus sources
            data = parse_mmjson_file(job.filepath)
            data = _merge_extra_paths(data, job)

            # Apply entry-specific patches
            apply_patches(job.entry_id, data)

            # Add hash columns to pdbx_struct_assembly_gen (avoid B-tree index limit)
            if "pdbx_struct_assembly_gen" in data:
                for row in data["pdbx_struct_assembly_gen"]:
                    row["_hash_asym_id_list"] = hex_sha256(row.get("asym_id_list", ""))
                    row["_hash_oper_expression"] = hex_sha256(
                        row.get("oper_expression", "")
                    )

            # Transform and load
            inserted, updated, _deleted = _load_pdbj_data(
                data=data,
                entry_id=job.entry_id,
                meta=meta,
                conninfo=conninfo,
                normalize_fn=normalize_column_name,
            )

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=inserted,
                rows_updated=updated,
            )

        except Exception as e:
            # Include traceback for debugging
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )


def _parse_cif_entry(
    job: Job,
) -> dict[str, Any]:
    """Parse a CIF entry: read file, merge plus data, patch, add hashes.

    Shared by both update (process_job) and load (_process_cif_load) modes.

    Args:
        job: Job with filepath. extra may contain 'plus_path' and/or
            'nextgen_plus_path' pointing to supplementary mmJSON files.

    Returns:
        Parsed and patched data dict.
    """
    data = parse_cif_file(job.filepath)
    data = _merge_extra_paths(data, job)
    apply_patches(job.entry_id, data)

    if "pdbx_struct_assembly_gen" in data:
        for row in data["pdbx_struct_assembly_gen"]:
            row["_hash_asym_id_list"] = hex_sha256(row.get("asym_id_list", ""))
            row["_hash_oper_expression"] = hex_sha256(row.get("oper_expression", ""))

    return data


class PdbjCifPipeline(BasePipeline):
    """Pipeline for loading PDB structure data from CIF files.

    Uses mmCIF files from structures/divided/mmCIF/ directory.
    Unlike mmJSON, CIF files contain full atomic data but we only
    load categories defined in the schema (atom_site is excluded).

    Uses gemmi.CifWalk for fast file discovery with streaming job submission.
    """

    name = "pdbj-cif"
    # file_pattern not used - using gemmi.CifWalk instead

    # extract_entry_id inherited from BasePipeline handles .cif.gz and .cif

    def run(
        self, limit: int | None = None, logger: logging.Logger | None = None
    ) -> list[LoaderResult]:
        """Run the pipeline with streaming job submission.

        Jobs are submitted to workers immediately as CifWalk discovers files,
        allowing scanning and processing to happen in parallel.
        """
        if logger is None:
            logger = _default_logger

        console.print(f"  Data dir: {self.config.data}")

        data_dir = Path(self.config.data)
        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        # Use streaming loader - jobs submitted as discovered
        results = run_loader_streaming(
            settings=self.settings,
            schema_name=self.meta.schema,
            jobs_iter=self._iter_jobs(),
            process_func=self.process_job,
            max_workers=self.settings.rdb.get_workers(),
            limit=limit,
            logger=logger,
        )

        return results

    def _iter_jobs(self):
        """Yield jobs as CifWalk discovers files.

        This is a generator that yields Job objects immediately,
        allowing the streaming loader to submit them to workers.
        """
        data_dir = Path(self.config.data)
        if not data_dir.exists():
            return

        plus_dir = _validate_plus_dir(
            "plus",
            Path(self.config.data_plus) if self.config.data_plus else None,
        )
        nextgen_plus_dir = _validate_plus_dir(
            "nextgen-plus",
            Path(self.config.data_nextgen_plus)
            if self.config.data_nextgen_plus
            else None,
        )

        for filepath_str in gemmi.CifWalk(str(data_dir)):
            filepath = Path(filepath_str)
            entry_id = self.extract_entry_id(filepath)
            yield Job(
                entry_id=entry_id,
                filepath=filepath,
                extra={
                    "plus_path": _resolve_plus_path(plus_dir, entry_id),
                    "nextgen_plus_path": _resolve_plus_path(nextgen_plus_dir, entry_id),
                },
            )

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find CIF files using gemmi.CifWalk.

        Note: run() uses streaming via _iter_jobs() for better performance,
        but this method is provided for testing and compatibility.
        """
        jobs = []
        for job in self._iter_jobs():
            jobs.append(job)
            if limit and len(jobs) >= limit:
                break
        return jobs

    def process_job(
        self,
        job: Job,
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PDB entry from CIF."""
        try:
            from mine2.models import get_metadata

            meta = get_metadata(schema_name)
            data = _parse_cif_entry(job)

            inserted, updated, _deleted = _load_pdbj_data(
                data=data,
                entry_id=job.entry_id,
                meta=meta,
                conninfo=conninfo,
                normalize_fn=None,
            )

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=inserted,
                rows_updated=updated,
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )


def run(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the pdbj pipeline (mmJSON version)."""
    if logger is None:
        logger = _default_logger
    pipeline = PdbjPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the pdbj-cif pipeline (CIF version)."""
    if logger is None:
        logger = _default_logger
    pipeline = PdbjCifPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)


# =============================================================================
# Load mode (COPY protocol, no delta sync)
# =============================================================================


def _process_cif_load(
    job: Job,
    schema_name: str,
    conninfo: str,
) -> LoaderResult:
    """Worker: parse CIF -> transform -> bulk_copy_entry (no delta sync)."""
    try:
        from mine2.models import get_metadata

        meta = get_metadata(schema_name)
        data = _parse_cif_entry(job)

        table_rows = _transform_pdbj_data(
            data=data,
            entry_id=job.entry_id,
            meta=meta,
            normalize_fn=None,
        )

        inserted = bulk_copy_entry(
            conninfo=conninfo,
            schema=meta.schema,
            entry_id=job.entry_id,
            pk_column=get_entry_pk(meta),
            table_rows=table_rows,
        )

        return LoaderResult(
            entry_id=job.entry_id,
            success=True,
            rows_inserted=inserted,
        )

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return LoaderResult(
            entry_id=job.entry_id,
            success=False,
            error=error_msg,
        )


def run_cif_load(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run pdbj pipeline in load mode (COPY, no delta sync)."""
    if logger is None:
        logger = _default_logger

    console.print(f"  Data dir: {config.data}")

    pipeline = PdbjCifPipeline(settings, config, meta)

    data_dir = Path(config.data)
    if not data_dir.exists():
        console.print(f"  [red]Data directory not found: {data_dir}[/red]")
        return []

    results = run_loader_streaming(
        settings=settings,
        schema_name=meta.schema,
        jobs_iter=pipeline._iter_jobs(),
        process_func=_process_cif_load,
        max_workers=settings.rdb.get_workers(),
        limit=limit,
        logger=logger,
    )

    return results
