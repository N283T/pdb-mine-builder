"""Tests for prd pipeline (CIF format)."""

import gzip
from pathlib import Path

import gemmi
from sqlalchemy import Column, MetaData, PrimaryKeyConstraint, Table, Text

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.parsers.cif import parse_cif_file
from mine2.pipelines.prd import (
    PRDCC_TABLES,
    PrdCifPipeline,
    _generate_brief_summary_prd,
    _process_prd_cif_block,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "prd"


def create_test_prd_cif_content(entries: list[dict]) -> str:
    """Create PRD CIF content string with the given entries.

    Args:
        entries: List of dicts with 'id', 'name', 'formula', 'description' keys

    Returns:
        CIF format string
    """
    blocks = []
    for entry in entries:
        prd_id = entry["id"]  # e.g., PRD_000001
        name = entry.get("name", "Test Compound")
        # Quote strings with spaces
        if " " in name:
            name = f"'{name}'"
        formula = entry.get("formula", "C10H20")
        description = entry.get("description", "Test description")
        if " " in description:
            description = f"'{description}'"
        blocks.append(f"""data_{prd_id}
_pdbx_reference_molecule.prd_id {prd_id}
_pdbx_reference_molecule.name {name}
_pdbx_reference_molecule.formula {formula}
_pdbx_reference_molecule.description {description}
""")
    return "\n".join(blocks)


def create_test_prdcc_cif_content(entries: list[dict]) -> str:
    """Create PRDCC CIF content string with the given entries.

    Args:
        entries: List of dicts with 'id', 'formula', 'name' keys

    Returns:
        CIF format string
    """
    blocks = []
    for entry in entries:
        prdcc_id = entry["id"]  # e.g., PRDCC_000001
        comp_id = entry.get("comp_id", "UNK")
        formula = entry.get("formula", "C10H20")
        name = entry.get("name", "Unknown")
        if " " in name:
            name = f"'{name}'"
        blocks.append(f"""data_{prdcc_id}
_chem_comp.id {comp_id}
_chem_comp.formula {formula}
_chem_comp.name {name}
""")
    return "\n".join(blocks)


def create_test_prd_cif_file(path: Path, entries: list[dict]) -> None:
    """Create a test PRD CIF file.

    Handles .gz extension by writing gzip-compressed content.
    """
    content = create_test_prd_cif_content(entries)
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


def create_test_prdcc_cif_file(path: Path, entries: list[dict]) -> None:
    """Create a test PRDCC CIF file.

    Handles .gz extension by writing gzip-compressed content.
    """
    content = create_test_prdcc_cif_content(entries)
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
            "prd": PipelineConfig(
                data=str(data_dir),
            )
        },
    )


def create_test_meta() -> MetaData:
    """Create minimal test MetaData for prd."""
    meta = MetaData(schema="prd")
    meta.info = {"entry_pk": "prd_id"}
    Table(
        "brief_summary",
        meta,
        Column("prd_id", Text),
        Column("name", Text),
        Column("formula", Text),
        Column("description", Text),
        PrimaryKeyConstraint("prd_id"),
    )
    Table(
        "pdbx_reference_molecule",
        meta,
        Column("prd_id", Text),
        Column("name", Text),
        Column("formula", Text),
        PrimaryKeyConstraint("prd_id"),
    )
    Table(
        "chem_comp",
        meta,
        Column("prd_id", Text),
        Column("id", Text),
        Column("formula", Text),
        Column("name", Text),
        PrimaryKeyConstraint("prd_id", "id"),
    )
    return meta


class TestGenerateBriefSummaryPrd:
    """Tests for _generate_brief_summary_prd function."""

    def test_with_data(self) -> None:
        """Generate brief_summary from pdbx_reference_molecule data."""
        data = {
            "pdbx_reference_molecule": [
                {
                    "prd_id": "PRD_000001",
                    "name": "Cyclosporin A",
                    "formula": "C62H111N11O12",
                    "description": "Immunosuppressant",
                },
            ]
        }
        result = _generate_brief_summary_prd(data, "PRD_000001")

        assert len(result) == 1
        assert result[0]["prd_id"] == "PRD_000001"
        assert result[0]["name"] == "Cyclosporin A"
        assert result[0]["formula"] == "C62H111N11O12"

    def test_without_data(self) -> None:
        """Return empty list when no pdbx_reference_molecule data."""
        data = {}
        result = _generate_brief_summary_prd(data, "PRD_000001")

        assert len(result) == 0


