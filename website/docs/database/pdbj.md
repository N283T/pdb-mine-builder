---
sidebar_position: 1
---

# pdbj Schema

- **Primary Key**: `pdbid`
- **Tables**: 250

## align_pdbjplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text |  |
| asym_id | text |  |
| align_id | integer |  |
| beg_label_seq_id | integer |  |
| end_label_seq_id | integer |  |
| db_align_beg | integer |  |
| db_align_end | integer |  |
| db_name | text |  |
| pdbx_db_accession | text |  |

## atom_sites

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| Cartn_transf_matrix11 | double precision |  |
| Cartn_transf_matrix12 | double precision |  |
| Cartn_transf_matrix13 | double precision |  |
| Cartn_transf_matrix21 | double precision |  |
| Cartn_transf_matrix22 | double precision |  |
| Cartn_transf_matrix23 | double precision |  |
| Cartn_transf_matrix31 | double precision |  |
| Cartn_transf_matrix32 | double precision |  |
| Cartn_transf_matrix33 | double precision |  |
| Cartn_transf_vector1 | double precision |  |
| Cartn_transf_vector2 | double precision |  |
| Cartn_transf_vector3 | double precision |  |
| fract_transf_matrix11 | double precision |  |
| fract_transf_matrix12 | double precision |  |
| fract_transf_matrix13 | double precision |  |
| fract_transf_matrix21 | double precision |  |
| fract_transf_matrix22 | double precision |  |
| fract_transf_matrix23 | double precision |  |
| fract_transf_matrix31 | double precision |  |
| fract_transf_matrix32 | double precision |  |
| fract_transf_matrix33 | double precision |  |
| fract_transf_vector1 | double precision |  |
| fract_transf_vector2 | double precision |  |
| fract_transf_vector3 | double precision |  |

## atom_sites_footnote

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | A code that identifies the footnote. |
| text | text | The text of the footnote. Footnotes are used to describe an atom site or a group of atom sites in the ATOM_SITE list. For example, footnotes may be used to indicate atoms for which the electron density is very weak, or atoms for which static disorder has been modelled. |

## atom_type

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| oxidation_number | integer | Formal oxidation state of this atom type in the structure. |
| scat_Cromer_Mann_a1 | double precision | The Cromer-Mann scattering-factor coefficient a1 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_a2 | double precision | The Cromer-Mann scattering-factor coefficient a2 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_a3 | double precision | The Cromer-Mann scattering-factor coefficient a3 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_a4 | double precision | The Cromer-Mann scattering-factor coefficient a4 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_b1 | double precision | The Cromer-Mann scattering-factor coefficient b1 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_b2 | double precision | The Cromer-Mann scattering-factor coefficient b2 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_b3 | double precision | The Cromer-Mann scattering-factor coefficient b3 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_b4 | double precision | The Cromer-Mann scattering-factor coefficient b4 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_Cromer_Mann_c | double precision | The Cromer-Mann scattering-factor coefficient c used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| scat_dispersion_imag | double precision | The imaginary component of the anomalous-dispersion scattering factor, f'', in electrons for this atom type and the radiation identified by _diffrn_radiation_wavelength.id. |
| scat_dispersion_real | double precision | The real component of the anomalous-dispersion scattering factor, f', in electrons for this atom type and the radiation identified by _diffrn_radiation_wavelength.id. |
| scat_source | text | Reference to the source of the scattering factors or scattering lengths used for this atom type. |
| symbol | text | The code used to identify the atom species (singular or plural) representing this atom type. Normally this code is the element symbol. The code may be composed of any character except an underscore with the additional proviso that digits designate an oxidation state and must be followed by a + or - character. |
| pdbx_scat_Cromer_Mann_a5 | double precision | Scattering-factor coefficient a5, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| pdbx_scat_Cromer_Mann_b5 | double precision | Scattering-factor coefficient b5, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| pdbx_scat_Cromer_Mann_a6 | double precision | Scattering-factor coefficient a6, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| pdbx_scat_Cromer_Mann_b6 | double precision | Scattering-factor coefficient b6, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5. |
| pdbx_scat_Z | integer | Atomic number of atom in scattering amplitude. |
| pdbx_N_electrons | integer | Number of electrons in atom used in scattering factor |

## audit

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| creation_date | date | A date that the data block was created. The date format is yyyy-mm-dd. |
| creation_method | text | A description of how data were entered into the data block. |
| revision_id | text | The value of _audit.revision_id must uniquely identify a record in the AUDIT list. |
| update_record | text | A record of any changes to the data block. The update format is a date (yyyy-mm-dd) followed by a description of the changes. The latest update entry is added to the bottom of this record. |

## audit_author

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| name | text | The name of an author of this data block. If there are multiple authors, _audit_author.name is looped with _audit_author.address. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s). |
| pdbx_ordinal | integer | This data item defines the order of the author's name in the list of audit authors. |
| identifier_ORCID | text | The Open Researcher and Contributor ID (ORCID). |

## audit_conform

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| dict_location | text | A file name or uniform resource locator (URL) for the dictionary to which the current data block conforms. |
| dict_name | text | The string identifying the highest-level dictionary defining data names used in this file. |
| dict_version | text | The version number of the dictionary to which the current data block conforms. |

## brief_summary

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All other tables/categories refer back to the PDBID in the brief_summary table. |
| docid | bigint | Serial counter (unique integer) to represent the row id. |
| deposition_date | date | Deposition date of an entry. |
| release_date | date | Release date of an entry. |
| modification_date | date | Modification date of a PDB entry (wwPDB data). |
| deposit_author | text[] | Array of deposition authors. |
| citation_author | text[] | Array of citation authors of associated paper. |
| citation_title | text[] | Title of associated paper. |
| citation_journal | text[] | Journal of associated paper. |
| citation_year | integer[] | Year of associated paper. |
| citation_volume | text[] | Volume of associated paper. |
| citation_author_pri | text[] | Array of primary citation authors for associated paper. |
| citation_title_pri | text | Primary citation title. |
| citation_journal_pri | text | Primary citation journal. |
| citation_year_pri | integer | Primary citation year. |
| citation_volume_pri | text | Primary citation volume. |
| chain_type | text[] | Array of chain types |
| chain_type_ids | integer[] | Array of chain types encoded as integers: 1: polypeptide(D) 2: polypeptide(L) 3: polydeoxyribonucleotide 4: polyribonucleotide 5: polysaccharide(D) 6: polysaccharide(L) 7: polydeoxyribonucleotide/polyribonucleotide hybrid 8: cyclic-pseudo-peptide 9: other |
| chain_number | integer | Number of chains. |
| chain_length | integer[] | Number of residues for each chain. |
| pdbx_descriptor | text | Structure descriptor (refers to entity.pdbx_description) |
| struct_title | text | Structure title. |
| ligand | text[] | Array of ligands. |
| exptl_method | text[] | Array of experimental methods used. |
| exptl_method_ids | integer[] | Array of experimental methods used encoded as integers: 1: X-RAY DIFFRACTION 2: NEUTRON DIFFRACTION 3: FIBER DIFFRACTION 4: ELECTRON CRYSTALLOGRAPHY 5: ELECTRON MICROSCOPY 6: SOLUTION NMR 7: SOLID-STATE NMR 8: SOLUTION SCATTERING 9: POWDER DIFFRACTION 10: INFRARED SPECTROSCOPY 11: EPR 12: FLUORESCENCE TRANSFER 13: THEORETICAL MODEL 14: HYBRID 15: THEORETICAL MODEL (obsolete) |
| resolution | double precision | Resolution |
| biol_species | text | Biological species. |
| host_species | text | Host species. |
| db_pubmed | text[] | Array of associated PubMed IDs. |
| db_doi | text[] | Array of associated DOI IDs. |
| db_ec_number | text[] | Array of associated EC numbers. |
| db_goid | text[] | Array of associated GO IDs. |
| db_uniprot | text[] | Array of associated Uniprot IDs. |
| db_genbank | text[] | Array of associated GenBank IDs. |
| db_embl | text[] | Array of associated EMBL IDs. |
| db_pir | text[] | Array of associated PIR IDs. |
| db_emdb | text[] | Array of associated EMDB IDs. |
| pdb_related | text[] | Array of associated PDB IDs. |
| keywords | text[] | Array of keywords. |
| aaseq | text | Amino acid sequence. |
| update_date | timestamp without time zone | Entry update date (within the RDB of any metadata, both regular wwPDB data and PDBj-generated plus data). |
| db_pfam | text[] | Array of associated PFam IDs. |
| group_id | text | Deposition Group ID |
| plus_fields | jsonb |  |

## cell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| angle_alpha | double precision | Unit-cell angle alpha of the reported structure in degrees. |
| angle_alpha_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.angle_alpha. |
| angle_beta | double precision | Unit-cell angle beta of the reported structure in degrees. |
| angle_beta_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.angle_beta. |
| angle_gamma | double precision | Unit-cell angle gamma of the reported structure in degrees. |
| angle_gamma_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.angle_gamma. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| formula_units_Z | integer | The number of the formula units in the unit cell as specified by _chemical_formula.structural, _chemical_formula.moiety or _chemical_formula.sum. |
| length_a | double precision | Unit-cell length a corresponding to the structure reported in angstroms. |
| length_a_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.length_a. |
| length_b | double precision | Unit-cell length b corresponding to the structure reported in angstroms. |
| length_b_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.length_b. |
| length_c | double precision | Unit-cell length c corresponding to the structure reported in angstroms. |
| length_c_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.length_c. |
| volume | double precision | Cell volume V in angstroms cubed. V = a b c (1 - cos^2^~alpha~ - cos^2^~beta~ - cos^2^~gamma~ + 2 cos~alpha~ cos~beta~ cos~gamma~)^1/2^ a = _cell.length_a b = _cell.length_b c = _cell.length_c alpha = _cell.angle_alpha beta = _cell.angle_beta gamma = _cell.angle_gamma |
| volume_esd | double precision | The standard uncertainty (estimated standard deviation) of _cell.volume. |
| Z_PDB | integer | The number of the polymeric chains in a unit cell. In the case of heteropolymers, Z is the number of occurrences of the most populous chain. This data item is provided for compatibility with the original Protein Data Bank format, and only for that purpose. |
| reciprocal_angle_alpha | double precision | The angle (recip-alpha) defining the reciprocal cell in degrees. (recip-alpha), (recip-alpha) and (recip-alpha) related to the angles in the real cell by: cos(recip-alpha) = [cos(beta)*cos(gamma) - cos(alpha)]/[sin(beta)*sin(gamma)] cos(recip-beta) = [cos(gamma)*cos(alpha) - cos(beta)]/[sin(gamma)*sin(alpha)] cos(recip-gamma) = [cos(alpha)*cos(beta) - cos(gamma)]/[sin(alpha)*sin(beta)] Ref: Buerger, M. J. (1942). X-ray Crystallography, p. 360. New York: John Wiley & Sons Inc. |
| reciprocal_angle_beta | double precision | The angle (recip-beta) defining the reciprocal cell in degrees. (recip-alpha), (recip-alpha) and (recip-alpha) related to the angles in the real cell by: cos(recip-alpha) = [cos(beta)*cos(gamma) - cos(alpha)]/[sin(beta)*sin(gamma)] cos(recip-beta) = [cos(gamma)*cos(alpha) - cos(beta)]/[sin(gamma)*sin(alpha)] cos(recip-gamma) = [cos(alpha)*cos(beta) - cos(gamma)]/[sin(alpha)*sin(beta)] Ref: Buerger, M. J. (1942). X-ray Crystallography, p. 360. New York: John Wiley & Sons Inc. |
| reciprocal_angle_gamma | double precision | The angle (recip-gamma) defining the reciprocal cell in degrees. (recip-alpha), (recip-alpha) and (recip-alpha) related to the angles in the real cell by: cos(recip-alpha) = [cos(beta)*cos(gamma) - cos(alpha)]/[sin(beta)*sin(gamma)] cos(recip-beta) = [cos(gamma)*cos(alpha) - cos(beta)]/[sin(gamma)*sin(alpha)] cos(recip-gamma) = [cos(alpha)*cos(beta) - cos(gamma)]/[sin(alpha)*sin(beta)] Ref: Buerger, M. J. (1942). X-ray Crystallography, p. 360. New York: John Wiley & Sons Inc. |
| pdbx_unique_axis | text | To further identify unique axis if necessary. E.g., P 21 with an unique C axis will have 'C' in this field. |

## cell_measurement

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| pressure | double precision | The pressure in kilopascals at which the unit-cell parameters were measured (not the pressure at which the sample was synthesized). |
| reflns_used | integer | The total number of reflections used to determine the unit cell. These reflections may be specified as CELL_MEASUREMENT_REFLN data items. |
| theta_max | double precision | The maximum theta angle of reflections used to measure the unit cell in degrees. |
| theta_min | double precision | The minimum theta angle of reflections used to measure the unit cell in degrees. |

## chem_comp

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| formula | text | The formula for the chemical component. Formulae are written according to the following rules: (1) Only recognized element symbols may be used. (2) Each element symbol is followed by a 'count' number. A count of '1' may be omitted. (3) A space or parenthesis must separate each cluster of (element symbol + count), but in general parentheses are not used. (4) The order of elements depends on whether carbon is present or not. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts. |
| formula_weight | double precision | Formula mass in daltons of the chemical component. |
| id | text | The value of _chem_comp.id must uniquely identify each item in the CHEM_COMP list. For protein polymer entities, this is the three-letter code for the amino acid. For nucleic acid polymer entities, this is the one-letter code for the base. |
| mon_nstd_flag | text | 'yes' indicates that this is a 'standard' monomer, 'no' indicates that it is 'nonstandard'. Nonstandard monomers should be described in more detail using the _chem_comp.mon_nstd_parent, _chem_comp.mon_nstd_class and _chem_comp.mon_nstd_details data items. |
| name | text | The full name of the component. |
| type | text | For standard polymer components, the type of the monomer. Note that monomers that will form polymers are of three types: linking monomers, monomers with some type of N-terminal (or 5') cap and monomers with some type of C-terminal (or 3') cap. |
| pdbx_synonyms | text | Synonym list for the component. |

## chem_comp_atom

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| atom_id | text | The value of _chem_comp_atom.atom_id must uniquely identify each atom in each monomer in the CHEM_COMP_ATOM list. The atom identifiers need not be unique over all atoms in the data block; they need only be unique for each atom in a component. Note that this item need not be a number; it can be any unique identifier. |
| comp_id | text | This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| type_symbol | text | The code used to identify the atom species representing this atom type. Normally this code is the element symbol. |
| pdbx_ordinal | integer | Ordinal index for the component atom list. |
| pdbx_stereo_config | text | The chiral configuration of the atom that is a chiral center. |
| pdbx_aromatic_flag | text | A flag indicating an aromatic atom. |

## chem_comp_bond

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| atom_id_1 | text | The ID of the first of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category. |
| atom_id_2 | text | The ID of the second of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category. |
| comp_id | text | This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| value_order | text | The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order. |
| pdbx_ordinal | integer | Ordinal index for the component bond list. |
| pdbx_stereo_config | text | Stereochemical configuration across a double bond. |
| pdbx_aromatic_flag | text | A flag indicating an aromatic bond. |

## chem_link

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _chem_link.id must uniquely identify each item in the CHEM_LINK list. |

## citation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| abstract | text | Abstract for the citation. This is used most when the citation is extracted from a bibliographic database that contains full text or abstract information. |
| book_id_ISBN | text | The International Standard Book Number (ISBN) code assigned to the book cited; relevant for books or book chapters. |
| book_publisher | text | The name of the publisher of the citation; relevant for books or book chapters. |
| book_publisher_city | text | The location of the publisher of the citation; relevant for books or book chapters. |
| book_title | text | The title of the book in which the citation appeared; relevant for books or book chapters. |
| coordinate_linkage | text | _citation.coordinate_linkage states whether this citation is concerned with precisely the set of coordinates given in the data block. If, for instance, the publication described the same structure, but the coordinates had undergone further refinement prior to the creation of the data block, the value of this data item would be 'no'. |
| country | text | The country/region of publication; relevant for books and book chapters. |
| details | text | A description of special aspects of the relationship of the contents of the data block to the literature item cited. |
| id | text | The value of _citation.id must uniquely identify a record in the CITATION list. The _citation.id 'primary' should be used to indicate the citation that the author(s) consider to be the most pertinent to the contents of the data block. Note that this item need not be a number; it can be any unique identifier. |
| journal_abbrev | text | Abbreviated name of the cited journal as given in the Chemical Abstracts Service Source Index. |
| journal_id_ASTM | text | The American Society for Testing and Materials (ASTM) code assigned to the journal cited (also referred to as the CODEN designator of the Chemical Abstracts Service); relevant for journal articles. |
| journal_id_CSD | text | The Cambridge Structural Database (CSD) code assigned to the journal cited; relevant for journal articles. This is also the system used at the Protein Data Bank (PDB). |
| journal_id_ISSN | text | The International Standard Serial Number (ISSN) code assigned to the journal cited; relevant for journal articles. |
| journal_issue | text | Issue number of the journal cited; relevant for journal articles. |
| journal_volume | text | Volume number of the journal cited; relevant for journal articles. |
| language | text | Language in which the cited article is written. |
| page_first | text | The first page of the citation; relevant for journal articles, books and book chapters. |
| page_last | text | The last page of the citation; relevant for journal articles, books and book chapters. |
| title | text | The title of the citation; relevant for journal articles, books and book chapters. |
| year | integer | The year of the citation; relevant for journal articles, books and book chapters. |
| database_id_CSD | text | Identifier ('refcode') of the database record in the Cambridge Structural Database that contains details of the cited structure. |
| pdbx_database_id_DOI | text | Document Object Identifier used by doi.org to uniquely specify bibliographic entry. |
| pdbx_database_id_PubMed | integer | Ascession number used by PubMed to categorize a specific bibliographic entry. |
| pdbx_database_id_patent | text | If citation is a patent, the accession issued by a patent office. |
| unpublished_flag | text | Flag to indicate that this citation will not be published. |

## citation_author

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| citation_id | text | This data item is a pointer to _citation.id in the CITATION category. |
| name | text | Name of an author of the citation; relevant for journal articles, books and book chapters. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s). |
| ordinal | integer | This data item defines the order of the author's name in the list of authors of a citation. |
| identifier_ORCID | text | The Open Researcher and Contributor ID (ORCID). |

## citation_editor

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| citation_id | text | This data item is a pointer to _citation.id in the CITATION category. |
| name | text | Names of an editor of the citation; relevant for books and book chapters. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s). |
| ordinal | integer | This data item defines the order of the editor's name in the list of editors of a citation. |

## citation_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| journal_abbrev | text |  |
| journal_volume | text |  |
| page_first | text |  |
| page_last | text |  |
| pdbx_database_id_DOI | text |  |
| pdbx_database_id_PubMed | text |  |
| title | text |  |
| year | integer |  |

## database_2

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| database_id | text | An abbreviation that identifies the database. |
| database_code | text | The code assigned by the database identified in _database_2.database_id. |
| pdbx_database_accession | text | Extended accession code issued for for _database_2.database_code assigned by the database identified in _database_2.database_id. |
| pdbx_DOI | text | Document Object Identifier (DOI) for this entry registered with http://crossref.org. |

## database_PDB_caveat

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | A unique identifier for the PDB caveat record. |
| text | text | The full text of the PDB caveat record. |

## database_PDB_matrix

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| origx11 | double precision |  |
| origx12 | double precision |  |
| origx13 | double precision |  |
| origx21 | double precision |  |
| origx22 | double precision |  |
| origx23 | double precision |  |
| origx31 | double precision |  |
| origx32 | double precision |  |
| origx33 | double precision |  |
| origx_vector1 | double precision |  |
| origx_vector2 | double precision |  |
| origx_vector3 | double precision |  |

## database_PDB_tvect

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _database_PDB_tvect.id must uniquely identify a record in the DATABASE_PDB_TVECT list. Note that this item need not be a number; it can be any unique identifier. |
| vector1 | double precision |  |
| vector2 | double precision |  |
| vector3 | double precision |  |

## diffrn

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ambient_environment | text | The gas or liquid surrounding the sample, if not air. |
| ambient_temp | double precision | The mean temperature in kelvins at which the intensities were measured. |
| ambient_temp_details | text | A description of special aspects of temperature control during data collection. |
| crystal_id | text | This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category. |
| crystal_support | text | The physical device used to support the crystal during data collection. |
| crystal_treatment | text | Remarks about how the crystal was treated prior to intensity measurement. Particularly relevant when intensities were measured at low temperature. |
| details | text | Special details of the diffraction measurement process. Should include information about source instability, crystal motion, degradation and so on. |
| id | text | This data item uniquely identifies a set of diffraction data. |
| ambient_pressure | double precision | The mean hydrostatic pressure in kilopascals at which the intensities were measured. |
| pdbx_serial_crystal_experiment | text | Y/N if using serial crystallography experiment in which multiple crystals contribute to each diffraction frame in the experiment. |

## diffrn_detector

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the radiation detector. |
| detector | text | The general class of the radiation detector. |
| diffrn_id | text | This data item is a pointer to _diffrn.id in the DIFFRN category. |
| type | text | The make, model or name of the detector device used. |
| pdbx_collection_date | text | The date of data collection. |
| pdbx_frequency | double precision | The operating frequency of the detector (Hz) used in data collection. |
| id | text | The value of _diffrn_detector.id must uniquely identify each detector used to collect each diffraction data set. If the value of _diffrn_detector.id is not given, it is implicitly equal to the value of _diffrn_detector.diffrn_id. |

## diffrn_measurement

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | This data item is a pointer to _diffrn.id in the DIFFRN category. |
| details | text | A description of special aspects of the intensity measurement. |
| method | text | Method used to measure intensities. |
| specimen_support | text | The physical device used to support the crystal during data collection. |

## diffrn_radiation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| collimation | text | The collimation or focusing applied to the radiation. |
| diffrn_id | text | This data item is a pointer to _diffrn.id in the DIFFRN category. |
| monochromator | text | The method used to obtain monochromatic radiation. If a mono- chromator crystal is used, the material and the indices of the Bragg reflection are specified. |
| type | text | The nature of the radiation. This is typically a description of the X-ray wavelength in Siegbahn notation. |
| wavelength_id | text | This data item is a pointer to _diffrn_radiation_wavelength.id in the DIFFRN_RADIATION_WAVELENGTH category. |
| pdbx_monochromatic_or_laue_m_l | text | Monochromatic or Laue. |
| pdbx_wavelength_list | text | Comma separated list of wavelengths or wavelength range. |
| pdbx_wavelength | text | Wavelength of radiation. |
| pdbx_diffrn_protocol | text | SINGLE WAVELENGTH, LAUE, or MAD. |
| pdbx_analyzer | text | Indicates the method used to obtain monochromatic radiation. _diffrn_radiation.monochromator describes the primary beam monochromator (pre-specimen monochromation). _diffrn_radiation.pdbx_analyzer specifies the post-diffraction analyser (post-specimen) monochromation. Note that monochromators may have either 'parallel' or 'antiparallel' orientation. It is assumed that the geometry is parallel unless specified otherwise. In a parallel geometry, the position of the monochromator allows the incident beam and the final post-specimen and post-monochromator beam to be as close to parallel as possible. In a parallel geometry, the diffracting planes in the specimen and monochromator will be parallel when 2*theta(monochromator) is equal to 2*theta (specimen). For further discussion see R. Jenkins and R. Snyder, Introduction to X-ray Powder Diffraction, Wiley (1996), pp. 164-5. |
| pdbx_scattering_type | text | The radiation scattering type for this diffraction data set. |

## diffrn_radiation_wavelength

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The code identifying each value of _diffrn_radiation_wavelength.wavelength. Items in the DIFFRN_RADIATION_WAVELENGTH category are looped when multiple wavelengths are used. This code is used to link with the DIFFRN_REFLN category. The _diffrn_refln.wavelength_id codes must match one of the codes defined in this category. |
| wavelength | double precision | The radiation wavelength in angstroms. |
| wt | double precision | The relative weight of a wavelength identified by the code _diffrn_radiation_wavelength.id in the list of wavelengths. |

## diffrn_reflns

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| av_R_equivalents | double precision | The residual [sum\|avdel(I)\| / sum\|av(I)\|] for symmetry-equivalent reflections used to calculate the average intensity av(I). The avdel(I) term is the average absolute difference between av(I) and the individual symmetry-equivalent intensities. |
| av_sigmaI_over_netI | double precision | Measure [sum\|sigma(I)\|/sum\|net(I)\|] for all measured reflections. |
| diffrn_id | text | This data item is a pointer to _diffrn.id in the DIFFRN category. |
| limit_h_max | integer | The maximum value of the Miller index h for the reflection data specified by _diffrn_refln.index_h. |
| limit_h_min | integer | The minimum value of the Miller index h for the reflection data specified by _diffrn_refln.index_h. |
| limit_k_max | integer | The maximum value of the Miller index k for the reflection data specified by _diffrn_refln.index_k. |
| limit_k_min | integer | The minimum value of the Miller index k for the reflection data specified by _diffrn_refln.index_k. |
| limit_l_max | integer | The maximum value of the Miller index l for the reflection data specified by _diffrn_refln.index_l. |
| limit_l_min | integer | The minimum value of the Miller index l for the reflection data specified by _diffrn_refln.index_l. |
| number | integer | The total number of measured intensities, excluding reflections that are classified as systematically absent. |
| theta_max | double precision | Maximum theta angle in degrees for the measured diffraction intensities. |
| theta_min | double precision | Minimum theta angle in degrees for the measured diffraction intensities. |
| pdbx_d_res_low | double precision | The lowest resolution for the interplanar spacings in the reflection data set. This is the largest d value. |
| pdbx_d_res_high | double precision | The highest resolution for the interplanar spacings in the reflection data set. This is the smallest d value. |
| pdbx_percent_possible_obs | double precision | The percentage of geometrically possible reflections represented by reflections that satisfy the resolution limits established by _diffrn_reflns.d_resolution_high and _diffrn_reflns.d_resolution_low and the observation limit established by _diffrn_reflns.observed_criterion. |
| pdbx_Rmerge_I_obs | double precision | The R factor for merging the reflections that satisfy the resolution limits established by _diffrn_reflns.d_resolution_high and _diffrn_reflns.d_resolution_low and the observation limit established by _diffrn_reflns.observed_criterion. Rmerge(I) = [sum~i~(sum~j~\|I~j~ - \|)] / [sum~i~(sum~j~)] I~j~ = the intensity of the jth observation of reflection i = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| pdbx_Rsym_value | double precision | The R factor for averaging the symmetry related reflections to a unique data set. |
| pdbx_chi_squared | double precision | Overall Chi-squared statistic for the data set. |
| pdbx_redundancy | double precision | The overall redundancy for the data set. |
| pdbx_rejects | integer | The number of rejected reflections in the data set. The reflections may be rejected by setting the observation criterion, _diffrn_reflns.observed_criterion. |
| pdbx_number_obs | integer | The number of reflections satisfying the observation criterion as in _diffrn_reflns.pdbx_observed_criterion |

## diffrn_source

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| current | double precision | The current in milliamperes at which the radiation source was operated. |
| details | text | A description of special aspects of the radiation source used. |
| diffrn_id | text | This data item is a pointer to _diffrn.id in the DIFFRN category. |
| power | double precision | The power in kilowatts at which the radiation source was operated. |
| size | text | The dimensions of the source as viewed from the sample. |
| source | text | The general class of the radiation source. |
| target | text | The chemical element symbol for the X-ray target (usually the anode) used to generate X-rays. This can also be used for spallation sources. |
| type | text | The make, model or name of the source of radiation. |
| voltage | double precision | The voltage in kilovolts at which the radiation source was operated. |
| take-off_angle | double precision |  |
| pdbx_wavelength_list | text | Comma separated list of wavelengths or wavelength range. |
| pdbx_wavelength | text | Wavelength of radiation. |
| pdbx_synchrotron_beamline | text | Synchrotron beamline. |
| pdbx_synchrotron_site | text | Synchrotron site. |

## em_2d_crystal_entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| angle_gamma | double precision | Unit-cell angle gamma in degrees. |
| c_sampling_length | double precision | Length used to sample the reciprocal lattice lines in the c-direction. |
| image_processing_id | text | pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category. |
| id | text | PRIMARY KEY |
| length_a | double precision | Unit-cell length a in angstroms. |
| length_b | double precision | Unit-cell length b in angstroms. |
| length_c | double precision | Thickness of 2D crystal |
| space_group_name_H-M | text |  |

## em_3d_crystal_entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| angle_alpha | double precision | Unit-cell angle alpha in degrees. |
| angle_beta | double precision | Unit-cell angle beta in degrees. |
| angle_gamma | double precision | Unit-cell angle gamma in degrees. |
| image_processing_id | text | pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category. |
| id | text | PRIMARY KEY |
| length_a | double precision | Unit-cell length a in angstroms. |
| length_b | double precision | Unit-cell length b in angstroms. |
| length_c | double precision | Unit-cell length c in angstroms. |
| space_group_name | text | Space group name. |
| space_group_num | integer | Space group number. |

