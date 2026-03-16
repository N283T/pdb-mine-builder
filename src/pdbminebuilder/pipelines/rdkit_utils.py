"""Shared RDKit utilities for chemical pipelines (cc, prd, chem)."""

import logging
from pathlib import Path
from typing import Any

import gemmi
import psycopg
from ccd2rdmol import read_ccd_block
from rdkit import Chem
from rich.console import Console
from rich.prompt import Confirm

logger = logging.getLogger(__name__)
console = Console()


def generate_canonical_smiles(block: gemmi.cif.Block) -> str | None:
    """Generate canonical SMILES from a CIF block using ccd2rdmol.

    Works with CCD blocks and PRDCC blocks (same _chem_comp_atom/_chem_comp_bond structure).

    Args:
        block: gemmi CIF block containing chemical component data

    Returns:
        Canonical SMILES string, or None if conversion failed
    """
    try:
        from rdkit import RDLogger

        RDLogger.DisableLog("rdApp.*")
        try:
            result = read_ccd_block(block, sanitize_mol=True, add_conformers=False)
            if result.mol is not None:
                return Chem.MolToSmiles(result.mol, canonical=True)
        finally:
            RDLogger.EnableLog("rdApp.*")
    except (ValueError, RuntimeError, KeyError, OSError) as e:
        logger.warning("SMILES generation failed for %s: %s", block.name, e)
    return None


# Hardcoded descriptors - NEVER derive from external sources
# Format: (column_name, column_type, rdkit_function)
RDKIT_DESCRIPTORS: list[tuple[str, str, str]] = [
    ("rdkit_mw", "double precision", "mol_amw"),
    ("rdkit_logp", "double precision", "mol_logp"),
    ("rdkit_tpsa", "double precision", "mol_tpsa"),
    ("rdkit_hba", "integer", "mol_hba"),
    ("rdkit_hbd", "integer", "mol_hbd"),
    ("rdkit_rotbonds", "integer", "mol_numrotatablebonds"),
    ("rdkit_rings", "integer", "mol_numrings"),
    ("rdkit_formula", "text", "mol_formula"),
]

# Allowed schema names for RDKit setup (security allowlist)
_ALLOWED_SCHEMAS = frozenset({"cc", "prd", "chem"})


def _add_rdkit_descriptor_columns(
    cur: "psycopg.Cursor[tuple[Any, ...]]",
    schema: str,
) -> None:
    """Add RDKit molecular descriptor columns to brief_summary.

    SECURITY: All column definitions are hardcoded allowlists.
    DO NOT accept external input for column names, types, or functions.
    """
    if schema not in _ALLOWED_SCHEMAS:
        raise ValueError(f"Schema {schema!r} not in allowed list: {_ALLOWED_SCHEMAS}")

    table_name = "brief_summary" if schema != "chem" else "compounds"

    # Check if table and mol column exist
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        ) AND EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = %s
            AND table_name = %s
            AND column_name = 'mol'
        )
    """,
        (schema, table_name, schema, table_name),
    )
    result = cur.fetchone()
    if not result or not result[0]:
        return  # Table or mol column doesn't exist yet

    fqn = f"{schema}.{table_name}"

    for col_name, col_type, _ in RDKIT_DESCRIPTORS:
        cur.execute(
            """
            SELECT
                EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = %s
                    AND table_name = %s
                    AND column_name = %s
                ),
                (
                    SELECT is_generated FROM information_schema.columns
                    WHERE table_schema = %s
                    AND table_name = %s
                    AND column_name = %s
                )
        """,
            (schema, table_name, col_name, schema, table_name, col_name),
        )
        result = cur.fetchone()
        col_exists = result[0] if result else False
        is_generated = result[1] if result else None

        if col_exists and is_generated == "ALWAYS":
            cur.execute(f"ALTER TABLE {fqn} DROP COLUMN {col_name}")  # type: ignore[arg-type]
            col_exists = False

        if not col_exists:
            cur.execute(
                f"ALTER TABLE {fqn} ADD COLUMN {col_name} {col_type}"  # type: ignore[arg-type]
            )

    # Create or replace trigger function to compute descriptors
    cur.execute(
        f"""
        CREATE OR REPLACE FUNCTION {schema}.compute_rdkit_descriptors()
        RETURNS TRIGGER AS $$
        DECLARE
            mol_obj mol;
        BEGIN
            IF NEW.canonical_smiles IS NOT NULL
               AND is_valid_smiles(NEW.canonical_smiles::cstring) THEN
                mol_obj := mol_from_smiles(NEW.canonical_smiles::cstring);
                NEW.rdkit_mw := mol_amw(mol_obj);
                NEW.rdkit_logp := mol_logp(mol_obj);
                NEW.rdkit_tpsa := mol_tpsa(mol_obj);
                NEW.rdkit_hba := mol_hba(mol_obj);
                NEW.rdkit_hbd := mol_hbd(mol_obj);
                NEW.rdkit_rotbonds := mol_numrotatablebonds(mol_obj);
                NEW.rdkit_rings := mol_numrings(mol_obj);
                NEW.rdkit_formula := mol_formula(mol_obj);
            ELSE
                NEW.rdkit_mw := NULL;
                NEW.rdkit_logp := NULL;
                NEW.rdkit_tpsa := NULL;
                NEW.rdkit_hba := NULL;
                NEW.rdkit_hbd := NULL;
                NEW.rdkit_rotbonds := NULL;
                NEW.rdkit_rings := NULL;
                NEW.rdkit_formula := NULL;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """  # type: ignore[arg-type]
    )

    # Create trigger if it doesn't exist
    trigger_name = f"trg_{schema}_compute_rdkit_descriptors"
    cur.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_trigger
                WHERE tgname = '{trigger_name}'
            ) THEN
                CREATE TRIGGER {trigger_name}
                BEFORE INSERT OR UPDATE OF canonical_smiles
                ON {fqn}
                FOR EACH ROW
                EXECUTE FUNCTION {schema}.compute_rdkit_descriptors();
            END IF;
        END $$
    """  # type: ignore[arg-type]
    )

    # Populate existing rows that have NULL descriptor values
    cur.execute(
        f"""
        UPDATE {fqn}
        SET rdkit_mw = mol_amw(mol),
            rdkit_logp = mol_logp(mol),
            rdkit_tpsa = mol_tpsa(mol),
            rdkit_hba = mol_hba(mol),
            rdkit_hbd = mol_hbd(mol),
            rdkit_rotbonds = mol_numrotatablebonds(mol),
            rdkit_rings = mol_numrings(mol),
            rdkit_formula = mol_formula(mol)
        WHERE canonical_smiles IS NOT NULL
          AND mol IS NOT NULL
          AND rdkit_mw IS NULL
    """  # type: ignore[arg-type]
    )


