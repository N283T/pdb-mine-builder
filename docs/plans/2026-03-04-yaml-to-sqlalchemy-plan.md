# YAML to SQLAlchemy Schema Migration - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace custom YAML schema definitions with SQLAlchemy Core Table objects and Alembic migrations.

**Architecture:** SQLAlchemy MetaData/Table as source of truth for schema definitions. Alembic for migration management. psycopg3 remains for all data operations. Workers import models directly instead of receiving pickled SchemaDef.

**Tech Stack:** SQLAlchemy Core 2.0+, Alembic 1.13+, psycopg3 (unchanged), pixi (unchanged)

**Design Doc:** `docs/plans/2026-03-04-yaml-to-sqlalchemy-design.md`

---

## Phase 1: Setup & Converter Script

### Task 1: Add SQLAlchemy and Alembic dependencies

**Files:**
- Modify: `pyproject.toml`

**Step 1: Add dependencies to pyproject.toml**

Add to `[project.dependencies]` (or pixi pypi-dependencies):
```
sqlalchemy>=2.0.0
alembic>=1.13.0
```

**Step 2: Install**

Run: `pixi install`
Expected: Clean install with sqlalchemy and alembic available

**Step 3: Verify import**

Run: `pixi run python -c "import sqlalchemy; import alembic; print(sqlalchemy.__version__, alembic.__version__)"`
Expected: Version numbers printed

**Step 4: Commit**

```bash
git add pyproject.toml pixi.lock
git commit -m "chore: add sqlalchemy and alembic dependencies"
```

---

### Task 2: Write YAML-to-SQLAlchemy converter script

**Files:**
- Create: `scripts/convert_yaml_to_sa.py`

**Step 1: Write the converter script**

This script reads all `schemas/*.def.yml` and generates `src/mine2/models/*.py`.

Type mapping (YAML → SQLAlchemy):
| YAML Type | SQLAlchemy Import | SA Expression |
|-----------|------------------|---------------|
| `text` | `Text` | `Text` |
| `integer` | `Integer` | `Integer` |
| `bigint` | `BigInteger` | `BigInteger` |
| `double precision` | `Double` | `Double` |
| `real` | `Float` | `Float` |
| `date` | `Date` | `Date` |
| `timestamp without time zone` | `DateTime` | `DateTime` |
| `timestamp with time zone` | `DateTime` | `DateTime(timezone=True)` |
| `boolean` | `Boolean` | `Boolean` |
| `text[]` | `ARRAY, Text` | `ARRAY(Text)` |
| `integer[]` | `ARRAY, Integer` | `ARRAY(Integer)` |
| `double precision[]` | `ARRAY, Double` | `ARRAY(Double)` |
| `boolean[]` | `ARRAY, Boolean` | `ARRAY(Boolean)` |
| `jsonb` | `JSONB` (from `sqlalchemy.dialects.postgresql`) | `JSONB` |
| `char(N)` | `String` | `String(N)` |
| `citext` | `Text` | `Text` (with `info={"citext": True}`) |

Key behaviors:
- Read `config.primaryKey` → `metadata.info["entry_pk"]`
- Read `config.skipForeignKeys` → `metadata.info["skip_foreign_keys"]`
- Read `config.type_overwrites` → apply before generating columns
- Read `tables[].keywords` → `table.info["keywords"]`
- Read `tables[].pkout` → `table.info["pkout"]`
- Read `skip-keywords` → `metadata.info["skip_keywords"]`
- Foreign keys → comments only (not SA ForeignKey objects)
- Column nullable always True (current YAML always has null)

Output file template:
```python
"""SQLAlchemy schema definition for {schema_name}.

Auto-generated from schemas/{schema_name}.def.yml by scripts/convert_yaml_to_sa.py.
"""

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Double,
    Float,
    Index,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData(schema="{schema_name}")
metadata.info = {{
    "entry_pk": "{primary_key}",
    "skip_foreign_keys": {skip_fk},
    "skip_keywords": {skip_keywords},
}}

{table_name} = Table(
    "{table_name}",
    metadata,
    Column("{col}", {type}),
    ...
    PrimaryKeyConstraint({pk_cols}),
    UniqueConstraint({uk_cols}),  # if any
    Index("ix_{schema}_{table}_{cols}", {idx_cols}),  # if any
    info={{
        "keywords": [...],
        "pkout": True/False,
    }},
)
```

