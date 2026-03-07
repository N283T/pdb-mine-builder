"""SQLAlchemy schema definition for pdbj."""

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Double,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData(schema="pdbj")
metadata.info = {
    "entry_pk": "pdbid",
    "skip_keywords": [
        "entity_poly.pdbx_seq_one_letter_code",
        "entity_poly.pdbx_seq_one_letter_code_can",
        "struct_ref.pdbx_seq_one_letter_code",
    ],
}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All other tables/categories refer back to the PDBID in the brief_summary table."),
    Column("docid", BigInteger, nullable=True, comment="Serial counter (unique integer) to represent the row id."),
    Column("deposition_date", Date, nullable=True, comment="Deposition date of an entry."),
    Column("release_date", Date, nullable=True, comment="Release date of an entry."),
    Column("modification_date", Date, nullable=True, comment="Modification date of a PDB entry (wwPDB data)."),
    Column("deposit_author", ARRAY(Text), nullable=True, comment="Array of deposition authors."),
    Column("citation_author", ARRAY(Text), nullable=True, comment="Array of citation authors of associated paper."),
    Column("citation_title", ARRAY(Text), nullable=True, comment="Title of associated paper."),
    Column("citation_journal", ARRAY(Text), nullable=True, comment="Journal of associated paper."),
    Column("citation_year", ARRAY(Integer), nullable=True, comment="Year of associated paper."),
    Column("citation_volume", ARRAY(Text), nullable=True, comment="Volume of associated paper."),
    Column("citation_author_pri", ARRAY(Text), nullable=True, comment="Array of primary citation authors for associated paper."),
    Column("citation_title_pri", Text, nullable=True, comment="Primary citation title."),
    Column("citation_journal_pri", Text, nullable=True, comment="Primary citation journal."),
    Column("citation_year_pri", Integer, nullable=True, comment="Primary citation year."),
    Column("citation_volume_pri", Text, nullable=True, comment="Primary citation volume."),
    Column("chain_type", ARRAY(Text), nullable=True, comment="Array of chain types"),
    Column("chain_type_ids", ARRAY(Integer), nullable=True, comment="Array of chain types encoded as integers: 1: polypeptide(D) 2: polypeptide(L) 3: polydeoxyribonucleotide 4: polyribonucleotide 5: polysaccharide(D) 6: polysaccharide(L) 7: polydeoxyribonucleotide/polyribonucleotide hybrid 8: cyclic-pseudo-peptide 9: other"),
    Column("chain_number", Integer, nullable=True, comment="Number of chains."),
    Column("chain_length", ARRAY(Integer), nullable=True, comment="Number of residues for each chain."),
    Column("pdbx_descriptor", Text, nullable=True, comment="Structure descriptor (refers to entity.pdbx_description)"),
    Column("struct_title", Text, nullable=True, comment="Structure title."),
    Column("ligand", ARRAY(Text), nullable=True, comment="Array of ligands."),
    Column("exptl_method", ARRAY(Text), nullable=True, comment="Array of experimental methods used."),
    Column("exptl_method_ids", ARRAY(Integer), nullable=True, comment="Array of experimental methods used encoded as integers: 1: X-RAY DIFFRACTION 2: NEUTRON DIFFRACTION 3: FIBER DIFFRACTION 4: ELECTRON CRYSTALLOGRAPHY 5: ELECTRON MICROSCOPY 6: SOLUTION NMR 7: SOLID-STATE NMR 8: SOLUTION SCATTERING 9: POWDER DIFFRACTION 10: INFRARED SPECTROSCOPY 11: EPR 12: FLUORESCENCE TRANSFER 13: THEORETICAL MODEL 14: HYBRID 15: THEORETICAL MODEL (obsolete)"),
    Column("resolution", Double, nullable=True, comment="Resolution"),
    Column("biol_species", Text, nullable=True, comment="Biological species."),
    Column("host_species", Text, nullable=True, comment="Host species."),
    Column("db_pubmed", ARRAY(Text), nullable=True, comment="Array of associated PubMed IDs."),
    Column("db_doi", ARRAY(Text), nullable=True, comment="Array of associated DOI IDs."),
    Column("db_ec_number", ARRAY(Text), nullable=True, comment="Array of associated EC numbers."),
    Column("db_goid", ARRAY(Text), nullable=True, comment="Array of associated GO IDs."),
    Column("db_uniprot", ARRAY(Text), nullable=True, comment="Array of associated Uniprot IDs."),
    Column("db_genbank", ARRAY(Text), nullable=True, comment="Array of associated GenBank IDs."),
    Column("db_embl", ARRAY(Text), nullable=True, comment="Array of associated EMBL IDs."),
    Column("db_pir", ARRAY(Text), nullable=True, comment="Array of associated PIR IDs."),
    Column("db_emdb", ARRAY(Text), nullable=True, comment="Array of associated EMDB IDs."),
    Column("pdb_related", ARRAY(Text), nullable=True, comment="Array of associated PDB IDs."),
    Column("keywords", ARRAY(Text), nullable=True, comment="Array of keywords."),
    Column("aaseq", Text, nullable=True, comment="Amino acid sequence."),
    Column("update_date", DateTime, nullable=True, comment="Entry update date (within the RDB of any metadata, both regular wwPDB data and PDBj-generated plus data)."),
    Column("db_pfam", ARRAY(Text), nullable=True, comment="Array of associated PFam IDs."),
    Column("group_id", Text, nullable=True, comment="Deposition Group ID"),
    Column("plus_fields", JSONB, nullable=True),
    PrimaryKeyConstraint("pdbid"),
)

atom_sites = Table(
    "atom_sites",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("Cartn_transf_matrix11", Double, nullable=True),
    Column("Cartn_transf_matrix12", Double, nullable=True),
    Column("Cartn_transf_matrix13", Double, nullable=True),
    Column("Cartn_transf_matrix21", Double, nullable=True),
    Column("Cartn_transf_matrix22", Double, nullable=True),
    Column("Cartn_transf_matrix23", Double, nullable=True),
    Column("Cartn_transf_matrix31", Double, nullable=True),
    Column("Cartn_transf_matrix32", Double, nullable=True),
    Column("Cartn_transf_matrix33", Double, nullable=True),
    Column("Cartn_transf_vector1", Double, nullable=True),
    Column("Cartn_transf_vector2", Double, nullable=True),
    Column("Cartn_transf_vector3", Double, nullable=True),
    Column("fract_transf_matrix11", Double, nullable=True),
    Column("fract_transf_matrix12", Double, nullable=True),
    Column("fract_transf_matrix13", Double, nullable=True),
    Column("fract_transf_matrix21", Double, nullable=True),
    Column("fract_transf_matrix22", Double, nullable=True),
    Column("fract_transf_matrix23", Double, nullable=True),
    Column("fract_transf_matrix31", Double, nullable=True),
    Column("fract_transf_matrix32", Double, nullable=True),
    Column("fract_transf_matrix33", Double, nullable=True),
    Column("fract_transf_vector1", Double, nullable=True),
    Column("fract_transf_vector2", Double, nullable=True),
    Column("fract_transf_vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["Cartn_transform_axes", "special_details"]},
)

atom_sites_footnote = Table(
    "atom_sites_footnote",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="A code that identifies the footnote."),
    Column("text", Text, nullable=True, comment="The text of the footnote. Footnotes are used to describe an atom site or a group of atom sites in the ATOM_SITE list. For example, footnotes may be used to indicate atoms for which the electron density is very weak, or atoms for which static disorder has been modelled."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["text"]},
)

