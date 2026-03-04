"""Tests for command modules."""

import warnings


from mine2.commands.update import AVAILABLE_PIPELINES, LEGACY_ALIASES
from mine2.commands.sync import LEGACY_SYNC_ALIASES, SYNC_TARGETS
from mine2.commands.utils import resolve_legacy_aliases


class TestLegacyAliases:
    """Tests for legacy alias resolution."""

    def test_all_update_legacy_aliases_resolve_to_valid_pipelines(self) -> None:
        """All legacy update aliases should map to valid pipeline names."""
        for legacy, new_name in LEGACY_ALIASES.items():
            assert new_name in AVAILABLE_PIPELINES, (
                f"Legacy alias '{legacy}' maps to invalid pipeline '{new_name}'"
            )

    def test_all_sync_legacy_aliases_resolve_to_valid_targets(self) -> None:
        """All legacy sync aliases should map to valid sync targets."""
        for legacy, new_name in LEGACY_SYNC_ALIASES.items():
            assert new_name in SYNC_TARGETS, (
                f"Legacy alias '{legacy}' maps to invalid sync target '{new_name}'"
            )

    def test_legacy_aliases_follow_naming_pattern(self) -> None:
        """Legacy aliases should follow the -cif suffix pattern."""
        for legacy in LEGACY_ALIASES:
            assert legacy.endswith("-cif"), (
                f"Legacy alias '{legacy}' should end with '-cif'"
            )

    def test_sync_legacy_aliases_follow_naming_pattern(self) -> None:
        """Sync legacy aliases should follow the -cif suffix pattern."""
        for legacy in LEGACY_SYNC_ALIASES:
            assert legacy.endswith("-cif"), (
                f"Legacy sync alias '{legacy}' should end with '-cif'"
            )


class TestResolveLegacyAliases:
    """Tests for resolve_legacy_aliases utility function."""

    def test_resolves_single_legacy_alias(self) -> None:
        """Single legacy alias should be resolved."""
        aliases = {"old-name": "new-name"}
        result = resolve_legacy_aliases(["old-name"], aliases, "Test")
        assert result == ["new-name"]

    def test_preserves_non_legacy_names(self) -> None:
        """Non-legacy names should be preserved unchanged."""
        aliases = {"old-name": "new-name"}
        result = resolve_legacy_aliases(["valid-name"], aliases, "Test")
        assert result == ["valid-name"]

    def test_resolves_mixed_list(self) -> None:
        """Mixed list of legacy and non-legacy names should be resolved correctly."""
        aliases = {"old1": "new1", "old2": "new2"}
        result = resolve_legacy_aliases(
            ["old1", "valid", "old2", "another"],
            aliases,
            "Test",
        )
        assert result == ["new1", "valid", "new2", "another"]

    def test_emits_deprecation_warning(self) -> None:
        """Using a legacy alias should emit a DeprecationWarning."""
        aliases = {"old-name": "new-name"}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            resolve_legacy_aliases(["old-name"], aliases, "Pipeline")
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "old-name" in str(w[0].message)
            assert "new-name" in str(w[0].message)
            assert "Pipeline" in str(w[0].message)

    def test_no_warning_for_valid_names(self) -> None:
        """Non-legacy names should not emit warnings."""
        aliases = {"old-name": "new-name"}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            resolve_legacy_aliases(["valid-name"], aliases, "Test")
            assert len(w) == 0

    def test_empty_list_returns_empty(self) -> None:
        """Empty input list should return empty list."""
        aliases = {"old-name": "new-name"}
        result = resolve_legacy_aliases([], aliases, "Test")
        assert result == []

    def test_empty_aliases_returns_unchanged(self) -> None:
        """Empty aliases dict should return input unchanged."""
        result = resolve_legacy_aliases(["name1", "name2"], {}, "Test")
        assert result == ["name1", "name2"]


class TestPipelineNamingConsistency:
    """Tests for pipeline naming consistency."""

    def test_cif_pipelines_have_json_counterparts(self) -> None:
        """Each CIF default pipeline should have a -json counterpart."""
        cif_defaults = {"pdbj", "cc", "ccmodel", "prd"}
        for name in cif_defaults:
            json_name = f"{name}-json"
            assert json_name in AVAILABLE_PIPELINES, (
                f"CIF pipeline '{name}' missing -json counterpart '{json_name}'"
            )

    def test_json_pipelines_have_cif_defaults(self) -> None:
        """Each -json pipeline should have a CIF default counterpart."""
        for name in AVAILABLE_PIPELINES:
            if name.endswith("-json"):
                base_name = name[:-5]  # Remove '-json' suffix
                assert base_name in AVAILABLE_PIPELINES, (
                    f"JSON pipeline '{name}' missing CIF default '{base_name}'"
                )

    def test_no_cif_suffix_in_available_pipelines(self) -> None:
        """Available pipelines should not have -cif suffix (use legacy aliases)."""
        for name in AVAILABLE_PIPELINES:
            assert not name.endswith("-cif"), (
                f"Pipeline '{name}' should not use -cif suffix; CIF is now the default"
            )


class TestSyncTargetNamingConsistency:
    """Tests for sync target naming consistency."""

    def test_no_cif_suffix_in_sync_targets(self) -> None:
        """Sync targets should not have -cif suffix (use legacy aliases)."""
        for name in SYNC_TARGETS:
            assert not name.endswith("-cif"), (
                f"Sync target '{name}' should not use -cif suffix; "
                "CIF is now the default"
            )
