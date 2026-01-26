"""Tests for cc-cif pipeline."""

import gzip
from pathlib import Path
from unittest.mock import MagicMock, patch

import gemmi
import psycopg
import pytest

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import SchemaDef, TableDef
from mine2.pipelines.cc import CcCifPipeline, _ensure_rdkit_setup, _process_cif_block


def create_test_cif_content(components: list[dict]) -> str:
    """Create CIF content string with the given components.

    Args:
        components: List of dicts with 'id', 'name', 'type' keys

    Returns:
        CIF format string
    """
    blocks = []
    for comp in components:
        comp_id = comp["id"]
        name = comp.get("name", "Test")
        comp_type = comp.get("type", "NON-POLYMER")
        # Quote name if it contains spaces
        if " " in name:
            name = f"'{name}'"
        blocks.append(f"""data_{comp_id}
_chem_comp.id {comp_id}
_chem_comp.name {name}
_chem_comp.type {comp_type}
""")
    return "\n".join(blocks)


def create_test_cif_file(path: Path, components: list[dict]) -> None:
    """Create a test CIF file with the given components.

    Handles .gz extension by writing gzip-compressed content.

    Args:
        path: Path to write the CIF file
        components: List of dicts with 'id', 'name', 'type' keys
    """
    content = create_test_cif_content(components)
    # Parse and re-write to ensure valid CIF format
    doc = gemmi.cif.read_string(content)

    if str(path).endswith(".gz"):
        # Write to temp file, then gzip
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".cif", delete=False) as tmp:
            doc.write_file(tmp.name)
            with open(tmp.name, "rb") as f_in:
                with gzip.open(path, "wb") as f_out:
                    f_out.write(f_in.read())
            Path(tmp.name).unlink()
    else:
        doc.write_file(str(path))


def create_test_settings(data_dir: Path) -> Settings:
    """Create test settings."""
    return Settings(
        rdb=RdbConfig(nworkers=2, constring="test"),
        pipelines={
            "cc-cif": PipelineConfig(
                deffile="schemas/cc.def.yml",
                data=str(data_dir),
            )
        },
    )


def create_test_schema_def() -> SchemaDef:
    """Create minimal test schema definition."""
    return SchemaDef(
        schema_name="cc",
        primary_key="id",
        tables=[
            TableDef(
                name="chem_comp",
                columns=[("id", "TEXT"), ("name", "TEXT"), ("type", "TEXT")],
                primary_key=["id"],
            ),
        ],
    )


