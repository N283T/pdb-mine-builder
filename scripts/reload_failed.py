#!/usr/bin/env python3
"""Reload failed PDB entries after schema fix.

Usage:
    pixi run python scripts/reload_failed.py

This script:
1. Recreates pdbx_struct_assembly_gen primary key with _hash_asym_id_list
2. Reloads only the 290 failed entries from failed_pdbids.txt
"""

import sys
from pathlib import Path

import psycopg
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mine2.config import load_config
from mine2.db.loader import Job, load_schema_def
from mine2.pipelines.pdbj import PdbjCifPipeline


def recreate_primary_key(conninfo: str, schema: str = "pdbj") -> None:
    """Drop and recreate pdbx_struct_assembly_gen primary key."""
    print("Recreating primary key for pdbx_struct_assembly_gen...")

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            # Drop existing primary key
            cur.execute(f"""
                ALTER TABLE {schema}.pdbx_struct_assembly_gen
                DROP CONSTRAINT IF EXISTS pdbx_struct_assembly_gen_pkey
            """)

            # Create new primary key with _hash_asym_id_list
            cur.execute(f"""
                ALTER TABLE {schema}.pdbx_struct_assembly_gen
                ADD CONSTRAINT pdbx_struct_assembly_gen_pkey
                PRIMARY KEY (pdbid, assembly_id, _hash_asym_id_list, oper_expression)
            """)

            conn.commit()

    print("  Done.")


def load_failed_pdbids(filepath: Path) -> list[str]:
    """Load failed PDB IDs from file."""
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return []

    pdbids = []
    for line in filepath.read_text().splitlines():
        # Format: "     1→1vy4" - extract the pdbid after →
        if "→" in line:
            pdbid = line.split("→")[1].strip()
            if pdbid:
                pdbids.append(pdbid)

    return pdbids


def find_cif_path(pdbid: str, data_dir: Path) -> Path | None:
    """Find CIF file path for a PDB ID.

    Files are in divided structure: data_dir/xy/1xyz.cif.gz
    """
    middle = pdbid[1:3]
    cif_path = data_dir / middle / f"{pdbid}.cif.gz"
    if cif_path.exists():
        return cif_path
    return None


def find_plus_path(pdbid: str, plus_dir: Path | None) -> Path | None:
    """Find plus JSON file path for a PDB ID."""
    if not plus_dir:
        return None
    plus_path = plus_dir / f"{pdbid}-plus.json.gz"
    if plus_path.exists():
        return plus_path
    return None


def main():
    # Load config
    config_path = Path("config.yml")
    if not config_path.exists():
        print("config.yml not found")
        return 1

    settings = load_config(config_path)
    conninfo = settings.rdb.constring

    # Load schema
    schema_path = Path("schemas/pdbj.def.yml")
    schema_def = load_schema_def(schema_path)

    # Get pipeline config
    pipeline_config = settings.pipelines.get("pdbj")
    if not pipeline_config:
        print("pdbj pipeline not configured")
        return 1

    data_dir = Path(pipeline_config.data)
    plus_dir = Path(pipeline_config.data_plus) if pipeline_config.data_plus else None

    # Load failed PDB IDs
    failed_file = Path("failed_pdbids.txt")
    pdbids = load_failed_pdbids(failed_file)
    print(f"Found {len(pdbids)} failed PDB IDs")

    if not pdbids:
        return 1

    # Step 1: Recreate primary key
    recreate_primary_key(conninfo)

    # Step 2: Delete existing data for these entries
    print(f"Deleting existing data for {len(pdbids)} entries...")
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM pdbj.pdbx_struct_assembly_gen WHERE pdbid = ANY(%s)",
                (pdbids,),
            )
            deleted = cur.rowcount
            print(f"  Deleted {deleted} rows from pdbx_struct_assembly_gen")
            conn.commit()

    # Step 3: Reload entries
    print(f"Reloading {len(pdbids)} entries...")

    # Create pipeline instance for process_job
    pipeline = PdbjCifPipeline(settings, pipeline_config, schema_def)

    success = 0
    failed = 0
    failed_entries = []

    for pdbid in tqdm(pdbids, desc="Processing"):
        cif_path = find_cif_path(pdbid, data_dir)
        if not cif_path:
            failed += 1
            failed_entries.append((pdbid, "CIF file not found"))
            continue

        plus_path = find_plus_path(pdbid, plus_dir)

        job = Job(
            entry_id=pdbid,
            filepath=cif_path,
            extra={"plus_path": plus_path},
        )

        result = pipeline.process_job(job, schema_def, conninfo)

        if result.success:
            success += 1
        else:
            failed += 1
            error = (result.error or "Unknown error").split("\n")[0][:100]
            failed_entries.append((pdbid, error))

    # Summary
    print(f"\nResults: {success} succeeded, {failed} failed")

    if failed_entries:
        print("\nFailed entries:")
        for pdbid, error in failed_entries[:10]:
            print(f"  {pdbid}: {error}")
        if len(failed_entries) > 10:
            print(f"  ... and {len(failed_entries) - 10} more")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
