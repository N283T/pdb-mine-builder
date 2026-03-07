"""Load command - bulk load data using COPY protocol."""

import importlib
from typing import Any, Callable

import typer
from rich.console import Console

from pdbminebuilder.commands.update import DUAL_FORMAT_PIPELINES, LEGACY_ALIASES
from pdbminebuilder.commands.utils import resolve_legacy_aliases
from pdbminebuilder.config import Settings
from pdbminebuilder.db.connection import close_pool, init_pool
from pdbminebuilder.db.loader import LoaderResult, ensure_schema, truncate_schema_tables
from pdbminebuilder.db.metadata import (
    ensure_entry_metadata_table,
    ensure_metadata_table,
    update_pipeline_metadata,
)
from pdbminebuilder.models import get_metadata

console = Console()

# Pipelines supported by load command.
# Each pipeline module must expose run_cif_load() for CIF format.
# Dual-format pipelines (DUAL_FORMAT_PIPELINES) must also expose
# run_load() for mmJSON format.
LOAD_PIPELINES = ["pdbj", "cc", "ccmodel", "prd", "prd_family", "vrpt", "contacts"]


def _get_load_runner(
    pipeline_name: str, settings: Settings
) -> Callable[..., list[LoaderResult]]:
    """Get the load runner function for a pipeline.

    For dual-format pipelines, reads format from config:
      - format=cif    -> run_cif_load()
      - format=mmjson -> run_load()

    Other pipelines always use run_cif_load().

    Returns:
        Callable with signature (settings, config, meta, limit=...) -> list[LoaderResult]

    Raises:
        RuntimeError: If the pipeline module cannot be imported or the
            required load function is missing.
    """
    try:
        pipeline_module = importlib.import_module(
            f"pdbminebuilder.pipelines.{pipeline_name}"
        )
    except ImportError as e:
        raise RuntimeError(
            f"Failed to import pipeline module 'pdbminebuilder.pipelines.{pipeline_name}': {e}. "
            f"Check that all required dependencies are installed."
        ) from e

    if pipeline_name in DUAL_FORMAT_PIPELINES:
        pipeline_config = settings.pipelines.get(pipeline_name)
        if pipeline_config and pipeline_config.format == "mmjson":
            runner = getattr(pipeline_module, "run_load", None)
            if runner is None:
                raise RuntimeError(
                    f"Pipeline '{pipeline_name}' does not support mmJSON load mode "
                    f"(missing run_load in pdbminebuilder.pipelines.{pipeline_name}). "
                    f"Set format='cif' in config.yml or implement run_load()."
                )
            return runner

    runner = getattr(pipeline_module, "run_cif_load", None)
    if runner is None:
        raise RuntimeError(
            f"Pipeline '{pipeline_name}' does not support load mode "
            f"(missing run_cif_load in pdbminebuilder.pipelines.{pipeline_name})."
        )
    return runner


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

    # Resolve legacy aliases with deprecation warnings
    pipelines = resolve_legacy_aliases(pipelines, LEGACY_ALIASES, "Pipeline")

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

        runner = _get_load_runner(pipeline_name, settings)
        meta = get_metadata(pipeline_name)
        pipeline_runners.append((pipeline_name, pipeline_config, meta, runner))

    init_pool(settings.rdb.constring, max_size=settings.rdb.get_workers() + 2)
    ensure_metadata_table(settings.rdb.constring)
    ensure_entry_metadata_table(settings.rdb.constring)

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
