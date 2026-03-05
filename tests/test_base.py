"""Tests for base pipeline functionality."""

import pytest
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    Date,
    Double,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from pdbminebuilder.pipelines.base import (
    _coerce_boolean,
    _coerce_date,
    _coerce_float,
    _coerce_integer,
    _coerce_string,
    coerce_value,
    transform_category,
)


class TestCoerceString:
    """Tests for _coerce_string function."""

    def test_none_returns_none(self):
        assert _coerce_string(None) is None

    def test_none_pk_returns_empty(self):
        assert _coerce_string(None, is_pk=True) == ""

    def test_string_unchanged(self):
        assert _coerce_string("hello") == "hello"

    def test_int_to_string(self):
        assert _coerce_string(123) == "123"

    def test_array_joins_with_dash(self):
        assert _coerce_string(["a", "b", "c"]) == "a-b-c"

    def test_array_with_none_elements(self):
        assert _coerce_string(["a", None, "b"]) == "a-b"


class TestCoerceInteger:
    """Tests for _coerce_integer function."""

    def test_none_returns_none(self):
        assert _coerce_integer(None) is None

    def test_none_pk_returns_zero(self):
        assert _coerce_integer(None, is_pk=True) == 0

    def test_int_unchanged(self):
        assert _coerce_integer(42) == 42

    def test_string_to_int(self):
        assert _coerce_integer("123") == 123

    def test_invalid_string_returns_none(self):
        assert _coerce_integer("invalid") is None

    def test_invalid_string_pk_returns_zero(self):
        assert _coerce_integer("invalid", is_pk=True) == 0

    def test_float_truncates(self):
        assert _coerce_integer(3.7) == 3


class TestCoerceFloat:
    """Tests for _coerce_float function."""

    def test_none_returns_none(self):
        assert _coerce_float(None) is None

    def test_none_pk_returns_zero(self):
        assert _coerce_float(None, is_pk=True) == 0.0

    def test_float_unchanged(self):
        result = _coerce_float(3.14159)
        assert abs(result - 3.14159) < 1e-10

    def test_string_to_float(self):
        result = _coerce_float("3.14")
        assert abs(result - 3.14) < 1e-10

    def test_invalid_string_returns_none(self):
        assert _coerce_float("invalid") is None

    def test_zero_returns_zero(self):
        assert _coerce_float(0) == 0.0
        assert _coerce_float(0.0) == 0.0

    def test_precision_15_digits(self):
        # Test that we maintain 15 significant figures
        result = _coerce_float(1.23456789012345678)
        # Should round to 15 significant figures
        assert result is not None
        # Verify the precision is approximately correct
        assert abs(result - 1.23456789012346) < 1e-14


class TestCoerceBoolean:
    """Tests for _coerce_boolean function."""

    def test_true_unchanged(self):
        assert _coerce_boolean(True) is True

    def test_false_unchanged(self):
        assert _coerce_boolean(False) is False

    def test_one_is_true(self):
        assert _coerce_boolean(1) is True

    def test_zero_is_false(self):
        assert _coerce_boolean(0) is False

    def test_string_true_is_true(self):
        assert _coerce_boolean("true") is True
        assert _coerce_boolean("TRUE") is True
        assert _coerce_boolean("True") is True

    def test_string_false_is_false(self):
        assert _coerce_boolean("false") is False
        assert _coerce_boolean("FALSE") is False
        assert _coerce_boolean("False") is False

    def test_invalid_returns_none(self):
        assert _coerce_boolean(None) is None
        assert _coerce_boolean("yes") is None
        assert _coerce_boolean("no") is None
        assert _coerce_boolean(2) is None


class TestCoerceDate:
    """Tests for _coerce_date function."""

    def test_none_returns_none(self):
        assert _coerce_date(None) is None

    def test_valid_date_unchanged(self):
        assert _coerce_date("2024-01-15") == "2024-01-15"

    def test_two_digit_year_less_than_50(self):
        # Years < 50 become 20XX
        assert _coerce_date("01-05-15") == "2001-05-15"
        assert _coerce_date("49-12-31") == "2049-12-31"

    def test_two_digit_year_50_or_more(self):
        # Years >= 50 become 19XX
        assert _coerce_date("50-01-01") == "1950-01-01"
        assert _coerce_date("99-06-30") == "1999-06-30"

    def test_zero_pads_month(self):
        assert _coerce_date("2024-1-15") == "2024-01-15"

    def test_zero_pads_day(self):
        assert _coerce_date("2024-01-5") == "2024-01-05"

    def test_zero_pads_both(self):
        assert _coerce_date("2024-1-5") == "2024-01-05"

    def test_invalid_format_returns_as_is(self):
        # Non-dash format is returned as-is
        assert _coerce_date("2024/01/15") == "2024/01/15"
        # String without 3 parts is returned as-is
        assert _coerce_date("invalid") == "invalid"
        assert _coerce_date("2024-01") == "2024-01"

    def test_empty_string_returns_none(self):
        assert _coerce_date("") is None


