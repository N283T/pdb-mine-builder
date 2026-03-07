# pdb-mine-builder

[![CI](https://github.com/N283T/pdb-mine-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/N283T/pdb-mine-builder/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pdbminebuilder)](https://pypi.org/project/pdbminebuilder/)
[![Python](https://img.shields.io/pypi/pyversions/pdbminebuilder)](https://pypi.org/project/pdbminebuilder/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)

Build a Mine-schema database from PDB data. Synchronizes structural biology data from PDBj (Protein Data Bank Japan) via rsync and loads it into PostgreSQL.

This project is based on PDBj's [mine2updater](https://gitlab.com/pdbjapan/mine2updater). Thanks to the PDBj team for the original implementation and the [Mine](https://doi.org/10.1093/database/baq021) relational database design.

**Documentation**: [https://n283t.github.io/pdb-mine-builder/](https://n283t.github.io/pdb-mine-builder/)

## Features

- Multi-process parallel data loading with configurable workers
- Support for multiple data formats (CIF default, mmJSON optional)
- RDKit chemical search integration (substructure, similarity)
- 9 database schemas covering PDB structures, chemical components, validation reports, and more

## Installation

### Pixi (recommended)

[Pixi](https://pixi.sh/) manages all dependencies including Python, PostgreSQL, and RDKit in a single environment.

```bash
git clone https://github.com/N283T/pdb-mine-builder.git
cd pdb-mine-builder
pixi install
cp config.example.yml config.yml  # Edit with your data paths
```

```bash
pixi run db-init       # Initialize PostgreSQL
pixi run db-start      # Start PostgreSQL
pixi run pmb sync      # Sync data from PDBj
pixi run pmb load pdbj --force  # Load data
pixi run pmb stats     # Check database statistics
```

### pip (alternative)

> **Note**: pip installs the Python package only. You must provide PostgreSQL (17+) and the [RDKit PostgreSQL cartridge](https://github.com/rdkit/rdkit-postgresql) separately. Database management commands (`pixi run db-*`) are not available.

```bash
pip install pdbminebuilder
cp config.example.yml config.yml  # Edit with your data paths and connection string
pmb --help
```

### conda + pip (alternative)

> **Note**: Database management commands (`pixi run db-*`) are not available. Use your own PostgreSQL instance.

```bash
conda create -n pmb python=3.12 rdkit-postgresql -c conda-forge
conda activate pmb
pip install pdbminebuilder
cp config.example.yml config.yml
pmb --help
```

See the [Getting Started guide](https://n283t.github.io/pdb-mine-builder/docs/getting-started/installation) for detailed setup instructions.

## Pipelines

| Pipeline | Description | Format |
|----------|-------------|--------|
| pdbj | Main structure data (~248k entries) | CIF / mmJSON |
| cc | Chemical component dictionary | CIF / mmJSON |
| ccmodel | Chemical component models | CIF / mmJSON |
| prd | BIRD reference dictionary | CIF / mmJSON |
| vrpt | Validation reports | CIF |
| contacts | Protein-protein contact data | JSON |

See the [Database Reference](https://n283t.github.io/pdb-mine-builder/docs/database/overview) for schema details and SQL examples.

## Development

```bash
pixi run lint      # Ruff check
pixi run format    # Ruff format
pixi run test      # Run tests (pytest)
pixi run check     # All checks
```

## Requirements

- Python 3.12+
- PostgreSQL 17+ (managed by rdkit-postgresql via conda-forge)
- [Pixi](https://pixi.sh/) — manages all dependencies (conda + PyPI)
- rsync

> **Note**: Most dependencies are installed from conda-forge. Only `ccd2rdmol` (PyPI only) and `psycopg[binary,pool]` (extras required) remain as PyPI dependencies. PostgreSQL version is determined by rdkit-postgresql.

## License

MIT - See [LICENSE](LICENSE) for details.

### Relationship to mine2updater

This project is inspired by [mine2updater](https://gitlab.com/pdbjapan/mine2updater) (LGPLv3) by PDBj, which loads PDB data into PostgreSQL using Node.js. pdb-mine-builder is an independent rewrite in Python with a completely different tech stack (gemmi, SQLAlchemy, psycopg3, RDKit), architecture, and data model. No code was copied or translated from the original project. Shared concepts (pipeline names, schema structures, PDB ID encoding) derive from PDB data specifications, not from the original codebase.

## References

- Kinjo AR, Yamashita R, Nakamura H. PDBj Mine: design and implementation of relational database interface for Protein Data Bank Japan. *Database (Oxford)*. 2010;2010:baq021. doi: [10.1093/database/baq021](https://doi.org/10.1093/database/baq021)
