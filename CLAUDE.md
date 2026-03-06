# pdb-mine-builder

PDBj (Protein Data Bank Japan) のデータを PostgreSQL にロードする CLI ツール。

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: Pixi (Conda/PyPI hybrid)
- **Database**: PostgreSQL 17+ (psycopg3)
- **Schema**: SQLAlchemy Core (DDL only) + Alembic (migrations)
- **CLI**: Typer + Rich
- **Config**: Pydantic
- **Parser**: gemmi (CIF and mmJSON unified)
- **Chemistry**: RDKit PostgreSQL cartridge + ccd2rdmol

## Quick Start

```bash
pixi install
pixi run pmb --help
pixi run pmb update pdbj --limit 10
```

## Project Structure

```
src/pdbminebuilder/
├── __init__.py
├── __main__.py             # Entry point
├── cli.py                  # Typer CLI commands (9 commands)
├── config.py               # Pydantic settings
├── models/
│   ├── __init__.py         # MetaData registry (ALL_METADATA, get_metadata())
│   ├── cc.py               # cc schema (10 tables)
│   ├── ccmodel.py          # ccmodel schema
│   ├── contacts.py         # contacts schema
│   ├── emdb.py             # emdb schema (schema only, no pipeline)
│   ├── ihm.py              # ihm schema (schema only, no pipeline)
│   ├── pdbj.py             # pdbj schema (~400 tables)
│   ├── prd.py              # prd schema
│   ├── prd_family.py       # prd_family schema
│   └── vrpt.py             # vrpt schema
├── db/
│   ├── connection.py       # psycopg3 connection pool
│   ├── delta.py            # Delta computing
│   ├── loader.py           # Parallel loader (ProcessPoolExecutor)
│   ├── metadata.py         # Entry metadata tracking (mtime-based skip)
│   └── _type_utils.py      # SA type to PostgreSQL type converter
├── parsers/
│   ├── cif.py              # Unified parser (CIF + mmJSON via gemmi)
│   └── mmjson.py           # Utilities: normalize_column_name(), merge_data()
└── pipelines/
    ├── base.py             # BasePipeline + transform_category()
    ├── pdbj.py             # Main PDB data (CIF/mmJSON)
    ├── cc.py               # Chemical components
    ├── ccmodel.py          # Chemical component models
    ├── prd.py              # BIRD data (dual data blocks)
    ├── vrpt.py             # Validation reports (CIF)
    └── contacts.py         # Contact data (custom JSON)
alembic/                    # Alembic migration config
├── env.py                  # Multi-schema support
└── versions/               # Migration scripts
docker/
├── docker-compose.test.yml # Test DB (PostgreSQL + RDKit)
└── init/
    └── 01-extensions.sql   # RDKit extension setup
scripts/                    # One-shot utility scripts
tests/                      # Unit + integration tests (pytest)
docs/                       # Architecture docs
```

## Pipelines

### Pipeline List

| Pipeline | Default Format | Notes |
|----------|---------------|-------|
| pdbj | CIF | File-based (~248k files), atom_site skipped |
| cc | CIF | Single file (components.cif.gz), ~40k blocks |
| ccmodel | CIF | Single file (chem_comp_model.cif.gz) |
| prd | CIF | Dual file (prd-all.cif.gz + prdcc-all.cif.gz) |
| vrpt | CIF | Uses gemmi.CifWalk for nested directory structure |
| contacts | JSON | Array format, not mmJSON |
| emdb | - | Schema only, no pipeline implementation |
| ihm | - | Schema only, no pipeline implementation |

### Format Selection (Dual-Format Pipelines)

Pipelines pdbj, cc, ccmodel, prd support both CIF and mmJSON.
Format is selected via `format` field in `config.yml`:

```yaml
pipelines:
  pdbj:
    format: cif          # "cif" (default) or "mmjson"
    data: /path/to/data/
```

### Backward Compatibility

Legacy pipeline names (`pdbj-cif`, `cc-cif`, `pdbj-json`, `cc-json`, etc.)
are still accepted but deprecated. They emit a warning and resolve to the
base pipeline name. Note: `-json` aliases resolve to the base name but do NOT
change the `format` config — users must set `format: mmjson` in config.yml.

### Mtime-Based Skip Optimization

The `entry_metadata` table tracks file modification times. During incremental
updates, unchanged entries are automatically skipped. Use `--force` flag to
bypass mtime checks and reprocess all entries.

## CLI Commands

```bash
pixi run pmb sync <target>           # Sync data via rsync
pixi run pmb update <pipeline>       # Incremental update (--limit, --workers, --force)
pixi run pmb load <pipeline>         # Bulk load via COPY protocol (initial load)
pixi run pmb all                     # Full sync + update cycle
pixi run pmb setup-rdkit             # Setup RDKit extension
pixi run pmb test [pipeline...]      # Run test pipelines against test DB
pixi run pmb reset <schema|all>      # Drop and reset schemas
pixi run pmb stats                   # Show database statistics
pixi run pmb --version               # Show version
```

## Key Patterns

### Unified Parsing (gemmi)
Both CIF and mmJSON are parsed via gemmi, returning row-oriented dicts:
```python
from pdbminebuilder.parsers.cif import parse_cif_file, parse_mmjson_file

# CIF files (supports .cif.gz)
data = parse_cif_file(filepath)

# mmJSON files (supports .json.gz)
data = parse_mmjson_file(filepath)

# Both return: {"category": [{"col": "val", ...}, ...], "_block_name": "..."}
```

