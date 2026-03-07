"""SQLAlchemy schema definition for prd."""

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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "docid",
        BigInteger,
        nullable=True,
        comment="Serial counter (unique integer) to represent the row id.",
    ),
    Column("name", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("description", Text, nullable=True),
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
    Column("keywords", ARRAY(Text), nullable=True, comment="Array of keywords."),
    PrimaryKeyConstraint("prd_id"),
    Index("ix_prd_brief_summary_docid", "docid"),
    Index("ix_prd_brief_summary_keywords", "keywords"),
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "formula",
        Text,
        nullable=True,
        comment="The formula for the chemical component. Formulae are written according to the following rules: (1) Only recognized element symbols may be used. (2) Each element symbol is followed by a 'count' number. A count of '1' may be omitted. (3) A space or parenthesis must separate each cluster of (element symbol + count), but in general parentheses are not used. (4) The order of elements depends on whether carbon is present or not. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts.",
    ),
    Column(
        "formula_weight",
        Double,
        nullable=True,
        comment="Formula mass in daltons of the chemical component.",
    ),
    Column(
        "id",
        Text,
        nullable=True,
        comment="The value of _chem_comp.id must uniquely identify each item in the CHEM_COMP list. For protein polymer entities, this is the three-letter code for the amino acid. For nucleic acid polymer entities, this is the one-letter code for the base.",
    ),
    Column("name", Text, nullable=True, comment="The full name of the component."),
    Column(
        "type",
        Text,
        nullable=True,
        comment="For standard polymer components, the type of the monomer. Note that monomers that will form polymers are of three types: linking monomers, monomers with some type of N-terminal (or 5') cap and monomers with some type of C-terminal (or 3') cap.",
    ),
    Column(
        "pdbx_release_status",
        Text,
        nullable=True,
        comment="This data item holds the current release status for the component.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "alt_atom_id",
        Text,
        nullable=True,
        comment="An alternative identifier for the atom. This data item would be used in cases where alternative nomenclatures exist for labelling atoms in a group.",
    ),
    Column(
        "atom_id",
        Text,
        nullable=True,
        comment="The value of _chem_comp_atom.atom_id must uniquely identify each atom in each monomer in the CHEM_COMP_ATOM list. The atom identifiers need not be unique over all atoms in the data block; they need only be unique for each atom in a component. Note that this item need not be a number; it can be any unique identifier.",
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
        comment="The x component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list.",
    ),
    Column(
        "model_Cartn_y",
        Double,
        nullable=True,
        comment="The y component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list.",
    ),
    Column(
        "model_Cartn_z",
        Double,
        nullable=True,
        comment="The z component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list.",
    ),
    Column(
        "comp_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category.",
    ),
    Column(
        "type_symbol",
        Text,
        nullable=True,
        comment="The code used to identify the atom species representing this atom type. Normally this code is the element symbol.",
    ),
    Column(
        "pdbx_align",
        Integer,
        nullable=True,
        comment="Atom name alignment offset in PDB atom field.",
    ),
    Column(
        "pdbx_ordinal",
        Integer,
        nullable=True,
        comment="Ordinal index for the component atom list.",
    ),
    Column(
        "pdbx_component_atom_id",
        Text,
        nullable=True,
        comment="The atom identifier in the subcomponent where a larger component has been divided subcomponents.",
    ),
    Column(
        "pdbx_component_comp_id",
        Text,
        nullable=True,
        comment="The component identifier for the subcomponent where a larger component has been divided subcomponents.",
    ),
    Column(
        "pdbx_model_Cartn_x_ideal",
        Double,
        nullable=True,
        comment="An alternative x component of the coordinates for this atom in this component specified as orthogonal angstroms.",
    ),
    Column(
        "pdbx_model_Cartn_y_ideal",
        Double,
        nullable=True,
        comment="An alternative y component of the coordinates for this atom in this component specified as orthogonal angstroms.",
    ),
    Column(
        "pdbx_model_Cartn_z_ideal",
        Double,
        nullable=True,
        comment="An alternative z component of the coordinates for this atom in this component specified as orthogonal angstroms.",
    ),
    Column(
        "pdbx_stereo_config",
        Text,
        nullable=True,
        comment="The chiral configuration of the atom that is a chiral center.",
    ),
    Column(
        "pdbx_aromatic_flag",
        Text,
        nullable=True,
        comment="A flag indicating an aromatic atom.",
    ),
    Column(
        "pdbx_leaving_atom_flag",
        Text,
        nullable=True,
        comment="A flag indicating a leaving atom.",
    ),
    Column(
        "pdbx_residue_numbering",
        Integer,
        nullable=True,
        comment="Preferred residue numbering in the BIRD definition.",
    ),
    Column(
        "pdbx_polymer_type",
        Text,
        nullable=True,
        comment="Is the atom in a polymer or non-polymer subcomponent in the BIRD definition.",
    ),
    Column(
        "pdbx_ref_id",
        Text,
        nullable=True,
        comment="A reference to _pdbx_reference_entity_list.ref_entity_id",
    ),
    Column(
        "pdbx_component_id",
        Integer,
        nullable=True,
        comment="A reference to _pdbx_reference_entity_list.component_id",
    ),
    Column(
        "pdbx_backbone_atom_flag",
        Text,
        nullable=True,
        comment="A flag indicating the backbone atoms in polypeptide units.",
    ),
    Column(
        "pdbx_n_terminal_atom_flag",
        Text,
        nullable=True,
        comment="A flag indicating the N-terminal group atoms in polypeptide units.",
    ),
    Column(
        "pdbx_c_terminal_atom_flag",
        Text,
        nullable=True,
        comment="A flag indicating the C-terminal group atoms in polypeptide units.",
    ),
    PrimaryKeyConstraint("prd_id", "comp_id", "atom_id"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
    info={"keywords": ["alt_atom_id", "pdbx_stnd_atom_id"]},
)