atom_type = Table(
    "atom_type",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("oxidation_number", Integer, nullable=True, comment="Formal oxidation state of this atom type in the structure."),
    Column("scat_Cromer_Mann_a1", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient a1 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_a2", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient a2 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_a3", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient a3 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_a4", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient a4 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_b1", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient b1 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_b2", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient b2 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_b3", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient b3 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_b4", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient b4 used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_Cromer_Mann_c", Double, nullable=True, comment="The Cromer-Mann scattering-factor coefficient c used to calculate the scattering factors for this atom type. Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("scat_dispersion_imag", Double, nullable=True, comment="The imaginary component of the anomalous-dispersion scattering factor, f'', in electrons for this atom type and the radiation identified by _diffrn_radiation_wavelength.id."),
    Column("scat_dispersion_real", Double, nullable=True, comment="The real component of the anomalous-dispersion scattering factor, f', in electrons for this atom type and the radiation identified by _diffrn_radiation_wavelength.id."),
    Column("scat_source", Text, nullable=True, comment="Reference to the source of the scattering factors or scattering lengths used for this atom type."),
    Column("symbol", Text, nullable=True, comment="The code used to identify the atom species (singular or plural) representing this atom type. Normally this code is the element symbol. The code may be composed of any character except an underscore with the additional proviso that digits designate an oxidation state and must be followed by a + or - character."),
    Column("pdbx_scat_Cromer_Mann_a5", Double, nullable=True, comment="Scattering-factor coefficient a5, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("pdbx_scat_Cromer_Mann_b5", Double, nullable=True, comment="Scattering-factor coefficient b5, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("pdbx_scat_Cromer_Mann_a6", Double, nullable=True, comment="Scattering-factor coefficient a6, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("pdbx_scat_Cromer_Mann_b6", Double, nullable=True, comment="Scattering-factor coefficient b6, used to calculate electron elastic atomic scattering factors for the defined atom type. Electron Elastic Scattering Factors Ref: International Tables for X-ray Crystallography (2006). Vol. C, Table 4.3.2.2, pp. 282-283. Cromer_Mann equation Ref: International Tables for X-ray Crystallography (1974). Vol. IV, Table 2.2B or: International Tables for Crystallography (2004). Vol. C, Tables 6.1.1.4 and 6.1.1.5."),
    Column("pdbx_scat_Z", Integer, nullable=True, comment="Atomic number of atom in scattering amplitude."),
    Column("pdbx_N_electrons", Integer, nullable=True, comment="Number of electrons in atom used in scattering factor"),
    PrimaryKeyConstraint("pdbid", "symbol"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "description",
            "scat_length_neutron",
            "scat_source",
            "scat_versus_stol_list",
            "scat_dispersion_source",
        ]
    },
)

audit = Table(
    "audit",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("creation_date", Date, nullable=True, comment="A date that the data block was created. The date format is yyyy-mm-dd."),
    Column("creation_method", Text, nullable=True, comment="A description of how data were entered into the data block."),
    Column("revision_id", Text, nullable=True, comment="The value of _audit.revision_id must uniquely identify a record in the AUDIT list."),
    Column("update_record", Text, nullable=True, comment="A record of any changes to the data block. The update format is a date (yyyy-mm-dd) followed by a description of the changes. The latest update entry is added to the bottom of this record."),
    PrimaryKeyConstraint("pdbid", "revision_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["creation_method", "update_record"]},
)

audit_author = Table(
    "audit_author",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("name", Text, nullable=True, comment="The name of an author of this data block. If there are multiple authors, _audit_author.name is looped with _audit_author.address. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s)."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="This data item defines the order of the author's name in the list of audit authors."),
    Column("identifier_ORCID", Text, nullable=True, comment="The Open Researcher and Contributor ID (ORCID)."),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["address", "name", "identifier_ORCID"]},
)

audit_conform = Table(
    "audit_conform",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("dict_location", Text, nullable=True, comment="A file name or uniform resource locator (URL) for the dictionary to which the current data block conforms."),
    Column("dict_name", Text, nullable=True, comment="The string identifying the highest-level dictionary defining data names used in this file."),
    Column("dict_version", Text, nullable=True, comment="The version number of the dictionary to which the current data block conforms."),
    PrimaryKeyConstraint("pdbid", "dict_name", "dict_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)

cell = Table(
    "cell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("angle_alpha", Double, nullable=True, comment="Unit-cell angle alpha of the reported structure in degrees."),
    Column("angle_alpha_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.angle_alpha."),
    Column("angle_beta", Double, nullable=True, comment="Unit-cell angle beta of the reported structure in degrees."),
    Column("angle_beta_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.angle_beta."),
    Column("angle_gamma", Double, nullable=True, comment="Unit-cell angle gamma of the reported structure in degrees."),
    Column("angle_gamma_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.angle_gamma."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("formula_units_Z", Integer, nullable=True, comment="The number of the formula units in the unit cell as specified by _chemical_formula.structural, _chemical_formula.moiety or _chemical_formula.sum."),
    Column("length_a", Double, nullable=True, comment="Unit-cell length a corresponding to the structure reported in angstroms."),
    Column("length_a_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.length_a."),
    Column("length_b", Double, nullable=True, comment="Unit-cell length b corresponding to the structure reported in angstroms."),
    Column("length_b_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.length_b."),
    Column("length_c", Double, nullable=True, comment="Unit-cell length c corresponding to the structure reported in angstroms."),
    Column("length_c_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.length_c."),
    Column("volume", Double, nullable=True, comment="Cell volume V in angstroms cubed. V = a b c (1 - cos^2^~alpha~ - cos^2^~beta~ - cos^2^~gamma~ + 2 cos~alpha~ cos~beta~ cos~gamma~)^1/2^ a = _cell.length_a b = _cell.length_b c = _cell.length_c alpha = _cell.angle_alpha beta = _cell.angle_beta gamma = _cell.angle_gamma"),
    Column("volume_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _cell.volume."),
    Column("Z_PDB", Integer, nullable=True, comment="The number of the polymeric chains in a unit cell. In the case of heteropolymers, Z is the number of occurrences of the most populous chain. This data item is provided for compatibility with the original Protein Data Bank format, and only for that purpose."),
    Column("reciprocal_angle_alpha", Double, nullable=True, comment="The angle (recip-alpha) defining the reciprocal cell in degrees. (recip-alpha), (recip-alpha) and (recip-alpha) related to the angles in the real cell by: cos(recip-alpha) = [cos(beta)*cos(gamma) - cos(alpha)]/[sin(beta)*sin(gamma)] cos(recip-beta) = [cos(gamma)*cos(alpha) - cos(beta)]/[sin(gamma)*sin(alpha)] cos(recip-gamma) = [cos(alpha)*cos(beta) - cos(gamma)]/[sin(alpha)*sin(beta)] Ref: Buerger, M. J. (1942). X-ray Crystallography, p. 360. New York: John Wiley & Sons Inc."),
    Column("reciprocal_angle_beta", Double, nullable=True, comment="The angle (recip-beta) defining the reciprocal cell in degrees. (recip-alpha), (recip-alpha) and (recip-alpha) related to the angles in the real cell by: cos(recip-alpha) = [cos(beta)*cos(gamma) - cos(alpha)]/[sin(beta)*sin(gamma)] cos(recip-beta) = [cos(gamma)*cos(alpha) - cos(beta)]/[sin(gamma)*sin(alpha)] cos(recip-gamma) = [cos(alpha)*cos(beta) - cos(gamma)]/[sin(alpha)*sin(beta)] Ref: Buerger, M. J. (1942). X-ray Crystallography, p. 360. New York: John Wiley & Sons Inc."),
    Column("reciprocal_angle_gamma", Double, nullable=True, comment="The angle (recip-gamma) defining the reciprocal cell in degrees. (recip-alpha), (recip-alpha) and (recip-alpha) related to the angles in the real cell by: cos(recip-alpha) = [cos(beta)*cos(gamma) - cos(alpha)]/[sin(beta)*sin(gamma)] cos(recip-beta) = [cos(gamma)*cos(alpha) - cos(beta)]/[sin(gamma)*sin(alpha)] cos(recip-gamma) = [cos(alpha)*cos(beta) - cos(gamma)]/[sin(alpha)*sin(beta)] Ref: Buerger, M. J. (1942). X-ray Crystallography, p. 360. New York: John Wiley & Sons Inc."),
    Column("pdbx_unique_axis", Text, nullable=True, comment="To further identify unique axis if necessary. E.g., P 21 with an unique C axis will have 'C' in this field."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "pdbx_unique_axis"]},
)

cell_measurement = Table(
    "cell_measurement",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("pressure", Double, nullable=True, comment="The pressure in kilopascals at which the unit-cell parameters were measured (not the pressure at which the sample was synthesized)."),
    Column("reflns_used", Integer, nullable=True, comment="The total number of reflections used to determine the unit cell. These reflections may be specified as CELL_MEASUREMENT_REFLN data items."),
    Column("theta_max", Double, nullable=True, comment="The maximum theta angle of reflections used to measure the unit cell in degrees."),
    Column("theta_min", Double, nullable=True, comment="The minimum theta angle of reflections used to measure the unit cell in degrees."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["radiation"]},
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("formula", Text, nullable=True, comment="The formula for the chemical component. Formulae are written according to the following rules: (1) Only recognized element symbols may be used. (2) Each element symbol is followed by a 'count' number. A count of '1' may be omitted. (3) A space or parenthesis must separate each cluster of (element symbol + count), but in general parentheses are not used. (4) The order of elements depends on whether carbon is present or not. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts."),
    Column("formula_weight", Double, nullable=True, comment="Formula mass in daltons of the chemical component."),
    Column("id", Text, nullable=True, comment="The value of _chem_comp.id must uniquely identify each item in the CHEM_COMP list. For protein polymer entities, this is the three-letter code for the amino acid. For nucleic acid polymer entities, this is the one-letter code for the base."),
    Column("mon_nstd_flag", Text, nullable=True, comment="'yes' indicates that this is a 'standard' monomer, 'no' indicates that it is 'nonstandard'. Nonstandard monomers should be described in more detail using the _chem_comp.mon_nstd_parent, _chem_comp.mon_nstd_class and _chem_comp.mon_nstd_details data items."),
    Column("name", Text, nullable=True, comment="The full name of the component."),
    Column("type", Text, nullable=True, comment="For standard polymer components, the type of the monomer. Note that monomers that will form polymers are of three types: linking monomers, monomers with some type of N-terminal (or 5') cap and monomers with some type of C-terminal (or 3') cap."),
    Column("pdbx_synonyms", Text, nullable=True, comment="Synonym list for the component."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "formula",
            "model_details",
            "model_erf",
            "model_source",
            "mon_nstd_class",
            "mon_nstd_details",
            "name",
            "pdbx_synonyms",
            "pdbx_modification_details",
            "pdbx_subcomponent_list",
            "pdbx_model_coordinates_details",
            "pdbx_model_coordinates_db_code",
            "pdbx_ideal_coordinates_details",
            "pdbx_class_1",
            "pdbx_class_2",
            "pdbx_reserved_name",
            "pdbx_casnum",
            "pdbx_smiles",
        ]
    },
)

chem_comp_atom = Table(
    "chem_comp_atom",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atom_id", Text, nullable=True, comment="The value of _chem_comp_atom.atom_id must uniquely identify each atom in each monomer in the CHEM_COMP_ATOM list. The atom identifiers need not be unique over all atoms in the data block; they need only be unique for each atom in a component. Note that this item need not be a number; it can be any unique identifier."),
    Column("comp_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("type_symbol", Text, nullable=True, comment="The code used to identify the atom species representing this atom type. Normally this code is the element symbol."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="Ordinal index for the component atom list."),
    Column("pdbx_stereo_config", Text, nullable=True, comment="The chiral configuration of the atom that is a chiral center."),
    Column("pdbx_aromatic_flag", Text, nullable=True, comment="A flag indicating an aromatic atom."),
    PrimaryKeyConstraint("pdbid", "comp_id", "atom_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
    info={"keywords": ["alt_atom_id", "pdbx_stnd_atom_id"]},
)

chem_comp_bond = Table(
    "chem_comp_bond",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atom_id_1", Text, nullable=True, comment="The ID of the first of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category."),
    Column("atom_id_2", Text, nullable=True, comment="The ID of the second of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category."),
    Column("comp_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("value_order", Text, nullable=True, comment="The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="Ordinal index for the component bond list."),
    Column("pdbx_stereo_config", Text, nullable=True, comment="Stereochemical configuration across a double bond."),
    Column("pdbx_aromatic_flag", Text, nullable=True, comment="A flag indicating an aromatic bond."),
    PrimaryKeyConstraint("pdbid", "comp_id", "atom_id_1", "atom_id_2"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id, atom_id_1) -> chem_comp_atom(pdbid, comp_id, atom_id)
    # FK: (pdbid, comp_id, atom_id_2) -> chem_comp_atom(pdbid, comp_id, atom_id)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
)

chem_link = Table(
    "chem_link",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _chem_link.id must uniquely identify each item in the CHEM_LINK list."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

citation = Table(
    "citation",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("abstract", Text, nullable=True, comment="Abstract for the citation. This is used most when the citation is extracted from a bibliographic database that contains full text or abstract information."),
    Column("book_id_ISBN", Text, nullable=True, comment="The International Standard Book Number (ISBN) code assigned to the book cited; relevant for books or book chapters."),
    Column("book_publisher", Text, nullable=True, comment="The name of the publisher of the citation; relevant for books or book chapters."),
    Column("book_publisher_city", Text, nullable=True, comment="The location of the publisher of the citation; relevant for books or book chapters."),
    Column("book_title", Text, nullable=True, comment="The title of the book in which the citation appeared; relevant for books or book chapters."),
    Column("coordinate_linkage", Text, nullable=True, comment="_citation.coordinate_linkage states whether this citation is concerned with precisely the set of coordinates given in the data block. If, for instance, the publication described the same structure, but the coordinates had undergone further refinement prior to the creation of the data block, the value of this data item would be 'no'."),
    Column("country", Text, nullable=True, comment="The country/region of publication; relevant for books and book chapters."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the relationship of the contents of the data block to the literature item cited."),
    Column("id", Text, nullable=True, comment="The value of _citation.id must uniquely identify a record in the CITATION list. The _citation.id 'primary' should be used to indicate the citation that the author(s) consider to be the most pertinent to the contents of the data block. Note that this item need not be a number; it can be any unique identifier."),
    Column("journal_abbrev", Text, nullable=True, comment="Abbreviated name of the cited journal as given in the Chemical Abstracts Service Source Index."),
    Column("journal_id_ASTM", Text, nullable=True, comment="The American Society for Testing and Materials (ASTM) code assigned to the journal cited (also referred to as the CODEN designator of the Chemical Abstracts Service); relevant for journal articles."),
    Column("journal_id_CSD", Text, nullable=True, comment="The Cambridge Structural Database (CSD) code assigned to the journal cited; relevant for journal articles. This is also the system used at the Protein Data Bank (PDB)."),
    Column("journal_id_ISSN", Text, nullable=True, comment="The International Standard Serial Number (ISSN) code assigned to the journal cited; relevant for journal articles."),
    Column("journal_issue", Text, nullable=True, comment="Issue number of the journal cited; relevant for journal articles."),
    Column("journal_volume", Text, nullable=True, comment="Volume number of the journal cited; relevant for journal articles."),
    Column("language", Text, nullable=True, comment="Language in which the cited article is written."),
    Column("page_first", Text, nullable=True, comment="The first page of the citation; relevant for journal articles, books and book chapters."),
    Column("page_last", Text, nullable=True, comment="The last page of the citation; relevant for journal articles, books and book chapters."),
    Column("title", Text, nullable=True, comment="The title of the citation; relevant for journal articles, books and book chapters."),
    Column("year", Integer, nullable=True, comment="The year of the citation; relevant for journal articles, books and book chapters."),
    Column("database_id_CSD", Text, nullable=True, comment="Identifier ('refcode') of the database record in the Cambridge Structural Database that contains details of the cited structure."),
    Column("pdbx_database_id_DOI", Text, nullable=True, comment="Document Object Identifier used by doi.org to uniquely specify bibliographic entry."),
    Column("pdbx_database_id_PubMed", Integer, nullable=True, comment="Ascession number used by PubMed to categorize a specific bibliographic entry."),
    Column("pdbx_database_id_patent", Text, nullable=True, comment="If citation is a patent, the accession issued by a patent office."),
    Column("unpublished_flag", Text, nullable=True, comment="Flag to indicate that this citation will not be published."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "abstract",
            "abstract_id_CAS",
            "book_id_ISBN",
            "book_publisher",
            "book_publisher_city",
            "book_title",
            "country",
            "details",
            "journal_abbrev",
            "journal_id_ASTM",
            "journal_id_CSD",
            "journal_id_ISSN",
            "journal_full",
            "journal_issue",
            "journal_volume",
            "language",
            "page_first",
            "page_last",
            "title",
            "pdbx_database_id_patent",
        ]
    },
)

citation_author = Table(
    "citation_author",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("citation_id", Text, nullable=True, comment="This data item is a pointer to _citation.id in the CITATION category."),
    Column("name", Text, nullable=True, comment="Name of an author of the citation; relevant for journal articles, books and book chapters. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s)."),
    Column("ordinal", Integer, nullable=True, comment="This data item defines the order of the author's name in the list of authors of a citation."),
    Column("identifier_ORCID", Text, nullable=True, comment="The Open Researcher and Contributor ID (ORCID)."),
    PrimaryKeyConstraint("pdbid", "citation_id", "name", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, citation_id) -> citation(pdbid, id)
    info={"keywords": ["name", "identifier_ORCID"]},
)

citation_editor = Table(
    "citation_editor",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("citation_id", Text, nullable=True, comment="This data item is a pointer to _citation.id in the CITATION category."),
    Column("name", Text, nullable=True, comment="Names of an editor of the citation; relevant for books and book chapters. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s)."),
    Column("ordinal", Integer, nullable=True, comment="This data item defines the order of the editor's name in the list of editors of a citation."),
    PrimaryKeyConstraint("pdbid", "citation_id", "name"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, citation_id) -> citation(pdbid, id)
    info={"keywords": ["name"]},
)

database_2 = Table(
    "database_2",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("database_id", Text, nullable=True, comment="An abbreviation that identifies the database."),
    Column("database_code", Text, nullable=True, comment="The code assigned by the database identified in _database_2.database_id."),
    Column("pdbx_database_accession", Text, nullable=True, comment="Extended accession code issued for for _database_2.database_code assigned by the database identified in _database_2.database_id."),
    Column("pdbx_DOI", Text, nullable=True, comment="Document Object Identifier (DOI) for this entry registered with http://crossref.org."),
    PrimaryKeyConstraint("pdbid", "database_id", "database_code"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["database_code", "pdbx_DOI"]},
)

database_PDB_caveat = Table(
    "database_PDB_caveat",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="A unique identifier for the PDB caveat record."),
    Column("text", Text, nullable=True, comment="The full text of the PDB caveat record."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["text"]},
)

database_PDB_matrix = Table(
    "database_PDB_matrix",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("origx11", Double, nullable=True),
    Column("origx12", Double, nullable=True),
    Column("origx13", Double, nullable=True),
    Column("origx21", Double, nullable=True),
    Column("origx22", Double, nullable=True),
    Column("origx23", Double, nullable=True),
    Column("origx31", Double, nullable=True),
    Column("origx32", Double, nullable=True),
    Column("origx33", Double, nullable=True),
    Column("origx_vector1", Double, nullable=True),
    Column("origx_vector2", Double, nullable=True),
    Column("origx_vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

database_PDB_tvect = Table(
    "database_PDB_tvect",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _database_PDB_tvect.id must uniquely identify a record in the DATABASE_PDB_TVECT list. Note that this item need not be a number; it can be any unique identifier."),
    Column("vector1", Double, nullable=True),
    Column("vector2", Double, nullable=True),
    Column("vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

diffrn = Table(
    "diffrn",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ambient_environment", Text, nullable=True, comment="The gas or liquid surrounding the sample, if not air."),
    Column("ambient_temp", Double, nullable=True, comment="The mean temperature in kelvins at which the intensities were measured."),
    Column("ambient_temp_details", Text, nullable=True, comment="A description of special aspects of temperature control during data collection."),
    Column("crystal_id", Text, nullable=True, comment="This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category."),
    Column("crystal_support", Text, nullable=True, comment="The physical device used to support the crystal during data collection."),
    Column("crystal_treatment", Text, nullable=True, comment="Remarks about how the crystal was treated prior to intensity measurement. Particularly relevant when intensities were measured at low temperature."),
    Column("details", Text, nullable=True, comment="Special details of the diffraction measurement process. Should include information about source instability, crystal motion, degradation and so on."),
    Column("id", Text, nullable=True, comment="This data item uniquely identifies a set of diffraction data."),
    Column("ambient_pressure", Double, nullable=True, comment="The mean hydrostatic pressure in kilopascals at which the intensities were measured."),
    Column("pdbx_serial_crystal_experiment", Text, nullable=True, comment="Y/N if using serial crystallography experiment in which multiple crystals contribute to each diffraction frame in the experiment."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
    info={
        "keywords": [
            "ambient_environment",
            "ambient_temp_details",
            "crystal_support",
            "crystal_treatment",
            "details",
        ]
    },
)

diffrn_detector = Table(
    "diffrn_detector",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the radiation detector."),
    Column("detector", Text, nullable=True, comment="The general class of the radiation detector."),
    Column("diffrn_id", Text, nullable=True, comment="This data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("type", Text, nullable=True, comment="The make, model or name of the detector device used."),
    Column("pdbx_collection_date", Text, nullable=True, comment="The date of data collection."),
    Column("pdbx_frequency", Double, nullable=True, comment="The operating frequency of the detector (Hz) used in data collection."),
    Column("id", Text, nullable=True, comment="The value of _diffrn_detector.id must uniquely identify each detector used to collect each diffraction data set. If the value of _diffrn_detector.id is not given, it is implicitly equal to the value of _diffrn_detector.diffrn_id."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["details", "detector", "type"]},
)

diffrn_measurement = Table(
    "diffrn_measurement",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="This data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the intensity measurement."),
    Column("method", Text, nullable=True, comment="Method used to measure intensities."),
    Column("specimen_support", Text, nullable=True, comment="The physical device used to support the crystal during data collection."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={
        "keywords": [
            "details",
            "device",
            "device_details",
            "device_type",
            "method",
            "specimen_support",
        ]
    },
)

diffrn_radiation = Table(
    "diffrn_radiation",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("collimation", Text, nullable=True, comment="The collimation or focusing applied to the radiation."),
    Column("diffrn_id", Text, nullable=True, comment="This data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("monochromator", Text, nullable=True, comment="The method used to obtain monochromatic radiation. If a mono- chromator crystal is used, the material and the indices of the Bragg reflection are specified."),
    Column("type", Text, nullable=True, comment="The nature of the radiation. This is typically a description of the X-ray wavelength in Siegbahn notation."),
    Column("wavelength_id", Text, nullable=True, comment="This data item is a pointer to _diffrn_radiation_wavelength.id in the DIFFRN_RADIATION_WAVELENGTH category."),
    Column("pdbx_monochromatic_or_laue_m_l", Text, nullable=True, comment="Monochromatic or Laue."),
    Column("pdbx_wavelength_list", Text, nullable=True, comment="Comma separated list of wavelengths or wavelength range."),
    Column("pdbx_wavelength", Text, nullable=True, comment="Wavelength of radiation."),
    Column("pdbx_diffrn_protocol", Text, nullable=True, comment="SINGLE WAVELENGTH, LAUE, or MAD."),
    Column("pdbx_analyzer", Text, nullable=True, comment="Indicates the method used to obtain monochromatic radiation. _diffrn_radiation.monochromator describes the primary beam monochromator (pre-specimen monochromation). _diffrn_radiation.pdbx_analyzer specifies the post-diffraction analyser (post-specimen) monochromation. Note that monochromators may have either 'parallel' or 'antiparallel' orientation. It is assumed that the geometry is parallel unless specified otherwise. In a parallel geometry, the position of the monochromator allows the incident beam and the final post-specimen and post-monochromator beam to be as close to parallel as possible. In a parallel geometry, the diffracting planes in the specimen and monochromator will be parallel when 2*theta(monochromator) is equal to 2*theta (specimen). For further discussion see R. Jenkins and R. Snyder, Introduction to X-ray Powder Diffraction, Wiley (1996), pp. 164-5."),
    Column("pdbx_scattering_type", Text, nullable=True, comment="The radiation scattering type for this diffraction data set."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={
        "keywords": [
            "collimation",
            "monochromator",
            "type",
            "pdbx_wavelength_list",
            "pdbx_wavelength",
            "pdbx_diffrn_protocol",
            "pdbx_analyzer",
        ]
    },
)

diffrn_radiation_wavelength = Table(
    "diffrn_radiation_wavelength",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The code identifying each value of _diffrn_radiation_wavelength.wavelength. Items in the DIFFRN_RADIATION_WAVELENGTH category are looped when multiple wavelengths are used. This code is used to link with the DIFFRN_REFLN category. The _diffrn_refln.wavelength_id codes must match one of the codes defined in this category."),
    Column("wavelength", Double, nullable=True, comment="The radiation wavelength in angstroms."),
    Column("wt", Double, nullable=True, comment="The relative weight of a wavelength identified by the code _diffrn_radiation_wavelength.id in the list of wavelengths."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

diffrn_reflns = Table(
    "diffrn_reflns",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("av_R_equivalents", Double, nullable=True, comment="The residual [sum|avdel(I)| / sum|av(I)|] for symmetry-equivalent reflections used to calculate the average intensity av(I). The avdel(I) term is the average absolute difference between av(I) and the individual symmetry-equivalent intensities."),
    Column("av_sigmaI_over_netI", Double, nullable=True, comment="Measure [sum|sigma(I)|/sum|net(I)|] for all measured reflections."),
    Column("diffrn_id", Text, nullable=True, comment="This data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("limit_h_max", Integer, nullable=True, comment="The maximum value of the Miller index h for the reflection data specified by _diffrn_refln.index_h."),
    Column("limit_h_min", Integer, nullable=True, comment="The minimum value of the Miller index h for the reflection data specified by _diffrn_refln.index_h."),
    Column("limit_k_max", Integer, nullable=True, comment="The maximum value of the Miller index k for the reflection data specified by _diffrn_refln.index_k."),
    Column("limit_k_min", Integer, nullable=True, comment="The minimum value of the Miller index k for the reflection data specified by _diffrn_refln.index_k."),
    Column("limit_l_max", Integer, nullable=True, comment="The maximum value of the Miller index l for the reflection data specified by _diffrn_refln.index_l."),
    Column("limit_l_min", Integer, nullable=True, comment="The minimum value of the Miller index l for the reflection data specified by _diffrn_refln.index_l."),
    Column("number", Integer, nullable=True, comment="The total number of measured intensities, excluding reflections that are classified as systematically absent."),
    Column("theta_max", Double, nullable=True, comment="Maximum theta angle in degrees for the measured diffraction intensities."),
    Column("theta_min", Double, nullable=True, comment="Minimum theta angle in degrees for the measured diffraction intensities."),
    Column("pdbx_d_res_low", Double, nullable=True, comment="The lowest resolution for the interplanar spacings in the reflection data set. This is the largest d value."),
    Column("pdbx_d_res_high", Double, nullable=True, comment="The highest resolution for the interplanar spacings in the reflection data set. This is the smallest d value."),
    Column("pdbx_percent_possible_obs", Double, nullable=True, comment="The percentage of geometrically possible reflections represented by reflections that satisfy the resolution limits established by _diffrn_reflns.d_resolution_high and _diffrn_reflns.d_resolution_low and the observation limit established by _diffrn_reflns.observed_criterion."),
    Column("pdbx_Rmerge_I_obs", Double, nullable=True, comment="The R factor for merging the reflections that satisfy the resolution limits established by _diffrn_reflns.d_resolution_high and _diffrn_reflns.d_resolution_low and the observation limit established by _diffrn_reflns.observed_criterion. Rmerge(I) = [sum~i~(sum~j~|I~j~ - |)] / [sum~i~(sum~j~)] I~j~ = the intensity of the jth observation of reflection i = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("pdbx_Rsym_value", Double, nullable=True, comment="The R factor for averaging the symmetry related reflections to a unique data set."),
    Column("pdbx_chi_squared", Double, nullable=True, comment="Overall Chi-squared statistic for the data set."),
    Column("pdbx_redundancy", Double, nullable=True, comment="The overall redundancy for the data set."),
    Column("pdbx_rejects", Integer, nullable=True, comment="The number of rejected reflections in the data set. The reflections may be rejected by setting the observation criterion, _diffrn_reflns.observed_criterion."),
    Column("pdbx_number_obs", Integer, nullable=True, comment="The number of reflections satisfying the observation criterion as in _diffrn_reflns.pdbx_observed_criterion"),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["reduction_process"]},
)

diffrn_source = Table(
    "diffrn_source",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("current", Double, nullable=True, comment="The current in milliamperes at which the radiation source was operated."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the radiation source used."),
    Column("diffrn_id", Text, nullable=True, comment="This data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("power", Double, nullable=True, comment="The power in kilowatts at which the radiation source was operated."),
    Column("size", Text, nullable=True, comment="The dimensions of the source as viewed from the sample."),
    Column("source", Text, nullable=True, comment="The general class of the radiation source."),
    Column("target", Text, nullable=True, comment="The chemical element symbol for the X-ray target (usually the anode) used to generate X-rays. This can also be used for spallation sources."),
    Column("type", Text, nullable=True, comment="The make, model or name of the source of radiation."),
    Column("voltage", Double, nullable=True, comment="The voltage in kilovolts at which the radiation source was operated."),
    Column("take-off_angle", Double, nullable=True),
    Column("pdbx_wavelength_list", Text, nullable=True, comment="Comma separated list of wavelengths or wavelength range."),
    Column("pdbx_wavelength", Text, nullable=True, comment="Wavelength of radiation."),
    Column("pdbx_synchrotron_beamline", Text, nullable=True, comment="Synchrotron beamline."),
    Column("pdbx_synchrotron_site", Text, nullable=True, comment="Synchrotron site."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={
        "keywords": [
            "details",
            "size",
            "source",
            "type",
            "pdbx_wavelength_list",
            "pdbx_wavelength",
            "pdbx_synchrotron_beamline",
            "pdbx_synchrotron_site",
            "pdbx_synchrotron_y_n",
            "pdbx_source_specific_beamline",
        ]
    },
)

entity = Table(
    "entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the entity."),
    Column("formula_weight", Double, nullable=True, comment="Formula mass in daltons of the entity."),
    Column("id", Text, nullable=True, comment="The value of _entity.id must uniquely identify a record in the ENTITY list. Note that this item need not be a number; it can be any unique identifier."),
    Column("src_method", Text, nullable=True, comment="The method by which the sample for the entity was produced. Entities isolated directly from natural sources (tissues, soil samples etc.) are expected to have further information in the ENTITY_SRC_NAT category. Entities isolated from genetically manipulated sources are expected to have further information in the ENTITY_SRC_GEN category."),
    Column("type", Text, nullable=True, comment="Defines the type of the entity. Polymer entities are expected to have corresponding ENTITY_POLY and associated entries. Non-polymer entities are expected to have corresponding CHEM_COMP and associated entries. Water entities are not expected to have corresponding entries in the ENTITY category."),
    Column("pdbx_description", Text, nullable=True, comment="A description of the entity. Corresponds to the compound name in the PDB format."),
    Column("pdbx_number_of_molecules", Integer, nullable=True, comment="A place holder for the number of molecules of the entity in the entry."),
    Column("pdbx_mutation", Text, nullable=True, comment="Details about any entity mutation(s)."),
    Column("pdbx_fragment", Text, nullable=True, comment="Entity fragment description(s)."),
    Column("pdbx_ec", Text, nullable=True, comment="Enzyme Commission (EC) number(s)"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "details",
            "pdbx_description",
            "pdbx_mutation",
            "pdbx_fragment",
            "pdbx_modification",
        ]
    },
)

entity_keywords = Table(
    "entity_keywords",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("text", Text, nullable=True, comment="Keywords describing this entity."),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={
        "keywords": [
            "text",
            "pdbx_mutation",
            "pdbx_fragment",
            "pdbx_ec",
            "pdbx_antibody_isotype",
        ]
    },
)

entity_name_com = Table(
    "entity_name_com",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("name", Text, nullable=True, comment="A common name for the entity."),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["name"]},
)

entity_name_sys = Table(
    "entity_name_sys",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("name", Text, nullable=True, comment="The systematic name for the entity."),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["name", "system"]},
)

entity_poly = Table(
    "entity_poly",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("nstd_linkage", Text, nullable=True, comment="A flag to indicate whether the polymer contains at least one monomer-to-monomer link different from that implied by _entity_poly.type."),
    Column("nstd_monomer", Text, nullable=True, comment="A flag to indicate whether the polymer contains at least one monomer that is not considered standard."),
    Column("type", Text, nullable=True, comment="The type of the polymer."),
    Column("pdbx_strand_id", Text, nullable=True, comment="The PDB strand/chain id(s) corresponding to this polymer entity."),
    Column("pdbx_seq_one_letter_code", Text, nullable=True, comment="Sequence of protein or nucleic acid polymer in standard one-letter codes of amino acids or nucleotides. Non-standard amino acids/nucleotides are represented by their Chemical Component Dictionary (CCD) codes in parenthesis. Deoxynucleotides are represented by the specially-assigned 2-letter CCD codes in parenthesis, with 'D' prefix added to their ribonucleotide counterparts. For hybrid polymer, each residue is represented by the code of its individual type. A cyclic polymer is represented in linear sequence from the chosen start to end. A for Alanine or Adenosine-5'-monophosphate C for Cysteine or Cytidine-5'-monophosphate D for Aspartic acid E for Glutamic acid F for Phenylalanine G for Glycine or Guanosine-5'-monophosphate H for Histidine I for Isoleucine or Inosinic Acid L for Leucine K for Lysine M for Methionine N for Asparagine or Unknown ribonucleotide O for Pyrrolysine P for Proline Q for Glutamine R for Arginine S for Serine T for Threonine U for Selenocysteine or Uridine-5'-monophosphate V for Valine W for Tryptophan Y for Tyrosine (DA) for 2'-deoxyadenosine-5'-monophosphate (DC) for 2'-deoxycytidine-5'-monophosphate (DG) for 2'-deoxyguanosine-5'-monophosphate (DT) for Thymidine-5'-monophosphate (MSE) for Selenomethionine (SEP) for Phosphoserine (TPO) for Phosphothreonine (PTR) for Phosphotyrosine (PCA) for Pyroglutamic acid (UNK) for Unknown amino acid (ACE) for Acetylation cap (NH2) for Amidation cap"),
    Column("pdbx_seq_one_letter_code_can", Text, nullable=True, comment="Canonical sequence of protein or nucleic acid polymer in standard one-letter codes of amino acids or nucleotides, corresponding to the sequence in _entity_poly.pdbx_seq_one_letter_code. Non-standard amino acids/nucleotides are represented by the codes of their parents if parent is specified in _chem_comp.mon_nstd_parent_comp_id, or by letter 'X' if parent is not specified. Deoxynucleotides are represented by their canonical one-letter codes of A, C, G, or T. For modifications with several parent amino acids, all corresponding parent amino acid codes will be listed (ex. chromophores)."),
    Column("pdbx_target_identifier", Text, nullable=True, comment="For Structural Genomics entries, the sequence's target identifier registered at the TargetTrack database."),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={
        "keywords": [
            "type_details",
            "pdbx_strand_id",
            "pdbx_target_identifier",
            "pdbx_seq_one_letter_code_sample",
            "pdbx_N_terminal_seq_one_letter_code",
            "pdbx_C_terminal_seq_one_letter_code",
            "pdbx_seq_three_letter_code",
            "pdbx_seq_db_id",
        ]
    },
)

entity_poly_seq = Table(
    "entity_poly_seq",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("hetero", Text, nullable=True, comment="A flag to indicate whether this monomer in the polymer is heterogeneous in sequence."),
    Column("mon_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("num", Integer, nullable=True, comment="The value of _entity_poly_seq.num must uniquely and sequentially identify a record in the ENTITY_POLY_SEQ list. Note that this item must be a number and that the sequence numbers must progress in increasing numerical order."),
    PrimaryKeyConstraint("pdbid", "entity_id", "num", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, mon_id) -> chem_comp(pdbid, id)
    # FK: (pdbid, entity_id) -> entity_poly(pdbid, entity_id)
)

entry = Table(
    "entry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _entry.id identifies the data block. Note that this item need not be a number; it can be any unique identifier."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

exptl = Table(
    "exptl",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("absorpt_correction_T_max", Double, nullable=True, comment="The maximum transmission factor for the crystal and radiation. The maximum and minimum transmission factors are also referred to as the absorption correction A or 1/A*."),
    Column("absorpt_correction_T_min", Double, nullable=True, comment="The minimum transmission factor for the crystal and radiation. The maximum and minimum transmission factors are also referred to as the absorption correction A or 1/A*."),
    Column("absorpt_correction_type", Text, nullable=True, comment="The absorption correction type and method. The value 'empirical' should NOT be used unless more detailed information is not available."),
    Column("absorpt_process_details", Text, nullable=True, comment="Description of the absorption process applied to the intensities. A literature reference should be supplied for psi-scan techniques."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("crystals_number", Integer, nullable=True, comment="The total number of crystals used in the measurement of intensities."),
    Column("details", Text, nullable=True, comment="Any special information about the experimental work prior to the intensity measurement. See also _exptl_crystal.preparation."),
    Column("method", Text, nullable=True, comment="The method used in the experiment."),
    Column("method_details", Text, nullable=True, comment="A description of special aspects of the experimental method."),
    PrimaryKeyConstraint("pdbid", "entry_id", "method"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["absorpt_process_details", "details", "method_details"]},
)

exptl_crystal = Table(
    "exptl_crystal",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("colour", Text, nullable=True, comment="The colour of the crystal."),
    Column("density_Matthews", Double, nullable=True, comment="The density of the crystal, expressed as the ratio of the volume of the asymmetric unit to the molecular mass of a monomer of the structure, in units of angstroms^3^ per dalton. Ref: Matthews, B. W. (1968). J. Mol. Biol. 33, 491-497."),
    Column("density_percent_sol", Double, nullable=True, comment="Density value P calculated from the crystal cell and contents, expressed as per cent solvent. P = 1 - (1.23 N MMass) / V N = the number of molecules in the unit cell MMass = the molecular mass of each molecule (gm/mole) V = the volume of the unit cell (A^3^) 1.23 = a conversion factor evaluated as: (0.74 cm^3^/g) (10^24^ A^3^/cm^3^) -------------------------------------- (6.02*10^23^) molecules/mole where 0.74 is an assumed value for the partial specific volume of the molecule"),
    Column("description", Text, nullable=True, comment="A description of the quality and habit of the crystal. The crystal dimensions should not normally be reported here; use instead the specific items in the EXPTL_CRYSTAL category relating to size for the gross dimensions of the crystal and data items in the EXPTL_CRYSTAL_FACE category to describe the relationship between individual faces."),
    Column("id", Text, nullable=True, comment="The value of _exptl_crystal.id must uniquely identify a record in the EXPTL_CRYSTAL list. Note that this item need not be a number; it can be any unique identifier."),
    Column("preparation", Text, nullable=True, comment="Details of crystal growth and preparation of the crystal (e.g. mounting) prior to the intensity measurements."),
    Column("density_meas", Double, nullable=True, comment="Density values measured using standard chemical and physical methods. The units are megagrams per cubic metre (grams per cubic centimetre)."),
    Column("pdbx_mosaicity", Double, nullable=True, comment="Isotropic approximation of the distribution of mis-orientation angles specified in degrees of all the mosaic domain blocks in the crystal, represented as a standard deviation. Here, a mosaic block is a set of contiguous unit cells assumed to be perfectly aligned. Lower mosaicity indicates better ordered crystals. See for example: Nave, C. (1998). Acta Cryst. D54, 848-853. Note that many software packages estimate the mosaic rotation distribution differently and may combine several physical properties of the experiment into a single mosaic term. This term will help fit the modeled spots to the observed spots without necessarily being directly related to the physics of the crystal itself."),
    Column("pdbx_mosaicity_esd", Double, nullable=True, comment="The uncertainty in the mosaicity estimate for the crystal."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "colour",
            "density_method",
            "description",
            "preparation",
            "pdbx_crystal_image_url",
            "pdbx_crystal_image_format",
            "pdbx_x-ray_image_type",
        ]
    },
)

exptl_crystal_grow = Table(
    "exptl_crystal_grow",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_id", Text, nullable=True, comment="This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the crystal growth."),
    Column("method", Text, nullable=True, comment="The method used to grow the crystals."),
    Column("pH", Double, nullable=True, comment="The pH at which the crystal was grown. If more than one pH was employed during the crystallization process, the final pH should be noted here and the protocol involving multiple pH values should be described in _exptl_crystal_grow.details."),
    Column("pressure", Double, nullable=True, comment="The ambient pressure in kilopascals at which the crystal was grown."),
    Column("seeding", Text, nullable=True, comment="A description of the protocol used for seeding the crystal growth."),
    Column("temp_details", Text, nullable=True, comment="A description of special aspects of temperature control during crystal growth."),
    Column("time", Text, nullable=True, comment="The approximate time that the crystal took to grow to the size used for data collection."),
    Column("pdbx_details", Text, nullable=True, comment="Text description of crystal growth procedure."),
    Column("pdbx_pH_range", Text, nullable=True, comment="The range of pH values at which the crystal was grown. Used when a point estimate of pH is not appropriate."),
    Column("temp", Double, nullable=True, comment="The temperature in kelvins at which the crystal was grown. If more than one temperature was employed during the crystallization process, the final temperature should be noted here and the protocol involving multiple temperatures should be described in _exptl_crystal_grow.details."),
    PrimaryKeyConstraint("pdbid", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
    info={
        "keywords": [
            "apparatus",
            "atmosphere",
            "details",
            "method",
            "method_ref",
            "seeding",
            "seeding_ref",
            "temp_details",
            "time",
            "pdbx_details",
            "pdbx_pH_range",
        ]
    },
)

exptl_crystal_grow_comp = Table(
    "exptl_crystal_grow_comp",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("conc", Text, nullable=True, comment="The concentration of the solution component."),
    Column("details", Text, nullable=True, comment="A description of any special aspects of the solution component. When the solution component is the one that contains the macromolecule, this could be the specification of the buffer in which the macromolecule was stored. When the solution component is a buffer component, this could be the methods (or formula) used to achieve a desired pH."),
    Column("crystal_id", Text, nullable=True, comment="This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category."),
    Column("id", Text, nullable=True, comment="The value of _exptl_crystal_grow_comp.id must uniquely identify each item in the EXPTL_CRYSTAL_GROW_COMP list. Note that this item need not be a number; it can be any unique identifier."),
    Column("name", Text, nullable=True, comment="A common name for the component of the solution."),
    Column("sol_id", Text, nullable=True, comment="An identifier for the solution to which the given solution component belongs."),
    Column("volume", Text, nullable=True, comment="The volume of the solution component."),
    PrimaryKeyConstraint("pdbid", "id", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
    info={
        "keywords": [
            "conc",
            "details",
            "id",
            "name",
            "sol_id",
            "volume",
            "pdbx_conc_final",
            "pdbx_bath",
            "pdbx_salt",
            "pdbx_soak_salt",
            "pdbx_soak_solv",
            "pdbx_solv",
        ]
    },
)

phasing = Table(
    "phasing",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("method", Text, nullable=True, comment="A listing of the method or methods used to phase this structure."),
    PrimaryKeyConstraint("pdbid", "method"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

phasing_MAD = Table(
    "phasing_MAD",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("pdbx_d_res_low", Double, nullable=True, comment="_phasing_MAD.pdbx_d_res_low records the lowest resolution for MAD phasing."),
    Column("pdbx_d_res_high", Double, nullable=True, comment="_phasing_MAD.pdbx_d_res_high records the highest resolution for MAD phasing."),
    Column("pdbx_reflns_acentric", Integer, nullable=True, comment="_phasing_MAD.pdbx_reflns_acentric records the number of acentric reflections for MAD phasing."),
    Column("pdbx_reflns_centric", Integer, nullable=True, comment="_phasing_MAD.pdbx_reflns_centric records the number of centric reflections for MAD phasing."),
    Column("pdbx_reflns", Integer, nullable=True, comment="_phasing_MAD.pdbx_reflns records the number of reflections used for MAD phasing."),
    Column("pdbx_fom_acentric", Double, nullable=True, comment="_phasing_MAD.pdbx_fom_acentric records the figure of merit using acentric data for MAD phasing."),
    Column("pdbx_fom_centric", Double, nullable=True, comment="_phasing_MAD.pdbx_fom_centric records the figure of merit using centric data for MAD phasing."),
    Column("pdbx_fom", Double, nullable=True, comment="_phasing_MAD.pdbx_fom records the figure of merit for MAD phasing."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "method", "pdbx_anom_scat_method"]},
)

phasing_MAD_clust = Table(
    "phasing_MAD_clust",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("expt_id", Text, nullable=True, comment="This data item is a pointer to _phasing_MAD_expt.id in the PHASING_MAD_EXPT category."),
    Column("id", Text, nullable=True, comment="The value of _phasing_MAD_clust.id must, together with _phasing_MAD_clust.expt_id, uniquely identify a record in the PHASING_MAD_CLUST list. Note that this item need not be a number; it can be any unique identifier."),
    PrimaryKeyConstraint("pdbid", "expt_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, expt_id) -> phasing_MAD_expt(pdbid, id)
    info={"keywords": ["expt_id", "id"]},
)

phasing_MAD_expt = Table(
    "phasing_MAD_expt",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _phasing_MAD_expt.id must uniquely identify each record in the PHASING_MAD_EXPT list."),
    Column("mean_fom", Double, nullable=True, comment="The mean figure of merit."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["id"]},
)

phasing_MAD_set = Table(
    "phasing_MAD_set",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("clust_id", Text, nullable=True, comment="This data item is a pointer to _phasing_MAD_clust.id in the PHASING_MAD_CLUST category."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value for the interplanar spacings for the reflection data used for this set of data. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value for the interplanar spacings for the reflection data used for this set of data. This is called the lowest resolution."),
    Column("expt_id", Text, nullable=True, comment="This data item is a pointer to _phasing_MAD_expt.id in the PHASING_MAD_EXPT category."),
    Column("f_double_prime", Double, nullable=True, comment="The f'' component of the anomalous scattering factor for this wavelength."),
    Column("f_prime", Double, nullable=True, comment="The f' component of the anomalous scattering factor for this wavelength."),
    Column("set_id", Text, nullable=True, comment="This data item is a pointer to _phasing_set.id in the PHASING_SET category."),
    Column("wavelength", Double, nullable=True, comment="The wavelength at which this data set was measured."),
    Column("pdbx_atom_type", Text, nullable=True, comment="record the type of heavy atoms which produce anomolous singal."),
    Column("pdbx_f_prime_refined", Double, nullable=True, comment="record the refined f_prime (not from experiment)."),
    Column("pdbx_f_double_prime_refined", Double, nullable=True, comment="record the refined f_double_prime (not from experiment)."),
    PrimaryKeyConstraint("pdbid", "expt_id", "clust_id", "set_id", "wavelength"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, expt_id) -> phasing_MAD_expt(pdbid, id)
    # FK: (pdbid, set_id) -> phasing_set(pdbid, id)
    info={"keywords": ["clust_id", "expt_id", "set_id", "wavelength_details"]},
)

phasing_MIR = Table(
    "phasing_MIR",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the isomorphous-replacement phasing."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value in angstroms for the interplanar spacings for the reflection data used for the native data set. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value in angstroms for the interplanar spacings for the reflection data used for the native data set. This is called the lowest resolution."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("FOM", Double, nullable=True, comment="The mean value of the figure of merit m for all reflections phased in the native data set. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi."),
    Column("FOM_acentric", Double, nullable=True, comment="The mean value of the figure of merit m for the acentric reflections phased in the native data set. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi."),
    Column("FOM_centric", Double, nullable=True, comment="The mean value of the figure of merit m for the centric reflections phased in the native data set. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi."),
    Column("reflns", Integer, nullable=True, comment="The total number of reflections phased in the native data set."),
    Column("reflns_acentric", Integer, nullable=True, comment="The number of acentric reflections phased in the native data set."),
    Column("reflns_centric", Integer, nullable=True, comment="The number of centric reflections phased in the native data set."),
    Column("reflns_criterion", Text, nullable=True, comment="Criterion used to limit the reflections used in the phasing calculations."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "method", "reflns_criterion"]},
)

phasing_MIR_der = Table(
    "phasing_MIR_der",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value for the interplanar spacings for the reflection data used for this derivative. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value for the interplanar spacings for the reflection data used for this derivative. This is called the lowest resolution."),
    Column("der_set_id", Text, nullable=True, comment="The data set that was treated as the derivative in this experiment. This data item is a pointer to _phasing_set.id in the PHASING_SET category."),
    Column("id", Text, nullable=True, comment="The value of _phasing_MIR_der.id must uniquely identify a record in the PHASING_MIR_DER list. Note that this item need not be a number; it can be any unique identifier."),
    Column("native_set_id", Text, nullable=True, comment="The data set that was treated as the native in this experiment. This data item is a pointer to _phasing_set.id in the PHASING_SET category."),
    Column("number_of_sites", Integer, nullable=True, comment="The number of heavy-atom sites in this derivative."),
    Column("power_acentric", Double, nullable=True, comment="The mean phasing power P for acentric reflections for this derivative. sum|Fh~calc~^2^| P = (----------------------------)^1/2^ sum|Fph~obs~ - Fph~calc~|^2^ Fph~obs~ = the observed structure-factor amplitude of this derivative Fph~calc~ = the calculated structure-factor amplitude of this derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections"),
    Column("power_centric", Double, nullable=True, comment="The mean phasing power P for centric reflections for this derivative. sum|Fh~calc~^2^| P = (----------------------------)^1/2^ sum|Fph~obs~ - Fph~calc~|^2^ Fph~obs~ = the observed structure-factor amplitude of the derivative Fph~calc~ = the calculated structure-factor amplitude of the derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections"),
    Column("R_cullis_acentric", Double, nullable=True, comment="Residual factor R~cullis,acen~ for acentric reflections for this derivative. The Cullis R factor was originally defined only for centric reflections. It is, however, also a useful statistical measure for acentric reflections, which is how it is used in this data item. sum| |Fph~obs~ +/- Fp~obs~| - Fh~calc~ | R~cullis,acen~ = ---------------------------------------- sum|Fph~obs~ - Fp~obs~| Fp~obs~ = the observed structure-factor amplitude of the native Fph~obs~ = the observed structure-factor amplitude of the derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections Ref: Cullis, A. F., Muirhead, H., Perutz, M. F., Rossmann, M. G. & North, A. C. T. (1961). Proc. R. Soc. London Ser. A, 265, 15-38."),
    Column("R_cullis_anomalous", Double, nullable=True, comment="Residual factor R~cullis,ano~ for anomalous reflections for this derivative. The Cullis R factor was originally defined only for centric reflections. It is, however, also a useful statistical measure for anomalous reflections, which is how it is used in this data item. This is tabulated for acentric terms. A value less than 1.0 means there is some contribution to the phasing from the anomalous data. sum |Fph+~obs~Fph-~obs~ - Fh+~calc~ - Fh-~calc~| R~cullis,ano~ = ------------------------------------------------ sum|Fph+~obs~ - Fph-~obs~| Fph+~obs~ = the observed positive Friedel structure-factor amplitude for the derivative Fph-~obs~ = the observed negative Friedel structure-factor amplitude for the derivative Fh+~calc~ = the calculated positive Friedel structure-factor amplitude from the heavy-atom model Fh-~calc~ = the calculated negative Friedel structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections Ref: Cullis, A. F., Muirhead, H., Perutz, M. F., Rossmann, M. G. & North, A. C. T. (1961). Proc. R. Soc. London Ser. A, 265, 15-38."),
    Column("R_cullis_centric", Double, nullable=True, comment="Residual factor R~cullis~ for centric reflections for this derivative. sum| |Fph~obs~ +/- Fp~obs~| - Fh~calc~ | R~cullis~ = ---------------------------------------- sum|Fph~obs~ - Fp~obs~| Fp~obs~ = the observed structure-factor amplitude of the native Fph~obs~ = the observed structure-factor amplitude of the derivative Fh~calc~ = the calculated structure-factor amplitude from the heavy-atom model sum is taken over the specified reflections Ref: Cullis, A. F., Muirhead, H., Perutz, M. F., Rossmann, M. G. & North, A. C. T. (1961). Proc. R. Soc. London Ser. A, 265, 15-38."),
    Column("reflns_acentric", Integer, nullable=True, comment="The number of acentric reflections used in phasing for this derivative."),
    Column("reflns_anomalous", Integer, nullable=True, comment="The number of anomalous reflections used in phasing for this derivative."),
    Column("reflns_centric", Integer, nullable=True, comment="The number of centric reflections used in phasing for this derivative."),
    Column("reflns_criteria", Text, nullable=True, comment="Criteria used to limit the reflections used in the phasing calculations."),
    Column("pdbx_loc_centric", Double, nullable=True, comment="record lack of closure obtained from centric data for each derivative."),
    Column("pdbx_loc_acentric", Double, nullable=True, comment="record lack of closure obtained from acentric data for each derivative."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, der_set_id) -> phasing_set(pdbid, id)
    # FK: (pdbid, native_set_id) -> phasing_set(pdbid, id)
    info={
        "keywords": ["der_set_id", "details", "id", "native_set_id", "reflns_criteria"]
    },
)

phasing_MIR_der_shell = Table(
    "phasing_MIR_der_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value for the interplanar spacings for the reflection data for this derivative in this shell. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value for the interplanar spacings for the reflection data for this derivative in this shell. This is called the lowest resolution."),
    Column("der_id", Text, nullable=True, comment="This data item is a pointer to _phasing_MIR_der.id in the PHASING_MIR_DER category."),
    Column("pdbx_R_cullis_centric", Double, nullable=True, comment="record R Cullis obtained from centric data for each derivative, but broken into resolution shells"),
    Column("pdbx_R_cullis_acentric", Double, nullable=True, comment="record R Cullis obtained from acentric data for each derivative, but broken into resolution shells"),
    Column("pdbx_loc_centric", Double, nullable=True, comment="record lack of closure obtained from centric data for each derivative, but broken into resolution shells"),
    Column("pdbx_loc_acentric", Double, nullable=True, comment="record lack of closure obtained from acentric data for each derivative, but broken into resolution shells"),
    Column("pdbx_power_centric", Double, nullable=True, comment="record phasing power obtained from centric data for each derivative, but broken into resolution shells"),
    Column("pdbx_power_acentric", Double, nullable=True, comment="record phasing power obtained from acentric data for each derivative, but broken into resolution shells"),
    Column("pdbx_reflns_centric", Double, nullable=True, comment="record number of centric reflections used for phasing for each derivative, but broken into resolution shells"),
    Column("pdbx_reflns_acentric", Integer, nullable=True, comment="record number of acentric reflections used for phasing for each derivative, but broken into resolution shells"),
    PrimaryKeyConstraint("pdbid", "der_id", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, der_id) -> phasing_MIR_der(pdbid, id)
    info={"keywords": ["der_id"]},
)

phasing_MIR_der_site = Table(
    "phasing_MIR_der_site",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atom_type_symbol", Text, nullable=True, comment="This data item is a pointer to _atom_type.symbol in the ATOM_TYPE category. The scattering factors referenced via this data item should be those used in the refinement of the heavy-atom data; in some cases this is the scattering factor for the single heavy atom, in other cases these are the scattering factors for an atomic cluster."),
    Column("B_iso", Double, nullable=True, comment="Isotropic displacement parameter for this heavy-atom site in this derivative."),
    Column("Cartn_x", Double, nullable=True, comment="The x coordinate of this heavy-atom position in this derivative specified as orthogonal angstroms. The orthogonal Cartesian axes are related to the cell axes as specified by the description given in _atom_sites.Cartn_transform_axes."),
    Column("Cartn_y", Double, nullable=True, comment="The y coordinate of this heavy-atom position in this derivative specified as orthogonal angstroms. The orthogonal Cartesian axes are related to the cell axes as specified by the description given in _atom_sites.Cartn_transform_axes."),
    Column("Cartn_z", Double, nullable=True, comment="The z coordinate of this heavy-atom position in this derivative specified as orthogonal angstroms. The orthogonal Cartesian axes are related to the cell axes as specified by the description given in _atom_sites.Cartn_transform_axes."),
    Column("der_id", Text, nullable=True, comment="This data item is a pointer to _phasing_MIR_der.id in the PHASING_MIR_DER category."),
    Column("fract_x", Double, nullable=True, comment="The x coordinate of this heavy-atom position in this derivative specified as a fraction of _cell.length_a."),
    Column("fract_y", Double, nullable=True, comment="The y coordinate of this heavy-atom position in this derivative specified as a fraction of _cell.length_b."),
    Column("fract_z", Double, nullable=True, comment="The z coordinate of this heavy-atom position in this derivative specified as a fraction of _cell.length_c."),
    Column("id", Text, nullable=True, comment="The value of _phasing_MIR_der_site.id must uniquely identify each site in each derivative in the PHASING_MIR_DER_SITE list. The atom identifiers need not be unique over all sites in all derivatives; they need only be unique for each site in each derivative. Note that this item need not be a number; it can be any unique identifier."),
    Column("occupancy", Double, nullable=True, comment="The fraction of the atom type present at this heavy-atom site in a given derivative. The sum of the occupancies of all the atom types at this site may not significantly exceed 1.0 unless it is a dummy site."),
    Column("occupancy_anom", Double, nullable=True, comment="The relative anomalous occupancy of the atom type present at this heavy-atom site in a given derivative. This atom occupancy will probably be on an arbitrary scale."),
    Column("occupancy_anom_su", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _phasing_MIR_der_site.occupancy_anom."),
    Column("occupancy_iso", Double, nullable=True, comment="The relative real isotropic occupancy of the atom type present at this heavy-atom site in a given derivative. This atom occupancy will probably be on an arbitrary scale."),
    Column("occupancy_iso_su", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _phasing_MIR_der_site.occupancy_iso."),
    PrimaryKeyConstraint("pdbid", "der_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, der_id) -> phasing_MIR_der(pdbid, id)
    info={"keywords": ["der_id", "details"]},
)

phasing_MIR_shell = Table(
    "phasing_MIR_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value for the interplanar spacings for the reflection data in this shell. This is called the highest resolution. Note that the resolution limits of shells in the items _phasing_MIR_shell.d_res_high and _phasing_MIR_shell.d_res_low are independent of the resolution limits of shells in the items _reflns_shell.d_res_high and _reflns_shell.d_res_low."),
    Column("d_res_low", Double, nullable=True, comment="The highest value for the interplanar spacings for the reflection data in this shell. This is called the lowest resolution. Note that the resolution limits of shells in the items _phasing_MIR_shell.d_res_high and _phasing_MIR_shell.d_res_low are independent of the resolution limits of shells in the items _reflns_shell.d_res_high and _reflns_shell.d_res_low."),
    Column("FOM", Double, nullable=True, comment="The mean value of the figure of merit m for reflections in this shell. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~alpha~ = the probability that the phase angle alpha is correct the integral is taken over the range alpha = 0 to 2 pi."),
    Column("FOM_acentric", Double, nullable=True, comment="The mean value of the figure of merit m for acentric reflections in this shell. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi."),
    Column("FOM_centric", Double, nullable=True, comment="The mean value of the figure of merit m for centric reflections in this shell. int P~alpha~ exp(i*alpha) dalpha m = -------------------------------- int P~alpha~ dalpha P~a~ = the probability that the phase angle a is correct the integral is taken over the range alpha = 0 to 2 pi."),
    Column("reflns", Integer, nullable=True, comment="The number of reflections in this shell."),
    Column("reflns_acentric", Integer, nullable=True, comment="The number of acentric reflections in this shell."),
    Column("reflns_centric", Integer, nullable=True, comment="The number of centric reflections in this shell."),
    PrimaryKeyConstraint("pdbid", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

phasing_set = Table(
    "phasing_set",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("cell_angle_alpha", Double, nullable=True, comment="Unit-cell angle alpha for this data set in degrees."),
    Column("cell_angle_beta", Double, nullable=True, comment="Unit-cell angle beta for this data set in degrees."),
    Column("cell_angle_gamma", Double, nullable=True, comment="Unit-cell angle gamma for this data set in degrees."),
    Column("cell_length_a", Double, nullable=True, comment="Unit-cell length a for this data set in angstroms."),
    Column("cell_length_b", Double, nullable=True, comment="Unit-cell length b for this data set in angstroms."),
    Column("cell_length_c", Double, nullable=True, comment="Unit-cell length c for this data set in angstroms."),
    Column("id", Text, nullable=True, comment="The value of _phasing_set.id must uniquely identify a record in the PHASING_SET list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_d_res_high", Double, nullable=True, comment="The smallest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the highest resolution."),
    Column("pdbx_d_res_low", Double, nullable=True, comment="The highest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the lowest resolution."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "detector_specific",
            "detector_type",
            "id",
            "radiation_source_specific",
            "pdbx_temp_details",
        ]
    },
)

publ = Table(
    "publ",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("section_references", Text, nullable=True, comment="The references section of a manuscript if the manuscript is submitted in parts. As an alternative see _publ.manuscript_text and _publ.manuscript_processed."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "contact_author",
            "contact_author_address",
            "contact_author_email",
            "contact_author_fax",
            "contact_author_name",
            "contact_author_phone",
            "contact_letter",
            "manuscript_creation",
            "manuscript_processed",
            "manuscript_text",
            "requested_coeditor_name",
            "requested_journal",
            "section_abstract",
            "section_acknowledgements",
            "section_comment",
            "section_discussion",
            "section_experimental",
            "section_exptl_prep",
            "section_exptl_refinement",
            "section_exptl_solution",
            "section_figure_captions",
            "section_introduction",
            "section_references",
            "section_synopsis",
            "section_table_legends",
            "section_title",
            "section_title_footnote",
        ]
    },
)

refine = Table(
    "refine",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("aniso_B11", Double, nullable=True),
    Column("aniso_B12", Double, nullable=True),
    Column("aniso_B13", Double, nullable=True),
    Column("aniso_B22", Double, nullable=True),
    Column("aniso_B23", Double, nullable=True),
    Column("aniso_B33", Double, nullable=True),
    Column("B_iso_max", Double, nullable=True, comment="The maximum isotropic displacement parameter (B value) found in the coordinate set."),
    Column("B_iso_mean", Double, nullable=True, comment="The mean isotropic displacement parameter (B value) for the coordinate set."),
    Column("B_iso_min", Double, nullable=True, comment="The minimum isotropic displacement parameter (B value) found in the coordinate set."),
    Column("correlation_coeff_Fo_to_Fc", Double, nullable=True, comment="The correlation coefficient between the observed and calculated structure factors for reflections included in the refinement. The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections included in the refinement"),
    Column("correlation_coeff_Fo_to_Fc_free", Double, nullable=True, comment="The correlation coefficient between the observed and calculated structure factors for reflections not included in the refinement (free reflections). The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections not included in the refinement (free reflections)"),
    Column("details", Text, nullable=True, comment="Description of special aspects of the refinement process."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("ls_d_res_high", Double, nullable=True, comment="The smallest value for the interplanar spacings for the reflection data used in the refinement in angstroms. This is called the highest resolution."),
    Column("ls_d_res_low", Double, nullable=True, comment="The largest value for the interplanar spacings for the reflection data used in the refinement in angstroms. This is called the lowest resolution."),
    Column("ls_extinction_coef_esd", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _refine.ls_extinction_coef."),
    Column("ls_goodness_of_fit_all", Double, nullable=True, comment="The least-squares goodness-of-fit parameter S for all data after the final cycle of refinement. Ideally, account should be taken of parameters restrained in the least-squares refinement. See also the definition of _refine.ls_restrained_S_all. ( sum|w |Y~obs~ - Y~calc~|^2^| )^1/2^ S = ( ---------------------------- ) ( N~ref~ - N~param~ ) Y~obs~ = the observed coefficients (see _refine.ls_structure_factor_coef) Y~calc~ = the calculated coefficients (see _refine.ls_structure_factor_coef) w = the least-squares reflection weight [1/(e.s.d. squared)] N~ref~ = the number of reflections used in the refinement N~param~ = the number of refined parameters sum is taken over the specified reflections"),
    Column("ls_hydrogen_treatment", Text, nullable=True, comment="Treatment of hydrogen atoms in the least-squares refinement."),
    Column("ls_matrix_type", Text, nullable=True, comment="Type of matrix used to accumulate the least-squares derivatives."),
    Column("ls_number_constraints", Integer, nullable=True, comment="The number of constrained (non-refined or dependent) parameters in the least-squares process. These may be due to symmetry or any other constraint process (e.g. rigid-body refinement). See also _atom_site.constraints and _atom_site.refinement_flags. A general description of constraints may appear in _refine.details."),
    Column("ls_number_parameters", Integer, nullable=True, comment="The number of parameters refined in the least-squares process. If possible, this number should include some contribution from the restrained parameters. The restrained parameters are distinct from the constrained parameters (where one or more parameters are linearly dependent on the refined value of another). Least-squares restraints often depend on geometry or energy considerations and this makes their direct contribution to this number, and to the goodness-of-fit calculation, difficult to assess."),
    Column("ls_number_reflns_all", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low."),
    Column("ls_number_reflns_obs", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion."),
    Column("ls_number_reflns_R_free", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details."),
    Column("ls_number_reflns_R_work", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details."),
    Column("ls_number_restraints", Integer, nullable=True, comment="The number of restrained parameters. These are parameters which are not directly dependent on another refined parameter. Restrained parameters often involve geometry or energy dependencies. See also _atom_site.constraints and _atom_site.refinement_flags. A general description of refinement constraints may appear in _refine.details."),
    Column("ls_percent_reflns_obs", Double, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, expressed as a percentage of the number of geometrically observable reflections that satisfy the resolution limits."),
    Column("ls_percent_reflns_R_free", Double, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor, expressed as a percentage of the number of geometrically observable reflections that satisfy the resolution limits."),
    Column("ls_R_factor_all", Double, nullable=True, comment="Residual factor R for all reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("ls_R_factor_obs", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion. _refine.ls_R_factor_obs should not be confused with _refine.ls_R_factor_R_work; the former reports the results of a refinement in which all observed reflections were used, the latter a refinement in which a subset of the observed reflections were excluded from refinement for the calculation of a 'free' R factor. However, it would be meaningful to quote both values if a 'free' R factor were calculated for most of the refinement, but all of the observed reflections were used in the final rounds of refinement; such a protocol should be explained in _refine.details. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("ls_R_factor_R_free", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("ls_R_factor_R_free_error", Double, nullable=True, comment="The estimated error in _refine.ls_R_factor_R_free. The method used to estimate the error is described in the item _refine.ls_R_factor_R_free_error_details."),
    Column("ls_R_factor_R_free_error_details", Text, nullable=True, comment="Special aspects of the method used to estimated the error in _refine.ls_R_factor_R_free."),
    Column("ls_R_factor_R_work", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. _refine.ls_R_factor_obs should not be confused with _refine.ls_R_factor_R_work; the former reports the results of a refinement in which all observed reflections were used, the latter a refinement in which a subset of the observed reflections were excluded from refinement for the calculation of a 'free' R factor. However, it would be meaningful to quote both values if a 'free' R factor were calculated for most of the refinement, but all of the observed reflections were used in the final rounds of refinement; such a protocol should be explained in _refine.details. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("ls_redundancy_reflns_all", Double, nullable=True, comment="The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low to the number of crystallographically unique reflections that satisfy the same limits."),
    Column("ls_redundancy_reflns_obs", Double, nullable=True, comment="The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion to the number of crystallographically unique reflections that satisfy the same limits."),
    Column("ls_wR_factor_all", Double, nullable=True, comment="Weighted residual factor wR for all reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low. ( sum|w |Y~obs~ - Y~calc~|^2^| )^1/2^ wR = ( ---------------------------- ) ( sum|w Y~obs~^2^| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections"),
    Column("ls_wR_factor_R_free", Double, nullable=True, comment="Weighted residual factor wR for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. ( sum|w |Y~obs~ - Y~calc~|^2^| )^1/2^ wR = ( ---------------------------- ) ( sum|w Y~obs~^2^| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections"),
    Column("ls_wR_factor_R_work", Double, nullable=True, comment="Weighted residual factor wR for reflections that satisfy the resolution limits established by _refine.ls_d_res_high and _refine.ls_d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. ( sum|w |Y~obs~ - Y~calc~|^2^| )^1/2^ wR = ( ---------------------------- ) ( sum|w Y~obs~^2^| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections"),
    Column("occupancy_max", Double, nullable=True, comment="The maximum value for occupancy found in the coordinate set."),
    Column("occupancy_min", Double, nullable=True, comment="The minimum value for occupancy found in the coordinate set."),
    Column("solvent_model_details", Text, nullable=True, comment="Special aspects of the solvent model used during refinement."),
    Column("solvent_model_param_bsol", Double, nullable=True, comment="The value of the BSOL solvent-model parameter describing the average isotropic displacement parameter of disordered solvent atoms. This is one of the two parameters (the other is _refine.solvent_model_param_ksol) in Tronrud's method of modelling the contribution of bulk solvent to the scattering. The standard scale factor is modified according to the expression k0 exp(-B0 * s^2^)[1-KSOL * exp(-BSOL * s^2^)] where k0 and B0 are the scale factors for the protein. Ref: Tronrud, D. E. (1997). Methods Enzymol. 277, 243-268."),
    Column("solvent_model_param_ksol", Double, nullable=True, comment="The value of the KSOL solvent-model parameter describing the ratio of the electron density in the bulk solvent to the electron density in the molecular solute. This is one of the two parameters (the other is _refine.solvent_model_param_bsol) in Tronrud's method of modelling the contribution of bulk solvent to the scattering. The standard scale factor is modified according to the expression k0 exp(-B0 * s^2^)[1-KSOL * exp(-BSOL * s^2^)] where k0 and B0 are the scale factors for the protein. Ref: Tronrud, D. E. (1997). Methods Enzymol. 277, 243-268."),
    Column("pdbx_ls_sigma_I", Double, nullable=True, comment="Data cutoff (SIGMA(I))"),
    Column("pdbx_ls_sigma_F", Double, nullable=True, comment="Data cutoff (SIGMA(F))"),
    Column("pdbx_ls_sigma_Fsqd", Double, nullable=True, comment="Data cutoff (SIGMA(F^2))"),
    Column("pdbx_data_cutoff_high_absF", Double, nullable=True, comment="Value of F at \"high end\" of data cutoff."),
    Column("pdbx_data_cutoff_high_rms_absF", Double, nullable=True, comment="Value of RMS |F| used as high data cutoff."),
    Column("pdbx_data_cutoff_low_absF", Double, nullable=True, comment="Value of F at \"low end\" of data cutoff."),
    Column("pdbx_isotropic_thermal_model", Text, nullable=True, comment="Whether the structure was refined with indvidual isotropic, anisotropic or overall temperature factor."),
    Column("pdbx_ls_cross_valid_method", Text, nullable=True, comment="Whether the cross validataion method was used through out or only at the end."),
    Column("pdbx_method_to_determine_struct", Text, nullable=True, comment="Method(s) used to determine the structure."),
    Column("pdbx_starting_model", Text, nullable=True, comment="Starting model for refinement. Starting model for molecular replacement should refer to a previous structure or experiment."),
    Column("pdbx_stereochemistry_target_values", Text, nullable=True, comment="Stereochemistry target values used in refinement."),
    Column("pdbx_R_Free_selection_details", Text, nullable=True, comment="Details of the manner in which the cross validation reflections were selected."),
    Column("pdbx_stereochem_target_val_spec_case", Text, nullable=True, comment="Special case of stereochemistry target values used in SHELXL refinement."),
    Column("pdbx_overall_ESU_R", Double, nullable=True, comment="Overall estimated standard uncertainties of positional parameters based on R value."),
    Column("pdbx_overall_ESU_R_Free", Double, nullable=True, comment="Overall estimated standard uncertainties of positional parameters based on R free value."),
    Column("pdbx_solvent_vdw_probe_radii", Double, nullable=True, comment="For bulk solvent mask calculation, the value by which the vdw radii of non-ion atoms (like carbon) are increased and used."),
    Column("pdbx_solvent_ion_probe_radii", Double, nullable=True, comment="For bulk solvent mask calculation, the amount that the ionic radii of atoms, which can be ions, are increased used."),
    Column("pdbx_solvent_shrinkage_radii", Double, nullable=True, comment="For bulk solvent mask calculation, amount mask is shrunk after taking away atoms with new radii and a constant value assigned to this new region."),
    Column("pdbx_pd_number_of_powder_patterns", Integer, nullable=True, comment="The total number of powder patterns used."),
    Column("pdbx_pd_number_of_points", Integer, nullable=True, comment="The total number of data points in the processed diffractogram."),
    Column("pdbx_pd_Marquardt_correlation_coeff", Double, nullable=True, comment="The correlation coefficient between the observed and calculated structure factors for reflections included in the refinement. This correlation factor is found in the fitting using the Levenberg-Marquardt algorithm to search for the minimum value of chisquare. Almost all computer codes for Rietveld refinement employ the Gauss-Newton algorithm to find parameters which minimize the weighted sum of squares of the residuals. A description of the equations is given on http://www.water.hut.fi/~tkarvone/fr_org_s.htm"),
    Column("pdbx_pd_ls_matrix_band_width", Integer, nullable=True, comment="The least squares refinement \"band matrix\" approximation to the full matrix."),
    Column("pdbx_overall_phase_error", Double, nullable=True, comment="The overall phase error for all reflections after refinement using the current refinement target."),
    Column("pdbx_overall_SU_R_free_Cruickshank_DPI", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R-free value, expressed in a formalism known as the dispersion precision indicator (DPI). Ref: Cruickshank, D. W. J. (1999). Acta Cryst. D55, 583-601."),
    Column("pdbx_overall_SU_R_free_Blow_DPI", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R-free value, expressed in a formalism known as the dispersion precision indicator (DPI). Ref: Blow, D (2002) Acta Cryst. D58, 792-797"),
    Column("pdbx_overall_SU_R_Blow_DPI", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R value, expressed in a formalism known as the dispersion precision indicator (DPI). Ref: Blow, D (2002) Acta Cryst. D58, 792-797"),
    Column("pdbx_TLS_residual_ADP_flag", Text, nullable=True, comment="A flag for TLS refinements identifying the type of atomic displacement parameters stored in _atom_site.B_iso_or_equiv."),
    Column("pdbx_diffrn_id", Text, nullable=True, comment="An identifier for the diffraction data set used in this refinement. Multiple diffraction data sets specified as a comma separated list."),
    Column("overall_SU_B", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on a maximum-likelihood residual. The overall standard uncertainty (sigma~B~)^2^ gives an idea of the uncertainty in the B values of averagely defined atoms (atoms with B values equal to the average B value). N~a~ (sigma~B~)^2^ = 8 ---------------------------------------------- sum~i~ {[1/Sigma - (E~o~)^2^ (1-m^2^)](SUM_AS)s^4^} N~a~ = number of atoms E~o~ = normalized structure factors m = figure of merit of phases of reflections included in the summation s = reciprocal-space vector SUM_AS = (sigma~A~)^2^/Sigma^2^ Sigma = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = experimental uncertainties of normalized structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = atom form factor delta~x~ = expected error epsilon = multiplicity of diffracting plane summation is over all reflections included in refinement Ref: (sigma~A~ estimation) \"Refinement of macromolecular structures by the maximum-likelihood method\", Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255. (SU B estimation) Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html"),
    Column("overall_SU_ML", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the positional parameters based on a maximum likelihood residual. The overall standard uncertainty (sigma~X~)^2^ gives an idea of the uncertainty in the position of averagely defined atoms (atoms with B values equal to average B value) 3 N~a~ (sigma~X~)^2^ = --------------------------------------------------------- 8 pi^2^ sum~i~ {[1/Sigma - (E~o~)^2^ (1-m^2^)](SUM_AS)s^2^} N~a~ = number of atoms E~o~ = normalized structure factors m = figure of merit of phases of reflections included in the summation s = reciprocal-space vector SUM_AS = (sigma~A~)^2^/Sigma^2^ Sigma = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = experimental uncertainties of normalized structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = atom form factor delta~x~ = expected error epsilon = multiplicity of diffracting plane summation is over all reflections included in refinement Ref: (sigma_A estimation) \"Refinement of macromolecular structures by the maximum-likelihood method\", Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255. (SU ML estimation) Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html"),
    Column("overall_SU_R_Cruickshank_DPI", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the crystallographic R value, expressed in a formalism known as the dispersion precision indicator (DPI). The overall standard uncertainty (sigma~B~) gives an idea of the uncertainty in the B values of averagely defined atoms (atoms with B values equal to the average B value). N~a~ (sigma~B~)^2^ = 0.65 ---------- (R~value~)^2^ (D~min~)^2^ C^-2/3^ (N~o~-N~p~) N~a~ = number of atoms included in refinement N~o~ = number of observations N~p~ = number of parameters refined R~value~ = conventional crystallographic R value D~min~ = maximum resolution C = completeness of data Ref: Cruickshank, D. W. J. (1999). Acta Cryst. D55, 583-601. Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html"),
    Column("overall_SU_R_free", Double, nullable=True, comment="The overall standard uncertainty (estimated standard deviation) of the displacement parameters based on the free R value. The overall standard uncertainty (sigma~B~) gives an idea of the uncertainty in the B values of averagely defined atoms (atoms with B values equal to the average B value). N~a~ (sigma~B~)^2^ = 0.65 ---------- (R~free~)^2^ (D~min~)^2^ C^-2/3^ (N~o~-N~p~) N~a~ = number of atoms included in refinement N~o~ = number of observations N~p~ = number of parameters refined R~free~ = conventional free crystallographic R value calculated using reflections not included in refinement D~min~ = maximum resolution C = completeness of data Ref: Cruickshank, D. W. J. (1999). Acta Cryst. D55, 583-601. Murshudov, G. N. & Dodson, E. J. (1997). Simplified error estimation a la Cruickshank in macromolecular crystallography. CCP4 Newsletter on Protein Crystallography, No. 33, January 1997, pp. 31-39. http://www.ccp4.ac.uk/newsletters/newsletter33/murshudov.html"),
    Column("overall_FOM_free_R_set", Double, nullable=True, comment="Average figure of merit of phases of reflections not included in the refinement. This value is derived from the likelihood function. FOM = I~1~(X)/I~0~(X) I~0~, I~1~ = zero- and first-order modified Bessel functions of the first kind X = sigma~A~ |E~o~| |E~c~|/SIGMA E~o~, E~c~ = normalized observed and calculated structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = form factor of atoms delta~x~ = expected error SIGMA = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = uncertainties of normalized observed structure factors epsilon = multiplicity of the diffracting plane Ref: Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255."),
    Column("overall_FOM_work_R_set", Double, nullable=True, comment="Average figure of merit of phases of reflections included in the refinement. This value is derived from the likelihood function. FOM = I~1~(X)/I~0~(X) I~0~, I~1~ = zero- and first-order modified Bessel functions of the first kind X = sigma~A~ |E~o~| |E~c~|/SIGMA E~o~, E~c~ = normalized observed and calculated structure factors sigma~A~ = <cos 2 pi s delta~x~> SQRT(Sigma~P~/Sigma~N~) estimated using maximum likelihood Sigma~P~ = sum~{atoms in model}~ f^2^ Sigma~N~ = sum~{atoms in crystal}~ f^2^ f = form factor of atoms delta~x~ = expected error SIGMA = (sigma~{E;exp}~)^2^ + epsilon [1-(sigma~A~)^2^] sigma~{E;exp}~ = uncertainties of normalized observed structure factors epsilon = multiplicity of the diffracting plane Ref: Murshudov, G. N., Vagin, A. A. & Dodson, E. J. (1997). Acta Cryst. D53, 240-255."),
    Column("pdbx_average_fsc_overall", Double, nullable=True, comment="Overall average Fourier Shell Correlation (avgFSC) between model and observed structure factors for all reflections. The average FSC is a measure of the agreement between observed and calculated structure factors. sum(N~i~ FSC~i~) avgFSC = ---------------- sum(N~i~) N~i~ = the number of all reflections in the resolution shell i FSC~i~ = FSC for all reflections in the i-th resolution shell calculated as: (sum(|F~o~| |F~c~| fom cos(phi~c~-phi~o~))) FSC~i~ = ------------------------------------------- (sum(|F~o~|^2^) (sum(|F~c~|^2^)))^1/2^ |F~o~| = amplitude of observed structure factor |F~c~| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation of FSC~i~ is carried over all reflections in the resolution shell. Summation of avgFSC is carried over all resolution shells. Ref: Rosenthal P.B., Henderson R. \"Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6)."),
    Column("pdbx_average_fsc_work", Double, nullable=True, comment="Average Fourier Shell Correlation (avgFSC) between model and observed structure factors for reflections included in refinement. The average FSC is a measure of the agreement between observed and calculated structure factors. sum(N~i~ FSC~work-i~) avgFSC~work~ = --------------------- sum(N~i~) N~i~ = the number of working reflections in the resolution shell i FSC~work-i~ = FSC for working reflections in the i-th resolution shell calculated as: (sum(|F~o~| |F~c~| fom cos(phi~c~-phi~o~))) FSC~work-i~ = ------------------------------------------- (sum(|F~o~|^2^) (sum(|F~c~|^2^)))^1/2^ |F~o~| = amplitude of observed structure factor |F~c~| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation of FSC~work-i~ is carried over all working reflections in the resolution shell. Summation of avgFSC~work~ is carried over all resolution shells. Ref: Rosenthal P.B., Henderson R. \"Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6)."),
    Column("pdbx_average_fsc_free", Double, nullable=True, comment="Average Fourier Shell Correlation (avgFSC) between model and observed structure factors for reflections not included in refinement. The average FSC is a measure of the agreement between observed and calculated structure factors. sum(N~i~ FSC~free-i~) avgFSC~free~ = --------------------- sum(N~i~) N~i~ = the number of free reflections in the resolution shell i FSC~free-i~ = FSC for free reflections in the i-th resolution shell calculated as: (sum(|F~o~| |F~c~| fom cos(phi~c~-phi~o~))) FSC~free-i~ = ------------------------------------------- (sum(|F~o~|^2^) (sum(|F~c~|^2^)))^1/2^ |F~o~| = amplitude of observed structure factor |F~c~| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation of FSC~free-i~ is carried over all free reflections in the resolution shell. Summation of avgFSC~free~ is carried over all resolution shells. Ref: Rosenthal P.B., Henderson R. \"Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6)."),
    PrimaryKeyConstraint("pdbid", "entry_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "details",
            "pdbx_refine_id",
            "ls_abs_structure_details",
            "ls_extinction_expression",
            "ls_extinction_method",
            "ls_R_factor_R_free_error_details",
            "ls_weighting_details",
            "solvent_model_details",
            "pdbx_isotropic_thermal_model",
            "pdbx_ls_cross_valid_method",
            "pdbx_method_to_determine_struct",
            "pdbx_starting_model",
            "pdbx_stereochemistry_target_values",
            "pdbx_R_Free_selection_details",
            "pdbx_stereochem_target_val_spec_case",
        ]
    },
)

refine_analyze = Table(
    "refine_analyze",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_analyze.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("Luzzati_coordinate_error_free", Double, nullable=True, comment="The estimated coordinate error obtained from the plot of the R value versus sin(theta)/lambda for the reflections treated as a test set during refinement. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810."),
    Column("Luzzati_coordinate_error_obs", Double, nullable=True, comment="The estimated coordinate error obtained from the plot of the R value versus sin(theta)/lambda for reflections classified as observed. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810."),
    Column("Luzzati_d_res_low_free", Double, nullable=True, comment="The value of the low-resolution cutoff used in constructing the Luzzati plot for reflections treated as a test set during refinement. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810."),
    Column("Luzzati_d_res_low_obs", Double, nullable=True, comment="The value of the low-resolution cutoff used in constructing the Luzzati plot for reflections classified as observed. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810."),
    Column("Luzzati_sigma_a_free", Double, nullable=True, comment="The value of sigma~a~ used in constructing the Luzzati plot for the reflections treated as a test set during refinement. Details of the estimation of sigma~a~ can be specified in _refine_analyze.Luzzati_sigma_a_free_details. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810."),
    Column("Luzzati_sigma_a_obs", Double, nullable=True, comment="The value of sigma~a~ used in constructing the Luzzati plot for reflections classified as observed. Details of the estimation of sigma~a~ can be specified in _refine_analyze.Luzzati_sigma_a_obs_details. Ref: Luzzati, V. (1952). Traitement statistique des erreurs dans la determination des structures cristallines. Acta Cryst. 5, 802-810."),
    Column("number_disordered_residues", Double, nullable=True, comment="The number of discretely disordered residues in the refined model."),
    Column("occupancy_sum_hydrogen", Double, nullable=True, comment="The sum of the occupancies of the hydrogen atoms in the refined model."),
    Column("occupancy_sum_non_hydrogen", Double, nullable=True, comment="The sum of the occupancies of the non-hydrogen atoms in the refined model."),
    Column("pdbx_Luzzati_d_res_high_obs", Double, nullable=True, comment="record the high resolution for calculating Luzzati statistics."),
    PrimaryKeyConstraint("pdbid", "entry_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "pdbx_refine_id",
            "Luzzati_sigma_a_free_details",
            "Luzzati_sigma_a_obs_details",
        ]
    },
)

refine_B_iso = Table(
    "refine_B_iso",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_B_iso.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("class", Text, nullable=True, comment="A class of atoms treated similarly for isotropic B-factor (displacement-parameter) refinement."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the isotropic B-factor (displacement-parameter) refinement for the class of atoms described in _refine_B_iso.class."),
    Column("treatment", Text, nullable=True, comment="The treatment of isotropic B-factor (displacement-parameter) refinement for a class of atoms defined in _refine_B_iso.class."),
    PrimaryKeyConstraint("pdbid", "class", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "class", "details"]},
)

refine_funct_minimized = Table(
    "refine_funct_minimized",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_funct_minimized.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("type", Text, nullable=True, comment="The type of the function being minimized."),
    PrimaryKeyConstraint("pdbid", "type", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "type"]},
)

refine_hist = Table(
    "refine_hist",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_hist.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("cycle_id", Text, nullable=True, comment="The value of _refine_hist.cycle_id must uniquely identify a record in the REFINE_HIST list. Note that this item need not be a number; it can be any unique identifier."),
    Column("details", Text, nullable=True, comment="A description of special aspects of this cycle of the refinement process."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value for the interplanar spacings for the reflection data for this cycle of refinement. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value for the interplanar spacings for the reflection data for this cycle of refinement. This is called the lowest resolution."),
    Column("number_atoms_solvent", Integer, nullable=True, comment="The number of solvent atoms that were included in the model at this cycle of the refinement."),
    Column("number_atoms_total", Integer, nullable=True, comment="The total number of atoms that were included in the model at this cycle of the refinement."),
    Column("pdbx_number_residues_total", Integer, nullable=True, comment="Total number of polymer residues included in refinement."),
    Column("pdbx_B_iso_mean_ligand", Double, nullable=True, comment="Mean isotropic B-value for ligand molecules included in refinement."),
    Column("pdbx_B_iso_mean_solvent", Double, nullable=True, comment="Mean isotropic B-value for solvent molecules included in refinement."),
    Column("pdbx_number_atoms_protein", Integer, nullable=True, comment="Number of protein atoms included in refinement"),
    Column("pdbx_number_atoms_nucleic_acid", Integer, nullable=True, comment="Number of nucleic atoms included in refinement"),
    Column("pdbx_number_atoms_ligand", Integer, nullable=True, comment="Number of ligand atoms included in refinement"),
    PrimaryKeyConstraint("pdbid", "cycle_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "details", "pdbx_pseudo_atom_details"]},
)

refine_ls_restr = Table(
    "refine_ls_restr",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_ls_restr.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("dev_ideal", Double, nullable=True, comment="For the given parameter type, the root-mean-square deviation between the ideal values used as restraints in the least-squares refinement and the values obtained by refinement. For instance, bond distances may deviate by 0.018 \\%A (r.m.s.) from ideal values in the current model."),
    Column("dev_ideal_target", Double, nullable=True, comment="For the given parameter type, the target root-mean-square deviation between the ideal values used as restraints in the least-squares refinement and the values obtained by refinement."),
    Column("number", Integer, nullable=True, comment="The number of parameters of this type subjected to restraint in least-squares refinement."),
    Column("type", Text, nullable=True, comment="The type of the parameter being restrained. Explicit sets of data values are provided for the programs PROTIN/PROLSQ (beginning with p_) and RESTRAIN (beginning with RESTRAIN_). As computer programs change, these data values are given as examples, not as an enumeration list. Computer programs that convert a data block to a refinement table will expect the exact form of the data values given here to be used."),
    Column("weight", Double, nullable=True, comment="The weighting value applied to this type of restraint in the least-squares refinement."),
    Column("pdbx_restraint_function", Text, nullable=True, comment="The functional form of the restraint function used in the least-squares refinement."),
    PrimaryKeyConstraint("pdbid", "type", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": ["pdbx_refine_id", "criterion", "type", "pdbx_restraint_function"]
    },
)

refine_ls_restr_ncs = Table(
    "refine_ls_restr_ncs",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_ls_restr_ncs.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("dom_id", Text, nullable=True, comment="This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category."),
    Column("ncs_model_details", Text, nullable=True, comment="Special aspects of the manner in which noncrystallographic restraints were applied to atomic parameters in the domain specified by _refine_ls_restr_ncs.dom_id and equivalent atomic parameters in the domains against which it was restrained."),
    Column("rms_dev_B_iso", Double, nullable=True, comment="The root-mean-square deviation in equivalent isotropic displacement parameters in the domain specified by _refine_ls_restr_ncs.dom_id and in the domains against which it was restrained."),
    Column("rms_dev_position", Double, nullable=True, comment="The root-mean-square deviation in equivalent atom positions in the domain specified by _refine_ls_restr_ncs.dom_id and in the domains against which it was restrained."),
    Column("weight_B_iso", Double, nullable=True, comment="The value of the weighting coefficient used in noncrystallographic symmetry restraint of isotropic displacement parameters in the domain specified by _refine_ls_restr_ncs.dom_id to equivalent isotropic displacement parameters in the domains against which it was restrained."),
    Column("weight_position", Double, nullable=True, comment="The value of the weighting coefficient used in noncrystallographic symmetry restraint of atom positions in the domain specified by _refine_ls_restr_ncs.dom_id to equivalent atom positions in the domains against which it was restrained."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="An ordinal index for the list of NCS restraints."),
    Column("pdbx_type", Text, nullable=True, comment="The type of NCS restraint. (for example: tight positional)"),
    Column("pdbx_asym_id", Text, nullable=True, comment="A reference to _struct_asym.id."),
    Column("pdbx_auth_asym_id", Text, nullable=True, comment="A reference to the PDB Chain ID"),
    Column("pdbx_number", Integer, nullable=True, comment="Records the number restraints in the contributing to the RMS statistic."),
    Column("pdbx_rms", Double, nullable=True, comment="Records the standard deviation in the restraint between NCS related domains."),
    Column("pdbx_weight", Double, nullable=True, comment="Records the weight used for NCS restraint."),
    Column("pdbx_ens_id", Text, nullable=True, comment="This is a unique identifier for a collection NCS related domains. This references item '_struct_ncs_dom.pdbx_ens_id'."),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "ncs_model_details", "pdbx_type"]},
)

refine_ls_shell = Table(
    "refine_ls_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_ls_shell.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("d_res_high", Double, nullable=True, comment="The lowest value for the interplanar spacings for the reflection data in this shell. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value for the interplanar spacings for the reflection data in this shell. This is called the lowest resolution."),
    Column("number_reflns_all", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low."),
    Column("number_reflns_obs", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion."),
    Column("number_reflns_R_free", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details."),
    Column("number_reflns_R_work", Integer, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details."),
    Column("percent_reflns_obs", Double, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion, expressed as a percentage of the number of geometrically observable reflections that satisfy the resolution limits."),
    Column("percent_reflns_R_free", Double, nullable=True, comment="The number of reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor, expressed as a percentage of the number of geometrically observable reflections that satisfy the reflection limits."),
    Column("R_factor_all", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("R_factor_obs", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("R_factor_R_free_error", Double, nullable=True, comment="The estimated error in _refine_ls_shell.R_factor_R_free. The method used to estimate the error is described in the item _refine.ls_R_factor_R_free_error_details."),
    Column("R_factor_R_work", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    Column("redundancy_reflns_all", Double, nullable=True, comment="The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low to the number of crystallographically unique reflections that satisfy the same limits."),
    Column("redundancy_reflns_obs", Double, nullable=True, comment="The ratio of the total number of observations of the reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation criterion established by _reflns.observed_criterion to the number of crystallographically unique reflections that satisfy the same limits."),
    Column("wR_factor_R_work", Double, nullable=True, comment="Weighted residual factor wR for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the working reflections (i.e. were included in the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. ( sum|w |Y~obs~ - Y~calc~|^2^| )^1/2^ wR = ( ---------------------------- ) ( sum|w Y~obs~^2^| ) Y~obs~ = the observed amplitude specified by _refine.ls_structure_factor_coef Y~calc~ = the calculated amplitude specified by _refine.ls_structure_factor_coef w = the least-squares weight sum is taken over the specified reflections"),
    Column("pdbx_R_complete", Double, nullable=True, comment="The crystallographic reliability index Rcomplete for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion Ref: Luebben, J., Gruene, T., (2015). Proc.Nat.Acad.Sci. 112(29) 8999-9003"),
    Column("correlation_coeff_Fo_to_Fc", Double, nullable=True, comment="The correlation coefficient between the observed and calculated structure factors for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low included in the refinement. The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections included in the refinement"),
    Column("correlation_coeff_Fo_to_Fc_free", Double, nullable=True, comment="The correlation coefficient between the observed and calculated structure factors for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low not included in the refinement (free reflections). The correlation coefficient is scale-independent and gives an idea of the quality of the refined model. sum~i~(Fo~i~ Fc~i~ - <Fo><Fc>) R~corr~ = ------------------------------------------------------------ SQRT{sum~i~(Fo~i~)^2^-<Fo>^2^} SQRT{sum~i~(Fc~i~)^2^-<Fc>^2^} Fo = observed structure factors Fc = calculated structure factors <> denotes average value summation is over reflections not included in the refinement (free reflections)"),
    Column("pdbx_total_number_of_bins_used", Integer, nullable=True, comment="Total number of bins used."),
    Column("pdbx_phase_error", Double, nullable=True, comment="The average phase error for all reflections in the resolution shell."),
    Column("pdbx_fsc_work", Double, nullable=True, comment="Fourier Shell Correlation (FSC) between model and observed structure factors for reflections included in refinement. FSC is a measure of the agreement between observed and calculated structure factors as complex numbers. (sum(|F~o~| |F~c~| fom cos(phi~c~-phi~o~))) FSC~work~ = -------------------------------------- (sum(|F~o~|^2^) (sum(|F~c~|^2^)))^1/2^ |F~o~| = amplitude of observed structure factor |F~c~| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation is carried over all working reflections in the resolution shell. Ref: Rosenthal P.B., Henderson R. \"Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6)."),
    Column("pdbx_fsc_free", Double, nullable=True, comment="Fourier Shell Correlation (FSC) between model and observed structure factors for reflections not included in refinement. FSC is a measure of the agreement between observed and calculated structure factors as complex numbers. (sum(|F~o~| |F~c~| fom cos(phi~c~-phi~o~))) FSC~free~ = -------------------------------------- (sum(|F~o~|^2^) (sum(|F~c~|^2^)))^1/2^ |F~o~| = amplitude of observed structure factor |F~c~| = amplitude of calculated structure factor phi~o~ = phase of observed structure factor phi~c~ = phase of calculated structure factor fom = figure of merit of the experimental phases. Summation is carried over all free reflections in the resolution shell. Ref: Rosenthal P.B., Henderson R. \"Optimal determination of particle orientation, absolute hand, and contrast loss in single-particle electron cryomicroscopy. Journal of Molecular Biology. 2003;333(4):721-745, equation (A6)."),
    Column("R_factor_R_free", Double, nullable=True, comment="Residual factor R for reflections that satisfy the resolution limits established by _refine_ls_shell.d_res_high and _refine_ls_shell.d_res_low and the observation limit established by _reflns.observed_criterion, and that were used as the test reflections (i.e. were excluded from the refinement) when the refinement included the calculation of a 'free' R factor. Details of how reflections were assigned to the working and test sets are given in _reflns.R_free_details. sum|F~obs~ - F~calc~| R = --------------------- sum|F~obs~| F~obs~ = the observed structure-factor amplitudes F~calc~ = the calculated structure-factor amplitudes sum is taken over the specified reflections"),
    PrimaryKeyConstraint("pdbid", "d_res_high", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id"]},
)

refine_occupancy = Table(
    "refine_occupancy",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _refine_occupancy.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("class", Text, nullable=True, comment="The class of atoms treated similarly for occupancy refinement."),
    Column("treatment", Text, nullable=True, comment="The treatment of occupancies for a class of atoms described in _refine_occupancy.class."),
    PrimaryKeyConstraint("pdbid", "class", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "class", "details"]},
)

refln_sys_abs = Table(
    "refln_sys_abs",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("I", Double, nullable=True, comment="The measured value of the intensity in arbitrary units."),
    Column("I_over_sigmaI", Double, nullable=True, comment="The ratio of _refln_sys_abs.I to _refln_sys_abs.sigmaI. Used to evaluate whether a reflection that should be systematically absent according to the designated space group is in fact absent."),
    Column("index_h", Integer, nullable=True, comment="Miller index h of the reflection. The values of the Miller indices in the REFLN_SYS_ABS category must correspond to the cell defined by cell lengths and cell angles in the CELL category."),
    Column("index_k", Integer, nullable=True, comment="Miller index k of the reflection. The values of the Miller indices in the REFLN_SYS_ABS category must correspond to the cell defined by cell lengths and cell angles in the CELL category."),
    Column("index_l", Integer, nullable=True, comment="Miller index l of the reflection. The values of the Miller indices in the REFLN_SYS_ABS category must correspond to the cell defined by cell lengths and cell angles in the CELL category."),
    Column("sigmaI", Double, nullable=True, comment="The standard uncertainty (estimated standard deviation) of _refln_sys_abs.I in arbitrary units."),
    PrimaryKeyConstraint("pdbid", "index_h", "index_k", "index_l"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

reflns = Table(
    "reflns",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("B_iso_Wilson_estimate", Double, nullable=True, comment="The value of the overall isotropic displacement parameter estimated from the slope of the Wilson plot."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("data_reduction_details", Text, nullable=True, comment="A description of special aspects of the data-reduction procedures."),
    Column("data_reduction_method", Text, nullable=True, comment="The method used for data reduction. Note that this is not the computer program used, which is described in the SOFTWARE category, but the method itself. This data item should be used to describe significant methodological options used within the data-reduction programs."),
    Column("d_resolution_high", Double, nullable=True, comment="The smallest value in angstroms for the interplanar spacings for the reflection data. This is called the highest resolution."),
    Column("d_resolution_low", Double, nullable=True, comment="The largest value in angstroms for the interplanar spacings for the reflection data. This is called the lowest resolution."),
    Column("details", Text, nullable=True, comment="A description of reflection data not covered by other data names. This should include details of the Friedel pairs."),
    Column("limit_h_max", Integer, nullable=True, comment="Maximum value of the Miller index h for the reflection data. This need not have the same value as _diffrn_reflns.limit_h_max."),
    Column("limit_h_min", Integer, nullable=True, comment="Minimum value of the Miller index h for the reflection data. This need not have the same value as _diffrn_reflns.limit_h_min."),
    Column("limit_k_max", Integer, nullable=True, comment="Maximum value of the Miller index k for the reflection data. This need not have the same value as _diffrn_reflns.limit_k_max."),
    Column("limit_k_min", Integer, nullable=True, comment="Minimum value of the Miller index k for the reflection data. This need not have the same value as _diffrn_reflns.limit_k_min."),
    Column("limit_l_max", Integer, nullable=True, comment="Maximum value of the Miller index l for the reflection data. This need not have the same value as _diffrn_reflns.limit_l_max."),
    Column("limit_l_min", Integer, nullable=True, comment="Minimum value of the Miller index l for the reflection data. This need not have the same value as _diffrn_reflns.limit_l_min."),
    Column("number_all", Integer, nullable=True, comment="The total number of reflections in the REFLN list (not the DIFFRN_REFLN list). This number may contain Friedel-equivalent reflections according to the nature of the structure and the procedures used. The item _reflns.details describes the reflection data."),
    Column("number_obs", Integer, nullable=True, comment="The number of reflections in the REFLN list (not the DIFFRN_REFLN list) classified as observed (see _reflns.observed_criterion). This number may contain Friedel-equivalent reflections according to the nature of the structure and the procedures used."),
    Column("observed_criterion_F_max", Double, nullable=True, comment="The criterion used to classify a reflection as 'observed' expressed as an upper limit for the value of F."),
    Column("observed_criterion_F_min", Double, nullable=True, comment="The criterion used to classify a reflection as 'observed' expressed as a lower limit for the value of F."),
    Column("observed_criterion_I_max", Double, nullable=True, comment="The criterion used to classify a reflection as 'observed' expressed as an upper limit for the value of I."),
    Column("observed_criterion_I_min", Double, nullable=True, comment="The criterion used to classify a reflection as 'observed' expressed as a lower limit for the value of I."),
    Column("observed_criterion_sigma_F", Double, nullable=True, comment="The criterion used to classify a reflection as 'observed' expressed as a multiple of the value of sigma(F)."),
    Column("observed_criterion_sigma_I", Double, nullable=True, comment="The criterion used to classify a reflection as 'observed' expressed as a multiple of the value of sigma(I)."),
    Column("percent_possible_obs", Double, nullable=True, comment="The percentage of geometrically possible reflections represented by reflections that satisfy the resolution limits established by _reflns.d_resolution_high and _reflns.d_resolution_low and the observation limit established by _reflns.observed_criterion."),
    Column("R_free_details", Text, nullable=True, comment="A description of the method by which a subset of reflections was selected for exclusion from refinement so as to be used in the calculation of a 'free' R factor."),
    Column("Rmerge_F_all", Double, nullable=True, comment="Residual factor Rmerge for all reflections that satisfy the resolution limits established by _reflns.d_resolution_high and _reflns.d_resolution_low. sum~i~(sum~j~|F~j~ - <F>|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("Rmerge_F_obs", Double, nullable=True, comment="Residual factor Rmerge for reflections that satisfy the resolution limits established by _reflns.d_resolution_high and _reflns.d_resolution_low and the observation limit established by _reflns.observed_criterion. sum~i~(sum~j~|F~j~ - <F>|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("pdbx_redundancy", Double, nullable=True, comment="Overall redundancy for this data set."),
    Column("pdbx_netI_over_av_sigmaI", Double, nullable=True, comment="The ratio of the average intensity to the average uncertainty, <I>/<sigma(I)>."),
    Column("pdbx_netI_over_sigmaI", Double, nullable=True, comment="The mean of the ratio of the intensities to their standard uncertainties, <I/sigma(I)>."),
    Column("pdbx_chi_squared", Double, nullable=True, comment="Overall Chi-squared statistic."),
    Column("pdbx_scaling_rejects", Integer, nullable=True, comment="Number of reflections rejected in scaling operations."),
    Column("phase_calculation_details", Text, nullable=True, comment="The value of _reflns.phase_calculation_details describes a special details about calculation of phases in _refln.phase_calc."),
    Column("pdbx_Rrim_I_all", Double, nullable=True, comment="The redundancy-independent merging R factor value Rrim, also denoted Rmeas, for merging all intensities in this data set. sum~i~ [N~i~/(N~i~ - 1)]1/2^ sum~j~ | I~j~ - <I~i~> | Rrim = ---------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135."),
    Column("pdbx_Rpim_I_all", Double, nullable=True, comment="The precision-indicating merging R factor value Rpim, for merging all intensities in this data set. sum~i~ [1/(N~i~ - 1)]1/2^ sum~j~ | I~j~ - <I~i~> | Rpim = -------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135."),
    Column("pdbx_number_measured_all", Integer, nullable=True, comment="Total number of measured reflections."),
    Column("pdbx_diffrn_id", Text, nullable=True, comment="An identifier for the diffraction data set for this set of summary statistics. Multiple diffraction data sets entered as a comma separated list."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="An ordinal identifier for this set of reflection statistics."),
    Column("pdbx_CC_half", Double, nullable=True, comment="The Pearson's correlation coefficient expressed as a decimal value between the average intensities from randomly selected half-datasets. Ref: Karplus & Diederichs (2012), Science 336, 1030-33"),
    Column("pdbx_CC_star", Double, nullable=True, comment="Estimates the value of CC_true, the true correlation coefficient between the average intensities from randomly selected half-datasets. CC_star = sqrt(2*CC_half/(1+CC_half)), where both CC_star and CC_half (CC1/2) Ref: Karplus & Diederichs (2012), Science 336, 1030-33"),
    Column("pdbx_R_split", Double, nullable=True, comment="R split measures the agreement between the sets of intensities created by merging odd- and even-numbered images from the overall data. Ref: T. A. White, R. A. Kirian, A. V. Martin, A. Aquila, K. Nass, A. Barty and H. N. Chapman (2012), J. Appl. Cryst. 45, 335-341"),
    Column("pdbx_Rmerge_I_obs", Double, nullable=True, comment="The R value for merging intensities satisfying the observed criteria in this data set."),
    Column("pdbx_Rmerge_I_all", Double, nullable=True, comment="The R value for merging all intensities in this data set."),
    Column("pdbx_Rsym_value", Double, nullable=True, comment="The R sym value as a decimal number."),
    Column("pdbx_aniso_diffraction_limit_axis_1_ortho1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_1_ortho2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_1_ortho3", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_2_ortho1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_2_ortho2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_2_ortho3", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_3_ortho1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_3_ortho2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_3_ortho3", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_1", Double, nullable=True, comment="Anisotropic diffraction limit along principal axis 1 (of ellipsoid fitted to the diffraction cut-off surface)."),
    Column("pdbx_aniso_diffraction_limit_2", Double, nullable=True, comment="Anisotropic diffraction limit along principal axis 2 (of ellipsoid fitted to the diffraction cut-off surface)"),
    Column("pdbx_aniso_diffraction_limit_3", Double, nullable=True, comment="Anisotropic diffraction limit along principal axis 3 (of ellipsoid fitted to the diffraction cut-off surface)"),
    Column("pdbx_aniso_B_tensor_eigenvector_1_ortho1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_1_ortho2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_1_ortho3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_2_ortho1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_2_ortho2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_2_ortho3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_3_ortho1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_3_ortho2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_3_ortho3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvalue_1", Double, nullable=True, comment="Eigen-B-factor along the first eigenvector of the diffraction anisotropy tensor"),
    Column("pdbx_aniso_B_tensor_eigenvalue_2", Double, nullable=True, comment="Eigen-B-factor along the second eigenvector of the diffraction anisotropy tensor"),
    Column("pdbx_aniso_B_tensor_eigenvalue_3", Double, nullable=True, comment="Eigen-B-factor along the third eigenvector of the diffraction anisotropy tensor"),
    Column("pdbx_orthogonalization_convention", Text, nullable=True, comment="Description of orthogonalization convention used. The notation can make use of unit cell axes \"a\", \"b\" and \"c\" and the reciprocal unit cell axes \"astar\", \"bstar\" and \"cstar\". Upper case letters \"X\", \"Y\" and \"Z\" denote the orthogonal axes, while lower case \"x\" stands for \"cross product\"."),
    Column("pdbx_percent_possible_ellipsoidal", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique data within the intersection of (1) a sphere (defined by the diffraction limits, _reflns.d_resolution_high and _reflns.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique reflections within that intersection."),
    Column("pdbx_percent_possible_spherical", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) relative to all possible symmetry-unique reflections within that sphere. In the absence of an anisotropy description this is identical to _reflns.percent_possible_obs."),
    Column("pdbx_percent_possible_ellipsoidal_anomalous", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique anomalous difference data within the intersection of (1) a sphere (defined by the diffraction limits, _reflns.d_resolution_high and _reflns.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique anomalous difference data within that intersection."),
    Column("pdbx_percent_possible_spherical_anomalous", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique anomalous difference data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that sphere. In the absence of an anisotropy description this is identical to _reflns.pdbx_percent_possible_anomalous."),
    Column("pdbx_redundancy_anomalous", Double, nullable=True, comment="The overall redundancy of anomalous difference data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low), i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection."),
    Column("pdbx_CC_half_anomalous", Double, nullable=True, comment="The overall correlation coefficient between two randomly chosen half-sets of anomalous intensity differences, I(+)-I(-) for anomalous data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low), i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection."),
    Column("pdbx_absDiff_over_sigma_anomalous", Double, nullable=True, comment="The overall mean ratio of absolute anomalous intensity differences to their standard deviation within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) and using data for which intensities for both instances of a Friedel pair are available for an acentric reflection. |Dano| ------------- sigma(Dano) with Dano = I(+) - I(-) sigma(Dano) = sqrt( sigma(I(+))^2 + sigma(I(-))^2 )"),
    Column("pdbx_percent_possible_anomalous", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique anomalous difference data within the sphere defined by the diffraction limits (_reflns.d_resolution_high and _reflns.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that sphere."),
    Column("pdbx_observed_signal_threshold", Double, nullable=True, comment="The threshold value for _refln.pdbx_signal as used to define the status of an individual reflection according to the description in _refln.pdbx_signal_status."),
    Column("pdbx_signal_type", Text, nullable=True, comment="Type of signal used for _reflns.pdbx_observed_signal_threshold and _refln.pdbx_signal In the enumeration details: Imean is the inverse-variance weighted mean intensity of all measurements for a given symmetry-unique reflection Ihalf is the inverse-variance weighted mean intensity of a random half-selection of all measurements for a given symmetry-unique reflection"),
    Column("pdbx_signal_details", Text, nullable=True, comment="Further details about the calculation of the values assigned to _refln.pdbx_signal"),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "data_reduction_details",
            "data_reduction_method",
            "details",
            "observed_criterion",
            "R_free_details",
            "threshold_expression",
            "pdbx_d_res_opt_method",
            "phase_calculation_details",
            "pdbx_signal_details",
            "pdbx_signal_software_id",
        ]
    },
)

reflns_scale = Table(
    "reflns_scale",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("group_code", Text, nullable=True, comment="The code identifying a scale _reflns_scale.meas_F, _reflns_scale.meas_F_squared or _reflns_scale.meas_intensity. These are linked to the REFLN list by the _refln.scale_group_code. These codes need not correspond to those in the DIFFRN_SCALE list."),
    PrimaryKeyConstraint("pdbid", "group_code"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["group_code"]},
)

reflns_shell = Table(
    "reflns_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("d_res_high", Double, nullable=True, comment="The smallest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the highest resolution."),
    Column("d_res_low", Double, nullable=True, comment="The highest value in angstroms for the interplanar spacings for the reflections in this shell. This is called the lowest resolution."),
    Column("meanI_over_sigI_all", Double, nullable=True, comment="The ratio of the mean of the intensities of all reflections in this shell to the mean of the standard uncertainties of the intensities of all reflections in this shell."),
    Column("meanI_over_sigI_obs", Double, nullable=True, comment="The ratio of the mean of the intensities of the reflections classified as 'observed' (see _reflns.observed_criterion) in this shell to the mean of the standard uncertainties of the intensities of the 'observed' reflections in this shell."),
    Column("number_measured_all", Integer, nullable=True, comment="The total number of reflections measured for this shell."),
    Column("number_measured_obs", Integer, nullable=True, comment="The number of reflections classified as 'observed' (see _reflns.observed_criterion) for this shell."),
    Column("number_possible", Integer, nullable=True, comment="The number of unique reflections it is possible to measure in this shell."),
    Column("number_unique_all", Integer, nullable=True, comment="The total number of measured reflections which are symmetry- unique after merging for this shell."),
    Column("number_unique_obs", Integer, nullable=True, comment="The total number of measured reflections classified as 'observed' (see _reflns.observed_criterion) which are symmetry-unique after merging for this shell."),
    Column("percent_possible_obs", Double, nullable=True, comment="The percentage of geometrically possible reflections represented by reflections classified as 'observed' (see _reflns.observed_criterion) for this shell."),
    Column("Rmerge_F_all", Double, nullable=True, comment="Residual factor Rmerge for all reflections that satisfy the resolution limits established by _reflns_shell.d_res_high and _reflns_shell.d_res_low. sum~i~(sum~j~|F~j~ - <F>|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("Rmerge_F_obs", Double, nullable=True, comment="Residual factor Rmerge for reflections that satisfy the resolution limits established by _reflns_shell.d_res_high and _reflns_shell.d_res_low and the observation criterion established by _reflns.observed_criterion. sum~i~(sum~j~|F~j~ - <F>|) Rmerge(F) = -------------------------- sum~i~(sum~j~<F>) F~j~ = the amplitude of the jth observation of reflection i <F> = the mean of the amplitudes of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("meanI_over_uI_all", Double, nullable=True, comment="The ratio of the mean of the intensities of all reflections in this shell to the mean of the standard uncertainties of the intensities of all reflections in this shell."),
    Column("percent_possible_gt", Double, nullable=True, comment="The percentage of geometrically possible reflections represented by significantly intense reflections (see _reflns.threshold_expression) measured for this shell."),
    Column("pdbx_redundancy", Double, nullable=True, comment="Redundancy for the current shell."),
    Column("pdbx_chi_squared", Double, nullable=True, comment="Chi-squared statistic for this resolution shell."),
    Column("pdbx_netI_over_sigmaI_all", Double, nullable=True, comment="The mean of the ratio of the intensities to their standard uncertainties of all reflections in the resolution shell. _reflns_shell.pdbx_netI_over_sigmaI_all = <I/sigma(I)>"),
    Column("pdbx_netI_over_sigmaI_obs", Double, nullable=True, comment="The mean of the ratio of the intensities to their standard uncertainties of observed reflections (see _reflns.observed_criterion) in the resolution shell. _reflns_shell.pdbx_netI_over_sigmaI_obs = <I/sigma(I)>"),
    Column("pdbx_Rrim_I_all", Double, nullable=True, comment="The redundancy-independent merging R factor value Rrim, also denoted Rmeas, for merging all intensities in a given shell. sum~i~ [N~i~ /( N~i~ - 1)]1/2^ sum~j~ | I~j~ - <I~i~> | Rrim = -------------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135."),
    Column("pdbx_Rpim_I_all", Double, nullable=True, comment="The precision-indicating merging R factor value Rpim, for merging all intensities in a given shell. sum~i~ [1/(N~i~ - 1)]1/2^ sum~j~ | I~j~ - <I~i~> | Rpim = -------------------------------------------------- sum~i~ ( sum~j~ I~j~ ) I~j~ = the intensity of the jth observation of reflection i <I~i~> = the mean of the intensities of all observations of reflection i N~i~ = the redundancy (the number of times reflection i has been measured). sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection. Ref: Diederichs, K. & Karplus, P. A. (1997). Nature Struct. Biol. 4, 269-275. Weiss, M. S. & Hilgenfeld, R. (1997). J. Appl. Cryst. 30, 203-205. Weiss, M. S. (2001). J. Appl. Cryst. 34, 130-135."),
    Column("pdbx_rejects", Integer, nullable=True, comment="The number of rejected reflections in the resolution shell. Reflections may be rejected from scaling by setting the observation criterion, _reflns.observed_criterion."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="An ordinal identifier for this resolution shell."),
    Column("pdbx_diffrn_id", Text, nullable=True, comment="An identifier for the diffraction data set corresponding to this resolution shell. Multiple diffraction data sets specified as a comma separated list."),
    Column("pdbx_CC_half", Double, nullable=True, comment="The Pearson's correlation coefficient expressed as a decimal value between the average intensities from randomly selected half-datasets within the resolution shell. Ref: Karplus & Diederichs (2012), Science 336, 1030-33"),
    Column("pdbx_CC_star", Double, nullable=True, comment="Estimates the value of CC_true, the true correlation coefficient between the average intensities from randomly selected half-datasets within the resolution shell. CC_star = sqrt(2*CC_half/(1+CC_half)) Ref: Karplus & Diederichs (2012), Science 336, 1030-33"),
    Column("pdbx_R_split", Double, nullable=True, comment="R split measures the agreement between the sets of intensities created by merging odd- and even-numbered images from the data within the resolution shell. Ref: T. A. White, R. A. Kirian, A. V. Martin, A. Aquila, K. Nass, A. Barty and H. N. Chapman (2012), J. Appl. Cryst. 45, 335-341"),
    Column("percent_possible_all", Double, nullable=True, comment="The percentage of geometrically possible reflections represented by all reflections measured for this shell."),
    Column("Rmerge_I_all", Double, nullable=True, comment="The value of Rmerge(I) for all reflections in a given shell. sum~i~(sum~j~|I~j~ - <I>|) Rmerge(I) = -------------------------- sum~i~(sum~j~<I>) I~j~ = the intensity of the jth observation of reflection i <I> = the mean of the intensities of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("Rmerge_I_obs", Double, nullable=True, comment="The value of Rmerge(I) for reflections classified as 'observed' (see _reflns.observed_criterion) in a given shell. sum~i~(sum~j~|I~j~ - <I>|) Rmerge(I) = -------------------------- sum~i~(sum~j~<I>) I~j~ = the intensity of the jth observation of reflection i <I> = the mean of the intensities of all observations of reflection i sum~i~ is taken over all reflections sum~j~ is taken over all observations of each reflection"),
    Column("pdbx_Rsym_value", Double, nullable=True, comment="R sym value in percent."),
    Column("pdbx_percent_possible_ellipsoidal", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique data within the intersection of (1) a spherical shell (defined by its diffraction limits, _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique reflections within that intersection."),
    Column("pdbx_percent_possible_spherical", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique data within the spherical shell defined by its diffraction limits (_reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) relative to all possible symmetry-unique reflections within that shell. In the absence of an anisotropy description this is identical to _reflns_shell.percent_possible_all."),
    Column("pdbx_percent_possible_ellipsoidal_anomalous", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique anomalous difference data within the intersection of (1) a spherical shell (defined by its diffraction limits, _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) and (2) the ellipsoid (described by __reflns.pdbx_aniso_diffraction_limit_* items), relative to all possible symmetry-unique anomalous difference data within that intersection."),
    Column("pdbx_percent_possible_spherical_anomalous", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique anomalous difference data within the spherical shell defined by its diffraction limits (_reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that shell. In the absence of an anisotropy description this is identical to _reflns.pdbx_percent_possible_anomalous."),
    Column("pdbx_redundancy_anomalous", Double, nullable=True, comment="The redundancy of anomalous difference data within the spherical shell (defined by its diffraction limits _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low), i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection."),
    Column("pdbx_CC_half_anomalous", Double, nullable=True, comment="The correlation coefficient within the spherical shell (defined by its diffraction limits _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) between two randomly chosen half-sets of anomalous intensity differences, I(+)-I(-) for anomalous data, i.e. data for which intensities for both instances of a Friedel pair are available for an acentric reflection."),
    Column("pdbx_absDiff_over_sigma_anomalous", Double, nullable=True, comment="The mean ratio of absolute anomalous intensity differences to their standard deviation within the spherical shell (defined by its diffraction limits _reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low). |Dano| ------------- sigma(Dano) with Dano = I(+) - I(-) sigma(Dano) = sqrt( sigma(I(+))^2 + sigma(I(-))^2 )"),
    Column("pdbx_percent_possible_anomalous", Double, nullable=True, comment="Completeness (as a percentage) of symmetry-unique anomalous difference data within the spherical shell defined by its diffraction limits (_reflns_shell.d_resolution_high and _reflns_shell.d_resolution_low) relative to all possible symmetry-unique anomalous difference data within that shell."),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

software = Table(
    "software",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("classification", Text, nullable=True, comment="The classification of the program according to its major function."),
    Column("compiler_version", Text, nullable=True, comment="The version of the compiler used to compile the software."),
    Column("contact_author", Text, nullable=True, comment="The recognized contact author of the software. This could be the original author, someone who has modified the code or someone who maintains the code. It should be the person most commonly associated with the code."),
    Column("contact_author_email", Text, nullable=True, comment="The e-mail address of the person specified in _software.contact_author."),
    Column("date", Text, nullable=True, comment="The date the software was released."),
    Column("description", Text, nullable=True, comment="Description of the software."),
    Column("language", Text, nullable=True, comment="The major computing language in which the software is coded."),
    Column("location", Text, nullable=True, comment="The URL for an Internet address at which details of the software can be found."),
    Column("name", Text, nullable=True, comment="The name of the software."),
    Column("os", Text, nullable=True, comment="The name of the operating system under which the software runs."),
    Column("os_version", Text, nullable=True, comment="The version of the operating system under which the software runs."),
    Column("type", Text, nullable=True, comment="The classification of the software according to the most common types."),
    Column("version", Text, nullable=True, comment="The version of the software."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="An ordinal index for this category"),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "compiler_name",
            "compiler_version",
            "contact_author",
            "contact_author_email",
            "date",
            "description",
            "dependencies",
            "hardware",
            "location",
            "mods",
            "name",
            "os",
            "os_version",
            "version",
        ]
    },
)

struct = Table(
    "struct",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("title", Text, nullable=True, comment="A title for the data block. The author should attempt to convey the essence of the structure archived in the CIF in the title, and to distinguish this structural result from others."),
    Column("pdbx_model_details", Text, nullable=True, comment="Text description of the methodology which produced this model structure."),
    Column("pdbx_model_type_details", Text, nullable=True, comment="A description of the type of structure model."),
    Column("pdbx_CASP_flag", Text, nullable=True, comment="The item indicates whether the entry is a CASP target, a CASD-NMR target, or similar target participating in methods development experiments."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "title",
            "pdbx_descriptor",
            "pdbx_model_details",
            "pdbx_formula_weight_method",
            "pdbx_model_type_details",
            "pdbx_details",
            "pdbx_title_text",
        ]
    },
)

struct_asym = Table(
    "struct_asym",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of this portion of the contents of the asymmetric unit."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("id", Text, nullable=True, comment="The value of _struct_asym.id must uniquely identify a record in the STRUCT_ASYM list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_modified", Text, nullable=True, comment="This data item indicates whether the structural elements are modified."),
    Column("pdbx_blank_PDB_chainid_flag", Text, nullable=True, comment="A flag indicating that this entity was originally labeled with a blank PDB chain id."),
    PrimaryKeyConstraint("pdbid", "id"),
    UniqueConstraint(
        "pdbid", "id", "entity_id", name="uq_pdbj_struct_asym_pdbid_id_entity_id"
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["details", "pdbx_modified", "pdbx_fraction_per_asym_unit"]},
)

struct_biol = Table(
    "struct_biol",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the biological unit."),
    Column("id", Text, nullable=True, comment="The value of _struct_biol.id must uniquely identify a record in the STRUCT_BIOL list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_parent_biol_id", Text, nullable=True, comment="An identifier for the parent biological assembly if this biological unit is part of a complex assembly."),
    Column("pdbx_formula_weight_method", Text, nullable=True, comment="Method used to determine _struct_biol.pdbx_formula_weight."),
    Column("pdbx_aggregation_state", Text, nullable=True, comment="A description of the structural aggregation in this assembly."),
    Column("pdbx_assembly_method", Text, nullable=True, comment="The method or experiment used to determine this assembly."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "details",
            "id",
            "pdbx_parent_biol_id",
            "pdbx_formula_weight_method",
            "pdbx_assembly_method",
        ]
    },
)

struct_biol_keywords = Table(
    "struct_biol_keywords",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("biol_id", Text, nullable=True, comment="This data item is a pointer to _struct_biol.id in the STRUCT_BIOL category."),
    Column("text", Text, nullable=True, comment="Keywords describing this biological entity."),
    PrimaryKeyConstraint("pdbid", "biol_id", "text"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, biol_id) -> struct_biol(pdbid, id)
    info={"keywords": ["biol_id", "text"]},
)

struct_conf = Table(
    "struct_conf",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("beg_label_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("beg_label_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("beg_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("beg_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("beg_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("beg_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("conf_type_id", Text, nullable=True, comment="This data item is a pointer to _struct_conf_type.id in the STRUCT_CONF_TYPE category."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the conformation assignment."),
    Column("end_label_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("end_label_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("end_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("end_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("end_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("end_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("id", Text, nullable=True, comment="The value of _struct_conf.id must uniquely identify a record in the STRUCT_CONF list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_beg_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment starts."),
    Column("pdbx_end_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the residue at which the conformation segment ends."),
    Column("pdbx_PDB_helix_class", Text, nullable=True, comment="This item is a place holder for the helix class used in the PDB HELIX record."),
    Column("pdbx_PDB_helix_length", Integer, nullable=True, comment="A placeholder for the lengths of the helix of the PDB HELIX record."),
    Column("pdbx_PDB_helix_id", Text, nullable=True, comment="A placeholder for the helix identifier of the PDB HELIX record."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, conf_type_id) -> struct_conf_type(pdbid, id)
    info={"keywords": ["details", "pdbx_PDB_helix_class"]},
)

struct_conf_type = Table(
    "struct_conf_type",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The descriptor that categorizes the type of the conformation of the backbone of the polymer (whether protein or nucleic acid). Explicit values for the torsion angles that define each conformation are not given here, but it is expected that the author would provide such information in either the _struct_conf_type.criteria or _struct_conf_type.reference data items, or both."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["criteria", "reference"]},
)

struct_conn = Table(
    "struct_conn",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("conn_type_id", Text, nullable=True, comment="This data item is a pointer to _struct_conn_type.id in the STRUCT_CONN_TYPE category."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the connection."),
    Column("id", Text, nullable=True, comment="The value of _struct_conn.id must uniquely identify a record in the STRUCT_CONN list. Note that this item need not be a number; it can be any unique identifier."),
    Column("ptnr1_label_asym_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("ptnr1_label_atom_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category."),
    Column("ptnr1_label_comp_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("ptnr1_label_seq_id", Integer, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("ptnr1_auth_asym_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("ptnr1_auth_comp_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("ptnr1_auth_seq_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("ptnr1_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the atom set specified by _struct_conn.ptnr1_label* to generate the first partner in the structure connection."),
    Column("ptnr2_label_asym_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("ptnr2_label_atom_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category."),
    Column("ptnr2_label_comp_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("ptnr2_label_seq_id", Integer, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("ptnr2_auth_asym_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("ptnr2_auth_comp_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("ptnr2_auth_seq_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("ptnr2_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the atom set specified by _struct_conn.ptnr2_label* to generate the second partner in the structure connection."),
    Column("pdbx_ptnr1_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("pdbx_ptnr1_label_alt_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("pdbx_ptnr2_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure connection. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("pdbx_ptnr2_label_alt_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure connection. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("pdbx_dist_value", Double, nullable=True, comment="Distance value for this contact."),
    Column("pdbx_value_order", Text, nullable=True, comment="The chemical bond order associated with the specified atoms in this contact."),
    Column("pdbx_leaving_atom_flag", Text, nullable=True, comment="This data item identifies if the linkage has displaced leaving atoms on both, one or none of the connected atoms forming the linkage. Leaving atoms are defined within their chemical defintions of each connected component."),
    Column("pdbx_role", Text, nullable=True, comment="The chemical or structural role of the interaction"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, conn_type_id) -> struct_conn_type(pdbid, id)
    info={"keywords": ["details", "pdbx_ptnr1_mod_name", "pdbx_ptnr1_sugar_name"]},
)

struct_conn_type = Table(
    "struct_conn_type",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The chemical or structural type of the interaction."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["criteria", "reference"]},
)

struct_keywords = Table(
    "struct_keywords",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("text", Text, nullable=True, comment="Keywords describing this structure."),
    Column("pdbx_keywords", Text, nullable=True, comment="Terms characterizing the macromolecular structure."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["text", "pdbx_keywords", "pdbx_details"]},
)

struct_mon_prot_cis = Table(
    "struct_mon_prot_cis",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("label_asym_id", Text, nullable=True, comment="A component of the identifier for the monomer. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_comp_id", Text, nullable=True, comment="A component of the identifier for the monomer. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="A component of the identifier for the monomer. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="A component of the identifier for the monomer. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="A component of the identifier for the monomer. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="A component of the identifier for the monomer. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("pdbx_auth_asym_id_2", Text, nullable=True, comment="Pointer to _atom_site.auth_asym_id."),
    Column("pdbx_auth_comp_id_2", Text, nullable=True, comment="Pointer to _atom_site.auth_comp_id."),
    Column("pdbx_auth_seq_id_2", Text, nullable=True, comment="Pointer to _atom_site.auth_seq_id"),
    Column("pdbx_label_asym_id_2", Text, nullable=True, comment="Pointer to _atom_site.label_asym_id."),
    Column("pdbx_label_comp_id_2", Text, nullable=True, comment="Pointer to _atom_site.label_comp_id."),
    Column("pdbx_label_seq_id_2", Integer, nullable=True, comment="Pointer to _atom_site.label_seq_id"),
    Column("pdbx_PDB_ins_code", Text, nullable=True, comment="Pointer to _atom_site.pdbx_PDB_ins_code"),
    Column("pdbx_PDB_ins_code_2", Text, nullable=True, comment="Pointer to _atom_site.pdbx_PDB_ins_code"),
    Column("pdbx_PDB_model_num", Integer, nullable=True, comment="Pointer to _atom_site.pdbx_PDB_model_num"),
    Column("pdbx_omega_angle", Text, nullable=True, comment="omega torsion angle"),
    Column("pdbx_id", Text, nullable=True, comment="ordinal index"),
    PrimaryKeyConstraint("pdbid", "pdbx_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

struct_ncs_dom = Table(
    "struct_ncs_dom",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the structural elements that comprise a domain in an ensemble of domains related by noncrystallographic symmetry."),
    Column("id", Text, nullable=True, comment="The value of _struct_ncs_dom.id must uniquely identify a record in the STRUCT_NCS_DOM list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_ens_id", Text, nullable=True, comment="This is a unique identifier for a collection NCS related domains. This references item '_struct_ncs_ens.id'."),
    PrimaryKeyConstraint("pdbid", "id", "pdbx_ens_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, pdbx_ens_id) -> struct_ncs_ens(pdbid, id)
    info={"keywords": ["details"]},
)

struct_ncs_dom_lim = Table(
    "struct_ncs_dom_lim",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("beg_label_alt_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins."),
    Column("beg_label_asym_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("beg_label_comp_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins."),
    Column("beg_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins."),
    Column("beg_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins."),
    Column("beg_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins."),
    Column("beg_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("dom_id", Text, nullable=True, comment="This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category."),
    Column("end_label_alt_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends."),
    Column("end_label_asym_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("end_label_comp_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends."),
    Column("end_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends."),
    Column("end_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends."),
    Column("end_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends."),
    Column("end_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the monomer at which this segment of the domain ends."),
    Column("selection_details", Text, nullable=True, comment="A text description of the selection of residues that correspond to this domain."),
    Column("pdbx_component_id", Integer, nullable=True, comment="Record number of the NCS domain limit assignment."),
    Column("pdbx_refine_code", Double, nullable=True, comment="record the refinement code number (from CCP4.)"),
    Column("pdbx_ens_id", Text, nullable=True, comment="This is a unique identifier for a collection NCS related domains. This references item '_struct_ncs_dom.pdbx_ens_id'."),
    PrimaryKeyConstraint("pdbid", "dom_id", "pdbx_ens_id", "pdbx_component_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, dom_id, pdbx_ens_id) -> struct_ncs_dom(pdbid, id, pdbx_ens_id)
    info={"keywords": ["selection_details"]},
)

struct_ncs_ens = Table(
    "struct_ncs_ens",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the ensemble."),
    Column("id", Text, nullable=True, comment="The value of _struct_ncs_ens.id must uniquely identify a record in the STRUCT_NCS_ENS list. Note that this item need not be a number; it can be any unique identifier."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "point_group"]},
)

struct_ncs_ens_gen = Table(
    "struct_ncs_ens_gen",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("dom_id_1", Text, nullable=True, comment="The identifier for the domain that will remain unchanged by the transformation operator. This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category."),
    Column("dom_id_2", Text, nullable=True, comment="The identifier for the domain that will be transformed by application of the transformation operator. This data item is a pointer to _struct_ncs_dom.id in the STRUCT_NCS_DOM category."),
    Column("ens_id", Text, nullable=True, comment="This data item is a pointer to _struct_ncs_ens.id in the STRUCT_NCS_ENS category."),
    Column("oper_id", Integer, nullable=True, comment="This data item is a pointer to _struct_ncs_oper.id in the STRUCT_NCS_OPER category."),
    PrimaryKeyConstraint("pdbid", "ens_id", "dom_id_1", "dom_id_2", "oper_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, ens_id) -> struct_ncs_ens(pdbid, id)
    # FK: (pdbid, oper_id) -> struct_ncs_oper(pdbid, id)
)

struct_ncs_oper = Table(
    "struct_ncs_oper",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("code", Text, nullable=True, comment="A code to indicate whether this operator describes a relationship between coordinates all of which are given in the data block (in which case the value of code is 'given'), or whether the operator is used to generate new coordinates from those that are given in the data block (in which case the value of code is 'generate')."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the noncrystallographic symmetry operator."),
    Column("id", Integer, nullable=True, comment="The value of _struct_ncs_oper.id must uniquely identify a record in the STRUCT_NCS_OPER list. Note that for PDB _struct_ncs_oper.id must be a number."),
    Column("matrix11", Double, nullable=True),
    Column("matrix12", Double, nullable=True),
    Column("matrix13", Double, nullable=True),
    Column("matrix21", Double, nullable=True),
    Column("matrix22", Double, nullable=True),
    Column("matrix23", Double, nullable=True),
    Column("matrix31", Double, nullable=True),
    Column("matrix32", Double, nullable=True),
    Column("matrix33", Double, nullable=True),
    Column("vector1", Double, nullable=True),
    Column("vector2", Double, nullable=True),
    Column("vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

struct_ref = Table(
    "struct_ref",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("db_code", Text, nullable=True, comment="The code for this entity or biological unit or for a closely related entity or biological unit in the named database."),
    Column("db_name", Text, nullable=True, comment="The name of the database containing reference information about this entity or biological unit."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("id", Text, nullable=True, comment="The value of _struct_ref.id must uniquely identify a record in the STRUCT_REF list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_db_accession", Text, nullable=True, comment="Accession code assigned by the reference database."),
    Column("pdbx_db_isoform", Text, nullable=True, comment="Database code assigned by the reference database for a sequence isoform. An isoform sequence is an alternative protein sequence that can be generated from the same gene by a single or by a combination of biological events such as: alternative promoter usage, alternative splicing, alternative initiation and ribosomal frameshifting."),
    Column("pdbx_seq_one_letter_code", Text, nullable=True, comment="Database chemical sequence expressed as string of one-letter amino acid codes."),
    Column("pdbx_align_begin", Text, nullable=True, comment="Beginning index in the chemical sequence from the reference database."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["biol_id", "db_code", "db_name", "details"]},
)

struct_ref_seq = Table(
    "struct_ref_seq",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("align_id", Text, nullable=True, comment="The value of _struct_ref_seq.align_id must uniquely identify a record in the STRUCT_REF_SEQ list. Note that this item need not be a number; it can be any unique identifier."),
    Column("db_align_beg", Integer, nullable=True, comment="The sequence position in the referenced database entry at which the alignment begins."),
    Column("db_align_end", Integer, nullable=True, comment="The sequence position in the referenced database entry at which the alignment ends."),
    Column("ref_id", Text, nullable=True, comment="This data item is a pointer to _struct_ref.id in the STRUCT_REF category."),
    Column("seq_align_beg", Integer, nullable=True, comment="The sequence position in the entity or biological unit described in the data block at which the alignment begins. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    Column("seq_align_end", Integer, nullable=True, comment="The sequence position in the entity or biological unit described in the data block at which the alignment ends. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    Column("pdbx_strand_id", Text, nullable=True, comment="The PDB strand/chain ID ."),
    Column("pdbx_db_accession", Text, nullable=True, comment="Accession code of the reference database."),
    Column("pdbx_db_align_beg_ins_code", Text, nullable=True, comment="Initial insertion code of the sequence segment of the reference database."),
    Column("pdbx_db_align_end_ins_code", Text, nullable=True, comment="Ending insertion code of the sequence segment of the reference database."),
    Column("pdbx_PDB_id_code", Text, nullable=True, comment="The PDB code of the structure."),
    Column("pdbx_auth_seq_align_beg", Text, nullable=True, comment="Initial position in the PDB sequence segment."),
    Column("pdbx_auth_seq_align_end", Text, nullable=True, comment="Ending position in the PDB sequence segment"),
    Column("pdbx_seq_align_beg_ins_code", Text, nullable=True, comment="Initial insertion code of the PDB sequence segment."),
    Column("pdbx_seq_align_end_ins_code", Text, nullable=True, comment="Ending insertion code of the sequence segment"),
    PrimaryKeyConstraint("pdbid", "align_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, ref_id) -> struct_ref(pdbid, id)
    info={"keywords": ["details"]},
)

struct_ref_seq_dif = Table(
    "struct_ref_seq_dif",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("align_id", Text, nullable=True, comment="This data item is a pointer to _struct_ref_seq.align_id in the STRUCT_REF_SEQ category."),
    Column("db_mon_id", Text, nullable=True, comment="The monomer type found at this position in the referenced database entry. This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the point differences between the sequence of the entity or biological unit described in the data block and that in the referenced database entry."),
    Column("mon_id", Text, nullable=True, comment="The monomer type found at this position in the sequence of the entity or biological unit described in this data block. This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("seq_num", Integer, nullable=True, comment="This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    Column("pdbx_pdb_id_code", Text, nullable=True, comment="The PDB ID code."),
    Column("pdbx_pdb_strand_id", Text, nullable=True, comment="PDB strand/chain id."),
    Column("pdbx_pdb_ins_code", Text, nullable=True, comment="Insertion code in PDB sequence"),
    Column("pdbx_auth_seq_num", Text, nullable=True, comment="The PDB sequence residue number."),
    Column("pdbx_seq_db_name", Text, nullable=True, comment="Sequence database name."),
    Column("pdbx_seq_db_accession_code", Text, nullable=True, comment="Sequence database accession number."),
    Column("pdbx_seq_db_seq_num", Text, nullable=True, comment="Sequence database sequence number."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="A synthetic integer primary key for this category."),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, align_id) -> struct_ref_seq(pdbid, align_id)
    info={"keywords": ["details"]},
)

struct_sheet = Table(
    "struct_sheet",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _struct_sheet.id must uniquely identify a record in the STRUCT_SHEET list. Note that this item need not be a number; it can be any unique identifier."),
    Column("number_strands", Integer, nullable=True, comment="The number of strands in the sheet. If a given range of residues bulges out from the strands, it is still counted as one strand. If a strand is composed of two different regions of polypeptide, it is still counted as one strand, as long as the proper hydrogen- bonding connections are made to adjacent strands."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "type"]},
)

struct_sheet_order = Table(
    "struct_sheet_order",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("range_id_1", Text, nullable=True, comment="This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category."),
    Column("range_id_2", Text, nullable=True, comment="This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category."),
    Column("sense", Text, nullable=True, comment="A flag to indicate whether the two designated residue ranges are parallel or antiparallel to one another."),
    Column("sheet_id", Text, nullable=True, comment="This data item is a pointer to _struct_sheet.id in the STRUCT_SHEET category."),
    PrimaryKeyConstraint("pdbid", "sheet_id", "range_id_1", "range_id_2"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, sheet_id) -> struct_sheet(pdbid, id)
)

struct_sheet_range = Table(
    "struct_sheet_range",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("beg_label_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("beg_label_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("beg_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("end_label_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("end_label_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("end_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("beg_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("beg_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("beg_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("end_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("end_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("end_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the residue at which the beta-sheet range ends. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("id", Text, nullable=True, comment="The value of _struct_sheet_range.id must uniquely identify a range in a given sheet in the STRUCT_SHEET_RANGE list. Note that this item need not be a number; it can be any unique identifier."),
    Column("sheet_id", Text, nullable=True, comment="This data item is a pointer to _struct_sheet.id in the STRUCT_SHEET category."),
    Column("pdbx_beg_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the residue at which the beta sheet range begins. Insertion code."),
    Column("pdbx_end_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the residue at which the beta sheet range ends. Insertion code."),
    PrimaryKeyConstraint("pdbid", "sheet_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, sheet_id) -> struct_sheet(pdbid, id)
)

struct_site = Table(
    "struct_site",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the site."),
    Column("id", Text, nullable=True, comment="The value of _struct_site.id must uniquely identify a record in the STRUCT_SITE list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_num_residues", Integer, nullable=True, comment="Number of residues in the site."),
    Column("pdbx_evidence_code", Text, nullable=True, comment="Source of evidence supporting the assignment of this site."),
    Column("pdbx_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the ligand in the site. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("pdbx_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the ligand in the site. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("pdbx_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the ligand in the site. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("pdbx_auth_ins_code", Text, nullable=True, comment="PDB insertion code for the ligand in the site."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "id", "pdbx_evidence_code"]},
)

struct_site_gen = Table(
    "struct_site_gen",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _struct_site_gen.id must uniquely identify a record in the STRUCT_SITE_GEN list. Note that this item need not be a number; it can be any unique identifier."),
    Column("label_asym_id", Text, nullable=True, comment="A component of the identifier for participants in the site. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_comp_id", Text, nullable=True, comment="A component of the identifier for participants in the site. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="A component of the identifier for participants in the site. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="A component of the identifier for participants in the site. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="A component of the identifier for participants in the site. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="A component of the identifier for participants in the site. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("site_id", Text, nullable=True, comment="This data item is a pointer to _struct_site.id in the STRUCT_SITE category."),
    Column("symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the atom set specified by _struct_site_gen.label* to generate a portion of the site."),
    Column("pdbx_auth_ins_code", Text, nullable=True, comment="PDB insertion code."),
    Column("pdbx_num_res", Integer, nullable=True, comment="Number of residues in the site."),
    PrimaryKeyConstraint("pdbid", "id", "site_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, site_id) -> struct_site(pdbid, id)
    info={"keywords": ["details", "id", "site_id"]},
)

struct_site_keywords = Table(
    "struct_site_keywords",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("site_id", Text, nullable=True, comment="This data item is a pointer to _struct_site.id in the STRUCT_SITE category."),
    Column("text", Text, nullable=True, comment="Keywords describing this site."),
    PrimaryKeyConstraint("pdbid", "site_id", "text"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, site_id) -> struct_site(pdbid, id)
    info={"keywords": ["site_id", "text"]},
)

symmetry = Table(
    "symmetry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("cell_setting", Text, nullable=True, comment="The cell settings for this space-group symmetry."),
    Column("Int_Tables_number", Integer, nullable=True, comment="Space-group number from International Tables for Crystallography Vol. A (2002)."),
    Column("space_group_name_Hall", Text, nullable=True, comment="Space-group symbol as described by Hall (1981). This symbol gives the space-group setting explicitly. Leave spaces between the separate components of the symbol. Ref: Hall, S. R. (1981). Acta Cryst. A37, 517-525; erratum (1981) A37, 921."),
    Column("space_group_name_H-M", Text, nullable=True),
    Column("pdbx_full_space_group_name_H-M", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "space_group_name_Hall",
            "space_group_name_H-M",
            "pdbx_full_space_group_name_H-M",
        ]
    },
)

symmetry_equiv = Table(
    "symmetry_equiv",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _symmetry_equiv.id must uniquely identify a record in the SYMMETRY_EQUIV category. Note that this item need not be a number; it can be any unique identifier."),
    Column("pos_as_xyz", Text, nullable=True, comment="Symmetry-equivalent position in the 'xyz' representation. Except for the space group P1, these data will be repeated in a loop. The format of the data item is as per International Tables for Crystallography Vol. A (2002). All equivalent positions should be entered, including those for lattice centring and a centre of symmetry, if present."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pos_as_xyz"]},
)

space_group = Table(
    "space_group",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_system", Text, nullable=True, comment="The name of the system of geometric crystal classes of space groups (crystal system) to which the space group belongs. Note that rhombohedral space groups belong to the trigonal system."),
    Column("id", Text, nullable=True, comment="This is the unique identifier for the SPACE_GROUP category."),
    Column("IT_number", Integer, nullable=True, comment="The number as assigned in International Tables for Crystallography Vol. A, specifying the proper affine class (i.e. the orientation-preserving affine class) of space groups (crystallographic space-group type) to which the space group belongs. This number defines the space-group type but not the coordinate system in which it is expressed."),
    Column("name_Hall", Text, nullable=True, comment="Space-group symbol defined by Hall. Each component of the space-group name is separated by a space or an underscore. The use of a space is strongly recommended. The underscore is only retained because it was used in old CIFs. It should not be used in new CIFs. _space_group.name_Hall uniquely defines the space group and its reference to a particular coordinate system. Ref: Hall, S. R. (1981). Acta Cryst. A37, 517-525; erratum (1981), A37, 921. [See also International Tables for Crystallography Vol. B (2001), Chapter 1.4, Appendix 1.4.2.]"),
    Column("name_H-M_alt", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name_Hall", "name_H-M_alt"]},
)

space_group_symop = Table(
    "space_group_symop",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="An arbitrary identifier that uniquely labels each symmetry operation in the list."),
    Column("operation_xyz", Text, nullable=True, comment="A parsable string giving one of the symmetry operations of the space group in algebraic form. If W is a matrix representation of the rotational part of the symmetry operation defined by the positions and signs of x, y and z, and w is a column of translations defined by the fractions, an equivalent position X' is generated from a given position X by the equation X' = WX + w (Note: X is used to represent bold_italics_x in International Tables for Crystallography Vol. A, Part 5) When a list of symmetry operations is given, it must contain a complete set of coordinate representatives which generates all the operations of the space group by the addition of all primitive translations of the space group. Such representatives are to be found as the coordinates of the general-equivalent position in International Tables for Crystallography Vol. A (2002), to which it is necessary to add any centring translations shown above the general-equivalent position. That is to say, it is necessary to list explicity all the symmetry operations required to generate all the atoms in the unit cell defined by the setting used."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["operation_xyz"]},
)

pdbx_database_PDB_obs_spr = Table(
    "pdbx_database_PDB_obs_spr",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="Identifier for the type of obsolete entry to be added to this entry."),
    Column("date", DateTime(timezone=True), nullable=True, comment="The date of replacement."),
    Column("pdb_id", Text, nullable=True, comment="The new PDB identifier for the replaced entry."),
    Column("replace_pdb_id", Text, nullable=True, comment="The PDB identifier for the replaced (OLD) entry/entries."),
    Column("details", Text, nullable=True, comment="Details related to the replaced or replacing entry."),
    PrimaryKeyConstraint("pdbid", "pdb_id", "replace_pdb_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["replace_pdb_id", "details"]},
)

pdbx_database_remark = Table(
    "pdbx_database_remark",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="A unique identifier for the PDB remark record."),
    Column("text", Text, nullable=True, comment="The full text of the PDB remark record."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["text"]},
)

pdbx_database_status = Table(
    "pdbx_database_status",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("status_code", Text, nullable=True, comment="Code for status of file."),
    Column("status_code_sf", Text, nullable=True, comment="Code for status of structure factor file."),
    Column("status_code_mr", Text, nullable=True, comment="Code for status of NMR constraints file."),
    Column("entry_id", Text, nullable=True, comment="The value of _pdbx_database_status.entry_id identifies the data block."),
    Column("recvd_initial_deposition_date", Date, nullable=True, comment="The date of initial deposition. (The first message for deposition has been received.)"),
    Column("SG_entry", Text, nullable=True, comment="This code indicates whether the entry belongs to Structural Genomics Project."),
    Column("deposit_site", Text, nullable=True, comment="The site where the file was deposited."),
    Column("process_site", Text, nullable=True, comment="The site where the file was deposited."),
    Column("status_code_cs", Text, nullable=True, comment="Code for status of chemical shift data file."),
    Column("status_code_nmr_data", Text, nullable=True, comment="Code for status of unified NMR data file."),
    Column("methods_development_category", Text, nullable=True, comment="The methods development category in which this entry has been placed."),
    Column("pdb_format_compatible", Text, nullable=True, comment="A flag indicating that the entry is compatible with the PDB format. A value of 'N' indicates that the no PDB format data file is corresponding to this entry is available in the PDB archive."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "name_depositor",
            "dep_release_code_chemical_shifts",
            "revision_description",
            "skip_PDB_REMARK",
        ]
    },
)

pdbx_poly_seq_scheme = Table(
    "pdbx_poly_seq_scheme",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("asym_id", Text, nullable=True, comment="Pointer to _atom_site.label_asym_id."),
    Column("entity_id", Text, nullable=True, comment="Pointer to _entity.id."),
    Column("seq_id", Integer, nullable=True, comment="Pointer to _entity_poly_seq.num"),
    Column("hetero", Text, nullable=True, comment="Pointer to _entity_poly_seq.hetero"),
    Column("mon_id", Text, nullable=True, comment="Pointer to _entity_poly_seq.mon_id."),
    Column("pdb_strand_id", Text, nullable=True, comment="PDB strand/chain id."),
    Column("ndb_seq_num", Integer, nullable=True, comment="NDB residue number."),
    Column("pdb_seq_num", Text, nullable=True, comment="PDB residue number."),
    Column("auth_seq_num", Text, nullable=True, comment="Author provided residue number. This value may differ from the PDB residue number and may not correspond to residue numbering within the coordinate records."),
    Column("pdb_mon_id", Text, nullable=True, comment="PDB residue identifier."),
    Column("auth_mon_id", Text, nullable=True, comment="Author provided residue identifier. This value may differ from the PDB residue identifier and may not correspond to residue identifier within the coordinate records."),
    Column("pdb_ins_code", Text, nullable=True, comment="PDB insertion code."),
    PrimaryKeyConstraint("pdbid", "asym_id", "entity_id", "seq_id", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id, seq_id, mon_id) -> entity_poly_seq(pdbid, entity_id, num, mon_id)
    # FK: (pdbid, asym_id, entity_id) -> struct_asym(pdbid, id, entity_id)
)

pdbx_nonpoly_scheme = Table(
    "pdbx_nonpoly_scheme",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("asym_id", Text, nullable=True, comment="Pointer to _atom_site.label_asym_id."),
    Column("entity_id", Text, nullable=True, comment="Pointer to _atom_site.label_entity_id."),
    Column("mon_id", Text, nullable=True, comment="Pointer to _atom_site.label_comp_id."),
    Column("pdb_strand_id", Text, nullable=True, comment="PDB strand/chain id."),
    Column("ndb_seq_num", Text, nullable=True, comment="NDB/RCSB residue number."),
    Column("pdb_seq_num", Text, nullable=True, comment="PDB residue number."),
    Column("auth_seq_num", Text, nullable=True, comment="Author provided residue numbering. This value may differ from the PDB residue number and may not correspond to residue numbering within the coordinate records."),
    Column("pdb_mon_id", Text, nullable=True, comment="PDB residue identifier."),
    Column("auth_mon_id", Text, nullable=True, comment="Author provided residue identifier. This value may differ from the PDB residue identifier and may not correspond to residue identification within the coordinate records."),
    Column("pdb_ins_code", Text, nullable=True, comment="PDB insertion code."),
    PrimaryKeyConstraint("pdbid", "asym_id", "ndb_seq_num"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_refine = Table(
    "pdbx_refine",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _pdbx_refine.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("R_factor_all_no_cutoff", Double, nullable=True, comment="R-value (all reflections, no cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("R_factor_obs_no_cutoff", Double, nullable=True, comment="R-value (working set reflections, no cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("free_R_factor_4sig_cutoff", Double, nullable=True, comment="R free value (4 sigma cutoff). Placeholder for PDB mapping of SHELXL refinement data."),
    Column("free_R_factor_no_cutoff", Double, nullable=True, comment="Free R-value (no cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("free_R_error_no_cutoff", Double, nullable=True, comment="Free R-value error(no cutoff)"),
    Column("free_R_val_test_set_size_perc_no_cutoff", Double, nullable=True, comment="Free R-value test set size (in percent, no cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("free_R_val_test_set_ct_no_cutoff", Double, nullable=True, comment="Free R-value test set count (no cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("number_reflns_obs_no_cutoff", Double, nullable=True, comment="Total number of reflections (no cutoff). Placeholder for PDB mapping of SHELXL refinement data."),
    Column("R_factor_all_4sig_cutoff", Double, nullable=True, comment="R-value (all reflections, 4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("R_factor_obs_4sig_cutoff", Double, nullable=True, comment="R-value (working set, 4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("free_R_val_test_set_size_perc_4sig_cutoff", Double, nullable=True, comment="Free R-value test set size (in percent, 4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("free_R_val_test_set_ct_4sig_cutoff", Double, nullable=True, comment="Free R-value test set count (4 sigma cutoff) Placeholder for PDB mapping of SHELXL refinement data."),
    Column("number_reflns_obs_4sig_cutoff", Double, nullable=True, comment="Total number of reflections (4 sigma cutoff). Placeholder for PDB mapping of SHELXL refinement data."),
    PrimaryKeyConstraint("pdbid", "entry_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["pdbx_refine_id"]},
)

pdbx_struct_sheet_hbond = Table(
    "pdbx_struct_sheet_hbond",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("range_id_1", Text, nullable=True, comment="This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category."),
    Column("range_id_2", Text, nullable=True, comment="This data item is a pointer to _struct_sheet_range.id in the STRUCT_SHEET_RANGE category."),
    Column("sheet_id", Text, nullable=True, comment="This data item is a pointer to _struct_sheet.id in the STRUCT_SHEET category."),
    Column("range_1_label_atom_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category."),
    Column("range_1_label_seq_id", Integer, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("range_1_label_comp_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("range_1_label_asym_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("range_1_auth_atom_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("range_1_auth_seq_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("range_1_auth_comp_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("range_1_auth_asym_id", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("range_1_PDB_ins_code", Text, nullable=True, comment="A component of the residue identifier for the first partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("range_2_label_atom_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category."),
    Column("range_2_label_seq_id", Integer, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("range_2_label_comp_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("range_2_label_asym_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("range_2_auth_atom_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("range_2_auth_seq_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("range_2_auth_comp_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("range_2_auth_asym_id", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("range_2_PDB_ins_code", Text, nullable=True, comment="A component of the residue identifier for the second partner of the registration hydrogen bond between two residue ranges in a sheet. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    PrimaryKeyConstraint("pdbid", "sheet_id", "range_id_1", "range_id_2"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, sheet_id) -> struct_sheet(pdbid, id)
)

pdbx_xplor_file = Table(
    "pdbx_xplor_file",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("serial_no", Text, nullable=True, comment="Serial number."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _pdbx_xplor_file.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("param_file", Text, nullable=True, comment="Parameter file name in X-PLOR/CNS refinement."),
    Column("topol_file", Text, nullable=True, comment="Topology file name in X-PLOR/CNS refinement."),
    PrimaryKeyConstraint("pdbid", "serial_no", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "param_file", "topol_file"]},
)

pdbx_database_related = Table(
    "pdbx_database_related",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("db_name", Text, nullable=True, comment="The name of the database containing the related entry."),
    Column("details", Text, nullable=True, comment="A description of the related entry."),
    Column("db_id", Text, nullable=True, comment="The identifying code in the related database."),
    Column("content_type", Text, nullable=True, comment="The identifying content type of the related entry."),
    PrimaryKeyConstraint("pdbid", "db_name", "db_id", "content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "db_id"]},
)

pdbx_exptl_crystal_grow_comp = Table(
    "pdbx_exptl_crystal_grow_comp",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_id", Text, nullable=True, comment="This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category."),
    Column("comp_id", Text, nullable=True, comment="The value of _exptl_crystal_grow_comp.comp_id must uniquely identify each item in the PDBX_EXPTL_CRYSTAL_GROW_COMP list. Note that this item need not be a number; it can be any unique identifier."),
    Column("comp_name", Text, nullable=True, comment="A common name for the component of the solution."),
    Column("sol_id", Text, nullable=True, comment="An identifier for the solution to which the given solution component belongs."),
    Column("conc", Double, nullable=True, comment="The concentration value of the solution component."),
    Column("conc_units", Text, nullable=True, comment="The concentration units for the solution component."),
    PrimaryKeyConstraint("pdbid", "comp_id", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
    info={"keywords": ["comp_name", "sol_id", "conc_range"]},
)

pdbx_exptl_crystal_grow_sol = Table(
    "pdbx_exptl_crystal_grow_sol",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_id", Text, nullable=True, comment="This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category."),
    Column("sol_id", Text, nullable=True, comment="An identifier for this solution (e.g. precipitant, reservoir, macromolecule)"),
    Column("volume", Double, nullable=True, comment="The volume of the solution."),
    Column("volume_units", Text, nullable=True, comment="The volume units of the solution."),
    Column("pH", Double, nullable=True, comment="The pH of the solution."),
    PrimaryKeyConstraint("pdbid", "sol_id", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
)

pdbx_exptl_crystal_cryo_treatment = Table(
    "pdbx_exptl_crystal_cryo_treatment",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_id", Text, nullable=True, comment="This data item is a pointer to _exptl_crystal.id in the EXPTL_CRYSTAL category."),
    Column("final_solution_details", Text, nullable=True, comment="Details of the final solution used in the treatment of this crystal"),
    Column("soaking_details", Text, nullable=True, comment="Details of the soaking treatment applied to this crystal."),
    Column("cooling_details", Text, nullable=True, comment="Details of the cooling treatment applied to this crystal."),
    PrimaryKeyConstraint("pdbid", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
    info={
        "keywords": [
            "final_solution_details",
            "soaking_details",
            "cooling_details",
            "annealing_details",
        ]
    },
)

pdbx_refine_tls = Table(
    "pdbx_refine_tls",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_refine_tls.id must uniquely identify a record in the PDBX_REFINE_TLS list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _pdbx_refine_tls.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("details", Text, nullable=True, comment="A description of the TLS group, such as a domain name or a chemical group name."),
    Column("method", Text, nullable=True, comment="The method by which the TLS parameters were obtained."),
    Column("origin_x", Double, nullable=True, comment="The x coordinate in angstroms of the origin to which the TLS parameters are referred, specified according to a set of orthogonal Cartesian axes related to the cell axes as given in _atom_sites.Cartn_transform_axes. If the origin is omitted, it is assumed to be the centre of reaction of the group, in which case S must be symmetric"),
    Column("origin_y", Double, nullable=True, comment="The y coordinate in angstroms of the origin to which the TLS parameters are referred, specified according to a set of orthogonal Cartesian axes related to the cell axes as given in _atom_sites.Cartn_transform_axes. If the origin is omitted, it is assumed to be the centre of reaction of the group, in which case S must be symmetric"),
    Column("origin_z", Double, nullable=True, comment="The z coordinate in angstroms of the origin to which the TLS parameters are referred, specified according to a set of orthogonal Cartesian axes related to the cell axes as given in _atom_sites.Cartn_transform_axes. If the origin is omitted, it is assumed to be the centre of reaction of the group, in which case S must be symmetric"),
    Column("T11", Double, nullable=True),
    Column("T11_esd", Double, nullable=True),
    Column("T12", Double, nullable=True),
    Column("T12_esd", Double, nullable=True),
    Column("T13", Double, nullable=True),
    Column("T13_esd", Double, nullable=True),
    Column("T22", Double, nullable=True),
    Column("T22_esd", Double, nullable=True),
    Column("T23", Double, nullable=True),
    Column("T23_esd", Double, nullable=True),
    Column("T33", Double, nullable=True),
    Column("T33_esd", Double, nullable=True),
    Column("L11", Double, nullable=True),
    Column("L11_esd", Double, nullable=True),
    Column("L12", Double, nullable=True),
    Column("L12_esd", Double, nullable=True),
    Column("L13", Double, nullable=True),
    Column("L13_esd", Double, nullable=True),
    Column("L22", Double, nullable=True),
    Column("L22_esd", Double, nullable=True),
    Column("L23", Double, nullable=True),
    Column("L23_esd", Double, nullable=True),
    Column("L33", Double, nullable=True),
    Column("L33_esd", Double, nullable=True),
    Column("S11", Double, nullable=True),
    Column("S11_esd", Double, nullable=True),
    Column("S12", Double, nullable=True),
    Column("S12_esd", Double, nullable=True),
    Column("S13", Double, nullable=True),
    Column("S13_esd", Double, nullable=True),
    Column("S21", Double, nullable=True),
    Column("S21_esd", Double, nullable=True),
    Column("S22", Double, nullable=True),
    Column("S22_esd", Double, nullable=True),
    Column("S23", Double, nullable=True),
    Column("S23_esd", Double, nullable=True),
    Column("S31", Double, nullable=True),
    Column("S31_esd", Double, nullable=True),
    Column("S32", Double, nullable=True),
    Column("S32_esd", Double, nullable=True),
    Column("S33", Double, nullable=True),
    Column("S33_esd", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "details"]},
)

pdbx_refine_tls_group = Table(
    "pdbx_refine_tls_group",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_refine_tls_group.id must uniquely identify a record in the REFINE_TLS_GROUP list for a particular refinement. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_refine_id", Text, nullable=True, comment="This data item uniquely identifies a refinement within an entry. _pdbx_refine_tls_group.pdbx_refine_id can be used to distinguish the results of joint refinements."),
    Column("refine_tls_id", Text, nullable=True, comment="This data item is a pointer to _pdbx_refine_tls.id in the REFINE_TLS category."),
    Column("beg_label_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("beg_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range begins."),
    Column("beg_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("beg_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("beg_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range begins. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("end_label_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("end_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range ends."),
    Column("end_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("end_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("end_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the residue at which the TLS fragment range ends. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("selection", Text, nullable=True, comment="A qualification of the subset of atoms in the specified range included in the TLS fragment."),
    Column("selection_details", Text, nullable=True, comment="A text description of subset of atoms included included in the TLS fragment."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, refine_tls_id) -> pdbx_refine_tls(pdbid, id)
    info={"keywords": ["pdbx_refine_id", "selection", "selection_details"]},
)

pdbx_contact_author = Table(
    "pdbx_contact_author",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="A unique integer identifier for this author"),
    Column("email", Text, nullable=True, comment="The electronic mail address of the author of the data block to whom correspondence should be addressed, in a form recognisable to international networks."),
    Column("name_first", Text, nullable=True, comment="The first name of the author of the data block to whom correspondence should be addressed."),
    Column("name_last", Text, nullable=True, comment="The last name of the author of the data block to whom correspondence should be addressed."),
    Column("name_mi", Text, nullable=True, comment="The middle initial(s) of the author of the data block to whom correspondence should be addressed."),
    Column("role", Text, nullable=True, comment="The role of this author in the project depositing this data."),
    Column("identifier_ORCID", Text, nullable=True, comment="The Open Researcher and Contributor ID (ORCID)."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "address_1",
            "address_2",
            "address_3",
            "legacy_address",
            "city",
            "state_province",
            "postal_code",
            "email",
            "fax",
            "name_first",
            "name_last",
            "name_mi",
            "country",
            "phone",
            "identifier_ORCID",
        ]
    },
)

pdbx_SG_project = Table(
    "pdbx_SG_project",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="A unique integer identifier for this center"),
    Column("project_name", Text, nullable=True, comment="The value identifies the Structural Genomics project."),
    Column("full_name_of_center", Text, nullable=True, comment="The value identifies the full name of center."),
    Column("initial_of_center", Text, nullable=True, comment="The value identifies the full name of center."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_nmr_details = Table(
    "pdbx_nmr_details",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="The entry ID for the structure determination."),
    Column("text", Text, nullable=True, comment="Additional details describing the NMR experiment."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["text"]},
)

pdbx_nmr_sample_details = Table(
    "pdbx_nmr_sample_details",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("solution_id", Text, nullable=True, comment="The name (number) of the sample."),
    Column("contents", Text, nullable=True, comment="A complete description of each NMR sample. Include the concentration and concentration units for each component (include buffers, etc.). For each component describe the isotopic composition, including the % labeling level, if known. For example: 1. Uniform (random) labeling with 15N: U-15N 2. Uniform (random) labeling with 13C, 15N at known labeling levels: U-95% 13C;U-98% 15N 3. Residue selective labeling: U-95% 15N-Thymine 4. Site specific labeling: 95% 13C-Ala18, 5. Natural abundance labeling in an otherwise uniformly labeled biomolecule is designated by NA: U-13C; NA-K,H"),
    Column("solvent_system", Text, nullable=True, comment="The solvent system used for this sample."),
    Column("label", Text, nullable=True, comment="A value that uniquely identifies this sample from the other samples listed in the entry."),
    Column("type", Text, nullable=True, comment="A descriptive term for the sample that defines the general physical properties of the sample."),
    Column("details", Text, nullable=True, comment="Brief description of the sample providing additional information not captured by other items in the category."),
    PrimaryKeyConstraint("pdbid", "solution_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["contents", "solvent_system", "label", "details"]},
)

pdbx_nmr_exptl_sample = Table(
    "pdbx_nmr_exptl_sample",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("solution_id", Text, nullable=True, comment="The name (number) of the sample."),
    Column("component", Text, nullable=True, comment="The name of each component in the sample"),
    Column("concentration", Double, nullable=True, comment="The concentration value of the component."),
    Column("concentration_range", Text, nullable=True, comment="The concentration range for the component."),
    Column("concentration_units", Text, nullable=True, comment="The concentration units of the component."),
    Column("isotopic_labeling", Text, nullable=True, comment="The isotopic composition of each component, including the % labeling level, if known. For example: 1. Uniform (random) labeling with 15N: U-15N 2. Uniform (random) labeling with 13C, 15N at known labeling levels: U-95% 13C;U-98% 15N 3. Residue selective labeling: U-95% 15N-Thymine 4. Site specific labeling: 95% 13C-Ala18, 5. Natural abundance labeling in an otherwise uniformly labled biomolecule is designated by NA: U-13C; NA-K,H"),
    PrimaryKeyConstraint("pdbid", "solution_id", "component"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["component", "isotopic_labeling"]},
)

pdbx_nmr_exptl_sample_conditions = Table(
    "pdbx_nmr_exptl_sample_conditions",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("conditions_id", Text, nullable=True, comment="The condition number as defined above."),
    Column("temperature", Text, nullable=True, comment="The temperature (in kelvin) at which NMR data were collected."),
    Column("pressure_units", Text, nullable=True, comment="The units of pressure at which NMR data were collected."),
    Column("pressure", Text, nullable=True, comment="The pressure at which NMR data were collected."),
    Column("pH", Text, nullable=True, comment="The pH at which the NMR data were collected."),
    Column("ionic_strength", Text, nullable=True, comment="The ionic strength at which the NMR data were collected -in lieu of this enter the concentration and identity of the salt in the sample."),
    Column("details", Text, nullable=True, comment="General details describing conditions of both the sample and the environment during measurements."),
    Column("ionic_strength_err", Double, nullable=True, comment="Estimate of the standard error for the value for the sample ionic strength."),
    Column("ionic_strength_units", Text, nullable=True, comment="Units for the value of the sample condition ionic strength.."),
    Column("label", Text, nullable=True, comment="A descriptive label that uniquely identifies this set of sample conditions."),
    Column("pH_err", Double, nullable=True, comment="Estimate of the standard error for the value for the sample pH."),
    Column("pH_units", Text, nullable=True, comment="Units for the value of the sample condition pH."),
    Column("pressure_err", Double, nullable=True, comment="Estimate of the standard error for the value for the sample pressure."),
    Column("temperature_err", Double, nullable=True, comment="Estimate of the standard error for the value for the sample temperature."),
    Column("temperature_units", Text, nullable=True, comment="Units for the value of the sample condition temperature."),
    PrimaryKeyConstraint("pdbid", "conditions_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pressure", "ionic_strength", "details", "label"]},
)

pdbx_nmr_spectrometer = Table(
    "pdbx_nmr_spectrometer",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("spectrometer_id", Text, nullable=True, comment="Assign a numerical ID to each instrument."),
    Column("model", Text, nullable=True, comment="The model of the NMR spectrometer."),
    Column("type", Text, nullable=True, comment="Select the instrument manufacturer(s) and the model(s) of the NMR(s) used for this work."),
    Column("manufacturer", Text, nullable=True, comment="The name of the manufacturer of the spectrometer."),
    Column("field_strength", Double, nullable=True, comment="The field strength in MHz of the spectrometer"),
    Column("details", Text, nullable=True, comment="A text description of the NMR spectrometer."),
    PrimaryKeyConstraint("pdbid", "spectrometer_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["model", "type", "manufacturer", "details", "name"]},
)

pdbx_nmr_exptl = Table(
    "pdbx_nmr_exptl",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("experiment_id", Text, nullable=True, comment="A numerical ID for each experiment."),
    Column("conditions_id", Text, nullable=True, comment="The number to identify the set of sample conditions."),
    Column("solution_id", Text, nullable=True, comment="The solution_id from the Experimental Sample to identify the sample that these conditions refer to. [Remember to save the entries here before returning to the Experimental Sample form]"),
    Column("type", Text, nullable=True, comment="The type of NMR experiment."),
    Column("spectrometer_id", Integer, nullable=True, comment="Pointer to '_pdbx_nmr_spectrometer.spectrometer_id'"),
    Column("sample_state", Text, nullable=True, comment="Physical state of the sample either anisotropic or isotropic."),
    PrimaryKeyConstraint("pdbid", "experiment_id", "conditions_id", "solution_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["type"]},
)

pdbx_nmr_software = Table(
    "pdbx_nmr_software",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="An ordinal index for this category"),
    Column("classification", Text, nullable=True, comment="The purpose of the software."),
    Column("name", Text, nullable=True, comment="The name of the software used for the task."),
    Column("version", Text, nullable=True, comment="The version of the software."),
    Column("authors", Text, nullable=True, comment="The name of the authors of the software used in this procedure."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["classification", "name", "version", "authors", "details"]},
)

pdbx_nmr_constraints = Table(
    "pdbx_nmr_constraints",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="You can leave this blank as an ID will be assigned by the MSD to the constraint file."),
    Column("NOE_constraints_total", Integer, nullable=True, comment="The total number of all NOE constraints used in the final structure calculation."),
    Column("NOE_intraresidue_total_count", Integer, nullable=True, comment="The total number of all intraresidue, [i-j]=0, NOE constraints used in the final structure calculation."),
    Column("NOE_interentity_total_count", Integer, nullable=True, comment="The total number of interentity, NOE constraints used in the final structure calculation. This field should only be if system is complex -i.e more than one entity e.g. a dimer or ligand-protein complex"),
    Column("NOE_sequential_total_count", Integer, nullable=True, comment="The total number of sequential, [i-j]=1, NOE constraints used in the final structure calculation."),
    Column("NOE_medium_range_total_count", Integer, nullable=True, comment="The total number of medium range 1<[i-j]<=5 NOE constraints used in the final structure calculation."),
    Column("NOE_long_range_total_count", Integer, nullable=True, comment="The total number of long range [i-j]>5 NOE constraints used in the final structure calculation."),
    Column("protein_phi_angle_constraints_total_count", Integer, nullable=True, comment="The total number of phi angle constraints used in the final structure calculation"),
    Column("protein_psi_angle_constraints_total_count", Integer, nullable=True, comment="The total number of psi angle constraints used in the final structure calculation."),
    Column("protein_chi_angle_constraints_total_count", Integer, nullable=True, comment="The total number of chi angle constraints used in the final structure calculation."),
    Column("protein_other_angle_constraints_total_count", Integer, nullable=True, comment="The total number of other angle constraints used in the final structure calculation."),
    Column("hydrogen_bond_constraints_total_count", Integer, nullable=True, comment="The total number of hydrogen bond constraints used in the final structure calculation."),
    Column("disulfide_bond_constraints_total_count", Integer, nullable=True, comment="The total number of disulfide bond constraints used in the final structure calculation."),
    Column("NA_alpha-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_beta-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_gamma-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_delta-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_epsilon-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_chi-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_other-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_sugar_pucker_constraints_total_count", Integer, nullable=True, comment="The total number of nucleic acid sugar pucker constraints used in the final structure calculation."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "NOE_interproton_distance_evaluation",
            "NOE_pseudoatom_corrections",
            "NOE_motional_averaging_correction",
        ]
    },
)

pdbx_nmr_ensemble = Table(
    "pdbx_nmr_ensemble",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="Leave this blank as the ID is provided by the MSD"),
    Column("conformers_calculated_total_number", Integer, nullable=True, comment="The total number of conformer (models) that were calculated in the final round."),
    Column("conformers_submitted_total_number", Integer, nullable=True, comment="The number of conformer (models) that are submitted for the ensemble."),
    Column("conformer_selection_criteria", Text, nullable=True, comment="By highlighting the appropriate choice(s), describe how the submitted conformer (models) were selected."),
    Column("representative_conformer", Integer, nullable=True, comment="The number of the conformer identified as most representative."),
    Column("average_constraints_per_residue", Integer, nullable=True, comment="The average number of constraints per residue for the ensemble"),
    Column("average_constraint_violations_per_residue", Integer, nullable=True, comment="The average number of constraint violations on a per residue basis for the ensemble."),
    Column("maximum_distance_constraint_violation", Double, nullable=True, comment="The maximum distance constraint violation for the ensemble."),
    Column("average_distance_constraint_violation", Double, nullable=True, comment="The average distance restraint violation for the ensemble."),
    Column("maximum_upper_distance_constraint_violation", Double, nullable=True, comment="The maximum upper distance constraint violation for the ensemble."),
    Column("maximum_lower_distance_constraint_violation", Double, nullable=True, comment="The maximum lower distance constraint violation for the ensemble."),
    Column("distance_constraint_violation_method", Text, nullable=True, comment="Describe the method used to calculate the distance constraint violation statistics, i.e. are they calculated over all the distance constraints or calculated for violations only?"),
    Column("maximum_torsion_angle_constraint_violation", Double, nullable=True, comment="The maximum torsion angle constraint violation for the ensemble."),
    Column("average_torsion_angle_constraint_violation", Double, nullable=True, comment="The average torsion angle constraint violation for the ensemble."),
    Column("torsion_angle_constraint_violation_method", Text, nullable=True, comment="This item describes the method used to calculate the torsion angle constraint violation statistics. i.e. are the entered values based on all torsion angle or calculated for violations only?"),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "conformer_selection_criteria",
            "distance_constraint_violation_method",
            "torsion_angle_constraint_violation_method",
        ]
    },
)

pdbx_nmr_ensemble_rms = Table(
    "pdbx_nmr_ensemble_rms",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="'?'"),
    Column("residue_range_begin", Integer, nullable=True, comment="Structure statistics are often calculated only over the well-ordered region(s) of the biopolymer. Portions of the macromolecule are often mobile and disordered, hence they are excluded in calculating the statistics. To define the range(s) over which the statistics are calculated, enter the beginning residue number(s): e.g. if the regions used were 5-32 and 41-69, enter 5,41"),
    Column("chain_range_begin", Text, nullable=True, comment="The beginning chain id."),
    Column("residue_range_end", Integer, nullable=True, comment="The ending residue number: e.g. 32,69."),
    Column("chain_range_end", Text, nullable=True, comment="The ending chain id:"),
    Column("atom_type", Text, nullable=True, comment="Statistics are often calculated over only some of the atoms, e.g. backbone, or heavy atoms. Describe which type of atoms are used for the statistical analysis."),
    Column("distance_rms_dev", Double, nullable=True, comment="The distance rmsd to the mean structure for the ensemble of structures."),
    Column("distance_rms_dev_error", Double, nullable=True, comment="The error in the distance rmsd."),
    Column("covalent_bond_rms_dev", Double, nullable=True, comment="The covalent bond rmsd to the target value for the ensemble."),
    Column("bond_angle_rms_dev", Double, nullable=True, comment="The bond angle rmsd to the target values for the ensemble."),
    Column("improper_torsion_angle_rms_dev", Double, nullable=True, comment="The improper torsion angle rmsd to the target values for the ensemble."),
    Column("dihedral_angles_rms_dev", Double, nullable=True, comment="The dihedral angle rmsd to the target values for the ensemble."),
    Column("dihedral_angles_rms_dev_error", Double, nullable=True, comment="The error of the rmsd dihedral angles."),
    Column("coord_average_rmsd_method", Text, nullable=True, comment="Describe the method for calculating the coordinate average rmsd."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["coord_average_rmsd_method"]},
)

pdbx_nmr_representative = Table(
    "pdbx_nmr_representative",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="msd will assign the ID."),
    Column("conformer_id", Text, nullable=True, comment="If a member of the ensemble has been selected as a representative structure, identify it by its model number."),
    Column("selection_criteria", Text, nullable=True, comment="By highlighting the appropriate choice(s), describe the criteria used to select this structure as a representative structure, or if an average structure has been calculated describe how this was done."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["conformer_id", "selection_criteria"]},
)

pdbx_nmr_refine = Table(
    "pdbx_nmr_refine",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="You can leave this blank as an ID will be assigned by the RCSB to the constraint file."),
    Column("method", Text, nullable=True, comment="The method used to determine the structure."),
    Column("details", Text, nullable=True, comment="Additional details about the NMR refinement."),
    Column("software_ordinal", Integer, nullable=True, comment="Pointer to _software.ordinal"),
    PrimaryKeyConstraint("pdbid", "entry_id", "software_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["method", "details"]},
)

ndb_struct_conf_na = Table(
    "ndb_struct_conf_na",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("feature", Text, nullable=True, comment="This data item identifies a secondary structure feature of this entry."),
    PrimaryKeyConstraint("pdbid", "entry_id", "feature"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

ndb_struct_na_base_pair = Table(
    "ndb_struct_na_base_pair",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("model_number", Integer, nullable=True, comment="Describes the model number of the base pair. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("pair_number", Integer, nullable=True, comment="Sequential number of pair in the pair sequence."),
    Column("pair_name", Text, nullable=True, comment="Text label for this base pair."),
    Column("i_label_asym_id", Text, nullable=True, comment="Describes the asym id of the i-th base in the base pair. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("i_label_comp_id", Text, nullable=True, comment="Describes the component id of the i-th base in the base pair. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("i_label_seq_id", Integer, nullable=True, comment="Describes the sequence number of the i-th base in the base pair. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("i_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the coordinates of the i-th base to generate the first partner in the base pair."),
    Column("j_label_asym_id", Text, nullable=True, comment="Describes the asym id of the j-th base in the base pair. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("j_label_comp_id", Text, nullable=True, comment="Describes the component id of the j-th base in the base pair. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("j_label_seq_id", Integer, nullable=True, comment="Describes the sequence number of the j-th base in the base pair. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("j_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the coordinates of the j-th base to generate the second partner in the base pair."),
    Column("i_auth_asym_id", Text, nullable=True, comment="Describes the asym id of the i-th base in the base pair. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("i_auth_seq_id", Text, nullable=True, comment="Describes the sequence number of the i-th base in the base pair. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("i_PDB_ins_code", Text, nullable=True, comment="Describes the PDB insertion code of the i-th base in the base pair. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("j_auth_asym_id", Text, nullable=True, comment="Describes the asym id of the j-th base in the base pair. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("j_auth_seq_id", Text, nullable=True, comment="Describes the sequence number of the j-th base in the base pair. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("j_PDB_ins_code", Text, nullable=True, comment="Describes the PDB insertion code of the j-th base in the base pair. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("shear", Double, nullable=True, comment="The value of the base pair shear parameter."),
    Column("stretch", Double, nullable=True, comment="The value of the base pair stretch parameter."),
    Column("stagger", Double, nullable=True, comment="The value of the base pair stagger parameter."),
    Column("buckle", Double, nullable=True, comment="The value of the base pair buckle parameter."),
    Column("propeller", Double, nullable=True, comment="The value of the base pair propeller parameter."),
    Column("opening", Double, nullable=True, comment="The value of the base pair opening parameter."),
    Column("hbond_type_12", Integer, nullable=True, comment="Base pair classification of Westhoff and Leontis."),
    Column("hbond_type_28", Integer, nullable=True, comment="Base pair classification of Saenger"),
    PrimaryKeyConstraint(
        "pdbid",
        "model_number",
        "i_label_comp_id",
        "i_label_asym_id",
        "i_label_seq_id",
        "i_symmetry",
        "j_label_comp_id",
        "j_label_asym_id",
        "j_label_seq_id",
        "j_symmetry",
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pair_name"]},
)

ndb_struct_na_base_pair_step = Table(
    "ndb_struct_na_base_pair_step",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("model_number", Integer, nullable=True, comment="Describes the model number of the base pair step. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("step_number", Integer, nullable=True, comment="The sequence number of this step in the step sequence."),
    Column("step_name", Text, nullable=True, comment="The text name of this step."),
    Column("i_label_asym_id_1", Text, nullable=True, comment="Describes the asym id of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("i_label_comp_id_1", Text, nullable=True, comment="Describes the component id of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("i_label_seq_id_1", Integer, nullable=True, comment="Describes the sequence number of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("i_symmetry_1", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the coordinates of the i-th base to generate the first partner in the first base pair of the step."),
    Column("j_label_asym_id_1", Text, nullable=True, comment="Describes the asym id of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("j_label_comp_id_1", Text, nullable=True, comment="Describes the component id of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("j_label_seq_id_1", Integer, nullable=True, comment="Describes the sequence number of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("j_symmetry_1", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the coordinates of the j-th base to generate the second partner in the first base pair of the step."),
    Column("i_label_asym_id_2", Text, nullable=True, comment="Describes the asym id of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("i_label_comp_id_2", Text, nullable=True, comment="Describes the component id of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("i_label_seq_id_2", Integer, nullable=True, comment="Describes the sequence number of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("i_symmetry_2", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the coordinates of the i-th base to generate the first partner in the second base pair of the step."),
    Column("j_label_asym_id_2", Text, nullable=True, comment="Describes the asym id of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("j_label_comp_id_2", Text, nullable=True, comment="Describes the component id of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("j_label_seq_id_2", Integer, nullable=True, comment="Describes the sequence number of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("j_symmetry_2", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the coordinates of the j-th base to generate the second partner in the second base pair of the step."),
    Column("i_auth_asym_id_1", Text, nullable=True, comment="Describes the author's asym id of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("i_auth_seq_id_1", Text, nullable=True, comment="Describes the author's sequence number of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("i_PDB_ins_code_1", Text, nullable=True, comment="Describes the PDB insertion code of the i-th base in the first base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("j_auth_asym_id_1", Text, nullable=True, comment="Describes the author's asym id of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("j_auth_seq_id_1", Text, nullable=True, comment="Describes the author's sequence number of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("j_PDB_ins_code_1", Text, nullable=True, comment="Describes the PDB insertion code of the j-th base in the first base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("i_auth_asym_id_2", Text, nullable=True, comment="Describes the author's asym id of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("i_auth_seq_id_2", Text, nullable=True, comment="Describes the author's sequence number of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("i_PDB_ins_code_2", Text, nullable=True, comment="Describes the PDB insertion code of the i-th base in the second base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("j_auth_asym_id_2", Text, nullable=True, comment="Describes the author's asym id of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("j_auth_seq_id_2", Text, nullable=True, comment="Describes the author's sequence number of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("j_PDB_ins_code_2", Text, nullable=True, comment="Describes the PDB insertion code of the j-th base in the second base pair of the step. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("shift", Double, nullable=True, comment="The value of the base pair step shift parameter."),
    Column("slide", Double, nullable=True, comment="The value of the base pair step slide parameter."),
    Column("rise", Double, nullable=True, comment="The value of the base pair step rise parameter."),
    Column("tilt", Double, nullable=True, comment="The value of the base pair step tilt parameter."),
    Column("roll", Double, nullable=True, comment="The value of the base pair step roll parameter."),
    Column("twist", Double, nullable=True, comment="The value of the base pair step twist parameter."),
    Column("x_displacement", Double, nullable=True, comment="The value of the base pair step X displacement parameter."),
    Column("y_displacement", Double, nullable=True, comment="The value of the base pair step Y displacement parameter."),
    Column("helical_rise", Double, nullable=True, comment="The value of the base pair step helical rise parameter."),
    Column("inclination", Double, nullable=True, comment="The value of the base pair step inclination parameter."),
    Column("tip", Double, nullable=True, comment="The value of the base pair step twist parameter."),
    Column("helical_twist", Double, nullable=True, comment="The value of the base pair step helical twist parameter."),
    PrimaryKeyConstraint(
        "pdbid",
        "model_number",
        "i_label_comp_id_1",
        "i_label_asym_id_1",
        "i_label_seq_id_1",
        "i_symmetry_1",
        "j_label_comp_id_1",
        "j_label_asym_id_1",
        "j_label_seq_id_1",
        "j_symmetry_1",
        "i_label_comp_id_2",
        "i_label_asym_id_2",
        "i_label_seq_id_2",
        "i_symmetry_2",
        "j_label_comp_id_2",
        "j_label_asym_id_2",
        "j_label_seq_id_2",
        "j_symmetry_2",
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["step_name"]},
)

pdbx_entity_nonpoly = Table(
    "pdbx_entity_nonpoly",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("comp_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("name", Text, nullable=True, comment="A name for the non-polymer entity"),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["name"]},
)

pdbx_phasing_dm = Table(
    "pdbx_phasing_dm",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="The value of _pdbx_phasing_dm.entry_id identifies the data block."),
    Column("method", Text, nullable=True, comment="The value of _pdbx_phasing_dm.method identifies the method used for density modification"),
    Column("mask_type", Text, nullable=True, comment="The value of _pdbx_phasing_dm.mask_type identifies the type of mask used for density modification"),
    Column("fom_acentric", Double, nullable=True, comment="The value of _pdbx_phasing_dm.fom_acentric identifies the figure of merit for acentric data"),
    Column("fom_centric", Double, nullable=True, comment="The value of _pdbx_phasing_dm.fom_centric identifies the figure of merit for acentric data"),
    Column("fom", Double, nullable=True, comment="The value of _pdbx_phasing_dm.fom identifies the figure of merit for all the data"),
    Column("reflns_acentric", Integer, nullable=True, comment="The value of _pdbx_phasing_dm.reflns_acentric identifies the number of acentric reflections."),
    Column("reflns_centric", Integer, nullable=True, comment="The value of _pdbx_phasing_dm.reflns_centric identifies the number of centric reflections."),
    Column("reflns", Integer, nullable=True, comment="The value of _pdbx_phasing_dm.reflns identifies the number of centric and acentric reflections."),
    Column("delta_phi_initial", Double, nullable=True, comment="The value of _pdbx_phasing_dm.delta_phi_initial identifies phase difference before density modification"),
    Column("delta_phi_final", Double, nullable=True, comment="The value of _pdbx_phasing_dm.delta_phi_final identifies phase difference after density modification"),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method", "mask_type"]},
)

pdbx_phasing_dm_shell = Table(
    "pdbx_phasing_dm_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("d_res_high", Double, nullable=True, comment="The value of _pdbx_phasing_dm_shell.d_res_high identifies high resolution"),
    Column("d_res_low", Double, nullable=True, comment="The value of _pdbx_phasing_dm_shell.d_res_low identifies low resolution"),
    Column("fom_acentric", Double, nullable=True, comment="The value of _pdbx_phasing_dm_shell.fom_acentric identifies the figure of merit for acentric data with resolution shells"),
    Column("fom_centric", Double, nullable=True, comment="The value of _pdbx_phasing_dm_shell.fom_centric identifies the figure of merit for centric data with resolution shells."),
    Column("fom", Double, nullable=True, comment="The value of _pdbx_phasing_dm_shell.fom identifies the figure of merit for all the data with resolution shells."),
    Column("reflns_acentric", Integer, nullable=True, comment="The value of _pdbx_phasing_dm_shell.reflns_acentric identifies the number of acentric reflections with resolution shells."),
    Column("reflns_centric", Integer, nullable=True, comment="The value of _pdbx_phasing_dm_shell.reflns_centric identifies the number of centric reflections with resolution shells."),
    Column("reflns", Integer, nullable=True, comment="The value of _pdbx_phasing_dm_shell.reflns identifies the number of centric and acentric reflections with resolution shells."),
    Column("delta_phi_final", Double, nullable=True, comment="The value of _pdbx_phasing_dm_shell.delta_phi_final identifies phase difference after density modification with resolution shells."),
    PrimaryKeyConstraint("pdbid", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_shell = Table(
    "pdbx_phasing_MAD_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("d_res_low", Double, nullable=True, comment="_pdbx_phasing_MAD_shell.d_res_low records the lower resolution for the shell."),
    Column("d_res_high", Double, nullable=True, comment="_pdbx_phasing_MAD_shell.d_res_high records the higher resolution for the shell."),
    Column("reflns_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_shell.reflns_acentric records the number of acentric reflections for MAD phasing."),
    Column("reflns_centric", Integer, nullable=True, comment="_pdbx_phasing_MAD_shell.reflns_centric records the number of centric reflections for MAD phasing."),
    Column("reflns", Integer, nullable=True, comment="_pdbx_phasing_MAD_shell.reflns records the number of reflections used for MAD phasing."),
    Column("fom_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_shell.fom_acentric records the figure of merit using acentric data for MAD phasing."),
    Column("fom_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_shell.fom_centric records the figure of merit using centric data for MAD phasing."),
    Column("fom", Double, nullable=True, comment="_pdbx_phasing_MAD_shell.fom records the figure of merit for MAD phasing."),
    PrimaryKeyConstraint("pdbid", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_set = Table(
    "pdbx_phasing_MAD_set",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="_pdbx_phasing_MAD_set.id records phase set name for MAD phasing."),
    Column("d_res_low", Double, nullable=True, comment="_pdbx_phasing_MAD_set.d_res_low records the lowerest resolution for phasing set."),
    Column("d_res_high", Double, nullable=True, comment="_pdbx_phasing_MAD_set.d_res_high records the highest resolution for the phasing set."),
    Column("reflns_acentric", Integer, nullable=True, comment="_pdbx_phasing_MAD_set.reflns_acentric records the number of acentric reflections for MAD phasing."),
    Column("reflns_centric", Integer, nullable=True, comment="_pdbx_phasing_MAD_set.reflns_centric records the number of centric reflections for MAD phasing."),
    Column("reflns", Integer, nullable=True, comment="_pdbx_phasing_MAD_set.reflns records the number of reflections used for MAD phasing."),
    Column("fom_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.fom_acentric records the figure of merit using acentric data for MAD phasing."),
    Column("fom_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.fom_centric records the figure of merit using centric data for MAD phasing."),
    Column("fom", Double, nullable=True, comment="_pdbx_phasing_MAD_set.fom records the figure of merit for MAD phasing."),
    Column("R_cullis_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.R_cullis_centric records R_cullis using centric data for MAD phasing."),
    Column("R_cullis_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.R_cullis_acentric records R_cullis using acentric data for MAD phasing."),
    Column("R_cullis", Double, nullable=True, comment="_pdbx_phasing_MAD_set.R_cullis records R_cullis for MAD phasing."),
    Column("R_kraut_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.R_kraut_centric records r_kraut using centric data for MAD phasing."),
    Column("R_kraut_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.r_kraut_acentric records r_kraut using acentric data for MAD phasing."),
    Column("R_kraut", Double, nullable=True, comment="_pdbx_phasing_MAD_set.R_kraut records R_kraut for MAD phasing."),
    Column("loc_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.loc_centric records lack of closure using centric data for MAD phasing."),
    Column("loc_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.loc_acentric records lack of closure using acentric data for MAD phasing."),
    Column("loc", Double, nullable=True, comment="_pdbx_phasing_MAD_set.loc records lack of closure for MAD phasing."),
    Column("power_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.power_centric records phasing powe using centric data for MAD phasing."),
    Column("power_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set.power_acentric records phasing powe using acentric data for MAD phasing."),
    Column("power", Double, nullable=True, comment="_pdbx_phasing_MAD_set.power records phasing power for MAD phasing."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_set_shell = Table(
    "pdbx_phasing_MAD_set_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="_pdbx_phasing_MAD_set_shell.id records phase set name for MAD phasing."),
    Column("d_res_low", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.d_res_low records the lowerest resolution for phasing set."),
    Column("d_res_high", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.d_res_high records the highest resolution for the phasing set."),
    Column("reflns_acentric", Integer, nullable=True, comment="_pdbx_phasing_MAD_set_shell.reflns_acentric records the number of acentric reflections for MAD phasing."),
    Column("reflns_centric", Integer, nullable=True, comment="_pdbx_phasing_MAD_set_shell.reflns_centric records the number of centric reflections for MAD phasing."),
    Column("reflns", Integer, nullable=True, comment="_pdbx_phasing_MAD_set_shell.reflns records the number of reflections used for MAD phasing."),
    Column("fom_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.fom_acentric records the figure of merit using acentric data for MAD phasing."),
    Column("fom_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.fom_centric records the figure of merit using centric data for MAD phasing."),
    Column("fom", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.fom records the figure of merit for MAD phasing."),
    Column("R_cullis_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.R_cullis_centric records R_cullis using centric data for MAD phasing."),
    Column("R_cullis_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.R_cullis_acentric records R_cullis using acentric data for MAD phasing."),
    Column("R_cullis", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.R_cullis records R_cullis for MAD phasing."),
    Column("R_kraut_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.R_kraut_centric records R_kraut using centric data for MAD phasing."),
    Column("R_kraut_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.R_kraut_acentric records R_kraut using acentric data for MAD phasing."),
    Column("R_kraut", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.R_kraut records R_kraut for MAD phasing."),
    Column("loc_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.loc_centric records lack of closure using centric data for MAD phasing."),
    Column("loc_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.loc_acentric records lack of closure using acentric data for MAD phasing."),
    Column("loc", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.loc records lack of closure for MAD phasing."),
    Column("power_centric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.power_centric records phasing power using centric data for MAD phasing."),
    Column("power_acentric", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.power_acentric records phasing power using acentric data for MAD phasing."),
    Column("power", Double, nullable=True, comment="_pdbx_phasing_MAD_set_shell.power records phasing power for MAD phasing."),
    PrimaryKeyConstraint("pdbid", "id", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_set_site = Table(
    "pdbx_phasing_MAD_set_site",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="_pdbx_phasing_MAD_set_site.id records the number of site obtained from MAD phasing."),
    Column("atom_type_symbol", Text, nullable=True, comment="_pdbx_phasing_MAD_set_site.atom_type_symbol records the name of site obtained from MAD phasing."),
    Column("Cartn_x", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.Cartn_x records the X Cartesian coordinate of site obtained from MAD phasing."),
    Column("Cartn_y", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.Cartn_y records the Y Cartesian coordinate of site obtained from MAD phasing."),
    Column("Cartn_z", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.Cartn_z records the Z Cartesian coordinate of site obtained from MAD phasing."),
    Column("fract_x", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.fract_x records the X fractional coordinate of site obtained from MAD phasing."),
    Column("fract_y", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.fract_y records the Y fractional coordinate of site obtained from MAD phasing."),
    Column("fract_z", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.fract_z records the Z fractional coordinate of site obtained from MAD phasing."),
    Column("b_iso", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.b_iso records isotropic temperature factor parameterthe for the site obtained from MAD phasing."),
    Column("occupancy", Double, nullable=True, comment="_pdbx_phasing_MAD_set_site.occupancy records the fraction of the atom type presented at this site."),
    Column("occupancy_iso", Double, nullable=True, comment="The relative real isotropic occupancy of the atom type present at this heavy-atom site in a given atom site."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MR = Table(
    "pdbx_phasing_MR",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="The value of _pdbx_phasing_MR.entry_id identifies the data block."),
    Column("method_rotation", Text, nullable=True, comment="The value of _pdbx_phasing_MR.method_rotation identifies the method used for rotation search. For example, the rotation method may be realspace, fastdirect, or direct. ."),
    Column("d_res_high_rotation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.d_res_high_rotation identifies the highest resolution used for rotation search."),
    Column("d_res_low_rotation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.d_res_low_rotation identifies the lowest resolution used for rotation search."),
    Column("sigma_F_rotation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.sigma_F_rotation identifies the sigma cut off of structure factor used for rotation search."),
    Column("reflns_percent_rotation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.reflns_percent_rotation identifies the completness of data used for rotation search."),
    Column("method_translation", Text, nullable=True, comment="The value of _pdbx_phasing_MR.method_translation identifies the method used for translation search. For example in CNS, the translation method may be \"general\" or \"phased\" with PC refinement target using \"fastf2f2\" \"e2e2\" \"e1e1\" \"f2f2\" \"f1f1\" \"residual\" \"vector\". ."),
    Column("d_res_high_translation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.d_res_high_translation identifies the highest resolution used for translation search."),
    Column("d_res_low_translation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.d_res_low_translation identifies the lowest resolution used for translation search."),
    Column("sigma_F_translation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.sigma_F_translation identifies the sigma cut off of structure factor used for translation search."),
    Column("reflns_percent_translation", Double, nullable=True, comment="The value of _pdbx_phasing_MR.reflns_percent_translation identifies the completness of data used for translation search."),
    Column("correlation_coeff_Io_to_Ic", Double, nullable=True, comment="The value of _pdbx_phasing_MR.correlation_coeff_Io_to_Ic identifies the correlation between the observed and the calculated intensity (~|F|^2) after rotation and translation."),
    Column("correlation_coeff_Fo_to_Fc", Double, nullable=True, comment="The value of _pdbx_phasing_MR.correlation_coeff_Fo_to_Fc identifies the correlation between the observed and the calculated structure factor after rotation and translation."),
    Column("R_factor", Double, nullable=True, comment="The value of _pdbx_phasing_MR.R_factor identifies the R factor (defined as uasual) after rotation and translation."),
    Column("R_rigid_body", Double, nullable=True, comment="The value of _pdbx_phasing_MR.R_rigid_body identifies the R factor for rigid body refinement after rotation and translation.(In general, rigid body refinement has to be carried out after molecular replacement."),
    Column("packing", Double, nullable=True, comment="The value of _pdbx_phasing_MR.packing identifies the packing of search model in the unit cell. Too many crystallographic contacts may indicate a bad search."),
    Column("model_details", Text, nullable=True, comment="The value of _pdbx_phasing_MR.model_details records the details of model used. For example, the original model can be truncated by deleting side chains, doubtful parts, using the monomer if the original model was an oligomer. The search model may be one domain of a large molecule. What is the pdb IDs."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "method_rotation",
            "method_translation",
            "model_details",
            "native_set_id",
        ]
    },
)

pdbx_buffer = Table(
    "pdbx_buffer",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_buffer.id must uniquely identify the sample buffer."),
    Column("name", Text, nullable=True, comment="The name of each buffer."),
    Column("details", Text, nullable=True, comment="Any additional details to do with buffer."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

pdbx_buffer_components = Table(
    "pdbx_buffer_components",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_buffer_components.id must uniquely identify a component of the buffer."),
    Column("buffer_id", Text, nullable=True, comment="This data item is a pointer to _pdbx_buffer.id in the BUFFER category."),
    Column("name", Text, nullable=True, comment="The name of each buffer component."),
    Column("conc", Text, nullable=True, comment="The millimolar concentration of buffer component."),
    Column("details", Text, nullable=True, comment="Any additional details to do with buffer composition."),
    Column("conc_units", Text, nullable=True, comment="The concentration units of the component."),
    PrimaryKeyConstraint("pdbid", "buffer_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, buffer_id) -> pdbx_buffer(pdbid, id)
    info={"keywords": ["name", "details", "isotopic_labeling"]},
)

pdbx_reflns_twin = Table(
    "pdbx_reflns_twin",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="The diffraction data set identifier. A reference to _diffrn.id in category DIFFRN."),
    Column("crystal_id", Text, nullable=True, comment="The crystal identifier. A reference to _exptl_crystal.id in category EXPTL_CRYSTAL."),
    Column("domain_id", Text, nullable=True, comment="An identifier for the twin domain."),
    Column("type", Text, nullable=True, comment="There are two types of twinning: merohedral or hemihedral non-merohedral or epitaxial For merohedral twinning the diffraction patterns from the different domains are completely superimposable. Hemihedral twinning is a special case of merohedral twinning. It only involves two distinct domains. Pseudo-merohedral twinning is a subclass merohedral twinning in which lattice is coincidentally superimposable. In the case of non-merohedral or epitaxial twinning the reciprocal lattices do not superimpose exactly. In this case the diffraction pattern consists of two (or more) interpenetrating lattices, which can in principle be separated."),
    Column("operator", Text, nullable=True, comment="The possible merohedral or hemihedral twinning operators for different point groups are: True point group Twin operation hkl related to 3 2 along a,b h,-h-k,-l 2 along a*,b* h+k,-k,-l 2 along c -h,-k,l 4 2 along a,b,a*,b* h,-k,-l 6 2 along a,b,a*,b* h,-h-k,-l 321 2 along a*,b*,c -h,-k,l 312 2 along a,b,c -h,-k,l 23 4 along a,b,c k,-h,l References: Yeates, T.O. (1997) Methods in Enzymology 276, 344-358. Detecting and Overcoming Crystal Twinning. and information from the following on-line sites: CNS site http://cns.csb.yale.edu/v1.1/ CCP4 site http://www.ccp4.ac.uk/dist/html/detwin.html SHELX site http://shelx.uni-ac.gwdg.de/~rherbst/twin.html"),
    Column("fraction", Double, nullable=True, comment="The twin fraction or twin factor represents a quantitative parameter for the crystal twinning. The value 0 represents no twinning, < 0.5 partial twinning, = 0.5 for perfect twinning."),
    PrimaryKeyConstraint("pdbid", "crystal_id", "diffrn_id", "operator"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["operator"]},
)

pdbx_struct_assembly_prop = Table(
    "pdbx_struct_assembly_prop",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("biol_id", Text, nullable=True, comment="The identifier for the assembly used in category PDBX_STRUCT_ASSEMBLY."),
    Column("type", Text, nullable=True, comment="The property type for the assembly."),
    Column("value", Text, nullable=True, comment="The value of the assembly property."),
    PrimaryKeyConstraint("pdbid", "type", "biol_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["value", "details"]},
)

pdbx_struct_chem_comp_diagnostics = Table(
    "pdbx_struct_chem_comp_diagnostics",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("type", Text, nullable=True, comment="A classification of the diagnostic for the chemical component instance"),
    Column("pdb_strand_id", Text, nullable=True, comment="PDB strand/chain id."),
    Column("asym_id", Text, nullable=True, comment="Instance identifier for the polymer molecule."),
    Column("auth_seq_id", Text, nullable=True, comment="PDB position in the sequence."),
    Column("seq_num", Integer, nullable=True, comment="Position in the sequence."),
    Column("auth_comp_id", Text, nullable=True, comment="PDB component ID"),
    Column("ordinal", Integer, nullable=True, comment="An ordinal index for this category"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_coordinate_model = Table(
    "pdbx_coordinate_model",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("asym_id", Text, nullable=True, comment="A reference to _struct_asym.id."),
    Column("type", Text, nullable=True, comment="A classification of the composition of the coordinate model."),
    PrimaryKeyConstraint("pdbid", "asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
)

pdbx_diffrn_reflns_shell = Table(
    "pdbx_diffrn_reflns_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="This data item is a pointer to _diffrn.id in the DIFFRN category. This item distingush the different data sets"),
    Column("d_res_low", Double, nullable=True, comment="The lowest resolution for the interplanar spacings in the resolution shell."),
    Column("d_res_high", Double, nullable=True, comment="The highest resolution for the interplanar spacings in the resolution shell."),
    Column("percent_possible_obs", Double, nullable=True, comment="The percentage of geometrically possible reflections represented by reflections that satisfy the resolution limits established by _diffrn_reflns_shell.d_resolution_high and _diffrn_reflns_shell.d_resolution_low and the observation limit established by _diffrn_reflns.observed_criterion."),
    Column("Rmerge_I_obs", Double, nullable=True, comment="The R factor for the reflections that satisfy the merging criteria for the resolution shell."),
    Column("Rsym_value", Double, nullable=True, comment="The R factor for averaging the symmetry related reflections for the resolution shell."),
    Column("chi_squared", Double, nullable=True, comment="The overall Chi-squared statistic for the resolution shell."),
    Column("redundancy", Double, nullable=True, comment="The overall redundancy for the resolution shell."),
    Column("rejects", Integer, nullable=True, comment="The number of rejected reflections in the resolution shell"),
    Column("number_obs", Integer, nullable=True, comment="The number of observed reflections in the resolution shell."),
    PrimaryKeyConstraint("pdbid", "d_res_high", "d_res_low", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
)

pdbx_soln_scatter = Table(
    "pdbx_soln_scatter",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_soln_scatter.id must uniquely identify the sample in the category PDBX_SOLN_SCATTER"),
    Column("type", Text, nullable=True, comment="The type of solution scattering experiment carried out"),
    Column("source_beamline", Text, nullable=True, comment="The beamline name used for the experiment"),
    Column("source_beamline_instrument", Text, nullable=True, comment="The instrumentation used on the beamline"),
    Column("detector_type", Text, nullable=True, comment="The general class of the radiation detector."),
    Column("detector_specific", Text, nullable=True, comment="The particular radiation detector. In general this will be a manufacturer, description, model number or some combination of these."),
    Column("source_type", Text, nullable=True, comment="The make, model, name or beamline of the source of radiation."),
    Column("source_class", Text, nullable=True, comment="The general class of the radiation source."),
    Column("num_time_frames", Integer, nullable=True, comment="The number of time frame solution scattering images used."),
    Column("sample_pH", Double, nullable=True, comment="The pH value of the buffered sample."),
    Column("temperature", Double, nullable=True, comment="The temperature in kelvins at which the experiment was conducted"),
    Column("concentration_range", Text, nullable=True, comment="The concentration range (mg/mL) of the complex in the sample used in the solution scattering experiment to determine the mean radius of structural elongation."),
    Column("buffer_name", Text, nullable=True, comment="The name of the buffer used for the sample in the solution scattering experiment."),
    Column("mean_guiner_radius", Double, nullable=True, comment="The mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q gives the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of \"Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2"),
    Column("mean_guiner_radius_esd", Double, nullable=True, comment="The estimated standard deviation for the mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of \"Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2"),
    Column("min_mean_cross_sectional_radii_gyration", Double, nullable=True, comment="The minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of \"Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2"),
    Column("min_mean_cross_sectional_radii_gyration_esd", Double, nullable=True, comment="The estimated standard deviation for the minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of \"Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2"),
    Column("max_mean_cross_sectional_radii_gyration", Double, nullable=True, comment="The maximum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of \"Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2"),
    Column("max_mean_cross_sectional_radii_gyration_esd", Double, nullable=True, comment="The estimated standard deviation for the minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyration R_G is a measure of structural elongation if the internal inhomogeneity of scattering densities has no effect. Guiner analysis at low Q give the R_G and the forward scattering at zero angle I(0). lnl(Q) = lnl(0) - R_G^2Q^2/3 where Q = 4(pi)sin(theta/lamda) 2theta = scattering angle lamda = wavelength The above expression is valid in a QR_G range for extended rod-like particles. The relative I(0)/c values ( where c = sample concentration) for sample measurements in a constant buffer for a single sample data session, gives the relative masses of the protein(s) studied when referenced against a standard. see: O.Glatter & O.Kratky, (1982). Editors of \"Small angle X-ray Scattering, Academic Press, New York. O.Kratky. (1963). X-ray small angle scattering with substances of biological interest in diluted solutions. Prog. Biophys. Chem., 13, 105-173. G.D.Wignall & F.S.Bates, (1987). The small-angle approximation of X-ray and neutron scatter from rigid rods of non-uniform cross section and finite length. J.Appl. Crystallog., 18, 452-460. If the structure is elongated, the mean radius of gyration of the cross-sectional structure R_XS and the mean cross sectional intensity at zero angle [I(Q).Q]_Q->0 is obtained from ln[I(Q).Q] = ln[l(Q).(Q)]_Q->0 - ((R_XS)^2Q^2)/2"),
    Column("protein_length", Text, nullable=True, comment="The length (or range) of the protein sample under study. If the solution structure is approximated as an elongated elliptical cyclinder the length L is determined from, L = sqrt [12( (R_G)^2 - (R_XS)^2 ) ] The length should also be given by L = pi I(0) / [ I(Q).Q]_Q->0"),
    Column("data_reduction_software_list", Text, nullable=True, comment="A list of the software used in the data reduction"),
    Column("data_analysis_software_list", Text, nullable=True, comment="A list of the software used in the data analysis"),
    PrimaryKeyConstraint("pdbid", "entry_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "source_beamline",
            "source_beamline_instrument",
            "detector_type",
            "detector_specific",
            "source_type",
            "source_class",
            "concentration_range",
            "buffer_name",
            "protein_length",
            "data_reduction_software_list",
            "data_analysis_software_list",
        ]
    },
)

pdbx_soln_scatter_model = Table(
    "pdbx_soln_scatter_model",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("scatter_id", Text, nullable=True, comment="This data item is a pointer to _pdbx_soln_scatter.id in the PDBX_SOLN_SCATTER category."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_soln_scatter_model.id must uniquely identify the sample in the category PDBX_SOLN_SCATTER_MODEL"),
    Column("details", Text, nullable=True, comment="A description of any additional details concerning the experiment."),
    Column("method", Text, nullable=True, comment="A description of the methods used in the modelling"),
    Column("software_list", Text, nullable=True, comment="A list of the software used in the modeeling"),
    Column("software_author_list", Text, nullable=True, comment="A list of the software authors"),
    Column("entry_fitting_list", Text, nullable=True, comment="A list of the entries used to fit the model to the scattering data"),
    Column("num_conformers_calculated", Integer, nullable=True, comment="The number of model conformers calculated."),
    Column("num_conformers_submitted", Integer, nullable=True, comment="The number of model conformers submitted in the entry"),
    Column("representative_conformer", Integer, nullable=True, comment="The index of the representative conformer among the submitted conformers for the entry"),
    Column("conformer_selection_criteria", Text, nullable=True, comment="A description of the conformer selection criteria used."),
    PrimaryKeyConstraint("pdbid", "id", "scatter_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "details",
            "method",
            "software_list",
            "software_author_list",
            "entry_fitting_list",
            "conformer_selection_criteria",
        ]
    },
)

pdbx_chem_comp_identifier = Table(
    "pdbx_chem_comp_identifier",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("comp_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("identifier", Text, nullable=True, comment="This data item contains the identifier value for this component."),
    Column("type", Text, nullable=True, comment="This data item contains the identifier type."),
    Column("program", Text, nullable=True, comment="This data item contains the name of the program or library used to compute the identifier."),
    Column("program_version", Text, nullable=True, comment="This data item contains the version of the program or library used to compute the identifier."),
    PrimaryKeyConstraint("pdbid", "comp_id", "type", "program", "program_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
    info={"keywords": ["identifier", "program", "program_version"]},
)

pdbx_validate_close_contact = Table(
    "pdbx_validate_close_contact",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_close_contact.id must uniquely identify each item in the PDBX_VALIDATE_CLOSE_CONTACT list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given contact"),
    Column("auth_asym_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_atom_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_asym_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code_1", Text, nullable=True, comment="Optional identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("PDB_ins_code_2", Text, nullable=True, comment="Optional identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id_1", Text, nullable=True, comment="An optional identifier of the first of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("label_alt_id_2", Text, nullable=True, comment="An optional identifier of the second of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("dist", Double, nullable=True, comment="The value of the close contact for the two atoms defined."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["symm_as_xyz_1", "symm_as_xyz_2"]},
)

pdbx_validate_symm_contact = Table(
    "pdbx_validate_symm_contact",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_symm_contact.id must uniquely identify each item in the PDBX_VALIDATE_SYMM_CONTACT list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given angle"),
    Column("auth_asym_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_atom_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_asym_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the close contact. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code_1", Text, nullable=True, comment="Optional identifier of the first of the two atom sites that define the close contact."),
    Column("PDB_ins_code_2", Text, nullable=True, comment="Optional identifier of the second of the two atom sites that define the close contact."),
    Column("label_alt_id_1", Text, nullable=True, comment="An optional identifier of the first of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category."),
    Column("label_alt_id_2", Text, nullable=True, comment="An optional identifier of the second of the two atoms that define the close contact. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("site_symmetry_1", Text, nullable=True, comment="The symmetry of the first of the two atoms define the close contact. Symmetry defined in ORTEP style of 555 equal to unit cell with translations +-1 from 555 as 000"),
    Column("site_symmetry_2", Text, nullable=True, comment="The symmetry of the second of the two atoms define the close contact. Symmetry defined in ORTEP style of 555 equal to unit cell with translations +-1 from 555 as 000"),
    Column("dist", Double, nullable=True, comment="The value of the close contact for the two atoms defined."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["site_symmetry_1", "site_symmetry_2"]},
)

pdbx_validate_rmsd_bond = Table(
    "pdbx_validate_rmsd_bond",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_rmsd_bond.id must uniquely identify each item in the PDBX_VALIDATE_RMSD_BOND list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given bond"),
    Column("auth_asym_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_atom_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_asym_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code_1", Text, nullable=True, comment="Optional identifier of the first of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("PDB_ins_code_2", Text, nullable=True, comment="Optional identifier of the second of the two atom sites that define the covalent bond. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id_1", Text, nullable=True, comment="An optional identifier of the first of the two atoms that define the covalent bond. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("label_alt_id_2", Text, nullable=True, comment="An optional identifier of the second of the two atoms that define the covalent bond. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("bond_deviation", Double, nullable=True, comment="The value of the deviation from ideal for the defined covalent bond for the two atoms defined."),
    Column("bond_value", Double, nullable=True, comment="The value of the bond length"),
    Column("bond_target_value", Double, nullable=True, comment="The target value of the bond length"),
    Column("bond_standard_deviation", Double, nullable=True, comment="The uncertaintiy in target value of the bond length expressed as a standard deviation."),
    Column("linker_flag", Text, nullable=True, comment="A flag to indicate if the bond is between two residues"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_rmsd_angle = Table(
    "pdbx_validate_rmsd_angle",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_rmsd_angle.id must uniquely identify each item in the PDBX_VALIDATE_RMSD_ANGLE list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given angle"),
    Column("auth_asym_id_1", Text, nullable=True, comment="Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id_1", Text, nullable=True, comment="Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id_1", Text, nullable=True, comment="Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_1", Text, nullable=True, comment="Part of the identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_atom_id_2", Text, nullable=True, comment="Part of the identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_asym_id_2", Text, nullable=True, comment="identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_2", Text, nullable=True, comment="Part of the identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_2", Text, nullable=True, comment="Part of the identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_atom_id_3", Text, nullable=True, comment="Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_asym_id_3", Text, nullable=True, comment="Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_3", Text, nullable=True, comment="Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_3", Text, nullable=True, comment="Part of the identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code_1", Text, nullable=True, comment="Optional identifier of the first of the three atom sites that define the angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("PDB_ins_code_2", Text, nullable=True, comment="Optional identifier of the second of the three atom sites that define the angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("PDB_ins_code_3", Text, nullable=True, comment="Optional identifier of the third of the three atom sites that define the angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id_1", Text, nullable=True, comment="An optional identifier of the first of the three atoms that define the covalent angle. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category."),
    Column("label_alt_id_2", Text, nullable=True, comment="An optional identifier of the second of the three atoms that define the covalent angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("label_alt_id_3", Text, nullable=True, comment="An optional identifier of the third of the three atoms that define the covalent angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("angle_deviation", Double, nullable=True, comment="Value of the deviation (in degrees) from 6*REBI for the angle bounded by the three sites from the expected dictionary value."),
    Column("angle_value", Double, nullable=True, comment="The value of the bond angle"),
    Column("angle_target_value", Double, nullable=True, comment="The target value of the bond angle"),
    Column("angle_standard_deviation", Double, nullable=True, comment="The uncertainty in the target value of the bond angle expressed as a standard deviation."),
    Column("linker_flag", Text, nullable=True, comment="A flag to indicate if the angle is between two residues"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_torsion = Table(
    "pdbx_validate_torsion",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_torsion.id must uniquely identify each item in the PDBX_VALIDATE_TORSION list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given residue This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Optional identifier of the residue This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="Optional identifier of the residue This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("phi", Double, nullable=True, comment="The Phi value that for the residue that lies outside normal limits (in combination with the Psi value) with regards to the rammachandran plot"),
    Column("psi", Double, nullable=True, comment="The Psi value that for the residue that lies outside normal limits (in combination with the Phi value) with regards to the rammachandran plot"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_peptide_omega = Table(
    "pdbx_validate_peptide_omega",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_peptide_omega.id must uniquely identify each item in the PDBX_VALIDATE_PEPTIDE_OMEGA list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given residue This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id_1", Text, nullable=True, comment="Part of the identifier of the first residue in the bond This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_asym_id_2", Text, nullable=True, comment="Part of the identifier of the second residue in the bond This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_1", Text, nullable=True, comment="Part of the identifier of the first residue in the bond This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_comp_id_2", Text, nullable=True, comment="Part of the identifier of the second residue in the bond This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_1", Text, nullable=True, comment="Part of the identifier of the first residue in the bond This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_seq_id_2", Text, nullable=True, comment="Part of the identifier of the second residue in the bond This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code_1", Text, nullable=True, comment="Optional identifier of the first residue in the bond This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("PDB_ins_code_2", Text, nullable=True, comment="Optional identifier of the second residue in the bond This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id_1", Text, nullable=True, comment="Optional identifier of the first residue in the torsion angle This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("label_alt_id_2", Text, nullable=True, comment="Optional identifier of the second residue in the torsion angle This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("omega", Double, nullable=True, comment="The value of the OMEGA angle for the peptide linkage between the two defined residues"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_chiral = Table(
    "pdbx_validate_chiral",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_chiral.id must uniquely identify each item in the PDBX_VALIDATE_CHIRAL list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given residue This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier of the residue This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Optional identifier of the residue This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("details", Text, nullable=True, comment="A description of the outlier angle e.g. ALPHA-CARBON"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_validate_planes = Table(
    "pdbx_validate_planes",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_planes.id must uniquely identify each item in the PDBX_VALIDATE_PLANES list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given angle This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("rmsd", Double, nullable=True, comment="The value of the overall deviation from ideal plane for the atoms defining the plane."),
    Column("type", Text, nullable=True, comment="The type of plane - MAIN CHAIN or SIDE CHAIN atoms"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_main_chain_plane = Table(
    "pdbx_validate_main_chain_plane",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_main_chain_plane.id must uniquely identify each item in the PDBX_VALIDATE_MAIN_CHAIN_PLANE list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the residue in which the plane is calculated This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="Optional identifier of the residue in which the plane is calculated This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("improper_torsion_angle", Double, nullable=True, comment="The value for the torsion angle C(i-1) - CA(i-1) - N(i) - O(i-1)"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_struct_conn_angle = Table(
    "pdbx_struct_conn_angle",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_struct_conn_angle.id must uniquely identify a record in the PDBX_STRUCT_CONN_ANGLE list. Note that this item need not be a number; it can be any unique identifier."),
    Column("ptnr1_label_alt_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("ptnr1_label_asym_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("ptnr1_label_atom_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category."),
    Column("ptnr1_label_comp_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("ptnr1_label_seq_id", Integer, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("ptnr1_auth_asym_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("ptnr1_auth_comp_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("ptnr1_auth_seq_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("ptnr1_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the atom specified by _pdbx_struct_conn_angle.ptnr1_label* to generate the first partner in the structure angle."),
    Column("ptnr2_label_alt_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category."),
    Column("ptnr2_label_asym_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("ptnr2_label_atom_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category."),
    Column("ptnr2_label_comp_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("ptnr2_label_seq_id", Integer, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("ptnr2_auth_asym_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("ptnr2_auth_comp_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("ptnr2_auth_seq_id", Text, nullable=True, comment="A component of the identifier for partner 2 of the structure angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("ptnr2_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the atom specified by _pdbx_struct_conn_angle.ptnr2_label* to generate the second partner in the structure angle."),
    Column("ptnr1_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("ptnr2_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("ptnr3_auth_asym_id", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("ptnr3_auth_comp_id", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("ptnr3_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("ptnr3_auth_seq_id", Text, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("ptnr3_label_alt_id", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("ptnr3_label_asym_id", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("ptnr3_label_atom_id", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category."),
    Column("ptnr3_label_comp_id", Text, nullable=True, comment="A component of the identifier for partner 3 of the structure angle. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("ptnr3_label_seq_id", Integer, nullable=True, comment="A component of the identifier for partner 1 of the structure angle. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("ptnr3_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the atom specified by _pdbx_struct_conn_angle.ptnr3_label* to generate the first partner in the structure angle."),
    Column("value", Double, nullable=True, comment="Angle in degrees defined by the three sites _pdbx_struct_conn_angle.ptnr1_label_atom_id, _pdbx_struct_conn_angle.ptnr2_label_atom_id _pdbx_struct_conn_angle.ptnr3_label_atom_id"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_unobs_or_zero_occ_residues = Table(
    "pdbx_unobs_or_zero_occ_residues",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_unobs_or_zero_occ_residues.id must uniquely identify each item in the PDBX_UNOBS_OR_ZERO_OCC_RESIDUES list. This is an integer serial number."),
    Column("polymer_flag", Text, nullable=True, comment="The value of polymer flag indicates whether the unobserved or zero occupancy residue is part of a polymer chain or not"),
    Column("occupancy_flag", Integer, nullable=True, comment="The value of occupancy flag indicates whether the residue is unobserved (= 1) or the coordinates have an occupancy of zero (=0)"),
    Column("PDB_model_num", Integer, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_asym_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_comp_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, auth_comp_id) -> chem_comp(pdbid, id)
)

pdbx_unobs_or_zero_occ_atoms = Table(
    "pdbx_unobs_or_zero_occ_atoms",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_unobs_or_zero_occ_atoms.id must uniquely identify each item in the PDBX_UNOBS_OR_ZERO_OCC_ATOMS list. This is an integer serial number."),
    Column("polymer_flag", Text, nullable=True, comment="The value of polymer flag indicates whether the unobserved or zero occupancy atom is part of a polymer chain"),
    Column("occupancy_flag", Integer, nullable=True, comment="The value of occupancy flag indicates whether the atom is either unobserved (=1) or has zero occupancy (=0)"),
    Column("PDB_model_num", Integer, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category."),
    Column("label_atom_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_atom_id in the ATOM_SITE category."),
    Column("label_asym_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_comp_id", Text, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy atom. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, auth_comp_id) -> chem_comp(pdbid, id)
)

pdbx_entry_details = Table(
    "pdbx_entry_details",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This item identifies the entry. This is a reference to _entry.id."),
    Column("nonpolymer_details", Text, nullable=True, comment="Additional details about the non-polymer components in this entry."),
    Column("sequence_details", Text, nullable=True, comment="Additional details about the sequence or sequence database correspondences for this entry."),
    Column("compound_details", Text, nullable=True, comment="Additional details about the macromolecular compounds in this entry."),
    Column("source_details", Text, nullable=True, comment="Additional details about the source and taxonomy of the macromolecular components in this entry."),
    Column("has_ligand_of_interest", Text, nullable=True, comment="A flag to indicate if author has indicated that there are any or no ligands that are the focus of research."),
    Column("has_protein_modification", Text, nullable=True, comment="A flag to indicate if the model contains any protein modifications."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "nonpolymer_details",
            "sequence_details",
            "compound_details",
            "source_details",
        ]
    },
)

pdbx_struct_mod_residue = Table(
    "pdbx_struct_mod_residue",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_struct_mod_residue.id must uniquely identify each item in the PDBX_STRUCT_MOD_RESIDUE list. This is an integer serial number."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_asym_id", Text, nullable=True, comment="Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_comp_id", Text, nullable=True, comment="Part of the identifier for the modified polymer component. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="Part of the identifier for the unobserved or zero occupancy residue. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("parent_comp_id", Text, nullable=True, comment="The parent component identifier for this modified polymer component."),
    Column("details", Text, nullable=True, comment="Details of the modification for this polymer component."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_validate_polymer_linkage = Table(
    "pdbx_validate_polymer_linkage",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_validate_polymer_linkage.id must uniquely identify each item in the PDBX_VALIDATE_POLYMER_LINKAGE list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="The model number for the given linkage"),
    Column("auth_asym_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_1", Text, nullable=True, comment="Part of the identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("auth_atom_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_asym_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id_2", Text, nullable=True, comment="Part of the identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code_1", Text, nullable=True, comment="Optional identifier of the first of the two atom sites that define the linkage. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("PDB_ins_code_2", Text, nullable=True, comment="Optional identifier of the second of the two atom sites that define the linkage. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_alt_id_1", Text, nullable=True, comment="An optional identifier of the first of the two atoms that define the linkage. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("label_alt_id_2", Text, nullable=True, comment="An optional identifier of the second of the two atoms that define the linkage. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("dist", Double, nullable=True, comment="The value of the polymer linkage for the two atoms defined."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_helical_symmetry = Table(
    "pdbx_helical_symmetry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("number_of_operations", Integer, nullable=True, comment="Number of operations."),
    Column("rotation_per_n_subunits", Double, nullable=True, comment="Angular rotation (degrees) in N subunits"),
    Column("rise_per_n_subunits", Double, nullable=True, comment="Angular rotation (degrees) in N subunits"),
    Column("n_subunits_divisor", Integer, nullable=True, comment="Number of subunits used in the calculation of rise and rotation."),
    Column("dyad_axis", Text, nullable=True, comment="Two-fold symmetry perpendicular to the helical axis."),
    Column("circular_symmetry", Integer, nullable=True, comment="Rotational n-fold symmetry about the helical axis."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

pdbx_point_symmetry = Table(
    "pdbx_point_symmetry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("Schoenflies_symbol", Text, nullable=True, comment="The Schoenflies point symmetry symbol."),
    Column("circular_symmetry", Integer, nullable=True, comment="Rotational n-fold C and D point symmetry."),
    Column("H-M_notation", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

pdbx_struct_entity_inst = Table(
    "pdbx_struct_entity_inst",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of this portion of the contents of the deposited unit."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_struct_entity_inst.id must uniquely identify a record in the PDBX_STRUCT_ENTITY_INST list. The entity instance is a method neutral identifier for the observed molecular entities in the deposited coordinate set."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_struct_oper_list = Table(
    "pdbx_struct_oper_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="This identifier code must uniquely identify a record in the PDBX_STRUCT_OPER_LIST list."),
    Column("type", Text, nullable=True, comment="A code to indicate the type of operator."),
    Column("name", Text, nullable=True, comment="A descriptive name for the transformation operation."),
    Column("symmetry_operation", Text, nullable=True, comment="The symmetry operation corresponding to the transformation operation."),
    Column("matrix11", Double, nullable=True),
    Column("matrix12", Double, nullable=True),
    Column("matrix13", Double, nullable=True),
    Column("matrix21", Double, nullable=True),
    Column("matrix22", Double, nullable=True),
    Column("matrix23", Double, nullable=True),
    Column("matrix31", Double, nullable=True),
    Column("matrix32", Double, nullable=True),
    Column("matrix33", Double, nullable=True),
    Column("vector1", Double, nullable=True),
    Column("vector2", Double, nullable=True),
    Column("vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "symmetry_operation"]},
)

pdbx_struct_assembly = Table(
    "pdbx_struct_assembly",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("method_details", Text, nullable=True, comment="Provides details of the method used to determine or compute the assembly."),
    Column("oligomeric_details", Text, nullable=True, comment="Provides the details of the oligomeric state of the assembly."),
    Column("oligomeric_count", Integer, nullable=True, comment="The number of polymer molecules in the assembly."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the macromolecular assembly. In the PDB, 'representative helical assembly', 'complete point assembly', 'complete icosahedral assembly', 'software_defined_assembly', 'author_defined_assembly', and 'author_and_software_defined_assembly' are considered \"biologically relevant assemblies."),
    Column("id", Text, nullable=True, comment="The value of _pdbx_struct_assembly.id must uniquely identify a record in the PDBX_STRUCT_ASSEMBLY list."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method_details", "oligomeric_details", "details", "id"]},
)

pdbx_struct_assembly_gen = Table(
    "pdbx_struct_assembly_gen",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("asym_id_list", Text, nullable=True),
    Column("_hash_asym_id_list", Text, nullable=True),
    Column("assembly_id", Text, nullable=True),
    Column("oper_expression", Text, nullable=True),
    Column("_hash_oper_expression", Text, nullable=True),
    PrimaryKeyConstraint(
        "pdbid", "assembly_id", "_hash_asym_id_list", "_hash_oper_expression"
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, assembly_id) -> pdbx_struct_assembly(pdbid, id)
    info={"keywords": ["asym_id_list", "auth_asym_id_list", "assembly_id"]},
)

pdbx_struct_msym_gen = Table(
    "pdbx_struct_msym_gen",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_inst_id", Text, nullable=True, comment="This data item is a pointer to _pdbx_struct_entity_inst.id in the PDBX_STRUCT_ENTITY_INST category."),
    Column("msym_id", Text, nullable=True, comment="Uniquely identifies the this structure instance in point symmetry unit."),
    Column("oper_expression", Text, nullable=True, comment="Identifies the operation from category PDBX_STRUCT_OPER_LIST."),
    PrimaryKeyConstraint("pdbid", "msym_id", "entity_inst_id", "oper_expression"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_inst_id) -> pdbx_struct_entity_inst(pdbid, id)
)

pdbx_struct_legacy_oper_list = Table(
    "pdbx_struct_legacy_oper_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="This integer value must uniquely identify a record in the PDBX_STRUCT_LEGACY_OPER_LIST list."),
    Column("name", Text, nullable=True, comment="A descriptive name for the transformation operation."),
    Column("matrix11", Double, nullable=True),
    Column("matrix12", Double, nullable=True),
    Column("matrix13", Double, nullable=True),
    Column("matrix21", Double, nullable=True),
    Column("matrix22", Double, nullable=True),
    Column("matrix23", Double, nullable=True),
    Column("matrix31", Double, nullable=True),
    Column("matrix32", Double, nullable=True),
    Column("matrix33", Double, nullable=True),
    Column("vector1", Double, nullable=True),
    Column("vector2", Double, nullable=True),
    Column("vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name"]},
)

pdbx_molecule = Table(
    "pdbx_molecule",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("prd_id", Text, nullable=True, comment="The value of _pdbx_molecule.prd_id is the PDB accession code for this reference molecule."),
    Column("instance_id", Integer, nullable=True, comment="The value of _pdbx_molecule.instance_id is identifies a particular molecule in the molecule list."),
    Column("asym_id", Text, nullable=True, comment="A reference to _struct_asym.id in the STRUCT_ASYM category."),
    PrimaryKeyConstraint("pdbid", "prd_id", "instance_id", "asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
)

pdbx_molecule_features = Table(
    "pdbx_molecule_features",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("prd_id", Text, nullable=True, comment="The value of _pdbx_molecule_features.prd_id is the accession code for this reference molecule."),
    Column("class", Text, nullable=True, comment="Broadly defines the function of the molecule."),
    Column("type", Text, nullable=True, comment="Defines the structural classification of the molecule."),
    Column("name", Text, nullable=True, comment="A name of the molecule."),
    Column("details", Text, nullable=True, comment="Additional details describing the molecule."),
    PrimaryKeyConstraint("pdbid", "prd_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

pdbx_distant_solvent_atoms = Table(
    "pdbx_distant_solvent_atoms",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_distant_solvent_atoms.id must uniquely identify each item in the PDBX_DISTANT_SOLVENT_ATOMS list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_atom_id", Text, nullable=True, comment="Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_atom_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="Part of the identifier for the distant solvent atom. This data item is a pointer to _atom_site.label_alt.id in the ATOM_SITE category."),
    Column("neighbor_macromolecule_distance", Double, nullable=True, comment="Distance to closest neighboring macromolecule atom."),
    Column("neighbor_ligand_distance", Double, nullable=True, comment="Distance to closest neighboring ligand or solvent atom."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, auth_comp_id) -> chem_comp(pdbid, id)
)

pdbx_struct_special_symmetry = Table(
    "pdbx_struct_special_symmetry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="The value of _pdbx_struct_special_symmetry.id must uniquely identify each item in the PDBX_STRUCT_SPECIAL_SYMMETRY list. This is an integer serial number."),
    Column("PDB_model_num", Integer, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.pdbx_PDB_model_num in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("label_asym_id", Text, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_comp_id", Text, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="Part of the identifier for the molecular component. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

entity_src_nat = Table(
    "entity_src_nat",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("common_name", Text, nullable=True, comment="The common name of the organism from which the entity was isolated."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the organism from which the entity was isolated."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("genus", Text, nullable=True, comment="The genus of the organism from which the entity was isolated."),
    Column("species", Text, nullable=True, comment="The species of the organism from which the entity was isolated."),
    Column("strain", Text, nullable=True, comment="The strain of the organism from which the entity was isolated."),
    Column("tissue", Text, nullable=True, comment="The tissue of the organism from which the entity was isolated."),
    Column("tissue_fraction", Text, nullable=True, comment="The subcellular fraction of the tissue of the organism from which the entity was isolated."),
    Column("pdbx_organism_scientific", Text, nullable=True, comment="Scientific name of the organism of the natural source."),
    Column("pdbx_secretion", Text, nullable=True, comment="Identifies the secretion from which the molecule was isolated."),
    Column("pdbx_fragment", Text, nullable=True, comment="A domain or fragment of the molecule."),
    Column("pdbx_variant", Text, nullable=True, comment="Identifies the variant."),
    Column("pdbx_cell_line", Text, nullable=True, comment="The specific line of cells."),
    Column("pdbx_atcc", Text, nullable=True, comment="Americal Tissue Culture Collection number."),
    Column("pdbx_cellular_location", Text, nullable=True, comment="Identifies the location inside (or outside) the cell."),
    Column("pdbx_organ", Text, nullable=True, comment="Organized group of tissues that carries on a specialized function."),
    Column("pdbx_organelle", Text, nullable=True, comment="Organized structure within cell."),
    Column("pdbx_cell", Text, nullable=True, comment="A particular cell type."),
    Column("pdbx_plasmid_name", Text, nullable=True, comment="The plasmid containing the gene."),
    Column("pdbx_plasmid_details", Text, nullable=True, comment="Details about the plasmid."),
    Column("pdbx_ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier for the source organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("pdbx_src_id", Integer, nullable=True, comment="This data item is an ordinal identifier for entity_src_nat data records."),
    Column("pdbx_alt_source_flag", Text, nullable=True, comment="This data item identifies cases in which an alternative source modeled."),
    Column("pdbx_beg_seq_num", Integer, nullable=True, comment="The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    Column("pdbx_end_seq_num", Integer, nullable=True, comment="The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    PrimaryKeyConstraint("pdbid", "entity_id", "pdbx_src_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={
        "keywords": [
            "common_name",
            "details",
            "genus",
            "species",
            "strain",
            "tissue",
            "tissue_fraction",
            "pdbx_organism_scientific",
            "pdbx_secretion",
            "pdbx_fragment",
            "pdbx_variant",
            "pdbx_cell_line",
            "pdbx_atcc",
            "pdbx_cellular_location",
            "pdbx_organ",
            "pdbx_organelle",
            "pdbx_cell",
            "pdbx_plasmid_name",
            "pdbx_plasmid_details",
            "pdbx_ncbi_taxonomy_id",
            "pdbx_culture_collection",
        ]
    },
)

entity_src_gen = Table(
    "entity_src_gen",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("gene_src_common_name", Text, nullable=True, comment="The common name of the natural organism from which the gene was obtained."),
    Column("gene_src_details", Text, nullable=True, comment="A description of special aspects of the natural organism from which the gene was obtained."),
    Column("gene_src_genus", Text, nullable=True, comment="The genus of the natural organism from which the gene was obtained."),
    Column("gene_src_species", Text, nullable=True, comment="The species of the natural organism from which the gene was obtained."),
    Column("gene_src_strain", Text, nullable=True, comment="The strain of the natural organism from which the gene was obtained, if relevant."),
    Column("gene_src_tissue", Text, nullable=True, comment="The tissue of the natural organism from which the gene was obtained."),
    Column("gene_src_tissue_fraction", Text, nullable=True, comment="The subcellular fraction of the tissue of the natural organism from which the gene was obtained."),
    Column("host_org_genus", Text, nullable=True, comment="The genus of the organism that served as host for the production of the entity."),
    Column("host_org_species", Text, nullable=True, comment="The species of the organism that served as host for the production of the entity."),
    Column("pdbx_gene_src_fragment", Text, nullable=True, comment="A domain or fragment of the molecule."),
    Column("pdbx_gene_src_gene", Text, nullable=True, comment="Identifies the gene."),
    Column("pdbx_gene_src_scientific_name", Text, nullable=True, comment="Scientific name of the organism."),
    Column("pdbx_gene_src_variant", Text, nullable=True, comment="Identifies the variant."),
    Column("pdbx_gene_src_cell_line", Text, nullable=True, comment="The specific line of cells."),
    Column("pdbx_gene_src_atcc", Text, nullable=True, comment="American Type Culture Collection tissue culture number."),
    Column("pdbx_gene_src_organ", Text, nullable=True, comment="Organized group of tissues that carries on a specialized function."),
    Column("pdbx_gene_src_organelle", Text, nullable=True, comment="Organized structure within cell."),
    Column("pdbx_gene_src_cell", Text, nullable=True, comment="Cell type."),
    Column("pdbx_gene_src_cellular_location", Text, nullable=True, comment="Identifies the location inside (or outside) the cell."),
    Column("pdbx_host_org_gene", Text, nullable=True, comment="Specific gene which expressed the molecule."),
    Column("pdbx_host_org_organ", Text, nullable=True, comment="Specific organ which expressed the molecule."),
    Column("pdbx_host_org_organelle", Text, nullable=True, comment="Specific organelle which expressed the molecule."),
    Column("pdbx_host_org_cellular_location", Text, nullable=True, comment="Identifies the location inside (or outside) the cell which expressed the molecule."),
    Column("pdbx_host_org_strain", Text, nullable=True, comment="The strain of the organism in which the entity was expressed."),
    Column("pdbx_host_org_tissue_fraction", Text, nullable=True, comment="The fraction of the tissue which expressed the molecule."),
    Column("pdbx_description", Text, nullable=True, comment="Information on the source which is not given elsewhere."),
    Column("host_org_common_name", Text, nullable=True, comment="The common name of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item be derived from _entity_src_gen_express.host_org_common_name or via _entity_src_gen_express.host_org_tax_id"),
    Column("host_org_details", Text, nullable=True, comment="A description of special aspects of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item would derived from _entity_src_gen_express.host_org_details"),
    Column("plasmid_details", Text, nullable=True, comment="A description of special aspects of the plasmid that produced the entity in the host organism. Where full details of the protein production are available it would be expected that this item would be derived from _pdbx_construct.details of the construct pointed to from _entity_src_gen_express.plasmid_id."),
    Column("plasmid_name", Text, nullable=True, comment="The name of the plasmid that produced the entity in the host organism. Where full details of the protein production are available it would be expected that this item would be derived from _pdbx_construct.name of the construct pointed to from _entity_src_gen_express.plasmid_id."),
    Column("pdbx_host_org_variant", Text, nullable=True, comment="Variant of the organism used as the expression system. Where full details of the protein production are available it would be expected that this item be derived from entity_src_gen_express.host_org_variant or via _entity_src_gen_express.host_org_tax_id"),
    Column("pdbx_host_org_cell_line", Text, nullable=True, comment="A specific line of cells used as the expression system. Where full details of the protein production are available it would be expected that this item would be derived from entity_src_gen_express.host_org_cell_line"),
    Column("pdbx_host_org_atcc", Text, nullable=True, comment="Americal Tissue Culture Collection of the expression system. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_culture_collection"),
    Column("pdbx_host_org_culture_collection", Text, nullable=True, comment="Culture collection of the expression system. Where full details of the protein production are available it would be expected that this item would be derived somehwere, but exactly where is not clear."),
    Column("pdbx_host_org_cell", Text, nullable=True, comment="Cell type from which the gene is derived. Where entity.target_id is provided this should be derived from details of the target."),
    Column("pdbx_host_org_scientific_name", Text, nullable=True, comment="The scientific name of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_scientific_name or via _entity_src_gen_express.host_org_tax_id"),
    Column("pdbx_host_org_tissue", Text, nullable=True, comment="The specific tissue which expressed the molecule. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_tissue"),
    Column("pdbx_host_org_vector", Text, nullable=True, comment="Identifies the vector used. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_clone.vector_name."),
    Column("pdbx_host_org_vector_type", Text, nullable=True, comment="Identifies the type of vector used (plasmid, virus, or cosmid). Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.vector_type."),
    Column("expression_system_id", Text, nullable=True, comment="A unique identifier for the expression system. This should be extracted from a local list of expression systems."),
    Column("pdbx_gene_src_ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier for the gene source organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("pdbx_host_org_ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier for the expression system organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("pdbx_src_id", Integer, nullable=True, comment="This data item is an ordinal identifier for entity_src_gen data records."),
    Column("pdbx_alt_source_flag", Text, nullable=True, comment="This data item identifies cases in which an alternative source modeled."),
    Column("pdbx_seq_type", Text, nullable=True, comment="This data item povides additional information about the sequence type."),
    Column("pdbx_beg_seq_num", Integer, nullable=True, comment="The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    Column("pdbx_end_seq_num", Integer, nullable=True, comment="The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    PrimaryKeyConstraint("pdbid", "entity_id", "pdbx_src_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={
        "keywords": [
            "gene_src_common_name",
            "gene_src_details",
            "gene_src_genus",
            "gene_src_species",
            "gene_src_strain",
            "gene_src_tissue",
            "gene_src_tissue_fraction",
            "host_org_genus",
            "host_org_species",
            "pdbx_gene_src_fragment",
            "pdbx_gene_src_gene",
            "pdbx_gene_src_scientific_name",
            "pdbx_gene_src_variant",
            "pdbx_gene_src_cell_line",
            "pdbx_gene_src_atcc",
            "pdbx_gene_src_organ",
            "pdbx_gene_src_organelle",
            "pdbx_gene_src_plasmid",
            "pdbx_gene_src_plasmid_name",
            "pdbx_gene_src_cell",
            "pdbx_gene_src_cellular_location",
            "pdbx_host_org_gene",
            "pdbx_host_org_organ",
            "pdbx_host_org_organelle",
            "pdbx_host_org_cellular_location",
            "pdbx_host_org_strain",
            "pdbx_host_org_tissue_fraction",
            "pdbx_description",
            "host_org_common_name",
            "host_org_details",
            "host_org_strain",
            "plasmid_details",
            "plasmid_name",
            "pdbx_host_org_variant",
            "pdbx_host_org_cell_line",
            "pdbx_host_org_atcc",
            "pdbx_host_org_culture_collection",
            "pdbx_host_org_cell",
            "pdbx_host_org_scientific_name",
            "pdbx_host_org_tissue",
            "pdbx_host_org_vector",
            "pdbx_host_org_vector_type",
            "gene_src_dev_stage",
            "pdbx_gene_src_ncbi_taxonomy_id",
            "pdbx_host_org_ncbi_taxonomy_id",
            "pdbx_gene_src_culture_collection",
        ]
    },
)

pdbx_entity_src_syn = Table(
    "pdbx_entity_src_syn",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the source for the synthetic entity."),
    Column("organism_scientific", Text, nullable=True, comment="The scientific name of the organism from which the sequence of the synthetic entity was derived."),
    Column("organism_common_name", Text, nullable=True, comment="The common name of the organism from which the sequence of the synthetic entity was derived."),
    Column("ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier of the organism from which the sequence of the synthetic entity was derived. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("pdbx_src_id", Integer, nullable=True, comment="This data item is an ordinal identifier for pdbx_entity_src_syn data records."),
    Column("pdbx_alt_source_flag", Text, nullable=True, comment="This data item identifies cases in which an alternative source modeled."),
    Column("pdbx_beg_seq_num", Integer, nullable=True, comment="The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    Column("pdbx_end_seq_num", Integer, nullable=True, comment="The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    PrimaryKeyConstraint("pdbid", "entity_id", "pdbx_src_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={
        "keywords": [
            "details",
            "organism_scientific",
            "organism_common_name",
            "strain",
            "ncbi_taxonomy_id",
        ]
    },
)

pdbx_entity_branch_descriptor = Table(
    "pdbx_entity_branch_descriptor",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity_poly.entity_id in the ENTITY category."),
    Column("descriptor", Text, nullable=True, comment="This data item contains the descriptor value for this entity."),
    Column("type", Text, nullable=True, comment="This data item contains the descriptor type."),
    Column("program", Text, nullable=True, comment="This data item contains the name of the program or library used to compute the descriptor."),
    Column("program_version", Text, nullable=True, comment="This data item contains the version of the program or library used to compute the descriptor."),
    Column("ordinal", Integer, nullable=True, comment="Ordinal index for this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["descriptor", "program", "program_version"]},
)

pdbx_related_exp_data_set = Table(
    "pdbx_related_exp_data_set",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Ordinal identifier for each related experimental data set."),
    Column("data_reference", Text, nullable=True, comment="A DOI reference to the related data set."),
    Column("metadata_reference", Text, nullable=True, comment="A DOI reference to the metadata decribing the related data set."),
    Column("data_set_type", Text, nullable=True, comment="The type of the experimenatal data set."),
    Column("details", Text, nullable=True, comment="Additional details describing the content of the related data set and its application to the current investigation."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": ["data_reference", "metadata_reference", "data_set_type", "details"]
    },
)

em_entity_assembly = Table(
    "em_entity_assembly",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("parent_id", Integer, nullable=True, comment="The parent of this assembly. This data item is an internal category pointer to _em_entity_assembly.id. By convention, the full assembly (top of hierarchy) is assigned parent id 0 (zero)."),
    Column("source", Text, nullable=True, comment="The type of source (e.g., natural source) for the component (sample or sample subcomponent)"),
    Column("type", Text, nullable=True, comment="The general type of the sample or sample subcomponent."),
    Column("name", Text, nullable=True, comment="The name of the sample or sample subcomponent."),
    Column("details", Text, nullable=True, comment="Additional details about the sample or sample subcomponent."),
    Column("synonym", Text, nullable=True, comment="Alternative name of the component."),
    Column("oligomeric_details", Text, nullable=True, comment="oligomeric details"),
    Column("entity_id_list", Text, nullable=True, comment="macromolecules associated with this component, if defined as comma separated list of entity ids (integers)."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "type",
            "name",
            "details",
            "go_id",
            "ipr_id",
            "synonym",
            "oligomeric_details",
            "entity_id_list",
            "ebi_organism_scientific",
            "ebi_organism_common",
            "ebi_strain",
            "ebi_tissue",
            "ebi_cell",
            "ebi_organelle",
            "ebi_cellular_location",
            "ebi_expression_system",
            "ebi_expression_system_plasmid",
        ]
    },
)

em_virus_entity = Table(
    "em_virus_entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("virus_host_category", Text, nullable=True, comment="The host category description for the virus."),
    Column("virus_type", Text, nullable=True, comment="The type of virus."),
    Column("virus_isolate", Text, nullable=True, comment="The isolate from which the virus was obtained."),
    Column("entity_assembly_id", Text, nullable=True, comment="This data item is a pointer to _em_virus_entity.id in the ENTITY_ASSEMBLY category."),
    Column("enveloped", Text, nullable=True, comment="Flag to indicate if the virus is enveloped or not."),
    Column("empty", Text, nullable=True, comment="Flag to indicate if the virus is empty or not."),
    Column("details", Text, nullable=True, comment="Additional details about this virus entity"),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={
        "keywords": [
            "virus_host_category",
            "virus_host_species",
            "virus_host_growth_cell",
            "ictvdb_id",
            "details",
        ]
    },
)

em_sample_support = Table(
    "em_sample_support",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("film_material", Text, nullable=True, comment="The support material covering the em grid."),
    Column("grid_material", Text, nullable=True, comment="The name of the material from which the grid is made."),
    Column("grid_mesh_size", Integer, nullable=True, comment="The value of the mesh size (divisions per inch) of the em grid."),
    Column("grid_type", Text, nullable=True, comment="A description of the grid type."),
    Column("details", Text, nullable=True, comment="Any additional details concerning the sample support."),
    Column("specimen_id", Text, nullable=True, comment="This data item is a pointer to _em_sample_preparation.id in the EM_SPECIMEN category."),
    PrimaryKeyConstraint("pdbid", "id", "specimen_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method", "grid_type", "pretreatment", "details"]},
)

em_buffer = Table(
    "em_buffer",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("specimen_id", Text, nullable=True, comment="pointer to _em_specimen.id"),
    Column("name", Text, nullable=True, comment="The name of the buffer."),
    Column("details", Text, nullable=True, comment="Additional details about the buffer."),
    Column("pH", Double, nullable=True, comment="The pH of the sample buffer."),
    PrimaryKeyConstraint("pdbid", "id", "specimen_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

em_vitrification = Table(
    "em_vitrification",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("specimen_id", Text, nullable=True, comment="This data item is a pointer to _em_specimen.id"),
    Column("cryogen_name", Text, nullable=True, comment="This is the name of the cryogen."),
    Column("humidity", Double, nullable=True, comment="Relative humidity (%) of air surrounding the specimen just prior to vitrification."),
    Column("temp", Double, nullable=True, comment="The vitrification temperature (in kelvin), e.g., temperature of the plunge instrument cryogen bath."),
    Column("chamber_temperature", Double, nullable=True, comment="The temperature (in kelvin) of the sample just prior to vitrification."),
    Column("instrument", Text, nullable=True, comment="The type of instrument used in the vitrification process."),
    Column("method", Text, nullable=True, comment="The procedure for vitrification."),
    Column("time_resolved_state", Text, nullable=True, comment="The length of time after an event effecting the sample that vitrification was induced and a description of the event."),
    Column("details", Text, nullable=True, comment="Any additional details relating to vitrification."),
    PrimaryKeyConstraint("pdbid", "id", "specimen_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["method", "time_resolved_state", "details"]},
)

em_imaging = Table(
    "em_imaging",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("astigmatism", Text, nullable=True, comment="astigmatism"),
    Column("electron_beam_tilt_params", Text, nullable=True, comment="electron beam tilt params"),
    Column("residual_tilt", Double, nullable=True, comment="Residual tilt of the electron beam (in miliradians)"),
    Column("microscope_model", Text, nullable=True, comment="The name of the model of microscope."),
    Column("specimen_holder_type", Text, nullable=True, comment="The type of specimen holder used during imaging."),
    Column("specimen_holder_model", Text, nullable=True, comment="The name of the model of specimen holder used during imaging."),
    Column("details", Text, nullable=True, comment="Any additional imaging details."),
    Column("date", Date, nullable=True, comment="Date (YYYY-MM-DD) of imaging experiment or the date at which a series of experiments began."),
    Column("accelerating_voltage", Integer, nullable=True, comment="A value of accelerating voltage (in kV) used for imaging."),
    Column("illumination_mode", Text, nullable=True, comment="The mode of illumination."),
    Column("mode", Text, nullable=True, comment="The mode of imaging."),
    Column("nominal_cs", Double, nullable=True, comment="The spherical aberration coefficient (Cs) in millimeters, of the objective lens."),
    Column("nominal_defocus_min", Double, nullable=True, comment="The minimum defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("nominal_defocus_max", Double, nullable=True, comment="The maximum defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("calibrated_defocus_min", Double, nullable=True, comment="The minimum calibrated defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("calibrated_defocus_max", Double, nullable=True, comment="The maximum calibrated defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("tilt_angle_min", Double, nullable=True, comment="The minimum angle at which the specimen was tilted to obtain recorded images."),
    Column("tilt_angle_max", Double, nullable=True, comment="The maximum angle at which the specimen was tilted to obtain recorded images."),
    Column("nominal_magnification", Integer, nullable=True, comment="The magnification indicated by the microscope readout."),
    Column("calibrated_magnification", Integer, nullable=True, comment="The magnification value obtained for a known standard just prior to, during or just after the imaging experiment."),
    Column("electron_source", Text, nullable=True, comment="The source of electrons. The electron gun."),
    Column("temperature", Double, nullable=True, comment="The mean specimen stage temperature (in kelvin) during imaging in the microscope."),
    Column("detector_distance", Double, nullable=True, comment="The camera length (in millimeters). The camera length is the product of the objective focal length and the combined magnification of the intermediate and projector lenses when the microscope is operated in the diffraction mode."),
    Column("recording_temperature_minimum", Double, nullable=True, comment="The specimen temperature minimum (kelvin) for the duration of imaging."),
    Column("recording_temperature_maximum", Double, nullable=True, comment="The specimen temperature maximum (kelvin) for the duration of imaging."),
    Column("alignment_procedure", Text, nullable=True, comment="The type of procedure used to align the microscope electron beam."),
    Column("c2_aperture_diameter", Double, nullable=True, comment="The open diameter of the c2 condenser lens, in microns."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key to the EM_SPECIMEN category"),
    Column("cryogen", Text, nullable=True, comment="Cryogen type used to maintain the specimen stage temperature during imaging in the microscope."),
    PrimaryKeyConstraint("pdbid", "entry_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "astigmatism",
            "electron_beam_tilt_params",
            "specimen_holder_type",
            "details",
            "electron_source",
            "energy_filter",
            "energy_window",
            "microscope_serial_number",
            "microscope_version",
        ]
    },
)

em_image_scans = Table(
    "em_image_scans",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="The value of _em_image_scans.id must uniquely identify the images scanned."),
    Column("number_digital_images", Integer, nullable=True, comment="The number of real images."),
    Column("details", Text, nullable=True, comment="Any additional details about image recording."),
    Column("scanner_model", Text, nullable=True, comment="The scanner model."),
    Column("sampling_size", Double, nullable=True, comment="The sampling step size (microns) set on the scanner."),
    Column("od_range", Double, nullable=True, comment="The optical density range (OD=-log 10 transmission). To the eye OD=1 appears light grey and OD=3 is opaque."),
    Column("quant_bit_size", Integer, nullable=True, comment="The number of bits per pixel."),
    Column("dimension_height", Integer, nullable=True, comment="Height of scanned image, in pixels"),
    Column("dimension_width", Integer, nullable=True, comment="Width of scanned image, in pixels"),
    Column("frames_per_image", Integer, nullable=True, comment="Total number of time-slice (movie) frames taken per image."),
    Column("image_recording_id", Text, nullable=True, comment="foreign key linked to _em_image_recording"),
    Column("used_frames_per_image", Text, nullable=True, comment="Range of time-slice (movie) frames used for the reconstruction."),
    PrimaryKeyConstraint("pdbid", "id", "image_recording_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details"]},
)

em_3d_reconstruction = Table(
    "em_3d_reconstruction",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("method", Text, nullable=True, comment="The algorithm method used for the 3d-reconstruction."),
    Column("algorithm", Text, nullable=True, comment="The reconstruction algorithm/technique used to generate the map."),
    Column("details", Text, nullable=True, comment="Any additional details used in the 3d reconstruction."),
    Column("resolution", Double, nullable=True, comment="The final resolution (in angstroms) of the 3D reconstruction."),
    Column("resolution_method", Text, nullable=True, comment="The method used to determine the final resolution of the 3d reconstruction. The Fourier Shell Correlation criterion as a measure of resolution is based on the concept of splitting the (2D) data set into two halves; averaging each and comparing them using the Fourier Ring Correlation (FRC) technique."),
    Column("magnification_calibration", Text, nullable=True, comment="The magnification calibration method for the 3d reconstruction."),
    Column("nominal_pixel_size", Double, nullable=True, comment="The nominal pixel size of the projection set of images in Angstroms."),
    Column("actual_pixel_size", Double, nullable=True, comment="The actual pixel size of the projection set of images in Angstroms."),
    Column("num_particles", Integer, nullable=True, comment="The number of 2D projections or 3D subtomograms used in the 3d reconstruction"),
    Column("num_class_averages", Integer, nullable=True, comment="The number of classes used in the final 3d reconstruction"),
    Column("refinement_type", Text, nullable=True, comment="Indicates details on how the half-map used for resolution determination (usually by FSC) have been generated."),
    Column("image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("symmetry_type", Text, nullable=True, comment="The type of symmetry applied to the reconstruction"),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={
        "keywords": [
            "method",
            "algorithm",
            "details",
            "resolution_method",
            "magnification_calibration",
            "ctf_correction_method",
            "euler_angles_details",
            "software",
        ]
    },
)

em_3d_fitting = Table(
    "em_3d_fitting",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _em_3d_fitting.id must uniquely identify a fitting procedure of atomic coordinates into 3dem reconstructed map volume."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry_id in the ENTRY category."),
    Column("method", Text, nullable=True, comment="The method used to fit atomic coordinates into the 3dem reconstructed map."),
    Column("target_criteria", Text, nullable=True, comment="The measure used to assess quality of fit of the atomic coordinates in the 3DEM map volume."),
    Column("details", Text, nullable=True, comment="Any additional details regarding fitting of atomic coordinates into the 3DEM volume, including data and considerations from other methods used in computation of the model."),
    Column("overall_b_value", Double, nullable=True, comment="The overall B (temperature factor) value for the 3d-em volume."),
    Column("ref_space", Text, nullable=True, comment="A flag to indicate whether fitting was carried out in real or reciprocal refinement space."),
    Column("ref_protocol", Text, nullable=True, comment="The refinement protocol used."),
    PrimaryKeyConstraint("pdbid", "id", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["method", "target_criteria", "software_name", "details"]},
)

em_3d_fitting_list = Table(
    "em_3d_fitting_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("3d_fitting_id", Text, nullable=True, comment="The value of _em_3d_fitting_list.3d_fitting_id is a pointer to _em_3d_fitting.id in the 3d_fitting category"),
    Column("pdb_entry_id", Text, nullable=True, comment="The PDB code for the entry used in fitting."),
    Column("pdb_chain_id", Text, nullable=True, comment="The ID of the biopolymer chain used for fitting, e.g., A. Please note that only one chain can be specified per instance. If all chains of a particular structure have been used for fitting, this field can be left blank."),
    Column("pdb_chain_residue_range", Text, nullable=True, comment="Residue range for the identified chain."),
    Column("details", Text, nullable=True, comment="Details about the model used in fitting."),
    Column("chain_id", Text, nullable=True, comment="The ID of the biopolymer chain used for fitting, e.g., A. Please note that only one chain can be specified per instance. If all chains of a particular structure have been used for fitting, this field can be left blank."),
    Column("chain_residue_range", Text, nullable=True, comment="The residue ranges of the initial model used in this fitting."),
    Column("source_name", Text, nullable=True, comment="This item identifies the resource of initial model used for refinement"),
    Column("type", Text, nullable=True, comment="This item describes the type of the initial model was generated"),
    Column("accession_code", Text, nullable=True, comment="This item identifies an accession code of the resource where the initial model is used"),
    Column("initial_refinement_model_id", Integer, nullable=True, comment="The value of _em_3d_fitting.initial_refinement_model_id itentifies the id in the _pdbx_initial_refinement_model"),
    PrimaryKeyConstraint("pdbid", "id", "3d_fitting_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "accession_code"]},
)

em_helical_entity = Table(
    "em_helical_entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="This data item is a pointer to _em_image_processing.id."),
    Column("details", Text, nullable=True, comment="Any other details regarding the helical assembly"),
    Column("axial_symmetry", Text, nullable=True, comment="Symmetry of the helical axis, either cyclic (Cn) or dihedral (Dn), where n>=1."),
    Column("angular_rotation_per_subunit", Double, nullable=True, comment="The angular rotation per helical subunit in degrees. Negative values indicate left-handed helices; positive values indicate right handed helices."),
    Column("axial_rise_per_subunit", Double, nullable=True, comment="The axial rise per subunit in the helical assembly."),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "hand"]},
)

em_experiment = Table(
    "em_experiment",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("reconstruction_method", Text, nullable=True, comment="The reconstruction method used in the EM experiment."),
    Column("aggregation_state", Text, nullable=True, comment="The aggregation/assembly state of the imaged specimen."),
    Column("entity_assembly_id", Text, nullable=True, comment="Foreign key to the EM_ENTITY_ASSEMBLY category"),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["specimen_type"]},
)

em_single_particle_entity = Table(
    "em_single_particle_entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Integer, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id."),
    Column("point_symmetry", Text, nullable=True, comment="Point symmetry symbol, either Cn, Dn, T, O, or I"),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

em_admin = Table(
    "em_admin",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("current_status", Text, nullable=True, comment="This data item indicates the current status of the EMDB entry."),
    Column("deposition_date", Date, nullable=True, comment="date of the entry deposition"),
    Column("deposition_site", Text, nullable=True, comment="entry deposition site"),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id."),
    Column("last_update", Date, nullable=True, comment="date of last update to the file"),
    Column("map_release_date", Date, nullable=True, comment="date of map release for this entry"),
    Column("title", Text, nullable=True, comment="Title for the EMDB entry."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "title"]},
)

em_entity_assembly_molwt = Table(
    "em_entity_assembly_molwt",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_assembly_id", Text, nullable=True, comment="A reference to em_entity_assembly.id which uniquely identifies one sample or sample subcomponent of the imaged specimen."),
    Column("experimental_flag", Text, nullable=True, comment="Identifies whether the given molecular weight was derived experimentally."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("units", Text, nullable=True, comment="Molecular weight units."),
    Column("value", Double, nullable=True, comment="The molecular weight of the sample or sample subcomponent"),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["method"]},
)

em_entity_assembly_naturalsource = Table(
    "em_entity_assembly_naturalsource",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("cell", Text, nullable=True, comment="The cell type from which the component was obtained."),
    Column("cellular_location", Text, nullable=True, comment="The cellular location of the component."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to the assembly component defined in the EM ENTITY ASSEMBLY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id for the natural organism source of the component."),
    Column("organism", Text, nullable=True, comment="The scientific name of the source organism for the component"),
    Column("organelle", Text, nullable=True, comment="The organelle from which the component was obtained."),
    Column("organ", Text, nullable=True, comment="The organ of the organism from which the component was obtained."),
    Column("strain", Text, nullable=True, comment="The strain of the natural organism from which the component was obtained, if relevant."),
    Column("tissue", Text, nullable=True, comment="The tissue of the natural organism from which the component was obtained."),
    Column("details", Text, nullable=True, comment="Additional details describing this natural source."),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={
        "keywords": [
            "cell",
            "cellular_location",
            "organism",
            "organelle",
            "organ",
            "strain",
            "tissue",
            "details",
        ]
    },
)

em_entity_assembly_synthetic = Table(
    "em_entity_assembly_synthetic",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to the assembly component defined in the EM ENTITY ASSEMBLY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id for the synthetic organism source of the component."),
    Column("organism", Text, nullable=True, comment="The scientific name of the source organism for the component"),
    Column("strain", Text, nullable=True, comment="The strain of the synthetic organism from which the component was obtained, if relevant."),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={
        "keywords": [
            "cell",
            "cellular_location",
            "organism",
            "organelle",
            "organ",
            "strain",
            "tissue",
        ]
    },
)

em_entity_assembly_recombinant = Table(
    "em_entity_assembly_recombinant",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("cell", Text, nullable=True, comment="The cell of the host organism from which the expressed component was obtained, if relevant."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to the expressed component described in the EM ENTITY ASSEMBLY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id of the expression host used to produce the component."),
    Column("organism", Text, nullable=True, comment="Expression system host organism used to produce the component."),
    Column("plasmid", Text, nullable=True, comment="The plasmid used to produce the component in the expression system."),
    Column("strain", Text, nullable=True, comment="The strain of the host organism from which the expresed component was obtained, if relevant."),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["cell", "organism", "plasmid", "strain"]},
)

em_virus_natural_host = Table(
    "em_virus_natural_host",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to _em_entity_assembly.id."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id for the natural host organism of the virus"),
    Column("organism", Text, nullable=True, comment="The host organism from which the virus was isolated."),
    Column("strain", Text, nullable=True, comment="The strain of the host organism from which the virus was obtained, if relevant."),
    PrimaryKeyConstraint("pdbid", "entity_assembly_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_synthetic = Table(
    "em_virus_synthetic",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to _em_entity_assembly.id."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("organism", Text, nullable=True, comment="The host organism from which the virus was isolated."),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy ID of the host species from which the virus was isolated"),
    Column("strain", Text, nullable=True, comment="The strain of the host organism from which the virus was obtained, if relevant."),
    PrimaryKeyConstraint("pdbid", "entity_assembly_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_shell = Table(
    "em_virus_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diameter", Double, nullable=True, comment="The value of the diameter (in angstroms) for this virus shell."),
    Column("entity_assembly_id", Text, nullable=True, comment="The value of _em_virus_shell.entity_assembly_id is a pointer to _em_entity_assembly.id category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("name", Text, nullable=True, comment="The name for this virus shell."),
    Column("triangulation", Integer, nullable=True, comment="The triangulation number, T, describes the organization of subunits within an icosahedron. T is defined as T= h^2 + h*k + k^2, where h and k are positive integers that define the position of the five-fold vertex on the original hexagonal net."),
    PrimaryKeyConstraint("pdbid", "entity_assembly_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["name"]},
)

em_specimen = Table(
    "em_specimen",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("concentration", Double, nullable=True, comment="The concentration (in milligrams per milliliter, mg/ml) of the complex in the sample."),
    Column("details", Text, nullable=True, comment="A description of any additional details of the specimen preparation."),
    Column("embedding_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen has been embedded."),
    Column("experiment_id", Text, nullable=True, comment="Pointer to _em_experiment.id."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("shadowing_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen has been shadowed."),
    Column("staining_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen has been stained."),
    Column("vitrification_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen was vitrified by cryopreservation."),
    PrimaryKeyConstraint("pdbid", "id", "experiment_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

em_embedding = Table(
    "em_embedding",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Staining procedure used in the specimen preparation."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("material", Text, nullable=True, comment="The embedding material."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM SPECIMEN category"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "material"]},
)

em_crystal_formation = Table(
    "em_crystal_formation",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atmosphere", Text, nullable=True, comment="The type of atmosphere in which crystals were grown"),
    Column("details", Text, nullable=True, comment="Description of growth of a 2D, 3D, or helical crystal array."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("instrument", Text, nullable=True, comment="Instrument used to prepare the crystalline array"),
    Column("lipid_mixture", Text, nullable=True, comment="Description of the lipid mixture used for crystallization"),
    Column("lipid_protein_ratio", Double, nullable=True, comment="The molar ratio of lipid to protein in the crystallized sample"),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the em_specimen category"),
    Column("temperature", Integer, nullable=True, comment="The value of the temperature in kelvin used for growing the crystals."),
    Column("time", Integer, nullable=True, comment="Time period for array crystallization, in time unit indicated (min, hr, day, month, year)"),
    Column("time_unit", Text, nullable=True, comment="Time unit for array crystallization"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["atmosphere", "details", "instrument", "lipid_mixture"]},
)

em_staining = Table(
    "em_staining",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Staining procedure used in the specimen preparation."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("material", Text, nullable=True, comment="The staining material."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM SPECIMEN category"),
    Column("type", Text, nullable=True, comment="type of staining"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "material"]},
)

em_buffer_component = Table(
    "em_buffer_component",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("buffer_id", Text, nullable=True, comment="Foreign key to the entry category."),
    Column("concentration", Double, nullable=True, comment="The concentration of the sample (arbitrary units)."),
    Column("concentration_units", Text, nullable=True, comment="Units for the sample concentration value."),
    Column("formula", Text, nullable=True, comment="formula for buffer component"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("name", Text, nullable=True, comment="name of the buffer component"),
    PrimaryKeyConstraint("pdbid", "id", "buffer_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["concentration_units", "name"]},
)

em_diffraction = Table(
    "em_diffraction",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("camera_length", Double, nullable=True, comment="The camera length (in millimeters). The camera length is the product of the objective focal length and the combined magnification of the intermediate and projector lenses when the microscope is operated in the diffraction mode."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="Foreign key to the EM_IMAGING category"),
    Column("tilt_angle_list", Text, nullable=True, comment="Comma-separated list of tilt angles (in degrees) used in the electron diffraction experiment."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["tilt_angle_list"]},
)

em_diffraction_shell = Table(
    "em_diffraction_shell",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("em_diffraction_stats_id", Text, nullable=True, comment="Pointer to EM CRYSTALLOGRAPHY STATS"),
    Column("fourier_space_coverage", Double, nullable=True, comment="Completeness of the structure factor data within this resolution shell, in percent"),
    Column("high_resolution", Double, nullable=True, comment="High resolution limit for this shell (angstroms)"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("low_resolution", Double, nullable=True, comment="Low resolution limit for this shell (angstroms)"),
    Column("multiplicity", Double, nullable=True, comment="Multiplicity (average number of measurements) for the structure factors in this resolution shell"),
    Column("num_structure_factors", Integer, nullable=True, comment="Number of measured structure factors in this resolution shell"),
    Column("phase_residual", Double, nullable=True, comment="Phase residual for this resolution shell, in degrees"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

em_diffraction_stats = Table(
    "em_diffraction_stats",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Any addition details about the structure factor measurements"),
    Column("fourier_space_coverage", Double, nullable=True, comment="Completeness of the structure factor data within the defined space group at the reported resolution (percent)."),
    Column("high_resolution", Double, nullable=True, comment="High resolution limit of the structure factor data, in angstroms"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="Pointer to _em_image_processing.id"),
    Column("num_intensities_measured", Integer, nullable=True, comment="Total number of diffraction intensities measured (before averaging)"),
    Column("num_structure_factors", Integer, nullable=True, comment="Number of structure factors obtained (merged amplitudes + phases)"),
    Column("overall_phase_error", Double, nullable=True, comment="Overall phase error in degrees"),
    Column("overall_phase_residual", Double, nullable=True, comment="Overall phase residual in degrees"),
    Column("phase_error_rejection_criteria", Text, nullable=True, comment="Criteria used to reject phases"),
    Column("r_merge", Double, nullable=True, comment="Rmerge value (percent)"),
    Column("r_sym", Double, nullable=True, comment="Rsym value (percent)"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "phase_error_rejection_criteria"]},
)

em_image_recording = Table(
    "em_image_recording",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("average_exposure_time", Double, nullable=True, comment="The average exposure time for each image."),
    Column("avg_electron_dose_per_subtomogram", Double, nullable=True, comment="The average total electron dose received by the specimen for each subtomogram (electrons per square angstrom)."),
    Column("avg_electron_dose_per_image", Double, nullable=True, comment="The electron dose received by the specimen per image (electrons per square angstrom)."),
    Column("details", Text, nullable=True, comment="Any additional details about image recording."),
    Column("detector_mode", Text, nullable=True, comment="The detector mode used during image recording."),
    Column("film_or_detector_model", Text, nullable=True, comment="The detector type used for recording images. Usually film , CCD camera or direct electron detector."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="This data item the id of the microscopy settings used in the imaging."),
    Column("num_diffraction_images", Integer, nullable=True, comment="The number of diffraction images collected."),
    Column("num_grids_imaged", Integer, nullable=True, comment="Number of grids in the microscopy session"),
    Column("num_real_images", Integer, nullable=True, comment="The number of micrograph images collected."),
    PrimaryKeyConstraint("pdbid", "id", "imaging_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "film_or_detector_model"]},
)

em_imaging_optics = Table(
    "em_imaging_optics",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("chr_aberration_corrector", Text, nullable=True, comment="Chromatic aberration corrector information"),
    Column("energyfilter_lower", Text, nullable=True, comment="The energy filter range lower value in electron volts (eV) set by spectrometer."),
    Column("energyfilter_slit_width", Double, nullable=True, comment="The energy filter range slit width in electron volts (eV)."),
    Column("energyfilter_name", Text, nullable=True, comment="The type of energy filter spectrometer"),
    Column("energyfilter_upper", Text, nullable=True, comment="The energy filter range upper value in electron volts (eV) set by spectrometer."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="Foreign key to the EM IMAGING category"),
    Column("phase_plate", Text, nullable=True, comment="Phase plate information"),
    Column("sph_aberration_corrector", Text, nullable=True, comment="Spherical aberration corrector information"),
    Column("details", Text, nullable=True, comment="Details on the use of the phase plate"),
    PrimaryKeyConstraint("pdbid", "id", "imaging_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "chr_aberration_corrector",
            "energyfilter_lower",
            "energyfilter_name",
            "energyfilter_upper",
            "phase_plate",
            "sph_aberration_corrector",
            "details",
        ]
    },
)

em_software = Table(
    "em_software",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("category", Text, nullable=True, comment="The purpose of the software."),
    Column("details", Text, nullable=True, comment="Details about the software used."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category."),
    Column("fitting_id", Text, nullable=True, comment="pointer to _em_3d_fitting.id in the EM_3D_FITTING category."),
    Column("imaging_id", Text, nullable=True, comment="pointer to _em_imaging.id in the EM_IMAGING category."),
    Column("name", Text, nullable=True, comment="The name of the software package used, e.g., RELION. Depositors are strongly encouraged to provide a value in this field."),
    Column("version", Text, nullable=True, comment="The version of the software."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "name", "version"]},
)

em_ctf_correction = Table(
    "em_ctf_correction",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Any additional details about CTF correction"),
    Column("em_image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("type", Text, nullable=True, comment="Type of CTF correction applied"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "type"]},
)

em_volume_selection = Table(
    "em_volume_selection",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Any additional details used for selecting volumes."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="The value of _em_volume_selection.image_processing_id points to the EM_IMAGE_PROCESSING category."),
    Column("method", Text, nullable=True, comment="The method used for selecting volumes."),
    Column("num_tomograms", Integer, nullable=True, comment="The number of tomograms used in the extraction/selection"),
    Column("num_volumes_extracted", Integer, nullable=True, comment="The number of volumes selected from the projection set of images."),
    Column("reference_model", Text, nullable=True, comment="Description of reference model used for volume selection"),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "method", "reference_model"]},
)

em_3d_crystal_entity = Table(
    "em_3d_crystal_entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("angle_alpha", Double, nullable=True, comment="Unit-cell angle alpha in degrees."),
    Column("angle_beta", Double, nullable=True, comment="Unit-cell angle beta in degrees."),
    Column("angle_gamma", Double, nullable=True, comment="Unit-cell angle gamma in degrees."),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("length_a", Double, nullable=True, comment="Unit-cell length a in angstroms."),
    Column("length_b", Double, nullable=True, comment="Unit-cell length b in angstroms."),
    Column("length_c", Double, nullable=True, comment="Unit-cell length c in angstroms."),
    Column("space_group_name", Text, nullable=True, comment="Space group name."),
    Column("space_group_num", Integer, nullable=True, comment="Space group number."),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["space_group_name"]},
)

em_2d_crystal_entity = Table(
    "em_2d_crystal_entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("angle_gamma", Double, nullable=True, comment="Unit-cell angle gamma in degrees."),
    Column("c_sampling_length", Double, nullable=True, comment="Length used to sample the reciprocal lattice lines in the c-direction."),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("length_a", Double, nullable=True, comment="Unit-cell length a in angstroms."),
    Column("length_b", Double, nullable=True, comment="Unit-cell length b in angstroms."),
    Column("length_c", Double, nullable=True, comment="Thickness of 2D crystal"),
    Column("space_group_name_H-M", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

em_image_processing = Table(
    "em_image_processing",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Method details."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_recording_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_RECORDING"),
    PrimaryKeyConstraint("pdbid", "image_recording_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

em_particle_selection = Table(
    "em_particle_selection",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("details", Text, nullable=True, comment="Additional detail such as description of filters used, if selection was manual or automated, and/or template details."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="The value of _em_particle_selection.image_processing_id points to the EM_IMAGE_PROCESSING category."),
    Column("num_particles_selected", BigInteger, nullable=True, comment="The number of particles selected from the projection set of images."),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "method", "reference_model"]},
)

pdbx_entity_instance_feature = Table(
    "pdbx_entity_instance_feature",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("feature_type", Text, nullable=True, comment="A feature type associated with entity instance."),
    Column("auth_asym_id", Text, nullable=True, comment="Author instance identifier (formerly PDB Chain ID)"),
    Column("asym_id", Text, nullable=True, comment="Instance identifier for this entity."),
    Column("auth_seq_num", Text, nullable=True, comment="Author provided residue number."),
    Column("comp_id", Text, nullable=True, comment="Chemical component identifier"),
    Column("auth_comp_id", Text, nullable=True, comment="The author provided chemical component identifier"),
    Column("ordinal", Integer, nullable=True, comment="An ordinal index for this category"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_deposit_group = Table(
    "pdbx_deposit_group",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("group_id", Text, nullable=True, comment="A unique identifier for a group of entries deposited as a collection."),
    Column("group_title", Text, nullable=True, comment="A title to describe the group of entries deposited in the collection."),
    Column("group_description", Text, nullable=True, comment="A description of the contents of entries in the collection."),
    Column("group_type", Text, nullable=True, comment="Text to describe a grouping of entries in multiple collections"),
    PrimaryKeyConstraint("pdbid", "group_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["group_title", "group_description"]},
)

pdbx_struct_assembly_auth_evidence = Table(
    "pdbx_struct_assembly_auth_evidence",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="Identifies a unique record in pdbx_struct_assembly_auth_evidence."),
    Column("assembly_id", Text, nullable=True, comment="This item references an assembly in pdbx_struct_assembly"),
    Column("experimental_support", Text, nullable=True, comment="Provides the experimental method to determine the state of this assembly"),
    Column("details", Text, nullable=True, comment="Provides any additional information regarding the evidence of this assembly"),
    PrimaryKeyConstraint("pdbid", "id", "assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, assembly_id) -> pdbx_struct_assembly(pdbid, id)
    info={"keywords": ["assembly_id", "details"]},
)

pdbx_audit_revision_history = Table(
    "pdbx_audit_revision_history",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_history record."),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("major_revision", Integer, nullable=True, comment="The major version number of deposition release."),
    Column("minor_revision", Integer, nullable=True, comment="The minor version number of deposition release."),
    Column("revision_date", Date, nullable=True, comment="The release date of the revision"),
    Column("part_number", Integer, nullable=True, comment="The part number of the content_type file correspondng to this milestone file"),
    PrimaryKeyConstraint("pdbid", "ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_audit_revision_group = Table(
    "pdbx_audit_revision_group",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_group record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("group", Text, nullable=True, comment="The collection of categories updated with this revision."),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
)

pdbx_audit_revision_category = Table(
    "pdbx_audit_revision_category",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_category record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("category", Text, nullable=True, comment="The category updated in the pdbx_audit_revision_category record."),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
)

pdbx_audit_revision_details = Table(
    "pdbx_audit_revision_details",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_details record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("provider", Text, nullable=True, comment="The provider of the revision."),
    Column("type", Text, nullable=True, comment="A type classification of the revision"),
    Column("description", Text, nullable=True, comment="Additional details describing the revision."),
    Column("details", Text, nullable=True, comment="Further details describing the revision."),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
    info={"keywords": ["description", "details"]},
)

pdbx_audit_revision_item = Table(
    "pdbx_audit_revision_item",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_item record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("item", Text, nullable=True, comment="A high level explanation the author has provided for submitting a revision."),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
)

pdbx_audit_conform = Table(
    "pdbx_audit_conform",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("dict_location", Text, nullable=True, comment="A file name or uniform resource locator (URL) for the dictionary to which the current data block conforms."),
    Column("dict_name", Text, nullable=True, comment="The dictionary name defining data names used in this file."),
    Column("dict_version", Text, nullable=True, comment="The version number of the dictionary to which the current data block conforms."),
    PrimaryKeyConstraint("pdbid", "dict_name", "dict_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)

pdbx_serial_crystallography_measurement = Table(
    "pdbx_serial_crystallography_measurement",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="The data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("pulse_energy", Double, nullable=True, comment="The energy/pulse of the X-ray pulse impacting the sample measured in microjoules."),
    Column("pulse_duration", Double, nullable=True, comment="The average duration (femtoseconds) of the pulse energy measured at the sample."),
    Column("xfel_pulse_repetition_rate", Double, nullable=True, comment="For FEL experiments, the pulse repetition rate measured in cycles per seconds."),
    Column("pulse_photon_energy", Double, nullable=True, comment="The photon energy of the X-ray pulse measured in KeV."),
    Column("photons_per_pulse", Double, nullable=True, comment="The photons per pulse measured in (tera photons (10^(12)^)/pulse units)."),
    Column("source_size", Double, nullable=True, comment="The dimension of the source beam measured at the source (micrometres squared)."),
    Column("source_distance", Double, nullable=True, comment="The distance from source to the sample along the optical axis (metres)."),
    Column("focal_spot_size", Double, nullable=True, comment="The focal spot size of the beam impinging on the sample (micrometres squared)."),
    Column("collimation", Text, nullable=True, comment="The collimation or type of focusing optics applied to the radiation."),
    Column("collection_time_total", Double, nullable=True, comment="The total number of hours required to measure this data set."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["collimation"]},
)

pdbx_serial_crystallography_sample_delivery = Table(
    "pdbx_serial_crystallography_sample_delivery",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="The data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("description", Text, nullable=True, comment="The description of the mechanism by which the specimen in placed in the path of the source."),
    Column("method", Text, nullable=True, comment="The description of the mechanism by which the specimen in placed in the path of the source."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["description"]},
)

pdbx_serial_crystallography_sample_delivery_injection = Table(
    "pdbx_serial_crystallography_sample_delivery_injection",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="The data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("description", Text, nullable=True, comment="For continuous sample flow experiments, a description of the injector used to move the sample into the beam."),
    Column("injector_diameter", Double, nullable=True, comment="For continuous sample flow experiments, the diameter of the injector in micrometres."),
    Column("injector_temperature", Double, nullable=True, comment="For continuous sample flow experiments, the temperature in Kelvins of the speciman injected. This may be different from the temperature of the sample."),
    Column("flow_rate", Double, nullable=True, comment="For continuous sample flow experiments, the flow rate of solution being injected measured in ul/min."),
    Column("carrier_solvent", Text, nullable=True, comment="For continuous sample flow experiments, the carrier buffer used to move the sample into the beam. Should include protein concentration."),
    Column("crystal_concentration", Double, nullable=True, comment="For continuous sample flow experiments, the concentration of crystals in the solution being injected. The concentration is measured in million crystals/ml."),
    Column("preparation", Text, nullable=True, comment="Details of crystal growth and preparation of the crystals"),
    Column("power_by", Text, nullable=True, comment="Sample deliver driving force, e.g. Gas, Electronic Potential"),
    Column("injector_nozzle", Text, nullable=True, comment="The type of nozzle to deliver and focus sample jet"),
    Column("jet_diameter", Double, nullable=True, comment="Diameter in micrometres of jet stream of sample delivery"),
    Column("filter_size", Double, nullable=True, comment="The size of filter in micrometres in filtering crystals"),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={
        "keywords": [
            "description",
            "carrier_solvent",
            "preparation",
            "power_by",
            "injector_nozzle",
        ]
    },
)

pdbx_serial_crystallography_sample_delivery_fixed_target = Table(
    "pdbx_serial_crystallography_sample_delivery_fixed_target",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="The data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("description", Text, nullable=True, comment="For a fixed target sample, a description of sample preparation"),
    Column("sample_holding", Text, nullable=True, comment="For a fixed target sample, mechanism to hold sample in the beam"),
    Column("support_base", Text, nullable=True, comment="Type of base holding the support"),
    Column("sample_unit_size", Double, nullable=True, comment="Size of pore in grid supporting sample. Diameter or length in micrometres, e.g. pore diameter"),
    Column("crystals_per_unit", Integer, nullable=True, comment="The number of crystals per dropplet or pore in fixed target"),
    Column("sample_solvent", Text, nullable=True, comment="The sample solution content and concentration"),
    Column("sample_dehydration_prevention", Text, nullable=True, comment="Method to prevent dehydration of sample"),
    Column("motion_control", Text, nullable=True, comment="Device used to control movement of the fixed sample"),
    Column("velocity_horizontal", Double, nullable=True, comment="Velocity of sample horizontally relative to a perpendicular beam in millimetres/second"),
    Column("velocity_vertical", Double, nullable=True, comment="Velocity of sample vertically relative to a perpendicular beam in millimetres/second"),
    Column("details", Text, nullable=True, comment="Any details pertinent to the fixed sample target"),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={
        "keywords": [
            "description",
            "sample_holding",
            "support_base",
            "sample_solvent",
            "sample_dehydration_prevention",
            "motion_control",
            "details",
        ]
    },
)

pdbx_serial_crystallography_data_reduction = Table(
    "pdbx_serial_crystallography_data_reduction",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("diffrn_id", Text, nullable=True, comment="The data item is a pointer to _diffrn.id in the DIFFRN category."),
    Column("frames_total", Integer, nullable=True, comment="The total number of data frames collected for this data set."),
    Column("xfel_pulse_events", Integer, nullable=True, comment="For FEL experiments, the number of pulse events in the dataset."),
    Column("frame_hits", Integer, nullable=True, comment="For experiments in which samples are provided in a continuous stream, the total number of data frames collected in which the sample was hit."),
    Column("crystal_hits", Integer, nullable=True, comment="For experiments in which samples are provided in a continuous stream, the total number of frames collected in which the crystal was hit."),
    Column("frames_failed_index", Integer, nullable=True, comment="For experiments in which samples are provided in a continuous stream, the total number of data frames collected that contained a \"hit\" but failed to index."),
    Column("frames_indexed", Integer, nullable=True, comment="For experiments in which samples are provided in a continuous stream, the total number of data frames collected that were indexed."),
    Column("lattices_indexed", Integer, nullable=True, comment="For experiments in which samples are provided in a continuous stream, the total number of lattices indexed."),
    Column("xfel_run_numbers", Text, nullable=True, comment="For FEL experiments, in which data collection was performed in batches, indicates which subset of the data collected were used in producing this dataset."),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["xfel_run_numbers"]},
)

pdbx_audit_support = Table(
    "pdbx_audit_support",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("funding_organization", Text, nullable=True, comment="The name of the organization providing funding support for the entry."),
    Column("country", Text, nullable=True, comment="The country/region providing the funding support for the entry."),
    Column("grant_number", Text, nullable=True, comment="The grant number associated with this source of support."),
    Column("ordinal", Integer, nullable=True, comment="A unique sequential integer identifier for each source of support for this entry."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["funding_organization", "country", "grant_number", "details"]},
)

pdbx_entity_branch_list = Table(
    "pdbx_entity_branch_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("hetero", Text, nullable=True, comment="A flag to indicate whether this monomer in the entity is heterogeneous in sequence."),
    Column("comp_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("num", Integer, nullable=True, comment="The value pair _pdbx_entity_branch_list.num and _pdbx_entity_branch_list.comp_id must uniquely identify a record in the PDBX_ENTITY_BRANCH_LIST list."),
    PrimaryKeyConstraint("pdbid", "entity_id", "num", "comp_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

pdbx_entity_branch_link = Table(
    "pdbx_entity_branch_link",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("link_id", Integer, nullable=True, comment="The value of _pdbx_entity_branch_link.link_id uniquely identifies linkages within the branched entity."),
    Column("entity_id", Text, nullable=True, comment="The entity id for this branched entity. This data item is a pointer to _pdbx_entity_branch_list.entity_id in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("entity_branch_list_num_1", Integer, nullable=True, comment="The component number for the first component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.num in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("entity_branch_list_num_2", Integer, nullable=True, comment="The component number for the second component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.num in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("comp_id_1", Text, nullable=True, comment="The component identifier for the first component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.comp_id in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("comp_id_2", Text, nullable=True, comment="The component identifier for the second component making the linkage. This data item is a pointer to _pdbx_entity_branch_list.comp_id in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("atom_id_1", Text, nullable=True, comment="The atom identifier/name for the first atom making the linkage."),
    Column("leaving_atom_id_1", Text, nullable=True, comment="The leaving atom identifier/name bonded to the first atom making the linkage."),
    Column("atom_id_2", Text, nullable=True, comment="The atom identifier/name for the second atom making the linkage."),
    Column("leaving_atom_id_2", Text, nullable=True, comment="The leaving atom identifier/name bonded to the second atom making the linkage."),
    Column("value_order", Text, nullable=True, comment="The bond order target for the chemical linkage."),
    PrimaryKeyConstraint("pdbid", "link_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_entity_branch = Table(
    "pdbx_entity_branch",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="The entity id for this branched entity. This data item is a pointer to _entity.id"),
    Column("type", Text, nullable=True, comment="The type of this branched oligosaccharide."),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

pdbx_branch_scheme = Table(
    "pdbx_branch_scheme",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("hetero", Text, nullable=True, comment="A flag to indicate whether this monomer in the entity is heterogeneous in sequence."),
    Column("asym_id", Text, nullable=True, comment="Pointer to _atom_site.label_asym_id."),
    Column("mon_id", Text, nullable=True, comment="This data item is a pointer to _atom_site.label_comp_id in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("num", Integer, nullable=True, comment="This data item is a pointer to _pdbx_entity_branch_list.num in the PDBX_ENTITY_BRANCH_LIST category."),
    Column("pdb_asym_id", Text, nullable=True, comment="This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("pdb_seq_num", Text, nullable=True, comment="This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("pdb_mon_id", Text, nullable=True, comment="This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="This data item is a pointer to _atom_site.pdbx_auth_asym_id in the ATOM_SITE category."),
    Column("auth_seq_num", Text, nullable=True, comment="This data item is a pointer to _atom_site.pdbx_auth_seq_id in the ATOM_SITE category."),
    Column("auth_mon_id", Text, nullable=True, comment="This data item is a pointer to _atom_site.pdbx_auth_comp_id in the ATOM_SITE category."),
    PrimaryKeyConstraint("pdbid", "asym_id", "entity_id", "num", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

pdbx_sifts_xref_db = Table(
    "pdbx_sifts_xref_db",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("asym_id", Text, nullable=True, comment="This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("seq_id_ordinal", Integer, nullable=True, comment="The value of pdbx_sifts_xref_db.seq_id_ordinal identifies a distinct residue specific cross-reference record in the _pdbx_sifts_xref_db category."),
    Column("seq_id", Integer, nullable=True, comment="This data item is an effective pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    Column("mon_id", Text, nullable=True, comment="This data item is an effective pointer to _entity_poly_seq.mon_id."),
    Column("mon_id_one_letter_code", Text, nullable=True, comment="Describes the standard polymer component of _pdbx_sifts_xref_db.mon_id as one-letter code"),
    Column("unp_res", Text, nullable=True, comment="Describes the residue type, in one-letter code, at the corresponding residue position of the related UniProt match"),
    Column("unp_num", Integer, nullable=True, comment="The sequence position of the UniProt entry that corresponds to the residue mapping."),
    Column("unp_acc", Text, nullable=True, comment="The UniProt accession code for the mapped entry"),
    Column("unp_segment_id", Integer, nullable=True, comment="The pdbx_sifts_xref_db UniProt segment ID refers to the distinct contiguous residue-range segments with a UniProt residue mapping."),
    Column("unp_instance_id", Integer, nullable=True, comment="The pdbx_sifts_xref_db UniProt instance ID refers to distinct UniProt residue mappings for a given position (i.e. the same segment, residue, asym, & entity)."),
    Column("res_type", Text, nullable=True, comment="A description of the difference between the entity sequence position residue type and that in the mapped UniProt entry."),
    Column("observed", Text, nullable=True, comment="Describes whether or not a reside has atomic coordinates in the corresponding model."),
    Column("mh_id", Integer, nullable=True, comment="An index value corresponding to the instance of microheterogeneity per residue"),
    Column("xref_db_name", Text, nullable=True, comment="The name of additional external databases with residue level mapping."),
    Column("xref_db_acc", Text, nullable=True, comment="The accession code related to the additional external database entry."),
    Column("xref_domain_name", Text, nullable=True, comment="The domain name defined by the external database."),
    Column("xref_db_segment_id", Integer, nullable=True, comment="The pdbx_sifts_xref_db xref segment ID refers to a distinct contiguous residue-range segment for a mapping to a specific external database."),
    Column("xref_db_instance_id", Integer, nullable=True, comment="The instance identifier defined by the external database."),
    PrimaryKeyConstraint("pdbid", "entity_id", "asym_id", "seq_id_ordinal", "seq_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
    info={"keywords": ["unp_acc", "res_type", "xref_domain_name"]},
)

pdbx_sifts_xref_db_segments = Table(
    "pdbx_sifts_xref_db_segments",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("asym_id", Text, nullable=True, comment="This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("xref_db", Text, nullable=True, comment="The name of additional external databases with range level mapping."),
    Column("xref_db_acc", Text, nullable=True, comment="The accession code related to the external database entry."),
    Column("domain_name", Text, nullable=True, comment="The domain name defined by the external database."),
    Column("segment_id", Integer, nullable=True, comment="The segment identifier defined by the external database."),
    Column("instance_id", Integer, nullable=True, comment="The instance identifier defined by the external database."),
    Column("seq_id_start", Integer, nullable=True, comment="The sequence position in the entity or biological unit described in the data block at which the segment alignment begins. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    Column("seq_id_end", Integer, nullable=True, comment="The sequence position in the entity or biological unit described in the data block at which the segment alignment ends. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    PrimaryKeyConstraint(
        "pdbid",
        "entity_id",
        "asym_id",
        "xref_db",
        "xref_db_acc",
        "segment_id",
        "instance_id",
        "seq_id_start",
        "seq_id_end",
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
    info={"keywords": ["xref_db", "domain_name"]},
)

pdbx_sifts_unp_segments = Table(
    "pdbx_sifts_unp_segments",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity_poly_seq.entity_id in the ENTITY_POLY_SEQ category."),
    Column("asym_id", Text, nullable=True, comment="This data item is a pointer to _struct_asym.id in the STRUCT_ASYM category."),
    Column("unp_acc", Text, nullable=True, comment="The UniProt accession code related to the SIFTS segment mapping."),
    Column("segment_id", Integer, nullable=True, comment="The UniProt segment defined by the external database."),
    Column("instance_id", Integer, nullable=True, comment="The UniProt instance identifier."),
    Column("unp_start", Integer, nullable=True, comment="The sequence position in the related UniProt entry at which the mapping alignment begins."),
    Column("unp_end", Integer, nullable=True, comment="The sequence position in the related UniProt entry at which the mapping alignment ends."),
    Column("seq_id_start", Integer, nullable=True, comment="The sequence position in the entity or biological unit described in the data block at which the UniProt alignment begins."),
    Column("seq_id_end", Integer, nullable=True, comment="The sequence position in the entity or biological unit described in the data block at which the UniProt alignment ends. This data item is a pointer to _entity_poly_seq.num in the ENTITY_POLY_SEQ category."),
    Column("best_mapping", Text, nullable=True, comment="This code indicates whether the SIFTS UniProt accession and residue range was the best-scoring sequence match."),
    Column("identity", Double, nullable=True, comment="The identity score reports on the sequence identity for the sequence defined by the entity start and end range compared to the sequence defined by start and end range of the related UniProt accession."),
    PrimaryKeyConstraint(
        "pdbid", "entity_id", "asym_id", "unp_acc", "segment_id", "instance_id"
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
    info={"keywords": ["unp_acc"]},
)

pdbx_initial_refinement_model = Table(
    "pdbx_initial_refinement_model",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Integer, nullable=True, comment="A unique identifier for the starting model record."),
    Column("entity_id_list", Text, nullable=True, comment="A comma separated list of entities reflecting the initial model used for refinement"),
    Column("type", Text, nullable=True, comment="This item describes the type of the initial model was generated"),
    Column("source_name", Text, nullable=True, comment="This item identifies the resource of initial model used for refinement"),
    Column("accession_code", Text, nullable=True, comment="This item identifies an accession code of the resource where the initial model is used"),
    Column("details", Text, nullable=True, comment="A description of special aspects of the initial model"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["accession_code", "details"]},
)

pdbx_modification_feature = Table(
    "pdbx_modification_feature",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="An ordinal index for this category."),
    Column("label_comp_id", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("label_asym_id", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("label_seq_id", Integer, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("label_alt_id", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("modified_residue_label_comp_id", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_comp_id in the ATOM_SITE category."),
    Column("modified_residue_label_asym_id", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_asym_id in the ATOM_SITE category."),
    Column("modified_residue_label_seq_id", Integer, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_seq_id in the ATOM_SITE category."),
    Column("modified_residue_label_alt_id", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.label_alt_id in the ATOM_SITE category."),
    Column("auth_comp_id", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("auth_asym_id", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("auth_seq_id", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the chemical component that describes the protein modification. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the protein modification group."),
    Column("modified_residue_auth_comp_id", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.auth_comp_id in the ATOM_SITE category."),
    Column("modified_residue_auth_asym_id", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.auth_asym_id in the ATOM_SITE category."),
    Column("modified_residue_auth_seq_id", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.auth_seq_id in the ATOM_SITE category."),
    Column("modified_residue_PDB_ins_code", Text, nullable=True, comment="A component of the identifier for the chemical component that is being modified. This data item is a pointer to _atom_site.pdbx_PDB_ins_code in the ATOM_SITE category."),
    Column("modified_residue_symmetry", Text, nullable=True, comment="Describes the symmetry operation that should be applied to the chemical component that is being modified."),
    Column("comp_id_linking_atom", Text, nullable=True, comment="The atom on the modification group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs."),
    Column("modified_residue_id_linking_atom", Text, nullable=True, comment="The atom on the polypeptide residue group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs."),
    Column("modified_residue_id", Text, nullable=True, comment="Chemical component identifier for the amino acid residue that is being modified."),
    Column("ref_pcm_id", Integer, nullable=True, comment="A component of the identifier for the unique kind of protein modification. This data item is a pointer to _pdbx_chem_comp_pcm.pcm_id in the CHEM_COMP_PCM category."),
    Column("ref_comp_id", Text, nullable=True, comment="A component of the identifier for the unique kind of protein modification. This data item is a pointer to _pdbx_chem_comp_pcm.comp_id in the CHEM_COMP_PCM category."),
    Column("type", Text, nullable=True, comment="The type of protein modification."),
    Column("category", Text, nullable=True, comment="The category of protein modification."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

citation_pdbmlplus = Table(
    "citation_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("journal_abbrev", Text, nullable=True),
    Column("journal_volume", Text, nullable=True),
    Column("page_first", Text, nullable=True),
    Column("page_last", Text, nullable=True),
    Column("pdbx_database_id_DOI", Text, nullable=True),
    Column("pdbx_database_id_PubMed", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("year", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "id",
            "auth_validate",
            "journal_abbrev",
            "journal_volume",
            "page_first",
            "page_last",
            "pdbx_database_id_DOI",
            "pdbx_database_id_PubMed",
            "title",
        ]
    },
)

exptl_crystal_grow_comp_pdbmlplus = Table(
    "exptl_crystal_grow_comp_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("chemical_formula", Text, nullable=True),
    Column("common_name", Text, nullable=True),
    Column("conc", Text, nullable=True),
    Column("conc_unit", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("sol_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "crystal_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "crystal_id",
            "id",
            "auth_validate",
            "chemical_formula",
            "common_name",
            "conc",
            "conc_unit",
            "details",
            "sol_id",
        ]
    },
)

exptl_crystal_grow_pdbmlplus = Table(
    "exptl_crystal_grow_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("crystal_id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("pH", Double, nullable=True),
    Column("pH_range_high", Double, nullable=True),
    Column("pH_range_low", Double, nullable=True),
    Column("pdbx_details", Text, nullable=True),
    Column("temp", Text, nullable=True),
    Column("temp_unit", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "crystal_id",
            "auth_validate",
            "method",
            "pdbx_details",
            "temp",
            "temp_unit",
        ]
    },
)

refine_pdbmlplus = Table(
    "refine_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("B_iso_mean", Double, nullable=True),
    Column("ls_R_factor_R_free", Double, nullable=True),
    Column("ls_R_factor_R_work", Double, nullable=True),
    Column("ls_R_factor_all", Double, nullable=True),
    Column("ls_R_factor_obs", Double, nullable=True),
    Column("ls_d_res_high", Double, nullable=True),
    Column("ls_d_res_low", Double, nullable=True),
    Column("ls_number_reflns_R_free", Double, nullable=True),
    Column("ls_number_reflns_all", Integer, nullable=True),
    Column("ls_number_reflns_obs", Integer, nullable=True),
    Column("ls_percent_reflns_R_free", Text, nullable=True),
    Column("pdbx_ls_sigma_F", Double, nullable=True),
    Column("pdbx_ls_sigma_I", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "entry_id",
            "pdbx_refine_id",
            "auth_validate",
            "ls_percent_reflns_R_free",
        ]
    },
)

refine_ls_restr_pdbmlplus = Table(
    "refine_ls_restr_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("dev_ideal", Double, nullable=True),
    Column("dev_ideal_target", Double, nullable=True),
    Column("weight", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_refine_id", "type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "type", "auth_validate"]},
)

reflns_pdbmlplus = Table(
    "reflns_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("B_iso_Wilson_estimate", Double, nullable=True),
    Column("Rmerge_F_obs", Double, nullable=True),
    Column("d_resolution_high", Double, nullable=True),
    Column("d_resolution_low", Double, nullable=True),
    Column("number_all", Integer, nullable=True),
    Column("number_obs", Integer, nullable=True),
    Column("observed_criterion_sigma_F", Double, nullable=True),
    Column("observed_criterion_sigma_I", Double, nullable=True),
    Column("pdbx_Rmerge_I_obs", Text, nullable=True),
    Column("pdbx_number_measured_all", Integer, nullable=True),
    Column("pdbx_redundancy", Text, nullable=True),
    Column("percent_possible_obs", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["auth_validate", "pdbx_Rmerge_I_obs", "pdbx_redundancy"]},
)

struct_ref_pdbmlplus = Table(
    "struct_ref_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("biological_source", Text, nullable=True),
    Column("cellular_location", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("pdbx_db_accession", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "id",
            "auth_validate",
            "biological_source",
            "cellular_location",
            "db_name",
            "entity_id",
            "pdbx_db_accession",
        ]
    },
)

struct_ref_seq_pdbmlplus = Table(
    "struct_ref_seq_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("align_id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("db_align_beg", Integer, nullable=True),
    Column("db_align_end", Integer, nullable=True),
    Column("pdbx_auth_seq_align_beg", Text, nullable=True),
    Column("pdbx_auth_seq_align_end", Text, nullable=True),
    Column("pdbx_db_accession", Text, nullable=True),
    Column("pdbx_strand_id", Text, nullable=True),
    Column("ref_id", Text, nullable=True),
    Column("seq_align_beg", Integer, nullable=True),
    Column("seq_align_end", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "align_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "align_id",
            "auth_validate",
            "pdbx_auth_seq_align_beg",
            "pdbx_auth_seq_align_end",
            "pdbx_db_accession",
            "pdbx_strand_id",
            "ref_id",
        ]
    },
)

struct_site_pdbmlplus = Table(
    "struct_site_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True),
    Column("info_type", Text, nullable=True),
    Column("info_subtype", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("pdbx_num_residues", Integer, nullable=True),
    Column("orig_data", Text, nullable=True),
    Column("orig_rmsd", Text, nullable=True),
    Column("orig_number_of_atom_pairs", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "id",
            "info_type",
            "info_subtype",
            "auth_validate",
            "details",
            "orig_data",
            "orig_rmsd",
        ]
    },
)

struct_site_gen_pdbmlplus = Table(
    "struct_site_gen_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True),
    Column("site_id", Text, nullable=True),
    Column("update_id", Integer, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Text, nullable=True),
    Column("beg_auth_seq_id", Text, nullable=True),
    Column("end_auth_seq_id", Text, nullable=True),
    Column("beg_label_seq_id", Text, nullable=True),
    Column("end_label_seq_id", Text, nullable=True),
    Column("beg_label_comp_id", Text, nullable=True),
    Column("end_label_comp_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "site_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "id",
            "site_id",
            "auth_validate",
            "auth_asym_id",
            "auth_seq_id",
            "details",
            "label_asym_id",
            "label_comp_id",
            "label_seq_id",
            "beg_auth_seq_id",
            "end_auth_seq_id",
            "beg_label_seq_id",
            "end_label_seq_id",
            "beg_label_comp_id",
            "end_label_comp_id",
            "ligand",
        ]
    },
)

gene_ontology_pdbmlplus = Table(
    "gene_ontology_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("update_id", Double, nullable=True),
    Column("auth_validate", Text, nullable=True),
    Column("goid", Text, nullable=True),
    Column("namespace", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("source", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "auth_asym_id", "goid"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "entry_id",
            "auth_asym_id",
            "auth_validate",
            "goid",
            "namespace",
            "name",
            "source",
        ]
    },
)

link_entry_pdbjplus = Table(
    "link_entry_pdbjplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("db_name", Text, nullable=True),
    Column("db_accession", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("pdbid", "db_name"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["db_name"]},
)

link_entity_pdbjplus = Table(
    "link_entity_pdbjplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("db_accession", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "db_name"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["db_name"]},
)

link_asym_pdbjplus = Table(
    "link_asym_pdbjplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("asym_id", Text, nullable=True),
    Column("pdb_strand_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["asym_id", "pdb_strand_id"]},
)

align_pdbjplus = Table(
    "align_pdbjplus",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("align_id", Integer, nullable=True),
    Column("beg_label_seq_id", Integer, nullable=True),
    Column("end_label_seq_id", Integer, nullable=True),
    Column("db_align_beg", Integer, nullable=True),
    Column("db_align_end", Integer, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("pdbx_db_accession", Text, nullable=True),
    PrimaryKeyConstraint(
        "pdbid",
        "asym_id",
        "db_name",
        "pdbx_db_accession",
        "align_id",
        "entity_id",
        "beg_label_seq_id",
        "end_label_seq_id",
        "db_align_beg",
        "db_align_end",
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["db_name"]},
)
