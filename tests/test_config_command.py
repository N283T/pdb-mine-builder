"""Tests for pmb config command."""

import json

from typer.testing import CliRunner

from pdbminebuilder.cli import app

runner = CliRunner()

MINIMAL_CONFIG = """\
rdb:
  constring: "host=localhost port=5433 dbname=test user=testuser password=secret123"
pipelines:
  pdbj:
    format: cif
    data: /tmp/data
"""


class TestConfigCommand:
    """Tests for pmb config command."""

    def test_no_config_found(self, monkeypatch, tmp_path) -> None:
        """Should exit 1 when no config file found."""
        monkeypatch.chdir(tmp_path)
        import pdbminebuilder.config as cfg

        monkeypatch.setattr(cfg, "CONFIG_SEARCH_PATHS", (tmp_path / "nope.yml",))
        result = runner.invoke(app, ["config"])
        assert result.exit_code == 1
        assert "No config file found" in result.output

    def test_explicit_path_not_found(self, tmp_path) -> None:
        """Should exit 1 with error message for missing explicit config."""
        result = runner.invoke(app, ["config", "-c", str(tmp_path / "missing.yml")])
        assert result.exit_code == 1
        assert "Config file not found" in result.output

    def test_rich_output(self, tmp_path) -> None:
        """Should display config summary in rich format."""
        config = tmp_path / "config.yml"
        config.write_text(MINIMAL_CONFIG)
        result = runner.invoke(app, ["config", "-c", str(config)])
        assert result.exit_code == 0
        assert "Config:" in result.output
        assert "Connection:" in result.output
        assert "Workers:" in result.output

    def test_json_output(self, tmp_path) -> None:
        """Should output valid JSON with expected keys."""
        config = tmp_path / "config.yml"
        config.write_text(MINIMAL_CONFIG)
        result = runner.invoke(app, ["config", "--json", "-c", str(config)])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "config_path" in data
        assert "connection" in data
        assert "data_dir" in data
        assert "workers" in data
        assert "pipelines" in data
        assert "sync_targets" in data

    def test_password_redaction(self, tmp_path) -> None:
        """Should redact password in connection string."""
        config = tmp_path / "config.yml"
        config.write_text(MINIMAL_CONFIG)
        result = runner.invoke(app, ["config", "-c", str(config)])
        assert result.exit_code == 0
        assert "secret123" not in result.output
        assert "password=****" in result.output

    def test_password_redaction_json(self, tmp_path) -> None:
        """Should redact password in JSON output too."""
        config = tmp_path / "config.yml"
        config.write_text(MINIMAL_CONFIG)
        result = runner.invoke(app, ["config", "--json", "-c", str(config)])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "secret123" not in data["connection"]
        assert "password=****" in data["connection"]

    def test_invalid_config(self, tmp_path) -> None:
        """Should exit 1 with error for invalid config."""
        config = tmp_path / "config.yml"
        config.write_text("invalid: {yaml: [broken")
        result = runner.invoke(app, ["config", "-c", str(config)])
        assert result.exit_code == 1
        assert "Error loading config" in result.output

    def test_no_config_suggests_init(self, monkeypatch, tmp_path) -> None:
        """Should suggest --init when no config found."""
        monkeypatch.chdir(tmp_path)
        import pdbminebuilder.config as cfg

        monkeypatch.setattr(cfg, "CONFIG_SEARCH_PATHS", (tmp_path / "nope.yml",))
        result = runner.invoke(app, ["config"])
        assert "pmb config --init" in result.output


class TestConfigInit:
    """Tests for pmb config --init."""

    def test_init_creates_default_config(self, monkeypatch, tmp_path) -> None:
        """Should create config at ~/.config/pmb/config.yml."""
        import pdbminebuilder.cli as cli_mod

        monkeypatch.setattr(cli_mod, "DEFAULT_CONFIG_DIR", tmp_path / ".config" / "pmb")
        result = runner.invoke(app, ["config", "--init"])
        assert result.exit_code == 0
        target = tmp_path / ".config" / "pmb" / "config.yml"
        assert target.exists()
        content = target.read_text()
        assert "constring" in content
        assert "Config file created" in result.output

    def test_init_to_directory(self, tmp_path) -> None:
        """Should create config.yml in specified directory."""
        result = runner.invoke(app, ["config", "--init", "-c", str(tmp_path)])
        assert result.exit_code == 0
        target = tmp_path / "config.yml"
        assert target.exists()
        content = target.read_text()
        assert "constring" in content

    def test_init_refuses_overwrite(self, monkeypatch, tmp_path) -> None:
        """Should refuse to overwrite existing config."""
        import pdbminebuilder.cli as cli_mod

        config_dir = tmp_path / ".config" / "pmb"
        config_dir.mkdir(parents=True)
        existing = config_dir / "config.yml"
        existing.write_text("existing config")
        monkeypatch.setattr(cli_mod, "DEFAULT_CONFIG_DIR", config_dir)
        result = runner.invoke(app, ["config", "--init"])
        assert result.exit_code == 1
        assert "already exists" in result.output
        assert existing.read_text() == "existing config"

    def test_init_to_explicit_path(self, tmp_path) -> None:
        """Should create config at explicit file path."""
        target = tmp_path / "my-config.yml"
        result = runner.invoke(app, ["config", "--init", "-c", str(target)])
        assert result.exit_code == 0
        assert target.exists()

    def test_init_template_matches_example(self, tmp_path) -> None:
        """Generated config should match bundled template."""
        import importlib.resources

        template = importlib.resources.files("pdbminebuilder").joinpath(
            "config.example.yml"
        )
        expected = template.read_text(encoding="utf-8")
        result = runner.invoke(app, ["config", "--init", "-c", str(tmp_path)])
        assert result.exit_code == 0
        actual = (tmp_path / "config.yml").read_text()
        assert actual == expected