**Step 2: Run converter on all schemas**

Run: `pixi run python scripts/convert_yaml_to_sa.py`
Expected: Files generated in `src/mine2/models/` for each schema

**Step 3: Commit**

```bash
git add scripts/convert_yaml_to_sa.py
git commit -m "chore: add YAML-to-SQLAlchemy converter script"
```

---

### Task 3: Generate all model files and verify

**Files:**
- Create: `src/mine2/models/__init__.py`
- Create: `src/mine2/models/cc.py` (and all other schema files)

**Step 1: Run the converter**

Run: `pixi run python scripts/convert_yaml_to_sa.py`
Expected: All model files generated

**Step 2: Write models/__init__.py registry**

```python
"""SQLAlchemy model registry.

Provides ALL_METADATA dict mapping schema names to MetaData objects,
and get_metadata() for worker process access.
"""

from sqlalchemy import MetaData

from mine2.models.cc import metadata as cc_metadata
from mine2.models.ccmodel import metadata as ccmodel_metadata
from mine2.models.contacts import metadata as contacts_metadata
from mine2.models.emdb import metadata as emdb_metadata
from mine2.models.ihm import metadata as ihm_metadata
from mine2.models.pdbj import metadata as pdbj_metadata
from mine2.models.prd import metadata as prd_metadata
from mine2.models.prd_family import metadata as prd_family_metadata
from mine2.models.sifts import metadata as sifts_metadata
from mine2.models.vrpt import metadata as vrpt_metadata

ALL_METADATA: dict[str, MetaData] = {
    "cc": cc_metadata,
    "ccmodel": ccmodel_metadata,
    "contacts": contacts_metadata,
    "emdb": emdb_metadata,
    "ihm": ihm_metadata,
    "pdbj": pdbj_metadata,
    "prd": prd_metadata,
    "prd_family": prd_family_metadata,
    "sifts": sifts_metadata,
    "vrpt": vrpt_metadata,
}


def get_metadata(schema_name: str) -> MetaData:
    """Get MetaData for a schema. Used by worker processes."""
    return ALL_METADATA[schema_name]
```

**Step 3: Verify DDL equivalence**

Write a verification script that:
1. Loads each YAML schema via `load_schema_def()`
2. Loads corresponding SA MetaData from `mine2.models`
3. Compares table names, column names/types, PKs, UKs, indexes
4. Reports any differences

Run: `pixi run python scripts/verify_schema_equivalence.py`
Expected: All schemas match

**Step 4: Verify imports work**

Run: `pixi run python -c "from mine2.models import ALL_METADATA; print(list(ALL_METADATA.keys()))"`
Expected: All 10 schema names printed

**Step 5: Commit**

```bash
git add src/mine2/models/
git commit -m "feat: add SQLAlchemy model definitions generated from YAML schemas"
```

---

## Phase 2: Core Rewrite - loader.py

### Task 4: Rewrite loader.py data classes and load functions

**Files:**
- Modify: `src/mine2/db/loader.py`

**Step 1: Remove SchemaDef and TableDef dataclasses** (lines 30-78)

Remove `TableDef`, `SchemaDef`, and `load_schema_def()` entirely.

**Step 2: Add helper functions for SA MetaData access**

```python
from sqlalchemy import MetaData, Table


def get_entry_pk(meta: MetaData) -> str:
    """Get the entry-level primary key column name from MetaData.info."""
    return meta.info["entry_pk"]


def get_table(meta: MetaData, table_name: str) -> Table:
    """Get a Table from MetaData by name."""
    key = f"{meta.schema}.{table_name}" if meta.schema else table_name
    return meta.tables[key]


def get_table_or_none(meta: MetaData, table_name: str) -> Table | None:
    """Get a Table from MetaData by name, or None if not found."""
    key = f"{meta.schema}.{table_name}" if meta.schema else table_name
    return meta.tables.get(key)


def get_all_tables(meta: MetaData) -> list[Table]:
    """Get all tables from MetaData in sorted order."""
    return list(meta.sorted_tables)


def get_column_types(table: Table) -> dict[str, str]:
    """Get column name → PostgreSQL type string mapping from SA Table."""
    from mine2.db._type_utils import sa_type_to_pg
    return {col.name: sa_type_to_pg(col.type) for col in table.columns}


def get_column_names(table: Table) -> set[str]:
    """Get set of column names from SA Table."""
    return {col.name for col in table.columns}
```

