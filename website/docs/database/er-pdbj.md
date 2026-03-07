---
sidebar_label: ER Diagram
title: "pdbj ER Diagram"
---

# pdbj ER Diagram

- **Primary Key**: `pdbid`
- **Tables**: 250

:::note
This schema has many tables. The diagram shows table names and primary key columns only. See the [schema reference](./pdbj) for full column details.
:::

```mermaid
erDiagram
    brief_summary {
        text pdbid PK
        text ___ "43 more columns"
    }
    align_pdbjplus {
        text pdbid PK
        text ___ "9 more columns"
    }
    atom_sites {
        text pdbid PK
        text ___ "25 more columns"
    }
    atom_sites_footnote {
        text pdbid PK
        text ___ "2 more columns"
    }
    atom_type {
        text pdbid PK
        text ___ "20 more columns"
    }
    audit {
        text pdbid PK
        text ___ "4 more columns"
    }
    audit_author {
        text pdbid PK
        text ___ "3 more columns"
    }
    audit_conform {
        text pdbid PK
        text ___ "3 more columns"
    }
    cell {
        text pdbid PK
        text ___ "21 more columns"
    }
    cell_measurement {
        text pdbid PK
        text ___ "5 more columns"
    }
    chem_comp {
        text pdbid PK
        text ___ "7 more columns"
    }
    chem_comp_atom {
        text pdbid PK
        text ___ "6 more columns"
    }
    chem_comp_bond {
        text pdbid PK
        text ___ "7 more columns"
    }
    chem_link {
        text pdbid PK
        text ___ "1 more columns"
    }
    citation {
        text pdbid PK
        text ___ "25 more columns"
    }
    citation_author {
        text pdbid PK
        text ___ "4 more columns"
    }
    citation_editor {
        text pdbid PK
        text ___ "3 more columns"
    }
    citation_pdbmlplus {
        text pdbid PK
        text ___ "11 more columns"
    }
    database_2 {
        text pdbid PK
        text ___ "4 more columns"
    }
    database_PDB_caveat {
        text pdbid PK
        text ___ "2 more columns"
    }
    database_PDB_matrix {
        text pdbid PK
        text ___ "13 more columns"
    }
    database_PDB_tvect {
        text pdbid PK
        text ___ "4 more columns"
    }
    diffrn {
        text pdbid PK
        text ___ "10 more columns"
    }
    diffrn_detector {
        text pdbid PK
        text ___ "7 more columns"
    }
    diffrn_measurement {
        text pdbid PK
        text ___ "4 more columns"
    }
    diffrn_radiation {
        text pdbid PK
        text ___ "11 more columns"
    }
    diffrn_radiation_wavelength {
        text pdbid PK
        text ___ "3 more columns"
    }
    diffrn_reflns {
        text pdbid PK
        text ___ "21 more columns"
    }
    diffrn_source {
        text pdbid PK
        text ___ "14 more columns"
    }
    em_2d_crystal_entity {
        text pdbid PK
        text ___ "8 more columns"
    }
    em_3d_crystal_entity {
        text pdbid PK
        text ___ "10 more columns"
    }
    em_3d_fitting {
        text pdbid PK
        text ___ "8 more columns"
    }
    em_3d_fitting_list {
        text pdbid PK
        text ___ "12 more columns"
    }
    em_3d_reconstruction {
        text pdbid PK
        text ___ "15 more columns"
    }
    em_admin {
        text pdbid PK
        text ___ "7 more columns"
    }
    em_buffer {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_buffer_component {
        text pdbid PK
        text ___ "6 more columns"
    }
    em_crystal_formation {
        text pdbid PK
        text ___ "10 more columns"
    }
    em_ctf_correction {
        text pdbid PK
        text ___ "4 more columns"
    }
    em_diffraction {
        text pdbid PK
        text ___ "4 more columns"
    }
    em_diffraction_shell {
        text pdbid PK
        text ___ "8 more columns"
    }
    em_diffraction_stats {
        text pdbid PK
        text ___ "12 more columns"
    }
    em_embedding {
        text pdbid PK
        text ___ "4 more columns"
    }
    em_entity_assembly {
        text pdbid PK
        text ___ "9 more columns"
    }
    em_entity_assembly_molwt {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_entity_assembly_naturalsource {
        text pdbid PK
        text ___ "11 more columns"
    }
    em_entity_assembly_recombinant {
        text pdbid PK
        text ___ "7 more columns"
    }
    em_entity_assembly_synthetic {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_experiment {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_helical_entity {
        text pdbid PK
        text ___ "6 more columns"
    }
    em_image_processing {
        text pdbid PK
        text ___ "3 more columns"
    }
    em_image_recording {
        text pdbid PK
        text ___ "11 more columns"
    }
    em_image_scans {
        text pdbid PK
        text ___ "13 more columns"
    }
    em_imaging {
        text pdbid PK
        text ___ "31 more columns"
    }
    em_imaging_optics {
        text pdbid PK
        text ___ "10 more columns"
    }
    em_particle_selection {
        text pdbid PK
        text ___ "4 more columns"
    }
    em_sample_support {
        text pdbid PK
        text ___ "7 more columns"
    }
    em_single_particle_entity {
        text pdbid PK
        text ___ "4 more columns"
    }
    em_software {
        text pdbid PK
        text ___ "8 more columns"
    }
    em_specimen {
        text pdbid PK
        text ___ "8 more columns"
    }
    em_staining {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_virus_entity {
        text pdbid PK
        text ___ "8 more columns"
    }
    em_virus_natural_host {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_virus_shell {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_virus_synthetic {
        text pdbid PK
        text ___ "5 more columns"
    }
    em_vitrification {
        text pdbid PK
        text ___ "11 more columns"
    }
    em_volume_selection {
        text pdbid PK
        text ___ "7 more columns"
    }
    entity {
        text pdbid PK
        text ___ "10 more columns"
    }
    entity_keywords {
        text pdbid PK
        text ___ "2 more columns"
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
        text ___ "8 more columns"
    }
    entity_poly_seq {
        text pdbid PK
        text ___ "4 more columns"
    }
    entity_src_gen {
        text pdbid PK
        text ___ "48 more columns"
    }
    entity_src_nat {
        text pdbid PK
        text ___ "25 more columns"
    }
    entry {
        text pdbid PK
        text ___ "1 more columns"
    }
    exptl {
        text pdbid PK
        text ___ "9 more columns"
    }
    exptl_crystal {
        text pdbid PK
        text ___ "9 more columns"
    }
    exptl_crystal_grow {
        text pdbid PK
        text ___ "11 more columns"
    }
    exptl_crystal_grow_comp {
        text pdbid PK
        text ___ "7 more columns"
    }
    exptl_crystal_grow_comp_pdbmlplus {
        text pdbid PK
        text ___ "10 more columns"
    }
    exptl_crystal_grow_pdbmlplus {
        text pdbid PK
        text ___ "10 more columns"
    }
    gene_ontology_pdbmlplus {
        text pdbid PK
        text ___ "8 more columns"
    }
    link_asym_pdbjplus {
        text pdbid PK
        text ___ "3 more columns"
    }
    link_entity_pdbjplus {
        text pdbid PK
        text ___ "3 more columns"
    }
    link_entry_pdbjplus {
        text pdbid PK
        text ___ "2 more columns"
    }
    ndb_struct_conf_na {
        text pdbid PK
        text ___ "2 more columns"
    }
    ndb_struct_na_base_pair {
        text pdbid PK
        text ___ "25 more columns"
    }
    ndb_struct_na_base_pair_step {
        text pdbid PK
        text ___ "43 more columns"
    }
    pdbx_SG_project {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_audit_conform {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_audit_revision_category {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_audit_revision_details {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_audit_revision_group {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_audit_revision_history {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_audit_revision_item {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_audit_support {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_branch_scheme {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_buffer {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_buffer_components {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_chem_comp_identifier {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_contact_author {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_coordinate_model {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_database_PDB_obs_spr {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_database_related {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_database_remark {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_database_status {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_deposit_group {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_diffrn_reflns_shell {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_distant_solvent_atoms {
        text pdbid PK
        text ___ "9 more columns"
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
        text ___ "4 more columns"
    }
    pdbx_entity_instance_feature {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_entity_nonpoly {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_entity_src_syn {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_entry_details {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_exptl_crystal_cryo_treatment {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_exptl_crystal_grow_comp {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_exptl_crystal_grow_sol {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_helical_symmetry {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_initial_refinement_model {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_modification_feature {
        text pdbid PK
        text ___ "26 more columns"
    }
    pdbx_molecule {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_molecule_features {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_nmr_constraints {
        text pdbid PK
        text ___ "21 more columns"
    }
    pdbx_nmr_details {
        text pdbid PK
        text ___ "2 more columns"
    }
    pdbx_nmr_ensemble {
        text pdbid PK
        text ___ "15 more columns"
    }
    pdbx_nmr_ensemble_rms {
        text pdbid PK
        text ___ "14 more columns"
    }
    pdbx_nmr_exptl {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_nmr_exptl_sample {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_nmr_exptl_sample_conditions {
        text pdbid PK
        text ___ "15 more columns"
    }
    pdbx_nmr_refine {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_nmr_representative {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_nmr_sample_details {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_nmr_software {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_nmr_spectrometer {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_nonpoly_scheme {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_phasing_MAD_set {
        text pdbid PK
        text ___ "21 more columns"
    }
    pdbx_phasing_MAD_set_shell {
        text pdbid PK
        text ___ "21 more columns"
    }
    pdbx_phasing_MAD_set_site {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_phasing_MAD_shell {
        text pdbid PK
        text ___ "8 more columns"
    }
    pdbx_phasing_MR {
        text pdbid PK
        text ___ "17 more columns"
    }
    pdbx_phasing_dm {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_phasing_dm_shell {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_point_symmetry {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_poly_seq_scheme {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_refine {
        text pdbid PK
        text ___ "15 more columns"
    }
    pdbx_refine_tls {
        text pdbid PK
        text ___ "49 more columns"
    }
    pdbx_refine_tls_group {
        text pdbid PK
        text ___ "15 more columns"
    }
    pdbx_reflns_twin {
        text pdbid PK
        text ___ "6 more columns"
    }
    pdbx_related_exp_data_set {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_serial_crystallography_data_reduction {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_serial_crystallography_measurement {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_serial_crystallography_sample_delivery {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_serial_crystallography_sample_delivery_fixed_target {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_serial_crystallography_sample_delivery_injection {
        text pdbid PK
        text ___ "12 more columns"
    }
    pdbx_sifts_unp_segments {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_sifts_xref_db {
        text pdbid PK
        text ___ "19 more columns"
    }
    pdbx_sifts_xref_db_segments {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_soln_scatter {
        text pdbid PK
        text ___ "23 more columns"
    }
    pdbx_soln_scatter_model {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_struct_assembly {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_struct_assembly_auth_evidence {
        text pdbid PK
        text ___ "4 more columns"
    }
    pdbx_struct_assembly_gen {
        text pdbid PK
        text ___ "5 more columns"
    }
    pdbx_struct_assembly_prop {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_struct_chem_comp_diagnostics {
        text pdbid PK
        text ___ "7 more columns"
    }
    pdbx_struct_conn_angle {
        text pdbid PK
        text ___ "32 more columns"
    }
    pdbx_struct_entity_inst {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_struct_legacy_oper_list {
        text pdbid PK
        text ___ "14 more columns"
    }
    pdbx_struct_mod_residue {
        text pdbid PK
        text ___ "10 more columns"
    }
    pdbx_struct_msym_gen {
        text pdbid PK
        text ___ "3 more columns"
    }
    pdbx_struct_oper_list {
        text pdbid PK
        text ___ "16 more columns"
    }
    pdbx_struct_sheet_hbond {
        text pdbid PK
        text ___ "21 more columns"
    }
    pdbx_struct_special_symmetry {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_unobs_or_zero_occ_atoms {
        text pdbid PK
        text ___ "14 more columns"
    }
    pdbx_unobs_or_zero_occ_residues {
        text pdbid PK
        text ___ "11 more columns"
    }
    pdbx_validate_chiral {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_validate_close_contact {
        text pdbid PK
        text ___ "15 more columns"
    }
    pdbx_validate_main_chain_plane {
        text pdbid PK
        text ___ "8 more columns"
    }
    pdbx_validate_peptide_omega {
        text pdbid PK
        text ___ "13 more columns"
    }
    pdbx_validate_planes {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_validate_polymer_linkage {
        text pdbid PK
        text ___ "15 more columns"
    }
    pdbx_validate_rmsd_angle {
        text pdbid PK
        text ___ "25 more columns"
    }
    pdbx_validate_rmsd_bond {
        text pdbid PK
        text ___ "19 more columns"
    }
    pdbx_validate_symm_contact {
        text pdbid PK
        text ___ "17 more columns"
    }
    pdbx_validate_torsion {
        text pdbid PK
        text ___ "9 more columns"
    }
    pdbx_xplor_file {
        text pdbid PK
        text ___ "4 more columns"
    }
    phasing {
        text pdbid PK
        text ___ "1 more columns"
    }
    phasing_MAD {
        text pdbid PK
        text ___ "9 more columns"
    }
    phasing_MAD_clust {
        text pdbid PK
        text ___ "2 more columns"
    }
    phasing_MAD_expt {
        text pdbid PK
        text ___ "2 more columns"
    }
    phasing_MAD_set {
        text pdbid PK
        text ___ "11 more columns"
    }
    phasing_MIR {
        text pdbid PK
        text ___ "11 more columns"
    }
    phasing_MIR_der {
        text pdbid PK
        text ___ "17 more columns"
    }
    phasing_MIR_der_shell {
        text pdbid PK
        text ___ "11 more columns"
    }
    phasing_MIR_der_site {
        text pdbid PK
        text ___ "15 more columns"
    }
    phasing_MIR_shell {
        text pdbid PK
        text ___ "8 more columns"
    }
    phasing_set {
        text pdbid PK
        text ___ "9 more columns"
    }
    publ {
        text pdbid PK
        text ___ "2 more columns"
    }
    refine {
        text pdbid PK
        text ___ "82 more columns"
    }
    refine_B_iso {
        text pdbid PK
        text ___ "4 more columns"
    }
    refine_analyze {
        text pdbid PK
        text ___ "12 more columns"
    }
    refine_funct_minimized {
        text pdbid PK
        text ___ "2 more columns"
    }
    refine_hist {
        text pdbid PK
        text ___ "13 more columns"
    }
    refine_ls_restr {
        text pdbid PK
        text ___ "7 more columns"
    }
    refine_ls_restr_ncs {
        text pdbid PK
        text ___ "15 more columns"
    }
    refine_ls_restr_pdbmlplus {
        text pdbid PK
        text ___ "7 more columns"
    }
    refine_ls_shell {
        text pdbid PK
        text ___ "24 more columns"
    }
    refine_occupancy {
        text pdbid PK
        text ___ "3 more columns"
    }
    refine_pdbmlplus {
        text pdbid PK
        text ___ "17 more columns"
    }
    refln_sys_abs {
        text pdbid PK
        text ___ "6 more columns"
    }
    reflns {
        text pdbid PK
        text ___ "78 more columns"
    }
    reflns_pdbmlplus {
        text pdbid PK
        text ___ "15 more columns"
    }
    reflns_scale {
        text pdbid PK
        text ___ "1 more columns"
    }
    reflns_shell {
        text pdbid PK
        text ___ "38 more columns"
    }
    software {
        text pdbid PK
        text ___ "14 more columns"
    }
    space_group {
        text pdbid PK
        text ___ "5 more columns"
    }
    space_group_symop {
        text pdbid PK
        text ___ "2 more columns"
    }
    struct {
        text pdbid PK
        text ___ "5 more columns"
    }
    struct_asym {
        text pdbid PK
        text ___ "5 more columns"
    }
    struct_biol {
        text pdbid PK
        text ___ "6 more columns"
    }
    struct_biol_keywords {
        text pdbid PK
        text ___ "2 more columns"
    }
    struct_conf {
        text pdbid PK
        text ___ "20 more columns"
    }
    struct_conf_type {
        text pdbid PK
        text ___ "1 more columns"
    }
    struct_conn {
        text pdbid PK
        text ___ "27 more columns"
    }
    struct_conn_type {
        text pdbid PK
        text ___ "1 more columns"
    }
    struct_keywords {
        text pdbid PK
        text ___ "3 more columns"
    }
    struct_mon_prot_cis {
        text pdbid PK
        text ___ "17 more columns"
    }
    struct_ncs_dom {
        text pdbid PK
        text ___ "3 more columns"
    }
    struct_ncs_dom_lim {
        text pdbid PK
        text ___ "19 more columns"
    }
    struct_ncs_ens {
        text pdbid PK
        text ___ "2 more columns"
    }
    struct_ncs_ens_gen {
        text pdbid PK
        text ___ "4 more columns"
    }
    struct_ncs_oper {
        text pdbid PK
        text ___ "15 more columns"
    }
    struct_ref {
        text pdbid PK
        text ___ "8 more columns"
    }
    struct_ref_pdbmlplus {
        text pdbid PK
        text ___ "8 more columns"
    }
    struct_ref_seq {
        text pdbid PK
        text ___ "15 more columns"
    }
    struct_ref_seq_dif {
        text pdbid PK
        text ___ "13 more columns"
    }
    struct_ref_seq_pdbmlplus {
        text pdbid PK
        text ___ "12 more columns"
    }
    struct_sheet {
        text pdbid PK
        text ___ "2 more columns"
    }
    struct_sheet_order {
        text pdbid PK
        text ___ "4 more columns"
    }
    struct_sheet_range {
        text pdbid PK
        text ___ "16 more columns"
    }
    struct_site {
        text pdbid PK
        text ___ "8 more columns"
    }
    struct_site_gen {
        text pdbid PK
        text ___ "11 more columns"
    }
    struct_site_gen_pdbmlplus {
        text pdbid PK
        text ___ "16 more columns"
    }
    struct_site_keywords {
        text pdbid PK
        text ___ "2 more columns"
    }
    struct_site_pdbmlplus {
        text pdbid PK
        text ___ "10 more columns"
    }
    symmetry {
        text pdbid PK
        text ___ "6 more columns"
    }
    symmetry_equiv {
        text pdbid PK
        text ___ "2 more columns"
    }
```
