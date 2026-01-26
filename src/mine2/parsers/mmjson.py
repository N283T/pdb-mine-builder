"""mmJSON parser for PDBj data files."""

import gzip
import json
import re
from pathlib import Path
from typing import Any


def normalize_column_name(name: str) -> str:
    """Normalize mmJSON column names to schema column names.

    Converts bracket notation to concatenated digits.

    Examples:
        fract_transf_matrix[1][1] -> fract_transf_matrix11
        column[0] -> column0
    """
    return re.sub(r"\[(\d+)\]", r"\1", name)


def load_mmjson(content: str) -> dict[str, Any]:
    """Parse mmJSON content string.

    mmJSON format:
    {
        "category_name": {
            "column1": ["value1", "value2", ...],
            "column2": ["value1", "value2", ...]
        }
    }

    Each category contains columns as arrays of equal length,
    representing rows of data.
    """
    return json.loads(content)


def load_mmjson_file(filepath: Path) -> dict[str, Any]:
    """Load mmJSON file (supports gzip compression).

    mmJSON files from PDBj have structure:
    {
        "data_<ENTRY_ID>": {
            "category": {...},
            ...
        }
    }

    This function extracts the inner data block automatically.

    Args:
        filepath: Path to the mmJSON file (.json or .json.gz)

    Returns:
        Parsed mmJSON data (the inner data block)
    """
    if filepath.suffix == ".gz" or str(filepath).endswith(".json.gz"):
        with gzip.open(filepath, "rt", encoding="utf-8") as f:
            content = f.read()
    else:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

    raw = load_mmjson(content)

    # Extract the data block (data_<ENTRY_ID>)
    # The file typically has one key like "data_100D"
    for key, value in raw.items():
        if key.startswith("data_") and isinstance(value, dict):
            return value

    # Fallback: return as-is if no data_ block found
    return raw


def get_rows(data: dict[str, Any], category: str) -> list[dict[str, Any]]:
    """Convert mmJSON category to list of row dicts.

    Args:
        data: mmJSON data
        category: Category name to extract

    Returns:
        List of dicts, one per row
    """
    if category not in data:
        return []

    cat_data = data[category]
    if not cat_data:
        return []

    # Get all column names
    columns = list(cat_data.keys())
    if not columns:
        return []

    # Get number of rows from first column
    num_rows = len(cat_data[columns[0]])

    # Build rows
    rows = []
    for i in range(num_rows):
        row = {}
        for col in columns:
            values = cat_data[col]
            row[col] = values[i] if i < len(values) else None
        rows.append(row)

    return rows


def get_value(data: dict[str, Any], category: str, column: str, row: int = 0) -> Any:
    """Get a single value from mmJSON data.

    Args:
        data: mmJSON data
        category: Category name
        column: Column name
        row: Row index (default 0)

    Returns:
        The value, or None if not found
    """
    if category not in data:
        return None

    cat_data = data[category]
    if column not in cat_data:
        return None

    values = cat_data[column]
    if row >= len(values):
        return None

    return values[row]


def merge_mmjson(base: dict[str, Any], plus: dict[str, Any]) -> dict[str, Any]:
    """Merge two mmJSON files (base + plus data).

    The 'plus' data is typically additional annotations from PDBj.
    Plus data takes precedence for overlapping categories.

    Args:
        base: Base mmJSON data
        plus: Additional mmJSON data to merge

    Returns:
        Merged mmJSON data
    """
    result = dict(base)

    for category, cat_data in plus.items():
        if category in result:
            # Merge columns - plus takes precedence
            result[category] = {**result[category], **cat_data}
        else:
            result[category] = cat_data

    return result
