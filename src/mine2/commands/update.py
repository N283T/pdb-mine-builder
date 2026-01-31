"""Update command - run database pipelines."""

import logging
from pathlib import Path

from rich.console import Console

from mine2.commands.utils import resolve_legacy_aliases
from mine2.config import Settings
from mine2.db.connection import close_pool, init_pool
from mine2.db.loader import ensure_schema, load_schema_def

console = Console()
# Default logger (no-op if not configured)
_default_logger = logging.getLogger("mine2.update")

# Available pipelines (CIF is default, -json suffix for mmJSON)
AVAILABLE_PIPELINES = [
    "pdbj",  # CIF (default)
    "pdbj-json",  # mmJSON (requires suffix)
    "cc",  # CIF (default)
    "cc-json",  # mmJSON (requires suffix)
    "ccmodel",  # CIF (default)
    "ccmodel-json",  # mmJSON (requires suffix)
    "prd",  # CIF (default)
    "prd-json",  # mmJSON (requires suffix)
    "vrpt",
    "contacts",
    "sifts",  # SIFTS cross-references (TTL)
    "emdb",  # EMDB (XML)
    "ihm",  # IHM (mmJSON)
]

# Legacy aliases for backward compatibility (deprecated)
LEGACY_ALIASES = {
    "pdbj-cif": "pdbj",
    "cc-cif": "cc",
    "ccmodel-cif": "ccmodel",
    "prd-cif": "prd",
}


def run_update(
    settings: Settings,
    pipelines: list[str],
    limit: int | None = None,
    tables: list[str] | None = None,
    chunk_size: int | None = None,
    logger: logging.Logger | None = None,
) -> None:
    """Run database update pipelines.

    Args:
        settings: Application settings
        pipelines: List of pipeline names to run (empty = all)
        limit: Optional limit on number of entries to process per pipeline
        tables: Optional list of tables for SIFTS pipeline (default: all)
        chunk_size: Optional chunk size for batch insert (pdbj, contacts, vrpt)
        logger: Optional logger for file output
    """
    if logger is None:
        logger = _default_logger
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
        logger.error(f"Invalid pipelines: {invalid}")
        return

    console.print(f"[bold]Running {len(pipelines)} pipeline(s)...[/bold]")
    logger.info(f"Running pipelines: {pipelines}")

    # Initialize connection pool
    init_pool(settings.rdb.constring, max_size=settings.rdb.get_workers() + 2)

    try:
        for pipeline_name in pipelines:
            console.print(f"\n[bold blue]Pipeline: {pipeline_name}[/bold blue]")
            logger.info(f"Starting pipeline: {pipeline_name}")

            pipeline_config = settings.pipelines.get(pipeline_name)
            if not pipeline_config:
                console.print("  [yellow]No config found, skipping[/yellow]")
                logger.warning(f"Pipeline {pipeline_name}: no config found, skipping")
                continue

            # Load schema definition
            deffile = Path(pipeline_config.deffile)
            if not deffile.exists():
                console.print(f"  [red]Schema file not found: {deffile}[/red]")
                logger.error(
                    f"Pipeline {pipeline_name}: schema file not found: {deffile}"
                )
                continue

            schema_def = load_schema_def(deffile)
            console.print(f"  Schema: {schema_def.schema_name}")
            console.print(f"  Tables: {len(schema_def.tables)}")

            # Ensure schema exists
            ensure_schema(schema_def, settings.rdb.constring)

            # Import and run pipeline
            try:
                module_name, run_func = _get_pipeline_runner(pipeline_name)
                pipeline_module = _import_pipeline(module_name)
                runner = getattr(pipeline_module, run_func)

                # Build kwargs based on pipeline type
                kwargs: dict = {"limit": limit, "logger": logger}

                # SIFTS pipeline accepts tables parameter
                if pipeline_name == "sifts" and tables:
                    kwargs["tables"] = tables

                # File-based pipelines accept chunk_size parameter
                if pipeline_name in ("pdbj", "contacts", "vrpt") and chunk_size:
                    kwargs["chunk_size"] = chunk_size

                runner(settings, pipeline_config, schema_def, **kwargs)
                logger.info(f"Pipeline {pipeline_name}: completed successfully")
            except ImportError as e:
                console.print(f"  [red]Pipeline not implemented: {e}[/red]")
                logger.error(f"Pipeline {pipeline_name}: not implemented - {e}")
            except Exception as e:
                console.print(f"  [red]Pipeline error: {e}[/red]")
                logger.exception(f"Pipeline {pipeline_name}: error - {e}")
                raise

    finally:
        close_pool()

    console.print("\n[bold green]Update completed![/bold green]")


def _get_pipeline_runner(pipeline_name: str) -> tuple[str, str]:
    """Get module name and run function for a pipeline.

    Returns:
        Tuple of (module_name, function_name)
    """
    # mmJSON pipelines require -json suffix, dispatch to run()
    json_pipelines = {
        "pdbj-json": ("pdbj", "run"),
        "cc-json": ("cc", "run"),
        "ccmodel-json": ("ccmodel", "run"),
        "prd-json": ("prd", "run"),
    }
    if pipeline_name in json_pipelines:
        return json_pipelines[pipeline_name]

    # Base names now use CIF (run_cif) as default
    cif_defaults = {"pdbj", "cc", "ccmodel", "prd"}
    if pipeline_name in cif_defaults:
        return (pipeline_name, "run_cif")

    # Other pipelines (vrpt, contacts) use their standard run()
    return (pipeline_name, "run")


def _import_pipeline(name: str):
    """Dynamically import a pipeline module."""
    import importlib

    return importlib.import_module(f"mine2.pipelines.{name}")
