---
sidebar_label: ER Diagram
title: "ihm ER Diagram"
---

# ihm ER Diagram

- **Primary Key**: `pdbid`
- **Tables**: 114

:::note
This schema has many tables. The diagram shows table names and primary key columns only. See the [schema reference](./ihm) for full column details.
:::

```mermaid
erDiagram
    brief_summary {
        text pdbid PK
        text ___ "41 more columns"
    }
    atom_type {
        text pdbid PK
        text ___ "1 more columns"
    }
    audit_author {
        text pdbid PK
        text ___ "2 more columns"
    }
    audit_conform {
        text pdbid PK
        text ___ "3 more columns"
    }
    chem_comp {
        text pdbid PK
        text ___ "7 more columns"
    }
    citation {
        text pdbid PK
        text ___ "14 more columns"
    }
    citation_author {
        text pdbid PK
        text ___ "3 more columns"
    }
    database_2 {
        text pdbid PK
        text ___ "4 more columns"
    }
    entity {
        text pdbid PK
        text ___ "7 more columns"
    }
    entity_name_com {
        text pdbid PK
        text ___ "2 more columns"
    }
    entity_name_sys {
        text pdbid PK
        text ___ "2 more columns"
    }
    entity_poly {
        text pdbid PK
        text ___ "10 more columns"
    }
    entity_poly_seq {
        text pdbid PK
        text ___ "4 more columns"
    }
    entity_src_gen {
        text pdbid PK
        text ___ "11 more columns"
    }
    entry {
        text pdbid PK
        text ___ "1 more columns"
    }
    ihm_2dem_class_average_fitting {
        text pdbid PK
        text ___ "16 more columns"
    }
    ihm_2dem_class_average_restraint {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_3dem_restraint {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_chemical_component_descriptor {
        text pdbid PK
        text ___ "9 more columns"
    }
    ihm_cross_link_list {
        text pdbid PK
        text ___ "14 more columns"
    }
    ihm_cross_link_pseudo_site {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_cross_link_restraint {
        text pdbid PK
        text ___ "20 more columns"
    }
    ihm_cross_link_result {
        text pdbid PK
        text ___ "7 more columns"
    }
    ihm_cross_link_result_parameters {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_data_transformation {
        text pdbid PK
        text ___ "13 more columns"
    }
    ihm_dataset_external_reference {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_dataset_group {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_dataset_group_link {
        text pdbid PK
        text ___ "2 more columns"
    }
    ihm_dataset_list {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_dataset_related_db_reference {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_derived_angle_restraint {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_derived_dihedral_restraint {
        text pdbid PK
        text ___ "11 more columns"
    }
    ihm_derived_distance_restraint {
        text pdbid PK
        text ___ "14 more columns"
    }
    ihm_ensemble_info {
        text pdbid PK
        text ___ "14 more columns"
    }
    ihm_ensemble_sub_sample {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_entity_poly_segment {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_entry_collection {
        text pdbid PK
        text ___ "2 more columns"
    }
    ihm_entry_collection_mapping {
        text pdbid PK
        text ___ "2 more columns"
    }
    ihm_epr_restraint {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_external_files {
        text pdbid PK
        text ___ "7 more columns"
    }
    ihm_external_reference_info {
        text pdbid PK
        text ___ "7 more columns"
    }
    ihm_feature_list {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_geometric_object_axis {
        text pdbid PK
        text ___ "2 more columns"
    }
    ihm_geometric_object_center {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_geometric_object_distance_restraint {
        text pdbid PK
        text ___ "12 more columns"
    }
    ihm_geometric_object_half_torus {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_geometric_object_list {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_geometric_object_plane {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_geometric_object_torus {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_geometric_object_transformation {
        text pdbid PK
        text ___ "13 more columns"
    }
    ihm_hdx_restraint {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_hydroxyl_radical_fp_restraint {
        text pdbid PK
        text ___ "12 more columns"
    }
    ihm_interface_residue_feature {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_kinetic_rate {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_localization_density_files {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_model_group {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_model_group_link {
        text pdbid PK
        text ___ "2 more columns"
    }
    ihm_model_list {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_model_representation {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_model_representation_details {
        text pdbid PK
        text ___ "12 more columns"
    }
    ihm_model_representative {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_modeling_post_process {
        text pdbid PK
        text ___ "14 more columns"
    }
    ihm_modeling_protocol {
        text pdbid PK
        text ___ "4 more columns"
    }
    ihm_modeling_protocol_details {
        text pdbid PK
        text ___ "17 more columns"
    }
    ihm_multi_state_model_group_link {
        text pdbid PK
        text ___ "2 more columns"
    }
    ihm_multi_state_modeling {
        text pdbid PK
        text ___ "7 more columns"
    }
    ihm_multi_state_scheme {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_multi_state_scheme_connectivity {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_non_poly_feature {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_ordered_model {
        text pdbid PK
        text ___ "9 more columns"
    }
    ihm_poly_atom_feature {
        text pdbid PK
        text ___ "7 more columns"
    }
    ihm_poly_probe_conjugate {
        text pdbid PK
        text ___ "6 more columns"
    }
    ihm_poly_probe_position {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_poly_residue_feature {
        text pdbid PK
        text ___ "11 more columns"
    }
    ihm_predicted_contact_restraint {
        text pdbid PK
        text ___ "21 more columns"
    }
    ihm_probe_list {
        text pdbid PK
        text ___ "8 more columns"
    }
    ihm_pseudo_site {
        text pdbid PK
        text ___ "5 more columns"
    }
    ihm_related_datasets {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_relaxation_time {
        text pdbid PK
        text ___ "7 more columns"
    }
    ihm_relaxation_time_multi_state_scheme {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_residues_not_modeled {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_sas_restraint {
        text pdbid PK
        text ___ "11 more columns"
    }
    ihm_sphere_obj_site {
        text pdbid PK
        text ___ "11 more columns"
    }
    ihm_starting_comparative_models {
        text pdbid PK
        text ___ "13 more columns"
    }
    ihm_starting_computational_models {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_starting_model_coord {
        text pdbid PK
        text ___ "14 more columns"
    }
    ihm_starting_model_details {
        text pdbid PK
        text ___ "10 more columns"
    }
    ihm_starting_model_seq_dif {
        text pdbid PK
        text ___ "11 more columns"
    }
    ihm_struct_assembly {
        text pdbid PK
        text ___ "3 more columns"
    }
    ihm_struct_assembly_details {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_audit_revision_details {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_audit_revision_history {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_branch_scheme {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_database_status {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_entity_branch {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_entity_branch_descriptor {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_entity_branch_link {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_entity_branch_list {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_entity_nonpoly {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_entity_poly_na_type {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_entry_details {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_nonpoly_scheme {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_poly_seq_scheme {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_protein_info {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_unobs_or_zero_occ_atoms {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_unobs_or_zero_occ_residues {
        text pdbid PK
        text ___ "10 more columns"
    }
    software {
        text pdbid PK
        text ___ "9 more columns"
    }
    struct {
        text pdbid PK
        text ___ "8 more columns"
    }
    struct_asym {
        text pdbid PK
        text ___ "9 more columns"
    }
    struct_conn {
        text pdbid PK
        text ___ "18 more columns"
    }
    struct_conn_type {
        text pdbid PK
        text ___ "1 more columns"
    }
    struct_ref {
        text pdbid PK
        text ___ "10 more columns"
    }
    struct_ref_seq {
        text pdbid PK
        text ___ "6 more columns"
    }
    struct_ref_seq_dif {
        text pdbid PK
        text ___ "7 more columns"
    }
```
