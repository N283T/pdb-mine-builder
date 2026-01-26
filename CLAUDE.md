# mine2updater-ng

PDBj (Protein Data Bank Japan) のデータを PostgreSQL にロードする CLI ツール。

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: Pixi (Conda/PyPI hybrid)
- **Database**: PostgreSQL 12+ (psycopg3)
- **CLI**: Typer + Rich
- **Config**: Pydantic
- **Parser**: gemmi (CIF and mmJSON unified)

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
├── db/
│   ├── connection.py   # Connection pool
│   └── loader.py       # Parallel loader (ProcessPoolExecutor)
├── parsers/
│   ├── cif.py          # Unified parser (CIF + mmJSON via gemmi)
│   └── mmjson.py       # Utilities: normalize_column_name(), merge_data()
├── pipelines/
│   ├── base.py         # BasePipeline + transform_category()
│   ├── pdbj.py         # Main PDB data (mmJSON + plus)
│   ├── cc.py           # Chemical components
│   ├── ccmodel.py      # Chemical component models
│   ├── prd.py          # BIRD data (dual data blocks)
│   ├── vrpt.py         # Validation reports (CIF)
│   └── contacts.py     # Contact data (custom JSON)
schemas/                # YAML schema definitions
tests/                  # Unit tests (pytest)
docs/                   # Architecture docs
```

## Pipelines

| Pipeline | Format | Notes |
|----------|--------|-------|
| pdbj | mmJSON | Merges noatom + plus files via merge_data() |
| cc | mmJSON | Chemical component dictionary |
| ccmodel | mmJSON | Component 3D models |
| prd | mmJSON | Has TWO data blocks (PRD + PRDCC) |
| vrpt | CIF | Uses gemmi.CifWalk for nested directory structure |
| contacts | JSON | Array format, not mmJSON |

## Key Patterns

### Unified Parsing (gemmi)
Both CIF and mmJSON are parsed via gemmi, returning row-oriented dicts:
```python
from mine2.parsers.cif import parse_cif_file, parse_mmjson_file

# CIF files (supports .cif.gz)
data = parse_cif_file(filepath)

# mmJSON files (supports .json.gz)
data = parse_mmjson_file(filepath)

# Both return: {"category": [{"col": "val", ...}, ...], "_block_name": "..."}
```

### Column Name Normalization
mmJSON uses `column[1][2]` → schema uses `column12`
```python
from mine2.parsers.mmjson import normalize_column_name
```

### Category Transformation
```python
from mine2.pipelines.base import transform_category
rows = transform_category(rows, table, pk_value, pk_col, normalize_column_name)
```

### Parallel Processing
- Workers create own DB connections (not pool)
- `ProcessPoolExecutor` with configurable worker count

## Development

```bash
pixi run lint          # ruff check
pixi run format        # ruff format
pixi run typecheck     # ty check
pixi run test          # pytest
pixi run check         # all checks (lint, format, typecheck)
```

## Database

```bash
pixi run db-start      # Start PostgreSQL
pixi run db-stop       # Stop PostgreSQL
```

Connection: `config.yml` の `rdb.constring`

## Configuration

- `config.yml` - Production config (gitignored)
- `config.test.yml` - Test config
- `.env` - Environment variables (gitignored)
- `.env.example` - Template

## Known Issues

- `ty check` warns about psycopg's `LiteralString` type (runtime OK)
- Global connection pool is for main process only; workers use direct connections