## em_3d_fitting

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _em_3d_fitting.id must uniquely identify a fitting procedure of atomic coordinates into 3dem reconstructed map volume. |
| entry_id | text | This data item is a pointer to _entry_id in the ENTRY category. |
| method | text | The method used to fit atomic coordinates into the 3dem reconstructed map. |
| target_criteria | text | The measure used to assess quality of fit of the atomic coordinates in the 3DEM map volume. |
| details | text | Any additional details regarding fitting of atomic coordinates into the 3DEM volume, including data and considerations from other methods used in computation of the model. |
| overall_b_value | double precision | The overall B (temperature factor) value for the 3d-em volume. |
| ref_space | text | A flag to indicate whether fitting was carried out in real or reciprocal refinement space. |
| ref_protocol | text | The refinement protocol used. |

## em_3d_fitting_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | PRIMARY KEY |
| 3d_fitting_id | text | The value of _em_3d_fitting_list.3d_fitting_id is a pointer to _em_3d_fitting.id in the 3d_fitting category |
| pdb_entry_id | text | The PDB code for the entry used in fitting. |
| pdb_chain_id | text | The ID of the biopolymer chain used for fitting, e.g., A. Please note that only one chain can be specified per instance. If all chains of a particular structure have been used for fitting, this field can be left blank. |
| pdb_chain_residue_range | text | Residue range for the identified chain. |
| details | text | Details about the model used in fitting. |
| chain_id | text | The ID of the biopolymer chain used for fitting, e.g., A. Please note that only one chain can be specified per instance. If all chains of a particular structure have been used for fitting, this field can be left blank. |
| chain_residue_range | text | The residue ranges of the initial model used in this fitting. |
| source_name | text | This item identifies the resource of initial model used for refinement |
| type | text | This item describes the type of the initial model was generated |
| accession_code | text | This item identifies an accession code of the resource where the initial model is used |
| initial_refinement_model_id | integer | The value of _em_3d_fitting.initial_refinement_model_id itentifies the id in the _pdbx_initial_refinement_model |

## em_3d_reconstruction

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | text | PRIMARY KEY |
| method | text | The algorithm method used for the 3d-reconstruction. |
| algorithm | text | The reconstruction algorithm/technique used to generate the map. |
| details | text | Any additional details used in the 3d reconstruction. |
| resolution | double precision | The final resolution (in angstroms) of the 3D reconstruction. |
| resolution_method | text | The method used to determine the final resolution of the 3d reconstruction. The Fourier Shell Correlation criterion as a measure of resolution is based on the concept of splitting the (2D) data set into two halves; averaging each and comparing them using the Fourier Ring Correlation (FRC) technique. |
| magnification_calibration | text | The magnification calibration method for the 3d reconstruction. |
| nominal_pixel_size | double precision | The nominal pixel size of the projection set of images in Angstroms. |
| actual_pixel_size | double precision | The actual pixel size of the projection set of images in Angstroms. |
| num_particles | integer | The number of 2D projections or 3D subtomograms used in the 3d reconstruction |
| num_class_averages | integer | The number of classes used in the final 3d reconstruction |
| refinement_type | text | Indicates details on how the half-map used for resolution determination (usually by FSC) have been generated. |
| image_processing_id | text | Foreign key to the EM_IMAGE_PROCESSING category |
| symmetry_type | text | The type of symmetry applied to the reconstruction |

## em_admin

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| current_status | text | This data item indicates the current status of the EMDB entry. |
| deposition_date | date | date of the entry deposition |
| deposition_site | text | entry deposition site |
| entry_id | text | This data item is a pointer to _entry.id. |
| last_update | date | date of last update to the file |
| map_release_date | date | date of map release for this entry |
| title | text | Title for the EMDB entry. |

## em_buffer

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | PRIMARY KEY |
| specimen_id | text | pointer to _em_specimen.id |
| name | text | The name of the buffer. |
| details | text | Additional details about the buffer. |
| pH | double precision | The pH of the sample buffer. |

## em_buffer_component

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| buffer_id | text | Foreign key to the entry category. |
| concentration | double precision | The concentration of the sample (arbitrary units). |
| concentration_units | text | Units for the sample concentration value. |
| formula | text | formula for buffer component |
| id | text | PRIMARY KEY |
| name | text | name of the buffer component |

## em_crystal_formation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| atmosphere | text | The type of atmosphere in which crystals were grown |
| details | text | Description of growth of a 2D, 3D, or helical crystal array. |
| id | text | PRIMARY KEY |
| instrument | text | Instrument used to prepare the crystalline array |
| lipid_mixture | text | Description of the lipid mixture used for crystallization |
| lipid_protein_ratio | double precision | The molar ratio of lipid to protein in the crystallized sample |
| specimen_id | text | Foreign key relationship to the em_specimen category |
| temperature | integer | The value of the temperature in kelvin used for growing the crystals. |
| time | integer | Time period for array crystallization, in time unit indicated (min, hr, day, month, year) |
| time_unit | text | Time unit for array crystallization |

## em_ctf_correction

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Any additional details about CTF correction |
| em_image_processing_id | text | Foreign key to the EM_IMAGE_PROCESSING category |
| id | text | PRIMARY KEY |
| type | text | Type of CTF correction applied |

## em_diffraction

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| camera_length | double precision | The camera length (in millimeters). The camera length is the product of the objective focal length and the combined magnification of the intermediate and projector lenses when the microscope is operated in the diffraction mode. |
| id | text | PRIMARY KEY |
| imaging_id | text | Foreign key to the EM_IMAGING category |
| tilt_angle_list | text | Comma-separated list of tilt angles (in degrees) used in the electron diffraction experiment. |

## em_diffraction_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| em_diffraction_stats_id | text | Pointer to EM CRYSTALLOGRAPHY STATS |
| fourier_space_coverage | double precision | Completeness of the structure factor data within this resolution shell, in percent |
| high_resolution | double precision | High resolution limit for this shell (angstroms) |
| id | text | PRIMARY KEY |
| low_resolution | double precision | Low resolution limit for this shell (angstroms) |
| multiplicity | double precision | Multiplicity (average number of measurements) for the structure factors in this resolution shell |
| num_structure_factors | integer | Number of measured structure factors in this resolution shell |
| phase_residual | double precision | Phase residual for this resolution shell, in degrees |

## em_diffraction_stats

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Any addition details about the structure factor measurements |
| fourier_space_coverage | double precision | Completeness of the structure factor data within the defined space group at the reported resolution (percent). |
| high_resolution | double precision | High resolution limit of the structure factor data, in angstroms |
| id | text | PRIMARY KEY |
| image_processing_id | text | Pointer to _em_image_processing.id |
| num_intensities_measured | integer | Total number of diffraction intensities measured (before averaging) |
| num_structure_factors | integer | Number of structure factors obtained (merged amplitudes + phases) |
| overall_phase_error | double precision | Overall phase error in degrees |
| overall_phase_residual | double precision | Overall phase residual in degrees |
| phase_error_rejection_criteria | text | Criteria used to reject phases |
| r_merge | double precision | Rmerge value (percent) |
| r_sym | double precision | Rsym value (percent) |

## em_embedding

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Staining procedure used in the specimen preparation. |
| id | text | PRIMARY KEY |
| material | text | The embedding material. |
| specimen_id | text | Foreign key relationship to the EM SPECIMEN category |

## em_entity_assembly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | PRIMARY KEY |
| parent_id | integer | The parent of this assembly. This data item is an internal category pointer to _em_entity_assembly.id. By convention, the full assembly (top of hierarchy) is assigned parent id 0 (zero). |
| source | text | The type of source (e.g., natural source) for the component (sample or sample subcomponent) |
| type | text | The general type of the sample or sample subcomponent. |
| name | text | The name of the sample or sample subcomponent. |
| details | text | Additional details about the sample or sample subcomponent. |
| synonym | text | Alternative name of the component. |
| oligomeric_details | text | oligomeric details |
| entity_id_list | text | macromolecules associated with this component, if defined as comma separated list of entity ids (integers). |

## em_entity_assembly_molwt

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_assembly_id | text | A reference to em_entity_assembly.id which uniquely identifies one sample or sample subcomponent of the imaged specimen. |
| experimental_flag | text | Identifies whether the given molecular weight was derived experimentally. |
| id | text | PRIMARY KEY |
| units | text | Molecular weight units. |
| value | double precision | The molecular weight of the sample or sample subcomponent |

## em_entity_assembly_naturalsource

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| cell | text | The cell type from which the component was obtained. |
| cellular_location | text | The cellular location of the component. |
| entity_assembly_id | text | Pointer to the assembly component defined in the EM ENTITY ASSEMBLY category. |
| id | text | PRIMARY KEY |
| ncbi_tax_id | integer | The NCBI taxonomy id for the natural organism source of the component. |
| organism | text | The scientific name of the source organism for the component |
| organelle | text | The organelle from which the component was obtained. |
| organ | text | The organ of the organism from which the component was obtained. |
| strain | text | The strain of the natural organism from which the component was obtained, if relevant. |
| tissue | text | The tissue of the natural organism from which the component was obtained. |
| details | text | Additional details describing this natural source. |

## em_entity_assembly_recombinant

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| cell | text | The cell of the host organism from which the expressed component was obtained, if relevant. |
| entity_assembly_id | text | Pointer to the expressed component described in the EM ENTITY ASSEMBLY category. |
| id | text | PRIMARY KEY |
| ncbi_tax_id | integer | The NCBI taxonomy id of the expression host used to produce the component. |
| organism | text | Expression system host organism used to produce the component. |
| plasmid | text | The plasmid used to produce the component in the expression system. |
| strain | text | The strain of the host organism from which the expresed component was obtained, if relevant. |

## em_entity_assembly_synthetic

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_assembly_id | text | Pointer to the assembly component defined in the EM ENTITY ASSEMBLY category. |
| id | text | PRIMARY KEY |
| ncbi_tax_id | integer | The NCBI taxonomy id for the synthetic organism source of the component. |
| organism | text | The scientific name of the source organism for the component |
| strain | text | The strain of the synthetic organism from which the component was obtained, if relevant. |

## em_experiment

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | text | PRIMARY KEY |
| reconstruction_method | text | The reconstruction method used in the EM experiment. |
| aggregation_state | text | The aggregation/assembly state of the imaged specimen. |
| entity_assembly_id | text | Foreign key to the EM_ENTITY_ASSEMBLY category |

## em_helical_entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | PRIMARY KEY |
| image_processing_id | text | This data item is a pointer to _em_image_processing.id. |
| details | text | Any other details regarding the helical assembly |
| axial_symmetry | text | Symmetry of the helical axis, either cyclic (Cn) or dihedral (Dn), where n>=1. |
| angular_rotation_per_subunit | double precision | The angular rotation per helical subunit in degrees. Negative values indicate left-handed helices; positive values indicate right handed helices. |
| axial_rise_per_subunit | double precision | The axial rise per subunit in the helical assembly. |

## em_image_processing

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Method details. |
| id | text | PRIMARY KEY |
| image_recording_id | text | Foreign key to the EM_IMAGE_RECORDING |

## em_image_recording

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| average_exposure_time | double precision | The average exposure time for each image. |
| avg_electron_dose_per_subtomogram | double precision | The average total electron dose received by the specimen for each subtomogram (electrons per square angstrom). |
| avg_electron_dose_per_image | double precision | The electron dose received by the specimen per image (electrons per square angstrom). |
| details | text | Any additional details about image recording. |
| detector_mode | text | The detector mode used during image recording. |
| film_or_detector_model | text | The detector type used for recording images. Usually film , CCD camera or direct electron detector. |
| id | text | PRIMARY KEY |
| imaging_id | text | This data item the id of the microscopy settings used in the imaging. |
| num_diffraction_images | integer | The number of diffraction images collected. |
| num_grids_imaged | integer | Number of grids in the microscopy session |
| num_real_images | integer | The number of micrograph images collected. |

## em_image_scans

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | text | The value of _em_image_scans.id must uniquely identify the images scanned. |
| number_digital_images | integer | The number of real images. |
| details | text | Any additional details about image recording. |
| scanner_model | text | The scanner model. |
| sampling_size | double precision | The sampling step size (microns) set on the scanner. |
| od_range | double precision | The optical density range (OD=-log 10 transmission). To the eye OD=1 appears light grey and OD=3 is opaque. |
| quant_bit_size | integer | The number of bits per pixel. |
| dimension_height | integer | Height of scanned image, in pixels |
| dimension_width | integer | Width of scanned image, in pixels |
| frames_per_image | integer | Total number of time-slice (movie) frames taken per image. |
| image_recording_id | text | foreign key linked to _em_image_recording |
| used_frames_per_image | text | Range of time-slice (movie) frames used for the reconstruction. |

## em_imaging

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | text | PRIMARY KEY |
| astigmatism | text | astigmatism |
| electron_beam_tilt_params | text | electron beam tilt params |
| residual_tilt | double precision | Residual tilt of the electron beam (in miliradians) |
| microscope_model | text | The name of the model of microscope. |
| specimen_holder_type | text | The type of specimen holder used during imaging. |
| specimen_holder_model | text | The name of the model of specimen holder used during imaging. |
| details | text | Any additional imaging details. |
| date | date | Date (YYYY-MM-DD) of imaging experiment or the date at which a series of experiments began. |
| accelerating_voltage | integer | A value of accelerating voltage (in kV) used for imaging. |
| illumination_mode | text | The mode of illumination. |
| mode | text | The mode of imaging. |
| nominal_cs | double precision | The spherical aberration coefficient (Cs) in millimeters, of the objective lens. |
| nominal_defocus_min | double precision | The minimum defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus. |
| nominal_defocus_max | double precision | The maximum defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus. |
| calibrated_defocus_min | double precision | The minimum calibrated defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus. |
| calibrated_defocus_max | double precision | The maximum calibrated defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus. |
| tilt_angle_min | double precision | The minimum angle at which the specimen was tilted to obtain recorded images. |
| tilt_angle_max | double precision | The maximum angle at which the specimen was tilted to obtain recorded images. |
| nominal_magnification | integer | The magnification indicated by the microscope readout. |
| calibrated_magnification | integer | The magnification value obtained for a known standard just prior to, during or just after the imaging experiment. |
| electron_source | text | The source of electrons. The electron gun. |
| temperature | double precision | The mean specimen stage temperature (in kelvin) during imaging in the microscope. |
| detector_distance | double precision | The camera length (in millimeters). The camera length is the product of the objective focal length and the combined magnification of the intermediate and projector lenses when the microscope is operated in the diffraction mode. |
| recording_temperature_minimum | double precision | The specimen temperature minimum (kelvin) for the duration of imaging. |
| recording_temperature_maximum | double precision | The specimen temperature maximum (kelvin) for the duration of imaging. |
| alignment_procedure | text | The type of procedure used to align the microscope electron beam. |
| c2_aperture_diameter | double precision | The open diameter of the c2 condenser lens, in microns. |
| specimen_id | text | Foreign key to the EM_SPECIMEN category |
| cryogen | text | Cryogen type used to maintain the specimen stage temperature during imaging in the microscope. |

## em_imaging_optics

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| chr_aberration_corrector | text | Chromatic aberration corrector information |
| energyfilter_lower | text | The energy filter range lower value in electron volts (eV) set by spectrometer. |
| energyfilter_slit_width | double precision | The energy filter range slit width in electron volts (eV). |
| energyfilter_name | text | The type of energy filter spectrometer |
| energyfilter_upper | text | The energy filter range upper value in electron volts (eV) set by spectrometer. |
| id | text | PRIMARY KEY |
| imaging_id | text | Foreign key to the EM IMAGING category |
| phase_plate | text | Phase plate information |
| sph_aberration_corrector | text | Spherical aberration corrector information |
| details | text | Details on the use of the phase plate |

## em_particle_selection

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Additional detail such as description of filters used, if selection was manual or automated, and/or template details. |
| id | text | PRIMARY KEY |
| image_processing_id | text | The value of _em_particle_selection.image_processing_id points to the EM_IMAGE_PROCESSING category. |
| num_particles_selected | bigint | The number of particles selected from the projection set of images. |

## em_sample_support

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | PRIMARY KEY |
| film_material | text | The support material covering the em grid. |
| grid_material | text | The name of the material from which the grid is made. |
| grid_mesh_size | integer | The value of the mesh size (divisions per inch) of the em grid. |
| grid_type | text | A description of the grid type. |
| details | text | Any additional details concerning the sample support. |
| specimen_id | text | This data item is a pointer to _em_sample_preparation.id in the EM_SPECIMEN category. |

## em_single_particle_entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | integer | PRIMARY KEY |
| image_processing_id | text | pointer to _em_image_processing.id. |
| point_symmetry | text | Point symmetry symbol, either Cn, Dn, T, O, or I |

## em_software

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| category | text | The purpose of the software. |
| details | text | Details about the software used. |
| id | text | PRIMARY KEY |
| image_processing_id | text | pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category. |
| fitting_id | text | pointer to _em_3d_fitting.id in the EM_3D_FITTING category. |
| imaging_id | text | pointer to _em_imaging.id in the EM_IMAGING category. |
| name | text | The name of the software package used, e.g., RELION. Depositors are strongly encouraged to provide a value in this field. |
| version | text | The version of the software. |

## em_specimen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| concentration | double precision | The concentration (in milligrams per milliliter, mg/ml) of the complex in the sample. |
| details | text | A description of any additional details of the specimen preparation. |
| embedding_applied | boolean | 'YES' indicates that the specimen has been embedded. |
| experiment_id | text | Pointer to _em_experiment.id. |
| id | text | PRIMARY KEY |
| shadowing_applied | boolean | 'YES' indicates that the specimen has been shadowed. |
| staining_applied | boolean | 'YES' indicates that the specimen has been stained. |
| vitrification_applied | boolean | 'YES' indicates that the specimen was vitrified by cryopreservation. |

## em_staining

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Staining procedure used in the specimen preparation. |
| id | text | PRIMARY KEY |
| material | text | The staining material. |
| specimen_id | text | Foreign key relationship to the EM SPECIMEN category |
| type | text | type of staining |

## em_virus_entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | PRIMARY KEY |
| virus_host_category | text | The host category description for the virus. |
| virus_type | text | The type of virus. |
| virus_isolate | text | The isolate from which the virus was obtained. |
| entity_assembly_id | text | This data item is a pointer to _em_virus_entity.id in the ENTITY_ASSEMBLY category. |
| enveloped | text | Flag to indicate if the virus is enveloped or not. |
| empty | text | Flag to indicate if the virus is empty or not. |
| details | text | Additional details about this virus entity |

## em_virus_natural_host

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_assembly_id | text | Pointer to _em_entity_assembly.id. |
| id | text | PRIMARY KEY |
| ncbi_tax_id | integer | The NCBI taxonomy id for the natural host organism of the virus |
| organism | text | The host organism from which the virus was isolated. |
| strain | text | The strain of the host organism from which the virus was obtained, if relevant. |

## em_virus_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diameter | double precision | The value of the diameter (in angstroms) for this virus shell. |
| entity_assembly_id | text | The value of _em_virus_shell.entity_assembly_id is a pointer to _em_entity_assembly.id category. |
| id | text | PRIMARY KEY |
| name | text | The name for this virus shell. |
| triangulation | integer | The triangulation number, T, describes the organization of subunits within an icosahedron. T is defined as T= h^2 + h*k + k^2, where h and k are positive integers that define the position of the five-fold vertex on the original hexagonal net. |

## em_virus_synthetic

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_assembly_id | text | Pointer to _em_entity_assembly.id. |
| id | text | PRIMARY KEY |
| organism | text | The host organism from which the virus was isolated. |
| ncbi_tax_id | integer | The NCBI taxonomy ID of the host species from which the virus was isolated |
| strain | text | The strain of the host organism from which the virus was obtained, if relevant. |

## em_vitrification

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | text | PRIMARY KEY |
| specimen_id | text | This data item is a pointer to _em_specimen.id |
| cryogen_name | text | This is the name of the cryogen. |
| humidity | double precision | Relative humidity (%) of air surrounding the specimen just prior to vitrification. |
| temp | double precision | The vitrification temperature (in kelvin), e.g., temperature of the plunge instrument cryogen bath. |
| chamber_temperature | double precision | The temperature (in kelvin) of the sample just prior to vitrification. |
| instrument | text | The type of instrument used in the vitrification process. |
| method | text | The procedure for vitrification. |
| time_resolved_state | text | The length of time after an event effecting the sample that vitrification was induced and a description of the event. |
| details | text | Any additional details relating to vitrification. |

## em_volume_selection

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | Any additional details used for selecting volumes. |
| id | text | PRIMARY KEY |
| image_processing_id | text | The value of _em_volume_selection.image_processing_id points to the EM_IMAGE_PROCESSING category. |
| method | text | The method used for selecting volumes. |
| num_tomograms | integer | The number of tomograms used in the extraction/selection |
| num_volumes_extracted | integer | The number of volumes selected from the projection set of images. |
| reference_model | text | Description of reference model used for volume selection |

## entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the entity. |
| formula_weight | double precision | Formula mass in daltons of the entity. |
| id | text | The value of _entity.id must uniquely identify a record in the ENTITY list. Note that this item need not be a number; it can be any unique identifier. |
| src_method | text | The method by which the sample for the entity was produced. Entities isolated directly from natural sources (tissues, soil samples etc.) are expected to have further information in the ENTITY_SRC_NAT category. Entities isolated from genetically manipulated sources are expected to have further information in the ENTITY_SRC_GEN category. |
| type | text | Defines the type of the entity. Polymer entities are expected to have corresponding ENTITY_POLY and associated entries. Non-polymer entities are expected to have corresponding CHEM_COMP and associated entries. Water entities are not expected to have corresponding entries in the ENTITY category. |
| pdbx_description | text | A description of the entity. Corresponds to the compound name in the PDB format. |
| pdbx_number_of_molecules | integer | A place holder for the number of molecules of the entity in the entry. |
| pdbx_mutation | text | Details about any entity mutation(s). |
| pdbx_fragment | text | Entity fragment description(s). |
| pdbx_ec | text | Enzyme Commission (EC) number(s) |

## entity_keywords

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| text | text | Keywords describing this entity. |

## entity_name_com

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| name | text | A common name for the entity. |

## entity_name_sys

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| name | text | The systematic name for the entity. |

## entity_poly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| nstd_linkage | text | A flag to indicate whether the polymer contains at least one monomer-to-monomer link different from that implied by _entity_poly.type. |
| nstd_monomer | text | A flag to indicate whether the polymer contains at least one monomer that is not considered standard. |
| type | text | The type of the polymer. |
| pdbx_strand_id | text | The PDB strand/chain id(s) corresponding to this polymer entity. |
| pdbx_seq_one_letter_code | text | Sequence of protein or nucleic acid polymer in standard one-letter codes of amino acids or nucleotides. Non-standard amino acids/nucleotides are represented by their Chemical Component Dictionary (CCD) codes in parenthesis. Deoxynucleotides are represented by the specially-assigned 2-letter CCD codes in parenthesis, with 'D' prefix added to their ribonucleotide counterparts. For hybrid polymer, each residue is represented by the code of its individual type. A cyclic polymer is represented in linear sequence from the chosen start to end. A for Alanine or Adenosine-5'-monophosphate C for Cysteine or Cytidine-5'-monophosphate D for Aspartic acid E for Glutamic acid F for Phenylalanine G for Glycine or Guanosine-5'-monophosphate H for Histidine I for Isoleucine or Inosinic Acid L for Leucine K for Lysine M for Methionine N for Asparagine or Unknown ribonucleotide O for Pyrrolysine P for Proline Q for Glutamine R for Arginine S for Serine T for Threonine U for Selenocysteine or Uridine-5'-monophosphate V for Valine W for Tryptophan Y for Tyrosine (DA) for 2'-deoxyadenosine-5'-monophosphate (DC) for 2'-deoxycytidine-5'-monophosphate (DG) for 2'-deoxyguanosine-5'-monophosphate (DT) for Thymidine-5'-monophosphate (MSE) for Selenomethionine (SEP) for Phosphoserine (TPO) for Phosphothreonine (PTR) for Phosphotyrosine (PCA) for Pyroglutamic acid (UNK) for Unknown amino acid (ACE) for Acetylation cap (NH2) for Amidation cap |
| pdbx_seq_one_letter_code_can | text | Canonical sequence of protein or nucleic acid polymer in standard one-letter codes of amino acids or nucleotides, corresponding to the sequence in _entity_poly.pdbx_seq_one_letter_code. Non-standard amino acids/nucleotides are represented by the codes of their parents if parent is specified in _chem_comp.mon_nstd_parent_comp_id, or by letter 'X' if parent is not specified. Deoxynucleotides are represented by their canonical one-letter codes of A, C, G, or T. For modifications with several parent amino acids, all corresponding parent amino acid codes will be listed (ex. chromophores). |
| pdbx_target_identifier | text | For Structural Genomics entries, the sequence's target identifier registered at the TargetTrack database. |

## entity_poly_seq

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| hetero | text | A flag to indicate whether this monomer in the polymer is heterogeneous in sequence. |
| mon_id | text | This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| num | integer | The value of _entity_poly_seq.num must uniquely and sequentially identify a record in the ENTITY_POLY_SEQ list. Note that this item must be a number and that the sequence numbers must progress in increasing numerical order. |

## entity_src_gen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| gene_src_common_name | text | The common name of the natural organism from which the gene was obtained. |
| gene_src_details | text | A description of special aspects of the natural organism from which the gene was obtained. |
| gene_src_genus | text | The genus of the natural organism from which the gene was obtained. |
| gene_src_species | text | The species of the natural organism from which the gene was obtained. |
| gene_src_strain | text | The strain of the natural organism from which the gene was obtained, if relevant. |
| gene_src_tissue | text | The tissue of the natural organism from which the gene was obtained. |
| gene_src_tissue_fraction | text | The subcellular fraction of the tissue of the natural organism from which the gene was obtained. |
| host_org_genus | text | The genus of the organism that served as host for the production of the entity. |
| host_org_species | text | The species of the organism that served as host for the production of the entity. |
| pdbx_gene_src_fragment | text | A domain or fragment of the molecule. |
| pdbx_gene_src_gene | text | Identifies the gene. |
| pdbx_gene_src_scientific_name | text | Scientific name of the organism. |
| pdbx_gene_src_variant | text | Identifies the variant. |
| pdbx_gene_src_cell_line | text | The specific line of cells. |
| pdbx_gene_src_atcc | text | American Type Culture Collection tissue culture number. |
| pdbx_gene_src_organ | text | Organized group of tissues that carries on a specialized function. |
| pdbx_gene_src_organelle | text | Organized structure within cell. |
| pdbx_gene_src_cell | text | Cell type. |
| pdbx_gene_src_cellular_location | text | Identifies the location inside (or outside) the cell. |
| pdbx_host_org_gene | text | Specific gene which expressed the molecule. |
| pdbx_host_org_organ | text | Specific organ which expressed the molecule. |
| pdbx_host_org_organelle | text | Specific organelle which expressed the molecule. |
| pdbx_host_org_cellular_location | text | Identifies the location inside (or outside) the cell which expressed the molecule. |
| pdbx_host_org_strain | text | The strain of the organism in which the entity was expressed. |
| pdbx_host_org_tissue_fraction | text | The fraction of the tissue which expressed the molecule. |
| pdbx_description | text | Information on the source which is not given elsewhere. |
| host_org_common_name | text | The common name of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item be derived from _entity_src_gen_express.host_org_common_name or via _entity_src_gen_express.host_org_tax_id |
| host_org_details | text | A description of special aspects of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item would derived from _entity_src_gen_express.host_org_details |
| plasmid_details | text | A description of special aspects of the plasmid that produced the entity in the host organism. Where full details of the protein production are available it would be expected that this item would be derived from _pdbx_construct.details of the construct pointed to from _entity_src_gen_express.plasmid_id. |
| plasmid_name | text | The name of the plasmid that produced the entity in the host organism. Where full details of the protein production are available it would be expected that this item would be derived from _pdbx_construct.name of the construct pointed to from _entity_src_gen_express.plasmid_id. |
| pdbx_host_org_variant | text | Variant of the organism used as the expression system. Where full details of the protein production are available it would be expected that this item be derived from entity_src_gen_express.host_org_variant or via _entity_src_gen_express.host_org_tax_id |
| pdbx_host_org_cell_line | text | A specific line of cells used as the expression system. Where full details of the protein production are available it would be expected that this item would be derived from entity_src_gen_express.host_org_cell_line |
| pdbx_host_org_atcc | text | Americal Tissue Culture Collection of the expression system. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_culture_collection |
| pdbx_host_org_culture_collection | text | Culture collection of the expression system. Where full details of the protein production are available it would be expected that this item would be derived somehwere, but exactly where is not clear. |
| pdbx_host_org_cell | text | Cell type from which the gene is derived. Where entity.target_id is provided this should be derived from details of the target. |
| pdbx_host_org_scientific_name | text | The scientific name of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_scientific_name or via _entity_src_gen_express.host_org_tax_id |
| pdbx_host_org_tissue | text | The specific tissue which expressed the molecule. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_tissue |
| pdbx_host_org_vector | text | Identifies the vector used. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_clone.vector_name. |
| pdbx_host_org_vector_type | text | Identifies the type of vector used (plasmid, virus, or cosmid). Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.vector_type. |
| expression_system_id | text | A unique identifier for the expression system. This should be extracted from a local list of expression systems. |
| pdbx_gene_src_ncbi_taxonomy_id | text | NCBI Taxonomy identifier for the gene source organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18. |
| pdbx_host_org_ncbi_taxonomy_id | text | NCBI Taxonomy identifier for the expression system organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18. |
| pdbx_src_id | integer | This data item is an ordinal identifier for entity_src_gen data records. |
| pdbx_alt_source_flag | text | This data item identifies cases in which an alternative source modeled. |
| pdbx_seq_type | text | This data item povides additional information about the sequence type. |
| pdbx_beg_seq_num | integer | The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category. |
| pdbx_end_seq_num | integer | The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category. |

