---
sidebar_position: 9
---

# ihm Schema

- **Primary Key**: `pdbid`
- **Tables**: 114

## atom_type

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| symbol | text |  |

## audit_author

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| name | text |  |
| pdbx_ordinal | integer |  |

## audit_conform

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| dict_location | text |  |
| dict_name | text |  |
| dict_version | text |  |

## brief_summary

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| docid | bigint |  |
| deposition_date | date |  |
| release_date | date |  |
| modification_date | date |  |
| deposit_author | text[] |  |
| citation_author | text[] |  |
| citation_title | text[] |  |
| citation_journal | text[] |  |
| citation_year | integer[] |  |
| citation_volume | text[] |  |
| citation_author_pri | text[] |  |
| citation_title_pri | text |  |
| citation_journal_pri | text |  |
| citation_year_pri | integer |  |
| citation_volume_pri | text |  |
| chain_type | text[] |  |
| chain_type_ids | integer[] |  |
| chain_number | integer |  |
| chain_length | integer[] |  |
| pdbx_descriptor | text |  |
| struct_title | text |  |
| ligand | text[] |  |
| exptl_method | text[] |  |
| exptl_method_ids | integer[] |  |
| biol_species | text |  |
| host_species | text |  |
| db_pubmed | text[] |  |
| db_doi | text[] |  |
| db_ec_number | text[] |  |
| db_goid | text[] |  |
| db_uniprot | text[] |  |
| db_genbank | text[] |  |
| db_embl | text[] |  |
| db_pir | text[] |  |
| db_emdb | text[] |  |
| pdb_related | text[] |  |
| keywords | text[] |  |
| aaseq | text |  |
| update_date | timestamp without time zone |  |
| db_pfam | text[] |  |
| plus_fields | jsonb |  |

## chem_comp

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| formula | text |  |
| formula_weight | double precision |  |
| id | text |  |
| mon_nstd_flag | text |  |
| name | text |  |
| type | text |  |
| pdbx_synonyms | text |  |

## citation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| country | text |  |
| id | text |  |
| journal_abbrev | text |  |
| journal_id_ASTM | text |  |
| journal_id_CSD | text |  |
| journal_id_ISSN | text |  |
| journal_issue | text |  |
| journal_volume | text |  |
| page_first | text |  |
| page_last | text |  |
| title | text |  |
| year | integer |  |
| pdbx_database_id_DOI | text |  |
| pdbx_database_id_PubMed | integer |  |

## citation_author

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| citation_id | text |  |
| name | text |  |
| ordinal | integer |  |

## database_2

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| database_id | text |  |
| database_code | text |  |
| pdbx_database_accession | text |  |
| pdbx_DOI | text |  |

## entity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| details | text |  |
| formula_weight | double precision |  |
| id | text |  |
| src_method | text |  |
| type | text |  |
| pdbx_description | text |  |
| pdbx_number_of_molecules | integer |  |

## entity_name_com

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| name | text |  |

## entity_name_sys

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| name | text |  |

## entity_poly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| nstd_chirality | text |  |
| nstd_linkage | text |  |
| nstd_monomer | text |  |
| type | text |  |
| type_details | text |  |
| pdbx_strand_id | text |  |
| pdbx_seq_one_letter_code | text |  |
| pdbx_seq_one_letter_code_can | text |  |
| pdbx_sequence_evidence_code | text |  |

## entity_poly_seq

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| hetero | text |  |
| mon_id | text |  |
| num | integer |  |

## entity_src_gen

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| gene_src_common_name | text |  |
| gene_src_genus | text |  |
| pdbx_gene_src_scientific_name | text |  |
| pdbx_host_org_strain | text |  |
| host_org_common_name | text |  |
| pdbx_host_org_scientific_name | text |  |
| pdbx_gene_src_ncbi_taxonomy_id | text |  |
| pdbx_host_org_ncbi_taxonomy_id | text |  |
| pdbx_src_id | integer |  |
| pdbx_alt_source_flag | text |  |

## entry

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | text |  |

