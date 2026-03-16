"""Tests for chem.compounds table and refresh logic."""

from unittest.mock import MagicMock


from pdbminebuilder.commands.compounds import (
    _insert_cc_compounds,
    _insert_prd_compounds,
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
