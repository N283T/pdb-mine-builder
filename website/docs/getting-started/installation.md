---
sidebar_position: 1
---

# Installation

This guide walks you through setting up pdb-mine-builder from scratch.

## Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.12+ | Runtime |
| PostgreSQL | 17+ | Database (with RDKit extension for chemical searches) |
| [Pixi](https://pixi.sh/) | Latest | Package manager (manages Python deps and CLI tools) |
| rsync | Any | Data synchronization from PDBj servers |

## Clone and Install

```bash
git clone https://github.com/N283T/pdb-mine-builder.git
cd pdb-mine-builder
pixi install
```

This installs all Python dependencies and CLI tools into an isolated Pixi environment.

## Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

The default `.env.example` contains:

```bash
# PostgreSQL connection
PGPORT=5433
PGHOST=localhost
PGDATA=postgres_data_5433
PGUSER=pdbj
PGDATABASE=pmb

# Data directory (PDBj data root)
DATA_DIR=/path/to/pdb/data
```

Edit `DATA_DIR` to point to where you want PDBj data stored on disk.

:::tip
Default PostgreSQL settings are also defined in `pixi.toml` under `[activation.env]`. The `.env` file overrides those defaults.
:::

## PostgreSQL Setup

Initialize and start PostgreSQL:

```bash
# Initialize the data directory
pixi run db-init

# Start PostgreSQL
pixi run db-start

# Verify it is running
pixi run db-status
```

To stop PostgreSQL later:

```bash
pixi run db-stop
```

## RDKit Extension

The RDKit PostgreSQL extension enables chemical structure searches (substructure, similarity, etc.) on the `cc` (Chemical Components) schema.

The extension is **automatically configured** when you run the `cc` pipeline. No manual setup is needed in most cases.

To set up RDKit independently (for example, before loading data):

```bash
pixi run pmb setup-rdkit
```

:::note
The initial `CREATE EXTENSION rdkit` requires superuser privileges. If auto-setup fails, run the SQL script manually:

```bash
psql -d pmb -f scripts/init_rdkit.sql
```
:::

## Verify Installation

Confirm everything is working:

```bash
pixi run pmb --help
pixi run pmb --version
```

You should see the CLI help output listing all available commands.

## Next Steps

- [Configure data paths and database settings](./configuration.md)
- [Sync data from PDBj servers](./sync.md)
- [Load data into PostgreSQL](./update.md)
