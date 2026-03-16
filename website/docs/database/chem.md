---
sidebar_position: 8
---

# chem Schema

- **Primary Key**: `(source, id)`
- **Tables**: 1

The `chem` schema provides a unified view of chemical compounds from both the [cc](./cc.md) (Chemical Component Dictionary) and [prd](./prd.md) (BIRD Reference Dictionary) schemas. This enables cross-schema chemical searches without needing to query each source separately.

## How It Works

The `chem.compounds` table is populated by the `pmb compounds` command, which:

1. Extracts compounds from `cc.brief_summary` (CCD entries)
2. Extracts compounds from `prd.brief_summary` (BIRD entries)
3. Combines them into a single table with a `source` column (`'cc'` or `'prd'`) to distinguish origin

The table is also automatically refreshed after `pmb update` when the cc or prd pipelines run.

## RDKit Integration

Like the `cc` and `prd` schemas, the `chem` schema has full RDKit support:

1. **`mol` column** -- stores RDKit molecule objects generated from canonical SMILES
2. **GiST index** on `mol` for fast substructure and similarity searches
3. **RDKit descriptor columns** -- molecular weight, LogP, TPSA, HBA, HBD, rotatable bonds, rings, formula
4. **Chemical search SQL functions**:
   - `chem.similar_compounds(smiles, threshold)` -- Tanimoto similarity search across all sources
   - `chem.substructure_search(smarts)` -- substructure matching across all sources

### Example Queries

```sql
-- Find all compounds (cc + prd) similar to aspirin
SELECT * FROM chem.similar_compounds('CC(=O)Oc1ccccc1C(O)=O', 0.5);

-- Substructure search across all sources
SELECT id, source, name, canonical_smiles
FROM chem.compounds
WHERE mol @> 'c1ccccc1'::mol;

-- Compare compound counts by source
SELECT source, COUNT(*) FROM chem.compounds GROUP BY source;

-- Find PRD compounds that share a CCD component
SELECT id, name, cc_comp_ids
FROM chem.compounds
WHERE source = 'prd' AND cc_comp_ids IS NOT NULL;
```

## compounds

| Column | Type | Description |
|--------|------|-------------|
| id | text | Compound identifier (comp_id for cc, prd_id for prd) |
| source | text | Source schema: `'cc'` or `'prd'` (CHECK constraint enforced) |
| canonical_smiles | text | Canonical SMILES string |
| name | text | Compound name |
| formula | text | Molecular formula |
| cc_comp_ids | text[] | Associated CCD comp_ids (self-referential for cc, linked chem_comp_id for prd) |

:::note
The `mol` column and RDKit descriptor columns (`rdkit_mw`, `rdkit_logp`, `rdkit_tpsa`, `rdkit_hba`, `rdkit_hbd`, `rdkit_rotbonds`, `rdkit_rings`, `rdkit_formula`) are added automatically by `pmb setup-rdkit` and are not shown in the table above.
:::
