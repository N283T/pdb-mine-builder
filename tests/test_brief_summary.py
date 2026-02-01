"""Tests for brief_summary utilities."""

import pytest

from mine2.utils.brief_summary import (
    clean_array,
    gen_docid,
    generate_brief_summary,
    get_all_values,
    get_first_value,
    get_values_where,
)


class TestGenDocid:
    """Tests for gen_docid function."""

    def test_standard_4char_pdbid(self):
        """Test standard 4-character PDB ID."""
        # "100d" -> ljust(4) = "100d" -> rjust(8, "0") = "0000100d"
        result = gen_docid("100d")
        assert isinstance(result, int)
        assert result > 0

    def test_standard_pdbid_1abc(self):
        """Test another standard PDB ID."""
        result = gen_docid("1abc")
        assert isinstance(result, int)
        assert result > 0

    def test_deterministic(self):
        """Test that same input produces same output."""
        assert gen_docid("100d") == gen_docid("100d")
        assert gen_docid("1abc") == gen_docid("1abc")

    def test_different_ids_different_docids(self):
        """Test that different PDB IDs produce different docids."""
        assert gen_docid("100d") != gen_docid("1abc")
        assert gen_docid("1a00") != gen_docid("1a01")

    def test_short_pdbid(self):
        """Test short PDB ID (less than 4 chars)."""
        # "ab" -> ljust(4) = "ab  " -> rjust(8, "0") = "0000ab  "
        result = gen_docid("ab")
        assert isinstance(result, int)
        assert result > 0

    def test_extended_8char_pdbid(self):
        """Test extended 8-character PDB ID (alphanumeric only)."""
        # Extended PDB IDs use alphanumeric characters only
        # Example: "pdb00001" (8 chars, no underscore)
        result = gen_docid("pdb00001")
        assert isinstance(result, int)
        assert result > 0

    def test_lowercase_only(self):
        """Test that lowercase letters work."""
        result = gen_docid("abcd")
        assert isinstance(result, int)

    def test_numbers_only(self):
        """Test that numbers only work."""
        result = gen_docid("1234")
        assert isinstance(result, int)

    def test_fits_in_bigint(self):
        """Test that result fits in PostgreSQL bigint."""
        max_bigint = 2**63 - 1
        # Test various IDs
        for pdbid in ["100d", "zzzz", "0000", "9999"]:
            result = gen_docid(pdbid)
            assert result <= max_bigint


class TestGetFirstValue:
    """Tests for get_first_value function."""

    def test_empty_rows(self):
        """Test with empty rows."""
        assert get_first_value([], "field") is None

    def test_single_row_with_value(self):
        """Test with single row containing the field."""
        rows = [{"field": "value"}]
        assert get_first_value(rows, "field") == "value"

    def test_single_row_without_field(self):
        """Test with single row not containing the field."""
        rows = [{"other": "value"}]
        assert get_first_value(rows, "field") is None

    def test_multiple_rows_first_has_value(self):
        """Test with multiple rows, first has value."""
        rows = [{"field": "first"}, {"field": "second"}]
        assert get_first_value(rows, "field") == "first"

    def test_multiple_rows_first_null(self):
        """Test with multiple rows, first has None."""
        rows = [{"field": None}, {"field": "second"}]
        assert get_first_value(rows, "field") == "second"


class TestGetAllValues:
    """Tests for get_all_values function."""

    def test_empty_rows(self):
        """Test with empty rows."""
        assert get_all_values([], "field") == []

    def test_single_row_with_value(self):
        """Test with single row containing the field."""
        rows = [{"field": "value"}]
        assert get_all_values(rows, "field") == ["value"]

    def test_multiple_values(self):
        """Test with multiple rows."""
        rows = [{"field": "a"}, {"field": "b"}, {"field": "c"}]
        assert get_all_values(rows, "field") == ["a", "b", "c"]

    def test_skips_none_values(self):
        """Test that None values are skipped."""
        rows = [{"field": "a"}, {"field": None}, {"field": "c"}]
        assert get_all_values(rows, "field") == ["a", "c"]


class TestGetValuesWhere:
    """Tests for get_values_where function."""

    def test_empty_rows(self):
        """Test with empty rows."""
        assert get_values_where([], "get", "cond", "val") == []

    def test_matching_condition(self):
        """Test with matching condition."""
        rows = [
            {"id": "primary", "value": "first"},
            {"id": "secondary", "value": "second"},
        ]
        assert get_values_where(rows, "value", "id", "primary") == ["first"]

    def test_multiple_matches(self):
        """Test with multiple matching conditions."""
        rows = [
            {"type": "UNP", "code": "P12345"},
            {"type": "GB", "code": "ABC123"},
            {"type": "UNP", "code": "Q67890"},
        ]
        assert get_values_where(rows, "code", "type", "UNP") == ["P12345", "Q67890"]

    def test_no_matches(self):
        """Test with no matching condition."""
        rows = [{"type": "GB", "code": "ABC123"}]
        assert get_values_where(rows, "code", "type", "UNP") == []


