"""Chemical Component dictionary pipeline."""

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
from sqlalchemy import MetaData, Table

from pdbminebuilder.config import PipelineConfig, Settings
from pdbminebuilder.db.loader import (
    Job,
    LoaderResult,
    bulk_copy_entry,
    bulk_upsert,
    get_all_tables,
    get_entry_pk,
    run_loader,
)
from pdbminebuilder.parsers.cif import parse_block
from pdbminebuilder.parsers.mmjson import normalize_column_name
from pdbminebuilder.pipelines.base import (
    BaseCifBatchPipeline,
    BasePipeline,
    sync_entry_tables,
    transform_category,
)
from pdbminebuilder.pipelines.rdkit_utils import (
    ensure_rdkit_setup,
    generate_canonical_smiles,
)

logger = logging.getLogger(__name__)
console = Console()


def _read_mmjson_block(filepath: Path) -> gemmi.cif.Block | None:
    """Read mmJSON file and return the first gemmi Block.

    gemmi can read mmJSON files and convert them to CIF-like structures,
    allowing us to use ccd2rdmol for SMILES generation.

    Args:
        filepath: Path to mmJSON file (.json or .json.gz)

    Returns:
        gemmi.cif.Block, or None if file is empty
    """
    doc = gemmi.cif.read_mmjson(str(filepath))
    if len(doc) == 0:
        return None
    return doc[0]


def _extract_descriptors_by_type(data: dict[str, Any], target_type: str) -> list[str]:
    """Extract descriptors of a specific type from pdbx_chem_comp_descriptor."""
    descriptors = data.get("pdbx_chem_comp_descriptor", [])
    results = []
    for desc in descriptors:
        desc_type = desc.get("type", "")
        if target_type.lower() in desc_type.lower():
            value = desc.get("descriptor")
            if value:
                results.append(value)
    return results


def _generate_brief_summary(
    data: dict[str, Any], comp_id: str, canonical_smiles: str | None
) -> dict[str, Any]:
    """Generate brief_summary row from mmJSON data.

    This is a derived table aggregating data from chem_comp,
    pdbx_chem_comp_descriptor, pdbx_chem_comp_identifier, etc.
    """
    # Get chem_comp data (first row)
    chem_comp = data.get("chem_comp", [{}])
    cc = chem_comp[0] if chem_comp else {}

    # Get release date from audit
    release_date = None
    audits = data.get("pdbx_chem_comp_audit", [])
    for audit in audits:
        if audit.get("action_type") == "Initial release":
            release_date = audit.get("date")
            break

    # Get identifier
    identifiers = data.get("pdbx_chem_comp_identifier", [])
    identifier = identifiers[0].get("identifier") if identifiers else None

    # Extract SMILES and InChI arrays
    smiles_list = _extract_descriptors_by_type(data, "smiles")
    inchi_list = _extract_descriptors_by_type(data, "inchi")

    # Parse synonyms into array
    synonyms_str = cc.get("pdbx_synonyms")
    pdbx_synonyms = [s.strip() for s in synonyms_str.split(";")] if synonyms_str else []

    return {
        "comp_id": comp_id,
        "pdbx_initial_date": cc.get("pdbx_initial_date"),
        "release_date": release_date,
        "pdbx_modified_date": cc.get("pdbx_modified_date"),
        "update_date": None,
        "name": cc.get("name"),
        "formula": cc.get("formula"),
        "pdbx_synonyms": pdbx_synonyms if pdbx_synonyms else None,
        "identifier": identifier,
        "smiles": smiles_list if smiles_list else None,
        "inchi": inchi_list if inchi_list else None,
        "canonical_smiles": canonical_smiles,
        "keywords": None,
    }


# =============================================================================
# Worker function for parallel CIF processing (must be at module level)
# =============================================================================


