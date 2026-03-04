"""SQLAlchemy schema definition for sifts.

Auto-generated from schemas/sifts.def.yml by scripts/convert_yaml_to_sa.py.
"""

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)

metadata = MetaData(schema="sifts")
metadata.info = {"entry_pk": "pdbid"}


pdb_pfam = Table(
    "pdb_pfam",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("pfam_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "pfam_id"),
)

pdb_interpro = Table(
    "pdb_interpro",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("interpro_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "interpro_id"),
)

pdb_go = Table(
    "pdb_go",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("go_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "go_id"),
)

pdb_enzyme = Table(
    "pdb_enzyme",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("ec_number", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "ec_number"),
)

pdb_taxonomy = Table(
    "pdb_taxonomy",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("taxonomy_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "taxonomy_id"),
)

pdb_uniprot_short = Table(
    "pdb_uniprot_short",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("uniprot_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "uniprot_id"),
)

pdb_uniprot = Table(
    "pdb_uniprot",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("pdb_start", Integer, nullable=True),
    Column("pdb_end", Integer, nullable=True),
    Column("uniprot_id", Text, nullable=True),
    Column("uniprot_start", Integer, nullable=True),
    Column("uniprot_end", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "pdb_start", "pdb_end", "uniprot_id"),
)

pdb_cath = Table(
    "pdb_cath",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("cath_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "cath_id"),
)

pdb_scop = Table(
    "pdb_scop",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Integer, nullable=True),
    Column("scop_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "entity_id", "scop_id"),
)

pdb_pubmed = Table(
    "pdb_pubmed",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("pubmed_id", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "pubmed_id"),
)