**Step 3: Commit**

```bash
git add src/mine2/db/loader.py
git commit -m "refactor: remove SchemaDef/TableDef, add SA MetaData helpers"
```

---

### Task 5: Add type utility module

**Files:**
- Create: `src/mine2/db/_type_utils.py`

**Step 1: Write SA type ↔ PG type conversion**

```python
"""SQLAlchemy type ↔ PostgreSQL type string utilities."""

from sqlalchemy import (
    ARRAY,
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
from sqlalchemy.types import TypeEngine


def sa_type_to_pg(sa_type: TypeEngine) -> str:
    """Convert SQLAlchemy type to PostgreSQL type string."""
    if isinstance(sa_type, ARRAY):
        item = sa_type_to_pg(sa_type.item_type)
        return f"{item}[]"
    if isinstance(sa_type, Text):
        return "text"
    if isinstance(sa_type, String):
        length = sa_type.length
        return f"char({length})" if length else "text"
    if isinstance(sa_type, BigInteger):
        return "bigint"
    if isinstance(sa_type, Integer):
        return "integer"
    if isinstance(sa_type, Double):
        return "double precision"
    if isinstance(sa_type, Float):
        return "real"
    if isinstance(sa_type, Date):
        return "date"
    if isinstance(sa_type, DateTime):
        if sa_type.timezone:
            return "timestamp with time zone"
        return "timestamp without time zone"
    if isinstance(sa_type, Boolean):
        return "boolean"
    if isinstance(sa_type, JSONB):
        return "jsonb"
    return str(sa_type)
```

Note: Order matters — `BigInteger` must be checked before `Integer` (BigInteger extends Integer in SA).

**Step 2: Write test**

Create `tests/test_type_utils.py`:
```python
from sqlalchemy import ARRAY, BigInteger, Boolean, Date, DateTime, Double, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from mine2.db._type_utils import sa_type_to_pg


class TestSaTypeToPg:
    def test_text(self):
        assert sa_type_to_pg(Text()) == "text"

    def test_integer(self):
        assert sa_type_to_pg(Integer()) == "integer"

    def test_bigint(self):
        assert sa_type_to_pg(BigInteger()) == "bigint"

    def test_double(self):
        assert sa_type_to_pg(Double()) == "double precision"

    def test_real(self):
        assert sa_type_to_pg(Float()) == "real"

    def test_date(self):
        assert sa_type_to_pg(Date()) == "date"

    def test_timestamp(self):
        assert sa_type_to_pg(DateTime()) == "timestamp without time zone"

    def test_timestamptz(self):
        assert sa_type_to_pg(DateTime(timezone=True)) == "timestamp with time zone"

    def test_boolean(self):
        assert sa_type_to_pg(Boolean()) == "boolean"

    def test_text_array(self):
        assert sa_type_to_pg(ARRAY(Text)) == "text[]"

    def test_integer_array(self):
        assert sa_type_to_pg(ARRAY(Integer)) == "integer[]"

    def test_jsonb(self):
        assert sa_type_to_pg(JSONB()) == "jsonb"

    def test_char(self):
        assert sa_type_to_pg(String(3)) == "char(3)"
```

**Step 3: Run test**

Run: `pixi run pytest tests/test_type_utils.py -v`
Expected: All pass

**Step 4: Commit**

```bash
git add src/mine2/db/_type_utils.py tests/test_type_utils.py
git commit -m "feat: add SQLAlchemy type to PostgreSQL type string converter"
```

---

### Task 6: Rewrite ensure_schema()

**Files:**
- Modify: `src/mine2/db/loader.py`

**Step 1: Rewrite ensure_schema using MetaData**

Replace the current `ensure_schema(schema_def, conninfo)` with:

