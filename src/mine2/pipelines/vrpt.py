"""Validation Report pipeline - using gemmi to parse CIF directly."""

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
from mine2.parsers.cif import parse_cif_file
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


def _parse_vrpt_entry(job: Job, schema_def: SchemaDef) -> ParsedEntry:
    """Parse a single validation report for chunked processing.

    This function is called by workers in run_loader_chunked.
    Returns parsed data without DB operations.
    """
    try:
        # Parse CIF directly with gemmi
        data = parse_cif_file(job.filepath)
        table_rows: dict[str, list[dict]] = {}

        # brief_summary
        table_rows["brief_summary"] = [{"pdbid": job.entry_id}]

        # Load all tables from schema
        for table in schema_def.tables:
            if table.name == "brief_summary":
                continue  # Already handled

            # CIF category name matches table name
            rows = data.get(table.name, [])
            if not rows:
                continue

            # Transform using base function (CIF: no normalization)
            category_rows = transform_category(
                rows, table, job.entry_id, schema_def.primary_key
            )
            if category_rows:
                table_rows[table.name] = category_rows

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


class VrptPipeline(BasePipeline):
    """Pipeline for loading Validation Report data.

    Uses gemmi to parse CIF files directly - no JSON conversion needed.

    Directory structure: data/<2-3char>/<pdbid>/<pdbid>_validation.cif.gz

    Uses gemmi.CifWalk with streaming job submission for parallel scanning
    and processing.
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

    def run(
        self, limit: int | None = None, logger: logging.Logger | None = None
    ) -> list[LoaderResult]:
        """Run the pipeline with streaming job submission.

        Jobs are submitted to workers immediately as CifWalk discovers files,
        allowing scanning and processing to happen in parallel.
        """
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
        """Yield jobs as CifWalk discovers validation files."""
        data_dir = Path(self.config.data)

        for filepath_str in gemmi.CifWalk(str(data_dir)):
            if self._is_validation_file(filepath_str):
                yield Job(
                    entry_id=self.extract_entry_id(filepath_str),
                    filepath=Path(filepath_str),
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
        """Process a single validation report."""
        try:
            # Parse CIF directly with gemmi
            data = parse_cif_file(job.filepath)
            rows_inserted = 0

            # Generate brief_summary
            brief_rows = self._generate_brief_summary(job.entry_id)
            if brief_rows:
                columns = list(brief_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "brief_summary",
                    columns,
                    [tuple(r[c] for c in columns) for r in brief_rows],
                    ["pdbid"],
                )
                rows_inserted += inserted

            # Load all tables from schema
            for table in schema_def.tables:
                if table.name == "brief_summary":
                    continue  # Already handled

                category_rows = self._transform_category(
                    data, table, job.entry_id, schema_def.primary_key
                )
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

    def _generate_brief_summary(self, pdbid: str) -> list[dict]:
        """Generate brief_summary for the validation report."""
        return [{"pdbid": pdbid}]

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
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
    schema_def: SchemaDef,
    limit: int | None = None,
    chunk_size: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the vrpt pipeline.

    Args:
        settings: Application settings
        config: Pipeline configuration
        schema_def: Schema definition
        limit: Optional limit on entries to process
        chunk_size: If provided, use chunked batch insert mode
        logger: Optional logger
    """
    pipeline = VrptPipeline(settings, config, schema_def)

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
            parse_func=_parse_vrpt_entry,
            chunk_size=chunk_size,
            max_workers=settings.rdb.get_workers(),
            logger=logger,
        )
    else:
        # Streaming mode (default)
        return pipeline.run(limit, logger=logger)
