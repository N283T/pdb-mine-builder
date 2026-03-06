---
sidebar_position: 2
---

# cc Schema

- **Primary Key**: `comp_id`
- **Tables**: 12

## brief_summary

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| docid | bigint | Serial counter (unique integer) to represent the row id. |
| pdbx_initial_date | date | Date that the entry was defined in the dictionary |
| release_date | date | Date at which the entry was officially released |
| pdbx_modified_date | date | Modification date of an entry |
| update_date | timestamp without time zone | Entry update date (within the RDB). |
| name | text | Name of an entry. |
| formula | text | Chemical formula of an entry. |
| pdbx_synonyms | text[] | Known synonyms of an entry. |
| identifier | text | Identifier of an entry. |
| smiles | text[] | SMILES representations of an entry. |
| inchi | text[] | InChI representations of an entry. |
| canonical_smiles | text |  |
| keywords | text[] | Array of keywords. |

## chem_comp

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| formula | text | The formula for the chemical component. Formulae are written according to the following rules: (1) Only recognized element symbols may be used. (2) Each element symbol is followed by a 'count' number. A count of '1' may be omitted. (3) A space or parenthesis must separate each cluster of (element symbol + count), but in general parentheses are not used. (4) The order of elements depends on whether carbon is present or not. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts. |
| formula_weight | double precision | Formula mass in daltons of the chemical component. |
| id | text | The value of _chem_comp.id must uniquely identify each item in the CHEM_COMP list. For protein polymer entities, this is the three-letter code for the amino acid. For nucleic acid polymer entities, this is the one-letter code for the base. |
| mon_nstd_parent_comp_id | text | The identifier for the parent component of the nonstandard component. May be be a comma separated list if this component is derived from multiple components. Items in this indirectly point to _chem_comp.id in the CHEM_COMP category. |
| name | text | The full name of the component. |
| one_letter_code | text | For standard polymer components, the one-letter code for the component. For non-standard polymer components, the one-letter code for parent component if this exists; otherwise, the one-letter code should be given as 'X'. Components that derived from multiple parents components are described by a sequence of one-letter-codes. |
| three_letter_code | text | For standard polymer components, the common three-letter code for the component. Non-standard polymer components and non-polymer components are also assigned three-letter-codes. For ambiguous polymer components three-letter code should be given as 'UNK'. Ambiguous ions are assigned the code 'UNX'. Ambiguous non-polymer components are assigned the code 'UNL'. |
| type | text | For standard polymer components, the type of the monomer. Note that monomers that will form polymers are of three types: linking monomers, monomers with some type of N-terminal (or 5') cap and monomers with some type of C-terminal (or 3') cap. |
| pdbx_synonyms | text | Synonym list for the component. |
| pdbx_type | text | A preliminary classification used by PDB. |
| pdbx_ambiguous_flag | text | A preliminary classification used by PDB to indicate that the chemistry of this component while described as clearly as possible is still ambiguous. Software tools may not be able to process this component definition. |
| pdbx_replaced_by | text | Identifies the _chem_comp.id of the component that has replaced this component. |
| pdbx_replaces | text | Identifies the _chem_comp.id's of the components which have been replaced by this component. Multiple id codes should be separated by commas. |
| pdbx_formal_charge | integer | The net integer charge assigned to this component. This is the formal charge assignment normally found in chemical diagrams. |
| pdbx_subcomponent_list | text | The list of subcomponents contained in this component. |
| pdbx_model_coordinates_details | text | This data item provides additional details about the model coordinates in the component definition. |
| pdbx_model_coordinates_db_code | text | This data item identifies the PDB database code from which the heavy atom model coordinates were obtained. |
| pdbx_ideal_coordinates_details | text | This data item identifies the source of the ideal coordinates in the component definition. |
| pdbx_ideal_coordinates_missing_flag | text | This data item identifies if ideal coordinates are missing in this definition. |
| pdbx_model_coordinates_missing_flag | text | This data item identifies if model coordinates are missing in this definition. |
| pdbx_initial_date | date | Date component was added to database. |
| pdbx_modified_date | date | Date component was last modified. |
| pdbx_release_status | text | This data item holds the current release status for the component. |
| pdbx_processing_site | text | This data item identifies the deposition site that processed this chemical component defintion. |
| pdbx_pcm | text | A flag to indicate if the CCD can be used to represent a protein modification. |

