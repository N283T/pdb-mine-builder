"""Shared utilities for commands."""

import warnings

from rich.console import Console

console = Console()


def resolve_legacy_aliases(
    items: list[str],
    aliases: dict[str, str],
    item_type: str = "name",
) -> list[str]:
    """Resolve legacy aliases with deprecation warnings.

    Args:
        items: List of items to resolve
        aliases: Dictionary mapping legacy names to new names
        item_type: Type of item for warning message (e.g., "Pipeline", "Sync target")

    Returns:
        List of resolved items with legacy names replaced
    """
    resolved = []
    for item in items:
        if item in aliases:
            new_name = aliases[item]
            # For -json aliases, remind user that format is now config-driven
            if item.endswith("-json"):
                console.print(
                    f"[yellow]Warning: '{item}' is deprecated. Use '{new_name}' instead. "
                    f"Format is now controlled by the 'format' field in config.yml.[/yellow]"
                )
            else:
                console.print(
                    f"[yellow]Warning: '{item}' is deprecated. Use '{new_name}' instead.[/yellow]"
                )
            warnings.warn(
                f"{item_type} '{item}' is deprecated. Use '{new_name}' instead.",
                DeprecationWarning,
                stacklevel=3,
            )
            resolved.append(new_name)
        else:
            resolved.append(item)
    return resolved
