#!/usr/bin/env -S pixi run python
"""Inject column comments from mine2 rdb_docs into SQLAlchemy model files.

Reads descriptions from mine2 rdb_docs JSON and adds comment= parameter
to Column() definitions in model .py files.

Usage:
    pixi run python scripts/inject_column_comments.py /path/to/rdb_docs/

This script modifies files in src/pdbminebuilder/models/ in-place.
"""

import json
import re
import sys
from pathlib import Path

MODELS_DIR = (
    Path(__file__).resolve().parent.parent.joinpath("src", "pdbminebuilder", "models")
)

# Schemas that have corresponding mine2 rdb_docs JSON files
SCHEMA_FILES = {
    "cc": "cc.json",
    "ccmodel": "ccmodel.json",
    "contacts": "contacts.json",
    "emdb": "emdb.json",
    "pdbj": "pdbj.json",
    "prd": "prd.json",
    "prd_family": "prd_family.json",
    "vrpt": "vrpt.json",
}


def load_desc_map(rdb_docs_dir: Path, schema: str) -> dict[str, dict[str, str]]:
    """Load column descriptions from mine2 rdb_docs JSON.

    Returns:
        {table_name: {column_name: description}}
    """
    json_path = rdb_docs_dir.joinpath(SCHEMA_FILES[schema])
    if not json_path.exists():
        print(f"  [skip] {json_path} not found")
        return {}

    data = json.loads(json_path.read_text())
    desc_map: dict[str, dict[str, str]] = {}
    for table in data["tables"]:
        table_descs: dict[str, str] = {}
        for col in table["columns"]:
            col_name, _col_type, col_desc = col[0], col[1], col[2]
            if col_desc:
                table_descs[col_name] = col_desc
        if table_descs:
            desc_map[table["name"]] = table_descs

    return desc_map


def escape_comment(text: str) -> str:
    """Escape and clean a string for use in a Python string literal."""
    # Normalize whitespace: collapse newlines and multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("\\", "\\\\").replace('"', '\\"')


def inject_comments(model_path: Path, desc_map: dict[str, dict[str, str]]) -> int:
    """Inject comment= into Column() calls in a model file.

    Returns number of comments injected.
    """
    content = model_path.read_text()
    lines = content.split("\n")
    new_lines: list[str] = []
    current_table: str | None = None
    injected = 0

    table_name_pattern = re.compile(r'^\s*"(\w+)"')
    # Pattern: Column("col_name", Type, nullable=True)
    # or       Column("col_name", Type, nullable=True),
    column_pattern = re.compile(
        r'^(\s*)Column\("(\w+)",\s*(.*?),\s*nullable=(True|False)\)'
    )

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect table definition start
        if "= Table(" in line:
            # Next line should have the table name
            if i + 1 < len(lines):
                name_match = table_name_pattern.match(lines[i + 1])
                if name_match:
                    current_table = name_match.group(1)

        # Detect Column with comment injection opportunity
        col_match = column_pattern.match(line.rstrip().rstrip(","))
        if col_match and current_table:
            indent = col_match.group(1)
            col_name = col_match.group(2)
            col_type_str = col_match.group(3)
            nullable_val = col_match.group(4)

            table_descs = desc_map.get(current_table, {})
            desc = table_descs.get(col_name, "")

            trailing_comma = "," if line.rstrip().endswith(",") else ""

            if desc and "comment=" not in line:
                escaped = escape_comment(desc)
                new_line = (
                    f'{indent}Column("{col_name}", {col_type_str}, '
                    f'nullable={nullable_val}, comment="{escaped}"){trailing_comma}'
                )
                new_lines.append(new_line)
                injected += 1
                i += 1
                continue

        new_lines.append(line)
        i += 1

    if injected > 0:
        model_path.write_text("\n".join(new_lines))

    return injected


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/mine2/rdb_docs/")
        sys.exit(1)

    rdb_docs_dir = Path(sys.argv[1])
    if not rdb_docs_dir.is_dir():
        print(f"Error: {rdb_docs_dir} is not a directory")
        sys.exit(1)

    total_injected = 0
    for schema, json_file in sorted(SCHEMA_FILES.items()):
        model_path = MODELS_DIR.joinpath(f"{schema}.py")
        if not model_path.exists():
            print(f"  [skip] {model_path} not found")
            continue

        desc_map = load_desc_map(rdb_docs_dir, schema)
        if not desc_map:
            print(f"  {schema}: no descriptions found")
            continue

        count = inject_comments(model_path, desc_map)
        total_injected += count
        print(f"  {schema}: {count} comments injected")

    print(f"\nTotal: {total_injected} comments injected")


if __name__ == "__main__":
    main()