def _parse_cif_block(
    block: gemmi.cif.Block,
    schema_name: str,
) -> tuple[str, dict[str, list[dict]], str | None]:
    """Parse a single CIF block (worker function for parallel processing).

    Args:
        block: gemmi CIF block
        schema_name: Schema name for model lookup

    Returns:
        Tuple of (comp_id, table_rows_dict, error_message or None)
        table_rows_dict maps table_name -> list of row dicts
    """
    comp_id = block.name
    try:
        from pdbminebuilder.models import get_metadata

        meta = get_metadata(schema_name)
        entry_pk = get_entry_pk(meta)

        data = parse_block(block)
        table_rows: dict[str, list[dict]] = {}

        # Generate canonical SMILES using ccd2rdmol
        canonical_smiles = generate_canonical_smiles(block)

        for table in get_all_tables(meta):
            # brief_summary is a derived table, generate it
            if table.name == "brief_summary":
                brief_row = _generate_brief_summary(data, comp_id, canonical_smiles)
                category_rows = [brief_row]
            else:
                rows = data.get(table.name, [])
                # CIF uses plain column names, no normalization needed
                category_rows = transform_category(rows, table, comp_id, entry_pk, None)

            if category_rows:
                table_rows[table.name] = category_rows

        return (comp_id, table_rows, None)

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return (comp_id, {}, error_msg)


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
        schema_name: str,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single chemical component."""
        try:
            from pdbminebuilder.models import get_metadata

            meta = get_metadata(schema_name)
            entry_pk = get_entry_pk(meta)

            # Read mmJSON as gemmi block for ccd2rdmol SMILES generation
            block = _read_mmjson_block(job.filepath)
            if block is None:
                return LoaderResult(
                    entry_id=job.entry_id,
                    success=False,
                    error="Empty mmJSON file",
                )

            # Parse block data for database insertion
            data = parse_block(block)
            table_rows: dict[str, list[dict[str, Any]]] = {}

            # Generate canonical SMILES using ccd2rdmol (same as CIF pipeline)
            # This is more reliable than extracting SMILES from CCD data
            canonical_smiles = generate_canonical_smiles(block)

            # Load all tables from schema
            for table in get_all_tables(meta):
                # brief_summary is a derived table, generate it
                if table.name == "brief_summary":
                    brief_row = _generate_brief_summary(
                        data, job.entry_id, canonical_smiles
                    )
                    category_rows = [brief_row]
                else:
                    category_rows = self._transform_category(
                        data, table, job.entry_id, entry_pk
                    )

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

    def _transform_category(
        self,
        data: dict[str, Any],
        table: Table,
        comp_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, comp_id, pk_col, normalize_column_name)


class CcCifPipeline(BaseCifBatchPipeline):
    """Pipeline for loading Chemical Components from single CIF file.

    Uses components.cif.gz which contains all components in one file.
    Each data block represents one component.

    Uses batch processing: all blocks are parsed first (in parallel),
    then all rows are inserted in a single bulk operation per table.
    This is much faster than inserting per-block (40k round-trips -> ~10).
    """

    name = "cc-cif"

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
        console.print(f"  Found {total_blocks} components")

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
        schema_name = self.meta.schema
        if len(blocks) <= 10 or max_workers == 1:
            # Sequential parsing
            results = []
            for block in track(blocks, description="Parsing...", console=console):
                result = _parse_cif_block(block, schema_name)
                results.append(result)
            return results

        # Parallel parsing
        results: list[tuple[str, dict[str, list[dict]], str | None]] = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_parse_cif_block, block, schema_name): block.name
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
                    comp_id = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append((comp_id, {}, f"{e}\n{traceback.format_exc()}"))
                    progress.advance(task)

        return results

    def _find_cif_file(self) -> Path | None:
        """Find components.cif.gz file.

        Config data can be a file path or directory path.
        """
        data_path = Path(self.config.data)

        # If config points directly to the file
        if data_path.is_file():
            return data_path

        # Otherwise treat as directory and search
        if not data_path.exists():
            console.print(f"  [red]Data path not found: {data_path}[/red]")
            return None

        cif_path = data_path.joinpath("components.cif.gz")
        if cif_path.is_file():
            return cif_path

        for path in data_path.rglob("components.cif.gz"):
            if path.is_file():
                return path

        console.print(f"  [red]components.cif.gz not found in: {data_path}[/red]")
        return None


def _ensure_rdkit_setup(conninfo: str) -> None:
    """Ensure RDKit extension, mol column, and SQL functions exist for cc schema.

    Delegates to shared ensure_rdkit_setup. Kept as wrapper for backward compatibility
    with CLI and tests.
    """
    sql_path = (
        Path(__file__).parent.parent.parent.parent / "scripts" / "rdkit_functions.sql"
    )
    ensure_rdkit_setup(
        conninfo,
        schema="cc",
        sql_functions_path=sql_path if sql_path.exists() else None,
    )


def _process_cif_block(
    block: gemmi.cif.Block,
    schema_name: str,
    conninfo: str,
) -> LoaderResult:
    """Process a single CIF block (parse and insert).

    This is a convenience wrapper for testing that combines parsing and inserting.
    Production code uses _parse_cif_block + batch insert.
    """
    from pdbminebuilder.models import get_metadata

    meta = get_metadata(schema_name)
    entry_pk = get_entry_pk(meta)

    comp_id, table_rows, error = _parse_cif_block(block, schema_name)

    if error:
        return LoaderResult(entry_id=comp_id, success=False, error=error)

    try:
        rows_inserted = 0
        for table in get_all_tables(meta):
            rows = table_rows.get(table.name, [])
            if not rows:
                continue

            # Collect all unique columns across all rows
            all_columns: set[str] = set()
            for row in rows:
                all_columns.update(row.keys())

            columns = [entry_pk] + sorted(c for c in all_columns if c != entry_pk)
            row_tuples = [tuple(r.get(c) for c in columns) for r in rows]

            pk_cols_for_table = [c.name for c in table.primary_key.columns]
            inserted, _ = bulk_upsert(
                conninfo,
                meta.schema,
                table.name,
                columns,
                row_tuples,
                pk_cols_for_table,
            )
            rows_inserted += inserted

        return LoaderResult(entry_id=comp_id, success=True, rows_inserted=rows_inserted)
    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        return LoaderResult(entry_id=comp_id, success=False, error=error_msg)


def run(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the cc pipeline (mmJSON version)."""
    _ensure_rdkit_setup(settings.rdb.constring)
    pipeline = CcPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the cc pipeline in CIF mode (single-file batch)."""
    _ensure_rdkit_setup(settings.rdb.constring)
    pipeline = CcCifPipeline(settings, config, meta)
    return pipeline.run(limit, logger=logger)


def run_cif_load(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run cc pipeline in load mode (COPY, no delta sync) - CIF version."""
    _ensure_rdkit_setup(settings.rdb.constring)
    pipeline = CcCifPipeline(settings, config, meta)
    return pipeline.run_load(limit, logger=logger)


