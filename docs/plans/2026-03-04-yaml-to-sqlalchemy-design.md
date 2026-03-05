# YAML to SQLAlchemy Schema Migration Design

> **Note:** This document was written when the project was named `mine2`.
> References to `mine2` now correspond to `pdbminebuilder`.

Date: 2026-03-04

## Goal

Migrate schema management from custom YAML format to SQLAlchemy Core + Alembic.
This eliminates the proprietary schema format and enables standard migration tooling.

## Requirements

- **Standardization**: Replace custom YAML schema definitions with SQLAlchemy Core `Table` objects
- **Migration management**: Use Alembic for schema versioning, diff detection, and rollback
- **Complete rewrite**: Remove `SchemaDef`/`TableDef` dataclasses; pipelines reference SA `Table` directly
- **Data**: Re-load from source after migration (no live data migration needed)
- **Scope**: DDL + migration only; data operations remain psycopg3 direct

## Current State

- 10 YAML schema files in `schemas/` (~20k lines total)
- `pdbj.def.yml` alone: ~400 tables, ~10k lines
- Custom `SchemaDef`/`TableDef` dataclasses in `loader.py`
- DDL generation via string assembly in `create_table()` / `migrate_table_schema()`
- No migration tracking or rollback capability
- Type changes discard data (`ALTER TYPE ... USING NULL`)

## Architecture

### Directory Structure

```
src/mine2/
├── models/                    # SQLAlchemy Table definitions
│   ├── __init__.py           # MetaData registry (ALL_METADATA dict)
│   ├── cc.py                 # cc schema tables
│   ├── ccmodel.py            # ccmodel schema tables
│   ├── contacts.py           # contacts schema tables
│   ├── pdbj.py               # pdbj schema tables (~400 tables)
│   ├── prd.py                # prd schema tables
│   ├── vrpt.py               # vrpt schema tables
│   ├── emdb.py               # emdb schema tables
│   ├── ihm.py                # ihm schema tables
│   ├── sifts.py              # sifts schema tables
│   └── prd_family.py         # prd_family schema tables
├── db/
│   ├── connection.py         # unchanged
│   ├── loader.py             # rewritten: uses SA Table objects
│   └── migration.py          # Alembic helper functions
alembic/                       # Alembic configuration
├── alembic.ini
├── env.py                    # Multi-schema support
└── versions/                 # Migration scripts
scripts/
└── convert_yaml_to_sa.py    # One-shot converter (temporary)
```

### Table Definition Format

```python
# src/mine2/models/cc.py
from sqlalchemy import (
    Column, MetaData, Table, Text, BigInteger, Date,
    ARRAY, Float, Boolean, Index, PrimaryKeyConstraint,
    UniqueConstraint,
)

metadata = MetaData(schema="cc")
metadata.info = {
    "entry_pk": "comp_id",
    "skip_foreign_keys": False,
}

brief_summary = Table(
    "brief_summary",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("pdbx_initial_date", Date, nullable=True),
    Column("name", Text, nullable=True),
    Column("smiles", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("comp_id"),
    info={
        "entry_pk": "comp_id",
        "keywords": ["name", "formula"],
        "skip_keywords": [],
    },
)
```

- Each schema has one `MetaData` object with `schema=` set
- Schema-level config stored in `metadata.info`
- Table-level config stored in `table.info` (keywords, skip_keywords, entry_pk)
- Column-level flags via `column.info` if needed
- FK definitions as comments only (not enforced at DB level)

### Registry

```python
# src/mine2/models/__init__.py
from mine2.models.cc import metadata as cc_metadata
from mine2.models.pdbj import metadata as pdbj_metadata
# ...

ALL_METADATA: dict[str, MetaData] = {
    "cc": cc_metadata,
    "pdbj": pdbj_metadata,
    # ...
}
```

### Loader Changes

`SchemaDef` and `TableDef` are removed. All consumers use SA `Table` / `MetaData` directly.

```python
# loader.py
def ensure_schema(meta: MetaData, conninfo: str) -> None:
    """Create all tables from MetaData using create_all()."""

def bulk_upsert(conninfo: str, table: Table, rows: list[tuple],
                conflict_columns: list[str]) -> tuple[int, int]:
    """Uses table.name, table.schema, table.columns."""

def delete_missing_entries(conninfo: str, table: Table,
                           pk_values: set[str]) -> int:
    """Delete entries not in pk_values set."""
```

### Pipeline Changes

```python
# Before (pipelines/cc.py)
from mine2.db.loader import load_schema_def
schema_def = load_schema_def(config.deffile)
table = schema_def.get_table("brief_summary")

# After
from mine2.models.cc import metadata, brief_summary
table = metadata.tables["brief_summary"]
```

### Type Coercion

`coerce_value()` dispatches on SA type objects instead of string matching:

```python
from sqlalchemy import Text, Integer, Float, BigInteger, Date, ARRAY, Boolean

def coerce_value(value, sa_type):
    match sa_type:
        case Text(): return _coerce_string(value)
        case Integer() | BigInteger(): return _coerce_integer(value)
        case Float(): return _coerce_float(value)
        case Date(): return _coerce_date(value)
        case ARRAY(): return _coerce_array(value, sa_type.item_type)
        case Boolean(): return _coerce_boolean(value)
```

### Alembic Integration

```python
# alembic/env.py
from mine2.models import ALL_METADATA
from sqlalchemy import MetaData

# Merge all schema MetaData into one for Alembic
target_metadata = MetaData()
for meta in ALL_METADATA.values():
    for table in meta.tables.values():
        table.to_metadata(target_metadata)
```

CLI usage:
```bash
pixi run alembic revision --autogenerate -m "description"
pixi run alembic upgrade head
pixi run alembic stamp head  # baseline existing schema
pixi run alembic downgrade -1  # rollback
```

## Conversion Strategy

1. Write `scripts/convert_yaml_to_sa.py` to auto-generate all `models/*.py` files
2. Verify generated models produce identical DDL to current YAML-based approach
3. Rewrite `loader.py` to consume SA `Table` objects
4. Rewrite `base.py` type coercion to use SA types
5. Update all pipelines to import from `models/`
6. Set up Alembic with initial baseline
7. Remove YAML files and `load_schema_def()`
8. Update tests

## What Does NOT Change

- psycopg3 direct connections (no SQLAlchemy Engine for data ops)
- ProcessPoolExecutor parallel loading
- Pipeline structure and data flow
- CIF/mmJSON parsing (gemmi)
- config.yml (except `deffile` field removed from pipeline configs)

## Risks

- **pdbj.py file size**: ~400 tables will produce a large file. Acceptable since auto-generated.
- **Type mapping accuracy**: Must verify YAML types map correctly to SA types.
- **Alembic multi-schema**: Needs custom `include_name` filter in env.py.
- **RDKit extension**: Not part of Alembic migrations. Keep manual setup.

---
- [ ] **DONE** - Design complete
