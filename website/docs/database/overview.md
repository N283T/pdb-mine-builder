---
sidebar_position: 0
---

# Database Overview

pdb-mine-builder creates a PostgreSQL database with multiple schemas, each containing tables derived from PDB (Protein Data Bank) data sources.

## Schemas

| Schema | Primary Key | Entries | Tables | Size | Description |
|--------|-------------|---------|--------|------|-------------|
| [pdbj](./pdbj.md) | `pdbid` | ~250k | 250 | 183 GB | Main structure data from mmCIF/mmJSON |
| [vrpt](./vrpt.md) | `pdbid` | ~250k | 69 | 152 GB | Validation reports |
| [contacts](./contacts.md) | `pdbid` | ~250k | 2 | 13 GB | Protein-protein contact data |
| [cc](./cc.md) | `comp_id` | ~50k | 12 | 811 MB | Chemical component dictionary (with RDKit) |
| [ccmodel](./ccmodel.md) | `model_id` | ~23k | 8 | 174 MB | Chemical component 3D models |
| [prd](./prd.md) | `prd_id` | ~1.2k | 17 | 50 MB | BIRD reference dictionary |
| [prd_family](./prd_family.md) | `family_prd_id` | ~200 | 10 | 2.3 MB | BIRD family classifications |
| [emdb](./emdb.md) | `emdb_id` | — | 79 | — | Electron Microscopy Data Bank (experimental) |
| [ihm](./ihm.md) | `pdbid` | — | 114 | — | Integrative/Hybrid Methods (experimental) |

**Total: 368 tables, ~349 GB** (excluding emdb/ihm which have no data pipeline yet)

**[Schema Search](/schema-search)** — Search across all schemas, tables, and columns in one place.
**[Table Relations](/table-relations)** — Explore relationships between tables interactively.

:::note emdb / ihm schemas
The `emdb` and `ihm` schemas have table definitions but have not been thoroughly tested with production data. They currently have no data-loading pipeline. If there is community demand, these schemas will receive full pipeline support and validation. Feedback and contributions are welcome via [GitHub Issues](https://github.com/N283T/pdb-mine-builder/issues).
:::

## Data Flow

```
PDBj rsync servers
       │
       │  pixi run pmb sync
       ▼
Local data files (CIF / mmJSON / JSON)
       │
       │  pixi run pmb load / update
       ▼
Pipelines: parse → transform → bulk upsert
       │
       ▼
PostgreSQL (one schema per data source)
```

## Schema Design

- Each schema has a **`brief_summary`** table with key metadata for quick lookups
- Primary keys are text-based identifiers (e.g., `pdbid`, `comp_id`)
- No foreign key constraints (for loading performance)
- All columns except primary keys are nullable
- Table names match CIF/mmJSON category names for straightforward mapping
- Columns added by pdb-mine-builder (not in the original mine2 schema) are marked with `[pmb]` prefix in their descriptions

## Common Query Patterns

### Find an entry

```sql
-- PDB structure
SELECT * FROM pdbj.brief_summary WHERE pdbid = '1abc';

-- Chemical component
SELECT * FROM cc.brief_summary WHERE comp_id = 'ATP';
```

### List tables in a schema

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'pdbj'
ORDER BY table_name;
```

### Count entries per schema

```sql
SELECT 'pdbj' AS schema, COUNT(*) FROM pdbj.brief_summary
UNION ALL
SELECT 'cc', COUNT(*) FROM cc.brief_summary
UNION ALL
SELECT 'vrpt', COUNT(*) FROM vrpt.brief_summary;
```
