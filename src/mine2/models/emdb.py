"""SQLAlchemy schema definition for emdb.

Auto-generated from schemas/emdb.def.yml by scripts/convert_yaml_to_sa.py.
"""

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
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
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData(schema="emdb")
metadata.info = {"entry_pk": "emdb_id"}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("deposition_date", Date, nullable=True),
    Column("header_release_date", Date, nullable=True),
    Column("map_release_date", Date, nullable=True),
    Column("modification_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("content", JSONB, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("emdb_id"),
)

audit_conform = Table(
    "audit_conform",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("dict_location", Text, nullable=True),
    Column("dict_name", Text, nullable=True),
    Column("dict_version", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "dict_name", "dict_version"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("mon_nstd_flag", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_synonyms", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
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

citation = Table(
    "citation",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("country", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("journal_abbrev", Text, nullable=True),
    Column("journal_id_ASTM", Text, nullable=True),
    Column("journal_id_CSD", Text, nullable=True),
    Column("journal_id_ISSN", Text, nullable=True),
    Column("journal_volume", Text, nullable=True),
    Column("page_first", Text, nullable=True),
    Column("page_last", Text, nullable=True),
    Column("title", Text, nullable=True),
    Column("year", Integer, nullable=True),
    Column("database_id_CSD", Text, nullable=True),
    Column("pdbx_database_id_DOI", Text, nullable=True),
    Column("pdbx_database_id_PubMed", Integer, nullable=True),
    Column("unpublished_flag", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
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
    Column("emdb_id", Text, nullable=True),
    Column("citation_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("identifier_ORCID", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "citation_id", "name", "ordinal"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, citation_id) -> citation(emdb_id, id)
    info={"keywords": ["name", "identifier_ORCID"]},
)

database_2 = Table(
    "database_2",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("database_id", Text, nullable=True),
    Column("database_code", Text, nullable=True),
    Column("pdbx_database_accession", Text, nullable=True),
    Column("pdbx_DOI", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "database_id", "database_code"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["database_code", "pdbx_DOI"]},
)

entity = Table(
    "entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("formula_weight", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("src_method", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_description", Text, nullable=True),
    Column("pdbx_number_of_molecules", Integer, nullable=True),
    Column("pdbx_mutation", Text, nullable=True),
    Column("pdbx_fragment", Text, nullable=True),
    Column("pdbx_ec", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "details",
            "pdbx_description",
            "pdbx_mutation",
            "pdbx_fragment",
            "pdbx_modification",
        ]
    },
)

entity_poly = Table(
    "entity_poly",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("pdbx_seq_one_letter_code", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "type_details",
            "pdbx_strand_id",
            "pdbx_seq_one_letter_code",
            "pdbx_seq_one_letter_code_can",
            "pdbx_target_identifier",
            "pdbx_seq_one_letter_code_sample",
            "pdbx_N_terminal_seq_one_letter_code",
            "pdbx_C_terminal_seq_one_letter_code",
            "pdbx_seq_three_letter_code",
            "pdbx_seq_db_id",
        ]
    },
)

entry = Table(
    "entry",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

exptl = Table(
    "exptl",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entry_id", "method"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["absorpt_process_details", "details", "method_details"]},
)

struct_keywords = Table(
    "struct_keywords",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("text", Text, nullable=True),
    Column("pdbx_keywords", Text, nullable=True),
    Column("pdbx_details", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["text", "pdbx_keywords", "pdbx_details"]},
)

struct_ref = Table(
    "struct_ref",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("db_code", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "biol_id",
            "db_code",
            "db_name",
            "details",
            "pdbx_seq_one_letter_code",
        ]
    },
)

pdbx_database_related = Table(
    "pdbx_database_related",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("db_id", Text, nullable=True),
    Column("content_type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "db_name", "db_id", "content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "db_id"]},
)

pdbx_entity_nonpoly = Table(
    "pdbx_entity_nonpoly",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("comp_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={"keywords": ["name"]},
)

entity_src_nat = Table(
    "entity_src_nat",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("common_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("genus", Text, nullable=True),
    Column("strain", Text, nullable=True),
    Column("tissue", Text, nullable=True),
    Column("pdbx_organism_scientific", Text, nullable=True),
    Column("pdbx_variant", Text, nullable=True),
    Column("pdbx_cell_line", Text, nullable=True),
    Column("pdbx_atcc", Text, nullable=True),
    Column("pdbx_cellular_location", Text, nullable=True),
    Column("pdbx_organ", Text, nullable=True),
    Column("pdbx_cell", Text, nullable=True),
    Column("pdbx_plasmid_details", Text, nullable=True),
    Column("pdbx_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
    Column("pdbx_beg_seq_num", Integer, nullable=True),
    Column("pdbx_end_seq_num", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_id", "pdbx_src_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "common_name",
            "details",
            "genus",
            "species",
            "strain",
            "tissue",
            "tissue_fraction",
            "pdbx_organism_scientific",
            "pdbx_secretion",
            "pdbx_fragment",
            "pdbx_variant",
            "pdbx_cell_line",
            "pdbx_atcc",
            "pdbx_cellular_location",
            "pdbx_organ",
            "pdbx_organelle",
            "pdbx_cell",
            "pdbx_plasmid_name",
            "pdbx_plasmid_details",
            "pdbx_ncbi_taxonomy_id",
            "pdbx_culture_collection",
        ]
    },
)

entity_src_gen = Table(
    "entity_src_gen",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("gene_src_common_name", Text, nullable=True),
    Column("gene_src_details", Text, nullable=True),
    Column("gene_src_genus", Text, nullable=True),
    Column("gene_src_species", Text, nullable=True),
    Column("gene_src_strain", Text, nullable=True),
    Column("gene_src_tissue", Text, nullable=True),
    Column("pdbx_gene_src_gene", Text, nullable=True),
    Column("pdbx_gene_src_scientific_name", Text, nullable=True),
    Column("pdbx_gene_src_variant", Text, nullable=True),
    Column("pdbx_gene_src_cell_line", Text, nullable=True),
    Column("pdbx_gene_src_atcc", Text, nullable=True),
    Column("pdbx_gene_src_organ", Text, nullable=True),
    Column("pdbx_gene_src_cell", Text, nullable=True),
    Column("pdbx_host_org_organ", Text, nullable=True),
    Column("pdbx_host_org_organelle", Text, nullable=True),
    Column("pdbx_host_org_cellular_location", Text, nullable=True),
    Column("pdbx_host_org_strain", Text, nullable=True),
    Column("pdbx_description", Text, nullable=True),
    Column("host_org_common_name", Text, nullable=True),
    Column("host_org_details", Text, nullable=True),
    Column("plasmid_details", Text, nullable=True),
    Column("plasmid_name", Text, nullable=True),
    Column("pdbx_host_org_variant", Text, nullable=True),
    Column("pdbx_host_org_cell_line", Text, nullable=True),
    Column("pdbx_host_org_atcc", Text, nullable=True),
    Column("pdbx_host_org_culture_collection", Text, nullable=True),
    Column("pdbx_host_org_cell", Text, nullable=True),
    Column("pdbx_host_org_scientific_name", Text, nullable=True),
    Column("pdbx_host_org_tissue", Text, nullable=True),
    Column("pdbx_host_org_vector", Text, nullable=True),
    Column("pdbx_host_org_vector_type", Text, nullable=True),
    Column("pdbx_gene_src_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_host_org_ncbi_taxonomy_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
    Column("pdbx_seq_type", Text, nullable=True),
    Column("pdbx_beg_seq_num", Integer, nullable=True),
    Column("pdbx_end_seq_num", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_id", "pdbx_src_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "gene_src_common_name",
            "gene_src_details",
            "gene_src_genus",
            "gene_src_species",
            "gene_src_strain",
            "gene_src_tissue",
            "gene_src_tissue_fraction",
            "host_org_genus",
            "host_org_species",
            "pdbx_gene_src_fragment",
            "pdbx_gene_src_gene",
            "pdbx_gene_src_scientific_name",
            "pdbx_gene_src_variant",
            "pdbx_gene_src_cell_line",
            "pdbx_gene_src_atcc",
            "pdbx_gene_src_organ",
            "pdbx_gene_src_organelle",
            "pdbx_gene_src_plasmid",
            "pdbx_gene_src_plasmid_name",
            "pdbx_gene_src_cell",
            "pdbx_gene_src_cellular_location",
            "pdbx_host_org_gene",
            "pdbx_host_org_organ",
            "pdbx_host_org_organelle",
            "pdbx_host_org_cellular_location",
            "pdbx_host_org_strain",
            "pdbx_host_org_tissue_fraction",
            "pdbx_description",
            "host_org_common_name",
            "host_org_details",
            "host_org_strain",
            "plasmid_details",
            "plasmid_name",
            "pdbx_host_org_variant",
            "pdbx_host_org_cell_line",
            "pdbx_host_org_atcc",
            "pdbx_host_org_culture_collection",
            "pdbx_host_org_cell",
            "pdbx_host_org_scientific_name",
            "pdbx_host_org_tissue",
            "pdbx_host_org_vector",
            "pdbx_host_org_vector_type",
            "gene_src_dev_stage",
            "pdbx_gene_src_ncbi_taxonomy_id",
            "pdbx_host_org_ncbi_taxonomy_id",
            "pdbx_gene_src_culture_collection",
        ]
    },
)

pdbx_entity_src_syn = Table(
    "pdbx_entity_src_syn",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("organism_scientific", Text, nullable=True),
    Column("organism_common_name", Text, nullable=True),
    Column("strain", Text, nullable=True),
    Column("ncbi_taxonomy_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True),
    Column("pdbx_src_id", Integer, nullable=True),
    Column("pdbx_alt_source_flag", Text, nullable=True),
    Column("pdbx_beg_seq_num", Integer, nullable=True),
    Column("pdbx_end_seq_num", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_id", "pdbx_src_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "details",
            "organism_scientific",
            "organism_common_name",
            "strain",
            "ncbi_taxonomy_id",
        ]
    },
)

em_entity_assembly = Table(
    "em_entity_assembly",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("parent_id", Integer, nullable=True),
    Column("source", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("synonym", Text, nullable=True),
    Column("entity_id_list", Text, nullable=True),
    Column("chimera", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "type",
            "name",
            "details",
            "go_id",
            "ipr_id",
            "synonym",
            "oligomeric_details",
            "entity_id_list",
            "ebi_organism_scientific",
            "ebi_organism_common",
            "ebi_strain",
            "ebi_tissue",
            "ebi_cell",
            "ebi_organelle",
            "ebi_cellular_location",
            "ebi_expression_system",
            "ebi_expression_system_plasmid",
        ]
    },
)

em_virus_entity = Table(
    "em_virus_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("virus_type", Text, nullable=True),
    Column("virus_isolate", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("enveloped", Text, nullable=True),
    Column("empty", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={
        "keywords": [
            "virus_host_category",
            "virus_host_species",
            "virus_host_growth_cell",
            "ictvdb_id",
            "details",
        ]
    },
)

em_sample_support = Table(
    "em_sample_support",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("film_material", Text, nullable=True),
    Column("grid_material", Text, nullable=True),
    Column("grid_mesh_size", Integer, nullable=True),
    Column("grid_type", Text, nullable=True),
    Column("pretreatment", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "specimen_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["method", "grid_type", "pretreatment", "details"]},
)

em_buffer = Table(
    "em_buffer",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("pH", Double, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "specimen_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["name", "details"]},
)

em_vitrification = Table(
    "em_vitrification",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("cryogen_name", Text, nullable=True),
    Column("humidity", Double, nullable=True),
    Column("temp", Double, nullable=True),
    Column("chamber_temperature", Double, nullable=True),
    Column("instrument", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "specimen_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["method", "time_resolved_state", "details"]},
)

em_imaging = Table(
    "em_imaging",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("residual_tilt", Double, nullable=True),
    Column("sample_support_id", Text, nullable=True),
    Column("detector_id", Text, nullable=True),
    Column("scans_id", Text, nullable=True),
    Column("microscope_id", Text, nullable=True),
    Column("microscope_model", Text, nullable=True),
    Column("specimen_holder_model", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("accelerating_voltage", Integer, nullable=True),
    Column("illumination_mode", Text, nullable=True),
    Column("mode", Text, nullable=True),
    Column("nominal_cs", Double, nullable=True),
    Column("nominal_defocus_min", Double, nullable=True),
    Column("nominal_defocus_max", Double, nullable=True),
    Column("calibrated_defocus_min", Double, nullable=True),
    Column("calibrated_defocus_max", Double, nullable=True),
    Column("nominal_magnification", Integer, nullable=True),
    Column("calibrated_magnification", Integer, nullable=True),
    Column("electron_source", Text, nullable=True),
    Column("recording_temperature_minimum", Double, nullable=True),
    Column("recording_temperature_maximum", Double, nullable=True),
    Column("alignment_procedure", Text, nullable=True),
    Column("c2_aperture_diameter", Double, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("cryogen", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entry_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={
        "keywords": [
            "astigmatism",
            "electron_beam_tilt_params",
            "specimen_holder_type",
            "details",
            "electron_source",
            "energy_filter",
            "energy_window",
            "microscope_serial_number",
            "microscope_version",
        ]
    },
)

em_image_scans = Table(
    "em_image_scans",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("scanner_model", Text, nullable=True),
    Column("sampling_size", Double, nullable=True),
    Column("dimension_height", Integer, nullable=True),
    Column("dimension_width", Integer, nullable=True),
    Column("frames_per_image", Integer, nullable=True),
    Column("image_recording_id", Text, nullable=True),
    Column("used_frames_per_image", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_recording_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["details"]},
)

em_3d_reconstruction = Table(
    "em_3d_reconstruction",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("algorithm", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("resolution", Double, nullable=True),
    Column("resolution_method", Text, nullable=True),
    Column("nominal_pixel_size", Double, nullable=True),
    Column("actual_pixel_size", Double, nullable=True),
    Column("num_particles", Integer, nullable=True),
    Column("num_class_averages", Integer, nullable=True),
    Column("fsc_type", Text, nullable=True),
    Column("refinement_type", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("symmetry_type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={
        "keywords": [
            "method",
            "algorithm",
            "details",
            "resolution_method",
            "magnification_calibration",
            "ctf_correction_method",
            "euler_angles_details",
            "software",
        ]
    },
)

em_3d_fitting = Table(
    "em_3d_fitting",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("target_criteria", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("overall_b_value", Double, nullable=True),
    Column("ref_space", Text, nullable=True),
    Column("ref_protocol", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["method", "target_criteria", "software_name", "details"]},
)

em_3d_fitting_list = Table(
    "em_3d_fitting_list",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("3d_fitting_id", Text, nullable=True),
    Column("pdb_entry_id", Text, nullable=True),
    Column("pdb_chain_id", Text, nullable=True),
    Column("pdb_chain_residue_range", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("chain_id", Text, nullable=True),
    Column("chain_residue_range", Text, nullable=True),
    Column("source_name", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("accession_code", Text, nullable=True),
    Column("initial_refinement_model_id", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "3d_fitting_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "accession_code"]},
)

em_helical_entity = Table(
    "em_helical_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("axial_symmetry", Text, nullable=True),
    Column("angular_rotation_per_subunit", Double, nullable=True),
    Column("axial_rise_per_subunit", Double, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "hand"]},
)

em_experiment = Table(
    "em_experiment",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("reconstruction_method", Text, nullable=True),
    Column("aggregation_state", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["specimen_type"]},
)

em_single_particle_entity = Table(
    "em_single_particle_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("point_symmetry", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_admin = Table(
    "em_admin",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("current_status", Text, nullable=True),
    Column("deposition_date", Date, nullable=True),
    Column("deposition_site", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("last_update", Date, nullable=True),
    Column("map_release_date", Date, nullable=True),
    Column("header_release_date", Date, nullable=True),
    Column("title", Text, nullable=True),
    Column("process_site", Text, nullable=True),
    Column("composite_map", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["details", "title"]},
)

em_author_list = Table(
    "em_author_list",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("author", Text, nullable=True),
    Column("identifier_ORCID", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["author", "identifier_ORCID"]},
)

em_db_reference = Table(
    "em_db_reference",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("access_code", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("relationship", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_db_reference_auxiliary = Table(
    "em_db_reference_auxiliary",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("link_type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_obsolete = Table(
    "em_obsolete",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("date", Date, nullable=True),
    Column("details", Text, nullable=True),
    Column("entry", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "entry"]},
)

em_supersede = Table(
    "em_supersede",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry", Text, nullable=True),
    Column("id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "entry"]},
)

em_entity_assembly_molwt = Table(
    "em_entity_assembly_molwt",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("experimental_flag", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("units", Text, nullable=True),
    Column("value", Double, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["method"]},
)

em_entity_assembly_naturalsource = Table(
    "em_entity_assembly_naturalsource",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("cell", Text, nullable=True),
    Column("cellular_location", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("organelle", Text, nullable=True),
    Column("organ", Text, nullable=True),
    Column("strain", Text, nullable=True),
    Column("tissue", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={
        "keywords": [
            "cell",
            "cellular_location",
            "organism",
            "organelle",
            "organ",
            "strain",
            "tissue",
            "details",
        ]
    },
)

em_entity_assembly_recombinant = Table(
    "em_entity_assembly_recombinant",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("cell", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("plasmid", Text, nullable=True),
    Column("strain", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["cell", "organism", "plasmid", "strain"]},
)

em_virus_natural_host = Table(
    "em_virus_natural_host",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("organism", Text, nullable=True),
    Column("strain", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_assembly_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_synthetic = Table(
    "em_virus_synthetic",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("organism", Text, nullable=True),
    Column("ncbi_tax_id", Integer, nullable=True),
    Column("strain", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_assembly_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_shell = Table(
    "em_virus_shell",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("diameter", Double, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("triangulation", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "entity_assembly_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["name"]},
)

em_specimen = Table(
    "em_specimen",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("concentration", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("embedding_applied", Boolean, nullable=True),
    Column("experiment_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("shadowing_applied", Boolean, nullable=True),
    Column("staining_applied", Boolean, nullable=True),
    Column("vitrification_applied", Boolean, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "experiment_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_embedding = Table(
    "em_embedding",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("material", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "material"]},
)

em_fiducial_markers = Table(
    "em_fiducial_markers",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("diameter", Double, nullable=True),
    Column("em_tomography_specimen_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("manufacturer", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["manufacturer"]},
)

em_focused_ion_beam = Table(
    "em_focused_ion_beam",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("current", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("duration", Double, nullable=True),
    Column("em_tomography_specimen_id", Text, nullable=True),
    Column("final_thickness", Integer, nullable=True),
    Column("id", Text, nullable=True),
    Column("initial_thickness", Integer, nullable=True),
    Column("instrument", Text, nullable=True),
    Column("ion", Text, nullable=True),
    Column("temperature", Integer, nullable=True),
    Column("voltage", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["details", "instrument", "ion"]},
)

em_grid_pretreatment = Table(
    "em_grid_pretreatment",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("atmosphere", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("pressure", Double, nullable=True),
    Column("sample_support_id", Text, nullable=True),
    Column("time", Integer, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["atmosphere"]},
)

em_ultramicrotomy = Table(
    "em_ultramicrotomy",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("em_tomography_specimen_id", Text, nullable=True),
    Column("final_thickness", Integer, nullable=True),
    Column("id", Text, nullable=True),
    Column("instrument", Text, nullable=True),
    Column("temperature", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["details", "instrument"]},
)

em_high_pressure_freezing = Table(
    "em_high_pressure_freezing",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("em_tomography_specimen_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("instrument", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["details", "instrument"]},
)

em_tomography_specimen = Table(
    "em_tomography_specimen",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("cryo_protectant", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("fiducial_markers", Text, nullable=True),
    Column("high_pressure_freezing", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("sectioning", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["cryo_protectant", "details"]},
)

em_crystal_formation = Table(
    "em_crystal_formation",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("atmosphere", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("instrument", Text, nullable=True),
    Column("lipid_mixture", Text, nullable=True),
    Column("lipid_protein_ratio", Double, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("temperature", Integer, nullable=True),
    Column("time", Integer, nullable=True),
    Column("time_unit", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["atmosphere", "details", "instrument", "lipid_mixture"]},
)

em_staining = Table(
    "em_staining",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("material", Text, nullable=True),
    Column("specimen_id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "material"]},
)

em_support_film = Table(
    "em_support_film",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("material", Text, nullable=True),
    Column("sample_support_id", Text, nullable=True),
    Column("thickness", Double, nullable=True),
    Column("topology", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_buffer_component = Table(
    "em_buffer_component",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("buffer_id", Text, nullable=True),
    Column("concentration", Double, nullable=True),
    Column("concentration_units", Text, nullable=True),
    Column("formula", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("name", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "buffer_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["concentration_units", "name"]},
)

em_diffraction = Table(
    "em_diffraction",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("camera_length", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("tilt_angle_list", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["tilt_angle_list"]},
)

em_diffraction_shell = Table(
    "em_diffraction_shell",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("em_diffraction_stats_id", Text, nullable=True),
    Column("fourier_space_coverage", Double, nullable=True),
    Column("high_resolution", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("low_resolution", Double, nullable=True),
    Column("multiplicity", Double, nullable=True),
    Column("num_structure_factors", Integer, nullable=True),
    Column("phase_residual", Double, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_diffraction_stats = Table(
    "em_diffraction_stats",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("fourier_space_coverage", Double, nullable=True),
    Column("high_resolution", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("num_intensities_measured", Integer, nullable=True),
    Column("num_structure_factors", Integer, nullable=True),
    Column("overall_phase_error", Double, nullable=True),
    Column("overall_phase_residual", Double, nullable=True),
    Column("phase_error_rejection_criteria", Text, nullable=True),
    Column("r_merge", Double, nullable=True),
    Column("r_sym", Double, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "phase_error_rejection_criteria"]},
)

em_tomography = Table(
    "em_tomography",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("axis1_angle_increment", Double, nullable=True),
    Column("axis1_max_angle", Double, nullable=True),
    Column("axis1_min_angle", Double, nullable=True),
    Column("axis2_angle_increment", Double, nullable=True),
    Column("axis2_max_angle", Double, nullable=True),
    Column("axis2_min_angle", Double, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "imaging_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_image_recording = Table(
    "em_image_recording",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("average_exposure_time", Double, nullable=True),
    Column("avg_electron_dose_per_subtomogram", Double, nullable=True),
    Column("avg_electron_dose_per_image", Double, nullable=True),
    Column("details", Text, nullable=True),
    Column("detector_mode", Text, nullable=True),
    Column("film_or_detector_model", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("num_diffraction_images", Integer, nullable=True),
    Column("num_grids_imaged", Integer, nullable=True),
    Column("num_real_images", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "imaging_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "film_or_detector_model"]},
)

em_imaging_optics = Table(
    "em_imaging_optics",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("chr_aberration_corrector", Text, nullable=True),
    Column("energyfilter_lower", Text, nullable=True),
    Column("energyfilter_slit_width", Double, nullable=True),
    Column("energyfilter_name", Text, nullable=True),
    Column("energyfilter_upper", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("phase_plate", Text, nullable=True),
    Column("sph_aberration_corrector", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "imaging_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "chr_aberration_corrector",
            "energyfilter_lower",
            "energyfilter_name",
            "energyfilter_upper",
            "phase_plate",
            "sph_aberration_corrector",
            "details",
        ]
    },
)

em_final_classification = Table(
    "em_final_classification",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("avg_num_images_per_class", Integer, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("num_classes", Integer, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_start_model = Table(
    "em_start_model",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("insilico_model", Text, nullable=True),
    Column("orthogonal_tilt_angle1", Double, nullable=True),
    Column("orthogonal_tilt_angle2", Double, nullable=True),
    Column("orthogonal_tilt_num_images", Integer, nullable=True),
    Column("other", Text, nullable=True),
    Column("pdb_id", Text, nullable=True),
    Column("random_conical_tilt_angle", Double, nullable=True),
    Column("random_conical_tilt_num_images", Integer, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": ["details", "insilico_model", "other", "pdb_id"],
        "pkout": True,
    },
)

em_software = Table(
    "em_software",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("category", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("fitting_id", Text, nullable=True),
    Column("imaging_id", Text, nullable=True),
    Column("name", Text, nullable=True),
    Column("version", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "name", "version"]},
)

em_euler_angle_assignment = Table(
    "em_euler_angle_assignment",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("order", Text, nullable=True),
    Column("proj_matching_angular_sampling", Double, nullable=True),
    Column("proj_matching_merit_function", Text, nullable=True),
    Column("proj_matching_num_projections", Integer, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "proj_matching_merit_function"]},
)

em_ctf_correction = Table(
    "em_ctf_correction",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("em_image_processing_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "type"]},
)

em_volume_selection = Table(
    "em_volume_selection",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("method", Text, nullable=True),
    Column("num_tomograms", Integer, nullable=True),
    Column("num_volumes_extracted", Integer, nullable=True),
    Column("reference_model", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "method", "reference_model"]},
)

em_3d_crystal_entity = Table(
    "em_3d_crystal_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("angle_alpha", Double, nullable=True),
    Column("angle_beta", Double, nullable=True),
    Column("angle_gamma", Double, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("length_a", Double, nullable=True),
    Column("length_b", Double, nullable=True),
    Column("length_c", Double, nullable=True),
    Column("space_group_name", Text, nullable=True),
    Column("space_group_num", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["space_group_name"]},
)

em_2d_crystal_entity = Table(
    "em_2d_crystal_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("angle_gamma", Double, nullable=True),
    Column("c_sampling_length", Double, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True),
    Column("length_a", Double, nullable=True),
    Column("length_b", Double, nullable=True),
    Column("length_c", Double, nullable=True),
    Column("space_group_name_H-M", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_image_processing = Table(
    "em_image_processing",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_recording_id", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "image_recording_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_particle_selection = Table(
    "em_particle_selection",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("id", Text, nullable=True),
    Column("image_processing_id", Text, nullable=True),
    Column("num_particles_selected", BigInteger, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "method", "reference_model"]},
)

em_map = Table(
    "em_map",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("annotation_details", Text, nullable=True),
    Column("axis_order_fast", Text, nullable=True),
    Column("axis_order_medium", Text, nullable=True),
    Column("axis_order_slow", Text, nullable=True),
    Column("cell_a", Double, nullable=True),
    Column("cell_b", Double, nullable=True),
    Column("cell_c", Double, nullable=True),
    Column("cell_alpha", Double, nullable=True),
    Column("cell_beta", Double, nullable=True),
    Column("cell_gamma", Double, nullable=True),
    Column("contour_level", Double, nullable=True),
    Column("contour_level_source", Text, nullable=True),
    Column("data_type", Text, nullable=True),
    Column("dimensions_col", Integer, nullable=True),
    Column("dimensions_row", Integer, nullable=True),
    Column("dimensions_sec", Integer, nullable=True),
    Column("endian_type", Text, nullable=True),
    Column("file", Text, nullable=True),
    Column("format", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("partition", Integer, nullable=True),
    Column("entry_id", Text, nullable=True),
    Column("label", Text, nullable=True),
    Column("limit_col", Integer, nullable=True),
    Column("limit_row", Integer, nullable=True),
    Column("limit_sec", Integer, nullable=True),
    Column("origin_col", Integer, nullable=True),
    Column("origin_row", Integer, nullable=True),
    Column("origin_sec", Integer, nullable=True),
    Column("pixel_spacing_x", Double, nullable=True),
    Column("pixel_spacing_y", Double, nullable=True),
    Column("pixel_spacing_z", Double, nullable=True),
    Column("size_kb", BigInteger, nullable=True),
    Column("spacing_x", Integer, nullable=True),
    Column("spacing_y", Integer, nullable=True),
    Column("spacing_z", Integer, nullable=True),
    Column("statistics_average", Double, nullable=True),
    Column("statistics_maximum", Double, nullable=True),
    Column("statistics_minimum", Double, nullable=True),
    Column("statistics_std", Double, nullable=True),
    Column("symmetry_space_group", Integer, nullable=True),
    Column("type", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["annotation_details", "file", "original_file", "label"]},
)

pdbx_audit_revision_history = Table(
    "pdbx_audit_revision_history",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("major_revision", Integer, nullable=True),
    Column("minor_revision", Integer, nullable=True),
    Column("revision_date", Date, nullable=True),
    Column("part_number", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

pdbx_audit_revision_group = Table(
    "pdbx_audit_revision_group",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("group", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
)

pdbx_audit_revision_category = Table(
    "pdbx_audit_revision_category",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("category", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
)

pdbx_audit_revision_details = Table(
    "pdbx_audit_revision_details",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("provider", Text, nullable=True),
    Column("type", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
    info={"keywords": ["description", "details"]},
)

pdbx_audit_revision_item = Table(
    "pdbx_audit_revision_item",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    Column("revision_ordinal", Integer, nullable=True),
    Column("data_content_type", Text, nullable=True),
    Column("item", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
)

pdbx_audit_support = Table(
    "pdbx_audit_support",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("funding_organization", Text, nullable=True),
    Column("country", Text, nullable=True),
    Column("grant_number", Text, nullable=True),
    Column("details", Text, nullable=True),
    Column("ordinal", Integer, nullable=True),
    PrimaryKeyConstraint("emdb_id", "ordinal"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["funding_organization", "country", "grant_number", "details"]},
)

pdbx_initial_refinement_model = Table(
    "pdbx_initial_refinement_model",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Integer, nullable=True),
    Column("type", Text, nullable=True),
    Column("source_name", Text, nullable=True),
    Column("accession_code", Text, nullable=True),
    Column("details", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["accession_code", "details"]},
)

link_entry_pdbjplus = Table(
    "link_entry_pdbjplus",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("db_accession", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("emdb_id", "db_name"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["db_name"]},
)
