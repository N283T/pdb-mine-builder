"""Update command - run database pipelines."""

from pathlib import Path

from rich.console import Console

from mine2.config import Settings
from mine2.db.connection import close_pool, init_pool
from mine2.db.loader import ensure_schema, load_schema_def

console = Console()

# Available pipelines
AVAILABLE_PIPELINES = [
    "pdbj",
    "pdbj-cif",
    "cc",
    "cc-cif",
    "ccmodel",
    "ccmodel-cif",
    "prd",
    "prd-cif",
    "vrpt",
    "contacts",
]


def run_update(
    settings: Settings, pipelines: list[str], limit: int | None = None
) -> None:
    """Run database update pipelines.

    Args:
        settings: Application settings
        pipelines: List of pipeline names to run (empty = all)
        limit: Optional limit on number of entries to process per pipeline
    """
    # If no pipelines specified, run all
    if not pipelines:
        pipelines = AVAILABLE_PIPELINES

    # Validate pipelines
    invalid = [p for p in pipelines if p not in AVAILABLE_PIPELINES]
    if invalid:
        console.print(f"[red]Invalid pipelines: {', '.join(invalid)}[/red]")
        console.print(f"[dim]Available: {', '.join(AVAILABLE_PIPELINES)}[/dim]")
        return

    console.print(f"[bold]Running {len(pipelines)} pipeline(s)...[/bold]")

    # Initialize connection pool
    init_pool(settings.rdb.constring, max_size=settings.rdb.nworkers + 2)

    try:
        for pipeline_name in pipelines:
            console.print(f"\n[bold blue]Pipeline: {pipeline_name}[/bold blue]")

            pipeline_config = settings.pipelines.get(pipeline_name)
            if not pipeline_config:
                console.print("  [yellow]No config found, skipping[/yellow]")
                continue

            # Load schema definition
            deffile = Path(pipeline_config.deffile)
            if not deffile.exists():
                console.print(f"  [red]Schema file not found: {deffile}[/red]")
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
                runner(settings, pipeline_config, schema_def, limit=limit)
            except ImportError as e:
                console.print(f"  [red]Pipeline not implemented: {e}[/red]")
            except Exception as e:
                console.print(f"  [red]Pipeline error: {e}[/red]")
                raise

    finally:
        close_pool()

    console.print("\n[bold green]Update completed![/bold green]")


def _get_pipeline_runner(pipeline_name: str) -> tuple[str, str]:
    """Get module name and run function for a pipeline.

    Returns:
        Tuple of (module_name, function_name)
    """
    # Special cases where pipeline name differs from module
    special_cases = {
        "pdbj-cif": ("pdbj", "run_cif"),
        "cc-cif": ("cc", "run_cif"),
        "ccmodel-cif": ("ccmodel", "run_cif"),
        "prd-cif": ("prd", "run_cif"),
    }
    if pipeline_name in special_cases:
        return special_cases[pipeline_name]
    return (pipeline_name, "run")


def _import_pipeline(name: str):
    """Dynamically import a pipeline module."""
    import importlib

    return importlib.import_module(f"mine2.pipelines.{name}")