## chem_comp_atom

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| alt_atom_id | text | An alternative identifier for the atom. This data item would be used in cases where alternative nomenclatures exist for labelling atoms in a group. |
| atom_id | text | The value of _chem_comp_atom.atom_id must uniquely identify each atom in each monomer in the CHEM_COMP_ATOM list. The atom identifiers need not be unique over all atoms in the data block; they need only be unique for each atom in a component. Note that this item need not be a number; it can be any unique identifier. |
| charge | integer | The net integer charge assigned to this atom. This is the formal charge assignment normally found in chemical diagrams. |
| model_Cartn_x | double precision | The x component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list. |
| model_Cartn_y | double precision | The y component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list. |
| model_Cartn_z | double precision | The z component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list. |
| type_symbol | text | The code used to identify the atom species representing this atom type. Normally this code is the element symbol. |
| pdbx_align | integer | Atom name alignment offset in PDB atom field. |
| pdbx_ordinal | integer | Ordinal index for the component atom list. |
| pdbx_component_atom_id | text | The atom identifier in the subcomponent where a larger component has been divided subcomponents. |
| pdbx_component_comp_id | text | The component identifier for the subcomponent where a larger component has been divided subcomponents. |
| pdbx_model_Cartn_x_ideal | double precision | An alternative x component of the coordinates for this atom in this component specified as orthogonal angstroms. |
| pdbx_model_Cartn_y_ideal | double precision | An alternative y component of the coordinates for this atom in this component specified as orthogonal angstroms. |
| pdbx_model_Cartn_z_ideal | double precision | An alternative z component of the coordinates for this atom in this component specified as orthogonal angstroms. |
| pdbx_stereo_config | text | The chiral configuration of the atom that is a chiral center. |
| pdbx_aromatic_flag | text | A flag indicating an aromatic atom. |
| pdbx_leaving_atom_flag | text | A flag indicating a leaving atom. |
| pdbx_residue_numbering | integer | Preferred residue numbering in the BIRD definition. |
| pdbx_polymer_type | text | Is the atom in a polymer or non-polymer subcomponent in the BIRD definition. |
| pdbx_component_id | integer | A reference to _pdbx_reference_entity_list.component_id |
| pdbx_backbone_atom_flag | text | A flag indicating the backbone atoms in polypeptide units. |
| pdbx_n_terminal_atom_flag | text | A flag indicating the N-terminal group atoms in polypeptide units. |
| pdbx_c_terminal_atom_flag | text | A flag indicating the C-terminal group atoms in polypeptide units. |

## chem_comp_bond

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| atom_id_1 | text | The ID of the first of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category. |
| atom_id_2 | text | The ID of the second of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category. |
| value_order | text | The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order. |
| pdbx_ordinal | integer | Ordinal index for the component bond list. |
| pdbx_stereo_config | text | Stereochemical configuration across a double bond. |
| pdbx_aromatic_flag | text | A flag indicating an aromatic bond. |

## pdbx_chem_comp_atom_related

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| related_comp_id | text | The related chemical component for which this chemical component is based. |
| ordinal | integer | An ordinal index for this category |
| atom_id | text | The atom identifier/name for the atom mapping |
| related_atom_id | text | The atom identifier/name for the atom mapping in the related chemical component |
| related_type | text | Describes the type of relationship |

## pdbx_chem_comp_audit

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| date | date | The date associated with this audit record. |
| processing_site | text | An identifier for the wwPDB site creating or modifying the component. |
| action_type | text | The action associated with this audit record. |

## pdbx_chem_comp_descriptor

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| descriptor | text | This data item contains the descriptor value for this component. |
| type | text | This data item contains the descriptor type. |
| program | text | This data item contains the name of the program or library used to compute the descriptor. |
| program_version | text | This data item contains the version of the program or library used to compute the descriptor. |

## pdbx_chem_comp_feature

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| type | text | The component feature type. |
| value | text | The component feature value. |
| source | text | The information source for the component feature. |

## pdbx_chem_comp_identifier

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| identifier | text | This data item contains the identifier value for this component. |
| type | text | This data item contains the identifier type. |
| program | text | This data item contains the name of the program or library used to compute the identifier. |
| program_version | text | This data item contains the version of the program or library used to compute the identifier. |

