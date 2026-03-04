"""Chemical Component Model pipeline."""

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

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import (
    Job,
    LoaderResult,
    SchemaDef,
    TableDef,
    bulk_upsert,
)
from mine2.parsers.cif import parse_block, parse_mmjson_file
from mine2.parsers.mmjson import normalize_column_name
from mine2.pipelines.base import (
    BaseCifBatchPipeline,
    BasePipeline,
    sync_entry_tables,
    transform_category,
)

console = Console()


# =============================================================================
# Worker function for parallel CIF processing (must be at module level)
# =============================================================================


def _parse_ccmodel_cif_block(
    block: gemmi.cif.Block,
    schema_def: SchemaDef,
) -> tuple[str, dict[str, list[dict]], str | None]:
    """Parse a single CIF block (worker function for parallel processing).

    Args:
        block: gemmi CIF block
        schema_def: Schema definition

    Returns:
        Tuple of (model_id, table_rows_dict, error_message or None)
        table_rows_dict maps table_name -> list of row dicts
    """
    model_id = block.name  # e.g., M_DAL_00001
    try:
        data = parse_block(block)
        table_rows: dict[str, list[dict]] = {}

        # Generate brief_summary
        brief_rows = _generate_brief_summary(data, model_id)
        if brief_rows:
            table_rows["brief_summary"] = brief_rows

        # Process other tables
        for table in schema_def.tables:
            if table.name == "brief_summary":
                continue

            rows = data.get(table.name, [])
            # CIF uses plain column names, no normalization needed
            category_rows = transform_category(
                rows, table, model_id, schema_def.primary_key, None
            )
            if category_rows:
                table_rows[table.name] = category_rows

        return (model_id, table_rows, None)

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return (model_id, {}, error_msg)


def _generate_brief_summary(data: dict[str, Any], model_id: str) -> list[dict]:
    """Generate brief_summary from pdbx_chem_comp_model data."""
    rows = data.get("pdbx_chem_comp_model", [])
    if not rows:
        return [{"model_id": model_id}]

    result = []
    for row in rows:
        result.append(
            {
                "model_id": model_id,
                "comp_id": row.get("comp_id"),
            }
        )
    return result


class CcmodelPipeline(BasePipeline):
    """Pipeline for loading Chemical Component Model data."""

    name = "ccmodel"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract model ID from filename.

        Handles filenames like: M_000_00001.json.gz -> M_000_00001
        """
        name = filepath.name
        if name.endswith(".json.gz"):
            name = name[:-8]
        return name

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single component model."""
        try:
            data = parse_mmjson_file(job.filepath)
            table_rows: dict[str, list[dict[str, Any]]] = {}

            # Generate and load brief_summary
            brief_rows = self._generate_brief_summary(data, job.entry_id)
            if brief_rows:
                table_rows["brief_summary"] = brief_rows

            # Load all tables from schema
            for table in schema_def.tables:
                if table.name == "brief_summary":
                    continue  # Already handled

                category_rows = self._transform_category(
                    data, table, job.entry_id, schema_def.primary_key
                )
                if category_rows:
                    table_rows[table.name] = category_rows

            inserted, updated, _deleted = sync_entry_tables(
                conninfo=conninfo,
                schema_def=schema_def,
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

    def _generate_brief_summary(
        self, data: dict[str, Any], model_id: str
    ) -> list[dict]:
        """Generate brief_summary from pdbx_chem_comp_model data."""
        rows = data.get("pdbx_chem_comp_model", [])
        if not rows:
            return [{"model_id": model_id}]

        result = []
        for row in rows:
            result.append(
                {
                    "model_id": model_id,
                    "comp_id": row.get("comp_id"),
                }
            )
        return result

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        model_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, model_id, pk_col, normalize_column_name)