```python
def ensure_schema(meta: MetaData, conninfo: str) -> None:
    """Create PostgreSQL schema and all tables from SQLAlchemy MetaData."""
    from sqlalchemy import create_engine, text

    engine = create_engine(f"postgresql+psycopg://?{_conninfo_to_dsn(conninfo)}")
    try:
        with engine.begin() as conn:
            # Create schema if not exists
            if meta.schema:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {meta.schema}"))
            # Create all tables (IF NOT EXISTS built-in)
            meta.create_all(engine)
    finally:
        engine.dispose()
```

Note: `_conninfo_to_dsn()` converts psycopg conninfo to SQLAlchemy DSN format. This needs to handle the format conversion (e.g., `host=localhost port=5433 dbname=mine2` → `host=localhost&port=5433&dbname=mine2`).

Alternatively, use `create_engine("postgresql+psycopg://", connect_args={"conninfo": conninfo})`.

**Step 2: Remove old migration functions**

Remove: `create_or_migrate_table()`, `create_table()`, `migrate_table_schema()`, `_table_exists()`, `_normalize_type_name()`, `_reconcile_primary_key()`, `_reconcile_unique_keys()`, `_drop_all_foreign_keys()`, `_ensure_indexes()`.

These are all replaced by `MetaData.create_all()` + Alembic for migrations.

**Step 3: Commit**

```bash
git add src/mine2/db/loader.py
git commit -m "refactor: rewrite ensure_schema to use SQLAlchemy MetaData.create_all()"
```

---

### Task 7: Rewrite bulk_upsert and bulk_insert

**Files:**
- Modify: `src/mine2/db/loader.py`

**Step 1: Update bulk_upsert signature**

Change from:
```python
def bulk_upsert(conninfo, schema, table, columns, rows, conflict_columns)
```

To:
```python
def bulk_upsert(
    conninfo: str,
    table: Table,
    columns: list[str],
    rows: list[tuple],
    conflict_columns: list[str],
) -> tuple[int, int]:
```

Internal SQL generation uses `table.name` and `table.schema` instead of separate `schema` and `table` string params.

**Step 2: Update bulk_insert signature**

Same pattern — accept `Table` object instead of separate schema/table strings.

**Step 3: Update delete_missing_entries signature**

Change from:
```python
def delete_missing_entries(conninfo, schema, pk_column, tables, keep_entry_ids)
```

To:
```python
def delete_missing_entries(
    conninfo: str,
    meta: MetaData,
    keep_entry_ids: list[str],
) -> int:
```

Uses `meta.info["entry_pk"]` for pk_column and `meta.sorted_tables` for table list.

**Step 4: Commit**

```bash
git add src/mine2/db/loader.py
git commit -m "refactor: update bulk_upsert/insert/delete to accept SA Table/MetaData"
```

---

### Task 8: Rewrite run_loader and run_loader_streaming

**Files:**
- Modify: `src/mine2/db/loader.py`

**Step 1: Update run_loader signature**

Change from:
```python
def run_loader(settings, schema_def: SchemaDef, jobs, process_func, ...)
```

To:
```python
def run_loader(
    settings: Settings,
    schema_name: str,
    jobs: list[Job],
    process_func: Callable[[Job, str, str], LoaderResult],
    max_workers: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
```

Workers receive `schema_name: str` instead of `SchemaDef`. Workers import from `mine2.models` to get MetaData.

**Step 2: Update run_loader_streaming similarly**

Same signature change.

**Step 3: Commit**

```bash
git add src/mine2/db/loader.py
git commit -m "refactor: update run_loader to pass schema_name instead of SchemaDef"
```

---

## Phase 3: Core Rewrite - base.py

### Task 9: Rewrite coerce_value to use SA types

**Files:**
- Modify: `src/mine2/pipelines/base.py`

**Step 1: Write test for SA-type-based coercion**

Create or modify test to validate coercion works with SA types:

```python
from sqlalchemy import ARRAY, BigInteger, Boolean, Date, DateTime, Double, Integer, Text
from mine2.pipelines.base import coerce_value

def test_coerce_text():
    assert coerce_value("hello", Text()) == "hello"

def test_coerce_integer():
    assert coerce_value("42", Integer()) == 42

def test_coerce_array_text():
    assert coerce_value("single", ARRAY(Text)) == ["single"]
```

**Step 2: Rewrite coerce_value**