chem_comp_bond = Table(
    "chem_comp_bond",
    metadata,
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "atom_id_1",
        Text,
        nullable=True,
        comment="The ID of the first of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category.",
    ),
    Column(
        "atom_id_2",
        Text,
        nullable=True,
        comment="The ID of the second of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category.",
    ),
    Column(
        "comp_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category.",
    ),
    Column(
        "value_order",
        Text,
        nullable=True,
        comment="The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order.",
    ),
    Column(
        "pdbx_ordinal",
        Integer,
        nullable=True,
        comment="Ordinal index for the component bond list.",
    ),
    Column(
        "pdbx_stereo_config",
        Text,
        nullable=True,
        comment="Stereochemical configuration across a double bond.",
    ),
    Column(
        "pdbx_aromatic_flag",
        Text,
        nullable=True,
        comment="A flag indicating an aromatic bond.",
    ),
    PrimaryKeyConstraint("prd_id", "comp_id", "atom_id_1", "atom_id_2"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id, atom_id_1) -> chem_comp_atom(prd_id, comp_id, atom_id)
    # FK: (prd_id, comp_id, atom_id_2) -> chem_comp_atom(prd_id, comp_id, atom_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
)

pdbx_chem_comp_descriptor = Table(
    "pdbx_chem_comp_descriptor",
    metadata,
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "comp_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category.",
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
    Column(
        "program",
        Text,
        nullable=True,
        comment="This data item contains the name of the program or library used to compute the descriptor.",
    ),
    Column(
        "program_version",
        Text,
        nullable=True,
        comment="This data item contains the version of the program or library used to compute the descriptor.",
    ),
    PrimaryKeyConstraint("prd_id", "comp_id", "type", "program", "program_version"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
    info={"keywords": ["descriptor", "program", "program_version"]},
)

pdbx_chem_comp_identifier = Table(
    "pdbx_chem_comp_identifier",
    metadata,
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "comp_id",
        Text,
        nullable=True,
        comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category.",
    ),
    Column(
        "identifier",
        Text,
        nullable=True,
        comment="This data item contains the identifier value for this component.",
    ),
    Column(
        "type",
        Text,
        nullable=True,
        comment="This data item contains the identifier type.",
    ),
    Column(
        "program",
        Text,
        nullable=True,
        comment="This data item contains the name of the program or library used to compute the identifier.",
    ),
    Column(
        "program_version",
        Text,
        nullable=True,
        comment="This data item contains the version of the program or library used to compute the identifier.",
    ),
    PrimaryKeyConstraint("prd_id", "comp_id", "type", "program", "program_version"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, comp_id) -> chem_comp(prd_id, id)
    info={"keywords": ["identifier", "program", "program_version"]},
)

