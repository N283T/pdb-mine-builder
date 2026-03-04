"""Tests for pdbj pipeline (mmJSON format) - Phase 5 features."""

import gzip
import json
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import (
    BigInteger,
    Column,
    Double,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import Job
from mine2.pipelines.pdbj import PdbjPipeline
from mine2.utils.assembly import hex_sha256


def create_test_mmjson_file(
    path: Path, entry_id: str, data: dict[str, list[dict]]
) -> None:
    """Create a test mmJSON file.

    mmJSON format is column-oriented:
    {"data_XXX": {"category": {"col1": [val1, val2], "col2": [val1, val2]}}}

    Args:
        path: Path to write the file (should end with .json.gz)
        entry_id: Entry ID (e.g., "100d")
        data: Dict of category name to list of row dicts
    """
    # Convert row-oriented to column-oriented
    block_data = {}
    for cat, rows in data.items():
        if not rows:
            continue
        columns = list(rows[0].keys())
        col_data = {col: [row.get(col) for row in rows] for col in columns}
        block_data[cat] = col_data

    mmjson = {"data_" + entry_id.upper(): block_data}
    content = json.dumps(mmjson)

    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt") as f:
        f.write(content)


def create_test_settings(data_dir: Path, plus_dir: Path | None = None) -> Settings:
    """Create test settings."""
    config = PipelineConfig(
        data=str(data_dir),
    )
    if plus_dir:
        config.data_plus = str(plus_dir)

    return Settings(
        rdb=RdbConfig(nworkers=2, constring="test"),
        pipelines={"pdbj": config},
    )


def create_test_meta() -> MetaData:
    """Create minimal test MetaData for pdbj."""
    meta = MetaData(schema="pdbj")
    meta.info = {"entry_pk": "pdbid"}
    Table(
        "entry",
        meta,
        Column("pdbid", Text),
        Column("id", Text),
        PrimaryKeyConstraint("pdbid", "id"),
    )
    Table(
        "pdbx_struct_assembly_gen",
        meta,
        Column("pdbid", Text),
        Column("asym_id_list", Text),
        Column("_hash_asym_id_list", Text),
        Column("assembly_id", Text),
        Column("oper_expression", Text),
        PrimaryKeyConstraint("pdbid", "assembly_id"),
    )
    Table(
        "brief_summary",
        meta,
        Column("pdbid", Text),
        Column("docid", BigInteger),
        Column("plus_fields", JSONB),
        PrimaryKeyConstraint("pdbid"),
    )
    Table(
        "entity",
        meta,
        Column("pdbid", Text),
        Column("id", Text),
        Column("formula_weight", Double),
        PrimaryKeyConstraint("pdbid", "id"),
    )
    Table(
        "struct_asym",
        meta,
        Column("pdbid", Text),
        Column("id", Text),
        Column("entity_id", Text),
        PrimaryKeyConstraint("pdbid", "id"),
    )
    Table(
        "pdbx_struct_assembly",
        meta,
        Column("pdbid", Text),
        Column("id", Text),
        Column("details", Text),
        PrimaryKeyConstraint("pdbid", "id"),
    )
    return meta


class TestHashAsymIdList:
    """Tests for _hash_asym_id_list computation."""

    @patch("mine2.pipelines.pdbj.sync_entry_tables")
    def test_hash_added_to_assembly_gen(self, mock_sync_entry_tables, tmp_path):
        """Test that _hash_asym_id_list is computed."""
        data_dir = tmp_path / "pdbj"
        data_dir.mkdir(parents=True)

        # Create test file with assembly_gen data
        mmjson_file = data_dir / "100d-noatom.json.gz"
        create_test_mmjson_file(
            mmjson_file,
            "100d",
            {
                "entry": [{"id": "100D"}],
                "pdbx_struct_assembly_gen": [
                    {
                        "assembly_id": "1",
                        "asym_id_list": "A,B,C",
                        "oper_expression": "1",
                    },
                ],
            },
        )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=mmjson_file, extra={})
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success

        table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
        assert "pdbx_struct_assembly_gen" in table_rows
        rows = table_rows["pdbx_struct_assembly_gen"]
        for row in rows:
            expected_hash = hex_sha256(row["asym_id_list"])
            assert row["_hash_asym_id_list"] == expected_hash

    @patch("mine2.pipelines.pdbj.sync_entry_tables")
    def test_hash_is_sha256(self, mock_sync_entry_tables, tmp_path):
        """Test that the hash is SHA256."""
        data_dir = tmp_path / "pdbj"
        data_dir.mkdir(parents=True)

        asym_id_list = "A,B,C"
        mmjson_file = data_dir / "100d-noatom.json.gz"
        create_test_mmjson_file(
            mmjson_file,
            "100d",
            {
                "entry": [{"id": "100D"}],
                "pdbx_struct_assembly_gen": [
                    {
                        "assembly_id": "1",
                        "asym_id_list": asym_id_list,
                        "oper_expression": "1",
                    },
                ],
            },
        )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=mmjson_file, extra={})
        pipeline.process_job(job, "pdbj", "test_conninfo")

        table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
        rows = table_rows["pdbx_struct_assembly_gen"]
        for row in rows:
            hash_value = row["_hash_asym_id_list"]
            assert len(hash_value) == 64
            assert all(c in "0123456789abcdef" for c in hash_value)


