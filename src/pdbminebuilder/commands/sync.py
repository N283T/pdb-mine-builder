"""Sync command - rsync data from configured sources."""

import subprocess
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdbminebuilder.config import Settings, SyncTarget

console = Console()


def run_rsync(
    source: str,
    dest: Path,
    options: list[str],
    dry_run: bool = False,
) -> bool:
    """Run rsync command."""
    dest.mkdir(parents=True, exist_ok=True)

    cmd = ["rsync"] + options
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend([source, str(dest) + "/"])

    console.print(f"  [dim]$ {' '.join(cmd)}[/dim]")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 1 hour timeout
        )
        if result.returncode != 0:
            console.print(f"  [red]Error: {result.stderr}[/red]")
            return False
        return True
    except FileNotFoundError:
        console.print("  [red]Error: rsync is not installed[/red]")
        return False
    except subprocess.TimeoutExpired:
        console.print("  [red]Error: rsync timed out[/red]")
        return False
    except Exception as e:
        console.print(f"  [red]Error: {e}[/red]")
        return False


def _sync_target(target: SyncTarget, dry_run: bool) -> bool:
    """Sync a single target (may have multiple sources)."""
    dest = Path(target.dest)
    results = [
        run_rsync(
            source=src_url,
            dest=dest,
            options=target.options,
            dry_run=dry_run,
        )
        for src_url in target.get_sources()
    ]
    return all(results)


def run_sync(
    settings: Settings,
    targets: list[str],
    dry_run: bool = False,
) -> None:
    """Run sync for specified targets.

    All sync targets must be defined in config.yml under the 'sync' section.
    """
    if not settings.sync:
        console.print(
            "[red]No sync targets configured.[/red]\n"
            "[dim]Add sync targets to the 'sync' section in config.yml. "
            "See config.example.yml for examples.[/dim]"
        )
        return

    # If no targets specified, sync all configured targets
    if not targets:
        targets = list(settings.sync.keys())

    # Validate targets exist in config
    invalid_targets = [t for t in targets if t not in settings.sync]
    if invalid_targets:
        console.print(f"[red]Invalid targets: {', '.join(invalid_targets)}[/red]")
        console.print(
            f"[dim]Configured targets: {', '.join(settings.sync.keys())}[/dim]"
        )
        return

    console.print(f"[bold]Syncing {len(targets)} target(s)...[/bold]")
    if dry_run:
        console.print("[yellow]Dry run mode - no changes will be made[/yellow]")

    succeeded = 0
    failed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for name in targets:
            task = progress.add_task(f"Syncing {name}...", total=None)
            target = settings.sync[name]

            success = _sync_target(target, dry_run)

            if success:
                progress.update(task, description=f"[green]✓[/green] {name}")
                succeeded += 1
            else:
                progress.update(task, description=f"[red]✗[/red] {name}")
                failed += 1

    if failed:
        console.print(
            f"[bold red]Sync finished: {succeeded} ok, {failed} failed[/bold red]"
        )
    else:
        console.print(
            f"[bold green]Sync completed: {succeeded} target(s) synced[/bold green]"
        )
