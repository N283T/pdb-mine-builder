"""Tests for assembly utilities."""

from mine2.utils.assembly import (
    CHAIN_TYPE_MAPPING,
    EXPTL_METHOD_MAPPING,
    calculate_mw_for_bu,
    expand_oper_expression,
    hex_sha256,
)


class TestHexSha256:
    """Tests for hex_sha256 function."""

    def test_empty_string(self):
        """Test hash of empty string."""
        result = hex_sha256("")
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_simple_string(self):
        """Test hash of simple string."""
        result = hex_sha256("A,B,C")
        assert len(result) == 64
        # SHA256 of "A,B,C" (utf-8 encoded)
        expected = "28f0fd5933ae52842b0f0a6e80b6876e5252f8e7549d768c2f76165e56b6f118"
        assert result == expected

    def test_deterministic(self):
        """Test that same input produces same output."""
        assert hex_sha256("test") == hex_sha256("test")

    def test_different_inputs_different_outputs(self):
        """Test that different inputs produce different outputs."""
        assert hex_sha256("a") != hex_sha256("b")


class TestExpandOperExpression:
    """Tests for expand_oper_expression function."""

    def test_empty_expression(self):
        """Test empty expression."""
        assert expand_oper_expression("") == []

    def test_single_value(self):
        """Test single value."""
        assert expand_oper_expression("1") == ["1"]

    def test_range_expression(self):
        """Test range like '1-3'."""
        assert expand_oper_expression("1-3") == ["1", "2", "3"]

    def test_comma_separated(self):
        """Test comma-separated values."""
        assert expand_oper_expression("1,2,3") == ["1", "2", "3"]

    def test_product_notation(self):
        """Test product notation like '(1,2)(3,4)'."""
        result = expand_oper_expression("(1,2)(3,4)")
        expected = ["1-3", "1-4", "2-3", "2-4"]
        assert result == expected

    def test_product_with_ranges(self):
        """Test product notation with ranges."""
        result = expand_oper_expression("(1-2)(3,4)")
        expected = ["1-3", "1-4", "2-3", "2-4"]
        assert result == expected

    def test_non_numeric_values(self):
        """Test non-numeric values like 'X-Y' are preserved."""
        # This tests the try/except in expand_range
        result = expand_oper_expression("X-Y")
        assert result == ["X-Y"]


