"""Load command - bulk load data using COPY protocol."""

import importlib
from typing import Any

import typer
from rich.console import Console

from mine2.config import Settings
from mine2.db.connection import close_pool, init_pool
from mine2.db.loader import ensure_schema, truncate_schema_tables
from mine2.db.metadata import ensure_metadata_table, update_pipeline_metadata
from mine2.models import get_metadata

console = Console()

# Pipelines supported by load command (CIF only).
# For these pipelines, schema name matches pipeline name.
LOAD_PIPELINES = ["pdbj", "cc", "ccmodel", "prd"]


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
        schema_names = sorted(set(pipelines))
        console.print(
            f"[bold red]WARNING: This will TRUNCATE all tables in: "
            f"{', '.join(schema_names)}[/bold red]"
        )
        typer.confirm("Continue?", abort=True)

    console.print(f"[bold]Loading {len(pipelines)} pipeline(s)...[/bold]")

    # Pre-flight: verify all pipelines are importable and configured
    # BEFORE truncating any data.
    pipeline_runners: list[tuple[str, Any, Any, Any]] = []

    for pipeline_name in pipelines:
        pipeline_config = settings.pipelines.get(pipeline_name)
        if not pipeline_config:
            msg = (
                f"Pipeline {pipeline_name!r} has no configuration in "
                f"settings.pipelines. Check config.yml."
            )
            raise RuntimeError(msg)

        pipeline_module = importlib.import_module(f"mine2.pipelines.{pipeline_name}")
        runner = getattr(pipeline_module, "run_cif_load")
        meta = get_metadata(pipeline_name)
        pipeline_runners.append((pipeline_name, pipeline_config, meta, runner))

    init_pool(settings.rdb.constring, max_size=settings.rdb.get_workers() + 2)
    ensure_metadata_table(settings.rdb.constring)

    try:
        for pipeline_name, pipeline_config, meta, runner in pipeline_runners:
            console.print(f"\n[bold blue]Pipeline: {pipeline_name} (load)[/bold blue]")
            console.print(f"  Schema: {meta.schema}")
            console.print(f"  Tables: {len(meta.tables)}")

            # Ensure schema exists
            ensure_schema(meta, settings.rdb.constring)

            # TRUNCATE all tables
            truncate_schema_tables(meta, settings.rdb.constring)

            # Run load pipeline
            results = runner(settings, pipeline_config, meta, limit=limit)

            success_count = sum(1 for r in results if r.success) if results else None
            update_pipeline_metadata(
                settings.rdb.constring,
                meta.schema,
                entries_count=success_count,
            )

    finally:
        close_pool()

    console.print("\n[bold green]Load completed![/bold green]")
