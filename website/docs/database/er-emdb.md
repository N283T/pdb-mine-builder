---
sidebar_label: ER Diagram
title: "emdb ER Diagram"
---

# emdb ER Diagram

- **Primary Key**: `emdb_id`
- **Tables**: 79

:::note
This schema has many tables. The diagram shows table names and primary key columns only. See the [schema reference](./emdb) for full column details.
:::

```mermaid
erDiagram
    brief_summary {
        text emdb_id PK
        text ___ "8 more columns"
    }
    audit_conform {
        text emdb_id PK
        text ___ "3 more columns"
    }
    chem_comp {
        text emdb_id PK
        text ___ "7 more columns"
    }
    citation {
        text emdb_id PK
        text ___ "15 more columns"
    }
    citation_author {
        text emdb_id PK
        text ___ "4 more columns"
    }
    database_2 {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_2d_crystal_entity {
        text emdb_id PK
        text ___ "9 more columns"
    }
    em_3d_crystal_entity {
        text emdb_id PK
        text ___ "10 more columns"
    }
    em_3d_fitting {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_3d_fitting_list {
        text emdb_id PK
        text ___ "12 more columns"
    }
    em_3d_reconstruction {
        text emdb_id PK
        text ___ "15 more columns"
    }
    em_admin {
        text emdb_id PK
        text ___ "11 more columns"
    }
    em_author_list {
        text emdb_id PK
        text ___ "3 more columns"
    }
    em_buffer {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_buffer_component {
        text emdb_id PK
        text ___ "6 more columns"
    }
    em_crystal_formation {
        text emdb_id PK
        text ___ "10 more columns"
    }
    em_ctf_correction {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_db_reference {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_db_reference_auxiliary {
        text emdb_id PK
        text ___ "2 more columns"
    }
    em_diffraction {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_diffraction_shell {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_diffraction_stats {
        text emdb_id PK
        text ___ "12 more columns"
    }
    em_embedding {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_entity_assembly {
        text emdb_id PK
        text ___ "9 more columns"
    }
    em_entity_assembly_molwt {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_entity_assembly_naturalsource {
        text emdb_id PK
        text ___ "11 more columns"
    }
    em_entity_assembly_recombinant {
        text emdb_id PK
        text ___ "7 more columns"
    }
    em_euler_angle_assignment {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_experiment {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_fiducial_markers {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_final_classification {
        text emdb_id PK
        text ___ "6 more columns"
    }
    em_focused_ion_beam {
        text emdb_id PK
        text ___ "11 more columns"
    }
    em_grid_pretreatment {
        text emdb_id PK
        text ___ "6 more columns"
    }
    em_helical_entity {
        text emdb_id PK
        text ___ "7 more columns"
    }
    em_high_pressure_freezing {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_image_processing {
        text emdb_id PK
        text ___ "3 more columns"
    }
    em_image_recording {
        text emdb_id PK
        text ___ "11 more columns"
    }
    em_image_scans {
        text emdb_id PK
        text ___ "9 more columns"
    }
    em_imaging {
        text emdb_id PK
        text ___ "28 more columns"
    }
    em_imaging_optics {
        text emdb_id PK
        text ___ "10 more columns"
    }
    em_map {
        text emdb_id PK
        text ___ "42 more columns"
    }
    em_obsolete {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_particle_selection {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_sample_support {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_single_particle_entity {
        text emdb_id PK
        text ___ "4 more columns"
    }
    em_software {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_specimen {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_staining {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_start_model {
        text emdb_id PK
        text ___ "12 more columns"
    }
    em_supersede {
        text emdb_id PK
        text ___ "2 more columns"
    }
    em_support_film {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_tomography {
        text emdb_id PK
        text ___ "8 more columns"
    }
    em_tomography_specimen {
        text emdb_id PK
        text ___ "7 more columns"
    }
    em_ultramicrotomy {
        text emdb_id PK
        text ___ "6 more columns"
    }
    em_virus_entity {
        text emdb_id PK
        text ___ "6 more columns"
    }
    em_virus_natural_host {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_virus_shell {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_virus_synthetic {
        text emdb_id PK
        text ___ "5 more columns"
    }
    em_vitrification {
        text emdb_id PK
        text ___ "9 more columns"
    }
    em_volume_selection {
        text emdb_id PK
        text ___ "7 more columns"
    }
    entity {
        text emdb_id PK
        text ___ "10 more columns"
    }
    entity_poly {
        text emdb_id PK
        text ___ "3 more columns"
    }
    entity_src_gen {
        text emdb_id PK
        text ___ "39 more columns"
    }
    entity_src_nat {
        text emdb_id PK
        text ___ "19 more columns"
    }
    entry {
        text emdb_id PK
        text ___ "1 more columns"
    }
    exptl {
        text emdb_id PK
        text ___ "2 more columns"
    }
    link_entry_pdbjplus {
        text emdb_id PK
        text ___ "2 more columns"
    }
    pdbx_audit_revision_category {
        text emdb_id PK
        text ___ "4 more columns"
    }
    pdbx_audit_revision_details {
        text emdb_id PK
        text ___ "7 more columns"
    }
    pdbx_audit_revision_group {
        text emdb_id PK
        text ___ "4 more columns"
    }
    pdbx_audit_revision_history {
        text emdb_id PK
        text ___ "6 more columns"
    }
    pdbx_audit_revision_item {
        text emdb_id PK
        text ___ "4 more columns"
    }
    pdbx_audit_support {
        text emdb_id PK
        text ___ "5 more columns"
    }
    pdbx_database_related {
        text emdb_id PK
        text ___ "4 more columns"
    }
    pdbx_entity_nonpoly {
        text emdb_id PK
        text ___ "3 more columns"
    }
    pdbx_entity_src_syn {
        text emdb_id PK
        text ___ "10 more columns"
    }
    pdbx_initial_refinement_model {
        text emdb_id PK
        text ___ "5 more columns"
    }
    struct_keywords {
        text emdb_id PK
        text ___ "4 more columns"
    }
    struct_ref {
        text emdb_id PK
        text ___ "4 more columns"
    }
```