class TestCalculateMwForBu:
    """Tests for calculate_mw_for_bu function."""

    def test_no_assembly_data(self):
        """Test with no assembly data."""
        data = {}
        assert calculate_mw_for_bu(data) == 0.0

    def test_empty_assembly_gen(self):
        """Test with empty assembly_gen."""
        data = {"pdbx_struct_assembly_gen": []}
        assert calculate_mw_for_bu(data) == 0.0

    def test_simple_assembly(self):
        """Test simple assembly with one chain."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined"}],
            "pdbx_struct_assembly_gen": [
                {
                    "assembly_id": "1",
                    "asym_id_list": "A",
                    "oper_expression": "1",
                }
            ],
        }
        result = calculate_mw_for_bu(data)
        assert result == 1000.0

    def test_multiple_chains(self):
        """Test assembly with multiple chains."""
        data = {
            "entity": [
                {"id": "1", "formula_weight": 1000.0},
                {"id": "2", "formula_weight": 500.0},
            ],
            "struct_asym": [
                {"id": "A", "entity_id": "1"},
                {"id": "B", "entity_id": "2"},
            ],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined"}],
            "pdbx_struct_assembly_gen": [
                {
                    "assembly_id": "1",
                    "asym_id_list": "A,B",
                    "oper_expression": "1",
                }
            ],
        }
        result = calculate_mw_for_bu(data)
        assert result == 1500.0

    def test_multiple_operators(self):
        """Test assembly with multiple operators (symmetry copies)."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined"}],
            "pdbx_struct_assembly_gen": [
                {
                    "assembly_id": "1",
                    "asym_id_list": "A",
                    "oper_expression": "1-3",  # 3 copies
                }
            ],
        }
        result = calculate_mw_for_bu(data)
        assert result == 3000.0  # 1000 * 3

    def test_author_and_software_priority(self):
        """Test that author_and_software assembly is preferred."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [
                {"id": "1", "details": "software_defined"},
                {"id": "2", "details": "author_and_software_defined"},
            ],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"},
                {"assembly_id": "2", "asym_id_list": "A", "oper_expression": "1-2"},
            ],
        }
        result = calculate_mw_for_bu(data)
        # Should use assembly_id=2 (author_and_software) with 2 operators
        assert result == 2000.0

    def test_author_priority(self):
        """Test that author assembly is preferred over software."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [
                {"id": "1", "details": "software_defined"},
                {"id": "2", "details": "author_defined"},
            ],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"},
                {"assembly_id": "2", "asym_id_list": "A", "oper_expression": "1-3"},
            ],
        }
        result = calculate_mw_for_bu(data)
        # Should use assembly_id=2 (author) with 3 operators
        assert result == 3000.0

    def test_software_priority(self):
        """Test that software assembly is used when no author."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [
                {"id": "1", "details": "something_else"},
                {"id": "2", "details": "software_defined"},
            ],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"},
                {"assembly_id": "2", "asym_id_list": "A", "oper_expression": "1-4"},
            ],
        }
        result = calculate_mw_for_bu(data)
        # Should use assembly_id=2 (software) with 4 operators
        assert result == 4000.0

    def test_largest_assembly_fallback(self):
        """Test fallback to largest assembly by sequence length."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "entity_poly": [
                {"entity_id": "1", "pdbx_seq_one_letter_code_can": "ACDEFG"}
            ],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [
                {"id": "1", "details": "something"},
                {"id": "2", "details": "something_else"},
            ],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"},
                {"assembly_id": "2", "asym_id_list": "A", "oper_expression": "1-2"},
            ],
        }
        result = calculate_mw_for_bu(data)
        # Should use assembly_id=2 (larger: 6 * 2 = 12 vs 6 * 1 = 6)
        assert result == 2000.0

    def test_non_numeric_assembly_id_skipped(self):
        """Test that non-numeric assembly IDs are skipped in fallback."""
        data = {
            "entity": [{"id": "1", "formula_weight": 1000.0}],
            "entity_poly": [
                {"entity_id": "1", "pdbx_seq_one_letter_code_can": "ACDEFG"}
            ],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [
                {"id": "PAU", "details": "something"},  # Non-numeric
                {"id": "1", "details": "something_else"},
            ],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "PAU", "asym_id_list": "A", "oper_expression": "1-5"},
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"},
            ],
        }
        result = calculate_mw_for_bu(data)
        # Should use assembly_id=1 (numeric) even though PAU has more operators
        assert result == 1000.0

    def test_missing_formula_weight(self):
        """Test handling of missing formula_weight."""
        data = {
            "entity": [{"id": "1"}],  # No formula_weight
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined"}],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"}
            ],
        }
        result = calculate_mw_for_bu(data)
        assert result == 0.0

    def test_zero_formula_weight(self):
        """Test handling of zero formula_weight."""
        data = {
            "entity": [{"id": "1", "formula_weight": 0}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined"}],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "asym_id_list": "A", "oper_expression": "1"}
            ],
        }
        result = calculate_mw_for_bu(data)
        assert result == 0.0


class TestMappings:
    """Tests for mapping constants."""

    def test_chain_type_mapping_has_common_types(self):
        """Test that common chain types are in mapping."""
        assert "polypeptide(L)" in CHAIN_TYPE_MAPPING
        assert "polypeptide(D)" in CHAIN_TYPE_MAPPING
        assert "polyribonucleotide" in CHAIN_TYPE_MAPPING
        assert "polydeoxyribonucleotide" in CHAIN_TYPE_MAPPING

    def test_exptl_method_mapping_has_common_methods(self):
        """Test that common experimental methods are in mapping."""
        assert "X-RAY DIFFRACTION" in EXPTL_METHOD_MAPPING
        assert "ELECTRON MICROSCOPY" in EXPTL_METHOD_MAPPING
        assert "SOLUTION NMR" in EXPTL_METHOD_MAPPING
        assert "IHM" in EXPTL_METHOD_MAPPING

    def test_ihm_method_id_is_16(self):
        """Test that IHM method ID is 16."""
        assert EXPTL_METHOD_MAPPING["IHM"] == 16
