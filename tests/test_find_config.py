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

        original = cfg.CONFIG_SEARCH_PATHS[:]
        cfg.CONFIG_SEARCH_PATHS[:] = [tmp_path / "nope.yml"]
        try:
            result = find_config(None)
            assert result is None
        finally:
            cfg.CONFIG_SEARCH_PATHS[:] = original

    def test_finds_cwd_config(self, monkeypatch, tmp_path) -> None:
        """Should find config.yml in CWD."""
        config = tmp_path / "config.yml"
        config.write_text("rdb:\n  constring: test\n")
        monkeypatch.chdir(tmp_path)
        import pdbminebuilder.config as cfg

        original = cfg.CONFIG_SEARCH_PATHS[:]
        cfg.CONFIG_SEARCH_PATHS[:] = [tmp_path / "config.yml"]
        try:
            result = find_config(None)
            assert result == tmp_path / "config.yml"
        finally:
            cfg.CONFIG_SEARCH_PATHS[:] = original
