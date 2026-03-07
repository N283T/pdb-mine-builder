"""SQLAlchemy schema definition for ccmodel."""

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
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "docid",
        BigInteger,
        nullable=True,
        comment="Serial counter (unique integer) to represent the row id.",
    ),
    Column(
        "pdbx_initial_date",
        Date,
        nullable=True,
        comment="Inclusion date to the PDB of an entry",
    ),
    Column(
        "pdbx_modified_date",
        Date,
        nullable=True,
        comment="Modification date of an entry",
    ),
    Column(
        "update_date",
        DateTime,
        nullable=True,
        comment="Entry update date (within the RDB).",
    ),
    Column("comp_id", Text, nullable=True),
    Column("csd_id", Text, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True, comment="Array of keywords."),
    PrimaryKeyConstraint("model_id"),
)

pdbx_chem_comp_model = Table(
    "pdbx_chem_comp_model",
    metadata,
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "id",
        Text,
        nullable=True,
        comment="The value of _pdbx_chem_comp_model.id must uniquely identify each model instance the PDBX_CHEM_COMP_MODEL list.",
    ),
    Column(
        "comp_id",
        Text,
        nullable=True,
        comment="An identifier for chemical component definition.",
    ),
    PrimaryKeyConstraint("model_id", "id"),
    UniqueConstraint("model_id", name="uq_ccmodel_pdbx_chem_comp_model_model_id"),
    # FK: (model_id) -> brief_summary(model_id)
)

pdbx_chem_comp_model_atom = Table(
    "pdbx_chem_comp_model_atom",
    metadata,
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "atom_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_chem_comp_model_atom.atom_id uniquely identifies each atom in the PDBX_CHEM_COMP_MODEL_ATOM list.",
    ),
    Column(
        "ordinal_id",
        Integer,
        nullable=True,
        comment="The value of _pdbx_chem_comp_model_atom.ordinal_id is an ordinal identifer for each atom in the PDBX_CHEM_COMP_MODEL_ATOM list.",
    ),
    Column(
        "charge",
        Integer,
        nullable=True,
        comment="The net integer charge assigned to this atom. This is the formal charge assignment normally found in chemical diagrams.",
    ),
    Column(
        "model_Cartn_x",
        Double,
        nullable=True,
        comment="The x component of the coordinates for this atom in this component model specified as orthogonal angstroms.",
    ),
    Column(
        "model_Cartn_y",
        Double,
        nullable=True,
        comment="The y component of the coordinates for this atom in this component model specified as orthogonal angstroms.",
    ),
    Column(
        "model_Cartn_z",
        Double,
        nullable=True,
        comment="The z component of the coordinates for this atom in this component model specified as orthogonal angstroms.",
    ),
    Column(
        "type_symbol",
        Text,
        nullable=True,
        comment="The code used to identify the atom species representing this atom type. Normally this code is the element symbol.",
    ),
    PrimaryKeyConstraint("model_id", "atom_id"),
    # FK: (model_id) -> brief_summary(model_id)
    # FK: (model_id) -> pdbx_chem_comp_model(model_id)
    info={"pkout": True},
)

pdbx_chem_comp_model_bond = Table(
    "pdbx_chem_comp_model_bond",
    metadata,
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "atom_id_1",
        Text,
        nullable=True,
        comment="The ID of the first of the two atoms that define the bond. This data item is a pointer to _pdbx_chem_comp_model_atom.atom_id in the PDBX_CHEM_COMP_MODEL_ATOM category.",
    ),
    Column(
        "atom_id_2",
        Text,
        nullable=True,
        comment="The ID of the second of the two atoms that define the bond. This data item is a pointer to _pdbx_chem_comp_model_atom.atom_id in the PDBX_CHEM_COMP_MODEL_ATOM category.",
    ),
    Column(
        "value_order",
        Text,
        nullable=True,
        comment="The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order.",
    ),
    Column(
        "ordinal_id",
        Integer,
        nullable=True,
        comment="The value of _pdbx_chem_comp_model_bond.ordinal_id is an ordinal identifer for each atom in the PDBX_CHEM_COMP_MODEL_BOND list.",
    ),
    PrimaryKeyConstraint("model_id", "atom_id_1", "atom_id_2"),
    # FK: (model_id) -> brief_summary(model_id)
    info={"pkout": True},
)

pdbx_chem_comp_model_feature = Table(
    "pdbx_chem_comp_model_feature",
    metadata,
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "feature_name", Text, nullable=True, comment="The component model feature type."
    ),
    Column(
        "feature_value", Text, nullable=True, comment="The component feature value."
    ),
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
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "descriptor",
        Text,
        nullable=True,
        comment="This data item contains the descriptor value for this component.",
    ),
    Column(
        "type",
        Text,
        nullable=True,
        comment="This data item contains the descriptor type.",
    ),
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
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column(
        "date",
        Date,
        nullable=True,
        comment="The date associated with this audit record.",
    ),
    Column(
        "action_type",
        Text,
        nullable=True,
        comment="The action associated with this audit record.",
    ),
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
    Column(
        "model_id",
        Text,
        nullable=True,
        comment="Model ID of an entry. All tables/categories refer back to this ID in the brief_summary table.",
    ),
    Column("db_name", Text, nullable=True, comment="The component model feature type."),
    Column("db_code", Text, nullable=True, comment="The component feature value."),
    PrimaryKeyConstraint("model_id", "db_name", "db_code"),
    # FK: (model_id) -> brief_summary(model_id)
    # FK: (model_id) -> pdbx_chem_comp_model(model_id)
    info={
        "keywords": ["db_name", "db_code"],
        "pkout": True,
    },
)
