"""Base pipeline functionality."""

import logging
import traceback
from abc import ABC, abstractmethod
from collections.abc import Callable
from math import floor, log10
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.progress import track

from mine2.config import PipelineConfig, Settings
from mine2.db.delta import apply_delta, compute_delta, fetch_entry_data
from mine2.db.loader import (
    Job,
    LoaderResult,
    SchemaDef,
    TableDef,
    bulk_upsert,
    delete_missing_entries,
    run_loader,
)

console = Console()
_default_logger = logging.getLogger("mine2.pipelines.base")


# =============================================================================
# Type Coercion Functions
# Ported from original mine2updater rdb-helper.js
# =============================================================================


def _coerce_string(value: Any, is_pk: bool = False) -> Any:
    """Coerce value to string.

    - None → None (or "" if PK)
    - Array → join with '-'
    - Other → str()
    """
    if value is None:
        return "" if is_pk else None
    if isinstance(value, list):
        return "-".join(str(v) for v in value if v is not None)
    return str(value)


def _coerce_string_lc(value: Any) -> Any:
    """Coerce value to lowercase string (for citext columns)."""
    if value is None:
        return None
    if isinstance(value, list):
        return "-".join(str(v) for v in value if v is not None).lower()
    return str(value).lower()


def _coerce_integer(value: Any, is_pk: bool = False) -> Any:
    """Coerce value to integer.

    - None → None (or 0 if PK)
    - Invalid → None
    """
    if value is None:
        return 0 if is_pk else None
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0 if is_pk else None


def _coerce_bigint(value: Any, is_pk: bool = False) -> Any:
    """Coerce value to bigint (same as integer in Python)."""
    return _coerce_integer(value, is_pk)


def _coerce_float(value: Any, is_pk: bool = False) -> Any:
    """Coerce value to float with 15-digit precision.

    Matches original: parseFloat(parseFloat(i).toPrecision(15))
    """
    if value is None:
        return 0.0 if is_pk else None
    try:
        # Python float has ~15-17 significant digits, matching JS toPrecision(15)
        f = float(value)
        # Round to 15 significant figures
        if f == 0:
            return 0.0
        magnitude = floor(log10(abs(f)))
        return round(f, 14 - magnitude)
    except (ValueError, TypeError):
        return 0.0 if is_pk else None


def _coerce_boolean(value: Any) -> Any:
    """Coerce value to boolean.

    - true/1/"true" → True
    - false/0/"false" → False
    - Other → None
    """
    if value is True or value == 1:
        return True
    if value is False or value == 0:
        return False
    if isinstance(value, str):
        lower = value.lower()
        if lower == "true":
            return True
        if lower == "false":
            return False
    return None


