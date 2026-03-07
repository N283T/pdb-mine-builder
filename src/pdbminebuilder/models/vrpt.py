"""SQLAlchemy schema definition for vrpt."""

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
)

metadata = MetaData(schema="vrpt")
metadata.info = {"entry_pk": "pdbid"}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("update_date", DateTime, nullable=True, comment="Entry update date (within the RDB)."),
    Column("keywords", ARRAY(Text), nullable=True, comment="Array of keywords."),
    PrimaryKeyConstraint("pdbid"),
)

entry = Table(
    "entry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _entry.id identifies the data block. Note that this item need not be a number; it can be any unique identifier."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

entity = Table(
    "entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="The value of _entity.id must uniquely identify a record in the ENTITY list. Note that this item need not be a number; it can be any unique identifier."),
    Column("type", Text, nullable=True, comment="Defines the type of the entity. Polymer entities are expected to have corresponding ENTITY_POLY and associated entries. Non-polymer entities are expected to have corresponding CHEM_COMP and associated entries. Water entities are not expected to have corresponding entries in the ENTITY category."),
    Column("src_method", Text, nullable=True, comment="The method by which the sample for the entity was produced. Entities isolated directly from natural sources (tissues, soil samples etc.) are expected to have further information in the ENTITY_SRC_NAT category. Entities isolated from genetically manipulated sources are expected to have further information in the ENTITY_SRC_GEN category."),
    Column("pdbx_description", Text, nullable=True, comment="A description of the entity. Corresponds to the compound name in the PDB format."),
    Column("formula_weight", Double, nullable=True, comment="Formula mass in daltons of the entity."),
    Column("pdbx_number_of_molecules", Integer, nullable=True, comment="A place holder for the number of molecules of the entity in the entry."),
    Column("pdbx_ec", Text, nullable=True, comment="Enzyme Commission (EC) number(s)"),
    Column("pdbx_mutation", Text, nullable=True, comment="Details about any entity mutation(s)."),
    Column("pdbx_fragment", Text, nullable=True, comment="Entity fragment description(s)."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the entity."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": ["pdbx_description", "pdbx_mutation", "pdbx_fragment", "details"]
    },
)

struct_asym = Table(
    "struct_asym",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("id", Text, nullable=True, comment="The value of _struct_asym.id must uniquely identify a record in the STRUCT_ASYM list. Note that this item need not be a number; it can be any unique identifier."),
    Column("pdbx_modified", Text, nullable=True, comment="This data item indicates whether the structural elements are modified."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["pdbx_modified", "details"]},
)

pdbx_vrpt_summary = Table(
    "pdbx_vrpt_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("entry_id", Text, nullable=True, comment="pdbx_vrpt_summary accesion code (PDB, EMDB or BMRB)"),
    Column("extended_entry_id", Text, nullable=True, comment="pdbx_vrpt_summary extended accesion code"),
    Column("PDB_deposition_date", Date, nullable=True, comment="Date in yyyy-mm-dd format when structure was deposited to the PDB. Obtained from model file _pdbx_database_status.recvd_initial_deposition_date."),
    Column("PDB_revision_number", Integer, nullable=True, comment="The highest number that appears in mmCIF model item _pdbx_audit_revision_history.ordinal."),
    Column("PDB_revision_date", Date, nullable=True, comment="Date in yyyy-mm-dd format when the structure was last revised by PDB. Obtained from the mmCIF model file _pdbx_audit_revision_history.revision_date"),
    Column("EMDB_deposition_date", Date, nullable=True, comment="Date in yyyy-mm-dd format when map was deposited to the EMDB."),
    Column("report_creation_date", DateTime(timezone=True), nullable=True, comment="The date, time and time-zone that the validation report was created. The string will be formatted like yyyy-mm-dd:hh:mm in GMT time."),
    Column("attempted_validation_steps", Text, nullable=True, comment="The steps that were attempted by the validation pipeline software. A step typically involves running a 3rd party validation tool, for instance \"mogul\" Each step will be enumerated in _pdbx_vrpt_software category."),
    Column("ligands_for_buster_report", Text, nullable=True, comment="A flag indicating if there are ligands in the model used for detailed Buster analysis."),
    Column("RNA_suiteness", Double, nullable=True, comment="The MolProbity conformer-match quality parameter for RNA structures. Low values are worse. Specific to structures that contain RNA polymers."),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["attempted_validation_steps"]},
)

pdbx_vrpt_model_list = Table(
    "pdbx_vrpt_model_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("PDB_model_num", Integer, nullable=True, comment="The integer identifier of a Model."),
    Column("nmrclust_cluster_id", Text, nullable=True, comment="NMRClust software is used to compare models in NMR entries. It clusters similar models. Each model in an NMR entry, therefore, can have an \"nmrclust_cluster_id\" indicating to which cluster the given model belongs. This value is either an integer or the string \"outlier\" if the model is sufficiently different from other models in the ensemble."),
    Column("nmrclust_representative", Text, nullable=True, comment="A flag indicating if the given model is also the representative model of the cluster to which it belongs."),
    PrimaryKeyConstraint("pdbid", "PDB_model_num"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["nmrclust_cluster_id"]},
)

