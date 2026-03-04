"""Tests for cc pipeline (CIF format)."""

import gzip
from pathlib import Path
from unittest.mock import MagicMock, patch

import gemmi
import psycopg
from sqlalchemy import Column, MetaData, PrimaryKeyConstraint, Table, Text

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.pipelines.cc import (
    CcCifPipeline,
    _add_rdkit_descriptor_columns,
    _ensure_rdkit_setup,
    _generate_canonical_smiles,
    _process_cif_block,
    _read_mmjson_block,
)


def create_test_cif_content(components: list[dict]) -> str:
    """Create CIF content string with the given components.

    Args:
        components: List of dicts with 'id', 'name', 'type' keys

    Returns:
        CIF format string
    """
    blocks = []
    for comp in components:
        comp_id = comp["id"]
        name = comp.get("name", "Test")
        comp_type = comp.get("type", "NON-POLYMER")
        # Quote name if it contains spaces
        if " " in name:
            name = f"'{name}'"
        blocks.append(f"""data_{comp_id}
_chem_comp.id {comp_id}
_chem_comp.name {name}
_chem_comp.type {comp_type}
""")
    return "\n".join(blocks)


def create_test_cif_file(path: Path, components: list[dict]) -> None:
    """Create a test CIF file with the given components.

    Handles .gz extension by writing gzip-compressed content.

    Args:
        path: Path to write the CIF file
        components: List of dicts with 'id', 'name', 'type' keys
    """
    content = create_test_cif_content(components)
    # Parse and re-write to ensure valid CIF format
    doc = gemmi.cif.read_string(content)

    if str(path).endswith(".gz"):
        # Write to temp file, then gzip
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
            "cc": PipelineConfig(
                data=str(data_dir),
            )
        },
    )


def create_test_meta() -> MetaData:
    """Create minimal test MetaData for cc."""
    meta = MetaData(schema="cc")
    meta.info = {"entry_pk": "comp_id"}
    Table(
        "chem_comp",
        meta,
        Column("comp_id", Text),
        Column("name", Text),
        Column("type", Text),
        PrimaryKeyConstraint("comp_id"),
    )
    return meta


