---
sidebar_position: 1
---

# CLI Reference

Quick reference for all `pmb` commands. See individual pages for detailed usage.

## Data Pipeline Commands

### `pmb sync`

Download data files from PDBj/wwPDB mirrors via rsync. Targets are defined in `config.yml`.

```bash
pmb sync                    # Sync all configured targets
pmb sync pdbj cc            # Sync specific targets
pmb sync --dry-run          # Preview without downloading
```

See [Syncing Data](./getting-started/sync.md) for details.

### `pmb update`

Run incremental database updates. Tracks file modification times to skip unchanged entries.

```bash
pmb update                  # Update all pipelines
pmb update pdbj cc          # Update specific pipelines
pmb update pdbj --limit 100 # Limit entries processed
pmb update pdbj --force     # Ignore mtime cache
```

See [Updating the Database](./getting-started/update.md) for details.

### `pmb load`

Bulk load data using PostgreSQL COPY protocol. **Truncates tables before loading.**

```bash
pmb load cc --force         # Load single pipeline
pmb load pdbj --limit 1000 --force  # Load with entry limit
```

See [Updating the Database - Initial Load](./getting-started/update.md#initial-load-bulk) for details.

### `pmb all`

Run full sync + update cycle in a single step.

```bash
pmb all
```

## Query Commands

### `pmb schema`

Inspect database schema definitions from model definitions. No database connection required.

```bash
pmb schema                  # List all schemas
pmb schema pdbj             # List tables in schema
pmb schema pdbj.brief_summary      # Show columns
pmb schema pdbj.brief_summary.pdbid  # Single column detail
pmb schema -s resolution    # Search columns
pmb schema pdbj --json      # JSON output (for AI/scripts)
```

See [Inspecting Schemas](./getting-started/schema.md) for details.

### `pmb query`

Execute SQL queries with multi-format output.

```bash
pmb query "SELECT * FROM cc.brief_summary LIMIT 5"
pmb query -f query.sql -F csv -o out.csv
pmb query "SELECT * FROM pdbj.brief_summary" -F parquet -o out.parquet
```

See [Querying the Database](./getting-started/query.md) for details.

### `pmb stats`

Show database statistics (table counts, row counts, sizes).

```bash
pmb stats
```

### `pmb config`

Display active configuration and resolved settings. Useful for verifying which config file is being used.

```bash
pmb config                  # Show config summary
pmb config --json           # JSON output
pmb config -c /path/to/config.yml  # Show specific config
```

Config file is discovered automatically: `./config.yml` → `~/.config/pmb/config.yml`.

## Administration Commands

### `pmb reset`

Drop and recreate database schemas. **Destructive -- cannot be undone.**

```bash
pmb reset cc                # Reset single schema
pmb reset all --force       # Reset all schemas
```

See [Updating the Database - Reset Schemas](./getting-started/update.md#reset-schemas) for details.

### `pmb setup-rdkit`

Set up RDKit PostgreSQL extension, create `mol` column on `cc.brief_summary`, and load chemical search SQL functions.

```bash
pmb setup-rdkit
```

:::note
This is automatically run by the `cc` pipeline. Use this command only when you need to add RDKit functions to an existing database without re-running the full pipeline.
:::

See [cc Schema - RDKit Integration](./database/cc.md#rdkit-integration) for details.

### `pmb test`

Create a test database and validate pipelines. Uses `config.test.yml` by default.

```bash
pmb test                    # Test all pipelines
pmb test pdbj cc            # Test specific pipelines
pmb test --drop --limit 20  # Drop existing test DB, process 20 entries
```

| Option | Short | Description |
|--------|-------|-------------|
| `--drop` | `-d` | Drop existing test database before testing |
| `--limit` | `-l` | Limit number of files to process (default: 10) |
| `--workers` | `-w` | Number of worker processes |
| `--config` | `-c` | Config file path (default: `config.test.yml`) |

## Global Options

These options are available for most commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--config` | `-c` | Config file path (auto-discovered if not set) |
| `--version` | `-v` | Show version |
| `--help` | | Show help |
