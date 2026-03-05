"""Tests for command modules."""

import warnings

import pytest
from pydantic import ValidationError

from pdbminebuilder.commands.load import LOAD_PIPELINES
from pdbminebuilder.commands.update import (
    AVAILABLE_PIPELINES,
    DUAL_FORMAT_PIPELINES,
    LEGACY_ALIASES,
    PIPELINE_SCHEMA_MAP,
    _get_pipeline_runner,
)
from pdbminebuilder.config import PipelineConfig
from pdbminebuilder.models import ALL_METADATA
from pdbminebuilder.commands.sync import LEGACY_SYNC_ALIASES, SYNC_TARGETS
from pdbminebuilder.commands.utils import resolve_legacy_aliases


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

    def test_legacy_aliases_include_cif_suffix(self) -> None:
        """Legacy aliases should include -cif suffix entries."""
        cif_aliases = {k for k in LEGACY_ALIASES if k.endswith("-cif")}
        assert len(cif_aliases) > 0, "Should have -cif legacy aliases"

    def test_legacy_aliases_include_json_suffix(self) -> None:
        """Legacy aliases should include -json suffix entries."""
        json_aliases = {k for k in LEGACY_ALIASES if k.endswith("-json")}
        assert len(json_aliases) > 0, "Should have -json legacy aliases"

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

    def test_no_json_suffix_in_available_pipelines(self) -> None:
        """Available pipelines should not have -json suffix (format via config)."""
        for name in AVAILABLE_PIPELINES:
            assert not name.endswith("-json"), (
                f"Pipeline '{name}' should not use -json suffix; "
                "format is now configured via config"
            )

    def test_no_cif_suffix_in_available_pipelines(self) -> None:
        """Available pipelines should not have -cif suffix."""
        for name in AVAILABLE_PIPELINES:
            assert not name.endswith("-cif"), (
                f"Pipeline '{name}' should not use -cif suffix"
            )

    def test_dual_format_pipelines_are_available(self) -> None:
        """All dual-format pipelines should be in AVAILABLE_PIPELINES."""
        for name in DUAL_FORMAT_PIPELINES:
            assert name in AVAILABLE_PIPELINES, (
                f"Dual-format pipeline '{name}' should be in AVAILABLE_PIPELINES"
            )


class TestPipelineSchemaMap:
    """Tests for PIPELINE_SCHEMA_MAP consistency."""

    def test_all_pipelines_have_schema_mapping(self) -> None:
        """Every available pipeline must have a schema mapping."""
        for p in AVAILABLE_PIPELINES:
            assert p in PIPELINE_SCHEMA_MAP, (
                f"Pipeline {p!r} missing from PIPELINE_SCHEMA_MAP"
            )

    def test_all_schema_values_are_valid(self) -> None:
        """All schema names in the map must exist in ALL_METADATA."""
        for pipeline, schema in PIPELINE_SCHEMA_MAP.items():
            assert schema in ALL_METADATA, (
                f"Pipeline {pipeline!r} maps to unknown schema {schema!r}"
            )

    def test_no_json_suffix_in_schema_map(self) -> None:
        """Schema map should not have -json suffix keys."""
        for name in PIPELINE_SCHEMA_MAP:
            assert not name.endswith("-json"), (
                f"Schema map key '{name}' should not use -json suffix"
            )


class TestGetPipelineRunner:
    """Tests for _get_pipeline_runner dispatch logic."""

    def test_dual_format_cif_dispatches_to_run_cif(self) -> None:
        """Dual-format pipelines with format=cif should dispatch to run_cif()."""
        config = PipelineConfig(data="/tmp", format="cif")
        for pipeline_name in DUAL_FORMAT_PIPELINES:
            module_name, func_name = _get_pipeline_runner(pipeline_name, config)
            assert module_name == pipeline_name
            assert func_name == "run_cif", (
                f"{pipeline_name} with format=cif should dispatch to run_cif, got {func_name}"
            )

    def test_dual_format_mmjson_dispatches_to_run(self) -> None:
        """Dual-format pipelines with format=mmjson should dispatch to run()."""
        config = PipelineConfig(data="/tmp", format="mmjson")
        for pipeline_name in DUAL_FORMAT_PIPELINES:
            module_name, func_name = _get_pipeline_runner(pipeline_name, config)
            assert module_name == pipeline_name
            assert func_name == "run", (
                f"{pipeline_name} with format=mmjson should dispatch to run, got {func_name}"
            )

    def test_other_pipelines_dispatch_to_run(self) -> None:
        """Other pipelines (vrpt, contacts, sifts, etc.) dispatch to run()."""
        config = PipelineConfig(data="/tmp")
        other_cases = {"vrpt", "contacts", "sifts", "emdb", "ihm"}
        for pipeline_name in other_cases:
            module_name, func_name = _get_pipeline_runner(pipeline_name, config)
            assert module_name == pipeline_name
            assert func_name == "run", (
                f"{pipeline_name} should dispatch to run, got {func_name}"
            )

    def test_all_available_pipelines_have_runner(self) -> None:
        """Every available pipeline should have a valid runner dispatch."""
        config = PipelineConfig(data="/tmp")
        for pipeline_name in AVAILABLE_PIPELINES:
            module_name, func_name = _get_pipeline_runner(pipeline_name, config)
            assert module_name, f"{pipeline_name} returned empty module name"
            assert func_name in ("run", "run_cif"), (
                f"{pipeline_name} returned unexpected func {func_name}"
            )


class TestPipelineConfigFormat:
    """Tests for PipelineConfig format field."""

    def test_default_format_is_cif(self) -> None:
        """Default format should be 'cif'."""
        config = PipelineConfig(data="/tmp")
        assert config.format == "cif"

    def test_format_cif_accepted(self) -> None:
        """Format 'cif' should be accepted."""
        config = PipelineConfig(data="/tmp", format="cif")
        assert config.format == "cif"

    def test_format_mmjson_accepted(self) -> None:
        """Format 'mmjson' should be accepted."""
        config = PipelineConfig(data="/tmp", format="mmjson")
        assert config.format == "mmjson"

    def test_invalid_format_rejected(self) -> None:
        """Invalid format should be rejected with ValidationError."""
        with pytest.raises(ValidationError):
            PipelineConfig(data="/tmp", format="xml")


class TestLoadPipelineConsistency:
    """Tests for LOAD_PIPELINES consistency with AVAILABLE_PIPELINES."""

    def test_all_load_pipelines_are_available(self) -> None:
        """Every load pipeline must be in AVAILABLE_PIPELINES."""
        for p in LOAD_PIPELINES:
            assert p in AVAILABLE_PIPELINES, (
                f"Load pipeline {p!r} is not in AVAILABLE_PIPELINES"
            )

    def test_dual_format_pipelines_are_loadable(self) -> None:
        """All dual-format pipelines should be in LOAD_PIPELINES."""
        for p in DUAL_FORMAT_PIPELINES:
            assert p in LOAD_PIPELINES, (
                f"Dual-format pipeline {p!r} should be in LOAD_PIPELINES"
            )

    def test_no_json_suffix_in_load_pipelines(self) -> None:
        """Load pipelines should not have -json suffix."""
        for name in LOAD_PIPELINES:
            assert not name.endswith("-json"), (
                f"Load pipeline '{name}' should not use -json suffix"
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
