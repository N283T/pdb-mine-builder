"""Helper functions for generating brief_summary from other categories."""

import json
from typing import Any

from mine2.utils.assembly import CHAIN_TYPE_MAPPING, EXPTL_METHOD_MAPPING

# Linking types to exclude from ligand list
LINKING_TYPES = {
    "peptide linking",
    "L-peptide linking",
    "D-peptide linking",
    "DNA linking",
    "RNA linking",
}


def gen_docid(pdbid: str) -> int:
    """Generate docid from PDB ID using base-37 encoding.

    This algorithm encodes an 8-character PDB ID into a 64-bit integer.
    Each character is converted to a value 0-36 (0-9, a-z, space) and
    packed into 8 bytes using bit-shifting.

    The encoding follows PDBj convention:
    - Short PDB IDs (e.g., "1abc") are left-padded with spaces to 4 chars
    - Then right-padded with zeros to 8 chars (for extended PDB IDs)
    - Example: "1abc" -> "1abc    " (ljust 4) -> "00001abc" (rjust 8)

    Args:
        pdbid: PDB entry ID (e.g., "100d", "1abc", "pdb_00001abc")

    Returns:
        Integer docid (fits in PostgreSQL bigint: max 2^63-1)

    Raises:
        ValueError: If resulting docid exceeds bigint range
    """
    # Pad to 8 characters: left-pad with spaces to 4, then right-pad with 0s to 8
    inp = pdbid.ljust(4, " ").rjust(8, "0")

    components = []
    for char in inp:
        if char == " ":
            components.append(36)  # space is type 36
        else:
            # Parse as base-36 (0-9, a-z -> 0-35)
            components.append(int(char, 36))

    # Combine into a single integer (bitwise operations)
    docid = (
        (components[0] << 56)
        | (components[1] << 48)
        | (components[2] << 40)
        | (components[3] << 32)
        | (components[4] << 24)
        | (components[5] << 16)
        | (components[6] << 8)
        | components[7]
    )

    # Validate fits in PostgreSQL bigint (signed 64-bit)
    max_bigint = 2**63 - 1
    if docid > max_bigint:
        raise ValueError(f"docid {docid} exceeds bigint max for pdbid '{pdbid}'")

    return docid


def get_first_value(rows: list[dict], field: str) -> Any:
    """Get first non-null value from a category's rows."""
    if not rows:
        return None
    for row in rows:
        val = row.get(field)
        if val is not None:
            return val
    return None


def get_all_values(rows: list[dict], field: str) -> list[Any]:
    """Get all non-null values from a category's rows."""
    if not rows:
        return []
    return [row.get(field) for row in rows if row.get(field) is not None]


def get_values_where(
    rows: list[dict], get_field: str, cond_field: str, cond_val: Any
) -> list[Any]:
    """Get values where a condition is met (like mmjsonAt in original)."""
    if not rows:
        return []
    return [
        row.get(get_field)
        for row in rows
        if row.get(cond_field) == cond_val and row.get(get_field) is not None
    ]