## ihm_2dem_class_average_fitting

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| restraint_id | integer |  |
| model_id | integer |  |
| cross_correlation_coefficient | double precision |  |
| rot_matrix11 | double precision |  |
| rot_matrix21 | double precision |  |
| rot_matrix31 | double precision |  |
| rot_matrix12 | double precision |  |
| rot_matrix22 | double precision |  |
| rot_matrix32 | double precision |  |
| rot_matrix13 | double precision |  |
| rot_matrix23 | double precision |  |
| rot_matrix33 | double precision |  |
| tr_vector1 | double precision |  |
| tr_vector2 | double precision |  |
| tr_vector3 | double precision |  |

## ihm_2dem_class_average_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| dataset_list_id | integer |  |
| number_raw_micrographs | integer |  |
| pixel_size_width | double precision |  |
| pixel_size_height | double precision |  |
| image_resolution | double precision |  |
| image_segment_flag | text |  |
| number_of_projections | integer |  |
| struct_assembly_id | integer |  |
| details | text |  |

## ihm_3dem_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| dataset_list_id | integer |  |
| model_id | integer |  |
| struct_assembly_id | integer |  |
| fitting_method | text |  |
| number_of_gaussians | integer |  |
| map_segment_flag | text |  |
| cross_correlation_coefficient | double precision |  |
| fitting_method_citation_id | text |  |
| details | text |  |

## ihm_chemical_component_descriptor

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| chemical_name | text |  |
| common_name | text |  |
| auth_name | text |  |
| smiles | text |  |
| smiles_canonical | text |  |
| inchi | text |  |
| inchi_key | text |  |
| details | text |  |

## ihm_cross_link_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| group_id | integer |  |
| entity_description_1 | text |  |
| entity_description_2 | text |  |
| entity_id_1 | text |  |
| entity_id_2 | text |  |
| comp_id_1 | text |  |
| comp_id_2 | text |  |
| seq_id_1 | integer |  |
| seq_id_2 | integer |  |
| linker_type | text |  |
| linker_chem_comp_descriptor_id | integer |  |
| dataset_list_id | integer |  |
| details | text |  |

## ihm_cross_link_pseudo_site

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| restraint_id | integer |  |
| cross_link_partner | integer |  |
| pseudo_site_id | integer |  |
| model_id | integer |  |

## ihm_cross_link_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| group_id | integer |  |
| entity_id_1 | text |  |
| entity_id_2 | text |  |
| asym_id_1 | text |  |
| asym_id_2 | text |  |
| comp_id_1 | text |  |
| comp_id_2 | text |  |
| seq_id_1 | integer |  |
| seq_id_2 | integer |  |
| atom_id_1 | text |  |
| atom_id_2 | text |  |
| restraint_type | text |  |
| conditional_crosslink_flag | text |  |
| model_granularity | text |  |
| distance_threshold | double precision |  |
| psi | double precision |  |
| sigma_1 | double precision |  |
| sigma_2 | double precision |  |
| pseudo_site_flag | text |  |

## ihm_cross_link_result

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| restraint_id | integer |  |
| ensemble_id | integer |  |
| num_models | integer |  |
| model_group_id | integer |  |
| distance_threshold | double precision |  |
| median_distance | double precision |  |

## ihm_cross_link_result_parameters

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| restraint_id | integer |  |
| model_id | integer |  |
| psi | double precision |  |
| sigma_1 | double precision |  |
| sigma_2 | double precision |  |

## ihm_data_transformation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| rot_matrix11 | double precision |  |
| rot_matrix21 | double precision |  |
| rot_matrix31 | double precision |  |
| rot_matrix12 | double precision |  |
| rot_matrix22 | double precision |  |
| rot_matrix32 | double precision |  |
| rot_matrix13 | double precision |  |
| rot_matrix23 | double precision |  |
| rot_matrix33 | double precision |  |
| tr_vector1 | double precision |  |
| tr_vector2 | double precision |  |
| tr_vector3 | double precision |  |

## ihm_dataset_external_reference

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| dataset_list_id | integer |  |
| file_id | integer |  |

## ihm_dataset_group

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| name | text |  |
| application | text |  |
| details | text |  |

## ihm_dataset_group_link

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| dataset_list_id | integer |  |
| group_id | integer |  |

## ihm_dataset_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| data_type | text |  |
| details | text |  |
| database_hosted | text |  |

## ihm_dataset_related_db_reference

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| dataset_list_id | integer |  |
| db_name | text |  |
| accession_code | text |  |
| version | text |  |
| details | text |  |

