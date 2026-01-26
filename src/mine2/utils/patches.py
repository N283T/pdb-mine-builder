"""Entry-specific data patches.

Some PDB entries have data issues that need to be corrected during loading.
This module provides patch functions for specific entries.
"""

from typing import Any


def apply_patches(entry_id: str, data: dict[str, Any]) -> dict[str, Any]:
    """Apply entry-specific patches to data.

    Args:
        entry_id: PDB entry ID (lowercase, e.g., "7ed1")
        data: Parsed mmJSON/CIF data to patch

    Returns:
        Patched data (modified in place)
    """
    # 7ed1: Missing MET record in chem_comp
    if entry_id == "7ed1":
        _patch_7ed1_met(data)

    return data


def _patch_7ed1_met(data: dict[str, Any]) -> None:
    """Add missing MET record to 7ed1 entry.

    Entry 7ed1 is missing the MET (methionine) chemical component
    record that is referenced in the structure.
    """
    chem_comp = data.get("chem_comp", [])

    # Check if MET already exists
    for row in chem_comp:
        if row.get("id") == "MET":
            return  # Already has MET, no patch needed

    # Add MET record
    met_record = {
        "id": "MET",
        "type": "L-peptide linking",
        "mon_nstd_flag": "y",
        "name": "METHIONINE",
        "formula": "C5 H11 N O2 S",
        "formula_weight": 149.211,
    }

    if not chem_comp:
        data["chem_comp"] = [met_record]
    else:
        chem_comp.append(met_record)
