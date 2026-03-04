"""SQLAlchemy schema definition for vrpt.

Auto-generated from schemas/vrpt.def.yml by scripts/convert_yaml_to_sa.py.
"""

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
    Column("update_date", DateTime, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("pdbid"),
)

entry = Table(
    "entry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

entity = Table(
    "entity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("src_method", Text, nullable=True),
    Column("pdbx_description", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("pdbx_number_of_molecules", Integer, nullable=True),
    Column("pdbx_ec", Text, nullable=True),
    Column("pdbx_mutation", Text, nullable=True),
    Column("pdbx_fragment", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={
        "keywords": ["pdbx_description", "pdbx_mutation", "pdbx_fragment", "details"]
    },
)

struct_asym = Table(
    "struct_asym",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pdbx_modified", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> entity(pdbid, id)
    info={"keywords": ["pdbx_modified", "details"]},
)

pdbx_vrpt_summary = Table(
    "pdbx_vrpt_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("extended_entry_id", Text, nullable=True),
    Column("PDB_deposition_date", Date, nullable=True),
    Column("PDB_revision_number", Integer, nullable=True),
    Column("PDB_revision_date", Date, nullable=True),
    Column("EMDB_deposition_date", Date, nullable=True),
    Column("report_creation_date", DateTime(timezone=True), nullable=True),
    Column("attempted_validation_steps", Text, nullable=True),
    Column("ligands_for_buster_report", Text, nullable=True),
    Column("RNA_suiteness", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "entry_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["attempted_validation_steps"]},
)

pdbx_vrpt_model_list = Table(
    "pdbx_vrpt_model_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("nmrclust_cluster_id", Text, nullable=True),
    Column("nmrclust_representative", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "PDB_model_num"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["nmrclust_cluster_id"]},
)

pdbx_vrpt_model_instance = Table(
    "pdbx_vrpt_model_instance",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("auth_seq_id", Integer, nullable=True),
    Column("label_comp_id", Text, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("label_alt_id", Text, nullable=True),
    Column("PDB_ins_code", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("label_seq_id", Integer, nullable=True),
    Column("count_angle_outliers", Integer, nullable=True),
    Column("count_bond_outliers", Integer, nullable=True),
    Column("count_symm_clashes", Integer, nullable=True),
    Column("count_chiral_outliers", Integer, nullable=True),
    Column("count_plane_outliers", Integer, nullable=True),
    Column("count_mogul_angle_outliers", Integer, nullable=True),
    Column("count_mogul_bond_outliers", Integer, nullable=True),
    Column("count_mogul_torsion_outliers", Integer, nullable=True),
    Column("count_mogul_ring_outliers", Integer, nullable=True),
    Column("count_clashes", Integer, nullable=True),
    Column("ligand_of_interest", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_cyrange_domain = Table(
    "pdbx_vrpt_cyrange_domain",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("domain", Integer, nullable=True),
    Column("number_of_gaps", Integer, nullable=True),
    Column("number_of_residues", Integer, nullable=True),
    Column("percentage_of_core", Double, nullable=True),
    Column("rmsd", Double, nullable=True),
    Column("medoid_model", Integer, nullable=True),
    Column("medoid_rmsd", Double, nullable=True),
    Column("residue_string", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["residue_string"]},
)

pdbx_vrpt_summary_entity_fit_to_map = Table(
    "pdbx_vrpt_summary_entity_fit_to_map",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("Q_score", Double, nullable=True),
    Column("average_residue_inclusion", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_summary_entity_geometry = Table(
    "pdbx_vrpt_summary_entity_geometry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("angles_RMSZ", Double, nullable=True),
    Column("bonds_RMSZ", Double, nullable=True),
    Column("num_bonds_RMSZ", Integer, nullable=True),
    Column("num_angles_RMSZ", Integer, nullable=True),
    Column("average_residue_inclusion", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_chemical_shift_list = Table(
    "pdbx_vrpt_chemical_shift_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("file_id", Integer, nullable=True),
    Column("file_name", Text, nullable=True),
    Column("block_name", Text, nullable=True),
    Column("list_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("number_of_errors_while_mapping", Integer, nullable=True),
    Column("number_of_warnings_while_mapping", Integer, nullable=True),
    Column("number_of_mapped_shifts", Integer, nullable=True),
    Column("number_of_parsed_shifts", Integer, nullable=True),
    Column("total_number_of_shifts", Integer, nullable=True),
    Column("number_of_unparsed_shifts", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["file_name", "block_name", "list_id"]},
)

pdbx_vrpt_unmapped_chemical_shift = Table(
    "pdbx_vrpt_unmapped_chemical_shift",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("rescode", Text, nullable=True),
    Column("auth_seq_id", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("value", Double, nullable=True),
    Column("error", Text, nullable=True),
    Column("ambiguity", Text, nullable=True),
    Column("diagnostic", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["error", "ambiguity", "diagnostic"]},
)

pdbx_vrpt_unparsed_chemical_shift = Table(
    "pdbx_vrpt_unparsed_chemical_shift",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("rescode", Text, nullable=True),
    Column("auth_seq_id", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("value", Double, nullable=True),
    Column("error", Text, nullable=True),
    Column("ambiguity", Text, nullable=True),
    Column("diagnostic", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["error", "ambiguity", "diagnostic"]},
)

pdbx_vrpt_random_coil_index = Table(
    "pdbx_vrpt_random_coil_index",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("rescode", Text, nullable=True),
    Column("auth_seq_id", Integer, nullable=True),
    Column("value", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_chemical_shift_outlier = Table(
    "pdbx_vrpt_chemical_shift_outlier",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("rescode", Text, nullable=True),
    Column("auth_seq_id", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("value", Double, nullable=True),
    Column("zscore", Double, nullable=True),
    Column("prediction", Text, nullable=True),
    Column("method", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["prediction", "method"]},
)

pdbx_vrpt_referencing_offset = Table(
    "pdbx_vrpt_referencing_offset",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("uncertainty", Double, nullable=True),
    Column("precision", Double, nullable=True),
    Column("value", Double, nullable=True),
    Column("number_of_measurements", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_assign_completeness_well_defined = Table(
    "pdbx_vrpt_assign_completeness_well_defined",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("number_of_assigned_shifts", Integer, nullable=True),
    Column("number_of_unassigned_shifts", Integer, nullable=True),
    Column("number_of_shifts", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("element", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["type"]},
)

pdbx_vrpt_assign_completeness_full_length = Table(
    "pdbx_vrpt_assign_completeness_full_length",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("number_of_assigned_shifts", Integer, nullable=True),
    Column("number_of_unassigned_shifts", Integer, nullable=True),
    Column("number_of_shifts", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("element", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["type"]},
)

pdbx_vrpt_software = Table(
    "pdbx_vrpt_software",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("name", Text, nullable=True),
    Column("version", Text, nullable=True),
    Column("success_y_or_n", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["name", "classification", "version", "details"]},
)

pdbx_vrpt_instance_intra_bond_outliers = Table(
    "pdbx_vrpt_instance_intra_bond_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("mean", Double, nullable=True),
    Column("stdev", Double, nullable=True),
    Column("obs", Double, nullable=True),
    Column("Z", Double, nullable=True),
    Column("link", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_intra_angle_outliers = Table(
    "pdbx_vrpt_instance_intra_angle_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("mean", Double, nullable=True),
    Column("stdev", Double, nullable=True),
    Column("obs", Double, nullable=True),
    Column("Z", Double, nullable=True),
    Column("link", Text, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("atom_3", Text, nullable=True),
    Column("instance_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_stereo_outliers = Table(
    "pdbx_vrpt_instance_stereo_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("problem", Text, nullable=True),
    Column("instance_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_intra_plane_outliers = Table(
    "pdbx_vrpt_instance_intra_plane_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("improper", Double, nullable=True),
    Column("omega", Double, nullable=True),
    Column("plane_rmsd", Double, nullable=True),
    Column("instance_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_clashes = Table(
    "pdbx_vrpt_instance_clashes",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("cid", Integer, nullable=True),
    Column("clashmag", Double, nullable=True),
    Column("dist", Double, nullable=True),
    Column("instance_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_symm_clashes = Table(
    "pdbx_vrpt_instance_symm_clashes",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("label_atom_id", Text, nullable=True),
    Column("symop", Text, nullable=True),
    Column("scid", Integer, nullable=True),
    Column("clashmag", Double, nullable=True),
    Column("dist", Double, nullable=True),
    Column("instance_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
    info={"keywords": ["symop"]},
)

pdbx_vrpt_instance_mogul_bond_outliers = Table(
    "pdbx_vrpt_instance_mogul_bond_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("obsval", Double, nullable=True),
    Column("mean", Double, nullable=True),
    Column("stdev", Double, nullable=True),
    Column("numobs", Integer, nullable=True),
    Column("Zscore", Double, nullable=True),
    Column("mindiff", Double, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_mogul_angle_outliers = Table(
    "pdbx_vrpt_instance_mogul_angle_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("obsval", Double, nullable=True),
    Column("mean", Double, nullable=True),
    Column("stdev", Double, nullable=True),
    Column("numobs", Integer, nullable=True),
    Column("Zscore", Double, nullable=True),
    Column("mindiff", Double, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("atom_3", Text, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_mogul_torsion_outliers = Table(
    "pdbx_vrpt_instance_mogul_torsion_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("obsval", Double, nullable=True),
    Column("mean", Double, nullable=True),
    Column("mindiff", Double, nullable=True),
    Column("numobs", Integer, nullable=True),
    Column("stdev", Double, nullable=True),
    Column("local_density", Double, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("atom_3", Text, nullable=True),
    Column("atom_4", Text, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_instance_mogul_ring_outliers = Table(
    "pdbx_vrpt_instance_mogul_ring_outliers",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("atoms", Text, nullable=True),
    Column("mean", Double, nullable=True),
    Column("mindiff", Double, nullable=True),
    Column("stdev", Double, nullable=True),
    Column("numobs", Integer, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_restraint_summary = Table(
    "pdbx_vrpt_restraint_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("value", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["description"]},
)

pdbx_vrpt_residual_angle_violations = Table(
    "pdbx_vrpt_residual_angle_violations",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("max_violation", Double, nullable=True),
    Column("bins", Text, nullable=True),
    Column("violations_per_model", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["bins"]},
)

pdbx_vrpt_distance_violation_summary = Table(
    "pdbx_vrpt_distance_violation_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("restraint_sub_type", Text, nullable=True),
    Column("consistently_violated_count", Integer, nullable=True),
    Column("consistently_violated_percent_total", Double, nullable=True),
    Column("consistently_violated_percent_type", Double, nullable=True),
    Column("restraints_count", Integer, nullable=True),
    Column("violated_count", Integer, nullable=True),
    Column("percent_total", Double, nullable=True),
    Column("violated_percent_total", Double, nullable=True),
    Column("violated_percent_type", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_distance_violation_model_summary = Table(
    "pdbx_vrpt_distance_violation_model_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("max_violation", Double, nullable=True),
    Column("mean_violation", Double, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("standard_deviation", Double, nullable=True),
    Column("median_violation", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_distance_violation_model_restraints = Table(
    "pdbx_vrpt_distance_violation_model_restraints",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dist_rest_type", Text, nullable=True),
    Column("violations_count", Integer, nullable=True),
    Column("PDB_model_num", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["PDB_model_num"]},
)

pdbx_vrpt_violated_dihedralangle_restraints = Table(
    "pdbx_vrpt_violated_dihedralangle_restraints",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("violation", Double, nullable=True),
    Column("atom_3", Text, nullable=True),
    Column("atom_4", Text, nullable=True),
    Column("rlist_id", Integer, nullable=True),
    Column("rest_id", Integer, nullable=True),
    Column("instance_id_1", Text, nullable=True),
    Column("instance_id_2", Text, nullable=True),
    Column("instance_id_3", Text, nullable=True),
    Column("instance_id_4", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("fraction_of_ensemble_count", Integer, nullable=True),
    Column("fraction_of_ensemble_percent", Double, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_distance_violation_ensemble = Table(
    "pdbx_vrpt_distance_violation_ensemble",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("dist_rest_type", Text, nullable=True),
    Column("violations_count", Integer, nullable=True),
    Column("ensemble_distance_count", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violations_summary = Table(
    "pdbx_vrpt_dihedralangle_violations_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("restraint_type", Text, nullable=True),
    Column("consistently_violated_count", Integer, nullable=True),
    Column("consistently_violated_percent_total", Double, nullable=True),
    Column("consistently_violated_percent_type", Double, nullable=True),
    Column("restraints_count", Integer, nullable=True),
    Column("violated_count", Integer, nullable=True),
    Column("percent_total", Double, nullable=True),
    Column("violated_percent_total", Double, nullable=True),
    Column("violated_percent_type", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violation_model_summary = Table(
    "pdbx_vrpt_dihedralangle_violation_model_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("max_violation", Double, nullable=True),
    Column("mean_violation", Double, nullable=True),
    Column("standard_deviation", Double, nullable=True),
    Column("median_violation", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violation_model = Table(
    "pdbx_vrpt_dihedralangle_violation_model",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ang_rest_type", Text, nullable=True),
    Column("violations_count", Integer, nullable=True),
    Column("PDB_model_num", Integer, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_violation_ensemble_summary = Table(
    "pdbx_vrpt_dihedralangle_violation_ensemble_summary",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("fraction_of_ensemble_count", Integer, nullable=True),
    Column("fraction_of_ensemble_percent", Double, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_dihedralangle_ensemble_violation = Table(
    "pdbx_vrpt_dihedralangle_ensemble_violation",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ang_rest_type", Text, nullable=True),
    Column("violations_count", Integer, nullable=True),
    Column("ensemble_dihedral_count", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_residual_distance_violations = Table(
    "pdbx_vrpt_residual_distance_violations",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("max_violation", Double, nullable=True),
    Column("bins", Text, nullable=True),
    Column("violations_per_model", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["bins"]},
)

pdbx_vrpt_most_violated_distance_restraints = Table(
    "pdbx_vrpt_most_violated_distance_restraints",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("altcode_1", Text, nullable=True),
    Column("chain_1", Text, nullable=True),
    Column("resnum_1", Integer, nullable=True),
    Column("resname_1", Text, nullable=True),
    Column("ent_1", Text, nullable=True),
    Column("said_1", Text, nullable=True),
    Column("seq_1", Integer, nullable=True),
    Column("chain_2", Text, nullable=True),
    Column("altcode_2", Text, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("resnum_2", Integer, nullable=True),
    Column("resname_2", Text, nullable=True),
    Column("seq_2", Integer, nullable=True),
    Column("said_2", Text, nullable=True),
    Column("ent_2", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("mean_distance_violation", Double, nullable=True),
    Column("median_violation", Double, nullable=True),
    Column("standard_deviation", Double, nullable=True),
    Column("violated_models", Integer, nullable=True),
    Column("rlist_id", Integer, nullable=True),
    Column("rest_id", Integer, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_violated_distance_restraints = Table(
    "pdbx_vrpt_violated_distance_restraints",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("violation", Double, nullable=True),
    Column("rlist_id", Integer, nullable=True),
    Column("rest_id", Integer, nullable=True),
    Column("instance_id_1", Text, nullable=True),
    Column("instance_id_2", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id_1) -> pdbx_vrpt_model_instance(pdbid, id)
    # FK: (pdbid, instance_id_2) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_most_violated_dihedralangle_restraints = Table(
    "pdbx_vrpt_most_violated_dihedralangle_restraints",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("altcode_1", Text, nullable=True),
    Column("chain_1", Text, nullable=True),
    Column("resnum_1", Integer, nullable=True),
    Column("resname_1", Text, nullable=True),
    Column("ent_1", Text, nullable=True),
    Column("said_1", Text, nullable=True),
    Column("seq_1", Integer, nullable=True),
    Column("atom_1", Text, nullable=True),
    Column("chain_2", Text, nullable=True),
    Column("altcode_2", Text, nullable=True),
    Column("resnum_2", Integer, nullable=True),
    Column("resname_2", Text, nullable=True),
    Column("seq_2", Integer, nullable=True),
    Column("said_2", Text, nullable=True),
    Column("ent_2", Text, nullable=True),
    Column("atom_2", Text, nullable=True),
    Column("mean_angle_violation", Double, nullable=True),
    Column("standard_deviation", Double, nullable=True),
    Column("median_violation", Double, nullable=True),
    Column("altcode_3", Text, nullable=True),
    Column("chain_3", Text, nullable=True),
    Column("resnum_3", Integer, nullable=True),
    Column("resname_3", Text, nullable=True),
    Column("ent_3", Text, nullable=True),
    Column("said_3", Text, nullable=True),
    Column("seq_3", Integer, nullable=True),
    Column("atom_3", Text, nullable=True),
    Column("altcode_4", Text, nullable=True),
    Column("chain_4", Text, nullable=True),
    Column("resnum_4", Integer, nullable=True),
    Column("resname_4", Text, nullable=True),
    Column("ent_4", Text, nullable=True),
    Column("said_4", Text, nullable=True),
    Column("seq_4", Integer, nullable=True),
    Column("atom_4", Text, nullable=True),
    Column("rlist_id", Integer, nullable=True),
    Column("rest_id", Integer, nullable=True),
    Column("violated_models", Integer, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["altcode_2", "altcode_3", "chain_3"]},
)

pdbx_vrpt_model_instance_geometry = Table(
    "pdbx_vrpt_model_instance_geometry",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("OWAB", Double, nullable=True),
    Column("residue_inclusion", Double, nullable=True),
    Column("num_H_reduce", Integer, nullable=True),
    Column("num_bonds_RMSZ", Integer, nullable=True),
    Column("bonds_RMSZ", Double, nullable=True),
    Column("num_angles_RMSZ", Integer, nullable=True),
    Column("angles_RMSZ", Double, nullable=True),
    Column("program_for_bond_angle_geometry", Text, nullable=True),
    Column("average_occupancy", Double, nullable=True),
    Column("ligand_chirality_outlier", Text, nullable=True),
    Column("validate", Text, nullable=True),
    Column("cyrange_domain_id", Integer, nullable=True),
    Column("cis_peptide", Text, nullable=True),
    Column("RNA_score", Double, nullable=True),
    Column("RNA_suite", Text, nullable=True),
    Column("RNA_pucker", Text, nullable=True),
    Column("flippable_sidechain", Text, nullable=True),
    Column("ramachandran_class", Text, nullable=True),
    Column("rotamer_class", Text, nullable=True),
    Column("phi", Double, nullable=True),
    Column("psi", Double, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
    info={"keywords": ["RNA_pucker", "rotamer_class"]},
)

pdbx_vrpt_model_instance_density = Table(
    "pdbx_vrpt_model_instance_density",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("natoms_eds", Integer, nullable=True),
    Column("RSRCC", Double, nullable=True),
    Column("RSR", Double, nullable=True),
    Column("RSRZ", Double, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("EDIAm", Double, nullable=True),
    Column("OPIA", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_model_instance_map_fitting = Table(
    "pdbx_vrpt_model_instance_map_fitting",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("residue_inclusion", Double, nullable=True),
    Column("Q_score", Double, nullable=True),
    Column("instance_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, instance_id) -> pdbx_vrpt_model_instance(pdbid, id)
)

pdbx_vrpt_summary_diffraction = Table(
    "pdbx_vrpt_summary_diffraction",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("exp_method", Text, nullable=True),
    Column("Babinet_b", Double, nullable=True),
    Column("bulk_solvent_b", Double, nullable=True),
    Column("Wilson_B_estimate", Double, nullable=True),
    Column("I_over_sigma", Text, nullable=True),
    Column("num_miller_indices", Integer, nullable=True),
    Column("Babinet_k", Double, nullable=True),
    Column("bulk_solvent_k", Double, nullable=True),
    Column("Padilla_Yeates_L_mean", Double, nullable=True),
    Column("Padilla_Yeates_L2_mean", Double, nullable=True),
    Column("DCC_R", Double, nullable=True),
    Column("DCC_Rfree", Double, nullable=True),
    Column("EDS_R", Double, nullable=True),
    Column("EDS_res_high", Double, nullable=True),
    Column("EDS_res_low", Double, nullable=True),
    Column("Wilson_B_aniso", Text, nullable=True),
    Column("data_anisotropy", Double, nullable=True),
    Column("trans_NCS_details", Text, nullable=True),
    Column("B_factor_type", Text, nullable=True),
    Column("acentric_outliers", Integer, nullable=True),
    Column("centric_outliers", Integer, nullable=True),
    Column("data_completeness", Double, nullable=True),
    Column("number_reflns_R_free", Integer, nullable=True),
    Column("percent_free_reflections", Double, nullable=True),
    Column("percent_RSRZ_outliers", Double, nullable=True),
    Column("PDB_resolution_high", Double, nullable=True),
    Column("PDB_resolution_low", Double, nullable=True),
    Column("PDB_R", Double, nullable=True),
    Column("PDB_Rfree", Double, nullable=True),
    Column("twin_fraction", Text, nullable=True),
    Column("Fo_Fc_correlation", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("density_fitness_version", Text, nullable=True),
    Column("CCP4_version", Text, nullable=True),
    Column("EDS_R_warning", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("percent_ramachandran_outliers", Double, nullable=True),
    Column("clashscore", Double, nullable=True),
    Column("angles_RMSZ", Double, nullable=True),
    Column("bonds_RMSZ", Double, nullable=True),
    Column("num_angles_RMSZ", Integer, nullable=True),
    Column("num_bonds_RMSZ", Integer, nullable=True),
    Column("percent_rotamer_outliers", Double, nullable=True),
    Column("percent_ramachandran_outliers_full_length", Double, nullable=True),
    Column("percent_rotamer_outliers_full_length", Double, nullable=True),
    Column("clashscore_full_length", Double, nullable=True),
    Column("num_H_reduce", Integer, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_summary_nmr = Table(
    "pdbx_vrpt_summary_nmr",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("exp_method", Text, nullable=True),
    Column("nmr_models_consistency_flag", Text, nullable=True),
    Column("nmrclust_representative_model", Integer, nullable=True),
    Column("medoid_model", Integer, nullable=True),
    Column("nmrclust_number_of_outliers", Integer, nullable=True),
    Column("nmrclust_number_of_models", Integer, nullable=True),
    Column("nmrclust_number_of_clusters", Integer, nullable=True),
    Column("cyrange_number_of_domains", Integer, nullable=True),
    Column("chemical_shift_completeness", Double, nullable=True),
    Column("chemical_shift_completeness_full_length", Double, nullable=True),
    Column("cyrange_error", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["exp_method", "cyrange_error", "nmrclust_error"]},
)

pdbx_vrpt_summary_em = Table(
    "pdbx_vrpt_summary_em",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("exp_method", Text, nullable=True),
    Column("contour_level_primary_map", Double, nullable=True),
    Column("atom_inclusion_all_atoms", Double, nullable=True),
    Column("atom_inclusion_backbone", Double, nullable=True),
    Column("author_provided_fsc_resolution_by_cutoff_pt_143", Double, nullable=True),
    Column("author_provided_fsc_resolution_by_cutoff_pt_333", Double, nullable=True),
    Column("author_provided_fsc_resolution_by_cutoff_pt_5", Double, nullable=True),
    Column("author_provided_fsc_resolution_by_cutoff_halfbit", Double, nullable=True),
    Column("author_provided_fsc_resolution_by_cutoff_onebit", Double, nullable=True),
    Column(
        "author_provided_fsc_resolution_by_cutoff_threesigma", Double, nullable=True
    ),
    Column("calculated_fsc_resolution_by_cutoff_pt_143", Double, nullable=True),
    Column("calculated_fsc_resolution_by_cutoff_pt_333", Double, nullable=True),
    Column("calculated_fsc_resolution_by_cutoff_pt_5", Double, nullable=True),
    Column("calculated_fsc_resolution_by_cutoff_halfbit", Double, nullable=True),
    Column("calculated_fsc_resolution_by_cutoff_onebit", Double, nullable=True),
    Column("calculated_fsc_resolution_by_cutoff_threesigma", Double, nullable=True),
    Column("EMDB_resolution", Double, nullable=True),
    Column("Q_score", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["exp_method"]},
)

pdbx_vrpt_percentile_list = Table(
    "pdbx_vrpt_percentile_list",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("exp_method", Text, nullable=True),
    Column("range", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["exp_method", "range"]},
)

pdbx_vrpt_percentile_type = Table(
    "pdbx_vrpt_percentile_type",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_percentile_conditions = Table(
    "pdbx_vrpt_percentile_conditions",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("percentile_list_id", Text, nullable=True),
    Column("type_id", Text, nullable=True),
    Column("rank", Double, nullable=True),
    Column("res_high", Double, nullable=True),
    Column("res_low", Double, nullable=True),
    Column("number_entries_total", Integer, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, percentile_list_id) -> pdbx_vrpt_percentile_list(pdbid, id)
)

pdbx_vrpt_percentile_entity_view = Table(
    "pdbx_vrpt_percentile_entity_view",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("conditions_id", Text, nullable=True),
    Column("type_id", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("PDB_model_num", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("auth_asym_id", Text, nullable=True),
    Column("rank", Double, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, conditions_id) -> pdbx_vrpt_percentile_conditions(pdbid, id)
    info={"keywords": ["PDB_model_num", "auth_asym_id"]},
)

pdbx_vrpt_database = Table(
    "pdbx_vrpt_database",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("code", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("extended_code", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["code", "extended_code"]},
)

pdbx_vrpt_exptl = Table(
    "pdbx_vrpt_exptl",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["method"]},
)

pdbx_vrpt_entity = Table(
    "pdbx_vrpt_entity",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("description", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["description"]},
)

pdbx_vrpt_asym = Table(
    "pdbx_vrpt_asym",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("label_asym_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "label_asym_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, entity_id) -> pdbx_vrpt_entity(pdbid, id)
)

pdbx_vrpt_em_graph_fsc_indicator_curve = Table(
    "pdbx_vrpt_em_graph_fsc_indicator_curve",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("graph_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("curve_name", Text, nullable=True),
    Column("data_curve_name", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, graph_id) -> pdbx_vrpt_em_2d_graph_info(pdbid, graph_id)
    info={"keywords": ["graph_id", "type", "curve_name", "data_curve_name"]},
)

pdbx_vrpt_em_graph_fsc_curve = Table(
    "pdbx_vrpt_em_graph_fsc_curve",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("graph_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("curve_name", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, graph_id) -> pdbx_vrpt_em_2d_graph_info(pdbid, graph_id)
    info={"keywords": ["graph_id", "type", "curve_name"]},
)

pdbx_vrpt_em_resolution_intersections = Table(
    "pdbx_vrpt_em_resolution_intersections",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("resolution_units", Text, nullable=True),
    Column("spatial_frequency_units", Text, nullable=True),
    Column("correlation", Double, nullable=True),
    Column("resolution", Double, nullable=True),
    Column("spatial_frequency", Double, nullable=True),
    Column("curve", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["curve", "type"]},
)

pdbx_vrpt_em_graph_atom_inclusion = Table(
    "pdbx_vrpt_em_graph_atom_inclusion",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("graph_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "graph_id"),
    # FK: (pdbid) -> brief_summary(pdbid)
    # FK: (pdbid, graph_id) -> pdbx_vrpt_em_2d_graph_info(pdbid, graph_id)
    info={"keywords": ["graph_id"]},
)

pdbx_vrpt_em_details = Table(
    "pdbx_vrpt_em_details",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("recommended_contour_level", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_em_2d_graph_data = Table(
    "pdbx_vrpt_em_2d_graph_data",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("graph_data_id", Text, nullable=True),
    Column("x_value", Double, nullable=True),
    Column("y_value", Double, nullable=True),
    PrimaryKeyConstraint("pdbid", "ordinal"),
    # FK: (pdbid) -> brief_summary(pdbid)
)

pdbx_vrpt_em_2d_graph_info = Table(
    "pdbx_vrpt_em_2d_graph_info",
    metadata,
    Column("pdbid", Text, nullable=True),
    Column("graph_data_id", Text, nullable=True),
    Column("graph_id", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("x_axis_title", Text, nullable=True),
    Column("x_axis_units", Text, nullable=True),
    Column("y_axis_title", Text, nullable=True),
    Column("y_axis_scale", Text, nullable=True),
    Column("y_axis_units", Text, nullable=True),
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
    Column("pdbid", Text, nullable=True),
    Column("dict_location", Text, nullable=True),
    Column("dict_name", Text, nullable=True),
    Column("dict_version", Text, nullable=True),
    PrimaryKeyConstraint("pdbid", "dict_name", "dict_version"),
    # FK: (pdbid) -> brief_summary(pdbid)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)