## ihm_derived_angle_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| group_id | integer |  |
| feature_id_1 | integer |  |
| feature_id_2 | integer |  |
| feature_id_3 | integer |  |
| group_conditionality | text |  |
| restraint_type | text |  |
| angle_threshold_mean | double precision |  |
| angle_threshold_esd | double precision |  |
| dataset_list_id | integer |  |

## ihm_derived_dihedral_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| group_id | integer |  |
| feature_id_1 | integer |  |
| feature_id_2 | integer |  |
| feature_id_3 | integer |  |
| feature_id_4 | integer |  |
| group_conditionality | text |  |
| restraint_type | text |  |
| dihedral_threshold_mean | double precision |  |
| dihedral_threshold_esd | double precision |  |
| dataset_list_id | integer |  |

## ihm_derived_distance_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| group_id | integer |  |
| feature_id_1 | integer |  |
| feature_id_2 | integer |  |
| group_conditionality | text |  |
| random_exclusion_fraction | double precision |  |
| distance_lower_limit | double precision |  |
| distance_upper_limit | double precision |  |
| distance_upper_limit_esd | double precision |  |
| probability | double precision |  |
| restraint_type | text |  |
| distance_threshold_mean | double precision |  |
| distance_threshold_esd | double precision |  |
| dataset_list_id | integer |  |

## ihm_ensemble_info

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ensemble_id | integer |  |
| ensemble_name | text |  |
| post_process_id | integer |  |
| model_group_id | integer |  |
| model_group_superimposed_flag | text |  |
| ensemble_clustering_method | text |  |
| ensemble_clustering_feature | text |  |
| num_ensemble_models | integer |  |
| num_ensemble_models_deposited | integer |  |
| ensemble_precision_value | double precision |  |
| ensemble_file_id | integer |  |
| details | text |  |
| sub_sample_flag | text |  |
| sub_sampling_type | text |  |

## ihm_ensemble_sub_sample

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| name | text |  |
| ensemble_id | integer |  |
| num_models | integer |  |
| num_models_deposited | integer |  |
| file_id | integer |  |

## ihm_entity_poly_segment

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| entity_id | text |  |
| seq_id_begin | integer |  |
| seq_id_end | integer |  |
| comp_id_begin | text |  |
| comp_id_end | text |  |

## ihm_entry_collection

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | text |  |
| details | text |  |

## ihm_entry_collection_mapping

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| collection_id | text |  |
| entry_id | text |  |

## ihm_epr_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal_id | integer |  |
| dataset_list_id | integer |  |
| model_id | integer |  |
| fitting_particle_type | text |  |
| fitting_method | text |  |
| fitting_method_citation_id | text |  |
| fitting_state | text |  |
| fitting_software_id | integer |  |
| chi_value | double precision |  |
| details | text |  |

## ihm_external_files

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| reference_id | integer |  |
| file_path | text |  |
| file_format | text |  |
| content_type | text |  |
| file_size_bytes | double precision |  |
| details | text |  |

## ihm_external_reference_info

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| reference_id | integer |  |
| reference_provider | text |  |
| reference_type | text |  |
| reference | text |  |
| refers_to | text |  |
| associated_url | text |  |
| details | text |  |

## ihm_feature_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| feature_id | integer |  |
| feature_type | text |  |
| entity_type | text |  |
| details | text |  |

## ihm_geometric_object_axis

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| object_id | integer |  |
| axis_type | text |  |

## ihm_geometric_object_center

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| xcoord | double precision |  |
| ycoord | double precision |  |
| zcoord | double precision |  |

## ihm_geometric_object_distance_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| object_id | integer |  |
| feature_id | integer |  |
| object_characteristic | text |  |
| restraint_type | text |  |
| harmonic_force_constant | double precision |  |
| group_conditionality | text |  |
| distance_lower_limit | double precision |  |
| distance_upper_limit | double precision |  |
| distance_probability | double precision |  |
| dataset_list_id | integer |  |
| details | text |  |

## ihm_geometric_object_half_torus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| object_id | integer |  |
| thickness_th | double precision |  |
| section | text |  |

## ihm_geometric_object_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| object_id | integer |  |
| object_type | text |  |
| object_name | text |  |
| object_description | text |  |

## ihm_geometric_object_plane

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| object_id | integer |  |
| plane_type | text |  |
| transformation_id | integer |  |

