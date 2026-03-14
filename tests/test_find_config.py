"""Tests for find_config."""

import pytest

from pdbminebuilder.config import find_config


class TestFindConfig:
    """Tests for find_config."""

    def test_explicit_path_exists(self, tmp_path) -> None:
        """Should return explicit path when it exists."""
        config = tmp_path / "config.yml"
        config.write_text("rdb:\n  constring: test\n")
        result = find_config(config)
        assert result == config

    def test_explicit_path_not_found(self, tmp_path) -> None:
        """Should raise FileNotFoundError for explicit path that doesn't exist."""
        missing = tmp_path / "nonexistent.yml"
        with pytest.raises(FileNotFoundError):
            find_config(missing)

    def test_none_returns_none_when_no_config(self, monkeypatch, tmp_path) -> None:
        """Should return None when no config found in standard locations."""
        monkeypatch.chdir(tmp_path)
        import pdbminebuilder.config as cfg

        monkeypatch.setattr(cfg, "CONFIG_SEARCH_PATHS", (tmp_path / "nope.yml",))
        result = find_config(None)
        assert result is None

    def test_finds_cwd_config(self, monkeypatch, tmp_path) -> None:
        """Should find config.yml in CWD."""
        config = tmp_path / "config.yml"
        config.write_text("rdb:\n  constring: test\n")
        monkeypatch.chdir(tmp_path)
        import pdbminebuilder.config as cfg

        monkeypatch.setattr(cfg, "CONFIG_SEARCH_PATHS", (tmp_path / "config.yml",))
        result = find_config(None)
        assert result == tmp_path / "config.yml"

    def test_search_order_priority(self, monkeypatch, tmp_path) -> None:
        """Should return first matching config when multiple exist."""
        first = tmp_path / "first.yml"
        second = tmp_path / "second.yml"
        first.write_text("rdb:\n  constring: first\n")
        second.write_text("rdb:\n  constring: second\n")
        import pdbminebuilder.config as cfg

        monkeypatch.setattr(cfg, "CONFIG_SEARCH_PATHS", (first, second))
        result = find_config(None)
        assert result == first
