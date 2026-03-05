# mine2updater-ng

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
- **Test DB**: Docker (mcs07/postgres-rdkit)

## Quick Start

```bash
pixi install
pixi run mine2 --help
pixi run mine2 update pdbj --limit 10
```

## Project Structure

```
src/mine2/
├── cli.py              # Typer CLI commands
├── config.py           # Pydantic settings
├── commands/
│   ├── update.py       # update command (incremental delta sync)
│   ├── load.py         # load command (TRUNCATE + COPY bulk load)
│   ├── sync.py         # sync command (rsync from PDBj)
│   ├── reset.py        # reset command (drop/recreate schemas)
│   ├── stats.py        # stats command
│   ├── test.py         # test command (limited data)
│   └── utils.py        # Legacy alias resolution
├── models/
│   ├── __init__.py     # MetaData registry (ALL_METADATA, get_metadata())
│   ├── pdbj.py         # pdbj schema (~400 tables)
│   ├── cc.py           # cc schema (10 tables)
│   ├── ccmodel.py      # ccmodel schema
│   ├── contacts.py     # contacts schema
│   ├── prd.py          # prd schema
│   ├── prd_family.py   # prd_family schema
│   ├── vrpt.py         # vrpt schema
│   ├── sifts.py        # sifts schema
│   ├── emdb.py         # emdb schema (schema only)
│   └── ihm.py          # ihm schema (schema only)
├── db/
│   ├── connection.py   # Connection pool (main process only)
│   ├── loader.py       # Parallel loader (ProcessPoolExecutor)
│   ├── metadata.py     # Pipeline/entry metadata tracking (mtime)
│   ├── delta.py        # Delta detection (insert/update/delete)
│   └── _type_utils.py  # SA type to PostgreSQL type converter
├── parsers/
│   ├── cif.py          # Unified parser (CIF + mmJSON via gemmi)
│   └── mmjson.py       # Utilities: normalize_column_name(), merge_data()
├── pipelines/
│   ├── base.py         # BasePipeline + transform_category() + sync_entry_tables()
│   ├── pdbj.py         # Main PDB data (CIF/mmJSON + plus data)
│   ├── cc.py           # Chemical components (SMILES generation)
│   ├── ccmodel.py      # Chemical component models
│   ├── prd.py          # BIRD data (dual data blocks)
│   ├── vrpt.py         # Validation reports (CIF, gemmi.CifWalk)
│   ├── contacts.py     # Contact data (custom JSON)
│   └── sifts.py        # SIFTS cross-references (TTL)
├── utils/
│   ├── assembly.py     # Assembly-related utilities
│   ├── brief_summary.py # Brief summary processing
│   └── patches.py      # Data patches
alembic/                # Alembic migration config (multi-schema)
docker/                 # Docker Compose for test DB
scripts/                # PostgreSQL configs, RDKit init, utility scripts
tests/                  # Unit + integration tests
└── integration/        # DB integration tests (requires Docker)
docs/                   # Architecture docs
```

## Pipelines

| Pipeline | Format | Type | Notes |
|----------|--------|------|-------|
| pdbj | CIF/mmJSON | File-per-entry | ~248k files, atom_site skipped, mtime skip |
| cc | CIF/mmJSON | Single file | components.cif.gz, ~40k blocks |
| ccmodel | CIF/mmJSON | Single file | chem_comp_model.cif.gz |
| prd | CIF/mmJSON | Single file | Dual file (prd-all + prdcc-all) |
| vrpt | CIF | File-per-entry | gemmi.CifWalk, nested dirs, mtime skip |
| contacts | JSON | File-per-entry | Array format (not mmJSON), mtime skip |
| sifts | TTL | Single file | SIFTS cross-references |
| emdb | XML | - | Schema defined, pipeline not implemented |
| ihm | mmJSON | - | Schema defined, pipeline not implemented |

### Format Selection (Dual-Format Pipelines)

pdbj, cc, ccmodel, prd support both CIF and mmJSON via `format` field in `config.yml`:

```yaml
pipelines:
  pdbj:
    format: cif          # "cif" (default) or "mmjson"
    data: /path/to/data/
```

Legacy names (`pdbj-cif`, `cc-json`, etc.) are accepted but deprecated.

### Mtime-Based Skip Optimization

File-per-entry pipelines (pdbj, vrpt, contacts) track file modification times
in `public.entry_metadata` table. Unchanged files are skipped on subsequent runs.
Use `--force` to bypass.