def _coerce_date(value: Any) -> Any:
    """Coerce value to date string (YYYY-MM-DD format).

    Handles 2-digit years:
    - < 50 → 20XX (e.g., 01 → 2001)
    - >= 50 → 19XX (e.g., 99 → 1999)

    Zero-pads month and day if needed.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    if not value:
        return None

    parts = value.split("-")
    if len(parts) != 3:
        return value  # Return as-is if not in expected format

    year, month, day = parts

    # Handle 2-digit year
    if len(year) < 4:
        try:
            year_int = int(year)
            if year_int < 50:
                year = "20" + year.zfill(2)
            else:
                year = "19" + year.zfill(2)
        except ValueError:
            pass  # Keep original if not a valid number

    # Zero-pad month and day
    if len(month) < 2:
        month = month.zfill(2)
    if len(day) < 2:
        day = day.zfill(2)

    return f"{year}-{month}-{day}"


def _coerce_timestamp(value: Any) -> Any:
    """Coerce value to timestamp (passthrough)."""
    return value


def _coerce_string_array(value: Any) -> Any:
    """Coerce value to text array.

    - Wrap non-list values in a list
    - Convert elements to strings
    """
    if value is None:
        return None
    if not isinstance(value, list):
        value = [value]
    return [str(v) if v is not None else None for v in value]


def _coerce_integer_array(value: Any) -> Any:
    """Coerce value to integer array."""
    if value is None:
        return None
    if not isinstance(value, list):
        value = [value]
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


def _coerce_boolean_array(value: Any) -> Any:
    """Coerce value to boolean array."""
    if value is None:
        return None
    if not isinstance(value, list):
        value = [value]
    return [_coerce_boolean(v) for v in value]


def _coerce_float_array(value: Any) -> Any:
    """Coerce value to float array."""
    if value is None:
        return None
    if not isinstance(value, list):
        value = [value]
    return [_coerce_float(v) for v in value]


def coerce_value(value: Any, col_type: str, is_pk: bool = False) -> Any:
    """Coerce a value to the appropriate type based on column type.

    Matches original mine2updater type coercion behavior.

    Args:
        value: The value to coerce
        col_type: The column type from schema (e.g., 'text', 'integer', 'date')
        is_pk: Whether this column is part of the primary key

    Returns:
        Coerced value
    """
    # Handle array types
    if col_type.endswith("[]"):
        base_type = col_type[:-2]
        if base_type == "text":
            return _coerce_string_array(value)
        elif base_type == "integer":
            return _coerce_integer_array(value)
        elif base_type == "boolean":
            return _coerce_boolean_array(value)
        elif base_type in ("double precision", "real"):
            return _coerce_float_array(value)
        else:
            # Default to string array for unknown types
            return _coerce_string_array(value)

    # Handle scalar types
    if col_type in ("text", "char(4)"):
        return _coerce_string(value, is_pk)
    elif col_type == "citext":
        return _coerce_string_lc(value)
    elif col_type == "integer":
        return _coerce_integer(value, is_pk)
    elif col_type in ("bigint", "serial", "bigserial"):
        return _coerce_bigint(value, is_pk)
    elif col_type in ("double precision", "real"):
        return _coerce_float(value, is_pk)
    elif col_type == "boolean":
        return _coerce_boolean(value)
    elif col_type == "date":
        return _coerce_date(value)
    elif col_type in ("timestamp without time zone", "timestamp with time zone"):
        return _coerce_timestamp(value)
    else:
        # Default: return as-is
        return value


def _coerce_array_value(value: Any, col_type: str) -> Any:
    """Coerce a value to array type if the column expects an array.

    Matches original mine2updater behavior (enforceStringArray):
    - If the column type ends with '[]' and the value is not a list, wrap it in a list
    - Convert elements to appropriate types

    Args:
        value: The value to coerce
        col_type: The column type from schema (e.g., 'text[]', 'integer[]')

    Returns:
        Coerced value (as list if array column, original otherwise)

    Note:
        This function is kept for backward compatibility.
        New code should use coerce_value() instead.
    """
    if value is None:
        return None

    if not col_type.endswith("[]"):
        return value

    return coerce_value(value, col_type)


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

    # Use cached column info from TableDef (avoids recreating dict each call)
    schema_columns = [col_name for col_name, _ in table.columns]
    column_types = table.column_types  # Cached property
    valid_columns = table.column_names  # Cached property

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
            # Coerce value to appropriate type based on column type
            col_type = column_types.get(col, "text")
            transformed_row[col] = coerce_value(value, col_type)

        result.append(transformed_row)

    return result


def sync_entry_tables(
    conninfo: str,
    schema_def: SchemaDef,
    entry_id: str,
    table_rows: dict[str, list[dict[str, Any]]],
) -> tuple[int, int, int]:
    """Synchronize all rows for one entry using delta (insert/update/delete).

    This preserves original mine2updater behavior where rows removed from
    source files are also removed from the database for the same entry.

    Returns:
        Tuple of (inserted_count, updated_count, deleted_count)
    """
    pk_column = schema_def.primary_key
    table_defs = {t.name: t for t in schema_def.tables}
    all_tables = [t.name for t in schema_def.tables]

    # Ensure every schema table is present in new_data so missing categories
    # are interpreted as "delete existing rows for this entry".
    new_data: dict[str, list[dict[str, Any]]] = {name: [] for name in all_tables}
    for table_name, rows in table_rows.items():
        if table_name in new_data:
            new_data[table_name] = rows

    db_data = fetch_entry_data(
        conninfo=conninfo,
        schema=schema_def.schema_name,
        entry_id=entry_id,
        pk_column=pk_column,
        tables=all_tables,
    )

    table_pk_columns = {
        name: [c for c in tdef.primary_key if c != pk_column]
        for name, tdef in table_defs.items()
    }
    table_columns = {
        name: [col_name for col_name, _ in tdef.columns]
        for name, tdef in table_defs.items()
    }

    delta = compute_delta(
        entry_id=entry_id,
        db_data=db_data,
        new_data=new_data,
        table_pk_columns=table_pk_columns,
        table_columns=table_columns,
    )

    return apply_delta(
        conninfo=conninfo,
        schema=schema_def.schema_name,
        entry_id=entry_id,
        pk_column=pk_column,
        delta=delta,
        new_data=new_data,
        db_data=db_data,
        table_pk_columns=table_pk_columns,
    )


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

    def run(
        self, limit: int | None = None, logger: logging.Logger | None = None
    ) -> list[LoaderResult]:
        """Run the pipeline.

        Args:
            limit: Optional limit on number of files to process
            logger: Optional logger for file output

        Returns:
            List of results for each processed entry
        """
        if logger is None:
            logger = _default_logger

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
            logger=logger,
        )

        return results

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find data files and create jobs."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath in data_dir.rglob(self.file_pattern):
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


class BaseCifBatchPipeline:
    """Base class for CIF batch pipelines (cc, ccmodel, prd).

    Provides shared methods for batch upsert, summary output,
    and stale-row pruning. Subclasses must set ``name`` and
    ``schema_def``, and implement ``_parse_all_blocks()`` and
    ``_find_cif_file()`` / ``_find_cif_files()``.
    """

    name: str = "base-cif-batch"

    def __init__(
        self,
        settings: Settings,
        config: PipelineConfig,
        schema_def: SchemaDef,
    ):
        self.settings = settings
        self.config = config
        self.schema_def = schema_def

    def _batch_insert(
        self,
        parsed_results: list[tuple[str, dict[str, list[dict]], str | None]],
        conninfo: str,
    ) -> list[LoaderResult]:
        """Accumulate rows from parsed blocks and bulk upsert per table."""
        table_rows: dict[str, list[dict]] = {}
        results: list[LoaderResult] = []

        for entry_id, rows_by_table, error in parsed_results:
            if error:
                results.append(
                    LoaderResult(entry_id=entry_id, success=False, error=error)
                )
                continue

            for table_name, rows in rows_by_table.items():
                if table_name not in table_rows:
                    table_rows[table_name] = []
                table_rows[table_name].extend(rows)

            results.append(
                LoaderResult(entry_id=entry_id, success=True, rows_inserted=0)
            )

        # Bulk upsert per table
        try:
            for table in track(
                self.schema_def.tables,
                description="Upserting...",
                console=console,
            ):
                rows = table_rows.get(table.name, [])
                if not rows:
                    continue

                all_columns: set[str] = set()
                for row in rows:
                    all_columns.update(row.keys())

                pk_col = self.schema_def.primary_key
                columns = [pk_col] + sorted(c for c in all_columns if c != pk_col)
                row_tuples = [tuple(r.get(c) for c in columns) for r in rows]

                bulk_upsert(
                    conninfo,
                    self.schema_def.schema_name,
                    table.name,
                    columns,
                    row_tuples,
                    table.primary_key,
                )
                console.print(f"  [dim]{table.name}: {len(rows)} rows[/dim]")
        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            results = [
                LoaderResult(entry_id=r.entry_id, success=False, error=error_msg)
                for r in results
            ]

        return results

    def _print_summary(
        self, results: list[LoaderResult], logger: logging.Logger | None = None
    ) -> None:
        """Print processing summary to console and logger."""
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count

        if logger:
            logger.info(f"Completed: {success_count} succeeded, {fail_count} failed")

        console.print(f"\n[green]✓ {success_count} succeeded[/green]", end="")
        if fail_count > 0:
            console.print(f", [red]✗ {fail_count} failed[/red]")
            shown = 0
            for r in results:
                if not r.success and r.error:
                    if shown < 5:
                        error_line = r.error.split("\n")[0][:100]
                        console.print(f"  [dim]{r.entry_id}: {error_line}[/dim]")
                        shown += 1
                    if logger:
                        logger.error(f"FAILED {r.entry_id}:\n{r.error}")
            if fail_count > 5:
                console.print(
                    f"  [dim]... and {fail_count - 5} more (see log file)[/dim]"
                )
        else:
            console.print()

    def _prune_stale_rows(
        self,
        results: list[LoaderResult],
        conninfo: str,
        limit: int | None,
    ) -> None:
        """Remove stale rows after a full successful reload.

        Skips pruning when:
        - ``limit`` is set (partial run)
        - No entries were processed
        - Any entry failed
        """
        if limit is not None:
            console.print("  [dim]Skipping prune (limited run)[/dim]")
            return

        if not results or not all(r.success for r in results):
            reason = "no entries processed" if not results else "failed entries"
            console.print(f"  [yellow]Skipping prune ({reason})[/yellow]")
            return

        deleted = delete_missing_entries(
            conninfo=conninfo,
            schema=self.schema_def.schema_name,
            pk_column=self.schema_def.primary_key,
            tables=[t.name for t in self.schema_def.tables],
            keep_entry_ids=[r.entry_id for r in results],
        )
        console.print(f"  [dim]Pruned stale rows: {deleted}[/dim]")