Change from string-based dispatch:
```python
def coerce_value(value, col_type: str, is_pk: bool = False)
```

To SA-type-based dispatch:
```python
from sqlalchemy.types import TypeEngine

def coerce_value(value: Any, sa_type: TypeEngine, is_pk: bool = False) -> Any:
    """Coerce value based on SQLAlchemy column type."""
    if isinstance(sa_type, ARRAY):
        return _coerce_array_by_type(value, sa_type.item_type)
    if isinstance(sa_type, Text):
        return _coerce_string(value, is_pk)
    if isinstance(sa_type, String):  # char(N) etc.
        return _coerce_string(value, is_pk)
    if isinstance(sa_type, BigInteger):
        return _coerce_bigint(value, is_pk)
    if isinstance(sa_type, Integer):
        return _coerce_integer(value, is_pk)
    if isinstance(sa_type, Double):
        return _coerce_float(value, is_pk)
    if isinstance(sa_type, Float):
        return _coerce_float(value, is_pk)
    if isinstance(sa_type, Boolean):
        return _coerce_boolean(value)
    if isinstance(sa_type, Date):
        return _coerce_date(value)
    if isinstance(sa_type, DateTime):
        return _coerce_timestamp(value)
    if isinstance(sa_type, JSONB):
        return value  # passthrough
    return _coerce_string(value, is_pk)
```

Note: Check order matters — `BigInteger` before `Integer`, `Double` before `Float`.

Individual coercion functions (`_coerce_string`, `_coerce_integer`, etc.) remain unchanged.

Remove `_coerce_array_value()` string-based wrapper. Add `_coerce_array_by_type()`:

```python
def _coerce_array_by_type(value: Any, item_type: TypeEngine) -> Any:
    if value is None:
        return None
    if not isinstance(value, list):
        value = [value]
    return [coerce_value(v, item_type) for v in value if v is not None]
```

**Step 3: Run tests**

Run: `pixi run pytest tests/test_base.py -v`
Expected: Tests need updating (they use string types). Update in Task 14.

**Step 4: Commit**

```bash
git add src/mine2/pipelines/base.py
git commit -m "refactor: rewrite coerce_value to dispatch on SA type objects"
```

---

### Task 10: Rewrite transform_category

**Files:**
- Modify: `src/mine2/pipelines/base.py`

**Step 1: Update transform_category signature**

Change from:
```python
def transform_category(rows, table: TableDef, pk_value, pk_col, normalize_fn)
```

To:
```python
def transform_category(
    rows: list[dict[str, Any]],
    table: Table,
    pk_value: str,
    pk_col: str,
    normalize_fn: Callable[[str], str] | None = None,
) -> list[dict[str, Any]]:
```

Internal changes:
- `table.column_types` → `{col.name: col.type for col in table.columns}`
- `table.column_names` → `{col.name for col in table.columns}`
- `table.primary_key` → `[col.name for col in table.primary_key.columns]`
- `coerce_value(val, col_type_str)` → `coerce_value(val, col.type)`

**Step 2: Commit**

```bash
git add src/mine2/pipelines/base.py
git commit -m "refactor: rewrite transform_category to accept SA Table"
```

---

### Task 11: Rewrite sync_entry_tables and BasePipeline

**Files:**
- Modify: `src/mine2/pipelines/base.py`

**Step 1: Update sync_entry_tables**

Change from:
```python
def sync_entry_tables(conninfo, schema_def: SchemaDef, entry_id, table_rows)
```

To:
```python
def sync_entry_tables(
    conninfo: str,
    meta: MetaData,
    entry_id: str,
    table_rows: dict[str, list[dict[str, Any]]],
) -> tuple[int, int, int]:
```

Uses `meta.schema`, `meta.info["entry_pk"]`, and `get_table(meta, name)` internally.

**Step 2: Update BasePipeline**

Change `__init__` from:
```python
def __init__(self, settings, config, schema_def: SchemaDef)
```

To:
```python
def __init__(self, settings: Settings, config: PipelineConfig, meta: MetaData)
```

Store `self.meta` instead of `self.schema_def`.
Update `run()` to pass `schema_name` to `run_loader()`.
Update `process_job()` signature from `(Job, SchemaDef, str)` to `(Job, str, str)`.

