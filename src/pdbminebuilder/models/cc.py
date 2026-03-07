"""SQLAlchemy schema definition for cc."""

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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("docid", BigInteger, nullable=True, comment="Serial counter (unique integer) to represent the row id."),
    Column("pdbx_initial_date", Date, nullable=True, comment="Date that the entry was defined in the dictionary"),
    Column("release_date", Date, nullable=True, comment="Date at which the entry was officially released"),
    Column("pdbx_modified_date", Date, nullable=True, comment="Modification date of an entry"),
    Column("update_date", DateTime, nullable=True, comment="Entry update date (within the RDB)."),
    Column("name", Text, nullable=True, comment="Name of an entry."),
    Column("formula", Text, nullable=True, comment="Chemical formula of an entry."),
    Column("pdbx_synonyms", ARRAY(Text), nullable=True, comment="Known synonyms of an entry."),
    Column("identifier", Text, nullable=True, comment="Identifier of an entry."),
    Column("smiles", ARRAY(Text), nullable=True, comment="SMILES representations of an entry."),
    Column("inchi", ARRAY(Text), nullable=True, comment="InChI representations of an entry."),
    Column("canonical_smiles", Text, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True, comment="Array of keywords."),
    PrimaryKeyConstraint("comp_id"),
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("formula", Text, nullable=True, comment="The formula for the chemical component. Formulae are written according to the following rules: (1) Only recognized element symbols may be used. (2) Each element symbol is followed by a 'count' number. A count of '1' may be omitted. (3) A space or parenthesis must separate each cluster of (element symbol + count), but in general parentheses are not used. (4) The order of elements depends on whether carbon is present or not. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts."),
    Column("formula_weight", Double, nullable=True, comment="Formula mass in daltons of the chemical component."),
    Column("id", Text, nullable=True, comment="The value of _chem_comp.id must uniquely identify each item in the CHEM_COMP list. For protein polymer entities, this is the three-letter code for the amino acid. For nucleic acid polymer entities, this is the one-letter code for the base."),
    Column("mon_nstd_parent_comp_id", Text, nullable=True, comment="The identifier for the parent component of the nonstandard component. May be be a comma separated list if this component is derived from multiple components. Items in this indirectly point to _chem_comp.id in the CHEM_COMP category."),
    Column("name", Text, nullable=True, comment="The full name of the component."),
    Column("one_letter_code", Text, nullable=True, comment="For standard polymer components, the one-letter code for the component. For non-standard polymer components, the one-letter code for parent component if this exists; otherwise, the one-letter code should be given as 'X'. Components that derived from multiple parents components are described by a sequence of one-letter-codes."),
    Column("three_letter_code", Text, nullable=True, comment="For standard polymer components, the common three-letter code for the component. Non-standard polymer components and non-polymer components are also assigned three-letter-codes. For ambiguous polymer components three-letter code should be given as 'UNK'. Ambiguous ions are assigned the code 'UNX'. Ambiguous non-polymer components are assigned the code 'UNL'."),
    Column("type", Text, nullable=True, comment="For standard polymer components, the type of the monomer. Note that monomers that will form polymers are of three types: linking monomers, monomers with some type of N-terminal (or 5') cap and monomers with some type of C-terminal (or 3') cap."),
    Column("pdbx_synonyms", Text, nullable=True, comment="Synonym list for the component."),
    Column("pdbx_type", Text, nullable=True, comment="A preliminary classification used by PDB."),
    Column("pdbx_ambiguous_flag", Text, nullable=True, comment="A preliminary classification used by PDB to indicate that the chemistry of this component while described as clearly as possible is still ambiguous. Software tools may not be able to process this component definition."),
    Column("pdbx_replaced_by", Text, nullable=True, comment="Identifies the _chem_comp.id of the component that has replaced this component."),
    Column("pdbx_replaces", Text, nullable=True, comment="Identifies the _chem_comp.id's of the components which have been replaced by this component. Multiple id codes should be separated by commas."),
    Column("pdbx_formal_charge", Integer, nullable=True, comment="The net integer charge assigned to this component. This is the formal charge assignment normally found in chemical diagrams."),
    Column("pdbx_subcomponent_list", Text, nullable=True, comment="The list of subcomponents contained in this component."),
    Column("pdbx_model_coordinates_details", Text, nullable=True, comment="This data item provides additional details about the model coordinates in the component definition."),
    Column("pdbx_model_coordinates_db_code", Text, nullable=True, comment="This data item identifies the PDB database code from which the heavy atom model coordinates were obtained."),
    Column("pdbx_ideal_coordinates_details", Text, nullable=True, comment="This data item identifies the source of the ideal coordinates in the component definition."),
    Column("pdbx_ideal_coordinates_missing_flag", Text, nullable=True, comment="This data item identifies if ideal coordinates are missing in this definition."),
    Column("pdbx_model_coordinates_missing_flag", Text, nullable=True, comment="This data item identifies if model coordinates are missing in this definition."),
    Column("pdbx_initial_date", Date, nullable=True, comment="Date component was added to database."),
    Column("pdbx_modified_date", Date, nullable=True, comment="Date component was last modified."),
    Column("pdbx_release_status", Text, nullable=True, comment="This data item holds the current release status for the component."),
    Column("pdbx_processing_site", Text, nullable=True, comment="This data item identifies the deposition site that processed this chemical component defintion."),
    Column("pdbx_pcm", Text, nullable=True, comment="A flag to indicate if the CCD can be used to represent a protein modification."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("alt_atom_id", Text, nullable=True, comment="An alternative identifier for the atom. This data item would be used in cases where alternative nomenclatures exist for labelling atoms in a group."),
    Column("atom_id", Text, nullable=True, comment="The value of _chem_comp_atom.atom_id must uniquely identify each atom in each monomer in the CHEM_COMP_ATOM list. The atom identifiers need not be unique over all atoms in the data block; they need only be unique for each atom in a component. Note that this item need not be a number; it can be any unique identifier."),
    Column("charge", Integer, nullable=True, comment="The net integer charge assigned to this atom. This is the formal charge assignment normally found in chemical diagrams."),
    Column("model_Cartn_x", Double, nullable=True, comment="The x component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list."),
    Column("model_Cartn_y", Double, nullable=True, comment="The y component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list."),
    Column("model_Cartn_z", Double, nullable=True, comment="The z component of the coordinates for this atom in this component specified as orthogonal angstroms. The choice of reference axis frame for the coordinates is arbitrary. The set of coordinates input for the entity here is intended to correspond to the atomic model used to generate restraints for structure refinement, not to atom sites in the ATOM_SITE list."),
    Column("type_symbol", Text, nullable=True, comment="The code used to identify the atom species representing this atom type. Normally this code is the element symbol."),
    Column("pdbx_align", Integer, nullable=True, comment="Atom name alignment offset in PDB atom field."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="Ordinal index for the component atom list."),
    Column("pdbx_component_atom_id", Text, nullable=True, comment="The atom identifier in the subcomponent where a larger component has been divided subcomponents."),
    Column("pdbx_component_comp_id", Text, nullable=True, comment="The component identifier for the subcomponent where a larger component has been divided subcomponents."),
    Column("pdbx_model_Cartn_x_ideal", Double, nullable=True, comment="An alternative x component of the coordinates for this atom in this component specified as orthogonal angstroms."),
    Column("pdbx_model_Cartn_y_ideal", Double, nullable=True, comment="An alternative y component of the coordinates for this atom in this component specified as orthogonal angstroms."),
    Column("pdbx_model_Cartn_z_ideal", Double, nullable=True, comment="An alternative z component of the coordinates for this atom in this component specified as orthogonal angstroms."),
    Column("pdbx_stereo_config", Text, nullable=True, comment="The chiral configuration of the atom that is a chiral center."),
    Column("pdbx_aromatic_flag", Text, nullable=True, comment="A flag indicating an aromatic atom."),
    Column("pdbx_leaving_atom_flag", Text, nullable=True, comment="A flag indicating a leaving atom."),
    Column("pdbx_residue_numbering", Integer, nullable=True, comment="Preferred residue numbering in the BIRD definition."),
    Column("pdbx_polymer_type", Text, nullable=True, comment="Is the atom in a polymer or non-polymer subcomponent in the BIRD definition."),
    Column("pdbx_component_id", Integer, nullable=True, comment="A reference to _pdbx_reference_entity_list.component_id"),
    Column("pdbx_backbone_atom_flag", Text, nullable=True, comment="A flag indicating the backbone atoms in polypeptide units."),
    Column("pdbx_n_terminal_atom_flag", Text, nullable=True, comment="A flag indicating the N-terminal group atoms in polypeptide units."),
    Column("pdbx_c_terminal_atom_flag", Text, nullable=True, comment="A flag indicating the C-terminal group atoms in polypeptide units."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("atom_id_1", Text, nullable=True, comment="The ID of the first of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category."),
    Column("atom_id_2", Text, nullable=True, comment="The ID of the second of the two atoms that define the bond. This data item is a pointer to _chem_comp_atom.atom_id in the CHEM_COMP_ATOM category."),
    Column("value_order", Text, nullable=True, comment="The value that should be taken as the target for the chemical bond associated with the specified atoms, expressed as a bond order."),
    Column("pdbx_ordinal", Integer, nullable=True, comment="Ordinal index for the component bond list."),
    Column("pdbx_stereo_config", Text, nullable=True, comment="Stereochemical configuration across a double bond."),
    Column("pdbx_aromatic_flag", Text, nullable=True, comment="A flag indicating an aromatic bond."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="An ordinal index for this category"),
    Column("name", Text, nullable=True, comment="The synonym of this particular chemical component."),
    Column("provenance", Text, nullable=True, comment="The provenance of this synonym."),
    Column("type", Text, nullable=True, comment="The type of this synonym."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("type", Text, nullable=True, comment="The component feature type."),
    Column("value", Text, nullable=True, comment="The component feature value."),
    Column("source", Text, nullable=True, comment="The information source for the component feature."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("descriptor", Text, nullable=True, comment="This data item contains the descriptor value for this component."),
    Column("type", Text, nullable=True, comment="This data item contains the descriptor type."),
    Column("program", Text, nullable=True, comment="This data item contains the name of the program or library used to compute the descriptor."),
    Column("program_version", Text, nullable=True, comment="This data item contains the version of the program or library used to compute the descriptor."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("identifier", Text, nullable=True, comment="This data item contains the identifier value for this component."),
    Column("type", Text, nullable=True, comment="This data item contains the identifier type."),
    Column("program", Text, nullable=True, comment="This data item contains the name of the program or library used to compute the identifier."),
    Column("program_version", Text, nullable=True, comment="This data item contains the version of the program or library used to compute the identifier."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("date", Date, nullable=True, comment="The date associated with this audit record."),
    Column("processing_site", Text, nullable=True, comment="An identifier for the wwPDB site creating or modifying the component."),
    Column("action_type", Text, nullable=True, comment="The action associated with this audit record."),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("related_comp_id", Text, nullable=True, comment="The related chemical component for which this chemical component is based."),
    Column("relationship_type", Text, nullable=True, comment="Describes the type of relationship"),
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
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("related_comp_id", Text, nullable=True, comment="The related chemical component for which this chemical component is based."),
    Column("ordinal", Integer, nullable=True, comment="An ordinal index for this category"),
    Column("atom_id", Text, nullable=True, comment="The atom identifier/name for the atom mapping"),
    Column("related_atom_id", Text, nullable=True, comment="The atom identifier/name for the atom mapping in the related chemical component"),
    Column("related_type", Text, nullable=True, comment="Describes the type of relationship"),
    PrimaryKeyConstraint("comp_id", "ordinal", "related_comp_id"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    # FK: (comp_id, atom_id) -> chem_comp_atom(comp_id, atom_id)
    info={"pkout": True},
)

pdbx_chem_comp_pcm = Table(
    "pdbx_chem_comp_pcm",
    metadata,
    Column("comp_id", Text, nullable=True, comment="Chemical Component ID of an entry. All tables/categories refer back to this ID in the brief_summary table."),
    Column("pcm_id", Integer, nullable=True, comment="An ordinal index for this category."),
    Column("modified_residue_id", Text, nullable=True, comment="Chemical component identifier for the amino acid residue that is being modified."),
    Column("type", Text, nullable=True, comment="The type of protein modification."),
    Column("category", Text, nullable=True, comment="The category of protein modification."),
    Column("position", Text, nullable=True, comment="The position of the modification on the amino acid."),
    Column("polypeptide_position", Text, nullable=True, comment="The position of the modification on the polypeptide."),
    Column("comp_id_linking_atom", Text, nullable=True, comment="The atom on the modification group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs."),
    Column("modified_residue_id_linking_atom", Text, nullable=True, comment="The atom on the polypeptide residue group that covalently links the modification to the residue that is being modified. This is only added when the protein modification is linked and so the amino acid group and the modification group are described by separate CCDs."),
    Column("uniprot_specific_ptm_accession", Text, nullable=True, comment="The UniProt PTM accession code that is an exact match for the protein modification."),
    Column("uniprot_generic_ptm_accession", Text, nullable=True, comment="The UniProt PTM accession code that describes the group of PTMs of which this protein modification is a member."),
    PrimaryKeyConstraint("comp_id", "pcm_id"),
    # FK: (comp_id) -> brief_summary(comp_id)
    # FK: (comp_id) -> chem_comp(comp_id)
    info={
        "keywords": ["first_instance_model_db_code"],
        "pkout": True,
    },
)
