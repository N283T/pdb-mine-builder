"""Configuration management using pydantic."""

import os
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator


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
    """Sync target configuration.

    Each target defines an rsync source (or multiple sources), a local
    destination, and rsync options. All fields are user-defined in config.yml.
    """

    source: str | None = Field(
        default=None, description="rsync source URL (single source)"
    )
    sources: list[str] | None = Field(
        default=None, description="rsync source URLs (multiple sources)"
    )
    dest: str = Field(description="Local destination directory")
    options: list[str] = Field(
        default_factory=lambda: ["-av", "--size-only"],
        description="rsync options",
    )

    @model_validator(mode="after")
    def validate_source(self) -> "SyncTarget":
        """Ensure exactly one of source or sources is set."""
        if self.source and self.sources:
            raise ValueError("Cannot set both 'source' and 'sources'")
        if not self.source and not self.sources:
            raise ValueError("Either 'source' or 'sources' must be set")
        return self

    def get_sources(self) -> list[str]:
        """Return source URLs as a list."""
        if self.sources:
            return list(self.sources)
        assert self.source is not None  # guaranteed by validator
        return [self.source]


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
    prdcc: str | None = Field(
        default=None,
        description="PRDCC CIF file path (prd pipeline only, optional)",
    )

    model_config = {"populate_by_name": True}


class Settings(BaseModel):
    """Application settings."""

    rdb: RdbConfig = Field(default_factory=RdbConfig)
    sync: dict[str, SyncTarget] = Field(default_factory=dict)
    pipelines: dict[str, PipelineConfig] = Field(default_factory=dict)

    # Runtime settings
    cwd: Path = Field(default_factory=Path.cwd)
    data_dir: Path = Field(
        default_factory=Path.cwd,
        alias="data-dir",
        description="Base directory for synced data",
    )

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


CONFIG_SEARCH_PATHS: tuple[Path, ...] = (
    Path("config.yml"),
    Path.home().joinpath(".config", "pmb", "config.yml"),
)


def find_config(explicit: Path | None = None) -> Path | None:
    """Find config file from explicit path or standard locations.

    Search order:
        1. Explicit path (--config flag) -- must exist, raises if not found
        2. ./config.yml (CWD)
        3. ~/.config/pmb/config.yml

    Returns:
        Path to config file, or None if no config found in standard locations.

    Raises:
        FileNotFoundError: If explicit path is given but does not exist.
    """
    if explicit is not None:
        if not explicit.exists():
            raise FileNotFoundError(f"Config file not found: {explicit}")
        return explicit

    for candidate in CONFIG_SEARCH_PATHS:
        if candidate.exists():
            return candidate

    return None


def load_config(config_path: Path) -> Settings:
    """Load configuration from YAML file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    # Determine data_dir: config > DATA_DIR env > CWD
    cwd = Path.cwd()
    raw_data_dir = raw_config.get("data-dir") or raw_config.get("data_dir")
    if raw_data_dir:
        # Resolve ${HOME} and ${CWD} in data-dir itself
        resolved_data_dir = str(raw_data_dir).replace("${HOME}", str(Path.home()))
        resolved_data_dir = resolved_data_dir.replace("${CWD}", str(cwd))
        data_dir = Path(resolved_data_dir)
    elif os.environ.get("DATA_DIR"):
        data_dir = Path(os.environ["DATA_DIR"])
    else:
        data_dir = cwd

    variables = {
        "CWD": str(cwd),
        "DATA_DIR": str(data_dir),
        "HOME": str(Path.home()),
    }

    # Resolve variables in config
    resolved_config = resolve_variables(raw_config, variables)

    # Add runtime settings
    resolved_config["cwd"] = cwd
    resolved_config["data-dir"] = data_dir

    return Settings.model_validate(resolved_config)