**Step 3: Update BaseCifBatchPipeline similarly**

Same pattern. Update `_batch_insert()`, `_prune_stale_rows()` to use MetaData.

**Step 4: Commit**

```bash
git add src/mine2/pipelines/base.py
git commit -m "refactor: rewrite BasePipeline and sync_entry_tables for SA MetaData"
```

---

## Phase 4: Pipeline Updates

### Task 12: Update update.py command dispatcher

**Files:**
- Modify: `src/mine2/commands/update.py`

**Step 1: Replace load_schema_def with model imports**

Change from:
```python
from mine2.db.loader import load_schema_def
schema_def = load_schema_def(config.deffile)
ensure_schema(schema_def, conninfo)
```

To:
```python
from mine2.models import get_metadata
meta = get_metadata(schema_name)
ensure_schema(meta, conninfo)
```

Where `schema_name` is derived from the pipeline name (mapping may be needed for `-json` suffixes that share the same schema).

**Step 2: Update pipeline runner calls**

Pass `meta` to pipeline constructors instead of `schema_def`.

**Step 3: Commit**

```bash
git add src/mine2/commands/update.py
git commit -m "refactor: update command dispatcher to use SA models"
```

---

### Task 13: Update cc.py pipeline

**Files:**
- Modify: `src/mine2/pipelines/cc.py`

**Step 1: Replace SchemaDef/TableDef imports**

Change:
```python
from mine2.db.loader import SchemaDef, TableDef
```

To:
```python
from sqlalchemy import MetaData, Table
from mine2.db.loader import get_table, get_all_tables, get_entry_pk
```

**Step 2: Update all function signatures and usages**

- `schema_def.tables` → `get_all_tables(meta)`
- `schema_def.primary_key` → `get_entry_pk(meta)`
- `table.name` → `table.name` (unchanged)
- `table.column_names` → `get_column_names(table)` or `{c.name for c in table.columns}`
- `schema_def` param in workers → `schema_name: str` + import in worker

**Step 3: Handle worker process pickling**

Worker functions currently receive `schema_def`. Change to receive `schema_name: str`:

```python
def _parse_cif_block(block, schema_name: str):
    from mine2.models import get_metadata
    meta = get_metadata(schema_name)
    entry_pk = get_entry_pk(meta)
    # ...
```

**Step 4: Commit**

```bash
git add src/mine2/pipelines/cc.py
git commit -m "refactor: update cc pipeline to use SA MetaData"
```

---

### Task 14: Update remaining pipelines (batch)

**Files:**
- Modify: `src/mine2/pipelines/pdbj.py`
- Modify: `src/mine2/pipelines/prd.py`
- Modify: `src/mine2/pipelines/vrpt.py`
- Modify: `src/mine2/pipelines/contacts.py`
- Modify: `src/mine2/pipelines/ccmodel.py`
- Modify: `src/mine2/pipelines/sifts.py`
- Modify: `src/mine2/pipelines/emdb.py`
- Modify: `src/mine2/pipelines/ihm.py`

Apply the same pattern as Task 13 to all remaining pipelines:

1. Replace `SchemaDef`/`TableDef` imports with `MetaData`/`Table` + helper imports
2. Update function signatures
3. Update worker functions to import models by schema_name
4. Update property accesses (see Task 13 mapping)

Each pipeline follows one of these patterns:
- **Standard file-based** (pdbj, vrpt, emdb, ihm): `BasePipeline` subclass, `process_job(job, schema_name, conninfo)`
- **Batch CIF** (ccmodel, prd): `BaseCifBatchPipeline` subclass, worker receives `schema_name`
- **Custom** (contacts): Minimal schema usage, update `sync_entry_tables()` call
- **Custom** (sifts): Uses `bulk_upsert()` directly, update call signature

**Commit per pipeline or batch:**

```bash
git add src/mine2/pipelines/*.py
git commit -m "refactor: update all pipelines to use SA MetaData"
```

---

## Phase 5: Alembic Setup

### Task 15: Initialize Alembic

**Files:**
- Create: `alembic.ini`
- Create: `alembic/env.py`
- Create: `alembic/script.py.mako`
- Create: `alembic/versions/` (directory)

**Step 1: Initialize Alembic**

