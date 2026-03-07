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
    Column("name", Text, nullable=True, comment="Name of the PRD family group."),
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
    Column(
        "id",
        Text,
        nullable=True,
        comment="The value of _citation.id must uniquely identify a record in the CITATION list. The _citation.id 'primary' should be used to indicate the citation that the author(s) consider to be the most pertinent to the contents of the data block. Note that this item need not be a number; it can be any unique identifier.",
    ),
    Column(
        "journal_abbrev",
        Text,
        nullable=True,
        comment="Abbreviated name of the cited journal as given in the Chemical Abstracts Service Source Index.",
    ),
    Column(
        "journal_volume",
        Text,
        nullable=True,
        comment="Volume number of the journal cited; relevant for journal articles.",
    ),
    Column(
        "page_first",
        Text,
        nullable=True,
        comment="The first page of the citation; relevant for journal articles, books and book chapters.",
    ),
    Column(
        "page_last",
        Text,
        nullable=True,
        comment="The last page of the citation; relevant for journal articles, books and book chapters.",
    ),
    Column(
        "title",
        Text,
        nullable=True,
        comment="The title of the citation; relevant for journal articles, books and book chapters.",
    ),
    Column(
        "year",
        Integer,
        nullable=True,
        comment="The year of the citation; relevant for journal articles, books and book chapters.",
    ),
    Column(
        "pdbx_database_id_DOI",
        Text,
        nullable=True,
        comment="Document Object Identifier used by doi.org to uniquely specify bibliographic entry.",
    ),
    Column(
        "pdbx_database_id_PubMed",
        Integer,
        nullable=True,
        comment="Ascession number used by PubMed to categorize a specific bibliographic entry.",
    ),
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
    Column(
        "citation_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _citation.id in the CITATION category.",
    ),
    Column(
        "name",
        Text,
        nullable=True,
        comment="Name of an author of the citation; relevant for journal articles, books and book chapters. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s).",
    ),
    Column(
        "ordinal",
        Integer,
        nullable=True,
        comment="This data item defines the order of the author's name in the list of authors of a citation.",
    ),
    PrimaryKeyConstraint("family_prd_id", "citation_id", "name", "ordinal"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id, citation_id) -> citation(family_prd_id, id)
    info={"keywords": ["name", "identifier_ORCID"]},
)

pdbx_reference_molecule_family = Table(
    "pdbx_reference_molecule_family",
    metadata,
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity.family_prd_id must uniquely identify a record in the PDBX_REFERENCE_MOLECULE_FAMILY list. By convention this ID uniquely identifies the reference family in in the PDB reference dictionary. The ID has the template form FAM_dddddd (e.g. FAM_000001)",
    ),
    Column("name", Text, nullable=True, comment="The entity family name."),
    Column(
        "release_status",
        Text,
        nullable=True,
        comment="Assigns the current PDB release status for this family.",
    ),
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
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_list.family_prd_id is a reference to _pdbx_reference_molecule_family.family_prd_id' in category PDBX_REFERENCE_MOLECULE_FAMILY.",
    ),
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_list.prd_id is the unique identifier for the reference molecule in this family. By convention this ID uniquely identifies the reference molecule in in the PDB reference dictionary. The ID has the template form PRD_dddddd (e.g. PRD_000001)",
    ),
    PrimaryKeyConstraint("family_prd_id", "prd_id"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id) -> pdbx_reference_molecule_family(family_prd_id)
    info={"pkout": True},
)

