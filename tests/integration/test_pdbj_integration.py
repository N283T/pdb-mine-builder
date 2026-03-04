"""Integration tests for pdbj pipeline (CIF format)."""

from pathlib import Path

import psycopg
import pytest
from psycopg import sql
from psycopg.rows import dict_row

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import Job
from mine2.parsers.cif import parse_cif_file
from mine2.pipelines.pdbj import PdbjCifPipeline


def create_test_settings(data_dir: Path, conninfo: str) -> Settings:
    """Create test settings with real DB connection."""
    return Settings(
        rdb=RdbConfig(nworkers=1, constring=conninfo),
        pipelines={
            "pdbj": PipelineConfig(
                data=str(data_dir),
            )
        },
    )


@pytest.mark.integration
class TestPdbjCifPipelineIntegration:
    """Integration tests for PdbjCifPipeline with real database."""

    def test_process_single_entry_1crn(
        self,
        db_connection: str,
        pdbj_schema,
        pdbj_fixtures_dir: Path,
    ) -> None:
        """Process 1crn (crambin) and verify data in database."""
        cif_path = pdbj_fixtures_dir / "1crn.cif.gz"
        assert cif_path.exists(), f"Fixture not found: {cif_path}"

        settings = create_test_settings(pdbj_fixtures_dir, db_connection)
        config = settings.pipelines["pdbj"]

        pipeline = PdbjCifPipeline(settings, config, pdbj_schema)
        job = Job(entry_id="1crn", filepath=cif_path, extra={"plus_path": None})

        result = pipeline.process_job(job, pdbj_schema, db_connection)

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "1crn"
        assert result.rows_inserted > 0

    def test_process_single_entry_1ubq(
        self,
        db_connection: str,
        pdbj_schema,
        pdbj_fixtures_dir: Path,
    ) -> None:
        """Process 1ubq (ubiquitin) and verify data in database."""
        cif_path = pdbj_fixtures_dir / "1ubq.cif.gz"
        assert cif_path.exists(), f"Fixture not found: {cif_path}"

        settings = create_test_settings(pdbj_fixtures_dir, db_connection)
        config = settings.pipelines["pdbj"]

        pipeline = PdbjCifPipeline(settings, config, pdbj_schema)
        job = Job(entry_id="1ubq", filepath=cif_path, extra={"plus_path": None})

        result = pipeline.process_job(job, pdbj_schema, db_connection)

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "1ubq"
        assert result.rows_inserted > 0

    def test_verify_entry_table_data(
        self,
        db_connection: str,
        pdbj_schema,
        pdbj_fixtures_dir: Path,
    ) -> None:
        """Verify entry table contains correct data after processing."""
        cif_path = pdbj_fixtures_dir / "1crn.cif.gz"
        settings = create_test_settings(pdbj_fixtures_dir, db_connection)
        config = settings.pipelines["pdbj"]

        pipeline = PdbjCifPipeline(settings, config, pdbj_schema)
        job = Job(entry_id="1crn", filepath=cif_path, extra={"plus_path": None})

        result = pipeline.process_job(job, pdbj_schema, db_connection)
        assert result.success

        # Query the database
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL("SELECT pdbid, id FROM {}.entry WHERE pdbid = %s").format(
                        sql.Identifier(pdbj_schema.schema_name)
                    ),
                    ("1crn",),
                )
                row = cur.fetchone()

        assert row is not None
        assert row["pdbid"] == "1crn"
        assert row["id"] == "1CRN"

    def test_verify_cell_table_data(
        self,
        db_connection: str,
        pdbj_schema,
        pdbj_fixtures_dir: Path,
    ) -> None:
        """Verify cell table contains crystal cell parameters."""
        cif_path = pdbj_fixtures_dir / "1crn.cif.gz"
        settings = create_test_settings(pdbj_fixtures_dir, db_connection)
        config = settings.pipelines["pdbj"]

        pipeline = PdbjCifPipeline(settings, config, pdbj_schema)
        job = Job(entry_id="1crn", filepath=cif_path, extra={"plus_path": None})

        result = pipeline.process_job(job, pdbj_schema, db_connection)
        assert result.success

        # Query the database for cell parameters
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT pdbid, length_a, length_b, length_c "
                        "FROM {}.cell WHERE pdbid = %s"
                    ).format(sql.Identifier(pdbj_schema.schema_name)),
                    ("1crn",),
                )
                row = cur.fetchone()

        assert row is not None
        assert row["pdbid"] == "1crn"
        # 1crn has orthorhombic crystal: a=40.96, b=18.65, c=22.52
        assert row["length_a"] is not None
        assert row["length_b"] is not None
        assert row["length_c"] is not None

    def test_process_multiple_entries(
        self,
        db_connection: str,
        pdbj_schema,
        pdbj_fixtures_dir: Path,
    ) -> None:
        """Process multiple entries and verify all are in database."""
        settings = create_test_settings(pdbj_fixtures_dir, db_connection)
        config = settings.pipelines["pdbj"]

        pipeline = PdbjCifPipeline(settings, config, pdbj_schema)

        # Process both fixtures
        for entry_id in ["1crn", "1ubq"]:
            cif_path = pdbj_fixtures_dir / f"{entry_id}.cif.gz"
            if cif_path.exists():
                job = Job(
                    entry_id=entry_id, filepath=cif_path, extra={"plus_path": None}
                )
                result = pipeline.process_job(job, pdbj_schema, db_connection)
                assert result.success, f"Processing {entry_id} failed: {result.error}"

        # Verify both entries exist in database
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL("SELECT COUNT(*) as count FROM {}.entry").format(
                        sql.Identifier(pdbj_schema.schema_name)
                    )
                )
                row = cur.fetchone()

        assert row["count"] >= 2

    def test_idempotent_processing(
        self,
        db_connection: str,
        pdbj_schema,
        pdbj_fixtures_dir: Path,
    ) -> None:
        """Processing same entry twice should not create duplicates."""
        cif_path = pdbj_fixtures_dir / "1crn.cif.gz"
        settings = create_test_settings(pdbj_fixtures_dir, db_connection)
        config = settings.pipelines["pdbj"]

        pipeline = PdbjCifPipeline(settings, config, pdbj_schema)
        job = Job(entry_id="1crn", filepath=cif_path, extra={"plus_path": None})

        # Process twice
        result1 = pipeline.process_job(job, pdbj_schema, db_connection)
        result2 = pipeline.process_job(job, pdbj_schema, db_connection)

        assert result1.success
        assert result2.success

        # Verify only one entry exists
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT COUNT(*) as count FROM {}.entry WHERE pdbid = %s"
                    ).format(sql.Identifier(pdbj_schema.schema_name)),
                    ("1crn",),
                )
                row = cur.fetchone()

        assert row["count"] == 1


@pytest.mark.integration
class TestPdbjCifParserIntegration:
    """Integration tests for CIF parser with fixture files."""

    def test_parse_1crn_has_expected_categories(self, pdbj_fixtures_dir: Path) -> None:
        """Parse 1crn and verify it has expected mmCIF categories."""
        cif_path = pdbj_fixtures_dir / "1crn.cif.gz"
        data = parse_cif_file(cif_path)

        expected_categories = [
            "entry",
            "cell",
            "symmetry",
            "entity",
            "struct",
        ]
        for cat in expected_categories:
            assert cat in data, f"Missing category: {cat}"

    def test_parse_1ubq_entry_data(self, pdbj_fixtures_dir: Path) -> None:
        """Parse 1ubq and verify entry data."""
        cif_path = pdbj_fixtures_dir / "1ubq.cif.gz"
        data = parse_cif_file(cif_path)

        assert data["_block_name"] == "1UBQ"
        assert "entry" in data
        assert data["entry"][0]["id"] == "1UBQ"
