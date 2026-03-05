"""Integration tests for prd (BIRD) pipeline."""

from pathlib import Path

import gemmi
import psycopg
import pytest
from psycopg import sql
from psycopg.rows import dict_row

from pdbminebuilder.pipelines.prd import _process_prd_cif_block


@pytest.mark.integration
class TestPrdCifPipelineIntegration:
    """Integration tests for PrdCifPipeline with real database."""

    def test_process_prd_000001(
        self,
        db_connection: str,
        prd_schema,
        prd_fixtures_dir: Path,
    ) -> None:
        """Process PRD_000001 and verify data in database."""
        prd_path = prd_fixtures_dir / "PRD_000001.cif.gz"
        prdcc_path = prd_fixtures_dir / "PRDCC_000001.cif.gz"
        assert prd_path.exists(), f"Fixture not found: {prd_path}"
        assert prdcc_path.exists(), f"PRDCC fixture not found: {prdcc_path}"

        prd_doc = gemmi.cif.read(str(prd_path))
        prdcc_doc = gemmi.cif.read(str(prdcc_path))
        prd_block = prd_doc[0]
        prdcc_block = prdcc_doc[0]

        result = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name=prd_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "PRD_000001"

    def test_process_prd_000006(
        self,
        db_connection: str,
        prd_schema,
        prd_fixtures_dir: Path,
    ) -> None:
        """Process PRD_000006 and verify data in database."""
        prd_path = prd_fixtures_dir / "PRD_000006.cif.gz"
        prdcc_path = prd_fixtures_dir / "PRDCC_000006.cif.gz"
        assert prd_path.exists(), f"Fixture not found: {prd_path}"
        assert prdcc_path.exists(), f"PRDCC fixture not found: {prdcc_path}"

        prd_doc = gemmi.cif.read(str(prd_path))
        prdcc_doc = gemmi.cif.read(str(prdcc_path))
        prd_block = prd_doc[0]
        prdcc_block = prdcc_doc[0]

        result = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name=prd_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "PRD_000006"

    def test_process_prd_000007(
        self,
        db_connection: str,
        prd_schema,
        prd_fixtures_dir: Path,
    ) -> None:
        """Process PRD_000007 and verify data in database."""
        prd_path = prd_fixtures_dir / "PRD_000007.cif.gz"
        prdcc_path = prd_fixtures_dir / "PRDCC_000007.cif.gz"
        assert prd_path.exists(), f"Fixture not found: {prd_path}"
        assert prdcc_path.exists(), f"PRDCC fixture not found: {prdcc_path}"

        prd_doc = gemmi.cif.read(str(prd_path))
        prdcc_doc = gemmi.cif.read(str(prdcc_path))
        prd_block = prd_doc[0]
        prdcc_block = prdcc_doc[0]

        result = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name=prd_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "PRD_000007"

    def test_verify_pdbx_reference_molecule_table_data(
        self,
        db_connection: str,
        prd_schema,
        prd_fixtures_dir: Path,
    ) -> None:
        """Verify pdbx_reference_molecule table contains data after processing."""
        prd_path = prd_fixtures_dir / "PRD_000001.cif.gz"
        prdcc_path = prd_fixtures_dir / "PRDCC_000001.cif.gz"

        prd_doc = gemmi.cif.read(str(prd_path))
        prdcc_doc = gemmi.cif.read(str(prdcc_path))
        prd_block = prd_doc[0]
        prdcc_block = prdcc_doc[0]

        result = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name=prd_schema.schema,
            conninfo=db_connection,
        )
        assert result.success

        # Query the database
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT prd_id, name FROM {}.pdbx_reference_molecule "
                        "WHERE prd_id = %s"
                    ).format(sql.Identifier(prd_schema.schema)),
                    ("PRD_000001",),
                )
                row = cur.fetchone()

        assert row is not None
        assert row["prd_id"] == "PRD_000001"

    def test_process_all_prd_fixtures(
        self,
        db_connection: str,
        prd_schema,
        prd_fixtures_dir: Path,
    ) -> None:
        """Process all PRD fixtures and verify all are in database."""
        # Process all fixtures
        prd_ids = ["PRD_000001", "PRD_000006", "PRD_000007"]
        for prd_id in prd_ids:
            prd_path = prd_fixtures_dir / f"{prd_id}.cif.gz"
            prdcc_id = prd_id.replace("PRD_", "PRDCC_")
            prdcc_path = prd_fixtures_dir / f"{prdcc_id}.cif.gz"

            if prd_path.exists() and prdcc_path.exists():
                prd_doc = gemmi.cif.read(str(prd_path))
                prdcc_doc = gemmi.cif.read(str(prdcc_path))
                prd_block = prd_doc[0]
                prdcc_block = prdcc_doc[0]

                result = _process_prd_cif_block(
                    prd_block=prd_block,
                    prdcc_block=prdcc_block,
                    schema_name=prd_schema.schema,
                    conninfo=db_connection,
                )
                assert result.success, f"Processing {prd_id} failed: {result.error}"

        # Verify all entries exist
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT COUNT(*) as count FROM {}.pdbx_reference_molecule"
                    ).format(sql.Identifier(prd_schema.schema))
                )
                row = cur.fetchone()

        assert row["count"] >= 3

    def test_idempotent_processing(
        self,
        db_connection: str,
        prd_schema,
        prd_fixtures_dir: Path,
    ) -> None:
        """Processing same PRD twice should not create duplicates."""
        prd_path = prd_fixtures_dir / "PRD_000001.cif.gz"
        prdcc_path = prd_fixtures_dir / "PRDCC_000001.cif.gz"

        prd_doc = gemmi.cif.read(str(prd_path))
        prdcc_doc = gemmi.cif.read(str(prdcc_path))
        prd_block = prd_doc[0]
        prdcc_block = prdcc_doc[0]

        # Process twice
        result1 = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name=prd_schema.schema,
            conninfo=db_connection,
        )
        result2 = _process_prd_cif_block(
            prd_block=prd_block,
            prdcc_block=prdcc_block,
            schema_name=prd_schema.schema,
            conninfo=db_connection,
        )

        assert result1.success
        assert result2.success

        # Verify only one entry exists
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT COUNT(*) as count FROM {}.pdbx_reference_molecule "
                        "WHERE prd_id = %s"
                    ).format(sql.Identifier(prd_schema.schema)),
                    ("PRD_000001",),
                )
                row = cur.fetchone()

        assert row["count"] == 1
