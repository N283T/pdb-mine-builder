"""Integration tests for cc (Chemical Components) pipeline."""

from pathlib import Path

import psycopg
import pytest
from psycopg import sql
from psycopg.rows import dict_row

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import Job
from mine2.pipelines.cc import (
    CcPipeline,
    _generate_canonical_smiles,
    _read_mmjson_block,
)


def create_test_settings(data_dir: Path, conninfo: str) -> Settings:
    """Create test settings with real DB connection."""
    return Settings(
        rdb=RdbConfig(nworkers=1, constring=conninfo),
        pipelines={
            "cc": PipelineConfig(
                deffile="schemas/cc.def.yml",
                data=str(data_dir),
            )
        },
    )


@pytest.mark.integration
class TestCcPipelineIntegration:
    """Integration tests for CcPipeline (mmJSON) with real database."""

    def test_process_atp_component(
        self,
        db_connection: str,
        cc_schema,
        cc_fixtures_dir: Path,
    ) -> None:
        """Process ATP component and verify data in database."""
        atp_path = cc_fixtures_dir / "ATP.json.gz"
        assert atp_path.exists(), f"Fixture not found: {atp_path}"

        settings = create_test_settings(cc_fixtures_dir, db_connection)
        config = settings.pipelines["cc"]

        pipeline = CcPipeline(settings, config, cc_schema)
        job = Job(entry_id="ATP", filepath=atp_path, extra={})

        result = pipeline.process_job(job, cc_schema, db_connection)

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "ATP"

    def test_process_hoh_component(
        self,
        db_connection: str,
        cc_schema,
        cc_fixtures_dir: Path,
    ) -> None:
        """Process HOH (water) component and verify data in database."""
        hoh_path = cc_fixtures_dir / "HOH.json.gz"
        assert hoh_path.exists(), f"Fixture not found: {hoh_path}"

        settings = create_test_settings(cc_fixtures_dir, db_connection)
        config = settings.pipelines["cc"]

        pipeline = CcPipeline(settings, config, cc_schema)
        job = Job(entry_id="HOH", filepath=hoh_path, extra={})

        result = pipeline.process_job(job, cc_schema, db_connection)

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "HOH"

    def test_process_eoh_component(
        self,
        db_connection: str,
        cc_schema,
        cc_fixtures_dir: Path,
    ) -> None:
        """Process EOH (ethanol) component and verify data in database."""
        eoh_path = cc_fixtures_dir / "EOH.json.gz"
        assert eoh_path.exists(), f"Fixture not found: {eoh_path}"

        settings = create_test_settings(cc_fixtures_dir, db_connection)
        config = settings.pipelines["cc"]

        pipeline = CcPipeline(settings, config, cc_schema)
        job = Job(entry_id="EOH", filepath=eoh_path, extra={})

        result = pipeline.process_job(job, cc_schema, db_connection)

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "EOH"

    def test_verify_chem_comp_table_data(
        self,
        db_connection: str,
        cc_schema,
        cc_fixtures_dir: Path,
    ) -> None:
        """Verify chem_comp table contains correct data after processing."""
        hoh_path = cc_fixtures_dir / "HOH.json.gz"
        settings = create_test_settings(cc_fixtures_dir, db_connection)
        config = settings.pipelines["cc"]

        pipeline = CcPipeline(settings, config, cc_schema)
        job = Job(entry_id="HOH", filepath=hoh_path, extra={})

        result = pipeline.process_job(job, cc_schema, db_connection)
        assert result.success

        # Query the database
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT id, name, type FROM {}.chem_comp WHERE id = %s"
                    ).format(sql.Identifier(cc_schema.schema_name)),
                    ("HOH",),
                )
                row = cur.fetchone()

        assert row is not None
        assert row["id"] == "HOH"
        assert "water" in row["name"].lower()

    def test_verify_brief_summary_has_smiles(
        self,
        db_connection: str,
        cc_schema,
        cc_fixtures_dir: Path,
    ) -> None:
        """Verify brief_summary table has SMILES after processing."""
        eoh_path = cc_fixtures_dir / "EOH.json.gz"
        settings = create_test_settings(cc_fixtures_dir, db_connection)
        config = settings.pipelines["cc"]

        pipeline = CcPipeline(settings, config, cc_schema)
        job = Job(entry_id="EOH", filepath=eoh_path, extra={})

        result = pipeline.process_job(job, cc_schema, db_connection)
        assert result.success

        # Query the database for SMILES
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT comp_id, smiles FROM {}.brief_summary WHERE comp_id = %s"
                    ).format(sql.Identifier(cc_schema.schema_name)),
                    ("EOH",),
                )
                row = cur.fetchone()

        assert row is not None
        assert row["comp_id"] == "EOH"
        # Ethanol SMILES should contain CCO (canonical SMILES for ethanol)
        # smiles column is an array of SMILES variants
        assert "CCO" in row["smiles"]

    def test_process_multiple_components(
        self,
        db_connection: str,
        cc_schema,
        cc_fixtures_dir: Path,
    ) -> None:
        """Process multiple components and verify all are in database."""
        settings = create_test_settings(cc_fixtures_dir, db_connection)
        config = settings.pipelines["cc"]

        pipeline = CcPipeline(settings, config, cc_schema)

        components = ["ATP", "HOH", "EOH"]
        for comp_id in components:
            fixture_path = cc_fixtures_dir / f"{comp_id}.json.gz"
            if fixture_path.exists():
                job = Job(entry_id=comp_id, filepath=fixture_path, extra={})
                result = pipeline.process_job(job, cc_schema, db_connection)
                assert result.success, f"Processing {comp_id} failed: {result.error}"

        # Verify all components exist
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL("SELECT COUNT(*) as count FROM {}.chem_comp").format(
                        sql.Identifier(cc_schema.schema_name)
                    )
                )
                row = cur.fetchone()

        assert row["count"] >= 3


@pytest.mark.integration
class TestCcSmilesGeneration:
    """Integration tests for SMILES generation from mmJSON via ccd2rdmol."""

    def test_hoh_generates_water_smiles(self, cc_fixtures_dir: Path) -> None:
        """HOH fixture should generate water SMILES."""
        hoh_path = cc_fixtures_dir / "HOH.json.gz"
        block = _read_mmjson_block(hoh_path)
        assert block is not None

        smiles = _generate_canonical_smiles(block)
        assert smiles == "O"

    def test_eoh_generates_ethanol_smiles(self, cc_fixtures_dir: Path) -> None:
        """EOH fixture should generate ethanol SMILES."""
        eoh_path = cc_fixtures_dir / "EOH.json.gz"
        block = _read_mmjson_block(eoh_path)
        assert block is not None

        smiles = _generate_canonical_smiles(block)
        assert smiles == "CCO"

    def test_atp_generates_valid_smiles(self, cc_fixtures_dir: Path) -> None:
        """ATP fixture should generate valid SMILES with N and P."""
        atp_path = cc_fixtures_dir / "ATP.json.gz"
        block = _read_mmjson_block(atp_path)
        assert block is not None

        smiles = _generate_canonical_smiles(block)
        assert smiles is not None
        assert len(smiles) > 0
        assert "N" in smiles  # Adenine has nitrogen
        assert "P" in smiles  # Phosphate groups