### Column Name Normalization
mmJSON uses `column[1][2]` → schema uses `column12`
```python
from pdbminebuilder.parsers.mmjson import normalize_column_name
```

### Schema Access (SQLAlchemy Core)
Schema definitions use SQLAlchemy Core Table objects with metadata:
```python
from pdbminebuilder.models import get_metadata, ALL_METADATA
from pdbminebuilder.db.loader import get_table, get_all_tables, get_entry_pk

meta = get_metadata("cc")                 # MetaData with schema="cc"
table = get_table(meta, "brief_summary")   # SA Table object
pk = get_entry_pk(meta)                    # "comp_id"
tables = get_all_tables(meta)              # All tables in schema

# Schema/table config stored in .info dicts
meta.info["entry_pk"]                      # Schema-level primary key
table.info["keywords"]                     # Table-level keywords list
```

### Category Transformation
```python
from pdbminebuilder.pipelines.base import transform_category

# mmJSON: needs normalization
rows = transform_category(rows, table, pk_value, pk_col, normalize_column_name)

# CIF: no normalization needed (pass None)
rows = transform_category(rows, table, pk_value, pk_col, None)
```

### Chemical SMILES Generation (cc pipeline)
Both CIF and mmJSON cc pipelines generate canonical SMILES using ccd2rdmol + RDKit.
This ensures consistent SMILES quality regardless of input format:
```python
from ccd2rdmol import read_ccd_block

block = gemmi.cif.read(cif_path)[0]          # CIF
block = gemmi.cif.read_mmjson(json_path)[0]   # mmJSON

result = read_ccd_block(block, sanitize_mol=True, add_conformers=False)
smiles = Chem.MolToSmiles(result.mol, canonical=True)
```

Note: The SMILES in `pdbx_chem_comp_descriptor` is NOT used. SMILES is always
generated from the molecular structure for consistency and quality.

### RDKit PostgreSQL Cartridge
Chemical searches use RDKit extension (auto-configured on `cc` pipeline run):
```sql
-- Substructure search
SELECT * FROM cc.brief_summary WHERE mol @> 'c1ccccc1'::mol;

-- Similarity search (Tanimoto)
SELECT *, tanimoto_sml(morganbv_fp(mol), morganbv_fp('CCO'::mol))
FROM cc.brief_summary WHERE morganbv_fp(mol) % morganbv_fp('CCO'::mol);
```

### Parallel Processing
- Workers create own DB connections (not pool)
- `ProcessPoolExecutor` with configurable worker count

## Development

```bash
pixi run lint          # ruff check
pixi run format        # ruff format
pixi run test          # pytest (unit tests)
pixi run check         # all checks (lint, format)
```

### Testing

**IMPORTANT**: テスト実行前に必ず Docker の test DB を起動すること。

```bash
# 1. Test DB を起動 (PostgreSQL + RDKit)
pixi run test-db-up

# 2. Test DB の状態確認
pixi run test-db-status

# 3. テスト実行
pixi run test              # All tests
pixi run test-unit         # Unit tests only
pixi run test-integration  # Integration tests (requires test DB)

# 4. Test DB を停止
pixi run test-db-down
```

Test DB details:
- Image: `mcs07/postgres-rdkit:latest` (PostgreSQL 17 + RDKit)
- Container: `pmb-postgres-test`
- Port: `15433`
- Database: `pmb_test`
- Config: `config.test.yml`

### Database Migrations (Alembic)

```bash
pixi run db-migrate "description"  # Generate migration
pixi run db-upgrade                # Apply all pending migrations
pixi run db-downgrade              # Rollback last migration
pixi run db-history                # Show migration history
```

Alembic is configured for multi-schema support (all 9 schemas).
Schema DDL is defined in `src/pdbminebuilder/models/` as SQLAlchemy Core Table objects.
Data operations still use psycopg3 direct connections (no SQLAlchemy Engine for data).

## Database

```bash
pixi run db-start      # Start PostgreSQL
pixi run db-stop       # Stop PostgreSQL
pixi run db-status     # Show PostgreSQL status
```

Connection: `config.yml` の `rdb.constring`

### Bulk Load Mode

For initial data loading, use bulk load mode to significantly improve performance:

```bash
# 1. Start PostgreSQL
pixi run db-start

# 2. Enable bulk load mode (disables fsync, autovacuum)
pixi run db-bulkload-mode

# 3. Run data loading
pixi run pmb load cc
pixi run pmb load pdbj
# ... other pipelines

# 4. Restore safe settings
pixi run db-safe-mode

# 5. Run VACUUM ANALYZE
psql -c "VACUUM ANALYZE;"
```

**WARNING**: Bulk load mode disables crash safety. If PostgreSQL crashes during bulk load:
```bash
pixi run db-stop
rm -rf $PGDATA
pixi run db-init
# Re-run data loading from scratch
```

## Configuration

- `config.yml` - Production config (customize locally)
- `config.test.yml` - Test config (uses fixture data with `${CWD}` expansion)
- `.env` - Environment variables (gitignored)
- `.env.example` - Template

## Known Issues

- Global connection pool is for main process only; workers use direct connections
- Workers receive `schema_name: str` and import models inside worker function (avoids pickling SA objects)
- `emdb` and `ihm` have schema definitions but no pipeline implementations yet
