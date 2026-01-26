"""Chemical Component Model pipeline."""

import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, bulk_upsert
from mine2.parsers.mmjson import get_rows, load_mmjson_file, normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


class CcmodelPipeline(BasePipeline):
    """Pipeline for loading Chemical Component Model data."""

    name = "ccmodel"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract model ID from filename.

        Handles filenames like: M_000_00001.json.gz -> M_000_00001
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
        """Process a single component model."""
        try:
            data = load_mmjson_file(job.filepath)
            rows_inserted = 0

            # Generate and load brief_summary
            brief_rows = self._generate_brief_summary(data, job.entry_id)
            if brief_rows:
                columns = list(brief_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "brief_summary",
                    columns,
                    [tuple(r[c] for c in columns) for r in brief_rows],
                    ["model_id"],
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

    def _generate_brief_summary(
        self, data: dict[str, Any], model_id: str
    ) -> list[dict]:
        """Generate brief_summary from pdbx_chem_comp_model data."""
        rows = get_rows(data, "pdbx_chem_comp_model")
        if not rows:
            return [{"model_id": model_id}]

        result = []
        for row in rows:
            result.append(
                {
                    "model_id": model_id,
                    "comp_id": row.get("comp_id"),
                }
            )
        return result

    def _transform_category(
        self,
        data: dict[str, Any],
        table: Any,
        model_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = get_rows(data, table.name)
        return transform_category(rows, table, model_id, pk_col, normalize_column_name)


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the ccmodel pipeline."""
    pipeline = CcmodelPipeline(settings, config, schema_def)
    return pipeline.run(limit)
