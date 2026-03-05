"""Tests for loader deletion, and pruning logic."""

import logging
from unittest.mock import MagicMock, patch

from sqlalchemy import Column, Integer, MetaData, PrimaryKeyConstraint, Table, Text

from pdbminebuilder.db.loader import LoaderResult
from pdbminebuilder.pipelines.base import BaseCifBatchPipeline


# =============================================================================
# delete_missing_entries tests
# =============================================================================


def _mock_psycopg_connect():
    """Create a mock psycopg connection context manager."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.rowcount = 0
    mock_cur.copy.return_value.__enter__ = MagicMock()
    mock_cur.copy.return_value.__exit__ = MagicMock(return_value=False)
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cur


class TestDeleteMissingEntries:
    """Tests for delete_missing_entries() safety guard."""

    @patch("psycopg.connect")
    def test_empty_keep_list_logs_warning(self, mock_connect, caplog):
        """Empty keep_entry_ids should log a warning."""
        mock_conn, mock_cur = _mock_psycopg_connect()
        mock_connect.return_value = mock_conn

        from pdbminebuilder.db.loader import delete_missing_entries

        with caplog.at_level(logging.WARNING, logger="pdbminebuilder.loader"):
            delete_missing_entries(
                conninfo="postgresql://test",
                schema="test",
                pk_column="id",
                tables=["table1"],
                keep_entry_ids=[],
            )

        assert any("empty keep_entry_ids" in r.message for r in caplog.records)

    @patch("psycopg.connect")
    def test_empty_tables_returns_zero(self, mock_connect):
        """No tables means nothing to delete."""
        mock_conn, _ = _mock_psycopg_connect()
        mock_connect.return_value = mock_conn

        from pdbminebuilder.db.loader import delete_missing_entries

        result = delete_missing_entries(
            conninfo="postgresql://test",
            schema="test",
            pk_column="id",
            tables=[],
            keep_entry_ids=["A", "B"],
        )
        assert result == 0


# =============================================================================
# BaseCifBatchPipeline._prune_stale_rows tests
# =============================================================================


def _make_pipeline() -> BaseCifBatchPipeline:
    """Create a minimal BaseCifBatchPipeline for testing."""
    meta = MetaData(schema="test")
    meta.info = {"entry_pk": "id"}
    Table(
        "t1",
        meta,
        Column("id", Text),
        Column("val", Integer),
        PrimaryKeyConstraint("id"),
    )
    settings = MagicMock()
    config = MagicMock()
    return BaseCifBatchPipeline(settings, config, meta)


class TestPruneStaleRows:
    """Tests for BaseCifBatchPipeline._prune_stale_rows()."""

    def test_limit_set_skips_prune(self, capsys):
        """When limit is not None, pruning is skipped."""
        pipeline = _make_pipeline()
        results = [LoaderResult(entry_id="A", success=True)]
        pipeline._prune_stale_rows(results, "conn", limit=5)
        captured = capsys.readouterr()
        assert "Skipping prune (limited run)" in captured.out

    def test_empty_results_skips_prune(self, capsys):
        """Empty results should skip pruning."""
        pipeline = _make_pipeline()
        pipeline._prune_stale_rows([], "conn", limit=None)
        captured = capsys.readouterr()
        assert "no entries processed" in captured.out

    def test_failed_entries_skips_prune(self, capsys):
        """Partial failure should skip pruning."""
        pipeline = _make_pipeline()
        results = [
            LoaderResult(entry_id="A", success=True),
            LoaderResult(entry_id="B", success=False, error="fail"),
        ]
        pipeline._prune_stale_rows(results, "conn", limit=None)
        captured = capsys.readouterr()
        assert "failed entries" in captured.out

    @patch("pdbminebuilder.pipelines.base.delete_missing_entries", return_value=3)
    def test_all_success_calls_prune(self, mock_delete, capsys):
        """All success with no limit should actually prune."""
        pipeline = _make_pipeline()
        results = [
            LoaderResult(entry_id="A", success=True),
            LoaderResult(entry_id="B", success=True),
        ]
        pipeline._prune_stale_rows(results, "postgresql://test", limit=None)

        mock_delete.assert_called_once_with(
            conninfo="postgresql://test",
            schema="test",
            pk_column="id",
            tables=["t1"],
            keep_entry_ids=["A", "B"],
        )
        captured = capsys.readouterr()
        assert "Pruned stale rows: 3" in captured.out
