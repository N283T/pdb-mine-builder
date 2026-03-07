#!/usr/bin/env -S pixi run python
"""Generate rdb_docs YAML and website Markdown from SQLAlchemy models.

Outputs:
  - docs/rdb_docs/{schema}.yml  — mine2-compatible YAML for AI/tooling
  - website/docs/database/{schema}.md — Docusaurus schema reference pages

Usage:
    pixi run python scripts/generate_rdb_docs.py
"""

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


def generate_schema_markdown(schema_name: str, data: dict) -> str:
    """Generate Docusaurus Markdown for a schema reference page."""
    config = data["config"]
    tables = data["tables"]
    position = SIDEBAR_POSITIONS.get(schema_name, 99)

    lines = [
        "---",
        f"sidebar_position: {position}",
        "---",
        "",
        f"# {schema_name} Schema",
        "",
        f"- **Primary Key**: `{config['primaryKey']}`",
        f"- **Tables**: {len(tables)}",
    ]

    for table in tables:
        lines.append("")
        lines.append(f"## {table['name']}")
        lines.append("")
        lines.append("| Column | Type | Description |")
        lines.append("|--------|------|-------------|")
        for col_name, col_type, col_desc in table["columns"]:
            # Escape pipe characters in descriptions for Markdown tables
            desc = col_desc.replace("|", "\\|")
            lines.append(f"| {col_name} | {col_type} | {desc} |")

    lines.append("")
    return "\n".join(lines)


def extract_custom_content(md_path: Path) -> str | None:
    """Extract hand-written content after the APPENDIX_MARKER from existing file."""
    if not md_path.exists():
        return None
    content = md_path.read_text()
    idx = content.find(APPENDIX_MARKER)
    if idx == -1:
        return None
    return content[idx:]


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    yaml_dir = project_root.joinpath("docs", "rdb_docs")
    md_dir = project_root.joinpath("website", "docs", "database")
    yaml_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

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

        # Write Markdown
        md_content = generate_schema_markdown(schema_name, data)

        md_path = md_dir.joinpath(f"{schema_name}.md")
        custom = extract_custom_content(md_path)
        if custom:
            md_content += custom

        md_path.write_text(md_content)

        print(
            f"  {schema_name}: {table_count} tables -> {yaml_path.name}, {md_path.name}"
        )

    print(f"\nGenerated {len(ALL_METADATA)} schemas (YAML + Markdown)")


if __name__ == "__main__":
    main()
