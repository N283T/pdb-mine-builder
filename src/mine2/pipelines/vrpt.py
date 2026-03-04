"""Validation Report pipeline - using gemmi to parse CIF directly."""

import traceback
from pathlib import Path
from typing import Any

import gemmi
from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef
from mine2.parsers.cif import parse_cif_file
from mine2.pipelines.base import BasePipeline, sync_entry_tables, transform_category

console = Console()


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

        jobs = []
        for filepath in gemmi.CifWalk(str(data_dir)):
            if not self._is_validation_file(filepath):
                continue

            entry_id = self.extract_entry_id(filepath)
            jobs.append(Job(entry_id=entry_id, filepath=Path(filepath)))

            if limit and len(jobs) >= limit:
                break

        return jobs

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
            table_rows: dict[str, list[dict[str, Any]]] = {}

            # Generate brief_summary
            brief_rows = self._generate_brief_summary(job.entry_id)
            if brief_rows:
                table_rows["brief_summary"] = brief_rows

            # Load all tables from schema
            for table in schema_def.tables:
                if table.name == "brief_summary":
                    continue  # Already handled

                category_rows = self._transform_category(
                    data, table, job.entry_id, schema_def.primary_key
                )
                if category_rows:
                    table_rows[table.name] = category_rows

            inserted, updated, _deleted = sync_entry_tables(
                conninfo=conninfo,
                schema_def=schema_def,
                entry_id=job.entry_id,
                table_rows=table_rows,
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
) -> list[LoaderResult]:
    """Run the vrpt pipeline."""
    pipeline = VrptPipeline(settings, config, schema_def)
    return pipeline.run(limit)
