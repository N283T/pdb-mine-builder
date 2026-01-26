"""Tests for cc-cif pipeline."""

import gzip
from pathlib import Path

import gemmi
import pytest

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import SchemaDef, TableDef
from mine2.pipelines.cc import CcCifPipeline, _process_cif_block


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
        cif_path = tmp_path / "components.cif.gz"
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
        nested_dir = tmp_path / "components.cif.gz"
        nested_dir.mkdir()
        cif_path = nested_dir / "components.cif.gz"
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
        subdir = tmp_path / "subdir" / "another"
        subdir.mkdir(parents=True)
        cif_path = subdir / "components.cif.gz"
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
        settings = create_test_settings(tmp_path / "nonexistent")
        config = settings.pipelines["cc-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found is None


class TestProcessCifBlock:
    """Tests for _process_cif_block function."""

    def test_process_single_block(self, tmp_path: Path) -> None:
        """Process a single CIF block."""
        cif_path = tmp_path / "test.cif"
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
        cif_path = tmp_path / "test.cif"
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
        cif_path = tmp_path / "components.cif.gz"
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
        cif_path = tmp_path / "components.cif.gz"
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
