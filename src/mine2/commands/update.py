"""Update command - run database pipelines."""

import logging

from rich.console import Console

from mine2.commands.utils import resolve_legacy_aliases
from mine2.config import PipelineConfig, Settings
from mine2.db.connection import close_pool, init_pool
from mine2.db.loader import ensure_schema
from mine2.db.metadata import ensure_metadata_table, update_pipeline_metadata
from mine2.models import get_metadata

console = Console()

# Available pipelines (format selected via config, not pipeline name)
AVAILABLE_PIPELINES = [
    "pdbj",
    "cc",
    "ccmodel",
    "prd",
    "vrpt",
    "contacts",
    "sifts",
    "emdb",
    "ihm",
]

# Legacy aliases for backward compatibility (deprecated)
LEGACY_ALIASES = {
    "pdbj-cif": "pdbj",
    "cc-cif": "cc",
    "ccmodel-cif": "ccmodel",
    "prd-cif": "prd",
    "pdbj-json": "pdbj",
    "cc-json": "cc",
    "ccmodel-json": "ccmodel",
    "prd-json": "prd",
}

# Pipeline name -> schema name mapping
PIPELINE_SCHEMA_MAP = {
    "pdbj": "pdbj",
    "cc": "cc",
    "ccmodel": "ccmodel",
    "prd": "prd",
    "vrpt": "vrpt",
    "contacts": "contacts",
    "sifts": "sifts",
    "emdb": "emdb",
    "ihm": "ihm",
}

# Pipelines that support dual format (CIF and mmJSON)
DUAL_FORMAT_PIPELINES = {"pdbj", "cc", "ccmodel", "prd"}


def _get_schema_name(pipeline_name: str) -> str:
    """Resolve pipeline name to database schema name.

    Args:
        pipeline_name: One of the AVAILABLE_PIPELINES names.

    Returns:
        The corresponding schema name.

    Raises:
        KeyError: If the pipeline name has no schema mapping.
    """
    try:
        return PIPELINE_SCHEMA_MAP[pipeline_name]
    except KeyError:
        available = ", ".join(sorted(PIPELINE_SCHEMA_MAP))
        msg = f"Pipeline {pipeline_name!r} has no entry in PIPELINE_SCHEMA_MAP. Available: {available}"
        raise KeyError(msg) from None


def run_update(
    settings: Settings,
    pipelines: list[str],
    limit: int | None = None,
    tables: list[str] | None = None,
) -> None:
    """Run database update pipelines.

    Args:
        settings: Application settings
        pipelines: List of pipeline names to run (empty = all)
        limit: Optional limit on number of entries to process per pipeline
        tables: Optional list of tables for SIFTS pipeline (default: all)
    """
    # If no pipelines specified, run all
    if not pipelines:
        pipelines = AVAILABLE_PIPELINES

    # Resolve legacy aliases with deprecation warnings
    pipelines = resolve_legacy_aliases(pipelines, LEGACY_ALIASES, "Pipeline")

    # Validate pipelines
    invalid = [p for p in pipelines if p not in AVAILABLE_PIPELINES]
    if invalid:
        console.print(f"[red]Invalid pipelines: {', '.join(invalid)}[/red]")
        console.print(f"[dim]Available: {', '.join(AVAILABLE_PIPELINES)}[/dim]")
        return

    console.print(f"[bold]Running {len(pipelines)} pipeline(s)...[/bold]")

    # Initialize connection pool
    init_pool(settings.rdb.constring, max_size=settings.rdb.get_workers() + 2)

    # Ensure metadata table exists
    ensure_metadata_table(settings.rdb.constring)

    try:
        for pipeline_name in pipelines:
            console.print(f"\n[bold blue]Pipeline: {pipeline_name}[/bold blue]")

            pipeline_config = settings.pipelines.get(pipeline_name)
            if not pipeline_config:
                msg = (
                    f"Pipeline {pipeline_name!r} has no configuration in "
                    f"settings.pipelines. Check config.yml."
                )
                logging.getLogger("mine2.update").warning(msg)
                console.print("  [yellow]No config found, skipping[/yellow]")
                continue

            # Get MetaData from SQLAlchemy models
            schema_name = _get_schema_name(pipeline_name)
            meta = get_metadata(schema_name)
            console.print(f"  Schema: {meta.schema}")
            console.print(f"  Tables: {len(meta.tables)}")

            # Ensure schema exists
            ensure_schema(meta, settings.rdb.constring)

            # Import and run pipeline
            try:
                module_name, run_func = _get_pipeline_runner(
                    pipeline_name, pipeline_config
                )
                pipeline_module = _import_pipeline(module_name)
                runner = getattr(pipeline_module, run_func)
                # SIFTS pipeline accepts tables parameter
                if pipeline_name == "sifts" and tables:
                    results = runner(
                        settings,
                        pipeline_config,
                        meta,
                        limit=limit,
                        tables=tables,
                    )
                else:
                    results = runner(settings, pipeline_config, meta, limit=limit)

                # Update pipeline metadata with timestamp
                success_count = (
                    sum(1 for r in results if r.success) if results else None
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

    console.print("\n[bold green]Update completed![/bold green]")


def _get_pipeline_runner(pipeline_name: str, config: PipelineConfig) -> tuple[str, str]:
    """Get module name and run function for a pipeline.

    For dual-format pipelines (pdbj, cc, ccmodel, prd), the format is read
    from the pipeline config to determine the run function:
      - format=cif    -> run_cif()
      - format=mmjson -> run()

    Other pipelines always use run().

    Returns:
        Tuple of (module_name, function_name)
    """
    if pipeline_name in DUAL_FORMAT_PIPELINES:
        if config.format == "mmjson":
            return (pipeline_name, "run")
        return (pipeline_name, "run_cif")

    # Other pipelines (vrpt, contacts, sifts, emdb, ihm) use run()
    return (pipeline_name, "run")


def _import_pipeline(name: str):
    """Dynamically import a pipeline module."""
    import importlib

    return importlib.import_module(f"mine2.pipelines.{name}")
