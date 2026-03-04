"""SQLAlchemy schema definition for cc.

Auto-generated from schemas/cc.def.yml by scripts/convert_yaml_to_sa.py.
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

metadata = MetaData(schema="cc")
metadata.info = {"entry_pk": "comp_id"}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("pdbx_initial_date", Date, nullable=True),
    Column("release_date", Date, nullable=True),
    Column("pdbx_modified_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("name", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("pdbx_synonyms", ARRAY(Text), nullable=True),
    Column("identifier", Text, nullable=True),
    Column("smiles", ARRAY(Text), nullable=True),
    Column("inchi", ARRAY(Text), nullable=True),
    Column("canonical_smiles", Text, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("comp_id"),
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("mon_nstd_parent_comp_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("one_letter_code", Text, nullable=True),
    Column("three_letter_code", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_synonyms", Text, nullable=True),
    Column("pdbx_type", Text, nullable=True),
    Column("pdbx_ambiguous_flag", Text, nullable=True),
    Column("pdbx_replaced_by", Text, nullable=True),
    Column("pdbx_replaces", Text, nullable=True),
    Column("pdbx_formal_charge", Integer, nullable=True),
    Column("pdbx_subcomponent_list", Text, nullable=True),
    Column("pdbx_model_coordinates_details", Text, nullable=True),
    Column("pdbx_model_coordinates_db_code", Text, nullable=True),
    Column("pdbx_ideal_coordinates_details", Text, nullable=True),
    Column("pdbx_ideal_coordinates_missing_flag", Text, nullable=True),
    Column("pdbx_model_coordinates_missing_flag", Text, nullable=True),
    Column("pdbx_initial_date", Date, nullable=True),
    Column("pdbx_modified_date", Date, nullable=True),
    Column("pdbx_release_status", Text, nullable=True),
    Column("pdbx_processing_site", Text, nullable=True),
    Column("pdbx_pcm", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "id"),
    UniqueConstraint("comp_id", name="uq_cc_chem_comp_comp_id"),
    # FK: (comp_id) -> brief_summary(comp_id)
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
    Column("comp_id", Text, nullable=True),
    Column("alt_atom_id", Text, nullable=True),
    Column("atom_id", Text, nullable=True),
    Column("charge", Integer, nullable=True),
    Column("model_Cartn_x", Double, nullable=True),
    Column("model_Cartn_y", Double, nullable=True),
    Column("model_Cartn_z", Double, nullable=True),
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
    Column("pdbx_component_id", Integer, nullable=True),
    Column("pdbx_backbone_atom_flag", Text, nullable=True),
    Column("pdbx_n_terminal_atom_flag", Text, nullable=True),
    Column("pdbx_c_terminal_atom_flag", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "atom_id"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["alt_atom_id", "pdbx_stnd_atom_id"],
        "pkout": True,
    },
)

chem_comp_bond = Table(
    "chem_comp_bond",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_stereo_config", Text, nullable=True),
    Column("pdbx_aromatic_flag", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "atom_id_1", "atom_id_2"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id, atom_id_1) -> chem_comp_atom(comp_id, atom_id)
    # FK: (comp_id, atom_id_2) -> chem_comp_atom(comp_id, atom_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={"pkout": True},
)

pdbx_chem_comp_synonyms = Table(
    "pdbx_chem_comp_synonyms",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("provenance", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "ordinal"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["name", "type"],
        "pkout": True,
    },
)

pdbx_chem_comp_feature = Table(
    "pdbx_chem_comp_feature",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("value", Text, nullable=True),
    Column("source", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "type", "value", "source"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["support", "value", "source"],
        "pkout": True,
    },
)

pdbx_chem_comp_descriptor = Table(
    "pdbx_chem_comp_descriptor",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("descriptor", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("program", Text, nullable=True),
    Column("program_version", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "type", "program", "program_version"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["descriptor", "program", "program_version"],
        "pkout": True,
    },
)

pdbx_chem_comp_identifier = Table(
    "pdbx_chem_comp_identifier",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("identifier", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("program", Text, nullable=True),
    Column("program_version", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "type", "program", "program_version"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["identifier", "program", "program_version"],
        "pkout": True,
    },
)

pdbx_chem_comp_audit = Table(
    "pdbx_chem_comp_audit",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("processing_site", Text, nullable=True),
    Column("action_type", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "date", "action_type"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)

pdbx_chem_comp_related = Table(
    "pdbx_chem_comp_related",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("related_comp_id", Text, nullable=True),
    Column("relationship_type", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "related_comp_id", "relationship_type"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)

pdbx_chem_comp_atom_related = Table(
    "pdbx_chem_comp_atom_related",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("related_comp_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("atom_id", Text, nullable=True),
    Column("related_atom_id", Text, nullable=True),
    Column("related_type", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "ordinal", "related_comp_id"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    # FK: (comp_id, atom_id) -> chem_comp_atom(comp_id, atom_id)
    info={"pkout": True},
)

pdbx_chem_comp_pcm = Table(
    "pdbx_chem_comp_pcm",
    metadata,
    Column("comp_id", Text, nullable=True),
    Column("pcm_id", Integer, nullable=True),
    Column("modified_residue_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("category", Text, nullable=True),
    Column("position", Text, nullable=True),
    Column("polypeptide_position", Text, nullable=True),
    Column("comp_id_linking_atom", Text, nullable=True),
    Column("modified_residue_id_linking_atom", Text, nullable=True),
    Column("uniprot_specific_ptm_accession", Text, nullable=True),
    Column("uniprot_generic_ptm_accession", Text, nullable=True),
    PrimaryKeyConstraint("comp_id", "pcm_id"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["first_instance_model_db_code"],
        "pkout": True,
    },
)
