"""Contacts pipeline - protein-protein contact data.

Contact files have a custom JSON format (not mmJSON). Two formats exist:

1. Array format (legacy):
   [[pdbid, asym_id_1, asym_id_2, seq_id_1, seq_id_2, comp_id_1, comp_id_2, distance, ...], ...]

2. Column-oriented format (new):
   {"label_asym_id_1": [...], "label_asym_id_2": [...], ...}
"""

import gzip
import json
import logging
import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, bulk_upsert
from mine2.pipelines.base import BasePipeline

console = Console()


class ContactsPipeline(BasePipeline):
    """Pipeline for loading protein contact data.

    Contact files use a custom JSON format (not mmJSON). Two formats are supported:

    1. Array format (legacy): List of arrays
       [[pdbid, label_asym_id_1, ...], ...]

    2. Column-oriented format: Dict of column arrays
       {"label_asym_id_1": [...], "label_asym_id_2": [...], ...}
    """

    name = "contacts"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract PDB ID from filename."""
        name = filepath.name
        if name.endswith(".json.gz"):
            name = name[:-8]
        return name.lower()

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process contact data for a single entry."""
        try:
            # Load JSON file (not mmJSON format)
            data = self._load_contacts_file(job.filepath)
            rows_inserted = 0

            # Generate and load brief_summary
            brief_rows = [{"pdbid": job.entry_id}]
            columns = list(brief_rows[0].keys())
            inserted, _ = bulk_upsert(
                conninfo,
                schema_def.schema_name,
                "brief_summary",
                columns,
                [tuple(r[c] for c in columns) for r in brief_rows],
                ["pdbid"],
            )
            rows_inserted += inserted

            # Transform and load contacts
            contact_rows = self._transform_contacts(data, job.entry_id)
            if contact_rows:
                columns = list(contact_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "list",
                    columns,
                    [tuple(r[c] for c in columns) for r in contact_rows],
                    [
                        "pdbid",
                        "label_asym_id_1",
                        "label_asym_id_2",
                        "label_seq_id_1",
                        "label_seq_id_2",
                    ],
                )
                rows_inserted += inserted

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=rows_inserted,
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )

    def _load_contacts_file(
        self, filepath: Path
    ) -> list[list[Any]] | dict[str, list[Any]]:
        """Load contacts JSON file.

        Returns either:
        - list[list]: Array format (legacy)
        - dict[str, list]: Column-oriented format (new)
        """
        if str(filepath).endswith(".json.gz"):
            with gzip.open(filepath, "rt", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(filepath, encoding="utf-8") as f:
                return json.load(f)

    # Required columns for column-oriented format
    _REQUIRED_COLUMNS = (
        "label_asym_id_1",
        "label_asym_id_2",
        "label_seq_id_1",
        "label_seq_id_2",
        "label_comp_id_1",
        "label_comp_id_2",
        "distance",
    )

    def _transform_contacts(
        self, data: list[list[Any]] | dict[str, list[Any]], pdbid: str
    ) -> list[dict]:
        """Transform contact records to database rows.

        Supports two formats:

        1. Array format (legacy):
           [[pdbid, asym_id_1, asym_id_2, seq_id_1, seq_id_2, comp_id_1, comp_id_2, distance, ...], ...]

        2. Column-oriented format (new):
           {
             "label_asym_id_1": [...],
             "label_asym_id_2": [...],
             "label_seq_id_1": [...],
             "label_seq_id_2": [...],
             "label_comp_id_1": [...],
             "label_comp_id_2": [...],
             "distance": [...]
           }
        """
        result = []

        if isinstance(data, dict):
            # Column-oriented format - validate required columns
            missing = set(self._REQUIRED_COLUMNS) - data.keys()
            if missing:
                raise ValueError(f"Missing required columns: {missing}")

            # Validate all columns have equal length
            lengths = {
                k: len(v) for k, v in data.items() if k in self._REQUIRED_COLUMNS
            }
            unique_lengths = set(lengths.values())
            if len(unique_lengths) > 1:
                raise ValueError(f"Column length mismatch: {lengths}")

            n = lengths.get("label_asym_id_1", 0)
            for i in range(n):
                result.append(
                    {
                        "pdbid": pdbid,
                        "label_asym_id_1": data["label_asym_id_1"][i],
                        "label_asym_id_2": data["label_asym_id_2"][i],
                        "label_seq_id_1": data["label_seq_id_1"][i],
                        "label_seq_id_2": data["label_seq_id_2"][i],
                        "label_comp_id_1": data["label_comp_id_1"][i],
                        "label_comp_id_2": data["label_comp_id_2"][i],
                        "distance": data["distance"][i],
                    }
                )
        else:
            # Array format (legacy)
            for record in data:
                if len(record) < 8:
                    continue

                result.append(
                    {
                        "pdbid": pdbid,
                        "label_asym_id_1": record[1],
                        "label_asym_id_2": record[2],
                        "label_seq_id_1": record[3],
                        "label_seq_id_2": record[4],
                        "label_comp_id_1": record[5],
                        "label_comp_id_2": record[6],
                        "distance": record[7],
                    }
                )

        return result


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the contacts pipeline."""
    pipeline = ContactsPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)
