#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "sqlalchemy>=2.0",
# ]
# ///
"""Generate Mermaid ER diagrams from SQLAlchemy Core model definitions.

Produces per-schema Mermaid erDiagram blocks suitable for embedding
in Docusaurus Markdown files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sqlalchemy import Column, MetaData
from sqlalchemy.dialects.postgresql import dialect as pg_dialect

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Schemas with many tables: show only table name + PK column
COMPACT_THRESHOLD = 30

_PG_DIALECT = pg_dialect()

# Mermaid type mapping (simplified)
_TYPE_MAP: dict[str, str] = {
    "text": "text",
    "integer": "int",
    "bigint": "bigint",
    "double precision": "float",
    "real": "float",
    "float": "float",
    "date": "date",
    "timestamp without time zone": "timestamp",
    "boolean": "bool",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mermaid_type(col: Column) -> str:  # type: ignore[type-arg]
    """Return a Mermaid-friendly type string for a SA column."""
    try:
        compiled = str(col.type.compile(dialect=_PG_DIALECT)).lower()
    except Exception:
        compiled = str(col.type).lower()

    # Strip array brackets for display
    base = compiled.replace("[]", "")
    is_array = "[]" in compiled

    result = _TYPE_MAP.get(base, base)
    if is_array:
        result = f"{result}_arr"
    return result


def _sanitize_name(name: str) -> str:
    """Sanitize table/column names for Mermaid compatibility."""
    # Mermaid doesn't allow hyphens or dots in entity names
    return name.replace("-", "_").replace(".", "_")


def _generate_er_diagram(
    schema_name: str,
    meta: MetaData,
    compact: bool = False,
) -> str:
    """Generate a Mermaid erDiagram string for a schema."""
    entry_pk: str = meta.info.get("entry_pk", "")

    # Collect tables
    tables: list[tuple[str, object]] = []
    for full_key, table in meta.tables.items():
        table_name = full_key.split(".", 1)[1] if "." in full_key else full_key
        tables.append((table_name, table))

    # Sort: brief_summary first, then alphabetically
    tables.sort(key=lambda t: (0 if t[0] == "brief_summary" else 1, t[0]))

    lines: list[str] = ["erDiagram"]

    # Add relationships only for non-compact schemas (too many lines overwhelm Mermaid)
    if not compact:
        has_brief_summary = any(t[0] == "brief_summary" for t in tables)
        if has_brief_summary and entry_pk:
            for table_name, table_obj in tables:
                if table_name == "brief_summary":
                    continue
                safe_name = _sanitize_name(table_name)
                has_pk = any(c.name == entry_pk for c in table_obj.columns)
                if has_pk:
                    lines.append(
                        f'    brief_summary ||--o{{ {safe_name} : "{entry_pk}"'
                    )

    # Add table definitions
    for table_name, table_obj in tables:
        safe_name = _sanitize_name(table_name)
        lines.append(f"    {safe_name} {{")

        if compact:
            # Show only PK column
            pk_cols = [c for c in table_obj.columns if c.name == entry_pk]
            for col in pk_cols:
                mtype = _mermaid_type(col)
                lines.append(f"        {mtype} {col.name} PK")
            # Show column count
            total = len(list(table_obj.columns))
            if total > len(pk_cols):
                remaining = total - len(pk_cols)
                lines.append(f'        text ___ "{remaining} more columns"')
        else:
            for col in table_obj.columns:
                mtype = _mermaid_type(col)
                marker = " PK" if col.name == entry_pk else ""
                lines.append(f"        {mtype} {col.name}{marker}")

        lines.append("    }")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point for the ER diagram generator."""
    parser = argparse.ArgumentParser(
        description="Generate Mermaid ER diagrams from SQLAlchemy models."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("website/docs/database"),
        help="Output directory for generated Markdown files (default: website/docs/database/).",
    )
    parser.add_argument(
        "--schemas",
        nargs="*",
        help="Specific schemas to generate (default: all).",
    )
    parser.add_argument(
        "--compact-threshold",
        type=int,
        default=COMPACT_THRESHOLD,
        help=f"Schemas with more tables than this use compact mode (default: {COMPACT_THRESHOLD}).",
    )
    args = parser.parse_args()

    output_dir: Path = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        from pdbminebuilder.models import ALL_METADATA
    except ImportError:
        print(
            "Error: Could not import pdbminebuilder.models. "
            "Run this script from the project root via: "
            "pixi run python scripts/generate_er_diagrams.py",
            file=sys.stderr,
        )
        sys.exit(1)

    schemas = args.schemas or sorted(ALL_METADATA.keys())

    for schema_name in schemas:
        meta = ALL_METADATA.get(schema_name)
        if meta is None:
            print(
                f"Warning: Unknown schema {schema_name!r}, skipping.", file=sys.stderr
            )
            continue

        table_count = len(meta.tables)
        compact = table_count > args.compact_threshold

        mermaid = _generate_er_diagram(schema_name, meta, compact=compact)

        out_path = output_dir.joinpath(f"er-{schema_name}.md")
        content = _build_markdown(schema_name, meta, mermaid, compact)
        out_path.write_text(content, encoding="utf-8")
        mode_label = "compact" if compact else "full"
        print(f"Generated {out_path} ({table_count} tables, {mode_label})")

    print(f"\nDone. {len(schemas)} ER diagram(s) written to {output_dir}")


def _build_markdown(
    schema_name: str,
    meta: MetaData,
    mermaid: str,
    compact: bool,
) -> str:
    """Build the Markdown file content wrapping the Mermaid diagram."""
    entry_pk = meta.info.get("entry_pk", "")
    table_count = len(meta.tables)

    lines = [
        "---",
        f"sidebar_label: ER Diagram",
        f'title: "{schema_name} ER Diagram"',
        "---",
        "",
        f"# {schema_name} ER Diagram",
        "",
        f"- **Primary Key**: `{entry_pk}`",
        f"- **Tables**: {table_count}",
    ]

    if compact:
        lines.append("")
        lines.append(
            ":::note\n"
            "This schema has many tables. The diagram shows table names "
            "and primary key columns only. See the "
            f"[schema reference](./{schema_name}) for full column details.\n"
            ":::"
        )

    lines.extend(
        [
            "",
            "```mermaid",
            mermaid,
            "```",
            "",
        ]
    )

    return "\n".join(lines)


if __name__ == "__main__":
    main()
