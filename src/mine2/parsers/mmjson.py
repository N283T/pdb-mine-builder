"""mmJSON utilities for PDBj data files.

Note: Parsing is now handled by parsers/cif.py using gemmi.
This module provides utility functions for column name normalization, data merging,
and querying mmJSON data structures.

Ported from original mine2updater rdb-helper.js.
"""

import re
from typing import Any, TypeVar

T = TypeVar("T")


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


# =============================================================================
# Query Functions
# Ported from original mine2updater rdb-helper.js
# =============================================================================


def mmjson_at(
    rows: list[dict[str, Any]],
    get_field: str,
    cond_field: str,
    cond_val: Any,
) -> list[Any]:
    """Get values from rows where a condition field matches a value.

    Filters rows where cond_field == cond_val and returns the get_field values.

    Args:
        rows: List of row dicts (from a category)
        get_field: Field name to retrieve values from
        cond_field: Field name to check condition against
        cond_val: Value to match in cond_field

    Returns:
        List of get_field values from matching rows

    Example:
        >>> rows = [{"type": "SMILES", "value": "CCO"}, {"type": "InChI", "value": "..."}]
        >>> mmjson_at(rows, "value", "type", "SMILES")
        ["CCO"]
    """
    if not rows:
        return []
    result = []
    for row in rows:
        if row.get(cond_field) == cond_val and get_field in row:
            result.append(row[get_field])
    return result


def mmjson_at_ic(
    rows: list[dict[str, Any]],
    get_field: str,
    cond_field: str,
    cond_val: str,
) -> list[Any]:
    """Case-insensitive version of mmjson_at.

    Args:
        rows: List of row dicts (from a category)
        get_field: Field name to retrieve values from
        cond_field: Field name to check condition against
        cond_val: Value to match (case-insensitive)

    Returns:
        List of get_field values from matching rows
    """
    if not rows:
        return []
    cond_val_lower = cond_val.lower()
    result = []
    for row in rows:
        field_val = row.get(cond_field)
        if field_val is not None and str(field_val).lower() == cond_val_lower:
            if get_field in row:
                result.append(row[get_field])
    return result


def mmjson_get(
    rows: list[dict[str, Any]],
    field: str,
    index: int | None = None,
) -> Any:
    """Safely get field values from rows.

    Args:
        rows: List of row dicts (from a category)
        field: Field name to retrieve
        index: Optional row index. If None, returns all values.

    Returns:
        - If index is specified: value at that row, or None if not found
        - If index is None: list of all values for that field
    """
    if not rows:
        return None if index is not None else []

    if index is not None:
        if 0 <= index < len(rows):
            return rows[index].get(field)
        return None

    return [row.get(field) for row in rows]


def get_object_value(obj: dict[str, Any], field: str, default: T) -> Any | T:
    """Safely get a value from a dict with a default.

    Args:
        obj: Dictionary to get value from
        field: Key to look up
        default: Default value if key not found

    Returns:
        Value if found, otherwise default
    """
    return obj.get(field, default)


# =============================================================================
# Array Utility Functions
# =============================================================================


def clean_array(array: list[Any]) -> list[Any]:
    """Remove nulls, empty strings, duplicates, and sort the array.

    Matches original mine2updater cleanArray():
    - Remove None/null values
    - Remove empty strings
    - Remove duplicates (preserving first occurrence)
    - Sort the result

    Args:
        array: Input list

    Returns:
        Cleaned and sorted list

    Example:
        >>> clean_array(["b", None, "a", "b", "", "c"])
        ["a", "b", "c"]
    """
    # Remove None, empty strings, and deduplicate using dict (preserves order in Python 3.7+)
    seen: dict[Any, None] = {}
    for item in array:
        if item is not None and item != "":
            seen[item] = None

    # Sort - handle mixed types by converting to string for comparison
    result = list(seen.keys())
    try:
        result.sort()
    except TypeError:
        # Mixed types that can't be compared - sort by string representation
        result.sort(key=str)

    return result


def remove_null(array: list[Any]) -> list[Any]:
    """Remove null/None values from an array.

    Args:
        array: Input list

    Returns:
        List with None values removed

    Example:
        >>> remove_null(["a", None, "b", None])
        ["a", "b"]
    """
    return [v for v in array if v is not None]