def clean_array(arr: list[Any]) -> list[Any]:
    """Remove None and empty values from array, return unique values."""
    seen = set()
    result = []
    for item in arr:
        if item is not None and item != "" and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def generate_brief_summary(
    data: dict[str, Any],
    entry_id: str,
    bu_mw: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Generate brief_summary row from other categories.

    Args:
        data: Parsed data dictionary with categories as keys
        entry_id: PDB entry ID
        bu_mw: Pre-calculated biological unit molecular weights (optional)

    Returns:
        Dictionary with brief_summary fields
    """
    result: dict[str, Any] = {}

    # Primary key
    result["pdbid"] = entry_id

    # Document ID
    result["docid"] = gen_docid(entry_id)

    # Dates from pdbx_database_status and pdbx_audit_revision_history
    db_status = data.get("pdbx_database_status", [])
    result["deposition_date"] = get_first_value(
        db_status, "recvd_initial_deposition_date"
    )

    revision_history = data.get("pdbx_audit_revision_history", [])
    revision_dates = get_all_values(revision_history, "revision_date")
    result["release_date"] = revision_dates[0] if revision_dates else None
    result["modification_date"] = revision_dates[-1] if revision_dates else None

    # Authors
    audit_author = data.get("audit_author", [])
    result["deposit_author"] = get_all_values(audit_author, "name") or None

    citation_author = data.get("citation_author", [])
    result["citation_author"] = get_all_values(citation_author, "name") or None
    result["citation_author_pri"] = (
        get_values_where(citation_author, "name", "citation_id", "primary") or None
    )

    # Citation info
    citation = data.get("citation", [])
    if citation:
        result["citation_title"] = get_all_values(citation, "title") or None
        result["citation_journal"] = get_all_values(citation, "journal_abbrev") or None
        # citation_year is integer[] - convert to int
        years = get_all_values(citation, "year")
        result["citation_year"] = [int(y) for y in years if y is not None] or None
        result["citation_volume"] = get_all_values(citation, "journal_volume") or None

        result["citation_title_pri"] = get_first_value(
            [r for r in citation if r.get("id") == "primary"], "title"
        )
        result["citation_journal_pri"] = get_first_value(
            [r for r in citation if r.get("id") == "primary"], "journal_abbrev"
        )
        # citation_year_pri is integer - convert to int
        year_pri = get_first_value(
            [r for r in citation if r.get("id") == "primary"], "year"
        )
        result["citation_year_pri"] = int(year_pri) if year_pri is not None else None
        result["citation_volume_pri"] = get_first_value(
            [r for r in citation if r.get("id") == "primary"], "journal_volume"
        )

        result["db_pubmed"] = [
            str(v)
            for v in get_all_values(citation, "pdbx_database_id_PubMed")
            if v is not None
        ] or None
        result["db_doi"] = get_all_values(citation, "pdbx_database_id_DOI") or None
    else:
        result["citation_title"] = None
        result["citation_journal"] = None
        result["citation_year"] = None
        result["citation_volume"] = None
        result["citation_title_pri"] = None
        result["citation_journal_pri"] = None
        result["citation_year_pri"] = None
        result["citation_volume_pri"] = None
        result["db_pubmed"] = None
        result["db_doi"] = None

    # Chain info from entity_poly
    entity_poly = data.get("entity_poly", [])
    chain_types = clean_array(get_all_values(entity_poly, "type"))
    result["chain_type"] = chain_types or None
    result["chain_type_ids"] = (
        clean_array([CHAIN_TYPE_MAPPING.get(t) for t in chain_types]) or None
    )

    # Chain number from entity
    entity = data.get("entity", [])
    polymer_entities = [e for e in entity if e.get("type") == "polymer"]
    chain_number = sum(
        int(e.get("pdbx_number_of_molecules", 0) or 0) for e in polymer_entities
    )
    result["chain_number"] = chain_number if chain_number > 0 else None

    # Chain length from sequences
    sequences = get_all_values(entity_poly, "pdbx_seq_one_letter_code_can")
    result["chain_length"] = [len(s.replace("\n", "")) for s in sequences if s] or None

    # Descriptor from entity
    descriptors = clean_array(get_all_values(entity, "pdbx_description"))
    result["pdbx_descriptor"] = ", ".join(descriptors) if descriptors else None

    # Structure title
    struct = data.get("struct", [])
    result["struct_title"] = get_first_value(struct, "title")

    # Ligands (excluding linking types)
    chem_comp = data.get("chem_comp", [])
    ligands = []
    for comp in chem_comp:
        comp_type = comp.get("type", "")
        if comp_type not in LINKING_TYPES:
            if comp.get("name"):
                ligands.append(comp["name"])
            if comp.get("pdbx_synonyms"):
                ligands.append(comp["pdbx_synonyms"])
            if comp.get("id"):
                ligands.append(comp["id"])
    result["ligand"] = clean_array(ligands) or None

    # Experimental methods
    exptl = data.get("exptl", [])
    methods = clean_array(get_all_values(exptl, "method"))
    if len(methods) > 1:
        methods.append("HYBRID")
    result["exptl_method"] = methods or None
    result["exptl_method_ids"] = (
        clean_array([EXPTL_METHOD_MAPPING.get(m) for m in methods]) or None
    )

    # Resolution (double precision)
    refine = data.get("refine", [])
    em_3d = data.get("em_3d_reconstruction", [])
    resolution = get_first_value(refine, "ls_d_res_high")
    if resolution is None:
        resolution = get_first_value(em_3d, "resolution")
    # Convert to float if present
    result["resolution"] = float(resolution) if resolution is not None else None

    # Species info
    entity_src_gen = data.get("entity_src_gen", [])
    entity_src_nat = data.get("entity_src_nat", [])
    pdbx_entity_src_syn = data.get("pdbx_entity_src_syn", [])

    biol_species_parts = clean_array(
        get_all_values(entity_src_gen, "pdbx_gene_src_scientific_name")
        + get_all_values(entity_src_gen, "gene_src_common_name")
        + get_all_values(entity_src_nat, "common_name")
        + get_all_values(entity_src_nat, "pdbx_organism_scientific")
        + get_all_values(pdbx_entity_src_syn, "organism_common_name")
        + get_all_values(pdbx_entity_src_syn, "organism_scientific")
    )
    result["biol_species"] = (
        " ".join(biol_species_parts) if biol_species_parts else None
    )

    result["host_species"] = get_first_value(
        entity_src_gen, "pdbx_host_org_scientific_name"
    )

    # Database cross-references
    result["db_ec_number"] = clean_array(get_all_values(entity, "pdbx_ec")) or None

    # GO IDs from plus data
    gene_ontology = data.get("gene_ontology_pdbmlplus", [])
    result["db_goid"] = clean_array(get_all_values(gene_ontology, "goid")) or None

    # External database references
    struct_ref = data.get("struct_ref", [])
    struct_ref_plus = data.get("struct_ref_pdbmlplus", [])

    result["db_uniprot"] = (
        clean_array(
            get_values_where(struct_ref, "pdbx_db_accession", "db_name", "UNP")
            + get_values_where(struct_ref, "db_code", "db_name", "UNP")
            + get_values_where(
                struct_ref_plus, "pdbx_db_accession", "db_name", "SIFTS_UNP"
            )
        )
        or None
    )

    result["db_genbank"] = (
        clean_array(
            get_values_where(struct_ref, "db_code", "db_name", "GB")
            + get_values_where(struct_ref, "pdbx_db_accession", "db_name", "GB")
        )
        or None
    )

    result["db_embl"] = (
        clean_array(
            get_values_where(struct_ref, "db_code", "db_name", "EMBL")
            + get_values_where(struct_ref, "pdbx_db_accession", "db_name", "EMBL")
        )
        or None
    )

    result["db_pir"] = (
        clean_array(
            get_values_where(struct_ref, "db_code", "db_name", "PIR")
            + get_values_where(struct_ref, "pdbx_db_accession", "db_name", "PIR")
        )
        or None
    )

    # Related databases
    pdbx_database_related = data.get("pdbx_database_related", [])
    result["db_emdb"] = (
        clean_array(get_values_where(pdbx_database_related, "db_id", "db_name", "EMDB"))
        or None
    )
    result["pdb_related"] = (
        clean_array(get_values_where(pdbx_database_related, "db_id", "db_name", "PDB"))
        or None
    )

    # Amino acid sequence
    result["aaseq"] = "".join(sequences) if sequences else None

    # Update date (will be set later by the pipeline)
    result["update_date"] = None

    # Pfam from plus data
    result["db_pfam"] = (
        clean_array(
            get_values_where(struct_ref_plus, "pdbx_db_accession", "db_name", "Pfam")
        )
        or None
    )

    # Group ID
    pdbx_deposit_group = data.get("pdbx_deposit_group", [])
    result["group_id"] = get_first_value(pdbx_deposit_group, "group_id")

    # Keywords
    result["keywords"] = [f"pdb_{entry_id.rjust(8, '0')}"]

    # Plus fields (bu_mw)
    plus_fields = {}
    if bu_mw is not None:
        plus_fields["bu_mw"] = bu_mw
    result["plus_fields"] = json.dumps(plus_fields) if plus_fields else None

    return result
