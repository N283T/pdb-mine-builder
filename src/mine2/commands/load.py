"""Load command - bulk load data using COPY protocol."""

import importlib
import logging

import typer
from rich.console import Console

from mine2.config import Settings
from mine2.db.connection import close_pool, init_pool
from mine2.db.loader import ensure_schema, truncate_schema_tables
from mine2.db.metadata import ensure_metadata_table, update_pipeline_metadata
from mine2.models import get_metadata

console = Console()

# Pipelines supported by load command (CIF only)
LOAD_PIPELINES = ["pdbj", "cc", "ccmodel", "prd"]

# Pipeline name -> schema name
PIPELINE_SCHEMA_MAP = {
    "pdbj": "pdbj",
    "cc": "cc",
    "ccmodel": "ccmodel",
    "prd": "prd",
}


def _get_load_runner(pipeline_name: str) -> tuple[str, str]:
    """Get module name and load function for a pipeline.

    Returns:
        Tuple of (module_name, function_name)
    """
    return (pipeline_name, "run_cif_load")


def run_load(
    settings: Settings,
    pipelines: list[str],
    limit: int | None = None,
    force: bool = False,
) -> None:
    """Run bulk load pipelines (TRUNCATE + COPY).

    Args:
        settings: Application settings
        pipelines: List of pipeline names to run
        limit: Optional limit on number of entries to process
        force: Skip interactive TRUNCATE confirmation
    """
    if not pipelines:
        console.print("[red]No pipelines specified.[/red]")
        console.print(f"[dim]Available: {', '.join(LOAD_PIPELINES)}[/dim]")
        return

    invalid = [p for p in pipelines if p not in LOAD_PIPELINES]
    if invalid:
        console.print(f"[red]Invalid pipelines: {', '.join(invalid)}[/red]")
        console.print(f"[dim]Available: {', '.join(LOAD_PIPELINES)}[/dim]")
        return

    # Confirmation prompt unless --force
    if not force:
        schema_names = sorted({PIPELINE_SCHEMA_MAP[p] for p in pipelines})
        console.print(
            f"[bold red]WARNING: This will TRUNCATE all tables in: "
            f"{', '.join(schema_names)}[/bold red]"
        )
        confirm = typer.confirm("Continue?", abort=True)
        if not confirm:
            return

    console.print(f"[bold]Loading {len(pipelines)} pipeline(s)...[/bold]")

    init_pool(settings.rdb.constring, max_size=settings.rdb.get_workers() + 2)
    ensure_metadata_table(settings.rdb.constring)

    try:
        for pipeline_name in pipelines:
            console.print(f"\n[bold blue]Pipeline: {pipeline_name} (load)[/bold blue]")

            pipeline_config = settings.pipelines.get(pipeline_name)
            if not pipeline_config:
                msg = (
                    f"Pipeline {pipeline_name!r} has no configuration in "
                    f"settings.pipelines. Check config.yml."
                )
                logging.getLogger("mine2.load").warning(msg)
                console.print("  [yellow]No config found, skipping[/yellow]")
                continue

            schema_name = PIPELINE_SCHEMA_MAP[pipeline_name]
            meta = get_metadata(schema_name)
            console.print(f"  Schema: {meta.schema}")
            console.print(f"  Tables: {len(meta.tables)}")

            # Ensure schema exists
            ensure_schema(meta, settings.rdb.constring)

            # TRUNCATE all tables
            truncate_schema_tables(meta, settings.rdb.constring)

            # Import and run load pipeline
            try:
                module_name, run_func = _get_load_runner(pipeline_name)
                pipeline_module = importlib.import_module(
                    f"mine2.pipelines.{module_name}"
                )
                runner = getattr(pipeline_module, run_func)
                results = runner(settings, pipeline_config, meta, limit=limit)

                success_count = (
                    len([r for r in results if r.success]) if results else None
                )
                update_pipeline_metadata(
                    settings.rdb.constring,
                    meta.schema,
                    entries_count=success_count,
                )
            except ImportError as e:
                console.print(f"  [red]Pipeline not implemented: {e}[/red]")
            except Exception as e:
                console.print(f"  [red]Pipeline error: {e}[/red]")
                raise

    finally:
        close_pool()

    console.print("\n[bold green]Load completed![/bold green]")
