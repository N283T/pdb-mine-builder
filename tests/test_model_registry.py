"""Tests for mine2.models registry and mine2.db.loader SA helpers."""

import pytest
from sqlalchemy import Column, MetaData, PrimaryKeyConstraint, Table, Text

from mine2.db.loader import (
    get_all_tables,
    get_column_names,
    get_entry_pk,
    get_table,
    get_table_or_none,
)
from mine2.models import ALL_METADATA, get_metadata


# =============================================================================
# Model registry tests
# =============================================================================


class TestModelRegistry:
    """Tests for ALL_METADATA and get_metadata()."""

    def test_all_metadata_has_expected_count(self) -> None:
        assert len(ALL_METADATA) == 10

    def test_get_metadata_returns_valid_metadata(self) -> None:
        for name, meta in ALL_METADATA.items():
            result = get_metadata(name)
            assert result is meta

    def test_get_metadata_unknown_raises_keyerror(self) -> None:
        with pytest.raises(KeyError, match="Unknown schema"):
            get_metadata("nonexistent_schema")

    def test_all_metadata_schemas_match_keys(self) -> None:
        """Each MetaData.schema must match its registry key."""
        for name, meta in ALL_METADATA.items():
            assert meta.schema == name, (
                f"Registry key {name!r} != MetaData.schema {meta.schema!r}"
            )

    def test_all_metadata_have_entry_pk(self) -> None:
        """Every registered MetaData must have info['entry_pk']."""
        for name, meta in ALL_METADATA.items():
            assert "entry_pk" in meta.info, (
                f"Schema {name!r} missing 'entry_pk' in metadata.info"
            )


# =============================================================================
# MetaData helper function tests
# =============================================================================


def _make_test_meta(*, schema: str | None = "test") -> MetaData:
    """Create a test MetaData with two tables."""
    meta = MetaData(schema=schema)
    meta.info = {"entry_pk": "test_id"}
    Table(
        "table_a",
        meta,
        Column("test_id", Text),
        Column("name", Text),
        PrimaryKeyConstraint("test_id"),
    )
    Table(
        "table_b",
        meta,
        Column("test_id", Text),
        Column("value", Text),
        PrimaryKeyConstraint("test_id"),
    )
    return meta


class TestGetEntryPk:
    """Tests for get_entry_pk()."""

    def test_returns_entry_pk(self) -> None:
        meta = _make_test_meta()
        assert get_entry_pk(meta) == "test_id"

    def test_missing_entry_pk_raises_descriptive_error(self) -> None:
        meta = MetaData(schema="broken")
        meta.info = {}
        with pytest.raises(KeyError, match="missing 'entry_pk'"):
            get_entry_pk(meta)


class TestGetTable:
    """Tests for get_table() and get_table_or_none()."""

    def test_get_table_with_schema(self) -> None:
        meta = _make_test_meta(schema="test")
        result = get_table(meta, "table_a")
        assert result.name == "table_a"

    def test_get_table_without_schema(self) -> None:
        meta = _make_test_meta(schema=None)
        result = get_table(meta, "table_a")
        assert result.name == "table_a"

    def test_get_table_missing_raises_descriptive_error(self) -> None:
        meta = _make_test_meta()
        with pytest.raises(KeyError, match="not found in schema"):
            get_table(meta, "nonexistent")

    def test_get_table_or_none_found(self) -> None:
        meta = _make_test_meta()
        result = get_table_or_none(meta, "table_a")
        assert result is not None
        assert result.name == "table_a"

    def test_get_table_or_none_missing(self) -> None:
        meta = _make_test_meta()
        assert get_table_or_none(meta, "nonexistent") is None


class TestGetAllTables:
    """Tests for get_all_tables()."""

    def test_returns_all_tables(self) -> None:
        meta = _make_test_meta()
        tables = get_all_tables(meta)
        names = {t.name for t in tables}
        assert names == {"table_a", "table_b"}

    def test_returns_list(self) -> None:
        meta = _make_test_meta()
        assert isinstance(get_all_tables(meta), list)


class TestGetColumnNames:
    """Tests for get_column_names()."""

    def test_returns_column_names(self) -> None:
        meta = _make_test_meta()
        table = get_table(meta, "table_a")
        assert get_column_names(table) == {"test_id", "name"}
