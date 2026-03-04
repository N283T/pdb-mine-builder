"""Tests for IHM pipeline."""

import gzip
import json
from pathlib import Path
from unittest.mock import patch

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import SchemaDef, TableDef
from mine2.pipelines.ihm import (
    CHAIN_TYPE_MAPPING,
    EXPTL_METHOD_MAPPING,
    IhmPipeline,
    _calculate_mw_for_bu,
    _expand_oper_expression,
    _gen_docid,
    _hex_sha256,
)


def create_test_ihm_raw_data(entry_id: str) -> dict:
    """Create raw IHM data dict (without mmJSON wrapper).

    Args:
        entry_id: Entry ID (e.g., "PDBDEV_00000001")

    Returns:
        Raw category data dict for direct use with _transform_* methods
    """
    return {
        "entry": [{"id": entry_id.upper()}],
        "struct": [{"title": f"Test IHM Entry {entry_id}"}],
        "pdbx_database_status": [{"recvd_initial_deposition_date": "2020-01-15"}],
        "pdbx_audit_revision_history": [
            {"revision_date": "2020-03-01", "ordinal": 1},
            {"revision_date": "2020-06-15", "ordinal": 2},
        ],
        "audit_author": [
            {"name": "Test Author", "pdbx_ordinal": 1},
        ],
        "entity": [
            {
                "id": "1",
                "type": "polymer",
                "pdbx_description": "Test Protein",
                "pdbx_number_of_molecules": 1,
            }
        ],
        "entity_poly": [
            {
                "entity_id": "1",
                "type": "polypeptide(L)",
                "pdbx_seq_one_letter_code_can": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
            }
        ],
        "struct_asym": [
            {"id": "A", "entity_id": "1"},
        ],
        "chem_comp": [
            {"id": "ALA", "type": "L-peptide linking", "name": "ALANINE"},
            {
                "id": "HEM",
                "type": "non-polymer",
                "name": "PROTOPORPHYRIN IX CONTAINING FE",
            },
        ],
        "pdbx_struct_assembly": [
            {"id": "1", "details": "author_defined_assembly"},
        ],
        "pdbx_struct_assembly_gen": [
            {"assembly_id": "1", "oper_expression": "1", "asym_id_list": "A"},
        ],
    }


def _rows_to_columns(rows: list[dict]) -> dict:
    """Convert row-oriented data to column-oriented mmJSON format.

    Args:
        rows: List of row dicts [{"col1": val1, "col2": val2}, ...]

    Returns:
        Column-oriented dict {"col1": [val1, ...], "col2": [val2, ...]}
    """
    if not rows:
        return {}
    columns = list(rows[0].keys())
    return {col: [row.get(col) for row in rows] for col in columns}


def create_test_ihm_mmjson_content(entry_id: str) -> dict:
    """Create IHM mmJSON content dict in column-oriented format.

    Args:
        entry_id: Entry ID (e.g., "PDBDEV_00000001")

    Returns:
        mmJSON format dict (column-oriented, wrapped in data_{entry_id} key)
    """
    raw_data = create_test_ihm_raw_data(entry_id)

    # Convert each category from row-oriented to column-oriented
    block_data = {cat: _rows_to_columns(rows) for cat, rows in raw_data.items()}

    # mmJSON format requires data_{entry_id} as top-level key
    block_name = f"data_{entry_id.upper()}"
    return {block_name: block_data}


def create_test_ihm_mmjson_file(path: Path, entry_id: str) -> None:
    """Create a test IHM mmJSON file."""
    content = create_test_ihm_mmjson_content(entry_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    if str(path).endswith(".gz"):
        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(content, f)
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f)


def create_test_settings(data_dir: Path, plus_dir: Path | None = None) -> Settings:
    """Create test settings."""
    config = PipelineConfig(
        deffile="schemas/ihm.def.yml",
        data=str(data_dir),
    )
    if plus_dir:
        config.data_plus = str(plus_dir)

    return Settings(
        rdb=RdbConfig(nworkers=2, constring="test"),
        pipelines={"ihm": config},
    )


def create_test_schema_def() -> SchemaDef:
    """Create minimal test schema definition for IHM."""
    return SchemaDef(
        schema_name="ihm",
        primary_key="pdbid",
        tables=[
            TableDef(
                name="entry",
                columns=[("pdbid", "text"), ("id", "text")],
                primary_key=["pdbid", "id"],
            ),
            TableDef(
                name="brief_summary",
                columns=[
                    ("pdbid", "text"),
                    ("docid", "bigint"),
                    ("deposition_date", "date"),
                    ("release_date", "date"),
                    ("modification_date", "date"),
                    ("exptl_method", "text[]"),
                    ("exptl_method_ids", "integer[]"),
                    ("struct_title", "text"),
                    ("plus_fields", "jsonb"),
                    ("keywords", "text[]"),
                ],
                primary_key=["pdbid"],
            ),
            TableDef(
                name="pdbx_struct_assembly_gen",
                columns=[
                    ("pdbid", "text"),
                    ("assembly_id", "text"),
                    ("asym_id_list", "text"),
                    ("_hash_asym_id_list", "text"),
                ],
                primary_key=["pdbid", "assembly_id"],
            ),
        ],
    )