## ihm_geometric_object_torus

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| object_id | integer |  |
| center_id | integer |  |
| transformation_id | integer |  |
| major_radius_R | double precision |  |
| minor_radius_r | double precision |  |

## ihm_geometric_object_transformation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| rot_matrix11 | double precision |  |
| rot_matrix21 | double precision |  |
| rot_matrix31 | double precision |  |
| rot_matrix12 | double precision |  |
| rot_matrix22 | double precision |  |
| rot_matrix32 | double precision |  |
| rot_matrix13 | double precision |  |
| rot_matrix23 | double precision |  |
| rot_matrix33 | double precision |  |
| tr_vector1 | double precision |  |
| tr_vector2 | double precision |  |
| tr_vector3 | double precision |  |

## ihm_hdx_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| feature_id | integer |  |
| protection_factor | double precision |  |
| dataset_list_id | integer |  |
| details | text |  |

## ihm_hydroxyl_radical_fp_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| entity_id | text |  |
| asym_id | text |  |
| comp_id | text |  |
| seq_id | integer |  |
| fp_rate | double precision |  |
| fp_rate_error | double precision |  |
| log_pf | double precision |  |
| log_pf_error | double precision |  |
| predicted_sasa | double precision |  |
| dataset_list_id | integer |  |
| software_id | integer |  |

## ihm_interface_residue_feature

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal_id | integer |  |
| feature_id | integer |  |
| binding_partner_entity_id | text |  |
| binding_partner_asym_id | text |  |
| dataset_list_id | integer |  |
| details | text |  |

## ihm_kinetic_rate

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| transition_rate_constant | double precision |  |
| scheme_connectivity_id | integer |  |
| dataset_group_id | integer |  |
| external_file_id | integer |  |

## ihm_localization_density_files

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| file_id | integer |  |
| ensemble_id | integer |  |
| entity_id | text |  |
| entity_poly_segment_id | integer |  |
| asym_id | text |  |

## ihm_model_group

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| name | text |  |
| details | text |  |

## ihm_model_group_link

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| model_id | integer |  |
| group_id | integer |  |

## ihm_model_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| model_id | integer |  |
| model_name | text |  |
| assembly_id | integer |  |
| protocol_id | integer |  |
| representation_id | integer |  |

## ihm_model_representation

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| name | text |  |
| details | text |  |

## ihm_model_representation_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| representation_id | integer |  |
| entity_poly_segment_id | integer |  |
| entity_id | text |  |
| entity_description | text |  |
| entity_asym_id | text |  |
| model_object_primitive | text |  |
| starting_model_id | text |  |
| model_mode | text |  |
| model_granularity | text |  |
| model_object_count | integer |  |
| description | text |  |

## ihm_model_representative

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| model_group_id | integer |  |
| model_id | integer |  |
| selection_criteria | text |  |

## ihm_modeling_post_process

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| protocol_id | integer |  |
| analysis_id | integer |  |
| step_id | integer |  |
| struct_assembly_id | integer |  |
| dataset_group_id | integer |  |
| type | text |  |
| feature | text |  |
| feature_name | text |  |
| num_models_begin | integer |  |
| num_models_end | integer |  |
| script_file_id | integer |  |
| software_id | integer |  |
| details | text |  |

## ihm_modeling_protocol

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| num_steps | integer |  |
| protocol_name | text |  |
| details | text |  |

## ihm_modeling_protocol_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| protocol_id | integer |  |
| step_id | integer |  |
| struct_assembly_id | integer |  |
| dataset_group_id | integer |  |
| struct_assembly_description | text |  |
| step_name | text |  |
| step_method | text |  |
| num_models_begin | integer |  |
| num_models_end | integer |  |
| multi_scale_flag | text |  |
| multi_state_flag | text |  |
| ordered_flag | text |  |
| ensemble_flag | text |  |
| script_file_id | integer |  |
| software_id | integer |  |
| description | text |  |

## ihm_multi_state_model_group_link

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| state_id | integer |  |
| model_group_id | integer |  |

## ihm_multi_state_modeling

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| state_id | integer |  |
| state_group_id | integer |  |
| population_fraction | double precision |  |
| state_type | text |  |
| state_name | text |  |
| experiment_type | text |  |
| details | text |  |

## ihm_multi_state_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| name | text |  |
| details | text |  |

## ihm_multi_state_scheme_connectivity

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| scheme_id | integer |  |
| begin_state_id | integer |  |
| end_state_id | integer |  |
| dataset_group_id | integer |  |

