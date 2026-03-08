"""Sync command - rsync data from PDBj."""

import subprocess
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdbminebuilder.commands.utils import resolve_legacy_aliases
from pdbminebuilder.config import Settings

console = Console()

# Default sync targets with their rsync configurations.
# "dest" is omitted — resolved at runtime from pipeline config or data_dir fallback.
SYNC_TARGETS: dict[str, dict] = {
    # CIF targets
    "pdbj": {
        "source": "data.pdbj.org::ftp_data/structures/divided/mmCIF/",
        "options": ["-avz", "--delete"],
    },
    "cc": {
        "source": "data.pdbj.org::ftp_data/monomers/components.cif.gz",
        "options": ["-avz"],
    },
    "ccmodel": {
        "source": "data.pdbj.org::ftp_data/component-models/complete/chem_comp_model.cif.gz",
        "options": ["-avz"],
    },
    "prd": {
        "sources": [
            "data.pdbj.org::ftp_data/bird/prd/prd-all.cif.gz",
            "data.pdbj.org::ftp_data/bird/prd/prdcc-all.cif.gz",
        ],
        "options": ["-avz"],
    },
    "prd-family": {
        "source": "data.pdbj.org::ftp_data/bird/family/family-all.cif.gz",
        "options": ["-avz"],
    },
    "vrpt": {
        "source": "data.pdbj.org::ftp/validation_reports/",
        "options": [
            "-avz",
            '--include="*/"',
            '--include="*_validation.cif.gz"',
            '--exclude="*"',
        ],
    },
    # mmJSON targets
    "pdbj-json": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson/",
        "fallback_dest": "data/mmjson-noatom/",
        "options": ["-avz", "--delete"],
    },
    "cc-json": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/cc/mmjson/",
        "fallback_dest": "data/cc/",
        "options": ["-avz", "--delete"],
    },
    "ccmodel-json": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/ccmodel/",
        "fallback_dest": "data/ccmodel/",
        "options": ["-avz", "--delete"],
    },
    "prd-json": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/prd/",
        "fallback_dest": "data/prd/",
        "options": ["-avz", "--delete"],
    },
    # Plus data targets
    "pdbj-plus": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-plus/",
        "fallback_dest": "data/mmjson-plus/",
        "options": ["-avz", "--delete"],
    },
    "nextgen-plus": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/pdb_nextgen/mmjson-plus/",
        "fallback_dest": "data/pdb_nextgen/mmjson-plus/",
        "options": ["-avz", "--delete"],
    },
    # Other targets
    "contacts": {
        "source": "data.pdbj.org::rsync/pdbjplus/data/pdb/contacts/",
        "fallback_dest": "data/contacts/",
        "options": ["-avz", "--delete"],
    },
}

# Mapping from sync target to pipeline config field.
# Value is (pipeline_name, field_name).
# For file paths, parent directory is used as rsync dest.
_PIPELINE_DEST_MAP: dict[str, tuple[str, str]] = {
    "pdbj": ("pdbj", "data"),
    "cc": ("cc", "data"),
    "ccmodel": ("ccmodel", "data"),
    "prd": ("prd", "data"),
    "prd-family": ("prd_family", "data"),
    "vrpt": ("vrpt", "data"),
    "contacts": ("contacts", "data"),
    "pdbj-plus": ("pdbj", "data_plus"),
    "nextgen-plus": ("pdbj", "data_nextgen_plus"),
}

# Targets whose source URL can be overridden via config sync-sources
# (these have wwPDB regional mirrors: PDBj, RCSB, PDBe)
CONFIGURABLE_TARGETS = {"pdbj", "cc", "ccmodel", "prd", "prd-family", "vrpt"}

# Legacy aliases for backward compatibility (deprecated)
LEGACY_SYNC_ALIASES = {
    "pdbj-cif": "pdbj",
    "cc-cif": "cc",
    "ccmodel-cif": "ccmodel",
    "prd-cif": "prd",
}


def _resolve_dest(target: str, settings: Settings) -> Path | None:
    """Resolve rsync destination from pipeline config or fallback.

    Returns None if the target has no configured destination.
    """
    # Try pipeline config first
    mapping = _PIPELINE_DEST_MAP.get(target)
    if mapping:
        pipeline_name, field_name = mapping
        pipeline = settings.pipelines.get(pipeline_name)
        if pipeline:
            value = getattr(pipeline, field_name, None)
            if value:
                path = Path(value)
                # For file paths, use parent directory as rsync dest
                if path.suffix:
                    return path.parent
                return path

    # Fallback to data_dir + hardcoded relative path
    fallback = SYNC_TARGETS[target].get("fallback_dest")
    if fallback:
        return settings.data_dir.joinpath(fallback)

    return None


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

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for target in targets:
            task = progress.add_task(f"Syncing {target}...", total=None)

            config = SYNC_TARGETS[target]

            # Resolve destination from pipeline config
            dest = _resolve_dest(target, settings)
            if dest is None:
                console.print(
                    f"  [yellow]Skipping {target}: "
                    "no pipeline config or fallback dest[/yellow]"
                )
                progress.update(
                    task, description=f"[yellow]⊘[/yellow] {target} (skipped)"
                )
                continue

            # Build source list (single or multiple files)
            sources = config.get("sources", [config["source"]])

            # Allow config override for wwPDB-mirrored targets
            if target in CONFIGURABLE_TARGETS and target in settings.sync_sources:
                sources = [settings.sync_sources[target]]
                console.print("  [dim](using config override)[/dim]")

            success = all(
                run_rsync(
                    source=source,
                    dest=dest,
                    options=config["options"],
                    dry_run=dry_run,
                )
                for source in sources
            )

            if success:
                progress.update(task, description=f"[green]✓[/green] {target}")
            else:
                progress.update(task, description=f"[red]✗[/red] {target}")

    console.print("[bold green]Sync completed![/bold green]")
