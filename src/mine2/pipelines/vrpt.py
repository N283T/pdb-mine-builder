"""Validation Report pipeline - using gemmi to parse CIF directly."""

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
    get_entry_pk,
    run_loader_streaming,
)
from mine2.parsers.cif import parse_cif_file
from mine2.db.metadata import fetch_entry_mtimes
from mine2.pipelines.base import (
    BasePipeline,
    compute_effective_mtime,
    sync_entry_tables,
    transform_category,
)

console = Console()
_default_logger = logging.getLogger("mine2.pipelines.vrpt")


class VrptPipeline(BasePipeline):
    """Pipeline for loading Validation Report data.

    Uses gemmi to parse CIF files directly - no JSON conversion needed.

    Directory structure: data/<2-3char>/<pdbid>/<pdbid>_validation.cif.gz

    Note: file_pattern is not defined because this pipeline uses gemmi.CifWalk
    with custom filtering (_is_validation_file) instead of rglob pattern matching.
    CifWalk recursively finds all CIF files and handles .cif.gz automatically.
    """

    name = "vrpt"
    # file_pattern intentionally omitted - using gemmi.CifWalk instead

    def extract_entry_id(self, filepath: Path | str) -> str:
        """Extract PDB ID from validation report filename."""
        # Files are named like: 100d_validation.cif.gz
        name = Path(filepath).name
        # Remove .gz suffix if present
        if name.endswith(".gz"):
            name = name[:-3]
        # Remove .cif suffix
        if name.endswith(".cif"):
            name = name[:-4]
        # Remove _validation suffix
        if name.endswith("_validation"):
            name = name[:-11]
        return name.lower()

    def _is_validation_file(self, filepath: str) -> bool:
        """Check if filepath is a validation report file."""
        name = Path(filepath).name.lower()
        return "_validation.cif" in name

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find validation report files using gemmi.CifWalk.

        Handles nested directory structure:
        data/<2-3char>/<pdbid>/<pdbid>_validation.cif.gz
        """
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        # Fetch stored mtimes for skip optimization
        stored_mtimes: dict[str, float] = {}
        if not self.force:
            try:
                stored_mtimes = fetch_entry_mtimes(
                    self.settings.rdb.constring, self.meta.schema
                )
            except Exception as e:
                _default_logger.warning(
                    "Failed to fetch entry mtimes for %s; "
                    "all entries will be processed: %s",
                    self.meta.schema,
                    e,
                )

        jobs = []
        skipped = 0
        for filepath_str in gemmi.CifWalk(str(data_dir)):
            if not self._is_validation_file(filepath_str):
                continue

            filepath = Path(filepath_str)
            entry_id = self.extract_entry_id(filepath)
            current_mtime = compute_effective_mtime(filepath)

            # Skip unchanged entries
            if not self.force and entry_id in stored_mtimes:
                if current_mtime <= stored_mtimes[entry_id]:
                    skipped += 1
                    continue

            jobs.append(
                Job(
                    entry_id=entry_id,
                    filepath=filepath,
                    extra={"file_mtime": current_mtime},
                )
            )

            if limit and len(jobs) >= limit:
                break

        if skipped > 0:
            console.print(
                f"  [dim]Skipped {skipped} unchanged entries (use --force to reprocess)[/dim]"
            )

        return jobs

    def process_job(
        self,
        job: Job,
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single validation report."""
        try:
            from mine2.models import get_metadata

            meta = get_metadata(schema_name)
            entry_pk = get_entry_pk(meta)

            # Parse CIF directly with gemmi
            data = parse_cif_file(job.filepath)
            table_rows: dict[str, list[dict[str, Any]]] = {}

            # Generate brief_summary
            brief_rows = self._generate_brief_summary(job.entry_id)
            if brief_rows:
                table_rows["brief_summary"] = brief_rows

            # Load all tables from schema
            for table in get_all_tables(meta):
                if table.name == "brief_summary":
                    continue  # Already handled

                category_rows = self._transform_category(
                    data, table, job.entry_id, entry_pk
                )
                if category_rows:
                    table_rows[table.name] = category_rows

            inserted, updated, _deleted = sync_entry_tables(
                conninfo=conninfo,
                meta=meta,
                entry_id=job.entry_id,
                table_rows=table_rows,
            )

            # Record file mtime on success (non-critical)
            file_mtime = (job.extra or {}).get("file_mtime")
            if file_mtime is not None:
                try:
                    from mine2.db.metadata import upsert_entry_mtime

                    upsert_entry_mtime(conninfo, schema_name, job.entry_id, file_mtime)
                except Exception as mtime_err:
                    _default_logger.warning(
                        "Failed to record mtime for %s: %s",
                        job.entry_id,
                        mtime_err,
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

    def _generate_brief_summary(self, pdbid: str) -> list[dict]:
        """Generate brief_summary for the validation report."""
        return [{"pdbid": pdbid}]

    def _transform_category(
        self,
        data: dict[str, Any],
        table: Table,
        pdbid: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a CIF category to database rows."""
        # CIF category name matches table name
        rows = data.get(table.name, [])
        return transform_category(rows, table, pdbid, pk_col)


def run(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    force: bool = False,
) -> list[LoaderResult]:
    """Run the vrpt pipeline."""
    pipeline = VrptPipeline(settings, config, meta, force=force)
    return pipeline.run(limit)


# =============================================================================
# Load mode (COPY protocol, no delta sync)
# =============================================================================


def _build_vrpt_table_rows(
    job: Job,
    meta: MetaData,
) -> dict[str, list[dict[str, Any]]]:
    """Parse CIF and build table_rows dict for a vrpt entry."""
    entry_pk = get_entry_pk(meta)
    data = parse_cif_file(job.filepath)
    table_rows: dict[str, list[dict[str, Any]]] = {}

    # brief_summary
    table_rows["brief_summary"] = [{"pdbid": job.entry_id}]

    # All other tables
    for table in get_all_tables(meta):
        if table.name == "brief_summary":
            continue
        rows = data.get(table.name, [])
        category_rows = transform_category(rows, table, job.entry_id, entry_pk)
        if category_rows:
            table_rows[table.name] = category_rows

    return table_rows


def _process_vrpt_load(
    job: Job,
    schema_name: str,
    conninfo: str,
) -> LoaderResult:
    """Worker: parse CIF -> build table_rows -> bulk_copy_entry."""
    try:
        from mine2.models import get_metadata

        meta = get_metadata(schema_name)
        table_rows = _build_vrpt_table_rows(job, meta)

        inserted = bulk_copy_entry(
            conninfo=conninfo,
            schema=meta.schema,
            entry_id=job.entry_id,
            pk_column=get_entry_pk(meta),
            table_rows=table_rows,
        )

        # Record file mtime on success (non-critical)
        try:
            from mine2.db.metadata import upsert_entry_mtime
            from mine2.pipelines.base import compute_effective_mtime

            file_mtime = compute_effective_mtime(job.filepath)
            upsert_entry_mtime(conninfo, schema_name, job.entry_id, file_mtime)
        except Exception as mtime_err:
            logging.getLogger("mine2.pipelines.vrpt").warning(
                "Failed to record mtime for %s: %s",
                job.entry_id,
                mtime_err,
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
    """Run vrpt pipeline in load mode (COPY, no delta sync)."""
    if logger is None:
        logger = _default_logger

    console.print(f"  Data dir: {config.data}")

    pipeline = VrptPipeline(settings, config, meta)

    data_dir = Path(config.data)
    if not data_dir.exists():
        console.print(f"  [red]Data directory not found: {data_dir}[/red]")
        return []

    def _iter_jobs():
        for filepath in gemmi.CifWalk(str(data_dir)):
            if not pipeline._is_validation_file(filepath):
                continue
            entry_id = pipeline.extract_entry_id(filepath)
            yield Job(entry_id=entry_id, filepath=Path(filepath))

    return run_loader_streaming(
        settings=settings,
        schema_name=meta.schema,
        jobs_iter=_iter_jobs(),
        process_func=_process_vrpt_load,
        max_workers=settings.rdb.get_workers(),
        limit=limit,
        logger=logger,
    )
