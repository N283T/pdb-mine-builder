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
from sqlalchemy import MetaData

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import (
    Job,
    LoaderResult,
    bulk_copy_entry,
    get_entry_pk,
    run_loader_streaming,
)
from mine2.pipelines.base import BasePipeline, sync_entry_tables

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
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process contact data for a single entry."""
        try:
            from mine2.models import get_metadata

            meta = get_metadata(schema_name)

            # Load JSON file (not mmJSON format)
            data = self._load_contacts_file(job.filepath)
            table_rows: dict[str, list[dict[str, Any]]] = {}

            # Generate and load brief_summary
            brief_rows = [{"pdbid": job.entry_id}]
            table_rows["brief_summary"] = brief_rows

            # Transform and load contacts
            contact_rows = self._transform_contacts(data, job.entry_id)
            if contact_rows:
                table_rows["list"] = contact_rows

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
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the contacts pipeline."""
    pipeline = ContactsPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)


# =============================================================================
# Load mode (COPY protocol, no delta sync)
# =============================================================================

_default_logger = logging.getLogger("mine2.pipelines.contacts")


def _process_contacts_load(
    job: Job,
    schema_name: str,
    conninfo: str,
) -> LoaderResult:
    """Worker: load JSON -> transform -> bulk_copy_entry."""
    try:
        from mine2.models import get_metadata

        meta = get_metadata(schema_name)
        pipeline_instance = ContactsPipeline.__new__(ContactsPipeline)

        # Load and transform
        data = pipeline_instance._load_contacts_file(job.filepath)
        table_rows: dict[str, list[dict[str, Any]]] = {}

        table_rows["brief_summary"] = [{"pdbid": job.entry_id}]

        contact_rows = pipeline_instance._transform_contacts(data, job.entry_id)
        if contact_rows:
            table_rows["list"] = contact_rows

        inserted = bulk_copy_entry(
            conninfo=conninfo,
            schema=meta.schema,
            entry_id=job.entry_id,
            pk_column=get_entry_pk(meta),
            table_rows=table_rows,
        )

        return LoaderResult(
            entry_id=job.entry_id,
            success=True,
            rows_inserted=inserted,
        )

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return LoaderResult(
            entry_id=job.entry_id,
            success=False,
            error=error_msg,
        )


def run_cif_load(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run contacts pipeline in load mode (COPY, no delta sync)."""
    if logger is None:
        logger = _default_logger

    console.print(f"  Data dir: {config.data}")

    pipeline = ContactsPipeline(settings, config, meta)

    data_dir = Path(config.data)
    if not data_dir.exists():
        console.print(f"  [red]Data directory not found: {data_dir}[/red]")
        return []

    def _iter_jobs():
        for filepath in sorted(data_dir.rglob(pipeline.file_pattern)):
            entry_id = pipeline.extract_entry_id(filepath)
            yield Job(entry_id=entry_id, filepath=filepath)

    return run_loader_streaming(
        settings=settings,
        schema_name=meta.schema,
        jobs_iter=_iter_jobs(),
        process_func=_process_contacts_load,
        max_workers=settings.rdb.get_workers(),
        limit=limit,
        logger=logger,
    )