## entity_src_nat

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| common_name | text | The common name of the organism from which the entity was isolated. |
| details | text | A description of special aspects of the organism from which the entity was isolated. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| genus | text | The genus of the organism from which the entity was isolated. |
| species | text | The species of the organism from which the entity was isolated. |
| strain | text | The strain of the organism from which the entity was isolated. |
| tissue | text | The tissue of the organism from which the entity was isolated. |
| tissue_fraction | text | The subcellular fraction of the tissue of the organism from which the entity was isolated. |
| pdbx_organism_scientific | text | Scientific name of the organism of the natural source. |
| pdbx_secretion | text | Identifies the secretion from which the molecule was isolated. |
| pdbx_fragment | text | A domain or fragment of the molecule. |
| pdbx_variant | text | Identifies the variant. |
| pdbx_cell_line | text | The specific line of cells. |
| pdbx_atcc | text | Americal Tissue Culture Collection number. |
| pdbx_cellular_location | text | Identifies the location inside (or outside) the cell. |
| pdbx_organ | text | Organized group of tissues that carries on a specialized function. |
| pdbx_organelle | text | Organized structure within cell. |
| pdbx_cell | text | A particular cell type. |
| pdbx_plasmid_name | text | The plasmid containing the gene. |
| pdbx_plasmid_details | text | Details about the plasmid. |
| pdbx_ncbi_taxonomy_id | text | NCBI Taxonomy identifier for the source organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18. |
| pdbx_src_id | integer | This data item is an ordinal identifier for entity_src_nat data records. |
| pdbx_alt_source_flag | text | This data item identifies cases in which an alternative source modeled. |
| pdbx_beg_seq_num | integer | The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category. |
| pdbx_end_seq_num | integer | The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category. |

## entry

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _entry.id identifies the data block. Note that this item need not be a number; it can be any unique identifier. |

## exptl

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| absorpt_correction_T_max | double precision | The maximum transmission factor for the crystal and radiation. The maximum and minimum transmission factors are also referred to as the absorption correction A or 1/A*. |
| absorpt_correction_T_min | double precision | The minimum transmission factor for the crystal and radiation. The maximum and minimum transmission factors are also referred to as the absorption correction A or 1/A*. |
| absorpt_correction_type | text | The absorption correction type and method. The value 'empirical' should NOT be used unless more detailed information is not available. |
| absorpt_process_details | text | Description of the absorption process applied to the intensities. A literature reference should be supplied for psi-scan techniques. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| crystals_number | integer | The total number of crystals used in the measurement of intensities. |
| details | text | Any special information about the experimental work prior to the intensity measurement. See also _exptl_crystal.preparation. |
| method | text | The method used in the experiment. |
| method_details | text | A description of special aspects of the experimental method. |

## exptl_crystal

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| colour | text | The colour of the crystal. |
| density_Matthews | double precision | The density of the crystal, expressed as the ratio of the volume of the asymmetric unit to the molecular mass of a monomer of the structure, in units of angstroms^3^ per dalton. Ref: Matthews, B. W. (1968). J. Mol. Biol. 33, 491-497. |
| density_percent_sol | double precision | Density value P calculated from the crystal cell and contents, expressed as per cent solvent. P = 1 - (1.23 N MMass) / V N = the number of molecules in the unit cell MMass = the molecular mass of each molecule (gm/mole) V = the volume of the unit cell (A^3^) 1.23 = a conversion factor evaluated as: (0.74 cm^3^/g) (10^24^ A^3^/cm^3^) -------------------------------------- (6.02*10^23^) molecules/mole where 0.74 is an assumed value for the partial specific volume of the molecule |
| description | text | A description of the quality and habit of the crystal. The crystal dimensions should not normally be reported here; use instead the specific items in the EXPTL_CRYSTAL category relating to size for the gross dimensions of the crystal and data items in the EXPTL_CRYSTAL_FACE category to describe the relationship between individual faces. |
| id | text | The value of _exptl_crystal.id must uniquely identify a record in the EXPTL_CRYSTAL list. Note that this item need not be a number; it can be any unique identifier. |
| preparation | text | Details of crystal growth and preparation of the crystal (e.g. mounting) prior to the intensity measurements. |
| density_meas | double precision | Density values measured using standard chemical and physical methods. The units are megagrams per cubic metre (grams per cubic centimetre). |
| pdbx_mosaicity | double precision | Isotropic approximation of the distribution of mis-orientation angles specified in degrees of all the mosaic domain blocks in the crystal, represented as a standard deviation. Here, a mosaic block is a set of contiguous unit cells assumed to be perfectly aligned. Lower mosaicity indicates better ordered crystals. See for example: Nave, C. (1998). Acta Cryst. D54, 848-853. Note that many software packages estimate the mosaic rotation distribution differently and may combine several physical properties of the experiment into a single mosaic term. This term will help fit the modeled spots to the observed spots without necessarily being directly related to the physics of the crystal itself. |
| pdbx_mosaicity_esd | double precision | The uncertainty in the mosaicity estimate for the crystal. |

## exptl_crystal_grow

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_id | text | This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category. |
| details | text | A description of special aspects of the crystal growth. |
| method | text | The method used to grow the crystals. |
| pH | double precision | The pH at which the crystal was grown. If more than one pH was employed during the crystallization process, the final pH should be noted here and the protocol involving multiple pH values should be described in _exptl_crystal_grow.details. |
| pressure | double precision | The ambient pressure in kilopascals at which the crystal was grown. |
| seeding | text | A description of the protocol used for seeding the crystal growth. |
| temp_details | text | A description of special aspects of temperature control during crystal growth. |
| time | text | The approximate time that the crystal took to grow to the size used for data collection. |
| pdbx_details | text | Text description of crystal growth procedure. |
| pdbx_pH_range | text | The range of pH values at which the crystal was grown. Used when a point estimate of pH is not appropriate. |
| temp | double precision | The temperature in kelvins at which the crystal was grown. If more than one temperature was employed during the crystallization process, the final temperature should be noted here and the protocol involving multiple temperatures should be described in _exptl_crystal_grow.details. |

## exptl_crystal_grow_comp

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| conc | text | The concentration of the solution component. |
| details | text | A description of any special aspects of the solution component. When the solution component is the one that contains the macromolecule, this could be the specification of the buffer in which the macromolecule was stored. When the solution component is a buffer component, this could be the methods (or formula) used to achieve a desired pH. |
| crystal_id | text | This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category. |
| id | text | The value of _exptl_crystal_grow_comp.id must uniquely identify each item in the EXPTL_CRYSTAL_GROW_COMP list. Note that this item need not be a number; it can be any unique identifier. |
| name | text | A common name for the component of the solution. |
| sol_id | text | An identifier for the solution to which the given solution component belongs. |
| volume | text | The volume of the solution component. |

## exptl_crystal_grow_comp_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_id | text |  |
| id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| chemical_formula | text |  |
| common_name | text |  |
| conc | text |  |
| conc_unit | text |  |
| details | text |  |
| sol_id | text |  |

## exptl_crystal_grow_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| method | text |  |
| pH | double precision |  |
| pH_range_high | double precision |  |
| pH_range_low | double precision |  |
| pdbx_details | text |  |
| temp | text |  |
| temp_unit | text |  |

## gene_ontology_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text |  |
| auth_asym_id | text |  |
| update_id | double precision |  |
| auth_validate | text |  |
| goid | text |  |
| namespace | text |  |
| name | text |  |
| source | text |  |

## link_asym_pdbjplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| asym_id | text |  |
| pdb_strand_id | text |  |
| entity_id | text |  |

## link_entity_pdbjplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text |  |
| db_name | text |  |
| db_accession | text[] |  |

## link_entry_pdbjplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| db_name | text |  |
| db_accession | text[] |  |

## ndb_struct_conf_na

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| feature | text | This data item identifies a secondary structure feature of this entry. |

## ndb_struct_na_base_pair

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| model_number | integer | Describes the model number of the base pair. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| pair_number | integer | Sequential number of pair in the pair sequence. |
| pair_name | text | Text label for this base pair. |
| i_label_asym_id | text | Describes the asym id of the i-th base in the base pair. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| i_label_comp_id | text | Describes the component id of the i-th base in the base pair. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| i_label_seq_id | integer | Describes the sequence number of the i-th base in the base pair. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| i_symmetry | text | Describes the symmetry operation that should be applied to the coordinates of the i-th base to generate the first partner in the base pair. |
| j_label_asym_id | text | Describes the asym id of the j-th base in the base pair. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| j_label_comp_id | text | Describes the component id of the j-th base in the base pair. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| j_label_seq_id | integer | Describes the sequence number of the j-th base in the base pair. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| j_symmetry | text | Describes the symmetry operation that should be applied to the coordinates of the j-th base to generate the second partner in the base pair. |
| i_auth_asym_id | text | Describes the asym id of the i-th base in the base pair. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| i_auth_seq_id | text | Describes the sequence number of the i-th base in the base pair. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| i_PDB_ins_code | text | Describes the PDB insertion code of the i-th base in the base pair. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| j_auth_asym_id | text | Describes the asym id of the j-th base in the base pair. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| j_auth_seq_id | text | Describes the sequence number of the j-th base in the base pair. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| j_PDB_ins_code | text | Describes the PDB insertion code of the j-th base in the base pair. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| shear | double precision | The value of the base pair shear parameter. |
| stretch | double precision | The value of the base pair stretch parameter. |
| stagger | double precision | The value of the base pair stagger parameter. |
| buckle | double precision | The value of the base pair buckle parameter. |
| propeller | double precision | The value of the base pair propeller parameter. |
| opening | double precision | The value of the base pair opening parameter. |
| hbond_type_12 | integer | Base pair classification of Westhoff and Leontis. |
| hbond_type_28 | integer | Base pair classification of Saenger |

## ndb_struct_na_base_pair_step

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| model_number | integer | Describes the model number of the base pair step. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| step_number | integer | The sequence number of this step in the step sequence. |
| step_name | text | The text name of this step. |
| i_label_asym_id_1 | text | Describes the asym id of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| i_label_comp_id_1 | text | Describes the component id of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| i_label_seq_id_1 | integer | Describes the sequence number of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| i_symmetry_1 | text | Describes the symmetry operation that should be applied to the coordinates of the i-th base to generate the first partner in the first base pair of the step. |
| j_label_asym_id_1 | text | Describes the asym id of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| j_label_comp_id_1 | text | Describes the component id of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| j_label_seq_id_1 | integer | Describes the sequence number of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| j_symmetry_1 | text | Describes the symmetry operation that should be applied to the coordinates of the j-th base to generate the second partner in the first base pair of the step. |
| i_label_asym_id_2 | text | Describes the asym id of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| i_label_comp_id_2 | text | Describes the component id of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| i_label_seq_id_2 | integer | Describes the sequence number of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| i_symmetry_2 | text | Describes the symmetry operation that should be applied to the coordinates of the i-th base to generate the first partner in the second base pair of the step. |
| j_label_asym_id_2 | text | Describes the asym id of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| j_label_comp_id_2 | text | Describes the component id of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| j_label_seq_id_2 | integer | Describes the sequence number of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| j_symmetry_2 | text | Describes the symmetry operation that should be applied to the coordinates of the j-th base to generate the second partner in the second base pair of the step. |
| i_auth_asym_id_1 | text | Describes the author's asym id of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| i_auth_seq_id_1 | text | Describes the author's sequence number of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| i_PDB_ins_code_1 | text | Describes the PDB insertion code of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| j_auth_asym_id_1 | text | Describes the author's asym id of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| j_auth_seq_id_1 | text | Describes the author's sequence number of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| j_PDB_ins_code_1 | text | Describes the PDB insertion code of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| i_auth_asym_id_2 | text | Describes the author's asym id of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| i_auth_seq_id_2 | text | Describes the author's sequence number of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| i_PDB_ins_code_2 | text | Describes the PDB insertion code of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| j_auth_asym_id_2 | text | Describes the author's asym id of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| j_auth_seq_id_2 | text | Describes the author's sequence number of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| j_PDB_ins_code_2 | text | Describes the PDB insertion code of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| shift | double precision | The value of the base pair step shift parameter. |
| slide | double precision | The value of the base pair step slide parameter. |
| rise | double precision | The value of the base pair step rise parameter. |
| tilt | double precision | The value of the base pair step tilt parameter. |
| roll | double precision | The value of the base pair step roll parameter. |
| twist | double precision | The value of the base pair step twist parameter. |
| x_displacement | double precision | The value of the base pair step X displacement parameter. |
| y_displacement | double precision | The value of the base pair step Y displacement parameter. |
| helical_rise | double precision | The value of the base pair step helical rise parameter. |
| inclination | double precision | The value of the base pair step inclination parameter. |
| tip | double precision | The value of the base pair step twist parameter. |
| helical_twist | double precision | The value of the base pair step helical twist parameter. |

## pdbx_SG_project

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | A unique integer identifier for this center |
| project_name | text | The value identifies the Structural Genomics project. |
| full_name_of_center | text | The value identifies the full name of center. |
| initial_of_center | text | The value identifies the full name of center. |

## pdbx_audit_conform

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| dict_location | text | A file name or uniform resource locator (URL) for the dictionary to which the current data block conforms. |
| dict_name | text | The dictionary name defining data names used in this file. |
| dict_version | text | The version number of the dictionary to which the current data block conforms. |

## pdbx_audit_revision_category

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | A unique identifier for the pdbx_audit_revision_category record. |
| revision_ordinal | integer | A pointer to _pdbx_audit_revision_history.ordinal |
| data_content_type | text | The type of file that the pdbx_audit_revision_history record refers to. |
| category | text | The category updated in the pdbx_audit_revision_category record. |

## pdbx_audit_revision_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | A unique identifier for the pdbx_audit_revision_details record. |
| revision_ordinal | integer | A pointer to _pdbx_audit_revision_history.ordinal |
| data_content_type | text | The type of file that the pdbx_audit_revision_history record refers to. |
| provider | text | The provider of the revision. |
| type | text | A type classification of the revision |
| description | text | Additional details describing the revision. |
| details | text | Further details describing the revision. |

## pdbx_audit_revision_group

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | A unique identifier for the pdbx_audit_revision_group record. |
| revision_ordinal | integer | A pointer to _pdbx_audit_revision_history.ordinal |
| data_content_type | text | The type of file that the pdbx_audit_revision_history record refers to. |
| group | text | The collection of categories updated with this revision. |

## pdbx_audit_revision_history

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | A unique identifier for the pdbx_audit_revision_history record. |
| data_content_type | text | The type of file that the pdbx_audit_revision_history record refers to. |
| major_revision | integer | The major version number of deposition release. |
| minor_revision | integer | The minor version number of deposition release. |
| revision_date | date | The release date of the revision |
| part_number | integer | The part number of the content_type file correspondng to this milestone file |

## pdbx_audit_revision_item

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | A unique identifier for the pdbx_audit_revision_item record. |
| revision_ordinal | integer | A pointer to _pdbx_audit_revision_history.ordinal |
| data_content_type | text | The type of file that the pdbx_audit_revision_history record refers to. |
| item | text | A high level explanation the author has provided for submitting a revision. |

## pdbx_audit_support

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| funding_organization | text | The name of the organization providing funding support for the entry. |
| country | text | The country/region providing the funding support for the entry. |
| grant_number | text | The grant number associated with this source of support. |
| ordinal | integer | A unique sequential integer identifier for each source of support for this entry. |

## pdbx_branch_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| hetero | text | A flag to indicate whether this monomer in the entity is heterogeneous in sequence. |
| asym_id | text | Pointer to _atom_site.label_asym_id. |
| mon_id | text | This data item is a pointer to _atom_site.label_comp_id in the PDBX_ENTITY_BRANCH_LIST category. |
| num | integer | This data item is a pointer to _pdbx_entity_branch_list.num in the PDBX_ENTITY_BRANCH_LIST category. |
| pdb_asym_id | text | This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| pdb_seq_num | text | This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| pdb_mon_id | text | This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_asym_id | text | This data item is a pointer to _atom_site.pdbx_auth_asym_id in the ATOM_SITE category. |
| auth_seq_num | text | This data item is a pointer to _atom_site.pdbx_auth_seq_id in the ATOM_SITE category. |
| auth_mon_id | text | This data item is a pointer to _atom_site.pdbx_auth_comp_id in the ATOM_SITE category. |

## pdbx_buffer

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _pdbx_buffer.id must uniquely identify the sample buffer. |
| name | text | The name of each buffer. |
| details | text | Any additional details to do with buffer. |

## pdbx_buffer_components

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _pdbx_buffer_components.id must uniquely identify a component of the buffer. |
| buffer_id | text | This data item is a pointer to _pdbx_buffer.id in the BUFFER category. |
| name | text | The name of each buffer component. |
| conc | text | The millimolar concentration of buffer component. |
| details | text | Any additional details to do with buffer composition. |
| conc_units | text | The concentration units of the component. |

## pdbx_chem_comp_identifier

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| comp_id | text | This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| identifier | text | This data item contains the identifier value for this component. |
| type | text | This data item contains the identifier type. |
| program | text | This data item contains the name of the program or library used to compute the identifier. |
| program_version | text | This data item contains the version of the program or library used to compute the identifier. |

## pdbx_contact_author

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | A unique integer identifier for this author |
| email | text | The electronic mail address of the author of the data block to whom correspondence should be addressed, in a form recognisable to international networks. |
| name_first | text | The first name of the author of the data block to whom correspondence should be addressed. |
| name_last | text | The last name of the author of the data block to whom correspondence should be addressed. |
| name_mi | text | The middle initial(s) of the author of the data block to whom correspondence should be addressed. |
| role | text | The role of this author in the project depositing this data. |
| identifier_ORCID | text | The Open Researcher and Contributor ID (ORCID). |

## pdbx_coordinate_model

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| asym_id | text | A reference to _struct_asym.id. |
| type | text | A classification of the composition of the coordinate model. |

## pdbx_database_PDB_obs_spr

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | Identifier for the type of obsolete entry to be added to this entry. |
| date | timestamp with time zone | The date of replacement. |
| pdb_id | text | The new PDB identifier for the replaced entry. |
| replace_pdb_id | text | The PDB identifier for the replaced (OLD) entry/entries. |
| details | text | Details related to the replaced or replacing entry. |

## pdbx_database_related

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| db_name | text | The name of the database containing the related entry. |
| details | text | A description of the related entry. |
| db_id | text | The identifying code in the related database. |
| content_type | text | The identifying content type of the related entry. |

## pdbx_database_remark

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | A unique identifier for the PDB remark record. |
| text | text | The full text of the PDB remark record. |

## pdbx_database_status

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| status_code | text | Code for status of file. |
| status_code_sf | text | Code for status of structure factor file. |
| status_code_mr | text | Code for status of NMR constraints file. |
| entry_id | text | The value of _pdbx_database_status.entry_id identifies the data block. |
| recvd_initial_deposition_date | date | The date of initial deposition. (The first message for deposition has been received.) |
| SG_entry | text | This code indicates whether the entry belongs to Structural Genomics Project. |
| deposit_site | text | The site where the file was deposited. |
| process_site | text | The site where the file was deposited. |
| status_code_cs | text | Code for status of chemical shift data file. |
| status_code_nmr_data | text | Code for status of unified NMR data file. |
| methods_development_category | text | The methods development category in which this entry has been placed. |
| pdb_format_compatible | text | A flag indicating that the entry is compatible with the PDB format. A value of 'N' indicates that the no PDB format data file is corresponding to this entry is available in the PDB archive. |

## pdbx_deposit_group

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| group_id | text | A unique identifier for a group of entries deposited as a collection. |
| group_title | text | A title to describe the group of entries deposited in the collection. |
| group_description | text | A description of the contents of entries in the collection. |
| group_type | text | Text to describe a grouping of entries in multiple collections |

## pdbx_diffrn_reflns_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | This data item is a pointer to _diffrn.id in the DIFFRN category. This item distingush the different data sets |
| d_res_low | double precision | The lowest resolution for the interplanar spacings in the resolution shell. |
| d_res_high | double precision | The highest resolution for the interplanar spacings in the resolution shell. |
| percent_possible_obs | double precision | The percentage of geometrically possible reflections represented by reflections that satisfy the resolution limits established by _diffrn_reflns_shell.d_resolution_high and _diffrn_reflns_shell.d_resolution_low and the observation limit established by _diffrn_reflns.observed_criterion. |
| Rmerge_I_obs | double precision | The R factor for the reflections that satisfy the merging criteria for the resolution shell. |
| Rsym_value | double precision | The R factor for averaging the symmetry related reflections for the resolution shell. |
| chi_squared | double precision | The overall Chi-squared statistic for the resolution shell. |
| redundancy | double precision | The overall redundancy for the resolution shell. |
| rejects | integer | The number of rejected reflections in the resolution shell |
| number_obs | integer | The number of observed reflections in the resolution shell. |

## pdbx_distant_solvent_atoms

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_distant_solvent_atoms.id must uniquely identify each item in the PDBX_DISTANT_SOLVENT_ATOMS list. This is an integer serial number. |
| PDB_model_num | integer | Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id | text | Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| label_alt_id | text | Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category. |
| neighbor_macromolecule_distance | double precision | Distance to closest neighboring macromolecule atom. |
| neighbor_ligand_distance | double precision | Distance to closest neighboring ligand or solvent atom. |

## pdbx_entity_branch

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | The entity id for this branched entity. This data item is a pointer to _entity.id |
| type | text | The type of this branched oligosaccharide. |

## pdbx_entity_branch_descriptor

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity_poly.entity_id in the ENTITY category. |
| descriptor | text | This data item contains the descriptor value for this entity. |
| type | text | This data item contains the descriptor type. |
| program | text | This data item contains the name of the program or library used to compute the descriptor. |
| program_version | text | This data item contains the version of the program or library used to compute the descriptor. |
| ordinal | integer | Ordinal index for this category. |

## pdbx_entity_branch_link

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| link_id | integer | The value of _pdbx_entity_branch_link.link_id uniquely identifies linkages within the branched entity. |
| entity_id | text | The entity id for this branched entity. This data item is a pointer to _pdbx_entity_branch_list.entity_id in the PDBX_ENTITY_BRANCH_LIST category. |
| entity_branch_list_num_1 | integer | The component number for the first component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.num in the PDBX_ENTITY_BRANCH_LIST category. |
| entity_branch_list_num_2 | integer | The component number for the second component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.num in the PDBX_ENTITY_BRANCH_LIST category. |
| comp_id_1 | text | The component identifier for the first component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.comp_id in the PDBX_ENTITY_BRANCH_LIST category. |
| comp_id_2 | text | The component identifier for the second component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.comp_id in the PDBX_ENTITY_BRANCH_LIST category. |
| atom_id_1 | text | The atom identifier/name for the first atom making the linkage. |
| leaving_atom_id_1 | text | The leaving atom identifier/name bonded to the first atom making the linkage. |
| atom_id_2 | text | The atom identifier/name for the second atom making the linkage. |
| leaving_atom_id_2 | text | The leaving atom identifier/name bonded to the second atom making the linkage. |
| value_order | text | The bond order target for the chemical linkage. |

## pdbx_entity_branch_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| hetero | text | A flag to indicate whether this monomer in the entity is heterogeneous in sequence. |
| comp_id | text | This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| num | integer | The value pair _pdbx_entity_branch_list.num and _pdbx_entity_branch_list.comp_id must uniquely identify a record in the PDBX_ENTITY_BRANCH_LIST list. |

## pdbx_entity_instance_feature

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| feature_type | text | A feature type associated with entity instance. |
| auth_asym_id | text | Author instance identifier (formerly PDB Chain ID) |
| asym_id | text | Instance identifier for this entity. |
| auth_seq_num | text | Author provided residue number. |
| comp_id | text | Chemical component identifier |
| auth_comp_id | text | The author provided chemical component identifier |
| ordinal | integer | An ordinal index for this category |

## pdbx_entity_nonpoly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| comp_id | text | This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| name | text | A name for the non-polymer entity |

## pdbx_entity_src_syn

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the source for the synthetic entity. |
| organism_scientific | text | The scientific name of the organism from which the sequence of the synthetic entity was derived. |
| organism_common_name | text | The common name of the organism from which the sequence of the synthetic entity was derived. |
| ncbi_taxonomy_id | text | NCBI Taxonomy identifier of the organism from which the sequence of the synthetic entity was derived. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| pdbx_src_id | integer | This data item is an ordinal identifier for pdbx_entity_src_syn data records. |
| pdbx_alt_source_flag | text | This data item identifies cases in which an alternative source modeled. |
| pdbx_beg_seq_num | integer | The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category. |
| pdbx_end_seq_num | integer | The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category. |

## pdbx_entry_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This item identifies the entry. This is a reference to _entry.id. |
| nonpolymer_details | text | Additional details about the non-polymer components in this entry. |
| sequence_details | text | Additional details about the sequence or sequence database correspondences for this entry. |
| compound_details | text | Additional details about the macromolecular compounds in this entry. |
| source_details | text | Additional details about the source and taxonomy of the macromolecular components in this entry. |
| has_ligand_of_interest | text | A flag to indicate if author has indicated that there are any or no ligands that are the focus of research. |
| has_protein_modification | text | A flag to indicate if the model contains any protein modifications. |

## pdbx_exptl_crystal_cryo_treatment

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_id | text | This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category. |
| final_solution_details | text | Details of the final solution used in the treatment of this crystal |
| soaking_details | text | Details of the soaking treatment applied to this crystal. |
| cooling_details | text | Details of the cooling treatment applied to this crystal. |

## pdbx_exptl_crystal_grow_comp

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_id | text | This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category. |
| comp_id | text | The value of _exptl_crystal_grow_comp.comp_id must uniquely identify each item in the PDBX_EXPTL_CRYSTAL_GROW_COMP list. Note that this item need not be a number; it can be any unique identifier. |
| comp_name | text | A common name for the component of the solution. |
| sol_id | text | An identifier for the solution to which the given solution component belongs. |
| conc | double precision | The concentration value of the solution component. |
| conc_units | text | The concentration units for the solution component. |

## pdbx_exptl_crystal_grow_sol

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_id | text | This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category. |
| sol_id | text | An identifier for this solution (e.g. precipitant, reservoir, macromolecule) |
| volume | double precision | The volume of the solution. |
| volume_units | text | The volume units of the solution. |
| pH | double precision | The pH of the solution. |

## pdbx_helical_symmetry

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| number_of_operations | integer | Number of operations. |
| rotation_per_n_subunits | double precision | Angular rotation (degrees) in N subunits |
| rise_per_n_subunits | double precision | Angular rotation (degrees) in N subunits |
| n_subunits_divisor | integer | Number of subunits used in the calculation of rise and rotation. |
| dyad_axis | text | Two-fold symmetry perpendicular to the helical axis. |
| circular_symmetry | integer | Rotational n-fold symmetry about the helical axis. |

## pdbx_initial_refinement_model

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | A unique identifier for the starting model record. |
| entity_id_list | text | A comma separated list of entities reflecting the initial model used for refinement |
| type | text | This item describes the type of the initial model was generated |
| source_name | text | This item identifies the resource of initial model used for refinement |
| accession_code | text | This item identifies an accession code of the resource where the initial model is used |
| details | text | A description of special aspects of the initial model |

## pdbx_modification_feature

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | An ordinal index for this category. |
| label_comp_id | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_asym_id | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_seq_id | integer | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| label_alt_id | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| modified_residue_label_comp_id | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| modified_residue_label_asym_id | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| modified_residue_label_seq_id | integer | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| modified_residue_label_alt_id | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| auth_comp_id | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_asym_id | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_seq_id | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| symmetry | text | Describes the symmetry operation that should be applied to the protein modification group. |
| modified_residue_auth_comp_id | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| modified_residue_auth_asym_id | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| modified_residue_auth_seq_id | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| modified_residue_PDB_ins_code | text | A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| modified_residue_symmetry | text | Describes the symmetry operation that should be applied to the chemical component that is being modified. |
| comp_id_linking_atom | text | The atom on the modification group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs. |
| modified_residue_id_linking_atom | text | The atom on the polypeptide residue group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs. |
| modified_residue_id | text | Chemical component identifier for the amino acid residue that is being modified. |
| ref_pcm_id | integer | A component of the identifier for the unique kind of protein modification. This data item is a pointer to _pdbx_chem_comp_pcm.pcm_id in the CHEM_COMP_PCM category. |
| ref_comp_id | text | A component of the identifier for the unique kind of protein modification. This data item is a pointer to _pdbx_chem_comp_pcm.comp_id in the CHEM_COMP_PCM category. |
| type | text | The type of protein modification. |
| category | text | The category of protein modification. |

