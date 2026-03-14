"""Tests for schema command."""

import pytest

from pdbminebuilder.commands.schema import (
    _redact_conninfo,
    describe_column,
    describe_table,
    describe_schema_full,
    list_schemas,
    list_tables,
    render_column_detail,
    render_columns,
    render_schemas,
    render_search_results,
    render_tables,
    search_columns,
    to_json,
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


class TestRedactConninfo:
    """Tests for _redact_conninfo."""

    def test_redacts_password(self) -> None:
        """Should redact password from conninfo."""
        conninfo = "host=localhost port=5433 dbname=pmb user=pdbj password=secret"
        result = _redact_conninfo(conninfo)
        assert "secret" not in result
        assert "password=****" in result

    def test_no_password_unchanged(self) -> None:
        """Conninfo without password should be unchanged."""
        conninfo = "host=localhost port=5433 dbname=pmb user=pdbj"
        result = _redact_conninfo(conninfo)
        assert result == conninfo


class TestRenderSmoke:
    """Smoke tests for render functions."""

    def test_render_schemas(self) -> None:
        """render_schemas should not raise."""
        render_schemas(conninfo="host=localhost dbname=test")

    def test_render_tables(self) -> None:
        """render_tables should not raise."""
        render_tables("pdbj")

    def test_render_columns(self) -> None:
        """render_columns should not raise."""
        render_columns("pdbj", "brief_summary")

    def test_render_column_detail(self) -> None:
        """render_column_detail should not raise."""
        render_column_detail("pdbj", "brief_summary", "pdbid")

    def test_render_search_results(self) -> None:
        """render_search_results should not raise."""
        results = search_columns("pdbid")
        render_search_results("pdbid", results)

    def test_render_search_results_empty(self) -> None:
        """render_search_results with no matches should not raise."""
        render_search_results("xyzzy_nonexistent", [])


class TestSearchColumns:
    """Tests for search_columns."""

    def test_finds_by_column_name(self) -> None:
        """Should find columns matching by name."""
        results = search_columns("pdbid")
        assert len(results) > 0
        assert all("pdbid" in r.column.lower() for r in results)

    def test_finds_by_comment(self) -> None:
        """Should find columns matching by comment text."""
        results = search_columns("deposition date")
        assert len(results) > 0
        assert any("deposition" in (r.comment or "").lower() for r in results)

    def test_case_insensitive(self) -> None:
        """Search should be case-insensitive."""
        results_lower = search_columns("pdbid")
        results_upper = search_columns("PDBID")
        assert len(results_lower) == len(results_upper)

    def test_no_results(self) -> None:
        """Should return empty list for no matches."""
        results = search_columns("xyzzy_nonexistent_12345")
        assert results == []

    def test_result_has_schema_and_table(self) -> None:
        """Each result should include schema and table info."""
        results = search_columns("resolution")
        assert len(results) > 0
        for r in results:
            assert r.schema
            assert r.table
            assert r.column

    def test_searches_across_schemas(self) -> None:
        """Should find matches across multiple schemas."""
        results = search_columns("pdbid")
        schemas = {r.schema for r in results}
        assert len(schemas) > 1


class TestDescribeSchemaFull:
    """Tests for describe_schema_full."""

    def test_returns_all_tables_with_columns(self) -> None:
        """Should return all tables with their columns."""
        result = describe_schema_full("contacts")
        assert "schema" in result
        assert result["schema"] == "contacts"
        assert "tables" in result
        assert len(result["tables"]) > 0
        first_table = result["tables"][0]
        assert "name" in first_table
        assert "columns" in first_table
        assert len(first_table["columns"]) > 0

    def test_columns_have_all_fields(self) -> None:
        """Each column should have name, type_str, nullable, primary_key, comment."""
        result = describe_schema_full("contacts")
        col = result["tables"][0]["columns"][0]
        assert "name" in col
        assert "type_str" in col
        assert "nullable" in col
        assert "primary_key" in col
        assert "comment" in col

    def test_unknown_schema_raises(self) -> None:
        """Unknown schema should raise KeyError."""
        with pytest.raises(KeyError):
            describe_schema_full("nonexistent")


class TestToJson:
    """Tests for to_json."""

    def test_schemas_json(self) -> None:
        """Should produce valid JSON for schemas."""
        import json

        schemas = list_schemas()
        output = to_json(schemas)
        parsed = json.loads(output)
        assert isinstance(parsed, list)
        assert len(parsed) > 0
        assert "name" in parsed[0]

    def test_schema_full_json(self) -> None:
        """Should produce valid JSON for full schema."""
        import json

        result = describe_schema_full("contacts")
        output = to_json(result)
        parsed = json.loads(output)
        assert parsed["schema"] == "contacts"
        assert "tables" in parsed

    def test_search_results_json(self) -> None:
        """Should produce valid JSON for search results."""
        import json

        results = search_columns("pdbid")
        output = to_json(results)
        parsed = json.loads(output)
        assert isinstance(parsed, list)
        assert len(parsed) > 0

    def test_column_detail_json(self) -> None:
        """Should produce valid JSON for column detail."""
        import json

        detail = describe_column("pdbj", "brief_summary", "pdbid")
        output = to_json(detail)
        parsed = json.loads(output)
        assert parsed["name"] == "pdbid"
