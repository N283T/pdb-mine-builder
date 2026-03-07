---
sidebar_position: 7
---

# contacts Schema

- **Primary Key**: `pdbid`
- **Tables**: 2

## brief_summary

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| modification_date | date |  |
| update_date | timestamp without time zone |  |

## list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| label_asym_id_1 | text | Chain ID of the first residue/molecule |
| label_asym_id_2 | text | Chain ID of the second residue/molecule |
| label_seq_id_1 | integer | Sequence ID of the first residue/molecule |
| label_seq_id_2 | integer | Sequence ID of the second residue/molecule |
| label_comp_id_1 | text | Residue/molecule name of the first residue |
| label_comp_id_2 | text | Residue/molecule name of the second residue |
| distance | real | Minimal distance between the two residues/molecules |
