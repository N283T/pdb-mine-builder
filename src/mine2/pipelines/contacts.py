"""Contacts pipeline - protein-protein contact data.

Contact files have a custom JSON format (not mmJSON):
[
  [pdbid, asym_id_1, asym_id_2, seq_id_1, seq_id_2, comp_id_1, comp_id_2, distance, ...],
  ...
]
"""

import gzip
import json
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

    Contact files are JSON arrays of contact records, not mmJSON format.
    Each contact record is an array:
    [pdbid, label_asym_id_1, label_asym_id_2, label_seq_id_1, label_seq_id_2,
     label_comp_id_1, label_comp_id_2, distance, ...]
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

    def _load_contacts_file(self, filepath: Path) -> list[list[Any]]:
        """Load contacts JSON file (array of arrays)."""
        if str(filepath).endswith(".json.gz"):
            with gzip.open(filepath, "rt", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(filepath, encoding="utf-8") as f:
                return json.load(f)

    def _transform_contacts(self, data: list[list[Any]], pdbid: str) -> list[dict]:
        """Transform contact records to database rows.

        Contact record format (array):
        [0] pdbid (ignored, we use the extracted one)
        [1] label_asym_id_1
        [2] label_asym_id_2
        [3] label_seq_id_1
        [4] label_seq_id_2
        [5] label_comp_id_1
        [6] label_comp_id_2
        [7] distance
        [8+] atom details (ignored for this table)
        """
        result = []
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
) -> list[LoaderResult]:
    """Run the contacts pipeline."""
    pipeline = ContactsPipeline(settings, config, schema_def)
    return pipeline.run(limit)
