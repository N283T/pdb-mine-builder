#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""One-time converter: YAML schema definitions to SQLAlchemy Table definitions.

Originally used to generate src/mine2/models/*.py from schemas/*.def.yml files.
The YAML files have been removed; models are now the source of truth.
Kept for reference in case similar conversions are needed.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Type mapping from YAML SQL types to SQLAlchemy expressions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SAType:
    """Represents a SQLAlchemy type expression and its required imports."""

    expression: str
    imports: frozenset[str] = frozenset()
    pg_imports: frozenset[str] = frozenset()
    info: dict[str, Any] = field(default_factory=dict)


def _parse_yaml_type(yaml_type: str) -> SAType:
    """Map a YAML SQL type string to a SAType descriptor.

    Args:
        yaml_type: The SQL type string from the YAML schema (e.g. "text",
            "integer[]", "timestamp with time zone", "char(10)").

    Returns:
        SAType with the expression string, required imports, and optional info.
    """
    # Array types: "text[]", "integer[]", "double precision[]", "boolean[]"
    if yaml_type.endswith("[]"):
        base_type = yaml_type[:-2]
        inner = _parse_yaml_type(base_type)
        return SAType(
            expression=f"ARRAY({inner.expression})",
            imports=frozenset({"ARRAY"}) | inner.imports,
            pg_imports=inner.pg_imports,
        )

    # char(N) -> String(N)
    char_match = re.match(r"char\((\d+)\)", yaml_type)
    if char_match:
        length = char_match.group(1)
        return SAType(expression=f"String({length})", imports=frozenset({"String"}))

    # Simple type lookup
    type_map: dict[str, SAType] = {
        "text": SAType(expression="Text", imports=frozenset({"Text"})),
        "integer": SAType(expression="Integer", imports=frozenset({"Integer"})),
        "bigint": SAType(expression="BigInteger", imports=frozenset({"BigInteger"})),
        "double precision": SAType(expression="Double", imports=frozenset({"Double"})),
        "real": SAType(expression="Float", imports=frozenset({"Float"})),
        "date": SAType(expression="Date", imports=frozenset({"Date"})),
        "timestamp without time zone": SAType(
            expression="DateTime", imports=frozenset({"DateTime"})
        ),
        "timestamp with time zone": SAType(
            expression="DateTime(timezone=True)",
            imports=frozenset({"DateTime"}),
        ),
        "boolean": SAType(expression="Boolean", imports=frozenset({"Boolean"})),
        "jsonb": SAType(expression="JSONB", pg_imports=frozenset({"JSONB"})),
        "citext": SAType(
            expression="Text",
            imports=frozenset({"Text"}),
            info={"citext": True},
        ),
    }

    result = type_map.get(yaml_type)
    if result is None:
        msg = f"Unknown YAML type: {yaml_type!r}"
        raise ValueError(msg)
    return result


# ---------------------------------------------------------------------------
# YAML schema parsing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ColumnDef:
    """A column definition extracted from YAML."""

    name: str
    yaml_type: str
    nullable: bool


@dataclass(frozen=True)
class TableDef:
    """A table definition extracted from YAML."""

    name: str
    columns: tuple[ColumnDef, ...]
    primary_key: tuple[str, ...]
    foreign_keys: list[Any]
    unique_keys: list[list[str]]
    indexes: list[Any]
    keywords: list[str]
    pkout: bool


@dataclass(frozen=True)
class SchemaDef:
    """A full schema definition extracted from YAML."""

    schema_name: str
    entry_pk: str
    skip_foreign_keys: bool
    skip_keywords: list[str]
    type_overwrites: dict[str, str]
    tables: tuple[TableDef, ...]
    source_filename: str


def _parse_column(raw: list[Any]) -> ColumnDef:
    """Parse a single column definition from YAML.

    Columns come in two forms:
        - [name, type, null]   (3-element with explicit nullable marker)
        - [name, type]         (2-element, still nullable=True per spec)
    """
    name = str(raw[0])
    yaml_type = str(raw[1])
    # All columns are nullable=True per project convention
    nullable = True
    return ColumnDef(name=name, yaml_type=yaml_type, nullable=nullable)


def _parse_table(raw: dict[str, Any]) -> TableDef:
    """Parse a single table definition from YAML."""
    name = raw["name"]
    columns = tuple(_parse_column(col) for col in raw.get("columns", []))
    primary_key = tuple(raw.get("primary_key", []))
    foreign_keys = raw.get("foreign_keys", [])
    unique_keys = raw.get("unique_keys", [])
    # Normalize unique_keys: could be list of lists or empty
    if unique_keys is None:
        unique_keys = []
    indexes = raw.get("indexes", [])
    if indexes is None:
        indexes = []
    keywords = raw.get("keywords", [])
    if keywords is None:
        keywords = []
    pkout = raw.get("pkout", False)

    return TableDef(
        name=name,
        columns=columns,
        primary_key=primary_key,
        foreign_keys=foreign_keys,
        unique_keys=unique_keys,
        indexes=indexes,
        keywords=keywords,
        pkout=pkout,
    )


def _parse_schema(filepath: Path) -> SchemaDef:
    """Parse a complete YAML schema file into a SchemaDef."""
    with filepath.open("r") as f:
        data = yaml.safe_load(f)

    config = data.get("config", {})
    schema_name = config.get("schema", "")
    entry_pk = config.get("primaryKey", "")
    skip_foreign_keys = config.get("skipForeignKeys", False)
    type_overwrites = config.get("type_overwrites", {})
    if type_overwrites is None:
        type_overwrites = {}
    skip_keywords = data.get("skip-keywords", [])
    if skip_keywords is None:
        skip_keywords = []

    tables = tuple(_parse_table(table_raw) for table_raw in data.get("tables", []))

    return SchemaDef(
        schema_name=schema_name,
        entry_pk=entry_pk,
        skip_foreign_keys=skip_foreign_keys,
        skip_keywords=skip_keywords,
        type_overwrites=type_overwrites,
        tables=tables,
        source_filename=filepath.name,
    )


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------


def _sanitize_identifier(name: str) -> str:
    """Convert a table name to a valid Python identifier.

    Replaces hyphens and other non-alphanumeric chars with underscores.
    Prepends underscore if the name starts with a digit.
    """
    result = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if result and result[0].isdigit():
        result = f"_{result}"
    return result


def _apply_type_overwrites(
    schema: SchemaDef,
) -> tuple[TableDef, ...]:
    """Return tables with type_overwrites applied to column types.

    Creates new TableDef/ColumnDef instances (immutable pattern).
    """
    if not schema.type_overwrites:
        return schema.tables

    new_tables = []
    for table in schema.tables:
        new_columns = []
        for col in table.columns:
            overwrite_key = f"{table.name}.{col.name}"
            overwritten_type = schema.type_overwrites.get(overwrite_key, col.yaml_type)
            new_columns.append(
                ColumnDef(
                    name=col.name,
                    yaml_type=overwritten_type,
                    nullable=col.nullable,
                )
            )
        new_tables.append(
            TableDef(
                name=table.name,
                columns=tuple(new_columns),
                primary_key=table.primary_key,
                foreign_keys=table.foreign_keys,
                unique_keys=table.unique_keys,
                indexes=table.indexes,
                keywords=table.keywords,
                pkout=table.pkout,
            )
        )
    return tuple(new_tables)


def _format_foreign_key_comment(fk: list[Any]) -> str:
    """Format a foreign key definition as a Python comment.

    FK format in YAML: [[source_cols...], target_table, [target_cols...]]
    """
    if not fk or len(fk) < 3:
        return ""
    source_cols = fk[0]
    target_table = fk[1]
    target_cols = fk[2]
    return (
        f"    # FK: ({', '.join(str(c) for c in source_cols)}) -> "
        f"{target_table}({', '.join(str(c) for c in target_cols)})"
    )


def _generate_unique_constraint_name(
    schema_name: str,
    table_name: str,
    cols: list[str],
) -> str:
    """Generate a deterministic name for a UniqueConstraint."""
    col_part = "_".join(cols)
    return f"uq_{schema_name}_{table_name}_{col_part}"


def _generate_index_name(
    schema_name: str,
    table_name: str,
    cols: list[str],
) -> str:
    """Generate a deterministic name for an Index."""
    col_part = "_".join(cols)
    return f"ix_{schema_name}_{table_name}_{col_part}"


def _generate_table_code(
    table: TableDef,
    schema_name: str,
) -> tuple[str, set[str], set[str]]:
    """Generate SQLAlchemy Table definition code for a single table.

    Args:
        table: The parsed table definition.
        schema_name: The PostgreSQL schema name.

    Returns:
        Tuple of (code_string, sa_imports_needed, pg_imports_needed).
    """
    sa_imports: set[str] = {"Column", "Table"}
    pg_imports: set[str] = set()
    lines: list[str] = []
    var_name = _sanitize_identifier(table.name)

    lines.append(f"{var_name} = Table(")
    lines.append(f'    "{table.name}",')
    lines.append("    metadata,")

    # Columns
    for col in table.columns:
        sa_type = _parse_yaml_type(col.yaml_type)
        sa_imports.update(sa_type.imports)
        pg_imports.update(sa_type.pg_imports)

        info_parts: dict[str, Any] = {}
        if sa_type.info:
            info_parts.update(sa_type.info)

        if info_parts:
            info_str = ", info=" + repr(info_parts)
        else:
            info_str = ""

        lines.append(
            f'    Column("{col.name}", {sa_type.expression}, nullable=True{info_str}),'
        )

    # PrimaryKeyConstraint
    if table.primary_key:
        sa_imports.add("PrimaryKeyConstraint")
        pk_cols = ", ".join(f'"{c}"' for c in table.primary_key)
        lines.append(f"    PrimaryKeyConstraint({pk_cols}),")

    # UniqueConstraints
    for uk in table.unique_keys:
        if not uk:
            continue
        sa_imports.add("UniqueConstraint")
        uk_cols = ", ".join(f'"{c}"' for c in uk)
        constraint_name = _generate_unique_constraint_name(schema_name, table.name, uk)
        lines.append(f'    UniqueConstraint({uk_cols}, name="{constraint_name}"),')

    # Indexes
    for idx in table.indexes:
        if not idx:
            continue
        sa_imports.add("Index")
        if isinstance(idx, list):
            idx_cols = idx
        else:
            idx_cols = [str(idx)]
        idx_col_strs = ", ".join(f'"{c}"' for c in idx_cols)
        idx_name = _generate_index_name(schema_name, table.name, idx_cols)
        lines.append(f'    Index("{idx_name}", {idx_col_strs}),')

    # Foreign key comments
    for fk in table.foreign_keys:
        comment = _format_foreign_key_comment(fk)
        if comment:
            lines.append(comment)

    # Table info dict
    table_info: dict[str, Any] = {}
    if table.keywords:
        table_info["keywords"] = table.keywords
    if table.pkout:
        table_info["pkout"] = True

    if table_info:
        # Format info dict across multiple lines for readability
        info_lines = _format_info_dict(table_info, indent=4)
        lines.append(f"    info={info_lines},")

    lines.append(")")
    return "\n".join(lines), sa_imports, pg_imports


def _format_info_dict(info: dict[str, Any], indent: int) -> str:
    """Format a dict literal for code output with proper indentation.

    Args:
        info: Dictionary to format.
        indent: Number of spaces for the base indentation level.

    Returns:
        String representation of the dict suitable for Python source code.
    """
    prefix = " " * indent
    inner_prefix = " " * (indent + 4)

    if len(info) == 1:
        key, value = next(iter(info.items()))
        return "{" + f"{key!r}: {value!r}" + "}"

    parts = ["{"]
    items = list(info.items())
    for key, value in items:
        parts.append(f"{inner_prefix}{key!r}: {value!r},")
    parts.append(f"{prefix}" + "}")
    return "\n".join(parts)


def _generate_file(schema: SchemaDef) -> str:
    """Generate the complete Python source file for a schema.

    Args:
        schema: The parsed schema definition.

    Returns:
        Complete Python source code as a string.
    """
    tables = _apply_type_overwrites(schema)

    # Collect all imports by generating table code first
    all_table_code: list[str] = []
    all_sa_imports: set[str] = {"MetaData"}
    all_pg_imports: set[str] = set()

    for table in tables:
        code, sa_imports, pg_imports = _generate_table_code(table, schema.schema_name)
        all_table_code.append(code)
        all_sa_imports.update(sa_imports)
        all_pg_imports.update(pg_imports)

    # Build file header
    parts: list[str] = []
    parts.append(
        f'"""SQLAlchemy schema definition for {schema.schema_name}.\n'
        f"\n"
        f"Auto-generated from schemas/{schema.source_filename} "
        f"by scripts/convert_yaml_to_sa.py.\n"
        f'"""'
    )
    parts.append("")

    # SA imports (sorted alphabetically)
    sorted_sa = sorted(all_sa_imports)
    if len(sorted_sa) <= 3:
        imports_str = ", ".join(sorted_sa)
        parts.append(f"from sqlalchemy import {imports_str}")
    else:
        parts.append("from sqlalchemy import (")
        for imp in sorted_sa:
            parts.append(f"    {imp},")
        parts.append(")")

    # PostgreSQL dialect imports
    if all_pg_imports:
        sorted_pg = sorted(all_pg_imports)
        if len(sorted_pg) == 1:
            parts.append(f"from sqlalchemy.dialects.postgresql import {sorted_pg[0]}")
        else:
            parts.append("from sqlalchemy.dialects.postgresql import (")
            for imp in sorted_pg:
                parts.append(f"    {imp},")
            parts.append(")")

    parts.append("")

    # Metadata definition
    parts.append(f'metadata = MetaData(schema="{schema.schema_name}")')

    # metadata.info
    metadata_info: dict[str, Any] = {
        "entry_pk": schema.entry_pk,
    }
    if schema.skip_foreign_keys:
        metadata_info["skip_foreign_keys"] = True
    if schema.skip_keywords:
        metadata_info["skip_keywords"] = schema.skip_keywords

    info_lines = _format_metadata_info(metadata_info)
    parts.append(f"metadata.info = {info_lines}")
    parts.append("")

    # Table definitions
    for code in all_table_code:
        parts.append("")
        parts.append(code)

    parts.append("")
    return "\n".join(parts)


def _format_metadata_info(info: dict[str, Any]) -> str:
    """Format metadata.info dict as multi-line Python code.

    Args:
        info: Dictionary for metadata.info.

    Returns:
        String representation of the dict.
    """
    if len(info) == 1:
        key, value = next(iter(info.items()))
        return "{" + f"{key!r}: {value!r}" + "}"

    parts = ["{"]
    for key, value in info.items():
        parts.append(f"    {key!r}: {value!r},")
    parts.append("}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Read all YAML schema files and generate SQLAlchemy model files."""
    project_root = Path(__file__).resolve().parent.parent
    schemas_dir = project_root.joinpath("schemas")
    output_dir = project_root.joinpath("src", "pdbminebuilder", "models")
    output_dir.mkdir(parents=True, exist_ok=True)

    yaml_files = sorted(schemas_dir.glob("*.def.yml"))
    if not yaml_files:
        print(f"No *.def.yml files found in {schemas_dir}", file=sys.stderr)
        sys.exit(1)

    # Create __init__.py if it does not exist
    init_path = output_dir.joinpath("__init__.py")
    if not init_path.exists():
        init_path.write_text('"""SQLAlchemy model definitions (auto-generated)."""\n')

    generated_files: list[str] = []

    for yaml_path in yaml_files:
        print(f"Processing {yaml_path.name}...")
        schema = _parse_schema(yaml_path)

        if not schema.schema_name:
            print(
                f"  WARNING: No schema name found in {yaml_path.name}, skipping.",
                file=sys.stderr,
            )
            continue

        output_filename = f"{schema.schema_name}.py"
        output_path = output_dir.joinpath(output_filename)

        source = _generate_file(schema)
        output_path.write_text(source)

        table_count = len(schema.tables)
        print(f"  -> {output_path.relative_to(project_root)} ({table_count} tables)")
        generated_files.append(output_filename)

    print(f"\nGenerated {len(generated_files)} model files in {output_dir}:")
    for filename in generated_files:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()
