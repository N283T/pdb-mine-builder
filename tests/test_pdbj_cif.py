"""Tests for pdbj-cif pipeline."""

import gzip
from pathlib import Path

import gemmi
import pytest

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import LoaderResult, SchemaDef, TableDef
from mine2.pipelines.pdbj import PdbjCifPipeline


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
            "pdbj-cif": PipelineConfig(
                deffile="schemas/pdbj.def.yml",
                data=str(data_dir),
            )
        },
    )


def create_test_schema_def() -> SchemaDef:
    """Create minimal test schema definition for pdbj."""
    return SchemaDef(
        schema_name="pdbj",
        primary_key="pdbid",
        tables=[
            TableDef(
                name="entry",
                columns=[("pdbid", "TEXT"), ("id", "TEXT")],
                primary_key=["pdbid", "id"],
            ),
            TableDef(
                name="cell",
                columns=[
                    ("pdbid", "TEXT"),
                    ("entry_id", "TEXT"),
                    ("length_a", "REAL"),
                    ("length_b", "REAL"),
                    ("length_c", "REAL"),
                ],
                primary_key=["pdbid"],
            ),
        ],
    )


class TestExtractEntryId:
    """Tests for PdbjCifPipeline.extract_entry_id()."""

    def test_cif_gz_extension(self, tmp_path: Path) -> None:
        """Extract entry ID from .cif.gz filename."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
        entry_id = pipeline.extract_entry_id(Path("/path/to/100d.cif.gz"))

        assert entry_id == "100d"

    def test_plain_cif_extension(self, tmp_path: Path) -> None:
        """Extract entry ID from .cif filename."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
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
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
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
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
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
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
        jobs = pipeline.find_jobs(limit=3)

        assert len(jobs) == 3

    def test_empty_directory(self, tmp_path: Path) -> None:
        """Find jobs returns empty list for empty directory."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
        jobs = pipeline.find_jobs()

        assert jobs == []

    def test_nonexistent_directory(self, tmp_path: Path) -> None:
        """Find jobs returns empty list for nonexistent directory."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
        jobs = pipeline.find_jobs()

        assert jobs == []


class TestProcessJob:
    """Tests for PdbjCifPipeline.process_job()."""

    def test_process_single_entry(self, tmp_path: Path) -> None:
        """Process a single PDB entry from CIF (entry_id only, no DB)."""
        cif_path = tmp_path.joinpath("100d.cif.gz")
        create_test_pdbj_cif_file(cif_path, [{"id": "100d"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)

        from mine2.db.loader import Job

        job = Job(entry_id="100d", filepath=cif_path, extra={})
        result = pipeline.process_job(job, schema_def, "mock://test")

        # Only check entry_id (success requires real DB connection)
        assert result.entry_id == "100d"


class TestPdbjCifPipelineRun:
    """Tests for PdbjCifPipeline.run() method."""

    def test_run_returns_empty_when_no_files(self, tmp_path: Path) -> None:
        """Run returns empty list when no CIF files found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
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
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
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
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)
        results = pipeline.run(limit=5)

        assert len(results) == 5


class TestTransformEntry:
    """Tests for PdbjCifPipeline._transform_entry()."""

    def test_with_entry_data(self, tmp_path: Path) -> None:
        """Transform entry with data."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)

        data = {"entry": [{"id": "100D"}]}
        result = pipeline._transform_entry(data, "100d")

        assert len(result) == 1
        assert result[0]["pdbid"] == "100d"
        assert result[0]["id"] == "100D"

    def test_without_entry_data(self, tmp_path: Path) -> None:
        """Transform entry creates fallback when no data."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["pdbj-cif"]
        schema_def = create_test_schema_def()

        pipeline = PdbjCifPipeline(settings, config, schema_def)

        data = {}
        result = pipeline._transform_entry(data, "100d")

        assert len(result) == 1
        assert result[0]["pdbid"] == "100d"
        assert result[0]["id"] == "100D"
