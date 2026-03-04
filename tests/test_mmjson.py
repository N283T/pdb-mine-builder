"""Tests for mmJSON utilities."""

from mine2.parsers.mmjson import (
    clean_array,
    get_object_value,
    merge_data,
    mmjson_at,
    mmjson_at_ic,
    mmjson_get,
    normalize_column_name,
    remove_null,
)


class TestNormalizeColumnName:
    """Tests for normalize_column_name function."""

    def test_single_bracket(self):
        assert normalize_column_name("column[0]") == "column0"

    def test_double_bracket(self):
        assert (
            normalize_column_name("fract_transf_matrix[1][1]")
            == "fract_transf_matrix11"
        )

    def test_no_brackets(self):
        assert normalize_column_name("simple_name") == "simple_name"

    def test_multiple_digits(self):
        assert normalize_column_name("data[12][34]") == "data1234"


class TestMergeData:
    """Tests for merge_data function."""

    def test_base_only(self):
        base = {"category": [{"a": 1}]}
        plus = {}
        result = merge_data(base, plus)
        assert result == {"category": [{"a": 1}]}

    def test_plus_only(self):
        base = {}
        plus = {"category": [{"b": 2}]}
        result = merge_data(base, plus)
        assert result == {"category": [{"b": 2}]}

    def test_merge_rows(self):
        base = {"cat": [{"a": 1, "b": 2}]}
        plus = {"cat": [{"b": 3, "c": 4}]}
        result = merge_data(base, plus)
        # Plus takes precedence for 'b'
        assert result == {"cat": [{"a": 1, "b": 3, "c": 4}]}

    def test_metadata_plus_precedence(self):
        base = {"_block_name": "base"}
        plus = {"_block_name": "plus"}
        result = merge_data(base, plus)
        assert result["_block_name"] == "plus"


class TestMmjsonAt:
    """Tests for mmjson_at function."""

    def test_empty_rows(self):
        assert mmjson_at([], "value", "type", "SMILES") == []

    def test_no_match(self):
        rows = [{"type": "InChI", "value": "xyz"}]
        assert mmjson_at(rows, "value", "type", "SMILES") == []

    def test_single_match(self):
        rows = [
            {"type": "SMILES", "value": "CCO"},
            {"type": "InChI", "value": "xyz"},
        ]
        result = mmjson_at(rows, "value", "type", "SMILES")
        assert result == ["CCO"]

    def test_multiple_matches(self):
        rows = [
            {"type": "SMILES", "value": "CCO"},
            {"type": "SMILES", "value": "CC"},
            {"type": "InChI", "value": "xyz"},
        ]
        result = mmjson_at(rows, "value", "type", "SMILES")
        assert result == ["CCO", "CC"]

    def test_missing_get_field_skipped(self):
        rows = [
            {"type": "SMILES"},  # No 'value' field
            {"type": "SMILES", "value": "CCO"},
        ]
        # Missing field should be skipped (consistent with mmjson_at_ic)
        result = mmjson_at(rows, "value", "type", "SMILES")
        assert result == ["CCO"]


class TestMmjsonAtIc:
    """Tests for mmjson_at_ic function (case-insensitive)."""

    def test_empty_rows(self):
        assert mmjson_at_ic([], "value", "type", "SMILES") == []

    def test_case_insensitive_match(self):
        rows = [
            {"type": "smiles", "value": "CCO"},
            {"type": "SMILES", "value": "CC"},
            {"type": "Smiles", "value": "CCC"},
        ]
        result = mmjson_at_ic(rows, "value", "type", "SMILES")
        assert result == ["CCO", "CC", "CCC"]

    def test_no_match(self):
        rows = [{"type": "InChI", "value": "xyz"}]
        assert mmjson_at_ic(rows, "value", "type", "SMILES") == []

    def test_missing_get_field_skipped(self):
        rows = [
            {"type": "SMILES"},  # No 'value' field
            {"type": "SMILES", "value": "CCO"},
        ]
        # Missing field should be skipped, not raise error
        result = mmjson_at_ic(rows, "value", "type", "SMILES")
        assert result == ["CCO"]

    def test_none_cond_field_skipped(self):
        rows = [
            {"type": None, "value": "CCO"},
            {"type": "SMILES", "value": "CC"},
        ]
        result = mmjson_at_ic(rows, "value", "type", "SMILES")
        assert result == ["CC"]


