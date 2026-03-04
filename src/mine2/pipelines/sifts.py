"""SIFTS pipeline - Structure Integration with Function, Taxonomy and Sequences.

SIFTS provides cross-references from PDB to external databases:
- Pfam, InterPro, GO, EC numbers
- UniProt, Taxonomy
- CATH, SCOP
- PubMed

Data format: RDF Turtle (.ttl.gz) files with simple triples.
"""

import gzip
import logging
import re
import traceback
from pathlib import Path
from typing import Iterator

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from sqlalchemy import MetaData

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import LoaderResult, bulk_insert, bulk_upsert

console = Console()

# TTL file to table mapping with parsing configuration
TTL_FILES = {
    "pdb_chain_pfam.ttl.gz": {
        "table": "pdb_pfam",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso pfam:(PF\d+)",
        "columns": ["pdbid", "entity_id", "pfam_id"],
        "pk": ["pdbid", "entity_id", "pfam_id"],
    },
    "pdb_chain_interpro.ttl.gz": {
        "table": "pdb_interpro",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso ipr:(IPR\d+)",
        "columns": ["pdbid", "entity_id", "interpro_id"],
        "pk": ["pdbid", "entity_id", "interpro_id"],
    },
    "pdb_chain_go.ttl.gz": {
        "table": "pdb_go",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso GO:(\d+)",
        "columns": ["pdbid", "entity_id", "go_id"],
        "pk": ["pdbid", "entity_id", "go_id"],
    },
    "pdb_chain_enzyme.ttl.gz": {
        "table": "pdb_enzyme",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso <http://identifiers\.org/ec-code/([\d\.\-]+)>",
        "columns": ["pdbid", "entity_id", "ec_number"],
        "pk": ["pdbid", "entity_id", "ec_number"],
    },
    "pdb_chain_taxonomy.ttl.gz": {
        "table": "pdb_taxonomy",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso tax:(\d+)",
        "columns": ["pdbid", "entity_id", "taxonomy_id"],
        "pk": ["pdbid", "entity_id", "taxonomy_id"],
    },
    "pdb_chain_uniprot_short.ttl.gz": {
        "table": "pdb_uniprot_short",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity_poly/(\d+)> rdfs:seeAlso up:(\w+)",
        "columns": ["pdbid", "entity_id", "uniprot_id"],
        "pk": ["pdbid", "entity_id", "uniprot_id"],
    },
    "pdb_chain_uniprot.ttl.gz": {
        "table": "pdb_uniprot",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity_poly/(\d+)#(\d+),(\d+)> sifts:region_match <https://purl\.uniprot\.org/uniprot/(\w+)#(\d+),(\d+)>",
        "columns": [
            "pdbid",
            "entity_id",
            "pdb_start",
            "pdb_end",
            "uniprot_id",
            "uniprot_start",
            "uniprot_end",
        ],
        "pk": ["pdbid", "entity_id", "pdb_start", "pdb_end", "uniprot_id"],
    },
    "pdb_chain_cath_uniprot.ttl.gz": {
        "table": "pdb_cath",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso cath:(\w+)",
        "columns": ["pdbid", "entity_id", "cath_id"],
        "pk": ["pdbid", "entity_id", "cath_id"],
    },
    "pdb_chain_scop_uniprot.ttl.gz": {
        "table": "pdb_scop",
        "pattern": r"<https://rdf\.wwpdb\.org/pdb/(\w+)/entity/(\d+)> rdfs:seeAlso scop:(\d+)",
        "columns": ["pdbid", "entity_id", "scop_id"],
        "pk": ["pdbid", "entity_id", "scop_id"],
    },
    "pdb_pubmed.ttl.gz": {
        "table": "pdb_pubmed",
        "pattern": r"pdbr:(\w+) dcterms:references pubmed:(\d+)",
        "columns": ["pdbid", "pubmed_id"],
        "pk": ["pdbid", "pubmed_id"],
    },
}


_INT_COLUMNS = frozenset(
    {
        "entity_id",
        "taxonomy_id",
        "pubmed_id",
        "pdb_start",
        "pdb_end",
        "uniprot_start",
        "uniprot_end",
    }
)