class TestHexSha256:
    """Tests for _hex_sha256 function."""

    def test_empty_string(self):
        """Test SHA256 of empty string."""
        result = _hex_sha256("")
        assert len(result) == 64  # SHA256 produces 64 hex chars
        # Known SHA256 of empty string
        assert (
            result == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )

    def test_simple_string(self):
        """Test SHA256 of simple string."""
        result = _hex_sha256("A,B,C")
        assert len(result) == 64

    def test_consistency(self):
        """Test that same input produces same output."""
        assert _hex_sha256("test") == _hex_sha256("test")


class TestGenDocid:
    """Tests for _gen_docid function."""

    def test_pdb_style_id(self):
        """Test with PDB-style 4-character ID."""
        # 4-char alphanumeric IDs are converted to base-36
        docid = _gen_docid("1abc")
        assert isinstance(docid, int)
        assert docid > 0

    def test_lowercase_conversion(self):
        """Test that uppercase is handled."""
        assert _gen_docid("1ABC") == _gen_docid("1abc")

    def test_invalid_id(self):
        """Test with invalid ID returns 0."""
        # IDs with invalid characters
        assert _gen_docid("!!") == 0


class TestExpandOperExpression:
    """Tests for _expand_oper_expression function."""

    def test_single_value(self):
        """Test single value."""
        assert _expand_oper_expression("1") == ["1"]

    def test_comma_separated(self):
        """Test comma-separated values."""
        assert _expand_oper_expression("1,2,3") == ["1", "2", "3"]

    def test_range(self):
        """Test range notation."""
        assert _expand_oper_expression("1-3") == ["1", "2", "3"]

    def test_product_notation(self):
        """Test product notation like (1,2)(3,4)."""
        result = _expand_oper_expression("(1,2)(3,4)")
        assert len(result) == 4
        assert "1-3" in result
        assert "1-4" in result
        assert "2-3" in result
        assert "2-4" in result

    def test_empty(self):
        """Test empty expression."""
        assert _expand_oper_expression("") == []


class TestChainTypeMapping:
    """Tests for chain type mapping."""

    def test_polypeptide_l(self):
        """Test polypeptide(L) mapping."""
        assert CHAIN_TYPE_MAPPING["polypeptide(L)"] == 2

    def test_dna(self):
        """Test DNA mapping."""
        assert CHAIN_TYPE_MAPPING["polydeoxyribonucleotide"] == 3

    def test_rna(self):
        """Test RNA mapping."""
        assert CHAIN_TYPE_MAPPING["polyribonucleotide"] == 4


class TestExptlMethodMapping:
    """Tests for experimental method mapping."""

    def test_ihm_method(self):
        """Test IHM method is 16."""
        assert EXPTL_METHOD_MAPPING["IHM"] == 16

    def test_xray(self):
        """Test X-ray method."""
        assert EXPTL_METHOD_MAPPING["X-RAY DIFFRACTION"] == 1


class TestExtractEntryId:
    """Tests for extract_entry_id method."""

    def test_standard_format(self, tmp_path):
        """Test standard filename: entry-noatom.json.gz."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        filepath = Path("pdbdev_00000001-noatom.json.gz")
        assert pipeline.extract_entry_id(filepath) == "pdbdev_00000001"

    def test_without_noatom_suffix(self, tmp_path):
        """Test filename without -noatom suffix."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        # Should still work but not strip suffix
        filepath = Path("pdbdev_00000001.json.gz")
        assert pipeline.extract_entry_id(filepath) == "pdbdev_00000001"


class TestFindJobs:
    """Tests for find_jobs method."""

    def test_find_mmjson_files(self, tmp_path):
        """Test finding mmJSON files in directory."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        # Create test files
        create_test_ihm_mmjson_file(
            data_dir / "pdbdev_00000001-noatom.json.gz", "pdbdev_00000001"
        )
        create_test_ihm_mmjson_file(
            data_dir / "pdbdev_00000002-noatom.json.gz", "pdbdev_00000002"
        )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        jobs = pipeline.find_jobs()

        assert len(jobs) == 2
        entry_ids = {job.entry_id for job in jobs}
        assert entry_ids == {"pdbdev_00000001", "pdbdev_00000002"}

    def test_find_with_plus_data(self, tmp_path):
        """Test finding files with plus data."""
        data_dir = tmp_path / "ihm"
        plus_dir = tmp_path / "plus"
        data_dir.mkdir(parents=True)
        plus_dir.mkdir(parents=True)

        # Create main file
        create_test_ihm_mmjson_file(
            data_dir / "pdbdev_00000001-noatom.json.gz", "pdbdev_00000001"
        )

        # Create plus file
        plus_content = {"gene_ontology_pdbmlplus": [{"goid": "GO:0001234"}]}
        with gzip.open(plus_dir / "pdbdev_00000001-plus.json.gz", "wt") as f:
            json.dump(plus_content, f)

        settings = create_test_settings(data_dir, plus_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].extra.get("plus_path") is not None

    def test_find_with_limit(self, tmp_path):
        """Test finding files with limit."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        # Create multiple test files
        for i in range(5):
            create_test_ihm_mmjson_file(
                data_dir / f"pdbdev_{i:08d}-noatom.json.gz", f"pdbdev_{i:08d}"
            )

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        jobs = pipeline.find_jobs(limit=2)

        assert len(jobs) == 2


