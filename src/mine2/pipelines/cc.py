"""Chemical Component dictionary pipeline."""

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
)
from tqdm import tqdm

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.cif import parse_block, parse_mmjson_file
from mine2.parsers.mmjson import normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


# =============================================================================
# Worker function for parallel CIF processing (must be at module level)
# =============================================================================


def _process_cif_chunk(
    cif_path: str,
    start_idx: int,
    end_idx: int,
    schema_def: SchemaDef,
    conninfo: str,
) -> list[LoaderResult]:
    """Process a chunk of blocks from the CIF file.

    This function runs in a worker process. It reads the CIF file and processes
    blocks from start_idx to end_idx (exclusive).

    Args:
        cif_path: Path to the CIF file
        start_idx: Starting block index (inclusive)
        end_idx: Ending block index (exclusive)
        schema_def: Schema definition
        conninfo: Database connection string

    Returns:
        List of LoaderResults for each processed block
    """
    doc = gemmi.cif.read(cif_path)
    results = []

    for i in range(start_idx, end_idx):
        block = doc[i]
        comp_id = block.name
        try:
            data = parse_block(block)
            rows_inserted = 0

            for table in schema_def.tables:
                rows = data.get(table.name, [])
                # CIF uses plain column names, no normalization needed
                category_rows = transform_category(
                    rows, table, comp_id, schema_def.primary_key, None
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

            results.append(
                LoaderResult(
                    entry_id=comp_id,
                    success=True,
                    rows_inserted=rows_inserted,
                )
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            results.append(
                LoaderResult(
                    entry_id=comp_id,
                    success=False,
                    error=error_msg,
                )
            )

    return results


class CcPipeline(BasePipeline):
    """Pipeline for loading Chemical Component dictionary data."""

    name = "cc"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract component ID from filename.

        Handles filenames like: ATP.json.gz -> ATP
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
        """Process a single chemical component."""
        try:
            data = parse_mmjson_file(job.filepath)
            rows_inserted = 0

            # Load all tables from schema
            for table in schema_def.tables:
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

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        comp_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, comp_id, pk_col, normalize_column_name)


class CcCifPipeline:
    """Pipeline for loading Chemical Components from single CIF file.

    Uses components.cif.gz which contains all components in one file.
    Each data block represents one component.
    """

    name = "cc-cif"

    def __init__(
        self,
        settings: Settings,
        config: PipelineConfig,
        schema_def: SchemaDef,
    ):
        self.settings = settings
        self.config = config
        self.schema_def = schema_def

    def run(self, limit: int | None = None) -> list[LoaderResult]:
        """Run the pipeline with parallel processing."""
        cif_path = self._find_cif_file()
        if not cif_path:
            return []
        console.print(f"  CIF file: {cif_path}")

        # Get block count without full parse (gemmi reads lazily for count)
        console.print("  Counting components...")
        doc = gemmi.cif.read(str(cif_path))
        total_blocks = len(doc)
        del doc  # Release memory, workers will re-read
        console.print(f"  Found {total_blocks} components")

        if limit:
            total_blocks = min(total_blocks, limit)
            console.print(f"  Processing {total_blocks} (limited)")

        max_workers = self.settings.rdb.nworkers
        conninfo = self.settings.rdb.constring

        # For small counts, process sequentially
        if total_blocks <= 10 or max_workers == 1:
            return self._run_sequential(cif_path, total_blocks, conninfo)

        return self._run_parallel(cif_path, total_blocks, max_workers, conninfo)

    def _run_sequential(
        self,
        cif_path: Path,
        total_blocks: int,
        conninfo: str,
    ) -> list[LoaderResult]:
        """Run sequentially for small datasets."""
        doc = gemmi.cif.read(str(cif_path))
        results: list[LoaderResult] = []

        for i in tqdm(range(total_blocks), desc="Processing"):
            block = doc[i]
            result = self._process_block(block, conninfo)
            results.append(result)

        self._print_summary(results)
        return results

    def _run_parallel(
        self,
        cif_path: Path,
        total_blocks: int,
        max_workers: int,
        conninfo: str,
    ) -> list[LoaderResult]:
        """Run with parallel processing using chunks."""
        # Calculate chunk size (each worker gets roughly equal work)
        chunk_size = max(100, total_blocks // max_workers)
        chunks = []
        for start in range(0, total_blocks, chunk_size):
            end = min(start + chunk_size, total_blocks)
            chunks.append((start, end))

        console.print(
            f"[bold]Processing {total_blocks} components "
            f"with {max_workers} workers ({len(chunks)} chunks)...[/bold]"
        )

        results: list[LoaderResult] = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_chunk = {
                executor.submit(
                    _process_cif_chunk,
                    str(cif_path),
                    start,
                    end,
                    self.schema_def,
                    conninfo,
                ): (start, end)
                for start, end in chunks
            }

            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Processing", total=len(chunks))

                for future in as_completed(future_to_chunk):
                    chunk = future_to_chunk[future]
                    try:
                        chunk_results = future.result()
                        results.extend(chunk_results)
                    except Exception as e:
                        # If entire chunk failed, create error results
                        start, end = chunk
                        for i in range(start, end):
                            results.append(
                                LoaderResult(
                                    entry_id=f"block_{i}",
                                    success=False,
                                    error=str(e),
                                )
                            )
                    progress.advance(task)

        self._print_summary(results)
        return results

    def _print_summary(self, results: list[LoaderResult]) -> None:
        """Print processing summary."""
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count

        console.print(f"\n[green]✓ {success_count} succeeded[/green]", end="")
        if fail_count > 0:
            console.print(f", [red]✗ {fail_count} failed[/red]")
            for r in results[:5]:
                if not r.success and r.error:
                    console.print(f"  [dim]{r.entry_id}: {r.error}[/dim]")
        else:
            console.print()

    def _find_cif_file(self) -> Path | None:
        """Find components.cif.gz file in data directory."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return None

        # Try direct path first
        cif_path = data_dir / "components.cif.gz"
        if cif_path.is_file():
            return cif_path

        # Handle rsync quirk where filename becomes directory
        # e.g., data/monomers/components.cif.gz/components.cif.gz
        nested_path = data_dir / "components.cif.gz" / "components.cif.gz"
        if nested_path.is_file():
            return nested_path

        # Search for any components.cif.gz in data dir
        for path in data_dir.rglob("components.cif.gz"):
            if path.is_file():
                return path

        console.print(f"  [red]CIF file not found in: {data_dir}[/red]")
        return None

    def _process_block(
        self,
        block: gemmi.cif.Block,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single component block."""
        comp_id = block.name
        try:
            data = parse_block(block)
            rows_inserted = 0

            for table in self.schema_def.tables:
                category_rows = self._transform_category(
                    data, table, comp_id, self.schema_def.primary_key
                )
                if category_rows:
                    columns = list(category_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        self.schema_def.schema_name,
                        table.name,
                        columns,
                        [tuple(r[c] for c in columns) for r in category_rows],
                        table.primary_key,
                    )
                    rows_inserted += inserted

            return LoaderResult(
                entry_id=comp_id,
                success=True,
                rows_inserted=rows_inserted,
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=comp_id,
                success=False,
                error=error_msg,
            )

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        comp_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        # CIF uses plain column names, no bracket notation like mmJSON
        return transform_category(rows, table, comp_id, pk_col, None)


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the cc pipeline (mmJSON version)."""
    pipeline = CcPipeline(settings, config, schema_def)
    return pipeline.run(limit)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the cc-cif pipeline (single CIF version)."""
    pipeline = CcCifPipeline(settings, config, schema_def)
    return pipeline.run(limit)