def parse_ttl_file(filepath: Path, pattern: str) -> Iterator[tuple]:
    """Parse TTL file and yield matching tuples.

    Args:
        filepath: Path to .ttl.gz file
        pattern: Regex pattern to extract values

    Yields:
        Tuples of extracted values
    """
    regex = re.compile(pattern)

    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line in f:
            match = regex.search(line)
            if match:
                yield match.groups()


def _convert_ttl_rows(
    filepath: Path,
    config: dict,
    batch_size: int = 10000,
) -> Iterator[list[tuple]]:
    """Parse TTL file and yield batches of type-converted rows.

    Shared by load_ttl_file (upsert) and load_ttl_file_copy (insert).

    Yields:
        Lists of converted row tuples, each up to batch_size rows.
    """
    pattern = config["pattern"]
    columns = config["columns"]

    batch: list[tuple] = []
    for row in parse_ttl_file(filepath, pattern):
        converted = []
        for col, val in zip(columns, row):
            if col in _INT_COLUMNS:
                converted.append(int(val))
            elif col == "pdbid":
                converted.append(val.lower())
            else:
                converted.append(val)
        batch.append(tuple(converted))

        if len(batch) >= batch_size:
            yield batch
            batch = []

    if batch:
        yield batch


def load_ttl_file(
    filepath: Path,
    config: dict,
    schema_name: str,
    conninfo: str,
    batch_size: int = 10000,
) -> tuple[int, int]:
    """Load a TTL file into database table.

    Args:
        filepath: Path to .ttl.gz file
        config: TTL file configuration (table, pattern, columns, pk)
        schema_name: Database schema name
        conninfo: Database connection string
        batch_size: Number of rows per batch insert

    Returns:
        Tuple of (rows_inserted, rows_updated)
    """
    table = config["table"]
    columns = config["columns"]
    pk = config["pk"]

    total_inserted = 0
    total_updated = 0

    for batch in _convert_ttl_rows(filepath, config, batch_size):
        inserted, updated = bulk_upsert(
            conninfo, schema_name, table, columns, batch, pk
        )
        total_inserted += inserted
        total_updated += updated

    return total_inserted, total_updated


