"""Core data loader with parallel processing support."""

import logging
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    track,
)
from sqlalchemy import MetaData, Table

from mine2.config import Settings
from mine2.db.connection import get_connection, init_pool

console = Console()
# Default logger (no-op if not configured)
_default_logger = logging.getLogger("mine2.loader")


# =============================================================================
# MetaData helper functions
# =============================================================================


def get_entry_pk(meta: MetaData) -> str:
    """Get entry-level primary key column name from MetaData.info.

    Args:
        meta: SQLAlchemy MetaData with ``info["entry_pk"]`` set.

    Returns:
        The entry primary key column name (e.g. "pdbid", "comp_id").
    """
    try:
        return meta.info["entry_pk"]
    except KeyError:
        schema = meta.schema or "<unknown>"
        msg = (
            f"MetaData for schema {schema!r} is missing 'entry_pk' in info dict. "
            f"Ensure the model module sets metadata.info = {{'entry_pk': '...'}}"
        )
        raise KeyError(msg) from None


def get_table(meta: MetaData, table_name: str) -> Table:
    """Get Table from MetaData by name.

    Keys in ``MetaData.tables`` use the format ``schema.table_name``
    when a schema is set.

    Args:
        meta: SQLAlchemy MetaData instance.
        table_name: Unqualified table name (e.g. "brief_summary").

    Returns:
        The matching Table object.

    Raises:
        KeyError: If the table is not found.
    """
    key = f"{meta.schema}.{table_name}" if meta.schema else table_name
    try:
        return meta.tables[key]
    except KeyError:
        available = ", ".join(sorted(t.name for t in meta.sorted_tables))
        msg = f"Table {table_name!r} not found in schema {meta.schema!r}. Available: {available}"
        raise KeyError(msg) from None


def get_table_or_none(meta: MetaData, table_name: str) -> Table | None:
    """Get Table from MetaData by name, returning None if not found.

    Args:
        meta: SQLAlchemy MetaData instance.
        table_name: Unqualified table name.

    Returns:
        The matching Table object, or None.
    """
    key = f"{meta.schema}.{table_name}" if meta.schema else table_name
    return meta.tables.get(key)


def get_all_tables(meta: MetaData) -> list[Table]:
    """Get all tables from MetaData in dependency order.

    Args:
        meta: SQLAlchemy MetaData instance.

    Returns:
        List of Table objects sorted by foreign key dependencies.
    """
    return list(meta.sorted_tables)


def get_column_names(table: Table) -> set[str]:
    """Get set of column names for a table.

    Args:
        table: SQLAlchemy Table object.

    Returns:
        Set of column name strings.
    """
    return {col.name for col in table.columns}


# =============================================================================
# Schema creation using SQLAlchemy MetaData.create_all()
# =============================================================================


def _create_engine(conninfo: str) -> Any:
    """Create SQLAlchemy engine from psycopg conninfo string.

    Args:
        conninfo: PostgreSQL connection string in psycopg format
            (e.g. "host=localhost port=5433 dbname=mine2 user=pdbj").

    Returns:
        SQLAlchemy Engine instance.
    """
    from sqlalchemy import create_engine

    return create_engine(
        "postgresql+psycopg://",
        connect_args={"conninfo": conninfo},
    )


def ensure_schema(meta: MetaData, conninfo: str) -> None:
    """Ensure database schema and tables exist.

    Creates the PostgreSQL schema (if set) and all tables defined in the
    MetaData using ``create_all(checkfirst=True)``. Existing tables are
    left untouched.

    Args:
        meta: SQLAlchemy MetaData describing the schema and tables.
        conninfo: PostgreSQL connection string.
    """
    from psycopg import sql as psql

    # Create the PostgreSQL schema using the connection pool
    init_pool(conninfo, min_size=1, max_size=2)
    with get_connection() as conn:
        with conn.cursor() as cur:
            if meta.schema:
                cur.execute(
                    psql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                        psql.Identifier(meta.schema)
                    )
                )
        conn.commit()

    # Create tables using SQLAlchemy engine
    engine = _create_engine(conninfo)
    try:
        meta.create_all(engine, checkfirst=True)
    finally:
        engine.dispose()

    console.print(f"[green]Schema '{meta.schema}' ready[/green]")


