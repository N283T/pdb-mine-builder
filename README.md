# MINE2 Updater

RDB updater for MINE2 database. Synchronizes structural biology data from PDBj (Protein Data Bank Japan) via rsync and loads it into PostgreSQL.

## Features

- Multi-process parallel data loading with configurable workers
- Schema-driven database management from YAML definitions
- Support for multiple data formats (mmJSON, CIF)
- Six data pipelines: pdbj, cc, ccmodel, prd, vrpt, contacts

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
# Targets: pdbj, cc, ccmodel, prd, vrpt, contacts, schemas, dictionaries

# Update database
pixi run mine2 update [pipelines...]
# Pipelines: pdbj, cc, ccmodel, prd, vrpt, contacts

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

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj | Main structure data (mmjson-noatom + mmjson-plus) | mmJSON |
| cc | Chemical component dictionary | mmJSON |
| ccmodel | Chemical component model data | mmJSON |
| prd | BIRD (Biologically Interesting Reference Dictionary) | mmJSON |
| vrpt | Validation reports | CIF |
| contacts | Protein-protein contact data | JSON |

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
│   │   ├── mmjson.py    # mmJSON parser
│   │   └── cif.py       # CIF parser (gemmi)
│   └── pipelines/
│       ├── base.py      # Base pipeline class
│       ├── pdbj.py      # PDB structure data
│       ├── cc.py        # Chemical components
│       ├── ccmodel.py   # Component models
│       ├── prd.py       # BIRD data
│       ├── vrpt.py      # Validation reports
│       └── contacts.py  # Contact data
├── schemas/             # Database schema definitions
├── scripts/             # Utility scripts
├── config.yml           # Production config
├── config.test.yml      # Test config
└── pixi.toml            # Pixi configuration
```

## License

GNU LGPLv3 - See [LICENSE](LICENSE) for details.