pdbx_reference_molecule = Table(
    "pdbx_reference_molecule",
    metadata,
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "formula_weight",
        Double,
        nullable=True,
        comment="Formula mass in daltons of the entity.",
    ),
    Column(
        "formula",
        Text,
        nullable=True,
        comment="The formula for the reference entity. Formulae are written according to the rules: 1. Only recognised element symbols may be used. 2. Each element symbol is followed by a 'count' number. A count of '1' may be omitted. 3. A space or parenthesis must separate each element symbol and its count, but in general parentheses are not used. 4. The order of elements depends on whether or not carbon is present. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts.",
    ),
    Column(
        "type",
        Text,
        nullable=True,
        comment="Defines the structural classification of the entity.",
    ),
    Column(
        "type_evidence_code",
        Text,
        nullable=True,
        comment="Evidence for the assignment of _pdbx_reference_molecule.type",
    ),
    Column(
        "class",
        Text,
        nullable=True,
        comment="Broadly defines the function of the entity.",
    ),
    Column(
        "class_evidence_code",
        Text,
        nullable=True,
        comment="Evidence for the assignment of _pdbx_reference_molecule.class",
    ),
    Column("name", Text, nullable=True, comment="A name of the entity."),
    Column(
        "represent_as",
        Text,
        nullable=True,
        comment="Defines how this entity is represented in PDB data files.",
    ),
    Column(
        "chem_comp_id",
        Text,
        nullable=True,
        comment="For entities represented as single molecules, the identifier corresponding to the chemical definition for the molecule.",
    ),
    Column(
        "compound_details",
        Text,
        nullable=True,
        comment="Special details about this molecule.",
    ),
    Column("description", Text, nullable=True, comment="Description of this molecule."),
    Column(
        "representative_PDB_id_code",
        Text,
        nullable=True,
        comment="The PDB accession code for the entry containing a representative example of this molecule.",
    ),
    Column(
        "release_status",
        Text,
        nullable=True,
        comment="Defines the current PDB release status for this molecule definition.",
    ),
    Column(
        "replaces",
        Text,
        nullable=True,
        comment="Assigns the identifier for the reference molecule which have been replaced by this reference molecule. Multiple molecule identifier codes should be separated by commas.",
    ),
    Column(
        "replaced_by",
        Text,
        nullable=True,
        comment="Assigns the identifier of the reference molecule that has replaced this molecule.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity_list.ref_entity_id is a unique identifier the a constituent entity within this reference molecule.",
    ),
    Column(
        "type",
        Text,
        nullable=True,
        comment="Defines the polymer characteristic of the entity.",
    ),
    Column(
        "details", Text, nullable=True, comment="Additional details about this entity."
    ),
    Column(
        "component_id",
        Integer,
        nullable=True,
        comment="The component number of this entity within the molecule.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity_nonpoly.ref_entity_id is a reference to _pdbx_reference_entity_list.ref_entity_id in PDBX_REFERENCE_ENTITY_LIST category.",
    ),
    Column("name", Text, nullable=True, comment="A name of the non-polymer entity."),
    Column(
        "chem_comp_id",
        Text,
        nullable=True,
        comment="For non-polymer entities, the identifier corresponding to the chemical definition for the molecule.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "link_id",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_entity_link.link_id uniquely identifies linkages between entities with a molecule.",
    ),
    Column(
        "ref_entity_id_1",
        Text,
        nullable=True,
        comment="The reference entity id of the first of the two entities joined by the linkage. This data item is a pointer to _pdbx_reference_entity_list.ref_entity_id in the PDBX_REFERENCE_ENTITY_LIST category.",
    ),
    Column(
        "ref_entity_id_2",
        Text,
        nullable=True,
        comment="The reference entity id of the second of the two entities joined by the linkage. This data item is a pointer to _pdbx_reference_entity_list.ref_entity_id in the PDBX_REFERENCE_ENTITY_LIST category.",
    ),
    Column(
        "entity_seq_num_1",
        Integer,
        nullable=True,
        comment="For a polymer entity, the sequence number in the first of the two entities containing the linkage. This data item is a pointer to _pdbx_reference_entity_poly_seq.num in the PDBX_REFERENCE_ENTITY_POLY_SEQ category.",
    ),
    Column(
        "entity_seq_num_2",
        Integer,
        nullable=True,
        comment="For a polymer entity, the sequence number in the second of the two entities containing the linkage. This data item is a pointer to _pdbx_reference_entity_poly_seq.num in the PDBX_REFERENCE_ENTITY_POLY_SEQ category.",
    ),
    Column(
        "comp_id_1",
        Text,
        nullable=True,
        comment="The component identifier in the first of the two entities containing the linkage. For polymer entities, this data item is a pointer to _pdbx_reference_entity_poly_seq.mon_id in the PDBX_REFERENCE_ENTITY_POLY_SEQ category. For non-polymer entities, this data item is a pointer to _pdbx_reference_entity_nonpoly.chem_comp_id in the PDBX_REFERENCE_ENTITY_NONPOLY category.",
    ),
    Column(
        "comp_id_2",
        Text,
        nullable=True,
        comment="The component identifier in the second of the two entities containing the linkage. For polymer entities, this data item is a pointer to _pdbx_reference_entity_poly_seq.mon_id in the PDBX_REFERENCE_ENTITY_POLY_SEQ category. For non-polymer entities, this data item is a pointer to _pdbx_reference_entity_nonpoly.chem_comp_id in the PDBX_REFERENCE_ENTITY_NONPOLY category.",
    ),
    Column(
        "atom_id_1",
        Text,
        nullable=True,
        comment="The atom identifier/name in the first of the two entities containing the linkage.",
    ),
    Column(
        "atom_id_2",
        Text,
        nullable=True,
        comment="The atom identifier/name in the second of the two entities containing the linkage.",
    ),
    Column(
        "value_order",
        Text,
        nullable=True,
        comment="The bond order target for the chemical linkage.",
    ),
    Column(
        "component_1",
        Integer,
        nullable=True,
        comment="The entity component identifier for the first of two entities containing the linkage.",
    ),
    Column(
        "component_2",
        Integer,
        nullable=True,
        comment="The entity component identifier for the second of two entities containing the linkage.",
    ),
    Column(
        "link_class",
        Text,
        nullable=True,
        comment="A code indicating the entity types involved in the linkage.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "link_id",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_entity_poly_link.link_id uniquely identifies a linkage within a polymer entity.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The reference entity id of the polymer entity containing the linkage. This data item is a pointer to _pdbx_reference_entity_poly.ref_entity_id in the PDBX_REFERENCE_ENTITY_POLY category.",
    ),
    Column(
        "component_id",
        Integer,
        nullable=True,
        comment="The entity component identifier entity containing the linkage.",
    ),
    Column(
        "entity_seq_num_1",
        Integer,
        nullable=True,
        comment="For a polymer entity, the sequence number in the first of the two components making the linkage. This data item is a pointer to _pdbx_reference_entity_poly_seq.num in the PDBX_REFERENCE_ENTITY_POLY_SEQ category.",
    ),
    Column(
        "entity_seq_num_2",
        Integer,
        nullable=True,
        comment="For a polymer entity, the sequence number in the second of the two components making the linkage. This data item is a pointer to _pdbx_reference_entity_poly_seq.num in the PDBX_REFERENCE_ENTITY_POLY_SEQ category.",
    ),
    Column(
        "comp_id_1",
        Text,
        nullable=True,
        comment="The component identifier in the first of the two components making the linkage. This data item is a pointer to _pdbx_reference_entity_poly_seq.mon_id in the PDBX_REFERENCE_ENTITY_POLY_SEQ category.",
    ),
    Column(
        "comp_id_2",
        Text,
        nullable=True,
        comment="The component identifier in the second of the two components making the linkage. This data item is a pointer to _pdbx_reference_entity_poly_seq.mon_id in the PDBX_REFERENCE_ENTITY_POLY_SEQ category.",
    ),
    Column(
        "atom_id_1",
        Text,
        nullable=True,
        comment="The atom identifier/name in the first of the two components making the linkage.",
    ),
    Column(
        "atom_id_2",
        Text,
        nullable=True,
        comment="The atom identifier/name in the second of the two components making the linkage.",
    ),
    Column(
        "value_order",
        Text,
        nullable=True,
        comment="The bond order target for the non-standard linkage.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity_poly.ref_entity_id is a reference to _pdbx_reference_entity_list.ref_entity_id in PDBX_REFERENCE_ENTITY_LIST category.",
    ),
    Column("type", Text, nullable=True, comment="The type of the polymer."),
    Column(
        "db_code",
        Text,
        nullable=True,
        comment="The database code for this source information",
    ),
    Column(
        "db_name",
        Text,
        nullable=True,
        comment="The database name for this source information",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity_poly_seq.ref_entity_id is a reference to _pdbx_reference_entity_poly.ref_entity_id in PDBX_REFERENCE_ENTITY_POLY category.",
    ),
    Column(
        "mon_id",
        Text,
        nullable=True,
        comment="This data item is the chemical component identifier of monomer.",
    ),
    Column(
        "parent_mon_id",
        Text,
        nullable=True,
        comment="This data item is the chemical component identifier for the parent component corresponding to this monomer.",
    ),
    Column(
        "num",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_entity_poly_seq.num must uniquely and sequentially identify a record in the PDBX_REFERENCE_ENTITY_POLY_SEQ list. This value is conforms to author numbering conventions and does not map directly to the numbering conventions used for _entity_poly_seq.num.",
    ),
    Column(
        "observed",
        Text,
        nullable=True,
        comment="A flag to indicate that this monomer is observed in the instance example.",
    ),
    Column(
        "hetero",
        Text,
        nullable=True,
        comment="A flag to indicate that sequence heterogeneity at this monomer position.",
    ),
    PrimaryKeyConstraint("prd_id", "ref_entity_id", "num", "mon_id", "hetero"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id, ref_entity_id) -> pdbx_reference_entity_poly(prd_id, ref_entity_id)
    info={"pkout": True},
)

