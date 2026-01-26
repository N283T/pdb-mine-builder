"""PRD (BIRD) pipeline - Biologically Interesting Reference Dictionary."""

import gzip
import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, bulk_upsert
from mine2.parsers.mmjson import get_rows, load_mmjson, normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


class PrdPipeline(BasePipeline):
    """Pipeline for loading BIRD (PRD) data.

    PRD files contain TWO data blocks:
    - data_PRD_XXXXXX: Contains pdbx_reference_* categories
    - data_PRDCC_XXXXXX: Contains chem_comp_* categories
    """

    name = "prd"
    file_pattern = "*.json.gz"

    # Tables that come from the PRDCC data block
    PRDCC_TABLES = {
        "chem_comp",
        "chem_comp_atom",
        "chem_comp_bond",
        "pdbx_chem_comp_descriptor",
        "pdbx_chem_comp_identifier",
    }

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract PRD ID from filename.

        Handles filenames like: PRD_000001.json.gz -> PRD_000001
        """
        name = filepath.name
        if name.endswith(".json.gz"):
            name = name[:-8]
        return name

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single PRD entry."""
        try:
            # Load raw JSON (PRD files have two data blocks, can't use load_mmjson_file)
            if str(job.filepath).endswith(".json.gz"):
                with gzip.open(job.filepath, "rt", encoding="utf-8") as f:
                    raw_data = load_mmjson(f.read())
            else:
                with open(job.filepath, encoding="utf-8") as f:
                    raw_data = load_mmjson(f.read())

            rows_inserted = 0

            # PRD files have two data blocks:
            # - data_PRD_XXXXXX (pdbx_reference_* categories)
            # - data_PRDCC_XXXXXX (chem_comp_* categories)
            prd_data = raw_data.get(f"data_{job.entry_id}", {})
            prdcc_id = job.entry_id.replace("PRD_", "PRDCC_")
            prdcc_data = raw_data.get(f"data_{prdcc_id}", {})

            # Generate and load brief_summary from pdbx_reference_molecule
            brief_rows = self._generate_brief_summary(prd_data, job.entry_id)
            if brief_rows:
                columns = list(brief_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "brief_summary",
                    columns,
                    [tuple(r[c] for c in columns) for r in brief_rows],
                    ["prd_id"],
                )
                rows_inserted += inserted

            # Load all tables from schema
            for table in schema_def.tables:
                if table.name == "brief_summary":
                    continue  # Already handled

                # Determine which data block to use
                if table.name in self.PRDCC_TABLES:
                    data = prdcc_data
                else:
                    data = prd_data

                category_rows = self._transform_category(
                    data, table, job.entry_id, schema_def.primary_key
                )
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

    def _generate_brief_summary(self, data: dict[str, Any], prd_id: str) -> list[dict]:
        """Generate brief_summary from pdbx_reference_molecule data."""
        rows = get_rows(data, "pdbx_reference_molecule")
        if not rows:
            return []

        result = []
        for row in rows:
            result.append(
                {
                    "prd_id": prd_id,
                    "name": row.get("name"),
                    "formula": row.get("formula"),
                    "description": row.get("description"),
                }
            )
        return result

    def _transform_category(
        self,
        data: dict[str, Any],
        table: Any,
        prd_id: str,
        pk_col: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = get_rows(data, table.name)
        return transform_category(rows, table, prd_id, pk_col, normalize_column_name)


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the prd pipeline."""
    pipeline = PrdPipeline(settings, config, schema_def)
    return pipeline.run(limit)
