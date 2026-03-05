"""Tests for mtime-based skip optimization."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from pdbminebuilder.db.loader import Job
from pdbminebuilder.pipelines.base import compute_effective_mtime


class TestComputeEffectiveMtime:
    """Tests for compute_effective_mtime helper."""

    def test_single_file(self, tmp_path):
        """Return mtime of a single file."""
        f = tmp_path / "data.json.gz"
        f.write_text("test")

        result = compute_effective_mtime(f)

        assert result == f.stat().st_mtime

    def test_max_across_extra_paths(self, tmp_path):
        """Return max mtime when extra paths are provided."""
        main = tmp_path / "main.json.gz"
        plus = tmp_path / "plus.json.gz"
        main.write_text("main")
        plus.write_text("plus")

        # Make plus file newer
        main_mtime = main.stat().st_mtime
        os.utime(plus, (main_mtime + 100, main_mtime + 100))

        result = compute_effective_mtime(main, [plus])

        assert result == plus.stat().st_mtime
        assert result > main_mtime

    def test_none_extra_paths_skipped(self, tmp_path):
        """None entries in extra_paths are safely skipped."""
        f = tmp_path / "data.json.gz"
        f.write_text("test")

        result = compute_effective_mtime(f, [None, None])

        assert result == f.stat().st_mtime

    def test_missing_extra_paths_skipped(self, tmp_path):
        """Non-existent extra paths are skipped."""
        f = tmp_path / "data.json.gz"
        f.write_text("test")
        missing = tmp_path / "nonexistent.json.gz"

        result = compute_effective_mtime(f, [missing])

        assert result == f.stat().st_mtime

    def test_empty_extra_paths(self, tmp_path):
        """Empty extra_paths list works like single file."""
        f = tmp_path / "data.json.gz"
        f.write_text("test")

        result = compute_effective_mtime(f, [])

        assert result == f.stat().st_mtime


class TestBasePipelineFindJobsMtimeFiltering:
    """Tests for BasePipeline.find_jobs() mtime skip logic."""

    def _make_pipeline(self, tmp_path, force=False, stored_mtimes=None):
        """Create a minimal concrete pipeline for testing."""
        from pdbminebuilder.pipelines.contacts import ContactsPipeline

        settings = MagicMock()
        settings.rdb.constring = "host=localhost dbname=test"
        config = MagicMock()
        config.data = str(tmp_path)

        meta = MagicMock()
        meta.schema = "contacts"

        pipeline = ContactsPipeline(settings, config, meta, force=force)

        # Patch fetch_entry_mtimes
        self._stored_mtimes = stored_mtimes or {}
        return pipeline

    @patch("pdbminebuilder.pipelines.base.fetch_entry_mtimes")
    def test_skips_unchanged_entries(self, mock_fetch, tmp_path):
        """Unchanged entries are skipped when mtime matches."""
        # Create test files
        f1 = tmp_path / "100d.json.gz"
        f2 = tmp_path / "200l.json.gz"
        f1.write_text("data1")
        f2.write_text("data2")

        # Mark 100d as already processed with current mtime
        f1_mtime = f1.stat().st_mtime
        mock_fetch.return_value = {"100d": f1_mtime + 1.0}  # stored is newer

        pipeline = self._make_pipeline(tmp_path, force=False)
        jobs = pipeline.find_jobs()

        # Only 200l should be returned
        entry_ids = [j.entry_id for j in jobs]
        assert "200l" in entry_ids
        assert "100d" not in entry_ids

    @patch("pdbminebuilder.pipelines.base.fetch_entry_mtimes")
    def test_processes_changed_entries(self, mock_fetch, tmp_path):
        """Changed entries (newer mtime) are included."""
        f1 = tmp_path / "100d.json.gz"
        f1.write_text("data1")

        # Stored mtime is older than current
        mock_fetch.return_value = {"100d": 0.0}

        pipeline = self._make_pipeline(tmp_path, force=False)
        jobs = pipeline.find_jobs()

        entry_ids = [j.entry_id for j in jobs]
        assert "100d" in entry_ids

    @patch("pdbminebuilder.pipelines.base.fetch_entry_mtimes")
    def test_force_bypasses_skip(self, mock_fetch, tmp_path):
        """Force mode processes all entries regardless of mtime."""
        f1 = tmp_path / "100d.json.gz"
        f1.write_text("data1")

        # Would normally be skipped
        mock_fetch.return_value = {"100d": f1.stat().st_mtime + 1.0}

        pipeline = self._make_pipeline(tmp_path, force=True)
        jobs = pipeline.find_jobs()

        entry_ids = [j.entry_id for j in jobs]
        assert "100d" in entry_ids
        # fetch_entry_mtimes should not be called in force mode
        mock_fetch.assert_not_called()

    @patch("pdbminebuilder.pipelines.base.fetch_entry_mtimes")
    def test_file_mtime_stored_in_job_extra(self, mock_fetch, tmp_path):
        """Jobs include file_mtime in extra dict."""
        f1 = tmp_path / "100d.json.gz"
        f1.write_text("data1")

        mock_fetch.return_value = {}

        pipeline = self._make_pipeline(tmp_path, force=False)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert "file_mtime" in jobs[0].extra
        assert jobs[0].extra["file_mtime"] == f1.stat().st_mtime

    @patch("pdbminebuilder.pipelines.base.fetch_entry_mtimes")
    def test_new_entries_always_processed(self, mock_fetch, tmp_path):
        """Entries not in stored mtimes are always processed."""
        f1 = tmp_path / "new_entry.json.gz"
        f1.write_text("data")

        mock_fetch.return_value = {"other_entry": 999999.0}

        pipeline = self._make_pipeline(tmp_path, force=False)
        jobs = pipeline.find_jobs()

        entry_ids = [j.entry_id for j in jobs]
        assert "new_entry" in entry_ids
