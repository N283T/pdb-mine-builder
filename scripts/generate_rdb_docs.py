#!/usr/bin/env -S pixi run python
"""Generate rdb_docs YAML and website MDX from SQLAlchemy models.

Outputs:
  - docs/rdb_docs/{schema}.yml  — mine2-compatible YAML for AI/tooling
  - website/docs/database/{schema}.mdx — Docusaurus schema reference pages (with search)

Usage:
    pixi run python scripts/generate_rdb_docs.py
"""

import json
from pathlib import Path

import yaml

from sqlalchemy import PrimaryKeyConstraint

from pdbminebuilder.db._type_utils import sa_type_to_pg
from pdbminebuilder.db.loader import get_all_tables, get_entry_pk
from pdbminebuilder.models import ALL_METADATA

# Sidebar order for Docusaurus (overview.md = 0)
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

# Marker that separates auto-generated content from hand-written appendices
APPENDIX_MARKER = "<!-- BEGIN CUSTOM CONTENT -->"


def generate_schema_data(schema_name: str) -> dict:
    """Generate rdb_docs data for a single schema."""
    meta = ALL_METADATA[schema_name]
    entry_pk = get_entry_pk(meta)

    config: dict = {
        "primaryKey": entry_pk,
        "schema": schema_name,
    }

    tables = []
    for table in get_all_tables(meta):
        columns = []
        for col in table.columns:
            pg_type = sa_type_to_pg(col.type)
            desc = col.comment or ""
            columns.append([str(col.name), pg_type, desc])

        pk_cols = []
        for constraint in table.constraints:
            if isinstance(constraint, PrimaryKeyConstraint):
                pk_cols = [str(c.name) for c in constraint.columns]
                break

        tables.append(
            {
                "name": str(table.name),
                "columns": columns,
                "primary_key": pk_cols,
                "foreign_keys": [],
                "desc": "",
            }
        )

    return {"config": config, "tables": tables}


def generate_schema_mdx(schema_name: str, data: dict) -> str:
    """Generate Docusaurus MDX for a schema reference page with search."""
    config = data["config"]
    tables = data["tables"]
    position = SIDEBAR_POSITIONS.get(schema_name, 99)

    # Convert column arrays to objects for the React component
    tables_for_component = [
        {
            "name": t["name"],
            "columns": [
                {"name": c[0], "type": c[1], "description": c[2]} for c in t["columns"]
            ],
        }
        for t in tables
    ]
    tables_json = json.dumps(tables_for_component, ensure_ascii=False)

    lines = [
        "---",
        f"sidebar_position: {position}",
        "---",
        "",
        "import SchemaFilter from '@site/src/components/SchemaFilter';",
        "",
        f"# {schema_name} Schema",
        "",
        f"- **Primary Key**: `{config['primaryKey']}`",
        f"- **Tables**: {len(tables)}",
        "",
        f"<SchemaFilter tables={{JSON.parse('{_escape_js_string(tables_json)}')}} />",
    ]

    lines.append("")
    return "\n".join(lines)


def _escape_js_string(s: str) -> str:
    """Escape a string for use inside a JS single-quoted string literal."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def extract_custom_content(dir_path: Path, schema_name: str) -> str | None:
    """Extract hand-written content after the APPENDIX_MARKER from existing file.

    Searches both .mdx and .md files (for migration from .md to .mdx).
    """
    for ext in (".mdx", ".md"):
        path = dir_path.joinpath(f"{schema_name}{ext}")
        if not path.exists():
            continue
        content = path.read_text()
        idx = content.find(APPENDIX_MARKER)
        if idx != -1:
            return content[idx:]
    return None


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    yaml_dir = project_root.joinpath("docs", "rdb_docs")
    mdx_dir = project_root.joinpath("website", "docs", "database")
    yaml_dir.mkdir(parents=True, exist_ok=True)
    mdx_dir.mkdir(parents=True, exist_ok=True)

    for schema_name in sorted(ALL_METADATA.keys()):
        data = generate_schema_data(schema_name)
        table_count = len(data["tables"])

        # Write YAML
        yaml_path = yaml_dir.joinpath(f"{schema_name}.yml")
        yaml_path.write_text(
            yaml.dump(
                data, allow_unicode=True, default_flow_style=False, sort_keys=False
            )
        )

        # Write MDX
        mdx_content = generate_schema_mdx(schema_name, data)

        custom = extract_custom_content(mdx_dir, schema_name)
        if custom:
            mdx_content += custom

        mdx_path = mdx_dir.joinpath(f"{schema_name}.mdx")
        mdx_path.write_text(mdx_content)

        # Remove old .md if .mdx was created
        old_md = mdx_dir.joinpath(f"{schema_name}.md")
        if old_md.exists():
            old_md.unlink()

        print(
            f"  {schema_name}: {table_count} tables -> {yaml_path.name}, {mdx_path.name}"
        )

    print(f"\nGenerated {len(ALL_METADATA)} schemas (YAML + MDX)")


if __name__ == "__main__":
    main()
