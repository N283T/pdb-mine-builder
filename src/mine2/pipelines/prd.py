"""PRD (BIRD) pipeline - Biologically Interesting Reference Dictionary."""

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
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.cif import parse_block, parse_mmjson_file_blocks
from mine2.parsers.mmjson import normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()

# Tables that come from the PRDCC data block (used by both pipelines)
PRDCC_TABLES = {
    "chem_comp",
    "chem_comp_atom",
    "chem_comp_bond",
    "pdbx_chem_comp_descriptor",
    "pdbx_chem_comp_identifier",
}


# =============================================================================
# Worker function for parallel CIF processing (must be at module level)
# =============================================================================


def _process_prd_cif_block(
    prd_block: gemmi.cif.Block,
    prdcc_block: gemmi.cif.Block | None,
    schema_def: SchemaDef,
    conninfo: str,
) -> LoaderResult:
    """Process a single PRD block with its corresponding PRDCC block.

    Args:
        prd_block: PRD CIF block
        prdcc_block: Corresponding PRDCC block (may be None)
        schema_def: Schema definition
        conninfo: Database connection string

    Returns:
        LoaderResult for the processed block
    """
    prd_id = prd_block.name  # e.g., PRD_000001

    try:
        # Parse block data
        prd_data = parse_block(prd_block)
        prdcc_data = parse_block(prdcc_block) if prdcc_block else {}

        rows_inserted = 0

        # Generate and load brief_summary
        brief_rows = _generate_brief_summary_prd(prd_data, prd_id)
        if brief_rows:
            columns = list(brief_rows[0].keys())
            inserted, _ = bulk_upsert(
                conninfo,
                schema_def.schema_name,
                "brief_summary",
                columns,
                [tuple(r[c] for c in columns) for r in brief_rows],
                ["prd_id"],
            )
            rows_inserted += inserted

        # Load other tables
        for table in schema_def.tables:
            if table.name == "brief_summary":
                continue

            # Determine which data block to use
            if table.name in PRDCC_TABLES:
                data = prdcc_data
            else:
                data = prd_data

            rows = data.get(table.name, [])
            # CIF uses plain column names, no normalization needed
            category_rows = transform_category(
                rows, table, prd_id, schema_def.primary_key, None
            )
            if category_rows:
                columns = list(category_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    table.name,
                    columns,
                    [tuple(r[c] for c in columns) for r in category_rows],
                    table.primary_key,
                )
                rows_inserted += inserted

        return LoaderResult(
            entry_id=prd_id,
            success=True,
            rows_inserted=rows_inserted,
        )

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return LoaderResult(
            entry_id=prd_id,
            success=False,
            error=error_msg,
        )


def _generate_brief_summary_prd(data: dict[str, Any], prd_id: str) -> list[dict]:
    """Generate brief_summary from pdbx_reference_molecule data."""
    rows = data.get("pdbx_reference_molecule", [])
    if not rows:
        return []

    result = []
    for row in rows:
        result.append(
            {
                "prd_id": prd_id,
                "name": row.get("name"),
                "formula": row.get("formula"),
                "description": row.get("description"),
            }
        )
    return result


class PrdPipeline(BasePipeline):
    """Pipeline for loading BIRD (PRD) data.

    PRD files contain TWO data blocks:
    - data_PRD_XXXXXX: Contains pdbx_reference_* categories
    - data_PRDCC_XXXXXX: Contains chem_comp_* categories
    """

    name = "prd"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract PRD ID from filename.

        Handles filenames like: PRD_000001.json.gz -> PRD_000001
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
        """Process a single PRD entry."""
        try:
            # Load all data blocks (PRD files have two: PRD and PRDCC)
            all_blocks = parse_mmjson_file_blocks(job.filepath)

            rows_inserted = 0

            # PRD files have two data blocks:
            # - PRD_XXXXXX (pdbx_reference_* categories)
            # - PRDCC_XXXXXX (chem_comp_* categories)
            prd_data = all_blocks.get(job.entry_id, {})
            prdcc_id = job.entry_id.replace("PRD_", "PRDCC_")
            prdcc_data = all_blocks.get(prdcc_id, {})

            # Generate and load brief_summary from pdbx_reference_molecule
            brief_rows = self._generate_brief_summary(prd_data, job.entry_id)
            if brief_rows:
                columns = list(brief_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "brief_summary",
                    columns,
                    [tuple(r[c] for c in columns) for r in brief_rows],
                    ["prd_id"],
                )
                rows_inserted += inserted

            # Load all tables from schema
            for table in schema_def.tables:
                if table.name == "brief_summary":
                    continue  # Already handled

                # Determine which data block to use
                if table.name in PRDCC_TABLES:
                    data = prdcc_data
                else:
                    data = prd_data

                category_rows = self._transform_category(
                    data, table, job.entry_id, schema_def.primary_key
                )
                if category_rows:
                    columns = list(category_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        schema_def.schema_name,
                        table.name,
                        columns,
                        [tuple(r[c] for c in columns) for r in category_rows],
                        table.primary_key,
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

    def _generate_brief_summary(self, data: dict[str, Any], prd_id: str) -> list[dict]:
        """Generate brief_summary from pdbx_reference_molecule data."""
        rows = data.get("pdbx_reference_molecule", [])
        if not rows:
            return []

        result = []
        for row in rows:
            result.append(
                {
                    "prd_id": prd_id,
                    "name": row.get("name"),
                    "formula": row.get("formula"),
                    "description": row.get("description"),
                }
            )
        return result

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        prd_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, prd_id, pk_col, normalize_column_name)


