"""Chemical Component dictionary pipeline."""

import logging
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import gemmi
import psycopg
from ccd2rdmol import read_ccd_block
from rdkit import Chem
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

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import (
    Job,
    LoaderResult,
    bulk_upsert,
    get_all_tables,
    get_entry_pk,
)
from mine2.parsers.cif import parse_block
from mine2.parsers.mmjson import normalize_column_name
from mine2.pipelines.base import (
    BaseCifBatchPipeline,
    BasePipeline,
    sync_entry_tables,
    transform_category,
)

logger = logging.getLogger(__name__)
console = Console()


def _generate_canonical_smiles(block: gemmi.cif.Block) -> str | None:
    """Generate canonical SMILES from a CIF block using ccd2rdmol.

    Args:
        block: gemmi CIF block containing chemical component data

    Returns:
        Canonical SMILES string, or None if conversion failed
    """
    try:
        # Suppress RDKit C++ warnings (ring finding, hydrogen removal, etc.)
        from rdkit import RDLogger

        RDLogger.DisableLog("rdApp.*")
        try:
            result = read_ccd_block(block, sanitize_mol=True, add_conformers=False)
            if result.mol is not None:
                return Chem.MolToSmiles(result.mol, canonical=True)
        finally:
            RDLogger.EnableLog("rdApp.*")
    except Exception as e:
        logger.warning(f"SMILES generation failed for {block.name}: {e}")
    return None


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
        from mine2.models import get_metadata

        meta = get_metadata(schema_name)
        entry_pk = get_entry_pk(meta)

        data = parse_block(block)
        table_rows: dict[str, list[dict]] = {}

        # Generate canonical SMILES using ccd2rdmol
        canonical_smiles = _generate_canonical_smiles(block)

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
            from mine2.models import get_metadata

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
            canonical_smiles = _generate_canonical_smiles(block)

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
        """Find components.cif.gz file in data directory."""
        data_dir = Path(self.config.data)

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return None

        # Try direct path first
        cif_path = data_dir.joinpath("components.cif.gz")
        if cif_path.is_file():
            return cif_path

        # Handle rsync quirk where filename becomes directory
        # e.g., data/monomers/components.cif.gz/components.cif.gz
        nested_path = data_dir.joinpath("components.cif.gz", "components.cif.gz")
        if nested_path.is_file():
            return nested_path

        # Search for any components.cif.gz in data dir
        for path in data_dir.rglob("components.cif.gz"):
            if path.is_file():
                return path

        console.print(f"  [red]CIF file not found in: {data_dir}[/red]")
        return None


