# mine2updater-ng

PDBj (Protein Data Bank Japan) のデータを PostgreSQL にロードする CLI ツール。

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: Pixi (Conda/PyPI hybrid)
- **Database**: PostgreSQL 12+ (psycopg3)
- **CLI**: Typer + Rich
- **Config**: Pydantic
- **Parser**: gemmi (CIF and mmJSON unified)
- **Chemistry**: RDKit PostgreSQL cartridge + ccd2rdmol

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

### CIF Pipelines (Default)

CIF is the default format for dual-format pipelines:

| Pipeline | Source | Notes |
|----------|--------|-------|
| pdbj | `divided/mmCIF/*.cif.gz` | File-based (~248k files), atom_site skipped |
| cc | `components.cif.gz` | Single file, ~40k blocks |
| ccmodel | `chem_comp_model.cif.gz` | Single file |
| prd | `prd-all.cif.gz` + `prdcc-all.cif.gz` | Dual file (PRD + PRDCC) |
| vrpt | `validation_reports/**/*.cif.gz` | Uses gemmi.CifWalk for nested directory structure |
| contacts | `contacts/**/*.json` | Array format, not mmJSON |

### mmJSON Pipelines (Optional)

For users who prefer mmJSON format, use the `-json` suffix:

| Pipeline | Format | Notes |
|----------|--------|-------|
| pdbj-json | mmJSON | Merges noatom + plus files via merge_data() |
| cc-json | mmJSON | Chemical component dictionary |
| ccmodel-json | mmJSON | Component 3D models |
| prd-json | mmJSON | Has TWO data blocks (PRD + PRDCC) |

### Backward Compatibility

Legacy pipeline names (`pdbj-cif`, `cc-cif`, etc.) are still accepted but deprecated.
They emit a warning and run the corresponding CIF pipeline.

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

# mmJSON: needs normalization
rows = transform_category(rows, table, pk_value, pk_col, normalize_column_name)

# CIF: no normalization needed (pass None)
rows = transform_category(rows, table, pk_value, pk_col, None)
```

### Chemical SMILES Generation (cc pipeline)
Both CIF and mmJSON cc pipelines generate canonical SMILES using ccd2rdmol + RDKit.
This ensures consistent SMILES quality regardless of input format:
```python
# Both CIF and mmJSON use the same approach:
# gemmi reads the file into a CIF-like block, then ccd2rdmol generates SMILES
from ccd2rdmol import read_ccd_block

# gemmi can read both CIF and mmJSON
block = gemmi.cif.read(cif_path)[0]       # CIF
block = gemmi.cif.read_mmjson(json_path)[0]  # mmJSON

# ccd2rdmol works on the gemmi block directly
result = read_ccd_block(block, sanitize_mol=True, add_conformers=False)
smiles = Chem.MolToSmiles(result.mol, canonical=True)
```

Note: The SMILES in `pdbx_chem_comp_descriptor` is NOT used. SMILES is always
generated from the molecular structure for consistency and quality.

### RDKit PostgreSQL Cartridge
Chemical searches use RDKit extension (auto-configured on `cc`/`cc-json` pipeline run):
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
