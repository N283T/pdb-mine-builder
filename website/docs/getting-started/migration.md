---
sidebar_position: 5
---

# Migration from mine2updater

pdb-mine-builder is a complete rewrite of the original [mine2updater](https://gitlab.com/pdbjapan/mine2updater) — the RDB updater for PDBj's MINE 2 system. This page covers what changed and why.

## Why Rewrite?

The original mine2updater served PDBj well, but had several limitations:

- **Unmaintained dependencies** — Node.js `libpq` native bindings, OpenBabel for fingerprinting
- **No chemical search integration** — Fingerprints stored as raw bigint columns (byte0–byte15) via OpenBabel, no built-in substructure or similarity search
- **PostgreSQL 12 era** — No support for newer PostgreSQL features
- **No tests or type checking** — Difficult to maintain and extend safely
- **mmJSON only** — CIF parsing not supported (mmJSON conversion required upstream)
- **No schema migration tooling** — Dynamic ALTER TABLE based schema upgrades, no version tracking

## Technology Comparison

| Aspect | mine2updater | pdb-mine-builder |
|--------|-------------|-----------------|
| **Language** | JavaScript (Node.js 14+) | Python 3.12+ |
| **PostgreSQL** | 12+ | 17+ |
| **DB driver** | libpq (C binding) | psycopg3 |
| **Parser** | Built-in mmJSON parser | gemmi (CIF + mmJSON) |
| **Default format** | mmJSON | CIF |
| **Chemical search** | OpenBabel fingerprints (bigint columns) | RDKit PostgreSQL cartridge (mol type) |
| **Schema definition** | YAML def files | SQLAlchemy Core |
| **Schema migration** | Dynamic ALTER TABLE | Alembic (versioned) |
| **CLI** | Shell script + `node mine2.js` | Typer + Rich |
| **Config validation** | None | Pydantic |
| **Package manager** | npm | Pixi (conda + PyPI) |
| **Parallel processing** | Node.js cluster | ProcessPoolExecutor |
| **Tests** | None | pytest |
| **Type checking** | None | ruff |

## Key Changes

### CIF as Default Format

mine2updater exclusively used mmJSON files. pdb-mine-builder defaults to **CIF** (mmCIF) format and parses both CIF and mmJSON via [gemmi](https://gemmi.readthedocs.io/). CIF is the canonical format distributed by wwPDB and avoids the need for upstream mmJSON conversion.

mmJSON is still supported — set `format: mmjson` in `config.yml` for pipelines that support it.

### RDKit Instead of OpenBabel

The original system used OpenBabel to generate FP2 fingerprints, stored as 16 bigint columns (`byte0`–`byte15`) in `cc.brief_summary`. Searches required custom bit-manipulation SQL.

pdb-mine-builder uses the **RDKit PostgreSQL cartridge**, which provides:

- Native `mol` column type for molecular structures
- Built-in substructure search (`@>` operator)
- Tanimoto similarity search (`%` operator with Morgan fingerprints)
- Molecular descriptor functions (MW, LogP, TPSA, etc.)

```sql
-- Substructure search (pdb-mine-builder)
SELECT * FROM cc.brief_summary WHERE mol @> 'c1ccccc1'::mol;

-- Similarity search
SELECT *, tanimoto_sml(morganbv_fp(mol), morganbv_fp('CCO'::mol)) AS similarity
FROM cc.brief_summary
WHERE morganbv_fp(mol) % morganbv_fp('CCO'::mol);
```

SMILES values are generated from molecular structure via [ccd2rdmol](https://github.com/N283T/ccd2rdmol) + RDKit, not taken from `pdbx_chem_comp_descriptor` records.

### No Foreign Key Constraints

mine2updater defined foreign keys in its YAML schema files and managed them during schema upgrades. pdb-mine-builder **removes all foreign key constraints** to improve bulk loading performance. Data integrity is ensured by the pipeline logic, not database constraints.

### Alembic Migrations

Schema changes in mine2updater were handled by comparing the running database against the YAML definition and issuing ALTER TABLE statements dynamically. This had no version tracking and could fail on complex changes.

pdb-mine-builder uses **Alembic** for versioned, reproducible schema migrations:

```bash
pixi run db-migrate "add new column"  # Generate migration
pixi run db-upgrade                   # Apply migrations
pixi run db-downgrade                 # Rollback
pixi run db-history                   # View history
```

### Removed Columns

- **`docid`** (bigint) — Removed from all `brief_summary` tables. The original system used docid for internal indexing; pdb-mine-builder uses text-based primary keys directly.
- **`byte0`–`byte15`** (bigint) — Replaced by RDKit `mol` column in `cc.brief_summary`.

### Schema Changes

**Removed schemas** (present in mine2 rdb_docs but not in pdb-mine-builder):

| Schema | Reason |
|--------|--------|
| `empiar` | Out of scope (EMPIAR data) |
| `misc` | Consolidated into other schemas |
| `sifts` | Out of scope (SIFTS mapping data) |

**Schema-only definitions** (no pipeline yet):

| Schema | Notes |
|--------|-------|
| `prd_family` | Schema definition existed in mine2 but had no loading pipeline. Has a dedicated primary key (`family_prd_id`) |
| `emdb` | Electron Microscopy Data Bank |
| `ihm` | Integrative/Hybrid Methods |

These schemas have table definitions but no data-loading pipeline. See the [Database Overview](../database/overview.md) for current status.

### Mtime-Based Skip Optimization

pdb-mine-builder tracks file modification times in an `entry_metadata` table. During incremental updates, unchanged entries are automatically skipped. Use `--force` to bypass this check.

mine2updater did not have this optimization — it processed all entries on every run.

### Bulk Load with COPY Protocol

pdb-mine-builder supports a dedicated bulk load mode using PostgreSQL's COPY protocol for initial data loading, which is significantly faster than row-by-row INSERT:

```bash
pixi run pmb load pdbj --force
```

## Database Compatibility

pdb-mine-builder produces a database with the **same MINE 2 schema structure**. Schema names, table names, and column naming conventions are preserved. Basic queries should work with minimal changes:

- Replace `docid`-based lookups with primary key lookups
- Replace `byte0`–`byte15` fingerprint queries with RDKit operators
- Schema names and table names are unchanged
- Column names follow the same CIF/mmJSON category naming convention

:::warning Important
pdb-mine-builder is an **independent reimplementation** of the MINE 2 database builder. While the schema structure is largely compatible, **full query compatibility with PDBj's official services is not guaranteed**.

- SQL queries written for PDBj's [Mine 2 RDB web API](https://pdbj.org/help/mine2-sql) or REST API may not work as-is against a pdb-mine-builder database
- Column types, NULL handling, and data transformations may differ in subtle ways
- The `brief_summary` tables are constructed differently (e.g., no `docid`, different fingerprint columns)
- New columns or tables added by PDBj's official MINE 2 system may not be present

If you rely on queries from PDBj's official documentation or web interface, **test them against your local database before use in production**.
:::

## Configuration Comparison

**mine2updater** (`config.yml`):
```yaml
rdb:
  nworkers: 16
  constring: "dbname='mine2' user='pdbj' password='pdbj_pwd' port=5432"

obabel: /usr/bin/obabel

pipelines:
  pdb:
    deffile: ${CWD}schemas/pdbj.def.yml
    data: ${CWD}data/mmjson-noatom/
```

**pdb-mine-builder** (`config.yml`):
```yaml
rdb:
  constring: "dbname=pmb user=pdbj port=5433"
  nworkers: 8

pipelines:
  pdbj:
    format: cif
    data: /path/to/data/pdb/cif/
```

Key config differences:
- `obabel` setting removed (RDKit handles chemistry natively)
- `deffile` removed (schemas defined in Python code)
- `format` field added (choose between `cif` and `mmjson`)
- Pipeline name `pdb` renamed to `pdbj`