def _add_rdkit_descriptor_columns(cur: "psycopg.Cursor[tuple[Any, ...]]") -> None:
    """Add RDKit molecular descriptor columns to brief_summary.

    These are regular columns populated via trigger since PostgreSQL does not
    allow generated columns to reference other generated columns (mol is generated
    from canonical_smiles).

    When mol is NULL (invalid SMILES), all descriptors will also be NULL.

    SECURITY: All column definitions are hardcoded allowlists.
    DO NOT accept external input for column names, types, or functions.
    """
    # Check if table and mol column exist
    cur.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'cc' AND table_name = 'brief_summary'
        ) AND EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = 'cc'
            AND table_name = 'brief_summary'
            AND column_name = 'mol'
        )
    """)
    result = cur.fetchone()
    if not result or not result[0]:
        return  # Table or mol column doesn't exist yet

    # Hardcoded descriptors - NEVER derive from external sources
    # Format: (column_name, column_type, rdkit_function)
    descriptors = [
        ("rdkit_mw", "double precision", "mol_amw"),
        ("rdkit_logp", "double precision", "mol_logp"),
        ("rdkit_tpsa", "double precision", "mol_tpsa"),
        ("rdkit_hba", "integer", "mol_hba"),
        ("rdkit_hbd", "integer", "mol_hbd"),
        ("rdkit_rotbonds", "integer", "mol_numrotatablebonds"),
        ("rdkit_rings", "integer", "mol_numrings"),
        ("rdkit_formula", "text", "mol_formula"),
    ]

    # Add columns if they don't exist, or drop and recreate if they're generated columns
    for col_name, col_type, _ in descriptors:
        # Check if column exists and if it's a generated column
        cur.execute(
            """
            SELECT
                EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = 'cc'
                    AND table_name = 'brief_summary'
                    AND column_name = %s
                ),
                (
                    SELECT is_generated FROM information_schema.columns
                    WHERE table_schema = 'cc'
                    AND table_name = 'brief_summary'
                    AND column_name = %s
                )
        """,
            (col_name, col_name),
        )
        result = cur.fetchone()
        col_exists = result[0] if result else False
        is_generated = result[1] if result else None

        if col_exists and is_generated == "ALWAYS":
            # Column exists as generated column - drop and recreate as regular
            cur.execute(f"ALTER TABLE cc.brief_summary DROP COLUMN {col_name}")  # type: ignore[arg-type]
            col_exists = False

        if not col_exists:
            # Column doesn't exist, add it as regular column
            # Safe: col_name and col_type are from hardcoded list above
            cur.execute(
                f"ALTER TABLE cc.brief_summary ADD COLUMN {col_name} {col_type}"
            )  # type: ignore[arg-type]

    # Create or replace trigger function to compute descriptors
    cur.execute("""
        CREATE OR REPLACE FUNCTION cc.compute_rdkit_descriptors()
        RETURNS TRIGGER AS $$
        DECLARE
            mol_obj mol;
        BEGIN
            -- Only compute if mol would be valid
            IF NEW.canonical_smiles IS NOT NULL
               AND is_valid_smiles(NEW.canonical_smiles::cstring) THEN
                -- Compute mol once and reuse for all descriptors
                mol_obj := mol_from_smiles(NEW.canonical_smiles::cstring);
                NEW.rdkit_mw := mol_amw(mol_obj);
                NEW.rdkit_logp := mol_logp(mol_obj);
                NEW.rdkit_tpsa := mol_tpsa(mol_obj);
                NEW.rdkit_hba := mol_hba(mol_obj);
                NEW.rdkit_hbd := mol_hbd(mol_obj);
                NEW.rdkit_rotbonds := mol_numrotatablebonds(mol_obj);
                NEW.rdkit_rings := mol_numrings(mol_obj);
                NEW.rdkit_formula := mol_formula(mol_obj);
            ELSE
                NEW.rdkit_mw := NULL;
                NEW.rdkit_logp := NULL;
                NEW.rdkit_tpsa := NULL;
                NEW.rdkit_hba := NULL;
                NEW.rdkit_hbd := NULL;
                NEW.rdkit_rotbonds := NULL;
                NEW.rdkit_rings := NULL;
                NEW.rdkit_formula := NULL;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger if it doesn't exist
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_trigger
                WHERE tgname = 'trg_compute_rdkit_descriptors'
            ) THEN
                CREATE TRIGGER trg_compute_rdkit_descriptors
                BEFORE INSERT OR UPDATE OF canonical_smiles
                ON cc.brief_summary
                FOR EACH ROW
                EXECUTE FUNCTION cc.compute_rdkit_descriptors();
            END IF;
        END $$
    """)

    # Populate existing rows that have NULL descriptor values
    # This handles rows inserted before the trigger was created
    cur.execute("""
        UPDATE cc.brief_summary
        SET rdkit_mw = mol_amw(mol),
            rdkit_logp = mol_logp(mol),
            rdkit_tpsa = mol_tpsa(mol),
            rdkit_hba = mol_hba(mol),
            rdkit_hbd = mol_hbd(mol),
            rdkit_rotbonds = mol_numrotatablebonds(mol),
            rdkit_rings = mol_numrings(mol),
            rdkit_formula = mol_formula(mol)
        WHERE canonical_smiles IS NOT NULL
          AND mol IS NOT NULL
          AND rdkit_mw IS NULL
    """)


def _ensure_rdkit_setup(conninfo: str) -> None:
    """Ensure RDKit extension, mol column, and SQL functions exist.

    This is idempotent - safe to call on every pipeline run.
    """
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            # Create RDKit extension (database-level, requires superuser or rds_superuser)
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS rdkit")
            except psycopg.errors.InsufficientPrivilege:
                msg = (
                    "Cannot create RDKit extension (insufficient privileges). "
                    "Run 'CREATE EXTENSION rdkit' as superuser."
                )
                logger.warning(msg)
                console.print(f"  [yellow]{msg}[/yellow]")
                return

            # Add mol column if table exists but column doesn't
            cur.execute("""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = 'cc' AND table_name = 'brief_summary'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_schema = 'cc'
                        AND table_name = 'brief_summary'
                        AND column_name = 'mol'
                    ) THEN
                        ALTER TABLE cc.brief_summary
                        ADD COLUMN mol mol GENERATED ALWAYS AS (
                            CASE
                                WHEN canonical_smiles IS NOT NULL
                                     AND is_valid_smiles(canonical_smiles::cstring)
                                THEN mol_from_smiles(canonical_smiles::cstring)
                                ELSE NULL
                            END
                        ) STORED;

                        -- Create GiST index for substructure searches
                        CREATE INDEX IF NOT EXISTS brief_summary_mol_idx
                        ON cc.brief_summary USING gist(mol);
                    END IF;
                END $$
            """)

            # Add RDKit descriptor columns (regular columns populated via trigger)
            _add_rdkit_descriptor_columns(cur)

            # Load RDKit SQL functions (CREATE OR REPLACE is idempotent)
            sql_path = (
                Path(__file__).parent.parent.parent.parent
                / "scripts"
                / "rdkit_functions.sql"
            )
            if sql_path.exists():
                # Trusted SQL file from codebase - type: ignore for LiteralString
                sql_content = sql_path.read_text()
                cur.execute(sql_content)  # type: ignore[arg-type]
                logger.debug(f"Loaded RDKit functions from {sql_path}")

        conn.commit()
    console.print("  [green]RDKit setup verified[/green]")


def _process_cif_block(
    block: gemmi.cif.Block,
    schema_name: str,
    conninfo: str,
) -> LoaderResult:
    """Process a single CIF block (parse and insert).

    This is a convenience wrapper for testing that combines parsing and inserting.
    Production code uses _parse_cif_block + batch insert.
    """
    from mine2.models import get_metadata

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
    """Run the cc-cif pipeline (single CIF version)."""
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
    """Run cc pipeline in load mode (COPY, no delta sync)."""
    _ensure_rdkit_setup(settings.rdb.constring)
    pipeline = CcCifPipeline(settings, config, meta)

    cif_path = pipeline._find_cif_file()
    if not cif_path:
        return []
    console.print(f"  CIF file: {cif_path}")

    console.print("  Loading CIF...")
    doc = gemmi.cif.read(str(cif_path))
    console.print(f"  Found {len(doc)} components")

    blocks = list(doc)[:limit]
    if limit:
        console.print(f"  Processing {len(blocks)} (limited)")

    max_workers = settings.rdb.get_workers()
    conninfo = settings.rdb.constring

    console.print("[bold]Phase 1: Parsing blocks...[/bold]")
    parsed_results = pipeline._parse_all_blocks(blocks, max_workers)

    console.print("[bold]Phase 2: COPY inserting...[/bold]")
    results = pipeline._batch_copy_insert(parsed_results, conninfo)

    pipeline._print_summary(results, logger)
    return results
