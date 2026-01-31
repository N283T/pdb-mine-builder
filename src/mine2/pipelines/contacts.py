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
from mine2.db.loader import (
    Job,
    LoaderResult,
    ParsedEntry,
    SchemaDef,
    bulk_upsert,
    run_loader_chunked,
)
from mine2.pipelines.base import BasePipeline

console = Console()

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


def _load_contacts_file(filepath: Path) -> list[list[Any]] | dict[str, list[Any]]:
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


def _transform_contacts(
    data: list[list[Any]] | dict[str, list[Any]], pdbid: str
) -> list[dict]:
    """Transform contact records to database rows.

    Supports two formats:

    1. Array format (legacy):
       [[pdbid, asym_id_1, asym_id_2, seq_id_1, seq_id_2, comp_id_1, comp_id_2, distance, ...], ...]

    2. Column-oriented format (new):
       {
         "label_asym_id_1": [...],
         "label_asym_id_2": [...],
         ...
       }
    """
    result = []

    if isinstance(data, dict):
        # Column-oriented format - validate required columns
        missing = set(_REQUIRED_COLUMNS) - data.keys()
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Validate all columns have equal length
        lengths = {k: len(v) for k, v in data.items() if k in _REQUIRED_COLUMNS}
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


def _parse_contacts_entry(job: Job, schema_def: SchemaDef) -> ParsedEntry:
    """Parse a single contacts entry for chunked processing.

    This function is called by workers in run_loader_chunked.
    Returns parsed data without DB operations.
    """
    try:
        data = _load_contacts_file(job.filepath)
        table_rows: dict[str, list[dict]] = {}

        # brief_summary
        table_rows["brief_summary"] = [{"pdbid": job.entry_id}]

        # contacts list
        contact_rows = _transform_contacts(data, job.entry_id)
        if contact_rows:
            table_rows["list"] = contact_rows

        return ParsedEntry(
            entry_id=job.entry_id,
            table_rows=table_rows,
        )

    except Exception as e:
        import traceback

        error_msg = f"{e}\n{traceback.format_exc()}"
        return ParsedEntry(
            entry_id=job.entry_id,
            table_rows={},
            error=error_msg,
        )


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
            data = _load_contacts_file(job.filepath)
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
            contact_rows = _transform_contacts(data, job.entry_id)
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


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    chunk_size: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the contacts pipeline.

    Args:
        settings: Application settings
        config: Pipeline configuration
        schema_def: Schema definition
        limit: Optional limit on entries to process
        chunk_size: If provided, use chunked batch insert mode
        logger: Optional logger
    """
    pipeline = ContactsPipeline(settings, config, schema_def)

    if chunk_size:
        # Chunked mode: collect jobs first, then process in chunks
        console.print(f"  Data dir: {config.data}")
        console.print(
            f"  [dim]Using chunked batch insert (chunk_size={chunk_size})[/dim]"
        )

        jobs = pipeline.find_jobs(limit)
        if not jobs:
            console.print("  [yellow]No files found[/yellow]")
            return []

        return run_loader_chunked(
            settings=settings,
            schema_def=schema_def,
            jobs=jobs,
            parse_func=_parse_contacts_entry,
            chunk_size=chunk_size,
            max_workers=settings.rdb.get_workers(),
            logger=logger,
        )
    else:
        # Default mode
        return pipeline.run(limit, logger=logger)
