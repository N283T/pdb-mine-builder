"""Assembly and molecular weight utilities.

Functions for calculating biological assembly properties and SHA256 hashing.
Used by pdbj, ihm, and other pipelines that need assembly data processing.
"""

import hashlib
from typing import Any


# Chain type mapping (entity_poly.type -> numeric ID)
CHAIN_TYPE_MAPPING = {
    "polypeptide(D)": 1,
    "polypeptide(L)": 2,
    "polydeoxyribonucleotide": 3,
    "polyribonucleotide": 4,
    "polysaccharide(D)": 5,
    "polysaccharide(L)": 6,
    "polydeoxyribonucleotide/polyribonucleotide hybrid": 7,
    "cyclic-pseudo-peptide": 8,
    "other": 9,
    "peptide nucleic acid": 10,
}

# Experimental method mapping
EXPTL_METHOD_MAPPING = {
    "X-RAY DIFFRACTION": 1,
    "NEUTRON DIFFRACTION": 2,
    "FIBER DIFFRACTION": 3,
    "ELECTRON CRYSTALLOGRAPHY": 4,
    "ELECTRON MICROSCOPY": 5,
    "SOLUTION NMR": 6,
    "SOLID-STATE NMR": 7,
    "SOLUTION SCATTERING": 8,
    "POWDER DIFFRACTION": 9,
    "INFRARED SPECTROSCOPY": 10,
    "EPR": 11,
    "FLUORESCENCE TRANSFER": 12,
    "THEORETICAL MODEL": 13,
    "HYBRID": 14,
    "THEORETICAL MODEL (obsolete)": 15,
    "IHM": 16,
}


def hex_sha256(text: str) -> str:
    """Compute SHA256 hex digest of text.

    Args:
        text: Input string to hash

    Returns:
        64-character hexadecimal SHA256 digest
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def expand_oper_expression(expr: str) -> list[str]:
    """Expand operator expression like '1-3' or '(1,2)(3,4)' to list of operations.

    Args:
        expr: Operator expression string (e.g., "1", "1-3", "(1,2)(3,4)")

    Returns:
        List of individual operation identifiers

    Examples:
        >>> expand_oper_expression("1")
        ['1']
        >>> expand_oper_expression("1-3")
        ['1', '2', '3']
        >>> expand_oper_expression("(1,2)(3,4)")
        ['1-3', '1-4', '2-3', '2-4']
    """
    if not expr:
        return []

    def expand_range(s: str) -> list[str]:
        """Expand a single range like '1-3' or '1,2,3'."""
        result: list[str] = []
        s = s.replace("(", "").replace(")", "")
        for part in s.split(","):
            if "-" in part:
                try:
                    start, end = part.split("-")
                    for i in range(int(start), int(end) + 1):
                        result.append(str(i))
                except ValueError:
                    result.append(part)
            else:
                result.append(part.strip())
        return result

    # Handle product notation like "(1,2)(3,4)"
    if ")(" in expr:
        parts = expr.split(")(")
        left = expand_range(parts[0][1:] if parts[0].startswith("(") else parts[0])
        right = expand_range(parts[1][:-1] if parts[1].endswith(")") else parts[1])
        return [f"{left_op}-{right_op}" for left_op in left for right_op in right]

    return expand_range(expr)


def calculate_mw_for_bu(mmjson: dict[str, Any]) -> float:
    """Calculate molecular weight for biological unit.

    Follows the original JavaScript implementation to find the preferred
    biological assembly and calculate its total molecular weight.

    Args:
        mmjson: Parsed mmJSON data with assembly categories

    Returns:
        Total molecular weight in Da, or 0.0 if no assembly found
    """
    # Build assembly info from pdbx_struct_assembly_gen
    bu_assemblies: dict[str, list[tuple[list[str], list[str]]]] = {}

    pdbx_struct_assembly_gen = mmjson.get("pdbx_struct_assembly_gen", [])
    for row in pdbx_struct_assembly_gen:
        assembly_id = row.get("assembly_id")
        if not assembly_id:
            continue

        if assembly_id not in bu_assemblies:
            bu_assemblies[assembly_id] = []

        # Parse operator expression
        oper_expr = row.get("oper_expression", "")
        mats = expand_oper_expression(oper_expr)

        # Parse asym_id_list
        asym_id_list = row.get("asym_id_list", "")
        asym_ids = asym_id_list.split(",") if asym_id_list else []

        bu_assemblies[assembly_id].append((mats, asym_ids))

    # Find preferred assembly_id
    assembly_id = _find_preferred_assembly_id(mmjson, bu_assemblies)

    if assembly_id is None:
        return 0.0

    # Build asym -> molecular weight mapping
    asym_to_mw: dict[str, float] = {}
    entity = mmjson.get("entity", [])
    entity_mw = {row.get("id"): row.get("formula_weight", 0) for row in entity}

    struct_asym = mmjson.get("struct_asym", [])
    for row in struct_asym:
        asym_id = row.get("id")
        entity_id = row.get("entity_id")
        if asym_id and entity_id:
            mw = entity_mw.get(entity_id, 0)
            asym_to_mw[asym_id] = float(mw) if mw else 0.0

    # Calculate total MW for assembly
    total_mw = 0.0
    if assembly_id in bu_assemblies:
        for mats, asym_ids in bu_assemblies[assembly_id]:
            asym_mw = sum(asym_to_mw.get(a, 0) for a in asym_ids)
            total_mw += asym_mw * len(mats)

    return total_mw


def _find_preferred_assembly_id(
    mmjson: dict[str, Any],
    bu_assemblies: dict[str, list[tuple[list[str], list[str]]]],
) -> str | None:
    """Find preferred assembly ID based on priority.

    Priority order:
    1. author_and_software
    2. author
    3. software
    4. largest by sequence length
    """
    pdbx_struct_assembly = mmjson.get("pdbx_struct_assembly", [])

    # Try author_and_software first
    for row in pdbx_struct_assembly:
        details = row.get("details", "")
        if details and details.startswith("author_and_software"):
            return row.get("id")

    # Try author
    for row in pdbx_struct_assembly:
        details = row.get("details", "")
        if details and details.startswith("author"):
            return row.get("id")

    # Try software
    for row in pdbx_struct_assembly:
        details = row.get("details", "")
        if details and details.startswith("software"):
            return row.get("id")

    # If still no assembly_id, find largest by sequence length
    sinfo: dict[str, int] = {}
    entity_poly = mmjson.get("entity_poly", [])
    for row in entity_poly:
        entity_id = row.get("entity_id")
        seq = row.get("pdbx_seq_one_letter_code_can", "")
        if entity_id and seq:
            sinfo[entity_id] = len(seq.replace("\n", "").replace(" ", ""))

    nor_info: dict[str, int] = {}
    struct_asym = mmjson.get("struct_asym", [])
    for row in struct_asym:
        asym_id = row.get("id")
        entity_id = row.get("entity_id")
        if asym_id:
            nor_info[asym_id] = sinfo.get(entity_id, 0)

    # Find largest assembly
    largest: tuple[str | None, int] = (None, 0)
    for aid, assembly_data in bu_assemblies.items():
        try:
            int(aid)
        except ValueError:
            continue  # Skip non-numeric assembly IDs

        size = 0
        for mats, asym_ids in assembly_data:
            nor = sum(nor_info.get(a, 0) for a in asym_ids)
            size += len(mats) * nor

        if size > largest[1]:
            largest = (aid, size)

    return largest[0]
