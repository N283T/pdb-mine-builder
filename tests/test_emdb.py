"""Tests for EMDB pipeline."""

from pathlib import Path
from unittest.mock import patch

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Column,
    Date,
    DateTime,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.pipelines.emdb import (
    EmdbPipeline,
    _ensure_list,
    _get_nested,
)


def create_test_emdb_xml_content(entry_id: str, docid: int) -> str:
    """Create EMDB XML content string.

    Args:
        entry_id: Entry ID without EMD- prefix (e.g., "1234")
        docid: Numeric ID (e.g., 1234)

    Returns:
        XML format string
    """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<emd xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" emdb_id="EMD-{entry_id}">
    <admin>
        <current_status>
            <code>REL</code>
        </current_status>
        <key_dates>
            <deposition>2020-01-15</deposition>
            <header_release>2020-03-01</header_release>
            <map_release>2020-03-01</map_release>
            <update>2020-06-15</update>
        </key_dates>
        <title>Test EMDB Entry {entry_id}</title>
    </admin>
    <crossreferences>
        <pdb_list>
            <pdb_reference>
                <pdb_id>1ABC</pdb_id>
            </pdb_reference>
        </pdb_list>
    </crossreferences>
    <sample>
        <supramolecule>
            <id>1</id>
            <name>Test Supramolecule</name>
        </supramolecule>
    </sample>
    <map>
        <format>CCP4</format>
        <size_kb>1024</size_kb>
    </map>
</emd>
"""


def create_test_emdb_xml_file(path: Path, entry_id: str, docid: int) -> None:
    """Create a test EMDB XML file."""
    content = create_test_emdb_xml_content(entry_id, docid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def create_test_settings(data_dir: Path) -> Settings:
    """Create test settings."""
    return Settings(
        rdb=RdbConfig(nworkers=2, constring="test"),
        pipelines={
            "emdb": PipelineConfig(
                data=str(data_dir),
            )
        },
    )


def create_test_meta() -> MetaData:
    """Create minimal test MetaData for EMDB."""
    meta = MetaData(schema="emdb")
    meta.info = {"entry_pk": "emdb_id"}
    Table(
        "brief_summary",
        meta,
        Column("emdb_id", Text),
        Column("docid", BigInteger),
        Column("deposition_date", Date),
        Column("header_release_date", Date),
        Column("map_release_date", Date),
        Column("modification_date", Date),
        Column("update_date", DateTime),
        Column("content", JSONB),
        Column("keywords", ARRAY(Text)),
        PrimaryKeyConstraint("emdb_id"),
    )
    Table(
        "em_admin",
        meta,
        Column("emdb_id", Text),
        Column("title", Text),
        PrimaryKeyConstraint("emdb_id"),
    )
    return meta


class TestExtractEntryId:
    """Tests for extract_entry_id method."""

    def test_standard_format(self, tmp_path):
        """Test standard EMDB filename: emd-1234-v1.0.xml."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        filepath = Path("emd-1234-v1.0.xml")
        assert pipeline.extract_entry_id(filepath) == "EMD-1234"

    def test_version_variations(self, tmp_path):
        """Test different version formats."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        assert pipeline.extract_entry_id(Path("emd-5678-v2.1.xml")) == "EMD-5678"
        assert pipeline.extract_entry_id(Path("emd-9999-v1.0.xml")) == "EMD-9999"

    def test_lowercase_to_uppercase(self, tmp_path):
        """Test that entry ID is uppercase."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        filepath = Path("emd-1234-v1.0.xml")
        result = pipeline.extract_entry_id(filepath)
        assert result == result.upper()