class TestMmjsonGet:
    """Tests for mmjson_get function."""

    def test_empty_rows_no_index(self):
        assert mmjson_get([], "field") == []

    def test_empty_rows_with_index(self):
        assert mmjson_get([], "field", 0) is None

    def test_get_all_values(self):
        rows = [{"a": 1}, {"a": 2}, {"a": 3}]
        result = mmjson_get(rows, "a")
        assert result == [1, 2, 3]

    def test_get_value_at_index(self):
        rows = [{"a": 1}, {"a": 2}, {"a": 3}]
        assert mmjson_get(rows, "a", 0) == 1
        assert mmjson_get(rows, "a", 1) == 2
        assert mmjson_get(rows, "a", 2) == 3

    def test_index_out_of_range(self):
        rows = [{"a": 1}]
        assert mmjson_get(rows, "a", 10) is None

    def test_negative_index_out_of_range(self):
        rows = [{"a": 1}]
        assert mmjson_get(rows, "a", -1) is None

    def test_missing_field_returns_none(self):
        rows = [{"a": 1}, {"b": 2}]
        result = mmjson_get(rows, "a")
        assert result == [1, None]


class TestGetObjectValue:
    """Tests for get_object_value function."""

    def test_field_exists(self):
        obj = {"a": 1, "b": 2}
        assert get_object_value(obj, "a", 0) == 1

    def test_field_missing_returns_default(self):
        obj = {"a": 1}
        assert get_object_value(obj, "b", 99) == 99

    def test_default_can_be_any_type(self):
        obj = {}
        assert get_object_value(obj, "x", []) == []
        assert get_object_value(obj, "x", None) is None
        assert get_object_value(obj, "x", "default") == "default"


class TestCleanArray:
    """Tests for clean_array function."""

    def test_empty_array(self):
        assert clean_array([]) == []

    def test_removes_none(self):
        assert clean_array([1, None, 2]) == [1, 2]

    def test_removes_empty_string(self):
        assert clean_array(["a", "", "b"]) == ["a", "b"]

    def test_removes_duplicates(self):
        assert clean_array(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    def test_sorts_result(self):
        assert clean_array(["c", "a", "b"]) == ["a", "b", "c"]

    def test_combined(self):
        result = clean_array(["b", None, "a", "b", "", "c", None])
        assert result == ["a", "b", "c"]

    def test_numeric_values(self):
        result = clean_array([3, 1, 2, 1, None, 3])
        assert result == [1, 2, 3]

    def test_mixed_types_sortable(self):
        # Strings only - should sort
        result = clean_array(["z", "a", "m"])
        assert result == ["a", "m", "z"]


class TestRemoveNull:
    """Tests for remove_null function."""

    def test_empty_array(self):
        assert remove_null([]) == []

    def test_no_nulls(self):
        assert remove_null([1, 2, 3]) == [1, 2, 3]

    def test_removes_none(self):
        assert remove_null([1, None, 2, None, 3]) == [1, 2, 3]

    def test_all_none(self):
        assert remove_null([None, None]) == []

    def test_preserves_empty_string(self):
        # Unlike clean_array, remove_null only removes None
        assert remove_null(["a", "", "b"]) == ["a", "", "b"]

    def test_preserves_zero(self):
        assert remove_null([0, None, 1]) == [0, 1]

    def test_preserves_false(self):
        assert remove_null([True, None, False]) == [True, False]
