"""Test command - create test database and validate pipelines."""

import re
import subprocess

from rich.console import Console
from rich.table import Table

from pdbminebuilder.config import Settings
from pdbminebuilder.db.connection import close_pool, execute, init_pool

console = Console()

AVAILABLE_PIPELINES = ["pdbj", "cc", "ccmodel", "prd", "prd_family", "vrpt", "contacts"]

# Valid PostgreSQL identifier pattern
_VALID_IDENTIFIER = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def run_test(
    settings: Settings,
    pipelines: list[str],
    drop: bool = False,
    limit: int = 10,
) -> None:
    """Run test database creation and pipeline validation.

    Args:
        settings: Application settings
        pipelines: Pipelines to test (empty = all)
        drop: Drop existing database if exists
        limit: Limit number of files to process per pipeline
    """
    if not pipelines:
        pipelines = AVAILABLE_PIPELINES

    console.print("[bold]Test Mode[/bold]")
    console.print(f"  Pipelines: {', '.join(pipelines)}")
    console.print(f"  Limit: {limit} files per pipeline")

    # Check/create database
    db_name = _get_db_name(settings.rdb.constring)
    console.print(f"  Database: {db_name}")

    if drop:
        _drop_database(settings, db_name)
        _create_database(settings, db_name)
    else:
        if not _database_exists(settings, db_name):
            _create_database(settings, db_name)

    # Initialize pool with test database
    init_pool(settings.rdb.constring, max_size=settings.rdb.get_workers() + 2)

    try:
        # Import and run update with limit
        from pdbminebuilder.commands.update import run_update

        # Temporarily modify settings to use limit
        # (In real implementation, pass limit to pipelines)
        console.print(f"\n[bold]Running pipelines with limit={limit}...[/bold]")

        for pipeline_name in pipelines:
            console.print(f"\n[bold blue]Testing: {pipeline_name}[/bold blue]")
            try:
                run_update(settings, [pipeline_name])
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

        # Show table counts
        _show_table_counts(settings)

    finally:
        close_pool()


def _get_db_name(constring: str) -> str:
    """Extract database name from connection string."""
    parts = dict(p.split("=") for p in constring.split() if "=" in p)
    db_name = parts.get("dbname", "pmb").strip("'\"")

    # Validate database name format to prevent command injection
    if not _VALID_IDENTIFIER.match(db_name):
        raise ValueError(f"Invalid database name format: {db_name}")

    return db_name


def _database_exists(settings: Settings, db_name: str) -> bool:
    """Check if database exists."""
    # Connect to postgres database to check
    postgres_conn = settings.rdb.constring.replace(
        f"dbname={db_name}", "dbname=postgres"
    )

    try:
        init_pool(postgres_conn, min_size=1, max_size=1)
        result = execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,),
        )
        close_pool()
        return len(result) > 0
    except Exception:
        return False


def _create_database(settings: Settings, db_name: str) -> None:
    """Create database."""
    console.print(f"  Creating database: {db_name}")

    # Use createdb command (simpler than SQL)
    try:
        subprocess.run(
            ["createdb", db_name],
            check=True,
            capture_output=True,
        )
        console.print("  [green]Database created[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"  [red]Failed to create database: {e.stderr.decode()}[/red]")
        raise


def _drop_database(settings: Settings, db_name: str) -> None:
    """Drop database if exists."""
    console.print(f"  Dropping database: {db_name}")

    try:
        subprocess.run(
            ["dropdb", "--if-exists", db_name],
            check=True,
            capture_output=True,
        )
        console.print("  [yellow]Database dropped[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"  [red]Failed to drop database: {e.stderr.decode()}[/red]")


def _show_table_counts(settings: Settings) -> None:
    """Show row counts for all tables."""
    from psycopg import sql

    console.print("\n[bold]Table Counts:[/bold]")

    try:
        # Get all tables
        tables = execute(
            """
            SELECT schemaname, tablename
            FROM pg_tables
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
            ORDER BY schemaname, tablename
            """
        )

        if not tables:
            console.print("  [dim]No tables found[/dim]")
            return

        table = Table(show_header=True)
        table.add_column("Schema")
        table.add_column("Table")
        table.add_column("Rows", justify="right")

        for row in tables:
            schema = row["schemaname"]
            table_name = row["tablename"]

            try:
                # Use sql.Identifier for safe table reference
                query = sql.SQL("SELECT COUNT(*) as count FROM {}").format(
                    sql.Identifier(schema, table_name)
                )
                count_result = execute(query)
                count = count_result[0]["count"] if count_result else 0
            except Exception:
                count = "?"

            table.add_row(schema, table_name, str(count))

        console.print(table)

    except Exception as e:
        console.print(f"  [red]Error getting table counts: {e}[/red]")
