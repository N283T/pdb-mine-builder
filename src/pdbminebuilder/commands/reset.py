"""Reset command - drop and reset database schemas."""

import psycopg
from rich.console import Console
from rich.prompt import Confirm

from pdbminebuilder.config import Settings

console = Console()

# Known schemas that can be reset
KNOWN_SCHEMAS = [
    "pdbj",
    "cc",
    "ccmodel",
    "prd",
    "prd_family",
    "vrpt",
    "contacts",
    "emdb",
    "ihm",
]


def run_reset(
    settings: Settings,
    schemas: list[str],
    force: bool = False,
) -> None:
    """Drop specified schemas from the database.

    Args:
        settings: Application settings
        schemas: List of schema names to drop, or ["all"] for all schemas
        force: Skip confirmation prompt
    """
    if not schemas:
        console.print("[yellow]No schemas specified. Available schemas:[/yellow]")
        console.print(f"  {', '.join(KNOWN_SCHEMAS)}")
        console.print("\nUsage:")
        console.print("  pmb reset cc          # Reset cc schema")
        console.print("  pmb reset cc pdbj     # Reset multiple schemas")
        console.print("  pmb reset all         # Reset ALL schemas")
        return

    # Handle 'all' keyword
    if "all" in schemas:
        target_schemas = KNOWN_SCHEMAS.copy()
    else:
        # Validate schema names
        invalid = [s for s in schemas if s not in KNOWN_SCHEMAS]
        if invalid:
            console.print(f"[red]Unknown schema(s): {', '.join(invalid)}[/red]")
            console.print(f"[yellow]Valid schemas: {', '.join(KNOWN_SCHEMAS)}[/yellow]")
            return
        target_schemas = schemas

    # Show what will be dropped
    console.print(
        "\n[bold red]WARNING: This will DROP the following schemas:[/bold red]"
    )
    for schema in target_schemas:
        console.print(f"  • {schema}")
    console.print(
        "\n[yellow]All data in these schemas will be permanently deleted![/yellow]"
    )

    # Confirm unless --force
    if not force:
        confirmed = Confirm.ask("\nAre you sure you want to continue?", default=False)
        if not confirmed:
            console.print("[dim]Aborted.[/dim]")
            return

    # Drop schemas
    with psycopg.connect(settings.rdb.constring) as conn:
        with conn.cursor() as cur:
            for schema in target_schemas:
                try:
                    # Check if schema exists
                    cur.execute(
                        "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = %s)",
                        (schema,),
                    )
                    result = cur.fetchone()
                    exists = result[0] if result else False

                    if exists:
                        cur.execute(
                            f"DROP SCHEMA {schema} CASCADE"  # type: ignore[arg-type]
                        )
                        console.print(f"  [green]✓[/green] Dropped schema: {schema}")
                    else:
                        console.print(f"  [dim]○[/dim] Schema not found: {schema}")
                except Exception as e:
                    console.print(f"  [red]✗[/red] Error dropping {schema}: {e}")

        conn.commit()

    console.print("\n[bold green]Reset completed![/bold green]")
    console.print("[dim]Run 'pmb update <pipeline>' to reload data.[/dim]")
