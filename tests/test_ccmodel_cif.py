"""Tests for ccmodel-cif pipeline."""

import gzip
from pathlib import Path

import gemmi
import pytest

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import SchemaDef, TableDef
from mine2.pipelines.ccmodel import (
    CcmodelCifPipeline,
    _generate_brief_summary,
    _process_ccmodel_cif_block,
)


def create_test_ccmodel_cif_content(models: list[dict]) -> str:
    """Create CIF content string with the given models.

    Args:
        models: List of dicts with 'id', 'comp_id' keys

    Returns:
        CIF format string
    """
    blocks = []
    for model in models:
        model_id = model["id"]  # e.g., M_DAL_00001
        comp_id = model.get("comp_id", "UNK")
        blocks.append(f"""data_{model_id}
_pdbx_chem_comp_model.id {model_id}
_pdbx_chem_comp_model.comp_id {comp_id}
""")
    return "\n".join(blocks)


def create_test_ccmodel_cif_file(path: Path, models: list[dict]) -> None:
    """Create a test ccmodel CIF file.

    Handles .gz extension by writing gzip-compressed content.
    """
    content = create_test_ccmodel_cif_content(models)
    doc = gemmi.cif.read_string(content)

    if str(path).endswith(".gz"):
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
            "ccmodel-cif": PipelineConfig(
                deffile="schemas/ccmodel.def.yml",
                data=str(data_dir),
            )
        },
    )


def create_test_schema_def() -> SchemaDef:
    """Create minimal test schema definition for ccmodel."""
    return SchemaDef(
        schema_name="ccmodel",
        primary_key="model_id",
        tables=[
            TableDef(
                name="brief_summary",
                columns=[("model_id", "TEXT"), ("comp_id", "TEXT")],
                primary_key=["model_id"],
            ),
            TableDef(
                name="pdbx_chem_comp_model",
                columns=[("model_id", "TEXT"), ("id", "TEXT"), ("comp_id", "TEXT")],
                primary_key=["model_id", "id"],
            ),
        ],
    )


class TestGenerateBriefSummary:
    """Tests for _generate_brief_summary function."""

    def test_with_data(self) -> None:
        """Generate brief_summary from pdbx_chem_comp_model data."""
        data = {
            "pdbx_chem_comp_model": [
                {"id": "M_DAL_00001", "comp_id": "DAL"},
            ]
        }
        result = _generate_brief_summary(data, "M_DAL_00001")

        assert len(result) == 1
        assert result[0]["model_id"] == "M_DAL_00001"
        assert result[0]["comp_id"] == "DAL"

    def test_without_data(self) -> None:
        """Generate minimal brief_summary when no data."""
        data = {}
        result = _generate_brief_summary(data, "M_TEST_00001")

        assert len(result) == 1
        assert result[0]["model_id"] == "M_TEST_00001"


class TestFindCifFile:
    """Tests for CcmodelCifPipeline._find_cif_file()."""

    def test_direct_path(self, tmp_path: Path) -> None:
        """Find CIF file at direct path."""
        cif_path = tmp_path.joinpath("chem_comp_model.cif.gz")
        create_test_ccmodel_cif_file(cif_path, [{"id": "M_DAL_00001"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_nested_path_rsync_quirk(self, tmp_path: Path) -> None:
        """Find CIF file in nested directory (rsync quirk)."""
        nested_dir = tmp_path.joinpath("chem_comp_model.cif.gz")
        nested_dir.mkdir()
        cif_path = nested_dir.joinpath("chem_comp_model.cif.gz")
        create_test_ccmodel_cif_file(cif_path, [{"id": "M_DAL_00001"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_complete_subdir(self, tmp_path: Path) -> None:
        """Find CIF file in 'complete' subdirectory."""
        complete_dir = tmp_path.joinpath("complete")
        complete_dir.mkdir()
        cif_path = complete_dir.joinpath("chem_comp_model.cif.gz")
        create_test_ccmodel_cif_file(cif_path, [{"id": "M_DAL_00001"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_not_found(self, tmp_path: Path) -> None:
        """Return None when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found is None

    def test_directory_not_exists(self, tmp_path: Path) -> None:
        """Return None when data directory doesn't exist."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        found = pipeline._find_cif_file()

        assert found is None


class TestProcessCcmodelCifBlock:
    """Tests for _process_ccmodel_cif_block function."""

    def test_process_single_block(self, tmp_path: Path) -> None:
        """Process a single CIF block."""
        cif_path = tmp_path.joinpath("test.cif")
        create_test_ccmodel_cif_file(
            cif_path,
            [{"id": "M_DAL_00001", "comp_id": "DAL"}],
        )

        schema_def = create_test_schema_def()
        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_def=schema_def,
            conninfo="mock://test",
        )

        assert result.entry_id == "M_DAL_00001"
        # Will fail to connect to mock DB
        assert result.success is False

    def test_process_block_extracts_model_id(self, tmp_path: Path) -> None:
        """Block name is used as model_id."""
        cif_path = tmp_path.joinpath("test.cif")
        create_test_ccmodel_cif_file(
            cif_path,
            [{"id": "M_ALA_00001", "comp_id": "ALA"}],
        )

        schema_def = create_test_schema_def()
        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_def=schema_def,
            conninfo="mock://test",
        )

        assert result.entry_id == "M_ALA_00001"


class TestCcmodelCifPipelineRun:
    """Tests for CcmodelCifPipeline.run() method."""

    def test_run_returns_empty_when_no_file(self, tmp_path: Path) -> None:
        """Run returns empty list when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        results = pipeline.run()

        assert results == []

    def test_run_sequential_for_small_count(self, tmp_path: Path) -> None:
        """Run uses sequential processing for small block counts."""
        cif_path = tmp_path.joinpath("chem_comp_model.cif.gz")
        create_test_ccmodel_cif_file(
            cif_path,
            [{"id": f"M_TEST_{i:05d}"} for i in range(5)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        results = pipeline.run(limit=5)

        assert len(results) == 5

    def test_run_respects_limit(self, tmp_path: Path) -> None:
        """Run respects the limit parameter."""
        cif_path = tmp_path.joinpath("chem_comp_model.cif.gz")
        create_test_ccmodel_cif_file(
            cif_path,
            [{"id": f"M_TEST_{i:05d}"} for i in range(100)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ccmodel-cif"]
        schema_def = create_test_schema_def()

        pipeline = CcmodelCifPipeline(settings, config, schema_def)
        results = pipeline.run(limit=10)

        assert len(results) == 10