## ihm_non_poly_feature

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal_id | integer |  |
| feature_id | integer |  |
| entity_id | text |  |
| asym_id | text |  |
| comp_id | text |  |
| atom_id | text |  |

## ihm_ordered_model

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| process_id | integer |  |
| process_description | text |  |
| edge_id | integer |  |
| edge_description | text |  |
| step_id | integer |  |
| step_description | text |  |
| ordered_by | text |  |
| model_group_id_begin | integer |  |
| model_group_id_end | integer |  |

## ihm_poly_atom_feature

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal_id | integer |  |
| feature_id | integer |  |
| entity_id | text |  |
| asym_id | text |  |
| comp_id | text |  |
| seq_id | integer |  |
| atom_id | text |  |

## ihm_poly_probe_conjugate

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| probe_id | integer |  |
| position_id | integer |  |
| chem_comp_descriptor_id | integer |  |
| ambiguous_stoichiometry_flag | text |  |
| dataset_list_id | integer |  |

## ihm_poly_probe_position

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| entity_id | text |  |
| entity_description | text |  |
| seq_id | integer |  |
| comp_id | text |  |
| mutation_flag | text |  |
| mut_res_chem_comp_id | text |  |
| modification_flag | text |  |
| mod_res_chem_comp_descriptor_id | integer |  |
| description | text |  |

## ihm_poly_residue_feature

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal_id | integer |  |
| feature_id | integer |  |
| entity_id | text |  |
| asym_id | text |  |
| comp_id_begin | text |  |
| comp_id_end | text |  |
| seq_id_begin | integer |  |
| seq_id_end | integer |  |
| residue_range_granularity | text |  |
| rep_atom | text |  |
| interface_residue_flag | text |  |

## ihm_predicted_contact_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| group_id | integer |  |
| entity_description_1 | text |  |
| entity_description_2 | text |  |
| entity_id_1 | text |  |
| entity_id_2 | text |  |
| asym_id_1 | text |  |
| asym_id_2 | text |  |
| comp_id_1 | text |  |
| comp_id_2 | text |  |
| seq_id_1 | integer |  |
| seq_id_2 | integer |  |
| rep_atom_1 | text |  |
| rep_atom_2 | text |  |
| distance_lower_limit | double precision |  |
| distance_upper_limit | double precision |  |
| probability | double precision |  |
| restraint_type | text |  |
| model_granularity | text |  |
| dataset_list_id | integer |  |
| software_id | integer |  |

## ihm_probe_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| probe_id | integer |  |
| probe_name | text |  |
| reactive_probe_flag | text |  |
| reactive_probe_name | text |  |
| probe_origin | text |  |
| probe_link_type | text |  |
| probe_chem_comp_descriptor_id | integer |  |
| reactive_probe_chem_comp_descriptor_id | integer |  |

## ihm_pseudo_site

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| Cartn_x | double precision |  |
| Cartn_y | double precision |  |
| Cartn_z | double precision |  |
| description | text |  |

## ihm_related_datasets

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| dataset_list_id_derived | integer |  |
| dataset_list_id_primary | integer |  |
| transformation_id | integer |  |

## ihm_relaxation_time

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| value | double precision |  |
| unit | text |  |
| amplitude | double precision |  |
| dataset_group_id | integer |  |
| external_file_id | integer |  |
| details | text |  |

## ihm_relaxation_time_multi_state_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| relaxation_time_id | integer |  |
| scheme_id | integer |  |

## ihm_residues_not_modeled

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| model_id | integer |  |
| entity_description | text |  |
| entity_id | text |  |
| asym_id | text |  |
| seq_id_begin | integer |  |
| seq_id_end | integer |  |
| comp_id_begin | text |  |
| comp_id_end | text |  |
| reason | text |  |

## ihm_sas_restraint

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| dataset_list_id | integer |  |
| model_id | integer |  |
| struct_assembly_id | integer |  |
| profile_segment_flag | text |  |
| fitting_atom_type | text |  |
| fitting_method | text |  |
| fitting_state | text |  |
| radius_of_gyration | double precision |  |
| chi_value | double precision |  |
| details | text |  |