# =============================================================================
# Job / Result dataclasses
# =============================================================================


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


# =============================================================================
# Parallel loader functions
# =============================================================================


def run_loader(
    settings: Settings,
    schema_name: str,
    jobs: list[Job],
    process_func: Callable[[Job, str, str], LoaderResult],
    max_workers: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run loader with parallel processing.

    Args:
        settings: Application settings.
        schema_name: Schema name passed to worker functions.
        jobs: List of jobs to process.
        process_func: Function to process each job.  Signature:
            ``(job, schema_name, conninfo) -> LoaderResult``.
        max_workers: Max worker processes (default from settings).
        logger: Optional logger for file output.

    Returns:
        List of results for each job.
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
            result = process_func(job, schema_name, conninfo)
            results.append(result)
    else:
        # Run in parallel
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_job = {
                executor.submit(process_func, job, schema_name, conninfo): job
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
    schema_name: str,
    jobs_iter: Iterator[Job],
    process_func: Callable[[Job, str, str], LoaderResult],
    max_workers: int | None = None,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run loader with streaming job submission.

    Jobs are submitted immediately as they are discovered, allowing
    scanning and processing to happen in parallel.

    Args:
        settings: Application settings.
        schema_name: Schema name passed to worker functions.
        jobs_iter: Iterator yielding jobs (e.g., from CifWalk).
        process_func: Function to process each job.
        max_workers: Max worker processes (default from settings).
        limit: Optional limit on jobs to process.
        logger: Optional logger for file output.

    Returns:
        List of results for each job.
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
                future = executor.submit(process_func, job, schema_name, conninfo)
                futures_to_job[future] = job
                submitted += 1
                if submitted >= limit:
                    break
        else:
            # Full scan: submit all jobs (no total known)
            with console.status("[bold]Scanning files..."):
                for job in jobs_iter:
                    future = executor.submit(process_func, job, schema_name, conninfo)
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


# =============================================================================
# Bulk data operations (string-based, unchanged interface)
# =============================================================================


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


def delete_missing_entries(
    conninfo: str,
    schema: str,
    pk_column: str,
    tables: list[str],
    keep_entry_ids: list[str],
) -> int:
    """Delete rows whose entry id is not in keep_entry_ids.

    This is primarily for full-reload pipelines that parse a single large CIF
    and upsert all rows in bulk. It removes stale rows for entries no longer
    present in source data.

    Args:
        conninfo: PostgreSQL connection string
        schema: Schema name
        pk_column: Entry-id column name (e.g., comp_id/model_id/prd_id)
        tables: Table names to prune
        keep_entry_ids: Entry IDs that must remain

    Returns:
        Total number of rows deleted across tables
    """
    import psycopg
    from psycopg import sql

    total_deleted = 0
    keep_ids = list(dict.fromkeys(keep_entry_ids))

    if not keep_ids:
        _default_logger.warning(
            "delete_missing_entries called with empty keep_entry_ids; "
            "this would delete ALL rows from %s tables",
            len(tables),
        )

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            for table in tables:
                table_lower = table.lower()
                full_table = sql.Identifier(schema, table_lower)
                pk_col = sql.Identifier(pk_column)

                if keep_ids:
                    # Use a temp table for efficient NOT IN filtering
                    cur.execute("CREATE TEMP TABLE _keep_ids (id text) ON COMMIT DROP")
                    with cur.copy("COPY _keep_ids (id) FROM STDIN") as copy:
                        for kid in keep_ids:
                            copy.write_row((kid,))
                    cur.execute(
                        sql.SQL(
                            "DELETE FROM {} WHERE {} NOT IN (SELECT id FROM _keep_ids)"
                        ).format(full_table, pk_col)
                    )
                    cur.execute("DROP TABLE _keep_ids")
                else:
                    cur.execute(sql.SQL("DELETE FROM {}").format(full_table))
                total_deleted += cur.rowcount
        conn.commit()

    return total_deleted
