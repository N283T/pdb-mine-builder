"""Base pipeline functionality."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, run_loader

console = Console()


def _coerce_array_value(value: Any, col_type: str) -> Any:
    """Coerce a value to array type if the column expects an array.

    Matches original mine2updater behavior (enforceStringArray):
    - If the column type ends with '[]' and the value is not a list, wrap it in a list
    - Convert elements to strings for text[], integers for integer[]

    Args:
        value: The value to coerce
        col_type: The column type from schema (e.g., 'text[]', 'integer[]')

    Returns:
        Coerced value (as list if array column, original otherwise)
    """
    if value is None:
        return None

    if not col_type.endswith("[]"):
        return value

    # Wrap non-list values in a list
    if not isinstance(value, list):
        value = [value]

    # Convert elements based on array type
    if col_type == "text[]":
        return [str(v) if v is not None else None for v in value]
    elif col_type == "integer[]":
        result = []
        for v in value:
            if v is None:
                result.append(None)
            else:
                try:
                    result.append(int(v))
                except (ValueError, TypeError):
                    result.append(None)
        return result

    return value


def transform_category(
    rows: list[dict[str, Any]],
    table: TableDef,
    pk_value: str,
    pk_col: str,
    normalize_fn: Callable[[str], str] | None = None,
) -> list[dict[str, Any]]:
    """Transform category rows to database rows with consistent column ordering.

    This is a shared transformation function used by multiple pipelines.

    Args:
        rows: List of row dicts from the source data
        table: Table definition from schema
        pk_value: Value for the primary key column (e.g., pdbid, prd_id)
        pk_col: Primary key column name
        normalize_fn: Optional function to normalize column names (for mmJSON bracket notation)

    Returns:
        List of transformed row dicts with consistent column ordering
    """
    if not rows:
        return []

    # Get column names and types from schema
    schema_columns = [col_name for col_name, _ in table.columns]
    column_types = {col_name: col_type for col_name, col_type in table.columns}
    valid_columns = set(schema_columns)

    # First pass: collect all columns that appear in any row
    used_columns = {pk_col}
    for row in rows:
        for col_name in row:
            normalized = normalize_fn(col_name) if normalize_fn else col_name
            if normalized in valid_columns:
                used_columns.add(normalized)

    # Determine final column order (pk first, then schema order)
    final_columns = [pk_col] + [
        c for c in schema_columns if c in used_columns and c != pk_col
    ]

    # Second pass: build rows with consistent columns
    result = []
    for row in rows:
        # Normalize all column names if needed
        if normalize_fn:
            normalized_row = {}
            for col_name, value in row.items():
                normalized = normalize_fn(col_name)
                if normalized in valid_columns:
                    normalized_row[normalized] = value
        else:
            normalized_row = {k: v for k, v in row.items() if k in valid_columns}

        # Build row with all final_columns (None for missing)
        transformed_row = {pk_col: pk_value}
        for col in final_columns:
            if col == pk_col:
                continue
            value = normalized_row.get(col)
            # Coerce to array type if needed
            col_type = column_types.get(col, "text")
            transformed_row[col] = _coerce_array_value(value, col_type)

        result.append(transformed_row)

    return result


class BasePipeline(ABC):
    """Base class for data loading pipelines."""

    name: str = "base"
    file_pattern: str = "*.json.gz"

    def __init__(
        self,
        settings: Settings,
        config: PipelineConfig,
        schema_def: SchemaDef,
    ):
        self.settings = settings
        self.config = config
        self.schema_def = schema_def

    def run(self, limit: int | None = None) -> list[LoaderResult]:
        """Run the pipeline.

        Args:
            limit: Optional limit on number of files to process

        Returns:
            List of results for each processed entry
        """
        console.print(f"  Data dir: {self.config.data}")

        # Find data files
        jobs = self.find_jobs(limit)
        console.print(f"  Found {len(jobs)} entries")

        if not jobs:
            console.print("  [yellow]No files to process[/yellow]")
            return []

        # Process jobs
        results = run_loader(
            settings=self.settings,
            schema_def=self.schema_def,
            jobs=jobs,
            process_func=self.process_job,
            max_workers=self.settings.rdb.get_workers(),
        )

        return results

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find data files and create jobs."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath in sorted(data_dir.rglob(self.file_pattern)):
            entry_id = self.extract_entry_id(filepath)
            jobs.append(Job(entry_id=entry_id, filepath=filepath))

            if limit and len(jobs) >= limit:
                break

        return jobs

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract entry ID from filepath."""
        # Default: use filename without extension
        name = filepath.name
        for suffix in [".json.gz", ".json", ".cif.gz", ".cif"]:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
                break
        return name

    @abstractmethod
    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single job.

        This method runs in a worker process.

        Args:
            job: The job to process
            schema_def: Schema definition
            conninfo: Database connection string

        Returns:
            Result of processing
        """
        pass

    def transform_data(self, data: dict[str, Any]) -> dict[str, list[dict]]:
        """Transform parsed data into table rows.

        Override this method for custom transformation logic.

        Args:
            data: Parsed data (mmJSON or CIF format)

        Returns:
            Dict mapping table names to lists of row dicts
        """
        return {}
