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
from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Double,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeEngine

from pdbminebuilder.config import PipelineConfig, Settings
from pdbminebuilder.db.metadata import fetch_entry_mtimes
from pdbminebuilder.db.delta import (
    apply_delta,
    compute_delta,
    entry_exists,
    fetch_entry_data,
    insert_new_entry,
)
from pdbminebuilder.db.loader import (
    Job,
    LoaderResult,
    bulk_insert,
    bulk_upsert,
    delete_missing_entries,
    get_all_tables,
    get_entry_pk,
    run_loader,
)

console = Console()
_default_logger = logging.getLogger("pdbminebuilder.pipelines.base")


# =============================================================================
# Type Coercion Functions
# Ported from original mine2updater rdb-helper.js
# =============================================================================


def _coerce_string(value: Any, is_pk: bool = False) -> Any:
    """Coerce value to string.

    - None -> None (or "" if PK)
    - Array -> join with '-'
    - Other -> str()
    """
    if value is None:
        return "" if is_pk else None
    if isinstance(value, list):
        return "-".join(str(v) for v in value if v is not None)
    return str(value)


def _coerce_integer(value: Any, is_pk: bool = False) -> Any:
    """Coerce value to integer.

    - None -> None (or 0 if PK)
    - Invalid -> None
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

    - true/1/"true" -> True
    - false/0/"false" -> False
    - Other -> None
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
    - < 50 -> 20XX (e.g., 01 -> 2001)
    - >= 50 -> 19XX (e.g., 99 -> 1999)

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


def _coerce_array_by_type(value: Any, item_type: TypeEngine) -> Any:
    """Coerce value to an array of the given item type.

    Args:
        value: The value to coerce.
        item_type: SQLAlchemy type of array elements.

    Returns:
        A list of coerced values, or None.
    """
    if value is None:
        return None
    if not isinstance(value, list):
        value = [value]
    return [coerce_value(v, item_type) if v is not None else None for v in value]


def coerce_value(value: Any, sa_type: TypeEngine, is_pk: bool = False) -> Any:
    """Coerce a value to the appropriate type based on SQLAlchemy type.

    Matches original mine2updater type coercion behavior.

    The isinstance check order matters for subclass relationships:
    - Text before String (Text extends String)
    - BigInteger before Integer (BigInteger extends Integer)
    - Double before Float (Double extends Float)

    Args:
        value: The value to coerce.
        sa_type: The SQLAlchemy type instance.
        is_pk: Whether this column is part of the primary key.

    Returns:
        Coerced value.
    """
    # Array types
    if isinstance(sa_type, ARRAY):
        return _coerce_array_by_type(value, sa_type.item_type)

    # Text before String (Text is a subclass of String)
    if isinstance(sa_type, Text):
        return _coerce_string(value, is_pk)
    if isinstance(sa_type, String):
        return _coerce_string(value, is_pk)

    # BigInteger before Integer
    if isinstance(sa_type, BigInteger):
        return _coerce_bigint(value, is_pk)
    if isinstance(sa_type, Integer):
        return _coerce_integer(value, is_pk)

    # Double before Float
    if isinstance(sa_type, Double):
        return _coerce_float(value, is_pk)
    if isinstance(sa_type, Float):
        return _coerce_float(value, is_pk)

    if isinstance(sa_type, Boolean):
        return _coerce_boolean(value)
    if isinstance(sa_type, Date):
        return _coerce_date(value)
    if isinstance(sa_type, DateTime):
        return _coerce_timestamp(value)
    if isinstance(sa_type, JSONB):
        return value

    # Default: treat as string
    return _coerce_string(value, is_pk)


def transform_category(
    rows: list[dict[str, Any]],
    table: Table,
    pk_value: str,
    pk_col: str,
    normalize_fn: Callable[[str], str] | None = None,
) -> list[dict[str, Any]]:
    """Transform category rows to database rows with consistent column ordering.

    This is a shared transformation function used by multiple pipelines.

    Args:
        rows: List of row dicts from the source data.
        table: SQLAlchemy Table object.
        pk_value: Value for the primary key column (e.g., pdbid, prd_id).
        pk_col: Primary key column name.
        normalize_fn: Optional function to normalize column names
            (for mmJSON bracket notation).

    Returns:
        List of transformed row dicts with consistent column ordering.
    """
    if not rows:
        return []

    # Build column info from SA Table
    column_map = {col.name: col for col in table.columns}
    valid_columns = set(column_map.keys())
    schema_columns = [col.name for col in table.columns]

    # First pass: collect all columns that appear in any row
    used_columns: set[str] = {pk_col}
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
            normalized_row = {
                normalized: v
                for k, v in row.items()
                if (normalized := normalize_fn(k)) in valid_columns
            }
        else:
            normalized_row = {k: v for k, v in row.items() if k in valid_columns}

        # Build row with all final_columns (None for missing)
        transformed_row: dict[str, Any] = {pk_col: pk_value}
        for col in final_columns:
            if col == pk_col:
                continue
            value = normalized_row.get(col)
            col_obj = column_map.get(col)
            if col_obj is not None:
                transformed_row[col] = coerce_value(value, col_obj.type)
            else:
                transformed_row[col] = value

        result.append(transformed_row)

    # Deduplicate by primary key (last occurrence wins, matching upsert semantics).
    # Some source files contain duplicate rows that violate PK constraints.
    pk_columns = [c.name for c in table.primary_key.columns]
    if pk_columns:
        seen: dict[tuple, int] = {}
        for i, row in enumerate(result):
            key = tuple(row.get(c) for c in pk_columns)
            seen[key] = i
        if len(seen) < len(result):
            result = [result[i] for i in sorted(seen.values())]

    return result


def sync_entry_tables(
    conninfo: str,
    meta: MetaData,
    entry_id: str,
    table_rows: dict[str, list[dict[str, Any]]],
) -> tuple[int, int, int]:
    """Synchronize all rows for one entry using delta (insert/update/delete).

    For new entries (not yet in brief_summary), uses a fast-path that
    directly inserts all rows without querying existing data.

    For existing entries, uses delta sync to detect and apply changes,
    preserving original mine2updater behavior where rows removed from
    source files are also removed from the database.

    Args:
        conninfo: Database connection string.
        meta: SQLAlchemy MetaData instance.
        entry_id: The entry identifier.
        table_rows: Dict mapping table names to lists of row dicts.

    Returns:
        Tuple of (inserted_count, updated_count, deleted_count).
    """
    pk_column = get_entry_pk(meta)

    # Fast path: new entry → direct insert (skip delta sync)
    if not entry_exists(conninfo, meta.schema, entry_id, pk_column):
        inserted = insert_new_entry(
            conninfo=conninfo,
            schema=meta.schema,
            entry_id=entry_id,
            pk_column=pk_column,
            table_rows=table_rows,
        )
        return inserted, 0, 0

    # Existing entry: full delta sync (fetch → compare → apply)
    all_tables_list = get_all_tables(meta)
    all_table_names = [t.name for t in all_tables_list]

    # Ensure every schema table is present in new_data so missing categories
    # are interpreted as "delete existing rows for this entry".
    new_data: dict[str, list[dict[str, Any]]] = {name: [] for name in all_table_names}
    for table_name, rows in table_rows.items():
        if table_name in new_data:
            new_data[table_name] = rows

    db_data = fetch_entry_data(
        conninfo=conninfo,
        schema=meta.schema,
        entry_id=entry_id,
        pk_column=pk_column,
        tables=all_table_names,
    )

    table_pk_columns: dict[str, list[str]] = {}
    table_columns: dict[str, list[str]] = {}
    for sa_table in all_tables_list:
        pk_cols = [
            col.name for col in sa_table.primary_key.columns if col.name != pk_column
        ]
        table_pk_columns[sa_table.name] = pk_cols
        table_columns[sa_table.name] = [col.name for col in sa_table.columns]

    delta = compute_delta(
        entry_id=entry_id,
        db_data=db_data,
        new_data=new_data,
        table_pk_columns=table_pk_columns,
        table_columns=table_columns,
    )

    return apply_delta(
        conninfo=conninfo,
        schema=meta.schema,
        entry_id=entry_id,
        pk_column=pk_column,
        delta=delta,
        new_data=new_data,
        db_data=db_data,
        table_pk_columns=table_pk_columns,
    )


def compute_effective_mtime(
    filepath: Path, extra_paths: list[Path | None] | None = None
) -> float:
    """Return max mtime across primary file and optional extra files.

    For pipelines with supplementary files (e.g., pdbj with plus data),
    any file change should trigger reprocessing.

    Args:
        filepath: Primary data file path.
        extra_paths: Optional list of supplementary file paths (None entries skipped).

    Returns:
        Maximum modification time (epoch seconds) across all files.
    """
    mtime = filepath.stat().st_mtime
    if extra_paths:
        for p in extra_paths:
            if p is not None and p.exists():
                mtime = max(mtime, p.stat().st_mtime)
    return mtime


class BasePipeline(ABC):
    """Base class for data loading pipelines."""

    name: str = "base"
    file_pattern: str = "*.json.gz"

    def __init__(
        self,
        settings: Settings,
        config: PipelineConfig,
        meta: MetaData,
        force: bool = False,
    ):
        self.settings = settings
        self.config = config
        self.meta = meta
        self.force = force

    def run(
        self, limit: int | None = None, logger: logging.Logger | None = None
    ) -> list[LoaderResult]:
        """Run the pipeline.

        Args:
            limit: Optional limit on number of files to process.
            logger: Optional logger for file output.

        Returns:
            List of results for each processed entry.
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
            schema_name=self.meta.schema,
            jobs=jobs,
            process_func=self.process_job,
            max_workers=self.settings.rdb.get_workers(),
            logger=logger,
        )

        return results

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find data files and create jobs, skipping unchanged entries."""
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
        for filepath in data_dir.rglob(self.file_pattern):
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
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single job.

        This method runs in a worker process.

        Args:
            job: The job to process.
            schema_name: Schema name for model lookup.
            conninfo: Database connection string.

        Returns:
            Result of processing.
        """
        pass

    def transform_data(self, data: dict[str, Any]) -> dict[str, list[dict]]:
        """Transform parsed data into table rows.

        Override this method for custom transformation logic.

        Args:
            data: Parsed data (mmJSON or CIF format).

        Returns:
            Dict mapping table names to lists of row dicts.
        """
        return {}


