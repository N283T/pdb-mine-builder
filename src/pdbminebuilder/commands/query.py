"""Query command - execute SQL and output results."""

import sys
from enum import Enum
from pathlib import Path

import polars as pl
import psycopg
import typer
from rich.console import Console
from rich.table import Table

from pdbminebuilder.config import Settings

console = Console()


class OutputFormat(str, Enum):
    """Output format for query results."""

    table = "table"
    csv = "csv"
    json = "json"
    parquet = "parquet"


def _execute_query(conninfo: str, sql: str) -> pl.DataFrame:
    """Execute SQL and return results as a Polars DataFrame.

    The connection is opened in read-only mode via a READ ONLY transaction
    to prevent accidental destructive operations.
    """
    with psycopg.connect(conninfo) as conn:
        conn.execute("SET TRANSACTION READ ONLY")
        with conn.cursor() as cur:
            cur.execute(sql)
            if cur.description is None:
                return pl.DataFrame()
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
    if not rows:
        return pl.DataFrame(schema={col: pl.String for col in columns})
    return pl.DataFrame(rows, schema=columns, orient="row")


def _render_rich_table(df: pl.DataFrame, max_rows: int | None = None) -> None:
    """Render a Polars DataFrame as a Rich table."""
    if df.is_empty():
        console.print("[dim]No rows returned.[/dim]")
        return

    table = Table(show_lines=False)
    for col in df.columns:
        table.add_column(col, overflow="fold")

    display_df = df.head(max_rows) if max_rows else df
    for row in display_df.iter_rows():
        table.add_row(*[str(v) if v is not None else "" for v in row])

    console.print(table)

    total = len(df)
    displayed = len(display_df)
    if displayed < total:
        console.print(f"[dim]Showing {displayed} of {total} rows.[/dim]")
    else:
        console.print(f"[dim]{total} row(s).[/dim]")


def run_query(
    settings: Settings,
    sql: str,
    *,
    output_format: OutputFormat = OutputFormat.table,
    output_file: Path | None = None,
    max_rows: int | None = None,
) -> None:
    """Execute a SQL query and output results."""
    try:
        df = _execute_query(settings.rdb.constring, sql)
    except psycopg.Error as e:
        console.print(f"[red]Database error: {e}[/red]")
        raise typer.Exit(1) from None

    if output_format == OutputFormat.table:
        _render_rich_table(df, max_rows=max_rows)
        return

    if output_format == OutputFormat.csv:
        if output_file:
            df.write_csv(output_file)
            console.print(f"[dim]Written {len(df)} rows to {output_file}[/dim]")
        else:
            sys.stdout.write(df.write_csv())
        return

    if output_format == OutputFormat.json:
        if output_file:
            df.write_json(output_file)
            console.print(f"[dim]Written {len(df)} rows to {output_file}[/dim]")
        else:
            sys.stdout.write(df.write_json())
            sys.stdout.write("\n")
        return

    if output_format == OutputFormat.parquet:
        if output_file is None:
            console.print("[red]Error: --output is required for parquet format.[/red]")
            raise typer.Exit(1)
        df.write_parquet(output_file)
        console.print(f"[dim]Written {len(df)} rows to {output_file}[/dim]")
