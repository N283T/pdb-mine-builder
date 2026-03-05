"""Sync command - rsync data from PDBj."""

import subprocess
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdbminebuilder.commands.utils import resolve_legacy_aliases
from pdbminebuilder.config import Settings

console = Console()

# Default sync targets with their rsync configurations
# CIF is default, -json suffix for mmJSON
SYNC_TARGETS: dict[str, dict] = {
    "pdbj": {  # CIF (default)
        "source": "rsync.pdbj.org::ftp_data/structures/divided/mmCIF/",
        "dest": "data/structures/divided/mmCIF/",
        "options": ["-avz", "--delete"],
    },
    "pdbj-json": {  # mmJSON (requires suffix)
        "source": "rsync.pdbj.org::ftp_data/structures/divided/mmjson-noatom/",
        "dest": "data/mmjson-noatom/",
        "options": ["-avz", "--delete"],
    },
    "pdbj-plus": {  # mmJSON plus data
        "source": "rsync.pdbj.org::mine/ftp_data/mine_data/mmjson-plus/",
        "dest": "pdbj/pdbjplus/",
        "options": ["-avz", "--delete"],
    },
    "cc": {  # CIF (default)
        "source": "rsync.pdbj.org::ftp_data/monomers/components.cif.gz",
        "dest": "data/monomers/",
        "options": ["-avz"],
    },
    "cc-json": {  # mmJSON (requires suffix)
        "source": "rsync.pdbj.org::ftp_data/component-models/complete/chem_comp-mmjson/",
        "dest": "data/cc/",
        "options": ["-avz", "--delete"],
    },
    "ccmodel": {  # CIF (default)
        "source": "rsync.pdbj.org::ftp_data/component-models/complete/chem_comp_model.cif.gz",
        "dest": "data/component-models/complete/",
        "options": ["-avz"],
    },
    "ccmodel-json": {  # mmJSON (requires suffix)
        "source": "rsync.pdbj.org::ftp_data/component-models/complete/chem_comp_model-mmjson/",
        "dest": "data/ccmodel/",
        "options": ["-avz", "--delete"],
    },
    "prd": {  # CIF (default)
        "source": "rsync.pdbj.org::ftp_data/bird/prd/",
        "dest": "data/bird/prd/",
        "options": ["-avz"],
    },
    "prd-json": {  # mmJSON (requires suffix)
        "source": "rsync.pdbj.org::ftp_data/bird/mmjson/",
        "dest": "data/prd/",
        "options": ["-avz", "--delete"],
    },
    "vrpt": {
        # Fixed: use include/exclude pattern to avoid timeout
        "source": "rsync.pdbj.org::ftp_data/validation_reports/",
        "dest": "validation_reports/",
        "options": [
            "-avz",
            '--include="*/"',
            '--include="*_validation.cif.gz"',
            '--exclude="*"',
        ],
    },
    "contacts": {
        "source": "rsync.pdbj.org::mine/ftp_data/mine_data/contacts/",
        "dest": "data/contacts/",
        "options": ["-avz", "--delete"],
    },
    "schemas": {
        "source": "rsync.pdbj.org::mine/ftp_data/mine_data/sql/pdb/schemas/",
        "dest": "schemas/",
        "options": ["-avz", "--delete"],
    },
    "sifts": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/sifts/rdf/",
        "dest": "pdbj/pdbjplus/data/sifts/rdf/",
        "options": ["-avz", "--delete"],
    },
}

# Legacy aliases for backward compatibility (deprecated)
LEGACY_SYNC_ALIASES = {
    "pdbj-cif": "pdbj",
    "cc-cif": "cc",
    "ccmodel-cif": "ccmodel",
    "prd-cif": "prd",
}


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
    except subprocess.TimeoutExpired:
        console.print("  [red]Error: rsync timed out[/red]")
        return False
    except Exception as e:
        console.print(f"  [red]Error: {e}[/red]")
        return False


def run_sync(
    settings: Settings,
    targets: list[str],
    dry_run: bool = False,
) -> None:
    """Run sync for specified targets."""
    # If no targets specified, sync all
    if not targets:
        targets = list(SYNC_TARGETS.keys())

    # Resolve legacy aliases with deprecation warnings
    targets = resolve_legacy_aliases(targets, LEGACY_SYNC_ALIASES, "Sync target")

    # Validate targets
    invalid_targets = [t for t in targets if t not in SYNC_TARGETS]
    if invalid_targets:
        console.print(f"[red]Invalid targets: {', '.join(invalid_targets)}[/red]")
        console.print(f"[dim]Available targets: {', '.join(SYNC_TARGETS.keys())}[/dim]")
        return

    console.print(f"[bold]Syncing {len(targets)} target(s)...[/bold]")
    if dry_run:
        console.print("[yellow]Dry run mode - no changes will be made[/yellow]")

    data_dir = settings.data_dir

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for target in targets:
            task = progress.add_task(f"Syncing {target}...", total=None)

            config = SYNC_TARGETS[target]
            dest = data_dir.joinpath(config["dest"])

            success = run_rsync(
                source=config["source"],
                dest=dest,
                options=config["options"],
                dry_run=dry_run,
            )

            if success:
                progress.update(task, description=f"[green]✓[/green] {target}")
            else:
                progress.update(task, description=f"[red]✗[/red] {target}")

    console.print("[bold green]Sync completed![/bold green]")
