# MINE2 Updater

RDB updater for MINE2 database. Synchronizes structural biology data from PDBj (Protein Data Bank Japan) via rsync and loads it into PostgreSQL.

## Features

- Multi-process parallel data loading with configurable workers
- Schema-driven database management from YAML definitions
- Support for multiple data formats (CIF default, mmJSON optional)
- 10 data pipelines: CIF default for dual-format pipelines, `-json` suffix for mmJSON
- Works seamlessly with wwPDB/PDBj mirrored data

## Requirements

- Python 3.12+
- PostgreSQL 17+ with RDKit extension
- [Pixi](https://pixi.sh/) (package manager)
- rsync (for data synchronization)

## Installation

```bash
git clone https://github.com/N283T/mine2updater-ng.git
cd mine2updater-ng
pixi install
```

## Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Default PostgreSQL settings are in `pixi.toml` (`[activation.env]`).

## Configuration

Copy and edit `config.yml`:

```yaml
rdb:
  nworkers: 8
  constring: "dbname='mine2' user='pdbj' port=5433"

pipelines:
  pdbj:
    deffile: ${CWD}schemas/pdbj.def.yml
    data: /path/to/pdb/mmjson-noatom/
    data-plus: /path/to/pdb/mmjson-plus/
  cc:
    deffile: ${CWD}schemas/cc.def.yml
    data: /path/to/cc/mmjson/
  # ... other pipelines
```

- `${CWD}` resolves to the repository root
- `config.test.yml` is used for testing with limited data

## Usage

```bash
# Show help
pixi run mine2 --help

# Sync data from PDBj
pixi run mine2 sync [targets...]
# Targets: pdbj (CIF), pdbj-json (mmJSON), pdbj-plus, cc, cc-json,
#          ccmodel, ccmodel-json, prd, prd-json, vrpt, contacts,
#          schemas, dictionaries

# Update database
pixi run mine2 update [pipelines...]
# Pipelines: pdbj (CIF), pdbj-json (mmJSON), cc, cc-json, ccmodel,
#            ccmodel-json, prd, prd-json, vrpt, contacts

# Full update (sync + update)
pixi run mine2 all

# Test with limited data
pixi run mine2 test -p pdbj,cc -n 10
```

### Examples

```bash
# Sync all data
pixi run mine2 sync

# Sync specific targets
pixi run mine2 sync pdbj cc prd

# Update all pipelines
pixi run mine2 update

# Update specific pipelines
pixi run mine2 update pdbj cc

# Update with entry limit
pixi run mine2 update pdbj --limit 100
```

## Pipelines

### Default Pipelines (CIF)

CIF is the default format for dual-format pipelines:

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj | Main structure data from mmCIF (~248k files) | CIF |
| cc | Chemical component dictionary (components.cif.gz) | CIF |
| ccmodel | Chemical component models (chem_comp_model.cif.gz) | CIF |
| prd | BIRD data (prd-all.cif.gz + prdcc-all.cif.gz) | CIF |
| vrpt | Validation reports | CIF |
| contacts | Protein-protein contact data | JSON |

### mmJSON Pipelines (Optional)

For users who prefer mmJSON format, use the `-json` suffix:

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj-json | Main structure data (mmjson-noatom + mmjson-plus) | mmJSON |
| cc-json | Chemical component dictionary | mmJSON |
| ccmodel-json | Chemical component model data | mmJSON |
| prd-json | BIRD data | mmJSON |

### Backward Compatibility

Legacy pipeline names (`pdbj-cif`, `cc-cif`, etc.) are still accepted but deprecated.
They will emit a warning and run the corresponding CIF pipeline.

### Plus Data Support (pdbj pipeline)

Both CIF and mmJSON pdbj pipelines can merge PDBj-specific plus data when configured:

```yaml
# config.yml
pipelines:
  pdbj:
    deffile: ${CWD}schemas/pdbj.def.yml
    data: /path/to/mmCIF/             # CIF files
    data-plus: /path/to/mmjson-plus/  # Plus data (mmJSON format)
```

Plus data adds PDBj-specific annotations:
- `gene_ontology_pdbmlplus` - Gene Ontology (GO) annotations
- `struct_ref_pdbmlplus` - Additional UniProt reference data
- `citation_pdbmlplus`, `refine_pdbmlplus`, etc. (18 total categories)

| Configuration | CIF Pipeline | mmJSON Pipeline |
|---------------|--------------|-----------------|
| Without `data-plus` | Standard mmCIF only | `mmjson-noatom` only |
| With `data-plus` | CIF + plus data merged | `mmjson-noatom` + plus merged |

### Unsupported Pipelines

The following data types have schema definitions but are **not implemented** as pipelines:

| Schema | Status | Notes |
|--------|--------|-------|
| ihm | Not supported | Integrative/hybrid methods (I/HM) data |
| emdb | Not supported | Electron Microscopy Data Bank |

These may be added in future versions if needed.

## Database Management

```bash
# Initialize PostgreSQL data directory
pixi run db-init

# Start/stop/status
pixi run db-start
pixi run db-stop
pixi run db-status
```

### RDKit Extension Setup

RDKit extension and mol column are **automatically configured** when running the `cc` or `cc-json` pipeline.

> **Note**: Requires superuser privileges for initial `CREATE EXTENSION rdkit`.
> If auto-setup fails, run manually: `psql -d mine2 -f scripts/init_rdkit.sql`

This enables:
- **Substructure search**: `mol @> 'c1ccccc1'::mol`
- **Similarity search**: `morganbv_fp(mol) % morganbv_fp('CCO'::mol)`
- **SMILES validation**: `is_valid_smiles(smiles)`

Example queries:

```sql
-- Find compounds containing benzene ring
SELECT comp_id, name FROM cc.brief_summary
WHERE mol @> 'c1ccccc1'::mol;

-- Find similar compounds (Tanimoto > 0.8)
SELECT comp_id, name,
       tanimoto_sml(morganbv_fp(mol), morganbv_fp('CCO'::mol)) as similarity
FROM cc.brief_summary
WHERE morganbv_fp(mol) % morganbv_fp('CCO'::mol)
ORDER BY similarity DESC;
```

## Development

```bash
# Lint
pixi run lint

# Format
pixi run format

# Type check
pixi run typecheck

# Run tests
pixi run test

# All checks
pixi run check
```

## Project Structure

```
mine2updater-ng/
├── src/mine2/
│   ├── __main__.py      # CLI entry point
│   ├── cli.py           # Typer CLI commands
│   ├── config.py        # Configuration (Pydantic)
│   ├── db/
│   │   ├── connection.py # Connection pool
│   │   └── loader.py     # Parallel data loader
│   ├── parsers/
│   │   ├── cif.py       # Unified parser (CIF + mmJSON via gemmi)
│   │   └── mmjson.py    # Utilities (normalize_column_name, merge_data)
│   └── pipelines/
│       ├── base.py      # Base pipeline class
│       ├── pdbj.py      # PDB structure data
│       ├── cc.py        # Chemical components
│       ├── ccmodel.py   # Component models
│       ├── prd.py       # BIRD data
│       ├── vrpt.py      # Validation reports
│       └── contacts.py  # Contact data
├── schemas/             # Database schema definitions
├── tests/               # Unit tests (pytest)
├── scripts/             # Utility scripts
├── config.yml           # Production config
├── config.test.yml      # Test config
└── pixi.toml            # Pixi configuration
```

## License

GNU LGPLv3 - See [LICENSE](LICENSE) for details.
