"""Tests for loader migration, normalization, and pruning logic."""

import logging
from unittest.mock import MagicMock, patch

from mine2.db.loader import (
    LoaderResult,
    SchemaDef,
    TableDef,
    _drop_all_foreign_keys,
    _normalize_type_name,
    migrate_table_schema,
)
from mine2.pipelines.base import BaseCifBatchPipeline


# =============================================================================
# _normalize_type_name tests
# =============================================================================


class TestNormalizeTypeName:
    """Tests for _normalize_type_name()."""

    def test_character_varying_to_text(self):
        assert _normalize_type_name("character varying") == "text"

    def test_character_to_char(self):
        assert _normalize_type_name("character") == "char"

    def test_character_n_to_char_n(self):
        assert _normalize_type_name("character(4)") == "char(4)"

    def test_character_n_with_spaces(self):
        assert _normalize_type_name("  character(10)  ") == "char(10)"

    def test_serial_to_integer(self):
        assert _normalize_type_name("serial") == "integer"

    def test_bigserial_to_bigint(self):
        assert _normalize_type_name("bigserial") == "bigint"

    def test_standard_types_passthrough(self):
        """Standard types should pass through unchanged."""
        standard = [
            "text",
            "integer",
            "bigint",
            "boolean",
            "date",
            "real",
            "double precision",
            "timestamp with time zone",
            "timestamp without time zone",
            "jsonb",
            "text[]",
            "integer[]",
            "boolean[]",
        ]
        for t in standard:
            assert _normalize_type_name(t) == t, f"Failed for type: {t}"

    def test_case_insensitive(self):
        assert _normalize_type_name("CHARACTER VARYING") == "text"
        assert _normalize_type_name("Character(4)") == "char(4)"

    def test_whitespace_stripped(self):
        assert _normalize_type_name("  text  ") == "text"


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

        from mine2.db.loader import delete_missing_entries

        with caplog.at_level(logging.WARNING, logger="mine2.loader"):
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

        from mine2.db.loader import delete_missing_entries

        result = delete_missing_entries(
            conninfo="postgresql://test",
            schema="test",
            pk_column="id",
            tables=[],
            keep_entry_ids=["A", "B"],
        )
        assert result == 0


# =============================================================================
# FK/PK migration behavior tests
# =============================================================================


class TestFkAndPkMigrationBehavior:
    """Tests for FK drop policy and PK migration SQL."""

    def test_drop_all_foreign_keys_executes_drop_statements(self):
        cur = MagicMock()
        cur.fetchall.return_value = [
            {"constraint_name": "fk_a"},
            {"constraint_name": "fk_b"},
        ]

        _drop_all_foreign_keys(cur, "test_schema", "my_table")

        assert cur.execute.call_count == 3
        first_call = cur.execute.call_args_list[0]
        assert first_call.args[1] == ("test_schema", "my_table")

    def test_drop_all_foreign_keys_no_constraints(self):
        cur = MagicMock()
        cur.fetchall.return_value = []

        _drop_all_foreign_keys(cur, "test_schema", "my_table")

        assert cur.execute.call_count == 1

    @patch("mine2.db.loader._ensure_indexes")
    @patch("mine2.db.loader._reconcile_unique_keys")
    @patch("mine2.db.loader._drop_all_foreign_keys")
    def test_migrate_table_schema_drops_fk_before_pk_reconcile(
        self,
        mock_drop_fks,
        _mock_reconcile_uks,
        _mock_ensure_indexes,
    ):
        cur = MagicMock()
        cur.fetchall.side_effect = [
            [{"column_name": "id", "data_type": "text"}],  # current columns
            [{"constraint_name": "my_table_pkey", "column_name": "id"}],  # current pk
            [],  # current unique keys
        ]
        table = TableDef(
            name="my_table",
            columns=[("id", "text")],
            primary_key=["id"],
        )

        migrate_table_schema(cur, "test_schema", table)

        mock_drop_fks.assert_called_once_with(cur, "test_schema", "my_table")

    def test_primary_key_drop_does_not_use_cascade(self):
        cur = MagicMock()
        cur.fetchall.side_effect = [
            [],  # current columns
            [{"constraint_name": "my_table_pkey", "column_name": "old_id"}],  # current pk
            [],  # current unique keys
        ]
        table = TableDef(
            name="my_table",
            columns=[("id", "text")],
            primary_key=["id"],
        )

        with patch("mine2.db.loader._drop_all_foreign_keys"), patch(
            "mine2.db.loader._ensure_indexes"
        ):
            migrate_table_schema(cur, "test_schema", table)

        executed_sql = [str(c.args[0]).lower() for c in cur.execute.call_args_list]
        assert any("drop constraint" in sql_text for sql_text in executed_sql)
        assert all("cascade" not in sql_text for sql_text in executed_sql)


# =============================================================================
# BaseCifBatchPipeline._prune_stale_rows tests
# =============================================================================


def _make_pipeline() -> BaseCifBatchPipeline:
    """Create a minimal BaseCifBatchPipeline for testing."""
    schema_def = SchemaDef(
        schema_name="test",
        primary_key="id",
        tables=[
            TableDef(
                name="t1",
                columns=[("id", "text"), ("val", "integer")],
                primary_key=["id"],
            )
        ],
    )
    settings = MagicMock()
    config = MagicMock()
    return BaseCifBatchPipeline(settings, config, schema_def)


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

    @patch("mine2.pipelines.base.delete_missing_entries", return_value=3)
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
