#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Generate SQL query examples documentation from sqlExamples.json.

Reads website/static/data/sqlExamples.json (the single source of truth)
and generates website/docs/examples/sql-examples.md for Docusaurus.
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_FILE = PROJECT_ROOT.joinpath("website", "static", "data", "sqlExamples.json")
OUTPUT_FILE = PROJECT_ROOT.joinpath("website", "docs", "examples", "sql-examples.md")

FRONTMATTER = """\
---
sidebar_position: 1
---

# SQL Query Examples

A collection of SQL query examples for the pdb-mine-builder database. These examples are adapted from [PDBj Mine SQL examples](https://pdbj.org/help/mine-sql) with schema-prefixed table names.

:::tip How to run
Use `pmb query` or connect directly with `psql`:

```bash
# Using pmb query
pmb query "SELECT pdbid FROM pdbj.brief_summary LIMIT 5"

# Using psql (via pixi)
pixi run psql -c "SELECT pdbid FROM pdbj.brief_summary LIMIT 5"
```

Click the **copy button** (top-right of each code block) to copy a query to your clipboard.
:::

:::info PostgreSQL array operators
Many examples use PostgreSQL array operators on `brief_summary` columns:

| Operator | Meaning | Example |
|----------|---------|---------|
| `<@` | is contained by (all elements match) | `'{1,2}' <@ chain_type_ids` |
| `&&` | overlaps (any element matches) | `'{2001}' && citation_year` |
| `ANY()` | matches any array element | `6 = ANY(exptl_method_ids)` |

See the [brief_summary column reference](/docs/database/pdbj#brief_summary) for array column definitions and ID mappings.
:::\
"""


def format_sql(sql: str) -> str:
    """Clean up SQL formatting by removing trailing whitespace from lines."""
    lines = sql.split("\n")
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


def escape_mdx(text: str) -> str:
    """Escape characters that MDX would interpret as JSX."""
    return (
        text.replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )


def generate_markdown(categories: list[dict]) -> str:
    """Generate the full markdown document from category data."""
    parts: list[str] = [FRONTMATTER]

    for category in categories:
        examples = category["examples"]
        if not examples:
            continue

        label = category["label"]
        count = category["count"]
        description = category["description"]

        parts.append(f"\n## {label} ({count})\n")
        parts.append(f"{description}\n")

        for example in examples:
            title = escape_mdx(example["title"])
            desc = escape_mdx(example["description"])
            sql = format_sql(example["sql"])

            parts.append(f"""
<details>
<summary>{title}</summary>

{desc}

```sql
{sql}
```

</details>
""")

    return "\n".join(parts)


def main() -> None:
    """Read sqlExamples.json and generate the markdown documentation."""
    categories: list[dict] = json.loads(INPUT_FILE.read_text())
    content = generate_markdown(categories)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(content)

    total_examples = sum(len(cat["examples"]) for cat in categories)
    print(f"Generated {OUTPUT_FILE} ({total_examples} examples)")


if __name__ == "__main__":
    main()
