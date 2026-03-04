"""SQLAlchemy schema definition for ihm.

Auto-generated from schemas/ihm.def.yml by scripts/convert_yaml_to_sa.py.
"""

from sqlalchemy import (
    ARRAY,
    BigInteger,
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

metadata = MetaData(schema="ihm")
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
    Column("plus_fields", JSONB, nullable=True),
    PrimaryKeyConstraint("pdbid"),
)

atom_type = Table(
    "atom_type",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("symbol", Text, nullable=True),
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

audit_author = Table(
    "audit_author",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
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

citation = Table(
    "citation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("country", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("journal_abbrev", Text, nullable=True),
    Column("journal_id_ASTM", Text, nullable=True),
    Column("journal_id_CSD", Text, nullable=True),
    Column("journal_id_ISSN", Text, nullable=True),
    Column("journal_issue", Text, nullable=True),
    Column("journal_volume", Text, nullable=True),
    Column("page_first", Text, nullable=True),
    Column("page_last", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("year", Integer, nullable=True),
    Column("pdbx_database_id_DOI", Text, nullable=True),
    Column("pdbx_database_id_PubMed", Integer, nullable=True),
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
    PrimaryKeyConstraint("pdbid", "citation_id", "name", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, citation_id) -> citation(pdbid, id)
    info={"keywords": ["name", "identifier_ORCID"]},
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
    Column("nstd_chirality", Text, nullable=True),
    Column("nstd_linkage", Text, nullable=True),
    Column("nstd_monomer", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("type_details", Text, nullable=True),
    Column("pdbx_strand_id", Text, nullable=True),
    Column("pdbx_seq_one_letter_code", Text, nullable=True),
    Column("pdbx_seq_one_letter_code_can", Text, nullable=True),
    Column("pdbx_sequence_evidence_code", Text, nullable=True),
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

software = Table(
    "software",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("citation_id", Text, nullable=True),
    Column("classification", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("dependencies", Text, nullable=True),
    Column("location", Text, nullable=True),
    Column("name", Text, nullable=True),
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
    Column("pdbx_structure_determination_methodology", Text, nullable=True),
    Column("pdbx_descriptor", Text, nullable=True),
    Column("pdbx_model_details", Text, nullable=True),
    Column("pdbx_model_type_details", Text, nullable=True),
    Column("pdbx_CASP_flag", Text, nullable=True),
    Column("pdbx_details", Text, nullable=True),
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
    Column("pdbx_PDB_id", Text, nullable=True),
    Column("pdbx_alt_id", Text, nullable=True),
    Column("pdbx_type", Text, nullable=True),
    Column("pdbx_order", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    UniqueConstraint(
        "pdbid", "id", "entity_id", name="uq_ihm_struct_asym_pdbid_id_entity_id"
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["details", "pdbx_modified", "pdbx_fraction_per_asym_unit"]},
)

struct_conn = Table(
    "struct_conn",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("conn_type_id", Text, nullable=True),
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
    Column("ptnr2_auth_asym_id", Text, nullable=True),
    Column("ptnr2_auth_comp_id", Text, nullable=True),
    Column("ptnr2_auth_seq_id", Text, nullable=True),
    Column("ptnr2_symmetry", Text, nullable=True),
    Column("pdbx_dist_value", Double, nullable=True),
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

struct_ref = Table(
    "struct_ref",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_db_accession", Text, nullable=True),
    Column("pdbx_db_isoform", Text, nullable=True),
    Column("pdbx_seq_one_letter_code", Text, nullable=True),
    Column("pdbx_align_begin", Text, nullable=True),
    Column("pdbx_align_end", Text, nullable=True),
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
    Column("pdbx_seq_db_seq_num", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "pdbx_ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, align_id) -> struct_ref_seq(pdbid, align_id)
    info={"keywords": ["details"]},
)

pdbx_database_status = Table(
    "pdbx_database_status",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("status_code", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("recvd_initial_deposition_date", Date, nullable=True),
    Column("deposit_site", Text, nullable=True),
    Column("process_site", Text, nullable=True),
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
    PrimaryKeyConstraint("pdbid", "asym_id", "ndb_seq_num"),
    # FK: (pdbid) -> brief_summary(pdbid)
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
    Column("sequence_details", Text, nullable=True),
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

entity_src_gen = Table(
    "entity_src_gen",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("gene_src_common_name", Text, nullable=True),
    Column("gene_src_genus", Text, nullable=True),
    Column("pdbx_gene_src_scientific_name", Text, nullable=True),
    Column("pdbx_host_org_strain", Text, nullable=True),
    Column("host_org_common_name", Text, nullable=True),
    Column("pdbx_host_org_scientific_name", Text, nullable=True),
    Column("pdbx_gene_src_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_host_org_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
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

pdbx_protein_info = Table(
    "pdbx_protein_info",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("num_per_asym_unit", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name"]},
)

pdbx_entity_poly_na_type = Table(
    "pdbx_entity_poly_na_type",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
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
    PrimaryKeyConstraint("pdbid", "ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
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
    PrimaryKeyConstraint("pdbid", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(pdbid, data_content_type, ordinal)
    info={"keywords": ["description", "details"]},
)

pdbx_entity_branch_list = Table(
    "pdbx_entity_branch_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
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
    Column("asym_id", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("num", Integer, nullable=True),
    Column("pdb_asym_id", Text, nullable=True),
    Column("pdb_seq_num", Text, nullable=True),
    Column("pdb_mon_id", Text, nullable=True),
    Column("auth_seq_num", Text, nullable=True),
    Column("auth_mon_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "asym_id", "entity_id", "num", "mon_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
)

ihm_entity_poly_segment = Table(
    "ihm_entity_poly_segment",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("seq_id_begin", Integer, nullable=True),
    Column("seq_id_end", Integer, nullable=True),
    Column("comp_id_begin", Text, nullable=True),
    Column("comp_id_end", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_starting_model_details = Table(
    "ihm_starting_model_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("starting_model_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("entity_description", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("entity_poly_segment_id", Integer, nullable=True),
    Column("starting_model_source", Text, nullable=True),
    Column("starting_model_auth_asym_id", Text, nullable=True),
    Column("starting_model_sequence_offset", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "starting_model_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description", "description"]},
)

ihm_starting_comparative_models = Table(
    "ihm_starting_comparative_models",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("starting_model_id", Text, nullable=True),
    Column("starting_model_auth_asym_id", Text, nullable=True),
    Column("starting_model_seq_id_begin", Integer, nullable=True),
    Column("starting_model_seq_id_end", Integer, nullable=True),
    Column("template_auth_asym_id", Text, nullable=True),
    Column("template_seq_id_begin", Integer, nullable=True),
    Column("template_seq_id_end", Integer, nullable=True),
    Column("template_sequence_identity", Double, nullable=True),
    Column("template_sequence_identity_denominator", Integer, nullable=True),
    Column("template_dataset_list_id", Integer, nullable=True),
    Column("alignment_file_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_starting_computational_models = Table(
    "ihm_starting_computational_models",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("starting_model_id", Text, nullable=True),
    Column("script_file_id", Integer, nullable=True),
    Column("software_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "starting_model_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_starting_model_seq_dif = Table(
    "ihm_starting_model_seq_dif",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("starting_model_id", Text, nullable=True),
    Column("db_entity_id", Text, nullable=True),
    Column("db_asym_id", Text, nullable=True),
    Column("db_seq_id", Integer, nullable=True),
    Column("db_comp_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_model_representation = Table(
    "ihm_model_representation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

ihm_model_representation_details = Table(
    "ihm_model_representation_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("representation_id", Integer, nullable=True),
    Column("entity_poly_segment_id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("entity_description", Text, nullable=True),
    Column("entity_asym_id", Text, nullable=True),
    Column("model_object_primitive", Text, nullable=True),
    Column("starting_model_id", Text, nullable=True),
    Column("model_mode", Text, nullable=True),
    Column("model_granularity", Text, nullable=True),
    Column("model_object_count", Integer, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description", "description"]},
)

ihm_struct_assembly_details = Table(
    "ihm_struct_assembly_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("assembly_id", Integer, nullable=True),
    Column("parent_assembly_id", Integer, nullable=True),
    Column("entity_description", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("entity_poly_segment_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description"]},
)

ihm_struct_assembly = Table(
    "ihm_struct_assembly",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "description"]},
)

ihm_modeling_protocol = Table(
    "ihm_modeling_protocol",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("num_steps", Integer, nullable=True),
    Column("protocol_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["protocol_name", "details"]},
)

ihm_modeling_protocol_details = Table(
    "ihm_modeling_protocol_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("protocol_id", Integer, nullable=True),
    Column("step_id", Integer, nullable=True),
    Column("struct_assembly_id", Integer, nullable=True),
    Column("dataset_group_id", Integer, nullable=True),
    Column("struct_assembly_description", Text, nullable=True),
    Column("step_name", Text, nullable=True),
    Column("step_method", Text, nullable=True),
    Column("num_models_begin", Integer, nullable=True),
    Column("num_models_end", Integer, nullable=True),
    Column("multi_scale_flag", Text, nullable=True),
    Column("multi_state_flag", Text, nullable=True),
    Column("ordered_flag", Text, nullable=True),
    Column("ensemble_flag", Text, nullable=True),
    Column("script_file_id", Integer, nullable=True),
    Column("software_id", Integer, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "struct_assembly_description",
            "step_name",
            "step_method",
            "description",
        ]
    },
)

ihm_multi_state_modeling = Table(
    "ihm_multi_state_modeling",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("state_id", Integer, nullable=True),
    Column("state_group_id", Integer, nullable=True),
    Column("population_fraction", Double, nullable=True),
    Column("state_type", Text, nullable=True),
    Column("state_name", Text, nullable=True),
    Column("experiment_type", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "state_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["state_type", "state_name", "details"]},
)

ihm_multi_state_model_group_link = Table(
    "ihm_multi_state_model_group_link",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("state_id", Integer, nullable=True),
    Column("model_group_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "model_group_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_ordered_model = Table(
    "ihm_ordered_model",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("process_id", Integer, nullable=True),
    Column("process_description", Text, nullable=True),
    Column("edge_id", Integer, nullable=True),
    Column("edge_description", Text, nullable=True),
    Column("step_id", Integer, nullable=True),
    Column("step_description", Text, nullable=True),
    Column("ordered_by", Text, nullable=True),
    Column("model_group_id_begin", Integer, nullable=True),
    Column("model_group_id_end", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "edge_id", "process_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "process_description",
            "edge_description",
            "step_description",
            "ordered_by",
        ]
    },
)

ihm_modeling_post_process = Table(
    "ihm_modeling_post_process",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("protocol_id", Integer, nullable=True),
    Column("analysis_id", Integer, nullable=True),
    Column("step_id", Integer, nullable=True),
    Column("struct_assembly_id", Integer, nullable=True),
    Column("dataset_group_id", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("feature", Text, nullable=True),
    Column("feature_name", Text, nullable=True),
    Column("num_models_begin", Integer, nullable=True),
    Column("num_models_end", Integer, nullable=True),
    Column("script_file_id", Integer, nullable=True),
    Column("software_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["feature_name", "details"]},
)

ihm_ensemble_info = Table(
    "ihm_ensemble_info",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ensemble_id", Integer, nullable=True),
    Column("ensemble_name", Text, nullable=True),
    Column("post_process_id", Integer, nullable=True),
    Column("model_group_id", Integer, nullable=True),
    Column("model_group_superimposed_flag", Text, nullable=True),
    Column("ensemble_clustering_method", Text, nullable=True),
    Column("ensemble_clustering_feature", Text, nullable=True),
    Column("num_ensemble_models", Integer, nullable=True),
    Column("num_ensemble_models_deposited", Integer, nullable=True),
    Column("ensemble_precision_value", Double, nullable=True),
    Column("ensemble_file_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    Column("sub_sample_flag", Text, nullable=True),
    Column("sub_sampling_type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ensemble_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["ensemble_name", "details"]},
)

ihm_ensemble_sub_sample = Table(
    "ihm_ensemble_sub_sample",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("ensemble_id", Integer, nullable=True),
    Column("num_models", Integer, nullable=True),
    Column("num_models_deposited", Integer, nullable=True),
    Column("file_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name"]},
)

ihm_model_list = Table(
    "ihm_model_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("model_name", Text, nullable=True),
    Column("assembly_id", Integer, nullable=True),
    Column("protocol_id", Integer, nullable=True),
    Column("representation_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "model_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["model_name"]},
)

ihm_model_group = Table(
    "ihm_model_group",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

ihm_model_group_link = Table(
    "ihm_model_group_link",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "model_id", "group_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_model_representative = Table(
    "ihm_model_representative",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("model_group_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("selection_criteria", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_dataset_list = Table(
    "ihm_dataset_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("data_type", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("database_hosted", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_dataset_group = Table(
    "ihm_dataset_group",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("application", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

ihm_dataset_group_link = Table(
    "ihm_dataset_group_link",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "dataset_list_id", "group_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_related_datasets = Table(
    "ihm_related_datasets",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dataset_list_id_derived", Integer, nullable=True),
    Column("dataset_list_id_primary", Integer, nullable=True),
    Column("transformation_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "dataset_list_id_primary", "dataset_list_id_derived"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_data_transformation = Table(
    "ihm_data_transformation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("rot_matrix11", Double, nullable=True),
    Column("rot_matrix21", Double, nullable=True),
    Column("rot_matrix31", Double, nullable=True),
    Column("rot_matrix12", Double, nullable=True),
    Column("rot_matrix22", Double, nullable=True),
    Column("rot_matrix32", Double, nullable=True),
    Column("rot_matrix13", Double, nullable=True),
    Column("rot_matrix23", Double, nullable=True),
    Column("rot_matrix33", Double, nullable=True),
    Column("tr_vector1", Double, nullable=True),
    Column("tr_vector2", Double, nullable=True),
    Column("tr_vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_dataset_related_db_reference = Table(
    "ihm_dataset_related_db_reference",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("accession_code", Text, nullable=True),
    Column("version", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_external_reference_info = Table(
    "ihm_external_reference_info",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("reference_id", Integer, nullable=True),
    Column("reference_provider", Text, nullable=True),
    Column("reference_type", Text, nullable=True),
    Column("reference", Text, nullable=True),
    Column("refers_to", Text, nullable=True),
    Column("associated_url", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "reference_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["reference_provider", "details"]},
)

ihm_external_files = Table(
    "ihm_external_files",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("reference_id", Integer, nullable=True),
    Column("file_path", Text, nullable=True),
    Column("file_format", Text, nullable=True),
    Column("content_type", Text, nullable=True),
    Column("file_size_bytes", Double, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["file_path", "details"]},
)

ihm_dataset_external_reference = Table(
    "ihm_dataset_external_reference",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("file_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_localization_density_files = Table(
    "ihm_localization_density_files",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("file_id", Integer, nullable=True),
    Column("ensemble_id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("entity_poly_segment_id", Integer, nullable=True),
    Column("asym_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_predicted_contact_restraint = Table(
    "ihm_predicted_contact_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    Column("entity_description_1", Text, nullable=True),
    Column("entity_description_2", Text, nullable=True),
    Column("entity_id_1", Text, nullable=True),
    Column("entity_id_2", Text, nullable=True),
    Column("asym_id_1", Text, nullable=True),
    Column("asym_id_2", Text, nullable=True),
    Column("comp_id_1", Text, nullable=True),
    Column("comp_id_2", Text, nullable=True),
    Column("seq_id_1", Integer, nullable=True),
    Column("seq_id_2", Integer, nullable=True),
    Column("rep_atom_1", Text, nullable=True),
    Column("rep_atom_2", Text, nullable=True),
    Column("distance_lower_limit", Double, nullable=True),
    Column("distance_upper_limit", Double, nullable=True),
    Column("probability", Double, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("model_granularity", Text, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("software_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description_1", "entity_description_2"]},
)

ihm_hydroxyl_radical_fp_restraint = Table(
    "ihm_hydroxyl_radical_fp_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("fp_rate", Double, nullable=True),
    Column("fp_rate_error", Double, nullable=True),
    Column("log_pf", Double, nullable=True),
    Column("log_pf_error", Double, nullable=True),
    Column("predicted_sasa", Double, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("software_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description"]},
)

ihm_chemical_component_descriptor = Table(
    "ihm_chemical_component_descriptor",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("chemical_name", Text, nullable=True),
    Column("common_name", Text, nullable=True),
    Column("auth_name", Text, nullable=True),
    Column("smiles", Text, nullable=True),
    Column("smiles_canonical", Text, nullable=True),
    Column("inchi", Text, nullable=True),
    Column("inchi_key", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "chemical_name",
            "common_name",
            "auth_name",
            "smiles",
            "smiles_canonical",
            "inchi",
            "inchi_key",
            "details",
        ]
    },
)

ihm_probe_list = Table(
    "ihm_probe_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("probe_id", Integer, nullable=True),
    Column("probe_name", Text, nullable=True),
    Column("reactive_probe_flag", Text, nullable=True),
    Column("reactive_probe_name", Text, nullable=True),
    Column("probe_origin", Text, nullable=True),
    Column("probe_link_type", Text, nullable=True),
    Column("probe_chem_comp_descriptor_id", Integer, nullable=True),
    Column("reactive_probe_chem_comp_descriptor_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "probe_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["probe_name", "reactive_probe_name"]},
)

ihm_poly_probe_position = Table(
    "ihm_poly_probe_position",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("entity_description", Text, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("mutation_flag", Text, nullable=True),
    Column("mut_res_chem_comp_id", Text, nullable=True),
    Column("modification_flag", Text, nullable=True),
    Column("mod_res_chem_comp_descriptor_id", Integer, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description", "description"]},
)

ihm_poly_probe_conjugate = Table(
    "ihm_poly_probe_conjugate",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("probe_id", Integer, nullable=True),
    Column("position_id", Integer, nullable=True),
    Column("chem_comp_descriptor_id", Integer, nullable=True),
    Column("ambiguous_stoichiometry_flag", Text, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_epr_restraint = Table(
    "ihm_epr_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("fitting_particle_type", Text, nullable=True),
    Column("fitting_method", Text, nullable=True),
    Column("fitting_method_citation_id", Text, nullable=True),
    Column("fitting_state", Text, nullable=True),
    Column("fitting_software_id", Integer, nullable=True),
    Column("chi_value", Double, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["fitting_particle_type", "fitting_method", "details"]},
)

ihm_cross_link_list = Table(
    "ihm_cross_link_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    Column("entity_description_1", Text, nullable=True),
    Column("entity_description_2", Text, nullable=True),
    Column("entity_id_1", Text, nullable=True),
    Column("entity_id_2", Text, nullable=True),
    Column("comp_id_1", Text, nullable=True),
    Column("comp_id_2", Text, nullable=True),
    Column("seq_id_1", Integer, nullable=True),
    Column("seq_id_2", Integer, nullable=True),
    Column("linker_type", Text, nullable=True),
    Column("linker_chem_comp_descriptor_id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description_1", "entity_description_2", "details"]},
)

ihm_cross_link_restraint = Table(
    "ihm_cross_link_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    Column("entity_id_1", Text, nullable=True),
    Column("entity_id_2", Text, nullable=True),
    Column("asym_id_1", Text, nullable=True),
    Column("asym_id_2", Text, nullable=True),
    Column("comp_id_1", Text, nullable=True),
    Column("comp_id_2", Text, nullable=True),
    Column("seq_id_1", Integer, nullable=True),
    Column("seq_id_2", Integer, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("conditional_crosslink_flag", Text, nullable=True),
    Column("model_granularity", Text, nullable=True),
    Column("distance_threshold", Double, nullable=True),
    Column("psi", Double, nullable=True),
    Column("sigma_1", Double, nullable=True),
    Column("sigma_2", Double, nullable=True),
    Column("pseudo_site_flag", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_cross_link_pseudo_site = Table(
    "ihm_cross_link_pseudo_site",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("restraint_id", Integer, nullable=True),
    Column("cross_link_partner", Integer, nullable=True),
    Column("pseudo_site_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_cross_link_result = Table(
    "ihm_cross_link_result",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("restraint_id", Integer, nullable=True),
    Column("ensemble_id", Integer, nullable=True),
    Column("num_models", Integer, nullable=True),
    Column("model_group_id", Integer, nullable=True),
    Column("distance_threshold", Double, nullable=True),
    Column("median_distance", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_cross_link_result_parameters = Table(
    "ihm_cross_link_result_parameters",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("restraint_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("psi", Double, nullable=True),
    Column("sigma_1", Double, nullable=True),
    Column("sigma_2", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_2dem_class_average_restraint = Table(
    "ihm_2dem_class_average_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("number_raw_micrographs", Integer, nullable=True),
    Column("pixel_size_width", Double, nullable=True),
    Column("pixel_size_height", Double, nullable=True),
    Column("image_resolution", Double, nullable=True),
    Column("image_segment_flag", Text, nullable=True),
    Column("number_of_projections", Integer, nullable=True),
    Column("struct_assembly_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_2dem_class_average_fitting = Table(
    "ihm_2dem_class_average_fitting",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("restraint_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("cross_correlation_coefficient", Double, nullable=True),
    Column("rot_matrix11", Double, nullable=True),
    Column("rot_matrix21", Double, nullable=True),
    Column("rot_matrix31", Double, nullable=True),
    Column("rot_matrix12", Double, nullable=True),
    Column("rot_matrix22", Double, nullable=True),
    Column("rot_matrix32", Double, nullable=True),
    Column("rot_matrix13", Double, nullable=True),
    Column("rot_matrix23", Double, nullable=True),
    Column("rot_matrix33", Double, nullable=True),
    Column("tr_vector1", Double, nullable=True),
    Column("tr_vector2", Double, nullable=True),
    Column("tr_vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_3dem_restraint = Table(
    "ihm_3dem_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("struct_assembly_id", Integer, nullable=True),
    Column("fitting_method", Text, nullable=True),
    Column("number_of_gaussians", Integer, nullable=True),
    Column("map_segment_flag", Text, nullable=True),
    Column("cross_correlation_coefficient", Double, nullable=True),
    Column("fitting_method_citation_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["fitting_method", "details"]},
)

ihm_sas_restraint = Table(
    "ihm_sas_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("struct_assembly_id", Integer, nullable=True),
    Column("profile_segment_flag", Text, nullable=True),
    Column("fitting_atom_type", Text, nullable=True),
    Column("fitting_method", Text, nullable=True),
    Column("fitting_state", Text, nullable=True),
    Column("radius_of_gyration", Double, nullable=True),
    Column("chi_value", Double, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["fitting_atom_type", "fitting_method", "details"]},
)

ihm_hdx_restraint = Table(
    "ihm_hdx_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("protection_factor", Double, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_starting_model_coord = Table(
    "ihm_starting_model_coord",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("starting_model_id", Text, nullable=True),
    Column("group_PDB", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("type_symbol", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("atom_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("Cartn_x", Double, nullable=True),
    Column("Cartn_y", Double, nullable=True),
    Column("Cartn_z", Double, nullable=True),
    Column("B_iso_or_equiv", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_sphere_obj_site = Table(
    "ihm_sphere_obj_site",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("seq_id_begin", Integer, nullable=True),
    Column("seq_id_end", Integer, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("Cartn_x", Double, nullable=True),
    Column("Cartn_y", Double, nullable=True),
    Column("Cartn_z", Double, nullable=True),
    Column("object_radius", Double, nullable=True),
    Column("rmsf", Double, nullable=True),
    Column("model_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_pseudo_site = Table(
    "ihm_pseudo_site",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("Cartn_x", Double, nullable=True),
    Column("Cartn_y", Double, nullable=True),
    Column("Cartn_z", Double, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["description"]},
)

ihm_residues_not_modeled = Table(
    "ihm_residues_not_modeled",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("model_id", Integer, nullable=True),
    Column("entity_description", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("seq_id_begin", Integer, nullable=True),
    Column("seq_id_end", Integer, nullable=True),
    Column("comp_id_begin", Text, nullable=True),
    Column("comp_id_end", Text, nullable=True),
    Column("reason", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["entity_description", "details"]},
)

ihm_feature_list = Table(
    "ihm_feature_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("feature_type", Text, nullable=True),
    Column("entity_type", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "feature_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_poly_atom_feature = Table(
    "ihm_poly_atom_feature",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("seq_id", Integer, nullable=True),
    Column("atom_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_poly_residue_feature = Table(
    "ihm_poly_residue_feature",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("comp_id_begin", Text, nullable=True),
    Column("comp_id_end", Text, nullable=True),
    Column("seq_id_begin", Integer, nullable=True),
    Column("seq_id_end", Integer, nullable=True),
    Column("residue_range_granularity", Text, nullable=True),
    Column("rep_atom", Text, nullable=True),
    Column("interface_residue_flag", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_non_poly_feature = Table(
    "ihm_non_poly_feature",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("asym_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("atom_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_interface_residue_feature = Table(
    "ihm_interface_residue_feature",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("binding_partner_entity_id", Text, nullable=True),
    Column("binding_partner_asym_id", Text, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_derived_distance_restraint = Table(
    "ihm_derived_distance_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    Column("feature_id_1", Integer, nullable=True),
    Column("feature_id_2", Integer, nullable=True),
    Column("group_conditionality", Text, nullable=True),
    Column("random_exclusion_fraction", Double, nullable=True),
    Column("distance_lower_limit", Double, nullable=True),
    Column("distance_upper_limit", Double, nullable=True),
    Column("distance_upper_limit_esd", Double, nullable=True),
    Column("probability", Double, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("distance_threshold_mean", Double, nullable=True),
    Column("distance_threshold_esd", Double, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_derived_angle_restraint = Table(
    "ihm_derived_angle_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    Column("feature_id_1", Integer, nullable=True),
    Column("feature_id_2", Integer, nullable=True),
    Column("feature_id_3", Integer, nullable=True),
    Column("group_conditionality", Text, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("angle_threshold_mean", Double, nullable=True),
    Column("angle_threshold_esd", Double, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_derived_dihedral_restraint = Table(
    "ihm_derived_dihedral_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("group_id", Integer, nullable=True),
    Column("feature_id_1", Integer, nullable=True),
    Column("feature_id_2", Integer, nullable=True),
    Column("feature_id_3", Integer, nullable=True),
    Column("feature_id_4", Integer, nullable=True),
    Column("group_conditionality", Text, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("dihedral_threshold_mean", Double, nullable=True),
    Column("dihedral_threshold_esd", Double, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_list = Table(
    "ihm_geometric_object_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("object_id", Integer, nullable=True),
    Column("object_type", Text, nullable=True),
    Column("object_name", Text, nullable=True),
    Column("object_description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "object_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["object_name", "object_description"]},
)

ihm_geometric_object_center = Table(
    "ihm_geometric_object_center",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("xcoord", Double, nullable=True),
    Column("ycoord", Double, nullable=True),
    Column("zcoord", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_transformation = Table(
    "ihm_geometric_object_transformation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("rot_matrix11", Double, nullable=True),
    Column("rot_matrix21", Double, nullable=True),
    Column("rot_matrix31", Double, nullable=True),
    Column("rot_matrix12", Double, nullable=True),
    Column("rot_matrix22", Double, nullable=True),
    Column("rot_matrix32", Double, nullable=True),
    Column("rot_matrix13", Double, nullable=True),
    Column("rot_matrix23", Double, nullable=True),
    Column("rot_matrix33", Double, nullable=True),
    Column("tr_vector1", Double, nullable=True),
    Column("tr_vector2", Double, nullable=True),
    Column("tr_vector3", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_torus = Table(
    "ihm_geometric_object_torus",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("object_id", Integer, nullable=True),
    Column("center_id", Integer, nullable=True),
    Column("transformation_id", Integer, nullable=True),
    Column("major_radius_R", Double, nullable=True),
    Column("minor_radius_r", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "object_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_half_torus = Table(
    "ihm_geometric_object_half_torus",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("object_id", Integer, nullable=True),
    Column("thickness_th", Double, nullable=True),
    Column("section", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "object_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_axis = Table(
    "ihm_geometric_object_axis",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("object_id", Integer, nullable=True),
    Column("axis_type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "object_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_plane = Table(
    "ihm_geometric_object_plane",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("object_id", Integer, nullable=True),
    Column("plane_type", Text, nullable=True),
    Column("transformation_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "object_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_geometric_object_distance_restraint = Table(
    "ihm_geometric_object_distance_restraint",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("object_id", Integer, nullable=True),
    Column("feature_id", Integer, nullable=True),
    Column("object_characteristic", Text, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("harmonic_force_constant", Double, nullable=True),
    Column("group_conditionality", Text, nullable=True),
    Column("distance_lower_limit", Double, nullable=True),
    Column("distance_upper_limit", Double, nullable=True),
    Column("distance_probability", Double, nullable=True),
    Column("dataset_list_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_entry_collection = Table(
    "ihm_entry_collection",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

ihm_entry_collection_mapping = Table(
    "ihm_entry_collection_mapping",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("collection_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "collection_id", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

ihm_multi_state_scheme = Table(
    "ihm_multi_state_scheme",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "details"]},
)

ihm_multi_state_scheme_connectivity = Table(
    "ihm_multi_state_scheme_connectivity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("scheme_id", Integer, nullable=True),
    Column("begin_state_id", Integer, nullable=True),
    Column("end_state_id", Integer, nullable=True),
    Column("dataset_group_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_kinetic_rate = Table(
    "ihm_kinetic_rate",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("transition_rate_constant", Double, nullable=True),
    Column("scheme_connectivity_id", Integer, nullable=True),
    Column("dataset_group_id", Integer, nullable=True),
    Column("external_file_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["equilibrium_constant_unit", "details"]},
)

ihm_relaxation_time = Table(
    "ihm_relaxation_time",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("value", Double, nullable=True),
    Column("unit", Text, nullable=True),
    Column("amplitude", Double, nullable=True),
    Column("dataset_group_id", Integer, nullable=True),
    Column("external_file_id", Integer, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)

ihm_relaxation_time_multi_state_scheme = Table(
    "ihm_relaxation_time_multi_state_scheme",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("relaxation_time_id", Integer, nullable=True),
    Column("scheme_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["details"]},
)