def _process_cc_mmjson_load(
    job: Job,
    schema_name: str,
    conninfo: str,
) -> LoaderResult:
    """Worker: parse cc mmJSON -> transform -> bulk_copy_entry (no delta sync)."""
    try:
        from pdbminebuilder.models import get_metadata

        meta = get_metadata(schema_name)
        entry_pk = get_entry_pk(meta)

        block = _read_mmjson_block(job.filepath)
        if block is None:
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error="Empty mmJSON file",
            )

        data = parse_block(block)
        table_rows: dict[str, list[dict[str, Any]]] = {}

        canonical_smiles = generate_canonical_smiles(block)

        for table in get_all_tables(meta):
            if table.name == "brief_summary":
                brief_row = _generate_brief_summary(
                    data, job.entry_id, canonical_smiles
                )
                category_rows = [brief_row]
            else:
                rows = data.get(table.name, [])
                category_rows = transform_category(
                    rows, table, job.entry_id, entry_pk, normalize_column_name
                )

            if category_rows:
                table_rows[table.name] = category_rows

        inserted = bulk_copy_entry(
            conninfo=conninfo,
            schema=meta.schema,
            entry_id=job.entry_id,
            pk_column=entry_pk,
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


def run_load(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run cc pipeline in load mode (COPY, no delta sync) - mmJSON version."""
    _ensure_rdkit_setup(settings.rdb.constring)
    pipeline = CcPipeline(settings, config, meta)
    jobs = pipeline.find_jobs(limit)

    if not jobs:
        console.print("  [yellow]No files to process[/yellow]")
        return []

    console.print(f"  Found {len(jobs)} entries")

    results = run_loader(
        settings=settings,
        schema_name=meta.schema,
        jobs=jobs,
        process_func=_process_cc_mmjson_load,
        max_workers=settings.rdb.get_workers(),
        logger=logger,
    )

    return results
