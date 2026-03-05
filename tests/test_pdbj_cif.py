"""Tests for pdbj pipeline (CIF format)."""

import gzip
import json
from pathlib import Path
from unittest.mock import patch

import gemmi
from sqlalchemy import (
    BigInteger,
    Column,
    Double,
    Float,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from pdbminebuilder.config import PipelineConfig, RdbConfig, Settings
from pdbminebuilder.db.loader import Job
from pdbminebuilder.parsers.cif import parse_cif_file
from pdbminebuilder.pipelines.pdbj import PdbjCifPipeline
from pdbminebuilder.utils.assembly import hex_sha256

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "pdbj"


def create_test_pdbj_cif_content(entries: list[dict]) -> str:
    """Create PDB CIF content string with the given entries.

    Args:
        entries: List of dicts with 'id' key and optional other fields

    Returns:
        CIF format string
    """
    blocks = []
    for entry in entries:
        pdb_id = entry["id"]  # e.g., 100d
        pdb_id_upper = pdb_id.upper()
        blocks.append(f"""data_{pdb_id_upper}
_entry.id {pdb_id_upper}
_cell.entry_id {pdb_id_upper}
_cell.length_a 1.0
_cell.length_b 1.0
_cell.length_c 1.0
""")
    return "\n".join(blocks)


def create_test_pdbj_cif_with_assembly(
    path: Path,
    entry_id: str,
    assembly_data: dict | None = None,
) -> None:
    """Create a test CIF file with assembly data for Phase 5 feature testing.

    Args:
        path: Path to write the file
        entry_id: PDB entry ID (e.g., "100d")
        assembly_data: Dict with optional keys:
            - asym_id_list: str (e.g., "A,B,C")
            - assembly_id: str (e.g., "1")
            - oper_expression: str (e.g., "1")
            - formula_weight: str (e.g., "1000.0")
            - assembly_details: str (e.g., "author_defined_assembly")
            - include_brief_summary: bool
    """
    if assembly_data is None:
        assembly_data = {}

    pdb_id_upper = entry_id.upper()
    asym_id_list = assembly_data.get("asym_id_list", "A")
    assembly_id = assembly_data.get("assembly_id", "1")
    oper_expression = assembly_data.get("oper_expression", "1")
    formula_weight = assembly_data.get("formula_weight", "1000.0")
    assembly_details = assembly_data.get("assembly_details", "author_defined_assembly")
    include_brief_summary = assembly_data.get("include_brief_summary", False)

    content = f"""data_{pdb_id_upper}
_entry.id {pdb_id_upper}

_entity.id 1
_entity.formula_weight {formula_weight}

_struct_asym.id A
_struct_asym.entity_id 1

_pdbx_struct_assembly.id {assembly_id}
_pdbx_struct_assembly.details '{assembly_details}'

_pdbx_struct_assembly_gen.assembly_id {assembly_id}
_pdbx_struct_assembly_gen.asym_id_list '{asym_id_list}'
_pdbx_struct_assembly_gen.oper_expression {oper_expression}
"""

    if include_brief_summary:
        content += f"""
_brief_summary.pdbid {entry_id}
_brief_summary.docid 100
"""

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


def create_test_pdbj_cif_file(path: Path, entries: list[dict]) -> None:
    """Create a test PDB CIF file.

    Handles .gz extension by writing gzip-compressed content.
    """
    content = create_test_pdbj_cif_content(entries)
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
            "pdbj": PipelineConfig(
                data=str(data_dir),
            )
        },
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
        "cell",
        meta,
        Column("pdbid", Text),
        Column("entry_id", Text),
        Column("length_a", Float),
        Column("length_b", Float),
        Column("length_c", Float),
        PrimaryKeyConstraint("pdbid"),
    )
    return meta


def create_test_meta_with_assembly() -> MetaData:
    """Create test MetaData with assembly tables for Phase 5 testing."""
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


