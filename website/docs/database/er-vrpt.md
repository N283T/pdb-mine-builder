---
sidebar_label: ER Diagram
title: "vrpt ER Diagram"
---

# vrpt ER Diagram

- **Primary Key**: `pdbid`
- **Tables**: 69

:::note
This schema has many tables. The diagram shows table names and primary key columns only. See the [schema reference](./vrpt) for full column details.
:::

```mermaid
erDiagram
    brief_summary {
        text pdbid PK
        text ___ "3 more columns"
    }
    audit_conform {
        text pdbid PK
        text ___ "3 more columns"
    }
    entity {
        text pdbid PK
        text ___ "10 more columns"
    }
    entry {
        text pdbid PK
        text ___ "1 more columns"
    }
    pdbx_vrpt_assign_completeness_full_length {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_assign_completeness_well_defined {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_asym {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_vrpt_chemical_shift_list {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_vrpt_chemical_shift_outlier {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_vrpt_cyrange_domain {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_vrpt_database {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_dihedralangle_ensemble_violation {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_dihedralangle_violation_ensemble_summary {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_dihedralangle_violation_model {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_dihedralangle_violation_model_summary {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_dihedralangle_violations_summary {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_vrpt_distance_violation_ensemble {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_distance_violation_model_restraints {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_distance_violation_model_summary {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_distance_violation_summary {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_vrpt_distance_violations_ensemble_summary {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_em_2d_graph_data {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_em_2d_graph_info {
        text pdbid PK
        text ___ "8 more columns"
    }
    pdbx_vrpt_em_details {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_vrpt_em_graph_atom_inclusion {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_vrpt_em_graph_fsc_curve {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_em_graph_fsc_indicator_curve {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_em_resolution_intersections {
        text pdbid PK
        text ___ "8 more columns"
    }
    pdbx_vrpt_entity {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_exptl {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_vrpt_instance_clashes {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_instance_intra_angle_outliers {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_vrpt_instance_intra_bond_outliers {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_vrpt_instance_intra_plane_outliers {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_instance_mogul_angle_outliers {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_vrpt_instance_mogul_bond_outliers {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_vrpt_instance_mogul_ring_outliers {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_vrpt_instance_mogul_torsion_outliers {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_vrpt_instance_stereo_outliers {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_instance_symm_clashes {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_vrpt_model_instance {
        text pdbid PK
        text ___ "21 more columns"
    }
    pdbx_vrpt_model_instance_density {
        text pdbid PK
        text ___ "8 more columns"
    }
    pdbx_vrpt_model_instance_geometry {
        text pdbid PK
        text ___ "23 more columns"
    }
    pdbx_vrpt_model_instance_map_fitting {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_model_list {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_most_violated_dihedralangle_restraints {
        text pdbid PK
        text ___ "39 more columns"
    }
    pdbx_vrpt_most_violated_distance_restraints {
        text pdbid PK
        text ___ "23 more columns"
    }
    pdbx_vrpt_percentile_conditions {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_vrpt_percentile_entity_view {
        text pdbid PK
        text ___ "8 more columns"
    }
    pdbx_vrpt_percentile_list {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_percentile_type {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_vrpt_random_coil_index {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_vrpt_referencing_offset {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_vrpt_residual_angle_violations {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_residual_distance_violations {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_restraint_summary {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_vrpt_software {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_vrpt_summary {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_vrpt_summary_diffraction {
        text pdbid PK
        text ___ "35 more columns"
    }
    pdbx_vrpt_summary_em {
        text pdbid PK
        text ___ "19 more columns"
    }
    pdbx_vrpt_summary_entity_fit_to_map {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_vrpt_summary_entity_geometry {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_vrpt_summary_geometry {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_vrpt_summary_nmr {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_vrpt_unmapped_chemical_shift {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_vrpt_unparsed_chemical_shift {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_vrpt_violated_dihedralangle_restraints {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_vrpt_violated_distance_restraints {
        text pdbid PK
        text ___ "8 more columns"
    }
    struct_asym {
        text pdbid PK
        text ___ "3 more columns"
    }
```
