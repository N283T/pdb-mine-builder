"""Tests for shared RDKit utilities."""

from unittest.mock import MagicMock, patch

import pytest

from pdbminebuilder.pipelines.rdkit_utils import (
    RDKIT_DESCRIPTORS,
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


class TestRdkitDescriptors:
    """Tests for RDKIT_DESCRIPTORS constant."""

    def test_has_eight_descriptors(self) -> None:
        """Should have exactly 8 descriptor definitions."""
        assert len(RDKIT_DESCRIPTORS) == 8

    def test_all_tuples_have_three_elements(self) -> None:
        """Each descriptor should be (column_name, column_type, rdkit_function)."""
        for desc in RDKIT_DESCRIPTORS:
            assert len(desc) == 3
            assert desc[0].startswith("rdkit_")
            assert desc[1] in ("double precision", "integer", "text")
            assert desc[2].startswith("mol_")


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