class CcmodelCifPipeline(BaseCifBatchPipeline):
    """Pipeline for loading Chemical Component Models from single CIF file.

    Uses chem_comp_model.cif.gz which contains all models in one file.
    Each data block represents one model (e.g., M_DAL_00001).

    Uses batch processing: all blocks are parsed first (in parallel),
    then all rows are inserted in a single bulk operation per table.
    """

    name = "ccmodel-cif"

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
        console.print(f"  Found {total_blocks} models")

        max_workers = self.settings.rdb.get_workers()
        conninfo = self.settings.rdb.constring

        # Collect blocks to process
        blocks = list(doc)[:limit]
        if limit:
            console.print(f"  Processing {len(blocks)} (limited)")

        # Phase 1: Parse all blocks (parallel) - collect rows
        console.print("[bold]Phase 1: Parsing blocks...[/bold]")
        parsed_results = self._parse_all_blocks(blocks, max_workers)

        # Phase 2: Batch upsert all rows per table
        console.print("[bold]Phase 2: Batch upserting...[/bold]")
        results = self._batch_insert(parsed_results, conninfo)

        # Phase 3: Prune stale rows
        self._prune_stale_rows(results, conninfo, limit)

        self._print_summary(results, logger)
        return results

    def _parse_all_blocks(
        self,
        blocks: list[gemmi.cif.Block],
        max_workers: int,
    ) -> list[tuple[str, dict[str, list[dict]], str | None]]:
        """Parse all blocks in parallel, returning parsed data."""
        if len(blocks) <= 10 or max_workers == 1:
            # Sequential parsing
            results = []
            for block in track(blocks, description="Parsing...", console=console):
                result = _parse_ccmodel_cif_block(block, self.schema_def)
                results.append(result)
            return results

        # Parallel parsing
        results: list[tuple[str, dict[str, list[dict]], str | None]] = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _parse_ccmodel_cif_block, block, self.schema_def
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
                    model_id = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append((model_id, {}, str(e)))
                    progress.advance(task)

        return results

    def _find_cif_file(self) -> Path | None:
        """Find chem_comp_model.cif.gz file in data directory."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return None

        # Try direct path first
        cif_path = data_dir.joinpath("chem_comp_model.cif.gz")
        if cif_path.is_file():
            return cif_path

        # Handle rsync quirk where filename becomes directory
        nested_path = data_dir.joinpath(
            "chem_comp_model.cif.gz", "chem_comp_model.cif.gz"
        )
        if nested_path.is_file():
            return nested_path

        # Also check 'complete' subdirectory (rsync quirk)
        complete_path = data_dir.joinpath("complete", "chem_comp_model.cif.gz")
        if complete_path.is_file():
            return complete_path

        # Search recursively
        for path in data_dir.rglob("chem_comp_model.cif.gz"):
            if path.is_file():
                return path

        console.print(f"  [red]CIF file not found in: {data_dir}[/red]")
        return None


def _process_ccmodel_cif_block(
    block: gemmi.cif.Block,
    schema_def: SchemaDef,
    conninfo: str,
) -> LoaderResult:
    """Process a single CIF block (parse and insert).

    This is a convenience wrapper for testing that combines parsing and inserting.
    Production code uses _parse_ccmodel_cif_block + batch insert.
    """
    model_id, table_rows, error = _parse_ccmodel_cif_block(block, schema_def)

    if error:
        return LoaderResult(entry_id=model_id, success=False, error=error)

    try:
        rows_inserted = 0
        for table in schema_def.tables:
            rows = table_rows.get(table.name, [])
            if not rows:
                continue

            columns = list(rows[0].keys())
            row_tuples = [tuple(r.get(c) for c in columns) for r in rows]
            inserted, _ = bulk_upsert(
                conninfo,
                schema_def.schema_name,
                table.name,
                columns,
                row_tuples,
                table.primary_key,
            )
            rows_inserted += inserted

        return LoaderResult(
            entry_id=model_id, success=True, rows_inserted=rows_inserted
        )
    except Exception as e:
        return LoaderResult(entry_id=model_id, success=False, error=str(e))


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the ccmodel pipeline (mmJSON version)."""
    pipeline = CcmodelPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the ccmodel-cif pipeline (single CIF version)."""
    pipeline = CcmodelCifPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)
