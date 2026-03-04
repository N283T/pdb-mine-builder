"""Tests for CIF vs mmJSON format parity.

These tests verify that CIF and mmJSON pipelines produce identical
results when processing the same PDB entry data.
"""

import gzip
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import gemmi

from mine2.config import PipelineConfig, RdbConfig, Settings
from mine2.db.loader import Job, SchemaDef, TableDef
from mine2.pipelines.pdbj import PdbjCifPipeline, PdbjPipeline
from mine2.utils.assembly import hex_sha256


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


def create_test_schema_def() -> SchemaDef:
    """Create test schema definition with assembly tables."""
    return SchemaDef(
        schema_name="pdbj",
        primary_key="pdbid",
        tables=[
            TableDef(
                name="entry",
                columns=[("pdbid", "text"), ("id", "text")],
                primary_key=["pdbid", "id"],
            ),
            TableDef(
                name="pdbx_struct_assembly_gen",
                columns=[
                    ("pdbid", "text"),
                    ("asym_id_list", "text"),
                    ("_hash_asym_id_list", "text"),
                    ("assembly_id", "text"),
                    ("oper_expression", "text"),
                ],
                primary_key=["pdbid", "assembly_id"],
            ),
            TableDef(
                name="brief_summary",
                columns=[
                    ("pdbid", "text"),
                    ("docid", "bigint"),
                    ("plus_fields", "jsonb"),
                ],
                primary_key=["pdbid"],
            ),
            TableDef(
                name="entity",
                columns=[
                    ("pdbid", "text"),
                    ("id", "text"),
                    ("formula_weight", "double precision"),
                ],
                primary_key=["pdbid", "id"],
            ),
            TableDef(
                name="struct_asym",
                columns=[
                    ("pdbid", "text"),
                    ("id", "text"),
                    ("entity_id", "text"),
                ],
                primary_key=["pdbid", "id"],
            ),
            TableDef(
                name="pdbx_struct_assembly",
                columns=[
                    ("pdbid", "text"),
                    ("id", "text"),
                    ("details", "text"),
                ],
                primary_key=["pdbid", "id"],
            ),
        ],
    )


