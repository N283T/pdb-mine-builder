"""Refresh the unified chem.compounds table from cc and prd data."""

import logging
from pathlib import Path

import psycopg
from rich.console import Console
from rich.prompt import Confirm

from pdbminebuilder.config import Settings
from pdbminebuilder.pipelines.rdkit_utils import ensure_rdkit_setup

logger = logging.getLogger(__name__)
console = Console()


def refresh_compounds(settings: Settings, *, force: bool = False) -> None:
    """Truncate and repopulate chem.compounds from cc and prd brief_summary.

    Args:
        settings: Application settings with DB connection info
        force: Skip confirmation prompt
    """
    if not force:
        if not Confirm.ask(
            "This will truncate and repopulate chem.compounds. Continue?"
        ):
            console.print("[yellow]Aborted.[/yellow]")
            return

    conninfo = settings.rdb.constring

    # Ensure chem schema and table exist
    _ensure_schema_and_table(conninfo)

    # Set up RDKit for chem schema (mol column, descriptors, triggers)
    sql_path = Path(__file__).parent.parent.parent.parent.joinpath(
        "scripts", "rdkit_functions_chem.sql"
    )
    ensure_rdkit_setup(
        conninfo,
        schema="chem",
        sql_functions_path=sql_path if sql_path.exists() else None,
    )

    # Populate the table
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE chem.compounds")

            # Insert from cc.brief_summary
            cc_count = _insert_cc_compounds(cur)
            console.print(f"  Inserted {cc_count} cc compounds")

            # Insert from prd.brief_summary
            prd_count = _insert_prd_compounds(cur)
            console.print(f"  Inserted {prd_count} prd compounds")

        conn.commit()

    console.print(
        f"  [green]chem.compounds refreshed: {cc_count + prd_count} total[/green]"
    )


def _ensure_schema_and_table(conninfo: str) -> None:
    """Create chem schema and compounds table if they don't exist."""
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS chem")
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'chem' AND table_name = 'compounds'
                )
                """
            )
            result = cur.fetchone()
            if not result or not result[0]:
                cur.execute("""
                    CREATE TABLE chem.compounds (
                        id TEXT NOT NULL,
                        source TEXT NOT NULL,
                        canonical_smiles TEXT,
                        name TEXT,
                        formula TEXT,
                        cc_comp_ids TEXT[],
                        PRIMARY KEY (source, id),
                        CONSTRAINT ck_compounds_source CHECK (source IN ('cc', 'prd'))
                    )
                """)
                console.print("  Created chem.compounds table")
        conn.commit()


def _insert_cc_compounds(cur: "psycopg.Cursor[tuple]") -> int:
    """Insert cc compounds into chem.compounds."""
    cur.execute("""
        INSERT INTO chem.compounds (id, source, canonical_smiles, name, formula, cc_comp_ids)
        SELECT comp_id, 'cc', canonical_smiles, name, formula, ARRAY[comp_id]
        FROM cc.brief_summary
        WHERE canonical_smiles IS NOT NULL
    """)
    return cur.rowcount


def _insert_prd_compounds(cur: "psycopg.Cursor[tuple]") -> int:
    """Insert prd compounds into chem.compounds."""
    cur.execute("""
        INSERT INTO chem.compounds (id, source, canonical_smiles, name, formula, cc_comp_ids)
        SELECT b.prd_id, 'prd', b.canonical_smiles, b.name, b.formula,
               CASE WHEN b.chem_comp_id IS NOT NULL
                    THEN ARRAY[b.chem_comp_id]
                    ELSE NULL
               END
        FROM prd.brief_summary b
        WHERE b.canonical_smiles IS NOT NULL
    """)
    return cur.rowcount
