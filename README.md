# pdb-mine-builder

Build a MINE-schema database from PDB data. Synchronizes structural biology data from PDBj (Protein Data Bank Japan) via rsync and loads it into PostgreSQL.

**Documentation**: [https://n283t.github.io/pdb-mine-builder/](https://n283t.github.io/pdb-mine-builder/)

## Features

- Multi-process parallel data loading with configurable workers
- Support for multiple data formats (CIF default, mmJSON optional)
- RDKit chemical search integration (substructure, similarity)
- 9 database schemas covering PDB structures, chemical components, validation reports, and more

## Quick Start

```bash
git clone https://github.com/N283T/pdb-mine-builder.git
cd pdb-mine-builder
pixi install
cp .env.example .env   # Edit with your settings
```

```bash
pixi run db-init       # Initialize PostgreSQL
pixi run db-start      # Start PostgreSQL
pixi run pmb sync      # Sync data from PDBj
pixi run pmb load pdbj --force  # Load data
pixi run pmb stats     # Check database statistics
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
- PostgreSQL 17+ (with RDKit extension for chemical searches)
- [Pixi](https://pixi.sh/)
- rsync

## License

MIT - See [LICENSE](LICENSE) for details.

### Relationship to mine2updater

This project is inspired by [mine2updater](https://gitlab.com/pdbjapan/mine2updater) (LGPLv3) by PDBj, which loads PDB data into PostgreSQL using Node.js. pdb-mine-builder is an independent rewrite in Python with a completely different tech stack (gemmi, SQLAlchemy, psycopg3, RDKit), architecture, and data model. No code was copied or translated from the original project. Shared concepts (pipeline names, schema structures, PDB ID encoding) derive from PDB data specifications, not from the original codebase.
