"""SQLAlchemy schema definition for chem (unified chemical compounds)."""

from sqlalchemy import (
    ARRAY,
    Column,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)

metadata = MetaData(schema="chem")
metadata.info = {
    "entry_pk": "id",
    "skip_foreign_keys": True,
}

compounds = Table(
    "compounds",
    metadata,
    Column(
        "id",
        Text,
        nullable=False,
        comment="Compound identifier (comp_id for cc, prd_id for prd)",
    ),
    Column(
        "source",
        Text,
        nullable=False,
        comment="Source schema: 'cc' or 'prd'",
    ),
    Column(
        "canonical_smiles",
        Text,
        nullable=True,
        comment="Canonical SMILES string",
    ),
    Column(
        "name",
        Text,
        nullable=True,
        comment="Compound name",
    ),
    Column(
        "formula",
        Text,
        nullable=True,
        comment="Molecular formula",
    ),
    Column(
        "cc_comp_ids",
        ARRAY(Text),
        nullable=True,
        comment="Linked CCD comp_ids for cross-reference",
    ),
    PrimaryKeyConstraint("source", "id"),
)
