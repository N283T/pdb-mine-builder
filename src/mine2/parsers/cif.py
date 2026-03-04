"""CIF parser using gemmi library."""

import gzip
import logging
from pathlib import Path
from typing import Any

import gemmi

logger = logging.getLogger(__name__)


def _normalize_cif_value(value: Any) -> Any:
    """Normalize CIF special values.

    gemmi converts: '?' -> None, '.' -> False
    We normalize both to None for database insertion.
    """
    if value is False:
        return None
    return value


def parse_block(block: gemmi.cif.Block) -> dict[str, Any]:
    """Parse a single gemmi Block into row-oriented dict."""
    result: dict[str, Any] = {}
    result["_block_name"] = block.name
    logger.debug("Parsing block: %s", block.name)

    for cat_name in block.get_mmcif_category_names():
        # '_entry.' -> 'entry'
        category = cat_name.strip("_").rstrip(".")
        col_data = block.get_mmcif_category(cat_name)

        if not col_data:
            continue

        # Convert column-oriented to row-oriented, normalizing values
        keys = list(col_data.keys())
        n_rows = len(col_data[keys[0]]) if keys else 0
        rows = [
            {k: _normalize_cif_value(col_data[k][i]) for k in keys}
            for i in range(n_rows)
        ]

        if category in result:
            result[category].extend(rows)
        else:
            result[category] = rows

        logger.debug("  Category %s: %d rows, %d columns", category, n_rows, len(keys))

    return result


def parse_cif_document(doc: gemmi.cif.Document) -> dict[str, Any]:
    """Parse gemmi Document into a dictionary.

    Uses gemmi's get_mmcif_category() for efficient parsing.
    Returns a dict where keys are category names (e.g., 'entry', 'atom_site')
    and values are lists of rows (each row is a dict of column -> value).

    For CIF files with multiple blocks, data from all blocks is merged.
    Metadata:
    - `_block_name`: Name of the last block (for backward compatibility)
    - `_block_names`: List of all block names (when multiple blocks exist)
    """
    result: dict[str, Any] = {}
    block_names: list[str] = []

    for block in doc:
        block_data = parse_block(block)
        # Merge block data into result
        for key, value in block_data.items():
            if key == "_block_name":
                block_names.append(value)
            elif key in result and isinstance(value, list):
                result[key].extend(value)
            else:
                result[key] = value

    # Store block name(s)
    if block_names:
        result["_block_name"] = block_names[-1]  # Last block for compatibility
        if len(block_names) > 1:
            result["_block_names"] = block_names

    return result


def parse_cif(content: str) -> dict[str, Any]:
    """Parse CIF content string into a dictionary.

    Returns a dict where keys are category names (e.g., 'entry', 'atom_site')
    and values are lists of rows (each row is a dict of column -> value).
    """
    doc = gemmi.cif.read_string(content)
    return parse_cif_document(doc)


def parse_cif_file(filepath: Path | str) -> dict[str, Any]:
    """Parse a CIF file (supports gzip compression).

    Uses gemmi.cif.read() which handles .gz files automatically.

    Args:
        filepath: Path to the CIF file (.cif or .cif.gz)

    Returns:
        Parsed CIF data as dictionary
    """
    logger.debug("Parsing CIF file: %s", filepath)
    doc = gemmi.cif.read(str(filepath))
    logger.debug("CIF document has %d block(s)", len(doc))
    return parse_cif_document(doc)


# =============================================================================
# mmJSON support
# =============================================================================


_MAX_MMJSON_DECOMPRESSED_SIZE = 500 * 1024 * 1024  # 500 MB safety limit


def _read_mmjson_gz(filepath: Path | str) -> gemmi.cif.Document:
    """Read an mmJSON file, handling gzip decompression in Python.

    gemmi's built-in gz reader rejects files with compression ratios
    exceeding ~100x (see gemmi src/gz.cpp estimate_uncompressed_size).
    We bypass this by decompressing in Python and passing the string
    to gemmi.
    """
    filepath = Path(filepath)
    if filepath.suffix == ".gz":
        with gzip.open(filepath, "rt", encoding="utf-8") as f:
            content = f.read(_MAX_MMJSON_DECOMPRESSED_SIZE + 1)
            if len(content) > _MAX_MMJSON_DECOMPRESSED_SIZE:
                raise ValueError(
                    f"Decompressed size of {filepath} exceeds "
                    f"{_MAX_MMJSON_DECOMPRESSED_SIZE} bytes safety limit"
                )
            return gemmi.cif.read_mmjson_string(content)
    return gemmi.cif.read_mmjson(str(filepath))


def parse_mmjson_document(doc: gemmi.cif.Document) -> dict[str, Any]:
    """Parse gemmi Document (from mmJSON) into a dictionary.

    Same output format as parse_cif_document - row-oriented dict.
    Uses the first block by default (use parse_mmjson_blocks for multi-block).
    """
    if len(doc) == 0:
        return {}
    return parse_block(doc[0])


def parse_mmjson_blocks(doc: gemmi.cif.Document) -> dict[str, dict[str, Any]]:
    """Parse all blocks from mmJSON Document.

    Returns dict mapping block names to their row-oriented data.
    Useful for PRD files with multiple data blocks.
    """
    return {block.name: parse_block(block) for block in doc}


def parse_mmjson(content: str) -> dict[str, Any]:
    """Parse mmJSON content string into a dictionary.

    Returns row-oriented dict (same format as parse_cif).
    """
    doc = gemmi.cif.read_mmjson_string(content)
    return parse_mmjson_document(doc)


def parse_mmjson_file(filepath: Path | str) -> dict[str, Any]:
    """Parse an mmJSON file (supports gzip compression).

    Args:
        filepath: Path to the mmJSON file (.json or .json.gz)

    Returns:
        Parsed data as row-oriented dictionary
    """
    logger.debug("Parsing mmJSON file: %s", filepath)
    doc = _read_mmjson_gz(filepath)
    logger.debug("mmJSON document has %d block(s)", len(doc))
    return parse_mmjson_document(doc)


def parse_mmjson_file_blocks(filepath: Path | str) -> dict[str, dict[str, Any]]:
    """Parse an mmJSON file with multiple data blocks.

    Useful for PRD files that contain both PRD and PRDCC blocks.

    Args:
        filepath: Path to the mmJSON file (.json or .json.gz)

    Returns:
        Dict mapping block names to their row-oriented data
    """
    logger.debug("Parsing mmJSON file (multi-block): %s", filepath)
    doc = _read_mmjson_gz(filepath)
    logger.debug("mmJSON document has %d block(s)", len(doc))
    return parse_mmjson_blocks(doc)
