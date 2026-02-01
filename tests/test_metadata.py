"""Tests for pipeline metadata management."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from mine2.db.metadata import (
    ensure_metadata_table,
    get_pipeline_metadata,
    update_pipeline_metadata,
)


class TestGetPipelineMetadata:
    """Tests for get_pipeline_metadata function."""

    def test_returns_none_when_table_not_exists(self):
        """Test returns None when pipeline_metadata table doesn't exist."""
        cur = MagicMock()
        # First query: table exists check returns False
        cur.fetchone.return_value = (False,)

        last_updated, entries_count = get_pipeline_metadata(cur, "pdbj")

        assert last_updated is None
        assert entries_count is None

    def test_returns_none_when_schema_not_found(self):
        """Test returns None when schema not in metadata table."""
        cur = MagicMock()
        # First query: table exists check returns True
        # Second query: no row found
        cur.fetchone.side_effect = [(True,), None]

        last_updated, entries_count = get_pipeline_metadata(cur, "pdbj")

        assert last_updated is None
        assert entries_count is None

    def test_returns_metadata_when_found(self):
        """Test returns metadata when schema found."""
        cur = MagicMock()
        test_time = datetime(2026, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        # First query: table exists check returns True
        # Second query: returns metadata
        cur.fetchone.side_effect = [(True,), (test_time, 100)]

        last_updated, entries_count = get_pipeline_metadata(cur, "pdbj")

        assert last_updated == test_time
        assert entries_count == 100


class TestEnsureMetadataTable:
    """Tests for ensure_metadata_table function."""

    @patch("mine2.db.metadata.psycopg.connect")
    def test_creates_table_if_not_exists(self, mock_connect):
        """Test that CREATE TABLE IF NOT EXISTS is executed."""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        ensure_metadata_table("postgresql://test")

        # Verify CREATE TABLE was called
        mock_cur.execute.assert_called_once()
        call_args = mock_cur.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS" in call_args
        assert "pipeline_metadata" in call_args
        mock_conn.commit.assert_called_once()

    @patch("mine2.db.metadata.psycopg.connect")
    def test_idempotent_multiple_calls(self, mock_connect):
        """Test that multiple calls don't fail (IF NOT EXISTS)."""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        # Call twice - should not raise
        ensure_metadata_table("postgresql://test")
        ensure_metadata_table("postgresql://test")

        assert mock_cur.execute.call_count == 2


class TestUpdatePipelineMetadata:
    """Tests for update_pipeline_metadata function."""

    @patch("mine2.db.metadata.psycopg.connect")
    def test_inserts_new_record(self, mock_connect):
        """Test that INSERT with ON CONFLICT is executed."""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        update_pipeline_metadata("postgresql://test", "pdbj", entries_count=100)

        mock_cur.execute.assert_called_once()
        call_args = mock_cur.execute.call_args[0]
        assert "INSERT INTO" in call_args[0]
        assert "ON CONFLICT" in call_args[0]
        assert call_args[1][0] == "pdbj"
        assert call_args[1][2] == 100
        mock_conn.commit.assert_called_once()

    @patch("mine2.db.metadata.psycopg.connect")
    def test_updates_existing_record(self, mock_connect):
        """Test that upsert updates existing record."""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        update_pipeline_metadata("postgresql://test", "pdbj", entries_count=200)

        call_args = mock_cur.execute.call_args[0]
        assert "DO UPDATE SET" in call_args[0]

    @patch("mine2.db.metadata.psycopg.connect")
    def test_handles_none_entries_count(self, mock_connect):
        """Test that None entries_count is handled correctly."""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        update_pipeline_metadata("postgresql://test", "cc")

        call_args = mock_cur.execute.call_args[0]
        assert call_args[1][2] is None  # entries_count should be None
