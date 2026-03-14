"""Schema command - inspect SQLAlchemy model definitions."""

import dataclasses
import json
from dataclasses import asdict, dataclass

from rich.console import Console
from rich.table import Table as RichTable

from pdbminebuilder.models import ALL_METADATA, get_metadata


@dataclass(frozen=True)
class SchemaInfo:
    """Summary info for a schema."""

    name: str
    table_count: int
    entry_pk: str | None


@dataclass(frozen=True)
class TableInfo:
    """Summary info for a table."""

    name: str
    column_count: int
    has_primary_key: bool


@dataclass(frozen=True)
class ColumnDetail:
    """Detailed info for a column."""

    name: str
    type_str: str
    nullable: bool
    primary_key: bool
    comment: str | None


def _type_to_str(col_type: object) -> str:
    """Convert SQLAlchemy column type to readable string."""
    type_str = str(col_type)
    return type_str.replace("()", "")


def list_schemas() -> list[SchemaInfo]:
    """List all registered schemas with summary info."""
    result = []
    for name in sorted(ALL_METADATA):
        meta = ALL_METADATA[name]
        entry_pk = meta.info.get("entry_pk") if meta.info else None
        result.append(
            SchemaInfo(
                name=name,
                table_count=len(meta.tables),
                entry_pk=entry_pk,
            )
        )
    return result


def list_tables(schema_name: str) -> list[TableInfo]:
    """List all tables in a schema."""
    meta = get_metadata(schema_name)
    result = []
    for table in meta.sorted_tables:
        result.append(
            TableInfo(
                name=table.name,
                column_count=len(table.columns),
                has_primary_key=len(table.primary_key.columns) > 0,
            )
        )
    return result


def describe_table(schema_name: str, table_name: str) -> list[ColumnDetail]:
    """Describe all columns in a table."""
    meta = get_metadata(schema_name)
    full_name = f"{meta.schema}.{table_name}"
    table = meta.tables.get(full_name)
    if table is None:
        available = [t.name for t in meta.sorted_tables]
        raise KeyError(
            f"Table {table_name!r} not found in schema {schema_name!r}. "
            f"Available: {', '.join(available)}"
        )

    pk_cols = {col.name for col in table.primary_key.columns}
    result = []
    for col in table.columns:
        result.append(
            ColumnDetail(
                name=col.name,
                type_str=_type_to_str(col.type),
                nullable=col.nullable if col.nullable is not None else True,
                primary_key=col.name in pk_cols,
                comment=col.comment,
            )
        )
    return result


def describe_column(
    schema_name: str, table_name: str, column_name: str
) -> ColumnDetail:
    """Describe a single column in detail."""
    columns = describe_table(schema_name, table_name)
    for col in columns:
        if col.name == column_name:
            return col
    available = [c.name for c in columns]
    raise KeyError(
        f"Column {column_name!r} not found in {schema_name}.{table_name}. "
        f"Available: {', '.join(available)}"
    )


@dataclass(frozen=True)
class SearchResult:
    """A column matching a search query."""

    schema: str
    table: str
    column: str
    type_str: str
    comment: str | None


def describe_schema_full(schema_name: str) -> dict:
    """Describe all tables and columns in a schema (for JSON output).

    Returns a dict with schema name, entry_pk, and all tables with their columns.
    """
    meta = get_metadata(schema_name)
    entry_pk = meta.info.get("entry_pk") if meta.info else None
    tables = []
    for table in meta.sorted_tables:
        columns = describe_table(schema_name, table.name)
        tables.append({"name": table.name, "columns": [asdict(c) for c in columns]})
    return {"schema": schema_name, "entry_pk": entry_pk, "tables": tables}


def to_json(data: object) -> str:
    """Convert dataclass, list of dataclasses, or dict to JSON string."""
    if isinstance(data, list):
        serializable = [
            asdict(item) if dataclasses.is_dataclass(item) else item for item in data
        ]
    elif dataclasses.is_dataclass(data):
        serializable = asdict(data)
    else:
        serializable = data
    return json.dumps(serializable, ensure_ascii=False, indent=2)


