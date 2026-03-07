"""SQLAlchemy schema definition for contacts."""

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
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("modification_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    PrimaryKeyConstraint("pdbid"),
)

list = Table(
    "list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("label_asym_id_1", Text, nullable=True, comment="Chain ID of the first residue/molecule"),
    Column("label_asym_id_2", Text, nullable=True, comment="Chain ID of the second residue/molecule"),
    Column("label_seq_id_1", Integer, nullable=True, comment="Sequence ID of the first residue/molecule"),
    Column("label_seq_id_2", Integer, nullable=True, comment="Sequence ID of the second residue/molecule"),
    Column("label_comp_id_1", Text, nullable=True, comment="Residue/molecule name of the first residue"),
    Column("label_comp_id_2", Text, nullable=True, comment="Residue/molecule name of the second residue"),
    Column("distance", Float, nullable=True, comment="Minimal distance between the two residues/molecules"),
    PrimaryKeyConstraint(
        "pdbid",
        "label_asym_id_1",
        "label_asym_id_2",
        "label_seq_id_1",
        "label_seq_id_2",
    ),
    # FK: (pdbid) -> brief_summary(pdbid)
)
