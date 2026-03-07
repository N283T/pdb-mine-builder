"""Tests for the query command."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import polars as pl
import pytest

from pdbminebuilder.commands.query import (
    OutputFormat,
    _render_rich_table,
    run_query,
)


class TestExecuteQuery:
    """Test SQL execution and DataFrame conversion."""

    def test_returns_dataframe_from_query(self):
        mock_cursor = MagicMock()
        mock_cursor.description = [("id",), ("name",)]
        mock_cursor.fetchall.return_value = [(1, "ATP"), (2, "GTP")]

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        with patch("pdbminebuilder.commands.query.psycopg.connect", return_value=mock_conn):
            from pdbminebuilder.commands.query import _execute_query

            df = _execute_query("dbname=test", "SELECT id, name FROM test")

        assert isinstance(df, pl.DataFrame)
        assert df.shape == (2, 2)
        assert df.columns == ["id", "name"]

    def test_empty_result_returns_empty_dataframe(self):
        mock_cursor = MagicMock()
        mock_cursor.description = [("id",), ("name",)]
        mock_cursor.fetchall.return_value = []

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        with patch("pdbminebuilder.commands.query.psycopg.connect", return_value=mock_conn):
            from pdbminebuilder.commands.query import _execute_query

            df = _execute_query("dbname=test", "SELECT id, name FROM empty")

        assert isinstance(df, pl.DataFrame)
        assert df.is_empty()
        assert df.columns == ["id", "name"]

    def test_no_description_returns_empty_dataframe(self):
        mock_cursor = MagicMock()
        mock_cursor.description = None

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        with patch("pdbminebuilder.commands.query.psycopg.connect", return_value=mock_conn):
            from pdbminebuilder.commands.query import _execute_query

            df = _execute_query("dbname=test", "CREATE TABLE t (id int)")

        assert isinstance(df, pl.DataFrame)
        assert df.is_empty()


class TestRenderRichTable:
    """Test Rich table rendering."""

    def test_empty_dataframe(self, capsys):
        df = pl.DataFrame()
        _render_rich_table(df)

    def test_with_max_rows(self):
        df = pl.DataFrame({"id": [1, 2, 3, 4, 5]})
        # Should not raise
        _render_rich_table(df, max_rows=2)


class TestOutputFormat:
    """Test output format enum."""

    def test_valid_formats(self):
        assert OutputFormat("table") == OutputFormat.table
        assert OutputFormat("csv") == OutputFormat.csv
        assert OutputFormat("json") == OutputFormat.json
        assert OutputFormat("parquet") == OutputFormat.parquet

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            OutputFormat("xml")


class TestRunQueryOutputFormats:
    """Test run_query with different output formats."""

    @pytest.fixture
    def mock_settings(self):
        settings = MagicMock()
        settings.rdb.constring = "dbname=test"
        return settings

    @pytest.fixture
    def sample_df(self):
        return pl.DataFrame({"id": [1, 2], "name": ["ATP", "GTP"]})

    def test_csv_to_file(self, mock_settings, sample_df, tmp_path):
        out = tmp_path / "out.csv"
        with patch("pdbminebuilder.commands.query._execute_query", return_value=sample_df):
            run_query(mock_settings, "SELECT 1", output_format=OutputFormat.csv, output_file=out)
        assert out.exists()
        content = out.read_text()
        assert "ATP" in content
        assert "GTP" in content

    def test_json_to_file(self, mock_settings, sample_df, tmp_path):
        out = tmp_path / "out.json"
        with patch("pdbminebuilder.commands.query._execute_query", return_value=sample_df):
            run_query(mock_settings, "SELECT 1", output_format=OutputFormat.json, output_file=out)
        assert out.exists()
        data = json.loads(out.read_text())
        assert len(data) == 2

    def test_parquet_to_file(self, mock_settings, sample_df, tmp_path):
        out = tmp_path / "out.parquet"
        with patch("pdbminebuilder.commands.query._execute_query", return_value=sample_df):
            run_query(
                mock_settings, "SELECT 1", output_format=OutputFormat.parquet, output_file=out
            )
        assert out.exists()
        result = pl.read_parquet(out)
        assert result.shape == (2, 2)

    def test_parquet_without_output_fails(self, mock_settings, sample_df):
        with patch("pdbminebuilder.commands.query._execute_query", return_value=sample_df):
            with pytest.raises(SystemExit):
                run_query(mock_settings, "SELECT 1", output_format=OutputFormat.parquet)

    def test_csv_to_stdout(self, mock_settings, sample_df, capsys):
        with patch("pdbminebuilder.commands.query._execute_query", return_value=sample_df):
            run_query(mock_settings, "SELECT 1", output_format=OutputFormat.csv)
        captured = capsys.readouterr()
        assert "ATP" in captured.out

    def test_json_to_stdout(self, mock_settings, sample_df, capsys):
        with patch("pdbminebuilder.commands.query._execute_query", return_value=sample_df):
            run_query(mock_settings, "SELECT 1", output_format=OutputFormat.json)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data) == 2
