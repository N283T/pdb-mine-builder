"""Tests for parsers module."""

from mine2.parsers.cif import (
    _normalize_cif_value,
    parse_cif,
    parse_mmjson,
    parse_mmjson_blocks,
)
from mine2.parsers.mmjson import merge_data, normalize_column_name


class TestNormalizeCifValue:
    """Tests for _normalize_cif_value function."""

    def test_false_to_none(self) -> None:
        """CIF '.' (inapplicable) is converted to False by gemmi, then to None."""
        assert _normalize_cif_value(False) is None

    def test_none_unchanged(self) -> None:
        """CIF '?' (unknown) is converted to None by gemmi, stays None."""
        assert _normalize_cif_value(None) is None

    def test_string_unchanged(self) -> None:
        """Regular string values are unchanged."""
        assert _normalize_cif_value("hello") == "hello"

    def test_empty_string_unchanged(self) -> None:
        """Empty strings are unchanged."""
        assert _normalize_cif_value("") == ""

    def test_numeric_string_unchanged(self) -> None:
        """Numeric strings are unchanged (gemmi returns all values as strings)."""
        assert _normalize_cif_value("42") == "42"
        assert _normalize_cif_value("3.14") == "3.14"


class TestNormalizeColumnName:
    """Tests for normalize_column_name function."""

    def test_single_bracket(self) -> None:
        """Single bracket notation is normalized."""
        assert normalize_column_name("column[0]") == "column0"

    def test_double_bracket(self) -> None:
        """Double bracket notation is normalized."""
        assert (
            normalize_column_name("fract_transf_matrix[1][1]")
            == "fract_transf_matrix11"
        )

    def test_no_bracket(self) -> None:
        """Column without brackets is unchanged."""
        assert normalize_column_name("simple_column") == "simple_column"

    def test_multiple_brackets(self) -> None:
        """Multiple brackets are all normalized."""
        assert normalize_column_name("a[1][2][3]") == "a123"


class TestMergeData:
    """Tests for merge_data function."""

    def test_non_overlapping_categories(self) -> None:
        """Categories unique to each dict are preserved."""
        base = {"cat1": [{"a": 1}]}
        plus = {"cat2": [{"b": 2}]}
        result = merge_data(base, plus)

        assert "cat1" in result
        assert "cat2" in result
        assert result["cat1"] == [{"a": 1}]
        assert result["cat2"] == [{"b": 2}]

    def test_overlapping_categories_merge_columns(self) -> None:
        """Overlapping categories merge row columns, plus takes precedence."""
        base = {"entry": [{"id": "TEST", "title": "Base Title"}]}
        plus = {"entry": [{"id": "PLUS", "keywords": "extra"}]}
        result = merge_data(base, plus)

        assert result["entry"] == [
            {"id": "PLUS", "title": "Base Title", "keywords": "extra"}
        ]

    def test_different_row_counts(self) -> None:
        """Categories with different row counts use max rows."""
        base = {"atoms": [{"id": "1"}, {"id": "2"}, {"id": "3"}]}
        plus = {"atoms": [{"x": "1.0"}]}  # Only 1 row
        result = merge_data(base, plus)

        assert len(result["atoms"]) == 3
        assert result["atoms"][0] == {"id": "1", "x": "1.0"}
        assert result["atoms"][1] == {"id": "2"}
        assert result["atoms"][2] == {"id": "3"}

    def test_metadata_plus_takes_precedence(self) -> None:
        """Metadata keys (starting with _) from plus take precedence."""
        base = {"_block_name": "BASE", "entry": [{"id": "1"}]}
        plus = {"_block_name": "PLUS"}
        result = merge_data(base, plus)

        assert result["_block_name"] == "PLUS"

    def test_empty_base(self) -> None:
        """Empty base returns plus data."""
        base: dict = {}
        plus = {"entry": [{"id": "TEST"}]}
        result = merge_data(base, plus)

        assert result == {"entry": [{"id": "TEST"}]}

    def test_empty_plus(self) -> None:
        """Empty plus returns base data."""
        base = {"entry": [{"id": "TEST"}]}
        plus: dict = {}
        result = merge_data(base, plus)

        assert result == {"entry": [{"id": "TEST"}]}


class TestParseCif:
    """Tests for CIF parsing functions."""

    def test_parse_cif_simple(self) -> None:
        """Parse simple CIF content."""
        cif_content = """data_TEST
_entry.id TEST
"""
        result = parse_cif(cif_content)

        assert result["_block_name"] == "TEST"
        assert result["entry"] == [{"id": "TEST"}]

    def test_parse_cif_loop(self) -> None:
        """Parse CIF with loop (table) data."""
        cif_content = """data_TEST
loop_
_atom_site.id
_atom_site.type_symbol
1 C
2 N
"""
        result = parse_cif(cif_content)

        assert result["atom_site"] == [
            {"id": "1", "type_symbol": "C"},
            {"id": "2", "type_symbol": "N"},
        ]

    def test_parse_cif_special_values(self) -> None:
        """CIF special values ? and . are converted to None."""
        cif_content = """data_TEST
loop_
_test.id
_test.val1
_test.val2
1 ? .
"""
        result = parse_cif(cif_content)

        assert result["test"] == [{"id": "1", "val1": None, "val2": None}]


class TestParseMmjson:
    """Tests for mmJSON parsing functions."""

    def test_parse_mmjson_simple(self) -> None:
        """Parse simple mmJSON content."""
        mmjson = """
{
  "data_TEST": {
    "entry": {
      "id": ["TEST"]
    }
  }
}
"""
        result = parse_mmjson(mmjson)

        assert result["_block_name"] == "TEST"
        assert result["entry"] == [{"id": "TEST"}]

    def test_parse_mmjson_multiple_rows(self) -> None:
        """Parse mmJSON with multiple rows."""
        mmjson = """
{
  "data_TEST": {
    "atom_site": {
      "id": ["1", "2"],
      "type_symbol": ["C", "N"]
    }
  }
}
"""
        result = parse_mmjson(mmjson)

        assert result["atom_site"] == [
            {"id": "1", "type_symbol": "C"},
            {"id": "2", "type_symbol": "N"},
        ]

    def test_parse_mmjson_blocks_multiple(self) -> None:
        """Parse mmJSON with multiple data blocks."""
        import gemmi

        mmjson = """
{
  "data_PRD_000001": {
    "pdbx_reference_molecule": {
      "name": ["Test Molecule"]
    }
  },
  "data_PRDCC_000001": {
    "chem_comp": {
      "id": ["ATP"]
    }
  }
}
"""
        doc = gemmi.cif.read_mmjson_string(mmjson)
        blocks = parse_mmjson_blocks(doc)

        assert "PRD_000001" in blocks
        assert "PRDCC_000001" in blocks
        assert blocks["PRD_000001"]["pdbx_reference_molecule"] == [
            {"name": "Test Molecule"}
        ]
        assert blocks["PRDCC_000001"]["chem_comp"] == [{"id": "ATP"}]