class TestExtractEntryId:
    """Tests for PdbjCifPipeline.extract_entry_id()."""

    def test_cif_gz_extension(self, tmp_path: Path) -> None:
        """Extract entry ID from .cif.gz filename."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        entry_id = pipeline.extract_entry_id(Path("/path/to/100d.cif.gz"))

        assert entry_id == "100d"

    def test_plain_cif_extension(self, tmp_path: Path) -> None:
        """Extract entry ID from .cif filename."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        # Base class handles .cif extension as well
        entry_id = pipeline.extract_entry_id(Path("/path/to/100d.cif"))

        assert entry_id == "100d"


class TestFindJobs:
    """Tests for PdbjCifPipeline.find_jobs()."""

    def test_find_cif_files(self, tmp_path: Path) -> None:
        """Find CIF files in data directory."""
        # Create divided directory structure
        subdir = tmp_path.joinpath("00")
        subdir.mkdir()
        cif_path = subdir.joinpath("100d.cif.gz")
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].entry_id == "100d"
        assert jobs[0].filepath == cif_path

    def test_find_multiple_files(self, tmp_path: Path) -> None:
        """Find multiple CIF files across subdirectories."""
        # Create divided directory structure
        for subdir_name, pdb_id in [("00", "100d"), ("01", "101d"), ("0a", "1a0a")]:
            subdir = tmp_path.joinpath(subdir_name)
            subdir.mkdir()
            cif_path = subdir.joinpath(f"{pdb_id}.cif.gz")
            create_test_pdbj_cif_file(cif_path, [{"id": pdb_id}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 3
        entry_ids = {j.entry_id for j in jobs}
        assert entry_ids == {"100d", "101d", "1a0a"}

    def test_respects_limit(self, tmp_path: Path) -> None:
        """Find jobs respects limit parameter."""
        # Create multiple files
        for i in range(10):
            subdir = tmp_path.joinpath(f"{i:02d}")
            subdir.mkdir()
            cif_path = subdir.joinpath(f"{i:03d}d.cif.gz")
            create_test_pdbj_cif_file(cif_path, [{"id": f"{i:03d}d"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs(limit=3)

        assert len(jobs) == 3

    def test_empty_directory(self, tmp_path: Path) -> None:
        """Find jobs returns empty list for empty directory."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert jobs == []

    def test_nonexistent_directory(self, tmp_path: Path) -> None:
        """Find jobs returns empty list for nonexistent directory."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert jobs == []


class TestProcessJob:
    """Tests for PdbjCifPipeline.process_job()."""

    def test_process_single_entry(self, tmp_path: Path) -> None:
        """Process a single PDB entry from CIF (entry_id only, no DB)."""
        cif_path = tmp_path.joinpath("100d.cif.gz")
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)

        job = Job(entry_id="100d", filepath=cif_path, extra={})
        result = pipeline.process_job(job, "pdbj", "mock://test")

        # Only check entry_id (success requires real DB connection)
        assert result.entry_id == "100d"


class TestPdbjCifPipelineRun:
    """Tests for PdbjCifPipeline.run() method."""

    def test_run_returns_empty_when_no_files(self, tmp_path: Path) -> None:
        """Run returns empty list when no CIF files found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta, force=True)
        results = pipeline.run()

        assert results == []

    def test_run_processes_files(self, tmp_path: Path) -> None:
        """Run processes found CIF files."""
        # Create files in divided structure
        subdir = tmp_path.joinpath("00")
        subdir.mkdir()
        for pdb_id in ["100d", "200d"]:
            cif_path = subdir.joinpath(f"{pdb_id}.cif.gz")
            create_test_pdbj_cif_file(cif_path, [{"id": pdb_id}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta, force=True)
        results = pipeline.run()

        assert len(results) == 2
        entry_ids = {r.entry_id for r in results}
        assert entry_ids == {"100d", "200d"}

    def test_run_respects_limit(self, tmp_path: Path) -> None:
        """Run respects the limit parameter."""
        # Create many files
        subdir = tmp_path.joinpath("00")
        subdir.mkdir()
        for i in range(20):
            cif_path = subdir.joinpath(f"{i:03d}d.cif.gz")
            create_test_pdbj_cif_file(cif_path, [{"id": f"{i:03d}d"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta, force=True)
        results = pipeline.run(limit=5)

        assert len(results) == 5


class TestTransformEntry:
    """Tests for _transform_entry() function."""

    def test_with_entry_data(self) -> None:
        """Transform entry with data."""
        from pdbminebuilder.pipelines.pdbj import _transform_entry

        data = {"entry": [{"id": "100D"}]}
        result = _transform_entry(data, "100d")

        assert len(result) == 1
        assert result[0]["pdbid"] == "100d"
        assert result[0]["id"] == "100D"

    def test_without_entry_data(self) -> None:
        """Transform entry creates fallback when no data."""
        from pdbminebuilder.pipelines.pdbj import _transform_entry

        data = {}
        result = _transform_entry(data, "100d")

        assert len(result) == 1
        assert result[0]["pdbid"] == "100d"
        assert result[0]["id"] == "100D"


class TestRealPdbFixtures:
    """Tests using real PDB CIF fixture files."""

    def test_parse_1crn_fixture(self) -> None:
        """Parse 1crn (crambin) fixture file."""
        fixture_path = FIXTURES_DIR / "1crn.cif.gz"
        assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

        data = parse_cif_file(fixture_path)

        # 1crn is crambin - a small protein
        assert data["_block_name"] == "1CRN"

        # Should have entry data
        assert "entry" in data
        assert data["entry"][0]["id"] == "1CRN"

        # Should have cell parameters
        assert "cell" in data
        cell = data["cell"][0]
        assert "length_a" in cell
        assert "length_b" in cell
        assert "length_c" in cell

    def test_parse_1ubq_fixture(self) -> None:
        """Parse 1ubq (ubiquitin) fixture file."""
        fixture_path = FIXTURES_DIR / "1ubq.cif.gz"
        assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

        data = parse_cif_file(fixture_path)

        # 1ubq is ubiquitin
        assert data["_block_name"] == "1UBQ"
        assert "entry" in data
        assert data["entry"][0]["id"] == "1UBQ"

    def test_fixture_has_expected_categories(self) -> None:
        """Fixture contains expected mmCIF categories."""
        fixture_path = FIXTURES_DIR / "1crn.cif.gz"
        data = parse_cif_file(fixture_path)

        # Common mmCIF categories
        expected_categories = [
            "entry",
            "cell",
            "symmetry",
            "entity",
            "struct",
        ]
        for cat in expected_categories:
            assert cat in data, f"Missing category: {cat}"


def create_test_settings_with_plus(
    data_dir: Path,
    plus_dir: Path,
    nextgen_plus_dir: Path | None = None,
) -> Settings:
    """Create test settings with plus data directory."""
    config = PipelineConfig(
        data=str(data_dir),
        data_plus=str(plus_dir),
    )
    if nextgen_plus_dir:
        config.data_nextgen_plus = str(nextgen_plus_dir)
    return Settings(
        rdb=RdbConfig(nworkers=2, constring="test"),
        pipelines={"pdbj": config},
    )


def create_test_plus_file(path: Path, entry_id: str, extra_categories: dict) -> None:
    """Create a test plus data file (mmJSON format).

    mmJSON is column-oriented:
    {"data_XXX": {"category": {"col1": [val1, val2], "col2": [val1, val2]}}}

    Args:
        path: Path to write the file (should end with -plus.json.gz)
        entry_id: PDB entry ID (e.g., "100d")
        extra_categories: Dict of category name to list of row dicts
    """
    import json

    # Build mmJSON structure (column-oriented)
    block_data = {}
    for cat, rows in extra_categories.items():
        if not rows:
            continue
        # Convert row-oriented to column-oriented
        columns = list(rows[0].keys())
        col_data = {col: [row.get(col) for row in rows] for col in columns}
        block_data[cat] = col_data

    data = {"data_" + entry_id.upper(): block_data}

    content = json.dumps(data)
    with gzip.open(path, "wt") as f:
        f.write(content)


def create_test_meta_with_plus() -> MetaData:
    """Create test MetaData with plus data tables."""
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
        "cell",
        meta,
        Column("pdbid", Text),
        Column("entry_id", Text),
        Column("length_a", Float),
        Column("length_b", Float),
        Column("length_c", Float),
        PrimaryKeyConstraint("pdbid"),
    )
    Table(
        "gene_ontology_pdbmlplus",
        meta,
        Column("pdbid", Text),
        Column("goid", Text),
        Column("name", Text),
        PrimaryKeyConstraint("pdbid", "goid"),
    )
    return meta


class TestFindJobsWithPlusData:
    """Tests for PdbjCifPipeline.find_jobs() with plus data."""

    def test_finds_plus_files_when_configured(self, tmp_path: Path) -> None:
        """Find jobs includes plus_path when plus directory is configured."""
        # Create CIF data directory
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        # Create plus data directory
        plus_dir = tmp_path / "mmjson-plus"
        plus_dir.mkdir()
        plus_path = plus_dir / "100d-plus.json.gz"
        create_test_plus_file(
            plus_path,
            "100d",
            {"gene_ontology_pdbmlplus": [{"goid": "GO:0001234", "name": "test"}]},
        )

        settings = create_test_settings_with_plus(cif_dir, plus_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].entry_id == "100d"
        assert jobs[0].extra is not None
        assert jobs[0].extra.get("plus_path") == plus_path

    def test_plus_path_none_when_file_not_exists(self, tmp_path: Path) -> None:
        """Plus path is None when plus file doesn't exist."""
        # Create CIF data directory
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        # Create empty plus data directory (no matching file)
        plus_dir = tmp_path / "mmjson-plus"
        plus_dir.mkdir()

        settings = create_test_settings_with_plus(cif_dir, plus_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].extra is not None
        assert jobs[0].extra.get("plus_path") is None

    def test_plus_path_none_when_plus_dir_not_configured(self, tmp_path: Path) -> None:
        """Plus path is None when plus directory is not configured."""
        # Create CIF data directory
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        # No plus directory configured
        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].extra is not None
        assert jobs[0].extra.get("plus_path") is None

    def test_finds_partial_plus_files(self, tmp_path: Path) -> None:
        """Some entries have plus files, some don't."""
        # Create CIF data directory with multiple entries
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        for pdb_id in ["100d", "101d", "102d"]:
            cif_path = cif_dir / f"{pdb_id}.cif.gz"
            create_test_pdbj_cif_file(cif_path, [{"id": pdb_id}])

        # Create plus directory with only one matching file
        plus_dir = tmp_path / "mmjson-plus"
        plus_dir.mkdir()
        plus_path = plus_dir / "100d-plus.json.gz"
        create_test_plus_file(
            plus_path,
            "100d",
            {"gene_ontology_pdbmlplus": [{"goid": "GO:0001234", "name": "test"}]},
        )

        settings = create_test_settings_with_plus(cif_dir, plus_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 3
        plus_paths = {j.entry_id: j.extra.get("plus_path") for j in jobs}
        assert plus_paths["100d"] == plus_path
        assert plus_paths["101d"] is None
        assert plus_paths["102d"] is None


class TestProcessJobWithPlusData:
    """Tests for PdbjCifPipeline.process_job() with plus data merging."""

    def test_merges_plus_data_into_cif_data(self, tmp_path: Path) -> None:
        """Plus data categories are merged into CIF data."""
        from unittest.mock import patch

        # Create CIF file
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        # Create plus file with extra category
        plus_dir = tmp_path / "mmjson-plus"
        plus_dir.mkdir()
        plus_path = plus_dir / "100d-plus.json.gz"
        create_test_plus_file(
            plus_path,
            "100d",
            {"gene_ontology_pdbmlplus": [{"goid": "GO:0001234", "name": "test"}]},
        )

        settings = create_test_settings_with_plus(cif_dir, plus_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta_with_plus()

        pipeline = PdbjCifPipeline(settings, config, meta)
        job = Job(
            entry_id="100d",
            filepath=cif_path,
            extra={"plus_path": plus_path},
        )

        # Mock bulk_upsert to capture what gets loaded
        with patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables") as mock_sync_entry_tables:
            mock_sync_entry_tables.return_value = (1, 0, 0)
            result = pipeline.process_job(job, "pdbj", "test_conninfo")

            assert result.success
            # Verify gene_ontology_pdbmlplus was loaded (from plus data)
            table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
            assert "gene_ontology_pdbmlplus" in table_rows

    def test_works_without_plus_data(self, tmp_path: Path) -> None:
        """Process job works when plus_path is None."""
        from unittest.mock import patch

        # Create CIF file only (no plus data)
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        job = Job(
            entry_id="100d",
            filepath=cif_path,
            extra={"plus_path": None},
        )

        # Mock bulk_upsert
        with patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables") as mock_sync_entry_tables:
            mock_sync_entry_tables.return_value = (1, 0, 0)
            result = pipeline.process_job(job, "pdbj", "test_conninfo")

            assert result.success
            # Should still load entry and cell tables
            table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
            assert "entry" in table_rows


# =============================================================================
# Phase 5 Feature Tests for CIF Pipeline
# =============================================================================


class TestCifHashAsymIdList:
    """Tests for _hash_asym_id_list computation in CIF pipeline."""

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_hash_added_to_assembly_gen_cif(self, mock_sync_entry_tables, tmp_path):
        """Test that _hash_asym_id_list is computed for CIF data."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()

        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_with_assembly(
            cif_path,
            "100d",
            {
                "asym_id_list": "A,B,C",
                "assembly_id": "1",
                "oper_expression": "1",
            },
        )

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta_with_assembly()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=cif_path, extra={})
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success

        table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
        assert "pdbx_struct_assembly_gen" in table_rows
        rows = table_rows["pdbx_struct_assembly_gen"]
        for row in rows:
            expected_hash = hex_sha256(row["asym_id_list"])
            assert row["_hash_asym_id_list"] == expected_hash

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_hash_is_sha256_cif(self, mock_sync_entry_tables, tmp_path):
        """Test that the hash is SHA256 (64 hex chars) for CIF data."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()

        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_with_assembly(
            cif_path,
            "100d",
            {"asym_id_list": "A,B,C"},
        )

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta_with_assembly()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=cif_path, extra={})
        pipeline.process_job(job, "pdbj", "test_conninfo")

        table_rows = mock_sync_entry_tables.call_args.kwargs["table_rows"]
        rows = table_rows["pdbx_struct_assembly_gen"]
        for row in rows:
            hash_value = row["_hash_asym_id_list"]
            assert len(hash_value) == 64
            assert all(c in "0123456789abcdef" for c in hash_value)


class TestCifBuMwCalculation:
    """Tests for bu_mw calculation in CIF pipeline."""

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_bu_mw_in_plus_fields_cif(self, mock_sync_entry_tables, tmp_path):
        """Test that bu_mw is calculated and added to plus_fields for CIF."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()

        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_with_assembly(
            cif_path,
            "100d",
            {
                "asym_id_list": "A",
                "assembly_id": "1",
                "oper_expression": "1",
                "formula_weight": "1000.0",
                "assembly_details": "author_defined_assembly",
                "include_brief_summary": True,
            },
        )

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta_with_assembly()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id="100d", filepath=cif_path, extra={})
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

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_bu_mw_zero_when_no_assembly_cif(self, mock_sync_entry_tables, tmp_path):
        """Test that bu_mw is 0 when no assembly data in CIF."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()

        # Create a simple CIF with brief_summary but no assembly
        pdb_id = "100d"
        content = f"""data_{pdb_id.upper()}
_entry.id {pdb_id.upper()}
_brief_summary.pdbid {pdb_id}
_brief_summary.docid 100
"""
        doc = gemmi.cif.read_string(content)
        cif_path = cif_dir / f"{pdb_id}.cif.gz"

        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".cif", delete=False) as tmp:
            doc.write_file(tmp.name)
            with open(tmp.name, "rb") as f_in:
                with gzip.open(cif_path, "wb") as f_out:
                    f_out.write(f_in.read())
            Path(tmp.name).unlink()

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta_with_assembly()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync_entry_tables.return_value = (1, 0, 0)

        job = Job(entry_id=pdb_id, filepath=cif_path, extra={})
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


class TestCifPatchApplication:
    """Tests for apply_patches() in CIF pipeline."""

    def test_patches_applied_to_cif_data(self):
        """Test that entry-specific patches are applied to CIF data."""
        from pdbminebuilder.utils.patches import apply_patches

        # Test that patches work with CIF-like data structure
        data = {"entry": [{"id": "7ED1"}]}
        result = apply_patches("7ed1", data)

        # 7ed1 patch adds MET to chem_comp
        assert "chem_comp" in result
        met_ids = [row["id"] for row in result["chem_comp"] if row.get("id") == "MET"]
        assert "MET" in met_ids

    def test_patches_not_applied_to_non_matching_entry(self):
        """Test that patches are not applied to non-matching entries."""
        from pdbminebuilder.utils.patches import apply_patches

        data = {"entry": [{"id": "100D"}]}
        result = apply_patches("100d", data)

        # No patches for 100d, chem_comp should not be added
        assert "chem_comp" not in result


# =============================================================================
# Nextgen-plus (SIFTS) data tests
# =============================================================================


class TestFindJobsWithNextgenPlusData:
    """Tests for PdbjCifPipeline.find_jobs() with nextgen-plus data."""

    def test_finds_nextgen_plus_files_when_configured(self, tmp_path: Path) -> None:
        """find_jobs includes nextgen_plus_path when directory is configured."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        nextgen_dir = tmp_path / "nextgen-plus"
        nextgen_dir.mkdir()
        nextgen_path = nextgen_dir / "100d-plus.json.gz"
        create_test_plus_file(
            nextgen_path,
            "100d",
            {
                "pdbx_sifts_xref_db": [
                    {
                        "entity_id": "1",
                        "seq_id_ordinal": "1",
                        "db_name": "UNP",
                        "db_accession": "P12345",
                    }
                ]
            },
        )

        settings = create_test_settings_with_plus(
            cif_dir, tmp_path / "empty-plus", nextgen_dir
        )
        # Create the empty plus dir so it doesn't interfere
        (tmp_path / "empty-plus").mkdir()
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].extra is not None
        assert jobs[0].extra.get("nextgen_plus_path") == nextgen_path

    def test_nextgen_plus_path_none_when_file_not_exists(self, tmp_path: Path) -> None:
        """nextgen_plus_path is None when file doesn't exist for entry."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        nextgen_dir = tmp_path / "nextgen-plus"
        nextgen_dir.mkdir()
        # No matching file created

        settings = create_test_settings_with_plus(
            cif_dir, tmp_path / "empty-plus", nextgen_dir
        )
        (tmp_path / "empty-plus").mkdir()
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].extra.get("nextgen_plus_path") is None

    def test_nextgen_plus_path_none_when_not_configured(self, tmp_path: Path) -> None:
        """nextgen_plus_path is None when directory is not configured."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        jobs = pipeline.find_jobs()

        assert len(jobs) == 1
        assert jobs[0].extra.get("nextgen_plus_path") is None


class TestProcessJobWithNextgenPlusData:
    """Tests for PdbjCifPipeline.process_job() with nextgen-plus data merging."""

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_merges_nextgen_plus_data(self, mock_sync, tmp_path: Path) -> None:
        """Nextgen-plus SIFTS categories are merged into CIF data."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        nextgen_dir = tmp_path / "nextgen-plus"
        nextgen_dir.mkdir()
        nextgen_path = nextgen_dir / "100d-plus.json.gz"
        create_test_plus_file(
            nextgen_path,
            "100d",
            {
                "pdbx_sifts_xref_db": [
                    {
                        "entity_id": "1",
                        "asym_id": "A",
                        "seq_id_ordinal": "1",
                        "seq_id": "1",
                        "xref_db_name": "UNP",
                        "xref_db_acc": "P12345",
                    }
                ]
            },
        )

        settings = create_test_settings_with_plus(
            cif_dir, tmp_path / "empty-plus", nextgen_dir
        )
        (tmp_path / "empty-plus").mkdir()
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync.return_value = (1, 0, 0)

        job = Job(
            entry_id="100d",
            filepath=cif_path,
            extra={"plus_path": None, "nextgen_plus_path": nextgen_path},
        )
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success
        table_rows = mock_sync.call_args.kwargs["table_rows"]
        assert "pdbx_sifts_xref_db" in table_rows
        assert table_rows["pdbx_sifts_xref_db"][0]["xref_db_acc"] == "P12345"

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_merges_both_plus_and_nextgen_plus(self, mock_sync, tmp_path: Path) -> None:
        """Both old plus and nextgen-plus data are merged."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        plus_dir = tmp_path / "mmjson-plus"
        plus_dir.mkdir()
        plus_path = plus_dir / "100d-plus.json.gz"
        create_test_plus_file(
            plus_path,
            "100d",
            {"gene_ontology_pdbmlplus": [{"goid": "GO:0001234", "name": "test"}]},
        )

        nextgen_dir = tmp_path / "nextgen-plus"
        nextgen_dir.mkdir()
        nextgen_path = nextgen_dir / "100d-plus.json.gz"
        create_test_plus_file(
            nextgen_path,
            "100d",
            {
                "pdbx_sifts_xref_db": [
                    {
                        "entity_id": "1",
                        "asym_id": "A",
                        "seq_id_ordinal": "1",
                        "seq_id": "1",
                        "xref_db_name": "UNP",
                        "xref_db_acc": "P12345",
                    }
                ]
            },
        )

        settings = create_test_settings_with_plus(cif_dir, plus_dir, nextgen_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync.return_value = (1, 0, 0)

        job = Job(
            entry_id="100d",
            filepath=cif_path,
            extra={"plus_path": plus_path, "nextgen_plus_path": nextgen_path},
        )
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success
        table_rows = mock_sync.call_args.kwargs["table_rows"]
        # Old plus data
        assert "gene_ontology_pdbmlplus" in table_rows
        # Nextgen-plus SIFTS data
        assert "pdbx_sifts_xref_db" in table_rows

    @patch("pdbminebuilder.pipelines.pdbj.sync_entry_tables")
    def test_works_without_nextgen_plus(self, mock_sync, tmp_path: Path) -> None:
        """Process job works when nextgen_plus_path is None."""
        cif_dir = tmp_path / "mmCIF"
        cif_dir.mkdir()
        cif_path = cif_dir / "100d.cif.gz"
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        settings = create_test_settings(cif_dir)
        config = settings.pipelines["pdbj"]
        meta = create_test_meta()

        pipeline = PdbjCifPipeline(settings, config, meta)
        mock_sync.return_value = (1, 0, 0)

        job = Job(
            entry_id="100d",
            filepath=cif_path,
            extra={"plus_path": None, "nextgen_plus_path": None},
        )
        result = pipeline.process_job(job, "pdbj", "test_conninfo")

        assert result.success
        table_rows = mock_sync.call_args.kwargs["table_rows"]
        assert "entry" in table_rows