## pdbx_chem_comp_pcm

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| pcm_id | integer | An ordinal index for this category. |
| modified_residue_id | text | Chemical component identifier for the amino acid residue that is being modified. |
| type | text | The type of protein modification. |
| category | text | The category of protein modification. |
| position | text | The position of the modification on the amino acid. |
| polypeptide_position | text | The position of the modification on the polypeptide. |
| comp_id_linking_atom | text | The atom on the modification group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs. |
| modified_residue_id_linking_atom | text | The atom on the polypeptide residue group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs. |
| uniprot_specific_ptm_accession | text | The UniProt PTM accession code that is an exact match for the protein modification. |
| uniprot_generic_ptm_accession | text | The UniProt PTM accession code that describes the group of PTMs of which this protein modification is a member. |

## pdbx_chem_comp_related

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| related_comp_id | text | The related chemical component for which this chemical component is based. |
| relationship_type | text | Describes the type of relationship |

## pdbx_chem_comp_synonyms

| Column | Type | Description |
|--------|------|-------------|
| comp_id | text | Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table. |
| ordinal | integer | An ordinal index for this category |
| name | text | The synonym of this particular chemical component. |
| provenance | text | The provenance of this synonym. |
| type | text | The type of this synonym. |

## RDKit Chemical Search

The `cc` schema includes RDKit PostgreSQL extension support for chemical structure searches. The `brief_summary.canonical_smiles` column stores canonical SMILES generated from molecular structure using ccd2rdmol + RDKit.

### Search Functions

| Function | Description |
|----------|-------------|
| `cc.similar_compounds(smiles, threshold, limit)` | Tanimoto similarity search (Morgan FP) |
| `cc.similar_compounds_dice(smiles, threshold, limit)` | Dice similarity search |
| `cc.substructure_search(smarts, limit)` | Substructure search (SMARTS) |
| `cc.exact_match(smiles)` | Exact structure match |
| `cc.similar_to_compound(comp_id, threshold, limit)` | Find compounds similar to existing component |
| `cc.compound_similarity(comp_id, smiles)` | Calculate similarity between component and SMILES |

### Molecular Descriptors

The `cc.brief_summary` table includes RDKit-calculated molecular descriptors:

| Column | Type | Description |
|--------|------|-------------|
| `rdkit_mw` | double precision | Average molecular weight |
| `rdkit_logp` | double precision | Wildman-Crippen LogP |
| `rdkit_tpsa` | double precision | Topological polar surface area |
| `rdkit_hba` | integer | Hydrogen bond acceptors |
| `rdkit_hbd` | integer | Hydrogen bond donors |
| `rdkit_rotbonds` | integer | Rotatable bonds |
| `rdkit_rings` | integer | Number of rings |
| `rdkit_formula` | text | Molecular formula |

:::note
Descriptors are NULL when the `mol` column is NULL (invalid SMILES).
:::

### Query Examples

```sql
-- Find compounds similar to aspirin (Tanimoto >= 0.7)
SELECT * FROM cc.similar_compounds('CC(=O)Oc1ccccc1C(=O)O', 0.7, 20);

-- Find compounds containing benzene ring
SELECT * FROM cc.substructure_search('c1ccccc1', 50);

-- Find compounds similar to ATP
SELECT * FROM cc.similar_to_compound('ATP', 0.6, 50);

-- Lipinski's Rule of Five filter (drug-like compounds)
SELECT comp_id, name, rdkit_mw, rdkit_logp, rdkit_hba, rdkit_hbd
FROM cc.brief_summary
WHERE rdkit_mw < 500
  AND rdkit_logp < 5
  AND rdkit_hba <= 10
  AND rdkit_hbd <= 5;

-- Combine similarity search with property filter
SELECT s.*, b.rdkit_mw, b.rdkit_logp
FROM cc.similar_compounds('c1ccccc1C(=O)O', 0.5, 100) s
JOIN cc.brief_summary b USING (comp_id)
WHERE b.rdkit_mw BETWEEN 100 AND 300;

-- Direct RDKit operators (for advanced queries)
SELECT comp_id, name FROM cc.brief_summary
WHERE mol @> 'C(=O)O'::qmol;  -- Carboxylic acid substructure
```
