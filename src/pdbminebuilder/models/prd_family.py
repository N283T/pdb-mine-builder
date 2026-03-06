"""SQLAlchemy schema definition for prd_family."""

from sqlalchemy import (
    ARRAY,
    Column,
    Date,
    DateTime,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)

metadata = MetaData(schema="prd_family")
metadata.info = {
    "entry_pk": "family_prd_id",
    "skip_foreign_keys": True,
}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("pdbx_initial_date", Date, nullable=True),
    Column("pdbx_modified_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("family_prd_id"),
)

citation = Table(
    "citation",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("journal_abbrev", Text, nullable=True),
    Column("journal_volume", Text, nullable=True),
    Column("page_first", Text, nullable=True),
    Column("page_last", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("year", Integer, nullable=True),
    Column("pdbx_database_id_DOI", Text, nullable=True),
    Column("pdbx_database_id_PubMed", Integer, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "id"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
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
    Column("family_prd_id", Text, nullable=True),
    Column("citation_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "citation_id", "name", "ordinal"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id, citation_id) -> citation(family_prd_id, id)
    info={"keywords": ["name", "identifier_ORCID"]},
)

pdbx_reference_molecule_family = Table(
    "pdbx_reference_molecule_family",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("release_status", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    info={
        "keywords": ["name"],
        "pkout": True,
    },
)

pdbx_reference_molecule_list = Table(
    "pdbx_reference_molecule_list",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("prd_id", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "prd_id"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id) -> pdbx_reference_molecule_family(family_prd_id)
    info={"pkout": True},
)

pdbx_reference_molecule_synonyms = Table(
    "pdbx_reference_molecule_synonyms",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("prd_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("source", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "prd_id", "ordinal"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id, prd_id) -> pdbx_reference_molecule_list(family_prd_id, prd_id)
    info={
        "keywords": ["name", "source"],
        "pkout": True,
    },
)

pdbx_reference_molecule_annotation = Table(
    "pdbx_reference_molecule_annotation",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("prd_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("text", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("source", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "ordinal"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    info={
        "keywords": ["text", "type", "support", "source"],
        "pkout": True,
    },
)

pdbx_reference_molecule_features = Table(
    "pdbx_reference_molecule_features",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("prd_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("source_ordinal", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("value", Text, nullable=True),
    Column("source", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "prd_id", "ordinal"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id, prd_id) -> pdbx_reference_molecule_list(family_prd_id, prd_id)
    info={
        "keywords": ["type", "value", "source"],
        "pkout": True,
    },
)

pdbx_reference_molecule_related_structures = Table(
    "pdbx_reference_molecule_related_structures",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    Column("db_accession", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("citation_id", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "ordinal"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    info={
        "keywords": ["db_name", "db_code", "db_accession", "name", "formula"],
        "pkout": True,
    },
)

pdbx_family_prd_audit = Table(
    "pdbx_family_prd_audit",
    metadata,
    Column("family_prd_id", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("processing_site", Text, nullable=True),
    Column("action_type", Text, nullable=True),
    PrimaryKeyConstraint("family_prd_id", "date", "action_type"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id) -> pdbx_reference_molecule_family(family_prd_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)