pdbx_vrpt_model_instance = Table(
    "pdbx_vrpt_model_instance",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of the model."),
    Column("auth_asym_id", Text, nullable=True, comment="The auth_asym_id identifier for the residue is the same as in the model mmCIF item _atom_site.auth_asym_id."),
    Column("auth_seq_id", Integer, nullable=True, comment="The authors residue number for a residue. This is obtained from _atom_site.auth_seq_id"),
    Column("label_comp_id", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. This is the same and the model mmCIF _atom_site.auth_comp_id."),
    Column("PDB_model_num", Integer, nullable=True, comment="The number corresponding to _atom_site.pdbx_PDB_model_num. If the structure does not have multiple models then PDB_model_num will be \"1\"."),
    Column("label_alt_id", Text, nullable=True, comment="This attribute will be set if the pdbx_vrpt_model_instance has atoms with the alternate position indicator set. Normally one character but can be up to 3. Example label_alt_id=\"A\" Obtained from _atom_site.label_alt_id"),
    Column("PDB_ins_code", Text, nullable=True, comment="Insertion code for residue from _atom_site.pdbx_PDB_ins_code"),
    Column("entity_id", Text, nullable=True, comment="The entity id for the residue or chain. This is a pointer to _pdbx_vrpt_entity.id"),
    Column("label_asym_id", Text, nullable=True, comment="The _atom_site.label_asym_id label for the residue. Normally this is the same as the author chain name."),
    Column("label_seq_id", Integer, nullable=True, comment="From the modell mmCIF item _atom_site.label_seq_id. This is an internal sequence number within a polymer chain or \".\" for non-polymeric residue."),
    Column("count_angle_outliers", Integer, nullable=True, comment="Count of number of atoms with angle outliers for this instance"),
    Column("count_bond_outliers", Integer, nullable=True, comment="Count of number of atoms with bond outliers in this instance"),
    Column("count_symm_clashes", Integer, nullable=True, comment="Count of number of symmetry related clashes for this instance."),
    Column("count_chiral_outliers", Integer, nullable=True, comment="Count of number of chiral outliers for instance."),
    Column("count_plane_outliers", Integer, nullable=True, comment="Count of number of planar outliers for this instance."),
    Column("count_mogul_angle_outliers", Integer, nullable=True, comment="Count of number of angle outliers as reported by MOGUL for this instance."),
    Column("count_mogul_bond_outliers", Integer, nullable=True, comment="Count of number of bond outliers as reported by MOGUL for this residue."),
    Column("count_mogul_torsion_outliers", Integer, nullable=True, comment="Count of number torsion angle outliers as reported by MOGUL for this instance."),
    Column("count_mogul_ring_outliers", Integer, nullable=True, comment="Count of number of atoms with ring outliers as reported by MOGUL for this instance."),
    Column("count_clashes", Integer, nullable=True, comment="Count of number of atoms a with a pdbx_vrpt_instance_clashes for this instance."),
    Column("ligand_of_interest", Text, nullable=True, comment="A flag to indicate if this instance is a ligand of interest."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_cyrange_domain = Table(
    "pdbx_vrpt_cyrange_domain",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each domain."),
    Column("domain", Integer, nullable=True, comment="Identifier of the well-defined core"),
    Column("number_of_gaps", Integer, nullable=True, comment="Number of omissions from the contiguous protein _atom_site.auth_asym_id within the individual well-defined core (domain)."),
    Column("number_of_residues", Integer, nullable=True, comment="Number of residues composing the individual well-defined core (domain)."),
    Column("percentage_of_core", Double, nullable=True, comment="What fraction the individual core contributes to the total well-defined portion of the protein."),
    Column("rmsd", Double, nullable=True, comment="Average pairwise backbone RMSD of the individual well-defined core (domain) over the ensemble."),
    Column("medoid_model", Integer, nullable=True, comment="For each Cyrange well-defined core (\"cyrange_domain\") the id of the model which is most similar to other models as measured by pairwise RMSDs over the domain. For the whole entry, the medoid model of the largest core is taken as an overall representative of the structure."),
    Column("medoid_rmsd", Double, nullable=True, comment="Average RMSD between the medoid model and other members of the ensemble."),
    Column("residue_string", Text, nullable=True, comment="Simplified description of the residue composition of the individual well-defined core (domain)."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["residue_string"]},
)

pdbx_vrpt_summary_entity_fit_to_map = Table(
    "pdbx_vrpt_summary_entity_fit_to_map",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this summary."),
    Column("PDB_model_num", Integer, nullable=True, comment="The unique model number from _atom_site.pdbx_PDB_model_num."),
    Column("entity_id", Text, nullable=True, comment="The entity id for the residue or chain."),
    Column("label_asym_id", Text, nullable=True, comment="The _atom_site.label_asym_id label for the residue. Normally this is the same as the chain."),
    Column("auth_asym_id", Text, nullable=True, comment="The _atom_site.auth_asym_id identifier for the instance."),
    Column("Q_score", Double, nullable=True, comment="The calculated average Q-score."),
    Column("average_residue_inclusion", Double, nullable=True, comment="The average of the residue inclusions for all residues in this instance"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_summary_entity_geometry = Table(
    "pdbx_vrpt_summary_entity_geometry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this summary."),
    Column("PDB_model_num", Integer, nullable=True, comment="The unique model number from _atom_site.pdbx_PDB_model_num."),
    Column("entity_id", Text, nullable=True, comment="The entity id for the residue or chain."),
    Column("label_asym_id", Text, nullable=True, comment="The _atom_site.label_asym_id label for the residue. Normally this is the same as the chain."),
    Column("auth_asym_id", Text, nullable=True, comment="The _atom_site.auth_asym_id identifier for the instance."),
    Column("angles_RMSZ", Double, nullable=True, comment="The overall root mean square of the Z-score for deviations of bond angles in comparison to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("bonds_RMSZ", Double, nullable=True, comment="The overall root mean square of the Z-score for deviations of bond lengths in comparison to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("num_bonds_RMSZ", Integer, nullable=True, comment="The number of bond lengths compared to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("num_angles_RMSZ", Integer, nullable=True, comment="The number of bond angles compared to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("average_residue_inclusion", Double, nullable=True, comment="The average of the residue inclusions for all residues in this instance"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_chemical_shift_list = Table(
    "pdbx_vrpt_chemical_shift_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each chemical shift."),
    Column("file_id", Integer, nullable=True, comment="An identifier of a chemical shifts file."),
    Column("file_name", Text, nullable=True, comment="The name of the chemical shifts file supplied to the validation pipeline."),
    Column("block_name", Text, nullable=True, comment="Label of the section that contains chemical shifts."),
    Column("list_id", Text, nullable=True, comment="Identifier of the chemical shift list in the file."),
    Column("type", Text, nullable=True, comment="A flag indicating if the chemical shift list contains all the required data items i.e., NMR-STAR 3.1 tags (\"full\") or if any data items are missing (\"partial\")."),
    Column("number_of_errors_while_mapping", Integer, nullable=True, comment="Number of chemical shifts that could not be mapped to structure."),
    Column("number_of_warnings_while_mapping", Integer, nullable=True, comment="Currently not used. Reserved for ambiguous mappings."),
    Column("number_of_mapped_shifts", Integer, nullable=True, comment="Number of chemical shifts successfully mapped to the structure."),
    Column("number_of_parsed_shifts", Integer, nullable=True, comment="Number of chemical shifts successfully parsed."),
    Column("total_number_of_shifts", Integer, nullable=True, comment="Total number of records in the chemical shift list."),
    Column("number_of_unparsed_shifts", Integer, nullable=True, comment="Number of chemical shifts that could not be parsed."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["file_name", "block_name", "list_id"]},
)

pdbx_vrpt_unmapped_chemical_shift = Table(
    "pdbx_vrpt_unmapped_chemical_shift",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("auth_asym_id", Text, nullable=True, comment="The auth_asym_id identifier for the residue or auth_asym_id obtained from cif item _atom_site.auth_asym_id. Currently this is limited to 5 characters. Example: auth_asym_id=\"A\""),
    Column("rescode", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("auth_seq_id", Integer, nullable=True, comment="The residue number aka sequence id for a residue. Obtained from _atom_site.auth_seq_id"),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("value", Double, nullable=True, comment="Value in ppm of a chemical shift"),
    Column("error", Text, nullable=True, comment="Uncertainty on a chemical shift value, if known."),
    Column("ambiguity", Text, nullable=True, comment="Ambiguity of the chemical shift assignment as per NMR-STAR V3.1 dictionary."),
    Column("diagnostic", Text, nullable=True, comment="Diagnostic text message when a chemical shift was not parsed or not mapped to structure."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["error", "ambiguity", "diagnostic"]},
)

pdbx_vrpt_unparsed_chemical_shift = Table(
    "pdbx_vrpt_unparsed_chemical_shift",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("id", Text, nullable=True, comment="ID of the chemical shift as parsed in the chemical shifts file."),
    Column("auth_asym_id", Text, nullable=True, comment="The auth_asym_id identifier for the residue obtained from mmCIF item _atom_site.auth_asym_id."),
    Column("rescode", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("auth_seq_id", Integer, nullable=True, comment="The residue number aka sequence id for a residue. Obtained from _atom_site.auth_seq_id"),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("value", Double, nullable=True, comment="Value in ppm of a chemical shift"),
    Column("error", Text, nullable=True, comment="Uncertainty on a chemical shift value - usually not available"),
    Column("ambiguity", Text, nullable=True, comment="Ambiguity of the chemical shift assignment as per NMR-STAR V3.1 dictionary."),
    Column("diagnostic", Text, nullable=True, comment="Diagnostic text message when a chemical shift was not parsed or not mapped to structure."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["error", "ambiguity", "diagnostic"]},
)

pdbx_vrpt_random_coil_index = Table(
    "pdbx_vrpt_random_coil_index",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("auth_asym_id", Text, nullable=True, comment="The auth_asym_id identifier for the residue or auth_asym_id obtained from cif item _atom_site.auth_asym_id."),
    Column("rescode", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("auth_seq_id", Integer, nullable=True, comment="The residue number aka sequence id for a residue. Obtained from _atom_site.auth_seq_id"),
    Column("value", Double, nullable=True, comment="Value in ppm of a chemical shift"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_chemical_shift_outlier = Table(
    "pdbx_vrpt_chemical_shift_outlier",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each outlier."),
    Column("auth_asym_id", Text, nullable=True, comment="The auth_asym_id identifier for the residue or auth_asym_id obtained from cif item _atom_site.auth_asym_id. Currently this is limited to 5 characters. Example: auth_asym_id=\"A\""),
    Column("rescode", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("auth_seq_id", Integer, nullable=True, comment="The residue number aka sequence id for a residue. Obtained from _atom_site.auth_seq_id"),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("value", Double, nullable=True, comment="Value in ppm of a chemical shift"),
    Column("zscore", Double, nullable=True, comment="The Zscore of the deviation of the bond length or bond angle in the model compared to Mogul expected values and standard deviation. A Z score is generally defined as the difference between an observed value an expected or average value, divided by the standard deviations of the latter. Units depend on the parameter being analyzed."),
    Column("prediction", Text, nullable=True, comment="The mean value of the chemical shift expected from the BMRB statistics."),
    Column("method", Text, nullable=True, comment="Method to determine the expected value and standard deviation. At present this is limited to BMRB statistics."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["prediction", "method"]},
)

pdbx_vrpt_referencing_offset = Table(
    "pdbx_vrpt_referencing_offset",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each referencing_offset."),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("uncertainty", Double, nullable=True, comment="Default uncertainty of the prediction, set to 0.05 ppm for protons and 0.5 ppm for 13C and 15N nuclei."),
    Column("precision", Double, nullable=True, comment="Precision of the suggested correction, as estimated by jack-knifing algorithm."),
    Column("value", Double, nullable=True, comment="Value in ppm of a chemical shift"),
    Column("number_of_measurements", Integer, nullable=True, comment="How many chemical shift values for this kind of nucleus are reported in the chemical shift list."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_assign_completeness_well_defined = Table(
    "pdbx_vrpt_assign_completeness_well_defined",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each well defined region."),
    Column("number_of_assigned_shifts", Integer, nullable=True, comment="Number of typically assigned nuclei of a given \"type\" (e.g., backbone) and \"element\" (13C) in the structure that have a chemical shift assignment."),
    Column("number_of_unassigned_shifts", Integer, nullable=True, comment="Number of typically assigned nuclei of a given \"type\" (e.g., backbone) and \"element\" (13C) in the structure that lack a chemical shift assignment"),
    Column("number_of_shifts", Integer, nullable=True, comment="Total number of typically assigned nuclei of a given \"type\" (e.g., backbone) and \"element\" (13C)in the structure irrespective of assignment. It should be a sum of \"number_of_unassigned_shifts\" and \"number_of_assigned_shifts\" for the same type and element."),
    Column("type", Text, nullable=True, comment="\"Type\" refers to a subset of assignments: overall, backbone, aliphatic sidechain, aromatic protein rings, nucleic acid base and ribose or deoxyribose ring."),
    Column("element", Text, nullable=True, comment="The chemical element (isotope) for which the assignment completeness is calculated."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["type"]},
)

pdbx_vrpt_assign_completeness_full_length = Table(
    "pdbx_vrpt_assign_completeness_full_length",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("number_of_assigned_shifts", Integer, nullable=True, comment="Number of typically assigned nuclei of a given \"type\" (e.g., backbone) and \"element\" (13C) in the structure that have a chemical shift assignment."),
    Column("number_of_unassigned_shifts", Integer, nullable=True, comment="Number of typically assigned nuclei of a given \"type\" (e.g., backbone) and \"element\" (13C) in the structure that lack a chemical shift assignment"),
    Column("number_of_shifts", Integer, nullable=True, comment="Total number of typically assigned nuclei of a given \"type\" (e.g., backbone) and \"element\" (13C) in the structure irrespective of assignment. It should be a sum of \"number_of_unassigned_shifts\" and \"number_of_assigned_shifts\" for the same type and element."),
    Column("type", Text, nullable=True, comment="\"Type\" refers to a subset of assignments: overall, backbone, aliphatic sidechain, aromatic protein rings, nucleic acid base and ribose or deoxyribose ring."),
    Column("element", Text, nullable=True, comment="The chemical element (isotope) for which the assignment completeness is calculated."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["type"]},
)

pdbx_vrpt_software = Table(
    "pdbx_vrpt_software",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each software used."),
    Column("name", Text, nullable=True, comment="The name of the program."),
    Column("version", Text, nullable=True, comment="Version string for the program. The format is software dependent."),
    Column("success_y_or_n", Text, nullable=True, comment="Indicates if pdbx_vrpt_software for step ran successfully"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "classification", "version", "details"]},
)

pdbx_vrpt_instance_intra_bond_outliers = Table(
    "pdbx_vrpt_instance_intra_bond_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each outlier."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("atom_1", Text, nullable=True, comment="A label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_2", Text, nullable=True, comment="A label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("mean", Double, nullable=True, comment="The \"ideal\" value of the bond length. Source is mean value from Engh and Huber EH99 parameters, Parkinson et al. parameter set or Mogul analysis of CSD structures that have a similar local chemistry. Units depend on the parameter being analyzed in Angstroms."),
    Column("stdev", Double, nullable=True, comment="The standard deviation for the bond length. Source is standard deviation found from Engh and Huber EH99 parameters, Parkinson et al. parameter set or Mogul analysis of CSD structures that have a similar local chemistry. Units depend on the parameter being analyzed."),
    Column("obs", Double, nullable=True, comment="The observed value for the bond length. that is the value found in the structure being analyzed for the atoms involved."),
    Column("Z", Double, nullable=True, comment="The Zscore of the deviation of the bond length compared to ideal values. A Z score is generally defined as the difference between an observed value an expected or average value, divided by the standard deviations of the latter."),
    Column("link", Text, nullable=True, comment="Flag indicating that the bond involves an atom that is in another residue"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_intra_angle_outliers = Table(
    "pdbx_vrpt_instance_intra_angle_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each angle outlier."),
    Column("mean", Double, nullable=True, comment="The \"ideal\" value of the bond angle. Source is mean value from Engh and Huber EH99 parameters, Parkinson et al. parameter set or Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("stdev", Double, nullable=True, comment="The standard deviation for the bond bond angle. Source is standard deviation found from Engh and Huber EH99 parameters, Parkinson et al. parameter set or Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("obs", Double, nullable=True, comment="The observed value for bond angle, that is the value fouund for the atoms involved."),
    Column("Z", Double, nullable=True, comment="The Zscore of the deviation of the bond angle compared to ideal values. A Z score is generally defined as the difference between an observed value an expected or average value, divided by the standard deviations of the latter."),
    Column("link", Text, nullable=True, comment="Flag indicating that the bond involves an atom that is in another residue."),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_3", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_stereo_outliers = Table(
    "pdbx_vrpt_instance_stereo_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each stereo outlier."),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("problem", Text, nullable=True, comment="The type of chiral problem that the label_atom_id has. either \"WRONG HAND\" or \"PLANAR\""),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_intra_plane_outliers = Table(
    "pdbx_vrpt_instance_intra_plane_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each planar outlier."),
    Column("type", Text, nullable=True, comment="The type of chiral problem that the label_atom_id has. One of: (A) \"mainchain\": The N label_atom_id of an amino acid residue is expected to be in the same plane as the Calpha, C, and O atoms of the previous residue. If the improper torsion angle of these atoms is more than 10 degrees, this is flagged as a planarity deviation. From mmcif item \"_pdbx_validate_main_chain_plane\". (B) \"peptide\": A deviation is flagged if the omega torsion angle of a peptide group differs by more than 30 degrees from the values expected for a proper cis or trans conformation (0 degrees and 180 degrees, respectively). For mmcif item: \"_pdbx_validate_peptide_omega\". (C) \"sidechain\": Certain groups of atoms in protein sidechains and nucleotide bases are expected to be in the same plane. An atom's deviation from planarity is calculated by fitting a plane through these atoms and then calculating distance of individual label_atom_id from the plane. Expected value of such distances have been pre-calculated from data analysis (wwPDB, 2012). If an label_atom_id is modelled to be more than six times farther than the pre-calculated value, the residue is flagged to have a sidechain planarity deviation. From mmcif item \"_pdbx_validate_planes\"."),
    Column("improper", Double, nullable=True, comment="For a type=\"mainchain\" outlier, the improper torsion angle in degrees."),
    Column("omega", Double, nullable=True, comment="For a type=\"peptide\" outlier, the omega torsion angle in degrees."),
    Column("plane_rmsd", Double, nullable=True, comment="For a type=\"sidechain\" outlier, the root mean squared deviation from the mean plane in Angstroms."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_clashes = Table(
    "pdbx_vrpt_instance_clashes",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each clash instance."),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("cid", Integer, nullable=True, comment="An identifier that cross references the other label_atom_id in the clash. The two atoms in the clash will have the same unique cid."),
    Column("clashmag", Double, nullable=True, comment="The \"magnitude\" of the pdbx_vrpt_instance_clashes in Angstroms assessed by MolProbity. The MolProbity \"magnitude\" of a pdbx_vrpt_instance_clashes is defined as the difference between the observed interatomic distance and the sum of the van der Waals radii of the atoms involved."),
    Column("dist", Double, nullable=True, comment="The distance in Angstroms between two atoms involved a clash."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_symm_clashes = Table(
    "pdbx_vrpt_instance_symm_clashes",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each symmetry clash."),
    Column("label_atom_id", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("symop", Text, nullable=True, comment="The symmetry operator for the label_atom_id in the contact. The 1_555 notation is crystallographic shorthand to describe a particular symmetry operator (the number before the underscore) and any required translation (the three numbers following the underscore). Symmetry operators are defined by the space group and the translations are given for the three-unit cell axis (a, b, and c) where 5 indicates no translation and numbers higher or lower signify the number of unit cell translations in the positive or negative direction. For example, 4_565 indicates the use of symmetry operator 4 followed by a one-unit cell translation in the positive b direction. One of the atoms in the contact will have symop=\"1_555\" that indicates the identity operator."),
    Column("scid", Integer, nullable=True, comment="An identifier that cross references the other label_atom_id in the clash. The two atoms in the clash will have the same unique scid."),
    Column("clashmag", Double, nullable=True, comment="The \"magnitude\" of the pdbx_vrpt_instance_clashes in Angstroms assessed by the validation package. In this case, the \"magnitude\" of a pdbx_vrpt_instance_clashes is defined as 2.2 Angstrom (or 1.6 Angstrom if either label_atom_id is a hydrogen atom) minus the interatomic distance."),
    Column("dist", Double, nullable=True, comment="The distance in Angstroms between two atoms involved a clash."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
    info={"keywords": ["symop"]},
)

pdbx_vrpt_instance_mogul_bond_outliers = Table(
    "pdbx_vrpt_instance_mogul_bond_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("obsval", Double, nullable=True, comment="The observed value for the bond length that is the value found in the structure being analyzed for the atoms involved."),
    Column("mean", Double, nullable=True, comment="The \"ideal\" value of the bond length. Source is mean value from Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("stdev", Double, nullable=True, comment="The standard deviation for the bond length. Source is standard deviation found from Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("numobs", Integer, nullable=True, comment="The number of observations found for bond length or bond angle or torsion angle in the Mogul analysis."),
    Column("Zscore", Double, nullable=True, comment="The Zscore of the deviation of the bond length compared to the Mogul expected values and standard deviation. A Z score is generally defined as the difference between an observed value an expected or average value, divided by the standard deviations of the latter."),
    Column("mindiff", Double, nullable=True, comment="The difference to the nearest value of the bond length found in the Mogul analysis."),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each bond outlier."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_mogul_angle_outliers = Table(
    "pdbx_vrpt_instance_mogul_angle_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("obsval", Double, nullable=True, comment="The observed value for the bond angle that is the value found in the structure being analyzed for the atoms involved."),
    Column("mean", Double, nullable=True, comment="The \"ideal\" value of the bond length or bond angle or torsion angle. Source is mean value Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("stdev", Double, nullable=True, comment="The standard deviation for the bond angle. Source is standard deviation found Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("numobs", Integer, nullable=True, comment="The number of observations found for bond length in the Mogul analysis."),
    Column("Zscore", Double, nullable=True, comment="The Zscore of the deviation of the bond angle in the model compared to Mogul expected values and standard deviation. A Z score is generally defined as the difference between an observed value an expected or average value, divided by the standard deviations of the latter."),
    Column("mindiff", Double, nullable=True, comment="The difference to the nearest value of the bond angle found in the Mogul analysis."),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_3", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_mogul_torsion_outliers = Table(
    "pdbx_vrpt_instance_mogul_torsion_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("obsval", Double, nullable=True, comment="The observed value for the torsion angle, that is the value found in the structure being analyzed for the atoms involved."),
    Column("mean", Double, nullable=True, comment="The \"ideal\" value of the torsion angle. Source is mean value from Mogul analysis of CSD structures that have a similar local chemistry. Units depend on the parameter being analyzed."),
    Column("mindiff", Double, nullable=True, comment="The difference to the nearest value of the torsion angle found in the Mogul analysis."),
    Column("numobs", Integer, nullable=True, comment="The number of observations found for torsion angle in the Mogul analysis."),
    Column("stdev", Double, nullable=True, comment="The standard deviation for the torsion angle. Source is standard deviation found from Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("local_density", Double, nullable=True, comment="The local density is the percentage of observed Mogul torsion angles within certain units of the query torsion angle."),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_3", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_4", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each torsion outlier."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_mogul_ring_outliers = Table(
    "pdbx_vrpt_instance_mogul_ring_outliers",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atoms", Text, nullable=True, comment="A comma separated list of label_atom_id names."),
    Column("mean", Double, nullable=True, comment="The \"ideal\" value of the bond length or bond angle or torsion angle. Source is mean value from Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("mindiff", Double, nullable=True, comment="The difference to the nearest value thetorsion angle found in the Mogul analysis."),
    Column("stdev", Double, nullable=True, comment="The standard deviation of the torsion angles. Source is standard deviation found in Mogul analysis of CSD structures that have a similar local chemistry."),
    Column("numobs", Integer, nullable=True, comment="The number of observations found for torsion angles in the Mogul analysis."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each ring outlier."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_restraint_summary = Table(
    "pdbx_vrpt_restraint_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("description", Text, nullable=True, comment="The description of the restraint type."),
    Column("value", Double, nullable=True, comment="The number of restraints or the value associated with the description."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["description"]},
)

pdbx_vrpt_residual_angle_violations = Table(
    "pdbx_vrpt_residual_angle_violations",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("max_violation", Double, nullable=True, comment="The maximum value of the dihedral-angle violation within the bin"),
    Column("bins", Text, nullable=True, comment="The violations are binned as small, medium and large violations based on its absolute value."),
    Column("violations_per_model", Double, nullable=True, comment="Average number of violations per model is calculated by dividing the total number of violations in each bin by the size of the ensemble."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each residual angle violation."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["bins"]},
)

pdbx_vrpt_distance_violation_summary = Table(
    "pdbx_vrpt_distance_violation_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("restraint_type", Text, nullable=True, comment="The restraint type (Intra-residue, Sequential, MediumRange, LongRange, InterChain, Total)"),
    Column("restraint_sub_type", Text, nullable=True, comment="The restraint sub type (BackboneBackbone, BackboneSidechain, SidechainSidechain, all)"),
    Column("consistently_violated_count", Integer, nullable=True, comment="Number of restraints that are violated in all models"),
    Column("consistently_violated_percent_total", Double, nullable=True, comment="Percentage of restraints that are violated in all models against total number of restraints"),
    Column("consistently_violated_percent_type", Double, nullable=True, comment="Percentage of restraints that are violated in all models against number of restraints in a given restraint type."),
    Column("restraints_count", Integer, nullable=True, comment="Number of restraints in a given restraint type."),
    Column("violated_count", Integer, nullable=True, comment="Number of restraints that are violated at least in one model"),
    Column("percent_total", Double, nullable=True, comment="Percentage of restraints in a given restraint type"),
    Column("violated_percent_total", Double, nullable=True, comment="Percentage of restraints that are violated at least in one model in given restraint type against the total restraints."),
    Column("violated_percent_type", Double, nullable=True, comment="Percentage of restraints that are violated at least in one model against the total number of restraints in a given restraints type."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each violation summary."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_distance_violation_model_summary = Table(
    "pdbx_vrpt_distance_violation_model_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("max_violation", Double, nullable=True, comment="The maximum value of violation of a particular restraint in an ensemble."),
    Column("mean_violation", Double, nullable=True, comment="The mean value of the violation of a given restraint in an ensemble."),
    Column("PDB_model_num", Integer, nullable=True, comment="Model identifier. If the structure does not have multiple models then PDB_model_num will be \"1\"."),
    Column("standard_deviation", Double, nullable=True, comment="The standard deviation of the value of the violations of a given restraint in an ensemble."),
    Column("median_violation", Double, nullable=True, comment="The median value of the violation of a given restraint in an ensemble"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each distance violation."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_distance_violation_model_restraints = Table(
    "pdbx_vrpt_distance_violation_model_restraints",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("dist_rest_type", Text, nullable=True, comment="The type of distance restraint (intraresidue, sequential, etc.)."),
    Column("violations_count", Integer, nullable=True, comment="Number of violated restraints."),
    Column("PDB_model_num", Text, nullable=True, comment="The model number."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each model restraint."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["PDB_model_num"]},
)

pdbx_vrpt_violated_dihedralangle_restraints = Table(
    "pdbx_vrpt_violated_dihedralangle_restraints",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("violation", Double, nullable=True, comment="The measureed violation."),
    Column("atom_3", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("atom_4", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("rlist_id", Integer, nullable=True, comment="An identifier used to uniquely identify a particular restraints loop."),
    Column("rest_id", Integer, nullable=True, comment="An identifier used to uniquely identify a restraint with in a particular restraint loop."),
    Column("instance_id_1", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("instance_id_2", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("instance_id_3", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("instance_id_4", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each dihedral angle restraint."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id_1) -> pdbx_vrpt_model_instance(pdbid, id)
    # FK: (pdbid, instance_id_2) -> pdbx_vrpt_model_instance(pdbid, id)
    # FK: (pdbid, instance_id_3) -> pdbx_vrpt_model_instance(pdbid, id)
    # FK: (pdbid, instance_id_4) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_distance_violations_ensemble_summary = Table(
    "pdbx_vrpt_distance_violations_ensemble_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("fraction_of_ensemble_count", Integer, nullable=True, comment="Number of violated models for given set of violated restraints."),
    Column("fraction_of_ensemble_percent", Double, nullable=True, comment="Percentage of violated models for given set of violated restraints"),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_distance_violation_ensemble = Table(
    "pdbx_vrpt_distance_violation_ensemble",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("dist_rest_type", Text, nullable=True, comment="The type of distance restraint (intraresidue, sequential, etc.)"),
    Column("violations_count", Integer, nullable=True, comment="Number of violated restraints in ensemble."),
    Column("ensemble_distance_count", Text, nullable=True, comment="Number of violated models for given set of violated restraint"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violations_summary = Table(
    "pdbx_vrpt_dihedralangle_violations_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("restraint_type", Text, nullable=True, comment="The dihedral-angle restraint type (PHI,PSI,etc)"),
    Column("consistently_violated_count", Integer, nullable=True, comment="Number of restraints that are violated in all models"),
    Column("consistently_violated_percent_total", Double, nullable=True, comment="Percentage of restraints that are violated in all models against total number of restraints."),
    Column("consistently_violated_percent_type", Double, nullable=True, comment="Percentage of restraints that are violated in all models against number of restraints in a given restraint type."),
    Column("restraints_count", Integer, nullable=True, comment="Number of restraints in a given restraint type."),
    Column("violated_count", Integer, nullable=True, comment="Number of restraints that are violated that are violated at least in one model."),
    Column("percent_total", Double, nullable=True, comment="Percentage of restraints in a given restraint type."),
    Column("violated_percent_total", Double, nullable=True, comment="Percentage of restraints that are violated at least in one model in given restraint type against the total restraints"),
    Column("violated_percent_type", Double, nullable=True, comment="Percentage of restraints that are violated at least in one model against the total number of restraints in a given restraints type"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violation_model_summary = Table(
    "pdbx_vrpt_dihedralangle_violation_model_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("PDB_model_num", Integer, nullable=True, comment="Model number in summary."),
    Column("max_violation", Double, nullable=True, comment="The maximum value of violation of a particular restraint in an ensemble"),
    Column("mean_violation", Double, nullable=True, comment="The mean value of the violation of a given restraint in an ensemble."),
    Column("standard_deviation", Double, nullable=True, comment="The standard deviation of the value of the violations of a given restraint in an ensemble."),
    Column("median_violation", Double, nullable=True, comment="The median value of the violation of a given restraint in an ensemble"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violation_model = Table(
    "pdbx_vrpt_dihedralangle_violation_model",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ang_rest_type", Text, nullable=True, comment="The type of dihedral-angle restraint"),
    Column("violations_count", Integer, nullable=True, comment="Number of violated restraints."),
    Column("PDB_model_num", Integer, nullable=True, comment="Model number."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violation_ensemble_summary = Table(
    "pdbx_vrpt_dihedralangle_violation_ensemble_summary",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("fraction_of_ensemble_count", Integer, nullable=True, comment="Number of violated models for given set of violated restraints"),
    Column("fraction_of_ensemble_percent", Double, nullable=True, comment="Percentage of violated models for given set of violated restraints"),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_ensemble_violation = Table(
    "pdbx_vrpt_dihedralangle_ensemble_violation",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ang_rest_type", Text, nullable=True, comment="The type of dihedral-angle restraint."),
    Column("violations_count", Integer, nullable=True, comment="Number of violated restraints"),
    Column("ensemble_dihedral_count", Text, nullable=True, comment="Indicates the count of the ensemble"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_residual_distance_violations = Table(
    "pdbx_vrpt_residual_distance_violations",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("max_violation", Double, nullable=True, comment="The maximum value of distance violation with in the given bin"),
    Column("bins", Text, nullable=True, comment="The violations are binned as small, medium and large violations based on its absolute value."),
    Column("violations_per_model", Double, nullable=True, comment="Average number of violations per model is calculated by dividing the total number of violations in each bin by the size of the ensemble."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["bins"]},
)

pdbx_vrpt_most_violated_distance_restraints = Table(
    "pdbx_vrpt_most_violated_distance_restraints",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("altcode_1", Text, nullable=True, comment="This attribute will be set if the model has atoms with the alternate position indicator set."),
    Column("chain_1", Text, nullable=True, comment="The auth_asym_id obtained from cif item _atom_site.auth_asym_id."),
    Column("resnum_1", Integer, nullable=True, comment="The residue number aka sequence id for a residue. Obtained from _atom_site.auth_seq_id"),
    Column("resname_1", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("ent_1", Text, nullable=True, comment="The entity id for the residue or chain. This is from item _atom_site.label_entity_id."),
    Column("said_1", Text, nullable=True, comment="The _atom_site.label_asym_id label for the residue. Normally this is the same as the chain."),
    Column("seq_1", Integer, nullable=True, comment="From cif item _atom_site.label_seq_id \"a pointer to _entity_poly_seq.num\""),
    Column("chain_2", Text, nullable=True, comment="The auth_asym_id identifier for the residue."),
    Column("altcode_2", Text, nullable=True, comment="This attribute will be set if the pdbx_vrpt_model_instance has atoms with the alternate position indicator set. Obtained from _atom_site.label_alt_id"),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("resnum_2", Integer, nullable=True, comment="The residue number aka sequence id for a residue. Obtained from _atom_site.auth_seq_id"),
    Column("resname_2", Text, nullable=True, comment="The \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("seq_2", Integer, nullable=True, comment="From cif item _atom_site.label_seq_id \"a pointer to _entity_poly_seq.num\""),
    Column("said_2", Text, nullable=True, comment="The _atom_site.label_asym_id label for the residue. Normally this is the same as the chain."),
    Column("ent_2", Text, nullable=True, comment="The entity id for the residue or chain. This is from item _atom_site.label_entity_id that is a pointer to _entity.id."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("mean_distance_violation", Double, nullable=True, comment="Mean distance violation over the violated models"),
    Column("median_violation", Double, nullable=True, comment="The median value of the violation of a given restraint in an ensemble"),
    Column("standard_deviation", Double, nullable=True, comment="The standard deviation of the value of the violations of a given restraint in an ensemble"),
    Column("violated_models", Integer, nullable=True, comment="Number of violated models for a given restraint or set of restraints"),
    Column("rlist_id", Integer, nullable=True, comment="An identifier used to uniquely identify a particular restraints loop."),
    Column("rest_id", Integer, nullable=True, comment="An identifier used to uniquely identify a restraint with in a particular restraint loop"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_violated_distance_restraints = Table(
    "pdbx_vrpt_violated_distance_restraints",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("atom_1", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id. The first atom in the pair."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id. The second atom in the pair."),
    Column("violation", Double, nullable=True, comment="Absolute value of the violation"),
    Column("rlist_id", Integer, nullable=True, comment="An identifier used to uniquely identify a particular restraints loop"),
    Column("rest_id", Integer, nullable=True, comment="An identifier used to uniquely identify a restraint with in a particular restraint loop"),
    Column("instance_id_1", Text, nullable=True, comment="A pointer to the first atom fro pdbx_vrpt_model_instance.id."),
    Column("instance_id_2", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id for second atom"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id_1) -> pdbx_vrpt_model_instance(pdbid, id)
    # FK: (pdbid, instance_id_2) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_most_violated_dihedralangle_restraints = Table(
    "pdbx_vrpt_most_violated_dihedralangle_restraints",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("altcode_1", Text, nullable=True, comment="This attribute will be set if the first pdb x_vrpt_model_instance has atoms with the alternate position indicator set."),
    Column("chain_1", Text, nullable=True, comment="The auth_asym_id identifier for the first residue or from cif item _atom_site.auth_asym_id."),
    Column("resnum_1", Integer, nullable=True, comment="The residue number aka sequence id for the first residue. Obtained from _atom_site.auth_seq_id"),
    Column("resname_1", Text, nullable=True, comment="The firs \"residue type\", this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id"),
    Column("ent_1", Text, nullable=True, comment="The entity id for the first residue."),
    Column("said_1", Text, nullable=True, comment="The _atom_site.label_asym_id label for the first residue. Normally this is the same as the chain."),
    Column("seq_1", Integer, nullable=True, comment="From cif item _atom_site.label_seq_id \"a pointer to _entity_poly_seq.num\""),
    Column("atom_1", Text, nullable=True, comment="The first atom label from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("chain_2", Text, nullable=True, comment="The auth_asym_id identifier for the second residue or auth_asym_id obtained from cif item _atom_site.auth_asym_id."),
    Column("altcode_2", Text, nullable=True, comment="This attribute will be set if the second atom has the alternate position indicator set."),
    Column("resnum_2", Integer, nullable=True, comment="The residue number aka sequence id for the second residue. Obtained from _atom_site.auth_seq_id"),
    Column("resname_2", Text, nullable=True, comment="The \"residue type\" of the second atom, this is the name of the chemical component from the PDB chemical component dictionary. Obtained from _atom_site.auth_comp_id."),
    Column("seq_2", Integer, nullable=True, comment="The sequence number for the second atom mrom cif item _atom_site.label_seq_id \"a pointer to _entity_poly_seq.num\""),
    Column("said_2", Text, nullable=True, comment="The _atom_site.label_asym_id label for the second residue. Normally this is the same as the chain."),
    Column("ent_2", Text, nullable=True, comment="The entity id for the second residue."),
    Column("atom_2", Text, nullable=True, comment="An label_atom_id name for the second item from cif item _atom_site.label_atom_id and _chem_comp_atom.atom_id."),
    Column("mean_angle_violation", Double, nullable=True, comment="Mean value of dihedral-angle violation over all violated models"),
    Column("standard_deviation", Double, nullable=True, comment="The standard deviation of the value of the violations of a given restraint in an ensemble"),
    Column("median_violation", Double, nullable=True, comment="The median value of the violation of a given restraint in an ensemble"),
    Column("altcode_3", Text, nullable=True, comment="Alternate position setting for the third atom. Obtained from _atom_site.label_alt_id"),
    Column("chain_3", Text, nullable=True, comment="The auth_asym_id identifier for the third residue."),
    Column("resnum_3", Integer, nullable=True, comment="The residue number aka sequence id for the third residue. Obtained from _atom_site.auth_seq_id."),
    Column("resname_3", Text, nullable=True, comment="The \"residue type\", of the third residue."),
    Column("ent_3", Text, nullable=True, comment="The entity id for the third residue."),
    Column("said_3", Text, nullable=True, comment="The _atom_site.label_asym_id label for the third residue. Normally this is the same as the chain."),
    Column("seq_3", Integer, nullable=True, comment="From cif item _atom_site.label_seq_id for the third residue."),
    Column("atom_3", Text, nullable=True, comment="The label_atom_id name for the third atom."),
    Column("altcode_4", Text, nullable=True, comment="This attribute will be set if the alternate position is set for the fourth atom. Obtained from _atom_site.label_alt_id"),
    Column("chain_4", Text, nullable=True, comment="The auth_asym_id identifier for the fourth residue."),
    Column("resnum_4", Integer, nullable=True, comment="The residue number aka sequence id for the fourth residue."),
    Column("resname_4", Text, nullable=True, comment="The \"residue type\", of the fourth atom. Obtained from _atom_site.auth_comp_id"),
    Column("ent_4", Text, nullable=True, comment="The entity id for the fourth atom."),
    Column("said_4", Text, nullable=True, comment="The _atom_site.label_asym_id label for the fourth atom. Normally this is the same as the chain."),
    Column("seq_4", Integer, nullable=True, comment="From cif item _atom_site.label_seq_id of fourth atom."),
    Column("atom_4", Text, nullable=True, comment="The label_atom_id name for the fourth atom."),
    Column("rlist_id", Integer, nullable=True, comment="An identifier used to uniquely identify a particular restraints loop."),
    Column("rest_id", Integer, nullable=True, comment="An identifier used to uniquely identify a restraint with in a particular restraint loop."),
    Column("violated_models", Integer, nullable=True, comment="number of violated models for a given restraint or set of restraints"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["altcode_2", "altcode_3", "chain_3"]},
)

pdbx_vrpt_model_instance_geometry = Table(
    "pdbx_vrpt_model_instance_geometry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("OWAB", Double, nullable=True, comment="The Occupancy-Weighted Average B (OWAB) value per residue (in units Angstroms squared). This value is calculated by multiplying the B factor for each label_atom_id in the residue by its occupancy and then averaging this value over all atoms in the residue. X-ray specific produced by the EDS step."),
    Column("residue_inclusion", Double, nullable=True, comment="The proportion of all atoms of the residue in density"),
    Column("num_H_reduce", Integer, nullable=True, comment="This is the number of hydrogen atoms added and optimized by the MolProbity reduce software as part of the all-atom clashscore."),
    Column("num_bonds_RMSZ", Integer, nullable=True, comment="The number of bond lengths compared to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("bonds_RMSZ", Double, nullable=True, comment="The overall root mean square of the Z-score for deviations of bond lengths in comparison to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("num_angles_RMSZ", Integer, nullable=True, comment="The number of bond angles compared to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("angles_RMSZ", Double, nullable=True, comment="The overall root mean square of the Z-score for deviations of bond angles in comparison to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996)."),
    Column("program_for_bond_angle_geometry", Text, nullable=True, comment="The software used to calculate the bond and angle RMSZ statistics."),
    Column("average_occupancy", Double, nullable=True, comment="The average occupancy for the residue. Hydrogen atoms are excluded from consideration. X-ray specific produce by the EDS step."),
    Column("ligand_chirality_outlier", Text, nullable=True, comment="A flag indicating of a ligand has a chirality outlier."),
    Column("validate", Text, nullable=True, comment="A flag for NMR entries to indicate if a residue should be included in calculating the overall entry scores (\"True\") or if it should be excluded from such calculations (\"False\")."),
    Column("cyrange_domain_id", Integer, nullable=True, comment="Identifier of the well-defined core (domain) to which the residue belongs, as determined by Cyrange."),
    Column("cis_peptide", Text, nullable=True, comment="A flag to indicate that the residue is a cis-peptide."),
    Column("RNA_score", Double, nullable=True, comment="MolProbity RNA match quality parameter \"suiteness\". The suiteness is a measure of how well the detailed local backbone conformation fits one of the most commonly observed (and thus presumably most favorable) conformational clusters. Varies between 1.0 meaning a good match to a commonly observed cluster to 0.0 meaning an outlier."),
    Column("RNA_suite", Text, nullable=True, comment="MolProbity RNA_suite conformation analysis. RNA specific produced by the molprobity step."),
    Column("RNA_pucker", Text, nullable=True, comment="Placeholder for reporting RNA pucker problem from MolProbity."),
    Column("flippable_sidechain", Text, nullable=True, comment="MolProbity identifies side chains of asparagine, glutamine and histidine that can be be rotated (\"flipped\") to make optimal hydrogen bonds, improving its contacts with its neighbours, without affecting their fit to the experimental electron density. These residues will have flippable_sidechain=\"1\". Protein and polypeptide specific produced by the molprobity step."),
    Column("ramachandran_class", Text, nullable=True, comment="MolProbity Ramachandran plot classification for this residue one of \"Favored\", \"Allowed\" or \"OUTLIER\". Example: ramachandran_class=\"Favored\" Protein and polypeptide specific produced by the molprobity step."),
    Column("rotamer_class", Text, nullable=True, comment="For proteins the MolProbity classification of the side conformation from the chi dihedral angles. For proline the ring pucker is classified as \"Cg_endo\", \"Cg_exo\" or \"OUTLIER\" Examples of common observed classifications: Protein and polypeptide specific produced by the molprobity step."),
    Column("phi", Double, nullable=True, comment="The phi torsion angle for the residue in degrees. Protein and polypeptide specific produced by the molprobity step."),
    Column("psi", Double, nullable=True, comment="The psi torsion angle for the residue in degrees. Protein and polypeptide specific produced by the molprobity step."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
    info={"keywords": ["RNA_pucker", "rotamer_class"]},
)

pdbx_vrpt_model_instance_density = Table(
    "pdbx_vrpt_model_instance_density",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("natoms_eds", Integer, nullable=True, comment="The number of atoms in the residue returned by the EDS software."),
    Column("RSRCC", Double, nullable=True, comment="The real space correlation coefficient for the instance. This is an alternative to RSR for assessing how well the residue's calculated electron density map matches the EDS electron density map calculated from the experimental diffraction data. A value above 0.95 normally indicates a very good fit. RSCC around 0.90 are generally OK. A poor fit results in a value around or below 0.80. X-ray specific produced by the EDS step."),
    Column("RSR", Double, nullable=True, comment="Real Space R-value (RSR) for the residue from the EDS generated map. X-ray specific produced by the EDS step."),
    Column("RSRZ", Double, nullable=True, comment="RSR Z-score (RSRZ) is a normalisation of RSR specific to a residue type and a resolution bin. RSRZ is calculated only for standard amino acids and nucleotides in protein, DNA and RNA chains. A residue is considered an RSRZ outlier if its RSRZ value is greater than 2. X-ray specific produced by the EDS step."),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("EDIAm", Double, nullable=True, comment="The EDIAm score aggregates the electron density support for individual atoms (EDIA score) within a residue, evaluating the overall electron density fit for the residue. A residue with an EDIAm below 0.8 suggests that its constituent atoms display increasing inconsistency with the electron density, and should be visually inspected."),
    Column("OPIA", Double, nullable=True, comment="Overall Percentage of well-resolved Interconnected Atoms score indicates the percentage of atoms within a residue where the EDIA score exceeds 0.8. A value below 50% suggests less than half of the atoms in the residue lack good electron density support and should be visually inspected."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_model_instance_map_fitting = Table(
    "pdbx_vrpt_model_instance_map_fitting",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("residue_inclusion", Double, nullable=True, comment="The proportion of all atoms of the residue in density"),
    Column("Q_score", Double, nullable=True, comment="The Q-score for the residue in the map"),
    Column("instance_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_model_instance.id."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_summary_diffraction = Table(
    "pdbx_vrpt_summary_diffraction",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("exp_method", Text, nullable=True, comment="Experimental method for statistics"),
    Column("Babinet_b", Double, nullable=True, comment="REFMAC scaling parameter as reported in log output line starting 'bulk solvent: scale'. X-ray entry specific, obtained in the EDS step from REFMAC calculation."),
    Column("bulk_solvent_b", Double, nullable=True, comment="REFMAC scaling parameter as reported in log output file. X-ray entry specific, obtained in the EDS step from REFMAC calculation."),
    Column("Wilson_B_estimate", Double, nullable=True, comment="An estimate of the overall B-value of the structure, calculated from the diffraction data. Units Angstroms squared. It serves as an indicator of the degree of order in the crystal and the value is usually not hugely different from the average B-value calculated from the model. X-ray entry specific, calculated by Phenix Xtriage program."),
    Column("I_over_sigma", Text, nullable=True, comment="Each reflection has an intensity (I) and an uncertainty in measurement (sigma(I)), so I/sigma(I) is the signal-to-noise ratio. This ratio decreases at higher resolution. <I/sigma(I)> is the mean of individual I/sigma(I) values. Value for outer resolution shell is given in parentheses. In case structure factor amplitudes are deposited, Xtriage estimates the intensities first and then calculates this metric. When intensities are available in the deposited file, these are converted to amplitudes and then back to intensity estimate before calculating the metric. X-ray entry specific, calculated by Phenix Xtriage program."),
    Column("num_miller_indices", Integer, nullable=True, comment="The number of Miller Indices reported by the Xtriage program. This should be the same as the number of _refln in the input structure factor file. X-ray entry specific, calculated by Phenix Xtriage program."),
    Column("Babinet_k", Double, nullable=True, comment="REFMAC scaling parameter as reported in log output line starting 'bulk solvent: scale'. X-ray entry specific, obtained in the EDS step from REFMAC calculation."),
    Column("bulk_solvent_k", Double, nullable=True, comment="REFMAC reported scaling parameter. X-ray entry specific, obtained in the EDS step from REFMAC calculation."),
    Column("Padilla_Yeates_L_mean", Double, nullable=True, comment="Padilla and Yeates twinning parameter <|L|>. Theoretical values is 0.5 in the untwinned case, and 0.375 in the perfectly twinned case. X-ray entry specific, obtained from the Xtriage program."),
    Column("Padilla_Yeates_L2_mean", Double, nullable=True, comment="Padilla and Yeates twinning parameter <|L**2|>. Theoretical values is 0.333 in the untwinned case, and 0.2 in the perfectly twinned case. X-ray entry specific, obtained from the Xtriage program."),
    Column("DCC_R", Double, nullable=True, comment="The overall R-factor from a DCC recalculation of an electron density map. Currently value is rounded to 2 decimal places. X-ray entry specific, obtained from the DCC program."),
    Column("DCC_Rfree", Double, nullable=True, comment="Rfree as calculated by DCC."),
    Column("EDS_R", Double, nullable=True, comment="The overall R factor from the EDS REFMAC calculation (no free set is used in this). Currently value is rounded to 2 decimal places. X-ray entry specific, obtained in the eds step from REFMAC calculation."),
    Column("EDS_res_high", Double, nullable=True, comment="The data high resolution diffraction limit, in Angstroms, found in the input structure factor file. X-ray entry specific, obtained in the EDS step."),
    Column("EDS_res_low", Double, nullable=True, comment="The data low resolution diffraction limit, in Angstroms, found in the input structure factor file. X-ray entry specific, obtained in the EDS step."),
    Column("Wilson_B_aniso", Text, nullable=True, comment="Result of absolute likelihood based Wilson scaling, The anisotropic B value of the data is determined using a likelihood based approach. The resulting B tensor is reported, the 3 diagonal values are given first, followed by the 3 off diagonal values. A large spread in (especially the diagonal) values indicates anisotropy. X-ray entry specific, calculated by Phenix Xtriage program."),
    Column("data_anisotropy", Double, nullable=True, comment="The ratio (Bmax - Bmin) / Bmean where Bmax, Bmin and Bmean are computed from the B-values associated with the principal axes of the anisotropic thermal ellipsoid. This ratio is usually less than 0.5; for only 1% of PDB entries it is more than 1.0 (Read et al., 2011). X-ray entry specific, obtained from the Xtriage program."),
    Column("trans_NCS_details", Text, nullable=True, comment="A sentence giving the result of Xtriage's analysis on translational NCS. X-ray entry specific, obtained from the Xtriage program."),
    Column("B_factor_type", Text, nullable=True, comment="An indicator if isotropic B factors are partial or full values."),
    Column("acentric_outliers", Integer, nullable=True, comment="The number of acentric reflections that Xtriage identifies as outliers on the basis of Wilson statistics. Note that if pseudo translational symmetry is present, a large number of 'outliers' will be present. X-ray entry specific, calculated by Phenix Xtriage program."),
    Column("centric_outliers", Integer, nullable=True, comment="The number of centric reflections that Xtriage identifies as outliers. X-ray entry specific, calculated by Phenix Xtriage program."),
    Column("data_completeness", Double, nullable=True, comment="The percent completeness of diffraction data."),
    Column("number_reflns_R_free", Integer, nullable=True, comment="The number of reflections in the free set as defined in the input structure factor file supplied to the validation pipeline. X-ray entry specific, obtained from the DCC program."),
    Column("percent_free_reflections", Double, nullable=True, comment="A percentage, Normally percent proportion of the total number. Between 0% and 100%."),
    Column("percent_RSRZ_outliers", Double, nullable=True, comment="The percent of RSRZ outliers."),
    Column("PDB_resolution_high", Double, nullable=True, comment="The high resolution limit of the data."),
    Column("PDB_resolution_low", Double, nullable=True, comment="The low resolution limit of the diffraction data."),
    Column("PDB_R", Double, nullable=True, comment="The reported R in the model file."),
    Column("PDB_Rfree", Double, nullable=True, comment="The reported Rfree."),
    Column("twin_fraction", Text, nullable=True, comment="Estimated twinning fraction for operators as identified by Xtriage. A semicolon separated list of operators with fractions is givens X-ray entry specific, obtained from the Xtriage program."),
    Column("Fo_Fc_correlation", Double, nullable=True, comment="Fo,Fc correlation: The difference between the observed structure factors (Fo) and the calculated structure factors (Fc) measures the correlation between the model and the experimental data. X-ray entry specific, obtained in the eds step from REFMAC calculation."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("density_fitness_version", Text, nullable=True, comment="The version of density-fitness suite programs used in the analysis."),
    Column("CCP4_version", Text, nullable=True, comment="The version of CCP4 suite used in the analysis."),
    Column("EDS_R_warning", Text, nullable=True, comment="Warning message when EDS calculated R vs reported R is higher than a threshold"),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "exp_method",
            "I_over_sigma",
            "Wilson_B_aniso",
            "trans_NCS_details",
            "twin_fraction",
            "density_fitness_version",
            "CCP4_version",
            "servalcat_version",
            "EDS_R_warning",
        ]
    },
)

pdbx_vrpt_summary_geometry = Table(
    "pdbx_vrpt_summary_geometry",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("percent_ramachandran_outliers", Double, nullable=True, comment="The percentage of residues with Ramachandran outliers."),
    Column("clashscore", Double, nullable=True, comment="This score is derived from the number of pairs of atoms in the PDB_model_num that are unusually close to each other. It is calculated by the MolProbity pdbx_vrpt_software and expressed as the number or such clashes per thousand atoms. For structures determined by NMR the clashscore value here will only consider label_atom_id pairs in the well-defined (core) residues from ensemble analysis."),
    Column("angles_RMSZ", Double, nullable=True, comment="The overall root mean square of the Z-score for deviations of bond angles in comparison to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996). This value is for all chains in the structure."),
    Column("bonds_RMSZ", Double, nullable=True, comment="The overall root mean square of the Z-score for deviations of bond lengths in comparison to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996). This value is for all chains in the structure."),
    Column("num_angles_RMSZ", Integer, nullable=True, comment="The number of bond angles compared to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996). This value is for all chains in the structure."),
    Column("num_bonds_RMSZ", Integer, nullable=True, comment="The number of bond lengths compared to \"standard geometry\" made using the MolProbity dangle program. Standard geometry parameters are taken from Engh and Huber (2001) and Parkinson et al. (1996). This value is for all chains in the structure."),
    Column("percent_rotamer_outliers", Double, nullable=True, comment="The MolProbity sidechain outlier score (a percentage). Protein sidechains mostly adopt certain (combinations of) preferred torsion angle values (called rotamers or rotameric conformers), much like their backbone torsion angles (as assessed in the Ramachandran analysis). MolProbity considers the sidechain conformation of a residue to be an outlier if its set of torsion angles is not similar to any preferred combination. The sidechain outlier score is calculated as the percentage of residues with an unusual sidechain conformation with respect to the total number of residues for which the assessment is available. Example: percent-rota-outliers=\"2.44\". Specific to structure that contain protein chains and have sidechains modelled. For NMR structures only the well-defined (core) residues from ensemble analysis will be considered. The percentage of residues with rotamer outliers."),
    Column("percent_ramachandran_outliers_full_length", Double, nullable=True, comment="Only given for structures determined by NMR. The MolProbity Ramachandran outlier score for all atoms in the structure rather than just the well-defined (core) residues."),
    Column("percent_rotamer_outliers_full_length", Double, nullable=True, comment="Only given for structures determined by NMR. The MolProbity sidechain outlier score for all atoms in the structure rather than just the well-defined (core) residues."),
    Column("clashscore_full_length", Double, nullable=True, comment="Only given for structures determined by NMR. The MolProbity pdbx_vrpt_instance_clashes score for all label_atom_id pairs."),
    Column("num_H_reduce", Integer, nullable=True, comment="This is the number of hydrogen atoms added and optimized by the MolProbity reduce pdbx_vrpt_software as part of the all-atom clashscore."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_summary_nmr = Table(
    "pdbx_vrpt_summary_nmr",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("exp_method", Text, nullable=True, comment="Experimental method for statistics"),
    Column("nmr_models_consistency_flag", Text, nullable=True, comment="A flag indicating if all models in the NMR ensemble contain the exact same atoms (\"True\") or if the models differ in this respect (\"False\")."),
    Column("nmrclust_representative_model", Integer, nullable=True, comment="Overall representative PDB_model_num of the NMR ensemble as identified by NMRClust."),
    Column("medoid_model", Integer, nullable=True, comment="For each Cyrange well-defined core (\"cyrange_domain\") the id of the PDB_model_num which is most similar to other models as measured by pairwise RMSDs over the domain. For the whole entry (\"Entry\"), the medoid PDB_model_num of the largest core is taken as an overall representative of the structure."),
    Column("nmrclust_number_of_outliers", Integer, nullable=True, comment="Number of models that do not belong to any cluster as deemed by NMRClust."),
    Column("nmrclust_number_of_models", Integer, nullable=True, comment="Number of models analysed by NMRClust - should in almost all cases be the same as the number of models in the NMR ensemble."),
    Column("nmrclust_number_of_clusters", Integer, nullable=True, comment="Total number of clusters in the NMR ensemble identified by NMRClust."),
    Column("cyrange_number_of_domains", Integer, nullable=True, comment="Total number of well-defined cores (domains) identified by Cyrange"),
    Column("chemical_shift_completeness", Double, nullable=True, comment="Overall completeness of the chemical shift assignments for the well-defined regions of the structure."),
    Column("chemical_shift_completeness_full_length", Double, nullable=True, comment="Overall completeness of the chemical shift assignments for the full macromolecule or complex as suggested by the molecular description of an entry (whether some portion of it is modelled or not)."),
    Column("cyrange_error", Text, nullable=True, comment="Diagnostic message from the wrapper of Cyrange software which identifies the well-defined cores (domains) of NMR protein structures."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["exp_method", "cyrange_error", "nmrclust_error"]},
)

pdbx_vrpt_summary_em = Table(
    "pdbx_vrpt_summary_em",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("exp_method", Text, nullable=True, comment="Experimental method for statistics"),
    Column("contour_level_primary_map", Double, nullable=True, comment="The recommended contour level for the primary map of this deposition."),
    Column("atom_inclusion_all_atoms", Double, nullable=True, comment="The proportion of all non hydrogen atoms within density."),
    Column("atom_inclusion_backbone", Double, nullable=True, comment="The proportion of backbone atoms within density."),
    Column("author_provided_fsc_resolution_by_cutoff_pt_143", Double, nullable=True, comment="The resolution from the intersection of the author provided fsc and the indicator curve 0.143."),
    Column("author_provided_fsc_resolution_by_cutoff_pt_333", Double, nullable=True, comment="The resolution from the intersection of the author provided fsc and the indicator curve 0.333."),
    Column("author_provided_fsc_resolution_by_cutoff_pt_5", Double, nullable=True, comment="The resolution from the intersection of the author provided fsc and the indicator curve 0.5."),
    Column("author_provided_fsc_resolution_by_cutoff_halfbit", Double, nullable=True, comment="The resolution from the intersection of the author provided fsc and the indicator curve halfbit."),
    Column("author_provided_fsc_resolution_by_cutoff_onebit", Double, nullable=True, comment="The resolution from the intersection of the author provided fsc and the indicator curve onebit."),
    Column(
        "author_provided_fsc_resolution_by_cutoff_threesigma", Double, nullable=True
    ),
    Column("calculated_fsc_resolution_by_cutoff_pt_143", Double, nullable=True, comment="The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve 0.143."),
    Column("calculated_fsc_resolution_by_cutoff_pt_333", Double, nullable=True, comment="The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve 0.333."),
    Column("calculated_fsc_resolution_by_cutoff_pt_5", Double, nullable=True, comment="The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve 0.5."),
    Column("calculated_fsc_resolution_by_cutoff_halfbit", Double, nullable=True, comment="The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve halfbit."),
    Column("calculated_fsc_resolution_by_cutoff_onebit", Double, nullable=True, comment="The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve onebit."),
    Column("calculated_fsc_resolution_by_cutoff_threesigma", Double, nullable=True, comment="The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve threesigma."),
    Column("EMDB_resolution", Double, nullable=True, comment="The resolution reported in the entry."),
    Column("Q_score", Double, nullable=True, comment="The overall Q-score of the fit of coordinates to the electron map. The Q-score is defined in Pintilie, GH. et al., Nature Methods, 17, 328-334 (2020)"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["exp_method"]},
)

pdbx_vrpt_percentile_list = Table(
    "pdbx_vrpt_percentile_list",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("exp_method", Text, nullable=True, comment="Experimental method for statistics"),
    Column("range", Text, nullable=True, comment="High resolution relative range of percentiles or 'all' to indicate all resolutions"),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["exp_method", "range"]},
)

pdbx_vrpt_percentile_type = Table(
    "pdbx_vrpt_percentile_type",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("type", Text, nullable=True, comment="Describes the percentile type being reported"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_percentile_conditions = Table(
    "pdbx_vrpt_percentile_conditions",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("percentile_list_id", Text, nullable=True, comment="A pointer to pdbx_vrpt_percentile_list.id."),
    Column("type_id", Text, nullable=True, comment="A pointer to _pdbx_vrpt_percentile_type.id indicating the type"),
    Column("rank", Double, nullable=True, comment="The score or percentile"),
    Column("res_high", Double, nullable=True, comment="The high resolution limit of relative entries or '?' if all entries"),
    Column("res_low", Double, nullable=True, comment="The low resolution limit of relative entries or '?' if all entries"),
    Column("number_entries_total", Integer, nullable=True, comment="The number of entries is this set of entries"),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, percentile_list_id) -> pdbx_vrpt_percentile_list(pdbid, id)
)

pdbx_vrpt_percentile_entity_view = Table(
    "pdbx_vrpt_percentile_entity_view",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("conditions_id", Text, nullable=True, comment="Points to a specific condition."),
    Column("type_id", Text, nullable=True, comment="A pointer to _pdbx_vrpt_percentile_type.id indicating the type"),
    Column("label_asym_id", Text, nullable=True, comment="The _atom_site.label_asym_id label for the residue. Normally this is the same as the chain."),
    Column("PDB_model_num", Text, nullable=True, comment="Model identifier. If the structure does not have multiple models then PDB_model_num will be \"1\"."),
    Column("entity_id", Text, nullable=True, comment="The entity id for the residue or chain. This is from item _atom_site.label_entity_id that is a pointer to _entity.id in the ENTITY category."),
    Column("auth_asym_id", Text, nullable=True, comment="The auth_asym_id identifier for the polymer."),
    Column("rank", Double, nullable=True, comment="The score or percentile"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, conditions_id) -> pdbx_vrpt_percentile_conditions(pdbid, id)
    info={"keywords": ["PDB_model_num", "auth_asym_id"]},
)

pdbx_vrpt_database = Table(
    "pdbx_vrpt_database",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("code", Text, nullable=True, comment="Accession code"),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("extended_code", Text, nullable=True, comment="Extended accession code"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["code", "extended_code"]},
)

pdbx_vrpt_exptl = Table(
    "pdbx_vrpt_exptl",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("method", Text, nullable=True, comment="Experimental methods used in structure determination"),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of this category."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method"]},
)

pdbx_vrpt_entity = Table(
    "pdbx_vrpt_entity",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("id", Text, nullable=True, comment="Uniquely identifies each instance of this category."),
    Column("type", Text, nullable=True, comment="Describes the percentile type being reported"),
    Column("description", Text, nullable=True, comment="The name of the entity"),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["description"]},
)

pdbx_vrpt_asym = Table(
    "pdbx_vrpt_asym",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("label_asym_id", Text, nullable=True, comment="The _struct_asym.label_asym_id in the PDB_model_num"),
    Column("entity_id", Text, nullable=True, comment="The entity id corresponding to the label_asym_id."),
    PrimaryKeyConstraint("pdbid", "label_asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> pdbx_vrpt_entity(pdbid, id)
)

pdbx_vrpt_em_graph_fsc_indicator_curve = Table(
    "pdbx_vrpt_em_graph_fsc_indicator_curve",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("graph_id", Text, nullable=True, comment="A unique identifier for a EM validation report 2D graph."),
    Column("type", Text, nullable=True, comment="The fsc indicator curve type (e.g. threshold)."),
    Column("curve_name", Text, nullable=True, comment="The fsc indicator curve name."),
    Column("data_curve_name", Text, nullable=True, comment="The fsc data (curve_name) used to calculate this fsc indicator curve."),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, graph_id) -> pdbx_vrpt_em_2d_graph_info(pdbid, graph_id)
    info={"keywords": ["graph_id", "type", "curve_name", "data_curve_name"]},
)

pdbx_vrpt_em_graph_fsc_curve = Table(
    "pdbx_vrpt_em_graph_fsc_curve",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("graph_id", Text, nullable=True, comment="A unique identifier for a EM validation report 2D graph."),
    Column("type", Text, nullable=True, comment="The fsc curve type (e.g. half_map to half_map fsc)."),
    Column("curve_name", Text, nullable=True, comment="The fsc curve name."),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, graph_id) -> pdbx_vrpt_em_2d_graph_info(pdbid, graph_id)
    info={"keywords": ["graph_id", "type", "curve_name"]},
)

pdbx_vrpt_em_resolution_intersections = Table(
    "pdbx_vrpt_em_resolution_intersections",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of data in this category."),
    Column("resolution_units", Text, nullable=True, comment="Units of resolution."),
    Column("spatial_frequency_units", Text, nullable=True, comment="Units of spatial frequency."),
    Column("correlation", Double, nullable=True, comment="fsc intersection correlation."),
    Column("resolution", Double, nullable=True, comment="fsc intersection resolution."),
    Column("spatial_frequency", Double, nullable=True, comment="fsc intersection spatial frequency."),
    Column("curve", Text, nullable=True, comment="fsc curve name."),
    Column("type", Text, nullable=True, comment="fsc curve type."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["curve", "type"]},
)

pdbx_vrpt_em_graph_atom_inclusion = Table(
    "pdbx_vrpt_em_graph_atom_inclusion",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("graph_id", Text, nullable=True, comment="A unique identifier for a EM validation report 2D graph."),
    Column("type", Text, nullable=True, comment="The atom type subset for this graph"),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, graph_id) -> pdbx_vrpt_em_2d_graph_info(pdbid, graph_id)
    info={"keywords": ["graph_id"]},
)

pdbx_vrpt_em_details = Table(
    "pdbx_vrpt_em_details",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of data in this category."),
    Column("recommended_contour_level", Double, nullable=True, comment="Recommended contour level for the primary map of this entry."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_em_2d_graph_data = Table(
    "pdbx_vrpt_em_2d_graph_data",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("ordinal", Integer, nullable=True, comment="Uniquely identifies each instance of data in this category."),
    Column("graph_data_id", Text, nullable=True, comment="A reference to the 2D graph containing this item of data."),
    Column("x_value", Double, nullable=True, comment="Data X-value."),
    Column("y_value", Double, nullable=True, comment="Data Y-value."),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_em_2d_graph_info = Table(
    "pdbx_vrpt_em_2d_graph_info",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("graph_data_id", Text, nullable=True, comment="An identifier for the data set associated with this 2D graph."),
    Column("graph_id", Text, nullable=True, comment="A unique identifier for a EM validation report 2D graph."),
    Column("title", Text, nullable=True, comment="2D graph title."),
    Column("x_axis_title", Text, nullable=True, comment="2D graph X-axis title."),
    Column("x_axis_units", Text, nullable=True, comment="2D graph X-axis units. (arbitrary if not provided)"),
    Column("y_axis_title", Text, nullable=True, comment="2D graph Y-axis title."),
    Column("y_axis_scale", Text, nullable=True, comment="2D graph Y-axis scale. (linear if not provided)"),
    Column("y_axis_units", Text, nullable=True, comment="2D graph X-axis units. (arbitrary if not provided)"),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": [
            "graph_id",
            "title",
            "x_axis_title",
            "x_axis_scale",
            "x_axis_units",
            "y_axis_title",
            "y_axis_scale",
            "y_axis_units",
        ]
    },
)

audit_conform = Table(
    "audit_conform",
    metadata,
    Column("pdbid", Text, nullable=True, comment="PDBID of an entry. All tables/categories refer back to the PDBID in the brief_summary table."),
    Column("dict_location", Text, nullable=True, comment="A file name or uniform resource locator (URL) for the dictionary to which the current data block conforms."),
    Column("dict_name", Text, nullable=True, comment="The string identifying the highest-level dictionary defining data names used in this file."),
    Column("dict_version", Text, nullable=True, comment="The version number of the dictionary to which the current data block conforms."),
    PrimaryKeyConstraint("pdbid", "dict_name", "dict_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)