## ihm_sphere_obj_site

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| entity_id | text |  |
| seq_id_begin | integer |  |
| seq_id_end | integer |  |
| asym_id | text |  |
| Cartn_x | double precision |  |
| Cartn_y | double precision |  |
| Cartn_z | double precision |  |
| object_radius | double precision |  |
| rmsf | double precision |  |
| model_id | integer |  |

## ihm_starting_comparative_models

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| starting_model_id | text |  |
| starting_model_auth_asym_id | text |  |
| starting_model_seq_id_begin | integer |  |
| starting_model_seq_id_end | integer |  |
| template_auth_asym_id | text |  |
| template_seq_id_begin | integer |  |
| template_seq_id_end | integer |  |
| template_sequence_identity | double precision |  |
| template_sequence_identity_denominator | integer |  |
| template_dataset_list_id | integer |  |
| alignment_file_id | integer |  |
| details | text |  |

## ihm_starting_computational_models

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| starting_model_id | text |  |
| script_file_id | integer |  |
| software_id | integer |  |

## ihm_starting_model_coord

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal_id | integer |  |
| starting_model_id | text |  |
| group_PDB | text |  |
| id | integer |  |
| type_symbol | text |  |
| entity_id | text |  |
| atom_id | text |  |
| comp_id | text |  |
| seq_id | integer |  |
| asym_id | text |  |
| Cartn_x | double precision |  |
| Cartn_y | double precision |  |
| Cartn_z | double precision |  |
| B_iso_or_equiv | double precision |  |

## ihm_starting_model_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| starting_model_id | text |  |
| entity_id | text |  |
| entity_description | text |  |
| asym_id | text |  |
| entity_poly_segment_id | integer |  |
| starting_model_source | text |  |
| starting_model_auth_asym_id | text |  |
| starting_model_sequence_offset | integer |  |
| dataset_list_id | integer |  |
| description | text |  |

## ihm_starting_model_seq_dif

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| entity_id | text |  |
| asym_id | text |  |
| seq_id | integer |  |
| comp_id | text |  |
| starting_model_id | text |  |
| db_entity_id | text |  |
| db_asym_id | text |  |
| db_seq_id | integer |  |
| db_comp_id | text |  |
| details | text |  |

## ihm_struct_assembly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| name | text |  |
| description | text |  |

## ihm_struct_assembly_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| assembly_id | integer |  |
| parent_assembly_id | integer |  |
| entity_description | text |  |
| entity_id | text |  |
| asym_id | text |  |
| entity_poly_segment_id | integer |  |

## pdbx_audit_revision_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal | integer |  |
| revision_ordinal | integer |  |
| data_content_type | text |  |
| provider | text |  |
| type | text |  |

## pdbx_audit_revision_history

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| ordinal | integer |  |
| data_content_type | text |  |
| major_revision | integer |  |
| minor_revision | integer |  |
| revision_date | date |  |

## pdbx_branch_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| asym_id | text |  |
| mon_id | text |  |
| num | integer |  |
| pdb_asym_id | text |  |
| pdb_seq_num | text |  |
| pdb_mon_id | text |  |
| auth_seq_num | text |  |
| auth_mon_id | text |  |

## pdbx_database_status

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| status_code | text |  |
| entry_id | text |  |
| recvd_initial_deposition_date | date |  |
| deposit_site | text |  |
| process_site | text |  |

## pdbx_entity_branch

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| type | text |  |

## pdbx_entity_branch_descriptor

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| descriptor | text |  |
| type | text |  |
| program | text |  |
| program_version | text |  |
| ordinal | integer |  |

## pdbx_entity_branch_link

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| link_id | integer |  |
| entity_id | text |  |
| entity_branch_list_num_1 | integer |  |
| entity_branch_list_num_2 | integer |  |
| comp_id_1 | text |  |
| comp_id_2 | text |  |
| atom_id_1 | text |  |
| leaving_atom_id_1 | text |  |
| atom_id_2 | text |  |
| leaving_atom_id_2 | text |  |
| value_order | text |  |

## pdbx_entity_branch_list

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| comp_id | text |  |
| num | integer |  |

## pdbx_entity_nonpoly

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| comp_id | text |  |
| name | text |  |

## pdbx_entity_poly_na_type

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entity_id | text |  |
| type | text |  |

## pdbx_entry_details

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entry_id | text |  |
| sequence_details | text |  |

