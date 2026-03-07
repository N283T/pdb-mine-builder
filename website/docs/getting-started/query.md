---
sidebar_position: 5
---

# Querying the Database

The `pmb query` command executes SQL queries against the configured database and outputs results in various formats.

## Basic Usage

```bash
# Display results as a Rich table (default)
pmb query "SELECT * FROM cc.brief_summary LIMIT 5"

# Read SQL from a file
pmb query -f query.sql
```

## Output Formats

### Table (default)

Rich-formatted table for terminal viewing:

```bash
pmb query "SELECT comp_id, name, formula FROM cc.brief_summary LIMIT 5"
```

Use `--limit` to cap the number of displayed rows:

```bash
pmb query "SELECT * FROM cc.brief_summary" --limit 20
```

### CSV

```bash
# Output to stdout (pipe or redirect)
pmb query "SELECT * FROM cc.brief_summary" -F csv > compounds.csv

# Output to file
pmb query "SELECT * FROM cc.brief_summary" -F csv -o compounds.csv
```

### JSON

```bash
# Output to stdout
pmb query "SELECT * FROM cc.brief_summary LIMIT 10" -F json

# Output to file
pmb query "SELECT * FROM cc.brief_summary" -F json -o compounds.json
```

### Parquet

Parquet output requires `--output` (`-o`):

```bash
pmb query "SELECT * FROM cc.brief_summary" -F parquet -o compounds.parquet
```

:::tip
Parquet files can be loaded directly into Polars or Pandas for further analysis:

```python
import polars as pl
df = pl.read_parquet("compounds.parquet")
```
:::

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--file` | `-f` | Read SQL from file instead of argument |
| `--format` | `-F` | Output format: `table`, `csv`, `json`, `parquet` |
| `--output` | `-o` | Output file path (required for parquet) |
| `--limit` | `-l` | Max rows to display (table format only) |
| `--config` | `-c` | Config file path (default: `config.yml`) |

## Examples

```bash
# Chemical substructure search → CSV
pmb query "SELECT comp_id, name FROM cc.brief_summary WHERE mol @> 'c1ccccc1'::mol" -F csv

# Export all entities for a structure
pmb query "SELECT * FROM pdbj.entity WHERE pdbid = '1A00'" -F json

# Large export to Parquet
pmb query "SELECT pdbid, title FROM pdbj.brief_summary" -F parquet -o structures.parquet
```
