"""Tests for environment version requirements."""

import subprocess
import sys


class TestPythonVersion:
    """Verify Python version meets pixi.toml requirements (>=3.12)."""

    def test_python_major_minor(self):
        assert sys.version_info >= (3, 12), (
            f"Python >=3.12 required, got {sys.version_info.major}.{sys.version_info.minor}"
        )


class TestPostgreSQLVersion:
    """Verify PostgreSQL version (provided by rdkit-postgresql dependency)."""

    def test_pg_version_minimum(self):
        result = subprocess.run(
            ["pg_config", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Output like "PostgreSQL 18.3"
        version_str = result.stdout.strip().split()[-1]
        major = int(version_str.split(".")[0])
        assert major >= 17, f"PostgreSQL >=17 required, got {version_str}"

    def test_psql_available(self):
        result = subprocess.run(
            ["psql", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "psql" in result.stdout
