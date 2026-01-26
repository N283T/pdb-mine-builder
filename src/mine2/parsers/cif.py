"""CIF parser using gemmi library."""

import gzip
from pathlib import Path
from typing import Any

import gemmi


def parse_cif(content: str) -> dict[str, Any]:
    """Parse CIF content string into a dictionary.

    Returns a dict where keys are category names (e.g., 'entry', 'atom_site')
    and values are lists of rows (each row is a dict of column -> value).
    """
    doc = gemmi.cif.read_string(content)

    result: dict[str, Any] = {}

    for block in doc:
        block_name = block.name

        for item in block:
            if item.loop is not None:
                # Loop (table) data
                loop = item.loop
                tags = [
                    tag.split(".")[-1] for tag in loop.tags
                ]  # Remove category prefix
                category = (
                    loop.tags[0].split(".")[0].lstrip("_") if loop.tags else "unknown"
                )

                rows = []
                width = loop.width()
                for row_idx in range(loop.length()):
                    row_data = {}
                    for col_idx, tag in enumerate(tags):
                        value = loop.values[row_idx * width + col_idx]
                        # Convert CIF special values
                        if value in (".", "?"):
                            value = None
                        row_data[tag] = value
                    rows.append(row_data)

                if category in result:
                    result[category].extend(rows)
                else:
                    result[category] = rows

            elif item.pair is not None:
                # Single key-value pair
                tag, value = item.pair
                category = tag.split(".")[0].lstrip("_")
                column = tag.split(".")[-1]

                if value in (".", "?"):
                    value = None

                if category not in result:
                    result[category] = [{}]
                if len(result[category]) == 0:
                    result[category].append({})
                result[category][0][column] = value

        # Store block name for reference
        result["_block_name"] = block_name

    return result


def parse_cif_file(filepath: Path) -> dict[str, Any]:
    """Parse a CIF file (supports gzip compression).

    Args:
        filepath: Path to the CIF file (.cif or .cif.gz)

    Returns:
        Parsed CIF data as dictionary
    """
    if filepath.suffix == ".gz" or str(filepath).endswith(".cif.gz"):
        with gzip.open(filepath, "rt", encoding="utf-8") as f:
            content = f.read()
    else:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

    return parse_cif(content)


def cif_to_mmjson_format(cif_data: dict[str, Any]) -> dict[str, Any]:
    """Convert CIF dict to mmJSON-like format.

    mmJSON format uses arrays of values instead of list of dicts:
    {
        "category": {
            "column1": ["val1", "val2"],
            "column2": ["val1", "val2"]
        }
    }
    """
    result: dict[str, Any] = {}

    for category, rows in cif_data.items():
        if category.startswith("_"):
            continue
        if not rows:
            continue

        # Convert list of dicts to dict of lists
        columns: dict[str, list] = {}
        for row in rows:
            for key, value in row.items():
                if key not in columns:
                    columns[key] = []
                columns[key].append(value)

        result[category] = columns

    return result
