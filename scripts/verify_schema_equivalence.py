#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
#     "sqlalchemy>=2.0",
# ]
# ///
"""Verify that generated SQLAlchemy models match YAML schema definitions.

Compares table names, column names/types, primary keys, unique keys, and
indexes between the YAML source-of-truth and the generated SA MetaData.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# Ensure project src is importable
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root.joinpath("src")))

import yaml  # noqa: E402
from sqlalchemy import ARRAY, MetaData  # noqa: E402

from pdbminebuilder.models import ALL_METADATA  # noqa: E402


# ---------------------------------------------------------------------------
# YAML loading (replicating loader.py logic)
# ---------------------------------------------------------------------------


def load_schema_yaml(deffile: Path) -> dict[str, Any]:
    """Load raw YAML schema and return parsed config + tables."""
    with deffile.open("r") as f:
        return yaml.safe_load(f)


def _apply_type_overwrites(
    raw: dict[str, Any],
) -> dict[str, str]:
    """Return a mapping of 'table.column' -> overwritten type."""
    config = raw.get("config", {})
    overwrites = config.get("type_overwrites", {})
    return overwrites if overwrites else {}


def _get_yaml_column_type(
    table_name: str,
    col_name: str,
    col_type: str,
    overwrites: dict[str, str],
) -> str:
    """Get the effective column type after applying overwrites."""
    key = f"{table_name}.{col_name}"
    return overwrites.get(key, col_type)


# ---------------------------------------------------------------------------
# Normalize PG type names (from loader.py)
# ---------------------------------------------------------------------------


def _normalize_type_name(type_name: str) -> str:
    """Normalize PostgreSQL type aliases to canonical names for comparison."""
    t = type_name.strip().lower()

    static_map = {
        "character varying": "text",
        "character": "char",
        "serial": "integer",
        "bigserial": "bigint",
    }
    if t in static_map:
        return static_map[t]

    m = re.match(r"^character\((\d+)\)$", t)
    if m:
        return f"char({m.group(1)})"

    return t


# ---------------------------------------------------------------------------
# SA type -> PG type string mapping
# ---------------------------------------------------------------------------


def _sa_type_to_pg(sa_type: Any) -> str:
    """Convert a SQLAlchemy type instance to its PostgreSQL type string.

    Args:
        sa_type: A SQLAlchemy type instance (e.g., Text(), Integer()).

    Returns:
        Normalized PostgreSQL type string.
    """
    from sqlalchemy import (
        BigInteger,
        Boolean,
        Date,
        DateTime,
        Double,
        Float,
        Integer,
        String,
        Text,
    )
    from sqlalchemy.dialects.postgresql import JSONB

    if isinstance(sa_type, ARRAY):
        inner = _sa_type_to_pg(sa_type.item_type)
        return f"{inner}[]"

    type_map: list[tuple[type, str]] = [
        (Text, "text"),
        (String, "char({length})"),
        (BigInteger, "bigint"),
        (Integer, "integer"),
        (Double, "double precision"),
        (Float, "real"),
        (Date, "date"),
        (Boolean, "boolean"),
        (JSONB, "jsonb"),
    ]

    for sa_cls, pg_str in type_map:
        if isinstance(sa_type, sa_cls):
            if sa_cls is String:
                length = getattr(sa_type, "length", None)
                if length is not None:
                    return f"char({length})"
                return "text"
            return pg_str

    # DateTime needs special handling for timezone
    if isinstance(sa_type, DateTime):
        if sa_type.timezone:
            return "timestamp with time zone"
        return "timestamp without time zone"

    return str(sa_type).lower()


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------


class Difference:
    """Represents a single difference between YAML and SA definitions."""

    def __init__(self, schema: str, table: str, kind: str, detail: str) -> None:
        self.schema = schema
        self.table = table
        self.kind = kind
        self.detail = detail

    def __str__(self) -> str:
        return f"  [{self.kind}] {self.schema}.{self.table}: {self.detail}"


def compare_schema(
    schema_name: str,
    yaml_path: Path,
    sa_metadata: MetaData,
) -> list[Difference]:
    """Compare a single YAML schema against its SA MetaData.

    Args:
        schema_name: The schema name (e.g., "cc", "pdbj").
        yaml_path: Path to the YAML definition file.
        sa_metadata: The SQLAlchemy MetaData object.

    Returns:
        List of differences found.
    """
    diffs: list[Difference] = []
    raw = load_schema_yaml(yaml_path)
    overwrites = _apply_type_overwrites(raw)

    yaml_tables = raw.get("tables", [])
    yaml_table_names = {t["name"] for t in yaml_tables}

    # SA table names are stored as schema.table_name in metadata.tables
    sa_table_names = set()
    sa_tables_by_name: dict[str, Any] = {}
    for key, table in sa_metadata.tables.items():
        # key format is "schema.table_name"
        short_name = table.name
        sa_table_names.add(short_name)
        sa_tables_by_name[short_name] = table

    # Check for missing / extra tables
    missing_in_sa = yaml_table_names - sa_table_names
    extra_in_sa = sa_table_names - yaml_table_names

    for name in sorted(missing_in_sa):
        diffs.append(Difference(schema_name, name, "TABLE", "missing in SA models"))

    for name in sorted(extra_in_sa):
        diffs.append(
            Difference(schema_name, name, "TABLE", "extra in SA models (not in YAML)")
        )

    # Compare each table that exists in both
    for yaml_table in yaml_tables:
        table_name = yaml_table["name"]
        if table_name not in sa_tables_by_name:
            continue

        sa_table = sa_tables_by_name[table_name]
        table_diffs = _compare_table(schema_name, yaml_table, sa_table, overwrites)
        diffs.extend(table_diffs)

    return diffs


def _compare_table(
    schema_name: str,
    yaml_table: dict[str, Any],
    sa_table: Any,
    overwrites: dict[str, str],
) -> list[Difference]:
    """Compare a single table between YAML and SA definitions."""
    diffs: list[Difference] = []
    table_name = yaml_table["name"]

    # --- Columns ---
    yaml_columns = yaml_table.get("columns", [])
    yaml_col_names = [c[0] for c in yaml_columns]
    yaml_col_types = {
        c[0]: _normalize_type_name(
            _get_yaml_column_type(table_name, c[0], c[1], overwrites)
        )
        for c in yaml_columns
    }

    sa_col_names = [col.name for col in sa_table.columns]
    sa_col_types = {
        col.name: _normalize_type_name(_sa_type_to_pg(col.type))
        for col in sa_table.columns
    }

    # Column order
    if yaml_col_names != sa_col_names:
        yaml_set = set(yaml_col_names)
        sa_set = set(sa_col_names)
        missing = yaml_set - sa_set
        extra = sa_set - yaml_set
        if missing:
            diffs.append(
                Difference(
                    schema_name,
                    table_name,
                    "COLUMN",
                    f"missing in SA: {sorted(missing)}",
                )
            )
        if extra:
            diffs.append(
                Difference(
                    schema_name,
                    table_name,
                    "COLUMN",
                    f"extra in SA: {sorted(extra)}",
                )
            )

    # Column types
    for col_name in yaml_col_names:
        if col_name not in sa_col_types:
            continue
        yaml_type = yaml_col_types[col_name]
        sa_type = sa_col_types[col_name]
        if yaml_type != sa_type:
            diffs.append(
                Difference(
                    schema_name,
                    table_name,
                    "TYPE",
                    f"column '{col_name}': YAML={yaml_type!r} SA={sa_type!r}",
                )
            )

    # --- Primary keys ---
    yaml_pk = yaml_table.get("primary_key", [])
    sa_pk = [col.name for col in sa_table.primary_key.columns]
    if yaml_pk != sa_pk:
        diffs.append(
            Difference(
                schema_name,
                table_name,
                "PK",
                f"YAML={yaml_pk} SA={sa_pk}",
            )
        )

    # --- Unique keys ---
    yaml_uks = yaml_table.get("unique_keys", [])
    if yaml_uks is None:
        yaml_uks = []
    yaml_uk_sets = [frozenset(uk) for uk in yaml_uks if uk]

    sa_uk_sets: list[frozenset[str]] = []
    for constraint in sa_table.constraints:
        from sqlalchemy import UniqueConstraint

        if isinstance(constraint, UniqueConstraint):
            cols = frozenset(col.name for col in constraint.columns)
            sa_uk_sets.append(cols)

    yaml_uk_sorted = sorted(yaml_uk_sets, key=lambda s: sorted(s))
    sa_uk_sorted = sorted(sa_uk_sets, key=lambda s: sorted(s))

    if yaml_uk_sorted != sa_uk_sorted:
        diffs.append(
            Difference(
                schema_name,
                table_name,
                "UNIQUE",
                f"YAML={[sorted(s) for s in yaml_uk_sorted]} "
                f"SA={[sorted(s) for s in sa_uk_sorted]}",
            )
        )

    # --- Indexes ---
    yaml_indexes = yaml_table.get("indexes", [])
    if yaml_indexes is None:
        yaml_indexes = []
    yaml_idx_sets: list[frozenset[str]] = []
    for idx in yaml_indexes:
        if not idx:
            continue
        if isinstance(idx, list):
            yaml_idx_sets.append(frozenset(idx))
        else:
            yaml_idx_sets.append(frozenset([str(idx)]))

    sa_idx_sets: list[frozenset[str]] = []
    for idx in sa_table.indexes:
        cols = frozenset(col.name for col in idx.columns)
        sa_idx_sets.append(cols)

    yaml_idx_sorted = sorted(yaml_idx_sets, key=lambda s: sorted(s))
    sa_idx_sorted = sorted(sa_idx_sets, key=lambda s: sorted(s))

    if yaml_idx_sorted != sa_idx_sorted:
        diffs.append(
            Difference(
                schema_name,
                table_name,
                "INDEX",
                f"YAML={[sorted(s) for s in yaml_idx_sorted]} "
                f"SA={[sorted(s) for s in sa_idx_sorted]}",
            )
        )

    return diffs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Compare all YAML schemas against their generated SA MetaData."""
    schemas_dir = project_root.joinpath("schemas")
    total_diffs = 0
    total_schemas = 0
    total_tables = 0

    for schema_name, sa_metadata in sorted(ALL_METADATA.items()):
        yaml_path = schemas_dir.joinpath(f"{schema_name}.def.yml")
        if not yaml_path.exists():
            print(
                f"WARNING: YAML file not found for schema '{schema_name}': {yaml_path}"
            )
            continue

        diffs = compare_schema(schema_name, yaml_path, sa_metadata)
        table_count = len(sa_metadata.tables)
        total_schemas += 1
        total_tables += table_count

        if diffs:
            print(
                f"\n{schema_name} ({table_count} tables) - {len(diffs)} difference(s):"
            )
            for d in diffs:
                print(str(d))
            total_diffs += len(diffs)
        else:
            print(f"{schema_name} ({table_count} tables) - OK")

    print(f"\n{'=' * 60}")
    print(f"Summary: {total_schemas} schemas, {total_tables} tables checked")
    if total_diffs == 0:
        print("All schemas match. No differences found.")
    else:
        print(f"Found {total_diffs} difference(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
