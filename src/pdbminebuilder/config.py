"""Configuration management using pydantic."""

import os
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field


class RdbConfig(BaseModel):
    """Database configuration."""

    nworkers: int | None = Field(
        default=None, description="Number of worker processes (None = auto-detect)"
    )
    constring: str = Field(
        default="host=localhost port=5433 dbname=pmb user=pdbj",
        description="PostgreSQL connection string",
    )

    def get_workers(self) -> int:
        """Get effective worker count (auto-detect if not set, capped at 32)."""
        if self.nworkers is not None:
            return self.nworkers
        return min(os.cpu_count() or 4, 32)


class SyncTarget(BaseModel):
    """Sync target configuration."""

    source: str = Field(description="rsync source URL")
    dest: str = Field(description="Local destination path")
    options: list[str] = Field(
        default_factory=list, description="Additional rsync options"
    )


class PipelineConfig(BaseModel):
    """Pipeline configuration."""

    format: Literal["cif", "mmjson"] = Field(
        default="cif",
        description="Data format: 'cif' (default) or 'mmjson'",
    )
    deffile: str | None = Field(
        default=None,
        description="Schema definition file path (deprecated: schemas are now defined in SQLAlchemy models)",
    )
    data: str = Field(description="Data directory path")
    data_plus: str | None = Field(
        default=None, alias="data-plus", description="Additional data directory"
    )
    data_nextgen_plus: str | None = Field(
        default=None,
        alias="data-nextgen-plus",
        description="Nextgen plus data directory (SIFTS)",
    )

    model_config = {"populate_by_name": True}


class Settings(BaseModel):
    """Application settings."""

    rdb: RdbConfig = Field(default_factory=RdbConfig)
    sync: dict[str, SyncTarget] = Field(default_factory=dict)
    pipelines: dict[str, PipelineConfig] = Field(default_factory=dict)

    # Runtime settings
    cwd: Path = Field(default_factory=Path.cwd)
    data_dir: Path = Field(default=Path("/mnt/c/pdb"))

    model_config = {"populate_by_name": True}


def resolve_variables(
    value: Any, variables: dict[str, str], *, check_unresolved: bool = True
) -> Any:
    """Resolve ${VAR} placeholders in config values.

    Args:
        value: The value to resolve
        variables: Dictionary of variable names to values
        check_unresolved: If True, raise error for unresolved variables

    Raises:
        ValueError: If check_unresolved is True and unresolved variables remain
    """
    if isinstance(value, str):
        for var_name, var_value in variables.items():
            value = value.replace(f"${{{var_name}}}", var_value)

        # Check for unresolved variables
        if check_unresolved:
            unresolved = re.findall(r"\${([^}]+)}", value)
            if unresolved:
                raise ValueError(f"Unresolved config variables: {unresolved}")

        return value
    elif isinstance(value, dict):
        return {
            k: resolve_variables(v, variables, check_unresolved=check_unresolved)
            for k, v in value.items()
        }
    elif isinstance(value, list):
        return [
            resolve_variables(item, variables, check_unresolved=check_unresolved)
            for item in value
        ]
    return value


def load_config(config_path: Path) -> Settings:
    """Load configuration from YAML file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    # Define variables for resolution
    cwd = Path.cwd()
    data_dir = Path(os.environ.get("DATA_DIR", "/mnt/c/pdb"))

    variables = {
        "CWD": str(cwd),
        "DATA_DIR": str(data_dir),
        "HOME": str(Path.home()),
    }

    # Resolve variables in config
    resolved_config = resolve_variables(raw_config, variables)

    # Add runtime settings
    resolved_config["cwd"] = cwd
    resolved_config["data_dir"] = data_dir

    return Settings.model_validate(resolved_config)