def run(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    tables: list[str] | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the SIFTS pipeline.

    Processes TTL files and loads cross-reference data into database.

    Args:
        settings: Application settings
        config: Pipeline configuration
        meta: SQLAlchemy MetaData instance
        limit: Not used (SIFTS processes all data)
        tables: Optional list of table names to process (default: all)
        logger: Optional logger for file output

    Returns:
        List of LoaderResult for each TTL file processed
    """
    # SIFTS has its own processing loop, logger is accepted but not heavily used
    results: list[LoaderResult] = []
    data_dir = Path(config.data)

    if not data_dir.exists():
        console.print(f"  [red]Data directory not found: {data_dir}[/red]")
        return results

    # Filter TTL files by table names if specified
    if tables:
        table_set = set(tables)
        files_to_process = {
            f: c for f, c in TTL_FILES.items() if c["table"] in table_set
        }
        if not files_to_process:
            available = [c["table"] for c in TTL_FILES.values()]
            console.print(
                f"  [red]No matching tables. Available: {', '.join(available)}[/red]"
            )
            return results
    else:
        files_to_process = TTL_FILES

    console.print(f"  Data directory: {data_dir}")
    console.print(f"  Processing {len(files_to_process)} TTL files...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for filename, ttl_config in files_to_process.items():
            filepath = data_dir / filename
            table = ttl_config["table"]

            task = progress.add_task(f"  Loading {table}...", total=None)

            if not filepath.exists():
                progress.update(
                    task, description=f"  [yellow]⚠[/yellow] {table} (file not found)"
                )
                results.append(
                    LoaderResult(
                        entry_id=filename,
                        success=False,
                        error=f"File not found: {filepath}",
                    )
                )
                continue

            try:
                inserted, updated = load_ttl_file(
                    filepath,
                    ttl_config,
                    meta.schema,
                    settings.rdb.constring,
                )
                progress.update(
                    task,
                    description=f"  [green]✓[/green] {table}: {inserted:,} inserted, {updated:,} updated",
                )
                results.append(
                    LoaderResult(
                        entry_id=filename,
                        success=True,
                        rows_inserted=inserted + updated,
                    )
                )
            except Exception as e:
                error_msg = f"{e}\n{traceback.format_exc()}"
                progress.update(task, description=f"  [red]✗[/red] {table}: {e}")
                results.append(
                    LoaderResult(
                        entry_id=filename,
                        success=False,
                        error=error_msg,
                    )
                )

    # Summary
    success_count = sum(1 for r in results if r.success)
    total_rows = sum(r.rows_inserted for r in results if r.success)
    console.print(
        f"\n  [bold]Summary:[/bold] {success_count}/{len(results)} files, {total_rows:,} total rows"
    )

    return results


# =============================================================================
# Load mode (COPY protocol via bulk_insert, no upsert)
# =============================================================================


def load_ttl_file_copy(
    filepath: Path,
    config: dict,
    schema_name: str,
    conninfo: str,
    batch_size: int = 10000,
) -> int:
    """Load a TTL file using bulk_insert (COPY) instead of bulk_upsert.

    Same parsing as load_ttl_file but uses COPY for initial load performance.

    Args:
        filepath: Path to .ttl.gz file
        config: TTL file configuration (table, pattern, columns)
        schema_name: Database schema name
        conninfo: Database connection string
        batch_size: Number of rows per batch insert

    Returns:
        Total rows inserted
    """
    table = config["table"]
    columns = config["columns"]

    total_inserted = 0
    for batch in _convert_ttl_rows(filepath, config, batch_size):
        total_inserted += bulk_insert(conninfo, schema_name, table, columns, batch)

    return total_inserted


def run_cif_load(
    settings: Settings,
    config: PipelineConfig,
    meta: MetaData,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run SIFTS pipeline in load mode (COPY, no upsert).

    Args:
        settings: Application settings
        config: Pipeline configuration
        meta: SQLAlchemy MetaData instance
        limit: Not used (SIFTS processes all data)
        logger: Optional logger for file output

    Returns:
        List of LoaderResult for each TTL file processed
    """
    results: list[LoaderResult] = []
    data_dir = Path(config.data)

    if not data_dir.exists():
        console.print(f"  [red]Data directory not found: {data_dir}[/red]")
        return results

    console.print(f"  Data directory: {data_dir}")
    console.print(f"  Processing {len(TTL_FILES)} TTL files (load mode)...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for filename, ttl_config in TTL_FILES.items():
            filepath = data_dir / filename
            table = ttl_config["table"]

            task = progress.add_task(f"  Loading {table}...", total=None)

            if not filepath.exists():
                progress.update(
                    task, description=f"  [yellow]⚠[/yellow] {table} (file not found)"
                )
                results.append(
                    LoaderResult(
                        entry_id=filename,
                        success=False,
                        error=f"File not found: {filepath}",
                    )
                )
                continue

            try:
                inserted = load_ttl_file_copy(
                    filepath,
                    ttl_config,
                    meta.schema,
                    settings.rdb.constring,
                )
                progress.update(
                    task,
                    description=f"  [green]✓[/green] {table}: {inserted:,} inserted",
                )
                results.append(
                    LoaderResult(
                        entry_id=filename,
                        success=True,
                        rows_inserted=inserted,
                    )
                )
            except Exception as e:
                error_msg = f"{e}\n{traceback.format_exc()}"
                progress.update(task, description=f"  [red]✗[/red] {table}: {e}")
                results.append(
                    LoaderResult(
                        entry_id=filename,
                        success=False,
                        error=error_msg,
                    )
                )

    # Summary
    success_count = sum(1 for r in results if r.success)
    total_rows = sum(r.rows_inserted for r in results if r.success)
    console.print(
        f"\n  [bold]Summary:[/bold] {success_count}/{len(results)} files, {total_rows:,} total rows"
    )

    return results
