"""CLI interface using typer + rich."""

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
            help="Sync targets: pdbj, cc, ccmodel, prd, vrpt, contacts, schemas, dictionaries"
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
        typer.Argument(help="Pipelines to run: pdbj, cc, ccmodel, prd, vrpt, contacts"),
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
) -> None:
    """Run database update pipelines."""
    from mine2.commands.update import run_update

    settings = load_config(config)
    if workers is not None:
        settings.rdb.nworkers = workers
    run_update(settings, pipelines or [], limit=limit)


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


if __name__ == "__main__":
    app()
