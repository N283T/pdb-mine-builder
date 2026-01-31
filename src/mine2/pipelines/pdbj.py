"""PDBj pipeline - main PDB structure data loader."""

import json
import logging
import traceback
from pathlib import Path
from typing import Any

import gemmi
from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import (
    Job,
    LoaderResult,
    ParsedEntry,
    SchemaDef,
    TableDef,
    bulk_upsert,
    run_loader_chunked,
    run_loader_streaming,
)
from mine2.parsers.cif import parse_cif_file, parse_mmjson_file
from mine2.parsers.mmjson import merge_data, normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category
from mine2.utils.assembly import calculate_mw_for_bu, hex_sha256
from mine2.utils.patches import apply_patches

console = Console()
_default_logger = logging.getLogger("mine2.pipelines.pdbj")


# =============================================================================
# Shared helper functions for both mmJSON and CIF pipelines
# =============================================================================


def _load_pdbj_data(
    data: dict[str, Any],
    entry_id: str,
    schema_def: SchemaDef,
    conninfo: str,
    normalize_fn: Any | None = None,
) -> int:
    """Load PDB data into database tables.

    Shared by both PdbjPipeline (mmJSON) and PdbjCifPipeline (CIF).

    Args:
        data: Parsed data dictionary
        entry_id: PDB entry ID
        schema_def: Schema definition with cached table lookups
        conninfo: Database connection string
        normalize_fn: Column name normalizer (for mmJSON) or None (for CIF)

    Returns:
        Number of rows inserted
    """
    rows_inserted = 0

    # Use cached table lookups (O(1) instead of O(n) iteration)
    entry_table = schema_def.get_table("entry")
    entry_pk = entry_table.primary_key if entry_table else [schema_def.primary_key]

    # Load entry table
    entry_rows = _transform_entry(data, entry_id)
    if entry_rows:
        columns = list(entry_rows[0].keys())
        inserted, _ = bulk_upsert(
            conninfo,
            schema_def.schema_name,
            "entry",
            columns,
            [tuple(r[c] for c in columns) for r in entry_rows],
            entry_pk,
        )
        rows_inserted += inserted
    # Free memory after processing
    data.pop("entry", None)

    # Load brief_summary with bu_mw calculation
    brief_table = schema_def.get_table("brief_summary")
    if brief_table:
        brief_rows = _transform_brief_summary(data, brief_table, entry_id, normalize_fn)
        if brief_rows:
            columns = list(brief_rows[0].keys())
            inserted, _ = bulk_upsert(
                conninfo,
                schema_def.schema_name,
                "brief_summary",
                columns,
                [tuple(r[c] for c in columns) for r in brief_rows],
                brief_table.primary_key,
            )
            rows_inserted += inserted
        # Free memory after processing
        data.pop("brief_summary", None)

    # Load other categories
    for table in schema_def.tables:
        if table.name in ("entry", "brief_summary"):
            continue

        rows = data.get(table.name, [])
        if not rows:
            continue

        category_rows = transform_category(rows, table, entry_id, "pdbid", normalize_fn)
        if category_rows:
            columns = list(category_rows[0].keys())
            inserted, _ = bulk_upsert(
                conninfo,
                schema_def.schema_name,
                table.name,
                columns,
                [tuple(r[c] for c in columns) for r in category_rows],
                table.primary_key,
            )
            rows_inserted += inserted

        # Free memory after processing each category
        data.pop(table.name, None)

    return rows_inserted


