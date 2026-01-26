"""PDBj pipeline - main PDB structure data loader."""

import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.mmjson import (
    get_rows,
    load_mmjson_file,
    merge_mmjson,
    normalize_column_name,
)
from mine2.pipelines.base import BasePipeline

console = Console()


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
        for filepath in sorted(data_dir.rglob(self.file_pattern)):
            entry_id = self.extract_entry_id(filepath)

            # Look for plus file: 100d-plus.json.gz
            plus_path = None
            if plus_dir and plus_dir.exists():
                candidate = plus_dir / f"{entry_id}-plus.json.gz"
                # Validate path is within plus_dir to prevent path traversal
                try:
                    resolved = candidate.resolve()
                    if (
                        resolved.is_relative_to(plus_dir.resolve())
                        and resolved.exists()
                    ):
                        plus_path = candidate
                except (ValueError, OSError):
                    # is_relative_to raises ValueError if not relative
                    pass

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
            # Load main data
            data = load_mmjson_file(job.filepath)

            # Merge with plus data if available
            plus_path = job.extra.get("plus_path")
            if plus_path:
                plus_data = load_mmjson_file(plus_path)
                data = merge_mmjson(data, plus_data)

            # Transform and load
            rows_inserted = 0

            # Get entry table definition for its primary key
            entry_table = next(
                (t for t in schema_def.tables if t.name == "entry"), None
            )
            entry_pk = (
                entry_table.primary_key if entry_table else [schema_def.primary_key]
            )

            # Load entry table
            entry_rows = self._transform_entry(data, job.entry_id)
            if entry_rows:
                # Explicitly order columns to avoid dict ordering assumptions
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

            # Load other categories
            for table in schema_def.tables:
                if table.name == "entry":
                    continue

                category_rows = self._transform_category(data, table, job.entry_id)
                if category_rows:
                    # Explicitly order columns to avoid dict ordering assumptions
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
            # Include traceback for debugging
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )

    def _transform_entry(self, data: dict[str, Any], entry_id: str) -> list[dict]:
        """Transform entry data."""
        rows = get_rows(data, "entry")
        if not rows:
            # Fallback: create minimal entry with both PK columns
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

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        entry_id: str,
    ) -> list[dict]:
        """Transform a category's data.

        Args:
            data: mmJSON data
            table: Table definition from schema
            entry_id: PDB entry ID
        """
        rows = get_rows(data, table.name)
        if not rows:
            return []

        # Get column names from schema (preserving order)
        schema_columns = [col_name for col_name, _ in table.columns]
        valid_columns = set(schema_columns)

        # First pass: collect all columns that appear in any row
        used_columns = {"pdbid"}  # Always include pdbid
        for row in rows:
            for col_name in row:
                normalized = normalize_column_name(col_name)
                if normalized in valid_columns:
                    used_columns.add(normalized)

        # Determine final column order (pdbid first, then schema order)
        final_columns = ["pdbid"] + [c for c in schema_columns if c in used_columns]

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
            transformed_row = {"pdbid": entry_id}
            for col in final_columns:
                if col == "pdbid":
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
    """Run the pdbj pipeline."""
    pipeline = PdbjPipeline(settings, config, schema_def)
    return pipeline.run(limit)
