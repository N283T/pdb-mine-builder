"""Tests for base pipeline functionality."""

import pytest

from mine2.pipelines.base import _coerce_array_value, transform_category
from mine2.db.loader import TableDef


class TestCoerceArrayValue:
    """Tests for _coerce_array_value function."""

    def test_none_value_returns_none(self):
        assert _coerce_array_value(None, "text[]") is None
        assert _coerce_array_value(None, "integer[]") is None
        assert _coerce_array_value(None, "text") is None

    def test_non_array_column_returns_unchanged(self):
        assert _coerce_array_value("hello", "text") == "hello"
        assert _coerce_array_value(123, "integer") == 123
        assert _coerce_array_value(["a", "b"], "text") == ["a", "b"]

    def test_text_array_wraps_string(self):
        # String value should be wrapped in array
        result = _coerce_array_value("101d-A,B", "text[]")
        assert result == ["101d-A,B"]

    def test_text_array_preserves_list(self):
        # List value should be preserved
        result = _coerce_array_value(["a", "b", "c"], "text[]")
        assert result == ["a", "b", "c"]

    def test_text_array_converts_elements_to_strings(self):
        # Elements should be converted to strings
        result = _coerce_array_value([1, 2, 3], "text[]")
        assert result == ["1", "2", "3"]

    def test_text_array_handles_none_elements(self):
        result = _coerce_array_value(["a", None, "b"], "text[]")
        assert result == ["a", None, "b"]

    def test_integer_array_wraps_integer(self):
        result = _coerce_array_value(42, "integer[]")
        assert result == [42]

    def test_integer_array_converts_strings_to_ints(self):
        result = _coerce_array_value(["1", "2", "3"], "integer[]")
        assert result == [1, 2, 3]

    def test_integer_array_handles_invalid_values(self):
        result = _coerce_array_value(["1", "invalid", "3"], "integer[]")
        assert result == [1, None, 3]


class TestTransformCategory:
    """Tests for transform_category function."""

    @pytest.fixture
    def table_with_arrays(self):
        """Table definition with array columns."""
        return TableDef(
            name="test_table",
            columns=[
                ("pdbid", "text"),
                ("name", "text"),
                ("tags", "text[]"),
                ("counts", "integer[]"),
            ],
            primary_key=["pdbid"],
        )

    def test_empty_rows_returns_empty(self, table_with_arrays):
        result = transform_category([], table_with_arrays, "101d", "pdbid")
        assert result == []

    def test_basic_transform(self, table_with_arrays):
        rows = [{"name": "test"}]
        result = transform_category(rows, table_with_arrays, "101d", "pdbid")
        assert len(result) == 1
        assert result[0]["pdbid"] == "101d"
        assert result[0]["name"] == "test"

    def test_array_column_wraps_string(self, table_with_arrays):
        rows = [{"name": "test", "tags": "single-tag"}]
        result = transform_category(rows, table_with_arrays, "101d", "pdbid")
        assert result[0]["tags"] == ["single-tag"]

    def test_array_column_preserves_list(self, table_with_arrays):
        rows = [{"name": "test", "tags": ["tag1", "tag2"]}]
        result = transform_category(rows, table_with_arrays, "101d", "pdbid")
        assert result[0]["tags"] == ["tag1", "tag2"]

    def test_integer_array_column(self, table_with_arrays):
        rows = [{"name": "test", "counts": "42"}]
        result = transform_category(rows, table_with_arrays, "101d", "pdbid")
        assert result[0]["counts"] == [42]
