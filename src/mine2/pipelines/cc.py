"""Chemical Component dictionary pipeline."""

import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.cif import parse_mmjson_file
from mine2.parsers.mmjson import normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


class CcPipeline(BasePipeline):
    """Pipeline for loading Chemical Component dictionary data."""

    name = "cc"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract component ID from filename.

        Handles filenames like: ATP.json.gz -> ATP
        """
        name = filepath.name
        if name.endswith(".json.gz"):
            name = name[:-8]
        return name

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single chemical component."""
        try:
            data = parse_mmjson_file(job.filepath)
            rows_inserted = 0

            # Load all tables from schema
            for table in schema_def.tables:
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

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        comp_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, comp_id, pk_col, normalize_column_name)


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the cc pipeline."""
    pipeline = CcPipeline(settings, config, schema_def)
    return pipeline.run(limit)