class PrdCifPipeline:
    """Pipeline for loading PRD data from CIF files.

    Uses prd-all.cif.gz and prdcc-all.cif.gz which contain all entries.
    Each data block represents one PRD/PRDCC entry.
    """

    name = "prd-cif"

    def __init__(
        self,
        settings: Settings,
        config: PipelineConfig,
        schema_def: SchemaDef,
    ):
        self.settings = settings
        self.config = config
        self.schema_def = schema_def

    def run(
        self, limit: int | None = None, logger: logging.Logger | None = None
    ) -> list[LoaderResult]:
        """Run the pipeline."""
        prd_path, prdcc_path = self._find_cif_files()
        if not prd_path:
            return []
        console.print(f"  PRD CIF: {prd_path}")
        if prdcc_path:
            console.print(f"  PRDCC CIF: {prdcc_path}")
        else:
            console.print(
                "  [yellow]PRDCC CIF not found, skipping PRDCC tables[/yellow]"
            )

        # Load both CIF files
        console.print("  Loading CIF files...")
        prd_doc = gemmi.cif.read(str(prd_path))
        console.print(f"  Found {len(prd_doc)} PRD entries")

        # Build PRDCC lookup
        prdcc_lookup: dict[str, gemmi.cif.Block] = {}
        if prdcc_path:
            prdcc_doc = gemmi.cif.read(str(prdcc_path))
            for block in prdcc_doc:
                prdcc_lookup[block.name] = block
            console.print(f"  Found {len(prdcc_lookup)} PRDCC entries")

        # Build block pairs (prd_block, prdcc_block_or_none)
        block_pairs: list[tuple[gemmi.cif.Block, gemmi.cif.Block | None]] = []
        for prd_block in prd_doc:
            prdcc_id = prd_block.name.replace("PRD_", "PRDCC_")
            prdcc_block = prdcc_lookup.get(prdcc_id)
            block_pairs.append((prd_block, prdcc_block))

        if limit:
            block_pairs = block_pairs[:limit]
            console.print(f"  Processing {len(block_pairs)} (limited)")

        max_workers = self.settings.rdb.get_workers()
        conninfo = self.settings.rdb.constring

        # Process sequentially or in parallel
        if len(block_pairs) <= 10 or max_workers == 1:
            results = self._run_sequential(block_pairs, conninfo)
        else:
            results = self._run_parallel(block_pairs, max_workers, conninfo)

        self._print_summary(results, logger)
        return results

    def _run_sequential(
        self,
        block_pairs: list[tuple[gemmi.cif.Block, gemmi.cif.Block | None]],
        conninfo: str,
    ) -> list[LoaderResult]:
        """Run sequentially."""
        results: list[LoaderResult] = []
        for prd_block, prdcc_block in track(
            block_pairs, description="Processing...", console=console
        ):
            result = _process_prd_cif_block(
                prd_block, prdcc_block, self.schema_def, conninfo
            )
            results.append(result)
        return results

    def _run_parallel(
        self,
        block_pairs: list[tuple[gemmi.cif.Block, gemmi.cif.Block | None]],
        max_workers: int,
        conninfo: str,
    ) -> list[LoaderResult]:
        """Run with parallel processing."""
        console.print(
            f"[bold]Processing {len(block_pairs)} PRD entries "
            f"with {max_workers} workers...[/bold]"
        )

        results: list[LoaderResult] = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _process_prd_cif_block,
                    prd_block,
                    prdcc_block,
                    self.schema_def,
                    conninfo,
                ): prd_block.name
                for prd_block, prdcc_block in block_pairs
            }

            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Processing", total=len(futures))

                for future in as_completed(futures):
                    prd_id = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append(
                            LoaderResult(
                                entry_id=prd_id,
                                success=False,
                                error=str(e),
                            )
                        )
                    progress.advance(task)

        return results

    def _find_cif_files(self) -> tuple[Path | None, Path | None]:
        """Find prd-all.cif.gz and prdcc-all.cif.gz files."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return None, None

        # Find PRD file
        prd_path = self._find_file(data_dir, "prd-all.cif.gz")
        if not prd_path:
            console.print(f"  [red]prd-all.cif.gz not found in: {data_dir}[/red]")
            return None, None

        # Find PRDCC file (optional)
        prdcc_path = self._find_file(data_dir, "prdcc-all.cif.gz")

        return prd_path, prdcc_path

    def _find_file(self, data_dir: Path, filename: str) -> Path | None:
        """Find a CIF file, handling rsync quirks."""
        # Try direct path
        direct_path = data_dir.joinpath(filename)
        if direct_path.is_file():
            return direct_path

        # Handle rsync quirk (filename becomes directory)
        nested_path = data_dir.joinpath(filename, filename)
        if nested_path.is_file():
            return nested_path

        # Search recursively
        for path in data_dir.rglob(filename):
            if path.is_file():
                return path

        return None

    def _print_summary(
        self, results: list[LoaderResult], logger: logging.Logger | None = None
    ) -> None:
        """Print processing summary."""
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count

        if logger:
            logger.info(f"Completed: {success_count} succeeded, {fail_count} failed")

        console.print(f"\n[green]✓ {success_count} succeeded[/green]", end="")
        if fail_count > 0:
            console.print(f", [red]✗ {fail_count} failed[/red]")
            shown = 0
            for r in results:
                if not r.success and r.error:
                    if shown < 5:
                        error_line = r.error.split("\n")[0][:100]
                        console.print(f"  [dim]{r.entry_id}: {error_line}[/dim]")
                        shown += 1
                    if logger:
                        logger.error(f"FAILED {r.entry_id}:\n{r.error}")
            if fail_count > 5:
                console.print(
                    f"  [dim]... and {fail_count - 5} more (see log file)[/dim]"
                )
        else:
            console.print()


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the prd pipeline (mmJSON version)."""
    pipeline = PrdPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the prd-cif pipeline (CIF version)."""
    pipeline = PrdCifPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)
