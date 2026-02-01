"""Stats command - show database statistics."""

from dataclasses import dataclass
from datetime import date, datetime

import psycopg
from psycopg import sql
from rich.console import Console
from rich.table import Table

from mine2.config import Settings

console = Console()

# Known schemas
KNOWN_SCHEMAS = [
    "pdbj",
    "cc",
    "ccmodel",
    "prd",
    "vrpt",
    "contacts",
    "sifts",
    "emdb",
    "ihm",
]


@dataclass
class SchemaStats:
    """Statistics for a single schema."""

    schema: str
    table_count: int
    row_count: int
    last_updated: datetime | None


def _schema_exists(cur: psycopg.Cursor, schema: str) -> bool:
    """Check if a schema exists."""
    cur.execute(
        "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = %s)",
        (schema,),
    )
    result = cur.fetchone()
    return result[0] if result else False


def _get_table_count(cur: psycopg.Cursor, schema: str) -> int:
    """Get the number of tables in a schema."""
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s",
        (schema,),
    )
    result = cur.fetchone()
    return result[0] if result else 0


def _get_row_count(cur: psycopg.Cursor, schema: str) -> int:
    """Get the total row count for all tables in a schema using pg_stat_user_tables."""
    cur.execute(
        "SELECT COALESCE(SUM(n_live_tup), 0) FROM pg_stat_user_tables WHERE schemaname = %s",
        (schema,),
    )
    result = cur.fetchone()
    return int(result[0]) if result else 0


def _get_last_updated(cur: psycopg.Cursor, schema: str) -> datetime | None:
    """Get the last update timestamp from brief_summary table if it exists."""
    # Check if brief_summary table exists
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'brief_summary'
        )
        """,
        (schema,),
    )
    result = cur.fetchone()
    if not result or not result[0]:
        return None

    # Check if modification_date column exists
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = %s AND table_name = 'brief_summary' AND column_name = 'modification_date'
        )
        """,
        (schema,),
    )
    result = cur.fetchone()
    if not result or not result[0]:
        return None

    # Get max modification_date
    cur.execute(
        sql.SQL("SELECT MAX(modification_date) FROM {}.{}").format(
            sql.Identifier(schema), sql.Identifier("brief_summary")
        )
    )
    result = cur.fetchone()
    if result and result[0]:
        val = result[0]
        if isinstance(val, datetime):
            return val
        # Handle date type (convert to datetime)
        if isinstance(val, date):
            return datetime.combine(val, datetime.min.time())
        # Handle date string
        if isinstance(val, str):
            try:
                return datetime.fromisoformat(val)
            except ValueError:
                return None
    return None


def run_stats(settings: Settings) -> None:
    """Display database statistics.

    Args:
        settings: Application settings
    """
    stats_list: list[SchemaStats] = []
    empty_schemas: list[str] = []

    with psycopg.connect(settings.rdb.constring) as conn:
        with conn.cursor() as cur:
            for schema in KNOWN_SCHEMAS:
                if not _schema_exists(cur, schema):
                    empty_schemas.append(schema)
                    continue

                table_count = _get_table_count(cur, schema)
                if table_count == 0:
                    empty_schemas.append(schema)
                    continue

                row_count = _get_row_count(cur, schema)
                last_updated = _get_last_updated(cur, schema)
                stats_list.append(
                    SchemaStats(
                        schema=schema,
                        table_count=table_count,
                        row_count=row_count,
                        last_updated=last_updated,
                    )
                )

    # Create table
    table = Table(title="Database Statistics")
    table.add_column("Schema", style="cyan")
    table.add_column("Tables", justify="right")
    table.add_column("Rows", justify="right")
    table.add_column("Last Updated", style="dim")

    total_tables = 0
    total_rows = 0

    for s in stats_list:
        total_tables += s.table_count
        total_rows += s.row_count
        last_updated_str = (
            s.last_updated.strftime("%Y-%m-%d %H:%M:%S") if s.last_updated else "-"
        )
        table.add_row(
            s.schema,
            str(s.table_count),
            f"{s.row_count:,}",
            last_updated_str,
        )

    # Add empty schemas section if any
    if empty_schemas:
        table.add_row("", "", "", "", style="dim")
        table.add_row("[dim](empty)[/dim]", "", "", "", style="dim")
        for schema in empty_schemas:
            table.add_row(
                f"  {schema}",
                "0",
                "0",
                "-",
                style="dim",
            )

    console.print()
    console.print(table)
    console.print()
    console.print(
        f"[bold]Total:[/bold] {len(stats_list)} schemas, {total_tables} tables, {total_rows:,} rows"
    )