pdbx_reference_molecule_synonyms = Table(
    "pdbx_reference_molecule_synonyms",
    metadata,
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_synonyms.family_prd_id is a reference to _pdbx_reference_molecule_list.family_prd_id in category PDBX_REFERENCE_MOLECULE_FAMILY_LIST.",
    ),
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_synonyms.prd_id is a reference _pdbx_reference_molecule.prd_id in the PDBX_REFERENCE_MOLECULE category.",
    ),
    Column(
        "ordinal",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_synonyms.ordinal is an ordinal to distinguish synonyms for this entity.",
    ),
    Column("name", Text, nullable=True, comment="A synonym name for the entity."),
    Column(
        "source",
        Text,
        nullable=True,
        comment="The source of this synonym name for the entity.",
    ),
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
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_annotation.family_prd_id is a reference to _pdbx_reference_molecule_list.family_prd_id in category PDBX_REFERENCE_MOLECULE_FAMILY_LIST.",
    ),
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _pdbx_reference_molecule.prd_id in the PDB_REFERENCE_MOLECULE category.",
    ),
    Column(
        "ordinal",
        Integer,
        nullable=True,
        comment="This data item distinguishes anotations for this entity.",
    ),
    Column(
        "text",
        Text,
        nullable=True,
        comment="Text describing the annotation for this entity.",
    ),
    Column("type", Text, nullable=True, comment="Type of annotation for this entity."),
    Column(
        "source",
        Text,
        nullable=True,
        comment="The source of the annoation for this entity.",
    ),
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
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_features.family_prd_id is a reference to _pdbx_reference_molecule_list.family_prd_id in category PDBX_REFERENCE_MOLECULE_FAMILY_LIST.",
    ),
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_features.prd_id is a reference _pdbx_reference_molecule.prd_id in the PDBX_REFERENCE_MOLECULE category.",
    ),
    Column(
        "ordinal",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_features.ordinal distinguishes each feature for this entity.",
    ),
    Column(
        "source_ordinal",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_features.source_ordinal provides the priority order of features from a particular source or database.",
    ),
    Column("type", Text, nullable=True, comment="The entity feature type."),
    Column("value", Text, nullable=True, comment="The entity feature value."),
    Column(
        "source",
        Text,
        nullable=True,
        comment="The information source for the component feature.",
    ),
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
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_related_structures.family_prd_id is a reference to _pdbx_reference_molecule_list.family_prd_id in category PDBX_REFERENCE_MOLECULE_FAMILY_LIST.",
    ),
    Column(
        "ordinal",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_molecule_related_structures.ordinal distinguishes related structural data for each entity.",
    ),
    Column(
        "db_name",
        Text,
        nullable=True,
        comment="The database name for the related structure reference.",
    ),
    Column(
        "db_code",
        Text,
        nullable=True,
        comment="The database identifier code for the related structure reference.",
    ),
    Column(
        "db_accession",
        Text,
        nullable=True,
        comment="The database accession code for the related structure reference.",
    ),
    Column(
        "name",
        Text,
        nullable=True,
        comment="The chemical name for the structure entry in the related database",
    ),
    Column(
        "formula",
        Text,
        nullable=True,
        comment="The formula for the reference entity. Formulae are written according to the rules: 1. Only recognised element symbols may be used. 2. Each element symbol is followed by a 'count' number. A count of '1' may be omitted. 3. A space or parenthesis must separate each element symbol and its count, but in general parentheses are not used. 4. The order of elements depends on whether or not carbon is present. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts.",
    ),
    Column(
        "citation_id",
        Text,
        nullable=True,
        comment="A link to related reference information in the citation category.",
    ),
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
    Column(
        "family_prd_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _pdbx_reference_molecule_family.family_prd_id in the pdbx_reference_molecule category.",
    ),
    Column(
        "date",
        Date,
        nullable=True,
        comment="The date associated with this audit record.",
    ),
    Column(
        "processing_site",
        Text,
        nullable=True,
        comment="An identifier for the wwPDB site creating or modifying the family.",
    ),
    Column(
        "action_type",
        Text,
        nullable=True,
        comment="The action associated with this audit record.",
    ),
    PrimaryKeyConstraint("family_prd_id", "date", "action_type"),
    # FK: (family_prd_id) -> brief_summary(family_prd_id)
    # FK: (family_prd_id) -> pdbx_reference_molecule_family(family_prd_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)
