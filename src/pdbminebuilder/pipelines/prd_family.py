"""PRD Family pipeline - loads BIRD family classification data from family-all.cif.gz.

CIF-only (no mmJSON variant). Each CIF data block represents one family entry
(e.g., FAM_000001).
"""

import logging
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import gemmi
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    track,
)
from sqlalchemy import MetaData

from pdbminebuilder.config import PipelineConfig, Settings
from pdbminebuilder.db.loader import LoaderResult, get_all_tables, get_entry_pk
from pdbminebuilder.parsers.cif import parse_block
from pdbminebuilder.pipelines.base import BaseCifBatchPipeline, transform_category

console = Console()


# =============================================================================
# Worker function for parallel CIF processing.
# Must be at module level to be picklable by ProcessPoolExecutor.
# =============================================================================


def _parse_prd_family_cif_block(
    block: gemmi.cif.Block,
    schema_name: str,
) -> tuple[str, dict[str, list[dict]], str | None]:
    """Parse a single PRD family CIF block.

    Args:
        block: gemmi CIF block (e.g., FAM_000001)
        schema_name: Schema name for model lookup

    Returns:
        Tuple of (family_prd_id, table_rows_dict, error_message or None)
    """
    family_prd_id = block.name

    try:
        from pdbminebuilder.models import get_metadata

        meta = get_metadata(schema_name)
        entry_pk = get_entry_pk(meta)

        data = parse_block(block)
        table_rows: dict[str, list[dict]] = {}

        # Generate brief_summary
        brief_rows = _generate_brief_summary(data, family_prd_id)
        if brief_rows:
            table_rows["brief_summary"] = brief_rows

        # Process other tables
        for table in get_all_tables(meta):
            if table.name == "brief_summary":
                continue

            rows = data.get(table.name, [])
            # CIF uses plain column names, no normalization needed
            category_rows = transform_category(
                rows, table, family_prd_id, entry_pk, None
            )
            if category_rows:
                table_rows[table.name] = category_rows

        return (family_prd_id, table_rows, None)

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return (family_prd_id, {}, error_msg)


def _generate_brief_summary(data: dict[str, Any], family_prd_id: str) -> list[dict]:
    """Generate synthetic brief_summary row.

    Extracts name from pdbx_reference_molecule_family and initial/modified
    dates from pdbx_family_prd_audit.
    """
    # Get name from pdbx_reference_molecule_family
    family_rows = data.get("pdbx_reference_molecule_family", [])
    name = family_rows[0].get("name") if family_rows else None

    # Get dates from pdbx_family_prd_audit
    audit_rows = data.get("pdbx_family_prd_audit", [])
    initial_date = None
    modified_date = None
    for row in audit_rows:
        action = row.get("action_type")
        date = row.get("date")
        if action == "Initial release":
            initial_date = date
        elif action == "Modify record":
            # Keep the latest modify date (ISO 8601 strings compare correctly)
            if modified_date is None or (date is not None and date > modified_date):
                modified_date = date

    return [
        {
            "family_prd_id": family_prd_id,
            "name": name,
            "pdbx_initial_date": initial_date,
            "pdbx_modified_date": modified_date,
        }
    ]


class PrdFamilyCifPipeline(BaseCifBatchPipeline):
    """Pipeline for loading PRD family data from CIF file.

    Uses family-all.cif.gz which contains all family entries.
    Each data block represents one family (e.g., FAM_000001).
    """

    name = "prd_family-cif"

    def run(
        self, limit: int | None = None, logger: logging.Logger | None = None
    ) -> list[LoaderResult]:
        """Run the pipeline with batch insert optimization."""
        cif_path = self._find_cif_file()
        if not cif_path:
            return []
        console.print(f"  CIF file: {cif_path}")

        console.print("  Loading CIF...")
        doc = gemmi.cif.read(str(cif_path))
        total_blocks = len(doc)
        console.print(f"  Found {total_blocks} entries")

        max_workers = self.settings.rdb.get_workers()
        conninfo = self.settings.rdb.constring

        blocks = list(doc)[:limit]
        if limit:
            console.print(f"  Processing {len(blocks)} (limited)")

        console.print("[bold]Phase 1: Parsing blocks...[/bold]")
        parsed_results = self._parse_all_blocks(blocks, max_workers)

        console.print("[bold]Phase 2: Batch upserting...[/bold]")
        results = self._batch_insert(parsed_results, conninfo)

        self._prune_stale_rows(results, conninfo, limit)

        self._print_summary(results, logger)
        return results

    def _parse_all_blocks(
        self,
        blocks: list[gemmi.cif.Block],
        max_workers: int,
    ) -> list[tuple[str, dict[str, list[dict]], str | None]]:
        """Parse all blocks in parallel, returning parsed data."""
        schema_name = self.meta.schema
        if len(blocks) <= 10 or max_workers == 1:
            results = []
            for block in track(blocks, description="Parsing...", console=console):
                result = _parse_prd_family_cif_block(block, schema_name)
                results.append(result)
            return results

        results: list[tuple[str, dict[str, list[dict]], str | None]] = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _parse_prd_family_cif_block, block, schema_name
                ): block.name
                for block in blocks
            }

            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Parsing", total=len(futures))

                for future in as_completed(futures):
                    fam_id = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append((fam_id, {}, f"{e}\n{traceback.format_exc()}"))
                    progress.advance(task)

        return results

    def _find_cif_file(self) -> Path | None:
        """Find family-all.cif.gz file in data directory."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return None

        # Try direct path first
        cif_path = data_dir.joinpath("family-all.cif.gz")
        if cif_path.is_file():
            return cif_path

        # Handle rsync quirk where filename becomes directory
        nested_path = data_dir.joinpath("family-all.cif.gz", "family-all.cif.gz")
        if nested_path.is_file():
            return nested_path

        # Search recursively
        for path in data_dir.rglob("family-all.cif.gz"):
            if path.is_file():
                return path

        console.print(f"  [red]family-all.cif.gz not found in: {data_dir}[/red]")
        return None


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the prd_family pipeline in CIF mode."""
    pipeline = PrdFamilyCifPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)


def run_cif_load(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run prd_family pipeline in load mode (COPY, no delta sync)."""
    pipeline = PrdFamilyCifPipeline(settings, config, meta)
    return pipeline.run_load(limit, logger=logger)
