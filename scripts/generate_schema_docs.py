#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "sqlalchemy>=2.0",
# ]
# ///
"""Generate Markdown documentation for database schemas.

Reads SQLAlchemy Core model definitions and mine2 JSON documentation
to produce per-schema Markdown files suitable for a Docusaurus site.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import Column, MetaData
from sqlalchemy.dialects.postgresql import dialect as pg_dialect

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIDEBAR_POSITIONS: dict[str, int] = {
    "pdbj": 1,
    "cc": 2,
    "ccmodel": 3,
    "prd": 4,
    "prd_family": 5,
    "vrpt": 6,
    "contacts": 7,
    "emdb": 8,
    "ihm": 9,
}

SKIP_JSON_FILES: set[str] = {
    "table-types.json",
    "misc.json",
    "sifts.json",
    "empiar.json",
}

# Mapping from SA schema name to mine2 JSON filename (without extension).
# Only entries that differ need to be listed.
SCHEMA_TO_JSON: dict[str, str] = {
    "prd_family": "prd_family",
}

_PG_DIALECT = pg_dialect()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _column_type_str(col: Column) -> str:  # type: ignore[type-arg]
    """Return a lowercase PostgreSQL type string for a SA column."""
    try:
        compiled = col.type.compile(dialect=_PG_DIALECT)
        return str(compiled).lower()
    except Exception:
        return str(col.type).lower()


def _load_mine2_json(mine2_dir: Path) -> dict[str, dict[str, Any]]:
    """Load all mine2 JSON files, returning a dict keyed by schema name."""
    result: dict[str, dict[str, Any]] = {}
    for json_path in sorted(mine2_dir.glob("*.json")):
        if json_path.name in SKIP_JSON_FILES:
            continue
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        schema_name = json_path.stem
        result[schema_name] = data
    return result


def _build_description_lookup(
    mine2_data: dict[str, Any],
) -> dict[tuple[str, str], str]:
    """Build {(table_name, col_name): description} from mine2 JSON data."""
    lookup: dict[tuple[str, str], str] = {}
    tables: list[dict[str, Any]] = mine2_data.get("tables", [])
    for table_info in tables:
        table_name: str = table_info["name"]
        for col_entry in table_info.get("columns", []):
            col_name = col_entry[0]
            description = col_entry[2] if len(col_entry) > 2 else ""
            # Collapse multi-line descriptions into a single line.
            cleaned = " ".join(description.split())
            lookup[(table_name, col_name)] = cleaned
    return lookup


def _escape_mdx(text: str) -> str:
    """Escape characters that conflict with MDX/Markdown table syntax."""
    text = text.replace("|", "\\|")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("{", "&#123;")
    text = text.replace("}", "&#125;")
    # Escape Markdown link syntax: [text](url)
    text = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1", text)
    # Escape remaining square brackets
    text = text.replace("[", "&#91;")
    text = text.replace("]", "&#93;")
    return text


def _generate_schema_md(
    schema_name: str,
    meta: MetaData,
    desc_lookup: dict[tuple[str, str], str],
) -> str:
    """Generate Markdown content for a single schema."""
    entry_pk: str = meta.info.get("entry_pk", "")
    sidebar_pos = SIDEBAR_POSITIONS.get(schema_name, 99)

    # Collect tables belonging to this schema.
    schema_tables: list[tuple[str, Any]] = []
    for full_key, table in meta.tables.items():
        # Keys are "schema.table_name" when schema is set.
        if "." in full_key:
            table_name = full_key.split(".", 1)[1]
        else:
            table_name = full_key
        schema_tables.append((table_name, table))

    # Sort tables alphabetically, but put brief_summary first if it exists.
    schema_tables.sort(key=lambda t: (0 if t[0] == "brief_summary" else 1, t[0]))

    lines: list[str] = [
        "---",
        f"sidebar_position: {sidebar_pos}",
        "---",
        "",
        f"# {schema_name} Schema",
        "",
        f"- **Primary Key**: `{entry_pk}`",
        f"- **Tables**: {len(schema_tables)}",
    ]

    for table_name, table in schema_tables:
        lines.append("")
        lines.append(f"## {table_name}")
        lines.append("")
        lines.append("| Column | Type | Description |")
        lines.append("|--------|------|-------------|")

        for col in table.columns:
            col_name: str = col.name
            col_type = _column_type_str(col)
            description = desc_lookup.get((table_name, col_name), "")
            safe_desc = _escape_mdx(description)
            lines.append(f"| {col_name} | {col_type} | {safe_desc} |")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point for the schema documentation generator."""
    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation for database schemas."
    )
    parser.add_argument(
        "--mine2-docs",
        type=Path,
        required=True,
        help="Path to mine2 rdb_docs directory containing JSON files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("website/docs/database"),
        help="Output directory for generated Markdown files (default: website/docs/database/).",
    )
    args = parser.parse_args()

    mine2_dir: Path = args.mine2_docs
    output_dir: Path = args.output

    if not mine2_dir.is_dir():
        print(f"Error: mine2 docs directory not found: {mine2_dir}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Lazy import to allow the script to run via uv with only sqlalchemy.
    # The project's own models must be importable (e.g. run from project root
    # with pixi or with PYTHONPATH set).
    try:
        from pdbminebuilder.models import ALL_METADATA
    except ImportError:
        print(
            "Error: Could not import pdbminebuilder.models. "
            "Run this script from the project root via: "
            "pixi run python scripts/generate_schema_docs.py ...",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load mine2 JSON documentation.
    mine2_schemas = _load_mine2_json(mine2_dir)

    for schema_name, meta in sorted(ALL_METADATA.items()):
        # Determine which mine2 JSON to use.
        json_key = SCHEMA_TO_JSON.get(schema_name, schema_name)
        mine2_data = mine2_schemas.get(json_key, {})
        desc_lookup = _build_description_lookup(mine2_data)

        md_content = _generate_schema_md(schema_name, meta, desc_lookup)
        out_path = output_dir.joinpath(f"{schema_name}.md")
        out_path.write_text(md_content, encoding="utf-8")
        table_count = len([k for k in meta.tables if True])
        print(f"Generated {out_path} ({table_count} tables)")

    print(f"\nDone. {len(ALL_METADATA)} schema files written to {output_dir}")


if __name__ == "__main__":
    main()
