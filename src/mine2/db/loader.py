"""Core data loader with parallel processing support."""

import logging
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    track,
)

from mine2.config import Settings
from mine2.db.connection import get_connection, init_pool

console = Console()
# Default logger (no-op if not configured)
_default_logger = logging.getLogger("mine2.loader")


@dataclass
class TableDef:
    """Table definition from schema YAML."""

    name: str
    columns: list[tuple[str, str]]  # [(column_name, sql_type), ...]
    primary_key: list[str]
    foreign_keys: list[tuple[list[str], str, list[str]]] = field(default_factory=list)
    unique_keys: list[list[str]] = field(default_factory=list)
    indexes: list[str | list[str]] = field(default_factory=list)
    # Cached properties (always computed from columns, not user-provided)
    _column_types: dict[str, str] = field(init=False, default_factory=dict, repr=False)
    _column_names: set[str] = field(init=False, default_factory=set, repr=False)

    def __post_init__(self) -> None:
        """Initialize cached properties from columns."""
        self._column_types = {name: ctype for name, ctype in self.columns}
        self._column_names = set(self._column_types.keys())

    @property
    def column_types(self) -> dict[str, str]:
        """Get column name to type mapping (cached)."""
        return self._column_types

    @property
    def column_names(self) -> set[str]:
        """Get set of valid column names (cached)."""
        return self._column_names


@dataclass
class SchemaDef:
    """Schema definition loaded from YAML."""

    schema_name: str
    primary_key: str
    tables: list[TableDef]
    # Cached table lookup (always computed from tables, not user-provided)
    _table_cache: dict[str, TableDef] = field(
        init=False, default_factory=dict, repr=False
    )

    def __post_init__(self) -> None:
        """Initialize cached properties from tables."""
        self._table_cache = {t.name: t for t in self.tables}

    def get_table(self, name: str) -> TableDef | None:
        """Get table definition by name (O(1) cached lookup)."""
        return self._table_cache.get(name)


def load_schema_def(deffile: Path) -> SchemaDef:
    """Load schema definition from YAML file."""
    with open(deffile) as f:
        raw = yaml.safe_load(f)

    config = raw.get("config", {})
    schema_name = config.get("schema", "public")
    primary_key = config.get("primaryKey", "id")

    tables = []
    for table_raw in raw.get("tables", []):
        table = TableDef(
            name=table_raw["name"],
            columns=[(c[0], c[1]) for c in table_raw.get("columns", [])],
            primary_key=table_raw.get("primary_key", []),
            foreign_keys=[
                (fk[0], fk[1], fk[2]) for fk in table_raw.get("foreign_keys", [])
            ],
            unique_keys=table_raw.get("unique_keys", []),
            indexes=table_raw.get("indexes", []),
        )
        tables.append(table)

    return SchemaDef(
        schema_name=schema_name,
        primary_key=primary_key,
        tables=tables,
    )


def ensure_schema(schema_def: SchemaDef, conninfo: str) -> None:
    """Ensure database schema exists and is up to date."""
    from psycopg import sql

    init_pool(conninfo, min_size=1, max_size=2)

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Create schema if not exists (use sql.Identifier for safety)
            cur.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                    sql.Identifier(schema_def.schema_name)
                )
            )

            # Create tables
            for table in schema_def.tables:
                create_table_if_not_exists(cur, schema_def.schema_name, table)

        conn.commit()

    console.print(f"[green]Schema '{schema_def.schema_name}' ready[/green]")


