"""SQLAlchemy schema definition for prd.

Auto-generated from schemas/prd.def.yml by scripts/convert_yaml_to_sa.py.
"""

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Column,
    Date,
    DateTime,
    Double,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)

metadata = MetaData(schema="prd")
metadata.info = {
    "entry_pk": "prd_id",
    "skip_foreign_keys": True,
}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("name", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("pdbx_initial_date", Date, nullable=True),
    Column("pdbx_modified_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("prd_id"),
    Index("ix_prd_brief_summary_docid", "docid"),
    Index("ix_prd_brief_summary_keywords", "keywords"),
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_release_status", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "id"),
    # FK: (prd_id) -> brief_summary(prd_id)
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
    Column("prd_id", Text, nullable=True),
    Column("alt_atom_id", Text, nullable=True),
    Column("atom_id", Text, nullable=True),
    Column("charge", Integer, nullable=True),
    Column("model_Cartn_x", Double, nullable=True),
    Column("model_Cartn_y", Double, nullable=True),
    Column("model_Cartn_z", Double, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("type_symbol", Text, nullable=True),
    Column("pdbx_align", Integer, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_component_atom_id", Text, nullable=True),
    Column("pdbx_component_comp_id", Text, nullable=True),
    Column("pdbx_model_Cartn_x_ideal", Double, nullable=True),
    Column("pdbx_model_Cartn_y_ideal", Double, nullable=True),
    Column("pdbx_model_Cartn_z_ideal", Double, nullable=True),
    Column("pdbx_stereo_config", Text, nullable=True),
    Column("pdbx_aromatic_flag", Text, nullable=True),
    Column("pdbx_leaving_atom_flag", Text, nullable=True),
    Column("pdbx_residue_numbering", Integer, nullable=True),
    Column("pdbx_polymer_type", Text, nullable=True),
    Column("pdbx_ref_id", Text, nullable=True),
    Column("pdbx_component_id", Integer, nullable=True),
    Column("pdbx_backbone_atom_flag", Text, nullable=True),
    Column("pdbx_n_terminal_atom_flag", Text, nullable=True),
    Column("pdbx_c_terminal_atom_flag", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "comp_id", "atom_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
    info={"keywords": ["alt_atom_id", "pdbx_stnd_atom_id"]},
)

chem_comp_bond = Table(
    "chem_comp_bond",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_stereo_config", Text, nullable=True),
    Column("pdbx_aromatic_flag", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "comp_id", "atom_id_1", "atom_id_2"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id, atom_id_1) -> chem_comp_atom(prd_id, comp_id, atom_id)
    # FK: (prd_id, comp_id, atom_id_2) -> chem_comp_atom(prd_id, comp_id, atom_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
)

pdbx_chem_comp_descriptor = Table(
    "pdbx_chem_comp_descriptor",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("descriptor", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("program", Text, nullable=True),
    Column("program_version", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "comp_id", "type", "program", "program_version"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
    info={"keywords": ["descriptor", "program", "program_version"]},
)

pdbx_chem_comp_identifier = Table(
    "pdbx_chem_comp_identifier",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("identifier", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("program", Text, nullable=True),
    Column("program_version", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "comp_id", "type", "program", "program_version"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
    info={"keywords": ["identifier", "program", "program_version"]},
)

pdbx_reference_molecule = Table(
    "pdbx_reference_molecule",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("formula", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("type_evidence_code", Text, nullable=True),
    Column("class", Text, nullable=True),
    Column("class_evidence_code", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("represent_as", Text, nullable=True),
    Column("chem_comp_id", Text, nullable=True),
    Column("compound_details", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("representative_PDB_id_code", Text, nullable=True),
    Column("release_status", Text, nullable=True),
    Column("replaces", Text, nullable=True),
    Column("replaced_by", Text, nullable=True),
    PrimaryKeyConstraint("prd_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    info={
        "keywords": [
            "formula",
            "type_evidence_code",
            "class_evidence_code",
            "name",
            "compound_details",
            "description",
        ],
        "pkout": True,
    },
)

pdbx_reference_entity_list = Table(
    "pdbx_reference_entity_list",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("component_id", Integer, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id", "component_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id) -> pdbx_reference_molecule(prd_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)

pdbx_reference_entity_nonpoly = Table(
    "pdbx_reference_entity_nonpoly",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("chem_comp_id", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    info={
        "keywords": ["details", "name"],
        "pkout": True,
    },
)

pdbx_reference_entity_link = Table(
    "pdbx_reference_entity_link",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("link_id", Integer, nullable=True),
    Column("ref_entity_id_1", Text, nullable=True),
    Column("ref_entity_id_2", Text, nullable=True),
    Column("entity_seq_num_1", Integer, nullable=True),
    Column("entity_seq_num_2", Integer, nullable=True),
    Column("comp_id_1", Text, nullable=True),
    Column("comp_id_2", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    Column("component_1", Integer, nullable=True),
    Column("component_2", Integer, nullable=True),
    Column("link_class", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "link_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, ref_entity_id_1, component_1) -> pdbx_reference_entity_list(prd_id, ref_entity_id, component_id)
    # FK: (prd_id, ref_entity_id_2, component_2) -> pdbx_reference_entity_list(prd_id, ref_entity_id, component_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)

pdbx_reference_entity_poly_link = Table(
    "pdbx_reference_entity_poly_link",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("link_id", Integer, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("component_id", Integer, nullable=True),
    Column("entity_seq_num_1", Integer, nullable=True),
    Column("entity_seq_num_2", Integer, nullable=True),
    Column("comp_id_1", Text, nullable=True),
    Column("comp_id_2", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id", "link_id", "component_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, ref_entity_id) -> pdbx_reference_entity_poly(prd_id, ref_entity_id)
    # FK: (prd_id, ref_entity_id, component_id) -> pdbx_reference_entity_list(prd_id, ref_entity_id, component_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)

pdbx_reference_entity_poly = Table(
    "pdbx_reference_entity_poly",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    info={
        "keywords": ["db_code", "db_name"],
        "pkout": True,
    },
)

pdbx_reference_entity_poly_seq = Table(
    "pdbx_reference_entity_poly_seq",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("mon_id", Text, nullable=True),
    Column("parent_mon_id", Text, nullable=True),
    Column("num", Integer, nullable=True),
    Column("observed", Text, nullable=True),
    Column("hetero", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id", "num", "mon_id", "hetero"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, ref_entity_id) -> pdbx_reference_entity_poly(prd_id, ref_entity_id)
    info={"pkout": True},
)

pdbx_reference_entity_sequence = Table(
    "pdbx_reference_entity_sequence",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("NRP_flag", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    info={
        "keywords": ["one_letter_codes"],
        "pkout": True,
    },
)

pdbx_reference_entity_src_nat = Table(
    "pdbx_reference_entity_src_nat",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("ref_entity_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("organism_scientific", Text, nullable=True),
    Column("strain", Text, nullable=True),
    Column("taxid", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("source", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "ref_entity_id", "ordinal"),
    # FK: (prd_id) -> brief_summary(prd_id)
    info={
        "keywords": [
            "organism_scientific",
            "strain",
            "taxid",
            "atcc",
            "db_code",
            "db_name",
            "source",
            "source_id",
        ],
        "pkout": True,
    },
)

pdbx_reference_entity_subcomponents = Table(
    "pdbx_reference_entity_subcomponents",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("seq", Text, nullable=True),
    Column("chem_comp_id", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "seq"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id) -> pdbx_reference_molecule(prd_id)
    info={
        "keywords": ["seq"],
        "pkout": True,
    },
)

pdbx_prd_audit = Table(
    "pdbx_prd_audit",
    metadata,
    Column("prd_id", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("processing_site", Text, nullable=True),
    Column("action_type", Text, nullable=True),
    PrimaryKeyConstraint("prd_id", "date", "action_type"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id) -> pdbx_reference_molecule(prd_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)