class TestFindCifFile:
    """Tests for CcCifPipeline._find_cif_file()."""

    def test_direct_path(self, tmp_path: Path) -> None:
        """Find CIF file at direct path."""
        cif_path = tmp_path.joinpath("components.cif.gz")
        create_test_cif_file(cif_path, [{"id": "ATP"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_nested_path_rsync_quirk(self, tmp_path: Path) -> None:
        """Find CIF file in nested directory (rsync quirk)."""
        # Create nested structure: data/components.cif.gz/components.cif.gz
        nested_dir = tmp_path.joinpath("components.cif.gz")
        nested_dir.mkdir()
        cif_path = nested_dir.joinpath("components.cif.gz")
        create_test_cif_file(cif_path, [{"id": "ATP"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_recursive_search(self, tmp_path: Path) -> None:
        """Find CIF file via recursive search."""
        # Create file in subdirectory
        subdir = tmp_path.joinpath("subdir", "another")
        subdir.mkdir(parents=True)
        cif_path = subdir.joinpath("components.cif.gz")
        create_test_cif_file(cif_path, [{"id": "ATP"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_not_found(self, tmp_path: Path) -> None:
        """Return None when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found is None

    def test_directory_not_exists(self, tmp_path: Path) -> None:
        """Return None when data directory doesn't exist."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found is None


class TestProcessCifBlock:
    """Tests for _process_cif_block function."""

    def test_process_single_block(self, tmp_path: Path) -> None:
        """Process a single CIF block."""
        cif_path = tmp_path.joinpath("test.cif")
        create_test_cif_file(
            cif_path,
            [
                {"id": "ATP", "name": "Adenosine Triphosphate", "type": "NON-POLYMER"},
            ],
        )

        schema_def = create_test_schema_def()

        # Load the CIF and get the block
        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        # Mock conninfo - will fail to connect but tests the function runs
        result = _process_cif_block(
            block=block,
            schema_def=schema_def,
            conninfo="mock://test",
        )

        # Should return a single LoaderResult
        assert result.entry_id == "ATP"
        # Will fail because we can't connect to mock DB
        assert result.success is False

    def test_process_block_extracts_comp_id(self, tmp_path: Path) -> None:
        """Block name is used as comp_id."""
        cif_path = tmp_path.joinpath("test.cif")
        create_test_cif_file(
            cif_path,
            [
                {"id": "ADP"},
            ],
        )

        schema_def = create_test_schema_def()

        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_cif_block(
            block=block,
            schema_def=schema_def,
            conninfo="mock://test",
        )

        assert result.entry_id == "ADP"


class TestCcCifPipelineRun:
    """Tests for CcCifPipeline.run() method."""

    def test_run_returns_empty_when_no_file(self, tmp_path: Path) -> None:
        """Run returns empty list when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        results = pipeline.run()

        assert results == []

    def test_run_sequential_for_small_count(self, tmp_path: Path) -> None:
        """Run uses sequential processing for small block counts."""
        cif_path = tmp_path.joinpath("components.cif.gz")
        create_test_cif_file(
            cif_path,
            [{"id": f"COMP{i}"} for i in range(5)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        # Limit to 5 - should use sequential (threshold is 10)
        results = pipeline.run(limit=5)

        # Will fail to connect to DB, but should process 5 blocks
        assert len(results) == 5

    def test_run_respects_limit(self, tmp_path: Path) -> None:
        """Run respects the limit parameter."""
        cif_path = tmp_path.joinpath("components.cif.gz")
        create_test_cif_file(
            cif_path,
            [{"id": f"COMP{i}"} for i in range(100)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        results = pipeline.run(limit=10)

        assert len(results) == 10


class TestEnsureRdkitSetup:
    """Tests for _ensure_rdkit_setup function."""

    def test_creates_extension_and_commits(self) -> None:
        """Successfully creates RDKit extension and commits."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            _ensure_rdkit_setup("test_conninfo")

        # Verify extension creation was attempted
        mock_cursor.execute.assert_any_call("CREATE EXTENSION IF NOT EXISTS rdkit")
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    def test_handles_insufficient_privilege(self) -> None:
        """Handles InsufficientPrivilege exception gracefully."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg.errors.InsufficientPrivilege(
            "permission denied"
        )
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            # Should not raise - logs warning and returns early
            _ensure_rdkit_setup("test_conninfo")

        # Commit should not be called when privilege error occurs
        mock_conn.commit.assert_not_called()

    def test_executes_mol_column_ddl(self) -> None:
        """Executes DDL for mol column creation."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            _ensure_rdkit_setup("test_conninfo")

        # Verify two execute calls: extension + mol column DDL
        assert mock_cursor.execute.call_count == 2
        # Second call should be the DO block for mol column
        second_call_sql = mock_cursor.execute.call_args_list[1][0][0]
        assert "cc.brief_summary" in second_call_sql
        assert "mol" in second_call_sql
        assert "is_valid_smiles" in second_call_sql

    def test_idempotent_multiple_calls(self) -> None:
        """Multiple calls work without error (idempotent)."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            # Call twice - should not raise
            _ensure_rdkit_setup("test_conninfo")
            _ensure_rdkit_setup("test_conninfo")

        # Should have been called twice (2 calls x 2 invocations)
        assert mock_cursor.execute.call_count == 4