def create_table_if_not_exists(cur: Any, schema: str, table: TableDef) -> None:
    """Create a table if it doesn't exist."""
    from psycopg import sql

    # PostgreSQL lowercases unquoted identifiers
    table_name_lower = table.name.lower()

    # Check if table exists
    cur.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        )
        """,
        (schema, table_name_lower),
    )
    exists = cur.fetchone()["exists"]

    if exists:
        return

    # Build CREATE TABLE statement using sql module for safety
    columns_sql_parts = []
    for col_name, col_type in table.columns:
        # Column name is identifier, type is SQL literal (validated from schema)
        col_def = sql.SQL("{} {}").format(
            sql.Identifier(col_name),
            sql.SQL(col_type),  # Type comes from trusted schema file
        )
        columns_sql_parts.append(col_def)

    if table.primary_key:
        pk_cols = sql.SQL(", ").join(sql.Identifier(c) for c in table.primary_key)
        columns_sql_parts.append(sql.SQL("PRIMARY KEY ({})").format(pk_cols))

    create_sql = sql.SQL("CREATE TABLE {} ({})").format(
        sql.Identifier(schema, table_name_lower),
        sql.SQL(", ").join(columns_sql_parts),
    )
    cur.execute(create_sql)

    # Create indexes
    for idx in table.indexes:
        if isinstance(idx, list):
            idx_name = f"idx_{table_name_lower}_{'_'.join(idx)}"
            idx_cols = sql.SQL(", ").join(sql.Identifier(c) for c in idx)
        else:
            idx_name = f"idx_{table_name_lower}_{idx}"
            idx_cols = sql.Identifier(idx)

        cur.execute(
            sql.SQL("CREATE INDEX IF NOT EXISTS {} ON {} ({})").format(
                sql.Identifier(idx_name),
                sql.Identifier(schema, table_name_lower),
                idx_cols,
            )
        )

    console.print(f"  Created table: {schema}.{table_name_lower}")


@dataclass
class Job:
    """A single processing job."""

    entry_id: str
    filepath: Path
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class LoaderResult:
    """Result from processing a job."""

    entry_id: str
    success: bool
    rows_inserted: int = 0
    rows_updated: int = 0
    error: str | None = None


@dataclass
class ParsedEntry:
    """Parsed entry data (for chunked processing)."""

    entry_id: str
    table_rows: dict[str, list[dict]]
    error: str | None = None


def run_loader(
    settings: Settings,
    schema_def: SchemaDef,
    jobs: list[Job],
    process_func: Callable[[Job, SchemaDef, str], LoaderResult],
    max_workers: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run loader with parallel processing.

    Args:
        settings: Application settings
        schema_def: Schema definition
        jobs: List of jobs to process
        process_func: Function to process each job
        max_workers: Max worker processes (default from settings)
        logger: Optional logger for file output

    Returns:
        List of results for each job
    """
    if logger is None:
        logger = _default_logger

    if max_workers is None:
        max_workers = settings.rdb.get_workers()

    conninfo = settings.rdb.constring
    results: list[LoaderResult] = []

    console.print(
        f"[bold]Processing {len(jobs)} entries with {max_workers} workers...[/bold]"
    )

    # For small job counts, run sequentially
    if len(jobs) <= 2 or max_workers == 1:
        for job in track(jobs, description="Processing...", console=console):
            result = process_func(job, schema_def, conninfo)
            results.append(result)
    else:
        # Run in parallel
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_job = {
                executor.submit(process_func, job, schema_def, conninfo): job
                for job in jobs
            }

            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Processing", total=len(jobs))

                for future in as_completed(future_to_job):
                    job = future_to_job[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append(
                            LoaderResult(
                                entry_id=job.entry_id,
                                success=False,
                                error=str(e),
                            )
                        )
                    progress.advance(task)

    # Summary
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count

    logger.info(f"Completed: {success_count} succeeded, {fail_count} failed")

    console.print(f"\n[green]✓ {success_count} succeeded[/green]", end="")
    if fail_count > 0:
        console.print(f", [red]✗ {fail_count} failed[/red]")
        # Show first 5 in console
        shown = 0
        for r in results:
            if not r.success and r.error:
                if shown < 5:
                    error_line = r.error.split("\n")[0][:100]
                    console.print(f"  [dim]{r.entry_id}: {error_line}[/dim]")
                    shown += 1
                # Log ALL failures with full error to file
                logger.error(f"FAILED {r.entry_id}:\n{r.error}")
        if fail_count > 5:
            console.print(f"  [dim]... and {fail_count - 5} more (see log file)[/dim]")
    else:
        console.print()

    return results


def run_loader_streaming(
    settings: Settings,
    schema_def: SchemaDef,
    jobs_iter: Iterator[Job],
    process_func: Callable[[Job, SchemaDef, str], LoaderResult],
    max_workers: int | None = None,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run loader with streaming job submission.

    Jobs are submitted immediately as they are discovered, allowing
    scanning and processing to happen in parallel.

    Args:
        settings: Application settings
        schema_def: Schema definition
        jobs_iter: Iterator yielding jobs (e.g., from CifWalk)
        process_func: Function to process each job
        max_workers: Max worker processes (default from settings)
        limit: Optional limit on jobs to process
        logger: Optional logger for file output

    Returns:
        List of results for each job
    """
    if logger is None:
        logger = _default_logger
    if max_workers is None:
        max_workers = settings.rdb.get_workers()

    conninfo = settings.rdb.constring
    results: list[LoaderResult] = []
    futures_to_job: dict[Any, Job] = {}

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit jobs as they come in
        submitted = 0

        if limit:
            # With limit: no progress display, just submit
            for job in jobs_iter:
                future = executor.submit(process_func, job, schema_def, conninfo)
                futures_to_job[future] = job
                submitted += 1
                if submitted >= limit:
                    break
        else:
            # Full scan: submit all jobs (no total known)
            with console.status("[bold]Scanning files..."):
                for job in jobs_iter:
                    future = executor.submit(process_func, job, schema_def, conninfo)
                    futures_to_job[future] = job
                    submitted += 1

        console.print(
            f"[bold]Processing {submitted} entries with {max_workers} workers...[/bold]"
        )

        # Wait for completion with Rich Progress
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing", total=submitted)
            for future in as_completed(futures_to_job):
                job = futures_to_job[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(
                        LoaderResult(
                            entry_id=job.entry_id,
                            success=False,
                            error=str(e),
                        )
                    )
                progress.advance(task)

    # Summary
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count

    logger.info(f"Completed: {success_count} succeeded, {fail_count} failed")

    console.print(f"\n[green]✓ {success_count} succeeded[/green]", end="")
    if fail_count > 0:
        console.print(f", [red]✗ {fail_count} failed[/red]")
        # Show first 5 in console
        shown = 0
        for r in results:
            if not r.success and r.error:
                if shown < 5:
                    # Show truncated error in console
                    error_line = r.error.split("\n")[0][:100]
                    console.print(f"  [dim]{r.entry_id}: {error_line}[/dim]")
                    shown += 1
                # Log ALL failures with full error to file
                logger.error(f"FAILED {r.entry_id}:\n{r.error}")
        if fail_count > 5:
            console.print(f"  [dim]... and {fail_count - 5} more (see log file)[/dim]")
    else:
        console.print()

    return results


def run_loader_chunked(
    settings: Settings,
    schema_def: SchemaDef,
    jobs: list[Job],
    parse_func: Callable[[Job, SchemaDef], ParsedEntry],
    chunk_size: int = 1000,
    max_workers: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run loader with chunked batch insert.

    Workers parse entries and return data (no DB insert).
    Main process accumulates chunks and does batch insert per table.

    Args:
        settings: Application settings
        schema_def: Schema definition
        jobs: List of jobs to process
        parse_func: Function to parse each job (returns ParsedEntry)
        chunk_size: Number of entries per batch insert (default 1000)
        max_workers: Max worker processes (default from settings)
        logger: Optional logger for file output

    Returns:
        List of results for each job
    """
    if logger is None:
        logger = _default_logger

    if max_workers is None:
        max_workers = settings.rdb.get_workers()

    conninfo = settings.rdb.constring
    results: list[LoaderResult] = []

    console.print(
        f"[bold]Processing {len(jobs)} entries "
        f"(chunk_size={chunk_size}, workers={max_workers})...[/bold]"
    )

    # Process in chunks
    total_chunks = (len(jobs) + chunk_size - 1) // chunk_size

    for chunk_idx in range(total_chunks):
        start = chunk_idx * chunk_size
        end = min(start + chunk_size, len(jobs))
        chunk_jobs = jobs[start:end]

        console.print(
            f"[dim]Chunk {chunk_idx + 1}/{total_chunks} "
            f"(entries {start + 1}-{end})[/dim]"
        )

        # Phase 1: Parse all entries in chunk (parallel)
        parsed_entries = _parse_chunk(chunk_jobs, parse_func, schema_def, max_workers)

        # Phase 2: Batch insert per table
        chunk_results = _batch_insert_chunk(parsed_entries, schema_def, conninfo)
        results.extend(chunk_results)

    # Summary
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count

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
                logger.error(f"FAILED {r.entry_id}:\n{r.error}")
        if fail_count > 5:
            console.print(f"  [dim]... and {fail_count - 5} more (see log file)[/dim]")
    else:
        console.print()

    return results


def _parse_chunk(
    jobs: list[Job],
    parse_func: Callable[[Job, SchemaDef], ParsedEntry],
    schema_def: SchemaDef,
    max_workers: int,
) -> list[ParsedEntry]:
    """Parse a chunk of jobs in parallel."""
    if len(jobs) <= 2 or max_workers == 1:
        # Sequential for small chunks
        return [parse_func(job, schema_def) for job in jobs]

    # Parallel parsing
    parsed: list[ParsedEntry] = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {
            executor.submit(parse_func, job, schema_def): job for job in jobs
        }

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Parsing", total=len(jobs))

            for future in as_completed(future_to_job):
                job = future_to_job[future]
                try:
                    result = future.result()
                    parsed.append(result)
                except Exception as e:
                    parsed.append(
                        ParsedEntry(
                            entry_id=job.entry_id,
                            table_rows={},
                            error=str(e),
                        )
                    )
                progress.advance(task)

    return parsed


def _batch_insert_chunk(
    parsed_entries: list[ParsedEntry],
    schema_def: SchemaDef,
    conninfo: str,
) -> list[LoaderResult]:
    """Batch insert parsed entries per table."""
    # Accumulate all rows per table
    table_rows: dict[str, list[dict]] = {}
    results: list[LoaderResult] = []

    for entry in parsed_entries:
        if entry.error:
            results.append(
                LoaderResult(entry_id=entry.entry_id, success=False, error=entry.error)
            )
            continue

        # Accumulate rows
        for table_name, rows in entry.table_rows.items():
            if table_name not in table_rows:
                table_rows[table_name] = []
            table_rows[table_name].extend(rows)

        results.append(
            LoaderResult(entry_id=entry.entry_id, success=True, rows_inserted=0)
        )

    # Bulk insert per table
    try:
        for table in track(
            schema_def.tables, description="Inserting...", console=console
        ):
            rows = table_rows.get(table.name, [])
            if not rows:
                continue

            # Collect all unique columns across all rows
            all_columns: set[str] = set()
            for row in rows:
                all_columns.update(row.keys())

            # Sort columns for consistent ordering (PK column first)
            pk_col = schema_def.primary_key
            columns = [pk_col] + sorted(c for c in all_columns if c != pk_col)

            # Build tuples with None for missing columns
            row_tuples = [tuple(r.get(c) for c in columns) for r in rows]

            bulk_upsert(
                conninfo,
                schema_def.schema_name,
                table.name,
                columns,
                row_tuples,
                table.primary_key,
            )
    except Exception as e:
        # Mark all successful results as failed
        error_msg = str(e)
        results = [
            LoaderResult(entry_id=r.entry_id, success=False, error=error_msg)
            if r.success
            else r
            for r in results
        ]

    return results


def bulk_insert(
    conninfo: str,
    schema: str,
    table: str,
    columns: list[str],
    rows: list[tuple],
) -> int:
    """Bulk insert rows into a table.

    Uses psycopg's copy for efficient insertion.

    Returns:
        Number of rows inserted
    """
    if not rows:
        return 0

    import psycopg
    from psycopg import sql

    full_table = sql.Identifier(schema, table)
    col_names = sql.SQL(", ").join(sql.Identifier(c) for c in columns)

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            # Use COPY for bulk insert
            with cur.copy(
                sql.SQL("COPY {} ({}) FROM STDIN").format(full_table, col_names)
            ) as copy:
                for row in rows:
                    copy.write_row(row)
        conn.commit()

    return len(rows)


def bulk_upsert(
    conninfo: str,
    schema: str,
    table: str,
    columns: list[str],
    rows: list[tuple],
    conflict_columns: list[str],
) -> tuple[int, int]:
    """Bulk upsert (insert or update) rows.

    Returns:
        Tuple of (inserted_count, updated_count)
    """
    if not rows:
        return 0, 0

    import psycopg
    from psycopg import sql

    # PostgreSQL lowercases unquoted identifiers, match table creation
    table_lower = table.lower()
    full_table = sql.Identifier(schema, table_lower)
    col_names = sql.SQL(", ").join(sql.Identifier(c) for c in columns)
    placeholders = sql.SQL(", ").join(sql.Placeholder() * len(columns))
    conflict_cols = sql.SQL(", ").join(sql.Identifier(c) for c in conflict_columns)

    # Build update clause for non-conflict columns
    update_cols = [c for c in columns if c not in conflict_columns]

    if update_cols:
        # Normal upsert with update clause
        update_clause = sql.SQL(", ").join(
            sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(c), sql.Identifier(c))
            for c in update_cols
        )
        query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO UPDATE SET {}"
        ).format(full_table, col_names, placeholders, conflict_cols, update_clause)
    else:
        # All columns are primary key - use DO NOTHING to skip duplicates
        query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO NOTHING"
        ).format(full_table, col_names, placeholders, conflict_cols)

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.executemany(query, rows)
        conn.commit()

    # Note: This doesn't accurately track insert vs update counts
    return len(rows), 0