## pdbx_molecule

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| prd_id | text | The value of _pdbx_molecule.prd_id is the PDB accession code for this reference molecule. |
| instance_id | integer | The value of _pdbx_molecule.instance_id is identifies a particular molecule in the molecule list. |
| asym_id | text | A reference to _struct_asym.id in the STRUCT_ASYM category. |

## pdbx_molecule_features

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| prd_id | text | The value of _pdbx_molecule_features.prd_id is the accession code for this reference molecule. |
| class | text | Broadly defines the function of the molecule. |
| type | text | Defines the structural classification of the molecule. |
| name | text | A name of the molecule. |
| details | text | Additional details describing the molecule. |

## pdbx_nmr_constraints

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | You can leave this blank as an ID will be assigned by the MSD to the constraint file. |
| NOE_constraints_total | integer | The total number of all NOE constraints used in the final structure calculation. |
| NOE_intraresidue_total_count | integer | The total number of all intraresidue, [i-j]=0, NOE constraints used in the final structure calculation. |
| NOE_interentity_total_count | integer | The total number of interentity, NOE constraints used in the final structure calculation. This field should only be if system is complex -i.e more than one entity e.g. a dimer or ligand-protein complex |
| NOE_sequential_total_count | integer | The total number of sequential, [i-j]=1, NOE constraints used in the final structure calculation. |
| NOE_medium_range_total_count | integer | The total number of medium range 1<[i-j]<=5 NOE constraints used in the final structure calculation. |
| NOE_long_range_total_count | integer | The total number of long range [i-j]>5 NOE constraints used in the final structure calculation. |
| protein_phi_angle_constraints_total_count | integer | The total number of phi angle constraints used in the final structure calculation |
| protein_psi_angle_constraints_total_count | integer | The total number of psi angle constraints used in the final structure calculation. |
| protein_chi_angle_constraints_total_count | integer | The total number of chi angle constraints used in the final structure calculation. |
| protein_other_angle_constraints_total_count | integer | The total number of other angle constraints used in the final structure calculation. |
| hydrogen_bond_constraints_total_count | integer | The total number of hydrogen bond constraints used in the final structure calculation. |
| disulfide_bond_constraints_total_count | integer | The total number of disulfide bond constraints used in the final structure calculation. |
| NA_alpha-angle_constraints_total_count | integer |  |
| NA_beta-angle_constraints_total_count | integer |  |
| NA_gamma-angle_constraints_total_count | integer |  |
| NA_delta-angle_constraints_total_count | integer |  |
| NA_epsilon-angle_constraints_total_count | integer |  |
| NA_chi-angle_constraints_total_count | integer |  |
| NA_other-angle_constraints_total_count | integer |  |
| NA_sugar_pucker_constraints_total_count | integer | The total number of nucleic acid sugar pucker constraints used in the final structure calculation. |

## pdbx_nmr_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | The entry ID for the structure determination. |
| text | text | Additional details describing the NMR experiment. |

## pdbx_nmr_ensemble

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | Leave this blank as the ID is provided by the MSD |
| conformers_calculated_total_number | integer | The total number of conformer (models) that were calculated in the final round. |
| conformers_submitted_total_number | integer | The number of conformer (models) that are submitted for the ensemble. |
| conformer_selection_criteria | text | By highlighting the appropriate choice(s), describe how the submitted conformer (models) were selected. |
| representative_conformer | integer | The number of the conformer identified as most representative. |
| average_constraints_per_residue | integer | The average number of constraints per residue for the ensemble |
| average_constraint_violations_per_residue | integer | The average number of constraint violations on a per residue basis for the ensemble. |
| maximum_distance_constraint_violation | double precision | The maximum distance constraint violation for the ensemble. |
| average_distance_constraint_violation | double precision | The average distance restraint violation for the ensemble. |
| maximum_upper_distance_constraint_violation | double precision | The maximum upper distance constraint violation for the ensemble. |
| maximum_lower_distance_constraint_violation | double precision | The maximum lower distance constraint violation for the ensemble. |
| distance_constraint_violation_method | text | Describe the method used to calculate the distance constraint violation statistics, i.e. are they calculated over all the distance constraints or calculated for violations only? |
| maximum_torsion_angle_constraint_violation | double precision | The maximum torsion angle constraint violation for the ensemble. |
| average_torsion_angle_constraint_violation | double precision | The average torsion angle constraint violation for the ensemble. |
| torsion_angle_constraint_violation_method | text | This item describes the method used to calculate the torsion angle constraint violation statistics. i.e. are the entered values based on all torsion angle or calculated for violations only? |

## pdbx_nmr_ensemble_rms

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | '?' |
| residue_range_begin | integer | Structure statistics are often calculated only over the well-ordered region(s) of the biopolymer. Portions of the macromolecule are often mobile and disordered, hence they are excluded in calculating the statistics. To define the range(s) over which the statistics are calculated, enter the beginning residue number(s): e.g. if the regions used were 5-32 and 41-69, enter 5,41 |
| chain_range_begin | text | The beginning chain id. |
| residue_range_end | integer | The ending residue number: e.g. 32,69. |
| chain_range_end | text | The ending chain id: |
| atom_type | text | Statistics are often calculated over only some of the atoms, e.g. backbone, or heavy atoms. Describe which type of atoms are used for the statistical analysis. |
| distance_rms_dev | double precision | The distance rmsd to the mean structure for the ensemble of structures. |
| distance_rms_dev_error | double precision | The error in the distance rmsd. |
| covalent_bond_rms_dev | double precision | The covalent bond rmsd to the target value for the ensemble. |
| bond_angle_rms_dev | double precision | The bond angle rmsd to the target values for the ensemble. |
| improper_torsion_angle_rms_dev | double precision | The improper torsion angle rmsd to the target values for the ensemble. |
| dihedral_angles_rms_dev | double precision | The dihedral angle rmsd to the target values for the ensemble. |
| dihedral_angles_rms_dev_error | double precision | The error of the rmsd dihedral angles. |
| coord_average_rmsd_method | text | Describe the method for calculating the coordinate average rmsd. |

## pdbx_nmr_exptl

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| experiment_id | text | A numerical ID for each experiment. |
| conditions_id | text | The number to identify the set of sample conditions. |
| solution_id | text | The solution_id from the Experimental Sample to identify the sample that these conditions refer to. [Remember to save the entries here before returning to the Experimental Sample form] |
| type | text | The type of NMR experiment. |
| spectrometer_id | integer | Pointer to '_pdbx_nmr_spectrometer.spectrometer_id' |
| sample_state | text | Physical state of the sample either anisotropic or isotropic. |

## pdbx_nmr_exptl_sample

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| solution_id | text | The name (number) of the sample. |
| component | text | The name of each component in the sample |
| concentration | double precision | The concentration value of the component. |
| concentration_range | text | The concentration range for the component. |
| concentration_units | text | The concentration units of the component. |
| isotopic_labeling | text | The isotopic composition of each component, including the % labeling level, if known. For example: 1. Uniform (random) labeling with 15N: U-15N 2. Uniform (random) labeling with 13C, 15N at known labeling levels: U-95% 13C;U-98% 15N 3. Residue selective labeling: U-95% 15N-Thymine 4. Site specific labeling: 95% 13C-Ala18, 5. Natural abundance labeling in an otherwise uniformly labled biomolecule is designated by NA: U-13C; NA-K,H |

## pdbx_nmr_exptl_sample_conditions

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| conditions_id | text | The condition number as defined above. |
| temperature | text | The temperature (in kelvin) at which NMR data were collected. |
| pressure_units | text | The units of pressure at which NMR data were collected. |
| pressure | text | The pressure at which NMR data were collected. |
| pH | text | The pH at which the NMR data were collected. |
| ionic_strength | text | The ionic strength at which the NMR data were collected -in lieu of this enter the concentration and identity of the salt in the sample. |
| details | text | General details describing conditions of both the sample and the environment during measurements. |
| ionic_strength_err | double precision | Estimate of the standard error for the value for the sample ionic strength. |
| ionic_strength_units | text | Units for the value of the sample condition ionic strength.. |
| label | text | A descriptive label that uniquely identifies this set of sample conditions. |
| pH_err | double precision | Estimate of the standard error for the value for the sample pH. |
| pH_units | text | Units for the value of the sample condition pH. |
| pressure_err | double precision | Estimate of the standard error for the value for the sample pressure. |
| temperature_err | double precision | Estimate of the standard error for the value for the sample temperature. |
| temperature_units | text | Units for the value of the sample condition temperature. |

## pdbx_nmr_refine

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | You can leave this blank as an ID will be assigned by the RCSB to the constraint file. |
| method | text | The method used to determine the structure. |
| details | text | Additional details about the NMR refinement. |
| software_ordinal | integer | Pointer to _software.ordinal |

## pdbx_nmr_representative

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | msd will assign the ID. |
| conformer_id | text | If a member of the ensemble has been selected as a representative structure, identify it by its model number. |
| selection_criteria | text | By highlighting the appropriate choice(s), describe the criteria used to select this structure as a representative structure, or if an average structure has been calculated describe how this was done. |

## pdbx_nmr_sample_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| solution_id | text | The name (number) of the sample. |
| contents | text | A complete description of each NMR sample. Include the concentration and concentration units for each component (include buffers, etc.). For each component describe the isotopic composition, including the % labeling level, if known. For example: 1. Uniform (random) labeling with 15N: U-15N 2. Uniform (random) labeling with 13C, 15N at known labeling levels: U-95% 13C;U-98% 15N 3. Residue selective labeling: U-95% 15N-Thymine 4. Site specific labeling: 95% 13C-Ala18, 5. Natural abundance labeling in an otherwise uniformly labeled biomolecule is designated by NA: U-13C; NA-K,H |
| solvent_system | text | The solvent system used for this sample. |
| label | text | A value that uniquely identifies this sample from the other samples listed in the entry. |
| type | text | A descriptive term for the sample that defines the general physical properties of the sample. |
| details | text | Brief description of the sample providing additional information not captured by other items in the category. |

## pdbx_nmr_software

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | An ordinal index for this category |
| classification | text | The purpose of the software. |
| name | text | The name of the software used for the task. |
| version | text | The version of the software. |
| authors | text | The name of the authors of the software used in this procedure. |

## pdbx_nmr_spectrometer

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| spectrometer_id | text | Assign a numerical ID to each instrument. |
| model | text | The model of the NMR spectrometer. |
| type | text | Select the instrument manufacturer(s) and the model(s) of the NMR(s) used for this work. |
| manufacturer | text | The name of the manufacturer of the spectrometer. |
| field_strength | double precision | The field strength in MHz of the spectrometer |
| details | text | A text description of the NMR spectrometer. |

## pdbx_nonpoly_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| asym_id | text | Pointer to _atom_site.label_asym_id. |
| entity_id | text | Pointer to _atom_site.label_entity_id. |
| mon_id | text | Pointer to _atom_site.label_comp_id. |
| pdb_strand_id | text | PDB strand/chain id. |
| ndb_seq_num | text | NDB/RCSB residue number. |
| pdb_seq_num | text | PDB residue number. |
| auth_seq_num | text | Author provided residue numbering. This value may differ from the PDB residue number and may not correspond to residue numbering within the coordinate records. |
| pdb_mon_id | text | PDB residue identifier. |
| auth_mon_id | text | Author provided residue identifier. This value may differ from the PDB residue identifier and may not correspond to residue identification within the coordinate records. |
| pdb_ins_code | text | PDB insertion code. |

## pdbx_phasing_MAD_set

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | _pdbx_phasing_MAD_set.id records phase set name for MAD phasing. |
| d_res_low | double precision | _pdbx_phasing_MAD_set.d_res_low records the lowerest resolution for phasing set. |
| d_res_high | double precision | _pdbx_phasing_MAD_set.d_res_high records the highest resolution for the phasing set. |
| reflns_acentric | integer | _pdbx_phasing_MAD_set.reflns_acentric records the number of acentric reflections for MAD phasing. |
| reflns_centric | integer | _pdbx_phasing_MAD_set.reflns_centric records the number of centric reflections for MAD phasing. |
| reflns | integer | _pdbx_phasing_MAD_set.reflns records the number of reflections used for MAD phasing. |
| fom_acentric | double precision | _pdbx_phasing_MAD_set.fom_acentric records the figure of merit using acentric data for MAD phasing. |
| fom_centric | double precision | _pdbx_phasing_MAD_set.fom_centric records the figure of merit using centric data for MAD phasing. |
| fom | double precision | _pdbx_phasing_MAD_set.fom records the figure of merit for MAD phasing. |
| R_cullis_centric | double precision | _pdbx_phasing_MAD_set.R_cullis_centric records R_cullis using centric data for MAD phasing. |
| R_cullis_acentric | double precision | _pdbx_phasing_MAD_set.R_cullis_acentric records R_cullis using acentric data for MAD phasing. |
| R_cullis | double precision | _pdbx_phasing_MAD_set.R_cullis records R_cullis for MAD phasing. |
| R_kraut_centric | double precision | _pdbx_phasing_MAD_set.R_kraut_centric records r_kraut using centric data for MAD phasing. |
| R_kraut_acentric | double precision | _pdbx_phasing_MAD_set.r_kraut_acentric records r_kraut using acentric data for MAD phasing. |
| R_kraut | double precision | _pdbx_phasing_MAD_set.R_kraut records R_kraut for MAD phasing. |
| loc_centric | double precision | _pdbx_phasing_MAD_set.loc_centric records lack of closure using centric data for MAD phasing. |
| loc_acentric | double precision | _pdbx_phasing_MAD_set.loc_acentric records lack of closure using acentric data for MAD phasing. |
| loc | double precision | _pdbx_phasing_MAD_set.loc records lack of closure for MAD phasing. |
| power_centric | double precision | _pdbx_phasing_MAD_set.power_centric records phasing powe using centric data for MAD phasing. |
| power_acentric | double precision | _pdbx_phasing_MAD_set.power_acentric records phasing powe using acentric data for MAD phasing. |
| power | double precision | _pdbx_phasing_MAD_set.power records phasing power for MAD phasing. |

## pdbx_phasing_MAD_set_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | _pdbx_phasing_MAD_set_shell.id records phase set name for MAD phasing. |
| d_res_low | double precision | _pdbx_phasing_MAD_set_shell.d_res_low records the lowerest resolution for phasing set. |
| d_res_high | double precision | _pdbx_phasing_MAD_set_shell.d_res_high records the highest resolution for the phasing set. |
| reflns_acentric | integer | _pdbx_phasing_MAD_set_shell.reflns_acentric records the number of acentric reflections for MAD phasing. |
| reflns_centric | integer | _pdbx_phasing_MAD_set_shell.reflns_centric records the number of centric reflections for MAD phasing. |
| reflns | integer | _pdbx_phasing_MAD_set_shell.reflns records the number of reflections used for MAD phasing. |
| fom_acentric | double precision | _pdbx_phasing_MAD_set_shell.fom_acentric records the figure of merit using acentric data for MAD phasing. |
| fom_centric | double precision | _pdbx_phasing_MAD_set_shell.fom_centric records the figure of merit using centric data for MAD phasing. |
| fom | double precision | _pdbx_phasing_MAD_set_shell.fom records the figure of merit for MAD phasing. |
| R_cullis_centric | double precision | _pdbx_phasing_MAD_set_shell.R_cullis_centric records R_cullis using centric data for MAD phasing. |
| R_cullis_acentric | double precision | _pdbx_phasing_MAD_set_shell.R_cullis_acentric records R_cullis using acentric data for MAD phasing. |
| R_cullis | double precision | _pdbx_phasing_MAD_set_shell.R_cullis records R_cullis for MAD phasing. |
| R_kraut_centric | double precision | _pdbx_phasing_MAD_set_shell.R_kraut_centric records R_kraut using centric data for MAD phasing. |
| R_kraut_acentric | double precision | _pdbx_phasing_MAD_set_shell.R_kraut_acentric records R_kraut using acentric data for MAD phasing. |
| R_kraut | double precision | _pdbx_phasing_MAD_set_shell.R_kraut records R_kraut for MAD phasing. |
| loc_centric | double precision | _pdbx_phasing_MAD_set_shell.loc_centric records lack of closure using centric data for MAD phasing. |
| loc_acentric | double precision | _pdbx_phasing_MAD_set_shell.loc_acentric records lack of closure using acentric data for MAD phasing. |
| loc | double precision | _pdbx_phasing_MAD_set_shell.loc records lack of closure for MAD phasing. |
| power_centric | double precision | _pdbx_phasing_MAD_set_shell.power_centric records phasing power using centric data for MAD phasing. |
| power_acentric | double precision | _pdbx_phasing_MAD_set_shell.power_acentric records phasing power using acentric data for MAD phasing. |
| power | double precision | _pdbx_phasing_MAD_set_shell.power records phasing power for MAD phasing. |

## pdbx_phasing_MAD_set_site

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | _pdbx_phasing_MAD_set_site.id records the number of site obtained from MAD phasing. |
| atom_type_symbol | text | _pdbx_phasing_MAD_set_site.atom_type_symbol records the name of site obtained from MAD phasing. |
| Cartn_x | double precision | _pdbx_phasing_MAD_set_site.Cartn_x records the X Cartesian coordinate of site obtained from MAD phasing. |
| Cartn_y | double precision | _pdbx_phasing_MAD_set_site.Cartn_y records the Y Cartesian coordinate of site obtained from MAD phasing. |
| Cartn_z | double precision | _pdbx_phasing_MAD_set_site.Cartn_z records the Z Cartesian coordinate of site obtained from MAD phasing. |
| fract_x | double precision | _pdbx_phasing_MAD_set_site.fract_x records the X fractional coordinate of site obtained from MAD phasing. |
| fract_y | double precision | _pdbx_phasing_MAD_set_site.fract_y records the Y fractional coordinate of site obtained from MAD phasing. |
| fract_z | double precision | _pdbx_phasing_MAD_set_site.fract_z records the Z fractional coordinate of site obtained from MAD phasing. |
| b_iso | double precision | _pdbx_phasing_MAD_set_site.b_iso records isotropic temperature factor parameterthe for the site obtained from MAD phasing. |
| occupancy | double precision | _pdbx_phasing_MAD_set_site.occupancy records the fraction of the atom type presented at this site. |
| occupancy_iso | double precision | The relative real isotropic occupancy of the atom type present at this heavy-atom site in a given atom site. |

## pdbx_phasing_MAD_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| d_res_low | double precision | _pdbx_phasing_MAD_shell.d_res_low records the lower resolution for the shell. |
| d_res_high | double precision | _pdbx_phasing_MAD_shell.d_res_high records the higher resolution for the shell. |
| reflns_acentric | double precision | _pdbx_phasing_MAD_shell.reflns_acentric records the number of acentric reflections for MAD phasing. |
| reflns_centric | integer | _pdbx_phasing_MAD_shell.reflns_centric records the number of centric reflections for MAD phasing. |
| reflns | integer | _pdbx_phasing_MAD_shell.reflns records the number of reflections used for MAD phasing. |
| fom_acentric | double precision | _pdbx_phasing_MAD_shell.fom_acentric records the figure of merit using acentric data for MAD phasing. |
| fom_centric | double precision | _pdbx_phasing_MAD_shell.fom_centric records the figure of merit using centric data for MAD phasing. |
| fom | double precision | _pdbx_phasing_MAD_shell.fom records the figure of merit for MAD phasing. |