def search_columns(query: str) -> list[SearchResult]:
    """Search column names and comments across all schemas."""
    query_lower = query.lower()
    results = []
    for schema_name in sorted(ALL_METADATA):
        meta = ALL_METADATA[schema_name]
        for table in meta.sorted_tables:
            for col in table.columns:
                name_match = query_lower in col.name.lower()
                comment_match = col.comment and query_lower in col.comment.lower()
                if name_match or comment_match:
                    results.append(
                        SearchResult(
                            schema=schema_name,
                            table=table.name,
                            column=col.name,
                            type_str=_type_to_str(col.type),
                            comment=col.comment,
                        )
                    )
    return results


console = Console()


def _redact_conninfo(conninfo: str) -> str:
    """Redact password from connection string for display."""
    import re

    return re.sub(r"password=\S+", "password=****", conninfo)


def render_schemas(conninfo: str | None = None) -> None:
    """Render schema list with rich."""
    if conninfo:
        console.print(f"[dim]Connection: {_redact_conninfo(conninfo)}[/dim]")
        console.print()

    schemas = list_schemas()
    table = RichTable(title="Schemas")
    table.add_column("Schema", style="cyan")
    table.add_column("Tables", justify="right")
    table.add_column("Entry PK", style="dim")

    for s in schemas:
        table.add_row(s.name, str(s.table_count), s.entry_pk or "-")

    console.print(table)


def render_tables(schema_name: str) -> None:
    """Render table list for a schema."""
    tables = list_tables(schema_name)
    table = RichTable(title=f"Schema: {schema_name} ({len(tables)} tables)")
    table.add_column("Table", style="cyan")
    table.add_column("Columns", justify="right")
    table.add_column("PK", justify="center")

    for t in tables:
        table.add_row(
            t.name,
            str(t.column_count),
            "✓" if t.has_primary_key else "",
        )

    console.print(table)


def render_columns(schema_name: str, table_name: str) -> None:
    """Render column details for a table."""
    columns = describe_table(schema_name, table_name)
    table = RichTable(title=f"{schema_name}.{table_name} ({len(columns)} columns)")
    table.add_column("Column", style="cyan")
    table.add_column("Type")
    table.add_column("Null", justify="center")
    table.add_column("PK", justify="center")
    table.add_column("Comment", style="dim", max_width=60)

    for col in columns:
        table.add_row(
            col.name,
            col.type_str,
            "✓" if col.nullable else "✗",
            "✓" if col.primary_key else "",
            col.comment or "",
        )

    console.print(table)


def render_column_detail(schema_name: str, table_name: str, column_name: str) -> None:
    """Render single column detail (mmcif-dict item style)."""
    col = describe_column(schema_name, table_name, column_name)
    console.print(f"[bold]Column:[/bold] {schema_name}.{table_name}.{col.name}")
    console.print(f"[bold]Type:[/bold] {col.type_str}")
    console.print(f"[bold]Nullable:[/bold] {'yes' if col.nullable else 'no'}")
    console.print(f"[bold]Primary Key:[/bold] {'yes' if col.primary_key else 'no'}")
    if col.comment:
        console.print()
        console.print("[bold]Comment:[/bold]")
        console.print(f"  {col.comment}")


def render_search_results(query: str, results: list[SearchResult]) -> None:
    """Render search results."""
    if not results:
        console.print(f"[dim]No matches for '{query}'.[/dim]")
        return

    table = RichTable(title=f"Search: '{query}' ({len(results)} matches)")
    table.add_column("Schema", style="cyan")
    table.add_column("Table", style="cyan")
    table.add_column("Column", style="bold")
    table.add_column("Type")
    table.add_column("Comment", style="dim", max_width=50)

    for r in results:
        table.add_row(
            r.schema,
            r.table,
            r.column,
            r.type_str,
            r.comment or "",
        )

    console.print(table)
