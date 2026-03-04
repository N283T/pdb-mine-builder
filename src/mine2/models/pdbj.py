"""SQLAlchemy schema definition for pdbj.

Auto-generated from schemas/pdbj.def.yml by scripts/convert_yaml_to_sa.py.
"""

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
    Column("pdbid", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("deposition_date", Date, nullable=True),
    Column("release_date", Date, nullable=True),
    Column("modification_date", Date, nullable=True),
    Column("deposit_author", ARRAY(Text), nullable=True),
    Column("citation_author", ARRAY(Text), nullable=True),
    Column("citation_title", ARRAY(Text), nullable=True),
    Column("citation_journal", ARRAY(Text), nullable=True),
    Column("citation_year", ARRAY(Integer), nullable=True),
    Column("citation_volume", ARRAY(Text), nullable=True),
    Column("citation_author_pri", ARRAY(Text), nullable=True),
    Column("citation_title_pri", Text, nullable=True),
    Column("citation_journal_pri", Text, nullable=True),
    Column("citation_year_pri", Integer, nullable=True),
    Column("citation_volume_pri", Text, nullable=True),
    Column("chain_type", ARRAY(Text), nullable=True),
    Column("chain_type_ids", ARRAY(Integer), nullable=True),
    Column("chain_number", Integer, nullable=True),
    Column("chain_length", ARRAY(Integer), nullable=True),
    Column("pdbx_descriptor", Text, nullable=True),
    Column("struct_title", Text, nullable=True),
    Column("ligand", ARRAY(Text), nullable=True),
    Column("exptl_method", ARRAY(Text), nullable=True),
    Column("exptl_method_ids", ARRAY(Integer), nullable=True),
    Column("resolution", Double, nullable=True),
    Column("biol_species", Text, nullable=True),
    Column("host_species", Text, nullable=True),
    Column("db_pubmed", ARRAY(Text), nullable=True),
    Column("db_doi", ARRAY(Text), nullable=True),
    Column("db_ec_number", ARRAY(Text), nullable=True),
    Column("db_goid", ARRAY(Text), nullable=True),
    Column("db_uniprot", ARRAY(Text), nullable=True),
    Column("db_genbank", ARRAY(Text), nullable=True),
    Column("db_embl", ARRAY(Text), nullable=True),
    Column("db_pir", ARRAY(Text), nullable=True),
    Column("db_emdb", ARRAY(Text), nullable=True),
    Column("pdb_related", ARRAY(Text), nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    Column("aaseq", Text, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("db_pfam", ARRAY(Text), nullable=True),
    Column("group_id", Text, nullable=True),
    Column("plus_fields", JSONB, nullable=True),
    PrimaryKeyConstraint("pdbid"),
)

atom_sites = Table(
    "atom_sites",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("text", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["text"]},
)

atom_type = Table(
    "atom_type",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("oxidation_number", Integer, nullable=True),
    Column("scat_Cromer_Mann_a1", Double, nullable=True),
    Column("scat_Cromer_Mann_a2", Double, nullable=True),
    Column("scat_Cromer_Mann_a3", Double, nullable=True),
    Column("scat_Cromer_Mann_a4", Double, nullable=True),
    Column("scat_Cromer_Mann_b1", Double, nullable=True),
    Column("scat_Cromer_Mann_b2", Double, nullable=True),
    Column("scat_Cromer_Mann_b3", Double, nullable=True),
    Column("scat_Cromer_Mann_b4", Double, nullable=True),
    Column("scat_Cromer_Mann_c", Double, nullable=True),
    Column("scat_dispersion_imag", Double, nullable=True),
    Column("scat_dispersion_real", Double, nullable=True),
    Column("scat_source", Text, nullable=True),
    Column("symbol", Text, nullable=True),
    Column("pdbx_scat_Cromer_Mann_a5", Double, nullable=True),
    Column("pdbx_scat_Cromer_Mann_b5", Double, nullable=True),
    Column("pdbx_scat_Cromer_Mann_a6", Double, nullable=True),
    Column("pdbx_scat_Cromer_Mann_b6", Double, nullable=True),
    Column("pdbx_scat_Z", Integer, nullable=True),
    Column("pdbx_N_electrons", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("creation_date", Date, nullable=True),
    Column("creation_method", Text, nullable=True),
    Column("revision_id", Text, nullable=True),
    Column("update_record", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "revision_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["creation_method", "update_record"]},
)

audit_author = Table(
    "audit_author",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("identifier_ORCID", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["address", "name", "identifier_ORCID"]},
)

audit_conform = Table(
    "audit_conform",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dict_location", Text, nullable=True),
    Column("dict_name", Text, nullable=True),
    Column("dict_version", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "dict_name", "dict_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)

cell = Table(
    "cell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("angle_alpha", Double, nullable=True),
    Column("angle_alpha_esd", Double, nullable=True),
    Column("angle_beta", Double, nullable=True),
    Column("angle_beta_esd", Double, nullable=True),
    Column("angle_gamma", Double, nullable=True),
    Column("angle_gamma_esd", Double, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("formula_units_Z", Integer, nullable=True),
    Column("length_a", Double, nullable=True),
    Column("length_a_esd", Double, nullable=True),
    Column("length_b", Double, nullable=True),
    Column("length_b_esd", Double, nullable=True),
    Column("length_c", Double, nullable=True),
    Column("length_c_esd", Double, nullable=True),
    Column("volume", Double, nullable=True),
    Column("volume_esd", Double, nullable=True),
    Column("Z_PDB", Integer, nullable=True),
    Column("reciprocal_angle_alpha", Double, nullable=True),
    Column("reciprocal_angle_beta", Double, nullable=True),
    Column("reciprocal_angle_gamma", Double, nullable=True),
    Column("pdbx_unique_axis", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "pdbx_unique_axis"]},
)

cell_measurement = Table(
    "cell_measurement",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("pressure", Double, nullable=True),
    Column("reflns_used", Integer, nullable=True),
    Column("theta_max", Double, nullable=True),
    Column("theta_min", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["radiation"]},
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("mon_nstd_flag", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_synonyms", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("atom_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("type_symbol", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_stereo_config", Text, nullable=True),
    Column("pdbx_aromatic_flag", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "comp_id", "atom_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
    info={"keywords": ["alt_atom_id", "pdbx_stnd_atom_id"]},
)

chem_comp_bond = Table(
    "chem_comp_bond",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_stereo_config", Text, nullable=True),
    Column("pdbx_aromatic_flag", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "comp_id", "atom_id_1", "atom_id_2"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id, atom_id_1) -> chem_comp_atom(pdbid, comp_id, atom_id)
    # FK: (pdbid, comp_id, atom_id_2) -> chem_comp_atom(pdbid, comp_id, atom_id)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
)

chem_link = Table(
    "chem_link",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

citation = Table(
    "citation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("abstract", Text, nullable=True),
    Column("book_id_ISBN", Text, nullable=True),
    Column("book_publisher", Text, nullable=True),
    Column("book_publisher_city", Text, nullable=True),
    Column("book_title", Text, nullable=True),
    Column("coordinate_linkage", Text, nullable=True),
    Column("country", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("journal_abbrev", Text, nullable=True),
    Column("journal_id_ASTM", Text, nullable=True),
    Column("journal_id_CSD", Text, nullable=True),
    Column("journal_id_ISSN", Text, nullable=True),
    Column("journal_issue", Text, nullable=True),
    Column("journal_volume", Text, nullable=True),
    Column("language", Text, nullable=True),
    Column("page_first", Text, nullable=True),
    Column("page_last", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("year", Integer, nullable=True),
    Column("database_id_CSD", Text, nullable=True),
    Column("pdbx_database_id_DOI", Text, nullable=True),
    Column("pdbx_database_id_PubMed", Integer, nullable=True),
    Column("pdbx_database_id_patent", Text, nullable=True),
    Column("unpublished_flag", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("citation_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("identifier_ORCID", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "citation_id", "name", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, citation_id) -> citation(pdbid, id)
    info={"keywords": ["name", "identifier_ORCID"]},
)

citation_editor = Table(
    "citation_editor",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("citation_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "citation_id", "name"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, citation_id) -> citation(pdbid, id)
    info={"keywords": ["name"]},
)

database_2 = Table(
    "database_2",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("database_id", Text, nullable=True),
    Column("database_code", Text, nullable=True),
    Column("pdbx_database_accession", Text, nullable=True),
    Column("pdbx_DOI", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "database_id", "database_code"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["database_code", "pdbx_DOI"]},
)

database_PDB_caveat = Table(
    "database_PDB_caveat",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("text", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["text"]},
)

database_PDB_matrix = Table(
    "database_PDB_matrix",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("ambient_environment", Text, nullable=True),
    Column("ambient_temp", Double, nullable=True),
    Column("ambient_temp_details", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("crystal_support", Text, nullable=True),
    Column("crystal_treatment", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ambient_pressure", Double, nullable=True),
    Column("pdbx_serial_crystal_experiment", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("detector", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_collection_date", Text, nullable=True),
    Column("pdbx_frequency", Double, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["details", "detector", "type"]},
)

diffrn_measurement = Table(
    "diffrn_measurement",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("specimen_support", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("collimation", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("monochromator", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("wavelength_id", Text, nullable=True),
    Column("pdbx_monochromatic_or_laue_m_l", Text, nullable=True),
    Column("pdbx_wavelength_list", Text, nullable=True),
    Column("pdbx_wavelength", Text, nullable=True),
    Column("pdbx_diffrn_protocol", Text, nullable=True),
    Column("pdbx_analyzer", Text, nullable=True),
    Column("pdbx_scattering_type", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("wavelength", Double, nullable=True),
    Column("wt", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

diffrn_reflns = Table(
    "diffrn_reflns",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("av_R_equivalents", Double, nullable=True),
    Column("av_sigmaI_over_netI", Double, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("limit_h_max", Integer, nullable=True),
    Column("limit_h_min", Integer, nullable=True),
    Column("limit_k_max", Integer, nullable=True),
    Column("limit_k_min", Integer, nullable=True),
    Column("limit_l_max", Integer, nullable=True),
    Column("limit_l_min", Integer, nullable=True),
    Column("number", Integer, nullable=True),
    Column("theta_max", Double, nullable=True),
    Column("theta_min", Double, nullable=True),
    Column("pdbx_d_res_low", Double, nullable=True),
    Column("pdbx_d_res_high", Double, nullable=True),
    Column("pdbx_percent_possible_obs", Double, nullable=True),
    Column("pdbx_Rmerge_I_obs", Double, nullable=True),
    Column("pdbx_Rsym_value", Double, nullable=True),
    Column("pdbx_chi_squared", Double, nullable=True),
    Column("pdbx_redundancy", Double, nullable=True),
    Column("pdbx_rejects", Integer, nullable=True),
    Column("pdbx_number_obs", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["reduction_process"]},
)

diffrn_source = Table(
    "diffrn_source",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("current", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("power", Double, nullable=True),
    Column("size", Text, nullable=True),
    Column("source", Text, nullable=True),
    Column("target", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("voltage", Double, nullable=True),
    Column("take-off_angle", Double, nullable=True),
    Column("pdbx_wavelength_list", Text, nullable=True),
    Column("pdbx_wavelength", Text, nullable=True),
    Column("pdbx_synchrotron_beamline", Text, nullable=True),
    Column("pdbx_synchrotron_site", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("src_method", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_description", Text, nullable=True),
    Column("pdbx_number_of_molecules", Integer, nullable=True),
    Column("pdbx_mutation", Text, nullable=True),
    Column("pdbx_fragment", Text, nullable=True),
    Column("pdbx_ec", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("text", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["name"]},
)

entity_name_sys = Table(
    "entity_name_sys",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["name", "system"]},
)

entity_poly = Table(
    "entity_poly",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("nstd_linkage", Text, nullable=True),
    Column("nstd_monomer", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_strand_id", Text, nullable=True),
    Column("pdbx_seq_one_letter_code", Text, nullable=True),
    Column("pdbx_seq_one_letter_code_can", Text, nullable=True),
    Column("pdbx_target_identifier", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("hetero", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("num", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "num", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, mon_id) -> chem_comp(pdbid, id)
    # FK: (pdbid, entity_id) -> entity_poly(pdbid, entity_id)
)

entry = Table(
    "entry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

exptl = Table(
    "exptl",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("absorpt_correction_T_max", Double, nullable=True),
    Column("absorpt_correction_T_min", Double, nullable=True),
    Column("absorpt_correction_type", Text, nullable=True),
    Column("absorpt_process_details", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("crystals_number", Integer, nullable=True),
    Column("details", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("method_details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id", "method"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["absorpt_process_details", "details", "method_details"]},
)

exptl_crystal = Table(
    "exptl_crystal",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("colour", Text, nullable=True),
    Column("density_Matthews", Double, nullable=True),
    Column("density_percent_sol", Double, nullable=True),
    Column("description", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("preparation", Text, nullable=True),
    Column("density_meas", Double, nullable=True),
    Column("pdbx_mosaicity", Double, nullable=True),
    Column("pdbx_mosaicity_esd", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("pH", Double, nullable=True),
    Column("pressure", Double, nullable=True),
    Column("seeding", Text, nullable=True),
    Column("temp_details", Text, nullable=True),
    Column("time", Text, nullable=True),
    Column("pdbx_details", Text, nullable=True),
    Column("pdbx_pH_range", Text, nullable=True),
    Column("temp", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("conc", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("sol_id", Text, nullable=True),
    Column("volume", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("method", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "method"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

phasing_MAD = Table(
    "phasing_MAD",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("pdbx_d_res_low", Double, nullable=True),
    Column("pdbx_d_res_high", Double, nullable=True),
    Column("pdbx_reflns_acentric", Integer, nullable=True),
    Column("pdbx_reflns_centric", Integer, nullable=True),
    Column("pdbx_reflns", Integer, nullable=True),
    Column("pdbx_fom_acentric", Double, nullable=True),
    Column("pdbx_fom_centric", Double, nullable=True),
    Column("pdbx_fom", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "method", "pdbx_anom_scat_method"]},
)

phasing_MAD_clust = Table(
    "phasing_MAD_clust",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("expt_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "expt_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, expt_id) -> phasing_MAD_expt(pdbid, id)
    info={"keywords": ["expt_id", "id"]},
)

phasing_MAD_expt = Table(
    "phasing_MAD_expt",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("mean_fom", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["id"]},
)

phasing_MAD_set = Table(
    "phasing_MAD_set",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("clust_id", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("expt_id", Text, nullable=True),
    Column("f_double_prime", Double, nullable=True),
    Column("f_prime", Double, nullable=True),
    Column("set_id", Text, nullable=True),
    Column("wavelength", Double, nullable=True),
    Column("pdbx_atom_type", Text, nullable=True),
    Column("pdbx_f_prime_refined", Double, nullable=True),
    Column("pdbx_f_double_prime_refined", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "expt_id", "clust_id", "set_id", "wavelength"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, expt_id) -> phasing_MAD_expt(pdbid, id)
    # FK: (pdbid, set_id) -> phasing_set(pdbid, id)
    info={"keywords": ["clust_id", "expt_id", "set_id", "wavelength_details"]},
)

phasing_MIR = Table(
    "phasing_MIR",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("FOM", Double, nullable=True),
    Column("FOM_acentric", Double, nullable=True),
    Column("FOM_centric", Double, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns_criterion", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "method", "reflns_criterion"]},
)

phasing_MIR_der = Table(
    "phasing_MIR_der",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("der_set_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("native_set_id", Text, nullable=True),
    Column("number_of_sites", Integer, nullable=True),
    Column("power_acentric", Double, nullable=True),
    Column("power_centric", Double, nullable=True),
    Column("R_cullis_acentric", Double, nullable=True),
    Column("R_cullis_anomalous", Double, nullable=True),
    Column("R_cullis_centric", Double, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_anomalous", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns_criteria", Text, nullable=True),
    Column("pdbx_loc_centric", Double, nullable=True),
    Column("pdbx_loc_acentric", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("der_id", Text, nullable=True),
    Column("pdbx_R_cullis_centric", Double, nullable=True),
    Column("pdbx_R_cullis_acentric", Double, nullable=True),
    Column("pdbx_loc_centric", Double, nullable=True),
    Column("pdbx_loc_acentric", Double, nullable=True),
    Column("pdbx_power_centric", Double, nullable=True),
    Column("pdbx_power_acentric", Double, nullable=True),
    Column("pdbx_reflns_centric", Double, nullable=True),
    Column("pdbx_reflns_acentric", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "der_id", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, der_id) -> phasing_MIR_der(pdbid, id)
    info={"keywords": ["der_id"]},
)

phasing_MIR_der_site = Table(
    "phasing_MIR_der_site",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("atom_type_symbol", Text, nullable=True),
    Column("B_iso", Double, nullable=True),
    Column("Cartn_x", Double, nullable=True),
    Column("Cartn_y", Double, nullable=True),
    Column("Cartn_z", Double, nullable=True),
    Column("der_id", Text, nullable=True),
    Column("fract_x", Double, nullable=True),
    Column("fract_y", Double, nullable=True),
    Column("fract_z", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("occupancy", Double, nullable=True),
    Column("occupancy_anom", Double, nullable=True),
    Column("occupancy_anom_su", Double, nullable=True),
    Column("occupancy_iso", Double, nullable=True),
    Column("occupancy_iso_su", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "der_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, der_id) -> phasing_MIR_der(pdbid, id)
    info={"keywords": ["der_id", "details"]},
)

phasing_MIR_shell = Table(
    "phasing_MIR_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("FOM", Double, nullable=True),
    Column("FOM_acentric", Double, nullable=True),
    Column("FOM_centric", Double, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

phasing_set = Table(
    "phasing_set",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("cell_angle_alpha", Double, nullable=True),
    Column("cell_angle_beta", Double, nullable=True),
    Column("cell_angle_gamma", Double, nullable=True),
    Column("cell_length_a", Double, nullable=True),
    Column("cell_length_b", Double, nullable=True),
    Column("cell_length_c", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_d_res_high", Double, nullable=True),
    Column("pdbx_d_res_low", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("section_references", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("aniso_B11", Double, nullable=True),
    Column("aniso_B12", Double, nullable=True),
    Column("aniso_B13", Double, nullable=True),
    Column("aniso_B22", Double, nullable=True),
    Column("aniso_B23", Double, nullable=True),
    Column("aniso_B33", Double, nullable=True),
    Column("B_iso_max", Double, nullable=True),
    Column("B_iso_mean", Double, nullable=True),
    Column("B_iso_min", Double, nullable=True),
    Column("correlation_coeff_Fo_to_Fc", Double, nullable=True),
    Column("correlation_coeff_Fo_to_Fc_free", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("ls_d_res_high", Double, nullable=True),
    Column("ls_d_res_low", Double, nullable=True),
    Column("ls_extinction_coef_esd", Double, nullable=True),
    Column("ls_goodness_of_fit_all", Double, nullable=True),
    Column("ls_hydrogen_treatment", Text, nullable=True),
    Column("ls_matrix_type", Text, nullable=True),
    Column("ls_number_constraints", Integer, nullable=True),
    Column("ls_number_parameters", Integer, nullable=True),
    Column("ls_number_reflns_all", Integer, nullable=True),
    Column("ls_number_reflns_obs", Integer, nullable=True),
    Column("ls_number_reflns_R_free", Integer, nullable=True),
    Column("ls_number_reflns_R_work", Integer, nullable=True),
    Column("ls_number_restraints", Integer, nullable=True),
    Column("ls_percent_reflns_obs", Double, nullable=True),
    Column("ls_percent_reflns_R_free", Double, nullable=True),
    Column("ls_R_factor_all", Double, nullable=True),
    Column("ls_R_factor_obs", Double, nullable=True),
    Column("ls_R_factor_R_free", Double, nullable=True),
    Column("ls_R_factor_R_free_error", Double, nullable=True),
    Column("ls_R_factor_R_free_error_details", Text, nullable=True),
    Column("ls_R_factor_R_work", Double, nullable=True),
    Column("ls_redundancy_reflns_all", Double, nullable=True),
    Column("ls_redundancy_reflns_obs", Double, nullable=True),
    Column("ls_wR_factor_all", Double, nullable=True),
    Column("ls_wR_factor_R_free", Double, nullable=True),
    Column("ls_wR_factor_R_work", Double, nullable=True),
    Column("occupancy_max", Double, nullable=True),
    Column("occupancy_min", Double, nullable=True),
    Column("solvent_model_details", Text, nullable=True),
    Column("solvent_model_param_bsol", Double, nullable=True),
    Column("solvent_model_param_ksol", Double, nullable=True),
    Column("pdbx_ls_sigma_I", Double, nullable=True),
    Column("pdbx_ls_sigma_F", Double, nullable=True),
    Column("pdbx_ls_sigma_Fsqd", Double, nullable=True),
    Column("pdbx_data_cutoff_high_absF", Double, nullable=True),
    Column("pdbx_data_cutoff_high_rms_absF", Double, nullable=True),
    Column("pdbx_data_cutoff_low_absF", Double, nullable=True),
    Column("pdbx_isotropic_thermal_model", Text, nullable=True),
    Column("pdbx_ls_cross_valid_method", Text, nullable=True),
    Column("pdbx_method_to_determine_struct", Text, nullable=True),
    Column("pdbx_starting_model", Text, nullable=True),
    Column("pdbx_stereochemistry_target_values", Text, nullable=True),
    Column("pdbx_R_Free_selection_details", Text, nullable=True),
    Column("pdbx_stereochem_target_val_spec_case", Text, nullable=True),
    Column("pdbx_overall_ESU_R", Double, nullable=True),
    Column("pdbx_overall_ESU_R_Free", Double, nullable=True),
    Column("pdbx_solvent_vdw_probe_radii", Double, nullable=True),
    Column("pdbx_solvent_ion_probe_radii", Double, nullable=True),
    Column("pdbx_solvent_shrinkage_radii", Double, nullable=True),
    Column("pdbx_pd_number_of_powder_patterns", Integer, nullable=True),
    Column("pdbx_pd_number_of_points", Integer, nullable=True),
    Column("pdbx_pd_Marquardt_correlation_coeff", Double, nullable=True),
    Column("pdbx_pd_ls_matrix_band_width", Integer, nullable=True),
    Column("pdbx_overall_phase_error", Double, nullable=True),
    Column("pdbx_overall_SU_R_free_Cruickshank_DPI", Double, nullable=True),
    Column("pdbx_overall_SU_R_free_Blow_DPI", Double, nullable=True),
    Column("pdbx_overall_SU_R_Blow_DPI", Double, nullable=True),
    Column("pdbx_TLS_residual_ADP_flag", Text, nullable=True),
    Column("pdbx_diffrn_id", Text, nullable=True),
    Column("overall_SU_B", Double, nullable=True),
    Column("overall_SU_ML", Double, nullable=True),
    Column("overall_SU_R_Cruickshank_DPI", Double, nullable=True),
    Column("overall_SU_R_free", Double, nullable=True),
    Column("overall_FOM_free_R_set", Double, nullable=True),
    Column("overall_FOM_work_R_set", Double, nullable=True),
    Column("pdbx_average_fsc_overall", Double, nullable=True),
    Column("pdbx_average_fsc_work", Double, nullable=True),
    Column("pdbx_average_fsc_free", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("Luzzati_coordinate_error_free", Double, nullable=True),
    Column("Luzzati_coordinate_error_obs", Double, nullable=True),
    Column("Luzzati_d_res_low_free", Double, nullable=True),
    Column("Luzzati_d_res_low_obs", Double, nullable=True),
    Column("Luzzati_sigma_a_free", Double, nullable=True),
    Column("Luzzati_sigma_a_obs", Double, nullable=True),
    Column("number_disordered_residues", Double, nullable=True),
    Column("occupancy_sum_hydrogen", Double, nullable=True),
    Column("occupancy_sum_non_hydrogen", Double, nullable=True),
    Column("pdbx_Luzzati_d_res_high_obs", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("class", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("treatment", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "class", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "class", "details"]},
)

refine_funct_minimized = Table(
    "refine_funct_minimized",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "type", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "type"]},
)

refine_hist = Table(
    "refine_hist",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("cycle_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("number_atoms_solvent", Integer, nullable=True),
    Column("number_atoms_total", Integer, nullable=True),
    Column("pdbx_number_residues_total", Integer, nullable=True),
    Column("pdbx_B_iso_mean_ligand", Double, nullable=True),
    Column("pdbx_B_iso_mean_solvent", Double, nullable=True),
    Column("pdbx_number_atoms_protein", Integer, nullable=True),
    Column("pdbx_number_atoms_nucleic_acid", Integer, nullable=True),
    Column("pdbx_number_atoms_ligand", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "cycle_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "details", "pdbx_pseudo_atom_details"]},
)

refine_ls_restr = Table(
    "refine_ls_restr",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("dev_ideal", Double, nullable=True),
    Column("dev_ideal_target", Double, nullable=True),
    Column("number", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("weight", Double, nullable=True),
    Column("pdbx_restraint_function", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "type", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": ["pdbx_refine_id", "criterion", "type", "pdbx_restraint_function"]
    },
)

refine_ls_restr_ncs = Table(
    "refine_ls_restr_ncs",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("dom_id", Text, nullable=True),
    Column("ncs_model_details", Text, nullable=True),
    Column("rms_dev_B_iso", Double, nullable=True),
    Column("rms_dev_position", Double, nullable=True),
    Column("weight_B_iso", Double, nullable=True),
    Column("weight_position", Double, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_type", Text, nullable=True),
    Column("pdbx_asym_id", Text, nullable=True),
    Column("pdbx_auth_asym_id", Text, nullable=True),
    Column("pdbx_number", Integer, nullable=True),
    Column("pdbx_rms", Double, nullable=True),
    Column("pdbx_weight", Double, nullable=True),
    Column("pdbx_ens_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "ncs_model_details", "pdbx_type"]},
)

refine_ls_shell = Table(
    "refine_ls_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("number_reflns_all", Integer, nullable=True),
    Column("number_reflns_obs", Integer, nullable=True),
    Column("number_reflns_R_free", Integer, nullable=True),
    Column("number_reflns_R_work", Integer, nullable=True),
    Column("percent_reflns_obs", Double, nullable=True),
    Column("percent_reflns_R_free", Double, nullable=True),
    Column("R_factor_all", Double, nullable=True),
    Column("R_factor_obs", Double, nullable=True),
    Column("R_factor_R_free_error", Double, nullable=True),
    Column("R_factor_R_work", Double, nullable=True),
    Column("redundancy_reflns_all", Double, nullable=True),
    Column("redundancy_reflns_obs", Double, nullable=True),
    Column("wR_factor_R_work", Double, nullable=True),
    Column("pdbx_R_complete", Double, nullable=True),
    Column("correlation_coeff_Fo_to_Fc", Double, nullable=True),
    Column("correlation_coeff_Fo_to_Fc_free", Double, nullable=True),
    Column("pdbx_total_number_of_bins_used", Integer, nullable=True),
    Column("pdbx_phase_error", Double, nullable=True),
    Column("pdbx_fsc_work", Double, nullable=True),
    Column("pdbx_fsc_free", Double, nullable=True),
    Column("R_factor_R_free", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "d_res_high", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id"]},
)

refine_occupancy = Table(
    "refine_occupancy",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("class", Text, nullable=True),
    Column("treatment", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "class", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "class", "details"]},
)

refln_sys_abs = Table(
    "refln_sys_abs",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("I", Double, nullable=True),
    Column("I_over_sigmaI", Double, nullable=True),
    Column("index_h", Integer, nullable=True),
    Column("index_k", Integer, nullable=True),
    Column("index_l", Integer, nullable=True),
    Column("sigmaI", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "index_h", "index_k", "index_l"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

reflns = Table(
    "reflns",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("B_iso_Wilson_estimate", Double, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("data_reduction_details", Text, nullable=True),
    Column("data_reduction_method", Text, nullable=True),
    Column("d_resolution_high", Double, nullable=True),
    Column("d_resolution_low", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("limit_h_max", Integer, nullable=True),
    Column("limit_h_min", Integer, nullable=True),
    Column("limit_k_max", Integer, nullable=True),
    Column("limit_k_min", Integer, nullable=True),
    Column("limit_l_max", Integer, nullable=True),
    Column("limit_l_min", Integer, nullable=True),
    Column("number_all", Integer, nullable=True),
    Column("number_obs", Integer, nullable=True),
    Column("observed_criterion_F_max", Double, nullable=True),
    Column("observed_criterion_F_min", Double, nullable=True),
    Column("observed_criterion_I_max", Double, nullable=True),
    Column("observed_criterion_I_min", Double, nullable=True),
    Column("observed_criterion_sigma_F", Double, nullable=True),
    Column("observed_criterion_sigma_I", Double, nullable=True),
    Column("percent_possible_obs", Double, nullable=True),
    Column("R_free_details", Text, nullable=True),
    Column("Rmerge_F_all", Double, nullable=True),
    Column("Rmerge_F_obs", Double, nullable=True),
    Column("pdbx_redundancy", Double, nullable=True),
    Column("pdbx_netI_over_av_sigmaI", Double, nullable=True),
    Column("pdbx_netI_over_sigmaI", Double, nullable=True),
    Column("pdbx_chi_squared", Double, nullable=True),
    Column("pdbx_scaling_rejects", Integer, nullable=True),
    Column("phase_calculation_details", Text, nullable=True),
    Column("pdbx_Rrim_I_all", Double, nullable=True),
    Column("pdbx_Rpim_I_all", Double, nullable=True),
    Column("pdbx_number_measured_all", Integer, nullable=True),
    Column("pdbx_diffrn_id", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_CC_half", Double, nullable=True),
    Column("pdbx_CC_star", Double, nullable=True),
    Column("pdbx_R_split", Double, nullable=True),
    Column("pdbx_Rmerge_I_obs", Double, nullable=True),
    Column("pdbx_Rmerge_I_all", Double, nullable=True),
    Column("pdbx_Rsym_value", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_1_ortho1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_1_ortho2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_1_ortho3", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_2_ortho1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_2_ortho2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_2_ortho3", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_3_ortho1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_3_ortho2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_axis_3_ortho3", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_1", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_2", Double, nullable=True),
    Column("pdbx_aniso_diffraction_limit_3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_1_ortho1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_1_ortho2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_1_ortho3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_2_ortho1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_2_ortho2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_2_ortho3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_3_ortho1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_3_ortho2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvector_3_ortho3", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvalue_1", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvalue_2", Double, nullable=True),
    Column("pdbx_aniso_B_tensor_eigenvalue_3", Double, nullable=True),
    Column("pdbx_orthogonalization_convention", Text, nullable=True),
    Column("pdbx_percent_possible_ellipsoidal", Double, nullable=True),
    Column("pdbx_percent_possible_spherical", Double, nullable=True),
    Column("pdbx_percent_possible_ellipsoidal_anomalous", Double, nullable=True),
    Column("pdbx_percent_possible_spherical_anomalous", Double, nullable=True),
    Column("pdbx_redundancy_anomalous", Double, nullable=True),
    Column("pdbx_CC_half_anomalous", Double, nullable=True),
    Column("pdbx_absDiff_over_sigma_anomalous", Double, nullable=True),
    Column("pdbx_percent_possible_anomalous", Double, nullable=True),
    Column("pdbx_observed_signal_threshold", Double, nullable=True),
    Column("pdbx_signal_type", Text, nullable=True),
    Column("pdbx_signal_details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("group_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "group_code"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["group_code"]},
)

reflns_shell = Table(
    "reflns_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("meanI_over_sigI_all", Double, nullable=True),
    Column("meanI_over_sigI_obs", Double, nullable=True),
    Column("number_measured_all", Integer, nullable=True),
    Column("number_measured_obs", Integer, nullable=True),
    Column("number_possible", Integer, nullable=True),
    Column("number_unique_all", Integer, nullable=True),
    Column("number_unique_obs", Integer, nullable=True),
    Column("percent_possible_obs", Double, nullable=True),
    Column("Rmerge_F_all", Double, nullable=True),
    Column("Rmerge_F_obs", Double, nullable=True),
    Column("meanI_over_uI_all", Double, nullable=True),
    Column("percent_possible_gt", Double, nullable=True),
    Column("pdbx_redundancy", Double, nullable=True),
    Column("pdbx_chi_squared", Double, nullable=True),
    Column("pdbx_netI_over_sigmaI_all", Double, nullable=True),
    Column("pdbx_netI_over_sigmaI_obs", Double, nullable=True),
    Column("pdbx_Rrim_I_all", Double, nullable=True),
    Column("pdbx_Rpim_I_all", Double, nullable=True),
    Column("pdbx_rejects", Integer, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_diffrn_id", Text, nullable=True),
    Column("pdbx_CC_half", Double, nullable=True),
    Column("pdbx_CC_star", Double, nullable=True),
    Column("pdbx_R_split", Double, nullable=True),
    Column("percent_possible_all", Double, nullable=True),
    Column("Rmerge_I_all", Double, nullable=True),
    Column("Rmerge_I_obs", Double, nullable=True),
    Column("pdbx_Rsym_value", Double, nullable=True),
    Column("pdbx_percent_possible_ellipsoidal", Double, nullable=True),
    Column("pdbx_percent_possible_spherical", Double, nullable=True),
    Column("pdbx_percent_possible_ellipsoidal_anomalous", Double, nullable=True),
    Column("pdbx_percent_possible_spherical_anomalous", Double, nullable=True),
    Column("pdbx_redundancy_anomalous", Double, nullable=True),
    Column("pdbx_CC_half_anomalous", Double, nullable=True),
    Column("pdbx_absDiff_over_sigma_anomalous", Double, nullable=True),
    Column("pdbx_percent_possible_anomalous", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

software = Table(
    "software",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("classification", Text, nullable=True),
    Column("compiler_version", Text, nullable=True),
    Column("contact_author", Text, nullable=True),
    Column("contact_author_email", Text, nullable=True),
    Column("date", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("language", Text, nullable=True),
    Column("location", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("os", Text, nullable=True),
    Column("os_version", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("version", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("pdbx_model_details", Text, nullable=True),
    Column("pdbx_model_type_details", Text, nullable=True),
    Column("pdbx_CASP_flag", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_modified", Text, nullable=True),
    Column("pdbx_blank_PDB_chainid_flag", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_parent_biol_id", Text, nullable=True),
    Column("pdbx_formula_weight_method", Text, nullable=True),
    Column("pdbx_aggregation_state", Text, nullable=True),
    Column("pdbx_assembly_method", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("biol_id", Text, nullable=True),
    Column("text", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "biol_id", "text"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, biol_id) -> struct_biol(pdbid, id)
    info={"keywords": ["biol_id", "text"]},
)

struct_conf = Table(
    "struct_conf",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("beg_label_asym_id", Text, nullable=True),
    Column("beg_label_comp_id", Text, nullable=True),
    Column("beg_label_seq_id", Integer, nullable=True),
    Column("beg_auth_asym_id", Text, nullable=True),
    Column("beg_auth_comp_id", Text, nullable=True),
    Column("beg_auth_seq_id", Text, nullable=True),
    Column("conf_type_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("end_label_asym_id", Text, nullable=True),
    Column("end_label_comp_id", Text, nullable=True),
    Column("end_label_seq_id", Integer, nullable=True),
    Column("end_auth_asym_id", Text, nullable=True),
    Column("end_auth_comp_id", Text, nullable=True),
    Column("end_auth_seq_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_beg_PDB_ins_code", Text, nullable=True),
    Column("pdbx_end_PDB_ins_code", Text, nullable=True),
    Column("pdbx_PDB_helix_class", Text, nullable=True),
    Column("pdbx_PDB_helix_length", Integer, nullable=True),
    Column("pdbx_PDB_helix_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, conf_type_id) -> struct_conf_type(pdbid, id)
    info={"keywords": ["details", "pdbx_PDB_helix_class"]},
)

struct_conf_type = Table(
    "struct_conf_type",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["criteria", "reference"]},
)

struct_conn = Table(
    "struct_conn",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("conn_type_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ptnr1_label_asym_id", Text, nullable=True),
    Column("ptnr1_label_atom_id", Text, nullable=True),
    Column("ptnr1_label_comp_id", Text, nullable=True),
    Column("ptnr1_label_seq_id", Integer, nullable=True),
    Column("ptnr1_auth_asym_id", Text, nullable=True),
    Column("ptnr1_auth_comp_id", Text, nullable=True),
    Column("ptnr1_auth_seq_id", Text, nullable=True),
    Column("ptnr1_symmetry", Text, nullable=True),
    Column("ptnr2_label_asym_id", Text, nullable=True),
    Column("ptnr2_label_atom_id", Text, nullable=True),
    Column("ptnr2_label_comp_id", Text, nullable=True),
    Column("ptnr2_label_seq_id", Integer, nullable=True),
    Column("ptnr2_auth_asym_id", Text, nullable=True),
    Column("ptnr2_auth_comp_id", Text, nullable=True),
    Column("ptnr2_auth_seq_id", Text, nullable=True),
    Column("ptnr2_symmetry", Text, nullable=True),
    Column("pdbx_ptnr1_PDB_ins_code", Text, nullable=True),
    Column("pdbx_ptnr1_label_alt_id", Text, nullable=True),
    Column("pdbx_ptnr2_PDB_ins_code", Text, nullable=True),
    Column("pdbx_ptnr2_label_alt_id", Text, nullable=True),
    Column("pdbx_dist_value", Double, nullable=True),
    Column("pdbx_value_order", Text, nullable=True),
    Column("pdbx_leaving_atom_flag", Text, nullable=True),
    Column("pdbx_role", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, conn_type_id) -> struct_conn_type(pdbid, id)
    info={"keywords": ["details", "pdbx_ptnr1_mod_name", "pdbx_ptnr1_sugar_name"]},
)

struct_conn_type = Table(
    "struct_conn_type",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["criteria", "reference"]},
)

struct_keywords = Table(
    "struct_keywords",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("text", Text, nullable=True),
    Column("pdbx_keywords", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["text", "pdbx_keywords", "pdbx_details"]},
)

struct_mon_prot_cis = Table(
    "struct_mon_prot_cis",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("pdbx_auth_asym_id_2", Text, nullable=True),
    Column("pdbx_auth_comp_id_2", Text, nullable=True),
    Column("pdbx_auth_seq_id_2", Text, nullable=True),
    Column("pdbx_label_asym_id_2", Text, nullable=True),
    Column("pdbx_label_comp_id_2", Text, nullable=True),
    Column("pdbx_label_seq_id_2", Integer, nullable=True),
    Column("pdbx_PDB_ins_code", Text, nullable=True),
    Column("pdbx_PDB_ins_code_2", Text, nullable=True),
    Column("pdbx_PDB_model_num", Integer, nullable=True),
    Column("pdbx_omega_angle", Text, nullable=True),
    Column("pdbx_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

struct_ncs_dom = Table(
    "struct_ncs_dom",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_ens_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "pdbx_ens_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, pdbx_ens_id) -> struct_ncs_ens(pdbid, id)
    info={"keywords": ["details"]},
)

struct_ncs_dom_lim = Table(
    "struct_ncs_dom_lim",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("beg_label_alt_id", Text, nullable=True),
    Column("beg_label_asym_id", Text, nullable=True),
    Column("beg_label_comp_id", Text, nullable=True),
    Column("beg_label_seq_id", Integer, nullable=True),
    Column("beg_auth_asym_id", Text, nullable=True),
    Column("beg_auth_comp_id", Text, nullable=True),
    Column("beg_auth_seq_id", Text, nullable=True),
    Column("dom_id", Text, nullable=True),
    Column("end_label_alt_id", Text, nullable=True),
    Column("end_label_asym_id", Text, nullable=True),
    Column("end_label_comp_id", Text, nullable=True),
    Column("end_label_seq_id", Integer, nullable=True),
    Column("end_auth_asym_id", Text, nullable=True),
    Column("end_auth_comp_id", Text, nullable=True),
    Column("end_auth_seq_id", Text, nullable=True),
    Column("selection_details", Text, nullable=True),
    Column("pdbx_component_id", Integer, nullable=True),
    Column("pdbx_refine_code", Double, nullable=True),
    Column("pdbx_ens_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "dom_id", "pdbx_ens_id", "pdbx_component_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, dom_id, pdbx_ens_id) -> struct_ncs_dom(pdbid, id, pdbx_ens_id)
    info={"keywords": ["selection_details"]},
)

struct_ncs_ens = Table(
    "struct_ncs_ens",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "point_group"]},
)

struct_ncs_ens_gen = Table(
    "struct_ncs_ens_gen",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dom_id_1", Text, nullable=True),
    Column("dom_id_2", Text, nullable=True),
    Column("ens_id", Text, nullable=True),
    Column("oper_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ens_id", "dom_id_1", "dom_id_2", "oper_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, ens_id) -> struct_ncs_ens(pdbid, id)
    # FK: (pdbid, oper_id) -> struct_ncs_oper(pdbid, id)
)

struct_ncs_oper = Table(
    "struct_ncs_oper",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("code", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_db_accession", Text, nullable=True),
    Column("pdbx_db_isoform", Text, nullable=True),
    Column("pdbx_seq_one_letter_code", Text, nullable=True),
    Column("pdbx_align_begin", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["biol_id", "db_code", "db_name", "details"]},
)

struct_ref_seq = Table(
    "struct_ref_seq",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("align_id", Text, nullable=True),
    Column("db_align_beg", Integer, nullable=True),
    Column("db_align_end", Integer, nullable=True),
    Column("ref_id", Text, nullable=True),
    Column("seq_align_beg", Integer, nullable=True),
    Column("seq_align_end", Integer, nullable=True),
    Column("pdbx_strand_id", Text, nullable=True),
    Column("pdbx_db_accession", Text, nullable=True),
    Column("pdbx_db_align_beg_ins_code", Text, nullable=True),
    Column("pdbx_db_align_end_ins_code", Text, nullable=True),
    Column("pdbx_PDB_id_code", Text, nullable=True),
    Column("pdbx_auth_seq_align_beg", Text, nullable=True),
    Column("pdbx_auth_seq_align_end", Text, nullable=True),
    Column("pdbx_seq_align_beg_ins_code", Text, nullable=True),
    Column("pdbx_seq_align_end_ins_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "align_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, ref_id) -> struct_ref(pdbid, id)
    info={"keywords": ["details"]},
)

struct_ref_seq_dif = Table(
    "struct_ref_seq_dif",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("align_id", Text, nullable=True),
    Column("db_mon_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("seq_num", Integer, nullable=True),
    Column("pdbx_pdb_id_code", Text, nullable=True),
    Column("pdbx_pdb_strand_id", Text, nullable=True),
    Column("pdbx_pdb_ins_code", Text, nullable=True),
    Column("pdbx_auth_seq_num", Text, nullable=True),
    Column("pdbx_seq_db_name", Text, nullable=True),
    Column("pdbx_seq_db_accession_code", Text, nullable=True),
    Column("pdbx_seq_db_seq_num", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, align_id) -> struct_ref_seq(pdbid, align_id)
    info={"keywords": ["details"]},
)

struct_sheet = Table(
    "struct_sheet",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("number_strands", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "type"]},
)

struct_sheet_order = Table(
    "struct_sheet_order",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("range_id_1", Text, nullable=True),
    Column("range_id_2", Text, nullable=True),
    Column("sense", Text, nullable=True),
    Column("sheet_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "sheet_id", "range_id_1", "range_id_2"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, sheet_id) -> struct_sheet(pdbid, id)
)

struct_sheet_range = Table(
    "struct_sheet_range",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("beg_label_asym_id", Text, nullable=True),
    Column("beg_label_comp_id", Text, nullable=True),
    Column("beg_label_seq_id", Integer, nullable=True),
    Column("end_label_asym_id", Text, nullable=True),
    Column("end_label_comp_id", Text, nullable=True),
    Column("end_label_seq_id", Integer, nullable=True),
    Column("beg_auth_asym_id", Text, nullable=True),
    Column("beg_auth_comp_id", Text, nullable=True),
    Column("beg_auth_seq_id", Text, nullable=True),
    Column("end_auth_asym_id", Text, nullable=True),
    Column("end_auth_comp_id", Text, nullable=True),
    Column("end_auth_seq_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("sheet_id", Text, nullable=True),
    Column("pdbx_beg_PDB_ins_code", Text, nullable=True),
    Column("pdbx_end_PDB_ins_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "sheet_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, sheet_id) -> struct_sheet(pdbid, id)
)

struct_site = Table(
    "struct_site",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_num_residues", Integer, nullable=True),
    Column("pdbx_evidence_code", Text, nullable=True),
    Column("pdbx_auth_asym_id", Text, nullable=True),
    Column("pdbx_auth_comp_id", Text, nullable=True),
    Column("pdbx_auth_seq_id", Text, nullable=True),
    Column("pdbx_auth_ins_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "id", "pdbx_evidence_code"]},
)

struct_site_gen = Table(
    "struct_site_gen",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("site_id", Text, nullable=True),
    Column("symmetry", Text, nullable=True),
    Column("pdbx_auth_ins_code", Text, nullable=True),
    Column("pdbx_num_res", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "site_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, site_id) -> struct_site(pdbid, id)
    info={"keywords": ["details", "id", "site_id"]},
)

struct_site_keywords = Table(
    "struct_site_keywords",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("site_id", Text, nullable=True),
    Column("text", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "site_id", "text"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, site_id) -> struct_site(pdbid, id)
    info={"keywords": ["site_id", "text"]},
)

symmetry = Table(
    "symmetry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("cell_setting", Text, nullable=True),
    Column("Int_Tables_number", Integer, nullable=True),
    Column("space_group_name_Hall", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pos_as_xyz", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pos_as_xyz"]},
)

space_group = Table(
    "space_group",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("crystal_system", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("IT_number", Integer, nullable=True),
    Column("name_Hall", Text, nullable=True),
    Column("name_H-M_alt", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name_Hall", "name_H-M_alt"]},
)

space_group_symop = Table(
    "space_group_symop",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("operation_xyz", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["operation_xyz"]},
)

pdbx_database_PDB_obs_spr = Table(
    "pdbx_database_PDB_obs_spr",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("date", DateTime(timezone=True), nullable=True),
    Column("pdb_id", Text, nullable=True),
    Column("replace_pdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdb_id", "replace_pdb_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["replace_pdb_id", "details"]},
)

pdbx_database_remark = Table(
    "pdbx_database_remark",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("text", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["text"]},
)

pdbx_database_status = Table(
    "pdbx_database_status",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("status_code", Text, nullable=True),
    Column("status_code_sf", Text, nullable=True),
    Column("status_code_mr", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("recvd_initial_deposition_date", Date, nullable=True),
    Column("SG_entry", Text, nullable=True),
    Column("deposit_site", Text, nullable=True),
    Column("process_site", Text, nullable=True),
    Column("status_code_cs", Text, nullable=True),
    Column("status_code_nmr_data", Text, nullable=True),
    Column("methods_development_category", Text, nullable=True),
    Column("pdb_format_compatible", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("hetero", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("pdb_strand_id", Text, nullable=True),
    Column("ndb_seq_num", Integer, nullable=True),
    Column("pdb_seq_num", Text, nullable=True),
    Column("auth_seq_num", Text, nullable=True),
    Column("pdb_mon_id", Text, nullable=True),
    Column("auth_mon_id", Text, nullable=True),
    Column("pdb_ins_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "asym_id", "entity_id", "seq_id", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id, seq_id, mon_id) -> entity_poly_seq(pdbid, entity_id, num, mon_id)
    # FK: (pdbid, asym_id, entity_id) -> struct_asym(pdbid, id, entity_id)
)

pdbx_nonpoly_scheme = Table(
    "pdbx_nonpoly_scheme",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("pdb_strand_id", Text, nullable=True),
    Column("ndb_seq_num", Text, nullable=True),
    Column("pdb_seq_num", Text, nullable=True),
    Column("auth_seq_num", Text, nullable=True),
    Column("pdb_mon_id", Text, nullable=True),
    Column("auth_mon_id", Text, nullable=True),
    Column("pdb_ins_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "asym_id", "ndb_seq_num"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_refine = Table(
    "pdbx_refine",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("R_factor_all_no_cutoff", Double, nullable=True),
    Column("R_factor_obs_no_cutoff", Double, nullable=True),
    Column("free_R_factor_4sig_cutoff", Double, nullable=True),
    Column("free_R_factor_no_cutoff", Double, nullable=True),
    Column("free_R_error_no_cutoff", Double, nullable=True),
    Column("free_R_val_test_set_size_perc_no_cutoff", Double, nullable=True),
    Column("free_R_val_test_set_ct_no_cutoff", Double, nullable=True),
    Column("number_reflns_obs_no_cutoff", Double, nullable=True),
    Column("R_factor_all_4sig_cutoff", Double, nullable=True),
    Column("R_factor_obs_4sig_cutoff", Double, nullable=True),
    Column("free_R_val_test_set_size_perc_4sig_cutoff", Double, nullable=True),
    Column("free_R_val_test_set_ct_4sig_cutoff", Double, nullable=True),
    Column("number_reflns_obs_4sig_cutoff", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["pdbx_refine_id"]},
)

pdbx_struct_sheet_hbond = Table(
    "pdbx_struct_sheet_hbond",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("range_id_1", Text, nullable=True),
    Column("range_id_2", Text, nullable=True),
    Column("sheet_id", Text, nullable=True),
    Column("range_1_label_atom_id", Text, nullable=True),
    Column("range_1_label_seq_id", Integer, nullable=True),
    Column("range_1_label_comp_id", Text, nullable=True),
    Column("range_1_label_asym_id", Text, nullable=True),
    Column("range_1_auth_atom_id", Text, nullable=True),
    Column("range_1_auth_seq_id", Text, nullable=True),
    Column("range_1_auth_comp_id", Text, nullable=True),
    Column("range_1_auth_asym_id", Text, nullable=True),
    Column("range_1_PDB_ins_code", Text, nullable=True),
    Column("range_2_label_atom_id", Text, nullable=True),
    Column("range_2_label_seq_id", Integer, nullable=True),
    Column("range_2_label_comp_id", Text, nullable=True),
    Column("range_2_label_asym_id", Text, nullable=True),
    Column("range_2_auth_atom_id", Text, nullable=True),
    Column("range_2_auth_seq_id", Text, nullable=True),
    Column("range_2_auth_comp_id", Text, nullable=True),
    Column("range_2_auth_asym_id", Text, nullable=True),
    Column("range_2_PDB_ins_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "sheet_id", "range_id_1", "range_id_2"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, sheet_id) -> struct_sheet(pdbid, id)
)

pdbx_xplor_file = Table(
    "pdbx_xplor_file",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("serial_no", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("param_file", Text, nullable=True),
    Column("topol_file", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "serial_no", "pdbx_refine_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pdbx_refine_id", "param_file", "topol_file"]},
)

pdbx_database_related = Table(
    "pdbx_database_related",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("db_id", Text, nullable=True),
    Column("content_type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "db_name", "db_id", "content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "db_id"]},
)

pdbx_exptl_crystal_grow_comp = Table(
    "pdbx_exptl_crystal_grow_comp",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("comp_name", Text, nullable=True),
    Column("sol_id", Text, nullable=True),
    Column("conc", Double, nullable=True),
    Column("conc_units", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "comp_id", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
    info={"keywords": ["comp_name", "sol_id", "conc_range"]},
)

pdbx_exptl_crystal_grow_sol = Table(
    "pdbx_exptl_crystal_grow_sol",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("sol_id", Text, nullable=True),
    Column("volume", Double, nullable=True),
    Column("volume_units", Text, nullable=True),
    Column("pH", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "sol_id", "crystal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, crystal_id) -> exptl_crystal(pdbid, id)
)

pdbx_exptl_crystal_cryo_treatment = Table(
    "pdbx_exptl_crystal_cryo_treatment",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("final_solution_details", Text, nullable=True),
    Column("soaking_details", Text, nullable=True),
    Column("cooling_details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("origin_x", Double, nullable=True),
    Column("origin_y", Double, nullable=True),
    Column("origin_z", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_refine_id", Text, nullable=True),
    Column("refine_tls_id", Text, nullable=True),
    Column("beg_label_asym_id", Text, nullable=True),
    Column("beg_label_seq_id", Integer, nullable=True),
    Column("beg_auth_asym_id", Text, nullable=True),
    Column("beg_auth_seq_id", Text, nullable=True),
    Column("beg_PDB_ins_code", Text, nullable=True),
    Column("end_label_asym_id", Text, nullable=True),
    Column("end_label_seq_id", Integer, nullable=True),
    Column("end_auth_asym_id", Text, nullable=True),
    Column("end_auth_seq_id", Text, nullable=True),
    Column("end_PDB_ins_code", Text, nullable=True),
    Column("selection", Text, nullable=True),
    Column("selection_details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, refine_tls_id) -> pdbx_refine_tls(pdbid, id)
    info={"keywords": ["pdbx_refine_id", "selection", "selection_details"]},
)

pdbx_contact_author = Table(
    "pdbx_contact_author",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("email", Text, nullable=True),
    Column("name_first", Text, nullable=True),
    Column("name_last", Text, nullable=True),
    Column("name_mi", Text, nullable=True),
    Column("role", Text, nullable=True),
    Column("identifier_ORCID", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("project_name", Text, nullable=True),
    Column("full_name_of_center", Text, nullable=True),
    Column("initial_of_center", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_nmr_details = Table(
    "pdbx_nmr_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("text", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["text"]},
)

pdbx_nmr_sample_details = Table(
    "pdbx_nmr_sample_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("solution_id", Text, nullable=True),
    Column("contents", Text, nullable=True),
    Column("solvent_system", Text, nullable=True),
    Column("label", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "solution_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["contents", "solvent_system", "label", "details"]},
)

pdbx_nmr_exptl_sample = Table(
    "pdbx_nmr_exptl_sample",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("solution_id", Text, nullable=True),
    Column("component", Text, nullable=True),
    Column("concentration", Double, nullable=True),
    Column("concentration_range", Text, nullable=True),
    Column("concentration_units", Text, nullable=True),
    Column("isotopic_labeling", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "solution_id", "component"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["component", "isotopic_labeling"]},
)

pdbx_nmr_exptl_sample_conditions = Table(
    "pdbx_nmr_exptl_sample_conditions",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("conditions_id", Text, nullable=True),
    Column("temperature", Text, nullable=True),
    Column("pressure_units", Text, nullable=True),
    Column("pressure", Text, nullable=True),
    Column("pH", Text, nullable=True),
    Column("ionic_strength", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("ionic_strength_err", Double, nullable=True),
    Column("ionic_strength_units", Text, nullable=True),
    Column("label", Text, nullable=True),
    Column("pH_err", Double, nullable=True),
    Column("pH_units", Text, nullable=True),
    Column("pressure_err", Double, nullable=True),
    Column("temperature_err", Double, nullable=True),
    Column("temperature_units", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "conditions_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["pressure", "ionic_strength", "details", "label"]},
)

pdbx_nmr_spectrometer = Table(
    "pdbx_nmr_spectrometer",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("spectrometer_id", Text, nullable=True),
    Column("model", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("manufacturer", Text, nullable=True),
    Column("field_strength", Double, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "spectrometer_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["model", "type", "manufacturer", "details", "name"]},
)

pdbx_nmr_exptl = Table(
    "pdbx_nmr_exptl",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("experiment_id", Text, nullable=True),
    Column("conditions_id", Text, nullable=True),
    Column("solution_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("spectrometer_id", Integer, nullable=True),
    Column("sample_state", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "experiment_id", "conditions_id", "solution_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["type"]},
)

pdbx_nmr_software = Table(
    "pdbx_nmr_software",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("classification", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("version", Text, nullable=True),
    Column("authors", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["classification", "name", "version", "authors", "details"]},
)

pdbx_nmr_constraints = Table(
    "pdbx_nmr_constraints",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("NOE_constraints_total", Integer, nullable=True),
    Column("NOE_intraresidue_total_count", Integer, nullable=True),
    Column("NOE_interentity_total_count", Integer, nullable=True),
    Column("NOE_sequential_total_count", Integer, nullable=True),
    Column("NOE_medium_range_total_count", Integer, nullable=True),
    Column("NOE_long_range_total_count", Integer, nullable=True),
    Column("protein_phi_angle_constraints_total_count", Integer, nullable=True),
    Column("protein_psi_angle_constraints_total_count", Integer, nullable=True),
    Column("protein_chi_angle_constraints_total_count", Integer, nullable=True),
    Column("protein_other_angle_constraints_total_count", Integer, nullable=True),
    Column("hydrogen_bond_constraints_total_count", Integer, nullable=True),
    Column("disulfide_bond_constraints_total_count", Integer, nullable=True),
    Column("NA_alpha-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_beta-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_gamma-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_delta-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_epsilon-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_chi-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_other-angle_constraints_total_count", Integer, nullable=True),
    Column("NA_sugar_pucker_constraints_total_count", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("conformers_calculated_total_number", Integer, nullable=True),
    Column("conformers_submitted_total_number", Integer, nullable=True),
    Column("conformer_selection_criteria", Text, nullable=True),
    Column("representative_conformer", Integer, nullable=True),
    Column("average_constraints_per_residue", Integer, nullable=True),
    Column("average_constraint_violations_per_residue", Integer, nullable=True),
    Column("maximum_distance_constraint_violation", Double, nullable=True),
    Column("average_distance_constraint_violation", Double, nullable=True),
    Column("maximum_upper_distance_constraint_violation", Double, nullable=True),
    Column("maximum_lower_distance_constraint_violation", Double, nullable=True),
    Column("distance_constraint_violation_method", Text, nullable=True),
    Column("maximum_torsion_angle_constraint_violation", Double, nullable=True),
    Column("average_torsion_angle_constraint_violation", Double, nullable=True),
    Column("torsion_angle_constraint_violation_method", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("residue_range_begin", Integer, nullable=True),
    Column("chain_range_begin", Text, nullable=True),
    Column("residue_range_end", Integer, nullable=True),
    Column("chain_range_end", Text, nullable=True),
    Column("atom_type", Text, nullable=True),
    Column("distance_rms_dev", Double, nullable=True),
    Column("distance_rms_dev_error", Double, nullable=True),
    Column("covalent_bond_rms_dev", Double, nullable=True),
    Column("bond_angle_rms_dev", Double, nullable=True),
    Column("improper_torsion_angle_rms_dev", Double, nullable=True),
    Column("dihedral_angles_rms_dev", Double, nullable=True),
    Column("dihedral_angles_rms_dev_error", Double, nullable=True),
    Column("coord_average_rmsd_method", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["coord_average_rmsd_method"]},
)

pdbx_nmr_representative = Table(
    "pdbx_nmr_representative",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("conformer_id", Text, nullable=True),
    Column("selection_criteria", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["conformer_id", "selection_criteria"]},
)

pdbx_nmr_refine = Table(
    "pdbx_nmr_refine",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("software_ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id", "software_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["method", "details"]},
)

ndb_struct_conf_na = Table(
    "ndb_struct_conf_na",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("feature", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id", "feature"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

ndb_struct_na_base_pair = Table(
    "ndb_struct_na_base_pair",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("model_number", Integer, nullable=True),
    Column("pair_number", Integer, nullable=True),
    Column("pair_name", Text, nullable=True),
    Column("i_label_asym_id", Text, nullable=True),
    Column("i_label_comp_id", Text, nullable=True),
    Column("i_label_seq_id", Integer, nullable=True),
    Column("i_symmetry", Text, nullable=True),
    Column("j_label_asym_id", Text, nullable=True),
    Column("j_label_comp_id", Text, nullable=True),
    Column("j_label_seq_id", Integer, nullable=True),
    Column("j_symmetry", Text, nullable=True),
    Column("i_auth_asym_id", Text, nullable=True),
    Column("i_auth_seq_id", Text, nullable=True),
    Column("i_PDB_ins_code", Text, nullable=True),
    Column("j_auth_asym_id", Text, nullable=True),
    Column("j_auth_seq_id", Text, nullable=True),
    Column("j_PDB_ins_code", Text, nullable=True),
    Column("shear", Double, nullable=True),
    Column("stretch", Double, nullable=True),
    Column("stagger", Double, nullable=True),
    Column("buckle", Double, nullable=True),
    Column("propeller", Double, nullable=True),
    Column("opening", Double, nullable=True),
    Column("hbond_type_12", Integer, nullable=True),
    Column("hbond_type_28", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("model_number", Integer, nullable=True),
    Column("step_number", Integer, nullable=True),
    Column("step_name", Text, nullable=True),
    Column("i_label_asym_id_1", Text, nullable=True),
    Column("i_label_comp_id_1", Text, nullable=True),
    Column("i_label_seq_id_1", Integer, nullable=True),
    Column("i_symmetry_1", Text, nullable=True),
    Column("j_label_asym_id_1", Text, nullable=True),
    Column("j_label_comp_id_1", Text, nullable=True),
    Column("j_label_seq_id_1", Integer, nullable=True),
    Column("j_symmetry_1", Text, nullable=True),
    Column("i_label_asym_id_2", Text, nullable=True),
    Column("i_label_comp_id_2", Text, nullable=True),
    Column("i_label_seq_id_2", Integer, nullable=True),
    Column("i_symmetry_2", Text, nullable=True),
    Column("j_label_asym_id_2", Text, nullable=True),
    Column("j_label_comp_id_2", Text, nullable=True),
    Column("j_label_seq_id_2", Integer, nullable=True),
    Column("j_symmetry_2", Text, nullable=True),
    Column("i_auth_asym_id_1", Text, nullable=True),
    Column("i_auth_seq_id_1", Text, nullable=True),
    Column("i_PDB_ins_code_1", Text, nullable=True),
    Column("j_auth_asym_id_1", Text, nullable=True),
    Column("j_auth_seq_id_1", Text, nullable=True),
    Column("j_PDB_ins_code_1", Text, nullable=True),
    Column("i_auth_asym_id_2", Text, nullable=True),
    Column("i_auth_seq_id_2", Text, nullable=True),
    Column("i_PDB_ins_code_2", Text, nullable=True),
    Column("j_auth_asym_id_2", Text, nullable=True),
    Column("j_auth_seq_id_2", Text, nullable=True),
    Column("j_PDB_ins_code_2", Text, nullable=True),
    Column("shift", Double, nullable=True),
    Column("slide", Double, nullable=True),
    Column("rise", Double, nullable=True),
    Column("tilt", Double, nullable=True),
    Column("roll", Double, nullable=True),
    Column("twist", Double, nullable=True),
    Column("x_displacement", Double, nullable=True),
    Column("y_displacement", Double, nullable=True),
    Column("helical_rise", Double, nullable=True),
    Column("inclination", Double, nullable=True),
    Column("tip", Double, nullable=True),
    Column("helical_twist", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["name"]},
)

pdbx_phasing_dm = Table(
    "pdbx_phasing_dm",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("mask_type", Text, nullable=True),
    Column("fom_acentric", Double, nullable=True),
    Column("fom_centric", Double, nullable=True),
    Column("fom", Double, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("delta_phi_initial", Double, nullable=True),
    Column("delta_phi_final", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method", "mask_type"]},
)

pdbx_phasing_dm_shell = Table(
    "pdbx_phasing_dm_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("fom_acentric", Double, nullable=True),
    Column("fom_centric", Double, nullable=True),
    Column("fom", Double, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("delta_phi_final", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_shell = Table(
    "pdbx_phasing_MAD_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("reflns_acentric", Double, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("fom_acentric", Double, nullable=True),
    Column("fom_centric", Double, nullable=True),
    Column("fom", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_set = Table(
    "pdbx_phasing_MAD_set",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("fom_acentric", Double, nullable=True),
    Column("fom_centric", Double, nullable=True),
    Column("fom", Double, nullable=True),
    Column("R_cullis_centric", Double, nullable=True),
    Column("R_cullis_acentric", Double, nullable=True),
    Column("R_cullis", Double, nullable=True),
    Column("R_kraut_centric", Double, nullable=True),
    Column("R_kraut_acentric", Double, nullable=True),
    Column("R_kraut", Double, nullable=True),
    Column("loc_centric", Double, nullable=True),
    Column("loc_acentric", Double, nullable=True),
    Column("loc", Double, nullable=True),
    Column("power_centric", Double, nullable=True),
    Column("power_acentric", Double, nullable=True),
    Column("power", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_set_shell = Table(
    "pdbx_phasing_MAD_set_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("reflns_acentric", Integer, nullable=True),
    Column("reflns_centric", Integer, nullable=True),
    Column("reflns", Integer, nullable=True),
    Column("fom_acentric", Double, nullable=True),
    Column("fom_centric", Double, nullable=True),
    Column("fom", Double, nullable=True),
    Column("R_cullis_centric", Double, nullable=True),
    Column("R_cullis_acentric", Double, nullable=True),
    Column("R_cullis", Double, nullable=True),
    Column("R_kraut_centric", Double, nullable=True),
    Column("R_kraut_acentric", Double, nullable=True),
    Column("R_kraut", Double, nullable=True),
    Column("loc_centric", Double, nullable=True),
    Column("loc_acentric", Double, nullable=True),
    Column("loc", Double, nullable=True),
    Column("power_centric", Double, nullable=True),
    Column("power_acentric", Double, nullable=True),
    Column("power", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "d_res_low", "d_res_high"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MAD_set_site = Table(
    "pdbx_phasing_MAD_set_site",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("atom_type_symbol", Text, nullable=True),
    Column("Cartn_x", Double, nullable=True),
    Column("Cartn_y", Double, nullable=True),
    Column("Cartn_z", Double, nullable=True),
    Column("fract_x", Double, nullable=True),
    Column("fract_y", Double, nullable=True),
    Column("fract_z", Double, nullable=True),
    Column("b_iso", Double, nullable=True),
    Column("occupancy", Double, nullable=True),
    Column("occupancy_iso", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_phasing_MR = Table(
    "pdbx_phasing_MR",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("method_rotation", Text, nullable=True),
    Column("d_res_high_rotation", Double, nullable=True),
    Column("d_res_low_rotation", Double, nullable=True),
    Column("sigma_F_rotation", Double, nullable=True),
    Column("reflns_percent_rotation", Double, nullable=True),
    Column("method_translation", Text, nullable=True),
    Column("d_res_high_translation", Double, nullable=True),
    Column("d_res_low_translation", Double, nullable=True),
    Column("sigma_F_translation", Double, nullable=True),
    Column("reflns_percent_translation", Double, nullable=True),
    Column("correlation_coeff_Io_to_Ic", Double, nullable=True),
    Column("correlation_coeff_Fo_to_Fc", Double, nullable=True),
    Column("R_factor", Double, nullable=True),
    Column("R_rigid_body", Double, nullable=True),
    Column("packing", Double, nullable=True),
    Column("model_details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

pdbx_buffer_components = Table(
    "pdbx_buffer_components",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("buffer_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("conc", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("conc_units", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "buffer_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, buffer_id) -> pdbx_buffer(pdbid, id)
    info={"keywords": ["name", "details", "isotopic_labeling"]},
)

pdbx_reflns_twin = Table(
    "pdbx_reflns_twin",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("crystal_id", Text, nullable=True),
    Column("domain_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("operator", Text, nullable=True),
    Column("fraction", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "crystal_id", "diffrn_id", "operator"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["operator"]},
)

pdbx_struct_assembly_prop = Table(
    "pdbx_struct_assembly_prop",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("biol_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("value", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "type", "biol_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["value", "details"]},
)

pdbx_struct_chem_comp_diagnostics = Table(
    "pdbx_struct_chem_comp_diagnostics",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdb_strand_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("seq_num", Integer, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_coordinate_model = Table(
    "pdbx_coordinate_model",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
)

pdbx_diffrn_reflns_shell = Table(
    "pdbx_diffrn_reflns_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("d_res_low", Double, nullable=True),
    Column("d_res_high", Double, nullable=True),
    Column("percent_possible_obs", Double, nullable=True),
    Column("Rmerge_I_obs", Double, nullable=True),
    Column("Rsym_value", Double, nullable=True),
    Column("chi_squared", Double, nullable=True),
    Column("redundancy", Double, nullable=True),
    Column("rejects", Integer, nullable=True),
    Column("number_obs", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "d_res_high", "d_res_low", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
)

pdbx_soln_scatter = Table(
    "pdbx_soln_scatter",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("source_beamline", Text, nullable=True),
    Column("source_beamline_instrument", Text, nullable=True),
    Column("detector_type", Text, nullable=True),
    Column("detector_specific", Text, nullable=True),
    Column("source_type", Text, nullable=True),
    Column("source_class", Text, nullable=True),
    Column("num_time_frames", Integer, nullable=True),
    Column("sample_pH", Double, nullable=True),
    Column("temperature", Double, nullable=True),
    Column("concentration_range", Text, nullable=True),
    Column("buffer_name", Text, nullable=True),
    Column("mean_guiner_radius", Double, nullable=True),
    Column("mean_guiner_radius_esd", Double, nullable=True),
    Column("min_mean_cross_sectional_radii_gyration", Double, nullable=True),
    Column("min_mean_cross_sectional_radii_gyration_esd", Double, nullable=True),
    Column("max_mean_cross_sectional_radii_gyration", Double, nullable=True),
    Column("max_mean_cross_sectional_radii_gyration_esd", Double, nullable=True),
    Column("protein_length", Text, nullable=True),
    Column("data_reduction_software_list", Text, nullable=True),
    Column("data_analysis_software_list", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("scatter_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("software_list", Text, nullable=True),
    Column("software_author_list", Text, nullable=True),
    Column("entry_fitting_list", Text, nullable=True),
    Column("num_conformers_calculated", Integer, nullable=True),
    Column("num_conformers_submitted", Integer, nullable=True),
    Column("representative_conformer", Integer, nullable=True),
    Column("conformer_selection_criteria", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("identifier", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("program", Text, nullable=True),
    Column("program_version", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "comp_id", "type", "program", "program_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
    info={"keywords": ["identifier", "program", "program_version"]},
)

pdbx_validate_close_contact = Table(
    "pdbx_validate_close_contact",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id_1", Text, nullable=True),
    Column("auth_atom_id_1", Text, nullable=True),
    Column("auth_comp_id_1", Text, nullable=True),
    Column("auth_seq_id_1", Text, nullable=True),
    Column("auth_atom_id_2", Text, nullable=True),
    Column("auth_asym_id_2", Text, nullable=True),
    Column("auth_comp_id_2", Text, nullable=True),
    Column("auth_seq_id_2", Text, nullable=True),
    Column("PDB_ins_code_1", Text, nullable=True),
    Column("PDB_ins_code_2", Text, nullable=True),
    Column("label_alt_id_1", Text, nullable=True),
    Column("label_alt_id_2", Text, nullable=True),
    Column("dist", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["symm_as_xyz_1", "symm_as_xyz_2"]},
)

pdbx_validate_symm_contact = Table(
    "pdbx_validate_symm_contact",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id_1", Text, nullable=True),
    Column("auth_atom_id_1", Text, nullable=True),
    Column("auth_comp_id_1", Text, nullable=True),
    Column("auth_seq_id_1", Text, nullable=True),
    Column("auth_atom_id_2", Text, nullable=True),
    Column("auth_asym_id_2", Text, nullable=True),
    Column("auth_comp_id_2", Text, nullable=True),
    Column("auth_seq_id_2", Text, nullable=True),
    Column("PDB_ins_code_1", Text, nullable=True),
    Column("PDB_ins_code_2", Text, nullable=True),
    Column("label_alt_id_1", Text, nullable=True),
    Column("label_alt_id_2", Text, nullable=True),
    Column("site_symmetry_1", Text, nullable=True),
    Column("site_symmetry_2", Text, nullable=True),
    Column("dist", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["site_symmetry_1", "site_symmetry_2"]},
)

pdbx_validate_rmsd_bond = Table(
    "pdbx_validate_rmsd_bond",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id_1", Text, nullable=True),
    Column("auth_atom_id_1", Text, nullable=True),
    Column("auth_comp_id_1", Text, nullable=True),
    Column("auth_seq_id_1", Text, nullable=True),
    Column("auth_atom_id_2", Text, nullable=True),
    Column("auth_asym_id_2", Text, nullable=True),
    Column("auth_comp_id_2", Text, nullable=True),
    Column("auth_seq_id_2", Text, nullable=True),
    Column("PDB_ins_code_1", Text, nullable=True),
    Column("PDB_ins_code_2", Text, nullable=True),
    Column("label_alt_id_1", Text, nullable=True),
    Column("label_alt_id_2", Text, nullable=True),
    Column("bond_deviation", Double, nullable=True),
    Column("bond_value", Double, nullable=True),
    Column("bond_target_value", Double, nullable=True),
    Column("bond_standard_deviation", Double, nullable=True),
    Column("linker_flag", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_rmsd_angle = Table(
    "pdbx_validate_rmsd_angle",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id_1", Text, nullable=True),
    Column("auth_atom_id_1", Text, nullable=True),
    Column("auth_comp_id_1", Text, nullable=True),
    Column("auth_seq_id_1", Text, nullable=True),
    Column("auth_atom_id_2", Text, nullable=True),
    Column("auth_asym_id_2", Text, nullable=True),
    Column("auth_comp_id_2", Text, nullable=True),
    Column("auth_seq_id_2", Text, nullable=True),
    Column("auth_atom_id_3", Text, nullable=True),
    Column("auth_asym_id_3", Text, nullable=True),
    Column("auth_comp_id_3", Text, nullable=True),
    Column("auth_seq_id_3", Text, nullable=True),
    Column("PDB_ins_code_1", Text, nullable=True),
    Column("PDB_ins_code_2", Text, nullable=True),
    Column("PDB_ins_code_3", Text, nullable=True),
    Column("label_alt_id_1", Text, nullable=True),
    Column("label_alt_id_2", Text, nullable=True),
    Column("label_alt_id_3", Text, nullable=True),
    Column("angle_deviation", Double, nullable=True),
    Column("angle_value", Double, nullable=True),
    Column("angle_target_value", Double, nullable=True),
    Column("angle_standard_deviation", Double, nullable=True),
    Column("linker_flag", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_torsion = Table(
    "pdbx_validate_torsion",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("phi", Double, nullable=True),
    Column("psi", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_peptide_omega = Table(
    "pdbx_validate_peptide_omega",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id_1", Text, nullable=True),
    Column("auth_asym_id_2", Text, nullable=True),
    Column("auth_comp_id_1", Text, nullable=True),
    Column("auth_comp_id_2", Text, nullable=True),
    Column("auth_seq_id_1", Text, nullable=True),
    Column("auth_seq_id_2", Text, nullable=True),
    Column("PDB_ins_code_1", Text, nullable=True),
    Column("PDB_ins_code_2", Text, nullable=True),
    Column("label_alt_id_1", Text, nullable=True),
    Column("label_alt_id_2", Text, nullable=True),
    Column("omega", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_chiral = Table(
    "pdbx_validate_chiral",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_atom_id", Text, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_validate_planes = Table(
    "pdbx_validate_planes",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("rmsd", Double, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_validate_main_chain_plane = Table(
    "pdbx_validate_main_chain_plane",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("improper_torsion_angle", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_struct_conn_angle = Table(
    "pdbx_struct_conn_angle",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ptnr1_label_alt_id", Text, nullable=True),
    Column("ptnr1_label_asym_id", Text, nullable=True),
    Column("ptnr1_label_atom_id", Text, nullable=True),
    Column("ptnr1_label_comp_id", Text, nullable=True),
    Column("ptnr1_label_seq_id", Integer, nullable=True),
    Column("ptnr1_auth_asym_id", Text, nullable=True),
    Column("ptnr1_auth_comp_id", Text, nullable=True),
    Column("ptnr1_auth_seq_id", Text, nullable=True),
    Column("ptnr1_symmetry", Text, nullable=True),
    Column("ptnr2_label_alt_id", Text, nullable=True),
    Column("ptnr2_label_asym_id", Text, nullable=True),
    Column("ptnr2_label_atom_id", Text, nullable=True),
    Column("ptnr2_label_comp_id", Text, nullable=True),
    Column("ptnr2_label_seq_id", Integer, nullable=True),
    Column("ptnr2_auth_asym_id", Text, nullable=True),
    Column("ptnr2_auth_comp_id", Text, nullable=True),
    Column("ptnr2_auth_seq_id", Text, nullable=True),
    Column("ptnr2_symmetry", Text, nullable=True),
    Column("ptnr1_PDB_ins_code", Text, nullable=True),
    Column("ptnr2_PDB_ins_code", Text, nullable=True),
    Column("ptnr3_auth_asym_id", Text, nullable=True),
    Column("ptnr3_auth_comp_id", Text, nullable=True),
    Column("ptnr3_PDB_ins_code", Text, nullable=True),
    Column("ptnr3_auth_seq_id", Text, nullable=True),
    Column("ptnr3_label_alt_id", Text, nullable=True),
    Column("ptnr3_label_asym_id", Text, nullable=True),
    Column("ptnr3_label_atom_id", Text, nullable=True),
    Column("ptnr3_label_comp_id", Text, nullable=True),
    Column("ptnr3_label_seq_id", Integer, nullable=True),
    Column("ptnr3_symmetry", Text, nullable=True),
    Column("value", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_unobs_or_zero_occ_residues = Table(
    "pdbx_unobs_or_zero_occ_residues",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("polymer_flag", Text, nullable=True),
    Column("occupancy_flag", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, auth_comp_id) -> chem_comp(pdbid, id)
)

pdbx_unobs_or_zero_occ_atoms = Table(
    "pdbx_unobs_or_zero_occ_atoms",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("polymer_flag", Text, nullable=True),
    Column("occupancy_flag", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_atom_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, auth_comp_id) -> chem_comp(pdbid, id)
)

pdbx_entry_details = Table(
    "pdbx_entry_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("nonpolymer_details", Text, nullable=True),
    Column("sequence_details", Text, nullable=True),
    Column("compound_details", Text, nullable=True),
    Column("source_details", Text, nullable=True),
    Column("has_ligand_of_interest", Text, nullable=True),
    Column("has_protein_modification", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    Column("parent_comp_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_validate_polymer_linkage = Table(
    "pdbx_validate_polymer_linkage",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id_1", Text, nullable=True),
    Column("auth_atom_id_1", Text, nullable=True),
    Column("auth_comp_id_1", Text, nullable=True),
    Column("auth_seq_id_1", Text, nullable=True),
    Column("auth_atom_id_2", Text, nullable=True),
    Column("auth_asym_id_2", Text, nullable=True),
    Column("auth_comp_id_2", Text, nullable=True),
    Column("auth_seq_id_2", Text, nullable=True),
    Column("PDB_ins_code_1", Text, nullable=True),
    Column("PDB_ins_code_2", Text, nullable=True),
    Column("label_alt_id_1", Text, nullable=True),
    Column("label_alt_id_2", Text, nullable=True),
    Column("dist", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_helical_symmetry = Table(
    "pdbx_helical_symmetry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("number_of_operations", Integer, nullable=True),
    Column("rotation_per_n_subunits", Double, nullable=True),
    Column("rise_per_n_subunits", Double, nullable=True),
    Column("n_subunits_divisor", Integer, nullable=True),
    Column("dyad_axis", Text, nullable=True),
    Column("circular_symmetry", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

pdbx_point_symmetry = Table(
    "pdbx_point_symmetry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("Schoenflies_symbol", Text, nullable=True),
    Column("circular_symmetry", Integer, nullable=True),
    Column("H-M_notation", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
)

pdbx_struct_entity_inst = Table(
    "pdbx_struct_entity_inst",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_struct_oper_list = Table(
    "pdbx_struct_oper_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("symmetry_operation", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("method_details", Text, nullable=True),
    Column("oligomeric_details", Text, nullable=True),
    Column("oligomeric_count", Integer, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_inst_id", Text, nullable=True),
    Column("msym_id", Text, nullable=True),
    Column("oper_expression", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "msym_id", "entity_inst_id", "oper_expression"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_inst_id) -> pdbx_struct_entity_inst(pdbid, id)
)

pdbx_struct_legacy_oper_list = Table(
    "pdbx_struct_legacy_oper_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("prd_id", Text, nullable=True),
    Column("instance_id", Integer, nullable=True),
    Column("asym_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "prd_id", "instance_id", "asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
)

pdbx_molecule_features = Table(
    "pdbx_molecule_features",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("prd_id", Text, nullable=True),
    Column("class", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "prd_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

pdbx_distant_solvent_atoms = Table(
    "pdbx_distant_solvent_atoms",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_atom_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("neighbor_macromolecule_distance", Double, nullable=True),
    Column("neighbor_ligand_distance", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, auth_comp_id) -> chem_comp(pdbid, id)
)

pdbx_struct_special_symmetry = Table(
    "pdbx_struct_special_symmetry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

entity_src_nat = Table(
    "entity_src_nat",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("common_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("genus", Text, nullable=True),
    Column("species", Text, nullable=True),
    Column("strain", Text, nullable=True),
    Column("tissue", Text, nullable=True),
    Column("tissue_fraction", Text, nullable=True),
    Column("pdbx_organism_scientific", Text, nullable=True),
    Column("pdbx_secretion", Text, nullable=True),
    Column("pdbx_fragment", Text, nullable=True),
    Column("pdbx_variant", Text, nullable=True),
    Column("pdbx_cell_line", Text, nullable=True),
    Column("pdbx_atcc", Text, nullable=True),
    Column("pdbx_cellular_location", Text, nullable=True),
    Column("pdbx_organ", Text, nullable=True),
    Column("pdbx_organelle", Text, nullable=True),
    Column("pdbx_cell", Text, nullable=True),
    Column("pdbx_plasmid_name", Text, nullable=True),
    Column("pdbx_plasmid_details", Text, nullable=True),
    Column("pdbx_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
    Column("pdbx_beg_seq_num", Integer, nullable=True),
    Column("pdbx_end_seq_num", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("gene_src_common_name", Text, nullable=True),
    Column("gene_src_details", Text, nullable=True),
    Column("gene_src_genus", Text, nullable=True),
    Column("gene_src_species", Text, nullable=True),
    Column("gene_src_strain", Text, nullable=True),
    Column("gene_src_tissue", Text, nullable=True),
    Column("gene_src_tissue_fraction", Text, nullable=True),
    Column("host_org_genus", Text, nullable=True),
    Column("host_org_species", Text, nullable=True),
    Column("pdbx_gene_src_fragment", Text, nullable=True),
    Column("pdbx_gene_src_gene", Text, nullable=True),
    Column("pdbx_gene_src_scientific_name", Text, nullable=True),
    Column("pdbx_gene_src_variant", Text, nullable=True),
    Column("pdbx_gene_src_cell_line", Text, nullable=True),
    Column("pdbx_gene_src_atcc", Text, nullable=True),
    Column("pdbx_gene_src_organ", Text, nullable=True),
    Column("pdbx_gene_src_organelle", Text, nullable=True),
    Column("pdbx_gene_src_cell", Text, nullable=True),
    Column("pdbx_gene_src_cellular_location", Text, nullable=True),
    Column("pdbx_host_org_gene", Text, nullable=True),
    Column("pdbx_host_org_organ", Text, nullable=True),
    Column("pdbx_host_org_organelle", Text, nullable=True),
    Column("pdbx_host_org_cellular_location", Text, nullable=True),
    Column("pdbx_host_org_strain", Text, nullable=True),
    Column("pdbx_host_org_tissue_fraction", Text, nullable=True),
    Column("pdbx_description", Text, nullable=True),
    Column("host_org_common_name", Text, nullable=True),
    Column("host_org_details", Text, nullable=True),
    Column("plasmid_details", Text, nullable=True),
    Column("plasmid_name", Text, nullable=True),
    Column("pdbx_host_org_variant", Text, nullable=True),
    Column("pdbx_host_org_cell_line", Text, nullable=True),
    Column("pdbx_host_org_atcc", Text, nullable=True),
    Column("pdbx_host_org_culture_collection", Text, nullable=True),
    Column("pdbx_host_org_cell", Text, nullable=True),
    Column("pdbx_host_org_scientific_name", Text, nullable=True),
    Column("pdbx_host_org_tissue", Text, nullable=True),
    Column("pdbx_host_org_vector", Text, nullable=True),
    Column("pdbx_host_org_vector_type", Text, nullable=True),
    Column("expression_system_id", Text, nullable=True),
    Column("pdbx_gene_src_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_host_org_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
    Column("pdbx_seq_type", Text, nullable=True),
    Column("pdbx_beg_seq_num", Integer, nullable=True),
    Column("pdbx_end_seq_num", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("organism_scientific", Text, nullable=True),
    Column("organism_common_name", Text, nullable=True),
    Column("ncbi_taxonomy_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
    Column("pdbx_beg_seq_num", Integer, nullable=True),
    Column("pdbx_end_seq_num", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("descriptor", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("program", Text, nullable=True),
    Column("program_version", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["descriptor", "program", "program_version"]},
)

pdbx_related_exp_data_set = Table(
    "pdbx_related_exp_data_set",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("data_reference", Text, nullable=True),
    Column("metadata_reference", Text, nullable=True),
    Column("data_set_type", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": ["data_reference", "metadata_reference", "data_set_type", "details"]
    },
)

em_entity_assembly = Table(
    "em_entity_assembly",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("parent_id", Integer, nullable=True),
    Column("source", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("synonym", Text, nullable=True),
    Column("oligomeric_details", Text, nullable=True),
    Column("entity_id_list", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("virus_host_category", Text, nullable=True),
    Column("virus_type", Text, nullable=True),
    Column("virus_isolate", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("enveloped", Text, nullable=True),
    Column("empty", Text, nullable=True),
    Column("details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("film_material", Text, nullable=True),
    Column("grid_material", Text, nullable=True),
    Column("grid_mesh_size", Integer, nullable=True),
    Column("grid_type", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "specimen_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method", "grid_type", "pretreatment", "details"]},
)

em_buffer = Table(
    "em_buffer",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("pH", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "specimen_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

em_vitrification = Table(
    "em_vitrification",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("cryogen_name", Text, nullable=True),
    Column("humidity", Double, nullable=True),
    Column("temp", Double, nullable=True),
    Column("chamber_temperature", Double, nullable=True),
    Column("instrument", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("time_resolved_state", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "specimen_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["method", "time_resolved_state", "details"]},
)

em_imaging = Table(
    "em_imaging",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("astigmatism", Text, nullable=True),
    Column("electron_beam_tilt_params", Text, nullable=True),
    Column("residual_tilt", Double, nullable=True),
    Column("microscope_model", Text, nullable=True),
    Column("specimen_holder_type", Text, nullable=True),
    Column("specimen_holder_model", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("accelerating_voltage", Integer, nullable=True),
    Column("illumination_mode", Text, nullable=True),
    Column("mode", Text, nullable=True),
    Column("nominal_cs", Double, nullable=True),
    Column("nominal_defocus_min", Double, nullable=True),
    Column("nominal_defocus_max", Double, nullable=True),
    Column("calibrated_defocus_min", Double, nullable=True),
    Column("calibrated_defocus_max", Double, nullable=True),
    Column("tilt_angle_min", Double, nullable=True),
    Column("tilt_angle_max", Double, nullable=True),
    Column("nominal_magnification", Integer, nullable=True),
    Column("calibrated_magnification", Integer, nullable=True),
    Column("electron_source", Text, nullable=True),
    Column("temperature", Double, nullable=True),
    Column("detector_distance", Double, nullable=True),
    Column("recording_temperature_minimum", Double, nullable=True),
    Column("recording_temperature_maximum", Double, nullable=True),
    Column("alignment_procedure", Text, nullable=True),
    Column("c2_aperture_diameter", Double, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("cryogen", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("number_digital_images", Integer, nullable=True),
    Column("details", Text, nullable=True),
    Column("scanner_model", Text, nullable=True),
    Column("sampling_size", Double, nullable=True),
    Column("od_range", Double, nullable=True),
    Column("quant_bit_size", Integer, nullable=True),
    Column("dimension_height", Integer, nullable=True),
    Column("dimension_width", Integer, nullable=True),
    Column("frames_per_image", Integer, nullable=True),
    Column("image_recording_id", Text, nullable=True),
    Column("used_frames_per_image", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_recording_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details"]},
)

em_3d_reconstruction = Table(
    "em_3d_reconstruction",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("algorithm", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("resolution", Double, nullable=True),
    Column("resolution_method", Text, nullable=True),
    Column("magnification_calibration", Text, nullable=True),
    Column("nominal_pixel_size", Double, nullable=True),
    Column("actual_pixel_size", Double, nullable=True),
    Column("num_particles", Integer, nullable=True),
    Column("num_class_averages", Integer, nullable=True),
    Column("refinement_type", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("symmetry_type", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("target_criteria", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("overall_b_value", Double, nullable=True),
    Column("ref_space", Text, nullable=True),
    Column("ref_protocol", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["method", "target_criteria", "software_name", "details"]},
)

em_3d_fitting_list = Table(
    "em_3d_fitting_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("3d_fitting_id", Text, nullable=True),
    Column("pdb_entry_id", Text, nullable=True),
    Column("pdb_chain_id", Text, nullable=True),
    Column("pdb_chain_residue_range", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("chain_id", Text, nullable=True),
    Column("chain_residue_range", Text, nullable=True),
    Column("source_name", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("accession_code", Text, nullable=True),
    Column("initial_refinement_model_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "3d_fitting_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "accession_code"]},
)

em_helical_entity = Table(
    "em_helical_entity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("axial_symmetry", Text, nullable=True),
    Column("angular_rotation_per_subunit", Double, nullable=True),
    Column("axial_rise_per_subunit", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "hand"]},
)

em_experiment = Table(
    "em_experiment",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("reconstruction_method", Text, nullable=True),
    Column("aggregation_state", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["specimen_type"]},
)

em_single_particle_entity = Table(
    "em_single_particle_entity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("point_symmetry", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

em_admin = Table(
    "em_admin",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("current_status", Text, nullable=True),
    Column("deposition_date", Date, nullable=True),
    Column("deposition_site", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("last_update", Date, nullable=True),
    Column("map_release_date", Date, nullable=True),
    Column("title", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entry_id) -> entry(pdbid, id)
    info={"keywords": ["details", "title"]},
)

em_entity_assembly_molwt = Table(
    "em_entity_assembly_molwt",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("experimental_flag", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("units", Text, nullable=True),
    Column("value", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["method"]},
)

em_entity_assembly_naturalsource = Table(
    "em_entity_assembly_naturalsource",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("cell", Text, nullable=True),
    Column("cellular_location", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("organelle", Text, nullable=True),
    Column("organ", Text, nullable=True),
    Column("strain", Text, nullable=True),
    Column("tissue", Text, nullable=True),
    Column("details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("strain", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("cell", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("plasmid", Text, nullable=True),
    Column("strain", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "entity_assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["cell", "organism", "plasmid", "strain"]},
)

em_virus_natural_host = Table(
    "em_virus_natural_host",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("strain", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_assembly_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_synthetic = Table(
    "em_virus_synthetic",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("organism", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("strain", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_assembly_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_shell = Table(
    "em_virus_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diameter", Double, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("triangulation", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_assembly_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_assembly_id) -> em_entity_assembly(pdbid, id)
    info={"keywords": ["name"]},
)

em_specimen = Table(
    "em_specimen",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("concentration", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("embedding_applied", Boolean, nullable=True),
    Column("experiment_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("shadowing_applied", Boolean, nullable=True),
    Column("staining_applied", Boolean, nullable=True),
    Column("vitrification_applied", Boolean, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "experiment_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

em_embedding = Table(
    "em_embedding",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("material", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "material"]},
)

em_crystal_formation = Table(
    "em_crystal_formation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("atmosphere", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("instrument", Text, nullable=True),
    Column("lipid_mixture", Text, nullable=True),
    Column("lipid_protein_ratio", Double, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("temperature", Integer, nullable=True),
    Column("time", Integer, nullable=True),
    Column("time_unit", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["atmosphere", "details", "instrument", "lipid_mixture"]},
)

em_staining = Table(
    "em_staining",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("material", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "material"]},
)

em_buffer_component = Table(
    "em_buffer_component",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("buffer_id", Text, nullable=True),
    Column("concentration", Double, nullable=True),
    Column("concentration_units", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "buffer_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["concentration_units", "name"]},
)

em_diffraction = Table(
    "em_diffraction",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("camera_length", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("tilt_angle_list", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["tilt_angle_list"]},
)

em_diffraction_shell = Table(
    "em_diffraction_shell",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("em_diffraction_stats_id", Text, nullable=True),
    Column("fourier_space_coverage", Double, nullable=True),
    Column("high_resolution", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("low_resolution", Double, nullable=True),
    Column("multiplicity", Double, nullable=True),
    Column("num_structure_factors", Integer, nullable=True),
    Column("phase_residual", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

em_diffraction_stats = Table(
    "em_diffraction_stats",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("fourier_space_coverage", Double, nullable=True),
    Column("high_resolution", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("num_intensities_measured", Integer, nullable=True),
    Column("num_structure_factors", Integer, nullable=True),
    Column("overall_phase_error", Double, nullable=True),
    Column("overall_phase_residual", Double, nullable=True),
    Column("phase_error_rejection_criteria", Text, nullable=True),
    Column("r_merge", Double, nullable=True),
    Column("r_sym", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "phase_error_rejection_criteria"]},
)

em_image_recording = Table(
    "em_image_recording",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("average_exposure_time", Double, nullable=True),
    Column("avg_electron_dose_per_subtomogram", Double, nullable=True),
    Column("avg_electron_dose_per_image", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("detector_mode", Text, nullable=True),
    Column("film_or_detector_model", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("num_diffraction_images", Integer, nullable=True),
    Column("num_grids_imaged", Integer, nullable=True),
    Column("num_real_images", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "imaging_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "film_or_detector_model"]},
)

em_imaging_optics = Table(
    "em_imaging_optics",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("chr_aberration_corrector", Text, nullable=True),
    Column("energyfilter_lower", Text, nullable=True),
    Column("energyfilter_slit_width", Double, nullable=True),
    Column("energyfilter_name", Text, nullable=True),
    Column("energyfilter_upper", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("phase_plate", Text, nullable=True),
    Column("sph_aberration_corrector", Text, nullable=True),
    Column("details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("category", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("fitting_id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("version", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "name", "version"]},
)

em_ctf_correction = Table(
    "em_ctf_correction",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("em_image_processing_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "type"]},
)

em_volume_selection = Table(
    "em_volume_selection",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("num_tomograms", Integer, nullable=True),
    Column("num_volumes_extracted", Integer, nullable=True),
    Column("reference_model", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "method", "reference_model"]},
)

em_3d_crystal_entity = Table(
    "em_3d_crystal_entity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("angle_alpha", Double, nullable=True),
    Column("angle_beta", Double, nullable=True),
    Column("angle_gamma", Double, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("length_a", Double, nullable=True),
    Column("length_b", Double, nullable=True),
    Column("length_c", Double, nullable=True),
    Column("space_group_name", Text, nullable=True),
    Column("space_group_num", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["space_group_name"]},
)

em_2d_crystal_entity = Table(
    "em_2d_crystal_entity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("angle_gamma", Double, nullable=True),
    Column("c_sampling_length", Double, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("length_a", Double, nullable=True),
    Column("length_b", Double, nullable=True),
    Column("length_c", Double, nullable=True),
    Column("space_group_name_H-M", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

em_image_processing = Table(
    "em_image_processing",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_recording_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "image_recording_id", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

em_particle_selection = Table(
    "em_particle_selection",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("num_particles_selected", BigInteger, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "image_processing_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details", "method", "reference_model"]},
)

pdbx_entity_instance_feature = Table(
    "pdbx_entity_instance_feature",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("feature_type", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("auth_seq_num", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_deposit_group = Table(
    "pdbx_deposit_group",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("group_id", Text, nullable=True),
    Column("group_title", Text, nullable=True),
    Column("group_description", Text, nullable=True),
    Column("group_type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "group_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["group_title", "group_description"]},
)

pdbx_struct_assembly_auth_evidence = Table(
    "pdbx_struct_assembly_auth_evidence",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("assembly_id", Text, nullable=True),
    Column("experimental_support", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id", "assembly_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, assembly_id) -> pdbx_struct_assembly(pdbid, id)
    info={"keywords": ["assembly_id", "details"]},
)

pdbx_audit_revision_history = Table(
    "pdbx_audit_revision_history",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("major_revision", Integer, nullable=True),
    Column("minor_revision", Integer, nullable=True),
    Column("revision_date", Date, nullable=True),
    Column("part_number", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_audit_revision_group = Table(
    "pdbx_audit_revision_group",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("group", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
)

pdbx_audit_revision_category = Table(
    "pdbx_audit_revision_category",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("category", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
)

pdbx_audit_revision_details = Table(
    "pdbx_audit_revision_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("provider", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
    info={"keywords": ["description", "details"]},
)

pdbx_audit_revision_item = Table(
    "pdbx_audit_revision_item",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("item", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
)

pdbx_audit_conform = Table(
    "pdbx_audit_conform",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dict_location", Text, nullable=True),
    Column("dict_name", Text, nullable=True),
    Column("dict_version", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "dict_name", "dict_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)

pdbx_serial_crystallography_measurement = Table(
    "pdbx_serial_crystallography_measurement",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("pulse_energy", Double, nullable=True),
    Column("pulse_duration", Double, nullable=True),
    Column("xfel_pulse_repetition_rate", Double, nullable=True),
    Column("pulse_photon_energy", Double, nullable=True),
    Column("photons_per_pulse", Double, nullable=True),
    Column("source_size", Double, nullable=True),
    Column("source_distance", Double, nullable=True),
    Column("focal_spot_size", Double, nullable=True),
    Column("collimation", Text, nullable=True),
    Column("collection_time_total", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["collimation"]},
)

pdbx_serial_crystallography_sample_delivery = Table(
    "pdbx_serial_crystallography_sample_delivery",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("method", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["description"]},
)

pdbx_serial_crystallography_sample_delivery_injection = Table(
    "pdbx_serial_crystallography_sample_delivery_injection",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("injector_diameter", Double, nullable=True),
    Column("injector_temperature", Double, nullable=True),
    Column("flow_rate", Double, nullable=True),
    Column("carrier_solvent", Text, nullable=True),
    Column("crystal_concentration", Double, nullable=True),
    Column("preparation", Text, nullable=True),
    Column("power_by", Text, nullable=True),
    Column("injector_nozzle", Text, nullable=True),
    Column("jet_diameter", Double, nullable=True),
    Column("filter_size", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("sample_holding", Text, nullable=True),
    Column("support_base", Text, nullable=True),
    Column("sample_unit_size", Double, nullable=True),
    Column("crystals_per_unit", Integer, nullable=True),
    Column("sample_solvent", Text, nullable=True),
    Column("sample_dehydration_prevention", Text, nullable=True),
    Column("motion_control", Text, nullable=True),
    Column("velocity_horizontal", Double, nullable=True),
    Column("velocity_vertical", Double, nullable=True),
    Column("details", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("diffrn_id", Text, nullable=True),
    Column("frames_total", Integer, nullable=True),
    Column("xfel_pulse_events", Integer, nullable=True),
    Column("frame_hits", Integer, nullable=True),
    Column("crystal_hits", Integer, nullable=True),
    Column("frames_failed_index", Integer, nullable=True),
    Column("frames_indexed", Integer, nullable=True),
    Column("lattices_indexed", Integer, nullable=True),
    Column("xfel_run_numbers", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "diffrn_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, diffrn_id) -> diffrn(pdbid, id)
    info={"keywords": ["xfel_run_numbers"]},
)

pdbx_audit_support = Table(
    "pdbx_audit_support",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("funding_organization", Text, nullable=True),
    Column("country", Text, nullable=True),
    Column("grant_number", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["funding_organization", "country", "grant_number", "details"]},
)

pdbx_entity_branch_list = Table(
    "pdbx_entity_branch_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("hetero", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("num", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "num", "comp_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, comp_id) -> chem_comp(pdbid, id)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

pdbx_entity_branch_link = Table(
    "pdbx_entity_branch_link",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("link_id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("entity_branch_list_num_1", Integer, nullable=True),
    Column("entity_branch_list_num_2", Integer, nullable=True),
    Column("comp_id_1", Text, nullable=True),
    Column("comp_id_2", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("leaving_atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("leaving_atom_id_2", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "link_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

pdbx_entity_branch = Table(
    "pdbx_entity_branch",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

pdbx_branch_scheme = Table(
    "pdbx_branch_scheme",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("hetero", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("num", Integer, nullable=True),
    Column("pdb_asym_id", Text, nullable=True),
    Column("pdb_seq_num", Text, nullable=True),
    Column("pdb_mon_id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_seq_num", Text, nullable=True),
    Column("auth_mon_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "asym_id", "entity_id", "num", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

pdbx_sifts_xref_db = Table(
    "pdbx_sifts_xref_db",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("seq_id_ordinal", Integer, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("mon_id_one_letter_code", Text, nullable=True),
    Column("unp_res", Text, nullable=True),
    Column("unp_num", Integer, nullable=True),
    Column("unp_acc", Text, nullable=True),
    Column("unp_segment_id", Integer, nullable=True),
    Column("unp_instance_id", Integer, nullable=True),
    Column("res_type", Text, nullable=True),
    Column("observed", Text, nullable=True),
    Column("mh_id", Integer, nullable=True),
    Column("xref_db_name", Text, nullable=True),
    Column("xref_db_acc", Text, nullable=True),
    Column("xref_domain_name", Text, nullable=True),
    Column("xref_db_segment_id", Integer, nullable=True),
    Column("xref_db_instance_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "asym_id", "seq_id_ordinal", "seq_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, asym_id) -> struct_asym(pdbid, id)
    info={"keywords": ["unp_acc", "res_type", "xref_domain_name"]},
)

pdbx_sifts_xref_db_segments = Table(
    "pdbx_sifts_xref_db_segments",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("xref_db", Text, nullable=True),
    Column("xref_db_acc", Text, nullable=True),
    Column("domain_name", Text, nullable=True),
    Column("segment_id", Integer, nullable=True),
    Column("instance_id", Integer, nullable=True),
    Column("seq_id_start", Integer, nullable=True),
    Column("seq_id_end", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("unp_acc", Text, nullable=True),
    Column("segment_id", Integer, nullable=True),
    Column("instance_id", Integer, nullable=True),
    Column("unp_start", Integer, nullable=True),
    Column("unp_end", Integer, nullable=True),
    Column("seq_id_start", Integer, nullable=True),
    Column("seq_id_end", Integer, nullable=True),
    Column("best_mapping", Text, nullable=True),
    Column("identity", Double, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("entity_id_list", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("source_name", Text, nullable=True),
    Column("accession_code", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["accession_code", "details"]},
)

pdbx_modification_feature = Table(
    "pdbx_modification_feature",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("modified_residue_label_comp_id", Text, nullable=True),
    Column("modified_residue_label_asym_id", Text, nullable=True),
    Column("modified_residue_label_seq_id", Integer, nullable=True),
    Column("modified_residue_label_alt_id", Text, nullable=True),
    Column("auth_comp_id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_seq_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("symmetry", Text, nullable=True),
    Column("modified_residue_auth_comp_id", Text, nullable=True),
    Column("modified_residue_auth_asym_id", Text, nullable=True),
    Column("modified_residue_auth_seq_id", Text, nullable=True),
    Column("modified_residue_PDB_ins_code", Text, nullable=True),
    Column("modified_residue_symmetry", Text, nullable=True),
    Column("comp_id_linking_atom", Text, nullable=True),
    Column("modified_residue_id_linking_atom", Text, nullable=True),
    Column("modified_residue_id", Text, nullable=True),
    Column("ref_pcm_id", Integer, nullable=True),
    Column("ref_comp_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("category", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

citation_pdbmlplus = Table(
    "citation_pdbmlplus",
    metadata,
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("db_accession", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("pdbid", "db_name"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["db_name"]},
)

link_entity_pdbjplus = Table(
    "link_entity_pdbjplus",
    metadata,
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
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
