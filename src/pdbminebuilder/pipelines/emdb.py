"""EMDB pipeline - Electron Microscopy Data Bank data loader.

EMDB uses XML data files. The pipeline:
1. Parses XML files using defusedxml for security
2. Extracts entry ID from filename (EMD-1234 -> docid 1234)
3. Stores dates from admin.key_dates in brief_summary
4. Stores the entire data content as JSONB in brief_summary.content
"""

import json
import logging
import traceback
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element

import defusedxml.ElementTree as ET
from rich.console import Console
from sqlalchemy import MetaData, Table

from pdbminebuilder.config import PipelineConfig, Settings
from pdbminebuilder.db.loader import (
    Job,
    LoaderResult,
    get_all_tables,
)
from pdbminebuilder.pipelines.base import BasePipeline, sync_entry_tables, transform_category

console = Console()


def _xml_to_dict(element: Element) -> dict[str, Any] | str | list[Any]:
    """Convert XML element to dictionary recursively.

    Handles:
    - Elements with children -> dict
    - Elements with text only -> string
    - Multiple elements with same tag -> list
    """
    result: dict[str, Any] = {}

    # Process child elements
    for child in element:
        tag = child.tag
        child_data = _xml_to_dict(child)

        if tag in result:
            # Convert to list if multiple elements with same tag
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_data)
        else:
            result[tag] = child_data

    # If no children, return text content
    if not result:
        text = element.text
        return text.strip() if text else ""

    # If has both children and text, add text as special key
    if element.text and element.text.strip():
        result["_text"] = element.text.strip()

    return result


def _get_nested(data: dict[str, Any], *keys: str) -> Any:
    """Safely get nested dictionary value.

    Args:
        data: Dictionary to traverse
        keys: Sequence of keys to follow

    Returns:
        Value at the nested path, or None if not found
    """
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
        if current is None:
            return None
    return current