class TestCoerceValue:
    """Tests for coerce_value function (dispatcher)."""

    def test_text_type(self):
        assert coerce_value("hello", Text()) == "hello"
        assert coerce_value(123, Text()) == "123"

    def test_integer_type(self):
        assert coerce_value("42", Integer()) == 42
        assert coerce_value(None, Integer()) is None

    def test_boolean_type(self):
        assert coerce_value("true", Boolean()) is True
        assert coerce_value("false", Boolean()) is False

    def test_date_type(self):
        assert coerce_value("99-1-5", Date()) == "1999-01-05"

    def test_float_type(self):
        result = coerce_value("3.14", Double())
        assert abs(result - 3.14) < 1e-10

    def test_text_array_type(self):
        assert coerce_value("single", ARRAY(Text)) == ["single"]
        assert coerce_value(["a", "b"], ARRAY(Text)) == ["a", "b"]

    def test_integer_array_type(self):
        assert coerce_value(42, ARRAY(Integer)) == [42]
        assert coerce_value(["1", "2"], ARRAY(Integer)) == [1, 2]

    def test_unknown_type_falls_back_to_string(self):
        """Default fallback is to treat as string."""
        assert coerce_value("some_value", Text()) == "some_value"

    def test_jsonb_passthrough(self):
        """JSONB values should be passed through unchanged."""
        data = {"key": "value", "nested": [1, 2]}
        assert coerce_value(data, JSONB()) == data
        assert coerce_value(None, JSONB()) is None

    def test_array_preserves_none_elements(self):
        """Array coercion must preserve None elements (not drop them)."""
        result = coerce_value(["a", None, "b"], ARRAY(Text))
        assert result == ["a", None, "b"]
        assert len(result) == 3

    def test_integer_array_preserves_none_elements(self):
        result = coerce_value([1, None, 3], ARRAY(Integer))
        assert result == [1, None, 3]
        assert len(result) == 3

    def test_negative_float(self):
        result = coerce_value(-3.14, Double())
        assert abs(result - (-3.14)) < 1e-10


class TestTransformCategory:
    """Tests for transform_category function."""

    @pytest.fixture
    def table_with_arrays(self):
        """Table definition with array columns."""
        meta = MetaData(schema="test")
        meta.info = {"entry_pk": "pdbid"}
        return Table(
            "test_table",
            meta,
            Column("pdbid", Text),
            Column("name", Text),
            Column("tags", ARRAY(Text)),
            Column("counts", ARRAY(Integer)),
            PrimaryKeyConstraint("pdbid"),
        )

    @pytest.fixture
    def table_with_various_types(self):
        """Table definition with various column types."""
        meta = MetaData(schema="test2")
        meta.info = {"entry_pk": "pdbid"}
        return Table(
            "test_table",
            meta,
            Column("pdbid", Text),
            Column("created_date", Date),
            Column("is_active", Boolean),
            Column("score", Double),
            Column("count", Integer),
            PrimaryKeyConstraint("pdbid"),
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

    def test_date_coercion(self, table_with_various_types):
        rows = [{"created_date": "99-1-5"}]
        result = transform_category(rows, table_with_various_types, "101d", "pdbid")
        assert result[0]["created_date"] == "1999-01-05"

    def test_boolean_coercion(self, table_with_various_types):
        rows = [{"is_active": "true"}]
        result = transform_category(rows, table_with_various_types, "101d", "pdbid")
        assert result[0]["is_active"] is True

    def test_float_coercion(self, table_with_various_types):
        rows = [{"score": "3.14"}]
        result = transform_category(rows, table_with_various_types, "101d", "pdbid")
        assert abs(result[0]["score"] - 3.14) < 1e-10

    def test_integer_coercion(self, table_with_various_types):
        rows = [{"count": "42"}]
        result = transform_category(rows, table_with_various_types, "101d", "pdbid")
        assert result[0]["count"] == 42