def create_mmjson_file(path: Path, entry_id: str, data: dict[str, list[dict]]) -> None:
    """Create a test mmJSON file (column-oriented format).

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


def create_cif_file(path: Path, entry_id: str, data: dict[str, list[dict]]) -> None:
    """Create a test CIF file with the same data structure.

    Args:
        path: Path to write the file (should end with .cif.gz)
        entry_id: Entry ID (e.g., "100d")
        data: Dict of category name to list of row dicts
    """
    pdb_id_upper = entry_id.upper()

    # Build CIF content
    lines = [f"data_{pdb_id_upper}"]

    for cat, rows in data.items():
        if not rows:
            continue

        columns = list(rows[0].keys())

        if len(rows) == 1:
            # Single row - use key-value format
            row = rows[0]
            for col in columns:
                val = row.get(col)
                if val is None:
                    val = "?"
                elif isinstance(val, str) and (" " in val or "'" in val):
                    val = f"'{val}'"
                lines.append(f"_{cat}.{col} {val}")
        else:
            # Multiple rows - use loop format
            lines.append("loop_")
            for col in columns:
                lines.append(f"_{cat}.{col}")
            for row in rows:
                row_vals = []
                for col in columns:
                    val = row.get(col)
                    if val is None:
                        val = "?"
                    elif isinstance(val, str) and (" " in val or "'" in val):
                        val = f"'{val}'"
                    row_vals.append(str(val))
                lines.append(" ".join(row_vals))

        lines.append("")  # Empty line between categories

    content = "\n".join(lines)
    doc = gemmi.cif.read_string(content)

    if str(path).endswith(".gz"):
        with tempfile.NamedTemporaryFile(suffix=".cif", delete=False) as tmp:
            doc.write_file(tmp.name)
            with open(tmp.name, "rb") as f_in:
                with gzip.open(path, "wb") as f_out:
                    f_out.write(f_in.read())
            Path(tmp.name).unlink()
    else:
        doc.write_file(str(path))


class TestHashAsymIdListParity:
    """Test that _hash_asym_id_list is computed identically for CIF and mmJSON."""

    @patch("mine2.pipelines.pdbj.sync_entry_tables")
    def test_same_hash_for_same_asym_id_list(self, mock_sync_entry_tables, tmp_path):
        """Both formats produce the same hash for identical asym_id_list."""
        entry_id = "100d"
        asym_id_list = "A,B,C"

        # Common data structure
        test_data = {
            "entry": [{"id": entry_id.upper()}],
            "entity": [{"id": "1", "formula_weight": "1000.0"}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined_assembly"}],
            "pdbx_struct_assembly_gen": [
                {
                    "assembly_id": "1",
                    "asym_id_list": asym_id_list,
                    "oper_expression": "1",
                }
            ],
        }

        # Create mmJSON file
        mmjson_dir = tmp_path / "mmjson"
        mmjson_dir.mkdir()
        mmjson_path = mmjson_dir / f"{entry_id}-noatom.json.gz"
        create_mmjson_file(mmjson_path, entry_id, test_data)

        # Create CIF file
        cif_dir = tmp_path / "cif"
        cif_dir.mkdir()
        cif_path = cif_dir / f"{entry_id}.cif.gz"
        create_cif_file(cif_path, entry_id, test_data)

        schema_def = create_test_schema_def()
        mock_sync_entry_tables.return_value = (1, 0, 0)

        # Process mmJSON
        mmjson_settings = create_test_settings(mmjson_dir)
        mmjson_pipeline = PdbjPipeline(
            mmjson_settings, mmjson_settings.pipelines["pdbj"], schema_def
        )
        mmjson_job = Job(entry_id=entry_id, filepath=mmjson_path, extra={})
        mmjson_pipeline.process_job(mmjson_job, schema_def, "test_conninfo")

        mmjson_call = mock_sync_entry_tables.call_args
        mock_sync_entry_tables.reset_mock()

        # Process CIF
        cif_settings = create_test_settings(cif_dir)
        cif_pipeline = PdbjCifPipeline(
            cif_settings, cif_settings.pipelines["pdbj"], schema_def
        )
        cif_job = Job(entry_id=entry_id, filepath=cif_path, extra={})
        cif_pipeline.process_job(cif_job, schema_def, "test_conninfo")

        cif_call = mock_sync_entry_tables.call_args
        mmjson_rows = mmjson_call.kwargs["table_rows"]["pdbx_struct_assembly_gen"]
        cif_rows = cif_call.kwargs["table_rows"]["pdbx_struct_assembly_gen"]
        mmjson_hash = mmjson_rows[0]["_hash_asym_id_list"]
        cif_hash = cif_rows[0]["_hash_asym_id_list"]

        # Verify both are correct
        expected_hash = hex_sha256(asym_id_list)
        assert mmjson_hash == expected_hash
        assert cif_hash == expected_hash
        assert mmjson_hash == cif_hash


class TestBuMwParity:
    """Test that bu_mw is calculated identically for CIF and mmJSON."""

    @patch("mine2.pipelines.pdbj.sync_entry_tables")
    def test_same_bu_mw_for_same_data(self, mock_sync_entry_tables, tmp_path):
        """Both formats produce the same bu_mw for identical assembly data."""
        entry_id = "100d"

        # Common data structure
        test_data = {
            "entry": [{"id": entry_id.upper()}],
            "brief_summary": [{"docid": "100"}],
            "entity": [{"id": "1", "formula_weight": "1000.0"}],
            "struct_asym": [{"id": "A", "entity_id": "1"}],
            "pdbx_struct_assembly": [{"id": "1", "details": "author_defined_assembly"}],
            "pdbx_struct_assembly_gen": [
                {
                    "assembly_id": "1",
                    "asym_id_list": "A",
                    "oper_expression": "1",
                }
            ],
        }

        # Create mmJSON file
        mmjson_dir = tmp_path / "mmjson"
        mmjson_dir.mkdir()
        mmjson_path = mmjson_dir / f"{entry_id}-noatom.json.gz"
        create_mmjson_file(mmjson_path, entry_id, test_data)

        # Create CIF file
        cif_dir = tmp_path / "cif"
        cif_dir.mkdir()
        cif_path = cif_dir / f"{entry_id}.cif.gz"
        create_cif_file(cif_path, entry_id, test_data)

        schema_def = create_test_schema_def()
        mock_sync_entry_tables.return_value = (1, 0, 0)

        # Process mmJSON
        mmjson_settings = create_test_settings(mmjson_dir)
        mmjson_pipeline = PdbjPipeline(
            mmjson_settings, mmjson_settings.pipelines["pdbj"], schema_def
        )
        mmjson_job = Job(entry_id=entry_id, filepath=mmjson_path, extra={})
        mmjson_pipeline.process_job(mmjson_job, schema_def, "test_conninfo")

        mmjson_call = mock_sync_entry_tables.call_args
        mock_sync_entry_tables.reset_mock()

        # Process CIF
        cif_settings = create_test_settings(cif_dir)
        cif_pipeline = PdbjCifPipeline(
            cif_settings, cif_settings.pipelines["pdbj"], schema_def
        )
        cif_job = Job(entry_id=entry_id, filepath=cif_path, extra={})
        cif_pipeline.process_job(cif_job, schema_def, "test_conninfo")

        cif_call = mock_sync_entry_tables.call_args
        mmjson_plus_fields = mmjson_call.kwargs["table_rows"]["brief_summary"][0][
            "plus_fields"
        ]
        cif_plus_fields = cif_call.kwargs["table_rows"]["brief_summary"][0][
            "plus_fields"
        ]
        if isinstance(mmjson_plus_fields, str):
            mmjson_plus_fields = json.loads(mmjson_plus_fields)
        if isinstance(cif_plus_fields, str):
            cif_plus_fields = json.loads(cif_plus_fields)
        mmjson_bu_mw = mmjson_plus_fields.get("bu_mw")
        cif_bu_mw = cif_plus_fields.get("bu_mw")

        # Verify both are correct
        assert mmjson_bu_mw == 1000.0
        assert cif_bu_mw == 1000.0
        assert mmjson_bu_mw == cif_bu_mw


class TestPatchParity:
    """Test that patches are applied identically for CIF and mmJSON."""

    def test_7ed1_patch_applied_to_both_formats(self):
        """7ed1 patch is applied identically to both formats."""
        from mine2.utils.patches import apply_patches

        # CIF-like data (plain column names)
        cif_data = {"entry": [{"id": "7ED1"}]}

        # mmJSON-like data (same structure after parsing)
        mmjson_data = {"entry": [{"id": "7ED1"}]}

        cif_result = apply_patches("7ed1", cif_data)
        mmjson_result = apply_patches("7ed1", mmjson_data)

        # Both should have chem_comp with MET
        assert "chem_comp" in cif_result
        assert "chem_comp" in mmjson_result

        cif_met = [r for r in cif_result["chem_comp"] if r.get("id") == "MET"]
        mmjson_met = [r for r in mmjson_result["chem_comp"] if r.get("id") == "MET"]

        assert len(cif_met) == 1
        assert len(mmjson_met) == 1
        assert cif_met[0] == mmjson_met[0]
