#!/usr/bin/env -S pixi run python
"""Generate rdb_docs JSON files from SQLAlchemy models.

Produces one JSON file per schema in docs/rdb_docs/, matching the format
used by mine2 rdb_docs (compatible with AI/documentation tooling).

Usage:
    pixi run python scripts/generate_rdb_docs.py
"""

import json
from pathlib import Path

from sqlalchemy import PrimaryKeyConstraint

from pdbminebuilder.db._type_utils import sa_type_to_pg
from pdbminebuilder.db.loader import get_all_tables, get_entry_pk
from pdbminebuilder.models import ALL_METADATA


def generate_schema_json(schema_name: str) -> dict:
    """Generate rdb_docs JSON for a single schema."""
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
            columns.append([col.name, pg_type, desc])

        pk_cols = []
        for constraint in table.constraints:
            if isinstance(constraint, PrimaryKeyConstraint):
                pk_cols = [c.name for c in constraint.columns]
                break

        tables.append(
            {
                "name": table.name,
                "columns": columns,
                "primary_key": pk_cols,
                "foreign_keys": [],
                "desc": "",
            }
        )

    return {"config": config, "tables": tables}


def main() -> None:
    output_dir = Path(__file__).resolve().parent.parent.joinpath("docs", "rdb_docs")
    output_dir.mkdir(parents=True, exist_ok=True)

    for schema_name in sorted(ALL_METADATA.keys()):
        data = generate_schema_json(schema_name)
        output_path = output_dir.joinpath(f"{schema_name}.json")
        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        table_count = len(data["tables"])
        print(f"  {schema_name}: {table_count} tables -> {output_path.name}")

    print(f"\nGenerated {len(ALL_METADATA)} schema files in {output_dir}")


if __name__ == "__main__":
    main()
