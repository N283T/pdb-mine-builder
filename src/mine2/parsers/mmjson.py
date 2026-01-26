"""mmJSON utilities for PDBj data files.

Note: Parsing is now handled by parsers/cif.py using gemmi.
This module provides utility functions for column name normalization and data merging.
"""

import re
from typing import Any


def normalize_column_name(name: str) -> str:
    """Normalize mmJSON column names to schema column names.

    Converts bracket notation to concatenated digits.

    Examples:
        fract_transf_matrix[1][1] -> fract_transf_matrix11
        column[0] -> column0
    """
    return re.sub(r"\[(\d+)\]", r"\1", name)


def merge_data(base: dict[str, Any], plus: dict[str, Any]) -> dict[str, Any]:
    """Merge two row-oriented data dicts (base + plus data).

    The 'plus' data is typically additional annotations from PDBj.
    Plus data takes precedence for overlapping categories/columns.

    For each category:
    - If only in base: keep as-is
    - If only in plus: add to result
    - If in both: merge rows by index (plus columns take precedence)

    Note:
        If a category exists in both base and plus with different row counts,
        the result will have max(base_rows, plus_rows) rows. Missing rows
        are treated as empty dicts (no columns added from the shorter side).

    Args:
        base: Base row-oriented data
        plus: Additional row-oriented data to merge

    Returns:
        Merged row-oriented data
    """
    result: dict[str, Any] = {}

    # Get all categories from both
    all_categories = set(base.keys()) | set(plus.keys())

    for category in all_categories:
        if category.startswith("_"):
            # Metadata like _block_name - plus takes precedence
            result[category] = plus.get(category, base.get(category))
            continue

        base_rows = base.get(category, [])
        plus_rows = plus.get(category, [])

        if not base_rows:
            result[category] = plus_rows
        elif not plus_rows:
            result[category] = base_rows
        else:
            # Merge rows by index
            merged_rows = []
            max_len = max(len(base_rows), len(plus_rows))
            for i in range(max_len):
                base_row = base_rows[i] if i < len(base_rows) else {}
                plus_row = plus_rows[i] if i < len(plus_rows) else {}
                # Plus takes precedence
                merged_rows.append({**base_row, **plus_row})
            result[category] = merged_rows

    return result