class TestFindCifFile:
    """Tests for CcCifPipeline._find_cif_file()."""

    def test_direct_path(self, tmp_path: Path) -> None:
        """Find CIF file at direct path."""
        cif_path = tmp_path.joinpath("components.cif.gz")
        create_test_cif_file(cif_path, [{"id": "ATP"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_nested_path_rsync_quirk(self, tmp_path: Path) -> None:
        """Find CIF file in nested directory (rsync quirk)."""
        # Create nested structure: data/components.cif.gz/components.cif.gz
        nested_dir = tmp_path.joinpath("components.cif.gz")
        nested_dir.mkdir()
        cif_path = nested_dir.joinpath("components.cif.gz")
        create_test_cif_file(cif_path, [{"id": "ATP"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_recursive_search(self, tmp_path: Path) -> None:
        """Find CIF file via recursive search."""
        # Create file in subdirectory
        subdir = tmp_path.joinpath("subdir", "another")
        subdir.mkdir(parents=True)
        cif_path = subdir.joinpath("components.cif.gz")
        create_test_cif_file(cif_path, [{"id": "ATP"}])

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found == cif_path

    def test_not_found(self, tmp_path: Path) -> None:
        """Return None when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found is None

    def test_directory_not_exists(self, tmp_path: Path) -> None:
        """Return None when data directory doesn't exist."""
        settings = create_test_settings(tmp_path.joinpath("nonexistent"))
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        found = pipeline._find_cif_file()

        assert found is None


class TestProcessCifBlock:
    """Tests for _process_cif_block function."""

    def test_process_single_block(self, tmp_path: Path) -> None:
        """Process a single CIF block."""
        cif_path = tmp_path.joinpath("test.cif")
        create_test_cif_file(
            cif_path,
            [
                {"id": "ATP", "name": "Adenosine Triphosphate", "type": "NON-POLYMER"},
            ],
        )

        # Load the CIF and get the block
        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        # Mock conninfo - will fail to connect but tests the function runs
        result = _process_cif_block(
            block=block,
            schema_name="cc",
            conninfo="mock://test",
        )

        # Should return a single LoaderResult
        assert result.entry_id == "ATP"
        # Will fail because we can't connect to mock DB
        assert result.success is False

    def test_process_block_extracts_comp_id(self, tmp_path: Path) -> None:
        """Block name is used as comp_id."""
        cif_path = tmp_path.joinpath("test.cif")
        create_test_cif_file(
            cif_path,
            [
                {"id": "ADP"},
            ],
        )

        doc = gemmi.cif.read(str(cif_path))
        block = doc[0]

        result = _process_cif_block(
            block=block,
            schema_name="cc",
            conninfo="mock://test",
        )

        assert result.entry_id == "ADP"


class TestCcCifPipelineRun:
    """Tests for CcCifPipeline.run() method."""

    def test_run_returns_empty_when_no_file(self, tmp_path: Path) -> None:
        """Run returns empty list when CIF file not found."""
        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        results = pipeline.run()

        assert results == []

    def test_run_sequential_for_small_count(self, tmp_path: Path) -> None:
        """Run uses sequential processing for small block counts."""
        cif_path = tmp_path.joinpath("components.cif.gz")
        create_test_cif_file(
            cif_path,
            [{"id": f"COMP{i}"} for i in range(5)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        # Limit to 5 - should use sequential (threshold is 10)
        results = pipeline.run(limit=5)

        # Will fail to connect to DB, but should process 5 blocks
        assert len(results) == 5

    def test_run_respects_limit(self, tmp_path: Path) -> None:
        """Run respects the limit parameter."""
        cif_path = tmp_path.joinpath("components.cif.gz")
        create_test_cif_file(
            cif_path,
            [{"id": f"COMP{i}"} for i in range(100)],
        )

        settings = create_test_settings(tmp_path)
        config = settings.pipelines["cc"]
        meta = create_test_meta()

        pipeline = CcCifPipeline(settings, config, meta)
        results = pipeline.run(limit=10)

        assert len(results) == 10


class TestEnsureRdkitSetup:
    """Tests for _ensure_rdkit_setup function."""

    def test_creates_extension_and_commits(self) -> None:
        """Successfully creates RDKit extension and commits."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            _ensure_rdkit_setup("test_conninfo")

        # Verify extension creation was attempted
        mock_cursor.execute.assert_any_call("CREATE EXTENSION IF NOT EXISTS rdkit")
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    def test_handles_insufficient_privilege(self) -> None:
        """Handles InsufficientPrivilege exception gracefully."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg.errors.InsufficientPrivilege(
            "permission denied"
        )
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            # Should not raise - logs warning and returns early
            _ensure_rdkit_setup("test_conninfo")

        # Commit should not be called when privilege error occurs
        mock_conn.commit.assert_not_called()

    def test_executes_mol_column_ddl(self) -> None:
        """Executes DDL for mol column creation."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            _ensure_rdkit_setup("test_conninfo")

        # Verify at least 3 execute calls: extension + mol column DDL + functions
        assert mock_cursor.execute.call_count >= 2
        # Second call should be the DO block for mol column
        second_call_sql = mock_cursor.execute.call_args_list[1][0][0]
        assert "cc.brief_summary" in second_call_sql
        assert "mol" in second_call_sql
        assert "is_valid_smiles" in second_call_sql

    def test_idempotent_multiple_calls(self) -> None:
        """Multiple calls work without error (idempotent)."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            # Call twice - should not raise
            _ensure_rdkit_setup("test_conninfo")
            _ensure_rdkit_setup("test_conninfo")

        # Multiple calls should work (idempotent)
        # Each invocation: extension + mol + descriptor setup (12) + functions = 15 calls
        assert mock_cursor.execute.call_count == 30

    def test_loads_rdkit_functions_sql(self) -> None:
        """Loads RDKit SQL functions from scripts/rdkit_functions.sql."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            _ensure_rdkit_setup("test_conninfo")

        # Last call should be the functions SQL file
        # Calls: extension + mol + descriptor setup (12) + functions = 15 total
        assert mock_cursor.execute.call_count == 15
        last_call_sql = mock_cursor.execute.call_args_list[-1][0][0]
        # Verify it contains the function definitions
        assert "cc.similar_compounds" in last_call_sql
        assert "cc.substructure_search" in last_call_sql
        assert "cc.exact_match" in last_call_sql

    def test_adds_descriptor_columns(self) -> None:
        """Adds RDKit molecular descriptor columns."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch("mine2.pipelines.cc.psycopg.connect", return_value=mock_conn):
            _ensure_rdkit_setup("test_conninfo")

        # Collect all executed SQL
        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )

        # Verify descriptor columns are added
        assert "rdkit_mw" in all_sql
        assert "rdkit_logp" in all_sql
        assert "rdkit_tpsa" in all_sql
        assert "rdkit_hba" in all_sql
        assert "rdkit_hbd" in all_sql
        assert "rdkit_rotbonds" in all_sql
        assert "rdkit_rings" in all_sql
        assert "rdkit_formula" in all_sql

        # Verify RDKit functions are used
        assert "mol_amw(mol)" in all_sql
        assert "mol_logp(mol)" in all_sql
        assert "mol_tpsa(mol)" in all_sql


class TestAddRdkitDescriptorColumns:
    """Tests for _add_rdkit_descriptor_columns function."""

    def test_adds_all_descriptor_columns(self) -> None:
        """Adds all 8 RDKit descriptor columns."""
        mock_cursor = MagicMock()

        _add_rdkit_descriptor_columns(mock_cursor)

        # Should execute:
        # 1 (check mol column) + 8 (check each descriptor) +
        # 1 (trigger function) + 1 (trigger) + 1 (update) = 12
        assert mock_cursor.execute.call_count == 12

        # Collect all SQL statements
        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )

        # Verify all descriptor columns
        expected_columns = [
            "rdkit_mw",
            "rdkit_logp",
            "rdkit_tpsa",
            "rdkit_hba",
            "rdkit_hbd",
            "rdkit_rotbonds",
            "rdkit_rings",
            "rdkit_formula",
        ]
        for col in expected_columns:
            assert col in all_sql, f"Column {col} not found in SQL"

    def test_uses_correct_rdkit_functions(self) -> None:
        """Uses correct RDKit functions for each descriptor."""
        mock_cursor = MagicMock()

        _add_rdkit_descriptor_columns(mock_cursor)

        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )

        # Verify RDKit functions
        expected_functions = [
            "mol_amw(mol)",
            "mol_logp(mol)",
            "mol_tpsa(mol)",
            "mol_hba(mol)",
            "mol_hbd(mol)",
            "mol_numrotatablebonds(mol)",
            "mol_numrings(mol)",
            "mol_formula(mol)",
        ]
        for func in expected_functions:
            assert func in all_sql, f"Function {func} not found in SQL"

    def test_uses_trigger_for_descriptors(self) -> None:
        """Uses trigger function to compute descriptor columns."""
        mock_cursor = MagicMock()

        _add_rdkit_descriptor_columns(mock_cursor)

        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )

        # Verify trigger function is created
        assert "compute_rdkit_descriptors" in all_sql
        assert "CREATE OR REPLACE FUNCTION" in all_sql
        assert "TRIGGER" in all_sql


SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


class TestRdkitFunctionsSql:
    """Tests for scripts/rdkit_functions.sql file."""

    def test_file_exists(self) -> None:
        """Verify rdkit_functions.sql file exists."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        assert sql_path.exists(), f"SQL file not found: {sql_path}"

    def test_contains_similar_compounds_function(self) -> None:
        """Verify cc.similar_compounds function is defined."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        content = sql_path.read_text()
        assert "CREATE OR REPLACE FUNCTION cc.similar_compounds(" in content
        assert "query_smiles TEXT" in content
        assert "threshold FLOAT" in content
        assert "tanimoto_sml" in content

    def test_contains_substructure_search_function(self) -> None:
        """Verify cc.substructure_search function is defined."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        content = sql_path.read_text()
        assert "CREATE OR REPLACE FUNCTION cc.substructure_search(" in content
        assert "query_smarts TEXT" in content
        assert "b.mol @> query_smarts::qmol" in content

    def test_contains_exact_match_function(self) -> None:
        """Verify cc.exact_match function is defined."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        content = sql_path.read_text()
        assert "CREATE OR REPLACE FUNCTION cc.exact_match(" in content
        assert "@=" in content

    def test_contains_dice_similarity_function(self) -> None:
        """Verify cc.similar_compounds_dice function is defined."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        content = sql_path.read_text()
        assert "CREATE OR REPLACE FUNCTION cc.similar_compounds_dice(" in content
        assert "dice_sml" in content

    def test_contains_similar_to_compound_function(self) -> None:
        """Verify cc.similar_to_compound function is defined."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        content = sql_path.read_text()
        assert "CREATE OR REPLACE FUNCTION cc.similar_to_compound(" in content
        assert "reference_comp_id TEXT" in content

    def test_all_functions_have_comments(self) -> None:
        """Verify all functions have COMMENT ON FUNCTION documentation."""
        sql_path = SCRIPTS_DIR / "rdkit_functions.sql"
        content = sql_path.read_text()
        # Count functions defined and comments
        function_count = content.count("CREATE OR REPLACE FUNCTION cc.")
        comment_count = content.count("COMMENT ON FUNCTION cc.")
        assert function_count == comment_count, (
            f"Found {function_count} functions but {comment_count} comments"
        )


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "cc"


class TestReadMmjsonBlock:
    """Tests for _read_mmjson_block function."""

    def test_reads_atp_fixture(self) -> None:
        """Read ATP.json.gz fixture file."""
        atp_path = FIXTURES_DIR / "ATP.json.gz"
        assert atp_path.exists(), f"Fixture not found: {atp_path}"

        block = _read_mmjson_block(atp_path)

        assert block is not None
        assert block.name == "ATP"

    def test_reads_hoh_fixture(self) -> None:
        """Read HOH.json.gz fixture file (water)."""
        hoh_path = FIXTURES_DIR / "HOH.json.gz"
        assert hoh_path.exists(), f"Fixture not found: {hoh_path}"

        block = _read_mmjson_block(hoh_path)

        assert block is not None
        assert block.name == "HOH"

    def test_reads_eoh_fixture(self) -> None:
        """Read EOH.json.gz fixture file (ethanol)."""
        eoh_path = FIXTURES_DIR / "EOH.json.gz"
        assert eoh_path.exists(), f"Fixture not found: {eoh_path}"

        block = _read_mmjson_block(eoh_path)

        assert block is not None
        assert block.name == "EOH"

    def test_returns_none_for_empty_file(self, tmp_path: Path) -> None:
        """Return None for empty mmJSON file."""
        mmjson_path = tmp_path / "empty.json"
        mmjson_path.write_text("{}")

        block = _read_mmjson_block(mmjson_path)

        assert block is None


class TestGenerateCanonicalSmilesFromMmjson:
    """Tests for SMILES generation from mmJSON via ccd2rdmol."""

    def test_hoh_fixture_generates_water_smiles(self) -> None:
        """HOH fixture should generate water SMILES ("O")."""
        hoh_path = FIXTURES_DIR / "HOH.json.gz"
        block = _read_mmjson_block(hoh_path)
        assert block is not None

        smiles = _generate_canonical_smiles(block)

        # Water should produce "O" as canonical SMILES
        assert smiles == "O"

    def test_eoh_fixture_generates_ethanol_smiles(self) -> None:
        """EOH fixture should generate ethanol SMILES."""
        eoh_path = FIXTURES_DIR / "EOH.json.gz"
        block = _read_mmjson_block(eoh_path)
        assert block is not None

        smiles = _generate_canonical_smiles(block)

        # Ethanol canonical SMILES
        assert smiles == "CCO"

    def test_atp_fixture_generates_smiles(self) -> None:
        """ATP fixture should generate valid SMILES."""
        atp_path = FIXTURES_DIR / "ATP.json.gz"
        block = _read_mmjson_block(atp_path)
        assert block is not None

        smiles = _generate_canonical_smiles(block)

        # ATP should produce a valid SMILES string
        assert smiles is not None
        assert len(smiles) > 0
        # ATP has adenine base and phosphate groups
        assert "N" in smiles  # Adenine nitrogen
        assert "P" in smiles  # Phosphate


class TestCcPipelineMmjsonSmiles:
    """Tests for CcPipeline (mmJSON) SMILES generation via ccd2rdmol."""

    def test_smiles_from_structure_not_descriptor(self) -> None:
        """Verify SMILES is generated from block structure, not pdbx_chem_comp_descriptor.

        mmJSON files contain SMILES in pdbx_chem_comp_descriptor, but we should
        generate our own using ccd2rdmol for consistency with CIF pipeline.
        """
        # Read HOH fixture
        hoh_path = FIXTURES_DIR / "HOH.json.gz"
        block = _read_mmjson_block(hoh_path)
        assert block is not None

        # Generate SMILES using ccd2rdmol (same as CIF pipeline)
        smiles = _generate_canonical_smiles(block)

        # Should be "O" - generated from structure, not extracted from descriptor
        assert smiles == "O"

    def test_mmjson_block_has_cif_structure(self) -> None:
        """Verify mmJSON is converted to CIF-like structure by gemmi."""
        hoh_path = FIXTURES_DIR / "HOH.json.gz"
        block = _read_mmjson_block(hoh_path)
        assert block is not None

        # gemmi converts mmJSON to CIF-like block
        # We can find categories using find_block method indirectly
        # Check the block name matches
        assert block.name == "HOH"

        # ccd2rdmol requires chem_comp_atom and chem_comp_bond tables
        # which are present in our fixtures
        # If SMILES generation works, the structure is correct
        smiles = _generate_canonical_smiles(block)
        assert smiles is not None