def _ensure_list(value: Any) -> list[Any]:
    """Ensure value is a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


class EmdbPipeline(BasePipeline):
    """Pipeline for loading EMDB data from XML files."""

    name = "emdb"
    file_pattern = "emd-*-v*.xml"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract entry ID from filepath.

        Handles filenames like: emd-1234-v1.0.xml -> EMD-1234
        """
        name = filepath.name
        # Remove .xml
        if name.endswith(".xml"):
            name = name[:-4]
        # Extract EMD-1234 part from emd-1234-v1.0
        parts = name.split("-")
        if len(parts) >= 2:
            # parts[0] = 'emd', parts[1] = '1234', rest is version
            return f"EMD-{parts[1]}".upper()
        return name.upper()

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find EMDB XML files."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath in data_dir.rglob(self.file_pattern):
            entry_id = self.extract_entry_id(filepath)
            jobs.append(
                Job(
                    entry_id=entry_id,
                    filepath=filepath,
                    extra={},
                )
            )

            if limit and len(jobs) >= limit:
                break
        return jobs

    def process_job(
        self,
        job: Job,
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single EMDB entry."""
        try:
            from pdbminebuilder.models import get_metadata

            meta = get_metadata(schema_name)

            # Parse XML file
            tree = ET.parse(str(job.filepath))
            root = tree.getroot()
            data_raw = _xml_to_dict(root)

            # Root element always returns a dict
            if not isinstance(data_raw, dict):
                raise ValueError(f"Invalid XML structure in {job.filepath}")
            data: dict[str, Any] = data_raw

            # Transform to row-oriented format for other tables
            row_data = self._xml_to_row_oriented(data)

            # Transform and load
            table_rows: dict[str, list[dict[str, Any]]] = {}

            # Load brief_summary first
            brief_rows = self._transform_brief_summary(
                data, row_data, job.entry_id, meta
            )
            if brief_rows:
                table_rows["brief_summary"] = brief_rows

            # Load other categories
            for table in get_all_tables(meta):
                if table.name == "brief_summary":
                    continue

                category_rows = self._transform_category(row_data, table, job.entry_id)
                if category_rows:
                    table_rows[table.name] = category_rows

            inserted, updated, _deleted = sync_entry_tables(
                conninfo=conninfo,
                meta=meta,
                entry_id=job.entry_id,
                table_rows=table_rows,
            )

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=inserted,
                rows_updated=updated,
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )

    def _xml_to_row_oriented(self, data: dict[str, Any]) -> dict[str, list[dict]]:
        """Convert XML dict structure to row-oriented format.

        EMDB XML has a hierarchical structure that needs to be flattened
        into category-based row-oriented format for database loading.
        """
        result: dict[str, list[dict]] = {}

        # Map XML structure to mmCIF-like categories
        # The XML structure varies, so we need to handle it flexibly

        # Process admin data
        admin_data = data.get("admin", {})
        if admin_data:
            result["em_admin"] = [self._flatten_dict(admin_data)]

        # Process crossreferences -> database_2, pdbx_database_related
        crossrefs = data.get("crossreferences", {})
        if crossrefs:
            db_refs = _ensure_list(
                crossrefs.get("pdb_list", {}).get("pdb_reference", [])
            )
            if db_refs:
                result["database_2"] = [
                    {"database_id": "PDB", "database_code": ref.get("pdb_id", "")}
                    for ref in db_refs
                    if isinstance(ref, dict)
                ]

            emdb_refs = _ensure_list(
                crossrefs.get("emdb_list", {}).get("emdb_reference", [])
            )
            if emdb_refs:
                result["pdbx_database_related"] = [
                    {
                        "db_name": "EMDB",
                        "db_id": ref.get("emdb_id", ""),
                        "content_type": ref.get("relationship", ""),
                    }
                    for ref in emdb_refs
                    if isinstance(ref, dict)
                ]

        # Process sample -> em_entity_assembly, entity, etc.
        sample = data.get("sample", {})
        if sample:
            # Supramolecule
            supra = sample.get("supramolecule", {})
            if supra:
                supra_list = _ensure_list(supra)
                result["em_entity_assembly"] = [
                    self._flatten_dict(s) for s in supra_list if isinstance(s, dict)
                ]

            # Macromolecule
            macro = sample.get("macromolecule_list", {}).get("macromolecule", [])
            if macro:
                macro_list = _ensure_list(macro)
                result["entity"] = [
                    self._flatten_dict(m) for m in macro_list if isinstance(m, dict)
                ]

        # Process structure_determination_list -> em_imaging, em_3d_reconstruction, etc.
        struct_det = data.get("structure_determination_list", {})
        if struct_det:
            det_list = _ensure_list(struct_det.get("structure_determination", []))
            for det in det_list:
                if not isinstance(det, dict):
                    continue

                # Imaging
                imaging = det.get("microscopy_list", {}).get("microscopy", [])
                if imaging:
                    img_list = _ensure_list(imaging)
                    if "em_imaging" not in result:
                        result["em_imaging"] = []
                    result["em_imaging"].extend(
                        [self._flatten_dict(i) for i in img_list if isinstance(i, dict)]
                    )

                # Reconstruction
                recon = det.get("image_processing", [])
                if recon:
                    recon_list = _ensure_list(recon)
                    if "em_3d_reconstruction" not in result:
                        result["em_3d_reconstruction"] = []
                    result["em_3d_reconstruction"].extend(
                        [
                            self._flatten_dict(r)
                            for r in recon_list
                            if isinstance(r, dict)
                        ]
                    )

        # Process map -> em_map
        map_data = data.get("map", {})
        if map_data:
            result["em_map"] = [self._flatten_dict(map_data)]

        return result

    def _flatten_dict(self, data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
        """Flatten nested dict to single level with underscore-joined keys."""
        result: dict[str, Any] = {}
        for key, value in data.items():
            new_key = f"{prefix}_{key}" if prefix else key
            if isinstance(value, dict):
                # Check if it's a simple dict with just text
                if "_text" in value or not value:
                    result[new_key] = value.get("_text", "")
                else:
                    result.update(self._flatten_dict(value, new_key))
            elif isinstance(value, list):
                # For lists, take first element if scalar values
                if value and not isinstance(value[0], (dict, list)):
                    result[new_key] = value[0] if len(value) == 1 else value
                elif value and isinstance(value[0], dict):
                    # Skip nested list of dicts (handled separately)
                    pass
            else:
                result[new_key] = value
        return result

    def _transform_brief_summary(
        self,
        xml_data: dict[str, Any],
        row_data: dict[str, list[dict]],
        entry_id: str,
        meta: MetaData,
    ) -> list[dict]:
        """Transform data to brief_summary format.

        EMDB brief_summary stores:
        - emdb_id: entry ID (EMD-1234)
        - docid: integer part (1234)
        - dates from admin.key_dates
        - content: entire data as JSONB (excluding brief_summary)
        - keywords: empty array
        """
        # Extract docid from entry_id (EMD-1234 -> 1234)
        try:
            docid = int(entry_id.split("-")[1])
        except (IndexError, ValueError):
            docid = 0

        # Extract dates from admin.key_dates
        admin = xml_data.get("admin", {})
        key_dates = admin.get("key_dates", {})

        deposition_date = key_dates.get("deposition")
        header_release_date = key_dates.get("header_release")
        map_release_date = key_dates.get("map_release")
        modification_date = key_dates.get("update")

        # Handle string or dict with _text
        def get_date(val: Any) -> str | None:
            if val is None:
                return None
            if isinstance(val, str):
                return val if val else None
            if isinstance(val, dict):
                return val.get("_text")
            return None

        # Create content as JSONB (entire data except brief_summary)
        content = {k: v for k, v in row_data.items() if k != "brief_summary"}

        return [
            {
                "emdb_id": entry_id,
                "docid": docid,
                "deposition_date": get_date(deposition_date),
                "header_release_date": get_date(header_release_date),
                "map_release_date": get_date(map_release_date),
                "modification_date": get_date(modification_date),
                "update_date": None,
                "content": json.dumps(content),
                "keywords": [],
            }
        ]

    def _transform_category(
        self,
        data: dict[str, list[dict]],
        table: Table,
        entry_id: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        # Use base transform_category with no column normalization
        return transform_category(rows, table, entry_id, "emdb_id", None)


def run(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the EMDB pipeline."""
    pipeline = EmdbPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)
