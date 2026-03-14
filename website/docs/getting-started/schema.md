---
sidebar_position: 6
---

# Inspecting Schemas

The `pmb schema` command inspects SQLAlchemy model definitions to display schema, table, and column information. **No database connection required** -- all data is read from the model definitions.

## Usage

```bash
# List all schemas
pixi run pmb schema

# List tables in a schema
pixi run pmb schema pdbj

# Show columns in a table
pixi run pmb schema pdbj.brief_summary

# Show single column detail
pixi run pmb schema pdbj.brief_summary.pdbid
```

## Search

Search column names and comments across all schemas:

```bash
# Search by column name
pixi run pmb schema -s resolution

# Search by comment text
pixi run pmb schema -s "deposition date"
```

## JSON Output

The `--json` flag outputs machine-readable JSON, useful for AI tools and scripts:

```bash
# All schemas as JSON
pixi run pmb schema --json

# Full schema with all tables and columns in one response
pixi run pmb schema pdbj --json

# Table columns as JSON
pixi run pmb schema pdbj.brief_summary --json

# Search results as JSON
pixi run pmb schema -s resolution --json
```

:::tip
`pmb schema pdbj --json` returns **all tables and columns** in a single JSON response. This is large but ideal for AI agents that need full schema context.
:::

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--search` | `-s` | Search column names and comments across all schemas |
| `--json` | | Output in JSON format (machine-readable) |
| `--config` | `-c` | Config file path (default: `config.yml`) |

## Examples

```bash
# Find all columns related to resolution
pixi run pmb schema -s resolution

# Check what columns are in the entity table
pixi run pmb schema pdbj.entity

# Get full cc schema for AI processing
pixi run pmb schema cc --json

# Look up a specific column's type and comment
pixi run pmb schema pdbj.brief_summary.pdbid
```
