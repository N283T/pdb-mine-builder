"""Tests for entry-specific patches."""


from mine2.utils.patches import apply_patches, _patch_7ed1_met


class TestApplyPatches:
    """Tests for apply_patches function."""

    def test_applies_7ed1_patch(self):
        """Test that 7ed1 patch is applied."""
        data = {"chem_comp": []}
        result = apply_patches("7ed1", data)

        assert len(result["chem_comp"]) == 1
        assert result["chem_comp"][0]["id"] == "MET"

    def test_does_not_apply_7ed1_patch_to_other_entries(self):
        """Test that 7ed1 patch is not applied to other entries."""
        data = {"chem_comp": []}
        result = apply_patches("1abc", data)

        assert len(result["chem_comp"]) == 0

    def test_returns_data(self):
        """Test that apply_patches returns the data dict."""
        data = {"chem_comp": []}
        result = apply_patches("1abc", data)

        assert result is data


class TestPatch7ed1Met:
    """Tests for _patch_7ed1_met function."""

    def test_adds_met_record(self):
        """Test that MET record is added when missing."""
        data = {"chem_comp": []}
        _patch_7ed1_met(data)

        assert len(data["chem_comp"]) == 1
        met = data["chem_comp"][0]
        assert met["id"] == "MET"
        assert met["type"] == "L-peptide linking"
        assert met["mon_nstd_flag"] == "y"
        assert met["name"] == "METHIONINE"
        assert met["formula"] == "C5 H11 N O2 S"
        assert met["formula_weight"] == 149.211

    def test_does_not_add_met_if_exists(self):
        """Test that MET is not added if already present."""
        existing_met = {"id": "MET", "name": "existing"}
        data = {"chem_comp": [existing_met]}
        _patch_7ed1_met(data)

        assert len(data["chem_comp"]) == 1
        assert data["chem_comp"][0]["name"] == "existing"

    def test_creates_chem_comp_if_missing(self):
        """Test that chem_comp is created if missing from data."""
        data = {}
        _patch_7ed1_met(data)

        assert "chem_comp" in data
        assert len(data["chem_comp"]) == 1
        assert data["chem_comp"][0]["id"] == "MET"

    def test_appends_to_existing_chem_comp(self):
        """Test that MET is appended to existing chem_comp list."""
        data = {"chem_comp": [{"id": "ALA", "name": "ALANINE"}]}
        _patch_7ed1_met(data)

        assert len(data["chem_comp"]) == 2
        ids = [c["id"] for c in data["chem_comp"]]
        assert "ALA" in ids
        assert "MET" in ids