## pdbx_nonpoly_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| asym_id | text |  |
| entity_id | text |  |
| mon_id | text |  |
| pdb_strand_id | text |  |
| ndb_seq_num | text |  |
| pdb_seq_num | text |  |
| auth_seq_num | text |  |
| pdb_mon_id | text |  |
| auth_mon_id | text |  |

## pdbx_poly_seq_scheme

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| asym_id | text |  |
| entity_id | text |  |
| seq_id | integer |  |
| hetero | text |  |
| mon_id | text |  |
| pdb_strand_id | text |  |
| ndb_seq_num | integer |  |
| pdb_seq_num | text |  |
| auth_seq_num | text |  |
| pdb_mon_id | text |  |
| auth_mon_id | text |  |
| pdb_ins_code | text |  |

## pdbx_protein_info

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | text |  |
| name | text |  |
| num_per_asym_unit | integer |  |

## pdbx_unobs_or_zero_occ_atoms

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| polymer_flag | text |  |
| occupancy_flag | integer |  |
| PDB_model_num | integer |  |
| auth_asym_id | text |  |
| auth_atom_id | text |  |
| auth_comp_id | text |  |
| auth_seq_id | text |  |
| label_atom_id | text |  |
| label_asym_id | text |  |
| label_comp_id | text |  |
| label_seq_id | integer |  |

## pdbx_unobs_or_zero_occ_residues

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | integer |  |
| polymer_flag | text |  |
| occupancy_flag | integer |  |
| PDB_model_num | integer |  |
| auth_asym_id | text |  |
| auth_comp_id | text |  |
| auth_seq_id | text |  |
| label_asym_id | text |  |
| label_comp_id | text |  |
| label_seq_id | integer |  |

## software

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| citation_id | text |  |
| classification | text |  |
| description | text |  |
| dependencies | text |  |
| location | text |  |
| name | text |  |
| type | text |  |
| version | text |  |
| pdbx_ordinal | integer |  |

## struct

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| entry_id | text |  |
| title | text |  |
| pdbx_structure_determination_methodology | text |  |
| pdbx_descriptor | text |  |
| pdbx_model_details | text |  |
| pdbx_model_type_details | text |  |
| pdbx_CASP_flag | text |  |
| pdbx_details | text |  |

## struct_asym

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| details | text |  |
| entity_id | text |  |
| id | text |  |
| pdbx_modified | text |  |
| pdbx_blank_PDB_chainid_flag | text |  |
| pdbx_PDB_id | text |  |
| pdbx_alt_id | text |  |
| pdbx_type | text |  |
| pdbx_order | integer |  |

## struct_conn

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| conn_type_id | text |  |
| id | text |  |
| ptnr1_label_asym_id | text |  |
| ptnr1_label_atom_id | text |  |
| ptnr1_label_comp_id | text |  |
| ptnr1_label_seq_id | integer |  |
| ptnr1_auth_asym_id | text |  |
| ptnr1_auth_comp_id | text |  |
| ptnr1_auth_seq_id | text |  |
| ptnr1_symmetry | text |  |
| ptnr2_label_asym_id | text |  |
| ptnr2_label_atom_id | text |  |
| ptnr2_label_comp_id | text |  |
| ptnr2_auth_asym_id | text |  |
| ptnr2_auth_comp_id | text |  |
| ptnr2_auth_seq_id | text |  |
| ptnr2_symmetry | text |  |
| pdbx_dist_value | double precision |  |

## struct_conn_type

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| id | text |  |

## struct_ref

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| db_code | text |  |
| db_name | text |  |
| details | text |  |
| entity_id | text |  |
| id | text |  |
| pdbx_db_accession | text |  |
| pdbx_db_isoform | text |  |
| pdbx_seq_one_letter_code | text |  |
| pdbx_align_begin | text |  |
| pdbx_align_end | text |  |

## struct_ref_seq

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| align_id | text |  |
| db_align_beg | integer |  |
| db_align_end | integer |  |
| ref_id | text |  |
| seq_align_beg | integer |  |
| seq_align_end | integer |  |

## struct_ref_seq_dif

| Column | Type | Description |
|--------|------|-------------|
| pdbid | text |  |
| align_id | text |  |
| db_mon_id | text |  |
| details | text |  |
| mon_id | text |  |
| seq_num | integer |  |
| pdbx_seq_db_seq_num | text |  |
| pdbx_ordinal | integer |  |
