"""PDBj pipeline - main PDB structure data loader."""

import json
import traceback
from pathlib import Path
from typing import Any

import gemmi
from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.cif import parse_cif_file, parse_mmjson_file
from mine2.parsers.mmjson import merge_data, normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category
from mine2.utils.assembly import calculate_mw_for_bu, hex_sha256
from mine2.utils.patches import apply_patches

console = Console()


class PdbjPipeline(BasePipeline):
    """Pipeline for loading PDB structure data."""

    name = "pdbj"
    file_pattern = "*-noatom.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract entry ID from filepath.

        Handles filenames like: 100d-noatom.json.gz -> 100d
        """
        name = filepath.name
        # Remove .json.gz
        if name.endswith(".json.gz"):
            name = name[:-8]
        # Remove -noatom suffix
        if name.endswith("-noatom"):
            name = name[:-7]
        return name

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find mmJSON files and pair with plus data if available."""
        data_dir = Path(self.config.data)
        plus_dir = Path(self.config.data_plus) if self.config.data_plus else None

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath in sorted(data_dir.rglob(self.file_pattern)):
            entry_id = self.extract_entry_id(filepath)

            # Look for plus file: 100d-plus.json.gz
            plus_path = None
            if plus_dir and plus_dir.exists():
                candidate = plus_dir.joinpath(f"{entry_id}-plus.json.gz")
                # Validate path is within plus_dir to prevent path traversal
                try:
                    resolved = candidate.resolve()
                    if (
                        resolved.is_relative_to(plus_dir.resolve())
                        and resolved.exists()
                    ):
                        plus_path = candidate
                except (ValueError, OSError):
                    # is_relative_to raises ValueError if not relative
                    pass

            jobs.append(
                Job(
                    entry_id=entry_id,
                    filepath=filepath,
                    extra={"plus_path": plus_path},
                )
            )

            if limit and len(jobs) >= limit:
                break

        return jobs

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PDB entry."""
        try:
            # Load main data (row-oriented)
            data = parse_mmjson_file(job.filepath)

            # Merge with plus data if available
            plus_path = job.extra.get("plus_path")
            if plus_path:
                plus_data = parse_mmjson_file(plus_path)
                data = merge_data(data, plus_data)

            # Apply entry-specific patches
            apply_patches(job.entry_id, data)

            # Add _hash_asym_id_list to pdbx_struct_assembly_gen
            if "pdbx_struct_assembly_gen" in data:
                for row in data["pdbx_struct_assembly_gen"]:
                    asym_id_list = row.get("asym_id_list", "")
                    row["_hash_asym_id_list"] = hex_sha256(asym_id_list)

            # Transform and load
            rows_inserted = 0

            # Get entry table definition for its primary key
            entry_table = next(
                (t for t in schema_def.tables if t.name == "entry"), None
            )
            entry_pk = (
                entry_table.primary_key if entry_table else [schema_def.primary_key]
            )

            # Load entry table
            entry_rows = self._transform_entry(data, job.entry_id)
            if entry_rows:
                # Explicitly order columns to avoid dict ordering assumptions
                columns = list(entry_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "entry",
                    columns,
                    [tuple(r[c] for c in columns) for r in entry_rows],
                    entry_pk,
                )
                rows_inserted += inserted

            # Load brief_summary with bu_mw calculation
            brief_table = next(
                (t for t in schema_def.tables if t.name == "brief_summary"), None
            )
            if brief_table:
                brief_rows = self._transform_brief_summary(
                    data, brief_table, job.entry_id
                )
                if brief_rows:
                    columns = list(brief_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        schema_def.schema_name,
                        "brief_summary",
                        columns,
                        [tuple(r[c] for c in columns) for r in brief_rows],
                        brief_table.primary_key,
                    )
                    rows_inserted += inserted

            # Load other categories
            for table in schema_def.tables:
                if table.name in ("entry", "brief_summary"):
                    continue

                category_rows = self._transform_category(data, table, job.entry_id)
                if category_rows:
                    # Explicitly order columns to avoid dict ordering assumptions
                    columns = list(category_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        schema_def.schema_name,
                        table.name,
                        columns,
                        [tuple(r[c] for c in columns) for r in category_rows],
                        table.primary_key,
                    )
                    rows_inserted += inserted

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=rows_inserted,
            )

        except Exception as e:
            # Include traceback for debugging
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )

    def _transform_entry(self, data: dict[str, Any], entry_id: str) -> list[dict]:
        """Transform entry data."""
        rows = data.get("entry", [])
        if not rows:
            # Fallback: create minimal entry with both PK columns
            return [{"pdbid": entry_id, "id": entry_id.upper()}]

        result = []
        for row in rows:
            result.append(
                {
                    "pdbid": entry_id,
                    **{k: v for k, v in row.items() if v is not None},
                }
            )
        return result

    def _transform_brief_summary(
        self,
        data: dict[str, Any],
        table: TableDef,
        entry_id: str,
    ) -> list[dict]:
        """Transform brief_summary with bu_mw calculation.

        Adds bu_mw (biological unit molecular weight) to plus_fields.
        """
        rows = data.get("brief_summary", [])
        result = transform_category(
            rows, table, entry_id, "pdbid", normalize_column_name
        )

        # Calculate bu_mw and add to plus_fields
        bu_mw = calculate_mw_for_bu(data)
        for row in result:
            # Merge bu_mw into existing plus_fields or create new
            existing_plus = row.get("plus_fields")
            if existing_plus:
                try:
                    plus_data = json.loads(existing_plus)
                except (json.JSONDecodeError, TypeError):
                    plus_data = {}
            else:
                plus_data = {}
            plus_data["bu_mw"] = bu_mw
            row["plus_fields"] = json.dumps(plus_data)

        return result

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        entry_id: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, entry_id, "pdbid", normalize_column_name)


class PdbjCifPipeline(BasePipeline):
    """Pipeline for loading PDB structure data from CIF files.

    Uses mmCIF files from structures/divided/mmCIF/ directory.
    Unlike mmJSON, CIF files contain full atomic data but we only
    load categories defined in the schema (atom_site is excluded).

    Uses gemmi.CifWalk for fast file discovery instead of rglob.
    """

    name = "pdbj-cif"
    # file_pattern not used - using gemmi.CifWalk instead

    # extract_entry_id inherited from BasePipeline handles .cif.gz and .cif

    def find_jobs(self, limit: int | None = None) -> list[Job]:
        """Find CIF files using gemmi.CifWalk.

        CifWalk is C++ native and faster than rglob for large directories.
        Automatically handles both .cif and .cif.gz files.
        Also pairs with plus data (mmJSON) if configured.
        """
        data_dir = Path(self.config.data)
        plus_dir = Path(self.config.data_plus) if self.config.data_plus else None

        if not data_dir.exists():
            console.print(f"  [red]Data directory not found: {data_dir}[/red]")
            return []

        jobs = []
        for filepath_str in gemmi.CifWalk(str(data_dir)):
            filepath = Path(filepath_str)
            entry_id = self.extract_entry_id(filepath)

            # Look for plus file: {entry_id}-plus.json.gz
            plus_path = None
            if plus_dir and plus_dir.exists():
                candidate = plus_dir.joinpath(f"{entry_id}-plus.json.gz")
                # Validate path is within plus_dir to prevent path traversal
                try:
                    resolved = candidate.resolve()
                    if (
                        resolved.is_relative_to(plus_dir.resolve())
                        and resolved.exists()
                    ):
                        plus_path = candidate
                except (ValueError, OSError):
                    # is_relative_to raises ValueError if not relative
                    pass

            jobs.append(
                Job(
                    entry_id=entry_id,
                    filepath=filepath,
                    extra={"plus_path": plus_path},
                )
            )

            if limit and len(jobs) >= limit:
                break

        return jobs

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PDB entry from CIF."""
        try:
            # Parse CIF file (row-oriented, same format as mmJSON)
            data = parse_cif_file(job.filepath)

            # Merge with plus data if available (mmJSON format)
            plus_path = job.extra.get("plus_path") if job.extra else None
            if plus_path:
                plus_data = parse_mmjson_file(plus_path)
                data = merge_data(data, plus_data)

            # Apply entry-specific patches
            apply_patches(job.entry_id, data)

            # Add _hash_asym_id_list to pdbx_struct_assembly_gen
            if "pdbx_struct_assembly_gen" in data:
                for row in data["pdbx_struct_assembly_gen"]:
                    asym_id_list = row.get("asym_id_list", "")
                    row["_hash_asym_id_list"] = hex_sha256(asym_id_list)

            # Transform and load
            rows_inserted = 0

            # Get entry table definition for its primary key
            entry_table = next(
                (t for t in schema_def.tables if t.name == "entry"), None
            )
            entry_pk = (
                entry_table.primary_key if entry_table else [schema_def.primary_key]
            )

            # Load entry table
            entry_rows = self._transform_entry(data, job.entry_id)
            if entry_rows:
                columns = list(entry_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "entry",
                    columns,
                    [tuple(r[c] for c in columns) for r in entry_rows],
                    entry_pk,
                )
                rows_inserted += inserted

            # Load brief_summary with bu_mw calculation
            brief_table = next(
                (t for t in schema_def.tables if t.name == "brief_summary"), None
            )
            if brief_table:
                brief_rows = self._transform_brief_summary(
                    data, brief_table, job.entry_id
                )
                if brief_rows:
                    columns = list(brief_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        schema_def.schema_name,
                        "brief_summary",
                        columns,
                        [tuple(r[c] for c in columns) for r in brief_rows],
                        brief_table.primary_key,
                    )
                    rows_inserted += inserted

            # Load other categories
            for table in schema_def.tables:
                if table.name in ("entry", "brief_summary"):
                    continue

                category_rows = self._transform_category(data, table, job.entry_id)
                if category_rows:
                    columns = list(category_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        schema_def.schema_name,
                        table.name,
                        columns,
                        [tuple(r[c] for c in columns) for r in category_rows],
                        table.primary_key,
                    )
                    rows_inserted += inserted

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=rows_inserted,
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )

    def _transform_entry(self, data: dict[str, Any], entry_id: str) -> list[dict]:
        """Transform entry data."""
        rows = data.get("entry", [])
        if not rows:
            # Fallback: create minimal entry with both PK columns
            return [{"pdbid": entry_id, "id": entry_id.upper()}]

        result = []
        for row in rows:
            result.append(
                {
                    "pdbid": entry_id,
                    **{k: v for k, v in row.items() if v is not None},
                }
            )
        return result

    def _transform_brief_summary(
        self,
        data: dict[str, Any],
        table: TableDef,
        entry_id: str,
    ) -> list[dict]:
        """Transform brief_summary with bu_mw calculation.

        Adds bu_mw (biological unit molecular weight) to plus_fields.
        CIF version - no column name normalization.
        """
        rows = data.get("brief_summary", [])
        # No normalization for CIF
        result = transform_category(rows, table, entry_id, "pdbid", None)

        # Calculate bu_mw and add to plus_fields
        bu_mw = calculate_mw_for_bu(data)
        for row in result:
            # Merge bu_mw into existing plus_fields or create new
            existing_plus = row.get("plus_fields")
            if existing_plus:
                try:
                    plus_data = json.loads(existing_plus)
                except (json.JSONDecodeError, TypeError):
                    plus_data = {}
            else:
                plus_data = {}
            plus_data["bu_mw"] = bu_mw
            row["plus_fields"] = json.dumps(plus_data)

        return result

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        entry_id: str,
    ) -> list[dict]:
        """Transform a category's data.

        CIF files use plain column names (no bracket notation),
        so we don't normalize column names.
        """
        rows = data.get(table.name, [])
        # No normalization for CIF - pass None instead of normalize_column_name
        return transform_category(rows, table, entry_id, "pdbid", None)


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the pdbj pipeline (mmJSON version)."""
    pipeline = PdbjPipeline(settings, config, schema_def)
    return pipeline.run(limit)


def run_cif(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the pdbj-cif pipeline (CIF version)."""
    pipeline = PdbjCifPipeline(settings, config, schema_def)
    return pipeline.run(limit)
