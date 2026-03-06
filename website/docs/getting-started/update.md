---
sidebar_position: 4
---

# Updating the Database

After syncing data files, use the `update` or `load` commands to parse them and load records into PostgreSQL.

## Pipelines

Each pipeline processes a specific type of PDB data:

| Pipeline | Description | Format | Notes |
|----------|-------------|--------|-------|
| `pdbj` | Main structure data (~248k entries) | CIF / mmJSON | File-per-entry, `atom_site` skipped |
| `cc` | Chemical component dictionary (~40k compounds) | CIF / mmJSON | Single file (`components.cif.gz`) |
| `ccmodel` | Chemical component models | CIF / mmJSON | Single file (`chem_comp_model.cif.gz`) |
| `prd` | BIRD reference dictionary | CIF / mmJSON | Dual file (`prd-all.cif.gz` + `prdcc-all.cif.gz`) |
| `vrpt` | Validation reports | CIF | Nested directory structure |
| `contacts` | Protein-protein contact data | JSON | Array format |
| `emdb` | Electron Microscopy Data Bank | -- | Schema only, no pipeline |
| `ihm` | Integrative/Hybrid Methods | -- | Schema only, no pipeline |

The first four pipelines (`pdbj`, `cc`, `ccmodel`, `prd`) support dual format. Set `format: cif` or `format: mmjson` in `config.yml` to choose. CIF is the default.

## Initial Load (Bulk)

For first-time database population, use the `load` command. It uses PostgreSQL's COPY protocol for significantly faster throughput.

:::warning
The `load` command **truncates all tables** in the target schema before loading. Do not use it on a database with data you want to keep.
:::

```bash
# Load a single pipeline
pixi run pmb load cc --force

# Load multiple pipelines
pixi run pmb load cc ccmodel prd --force

# Load with entry limit (useful for testing)
pixi run pmb load pdbj --limit 1000 --force
```

The `--force` flag skips the interactive confirmation prompt for the truncate operation.

### Bulk Load Mode (Optional)

For very large initial loads (especially `pdbj` with 248k+ entries), you can tune PostgreSQL for maximum write throughput:

```bash
# 1. Enable bulk load mode (disables fsync, autovacuum)
pixi run db-bulkload-mode

# 2. Run data loading
pixi run pmb load pdbj --force
pixi run pmb load cc ccmodel prd vrpt contacts --force

# 3. Restore safe settings
pixi run db-safe-mode

# 4. Run VACUUM ANALYZE to update statistics
psql -d pmb -c "VACUUM ANALYZE;"
```

:::warning
Bulk load mode disables crash safety (`fsync=off`). If PostgreSQL crashes during bulk load, the data directory may be corrupted and you will need to reinitialize:

```bash
pixi run db-stop
rm -rf $PGDATA
pixi run db-init
pixi run db-start
# Re-run loading from scratch
```
:::

## Incremental Updates

After the initial load, use the `update` command for ongoing incremental updates:

```bash
# Update all pipelines
pixi run pmb update

# Update specific pipelines
pixi run pmb update pdbj cc

# Limit entries processed (useful for testing)
pixi run pmb update pdbj --limit 100

# Force reprocessing (ignore mtime cache)
pixi run pmb update pdbj --force
```

The `update` command tracks file modification times (`mtime`) for file-per-entry pipelines (`pdbj`, `vrpt`, `contacts`). Unchanged entries are automatically skipped, making incremental updates fast.

### CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--limit` | `-l` | Limit number of entries to process |
| `--workers` | `-w` | Number of worker processes (overrides `nworkers` in config) |
| `--force` | `-f` | Reprocess all entries, ignoring mtime cache (`pdbj`, `vrpt`, `contacts`) |
| `--log` | | Custom log file path (default: `logs/<pipeline>_YYYYMMDD_HHMMSS.log`) |
| `--verbose` | `-v` | Enable DEBUG-level logging |
| `--config` | `-c` | Path to config file (default: `config.yml`) |

## Full Cycle: sync + update

The `all` command runs sync followed by update in a single step:

```bash
pixi run pmb all
```

This is equivalent to:

```bash
pixi run pmb sync
pixi run pmb update
```

## Reset Schemas

To drop all tables in a schema and start over:

```bash
# Reset a single schema
pixi run pmb reset cc

# Reset multiple schemas
pixi run pmb reset cc pdbj

# Reset all schemas
pixi run pmb reset all

# Skip confirmation prompt
pixi run pmb reset all --force
```

:::warning
`reset` drops all tables and data in the specified schema(s). This cannot be undone.
:::

## Database Statistics

View current table counts, row counts, and last update timestamps:

```bash
pixi run pmb stats
```

## Backward Compatibility

Legacy pipeline names with format suffixes (`pdbj-cif`, `cc-json`, etc.) are still accepted but deprecated. They emit a warning and resolve to the base pipeline name. Format selection is now controlled by the `format` field in `config.yml`.

## Recommended Workflow

A typical first-time setup looks like this:

```bash
# 1. Sync data from PDBj
pixi run pmb sync pdbj cc prd

# 2. (Optional) Enable bulk load mode
pixi run db-bulkload-mode

# 3. Load data into PostgreSQL
pixi run pmb load cc --force
pixi run pmb load prd --force
pixi run pmb load pdbj --limit 1000 --force   # Test with subset first
pixi run pmb load pdbj --force                 # Then load everything

# 4. Restore safe mode and vacuum
pixi run db-safe-mode
psql -d pmb -c "VACUUM ANALYZE;"

# 5. Check stats
pixi run pmb stats
```

For ongoing updates after the initial load:

```bash
pixi run pmb sync
pixi run pmb update
```
