"""Tests for environment version requirements."""

import re
import shutil
import subprocess
import sys

import pytest


class TestPythonVersion:
    """Verify Python version meets pixi.toml requirements (>=3.12)."""

    def test_python_major_minor(self):
        assert sys.version_info >= (3, 12), (
            f"Python >=3.12 required, got {sys.version_info.major}.{sys.version_info.minor}"
        )


class TestPostgreSQLVersion:
    """Verify PostgreSQL version (provided by rdkit-postgresql dependency)."""

    @pytest.mark.skipif(not shutil.which("pg_config"), reason="pg_config not found")
    def test_pg_version_minimum(self):
        result = subprocess.run(
            ["pg_config", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        match = re.search(r"(\d+)\.\d+", result.stdout)
        assert match, f"Could not parse PostgreSQL version from: {result.stdout.strip()}"
        major = int(match.group(1))
        assert major >= 17, f"PostgreSQL >=17 required, got {result.stdout.strip()}"

    @pytest.mark.skipif(not shutil.which("psql"), reason="psql not found")
    def test_psql_version_minimum(self):
        result = subprocess.run(
            ["psql", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        match = re.search(r"(\d+)\.\d+", result.stdout)
        assert match, f"Could not parse psql version from: {result.stdout.strip()}"
        major = int(match.group(1))
        assert major >= 17, f"psql >=17 required, got {result.stdout.strip()}"


CONDA_PACKAGES = [
    "alembic",
    "defusedxml",
    "gemmi",
    "pydantic",
    "pydantic_settings",
    "rich",
    "ruff",
    "sqlalchemy",
    "typer",
    "yaml",
]


class TestCondaPackages:
    """Verify conda-forge packages are importable."""

    @pytest.mark.parametrize("module", CONDA_PACKAGES)
    def test_import(self, module):
        __import__(module)
