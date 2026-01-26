# Schema Definition Format

## Overview

Schema definitions are YAML files that describe database tables for each pipeline.

Location: `schemas/<pipeline>.def.yml`

## Structure

```yaml
schema_name: <string>     # PostgreSQL schema name
primary_key: <string>     # Default primary key column (e.g., "pdbid")

tables:
  - name: <string>        # Table name
    primary_key: [<col1>, <col2>]  # Primary key columns
    columns:
      - [<col_name>, <sql_type>]
      - [<col_name>, <sql_type>]
```

## Example

```yaml
schema_name: pdbj
primary_key: pdbid

tables:
  - name: brief_summary
    primary_key: [pdbid]
    columns:
      - [pdbid, TEXT]
      - [title, TEXT]
      - [deposition_date, TEXT]
      - [resolution, REAL]

  - name: entity
    primary_key: [pdbid, id]
    columns:
      - [pdbid, TEXT]
      - [id, TEXT]
      - [type, TEXT]
      - [description, TEXT]
      - [formula_weight, REAL]

  - name: atom_site
    primary_key: [pdbid, id]
    columns:
      - [pdbid, TEXT]
      - [id, INTEGER]
      - [type_symbol, TEXT]
      - [cartn_x, REAL]
      - [cartn_y, REAL]
      - [cartn_z, REAL]
```

## SQL Types

Common PostgreSQL types used:

| Type | Description | Example |
|------|-------------|---------|
| `TEXT` | Variable-length string | IDs, names, descriptions |
| `INTEGER` | 4-byte integer | Counts, sequence numbers |
| `REAL` | 4-byte floating point | Coordinates, resolutions |
| `DOUBLE PRECISION` | 8-byte floating point | High-precision values |
| `BOOLEAN` | True/false | Flags |
| `JSONB` | Binary JSON | Complex nested data |

## Primary Keys

### Single Column

```yaml
primary_key: [pdbid]
```

### Composite Key

```yaml
primary_key: [pdbid, entity_id, seq_num]
```

## Table Generation

The loader automatically:

1. Creates schema if not exists: `CREATE SCHEMA IF NOT EXISTS <schema_name>`
2. Creates tables: `CREATE TABLE IF NOT EXISTS <schema>.<table> (...)`
3. Adds indexes on primary keys

## Column Name Normalization

mmJSON uses bracket notation for array indices:

```
fract_transf_matrix[1][1]
```

Schema columns should use concatenated form:

```yaml
columns:
  - [fract_transf_matrix11, REAL]
  - [fract_transf_matrix12, REAL]
  - [fract_transf_matrix13, REAL]
```

The `normalize_column_name()` function handles this conversion during data loading.

## Brief Summary Table

Every pipeline should have a `brief_summary` table:

```yaml
tables:
  - name: brief_summary
    primary_key: [<primary_key>]
    columns:
      - [<primary_key>, TEXT]
      - [title, TEXT]
      # ... key metadata fields
```

This table provides quick access to entry metadata without joining large tables.

## Category-to-Table Mapping

Table names should match the source data category names:

| Data Category | Table Name |
|---------------|------------|
| `entity` | `entity` |
| `atom_site` | `atom_site` |
| `pdbx_chem_comp_model` | `pdbx_chem_comp_model` |

This allows automatic data loading without explicit mapping.

## Validation

Schema files are validated at load time by Pydantic. Errors include:

- Missing required fields
- Invalid YAML syntax
- Unknown field names

## Tips

1. **Order matters**: Define tables in dependency order
2. **Use TEXT for IDs**: Even numeric-looking IDs should be TEXT
3. **Nullable by default**: All columns except primary keys can be NULL
4. **No foreign keys**: For performance, foreign keys are not enforced
