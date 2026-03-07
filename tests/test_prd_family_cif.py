"""Tests for prd_family pipeline (CIF format)."""

from pathlib import Path

import gemmi
from sqlalchemy import MetaData

from pdbminebuilder.config import PipelineConfig, RdbConfig, Settings
from pdbminebuilder.parsers.cif import parse_block
from pdbminebuilder.pipelines.prd_family import (
    PrdFamilyCifPipeline,
    _generate_brief_summary,
    _parse_prd_family_cif_block,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "prd_family"


def create_test_settings(data_dir: Path) -> Settings:
    """Create test settings."""
    return Settings(
        rdb=RdbConfig(nworkers=1, constring="test"),
        pipelines={
            "prd_family": PipelineConfig(
                data=str(data_dir),
            )
        },
    )


class TestGenerateBriefSummary:
    """Tests for _generate_brief_summary function."""

    def test_with_full_data(self) -> None:
        """Generate brief_summary from audit and family data."""
        data = {
            "pdbx_reference_molecule_family": [
                {
                    "family_prd_id": "FAM_000001",
                    "name": "Actinomycin",
                    "release_status": "REL",
                }
            ],
            "pdbx_family_prd_audit": [
                {
                    "family_prd_id": "FAM_000001",
                    "date": "2011-07-13",
                    "action_type": "Initial release",
                },
                {
                    "family_prd_id": "FAM_000001",
                    "date": "2017-09-13",
                    "action_type": "Modify record",
                },
            ],
        }
        result = _generate_brief_summary(data, "FAM_000001")

        assert len(result) == 1
        assert result[0]["family_prd_id"] == "FAM_000001"
        assert result[0]["name"] == "Actinomycin"
        assert result[0]["pdbx_initial_date"] == "2011-07-13"
        assert result[0]["pdbx_modified_date"] == "2017-09-13"

    def test_without_audit_data(self) -> None:
        """Generate brief_summary with no audit dates."""
        data = {
            "pdbx_reference_molecule_family": [
                {"family_prd_id": "FAM_000001", "name": "Test Family"}
            ]
        }
        result = _generate_brief_summary(data, "FAM_000001")

        assert len(result) == 1
        assert result[0]["name"] == "Test Family"
        assert result[0]["pdbx_initial_date"] is None
        assert result[0]["pdbx_modified_date"] is None

    def test_without_family_data(self) -> None:
        """Generate brief_summary with no family data."""
        data = {}
        result = _generate_brief_summary(data, "FAM_000001")

        assert len(result) == 1
        assert result[0]["name"] is None


class TestParsePrdFamilyCifBlock:
    """Tests for _parse_prd_family_cif_block function."""

    def test_parse_real_fixture(self) -> None:
        """Parse real FAM_000001 block from fixture."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

        doc = gemmi.cif.read(str(fixture_path))
        block = doc[0]

        family_id, table_rows, error = _parse_prd_family_cif_block(block, "prd_family")

        assert error is None
        assert family_id == "FAM_000001"
        assert "brief_summary" in table_rows
        assert "pdbx_reference_molecule_family" in table_rows
        assert "pdbx_reference_molecule_list" in table_rows
        assert "citation" in table_rows
        assert "citation_author" in table_rows
        assert "pdbx_family_prd_audit" in table_rows

        # Check brief_summary content
        brief = table_rows["brief_summary"][0]
        assert brief["family_prd_id"] == "FAM_000001"
        assert brief["name"] is not None

        # Check citation has family_prd_id injected
        for row in table_rows["citation"]:
            assert row["family_prd_id"] == "FAM_000001"

        # Check citation_author has family_prd_id injected
        for row in table_rows["citation_author"]:
            assert row["family_prd_id"] == "FAM_000001"

    def test_parse_second_block(self) -> None:
        """Parse second block from fixture."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        doc = gemmi.cif.read(str(fixture_path))
        block = doc[1]

        family_id, table_rows, error = _parse_prd_family_cif_block(block, "prd_family")

        assert error is None
        assert family_id == "FAM_000003"
        assert "brief_summary" in table_rows


class TestFindCifFile:
    """Tests for PrdFamilyCifPipeline._find_cif_file()."""

    def test_direct_path(self, tmp_path: Path) -> None:
        """Find CIF file at direct path."""
        cif_path = tmp_path.joinpath("family-all.cif.gz")
        cif_path.write_bytes(b"dummy")

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd_family"]
        meta = MetaData(schema="prd_family")
        meta.info = {"entry_pk": "family_prd_id"}

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_nested_path_rsync_quirk(self, tmp_path: Path) -> None:
        """Find CIF file in nested directory (rsync quirk)."""
        nested_dir = tmp_path.joinpath("family-all.cif.gz")
        nested_dir.mkdir()
        cif_path = nested_dir.joinpath("family-all.cif.gz")
        cif_path.write_bytes(b"dummy")

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd_family"]
        meta = MetaData(schema="prd_family")
        meta.info = {"entry_pk": "family_prd_id"}

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_not_found(self, tmp_path: Path) -> None:
        """Return None when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd_family"]
        meta = MetaData(schema="prd_family")
        meta.info = {"entry_pk": "family_prd_id"}

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found is None

    def test_directory_not_exists(self, tmp_path: Path) -> None:
        """Return None when data directory doesn't exist."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["prd_family"]
        meta = MetaData(schema="prd_family")
        meta.info = {"entry_pk": "family_prd_id"}

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found is None


class TestPrdFamilyCifPipelineRun:
    """Tests for PrdFamilyCifPipeline.run() method."""

    def test_run_returns_empty_when_no_file(self, tmp_path: Path) -> None:
        """Run returns empty list when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["prd_family"]
        meta = MetaData(schema="prd_family")
        meta.info = {"entry_pk": "family_prd_id"}

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        results = pipeline.run()

        assert results == []

    def test_run_with_fixture(self) -> None:
        """Run pipeline with real fixture data (sequential, no DB)."""
        from pdbminebuilder.models import get_metadata

        meta = get_metadata("prd_family")
        settings = create_test_settings(FIXTURES_DIR)
        config = settings.pipelines["prd_family"]

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        # This will parse successfully but fail at batch upsert (no DB)
        # We just verify parsing works
        results = pipeline.run(limit=2)

        # All entries should be processed (success depends on DB availability)
        assert len(results) == 2

    def test_run_respects_limit(self) -> None:
        """Run respects the limit parameter."""
        from pdbminebuilder.models import get_metadata

        meta = get_metadata("prd_family")
        settings = create_test_settings(FIXTURES_DIR)
        config = settings.pipelines["prd_family"]

        pipeline = PrdFamilyCifPipeline(settings, config, meta)
        results = pipeline.run(limit=1)

        assert len(results) == 1


class TestRealFixtures:
    """Tests using real prd_family CIF fixture files."""

    def test_fixture_exists(self) -> None:
        """Fixture file exists and is readable."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        assert fixture_path.exists()

        doc = gemmi.cif.read(str(fixture_path))
        assert len(doc) == 2

    def test_fixture_block_names(self) -> None:
        """Fixture blocks have expected names."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        doc = gemmi.cif.read(str(fixture_path))

        assert doc[0].name == "FAM_000001"
        assert doc[1].name == "FAM_000003"

    def test_fixture_has_expected_categories(self) -> None:
        """First block has expected categories."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        doc = gemmi.cif.read(str(fixture_path))
        data = parse_block(doc[0])

        assert "pdbx_reference_molecule_family" in data
        assert "pdbx_reference_molecule_list" in data
        assert "citation" in data
        assert "citation_author" in data
        assert "pdbx_family_prd_audit" in data

    def test_citation_has_no_family_prd_id(self) -> None:
        """Citation category in raw data lacks family_prd_id (needs PK injection)."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        doc = gemmi.cif.read(str(fixture_path))
        data = parse_block(doc[0])

        citation_rows = data.get("citation", [])
        assert len(citation_rows) > 0
        # Raw CIF data should NOT have family_prd_id
        assert "family_prd_id" not in citation_rows[0]

    def test_pk_injection_via_transform(self) -> None:
        """transform_category injects family_prd_id into citation rows."""
        fixture_path = FIXTURES_DIR / "family-all.cif.gz"
        doc = gemmi.cif.read(str(fixture_path))

        family_id, table_rows, error = _parse_prd_family_cif_block(doc[0], "prd_family")

        assert error is None
        # After transform, citation rows should have family_prd_id
        for row in table_rows["citation"]:
            assert row["family_prd_id"] == "FAM_000001"

        for row in table_rows["citation_author"]:
            assert row["family_prd_id"] == "FAM_000001"