class TestPrdccTables:
    """Tests for PRDCC_TABLES constant."""

    def test_contains_expected_tables(self) -> None:
        """PRDCC_TABLES contains expected chem_comp tables."""
        assert "chem_comp" in PRDCC_TABLES
        assert "chem_comp_atom" in PRDCC_TABLES
        assert "chem_comp_bond" in PRDCC_TABLES

    def test_does_not_contain_prd_tables(self) -> None:
        """PRDCC_TABLES does not contain pdbx_reference tables."""
        assert "pdbx_reference_molecule" not in PRDCC_TABLES
        assert "brief_summary" not in PRDCC_TABLES


class TestFindCifFiles:
    """Tests for PrdCifPipeline._find_cif_files()."""

    def test_direct_path(self, tmp_path: Path) -> None:
        """Find CIF files at direct path."""
        prd_path = tmp_path.joinpath("prd-all.cif.gz")
        prdcc_path = tmp_path.joinpath("prdcc-all.cif.gz")
        create_test_prd_cif_file(prd_path, [{"id": "PRD_000001"}])
        create_test_prdcc_cif_file(prdcc_path, [{"id": "PRDCC_000001"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        found_prd, found_prdcc = pipeline._find_cif_files()

        assert found_prd == prd_path
        assert found_prdcc == prdcc_path

    def test_prd_only(self, tmp_path: Path) -> None:
        """Find PRD file when PRDCC is missing."""
        prd_path = tmp_path.joinpath("prd-all.cif.gz")
        create_test_prd_cif_file(prd_path, [{"id": "PRD_000001"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        found_prd, found_prdcc = pipeline._find_cif_files()

        assert found_prd == prd_path
        assert found_prdcc is None

    def test_nested_path_rsync_quirk(self, tmp_path: Path) -> None:
        """Find CIF files in nested directory (rsync quirk)."""
        nested_dir = tmp_path.joinpath("prd-all.cif.gz")
        nested_dir.mkdir()
        prd_path = nested_dir.joinpath("prd-all.cif.gz")
        create_test_prd_cif_file(prd_path, [{"id": "PRD_000001"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        found_prd, found_prdcc = pipeline._find_cif_files()

        assert found_prd == prd_path

    def test_not_found(self, tmp_path: Path) -> None:
        """Return None when PRD CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        found_prd, found_prdcc = pipeline._find_cif_files()

        assert found_prd is None
        assert found_prdcc is None

    def test_directory_not_exists(self, tmp_path: Path) -> None:
        """Return None when data directory doesn't exist."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        found_prd, found_prdcc = pipeline._find_cif_files()

        assert found_prd is None


class TestProcessPrdCifBlock:
    """Tests for _process_prd_cif_block function."""

    def test_process_single_block(self, tmp_path: Path) -> None:
        """Process a single PRD block with PRDCC."""
        prd_path = tmp_path.joinpath("prd.cif")
        prdcc_path = tmp_path.joinpath("prdcc.cif")
        create_test_prd_cif_file(
            prd_path,
            [{"id": "PRD_000001", "name": "Test", "formula": "C10H20"}],
        )
        create_test_prdcc_cif_file(
            prdcc_path,
            [{"id": "PRDCC_000001", "comp_id": "TST", "formula": "C10H20"}],
        )

        prd_doc = gemmi.cif.read(str(prd_path))
        prdcc_doc = gemmi.cif.read(str(prdcc_path))
        prd_block = prd_doc[0]
        prdcc_block = prdcc_doc[0]

        result = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name="prd",
            conninfo="mock://test",
        )

        assert result.entry_id == "PRD_000001"
        # Will fail to connect to mock DB
        assert result.success is False

    def test_process_without_prdcc(self, tmp_path: Path) -> None:
        """Process PRD block without PRDCC."""
        prd_path = tmp_path.joinpath("prd.cif")
        create_test_prd_cif_file(
            prd_path,
            [{"id": "PRD_000001", "name": "Test", "formula": "C10H20"}],
        )

        prd_doc = gemmi.cif.read(str(prd_path))
        prd_block = prd_doc[0]

        result = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=None,  # No PRDCC block
            schema_name="prd",
            conninfo="mock://test",
        )

        assert result.entry_id == "PRD_000001"


class TestPrdCifPipelineRun:
    """Tests for PrdCifPipeline.run() method."""

    def test_run_returns_empty_when_no_file(self, tmp_path: Path) -> None:
        """Run returns empty list when PRD CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        results = pipeline.run()

        assert results == []

    def test_run_sequential_for_small_count(self, tmp_path: Path) -> None:
        """Run uses sequential processing for small block counts."""
        prd_path = tmp_path.joinpath("prd-all.cif.gz")
        prdcc_path = tmp_path.joinpath("prdcc-all.cif.gz")
        create_test_prd_cif_file(
            prd_path,
            [{"id": f"PRD_{i:06d}"} for i in range(1, 6)],
        )
        create_test_prdcc_cif_file(
            prdcc_path,
            [{"id": f"PRDCC_{i:06d}"} for i in range(1, 4)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        results = pipeline.run(limit=5)

        assert len(results) == 5

    def test_run_respects_limit(self, tmp_path: Path) -> None:
        """Run respects the limit parameter."""
        prd_path = tmp_path.joinpath("prd-all.cif.gz")
        create_test_prd_cif_file(
            prd_path,
            [{"id": f"PRD_{i:06d}"} for i in range(1, 51)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd"]
        meta = create_test_meta()

        pipeline = PrdCifPipeline(settings, config, meta)
        results = pipeline.run(limit=10)

        assert len(results) == 10


class TestRealPrdFixtures:
    """Tests using real PRD CIF fixture files."""

    def test_parse_prd_000001_fixture(self) -> None:
        """Parse PRD_000001 fixture file."""
        fixture_path = FIXTURES_DIR / "PRD_000001.cif.gz"
        assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

        data = parse_cif_file(fixture_path)

        # Check block name
        assert data["_block_name"] == "PRD_000001"

        # Should have pdbx_reference_molecule data
        assert "pdbx_reference_molecule" in data
        ref_mol = data["pdbx_reference_molecule"][0]
        assert ref_mol["prd_id"] == "PRD_000001"

    def test_parse_prdcc_000001_fixture(self) -> None:
        """Parse PRDCC_000001 fixture file."""
        fixture_path = FIXTURES_DIR / "PRDCC_000001.cif.gz"
        assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

        data = parse_cif_file(fixture_path)

        # Check block name
        assert data["_block_name"] == "PRDCC_000001"

        # Should have chem_comp data
        assert "chem_comp" in data

    def test_prd_prdcc_pair_matching(self) -> None:
        """PRD and PRDCC fixtures have matching IDs."""
        prd_path = FIXTURES_DIR / "PRD_000001.cif.gz"
        prdcc_path = FIXTURES_DIR / "PRDCC_000001.cif.gz"

        prd_data = parse_cif_file(prd_path)
        prdcc_data = parse_cif_file(prdcc_path)

        # Both should reference the same PRD ID
        prd_id = prd_data["pdbx_reference_molecule"][0]["prd_id"]
        # PRDCC block name follows pattern PRDCC_XXXXXX where XXXXXX matches PRD
        prdcc_num = prdcc_data["_block_name"].split("_")[1]
        prd_num = prd_id.split("_")[1]
        assert prdcc_num == prd_num

    def test_prd_has_reference_molecule_list(self) -> None:
        """PRD fixture has pdbx_reference_molecule_list category."""
        fixture_path = FIXTURES_DIR / "PRD_000001.cif.gz"
        data = parse_cif_file(fixture_path)

        # PRD files typically have molecule list
        if "pdbx_reference_molecule_list" in data:
            mol_list = data["pdbx_reference_molecule_list"]
            assert len(mol_list) > 0