Run: `pixi run alembic init alembic`
Expected: alembic/ directory and alembic.ini created

**Step 2: Configure alembic.ini**

Set `sqlalchemy.url` to use config.yml connection string or environment variable:
```ini
sqlalchemy.url = postgresql+psycopg://pdbj@localhost:5433/mine2
```

Or better, configure in env.py to read from mine2 config.

**Step 3: Configure env.py for multi-schema**

```python
from mine2.models import ALL_METADATA
from sqlalchemy import MetaData

# Combine all schema MetaData
target_metadata = MetaData()
for meta in ALL_METADATA.values():
    for table in meta.tables.values():
        table.to_metadata(target_metadata)

def include_name(name, type_, parent_names):
    """Include all mine2 schemas in migration."""
    if type_ == "schema":
        return name in {m.schema for m in ALL_METADATA.values()}
    return True
```

Set `include_schemas=True` in `context.configure()` and add `include_name` filter.

**Step 4: Create initial migration (baseline)**

Run: `pixi run alembic revision --autogenerate -m "initial schema"`
Expected: Migration file created in alembic/versions/

Or if DB already has tables:
Run: `pixi run alembic stamp head`
Expected: alembic_version table created with current head

**Step 5: Add alembic commands to pixi**

Add to pixi.toml:
```toml
[tasks]
alembic = "alembic"
db-migrate = "alembic revision --autogenerate"
db-upgrade = "alembic upgrade head"
```

**Step 6: Commit**

```bash
git add alembic/ alembic.ini
git commit -m "feat: set up Alembic for schema migration management"
```

---

## Phase 6: Config & Cleanup

### Task 16: Update config.py

**Files:**
- Modify: `src/mine2/config.py`

**Step 1: Remove deffile from PipelineConfig**

The `deffile` field in `PipelineConfig` is no longer needed since schemas are defined in Python code.

However, keep the field as optional/deprecated if config.yml still has it, or remove it and update config.yml.

**Step 2: Add schema_name mapping**

Add a pipeline-to-schema mapping if pipeline names don't match schema names:

```python
PIPELINE_SCHEMA_MAP: dict[str, str] = {
    "pdbj": "pdbj",
    "pdbj-json": "pdbj",
    "cc": "cc",
    "cc-json": "cc",
    "ccmodel": "ccmodel",
    "ccmodel-json": "ccmodel",
    "prd": "prd",
    "prd-json": "prd",
    "vrpt": "vrpt",
    "contacts": "contacts",
    "sifts": "sifts",
    "emdb": "emdb",
    "ihm": "ihm",
}
```

**Step 3: Commit**

```bash
git add src/mine2/config.py
git commit -m "refactor: remove deffile from PipelineConfig, add schema mapping"
```

---

### Task 17: Remove YAML schema files

**Files:**
- Delete: `schemas/*.def.yml`

**Step 1: Verify all tests pass without YAML**

Run: `pixi run pytest -v`
Expected: All pass (no code references YAML files anymore)

**Step 2: Remove YAML files**

```bash
git rm schemas/cc.def.yml schemas/ccmodel.def.yml schemas/contacts.def.yml \
       schemas/emdb.def.yml schemas/ihm.def.yml schemas/pdbj.def.yml \
       schemas/prd.def.yml schemas/prd_family.def.yml schemas/sifts.def.yml \
       schemas/vrpt.def.yml
```

Keep `schemas/pkout.json` if it's still used.

**Step 3: Remove pyyaml dependency** (if not used elsewhere)

Check for other YAML usage first:
```bash
grep -r "import yaml" src/
```

If only used for schema loading, remove from dependencies.

**Step 4: Commit**

```bash
git commit -m "chore: remove YAML schema files (replaced by SQLAlchemy models)"
```

---

### Task 18: Update config.yml

**Files:**
- Modify: `config.yml`

**Step 1: Remove deffile entries from pipeline configs**

Remove `deffile: schemas/xxx.def.yml` from each pipeline config.

**Step 2: Commit**

```bash
git add config.yml
git commit -m "chore: remove deffile from pipeline configs"
```

---

## Phase 7: Test Updates

### Task 19: Update test_loader_migration.py

**Files:**
- Modify: `tests/test_loader_migration.py`

