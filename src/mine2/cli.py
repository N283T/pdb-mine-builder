"""CLI interface using typer + rich."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from mine2 import __version__
from mine2.config import load_config

app = typer.Typer(
    name="mine2",
    help="MINE2 Updater - PDBj data synchronization and database loading tool.",
    rich_markup_mode="rich",
)
console = Console()


def setup_logging(log_file: Path | None, verbose: bool = False) -> logging.Logger:
    """Configure logging with optional file output.

    Args:
        log_file: Path to log file (None for no file logging)
        verbose: If True, set DEBUG level; otherwise INFO

    Returns:
        Configured logger
    """
    logger = logging.getLogger("mine2")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler (only warnings and errors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        )
        logger.addHandler(file_handler)
        console.print(f"[dim]Logging to: {log_file}[/dim]")

    return logger


def version_callback(value: bool) -> None:
    if value:
        console.print(f"mine2 version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """MINE2 Updater - PDBj data synchronization and database loading tool."""
    pass


@app.command()
def sync(
    targets: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="Sync targets: pdbj (CIF), pdbj-json (mmJSON), cc, cc-json, ccmodel, ccmodel-json, prd, prd-json, vrpt, contacts, sifts, schemas"
        ),
    ] = None,
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.yml"),
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run", "-n", help="Show what would be synced without actually syncing"
        ),
    ] = False,
) -> None:
    """Synchronize data from PDBj via rsync."""
    from mine2.commands.sync import run_sync

    settings = load_config(config)
    run_sync(settings, targets or [], dry_run=dry_run)


@app.command()
def update(
    pipelines: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="Pipelines: pdbj (CIF), pdbj-json (mmJSON), cc, cc-json, ccmodel, ccmodel-json, prd, prd-json, vrpt, contacts, sifts, emdb (XML), ihm (mmJSON)"
        ),
    ] = None,
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.yml"),
    limit: Annotated[
        Optional[int],
        typer.Option("--limit", "-l", help="Limit number of entries to process"),
    ] = None,
    workers: Annotated[
        Optional[int],
        typer.Option(
            "--workers", "-w", help="Number of worker processes (overrides config)"
        ),
    ] = None,
    tables: Annotated[
        Optional[list[str]],
        typer.Option(
            "--tables",
            "-t",
            help="SIFTS only: tables to load (e.g., pdb_pfam,pdb_uniprot). Default: all",
        ),
    ] = None,
    log: Annotated[
        Optional[Path],
        typer.Option(
            "--log",
            help="Log file path (default: logs/<pipeline>_YYYYMMDD_HHMMSS.log)",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose (DEBUG) logging"),
    ] = False,
) -> None:
    """Run database update pipelines."""
    from mine2.commands.update import run_update

    # Setup logging with pipeline name in filename
    if log is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if pipelines and len(pipelines) == 1:
            # Single pipeline: use pipeline name
            log_name = pipelines[0].replace("-", "_")
        elif pipelines:
            # Multiple pipelines: use "multi"
            log_name = "multi"
        else:
            # All pipelines
            log_name = "all"
        log = Path(f"logs/{log_name}_{timestamp}.log")
    logger = setup_logging(log, verbose)

    settings = load_config(config)
    if workers is not None:
        settings.rdb.nworkers = workers

    logger.info(f"Starting update: pipelines={pipelines or 'all'}, limit={limit}")
    run_update(settings, pipelines or [], limit=limit, tables=tables)
    logger.info("Update completed")


@app.command(name="all")
def run_all(
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.yml"),
) -> None:
    """Run full sync and update cycle."""
    from mine2.commands.sync import run_sync
    from mine2.commands.update import run_update

    settings = load_config(config)
    console.print("[bold blue]Starting full sync and update cycle...[/bold blue]")

    console.print("\n[bold]Phase 1: Sync[/bold]")
    run_sync(settings, [], dry_run=False)

    console.print("\n[bold]Phase 2: Update[/bold]")
    run_update(settings, [])

    console.print("\n[bold green]Full cycle completed![/bold green]")


@app.command(name="setup-rdkit")
def setup_rdkit(
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.yml"),
) -> None:
    """Setup RDKit extension and SQL functions.

    Creates RDKit extension, mol column on cc.brief_summary,
    and loads chemical search functions (similar_compounds, substructure_search, etc.).

    This is automatically run by cc/cc-json pipelines, but can be run
    independently to add functions to an existing database.
    """
    from mine2.pipelines.cc import _ensure_rdkit_setup

    settings = load_config(config)
    console.print("[bold]Setting up RDKit extension and functions...[/bold]")
    _ensure_rdkit_setup(settings.rdb.constring)
    console.print("[bold green]RDKit setup completed![/bold green]")


@app.command()
def test(
    pipelines: Annotated[
        Optional[list[str]],
        typer.Argument(help="Pipelines to test"),
    ] = None,
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.test.yml"),
    drop: Annotated[
        bool,
        typer.Option("--drop", "-d", help="Drop existing test database"),
    ] = False,
    limit: Annotated[
        int,
        typer.Option("--limit", "-l", help="Limit number of files to process"),
    ] = 10,
    workers: Annotated[
        Optional[int],
        typer.Option(
            "--workers", "-w", help="Number of worker processes (overrides config)"
        ),
    ] = None,
) -> None:
    """Create test database and validate pipelines."""
    from mine2.commands.test import run_test

    settings = load_config(config)
    if workers is not None:
        settings.rdb.nworkers = workers
    run_test(settings, pipelines or [], drop=drop, limit=limit)


@app.command()
def reset(
    schemas: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="Schemas to reset: pdbj, cc, ccmodel, prd, vrpt, contacts, sifts, emdb, ihm (or 'all')"
        ),
    ] = None,
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.yml"),
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Skip confirmation prompt"),
    ] = False,
) -> None:
    """Drop and reset database schemas (for testing/reloading).

    Examples:
        mine2 reset cc          # Reset cc schema only
        mine2 reset cc pdbj     # Reset cc and pdbj schemas
        mine2 reset all         # Reset ALL schemas (dangerous!)
        mine2 reset all -f      # Reset all without confirmation
    """
    from mine2.commands.reset import run_reset

    settings = load_config(config)
    run_reset(settings, schemas or [], force=force)


@app.command()
def stats(
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Config file path"),
    ] = Path("config.yml"),
) -> None:
    """Show database statistics.

    Displays table counts, row counts, and last update timestamps
    for each schema in the database.
    """
    from mine2.commands.stats import run_stats

    settings = load_config(config)
    run_stats(settings)


if __name__ == "__main__":
    app()