def _prepare_pdbj_data(
    data: dict[str, Any],
    entry_id: str,
    schema_def: SchemaDef,
    normalize_fn: Any | None = None,
) -> dict[str, list[dict]]:
    """Prepare PDB data for batch insert (no DB operations).

    Same logic as _load_pdbj_data but returns table_rows dict.

    Args:
        data: Parsed data dictionary
        entry_id: PDB entry ID
        schema_def: Schema definition with cached table lookups
        normalize_fn: Column name normalizer (for mmJSON) or None (for CIF)

    Returns:
        Dict of table_name -> list of row dicts
    """
    table_rows: dict[str, list[dict]] = {}

    # Prepare entry table
    entry_rows = _transform_entry(data, entry_id)
    if entry_rows:
        table_rows["entry"] = entry_rows
    data.pop("entry", None)

    # Prepare brief_summary with bu_mw calculation
    brief_table = schema_def.get_table("brief_summary")
    if brief_table:
        brief_rows = _transform_brief_summary(data, brief_table, entry_id, normalize_fn)
        if brief_rows:
            table_rows["brief_summary"] = brief_rows
        data.pop("brief_summary", None)

    # Prepare other categories
    for table in schema_def.tables:
        if table.name in ("entry", "brief_summary"):
            continue

        rows = data.get(table.name, [])
        if not rows:
            continue

        category_rows = transform_category(rows, table, entry_id, "pdbid", normalize_fn)
        if category_rows:
            table_rows[table.name] = category_rows

        data.pop(table.name, None)

    return table_rows


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
    table: TableDef,
    entry_id: str,
    normalize_fn: Any | None = None,
) -> list[dict]:
    """Transform brief_summary with bu_mw calculation.

    Adds bu_mw (biological unit molecular weight) to plus_fields.
    """
    rows = data.get("brief_summary", [])
    result = transform_category(rows, table, entry_id, "pdbid", normalize_fn)

    # Calculate bu_mw and add to plus_fields
    bu_mw = calculate_mw_for_bu(data)
    for row in result:
        existing_plus = row.get("plus_fields")
        if existing_plus:
            try:
                plus_data = json.loads(existing_plus)
            except (json.JSONDecodeError, TypeError):
                plus_data = {}
        else:
            plus_data = {}
        plus_data["bu_mw"] = bu_mw
        row["plus_fields"] = json.dumps(plus_data)

    return result


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
        """Find mmJSON files and pair with plus data if available."""
        data_dir = Path(self.config.data)
        plus_dir = Path(self.config.data_plus) if self.config.data_plus else None

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath in data_dir.rglob(self.file_pattern):
            entry_id = self.extract_entry_id(filepath)

            # Look for plus file: {entry_id}-plus.json.gz
            plus_path = None
            if plus_dir:
                candidate = plus_dir / f"{entry_id}-plus.json.gz"
                if candidate.exists():
                    plus_path = candidate

            jobs.append(
                Job(
                    entry_id=entry_id,
                    filepath=filepath,
                    extra={"plus_path": plus_path},
                )
            )

            if limit and len(jobs) >= limit:
                break
        return jobs

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PDB entry."""
        try:
            # Load main data (row-oriented)
            data = parse_mmjson_file(job.filepath)

            # Merge with plus data if available
            plus_path = job.extra.get("plus_path")
            if plus_path:
                plus_data = parse_mmjson_file(plus_path)
                data = merge_data(data, plus_data)

            # Apply entry-specific patches
            apply_patches(job.entry_id, data)

            # Add hash columns to pdbx_struct_assembly_gen (avoid B-tree index limit)
            if "pdbx_struct_assembly_gen" in data:
                for row in data["pdbx_struct_assembly_gen"]:
                    row["_hash_asym_id_list"] = hex_sha256(row.get("asym_id_list", ""))
                    row["_hash_oper_expression"] = hex_sha256(
                        row.get("oper_expression", "")
                    )

            # Transform and load using cached table lookups
            rows_inserted = _load_pdbj_data(
                data=data,
                entry_id=job.entry_id,
                schema_def=schema_def,
                conninfo=conninfo,
                normalize_fn=normalize_column_name,
            )

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=rows_inserted,
            )

        except Exception as e:
            # Include traceback for debugging
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )


def _parse_pdbj_cif_entry(job: Job, schema_def: SchemaDef) -> ParsedEntry:
    """Parse a single PDB CIF entry for chunked processing.

    This function is called by workers in run_loader_chunked.
    Returns parsed data without DB operations.
    """
    try:
        # Parse CIF file
        data = parse_cif_file(job.filepath)

        # Merge with plus data if available
        plus_path = job.extra.get("plus_path") if job.extra else None
        if plus_path:
            plus_data = parse_mmjson_file(plus_path)
            data = merge_data(data, plus_data)

        # Apply entry-specific patches
        apply_patches(job.entry_id, data)

        # Add hash columns to pdbx_struct_assembly_gen
        if "pdbx_struct_assembly_gen" in data:
            for row in data["pdbx_struct_assembly_gen"]:
                row["_hash_asym_id_list"] = hex_sha256(row.get("asym_id_list", ""))
                row["_hash_oper_expression"] = hex_sha256(
                    row.get("oper_expression", "")
                )

        # Prepare data without DB insert
        table_rows = _prepare_pdbj_data(
            data=data,
            entry_id=job.entry_id,
            schema_def=schema_def,
            normalize_fn=None,  # CIF: no normalization
        )

        return ParsedEntry(
            entry_id=job.entry_id,
            table_rows=table_rows,
        )

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return ParsedEntry(
            entry_id=job.entry_id,
            table_rows={},
            error=error_msg,
        )


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
            schema_def=self.schema_def,
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
        plus_dir = Path(self.config.data_plus) if self.config.data_plus else None

        for filepath_str in gemmi.CifWalk(str(data_dir)):
            filepath = Path(filepath_str)
            entry_id = self.extract_entry_id(filepath)

            plus_path = None
            if plus_dir:
                candidate = plus_dir / f"{entry_id}-plus.json.gz"
                if candidate.exists():
                    plus_path = candidate

            yield Job(
                entry_id=entry_id,
                filepath=filepath,
                extra={"plus_path": plus_path},
            )

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find jobs (not used - streaming via run() instead)."""
        return []

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PDB entry from CIF."""
        try:
            # Parse CIF file (row-oriented, same format as mmJSON)
            data = parse_cif_file(job.filepath)

            # Merge with plus data if available (mmJSON format)
            plus_path = job.extra.get("plus_path") if job.extra else None
            if plus_path:
                plus_data = parse_mmjson_file(plus_path)
                data = merge_data(data, plus_data)

            # Apply entry-specific patches
            apply_patches(job.entry_id, data)

            # Add hash columns to pdbx_struct_assembly_gen (avoid B-tree index limit)
            if "pdbx_struct_assembly_gen" in data:
                for row in data["pdbx_struct_assembly_gen"]:
                    row["_hash_asym_id_list"] = hex_sha256(row.get("asym_id_list", ""))
                    row["_hash_oper_expression"] = hex_sha256(
                        row.get("oper_expression", "")
                    )

            # Transform and load using shared function
            # CIF: no column name normalization (pass None)
            rows_inserted = _load_pdbj_data(
                data=data,
                entry_id=job.entry_id,
                schema_def=schema_def,
                conninfo=conninfo,
                normalize_fn=None,
            )

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=rows_inserted,
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
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the pdbj pipeline (mmJSON version)."""
    if logger is None:
        logger = _default_logger
    pipeline = PdbjPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    chunk_size: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the pdbj-cif pipeline (CIF version).

    Args:
        settings: Application settings
        config: Pipeline configuration
        schema_def: Schema definition
        limit: Optional limit on entries to process
        chunk_size: If provided, use chunked batch insert mode
        logger: Optional logger
    """
    if logger is None:
        logger = _default_logger

    pipeline = PdbjCifPipeline(settings, config, schema_def)

    if chunk_size:
        # Chunked mode: collect jobs first, then process in chunks
        console.print(f"  Data dir: {config.data}")
        console.print(
            f"  [dim]Using chunked batch insert (chunk_size={chunk_size})[/dim]"
        )

        data_dir = Path(config.data)
        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        # Collect jobs from iterator
        jobs = []
        for job in pipeline._iter_jobs():
            jobs.append(job)
            if limit and len(jobs) >= limit:
                break

        if not jobs:
            console.print("  [yellow]No files found[/yellow]")
            return []

        return run_loader_chunked(
            settings=settings,
            schema_def=schema_def,
            jobs=jobs,
            parse_func=_parse_pdbj_cif_entry,
            chunk_size=chunk_size,
            max_workers=settings.rdb.get_workers(),
            logger=logger,
        )
    else:
        # Streaming mode (default)
        return pipeline.run(limit, logger=logger)
