"""Integration tests for ccmodel (Chemical Component Models) pipeline."""

from pathlib import Path

import gemmi
import psycopg
import pytest
from psycopg import sql
from psycopg.rows import dict_row

from pdbminebuilder.pipelines.ccmodel import _process_ccmodel_cif_block


@pytest.mark.integration
class TestCcmodelCifPipelineIntegration:
    """Integration tests for ccmodel CIF pipeline with real database."""

    def test_process_m_dal_model(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Process M_DAL_00001 model and verify data in database."""
        cif_path = ccmodel_fixtures_dir / "M_DAL_00001.cif.gz"
        assert cif_path.exists(), f"Fixture not found: {cif_path}"

        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "M_DAL_00001"

    def test_process_m_eoh_model(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Process M_EOH_00001 model and verify data in database."""
        cif_path = ccmodel_fixtures_dir / "M_EOH_00001.cif.gz"
        assert cif_path.exists(), f"Fixture not found: {cif_path}"

        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "M_EOH_00001"

    def test_process_m_6el_model(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Process M_6EL_00001 model and verify data in database."""
        cif_path = ccmodel_fixtures_dir / "M_6EL_00001.cif.gz"
        assert cif_path.exists(), f"Fixture not found: {cif_path}"

        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "M_6EL_00001"

    def test_process_m_94m_model(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Process M_94M_00001 model and verify data in database."""
        cif_path = ccmodel_fixtures_dir / "M_94M_00001.cif.gz"
        assert cif_path.exists(), f"Fixture not found: {cif_path}"

        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )

        assert result.success, f"Processing failed: {result.error}"
        assert result.entry_id == "M_94M_00001"

    def test_verify_pdbx_chem_comp_model_table_data(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Verify pdbx_chem_comp_model table contains data after processing."""
        cif_path = ccmodel_fixtures_dir / "M_DAL_00001.cif.gz"
        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )
        assert result.success

        # Query the database
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT id, comp_id FROM {}.pdbx_chem_comp_model WHERE id = %s"
                    ).format(sql.Identifier(ccmodel_schema.schema)),
                    ("M_DAL_00001",),
                )
                row = cur.fetchone()

        assert row is not None
        assert row["id"] == "M_DAL_00001"
        assert row["comp_id"] == "DAL"

    def test_process_all_fixtures(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Process all ccmodel fixtures and verify all are in database."""
        # Process all fixtures
        fixtures = [
            "M_DAL_00001",
            "M_EOH_00001",
            "M_6EL_00001",
            "M_94M_00001",
        ]
        for entry_id in fixtures:
            cif_path = ccmodel_fixtures_dir / f"{entry_id}.cif.gz"
            if cif_path.exists():
                doc = gemmi.cif.read(str(cif_path))
                block = doc[0]
                result = _process_ccmodel_cif_block(
                    block=block,
                    schema_name=ccmodel_schema.schema,
                    conninfo=db_connection,
                )
                assert result.success, f"Processing {entry_id} failed: {result.error}"

        # Verify all entries exist
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT COUNT(*) as count FROM {}.pdbx_chem_comp_model"
                    ).format(sql.Identifier(ccmodel_schema.schema))
                )
                row = cur.fetchone()

        assert row["count"] >= 4

    def test_idempotent_processing(
        self,
        db_connection: str,
        ccmodel_schema,
        ccmodel_fixtures_dir: Path,
    ) -> None:
        """Processing same model twice should not create duplicates."""
        cif_path = ccmodel_fixtures_dir / "M_DAL_00001.cif.gz"
        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        # Process twice
        result1 = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )
        result2 = _process_ccmodel_cif_block(
            block=block,
            schema_name=ccmodel_schema.schema,
            conninfo=db_connection,
        )

        assert result1.success
        assert result2.success

        # Verify only one entry exists
        with psycopg.connect(db_connection) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    sql.SQL(
                        "SELECT COUNT(*) as count FROM {}.pdbx_chem_comp_model "
                        "WHERE id = %s"
                    ).format(sql.Identifier(ccmodel_schema.schema)),
                    ("M_DAL_00001",),
                )
                row = cur.fetchone()

        assert row["count"] == 1