class TestBuMwCalculation:
    """Tests for bu_mw calculation in brief_summary."""

    @patch("mine2.pipelines.pdbj.sync_entry_tables")
    def test_bu_mw_in_plus_fields(self, mock_sync_entry_tables, tmp_path):
        """Test that bu_mw is calculated and added to plus_fields."""
        data_dir = tmp_path / "pdbj"
        data_dir.mkdir(parents=True)

        mmjson_file = data_dir / "100d-noatom.json.gz"
        create_test_mmjson_file(
            mmjson_file,
            "100d",
            {
                "entry": [{"id": "100D"}],
                "brief_summary": [{"docid": 100}],
                "entity": [{"id": "1", "formula_weight": "1000.0"}],
                "struct_asym": [{"id": "A", "entity_id": "1"}],
                "pdbx_struct_assembly": [{"id": "1", "details": "author_defined"}],
                "pdbx_struct_assembly_gen": [
                    {
                        "assembly_id": "1",
                        "asym_id_list": "A",
                        "oper_expression": "1",
                    },
                ],
            },
        )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=mmjson_file, extra={})
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success

        table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
        assert "brief_summary" in table_rows
        rows = table_rows["brief_summary"]
        for row in rows:
            plus_fields = row["plus_fields"]
            if isinstance(plus_fields, str):
                plus_fields = json.loads(plus_fields)
            assert "bu_mw" in plus_fields
            assert plus_fields["bu_mw"] == 1000.0

    @patch("mine2.pipelines.pdbj.sync_entry_tables")
    def test_bu_mw_zero_when_no_assembly(self, mock_sync_entry_tables, tmp_path):
        """Test that bu_mw is 0 when no assembly data."""
        data_dir = tmp_path / "pdbj"
        data_dir.mkdir(parents=True)

        mmjson_file = data_dir / "100d-noatom.json.gz"
        create_test_mmjson_file(
            mmjson_file,
            "100d",
            {
                "entry": [{"id": "100D"}],
                "brief_summary": [{"docid": 100}],
            },
        )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=mmjson_file, extra={})
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success

        table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
        rows = table_rows["brief_summary"]
        for row in rows:
            plus_fields = row["plus_fields"]
            if isinstance(plus_fields, str):
                plus_fields = json.loads(plus_fields)
            assert "bu_mw" in plus_fields
            assert plus_fields["bu_mw"] == 0.0


class TestExtractEntryId:
    """Tests for PdbjPipeline.extract_entry_id()."""

    def test_noatom_json_gz_extension(self, tmp_path):
        """Extract entry ID from -noatom.json.gz filename."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        entry_id = pipeline.extract_entry_id(Path("/path/to/100d-noatom.json.gz"))

        assert entry_id == "100d"

    def test_alphanumeric_id(self, tmp_path):
        """Extract alphanumeric entry ID."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        entry_id = pipeline.extract_entry_id(Path("/path/to/1a2b-noatom.json.gz"))

        assert entry_id == "1a2b"


class TestFindJobs:
    """Tests for PdbjPipeline.find_jobs()."""

    def test_find_mmjson_files(self, tmp_path):
        """Find mmJSON files in data directory."""
        data_dir = tmp_path / "pdbj"
        data_dir.mkdir(parents=True)

        create_test_mmjson_file(
            data_dir / "100d-noatom.json.gz", "100d", {"entry": [{"id": "100D"}]}
        )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].entry_id == "100d"

    def test_empty_directory(self, tmp_path):
        """Find jobs returns empty list for empty directory."""
        data_dir = tmp_path / "pdbj"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert jobs == []