## Key Patterns

### Unified Parsing (gemmi)
```python
from mine2.parsers.cif import parse_cif_file, parse_mmjson_file

data = parse_cif_file(filepath)       # CIF (supports .cif.gz)
data = parse_mmjson_file(filepath)    # mmJSON (supports .json.gz)
# Both return: {"category": [{"col": "val", ...}, ...], "_block_name": "..."}
```

### Schema Access (SQLAlchemy Core)
```python
from mine2.models import get_metadata, ALL_METADATA
from mine2.db.loader import get_table, get_all_tables, get_entry_pk

meta = get_metadata("cc")              # MetaData with schema="cc"
meta.schema                            # "cc" (use this for schema_name: str params)
table = get_table(meta, "brief_summary")
pk = get_entry_pk(meta)                # "comp_id"

# Config stored in .info dicts
meta.info["entry_pk"]                  # Schema-level primary key
table.info["keywords"]                 # Table-level keywords list
```

**Important**: Use `meta.schema` (not `meta.schema_name`) to get the schema name string.

### Category Transformation
```python
from mine2.pipelines.base import transform_category

rows = transform_category(rows, table, pk_value, pk_col, normalize_column_name)  # mmJSON
rows = transform_category(rows, table, pk_value, pk_col, None)                  # CIF
```

### Chemical SMILES Generation (cc pipeline)
```python
from ccd2rdmol import read_ccd_block

block = gemmi.cif.read(cif_path)[0]        # CIF
block = gemmi.cif.read_mmjson(json_path)[0] # mmJSON

result = read_ccd_block(block, sanitize_mol=True, add_conformers=False)
smiles = Chem.MolToSmiles(result.mol, canonical=True)
```

SMILES is always generated from molecular structure, not from `pdbx_chem_comp_descriptor`.

### Parallel Processing
- Workers create own DB connections (not pool)
- `ProcessPoolExecutor` with configurable worker count
- Workers receive `schema_name: str` and import models inside worker function (avoids pickling SA objects)

## Development

### Code Quality

```bash
pixi run lint          # ruff check
pixi run format        # ruff format
pixi run typecheck     # ty check
pixi run check         # all checks (lint, format, typecheck)
```

### Testing (MANDATORY)

**Both unit tests AND integration tests must pass before creating a PR.**

```bash
# Unit tests (no DB required)
pixi run test-unit

# Integration tests (requires Docker test DB)
pixi run test-db-up              # Start test DB (Docker, port 15433)
pixi run test                    # Run ALL tests (unit + integration)
pixi run test-db-down            # Stop test DB

# Check test DB status
pixi run test-db-status
```

Test DB connection: `host=localhost port=15433 dbname=mine2_test user=pdbj password=test_password`

Integration test fixtures (`tests/conftest.py`):
- `db_connection` - Session-scoped connection string
- `pdbj_schema`, `cc_schema`, `ccmodel_schema`, `prd_schema` - Auto-cleanup after each test

### Database Migrations (Alembic)

```bash
pixi run db-migrate "description"  # Generate migration
pixi run db-upgrade                # Apply all pending migrations
pixi run db-downgrade              # Rollback last migration
pixi run db-history                # Show migration history
```

Alembic is configured for multi-schema support (all 10 schemas).
Schema DDL is defined in `src/mine2/models/` as SQLAlchemy Core Table objects.

## Database

### Local PostgreSQL

```bash
pixi run db-start      # Start PostgreSQL (port 5433)
pixi run db-stop       # Stop PostgreSQL
```

Connection: `config.yml` の `rdb.constring`

### Bulk Load Mode

```bash
pixi run db-bulkload-mode    # Disable fsync, autovacuum (UNSAFE)
pixi run mine2 load cc pdbj  # Bulk load with COPY protocol
pixi run db-safe-mode        # Restore safe settings
psql -c "VACUUM ANALYZE;"
```

**WARNING**: Bulk load mode disables crash safety. If PostgreSQL crashes,
data must be reloaded from scratch.

## Configuration

- `config.yml` - Production config (gitignored)
- `config.test.yml` - Test config
- `.env` / `.env.example` - Environment variables

## Known Issues

- `ty check` warns about psycopg's `LiteralString` type (runtime OK)
- Global connection pool is for main process only; workers use direct connections
