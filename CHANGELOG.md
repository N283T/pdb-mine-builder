# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Interactive SQL query examples page with 75 examples across 10 categories (#95)
- RDKit chemical search examples: substructure, similarity, SMARTS patterns (#97)
- Configurable sync source URLs for regional wwPDB mirrors (RCSB, PDBe) (#100)
- `data-dir` config field with priority resolution (config > env > CWD) (#100)
- `prdcc` config field for explicit PRDCC file path in prd pipeline (#100)
- PDBj dump file incompatibility warning in migration docs (#98)

### Changed

- Sync URLs updated from `rsync.pdbj.org` to `data.pdbj.org` (#100)
- Sync targets cc, ccmodel, prd, prd-family now download only required files (#100)
- Sync destinations derived from pipeline config (single source of truth) (#100)
- Sync completion message now shows success/failure/skip counts (#100)
- SQL examples pipeline simplified to use `sqlExamples.json` as single source of truth (#96)

### Removed

- Unused `SyncTarget` class and `sync` field from Settings (#100)
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
