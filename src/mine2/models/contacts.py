"""SQLAlchemy schema definition for contacts.

Auto-generated from schemas/contacts.def.yml by scripts/convert_yaml_to_sa.py.
"""

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)

metadata = MetaData(schema="contacts")
metadata.info = {"entry_pk": "pdbid"}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("modification_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    PrimaryKeyConstraint("pdbid"),
)

list = Table(
    "list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("label_asym_id_1", Text, nullable=True),
    Column("label_asym_id_2", Text, nullable=True),
    Column("label_seq_id_1", Integer, nullable=True),
    Column("label_seq_id_2", Integer, nullable=True),
    Column("label_comp_id_1", Text, nullable=True),
    Column("label_comp_id_2", Text, nullable=True),
    Column("distance", Float, nullable=True),
    PrimaryKeyConstraint(
        "pdbid",
        "label_asym_id_1",
        "label_asym_id_2",
        "label_seq_id_1",
        "label_seq_id_2",
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
)