pdbx_reference_entity_sequence = Table(
    "pdbx_reference_entity_sequence",
    metadata,
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity_sequence.ref_entity_id is a reference to _pdbx_reference_entity_list.ref_entity_id in PDBX_REFERENCE_ENTITY_LIST category.",
    ),
    Column("type", Text, nullable=True, comment="The monomer type for the sequence."),
    Column(
        "NRP_flag",
        Text,
        nullable=True,
        comment="A flag to indicate a non-ribosomal entity.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "ref_entity_id",
        Text,
        nullable=True,
        comment="The value of _pdbx_reference_entity_src_nat.ref_entity_id is a reference to _pdbx_reference_entity_list.ref_entity_id in PDBX_REFERENCE_ENTITY_LIST category.",
    ),
    Column(
        "ordinal",
        Integer,
        nullable=True,
        comment="The value of _pdbx_reference_entity_src_nat.ordinal distinguishes source details for this entity.",
    ),
    Column(
        "organism_scientific",
        Text,
        nullable=True,
        comment="The scientific name of the organism from which the entity was isolated.",
    ),
    Column(
        "strain",
        Text,
        nullable=True,
        comment="The strain of the organism from which the entity was isolated.",
    ),
    Column(
        "taxid",
        Text,
        nullable=True,
        comment="The NCBI TaxId of the organism from which the entity was isolated.",
    ),
    Column(
        "db_code",
        Text,
        nullable=True,
        comment="The database code for this source information",
    ),
    Column(
        "db_name",
        Text,
        nullable=True,
        comment="The database name for this source information",
    ),
    Column(
        "source", Text, nullable=True, comment="The data source for this information."
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
    ),
    Column(
        "seq", Text, nullable=True, comment="The subcomponent sequence for the entity."
    ),
    Column(
        "chem_comp_id",
        Text,
        nullable=True,
        comment="For entities represented as single molecules, the identifier corresponding to the chemical definition for the molecule.",
    ),
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
    Column(
        "prd_id",
        Text,
        nullable=True,
        comment="PRDID of an entry. All tables/categories refer back to the PRDID in the brief_summary table.",
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
        comment="An identifier for the wwPDB site creating or modifying the molecule.",
    ),
    Column(
        "action_type",
        Text,
        nullable=True,
        comment="The action associated with this audit record.",
    ),
    PrimaryKeyConstraint("prd_id", "date", "action_type"),
    # FK: (prd_id) -> brief_summary(prd_id)
    # FK: (prd_id) -> pdbx_reference_molecule(prd_id)
    info={
        "keywords": ["details"],
        "pkout": True,
    },
)
