"""Tests for shared RDKit utilities."""

from unittest.mock import MagicMock, patch

import pytest

from pdbminebuilder.pipelines.rdkit_utils import (
    RDKIT_DESCRIPTORS,
    RdkitDescriptor,
    _ALLOWED_SCHEMAS,
    _add_rdkit_descriptor_columns,
    ensure_rdkit_setup,
    generate_canonical_smiles,
)


class TestGenerateCanonicalSmiles:
    """Tests for generate_canonical_smiles function."""

    def test_returns_string_or_none(self) -> None:
        """Return a string SMILES or None, never raises."""
        import gemmi

        block = gemmi.cif.read_string("data_EMPTY\n")[0]
        result = generate_canonical_smiles(block)
        assert result is None or isinstance(result, str)

    def test_returns_none_on_value_error(self) -> None:
        """Return None and log warning when ccd2rdmol raises ValueError."""
        import gemmi

        block = gemmi.cif.read_string("data_EMPTY\n")[0]
        with patch(
            "pdbminebuilder.pipelines.rdkit_utils.read_ccd_block",
            side_effect=ValueError("bad data"),
        ):
            result = generate_canonical_smiles(block)
        assert result is None

    def test_returns_none_on_runtime_error(self) -> None:
        """Return None and log warning when RDKit raises RuntimeError."""
        import gemmi

        block = gemmi.cif.read_string("data_TEST\n")[0]
        with patch(
            "pdbminebuilder.pipelines.rdkit_utils.read_ccd_block",
            side_effect=RuntimeError("RDKit internal error"),
        ):
            result = generate_canonical_smiles(block)
        assert result is None

    def test_returns_none_when_mol_is_none(self) -> None:
        """Return None when read_ccd_block produces mol=None."""
        import gemmi

        block = gemmi.cif.read_string("data_NOMOL\n")[0]
        mock_result = MagicMock()
        mock_result.mol = None
        with patch(
            "pdbminebuilder.pipelines.rdkit_utils.read_ccd_block",
            return_value=mock_result,
        ):
            result = generate_canonical_smiles(block)
        assert result is None


class TestRdkitDescriptors:
    """Tests for RDKIT_DESCRIPTORS constant."""

    def test_has_eight_descriptors(self) -> None:
        """Should have exactly 8 descriptor definitions."""
        assert len(RDKIT_DESCRIPTORS) == 8

    def test_is_immutable_tuple(self) -> None:
        """Should be a tuple (immutable), not a list."""
        assert isinstance(RDKIT_DESCRIPTORS, tuple)

    def test_elements_are_named_tuples(self) -> None:
        """Each descriptor should be an RdkitDescriptor NamedTuple."""
        for desc in RDKIT_DESCRIPTORS:
            assert isinstance(desc, RdkitDescriptor)
            assert desc.column_name.startswith("rdkit_")
            assert desc.column_type in ("double precision", "integer", "text")
            assert desc.rdkit_function.startswith("mol_")


class TestAllowedSchemas:
    """Tests for _ALLOWED_SCHEMAS security allowlist."""

    def test_contains_expected_schemas(self) -> None:
        """Should contain cc, prd, and chem."""
        assert "cc" in _ALLOWED_SCHEMAS
        assert "prd" in _ALLOWED_SCHEMAS
        assert "chem" in _ALLOWED_SCHEMAS

    def test_is_frozenset(self) -> None:
        """Should be immutable."""
        assert isinstance(_ALLOWED_SCHEMAS, frozenset)


class TestAddRdkitDescriptorColumns:
    """Tests for _add_rdkit_descriptor_columns function."""

    def test_rejects_invalid_schema(self) -> None:
        """Raises ValueError for schemas not in allowlist."""
        mock_cursor = MagicMock()
        with pytest.raises(ValueError, match="not in allowed list"):
            _add_rdkit_descriptor_columns(mock_cursor, "evil_schema")

    def test_uses_correct_table_for_chem_schema(self) -> None:
        """Uses 'compounds' table for chem schema."""
        mock_cursor = MagicMock()
        # Table doesn't exist
        mock_cursor.fetchone.return_value = (False,)
        _add_rdkit_descriptor_columns(mock_cursor, "chem")

        # Should check for chem.compounds table
        first_call_args = mock_cursor.execute.call_args_list[0]
        params = first_call_args[0][1]
        assert params[0] == "chem"
        assert params[1] == "compounds"

    def test_early_return_when_table_missing(self) -> None:
        """Returns early without ALTER when table/mol column not found."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (False,)
        _add_rdkit_descriptor_columns(mock_cursor, "cc")

        # Only the EXISTS check query should have been executed
        assert mock_cursor.execute.call_count == 1
        sql = str(mock_cursor.execute.call_args_list[0][0][0])
        assert "information_schema" in sql

    def test_parameterized_for_prd_schema(self) -> None:
        """Uses prd schema correctly."""
        mock_cursor = MagicMock()
        _add_rdkit_descriptor_columns(mock_cursor, "prd")

        all_sql = " ".join(
            str(call[0][0]) for call in mock_cursor.execute.call_args_list
        )
        assert "compute_rdkit_descriptors" in all_sql


class TestEnsureRdkitSetup:
    """Tests for ensure_rdkit_setup function."""

    def test_rejects_invalid_schema(self) -> None:
        """Raises ValueError for schemas not in allowlist."""
        with pytest.raises(ValueError, match="not in allowed list"):
            ensure_rdkit_setup("test_conninfo", schema="evil_schema")

    def test_creates_extension_for_prd(self) -> None:
        """Creates RDKit extension for prd schema."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        with patch(
            "pdbminebuilder.pipelines.rdkit_utils.psycopg.connect",
            return_value=mock_conn,
        ):
            ensure_rdkit_setup("test_conninfo", schema="prd")

        mock_cursor.execute.assert_any_call("CREATE EXTENSION IF NOT EXISTS rdkit")
        mock_conn.commit.assert_called_once()

    def test_loads_sql_functions(self, tmp_path) -> None:
        """Loads SQL functions from provided path."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        sql_file = tmp_path / "test_functions.sql"
        sql_file.write_text("SELECT 1;")

        with patch(
            "pdbminebuilder.pipelines.rdkit_utils.psycopg.connect",
            return_value=mock_conn,
        ):
            ensure_rdkit_setup(
                "test_conninfo", schema="cc", sql_functions_path=sql_file
            )

        # Verify the SQL file content was executed
        all_sql = [str(call[0][0]) for call in mock_cursor.execute.call_args_list]
        assert "SELECT 1;" in all_sql