class TestFindJobs:
    """Tests for find_jobs method."""

    def test_find_xml_files(self, tmp_path):
        """Test finding XML files in directory."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        # Create test files
        create_test_emdb_xml_file(data_dir / "emd-1234-v1.0.xml", "1234", 1234)
        create_test_emdb_xml_file(data_dir / "emd-5678-v1.0.xml", "5678", 5678)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        jobs = pipeline.find_jobs()

        assert len(jobs) == 2
        entry_ids = {job.entry_id for job in jobs}
        assert entry_ids == {"EMD-1234", "EMD-5678"}

    def test_find_with_limit(self, tmp_path):
        """Test finding files with limit."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        # Create multiple test files
        for i in range(5):
            create_test_emdb_xml_file(
                data_dir / f"emd-{1000 + i}-v1.0.xml", str(1000 + i), 1000 + i
            )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        jobs = pipeline.find_jobs(limit=2)

        assert len(jobs) == 2

    def test_empty_directory(self, tmp_path):
        """Test finding files in empty directory."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        jobs = pipeline.find_jobs()

        assert len(jobs) == 0


class TestXmlParsing:
    """Tests for XML parsing utilities."""

    def test_ensure_list_with_none(self):
        """Test _ensure_list with None."""
        assert _ensure_list(None) == []

    def test_ensure_list_with_value(self):
        """Test _ensure_list with single value."""
        assert _ensure_list("test") == ["test"]

    def test_ensure_list_with_list(self):
        """Test _ensure_list with list."""
        assert _ensure_list(["a", "b"]) == ["a", "b"]

    def test_get_nested_existing(self):
        """Test _get_nested with existing path."""
        data = {"a": {"b": {"c": "value"}}}
        assert _get_nested(data, "a", "b", "c") == "value"

    def test_get_nested_missing(self):
        """Test _get_nested with missing path."""
        data = {"a": {"b": {}}}
        assert _get_nested(data, "a", "b", "c") is None

    def test_get_nested_partial(self):
        """Test _get_nested with partial path."""
        data = {"a": {"b": "not_dict"}}
        assert _get_nested(data, "a", "b", "c") is None


class TestTransformBriefSummary:
    """Tests for brief_summary transformation."""

    def test_docid_extraction(self, tmp_path):
        """Test that docid is correctly extracted from entry ID."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        xml_data = {
            "admin": {
                "key_dates": {
                    "deposition": "2020-01-15",
                    "header_release": "2020-03-01",
                    "map_release": "2020-03-01",
                    "update": "2020-06-15",
                }
            }
        }
        row_data = {}

        result = pipeline._transform_brief_summary(xml_data, row_data, "EMD-1234", meta)

        assert len(result) == 1
        assert result[0]["emdb_id"] == "EMD-1234"
        assert result[0]["docid"] == 1234

    def test_dates_extraction(self, tmp_path):
        """Test that dates are correctly extracted."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        xml_data = {
            "admin": {
                "key_dates": {
                    "deposition": "2020-01-15",
                    "header_release": "2020-03-01",
                    "map_release": "2020-03-15",
                    "update": "2020-06-15",
                }
            }
        }
        row_data = {}

        result = pipeline._transform_brief_summary(xml_data, row_data, "EMD-1234", meta)

        assert result[0]["deposition_date"] == "2020-01-15"
        assert result[0]["header_release_date"] == "2020-03-01"
        assert result[0]["map_release_date"] == "2020-03-15"
        assert result[0]["modification_date"] == "2020-06-15"

    def test_content_as_jsonb(self, tmp_path):
        """Test that content is stored as JSON string."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        xml_data = {"admin": {"key_dates": {}}}
        row_data = {"em_admin": [{"title": "Test"}]}

        result = pipeline._transform_brief_summary(xml_data, row_data, "EMD-1234", meta)

        import json

        content = json.loads(result[0]["content"])
        assert "em_admin" in content
        assert content["em_admin"][0]["title"] == "Test"

    def test_keywords_empty(self, tmp_path):
        """Test that keywords are empty array."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        xml_data = {"admin": {"key_dates": {}}}
        row_data = {}

        result = pipeline._transform_brief_summary(xml_data, row_data, "EMD-1234", meta)

        assert result[0]["keywords"] == []


class TestProcessJob:
    """Tests for process_job method."""

    @patch("mine2.pipelines.emdb.sync_entry_tables")
    def test_process_job_success(self, mock_bulk_upsert, tmp_path):
        """Test successful job processing."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        # Create test file
        xml_file = data_dir / "emd-1234-v1.0.xml"
        create_test_emdb_xml_file(xml_file, "1234", 1234)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        # Mock bulk_upsert to return success
        mock_bulk_upsert.return_value = (1, 0, 0)

        from mine2.db.loader import Job

        job = Job(entry_id="EMD-1234", filepath=xml_file, extra={})

        result = pipeline.process_job(job, "emdb", "test_conninfo")

        assert result.success is True
        assert result.entry_id == "EMD-1234"

    def test_process_job_file_not_found(self, tmp_path):
        """Test job processing with non-existent file."""
        data_dir = tmp_path / "emdb"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["emdb"]
        meta = create_test_meta()
        pipeline = EmdbPipeline(settings, config, meta)

        from mine2.db.loader import Job

        job = Job(
            entry_id="EMD-9999",
            filepath=data_dir / "nonexistent.xml",
            extra={},
        )

        result = pipeline.process_job(job, "emdb", "test_conninfo")

        assert result.success is False
        assert "EMD-9999" in result.entry_id