**Step 1: Remove tests for deleted functions**

Remove tests for: `_normalize_type_name`, `_drop_all_foreign_keys` PK/FK migration behaviors that are now handled by Alembic.

**Step 2: Add tests for new loader functions**

Test `ensure_schema()` with MetaData, `get_entry_pk()`, `get_table()`, `get_column_types()`.

**Step 3: Update remaining tests**

Update `TestDeleteMissingEntries` and `TestPruneStaleRows` to use MetaData instead of SchemaDef.

**Step 4: Commit**

```bash
git add tests/test_loader_migration.py
git commit -m "test: update loader migration tests for SA MetaData"
```

---

### Task 20: Update test_base.py and pipeline tests

**Files:**
- Modify: `tests/test_base.py`
- Modify: `tests/test_pdbj.py`, `tests/test_pdbj_cif.py`
- Modify: `tests/test_cc_cif.py`, `tests/test_ccmodel_cif.py`, `tests/test_prd_cif.py`
- Modify: `tests/test_format_parity.py`
- Modify: Other test files as needed

**Step 1: Update test_base.py**

Replace `TableDef(...)` construction in tests with SA `Table(...)` construction:

```python
# Before
table = TableDef(
    name="test_table",
    columns=[("id", "text"), ("value", "integer")],
    primary_key=["id"],
)

# After
from sqlalchemy import Column, Integer, MetaData, PrimaryKeyConstraint, Table, Text
meta = MetaData(schema="test")
table = Table(
    "test_table", meta,
    Column("id", Text),
    Column("value", Integer),
    PrimaryKeyConstraint("id"),
)
```

**Step 2: Update coerce_value test calls**

Change from string types to SA types:
```python
# Before
coerce_value("42", "integer")

# After
coerce_value("42", Integer())
```

**Step 3: Update conftest.py fixtures**

Schema fixtures that use `load_schema_def()` → import from `mine2.models`.

**Step 4: Run full test suite**

Run: `pixi run pytest -v`
Expected: All pass

**Step 5: Commit**

```bash
git add tests/
git commit -m "test: update all tests for SA MetaData migration"
```

---

### Task 21: Update CLAUDE.md and documentation

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md` (if exists)

**Step 1: Update CLAUDE.md**

- Update "Project Structure" section: add `models/` directory, remove `schemas/` YAML references
- Update "Key Patterns" section: replace YAML examples with SA Table examples
- Add Alembic usage section
- Update development commands (add `db-migrate`, `db-upgrade`)

**Step 2: Update CHANGELOG**

Add entry under `[Unreleased]`:
```markdown
### Changed
- Schema definitions migrated from YAML to SQLAlchemy Core Table objects
- Added Alembic for database migration management
- Removed custom SchemaDef/TableDef dataclasses

### Removed
- YAML schema definition files (schemas/*.def.yml)
- Custom DDL generation and migration code in loader.py
```

**Step 3: Commit**

```bash
git add CLAUDE.md README.md CHANGELOG.md
git commit -m "docs: update documentation for SQLAlchemy schema migration"
```

---

## Execution Notes

### Dependencies Between Tasks

- Tasks 1-3 are sequential (setup → converter → generate)
- Tasks 4-8 are sequential (loader rewrite)
- Tasks 9-11 are sequential (base.py rewrite)
- Task 12 depends on Tasks 8 and 11
- Tasks 13-14 depend on Task 12
- Task 15 depends on Task 3 (models must exist)
- Tasks 16-18 depend on Tasks 13-14 (all pipelines updated)
- Tasks 19-20 can be partially parallelized
- Task 21 is last

### Risk Mitigation

1. **DDL equivalence**: Task 3 Step 3 verifies generated models match YAML exactly
2. **Type mapping**: Task 5 has comprehensive unit tests
3. **Pickle safety**: Workers import models by name instead of receiving pickled objects
4. **Incremental verification**: Run `pixi run pytest` after each phase

### Estimated Scope

- ~10 new files (models/*.py + converter + type_utils + alembic)
- ~15 modified files (loader, base, 9 pipelines, update, config, tests)
- ~10 deleted files (YAML schemas)
- Total: ~35 file operations

---
- [ ] **DONE** - Plan complete
