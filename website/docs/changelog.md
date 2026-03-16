---
sidebar_position: 99
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- SMILES generation for PRD pipeline via ccd2rdmol on PRDCC blocks
- `canonical_smiles` and `chem_comp_id` columns on `prd.brief_summary`
- RDKit mol column, GiST index, and descriptor triggers for prd schema
- Unified `chem.compounds` table for cross-schema chemical searches (cc + prd)
- `pmb compounds` command to refresh chem.compounds table
- `scripts/rdkit_functions_chem.sql` with similarity/substructure search functions for chem schema
- Automatic compounds refresh after `pmb update` when cc/prd pipelines run
- Documentation for `chem` schema and `prd` RDKit integration

### Changed

- Extracted shared RDKit utilities to `pipelines/rdkit_utils.py` (from cc.py)
- `pmb setup-rdkit` now sets up both cc and prd schemas
- Docker test tasks use `docker-compose` (standalone) instead of `docker compose` (subcommand)

### Fixed

- Docker test container crashes on ARM Mac (`mcs07/postgres-rdkit` amd64-only image) by adding `platform: linux/amd64`

## [0.2.3] - 2026-03-14

### Added

- `pmb config` command to display active configuration and resolved settings
  - Shows config file location, connection string (redacted), data directory, workers, pipelines, sync targets
  - `pmb config --json` for machine-readable output
  - `pmb config --init` to generate config from bundled template (`~/.config/pmb/config.yml`)
- Config file auto-discovery: `./config.yml` → `~/.config/pmb/config.yml`
- `pmb schema` command to inspect database schema definitions (no DB connection required)
  - `pmb schema` - list all schemas with table counts and entry PK
  - `pmb schema <name>` - list tables in a schema with column counts
  - `pmb schema <name>.<table>` - show columns with types, nullable, PK, and comments
  - `pmb schema <name>.<table>.<column>` - show single column detail
  - `pmb schema --search <query>` - search column names and comments across all schemas
  - `pmb schema --json` - JSON output for all modes (machine/AI-readable)
  - `pmb schema <name> --json` returns all tables and columns in one response
- CLI Reference documentation page with all commands
- Schema inspection guide in Getting Started docs
- Query command added to Getting Started sidebar
- RDKit integration section in cc schema documentation

## [0.2.2] - 2026-03-08

### Added

- Interactive SQL query examples page with 75 examples across 10 categories (#95)
- RDKit chemical search examples: substructure, similarity, SMARTS patterns (#97)
- Fully config-driven sync: all targets defined in `config.yml` `sync` section (#102)
- `SyncTarget` model with `source`/`sources`, `dest`, and `options` fields (#102)
- Configurable rsync options per target (default: `["-av", "--size-only"]`) (#102)
- `data-dir` config field with priority resolution (config > env > CWD) (#100)
- `prdcc` config field for explicit PRDCC file path in prd pipeline (#100)
- PDBj dump file incompatibility warning in migration docs (#98)
- Database size and entry count statistics (#93)
- Missing `data-nextgen-plus` configuration documentation (#99)

### Changed

- Sync command is now purely config-driven: no hardcoded URLs, destinations, or options (#102)
- `config.example.yml` rewritten with full `sync` section and all available targets (#102)
- Sync URLs updated from `rsync.pdbj.org` to `data.pdbj.org` (#100)
- Sync targets cc, ccmodel, prd, prd-family now download only required files (#100)
- SQL examples pipeline simplified to use `sqlExamples.json` as single source of truth (#96)

### Fixed

- vrpt rsync include/exclude options had embedded quotes that broke filtering (#103)

### Removed

- Hardcoded sync target definitions (`SYNC_TARGETS`, `_PIPELINE_DEST_MAP`, etc.) (#102)
- `sync-sources` config field (replaced by `sync` section) (#102)
- Legacy sync alias resolution (#102)
- PDBj example fetching scripts (`fetch_pdbj_examples.py`, `process_examples.py`, `generate_examples_json.py`) (#96)

## [0.2.1] - 2026-03-08

### Added

- `pmb query` command for executing SQL queries with multi-format output (table, CSV, JSON, Parquet)
- Read-only connection mode for query command to prevent accidental destructive SQL
- Polars dependency for DataFrame-based query result handling
- Docker/Podman support for production deployment
- Interactive Table Relations page with dynamic Mermaid ER diagrams
- Schema tab picker with preset examples for quick exploration
- SVG/PNG diagram download
- Schema search page with cross-schema column search

### Changed

- Migrated schema docs from .mdx to .md format
- Extracted shared Schema interface and SCHEMA_PRIORITY to types module

### Fixed

- Schema ordering bug (unknown schemas sorted incorrectly)
- PNG download silent failures with proper error handling

## [0.2.0] - 2026-03-07

Initial release as an independent Python project. Rewritten from
[mine2updater](https://gitlab.com/pdbjapan/mine2updater) (Node.js) by PDBj.

### Added

- 7 data pipelines: pdbj, cc, ccmodel, prd, prd_family, vrpt, contacts
- 2 schema-only definitions: emdb, ihm
- Dual format support (CIF / mmJSON) for pdbj, cc, ccmodel, prd pipelines
- Unified parsing via gemmi for both CIF and mmJSON
- Multi-process parallel loading with ProcessPoolExecutor
- Bulk load mode (COPY protocol) for initial data loading
- Mtime-based skip optimization for incremental updates
- RDKit PostgreSQL cartridge integration for chemical searches
- SMILES generation from molecular structure via ccd2rdmol
- SQLAlchemy Core schema definitions with Alembic migrations
- CLI with 9 commands: sync, update, load, all, setup-rdkit, test, reset, stats, version
- Pydantic-based configuration with YAML and environment variable support
- Documentation website with auto-generated schema docs
- Docker-based test environment (PostgreSQL + RDKit)
- PyPI publishing support with trusted publishing
- Environment version tests for Python and PostgreSQL
- Alternative installation methods (pip, conda+pip)
- `config.example.yml` with documented options
- MIT license
