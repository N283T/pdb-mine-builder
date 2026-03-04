"""SQLAlchemy schema definition for ccmodel.

Auto-generated from schemas/ccmodel.def.yml by scripts/convert_yaml_to_sa.py.
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

metadata = MetaData(schema="ccmodel")
metadata.info = {"entry_pk": "model_id"}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("pdbx_initial_date", Date, nullable=True),
    Column("pdbx_modified_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("csd_id", Text, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("model_id"),
)

pdbx_chem_comp_model = Table(
    "pdbx_chem_comp_model",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    PrimaryKeyConstraint("model_id", "id"),
    UniqueConstraint("model_id", name="uq_ccmodel_pdbx_chem_comp_model_model_id"),
    # FK: (model_id) -> brief_summary(model_id)
)

pdbx_chem_comp_model_atom = Table(
    "pdbx_chem_comp_model_atom",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("atom_id", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    Column("charge", Integer, nullable=True),
    Column("model_Cartn_x", Double, nullable=True),
    Column("model_Cartn_y", Double, nullable=True),
    Column("model_Cartn_z", Double, nullable=True),
    Column("type_symbol", Text, nullable=True),
    PrimaryKeyConstraint("model_id", "atom_id"),
    # FK: (model_id) -> brief_summary(model_id)
    # FK: (model_id) -> pdbx_chem_comp_model(model_id)
    info={"pkout": True},
)

pdbx_chem_comp_model_bond = Table(
    "pdbx_chem_comp_model_bond",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("atom_id_1", Text, nullable=True),
    Column("atom_id_2", Text, nullable=True),
    Column("value_order", Text, nullable=True),
    Column("ordinal_id", Integer, nullable=True),
    PrimaryKeyConstraint("model_id", "atom_id_1", "atom_id_2"),
    # FK: (model_id) -> brief_summary(model_id)
    info={"pkout": True},
)

pdbx_chem_comp_model_feature = Table(
    "pdbx_chem_comp_model_feature",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("feature_name", Text, nullable=True),
    Column("feature_value", Text, nullable=True),
    PrimaryKeyConstraint("model_id", "feature_name"),
    # FK: (model_id) -> brief_summary(model_id)
    # FK: (model_id) -> pdbx_chem_comp_model(model_id)
    info={
        "keywords": ["feature_name", "feature_value"],
        "pkout": True,
    },
)

pdbx_chem_comp_model_descriptor = Table(
    "pdbx_chem_comp_model_descriptor",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("descriptor", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("model_id", "type"),
    # FK: (model_id) -> brief_summary(model_id)
    # FK: (model_id) -> pdbx_chem_comp_model(model_id)
    info={
        "keywords": ["descriptor"],
        "pkout": True,
    },
)

pdbx_chem_comp_model_audit = Table(
    "pdbx_chem_comp_model_audit",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("action_type", Text, nullable=True),
    PrimaryKeyConstraint("model_id", "date", "action_type"),
    # FK: (model_id) -> brief_summary(model_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)

pdbx_chem_comp_model_reference = Table(
    "pdbx_chem_comp_model_reference",
    metadata,
    Column("model_id", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    PrimaryKeyConstraint("model_id", "db_name", "db_code"),
    # FK: (model_id) -> brief_summary(model_id)
    # FK: (model_id) -> pdbx_chem_comp_model(model_id)
    info={
        "keywords": ["db_name", "db_code"],
        "pkout": True,
    },
)
