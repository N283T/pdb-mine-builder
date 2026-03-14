"""Tests for schema command."""

import pytest

from pdbminebuilder.commands.schema import (
    describe_column,
    describe_table,
    list_schemas,
    list_tables,
)


class TestListSchemas:
    """Tests for list_schemas."""

    def test_returns_all_known_schemas(self) -> None:
        """Should return all registered schema names."""
        schemas = list_schemas()
        names = [s.name for s in schemas]
        assert "pdbj" in names
        assert "cc" in names
        assert "vrpt" in names
        assert "contacts" in names

    def test_returns_sorted(self) -> None:
        """Schema names should be sorted alphabetically."""
        schemas = list_schemas()
        names = [s.name for s in schemas]
        assert names == sorted(names)

    def test_includes_table_count(self) -> None:
        """Each schema entry should include a table count."""
        schemas = list_schemas()
        for schema in schemas:
            assert schema.table_count > 0


class TestListTables:
    """Tests for list_tables."""

    def test_pdbj_has_tables(self) -> None:
        """pdbj schema should have tables."""
        tables = list_tables("pdbj")
        assert len(tables) > 0

    def test_table_has_column_count(self) -> None:
        """Each table entry should have a column count."""
        tables = list_tables("pdbj")
        for t in tables:
            assert t.column_count > 0

    def test_unknown_schema_raises(self) -> None:
        """Unknown schema should raise KeyError."""
        with pytest.raises(KeyError):
            list_tables("nonexistent")

    def test_brief_summary_in_pdbj(self) -> None:
        """brief_summary should be in pdbj tables."""
        tables = list_tables("pdbj")
        names = [t.name for t in tables]
        assert "brief_summary" in names


class TestDescribeTable:
    """Tests for describe_table."""

    def test_returns_columns(self) -> None:
        """Should return column info for a valid table."""
        columns = describe_table("pdbj", "brief_summary")
        assert len(columns) > 0

    def test_column_has_name_and_type(self) -> None:
        """Each column should have name and type."""
        columns = describe_table("pdbj", "brief_summary")
        for col in columns:
            assert col.name
            assert col.type_str

    def test_pdbid_has_comment(self) -> None:
        """pdbid column in pdbj.brief_summary should have a comment."""
        columns = describe_table("pdbj", "brief_summary")
        pdbid = next(c for c in columns if c.name == "pdbid")
        assert pdbid.comment is not None
        assert "PDBID" in pdbid.comment

    def test_unknown_table_raises(self) -> None:
        """Unknown table should raise KeyError."""
        with pytest.raises(KeyError):
            describe_table("pdbj", "nonexistent_table")

    def test_unknown_schema_raises(self) -> None:
        """Unknown schema should raise KeyError."""
        with pytest.raises(KeyError):
            describe_table("nonexistent", "brief_summary")


class TestDescribeColumn:
    """Tests for describe_column."""

    def test_returns_column_detail(self) -> None:
        """Should return detail for a valid column."""
        detail = describe_column("pdbj", "brief_summary", "pdbid")
        assert detail.name == "pdbid"
        assert detail.type_str == "TEXT"
        assert detail.comment is not None

    def test_includes_nullable(self) -> None:
        """Should include nullable info."""
        detail = describe_column("pdbj", "brief_summary", "pdbid")
        assert isinstance(detail.nullable, bool)

    def test_includes_primary_key(self) -> None:
        """Should include primary key info."""
        detail = describe_column("contacts", "brief_summary", "pdbid")
        assert detail.primary_key is True

    def test_unknown_column_raises(self) -> None:
        """Unknown column should raise KeyError."""
        with pytest.raises(KeyError):
            describe_column("pdbj", "brief_summary", "nonexistent_col")
