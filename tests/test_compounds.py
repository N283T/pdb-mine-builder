"""Tests for chem.compounds table and refresh logic."""

from unittest.mock import MagicMock, patch

from pdbminebuilder.commands.compounds import (
    _ensure_schema_and_table,
    _insert_cc_compounds,
    _insert_prd_compounds,
    refresh_compounds,
)
from pdbminebuilder.models.chem import compounds, metadata


class TestChemModel:
    """Tests for chem.compounds model definition."""

    def test_schema_is_chem(self) -> None:
        """Schema should be 'chem'."""
        assert metadata.schema == "chem"

    def test_entry_pk_is_id(self) -> None:
        """Entry PK should be 'id'."""
        assert metadata.info["entry_pk"] == "id"

    def test_compounds_table_exists(self) -> None:
        """Compounds table should exist in metadata."""
        assert "chem.compounds" in metadata.tables

    def test_compounds_has_expected_columns(self) -> None:
        """Compounds table should have all expected columns."""
        col_names = {c.name for c in compounds.columns}
        expected = {
            "id",
            "source",
            "canonical_smiles",
            "name",
            "formula",
            "cc_comp_ids",
        }
        assert expected == col_names

    def test_primary_key(self) -> None:
        """Primary key should be (source, id)."""
        pk_cols = [c.name for c in compounds.primary_key.columns]
        assert pk_cols == ["source", "id"]


class TestEnsureSchemaAndTable:
    """Tests for _ensure_schema_and_table function."""

    def test_creates_schema_and_table_when_not_exists(self) -> None:
        """Creates chem schema and compounds table when they don't exist."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (False,)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch(
            "pdbminebuilder.commands.compounds.psycopg.connect",
            return_value=mock_conn,
        ):
            _ensure_schema_and_table("test_conninfo")

        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )
        assert "CREATE SCHEMA IF NOT EXISTS chem" in all_sql
        assert "CREATE TABLE chem.compounds" in all_sql
        mock_conn.commit.assert_called_once()

    def test_skips_create_when_table_exists(self) -> None:
        """Does not CREATE TABLE if it already exists."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (True,)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch(
            "pdbminebuilder.commands.compounds.psycopg.connect",
            return_value=mock_conn,
        ):
            _ensure_schema_and_table("test_conninfo")

        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )
        assert "CREATE TABLE" not in all_sql


class TestRefreshCompounds:
    """Tests for refresh_compounds function."""

    def test_aborts_when_not_confirmed(self) -> None:
        """Aborts when user declines confirmation prompt."""
        mock_settings = MagicMock()
        with (
            patch(
                "pdbminebuilder.commands.compounds.Confirm.ask",
                return_value=False,
            ),
            patch(
                "pdbminebuilder.commands.compounds._ensure_schema_and_table",
            ) as mock_ensure,
        ):
            refresh_compounds(mock_settings, force=False)

        # Should not have attempted any DB operations
        mock_ensure.assert_not_called()

    def test_force_skips_confirmation(self) -> None:
        """force=True skips the confirmation prompt."""
        mock_settings = MagicMock()
        mock_settings.rdb.constring = "test_conninfo"

        with (
            patch(
                "pdbminebuilder.commands.compounds._ensure_schema_and_table",
            ) as mock_ensure,
            patch(
                "pdbminebuilder.commands.compounds.ensure_rdkit_setup",
            ),
            patch(
                "pdbminebuilder.commands.compounds.psycopg.connect",
            ) as mock_connect,
            patch(
                "pdbminebuilder.commands.compounds.Confirm.ask",
            ) as mock_confirm,
        ):
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 0
            mock_conn = MagicMock()
            mock_conn.cursor.return_value.__enter__ = MagicMock(
                return_value=mock_cursor
            )
            mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
            mock_conn.__enter__ = MagicMock(return_value=mock_conn)
            mock_conn.__exit__ = MagicMock(return_value=False)
            mock_connect.return_value = mock_conn

            refresh_compounds(mock_settings, force=True)

            mock_confirm.assert_not_called()
            mock_ensure.assert_called_once_with("test_conninfo")

    def test_truncates_and_inserts(self) -> None:
        """Truncates table and inserts from both sources."""
        mock_settings = MagicMock()
        mock_settings.rdb.constring = "test_conninfo"

        with (
            patch("pdbminebuilder.commands.compounds._ensure_schema_and_table"),
            patch("pdbminebuilder.commands.compounds.ensure_rdkit_setup"),
            patch(
                "pdbminebuilder.commands.compounds.psycopg.connect",
            ) as mock_connect,
        ):
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 5
            mock_conn = MagicMock()
            mock_conn.cursor.return_value.__enter__ = MagicMock(
                return_value=mock_cursor
            )
            mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
            mock_conn.__enter__ = MagicMock(return_value=mock_conn)
            mock_conn.__exit__ = MagicMock(return_value=False)
            mock_connect.return_value = mock_conn

            refresh_compounds(mock_settings, force=True)

            all_sql = " ".join(
                str(call[0][0]) for call in mock_cursor.execute.call_args_list
            )
            assert "TRUNCATE" in all_sql
            assert "cc.brief_summary" in all_sql
            assert "prd.brief_summary" in all_sql
            mock_conn.commit.assert_called_once()


class TestInsertCcCompounds:
    """Tests for _insert_cc_compounds function."""

    def test_executes_insert_sql(self) -> None:
        """Should execute INSERT INTO chem.compounds from cc.brief_summary."""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 42

        result = _insert_cc_compounds(mock_cursor)

        assert result == 42
        sql = mock_cursor.execute.call_args[0][0]
        assert "cc.brief_summary" in sql
        assert "chem.compounds" in sql
        assert "'cc'" in sql


class TestInsertPrdCompounds:
    """Tests for _insert_prd_compounds function."""

    def test_executes_insert_sql(self) -> None:
        """Should execute INSERT INTO chem.compounds from prd.brief_summary."""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 10

        result = _insert_prd_compounds(mock_cursor)

        assert result == 10
        sql = mock_cursor.execute.call_args[0][0]
        assert "prd.brief_summary" in sql
        assert "chem.compounds" in sql
        assert "'prd'" in sql
        assert "chem_comp_id" in sql
