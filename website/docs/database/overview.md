---
sidebar_position: 0
---

# Database Overview

pdb-mine-builder creates a PostgreSQL database with multiple schemas, each containing tables derived from PDB (Protein Data Bank) data sources.

## Schemas

| Schema | Primary Key | Tables | Description |
|--------|-------------|--------|-------------|
| [pdbj](./pdbj.mdx) | `pdbid` | ~250 | Main structure data from mmCIF/mmJSON |
| [cc](./cc.mdx) | `comp_id` | 12 | Chemical component dictionary (with RDKit) |
| [ccmodel](./ccmodel.mdx) | `model_id` | 8 | Chemical component 3D models |
| [prd](./prd.mdx) | `prd_id` | 17 | BIRD reference dictionary |
| [prd_family](./prd_family.mdx) | `family_prd_id` | 10 | BIRD family classifications |
| [vrpt](./vrpt.mdx) | `pdbid` | 69 | Validation reports |
| [contacts](./contacts.mdx) | `pdbid` | 2 | Protein-protein contact data |
| [emdb](./emdb.mdx) | `emdb_id` | 79 | Electron Microscopy Data Bank (experimental) |
| [ihm](./ihm.mdx) | `pdbid` | 114 | Integrative/Hybrid Methods (experimental) |

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