class TestCleanArray:
    """Tests for clean_array function."""

    def test_empty_array(self):
        """Test with empty array."""
        assert clean_array([]) == []

    def test_removes_none(self):
        """Test that None values are removed."""
        assert clean_array([1, None, 2, None]) == [1, 2]

    def test_removes_empty_strings(self):
        """Test that empty strings are removed."""
        assert clean_array(["a", "", "b", ""]) == ["a", "b"]

    def test_removes_duplicates(self):
        """Test that duplicates are removed."""
        assert clean_array([1, 2, 1, 3, 2]) == [1, 2, 3]

    def test_preserves_order(self):
        """Test that order is preserved (first occurrence)."""
        assert clean_array([3, 1, 2, 1, 3]) == [3, 1, 2]


class TestGenerateBriefSummary:
    """Tests for generate_brief_summary function."""

    def test_minimal_data(self):
        """Test with minimal data (just entry_id)."""
        result = generate_brief_summary({}, "100d")
        assert result["pdbid"] == "100d"
        assert result["docid"] == gen_docid("100d")
        assert result["deposition_date"] is None
        assert result["release_date"] is None
        assert result["modification_date"] is None

    def test_with_dates(self):
        """Test with date fields populated."""
        data = {
            "pdbx_database_status": [{"recvd_initial_deposition_date": "2020-01-15"}],
            "pdbx_audit_revision_history": [
                {"revision_date": "2020-02-01"},
                {"revision_date": "2021-03-15"},
            ],
        }
        result = generate_brief_summary(data, "100d")
        assert result["deposition_date"] == "2020-01-15"
        assert result["release_date"] == "2020-02-01"
        assert result["modification_date"] == "2021-03-15"

    def test_with_authors(self):
        """Test with author fields."""
        data = {
            "audit_author": [
                {"name": "Smith, J."},
                {"name": "Jones, A."},
            ],
        }
        result = generate_brief_summary(data, "100d")
        assert result["deposit_author"] == ["Smith, J.", "Jones, A."]

    def test_with_citation(self):
        """Test with citation data."""
        data = {
            "citation": [
                {
                    "id": "primary",
                    "title": "Test Paper",
                    "journal_abbrev": "Nature",
                    "year": 2020,
                    "journal_volume": "580",
                },
            ],
        }
        result = generate_brief_summary(data, "100d")
        assert result["citation_title"] == ["Test Paper"]
        assert result["citation_year"] == [2020]
        assert result["citation_title_pri"] == "Test Paper"
        assert result["citation_year_pri"] == 2020

    def test_citation_year_conversion(self):
        """Test that citation_year is converted to integer array."""
        data = {
            "citation": [
                {"id": "1", "year": "2020"},  # String year
                {"id": "2", "year": 2021},  # Integer year
            ],
        }
        result = generate_brief_summary(data, "100d")
        assert result["citation_year"] == [2020, 2021]
        assert all(isinstance(y, int) for y in result["citation_year"])

    def test_resolution_conversion(self):
        """Test that resolution is converted to float."""
        data = {
            "refine": [{"ls_d_res_high": "2.5"}],  # String resolution
        }
        result = generate_brief_summary(data, "100d")
        assert result["resolution"] == 2.5
        assert isinstance(result["resolution"], float)

    def test_resolution_from_em(self):
        """Test resolution fallback to em_3d_reconstruction."""
        data = {
            "em_3d_reconstruction": [{"resolution": 3.2}],
        }
        result = generate_brief_summary(data, "100d")
        assert result["resolution"] == 3.2

    def test_with_chain_info(self):
        """Test with entity_poly chain info."""
        data = {
            "entity_poly": [
                {"type": "polypeptide(L)", "pdbx_seq_one_letter_code_can": "ACDEFG"},
                {"type": "polyribonucleotide", "pdbx_seq_one_letter_code_can": "AUGC"},
            ],
        }
        result = generate_brief_summary(data, "100d")
        assert result["chain_type"] == ["polypeptide(L)", "polyribonucleotide"]
        assert result["chain_type_ids"] == [2, 4]
        assert result["chain_length"] == [6, 4]
        assert result["aaseq"] == "ACDEFGAUGC"

    def test_with_exptl_method(self):
        """Test with experimental method."""
        data = {
            "exptl": [{"method": "X-RAY DIFFRACTION"}],
        }
        result = generate_brief_summary(data, "100d")
        assert result["exptl_method"] == ["X-RAY DIFFRACTION"]
        assert result["exptl_method_ids"] == [1]

    def test_hybrid_method(self):
        """Test HYBRID is added for multiple methods."""
        data = {
            "exptl": [
                {"method": "X-RAY DIFFRACTION"},
                {"method": "NEUTRON DIFFRACTION"},
            ],
        }
        result = generate_brief_summary(data, "100d")
        assert "HYBRID" in result["exptl_method"]
        assert 14 in result["exptl_method_ids"]  # HYBRID id

    def test_keywords(self):
        """Test keywords generation."""
        result = generate_brief_summary({}, "100d")
        assert result["keywords"] == ["pdb_0000100d"]

    def test_with_bu_mw(self):
        """Test with bu_mw parameter."""
        bu_mw = {"1": 12345.6}
        result = generate_brief_summary({}, "100d", bu_mw)
        assert result["plus_fields"] is not None
        assert "bu_mw" in result["plus_fields"]
