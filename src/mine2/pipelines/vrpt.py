"""Validation Report pipeline - using gemmi to parse CIF directly."""

import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, bulk_upsert
from mine2.parsers.cif import parse_cif_file
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


class VrptPipeline(BasePipeline):
    """Pipeline for loading Validation Report data.

    Uses gemmi to parse CIF files directly - no JSON conversion needed.

    Directory structure: data/<2-3char>/<pdbid>/<pdbid>_validation.cif.gz
    """

    name = "vrpt"
    file_pattern = "*_validation.cif.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract PDB ID from validation report filename."""
        # Files are named like: 100d_validation.cif.gz
        name = filepath.stem
        if name.endswith(".cif"):
            name = name[:-4]
        if name.endswith("_validation"):
            name = name[:-11]
        return name.lower()

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find validation report files.

        Handles nested directory structure:
        data/<2-3char>/<pdbid>/<pdbid>_validation.cif.gz
        """
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        # Iterate through hash directories (2-3 char subdirs) for efficiency
        for hash_dir in sorted(data_dir.iterdir()):
            if not hash_dir.is_dir():
                continue
            # Iterate through entry directories
            for entry_dir in sorted(hash_dir.iterdir()):
                if not entry_dir.is_dir():
                    continue
                # Find validation files in entry directory
                for filepath in entry_dir.glob(self.file_pattern):
                    entry_id = self.extract_entry_id(filepath)
                    jobs.append(Job(entry_id=entry_id, filepath=filepath))

                    if limit and len(jobs) >= limit:
                        return jobs

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
        table: Any,
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
