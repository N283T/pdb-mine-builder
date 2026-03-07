# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `pmb query` command for executing SQL queries with multi-format output (table, CSV, JSON, Parquet)
- Read-only connection mode for query command to prevent accidental destructive SQL
- Polars dependency for DataFrame-based query result handling

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