class BaseCifBatchPipeline:
    """Base class for CIF batch pipelines (cc, ccmodel, prd, prd_family).

    Provides shared methods for batch upsert, summary output,
    and stale-row pruning. Subclasses must set ``name`` and
    ``meta``, and implement ``_parse_all_blocks()`` and
    ``_find_cif_file()`` / ``_find_cif_files()``.
    """

    name: str = "base-cif-batch"

    def __init__(
        self,
        settings: Settings,
        config: PipelineConfig,
        meta: MetaData,
    ):
        self.settings = settings
        self.config = config
        self.meta = meta

    def _find_cif_file(self) -> Path | None:
        """Find the CIF file for this pipeline. Subclasses must override."""
        raise NotImplementedError

    def _parse_all_blocks(  # noqa: D102
        self,
        blocks: Any,
        max_workers: int,
    ) -> list[tuple[str, dict[str, list[dict]], str | None]]:
        """Parse all blocks in parallel. Subclasses must override."""
        raise NotImplementedError

    def _accumulate_rows(
        self,
        parsed_results: list[tuple[str, dict[str, list[dict]], str | None]],
    ) -> tuple[dict[str, list[dict]], list[LoaderResult]]:
        """Separate parsed results into accumulated table rows and entry results.

        Returns:
            Tuple of (table_rows dict, per-entry LoaderResult list).
        """
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

        return table_rows, results

    def _prepare_table_data(self, rows: list[dict]) -> tuple[list[str], list[tuple]]:
        """Build ordered column list and row tuples from accumulated rows.

        Returns:
            Tuple of (columns, row_tuples).
        """
        all_columns: set[str] = set()
        for row in rows:
            all_columns.update(row.keys())

        pk_col = get_entry_pk(self.meta)
        columns = [pk_col] + sorted(c for c in all_columns if c != pk_col)
        row_tuples = [tuple(r.get(c) for c in columns) for r in rows]
        return columns, row_tuples

    def _batch_insert(
        self,
        parsed_results: list[tuple[str, dict[str, list[dict]], str | None]],
        conninfo: str,
    ) -> list[LoaderResult]:
        """Accumulate rows from parsed blocks and bulk upsert per table."""
        table_rows, results = self._accumulate_rows(parsed_results)

        current_table_name = "<unknown>"
        try:
            for sa_table in track(
                get_all_tables(self.meta),
                description="Upserting...",
                console=console,
            ):
                current_table_name = sa_table.name
                rows = table_rows.get(sa_table.name, [])
                if not rows:
                    continue

                columns, row_tuples = self._prepare_table_data(rows)
                pk_cols_for_table = [c.name for c in sa_table.primary_key.columns]
                bulk_upsert(
                    conninfo,
                    self.meta.schema,
                    sa_table.name,
                    columns,
                    row_tuples,
                    pk_cols_for_table,
                )
                console.print(f"  [dim]{sa_table.name}: {len(rows)} rows[/dim]")
        except Exception as e:
            error_msg = (
                f"Bulk upsert failed on table {current_table_name}: "
                f"{e}\n{traceback.format_exc()}"
            )
            _default_logger.error(error_msg)
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
            schema=self.meta.schema,
            pk_column=get_entry_pk(self.meta),
            tables=[t.name for t in get_all_tables(self.meta)],
            keep_entry_ids=[r.entry_id for r in results],
        )
        console.print(f"  [dim]Pruned stale rows: {deleted}[/dim]")

    def run_load(
        self,
        limit: int | None = None,
        logger: logging.Logger | None = None,
    ) -> list[LoaderResult]:
        """Run the pipeline in load mode (COPY insert, no delta/prune).

        This is the single-CIF-file variant used by cc and ccmodel.
        Subclasses must implement ``_find_cif_file()`` and
        ``_parse_all_blocks()``.

        Pipelines with different file loading (e.g. prd with paired files)
        should override this method.
        """
        import gemmi

        cif_path = self._find_cif_file()
        if not cif_path:
            return []
        console.print(f"  CIF file: {cif_path}")

        console.print("  Loading CIF...")
        doc = gemmi.cif.read(str(cif_path))
        console.print(f"  Found {len(doc)} entries")

        blocks = list(doc)[:limit]
        if limit:
            console.print(f"  Processing {len(blocks)} (limited)")

        max_workers = self.settings.rdb.get_workers()
        conninfo = self.settings.rdb.constring

        console.print("[bold]Phase 1: Parsing blocks...[/bold]")
        parsed_results = self._parse_all_blocks(blocks, max_workers)

        console.print("[bold]Phase 2: COPY inserting...[/bold]")
        results = self._batch_copy_insert(parsed_results, conninfo)

        self._print_summary(results, logger)
        return results

    def _batch_copy_insert(
        self,
        parsed_results: list[tuple[str, dict[str, list[dict]], str | None]],
        conninfo: str,
    ) -> list[LoaderResult]:
        """Accumulate rows from parsed blocks and bulk COPY insert per table.

        Unlike _batch_insert (upsert), this uses COPY protocol for faster
        insertion into already-truncated tables. No conflict handling needed.
        """
        table_rows, results = self._accumulate_rows(parsed_results)

        current_table_name = "<unknown>"
        try:
            for sa_table in track(
                get_all_tables(self.meta),
                description="COPY inserting...",
                console=console,
            ):
                current_table_name = sa_table.name
                rows = table_rows.get(sa_table.name, [])
                if not rows:
                    continue

                columns, row_tuples = self._prepare_table_data(rows)
                bulk_insert(
                    conninfo,
                    self.meta.schema,
                    sa_table.name,
                    columns,
                    row_tuples,
                )
                console.print(f"  [dim]{sa_table.name}: {len(rows)} rows[/dim]")
        except Exception as e:
            error_msg = (
                f"Bulk COPY insert failed on table {current_table_name}: "
                f"{e}\n{traceback.format_exc()}"
            )
            _default_logger.error(error_msg)
            results = [
                LoaderResult(entry_id=r.entry_id, success=False, error=error_msg)
                for r in results
            ]

        return results