def ensure_rdkit_setup(
    conninfo: str,
    schema: str,
    sql_functions_path: Path | None = None,
) -> None:
    """Ensure RDKit extension, mol column, and SQL functions exist for a schema.

    This is idempotent - safe to call on every pipeline run.

    Args:
        conninfo: PostgreSQL connection string
        schema: Schema name (must be in _ALLOWED_SCHEMAS)
        sql_functions_path: Path to SQL functions file to load (optional)
    """
    if schema not in _ALLOWED_SCHEMAS:
        raise ValueError(f"Schema {schema!r} not in allowed list: {_ALLOWED_SCHEMAS}")

    table_name = "brief_summary" if schema != "chem" else "compounds"
    fqn = f"{schema}.{table_name}"

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            # Create RDKit extension
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS rdkit")
            except psycopg.errors.InsufficientPrivilege:
                conn.rollback()
                msg = "Cannot create RDKit extension (insufficient privileges)."
                logger.warning(msg)
                console.print(f"  [yellow]{msg}[/yellow]")
                console.print(
                    "  Run: psql -U <superuser> -d <dbname> -c 'CREATE EXTENSION rdkit'"
                )
                if not Confirm.ask("  Continue without RDKit?", default=False):
                    raise SystemExit(1)
                return

            # Add mol column if table exists but column doesn't
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = %s
                ), EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = %s
                    AND table_name = %s
                    AND column_name = 'mol'
                )
            """,
                (schema, table_name, schema, table_name),
            )
            result = cur.fetchone()
            table_exists = result[0] if result else False
            mol_exists = result[1] if result else False

            if table_exists and not mol_exists:
                mol_ddl = f"""
                    ALTER TABLE {fqn}
                    ADD COLUMN mol mol GENERATED ALWAYS AS (
                        CASE
                            WHEN canonical_smiles IS NOT NULL
                                 AND is_valid_smiles(canonical_smiles::cstring)
                            THEN mol_from_smiles(canonical_smiles::cstring)
                            ELSE NULL
                        END
                    ) STORED
                """
                cur.execute(mol_ddl)  # type: ignore[arg-type]

                idx_ddl = f"""
                    CREATE INDEX IF NOT EXISTS {table_name}_mol_idx
                    ON {fqn} USING gist(mol)
                """
                cur.execute(idx_ddl)  # type: ignore[arg-type]

            # Add RDKit descriptor columns
            _add_rdkit_descriptor_columns(cur, schema)

            # Load RDKit SQL functions
            if sql_functions_path and sql_functions_path.exists():
                sql_content = sql_functions_path.read_text()
                cur.execute(sql_content)  # type: ignore[arg-type]
                logger.debug(f"Loaded RDKit functions from {sql_functions_path}")

        conn.commit()
    console.print(f"  [green]RDKit setup verified ({schema})[/green]")