## pdbx_phasing_MR

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | The value of _pdbx_phasing_MR.entry_id identifies the data block. |
| method_rotation | text | The value of _pdbx_phasing_MR.method_rotation identifies the method used for rotation search. For example, the rotation method may be realspace, fastdirect, or direct. . |
| d_res_high_rotation | double precision | The value of _pdbx_phasing_MR.d_res_high_rotation identifies the highest resolution used for rotation search. |
| d_res_low_rotation | double precision | The value of _pdbx_phasing_MR.d_res_low_rotation identifies the lowest resolution used for rotation search. |
| sigma_F_rotation | double precision | The value of _pdbx_phasing_MR.sigma_F_rotation identifies the sigma cut off of structure factor used for rotation search. |
| reflns_percent_rotation | double precision | The value of _pdbx_phasing_MR.reflns_percent_rotation identifies the completness of data used for rotation search. |
| method_translation | text | The value of _pdbx_phasing_MR.method_translation identifies the method used for translation search. For example in CNS, the translation method may be "general" or "phased" with PC refinement target using "fastf2f2" "e2e2" "e1e1" "f2f2" "f1f1" "residual" "vector". . |
| d_res_high_translation | double precision | The value of _pdbx_phasing_MR.d_res_high_translation identifies the highest resolution used for translation search. |
| d_res_low_translation | double precision | The value of _pdbx_phasing_MR.d_res_low_translation identifies the lowest resolution used for translation search. |
| sigma_F_translation | double precision | The value of _pdbx_phasing_MR.sigma_F_translation identifies the sigma cut off of structure factor used for translation search. |
| reflns_percent_translation | double precision | The value of _pdbx_phasing_MR.reflns_percent_translation identifies the completness of data used for translation search. |
| correlation_coeff_Io_to_Ic | double precision | The value of _pdbx_phasing_MR.correlation_coeff_Io_to_Ic identifies the correlation between the observed and the calculated intensity (~\|F\|^2) after rotation and translation. |
| correlation_coeff_Fo_to_Fc | double precision | The value of _pdbx_phasing_MR.correlation_coeff_Fo_to_Fc identifies the correlation between the observed and the calculated structure factor after rotation and translation. |
| R_factor | double precision | The value of _pdbx_phasing_MR.R_factor identifies the R factor (defined as uasual) after rotation and translation. |
| R_rigid_body | double precision | The value of _pdbx_phasing_MR.R_rigid_body identifies the R factor for rigid body refinement after rotation and translation.(In general, rigid body refinement has to be carried out after molecular replacement. |
| packing | double precision | The value of _pdbx_phasing_MR.packing identifies the packing of search model in the unit cell. Too many crystallographic contacts may indicate a bad search. |
| model_details | text | The value of _pdbx_phasing_MR.model_details records the details of model used. For example, the original model can be truncated by deleting side chains, doubtful parts, using the monomer if the original model was an oligomer. The search model may be one domain of a large molecule. What is the pdb IDs. |

## pdbx_phasing_dm

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | The value of _pdbx_phasing_dm.entry_id identifies the data block. |
| method | text | The value of _pdbx_phasing_dm.method identifies the method used for density modification |
| mask_type | text | The value of _pdbx_phasing_dm.mask_type identifies the type of mask used for density modification |
| fom_acentric | double precision | The value of _pdbx_phasing_dm.fom_acentric identifies the figure of merit for acentric data |
| fom_centric | double precision | The value of _pdbx_phasing_dm.fom_centric identifies the figure of merit for acentric data |
| fom | double precision | The value of _pdbx_phasing_dm.fom identifies the figure of merit for all the data |
| reflns_acentric | integer | The value of _pdbx_phasing_dm.reflns_acentric identifies the number of acentric reflections. |
| reflns_centric | integer | The value of _pdbx_phasing_dm.reflns_centric identifies the number of centric reflections. |
| reflns | integer | The value of _pdbx_phasing_dm.reflns identifies the number of centric and acentric reflections. |
| delta_phi_initial | double precision | The value of _pdbx_phasing_dm.delta_phi_initial identifies phase difference before density modification |
| delta_phi_final | double precision | The value of _pdbx_phasing_dm.delta_phi_final identifies phase difference after density modification |

## pdbx_phasing_dm_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| d_res_high | double precision | The value of _pdbx_phasing_dm_shell.d_res_high identifies high resolution |
| d_res_low | double precision | The value of _pdbx_phasing_dm_shell.d_res_low identifies low resolution |
| fom_acentric | double precision | The value of _pdbx_phasing_dm_shell.fom_acentric identifies the figure of merit for acentric data with resolution shells |
| fom_centric | double precision | The value of _pdbx_phasing_dm_shell.fom_centric identifies the figure of merit for centric data with resolution shells. |
| fom | double precision | The value of _pdbx_phasing_dm_shell.fom identifies the figure of merit for all the data with resolution shells. |
| reflns_acentric | integer | The value of _pdbx_phasing_dm_shell.reflns_acentric identifies the number of acentric reflections with resolution shells. |
| reflns_centric | integer | The value of _pdbx_phasing_dm_shell.reflns_centric identifies the number of centric reflections with resolution shells. |
| reflns | integer | The value of _pdbx_phasing_dm_shell.reflns identifies the number of centric and acentric reflections with resolution shells. |
| delta_phi_final | double precision | The value of _pdbx_phasing_dm_shell.delta_phi_final identifies phase difference after density modification with resolution shells. |

## pdbx_point_symmetry

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| Schoenflies_symbol | text | The Schoenflies point symmetry symbol. |
| circular_symmetry | integer | Rotational n-fold C and D point symmetry. |
| H-M_notation | text |  |

## pdbx_poly_seq_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| asym_id | text | Pointer to _atom_site.label_asym_id. |
| entity_id | text | Pointer to _entity.id. |
| seq_id | integer | Pointer to _entity_poly_seq.num |
| hetero | text | Pointer to _entity_poly_seq.hetero |
| mon_id | text | Pointer to _entity_poly_seq.mon_id. |
| pdb_strand_id | text | PDB strand/chain id. |
| ndb_seq_num | integer | NDB residue number. |
| pdb_seq_num | text | PDB residue number. |
| auth_seq_num | text | Author provided residue number. This value may differ from the PDB residue number and may not correspond to residue numbering within the coordinate records. |
| pdb_mon_id | text | PDB residue identifier. |
| auth_mon_id | text | Author provided residue identifier. This value may differ from the PDB residue identifier and may not correspond to residue identifier within the coordinate records. |
| pdb_ins_code | text | PDB insertion code. |

## pdbx_refine

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _pdbx_refine.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| R_factor_all_no_cutoff | double precision | R-value (all reflections, no cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| R_factor_obs_no_cutoff | double precision | R-value (working set reflections, no cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| free_R_factor_4sig_cutoff | double precision | R free value (4 sigma cutoff). Placeholder for PDB mapping of SHELXL refinement data. |
| free_R_factor_no_cutoff | double precision | Free R-value (no cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| free_R_error_no_cutoff | double precision | Free R-value error(no cutoff) |
| free_R_val_test_set_size_perc_no_cutoff | double precision | Free R-value test set size (in percent, no cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| free_R_val_test_set_ct_no_cutoff | double precision | Free R-value test set count (no cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| number_reflns_obs_no_cutoff | double precision | Total number of reflections (no cutoff). Placeholder for PDB mapping of SHELXL refinement data. |
| R_factor_all_4sig_cutoff | double precision | R-value (all reflections, 4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| R_factor_obs_4sig_cutoff | double precision | R-value (working set, 4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| free_R_val_test_set_size_perc_4sig_cutoff | double precision | Free R-value test set size (in percent, 4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| free_R_val_test_set_ct_4sig_cutoff | double precision | Free R-value test set count (4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data. |
| number_reflns_obs_4sig_cutoff | double precision | Total number of reflections (4 sigma cutoff). Placeholder for PDB mapping of SHELXL refinement data. |

## pdbx_refine_tls

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _pdbx_refine_tls.id must uniquely identify a record in the PDBX_REFINE_TLS list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _pdbx_refine_tls.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| details | text | A description of the TLS group, such as a domain name or a chemical group name. |
| method | text | The method by which the TLS parameters were obtained. |
| origin_x | double precision | The x coordinate in angstroms of the origin to which the TLS parameters are referred, specified according to a set of orthogonal Cartesian axes related to the cell axes as given in _atom_sites.Cartn_transform_axes. If the origin is omitted, it is assumed to be the centre of reaction of the group, in which case S must be symmetric |
| origin_y | double precision | The y coordinate in angstroms of the origin to which the TLS parameters are referred, specified according to a set of orthogonal Cartesian axes related to the cell axes as given in _atom_sites.Cartn_transform_axes. If the origin is omitted, it is assumed to be the centre of reaction of the group, in which case S must be symmetric |
| origin_z | double precision | The z coordinate in angstroms of the origin to which the TLS parameters are referred, specified according to a set of orthogonal Cartesian axes related to the cell axes as given in _atom_sites.Cartn_transform_axes. If the origin is omitted, it is assumed to be the centre of reaction of the group, in which case S must be symmetric |
| T11 | double precision |  |
| T11_esd | double precision |  |
| T12 | double precision |  |
| T12_esd | double precision |  |
| T13 | double precision |  |
| T13_esd | double precision |  |
| T22 | double precision |  |
| T22_esd | double precision |  |
| T23 | double precision |  |
| T23_esd | double precision |  |
| T33 | double precision |  |
| T33_esd | double precision |  |
| L11 | double precision |  |
| L11_esd | double precision |  |
| L12 | double precision |  |
| L12_esd | double precision |  |
| L13 | double precision |  |
| L13_esd | double precision |  |
| L22 | double precision |  |
| L22_esd | double precision |  |
| L23 | double precision |  |
| L23_esd | double precision |  |
| L33 | double precision |  |
| L33_esd | double precision |  |
| S11 | double precision |  |
| S11_esd | double precision |  |
| S12 | double precision |  |
| S12_esd | double precision |  |
| S13 | double precision |  |
| S13_esd | double precision |  |
| S21 | double precision |  |
| S21_esd | double precision |  |
| S22 | double precision |  |
| S22_esd | double precision |  |
| S23 | double precision |  |
| S23_esd | double precision |  |
| S31 | double precision |  |
| S31_esd | double precision |  |
| S32 | double precision |  |
| S32_esd | double precision |  |
| S33 | double precision |  |
| S33_esd | double precision |  |

## pdbx_refine_tls_group

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _pdbx_refine_tls_group.id must uniquely identify a record in the REFINE_TLS_GROUP list for a particular refinement. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _pdbx_refine_tls_group.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| refine_tls_id | text | This data item is a pointer to _pdbx_refine_tls.id in the REFINE_TLS category. |
| beg_label_asym_id | text | A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| beg_label_seq_id | integer | A component of the identifier for the residue at which the TLS fragment range begins. |
| beg_auth_asym_id | text | A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| beg_auth_seq_id | text | A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| beg_PDB_ins_code | text | A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| end_label_asym_id | text | A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| end_label_seq_id | integer | A component of the identifier for the residue at which the TLS fragment range ends. |
| end_auth_asym_id | text | A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| end_auth_seq_id | text | A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| end_PDB_ins_code | text | A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| selection | text | A qualification of the subset of atoms in the specified range included in the TLS fragment. |
| selection_details | text | A text description of subset of atoms included included in the TLS fragment. |

## pdbx_reflns_twin

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | The diffraction data set identifier. A reference to _diffrn.id in category DIFFRN. |
| crystal_id | text | The crystal identifier. A reference to _exptl_crystal.id in category EXPTL_CRYSTAL. |
| domain_id | text | An identifier for the twin domain. |
| type | text | There are two types of twinning: merohedral or hemihedral non-merohedral or epitaxial For merohedral twinning the diffraction patterns from the different domains are completely superimposable. Hemihedral twinning is a special case of merohedral twinning. It only involves two distinct domains. Pseudo-merohedral twinning is a subclass merohedral twinning in which lattice is coincidentally superimposable. In the case of non-merohedral or epitaxial twinning the reciprocal lattices do not superimpose exactly. In this case the diffraction pattern consists of two (or more) interpenetrating lattices, which can in principle be separated. |
| operator | text | The possible merohedral or hemihedral twinning operators for different point groups are: True point group Twin operation hkl related to 3 2 along a,b h,-h-k,-l 2 along a*,b* h+k,-k,-l 2 along c -h,-k,l 4 2 along a,b,a*,b* h,-k,-l 6 2 along a,b,a*,b* h,-h-k,-l 321 2 along a*,b*,c -h,-k,l 312 2 along a,b,c -h,-k,l 23 4 along a,b,c k,-h,l References: Yeates, T.O. (1997) Methods in Enzymology 276, 344-358. Detecting and Overcoming Crystal Twinning. and information from the following on-line sites: CNS site http://cns.csb.yale.edu/v1.1/ CCP4 site http://www.ccp4.ac.uk/dist/html/detwin.html SHELX site http://shelx.uni-ac.gwdg.de/~rherbst/twin.html |
| fraction | double precision | The twin fraction or twin factor represents a quantitative parameter for the crystal twinning. The value 0 represents no twinning, < 0.5 partial twinning, = 0.5 for perfect twinning. |

## pdbx_related_exp_data_set

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| ordinal | integer | Ordinal identifier for each related experimental data set. |
| data_reference | text | A DOI reference to the related data set. |
| metadata_reference | text | A DOI reference to the metadata decribing the related data set. |
| data_set_type | text | The type of the experimenatal data set. |
| details | text | Additional details describing the content of the related data set and its application to the current investigation. |

## pdbx_serial_crystallography_data_reduction

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | The data item is a pointer to _diffrn.id in the DIFFRN category. |
| frames_total | integer | The total number of data frames collected for this data set. |
| xfel_pulse_events | integer | For FEL experiments, the number of pulse events in the dataset. |
| frame_hits | integer | For experiments in which samples are provided in a continuous stream, the total number of data frames collected in which the sample was hit. |
| crystal_hits | integer | For experiments in which samples are provided in a continuous stream, the total number of frames collected in which the crystal was hit. |
| frames_failed_index | integer | For experiments in which samples are provided in a continuous stream, the total number of data frames collected that contained a "hit" but failed to index. |
| frames_indexed | integer | For experiments in which samples are provided in a continuous stream, the total number of data frames collected that were indexed. |
| lattices_indexed | integer | For experiments in which samples are provided in a continuous stream, the total number of lattices indexed. |
| xfel_run_numbers | text | For FEL experiments, in which data collection was performed in batches, indicates which subset of the data collected were used in producing this dataset. |

## pdbx_serial_crystallography_measurement

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | The data item is a pointer to _diffrn.id in the DIFFRN category. |
| pulse_energy | double precision | The energy/pulse of the X-ray pulse impacting the sample measured in microjoules. |
| pulse_duration | double precision | The average duration (femtoseconds) of the pulse energy measured at the sample. |
| xfel_pulse_repetition_rate | double precision | For FEL experiments, the pulse repetition rate measured in cycles per seconds. |
| pulse_photon_energy | double precision | The photon energy of the X-ray pulse measured in KeV. |
| photons_per_pulse | double precision | The photons per pulse measured in (tera photons (10^(12)^)/pulse units). |
| source_size | double precision | The dimension of the source beam measured at the source (micrometres squared). |
| source_distance | double precision | The distance from source to the sample along the optical axis (metres). |
| focal_spot_size | double precision | The focal spot size of the beam impinging on the sample (micrometres squared). |
| collimation | text | The collimation or type of focusing optics applied to the radiation. |
| collection_time_total | double precision | The total number of hours required to measure this data set. |

## pdbx_serial_crystallography_sample_delivery

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | The data item is a pointer to _diffrn.id in the DIFFRN category. |
| description | text | The description of the mechanism by which the specimen in placed in the path of the source. |
| method | text | The description of the mechanism by which the specimen in placed in the path of the source. |

## pdbx_serial_crystallography_sample_delivery_fixed_target

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | The data item is a pointer to _diffrn.id in the DIFFRN category. |
| description | text | For a fixed target sample, a description of sample preparation |
| sample_holding | text | For a fixed target sample, mechanism to hold sample in the beam |
| support_base | text | Type of base holding the support |
| sample_unit_size | double precision | Size of pore in grid supporting sample. Diameter or length in micrometres, e.g. pore diameter |
| crystals_per_unit | integer | The number of crystals per dropplet or pore in fixed target |
| sample_solvent | text | The sample solution content and concentration |
| sample_dehydration_prevention | text | Method to prevent dehydration of sample |
| motion_control | text | Device used to control movement of the fixed sample |
| velocity_horizontal | double precision | Velocity of sample horizontally relative to a perpendicular beam in millimetres/second |
| velocity_vertical | double precision | Velocity of sample vertically relative to a perpendicular beam in millimetres/second |
| details | text | Any details pertinent to the fixed sample target |

## pdbx_serial_crystallography_sample_delivery_injection

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| diffrn_id | text | The data item is a pointer to _diffrn.id in the DIFFRN category. |
| description | text | For continuous sample flow experiments, a description of the injector used to move the sample into the beam. |
| injector_diameter | double precision | For continuous sample flow experiments, the diameter of the injector in micrometres. |
| injector_temperature | double precision | For continuous sample flow experiments, the temperature in Kelvins of the speciman injected. This may be different from the temperature of the sample. |
| flow_rate | double precision | For continuous sample flow experiments, the flow rate of solution being injected measured in ul/min. |
| carrier_solvent | text | For continuous sample flow experiments, the carrier buffer used to move the sample into the beam. Should include protein concentration. |
| crystal_concentration | double precision | For continuous sample flow experiments, the concentration of crystals in the solution being injected. The concentration is measured in million crystals/ml. |
| preparation | text | Details of crystal growth and preparation of the crystals |
| power_by | text | Sample deliver driving force, e.g. Gas, Electronic Potential |
| injector_nozzle | text | The type of nozzle to deliver and focus sample jet |
| jet_diameter | double precision | Diameter in micrometres of jet stream of sample delivery |
| filter_size | double precision | The size of filter in micrometres in filtering crystals |

## pdbx_sifts_unp_segments

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity_poly_seq.entity_id in the ENTITY_POLY_SEQ category. |
| asym_id | text | This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| unp_acc | text | The UniProt accession code related to the SIFTS segment mapping. |
| segment_id | integer | The UniProt segment defined by the external database. |
| instance_id | integer | The UniProt instance identifier. |
| unp_start | integer | The sequence position in the related UniProt entry at which the mapping alignment begins. |
| unp_end | integer | The sequence position in the related UniProt entry at which the mapping alignment ends. |
| seq_id_start | integer | The sequence position in the entity or biological unit described in the data block at which the UniProt alignment begins. |
| seq_id_end | integer | The sequence position in the entity or biological unit described in the data block at which the UniProt alignment ends. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |
| best_mapping | text | This code indicates whether the SIFTS UniProt accession and residue range was the best-scoring sequence match. |
| identity | double precision | The identity score reports on the sequence identity for the sequence defined by the entity start and end range compared to the sequence defined by start and end range of the related UniProt accession. |

## pdbx_sifts_xref_db

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| asym_id | text | This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| seq_id_ordinal | integer | The value of pdbx_sifts_xref_db.seq_id_ordinal identifies a distinct residue specific cross-reference record in the _pdbx_sifts_xref_db category. |
| seq_id | integer | This data item is an effective pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |
| mon_id | text | This data item is an effective pointer to _entity_poly_seq.mon_id. |
| mon_id_one_letter_code | text | Describes the standard polymer component of _pdbx_sifts_xref_db.mon_id as one-letter code |
| unp_res | text | Describes the residue type, in one-letter code, at the corresponding residue position of the related UniProt match |
| unp_num | integer | The sequence position of the UniProt entry that corresponds to the residue mapping. |
| unp_acc | text | The UniProt accession code for the mapped entry |
| unp_segment_id | integer | The pdbx_sifts_xref_db UniProt segment ID refers to the distinct contiguous residue-range segments with a UniProt residue mapping. |
| unp_instance_id | integer | The pdbx_sifts_xref_db UniProt instance ID refers to distinct UniProt residue mappings for a given position (i.e. the same segment, residue, asym, & entity). |
| res_type | text | A description of the difference between the entity sequence position residue type and that in the mapped UniProt entry. |
| observed | text | Describes whether or not a reside has atomic coordinates in the corresponding model. |
| mh_id | integer | An index value corresponding to the instance of microheterogeneity per residue |
| xref_db_name | text | The name of additional external databases with residue level mapping. |
| xref_db_acc | text | The accession code related to the additional external database entry. |
| xref_domain_name | text | The domain name defined by the external database. |
| xref_db_segment_id | integer | The pdbx_sifts_xref_db xref segment ID refers to a distinct contiguous residue-range segment for a mapping to a specific external database. |
| xref_db_instance_id | integer | The instance identifier defined by the external database. |

## pdbx_sifts_xref_db_segments

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| asym_id | text | This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| xref_db | text | The name of additional external databases with range level mapping. |
| xref_db_acc | text | The accession code related to the external database entry. |
| domain_name | text | The domain name defined by the external database. |
| segment_id | integer | The segment identifier defined by the external database. |
| instance_id | integer | The instance identifier defined by the external database. |
| seq_id_start | integer | The sequence position in the entity or biological unit described in the data block at which the segment alignment begins. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |
| seq_id_end | integer | The sequence position in the entity or biological unit described in the data block at which the segment alignment ends. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |

## pdbx_soln_scatter

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| id | text | The value of _pdbx_soln_scatter.id must uniquely identify the sample in the category PDBX_SOLN_SCATTER |
| type | text | The type of solution scattering experiment carried out |
| source_beamline | text | The beamline name used for the experiment |
| source_beamline_instrument | text | The instrumentation used on the beamline |
| detector_type | text | The general class of the radiation detector. |
| detector_specific | text | The particular radiation detector. In general this will be a manufacturer, description, model number or some combination of these. |
| source_type | text | The make, model, name or beamline of the source of radiation. |
| source_class | text | The general class of the radiation source. |
| num_time_frames | integer | The number of time frame solution scattering images used. |
| sample_pH | double precision | The pH value of the buffered sample. |
| temperature | double precision | The temperature in kelvins at which the experiment was conducted |
| concentration_range | text | The concentration range (mg/mL) of the complex in the sample used in the solution scattering experiment to determine the mean radius of structural elongation. |
| buffer_name | text | The name of the buffer used for the sample in the solution scattering experiment. |
| mean_guiner_radius | double precision | The mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q gives the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of "Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2 |
| mean_guiner_radius_esd | double precision | The estimated standard deviation for the mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of "Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2 |
| min_mean_cross_sectional_radii_gyration | double precision | The minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of "Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2 |
| min_mean_cross_sectional_radii_gyration_esd | double precision | The estimated standard deviation for the minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of "Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2 |
| max_mean_cross_sectional_radii_gyration | double precision | The maximum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of "Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2 |
| max_mean_cross_sectional_radii_gyration_esd | double precision | The estimated standard deviation for the minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of "Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2 |
| protein_length | text | The length (or range) of the protein sample under study. If the solution structure is approximated as an elongated elliptical cyclinder the length L is determined from, L = sqrt [12( (R_G)^2 - (R_XS)^2 ) ] The length should also be given by L = pi I(0) / [ I(Q).Q]_Q->0 |
| data_reduction_software_list | text | A list of the software used in the data reduction |
| data_analysis_software_list | text | A list of the software used in the data analysis |

## pdbx_soln_scatter_model

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| scatter_id | text | This data item is a pointer to _pdbx_soln_scatter.id in the PDBX_SOLN_SCATTER category. |
| id | text | The value of _pdbx_soln_scatter_model.id must uniquely identify the sample in the category PDBX_SOLN_SCATTER_MODEL |
| details | text | A description of any additional details concerning the experiment. |
| method | text | A description of the methods used in the modelling |
| software_list | text | A list of the software used in the modeeling |
| software_author_list | text | A list of the software authors |
| entry_fitting_list | text | A list of the entries used to fit the model to the scattering data |
| num_conformers_calculated | integer | The number of model conformers calculated. |
| num_conformers_submitted | integer | The number of model conformers submitted in the entry |
| representative_conformer | integer | The index of the representative conformer among the submitted conformers for the entry |
| conformer_selection_criteria | text | A description of the conformer selection criteria used. |

## pdbx_struct_assembly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| method_details | text | Provides details of the method used to determine or compute the assembly. |
| oligomeric_details | text | Provides the details of the oligomeric state of the assembly. |
| oligomeric_count | integer | The number of polymer molecules in the assembly. |
| details | text | A description of special aspects of the macromolecular assembly. In the PDB, 'representative helical assembly', 'complete point assembly', 'complete icosahedral assembly', 'software_defined_assembly', 'author_defined_assembly', and 'author_and_software_defined_assembly' are considered "biologically relevant assemblies. |
| id | text | The value of _pdbx_struct_assembly.id must uniquely identify a record in the PDBX_STRUCT_ASSEMBLY list. |

## pdbx_struct_assembly_auth_evidence

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | Identifies a unique record in pdbx_struct_assembly_auth_evidence. |
| assembly_id | text | This item references an assembly in pdbx_struct_assembly |
| experimental_support | text | Provides the experimental method to determine the state of this assembly |
| details | text | Provides any additional information regarding the evidence of this assembly |

## pdbx_struct_assembly_gen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| asym_id_list | text |  |
| _hash_asym_id_list | text | [pmb] SHA-256 hash of asym_id_list for composite primary key deduplication. |
| assembly_id | text |  |
| oper_expression | text |  |
| _hash_oper_expression | text | [pmb] SHA-256 hash of oper_expression for composite primary key deduplication. |

## pdbx_struct_assembly_prop

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| biol_id | text | The identifier for the assembly used in category PDBX_STRUCT_ASSEMBLY. |
| type | text | The property type for the assembly. |
| value | text | The value of the assembly property. |

## pdbx_struct_chem_comp_diagnostics

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| type | text | A classification of the diagnostic for the chemical component instance |
| pdb_strand_id | text | PDB strand/chain id. |
| asym_id | text | Instance identifier for the polymer molecule. |
| auth_seq_id | text | PDB position in the sequence. |
| seq_num | integer | Position in the sequence. |
| auth_comp_id | text | PDB component ID |
| ordinal | integer | An ordinal index for this category |

## pdbx_struct_conn_angle

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _pdbx_struct_conn_angle.id must uniquely identify a record in the PDBX_STRUCT_CONN_ANGLE list. Note that this item need not be a number; it can be any unique identifier. |
| ptnr1_label_alt_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| ptnr1_label_asym_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| ptnr1_label_atom_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category. |
| ptnr1_label_comp_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| ptnr1_label_seq_id | integer | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| ptnr1_auth_asym_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| ptnr1_auth_comp_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| ptnr1_auth_seq_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| ptnr1_symmetry | text | Describes the symmetry operation that should be applied to the atom specified by _pdbx_struct_conn_angle.ptnr1_label* to generate the first partner in the structure angle. |
| ptnr2_label_alt_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category. |
| ptnr2_label_asym_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| ptnr2_label_atom_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category. |
| ptnr2_label_comp_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| ptnr2_label_seq_id | integer | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| ptnr2_auth_asym_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| ptnr2_auth_comp_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| ptnr2_auth_seq_id | text | A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| ptnr2_symmetry | text | Describes the symmetry operation that should be applied to the atom specified by _pdbx_struct_conn_angle.ptnr2_label* to generate the second partner in the structure angle. |
| ptnr1_PDB_ins_code | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| ptnr2_PDB_ins_code | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| ptnr3_auth_asym_id | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| ptnr3_auth_comp_id | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| ptnr3_PDB_ins_code | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| ptnr3_auth_seq_id | text | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| ptnr3_label_alt_id | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| ptnr3_label_asym_id | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| ptnr3_label_atom_id | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category. |
| ptnr3_label_comp_id | text | A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| ptnr3_label_seq_id | integer | A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| ptnr3_symmetry | text | Describes the symmetry operation that should be applied to the atom specified by _pdbx_struct_conn_angle.ptnr3_label* to generate the first partner in the structure angle. |
| value | double precision | Angle in degrees defined by the three sites _pdbx_struct_conn_angle.ptnr1_label_atom_id, _pdbx_struct_conn_angle.ptnr2_label_atom_id _pdbx_struct_conn_angle.ptnr3_label_atom_id |

## pdbx_struct_entity_inst

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of this portion of the contents of the deposited unit. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| id | text | The value of _pdbx_struct_entity_inst.id must uniquely identify a record in the PDBX_STRUCT_ENTITY_INST list. The entity instance is a method neutral identifier for the observed molecular entities in the deposited coordinate set. |

## pdbx_struct_legacy_oper_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | This integer value must uniquely identify a record in the PDBX_STRUCT_LEGACY_OPER_LIST list. |
| name | text | A descriptive name for the transformation operation. |
| matrix11 | double precision |  |
| matrix12 | double precision |  |
| matrix13 | double precision |  |
| matrix21 | double precision |  |
| matrix22 | double precision |  |
| matrix23 | double precision |  |
| matrix31 | double precision |  |
| matrix32 | double precision |  |
| matrix33 | double precision |  |
| vector1 | double precision |  |
| vector2 | double precision |  |
| vector3 | double precision |  |

## pdbx_struct_mod_residue

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_struct_mod_residue.id must uniquely identify each item in the PDBX_STRUCT_MOD_RESIDUE list. This is an integer serial number. |
| auth_asym_id | text | Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_asym_id | text | Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_comp_id | text | Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_seq_id | integer | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| parent_comp_id | text | The parent component identifier for this modified polymer component. |
| details | text | Details of the modification for this polymer component. |

## pdbx_struct_msym_gen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entity_inst_id | text | This data item is a pointer to _pdbx_struct_entity_inst.id in the PDBX_STRUCT_ENTITY_INST category. |
| msym_id | text | Uniquely identifies the this structure instance in point symmetry unit. |
| oper_expression | text | Identifies the operation from category PDBX_STRUCT_OPER_LIST. |

## pdbx_struct_oper_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | This identifier code must uniquely identify a record in the PDBX_STRUCT_OPER_LIST list. |
| type | text | A code to indicate the type of operator. |
| name | text | A descriptive name for the transformation operation. |
| symmetry_operation | text | The symmetry operation corresponding to the transformation operation. |
| matrix11 | double precision |  |
| matrix12 | double precision |  |
| matrix13 | double precision |  |
| matrix21 | double precision |  |
| matrix22 | double precision |  |
| matrix23 | double precision |  |
| matrix31 | double precision |  |
| matrix32 | double precision |  |
| matrix33 | double precision |  |
| vector1 | double precision |  |
| vector2 | double precision |  |
| vector3 | double precision |  |

## pdbx_struct_sheet_hbond

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| range_id_1 | text | This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category. |
| range_id_2 | text | This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category. |
| sheet_id | text | This data item is a pointer to _struct_sheet.id in the STRUCT_SHEET category. |
| range_1_label_atom_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category. |
| range_1_label_seq_id | integer | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| range_1_label_comp_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| range_1_label_asym_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| range_1_auth_atom_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| range_1_auth_seq_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| range_1_auth_comp_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| range_1_auth_asym_id | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| range_1_PDB_ins_code | text | A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| range_2_label_atom_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category. |
| range_2_label_seq_id | integer | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| range_2_label_comp_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| range_2_label_asym_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| range_2_auth_atom_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| range_2_auth_seq_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| range_2_auth_comp_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| range_2_auth_asym_id | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| range_2_PDB_ins_code | text | A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |

## pdbx_struct_special_symmetry

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_struct_special_symmetry.id must uniquely identify each item in the PDBX_STRUCT_SPECIAL_SYMMETRY list. This is an integer serial number. |
| PDB_model_num | integer | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_asym_id | text | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_comp_id | text | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_seq_id | integer | Part of the identifier for the molecular component. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |

## pdbx_unobs_or_zero_occ_atoms

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_unobs_or_zero_occ_atoms.id must uniquely identify each item in the PDBX_UNOBS_OR_ZERO_OCC_ATOMS list. This is an integer serial number. |
| polymer_flag | text | The value of polymer flag indicates whether the unobserved or zero occupancy atom is part of a polymer chain |
| occupancy_flag | integer | The value of occupancy flag indicates whether the atom is either unobserved (=1) or has zero occupancy (=0) |
| PDB_model_num | integer | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category. |
| label_atom_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category. |
| label_asym_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_comp_id | text | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_seq_id | integer | Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |

## pdbx_unobs_or_zero_occ_residues

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_unobs_or_zero_occ_residues.id must uniquely identify each item in the PDBX_UNOBS_OR_ZERO_OCC_RESIDUES list. This is an integer serial number. |
| polymer_flag | text | The value of polymer flag indicates whether the unobserved or zero occupancy residue is part of a polymer chain or not |
| occupancy_flag | integer | The value of occupancy flag indicates whether the residue is unobserved (= 1) or the coordinates have an occupancy of zero (=0) |
| PDB_model_num | integer | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_asym_id | text | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_comp_id | text | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_seq_id | integer | Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |

## pdbx_validate_chiral

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_chiral.id must uniquely identify each item in the PDBX_VALIDATE_CHIRAL list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given residue This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| label_alt_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Optional identifier of the residue This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| details | text | A description of the outlier angle e.g. ALPHA-CARBON |

## pdbx_validate_close_contact

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_close_contact.id must uniquely identify each item in the PDBX_VALIDATE_CLOSE_CONTACT list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given contact |
| auth_asym_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_atom_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_asym_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code_1 | text | Optional identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| PDB_ins_code_2 | text | Optional identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id_1 | text | An optional identifier of the first of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| label_alt_id_2 | text | An optional identifier of the second of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| dist | double precision | The value of the close contact for the two atoms defined. |

## pdbx_validate_main_chain_plane

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_main_chain_plane.id must uniquely identify each item in the PDBX_VALIDATE_MAIN_CHAIN_PLANE list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the residue in which the plane is calculated This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id | text | Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| improper_torsion_angle | double precision | The value for the torsion angle C(i-1) - CA(i-1) - N(i) - O(i-1) |

## pdbx_validate_peptide_omega

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_peptide_omega.id must uniquely identify each item in the PDBX_VALIDATE_PEPTIDE_OMEGA list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given residue This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id_1 | text | Part of the identifier of the first residue in the bond This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_asym_id_2 | text | Part of the identifier of the second residue in the bond This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_1 | text | Part of the identifier of the first residue in the bond This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_comp_id_2 | text | Part of the identifier of the second residue in the bond This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_1 | text | Part of the identifier of the first residue in the bond This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_seq_id_2 | text | Part of the identifier of the second residue in the bond This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code_1 | text | Optional identifier of the first residue in the bond This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| PDB_ins_code_2 | text | Optional identifier of the second residue in the bond This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id_1 | text | Optional identifier of the first residue in the torsion angle This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| label_alt_id_2 | text | Optional identifier of the second residue in the torsion angle This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| omega | double precision | The value of the OMEGA angle for the peptide linkage between the two defined residues |

## pdbx_validate_planes

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_planes.id must uniquely identify each item in the PDBX_VALIDATE_PLANES list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given angle This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id | text | Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| rmsd | double precision | The value of the overall deviation from ideal plane for the atoms defining the plane. |
| type | text | The type of plane - MAIN CHAIN or SIDE CHAIN atoms |

## pdbx_validate_polymer_linkage

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_polymer_linkage.id must uniquely identify each item in the PDBX_VALIDATE_POLYMER_LINKAGE list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given linkage |
| auth_asym_id_1 | text | Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id_1 | text | Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id_1 | text | Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_1 | text | Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_atom_id_2 | text | Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_asym_id_2 | text | Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_2 | text | Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_2 | text | Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code_1 | text | Optional identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| PDB_ins_code_2 | text | Optional identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id_1 | text | An optional identifier of the first of the two atoms that define the linkage. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| label_alt_id_2 | text | An optional identifier of the second of the two atoms that define the linkage. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| dist | double precision | The value of the polymer linkage for the two atoms defined. |

## pdbx_validate_rmsd_angle

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_rmsd_angle.id must uniquely identify each item in the PDBX_VALIDATE_RMSD_ANGLE list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given angle |
| auth_asym_id_1 | text | Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id_1 | text | Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id_1 | text | Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_1 | text | Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_atom_id_2 | text | Part of the identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_asym_id_2 | text | identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_2 | text | Part of the identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_2 | text | Part of the identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_atom_id_3 | text | Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_asym_id_3 | text | Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_3 | text | Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_3 | text | Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code_1 | text | Optional identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| PDB_ins_code_2 | text | Optional identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| PDB_ins_code_3 | text | Optional identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id_1 | text | An optional identifier of the first of the three atoms that define the covalent angle. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category. |
| label_alt_id_2 | text | An optional identifier of the second of the three atoms that define the covalent angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| label_alt_id_3 | text | An optional identifier of the third of the three atoms that define the covalent angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| angle_deviation | double precision | Value of the deviation (in degrees) from 6*REBI for the angle bounded by the three sites from the expected dictionary value. |
| angle_value | double precision | The value of the bond angle |
| angle_target_value | double precision | The target value of the bond angle |
| angle_standard_deviation | double precision | The uncertainty in the target value of the bond angle expressed as a standard deviation. |
| linker_flag | text | A flag to indicate if the angle is between two residues |

## pdbx_validate_rmsd_bond

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_rmsd_bond.id must uniquely identify each item in the PDBX_VALIDATE_RMSD_BOND list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given bond |
| auth_asym_id_1 | text | Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id_1 | text | Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id_1 | text | Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_1 | text | Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_atom_id_2 | text | Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_asym_id_2 | text | Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_2 | text | Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_2 | text | Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code_1 | text | Optional identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| PDB_ins_code_2 | text | Optional identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id_1 | text | An optional identifier of the first of the two atoms that define the covalent bond. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| label_alt_id_2 | text | An optional identifier of the second of the two atoms that define the covalent bond. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| bond_deviation | double precision | The value of the deviation from ideal for the defined covalent bond for the two atoms defined. |
| bond_value | double precision | The value of the bond length |
| bond_target_value | double precision | The target value of the bond length |
| bond_standard_deviation | double precision | The uncertaintiy in target value of the bond length expressed as a standard deviation. |
| linker_flag | text | A flag to indicate if the bond is between two residues |

## pdbx_validate_symm_contact

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_symm_contact.id must uniquely identify each item in the PDBX_VALIDATE_SYMM_CONTACT list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given angle |
| auth_asym_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_atom_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_comp_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_1 | text | Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| auth_atom_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category. |
| auth_asym_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id_2 | text | Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code_1 | text | Optional identifier of the first of the two atom sites that define the close contact. |
| PDB_ins_code_2 | text | Optional identifier of the second of the two atom sites that define the close contact. |
| label_alt_id_1 | text | An optional identifier of the first of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category. |
| label_alt_id_2 | text | An optional identifier of the second of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| site_symmetry_1 | text | The symmetry of the first of the two atoms define the close contact. Symmetry defined in ORTEP style of 555 equal to unit cell with translations +-1 from 555 as 000 |
| site_symmetry_2 | text | The symmetry of the second of the two atoms define the close contact. Symmetry defined in ORTEP style of 555 equal to unit cell with translations +-1 from 555 as 000 |
| dist | double precision | The value of the close contact for the two atoms defined. |

## pdbx_validate_torsion

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | integer | The value of _pdbx_validate_torsion.id must uniquely identify each item in the PDBX_VALIDATE_TORSION list. This is an integer serial number. |
| PDB_model_num | integer | The model number for the given residue This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category. |
| auth_asym_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | Part of the identifier of the residue This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| PDB_ins_code | text | Optional identifier of the residue This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| label_alt_id | text | Optional identifier of the residue This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| phi | double precision | The Phi value that for the residue that lies outside normal limits (in combination with the Psi value) with regards to the rammachandran plot |
| psi | double precision | The Psi value that for the residue that lies outside normal limits (in combination with the Phi value) with regards to the rammachandran plot |

## pdbx_xplor_file

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| serial_no | text | Serial number. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _pdbx_xplor_file.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| param_file | text | Parameter file name in X-PLOR/CNS refinement. |
| topol_file | text | Topology file name in X-PLOR/CNS refinement. |

## phasing

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| method | text | A listing of the method or methods used to phase this structure. |

## phasing_MAD

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| pdbx_d_res_low | double precision | _phasing_MAD.pdbx_d_res_low records the lowest resolution for MAD phasing. |
| pdbx_d_res_high | double precision | _phasing_MAD.pdbx_d_res_high records the highest resolution for MAD phasing. |
| pdbx_reflns_acentric | integer | _phasing_MAD.pdbx_reflns_acentric records the number of acentric reflections for MAD phasing. |
| pdbx_reflns_centric | integer | _phasing_MAD.pdbx_reflns_centric records the number of centric reflections for MAD phasing. |
| pdbx_reflns | integer | _phasing_MAD.pdbx_reflns records the number of reflections used for MAD phasing. |
| pdbx_fom_acentric | double precision | _phasing_MAD.pdbx_fom_acentric records the figure of merit using acentric data for MAD phasing. |
| pdbx_fom_centric | double precision | _phasing_MAD.pdbx_fom_centric records the figure of merit using centric data for MAD phasing. |
| pdbx_fom | double precision | _phasing_MAD.pdbx_fom records the figure of merit for MAD phasing. |

## phasing_MAD_clust

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| expt_id | text | This data item is a pointer to _phasing_MAD_expt.id in the PHASING_MAD_EXPT category. |
| id | text | The value of _phasing_MAD_clust.id must, together with _phasing_MAD_clust.expt_id, uniquely identify a record in the PHASING_MAD_CLUST list. Note that this item need not be a number; it can be any unique identifier. |

## phasing_MAD_expt

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _phasing_MAD_expt.id must uniquely identify each record in the PHASING_MAD_EXPT list. |
| mean_fom | double precision | The mean figure of merit. |

## phasing_MAD_set

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| clust_id | text | This data item is a pointer to _phasing_MAD_clust.id in the PHASING_MAD_CLUST category. |
| d_res_high | double precision | The lowest value for the interplanar spacings for the reflection data used for this set of data. This is called the highest resolution. |
| d_res_low | double precision | The highest value for the interplanar spacings for the reflection data used for this set of data. This is called the lowest resolution. |
| expt_id | text | This data item is a pointer to _phasing_MAD_expt.id in the PHASING_MAD_EXPT category. |
| f_double_prime | double precision | The f'' component of the anomalous scattering factor for this wavelength. |
| f_prime | double precision | The f' component of the anomalous scattering factor for this wavelength. |
| set_id | text | This data item is a pointer to _phasing_set.id in the PHASING_SET category. |
| wavelength | double precision | The wavelength at which this data set was measured. |
| pdbx_atom_type | text | record the type of heavy atoms which produce anomolous singal. |
| pdbx_f_prime_refined | double precision | record the refined f_prime (not from experiment). |
| pdbx_f_double_prime_refined | double precision | record the refined f_double_prime (not from experiment). |

## phasing_MIR

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the isomorphous-replacement phasing. |
| d_res_high | double precision | The lowest value in angstroms for the interplanar spacings for the reflection data used for the native data set. This is called the highest resolution. |
| d_res_low | double precision | The highest value in angstroms for the interplanar spacings for the reflection data used for the native data set. This is called the lowest resolution. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| FOM | double precision | The mean value of the figure of merit m for all reflections phased in the native data set. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi. |
| FOM_acentric | double precision | The mean value of the figure of merit m for the acentric reflections phased in the native data set. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi. |
| FOM_centric | double precision | The mean value of the figure of merit m for the centric reflections phased in the native data set. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi. |
| reflns | integer | The total number of reflections phased in the native data set. |
| reflns_acentric | integer | The number of acentric reflections phased in the native data set. |
| reflns_centric | integer | The number of centric reflections phased in the native data set. |
| reflns_criterion | text | Criterion used to limit the reflections used in the phasing calculations. |

## phasing_MIR_der

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| d_res_high | double precision | The lowest value for the interplanar spacings for the reflection data used for this derivative. This is called the highest resolution. |
| d_res_low | double precision | The highest value for the interplanar spacings for the reflection data used for this derivative. This is called the lowest resolution. |
| der_set_id | text | The data set that was treated as the derivative in this experiment. This data item is a pointer to _phasing_set.id in the PHASING_SET category. |
| id | text | The value of _phasing_MIR_der.id must uniquely identify a record in the PHASING_MIR_DER list. Note that this item need not be a number; it can be any unique identifier. |
| native_set_id | text | The data set that was treated as the native in this experiment. This data item is a pointer to _phasing_set.id in the PHASING_SET category. |
| number_of_sites | integer | The number of heavy-atom sites in this derivative. |
| power_acentric | double precision | The mean phasing power P for acentric reflections for this derivative. sum\|Fh~calc~^2^\| P = (----------------------------)^1/2^ sum\|Fph~obs~ - Fph~calc~\|^2^ Fph~obs~ = the observed structure-factor amplitude of this derivative Fph~calc~ = the calculated structure-factor amplitude of this derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections |
| power_centric | double precision | The mean phasing power P for centric reflections for this derivative. sum\|Fh~calc~^2^\| P = (----------------------------)^1/2^ sum\|Fph~obs~ - Fph~calc~\|^2^ Fph~obs~ = the observed structure-factor amplitude of the derivative Fph~calc~ = the calculated structure-factor amplitude of the derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections |
| R_cullis_acentric | double precision | Residual factor R~cullis,acen~ for acentric reflections for this derivative. The Cullis R factor was originally defined only for centric reflections. It is, however, also a useful statistical measure for acentric reflections, which is how it is used in this data item. sum\| \|Fph~obs~ +/- Fp~obs~\| - Fh~calc~ \| R~cullis,acen~ = ---------------------------------------- sum\|Fph~obs~ - Fp~obs~\| Fp~obs~ = the observed structure-factor amplitude of the native Fph~obs~ = the observed structure-factor amplitude of the derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections Ref: Cullis, A. F., Muirhead, H., Perutz, M. F., Rossmann, M. G. & North, A. C. T. (1961). Proc. R. Soc. London Ser. A, 265, 15-38. |
| R_cullis_anomalous | double precision | Residual factor R~cullis,ano~ for anomalous reflections for this derivative. The Cullis R factor was originally defined only for centric reflections. It is, however, also a useful statistical measure for anomalous reflections, which is how it is used in this data item. This is tabulated for acentric terms. A value less than 1.0 means there is some contribution to the phasing from the anomalous data. sum \|Fph+~obs~Fph-~obs~ - Fh+~calc~ - Fh-~calc~\| R~cullis,ano~ = ------------------------------------------------ sum\|Fph+~obs~ - Fph-~obs~\| Fph+~obs~ = the observed positive Friedel structure-factor amplitude for the derivative Fph-~obs~ = the observed negative Friedel structure-factor amplitude for the derivative Fh+~calc~ = the calculated positive Friedel structure-factor amplitude from the heavy-atom model Fh-~calc~ = the calculated negative Friedel structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections Ref: Cullis, A. F., Muirhead, H., Perutz, M. F., Rossmann, M. G. & North, A. C. T. (1961). Proc. R. Soc. London Ser. A, 265, 15-38. |
| R_cullis_centric | double precision | Residual factor R~cullis~ for centric reflections for this derivative. sum\| \|Fph~obs~ +/- Fp~obs~\| - Fh~calc~ \| R~cullis~ = ---------------------------------------- sum\|Fph~obs~ - Fp~obs~\| Fp~obs~ = the observed structure-factor amplitude of the native Fph~obs~ = the observed structure-factor amplitude of the derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections Ref: Cullis, A. F., Muirhead, H., Perutz, M. F., Rossmann, M. G. & North, A. C. T. (1961). Proc. R. Soc. London Ser. A, 265, 15-38. |
| reflns_acentric | integer | The number of acentric reflections used in phasing for this derivative. |
| reflns_anomalous | integer | The number of anomalous reflections used in phasing for this derivative. |
| reflns_centric | integer | The number of centric reflections used in phasing for this derivative. |
| reflns_criteria | text | Criteria used to limit the reflections used in the phasing calculations. |
| pdbx_loc_centric | double precision | record lack of closure obtained from centric data for each derivative. |
| pdbx_loc_acentric | double precision | record lack of closure obtained from acentric data for each derivative. |

## phasing_MIR_der_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| d_res_high | double precision | The lowest value for the interplanar spacings for the reflection data for this derivative in this shell. This is called the highest resolution. |
| d_res_low | double precision | The highest value for the interplanar spacings for the reflection data for this derivative in this shell. This is called the lowest resolution. |
| der_id | text | This data item is a pointer to _phasing_MIR_der.id in the PHASING_MIR_DER category. |
| pdbx_R_cullis_centric | double precision | record R Cullis obtained from centric data for each derivative, but broken into resolution shells |
| pdbx_R_cullis_acentric | double precision | record R Cullis obtained from acentric data for each derivative, but broken into resolution shells |
| pdbx_loc_centric | double precision | record lack of closure obtained from centric data for each derivative, but broken into resolution shells |
| pdbx_loc_acentric | double precision | record lack of closure obtained from acentric data for each derivative, but broken into resolution shells |
| pdbx_power_centric | double precision | record phasing power obtained from centric data for each derivative, but broken into resolution shells |
| pdbx_power_acentric | double precision | record phasing power obtained from acentric data for each derivative, but broken into resolution shells |
| pdbx_reflns_centric | double precision | record number of centric reflections used for phasing for each derivative, but broken into resolution shells |
| pdbx_reflns_acentric | integer | record number of acentric reflections used for phasing for each derivative, but broken into resolution shells |

## phasing_MIR_der_site

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| atom_type_symbol | text | This data item is a pointer to _atom_type.symbol in the ATOM_TYPE category. The scattering factors referenced via this data item should be those used in the refinement of the heavy-atom data; in some cases this is the scattering factor for the single heavy atom, in other cases these are the scattering factors for an atomic cluster. |
| B_iso | double precision | Isotropic displacement parameter for this heavy-atom site in this derivative. |
| Cartn_x | double precision | The x coordinate of this heavy-atom position in this derivative specified as orthogonal angstroms. The orthogonal Cartesian axes are related to the cell axes as specified by the description given in _atom_sites.Cartn_transform_axes. |
| Cartn_y | double precision | The y coordinate of this heavy-atom position in this derivative specified as orthogonal angstroms. The orthogonal Cartesian axes are related to the cell axes as specified by the description given in _atom_sites.Cartn_transform_axes. |
| Cartn_z | double precision | The z coordinate of this heavy-atom position in this derivative specified as orthogonal angstroms. The orthogonal Cartesian axes are related to the cell axes as specified by the description given in _atom_sites.Cartn_transform_axes. |
| der_id | text | This data item is a pointer to _phasing_MIR_der.id in the PHASING_MIR_DER category. |
| fract_x | double precision | The x coordinate of this heavy-atom position in this derivative specified as a fraction of _cell.length_a. |
| fract_y | double precision | The y coordinate of this heavy-atom position in this derivative specified as a fraction of _cell.length_b. |
| fract_z | double precision | The z coordinate of this heavy-atom position in this derivative specified as a fraction of _cell.length_c. |
| id | text | The value of _phasing_MIR_der_site.id must uniquely identify each site in each derivative in the PHASING_MIR_DER_SITE list. The atom identifiers need not be unique over all sites in all derivatives; they need only be unique for each site in each derivative. Note that this item need not be a number; it can be any unique identifier. |
| occupancy | double precision | The fraction of the atom type present at this heavy-atom site in a given derivative. The sum of the occupancies of all the atom types at this site may not significantly exceed 1.0 unless it is a dummy site. |
| occupancy_anom | double precision | The relative anomalous occupancy of the atom type present at this heavy-atom site in a given derivative. This atom occupancy will probably be on an arbitrary scale. |
| occupancy_anom_su | double precision | The standard uncertainty (estimated standard deviation) of _phasing_MIR_der_site.occupancy_anom. |
| occupancy_iso | double precision | The relative real isotropic occupancy of the atom type present at this heavy-atom site in a given derivative. This atom occupancy will probably be on an arbitrary scale. |
| occupancy_iso_su | double precision | The standard uncertainty (estimated standard deviation) of _phasing_MIR_der_site.occupancy_iso. |

## phasing_MIR_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| d_res_high | double precision | The lowest value for the interplanar spacings for the reflection data in this shell. This is called the highest resolution. Note that the resolution limits of shells in the items _phasing_MIR_shell.d_res_high and _phasing_MIR_shell.d_res_low are independent of the resolution limits of shells in the items _reflns_shell.d_res_high and _reflns_shell.d_res_low. |
| d_res_low | double precision | The highest value for the interplanar spacings for the reflection data in this shell. This is called the lowest resolution. Note that the resolution limits of shells in the items _phasing_MIR_shell.d_res_high and _phasing_MIR_shell.d_res_low are independent of the resolution limits of shells in the items _reflns_shell.d_res_high and _reflns_shell.d_res_low. |
| FOM | double precision | The mean value of the figure of merit m for reflections in this shell. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~alpha~ = the probability that the phase angle alpha is correct the integral is taken over the range alpha = 0 to 2 pi. |
| FOM_acentric | double precision | The mean value of the figure of merit m for acentric reflections in this shell. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi. |
| FOM_centric | double precision | The mean value of the figure of merit m for centric reflections in this shell. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi. |
| reflns | integer | The number of reflections in this shell. |
| reflns_acentric | integer | The number of acentric reflections in this shell. |
| reflns_centric | integer | The number of centric reflections in this shell. |

## phasing_set

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| cell_angle_alpha | double precision | Unit-cell angle alpha for this data set in degrees. |
| cell_angle_beta | double precision | Unit-cell angle beta for this data set in degrees. |
| cell_angle_gamma | double precision | Unit-cell angle gamma for this data set in degrees. |
| cell_length_a | double precision | Unit-cell length a for this data set in angstroms. |
| cell_length_b | double precision | Unit-cell length b for this data set in angstroms. |
| cell_length_c | double precision | Unit-cell length c for this data set in angstroms. |
| id | text | The value of _phasing_set.id must uniquely identify a record in the PHASING_SET list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_d_res_high | double precision | The smallest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the highest resolution. |
| pdbx_d_res_low | double precision | The highest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the lowest resolution. |

## publ

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| section_references | text | The references section of a manuscript if the manuscript is submitted in parts. As an alternative see _publ.manuscript_text and _publ.manuscript_processed. |

## refine

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| aniso_B11 | double precision |  |
| aniso_B12 | double precision |  |
| aniso_B13 | double precision |  |
| aniso_B22 | double precision |  |
| aniso_B23 | double precision |  |
| aniso_B33 | double precision |  |
| B_iso_max | double precision | The maximum isotropic displacement parameter (B value) found in the coordinate set. |
| B_iso_mean | double precision | The mean isotropic displacement parameter (B value) for the coordinate set. |
| B_iso_min | double precision | The minimum isotropic displacement parameter (B value) found in the coordinate set. |
| correlation_coeff_Fo_to_Fc | double precision | The correlation coefficient between the observed and calculated structure factors for reflections included in the refinement. The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections included in the refinement |
| correlation_coeff_Fo_to_Fc_free | double precision | The correlation coefficient between the observed and calculated structure factors for reflections not included in the refinement (free reflections). The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections not included in the refinement (free reflections) |
| details | text | Description of special aspects of the refinement process. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| ls_d_res_high | double precision | The smallest value for the interplanar spacings for the reflection data used in the refinement in angstroms. This is called the highest resolution. |
| ls_d_res_low | double precision | The largest value for the interplanar spacings for the reflection data used in the refinement in angstroms. This is called the lowest resolution. |
| ls_extinction_coef_esd | double precision | The standard uncertainty (estimated standard deviation) of _refine.ls_extinction_coef. |
| ls_goodness_of_fit_all | double precision | The least-squares goodness-of-fit parameter S for all data after the final cycle of refinement. Ideally, account should be taken of parameters restrained in the least-squares refinement. See also the definition of _refine.ls_restrained_S_all. ( sum\|w \|Y~obs~ - Y~calc~\|^2^\| )^1/2^ S = ( ---------------------------- ) ( N~ref~ - N~param~ ) Y~obs~ = the observed coefficients (see _refine.ls_structure_factor_coef) Y~calc~ = the calculated coefficients (see _refine.ls_structure_factor_coef) w = the least-squares reflection weight [1/(e.s.d. squared)] N~ref~ = the number of reflections used in the refinement N~param~ = the number of refined parameters sum is taken over the specified reflections |
| ls_hydrogen_treatment | text | Treatment of hydrogen atoms in the least-squares refinement. |
| ls_matrix_type | text | Type of matrix used to accumulate the least-squares derivatives. |
| ls_number_constraints | integer | The number of constrained (non-refined or dependent) parameters in the least-squares process. These may be due to symmetry or any other constraint process (e.g. rigid-body refinement). See also _atom_site.constraints and _atom_site.refinement_flags. A general description of constraints may appear in _refine.details. |
| ls_number_parameters | integer | The number of parameters refined in the least-squares process. If possible, this number should include some contribution from the restrained parameters. The restrained parameters are distinct from the constrained parameters (where one or more parameters are linearly dependent on the refined value of another). Least-squares restraints often depend on geometry or energy considerations and this makes their direct contribution to this number, and to the goodness-of-fit calculation, difficult to assess. |
| ls_number_reflns_all | integer | The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low. |
| ls_number_reflns_obs | integer | The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion. |
| ls_number_reflns_R_free | integer | The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. |
| ls_number_reflns_R_work | integer | The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. |
| ls_number_restraints | integer | The number of restrained parameters. These are parameters which are not directly dependent on another refined parameter. Restrained parameters often involve geometry or energy dependencies. See also _atom_site.constraints and _atom_site.refinement_flags. A general description of refinement constraints may appear in _refine.details. |
| ls_percent_reflns_obs | double precision | The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, expressed as a percentage of the number of geometrically observable reflections that satisfy the resolution limits. |
| ls_percent_reflns_R_free | double precision | The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor, expressed as a percentage of the number of geometrically observable reflections that satisfy the resolution limits. |
| ls_R_factor_all | double precision | Residual factor R for all reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| ls_R_factor_obs | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion. _refine.ls_R_factor_obs should not be confused with _refine.ls_R_factor_R_work; the former reports the results of a refinement in which all observed reflections were used, the latter a refinement in which a subset of the observed reflections were excluded from refinement for the calculation of a 'free' R factor. However, it would be meaningful to quote both values if a 'free' R factor were calculated for most of the refinement, but all of the observed reflections were used in the final rounds of refinement; such a protocol should be explained in _refine.details. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| ls_R_factor_R_free | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| ls_R_factor_R_free_error | double precision | The estimated error in _refine.ls_R_factor_R_free. The method used to estimate the error is described in the item _refine.ls_R_factor_R_free_error_details. |
| ls_R_factor_R_free_error_details | text | Special aspects of the method used to estimated the error in _refine.ls_R_factor_R_free. |
| ls_R_factor_R_work | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. _refine.ls_R_factor_obs should not be confused with _refine.ls_R_factor_R_work; the former reports the results of a refinement in which all observed reflections were used, the latter a refinement in which a subset of the observed reflections were excluded from refinement for the calculation of a 'free' R factor. However, it would be meaningful to quote both values if a 'free' R factor were calculated for most of the refinement, but all of the observed reflections were used in the final rounds of refinement; such a protocol should be explained in _refine.details. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| ls_redundancy_reflns_all | double precision | The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low to the number of crystallographically unique reflections that satisfy the same limits. |
| ls_redundancy_reflns_obs | double precision | The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion to the number of crystallographically unique reflections that satisfy the same limits. |
| ls_wR_factor_all | double precision | Weighted residual factor wR for all reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low. ( sum\|w \|Y~obs~ - Y~calc~\|^2^\| )^1/2^ wR = ( ---------------------------- ) ( sum\|w Y~obs~^2^\| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections |
| ls_wR_factor_R_free | double precision | Weighted residual factor wR for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. ( sum\|w \|Y~obs~ - Y~calc~\|^2^\| )^1/2^ wR = ( ---------------------------- ) ( sum\|w Y~obs~^2^\| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections |
| ls_wR_factor_R_work | double precision | Weighted residual factor wR for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. ( sum\|w \|Y~obs~ - Y~calc~\|^2^\| )^1/2^ wR = ( ---------------------------- ) ( sum\|w Y~obs~^2^\| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections |
| occupancy_max | double precision | The maximum value for occupancy found in the coordinate set. |
| occupancy_min | double precision | The minimum value for occupancy found in the coordinate set. |
| solvent_model_details | text | Special aspects of the solvent model used during refinement. |
| solvent_model_param_bsol | double precision | The value of the BSOL solvent-model parameter describing the average isotropic displacement parameter of disordered solvent atoms. This is one of the two parameters (the other is _refine.solvent_model_param_ksol) in Tronrud's method of modelling the contribution of bulk solvent to the scattering. The standard scale factor is modified according to the expression k0 exp(-B0 * s^2^)[1-KSOL * exp(-BSOL * s^2^)] where k0 and B0 are the scale factors for the protein. Ref: Tronrud, D. E. (1997). Methods Enzymol. 277, 243-268. |
| solvent_model_param_ksol | double precision | The value of the KSOL solvent-model parameter describing the ratio of the electron density in the bulk solvent to the electron density in the molecular solute. This is one of the two parameters (the other is _refine.solvent_model_param_bsol) in Tronrud's method of modelling the contribution of bulk solvent to the scattering. The standard scale factor is modified according to the expression k0 exp(-B0 * s^2^)[1-KSOL * exp(-BSOL * s^2^)] where k0 and B0 are the scale factors for the protein. Ref: Tronrud, D. E. (1997). Methods Enzymol. 277, 243-268. |
| pdbx_ls_sigma_I | double precision | Data cutoff (SIGMA(I)) |
| pdbx_ls_sigma_F | double precision | Data cutoff (SIGMA(F)) |
| pdbx_ls_sigma_Fsqd | double precision | Data cutoff (SIGMA(F^2)) |
| pdbx_data_cutoff_high_absF | double precision | Value of F at "high end" of data cutoff. |
| pdbx_data_cutoff_high_rms_absF | double precision | Value of RMS \|F\| used as high data cutoff. |
| pdbx_data_cutoff_low_absF | double precision | Value of F at "low end" of data cutoff. |
| pdbx_isotropic_thermal_model | text | Whether the structure was refined with indvidual isotropic, anisotropic or overall temperature factor. |
| pdbx_ls_cross_valid_method | text | Whether the cross validataion method was used through out or only at the end. |
| pdbx_method_to_determine_struct | text | Method(s) used to determine the structure. |
| pdbx_starting_model | text | Starting model for refinement. Starting model for molecular replacement should refer to a previous structure or experiment. |
| pdbx_stereochemistry_target_values | text | Stereochemistry target values used in refinement. |
| pdbx_R_Free_selection_details | text | Details of the manner in which the cross validation reflections were selected. |
| pdbx_stereochem_target_val_spec_case | text | Special case of stereochemistry target values used in SHELXL refinement. |
| pdbx_overall_ESU_R | double precision | Overall estimated standard uncertainties of positional parameters based on R value. |
| pdbx_overall_ESU_R_Free | double precision | Overall estimated standard uncertainties of positional parameters based on R free value. |
| pdbx_solvent_vdw_probe_radii | double precision | For bulk solvent mask calculation, the value by which the vdw radii of non-ion atoms (like carbon) are increased and used. |
| pdbx_solvent_ion_probe_radii | double precision | For bulk solvent mask calculation, the amount that the ionic radii of atoms, which can be ions, are increased used. |
| pdbx_solvent_shrinkage_radii | double precision | For bulk solvent mask calculation, amount mask is shrunk after taking away atoms with new radii and a constant value assigned to this new region. |
| pdbx_pd_number_of_powder_patterns | integer | The total number of powder patterns used. |
| pdbx_pd_number_of_points | integer | The total number of data points in the processed diffractogram. |
| pdbx_pd_Marquardt_correlation_coeff | double precision | The correlation coefficient between the observed and calculated structure factors for reflections included in the refinement. This correlation factor is found in the fitting using the Levenberg-Marquardt algorithm to search for the minimum value of chisquare. Almost all computer codes for Rietveld refinement employ the Gauss-Newton algorithm to find parameters which minimize the weighted sum of squares of the residuals. A description of the equations is given on http://www.water.hut.fi/~tkarvone/fr_org_s.htm |
| pdbx_pd_ls_matrix_band_width | integer | The least squares refinement "band matrix" approximation to the full matrix. |
| pdbx_overall_phase_error | double precision | The overall phase error for all reflections after refinement using the current refinement target. |
| pdbx_overall_SU_R_free_Cruickshank_DPI | double precision | The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R-free value, expressed in a formalism known as the dispersion precision indicator (DPI). Ref: Cruickshank, D. W. J. (1999). Acta Cryst. D55, 583-601. |
| pdbx_overall_SU_R_free_Blow_DPI | double precision | The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R-free value, expressed in a formalism known as the dispersion precision indicator (DPI). Ref: Blow, D (2002) Acta Cryst. D58, 792-797 |
| pdbx_overall_SU_R_Blow_DPI | double precision | The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R value, expressed in a formalism known as the dispersion precision indicator (DPI). Ref: Blow, D (2002) Acta Cryst. D58, 792-797 |
| pdbx_TLS_residual_ADP_flag | text | A flag for TLS refinements identifying the type of atomic displacement parameters stored in _atom_site.B_iso_or_equiv. |
| pdbx_diffrn_id | text | An identifier for the diffraction data set used in this refinement. Multiple diffraction data sets specified as a comma separated list. |
| overall_SU_B | double precision | The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on a maximum-likelihood residual. The overall standard uncertainty (sigma~B~)^2^ gives an idea of the uncertainty in the B values of averagely defined atoms (atoms with B values equal to the average B value). N~a~ (sigma~B~)^2^ = 8 ---------------------------------------------- sum~i~ {[1/Sigma - (E~o~)^2^ (1-m^2^)](SUM_AS)s^4^} N~a~ = number of atoms E~o~ = normalized structure factors m = figure of merit of phases of reflections included in the summation s = reciprocal-space vector SUM_AS = (sigma~A~)^2^/Sigma^2^ Sigma = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = experimental uncertainties of normalized structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = atom form factor delta~x~ = expected error epsilon = multiplicity of diffracting plane summation is over all reflections included in refinement Ref: (sigma~A~ estimation) "Refinement of macromolecular structures by the maximum-likelihood method", Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255. (SU B estimation) Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html |
| overall_SU_ML | double precision | The overall standard uncertainty (estimated standard deviation) of the positional parameters based on a maximum likelihood residual. The overall standard uncertainty (sigma~X~)^2^ gives an idea of the uncertainty in the position of averagely defined atoms (atoms with B values equal to average B value) 3 N~a~ (sigma~X~)^2^ = --------------------------------------------------------- 8 pi^2^ sum~i~ {[1/Sigma - (E~o~)^2^ (1-m^2^)](SUM_AS)s^2^} N~a~ = number of atoms E~o~ = normalized structure factors m = figure of merit of phases of reflections included in the summation s = reciprocal-space vector SUM_AS = (sigma~A~)^2^/Sigma^2^ Sigma = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = experimental uncertainties of normalized structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = atom form factor delta~x~ = expected error epsilon = multiplicity of diffracting plane summation is over all reflections included in refinement Ref: (sigma_A estimation) "Refinement of macromolecular structures by the maximum-likelihood method", Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255. (SU ML estimation) Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html |
| overall_SU_R_Cruickshank_DPI | double precision | The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R value, expressed in a formalism known as the dispersion precision indicator (DPI). The overall standard uncertainty (sigma~B~) gives an idea of the uncertainty in the B values of averagely defined atoms (atoms with B values equal to the average B value). N~a~ (sigma~B~)^2^ = 0.65 ---------- (R~value~)^2^ (D~min~)^2^ C^-2/3^ (N~o~-N~p~) N~a~ = number of atoms included in refinement N~o~ = number of observations N~p~ = number of parameters refined R~value~ = conventional crystallographic R value D~min~ = maximum resolution C = completeness of data Ref: Cruickshank, D. W. J. (1999). Acta Cryst. D55, 583-601. Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html |
| overall_SU_R_free | double precision | The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the free R value. The overall standard uncertainty (sigma~B~) gives an idea of the uncertainty in the B values of averagely defined atoms (atoms with B values equal to the average B value). N~a~ (sigma~B~)^2^ = 0.65 ---------- (R~free~)^2^ (D~min~)^2^ C^-2/3^ (N~o~-N~p~) N~a~ = number of atoms included in refinement N~o~ = number of observations N~p~ = number of parameters refined R~free~ = conventional free crystallographic R value calculated using reflections not included in refinement D~min~ = maximum resolution C = completeness of data Ref: Cruickshank, D. W. J. (1999). Acta Cryst. D55, 583-601. Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html |
| overall_FOM_free_R_set | double precision | Average figure of merit of phases of reflections not included in the refinement. This value is derived from the likelihood function. FOM = I~1~(X)/I~0~(X) I~0~, I~1~ = zero- and first-order modified Bessel functions of the first kind X = sigma~A~ \|E~o~\| \|E~c~\|/SIGMA E~o~, E~c~ = normalized observed and calculated structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = form factor of atoms delta~x~ = expected error SIGMA = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = uncertainties of normalized observed structure factors epsilon = multiplicity of the diffracting plane Ref: Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255. |
| overall_FOM_work_R_set | double precision | Average figure of merit of phases of reflections included in the refinement. This value is derived from the likelihood function. FOM = I~1~(X)/I~0~(X) I~0~, I~1~ = zero- and first-order modified Bessel functions of the first kind X = sigma~A~ \|E~o~\| \|E~c~\|/SIGMA E~o~, E~c~ = normalized observed and calculated structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = form factor of atoms delta~x~ = expected error SIGMA = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = uncertainties of normalized observed structure factors epsilon = multiplicity of the diffracting plane Ref: Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255. |
| pdbx_average_fsc_overall | double precision | Overall average Fourier Shell Correlation (avgFSC) between model and observed structure factors for all reflections. The average FSC is a measure of the agreement between observed and calculated structure factors. sum(N~i~ FSC~i~) avgFSC = ---------------- sum(N~i~) N~i~ = the number of all reflections in the resolution shell i FSC~i~ = FSC for all reflections in the i-th resolution shell calculated as: (sum(\|F~o~\| \|F~c~\| fom cos(phi~c~-phi~o~))) FSC~i~ = ------------------------------------------- (sum(\|F~o~\|^2^) (sum(\|F~c~\|^2^)))^1/2^ \|F~o~\| = amplitude of observed structure factor \|F~c~\| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation of FSC~i~ is carried over all reflections in the resolution shell. Summation of avgFSC is carried over all resolution shells. Ref: Rosenthal P.B., Henderson R. "Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6). |
| pdbx_average_fsc_work | double precision | Average Fourier Shell Correlation (avgFSC) between model and observed structure factors for reflections included in refinement. The average FSC is a measure of the agreement between observed and calculated structure factors. sum(N~i~ FSC~work-i~) avgFSC~work~ = --------------------- sum(N~i~) N~i~ = the number of working reflections in the resolution shell i FSC~work-i~ = FSC for working reflections in the i-th resolution shell calculated as: (sum(\|F~o~\| \|F~c~\| fom cos(phi~c~-phi~o~))) FSC~work-i~ = ------------------------------------------- (sum(\|F~o~\|^2^) (sum(\|F~c~\|^2^)))^1/2^ \|F~o~\| = amplitude of observed structure factor \|F~c~\| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation of FSC~work-i~ is carried over all working reflections in the resolution shell. Summation of avgFSC~work~ is carried over all resolution shells. Ref: Rosenthal P.B., Henderson R. "Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6). |
| pdbx_average_fsc_free | double precision | Average Fourier Shell Correlation (avgFSC) between model and observed structure factors for reflections not included in refinement. The average FSC is a measure of the agreement between observed and calculated structure factors. sum(N~i~ FSC~free-i~) avgFSC~free~ = --------------------- sum(N~i~) N~i~ = the number of free reflections in the resolution shell i FSC~free-i~ = FSC for free reflections in the i-th resolution shell calculated as: (sum(\|F~o~\| \|F~c~\| fom cos(phi~c~-phi~o~))) FSC~free-i~ = ------------------------------------------- (sum(\|F~o~\|^2^) (sum(\|F~c~\|^2^)))^1/2^ \|F~o~\| = amplitude of observed structure factor \|F~c~\| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation of FSC~free-i~ is carried over all free reflections in the resolution shell. Summation of avgFSC~free~ is carried over all resolution shells. Ref: Rosenthal P.B., Henderson R. "Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6). |

## refine_B_iso

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_B_iso.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| class | text | A class of atoms treated similarly for isotropic B-factor (displacement-parameter) refinement. |
| details | text | A description of special aspects of the isotropic B-factor (displacement-parameter) refinement for the class of atoms described in _refine_B_iso.class. |
| treatment | text | The treatment of isotropic B-factor (displacement-parameter) refinement for a class of atoms defined in _refine_B_iso.class. |

## refine_analyze

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_analyze.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| Luzzati_coordinate_error_free | double precision | The estimated coordinate error obtained from the plot of the R value versus sin(theta)/lambda for the reflections treated as a test set during refinement. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810. |
| Luzzati_coordinate_error_obs | double precision | The estimated coordinate error obtained from the plot of the R value versus sin(theta)/lambda for reflections classified as observed. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810. |
| Luzzati_d_res_low_free | double precision | The value of the low-resolution cutoff used in constructing the Luzzati plot for reflections treated as a test set during refinement. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810. |
| Luzzati_d_res_low_obs | double precision | The value of the low-resolution cutoff used in constructing the Luzzati plot for reflections classified as observed. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810. |
| Luzzati_sigma_a_free | double precision | The value of sigma~a~ used in constructing the Luzzati plot for the reflections treated as a test set during refinement. Details of the estimation of sigma~a~ can be specified in _refine_analyze.Luzzati_sigma_a_free_details. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810. |
| Luzzati_sigma_a_obs | double precision | The value of sigma~a~ used in constructing the Luzzati plot for reflections classified as observed. Details of the estimation of sigma~a~ can be specified in _refine_analyze.Luzzati_sigma_a_obs_details. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810. |
| number_disordered_residues | double precision | The number of discretely disordered residues in the refined model. |
| occupancy_sum_hydrogen | double precision | The sum of the occupancies of the hydrogen atoms in the refined model. |
| occupancy_sum_non_hydrogen | double precision | The sum of the occupancies of the non-hydrogen atoms in the refined model. |
| pdbx_Luzzati_d_res_high_obs | double precision | record the high resolution for calculating Luzzati statistics. |

## refine_funct_minimized

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_funct_minimized.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| type | text | The type of the function being minimized. |

## refine_hist

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_hist.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| cycle_id | text | The value of _refine_hist.cycle_id must uniquely identify a record in the REFINE_HIST list. Note that this item need not be a number; it can be any unique identifier. |
| details | text | A description of special aspects of this cycle of the refinement process. |
| d_res_high | double precision | The lowest value for the interplanar spacings for the reflection data for this cycle of refinement. This is called the highest resolution. |
| d_res_low | double precision | The highest value for the interplanar spacings for the reflection data for this cycle of refinement. This is called the lowest resolution. |
| number_atoms_solvent | integer | The number of solvent atoms that were included in the model at this cycle of the refinement. |
| number_atoms_total | integer | The total number of atoms that were included in the model at this cycle of the refinement. |
| pdbx_number_residues_total | integer | Total number of polymer residues included in refinement. |
| pdbx_B_iso_mean_ligand | double precision | Mean isotropic B-value for ligand molecules included in refinement. |
| pdbx_B_iso_mean_solvent | double precision | Mean isotropic B-value for solvent molecules included in refinement. |
| pdbx_number_atoms_protein | integer | Number of protein atoms included in refinement |
| pdbx_number_atoms_nucleic_acid | integer | Number of nucleic atoms included in refinement |
| pdbx_number_atoms_ligand | integer | Number of ligand atoms included in refinement |

## refine_ls_restr

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_ls_restr.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| dev_ideal | double precision | For the given parameter type, the root-mean-square deviation between the ideal values used as restraints in the least-squares refinement and the values obtained by refinement. For instance, bond distances may deviate by 0.018 \%A (r.m.s.) from ideal values in the current model. |
| dev_ideal_target | double precision | For the given parameter type, the target root-mean-square deviation between the ideal values used as restraints in the least-squares refinement and the values obtained by refinement. |
| number | integer | The number of parameters of this type subjected to restraint in least-squares refinement. |
| type | text | The type of the parameter being restrained. Explicit sets of data values are provided for the programs PROTIN/PROLSQ (beginning with p_) and RESTRAIN (beginning with RESTRAIN_). As computer programs change, these data values are given as examples, not as an enumeration list. Computer programs that convert a data block to a refinement table will expect the exact form of the data values given here to be used. |
| weight | double precision | The weighting value applied to this type of restraint in the least-squares refinement. |
| pdbx_restraint_function | text | The functional form of the restraint function used in the least-squares refinement. |

## refine_ls_restr_ncs

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_ls_restr_ncs.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| dom_id | text | This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category. |
| ncs_model_details | text | Special aspects of the manner in which noncrystallographic restraints were applied to atomic parameters in the domain specified by _refine_ls_restr_ncs.dom_id and equivalent atomic parameters in the domains against which it was restrained. |
| rms_dev_B_iso | double precision | The root-mean-square deviation in equivalent isotropic displacement parameters in the domain specified by _refine_ls_restr_ncs.dom_id and in the domains against which it was restrained. |
| rms_dev_position | double precision | The root-mean-square deviation in equivalent atom positions in the domain specified by _refine_ls_restr_ncs.dom_id and in the domains against which it was restrained. |
| weight_B_iso | double precision | The value of the weighting coefficient used in noncrystallographic symmetry restraint of isotropic displacement parameters in the domain specified by _refine_ls_restr_ncs.dom_id to equivalent isotropic displacement parameters in the domains against which it was restrained. |
| weight_position | double precision | The value of the weighting coefficient used in noncrystallographic symmetry restraint of atom positions in the domain specified by _refine_ls_restr_ncs.dom_id to equivalent atom positions in the domains against which it was restrained. |
| pdbx_ordinal | integer | An ordinal index for the list of NCS restraints. |
| pdbx_type | text | The type of NCS restraint. (for example: tight positional) |
| pdbx_asym_id | text | A reference to _struct_asym.id. |
| pdbx_auth_asym_id | text | A reference to the PDB Chain ID |
| pdbx_number | integer | Records the number restraints in the contributing to the RMS statistic. |
| pdbx_rms | double precision | Records the standard deviation in the restraint between NCS related domains. |
| pdbx_weight | double precision | Records the weight used for NCS restraint. |
| pdbx_ens_id | text | This is a unique identifier for a collection NCS related domains. This references item '_struct_ncs_dom.pdbx_ens_id'. |

## refine_ls_restr_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text |  |
| type | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| dev_ideal | double precision |  |
| dev_ideal_target | double precision |  |
| weight | double precision |  |

## refine_ls_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_ls_shell.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| d_res_high | double precision | The lowest value for the interplanar spacings for the reflection data in this shell. This is called the highest resolution. |
| d_res_low | double precision | The highest value for the interplanar spacings for the reflection data in this shell. This is called the lowest resolution. |
| number_reflns_all | integer | The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low. |
| number_reflns_obs | integer | The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion. |
| number_reflns_R_free | integer | The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. |
| number_reflns_R_work | integer | The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. |
| percent_reflns_obs | double precision | The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion, expressed as a percentage of the number of geometrically observable reflections that satisfy the resolution limits. |
| percent_reflns_R_free | double precision | The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor, expressed as a percentage of the number of geometrically observable reflections that satisfy the reflection limits. |
| R_factor_all | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| R_factor_obs | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| R_factor_R_free_error | double precision | The estimated error in _refine_ls_shell.R_factor_R_free. The method used to estimate the error is described in the item _refine.ls_R_factor_R_free_error_details. |
| R_factor_R_work | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |
| redundancy_reflns_all | double precision | The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low to the number of crystallographically unique reflections that satisfy the same limits. |
| redundancy_reflns_obs | double precision | The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion to the number of crystallographically unique reflections that satisfy the same limits. |
| wR_factor_R_work | double precision | Weighted residual factor wR for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. ( sum\|w \|Y~obs~ - Y~calc~\|^2^\| )^1/2^ wR = ( ---------------------------- ) ( sum\|w Y~obs~^2^\| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections |
| pdbx_R_complete | double precision | The crystallographic reliability index Rcomplete for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion Ref: Luebben, J., Gruene, T., (2015). Proc.Nat.Acad.Sci. 112(29) 8999-9003 |
| correlation_coeff_Fo_to_Fc | double precision | The correlation coefficient between the observed and calculated structure factors for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low included in the refinement. The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections included in the refinement |
| correlation_coeff_Fo_to_Fc_free | double precision | The correlation coefficient between the observed and calculated structure factors for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low not included in the refinement (free reflections). The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections not included in the refinement (free reflections) |
| pdbx_total_number_of_bins_used | integer | Total number of bins used. |
| pdbx_phase_error | double precision | The average phase error for all reflections in the resolution shell. |
| pdbx_fsc_work | double precision | Fourier Shell Correlation (FSC) between model and observed structure factors for reflections included in refinement. FSC is a measure of the agreement between observed and calculated structure factors as complex numbers. (sum(\|F~o~\| \|F~c~\| fom cos(phi~c~-phi~o~))) FSC~work~ = -------------------------------------- (sum(\|F~o~\|^2^) (sum(\|F~c~\|^2^)))^1/2^ \|F~o~\| = amplitude of observed structure factor \|F~c~\| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation is carried over all working reflections in the resolution shell. Ref: Rosenthal P.B., Henderson R. "Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6). |
| pdbx_fsc_free | double precision | Fourier Shell Correlation (FSC) between model and observed structure factors for reflections not included in refinement. FSC is a measure of the agreement between observed and calculated structure factors as complex numbers. (sum(\|F~o~\| \|F~c~\| fom cos(phi~c~-phi~o~))) FSC~free~ = -------------------------------------- (sum(\|F~o~\|^2^) (sum(\|F~c~\|^2^)))^1/2^ \|F~o~\| = amplitude of observed structure factor \|F~c~\| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation is carried over all free reflections in the resolution shell. Ref: Rosenthal P.B., Henderson R. "Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6). |
| R_factor_R_free | double precision | Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. sum\|F~obs~ - F~calc~\| R = --------------------- sum\|F~obs~\| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections |

## refine_occupancy

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_refine_id | text | This data item uniquely identifies a refinement within an entry. _refine_occupancy.pdbx_refine_id can be used to distinguish the results of joint refinements. |
| class | text | The class of atoms treated similarly for occupancy refinement. |
| treatment | text | The treatment of occupancies for a class of atoms described in _refine_occupancy.class. |

## refine_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text |  |
| pdbx_refine_id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| B_iso_mean | double precision |  |
| ls_R_factor_R_free | double precision |  |
| ls_R_factor_R_work | double precision |  |
| ls_R_factor_all | double precision |  |
| ls_R_factor_obs | double precision |  |
| ls_d_res_high | double precision |  |
| ls_d_res_low | double precision |  |
| ls_number_reflns_R_free | double precision |  |
| ls_number_reflns_all | integer |  |
| ls_number_reflns_obs | integer |  |
| ls_percent_reflns_R_free | text |  |
| pdbx_ls_sigma_F | double precision |  |
| pdbx_ls_sigma_I | double precision |  |

## refln_sys_abs

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| I | double precision | The measured value of the intensity in arbitrary units. |
| I_over_sigmaI | double precision | The ratio of _refln_sys_abs.I to _refln_sys_abs.sigmaI. Used to evaluate whether a reflection that should be systematically absent according to the designated space group is in fact absent. |
| index_h | integer | Miller index h of the reflection. The values of the Miller indices in the REFLN_SYS_ABS category must correspond to the cell defined by cell lengths and cell angles in the CELL category. |
| index_k | integer | Miller index k of the reflection. The values of the Miller indices in the REFLN_SYS_ABS category must correspond to the cell defined by cell lengths and cell angles in the CELL category. |
| index_l | integer | Miller index l of the reflection. The values of the Miller indices in the REFLN_SYS_ABS category must correspond to the cell defined by cell lengths and cell angles in the CELL category. |
| sigmaI | double precision | The standard uncertainty (estimated standard deviation) of _refln_sys_abs.I in arbitrary units. |

## reflns

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| B_iso_Wilson_estimate | double precision | The value of the overall isotropic displacement parameter estimated from the slope of the Wilson plot. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| data_reduction_details | text | A description of special aspects of the data-reduction procedures. |
| data_reduction_method | text | The method used for data reduction. Note that this is not the computer program used, which is described in the SOFTWARE category, but the method itself. This data item should be used to describe significant methodological options used within the data-reduction programs. |
| d_resolution_high | double precision | The smallest value in angstroms for the interplanar spacings for the reflection data. This is called the highest resolution. |
| d_resolution_low | double precision | The largest value in angstroms for the interplanar spacings for the reflection data. This is called the lowest resolution. |
| details | text | A description of reflection data not covered by other data names. This should include details of the Friedel pairs. |
| limit_h_max | integer | Maximum value of the Miller index h for the reflection data. This need not have the same value as _diffrn_reflns.limit_h_max. |
| limit_h_min | integer | Minimum value of the Miller index h for the reflection data. This need not have the same value as _diffrn_reflns.limit_h_min. |
| limit_k_max | integer | Maximum value of the Miller index k for the reflection data. This need not have the same value as _diffrn_reflns.limit_k_max. |
| limit_k_min | integer | Minimum value of the Miller index k for the reflection data. This need not have the same value as _diffrn_reflns.limit_k_min. |
| limit_l_max | integer | Maximum value of the Miller index l for the reflection data. This need not have the same value as _diffrn_reflns.limit_l_max. |
| limit_l_min | integer | Minimum value of the Miller index l for the reflection data. This need not have the same value as _diffrn_reflns.limit_l_min. |
| number_all | integer | The total number of reflections in the REFLN list (not the DIFFRN_REFLN list). This number may contain Friedel-equivalent reflections according to the nature of the structure and the procedures used. The item _reflns.details describes the reflection data. |
| number_obs | integer | The number of reflections in the REFLN list (not the DIFFRN_REFLN list) classified as observed (see _reflns.observed_criterion). This number may contain Friedel-equivalent reflections according to the nature of the structure and the procedures used. |
| observed_criterion_F_max | double precision | The criterion used to classify a reflection as 'observed' expressed as an upper limit for the value of F. |
| observed_criterion_F_min | double precision | The criterion used to classify a reflection as 'observed' expressed as a lower limit for the value of F. |
| observed_criterion_I_max | double precision | The criterion used to classify a reflection as 'observed' expressed as an upper limit for the value of I. |
| observed_criterion_I_min | double precision | The criterion used to classify a reflection as 'observed' expressed as a lower limit for the value of I. |
| observed_criterion_sigma_F | double precision | The criterion used to classify a reflection as 'observed' expressed as a multiple of the value of sigma(F). |
| observed_criterion_sigma_I | double precision | The criterion used to classify a reflection as 'observed' expressed as a multiple of the value of sigma(I). |
| percent_possible_obs | double precision | The percentage of geometrically possible reflections represented by reflections that satisfy the resolution limits established by _reflns.d_resolution_high and _reflns.d_resolution_low and the observation limit established by _reflns.observed_criterion. |
| R_free_details | text | A description of the method by which a subset of reflections was selected for exclusion from refinement so as to be used in the calculation of a 'free' R factor. |
| Rmerge_F_all | double precision | Residual factor Rmerge for all reflections that satisfy the resolution limits established by _reflns.d_resolution_high and _reflns.d_resolution_low. sum~i~(sum~j~\|F~j~ - <F>\|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| Rmerge_F_obs | double precision | Residual factor Rmerge for reflections that satisfy the resolution limits established by _reflns.d_resolution_high and _reflns.d_resolution_low and the observation limit established by _reflns.observed_criterion. sum~i~(sum~j~\|F~j~ - <F>\|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| pdbx_redundancy | double precision | Overall redundancy for this data set. |
| pdbx_netI_over_av_sigmaI | double precision | The ratio of the average intensity to the average uncertainty, <I>/<sigma(I)>. |
| pdbx_netI_over_sigmaI | double precision | The mean of the ratio of the intensities to their standard uncertainties, <I/sigma(I)>. |
| pdbx_chi_squared | double precision | Overall Chi-squared statistic. |
| pdbx_scaling_rejects | integer | Number of reflections rejected in scaling operations. |
| phase_calculation_details | text | The value of _reflns.phase_calculation_details describes a special details about calculation of phases in _refln.phase_calc. |
| pdbx_Rrim_I_all | double precision | The redundancy-independent merging R factor value Rrim, also denoted Rmeas, for merging all intensities in this data set. sum~i~ [N~i~/(N~i~ - 1)]1/2^ sum~j~ \| I~j~ - <I~i~> \| Rrim = ---------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135. |
| pdbx_Rpim_I_all | double precision | The precision-indicating merging R factor value Rpim, for merging all intensities in this data set. sum~i~ [1/(N~i~ - 1)]1/2^ sum~j~ \| I~j~ - <I~i~> \| Rpim = -------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135. |
| pdbx_number_measured_all | integer | Total number of measured reflections. |
| pdbx_diffrn_id | text | An identifier for the diffraction data set for this set of summary statistics. Multiple diffraction data sets entered as a comma separated list. |
| pdbx_ordinal | integer | An ordinal identifier for this set of reflection statistics. |
| pdbx_CC_half | double precision | The Pearson's correlation coefficient expressed as a decimal value between the average intensities from randomly selected half-datasets. Ref: Karplus & Diederichs (2012), Science 336, 1030-33 |
| pdbx_CC_star | double precision | Estimates the value of CC_true, the true correlation coefficient between the average intensities from randomly selected half-datasets. CC_star = sqrt(2*CC_half/(1+CC_half)), where both CC_star and CC_half (CC1/2) Ref: Karplus & Diederichs (2012), Science 336, 1030-33 |
| pdbx_R_split | double precision | R split measures the agreement between the sets of intensities created by merging odd- and even-numbered images from the overall data. Ref: T. A. White, R. A. Kirian, A. V. Martin, A. Aquila, K. Nass, A. Barty and H. N. Chapman (2012), J. Appl. Cryst. 45, 335-341 |
| pdbx_Rmerge_I_obs | double precision | The R value for merging intensities satisfying the observed criteria in this data set. |
| pdbx_Rmerge_I_all | double precision | The R value for merging all intensities in this data set. |
| pdbx_Rsym_value | double precision | The R sym value as a decimal number. |
| pdbx_aniso_diffraction_limit_axis_1_ortho1 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_1_ortho2 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_1_ortho3 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_2_ortho1 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_2_ortho2 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_2_ortho3 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_3_ortho1 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_3_ortho2 | double precision |  |
| pdbx_aniso_diffraction_limit_axis_3_ortho3 | double precision |  |
| pdbx_aniso_diffraction_limit_1 | double precision | Anisotropic diffraction limit along principal axis 1 (of ellipsoid fitted to the diffraction cut-off surface). |
| pdbx_aniso_diffraction_limit_2 | double precision | Anisotropic diffraction limit along principal axis 2 (of ellipsoid fitted to the diffraction cut-off surface) |
| pdbx_aniso_diffraction_limit_3 | double precision | Anisotropic diffraction limit along principal axis 3 (of ellipsoid fitted to the diffraction cut-off surface) |
| pdbx_aniso_B_tensor_eigenvector_1_ortho1 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_1_ortho2 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_1_ortho3 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_2_ortho1 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_2_ortho2 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_2_ortho3 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_3_ortho1 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_3_ortho2 | double precision |  |
| pdbx_aniso_B_tensor_eigenvector_3_ortho3 | double precision |  |
| pdbx_aniso_B_tensor_eigenvalue_1 | double precision | Eigen-B-factor along the first eigenvector of the diffraction anisotropy tensor |
| pdbx_aniso_B_tensor_eigenvalue_2 | double precision | Eigen-B-factor along the second eigenvector of the diffraction anisotropy tensor |
| pdbx_aniso_B_tensor_eigenvalue_3 | double precision | Eigen-B-factor along the third eigenvector of the diffraction anisotropy tensor |
| pdbx_orthogonalization_convention | text | Description of orthogonalization convention used. The notation can make use of unit cell axes "a", "b" and "c" and the reciprocal unit cell axes "astar", "bstar" and "cstar". Upper case letters "X", "Y" and "Z" denote the orthogonal axes, while lower case "x" stands for "cross product". |
| pdbx_percent_possible_ellipsoidal | double precision | Completeness (as a percentage) of symmetry-unique data within the intersection of (1) a sphere (defined by the diffraction limits, _reflns.d_resolution_high and _reflns.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique reflections within that intersection. |
| pdbx_percent_possible_spherical | double precision | Completeness (as a percentage) of symmetry-unique data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) relative to all possible symmetry-unique reflections within that sphere. In the absence of an anisotropy description this is identical to _reflns.percent_possible_obs. |
| pdbx_percent_possible_ellipsoidal_anomalous | double precision | Completeness (as a percentage) of symmetry-unique anomalous difference data within the intersection of (1) a sphere (defined by the diffraction limits, _reflns.d_resolution_high and _reflns.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique anomalous difference data within that intersection. |
| pdbx_percent_possible_spherical_anomalous | double precision | Completeness (as a percentage) of symmetry-unique anomalous difference data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that sphere. In the absence of an anisotropy description this is identical to _reflns.pdbx_percent_possible_anomalous. |
| pdbx_redundancy_anomalous | double precision | The overall redundancy of anomalous difference data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low), i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection. |
| pdbx_CC_half_anomalous | double precision | The overall correlation coefficient between two randomly chosen half-sets of anomalous intensity differences, I(+)-I(-) for anomalous data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low), i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection. |
| pdbx_absDiff_over_sigma_anomalous | double precision | The overall mean ratio of absolute anomalous intensity differences to their standard deviation within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) and using data for which intensities for both instances of a Friedel pair are available for an acentric reflection. \|Dano\| ------------- sigma(Dano) with Dano = I(+) - I(-) sigma(Dano) = sqrt( sigma(I(+))^2 + sigma(I(-))^2 ) |
| pdbx_percent_possible_anomalous | double precision | Completeness (as a percentage) of symmetry-unique anomalous difference data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that sphere. |
| pdbx_observed_signal_threshold | double precision | The threshold value for _refln.pdbx_signal as used to define the status of an individual reflection according to the description in _refln.pdbx_signal_status. |
| pdbx_signal_type | text | Type of signal used for _reflns.pdbx_observed_signal_threshold and _refln.pdbx_signal In the enumeration details: Imean is the inverse-variance weighted mean intensity of all measurements for a given symmetry-unique reflection Ihalf is the inverse-variance weighted mean intensity of a random half-selection of all measurements for a given symmetry-unique reflection |
| pdbx_signal_details | text | Further details about the calculation of the values assigned to _refln.pdbx_signal |

## reflns_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| pdbx_ordinal | integer |  |
| update_id | integer |  |
| auth_validate | text |  |
| B_iso_Wilson_estimate | double precision |  |
| Rmerge_F_obs | double precision |  |
| d_resolution_high | double precision |  |
| d_resolution_low | double precision |  |
| number_all | integer |  |
| number_obs | integer |  |
| observed_criterion_sigma_F | double precision |  |
| observed_criterion_sigma_I | double precision |  |
| pdbx_Rmerge_I_obs | text |  |
| pdbx_number_measured_all | integer |  |
| pdbx_redundancy | text |  |
| percent_possible_obs | double precision |  |

## reflns_scale

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| group_code | text | The code identifying a scale _reflns_scale.meas_F, _reflns_scale.meas_F_squared or _reflns_scale.meas_intensity. These are linked to the REFLN list by the _refln.scale_group_code. These codes need not correspond to those in the DIFFRN_SCALE list. |

## reflns_shell

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| d_res_high | double precision | The smallest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the highest resolution. |
| d_res_low | double precision | The highest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the lowest resolution. |
| meanI_over_sigI_all | double precision | The ratio of the mean of the intensities of all reflections in this shell to the mean of the standard uncertainties of the intensities of all reflections in this shell. |
| meanI_over_sigI_obs | double precision | The ratio of the mean of the intensities of the reflections classified as 'observed' (see _reflns.observed_criterion) in this shell to the mean of the standard uncertainties of the intensities of the 'observed' reflections in this shell. |
| number_measured_all | integer | The total number of reflections measured for this shell. |
| number_measured_obs | integer | The number of reflections classified as 'observed' (see _reflns.observed_criterion) for this shell. |
| number_possible | integer | The number of unique reflections it is possible to measure in this shell. |
| number_unique_all | integer | The total number of measured reflections which are symmetry- unique after merging for this shell. |
| number_unique_obs | integer | The total number of measured reflections classified as 'observed' (see _reflns.observed_criterion) which are symmetry-unique after merging for this shell. |
| percent_possible_obs | double precision | The percentage of geometrically possible reflections represented by reflections classified as 'observed' (see _reflns.observed_criterion) for this shell. |
| Rmerge_F_all | double precision | Residual factor Rmerge for all reflections that satisfy the resolution limits established by _reflns_shell.d_res_high and _reflns_shell.d_res_low. sum~i~(sum~j~\|F~j~ - <F>\|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| Rmerge_F_obs | double precision | Residual factor Rmerge for reflections that satisfy the resolution limits established by _reflns_shell.d_res_high and _reflns_shell.d_res_low and the observation criterion established by _reflns.observed_criterion. sum~i~(sum~j~\|F~j~ - <F>\|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| meanI_over_uI_all | double precision | The ratio of the mean of the intensities of all reflections in this shell to the mean of the standard uncertainties of the intensities of all reflections in this shell. |
| percent_possible_gt | double precision | The percentage of geometrically possible reflections represented by significantly intense reflections (see _reflns.threshold_expression) measured for this shell. |
| pdbx_redundancy | double precision | Redundancy for the current shell. |
| pdbx_chi_squared | double precision | Chi-squared statistic for this resolution shell. |
| pdbx_netI_over_sigmaI_all | double precision | The mean of the ratio of the intensities to their standard uncertainties of all reflections in the resolution shell. _reflns_shell.pdbx_netI_over_sigmaI_all = <I/sigma(I)> |
| pdbx_netI_over_sigmaI_obs | double precision | The mean of the ratio of the intensities to their standard uncertainties of observed reflections (see _reflns.observed_criterion) in the resolution shell. _reflns_shell.pdbx_netI_over_sigmaI_obs = <I/sigma(I)> |
| pdbx_Rrim_I_all | double precision | The redundancy-independent merging R factor value Rrim, also denoted Rmeas, for merging all intensities in a given shell. sum~i~ [N~i~ /( N~i~ - 1)]1/2^ sum~j~ \| I~j~ - <I~i~> \| Rrim = -------------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135. |
| pdbx_Rpim_I_all | double precision | The precision-indicating merging R factor value Rpim, for merging all intensities in a given shell. sum~i~ [1/(N~i~ - 1)]1/2^ sum~j~ \| I~j~ - <I~i~> \| Rpim = -------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135. |
| pdbx_rejects | integer | The number of rejected reflections in the resolution shell. Reflections may be rejected from scaling by setting the observation criterion, _reflns.observed_criterion. |
| pdbx_ordinal | integer | An ordinal identifier for this resolution shell. |
| pdbx_diffrn_id | text | An identifier for the diffraction data set corresponding to this resolution shell. Multiple diffraction data sets specified as a comma separated list. |
| pdbx_CC_half | double precision | The Pearson's correlation coefficient expressed as a decimal value between the average intensities from randomly selected half-datasets within the resolution shell. Ref: Karplus & Diederichs (2012), Science 336, 1030-33 |
| pdbx_CC_star | double precision | Estimates the value of CC_true, the true correlation coefficient between the average intensities from randomly selected half-datasets within the resolution shell. CC_star = sqrt(2*CC_half/(1+CC_half)) Ref: Karplus & Diederichs (2012), Science 336, 1030-33 |
| pdbx_R_split | double precision | R split measures the agreement between the sets of intensities created by merging odd- and even-numbered images from the data within the resolution shell. Ref: T. A. White, R. A. Kirian, A. V. Martin, A. Aquila, K. Nass, A. Barty and H. N. Chapman (2012), J. Appl. Cryst. 45, 335-341 |
| percent_possible_all | double precision | The percentage of geometrically possible reflections represented by all reflections measured for this shell. |
| Rmerge_I_all | double precision | The value of Rmerge(I) for all reflections in a given shell. sum~i~(sum~j~\|I~j~ - <I>\|) Rmerge(I) = -------------------------- sum~i~(sum~j~<I>) I~j~ = the intensity of the jth observation of reflection i <I> = the mean of the intensities of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| Rmerge_I_obs | double precision | The value of Rmerge(I) for reflections classified as 'observed' (see _reflns.observed_criterion) in a given shell. sum~i~(sum~j~\|I~j~ - <I>\|) Rmerge(I) = -------------------------- sum~i~(sum~j~<I>) I~j~ = the intensity of the jth observation of reflection i <I> = the mean of the intensities of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection |
| pdbx_Rsym_value | double precision | R sym value in percent. |
| pdbx_percent_possible_ellipsoidal | double precision | Completeness (as a percentage) of symmetry-unique data within the intersection of (1) a spherical shell (defined by its diffraction limits, _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique reflections within that intersection. |
| pdbx_percent_possible_spherical | double precision | Completeness (as a percentage) of symmetry-unique data within the spherical shell defined by its diffraction limits (_reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) relative to all possible symmetry-unique reflections within that shell. In the absence of an anisotropy description this is identical to _reflns_shell.percent_possible_all. |
| pdbx_percent_possible_ellipsoidal_anomalous | double precision | Completeness (as a percentage) of symmetry-unique anomalous difference data within the intersection of (1) a spherical shell (defined by its diffraction limits, _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique anomalous difference data within that intersection. |
| pdbx_percent_possible_spherical_anomalous | double precision | Completeness (as a percentage) of symmetry-unique anomalous difference data within the spherical shell defined by its diffraction limits (_reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that shell. In the absence of an anisotropy description this is identical to _reflns.pdbx_percent_possible_anomalous. |
| pdbx_redundancy_anomalous | double precision | The redundancy of anomalous difference data within the spherical shell (defined by its diffraction limits _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low), i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection. |
| pdbx_CC_half_anomalous | double precision | The correlation coefficient within the spherical shell (defined by its diffraction limits _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) between two randomly chosen half-sets of anomalous intensity differences, I(+)-I(-) for anomalous data, i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection. |
| pdbx_absDiff_over_sigma_anomalous | double precision | The mean ratio of absolute anomalous intensity differences to their standard deviation within the spherical shell (defined by its diffraction limits _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low). \|Dano\| ------------- sigma(Dano) with Dano = I(+) - I(-) sigma(Dano) = sqrt( sigma(I(+))^2 + sigma(I(-))^2 ) |
| pdbx_percent_possible_anomalous | double precision | Completeness (as a percentage) of symmetry-unique anomalous difference data within the spherical shell defined by its diffraction limits (_reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that shell. |

## software

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| classification | text | The classification of the program according to its major function. |
| compiler_version | text | The version of the compiler used to compile the software. |
| contact_author | text | The recognized contact author of the software. This could be the original author, someone who has modified the code or someone who maintains the code. It should be the person most commonly associated with the code. |
| contact_author_email | text | The e-mail address of the person specified in _software.contact_author. |
| date | text | The date the software was released. |
| description | text | Description of the software. |
| language | text | The major computing language in which the software is coded. |
| location | text | The URL for an Internet address at which details of the software can be found. |
| name | text | The name of the software. |
| os | text | The name of the operating system under which the software runs. |
| os_version | text | The version of the operating system under which the software runs. |
| type | text | The classification of the software according to the most common types. |
| version | text | The version of the software. |
| pdbx_ordinal | integer | An ordinal index for this category |

## space_group

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| crystal_system | text | The name of the system of geometric crystal classes of space groups (crystal system) to which the space group belongs. Note that rhombohedral space groups belong to the trigonal system. |
| id | text | This is the unique identifier for the SPACE_GROUP category. |
| IT_number | integer | The number as assigned in International Tables for Crystallography Vol. A, specifying the proper affine class (i.e. the orientation-preserving affine class) of space groups (crystallographic space-group type) to which the space group belongs. This number defines the space-group type but not the coordinate system in which it is expressed. |
| name_Hall | text | Space-group symbol defined by Hall. Each component of the space-group name is separated by a space or an underscore. The use of a space is strongly recommended. The underscore is only retained because it was used in old CIFs. It should not be used in new CIFs. _space_group.name_Hall uniquely defines the space group and its reference to a particular coordinate system. Ref: Hall, S. R. (1981). Acta Cryst. A37, 517-525; erratum (1981), A37, 921. [See also International Tables for Crystallography Vol. B (2001), Chapter 1.4, Appendix 1.4.2.] |
| name_H-M_alt | text |  |

## space_group_symop

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | An arbitrary identifier that uniquely labels each symmetry operation in the list. |
| operation_xyz | text | A parsable string giving one of the symmetry operations of the space group in algebraic form. If W is a matrix representation of the rotational part of the symmetry operation defined by the positions and signs of x, y and z, and w is a column of translations defined by the fractions, an equivalent position X' is generated from a given position X by the equation X' = WX + w (Note: X is used to represent bold_italics_x in International Tables for Crystallography Vol. A, Part 5) When a list of symmetry operations is given, it must contain a complete set of coordinate representatives which generates all the operations of the space group by the addition of all primitive translations of the space group. Such representatives are to be found as the coordinates of the general-equivalent position in International Tables for Crystallography Vol. A (2002), to which it is necessary to add any centring translations shown above the general-equivalent position. That is to say, it is necessary to list explicity all the symmetry operations required to generate all the atoms in the unit cell defined by the setting used. |

## struct

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| title | text | A title for the data block. The author should attempt to convey the essence of the structure archived in the CIF in the title, and to distinguish this structural result from others. |
| pdbx_model_details | text | Text description of the methodology which produced this model structure. |
| pdbx_model_type_details | text | A description of the type of structure model. |
| pdbx_CASP_flag | text | The item indicates whether the entry is a CASP target, a CASD-NMR target, or similar target participating in methods development experiments. |

## struct_asym

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of this portion of the contents of the asymmetric unit. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| id | text | The value of _struct_asym.id must uniquely identify a record in the STRUCT_ASYM list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_modified | text | This data item indicates whether the structural elements are modified. |
| pdbx_blank_PDB_chainid_flag | text | A flag indicating that this entity was originally labeled with a blank PDB chain id. |

## struct_biol

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the biological unit. |
| id | text | The value of _struct_biol.id must uniquely identify a record in the STRUCT_BIOL list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_parent_biol_id | text | An identifier for the parent biological assembly if this biological unit is part of a complex assembly. |
| pdbx_formula_weight_method | text | Method used to determine _struct_biol.pdbx_formula_weight. |
| pdbx_aggregation_state | text | A description of the structural aggregation in this assembly. |
| pdbx_assembly_method | text | The method or experiment used to determine this assembly. |

## struct_biol_keywords

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| biol_id | text | This data item is a pointer to _struct_biol.id in the STRUCT_BIOL category. |
| text | text | Keywords describing this biological entity. |

## struct_conf

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| beg_label_asym_id | text | A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| beg_label_comp_id | text | A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| beg_label_seq_id | integer | A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| beg_auth_asym_id | text | A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| beg_auth_comp_id | text | A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| beg_auth_seq_id | text | A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| conf_type_id | text | This data item is a pointer to _struct_conf_type.id in the STRUCT_CONF_TYPE category. |
| details | text | A description of special aspects of the conformation assignment. |
| end_label_asym_id | text | A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| end_label_comp_id | text | A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| end_label_seq_id | integer | A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| end_auth_asym_id | text | A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| end_auth_comp_id | text | A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| end_auth_seq_id | text | A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| id | text | The value of _struct_conf.id must uniquely identify a record in the STRUCT_CONF list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_beg_PDB_ins_code | text | A component of the identifier for the residue at which the conformation segment starts. |
| pdbx_end_PDB_ins_code | text | A component of the identifier for the residue at which the conformation segment ends. |
| pdbx_PDB_helix_class | text | This item is a place holder for the helix class used in the PDB HELIX record. |
| pdbx_PDB_helix_length | integer | A placeholder for the lengths of the helix of the PDB HELIX record. |
| pdbx_PDB_helix_id | text | A placeholder for the helix identifier of the PDB HELIX record. |

## struct_conf_type

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The descriptor that categorizes the type of the conformation of the backbone of the polymer (whether protein or nucleic acid). Explicit values for the torsion angles that define each conformation are not given here, but it is expected that the author would provide such information in either the _struct_conf_type.criteria or _struct_conf_type.reference data items, or both. |

## struct_conn

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| conn_type_id | text | This data item is a pointer to _struct_conn_type.id in the STRUCT_CONN_TYPE category. |
| details | text | A description of special aspects of the connection. |
| id | text | The value of _struct_conn.id must uniquely identify a record in the STRUCT_CONN list. Note that this item need not be a number; it can be any unique identifier. |
| ptnr1_label_asym_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| ptnr1_label_atom_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category. |
| ptnr1_label_comp_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| ptnr1_label_seq_id | integer | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| ptnr1_auth_asym_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| ptnr1_auth_comp_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| ptnr1_auth_seq_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| ptnr1_symmetry | text | Describes the symmetry operation that should be applied to the atom set specified by _struct_conn.ptnr1_label* to generate the first partner in the structure connection. |
| ptnr2_label_asym_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| ptnr2_label_atom_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category. |
| ptnr2_label_comp_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| ptnr2_label_seq_id | integer | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| ptnr2_auth_asym_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| ptnr2_auth_comp_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| ptnr2_auth_seq_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| ptnr2_symmetry | text | Describes the symmetry operation that should be applied to the atom set specified by _struct_conn.ptnr2_label* to generate the second partner in the structure connection. |
| pdbx_ptnr1_PDB_ins_code | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| pdbx_ptnr1_label_alt_id | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| pdbx_ptnr2_PDB_ins_code | text | A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category. |
| pdbx_ptnr2_label_alt_id | text | A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category. |
| pdbx_dist_value | double precision | Distance value for this contact. |
| pdbx_value_order | text | The chemical bond order associated with the specified atoms in this contact. |
| pdbx_leaving_atom_flag | text | This data item identifies if the linkage has displaced leaving atoms on both, one or none of the connected atoms forming the linkage. Leaving atoms are defined within their chemical defintions of each connected component. |
| pdbx_role | text | The chemical or structural role of the interaction |

## struct_conn_type

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The chemical or structural type of the interaction. |

## struct_keywords

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| text | text | Keywords describing this structure. |
| pdbx_keywords | text | Terms characterizing the macromolecular structure. |

## struct_mon_prot_cis

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| label_asym_id | text | A component of the identifier for the monomer. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_comp_id | text | A component of the identifier for the monomer. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_seq_id | integer | A component of the identifier for the monomer. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| auth_asym_id | text | A component of the identifier for the monomer. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | A component of the identifier for the monomer. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | A component of the identifier for the monomer. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| pdbx_auth_asym_id_2 | text | Pointer to _atom_site.auth_asym_id. |
| pdbx_auth_comp_id_2 | text | Pointer to _atom_site.auth_comp_id. |
| pdbx_auth_seq_id_2 | text | Pointer to _atom_site.auth_seq_id |
| pdbx_label_asym_id_2 | text | Pointer to _atom_site.label_asym_id. |
| pdbx_label_comp_id_2 | text | Pointer to _atom_site.label_comp_id. |
| pdbx_label_seq_id_2 | integer | Pointer to _atom_site.label_seq_id |
| pdbx_PDB_ins_code | text | Pointer to _atom_site.pdbx_PDB_ins_code |
| pdbx_PDB_ins_code_2 | text | Pointer to _atom_site.pdbx_PDB_ins_code |
| pdbx_PDB_model_num | integer | Pointer to _atom_site.pdbx_PDB_model_num |
| pdbx_omega_angle | text | omega torsion angle |
| pdbx_id | text | ordinal index |

## struct_ncs_dom

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the structural elements that comprise a domain in an ensemble of domains related by noncrystallographic symmetry. |
| id | text | The value of _struct_ncs_dom.id must uniquely identify a record in the STRUCT_NCS_DOM list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_ens_id | text | This is a unique identifier for a collection NCS related domains. This references item '_struct_ncs_ens.id'. |

## struct_ncs_dom_lim

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| beg_label_alt_id | text | A component of the identifier for the monomer at which this segment of the domain begins. |
| beg_label_asym_id | text | A component of the identifier for the monomer at which this segment of the domain begins. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| beg_label_comp_id | text | A component of the identifier for the monomer at which this segment of the domain begins. |
| beg_label_seq_id | integer | A component of the identifier for the monomer at which this segment of the domain begins. |
| beg_auth_asym_id | text | A component of the identifier for the monomer at which this segment of the domain begins. |
| beg_auth_comp_id | text | A component of the identifier for the monomer at which this segment of the domain begins. |
| beg_auth_seq_id | text | A component of the identifier for the monomer at which this segment of the domain begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| dom_id | text | This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category. |
| end_label_alt_id | text | A component of the identifier for the monomer at which this segment of the domain ends. |
| end_label_asym_id | text | A component of the identifier for the monomer at which this segment of the domain ends. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| end_label_comp_id | text | A component of the identifier for the monomer at which this segment of the domain ends. |
| end_label_seq_id | integer | A component of the identifier for the monomer at which this segment of the domain ends. |
| end_auth_asym_id | text | A component of the identifier for the monomer at which this segment of the domain ends. |
| end_auth_comp_id | text | A component of the identifier for the monomer at which this segment of the domain ends. |
| end_auth_seq_id | text | A component of the identifier for the monomer at which this segment of the domain ends. |
| selection_details | text | A text description of the selection of residues that correspond to this domain. |
| pdbx_component_id | integer | Record number of the NCS domain limit assignment. |
| pdbx_refine_code | double precision | record the refinement code number (from CCP4.) |
| pdbx_ens_id | text | This is a unique identifier for a collection NCS related domains. This references item '_struct_ncs_dom.pdbx_ens_id'. |

## struct_ncs_ens

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the ensemble. |
| id | text | The value of _struct_ncs_ens.id must uniquely identify a record in the STRUCT_NCS_ENS list. Note that this item need not be a number; it can be any unique identifier. |

## struct_ncs_ens_gen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| dom_id_1 | text | The identifier for the domain that will remain unchanged by the transformation operator. This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category. |
| dom_id_2 | text | The identifier for the domain that will be transformed by application of the transformation operator. This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category. |
| ens_id | text | This data item is a pointer to _struct_ncs_ens.id in the STRUCT_NCS_ENS category. |
| oper_id | integer | This data item is a pointer to _struct_ncs_oper.id in the STRUCT_NCS_OPER category. |

## struct_ncs_oper

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| code | text | A code to indicate whether this operator describes a relationship between coordinates all of which are given in the data block (in which case the value of code is 'given'), or whether the operator is used to generate new coordinates from those that are given in the data block (in which case the value of code is 'generate'). |
| details | text | A description of special aspects of the noncrystallographic symmetry operator. |
| id | integer | The value of _struct_ncs_oper.id must uniquely identify a record in the STRUCT_NCS_OPER list. Note that for PDB _struct_ncs_oper.id must be a number. |
| matrix11 | double precision |  |
| matrix12 | double precision |  |
| matrix13 | double precision |  |
| matrix21 | double precision |  |
| matrix22 | double precision |  |
| matrix23 | double precision |  |
| matrix31 | double precision |  |
| matrix32 | double precision |  |
| matrix33 | double precision |  |
| vector1 | double precision |  |
| vector2 | double precision |  |
| vector3 | double precision |  |

## struct_ref

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| db_code | text | The code for this entity or biological unit or for a closely related entity or biological unit in the named database. |
| db_name | text | The name of the database containing reference information about this entity or biological unit. |
| entity_id | text | This data item is a pointer to _entity.id in the ENTITY category. |
| id | text | The value of _struct_ref.id must uniquely identify a record in the STRUCT_REF list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_db_accession | text | Accession code assigned by the reference database. |
| pdbx_db_isoform | text | Database code assigned by the reference database for a sequence isoform. An isoform sequence is an alternative protein sequence that can be generated from the same gene by a single or by a combination of biological events such as: alternative promoter usage, alternative splicing, alternative initiation and ribosomal frameshifting. |
| pdbx_seq_one_letter_code | text | Database chemical sequence expressed as string of one-letter amino acid codes. |
| pdbx_align_begin | text | Beginning index in the chemical sequence from the reference database. |

## struct_ref_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| biological_source | text |  |
| cellular_location | text |  |
| db_name | text |  |
| entity_id | text |  |
| pdbx_db_accession | text |  |

## struct_ref_seq

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| align_id | text | The value of _struct_ref_seq.align_id must uniquely identify a record in the STRUCT_REF_SEQ list. Note that this item need not be a number; it can be any unique identifier. |
| db_align_beg | integer | The sequence position in the referenced database entry at which the alignment begins. |
| db_align_end | integer | The sequence position in the referenced database entry at which the alignment ends. |
| ref_id | text | This data item is a pointer to _struct_ref.id in the STRUCT_REF category. |
| seq_align_beg | integer | The sequence position in the entity or biological unit described in the data block at which the alignment begins. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |
| seq_align_end | integer | The sequence position in the entity or biological unit described in the data block at which the alignment ends. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |
| pdbx_strand_id | text | The PDB strand/chain ID . |
| pdbx_db_accession | text | Accession code of the reference database. |
| pdbx_db_align_beg_ins_code | text | Initial insertion code of the sequence segment of the reference database. |
| pdbx_db_align_end_ins_code | text | Ending insertion code of the sequence segment of the reference database. |
| pdbx_PDB_id_code | text | The PDB code of the structure. |
| pdbx_auth_seq_align_beg | text | Initial position in the PDB sequence segment. |
| pdbx_auth_seq_align_end | text | Ending position in the PDB sequence segment |
| pdbx_seq_align_beg_ins_code | text | Initial insertion code of the PDB sequence segment. |
| pdbx_seq_align_end_ins_code | text | Ending insertion code of the sequence segment |

## struct_ref_seq_dif

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| align_id | text | This data item is a pointer to _struct_ref_seq.align_id in the STRUCT_REF_SEQ category. |
| db_mon_id | text | The monomer type found at this position in the referenced database entry. This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| details | text | A description of special aspects of the point differences between the sequence of the entity or biological unit described in the data block and that in the referenced database entry. |
| mon_id | text | The monomer type found at this position in the sequence of the entity or biological unit described in this data block. This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| seq_num | integer | This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category. |
| pdbx_pdb_id_code | text | The PDB ID code. |
| pdbx_pdb_strand_id | text | PDB strand/chain id. |
| pdbx_pdb_ins_code | text | Insertion code in PDB sequence |
| pdbx_auth_seq_num | text | The PDB sequence residue number. |
| pdbx_seq_db_name | text | Sequence database name. |
| pdbx_seq_db_accession_code | text | Sequence database accession number. |
| pdbx_seq_db_seq_num | text | Sequence database sequence number. |
| pdbx_ordinal | integer | A synthetic integer primary key for this category. |

## struct_ref_seq_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| align_id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| db_align_beg | integer |  |
| db_align_end | integer |  |
| pdbx_auth_seq_align_beg | text |  |
| pdbx_auth_seq_align_end | text |  |
| pdbx_db_accession | text |  |
| pdbx_strand_id | text |  |
| ref_id | text |  |
| seq_align_beg | integer |  |
| seq_align_end | integer |  |

## struct_sheet

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _struct_sheet.id must uniquely identify a record in the STRUCT_SHEET list. Note that this item need not be a number; it can be any unique identifier. |
| number_strands | integer | The number of strands in the sheet. If a given range of residues bulges out from the strands, it is still counted as one strand. If a strand is composed of two different regions of polypeptide, it is still counted as one strand, as long as the proper hydrogen- bonding connections are made to adjacent strands. |

## struct_sheet_order

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| range_id_1 | text | This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category. |
| range_id_2 | text | This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category. |
| sense | text | A flag to indicate whether the two designated residue ranges are parallel or antiparallel to one another. |
| sheet_id | text | This data item is a pointer to _struct_sheet.id in the STRUCT_SHEET category. |

## struct_sheet_range

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| beg_label_asym_id | text | A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| beg_label_comp_id | text | A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| beg_label_seq_id | integer | A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| end_label_asym_id | text | A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category. |
| end_label_comp_id | text | A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _chem_comp.id in the CHEM_COMP category. |
| end_label_seq_id | integer | A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| beg_auth_asym_id | text | A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| beg_auth_comp_id | text | A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| beg_auth_seq_id | text | A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| end_auth_asym_id | text | A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| end_auth_comp_id | text | A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| end_auth_seq_id | text | A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| id | text | The value of _struct_sheet_range.id must uniquely identify a range in a given sheet in the STRUCT_SHEET_RANGE list. Note that this item need not be a number; it can be any unique identifier. |
| sheet_id | text | This data item is a pointer to _struct_sheet.id in the STRUCT_SHEET category. |
| pdbx_beg_PDB_ins_code | text | A component of the identifier for the residue at which the beta sheet range begins. Insertion code. |
| pdbx_end_PDB_ins_code | text | A component of the identifier for the residue at which the beta sheet range ends. Insertion code. |

## struct_site

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| details | text | A description of special aspects of the site. |
| id | text | The value of _struct_site.id must uniquely identify a record in the STRUCT_SITE list. Note that this item need not be a number; it can be any unique identifier. |
| pdbx_num_residues | integer | Number of residues in the site. |
| pdbx_evidence_code | text | Source of evidence supporting the assignment of this site. |
| pdbx_auth_asym_id | text | A component of the identifier for the ligand in the site. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| pdbx_auth_comp_id | text | A component of the identifier for the ligand in the site. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| pdbx_auth_seq_id | text | A component of the identifier for the ligand in the site. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| pdbx_auth_ins_code | text | PDB insertion code for the ligand in the site. |

## struct_site_gen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _struct_site_gen.id must uniquely identify a record in the STRUCT_SITE_GEN list. Note that this item need not be a number; it can be any unique identifier. |
| label_asym_id | text | A component of the identifier for participants in the site. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category. |
| label_comp_id | text | A component of the identifier for participants in the site. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category. |
| label_seq_id | integer | A component of the identifier for participants in the site. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category. |
| auth_asym_id | text | A component of the identifier for participants in the site. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category. |
| auth_comp_id | text | A component of the identifier for participants in the site. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category. |
| auth_seq_id | text | A component of the identifier for participants in the site. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category. |
| site_id | text | This data item is a pointer to _struct_site.id in the STRUCT_SITE category. |
| symmetry | text | Describes the symmetry operation that should be applied to the atom set specified by _struct_site_gen.label* to generate a portion of the site. |
| pdbx_auth_ins_code | text | PDB insertion code. |
| pdbx_num_res | integer | Number of residues in the site. |

## struct_site_gen_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text |  |
| site_id | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| auth_asym_id | text |  |
| auth_seq_id | text |  |
| details | text |  |
| label_asym_id | text |  |
| label_comp_id | text |  |
| label_seq_id | text |  |
| beg_auth_seq_id | text |  |
| end_auth_seq_id | text |  |
| beg_label_seq_id | text |  |
| end_label_seq_id | text |  |
| beg_label_comp_id | text |  |
| end_label_comp_id | text |  |

## struct_site_keywords

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| site_id | text | This data item is a pointer to _struct_site.id in the STRUCT_SITE category. |
| text | text | Keywords describing this site. |

## struct_site_pdbmlplus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text |  |
| info_type | text |  |
| info_subtype | text |  |
| update_id | integer |  |
| auth_validate | text |  |
| details | text |  |
| pdbx_num_residues | integer |  |
| orig_data | text |  |
| orig_rmsd | text |  |
| orig_number_of_atom_pairs | integer |  |

## symmetry

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| entry_id | text | This data item is a pointer to _entry.id in the ENTRY category. |
| cell_setting | text | The cell settings for this space-group symmetry. |
| Int_Tables_number | integer | Space-group number from International Tables for Crystallography Vol. A (2002). |
| space_group_name_Hall | text | Space-group symbol as described by Hall (1981). This symbol gives the space-group setting explicitly. Leave spaces between the separate components of the symbol. Ref: Hall, S. R. (1981). Acta Cryst. A37, 517-525; erratum (1981) A37, 921. |
| space_group_name_H-M | text |  |
| pdbx_full_space_group_name_H-M | text |  |

## symmetry_equiv

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text | PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table. |
| id | text | The value of _symmetry_equiv.id must uniquely identify a record in the SYMMETRY_EQUIV category. Note that this item need not be a number; it can be any unique identifier. |
| pos_as_xyz | text | Symmetry-equivalent position in the 'xyz' representation. Except for the space group P1, these data will be repeated in a loop. The format of the data item is as per International Tables for Crystallography Vol. A (2002). All equivalent positions should be entered, including those for lattice centring and a centre of symmetry, if present. |
