"""Chemical Component dictionary pipeline."""

import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import gemmi
from ccd2rdmol import read_ccd_block
from rdkit import Chem
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


def _generate_canonical_smiles(block: gemmi.cif.Block) -> str | None:
    """Generate canonical SMILES from a CIF block using ccd2rdmol.

    Args:
        block: gemmi CIF block containing chemical component data

    Returns:
        Canonical SMILES string, or None if conversion failed
    """
    try:
        result = read_ccd_block(block, sanitize_mol=True, add_conformers=False)
        if result.mol is not None:
            return Chem.MolToSmiles(result.mol, canonical=True)
    except Exception:
        pass
    return None


def _canonicalize_smiles(smiles: str | None) -> str | None:
    """Canonicalize a SMILES string using RDKit.

    Args:
        smiles: Input SMILES string

    Returns:
        Canonical SMILES string, or None if invalid
    """
    if not smiles:
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            return Chem.MolToSmiles(mol, canonical=True)
    except Exception:
        pass
    return None


def _extract_smiles_from_mmjson(data: dict[str, Any]) -> str | None:
    """Extract SMILES from mmJSON pdbx_chem_comp_descriptor.

    Looks for SMILES or SMILES_CANONICAL type descriptors.

    Args:
        data: Parsed mmJSON data

    Returns:
        SMILES string, or None if not found
    """
    descriptors = data.get("pdbx_chem_comp_descriptor", [])
    for desc in descriptors:
        desc_type = desc.get("type", "")
        if "SMILES" in desc_type.upper():
            smiles = desc.get("descriptor")
            if smiles:
                return smiles
    return None


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


def _process_cif_block(
    block: gemmi.cif.Block,
    schema_def: SchemaDef,
    conninfo: str,
) -> LoaderResult:
    """Process a single CIF block (worker function for parallel processing).

    Args:
        block: gemmi CIF block
        schema_def: Schema definition
        conninfo: Database connection string

    Returns:
        LoaderResult for the processed block
    """
    comp_id = block.name
    try:
        data = parse_block(block)
        rows_inserted = 0

        # Generate canonical SMILES using ccd2rdmol
        canonical_smiles = _generate_canonical_smiles(block)

        for table in schema_def.tables:
            # brief_summary is a derived table, generate it
            if table.name == "brief_summary":
                brief_row = _generate_brief_summary(data, comp_id, canonical_smiles)
                category_rows = [brief_row]
            else:
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

            # Extract and canonicalize SMILES from mmJSON
            raw_smiles = _extract_smiles_from_mmjson(data)
            canonical_smiles = _canonicalize_smiles(raw_smiles)

            # Load all tables from schema
            for table in schema_def.tables:
                # brief_summary is a derived table, generate it
                if table.name == "brief_summary":
                    brief_row = _generate_brief_summary(
                        data, job.entry_id, canonical_smiles
                    )
                    category_rows = [brief_row]
                else:
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
        """Run the pipeline."""
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
        blocks = list(doc) if not limit else list(doc)[:limit]
        if limit:
            console.print(f"  Processing {len(blocks)} (limited)")

        # Process sequentially or in parallel
        if len(blocks) <= 10 or max_workers == 1:
            results = self._run_sequential(blocks, conninfo)
        else:
            results = self._run_parallel(blocks, max_workers, conninfo)

        self._print_summary(results)
        return results

    def _run_sequential(
        self,
        blocks: list[gemmi.cif.Block],
        conninfo: str,
    ) -> list[LoaderResult]:
        """Run sequentially."""
        results: list[LoaderResult] = []
        for block in tqdm(blocks, desc="Processing"):
            result = _process_cif_block(block, self.schema_def, conninfo)
            results.append(result)
        return results

    def _run_parallel(
        self,
        blocks: list[gemmi.cif.Block],
        max_workers: int,
        conninfo: str,
    ) -> list[LoaderResult]:
        """Run with parallel processing."""
        console.print(
            f"[bold]Processing {len(blocks)} components "
            f"with {max_workers} workers...[/bold]"
        )

        results: list[LoaderResult] = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _process_cif_block, block, self.schema_def, conninfo
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
                task = progress.add_task("Processing", total=len(futures))

                for future in as_completed(futures):
                    comp_id = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append(
                            LoaderResult(
                                entry_id=comp_id,
                                success=False,
                                error=str(e),
                            )
                        )
                    progress.advance(task)

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
