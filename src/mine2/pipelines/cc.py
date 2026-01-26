"""Chemical Component dictionary pipeline."""

import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.mmjson import get_rows, load_mmjson_file, normalize_column_name
from mine2.pipelines.base import BasePipeline

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
            data = load_mmjson_file(job.filepath)
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
        """Transform a category's data.

        Args:
            data: mmJSON data
            table: Table definition from schema
            comp_id: Chemical component ID
            pk_col: Primary key column name (comp_id)
        """
        rows = get_rows(data, table.name)
        if not rows:
            return []

        # Get column names from schema (preserving order)
        schema_columns = [col_name for col_name, _ in table.columns]
        valid_columns = set(schema_columns)

        # First pass: collect all columns that appear in any row
        used_columns = {pk_col}
        for row in rows:
            for col_name in row:
                normalized = normalize_column_name(col_name)
                if normalized in valid_columns:
                    used_columns.add(normalized)

        # Determine final column order (pk first, then schema order)
        final_columns = [pk_col] + [
            c for c in schema_columns if c in used_columns and c != pk_col
        ]

        # Second pass: build rows with consistent columns
        result = []
        for row in rows:
            # Normalize all column names
            normalized_row = {}
            for col_name, value in row.items():
                normalized = normalize_column_name(col_name)
                if normalized in valid_columns:
                    normalized_row[normalized] = value

            # Build row with all final_columns (None for missing)
            transformed_row = {pk_col: comp_id}
            for col in final_columns:
                if col == pk_col:
                    continue
                transformed_row[col] = normalized_row.get(col)

            result.append(transformed_row)
        return result


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the cc pipeline."""
    pipeline = CcPipeline(settings, config, schema_def)
    return pipeline.run(limit)