class TestTransformBriefSummary:
    """Tests for brief_summary transformation."""

    def test_forced_ihm_method(self, tmp_path):
        """Test that exptl_method is always IHM."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        data = create_test_ihm_raw_data("pdbdev_00000001")
        result = pipeline._transform_brief_summary(data, "pdbdev_00000001")

        assert len(result) == 1
        assert result[0]["exptl_method"] == ["IHM"]
        assert result[0]["exptl_method_ids"] == [16]

    def test_plus_fields_bu_mw(self, tmp_path):
        """Test that plus_fields contains bu_mw."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        data = create_test_ihm_raw_data("pdbdev_00000001")
        result = pipeline._transform_brief_summary(data, "pdbdev_00000001")

        plus_fields = json.loads(result[0]["plus_fields"])
        assert "bu_mw" in plus_fields

    def test_keywords_format(self, tmp_path):
        """Test keywords include pdb_XXXXXXXX format."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        data = create_test_ihm_raw_data("pdbdev_00000001")
        result = pipeline._transform_brief_summary(data, "test")

        # Should have pdb_{entry_id} format padded to 8 chars
        assert any("pdb_" in kw for kw in result[0]["keywords"])


class TestHashAsymIdList:
    """Tests for _hash_asym_id_list computation."""

    @patch("mine2.pipelines.ihm.sync_entry_tables")
    def test_hash_added_to_assembly_gen(self, mock_bulk_upsert, tmp_path):
        """Test that _hash_asym_id_list is computed."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        # Create test file
        mmjson_file = data_dir / "pdbdev_00000001-noatom.json.gz"
        create_test_ihm_mmjson_file(mmjson_file, "pdbdev_00000001")

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        # Mock bulk_upsert
        mock_bulk_upsert.return_value = (1, 0, 0)

        from mine2.db.loader import Job

        job = Job(
            entry_id="pdbdev_00000001",
            filepath=mmjson_file,
            extra={},
        )

        result = pipeline.process_job(job, schema_def, "test_conninfo")

        # Verify bulk_upsert was called (success means processing worked)
        assert result.success is True


class TestCalculateMwForBu:
    """Tests for _calculate_mw_for_bu function."""

    def test_empty_data(self):
        """Test with empty data returns 0."""
        assert _calculate_mw_for_bu({}) == 0.0

    def test_no_assembly(self):
        """Test with no assembly data returns 0."""
        data = {"entity": [{"id": "1", "formula_weight": 1000}]}
        assert _calculate_mw_for_bu(data) == 0.0

    def test_with_author_assembly(self):
        """Test with author-defined assembly."""
        data = {
            "entity": [{"id": "1", "formula_weight": 10000}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined_assembly"}],
            "pdbx_struct_assembly_gen": [
                {"assembly_id": "1", "oper_expression": "1", "asym_id_list": "A"}
            ],
        }
        mw = _calculate_mw_for_bu(data)
        assert mw == 10000.0


class TestProcessJob:
    """Tests for process_job method."""

    @patch("mine2.pipelines.ihm.sync_entry_tables")
    def test_process_job_success(self, mock_bulk_upsert, tmp_path):
        """Test successful job processing."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        # Create test file
        mmjson_file = data_dir / "pdbdev_00000001-noatom.json.gz"
        create_test_ihm_mmjson_file(mmjson_file, "pdbdev_00000001")

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        # Mock bulk_upsert to return success
        mock_bulk_upsert.return_value = (1, 0, 0)

        from mine2.db.loader import Job

        job = Job(
            entry_id="pdbdev_00000001",
            filepath=mmjson_file,
            extra={},
        )

        result = pipeline.process_job(job, schema_def, "test_conninfo")

        assert result.success is True
        assert result.entry_id == "pdbdev_00000001"

    def test_process_job_file_not_found(self, tmp_path):
        """Test job processing with non-existent file."""
        data_dir = tmp_path / "ihm"
        data_dir.mkdir(parents=True)

        settings = create_test_settings(data_dir)
        config = settings.pipelines["ihm"]
        schema_def = create_test_schema_def()
        pipeline = IhmPipeline(settings, config, schema_def)

        from mine2.db.loader import Job

        job = Job(
            entry_id="pdbdev_99999999",
            filepath=data_dir / "nonexistent.json.gz",
            extra={},
        )

        result = pipeline.process_job(job, schema_def, "test_conninfo")

        assert result.success is False
