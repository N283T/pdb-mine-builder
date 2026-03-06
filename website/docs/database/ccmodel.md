---
sidebar_position: 3
---

# ccmodel Schema

- **Primary Key**: `model_id`
- **Tables**: 8

## brief_summary

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| docid | bigint | Serial counter (unique integer) to represent the row id. |
| pdbx_initial_date | date | Inclusion date to the PDB of an entry |
| pdbx_modified_date | date | Modification date of an entry |
| update_date | timestamp without time zone | Entry update date (within the RDB). |
| comp_id | text |  |
| csd_id | text |  |
| keywords | text[] | Array of keywords. |

## pdbx_chem_comp_model

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| id | text | The value of _pdbx_chem_comp_model.id must uniquely identify each model instance the PDBX_CHEM_COMP_MODEL list. |
| comp_id | text | An identifier for chemical component definition. |

## pdbx_chem_comp_model_atom

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| atom_id | text | The value of _pdbx_chem_comp_model_atom.atom_id uniquely identifies each atom in the PDBX_CHEM_COMP_MODEL_ATOM list. |
| ordinal_id | integer | The value of _pdbx_chem_comp_model_atom.ordinal_id is an ordinal identifer for each atom in the PDBX_CHEM_COMP_MODEL_ATOM list. |
| charge | integer | The net integer charge assigned to this atom. This is the formal charge assignment normally found in chemical diagrams. |
| model_Cartn_x | double precision | The x component of the coordinates for this atom in this component model specified as orthogonal angstroms. |
| model_Cartn_y | double precision | The y component of the coordinates for this atom in this component model specified as orthogonal angstroms. |
| model_Cartn_z | double precision | The z component of the coordinates for this atom in this component model specified as orthogonal angstroms. |
| type_symbol | text | The code used to identify the atom species representing this atom type. Normally this code is the element symbol. |

## pdbx_chem_comp_model_audit

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| date | date | The date associated with this audit record. |
| action_type | text | The action associated with this audit record. |

## pdbx_chem_comp_model_bond

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| atom_id_1 | text | The ID of the first of the two atoms that define the bond. This data item is a pointer to _pdbx_chem_comp_model_atom.atom_id in the PDBX_CHEM_COMP_MODEL_ATOM category. |
| atom_id_2 | text | The ID of the second of the two atoms that define the bond. This data item is a pointer to _pdbx_chem_comp_model_atom.atom_id in the PDBX_CHEM_COMP_MODEL_ATOM category. |
| value_order | text | The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order. |
| ordinal_id | integer | The value of _pdbx_chem_comp_model_bond.ordinal_id is an ordinal identifer for each atom in the PDBX_CHEM_COMP_MODEL_BOND list. |

## pdbx_chem_comp_model_descriptor

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| descriptor | text | This data item contains the descriptor value for this component. |
| type | text | This data item contains the descriptor type. |

## pdbx_chem_comp_model_feature

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| feature_name | text | The component model feature type. |
| feature_value | text | The component feature value. |

## pdbx_chem_comp_model_reference

| Column | Type | Description |
|--------|------|-------------|
| model_id | text | Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| db_name | text | The component model feature type. |
| db_code | text | The component feature value. |
