# MINE2 Updater

RDB updater for MINE2 database. Synchronizes structural biology data from PDBj (Protein Data Bank Japan) via rsync and loads it into PostgreSQL.

## Features

- Multi-process parallel data loading with configurable workers
- Schema-driven database management from YAML definitions
- Support for multiple data formats (mmJSON, CIF)
- 10 data pipelines: 6 primary (mmJSON) + 4 CIF alternatives
- CIF pipelines for users who already mirror wwPDB/PDBj CIF files

## Requirements

- Python 3.12+
- PostgreSQL 12+
- [Pixi](https://pixi.sh/) (package manager)
- rsync (for data synchronization)
- OpenBabel (for chemical fingerprinting)

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

obabel: /usr/bin/obabel

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
# Targets: pdbj, pdbj-cif, pdbj-plus, cc, cc-cif, ccmodel, ccmodel-cif,
#          prd, prd-cif, vrpt, contacts, schemas, dictionaries

# Update database
pixi run mine2 update [pipelines...]
# Pipelines: pdbj, pdbj-cif, cc, cc-cif, ccmodel, ccmodel-cif,
#            prd, prd-cif, vrpt, contacts

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

### Primary Pipelines (mmJSON)

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj | Main structure data (mmjson-noatom + mmjson-plus) | mmJSON |
| cc | Chemical component dictionary | mmJSON |
| ccmodel | Chemical component model data | mmJSON |
| prd | BIRD (Biologically Interesting Reference Dictionary) | mmJSON |
| vrpt | Validation reports | CIF |
| contacts | Protein-protein contact data | JSON |

### CIF Alternative Pipelines

For users who already mirror CIF files from wwPDB/PDBj:

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj-cif | Main structure data from mmCIF (~248k files) | CIF |
| cc-cif | Chemical component dictionary (components.cif.gz) | CIF |
| ccmodel-cif | Chemical component models (chem_comp_model.cif.gz) | CIF |
| prd-cif | BIRD data (prd-all.cif.gz + prdcc-all.cif.gz) | CIF |

## Database Management

```bash
# Initialize PostgreSQL data directory
pixi run db-init

# Start/stop/status
pixi run db-start
pixi run db-stop
pixi run db-status
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
