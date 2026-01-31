"""IHM pipeline - Integrative Hybrid Methods data loader.

IHM pipeline is similar to pdbj but with key differences:
1. Forces exptl_method to "IHM" (method id 16)
2. Adds _hash_asym_id_list SHA256 hash for pdbx_struct_assembly_gen
3. Calculates biological unit molecular weight (bu_mw) for plus_fields

Uses mmJSON input (noatom + plus files) like the pdbj pipeline.
"""

import json
import logging
import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.cif import parse_mmjson_file
from mine2.parsers.mmjson import (
    clean_array,
    merge_data,
    mmjson_at,
    mmjson_get,
    normalize_column_name,
    remove_null,
)
from mine2.pipelines.base import BasePipeline, transform_category
from mine2.utils.assembly import (
    CHAIN_TYPE_MAPPING,
    EXPTL_METHOD_MAPPING,
    calculate_mw_for_bu,
    expand_oper_expression,
    hex_sha256,
)

console = Console()


# Local aliases for backward compatibility with existing tests.
# TODO: Remove once tests import directly from mine2.utils.assembly
_hex_sha256 = hex_sha256
_calculate_mw_for_bu = calculate_mw_for_bu
_expand_oper_expression = expand_oper_expression


def _gen_docid(entry_id: str) -> int:
    """Generate numeric docid from entry ID.

    PDB IDs are 4-character alphanumeric codes (e.g., "1abc").
    Convert to numeric using base-36 encoding.
    """
    entry_id = entry_id.lower()
    try:
        return int(entry_id, 36)
    except ValueError:
        return 0


class IhmPipeline(BasePipeline):
    """Pipeline for loading IHM structure data."""

    name = "ihm"
    file_pattern = "*-noatom.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract entry ID from filepath.

        Handles filenames like: 100d-noatom.json.gz -> 100d
        """
        name = filepath.name
        if name.endswith(".json.gz"):
            name = name[:-8]
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
        for filepath in data_dir.rglob(self.file_pattern):
            entry_id = self.extract_entry_id(filepath)

            # Look for plus file: {entry_id}-plus.json.gz
            plus_path = None
            if plus_dir:
                candidate = plus_dir / f"{entry_id}-plus.json.gz"
                if candidate.exists():
                    plus_path = candidate

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
        """Process a single IHM entry."""
        try:
            # Load main data
            data = parse_mmjson_file(job.filepath)

            # Merge with plus data if available
            plus_path = job.extra.get("plus_path")
            if plus_path:
                plus_data = parse_mmjson_file(plus_path)
                data = merge_data(data, plus_data)

            # Add hash columns to pdbx_struct_assembly_gen (avoid B-tree index limit)
            if "pdbx_struct_assembly_gen" in data:
                for row in data["pdbx_struct_assembly_gen"]:
                    row["_hash_asym_id_list"] = _hex_sha256(row.get("asym_id_list", ""))
                    row["_hash_oper_expression"] = _hex_sha256(
                        row.get("oper_expression", "")
                    )

            # Transform and load
            rows_inserted = 0

            # Get entry table definition
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

            # Load brief_summary
            brief_rows = self._transform_brief_summary(data, job.entry_id)
            if brief_rows:
                brief_table = next(
                    (t for t in schema_def.tables if t.name == "brief_summary"), None
                )
                if brief_table:
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
        self, data: dict[str, Any], entry_id: str
    ) -> list[dict]:
        """Transform data to brief_summary format.

        IHM brief_summary is similar to pdbj but:
        - Forces exptl_method to ["IHM"] with method_id [16]
        - Includes bu_mw calculation in plus_fields
        """
        # Get sequences for various calculations
        entity_poly = data.get("entity_poly", [])
        sequences = [
            row.get("pdbx_seq_one_letter_code_can", "")
            for row in entity_poly
            if row.get("pdbx_seq_one_letter_code_can")
        ]

        # Basic IDs
        result: dict[str, Any] = {
            "pdbid": entry_id,
            "docid": _gen_docid(entry_id),
        }

        # Dates
        pdbx_database_status = data.get("pdbx_database_status", [])
        if pdbx_database_status:
            result["deposition_date"] = pdbx_database_status[0].get(
                "recvd_initial_deposition_date"
            )

        pdbx_audit_revision_history = data.get("pdbx_audit_revision_history", [])
        if pdbx_audit_revision_history:
            revision_dates = [
                row.get("revision_date")
                for row in pdbx_audit_revision_history
                if row.get("revision_date")
            ]
            if revision_dates:
                result["release_date"] = revision_dates[0]
                result["modification_date"] = revision_dates[-1]

        # Authors
        audit_author = data.get("audit_author", [])
        if audit_author:
            result["deposit_author"] = [
                row.get("name") for row in audit_author if row.get("name")
            ]

        citation_author = data.get("citation_author", [])
        if citation_author:
            result["citation_author"] = [
                row.get("name") for row in citation_author if row.get("name")
            ]
            result["citation_author_pri"] = mmjson_at(
                citation_author, "name", "citation_id", "primary"
            )

        # Citations
        citation = data.get("citation", [])
        if citation:
            result["citation_title"] = remove_null(
                [row.get("title") for row in citation]
            )
            result["citation_journal"] = remove_null(
                [row.get("journal_abbrev") for row in citation]
            )
            result["citation_year"] = remove_null([row.get("year") for row in citation])
            result["citation_volume"] = remove_null(
                [row.get("journal_volume") for row in citation]
            )

            result["citation_title_pri"] = mmjson_at(citation, "title", "id", "primary")
            result["citation_journal_pri"] = mmjson_at(
                citation, "journal_abbrev", "id", "primary"
            )
            result["citation_year_pri"] = mmjson_at(citation, "year", "id", "primary")
            result["citation_volume_pri"] = mmjson_at(
                citation, "journal_volume", "id", "primary"
            )

            # Fallback to first values if no primary
            if not result.get("citation_title_pri"):
                result["citation_title_pri"] = (
                    result["citation_title"][0] if result["citation_title"] else None
                )
                result["citation_journal_pri"] = (
                    result["citation_journal"][0]
                    if result["citation_journal"]
                    else None
                )
                result["citation_year_pri"] = (
                    result["citation_year"][0] if result["citation_year"] else None
                )
                result["citation_volume_pri"] = (
                    result["citation_volume"][0] if result["citation_volume"] else None
                )
            else:
                # mmjson_at returns list, get first element
                result["citation_title_pri"] = (
                    result["citation_title_pri"][0]
                    if result["citation_title_pri"]
                    else None
                )
                result["citation_journal_pri"] = (
                    result["citation_journal_pri"][0]
                    if result["citation_journal_pri"]
                    else None
                )
                result["citation_year_pri"] = (
                    result["citation_year_pri"][0]
                    if result["citation_year_pri"]
                    else None
                )
                result["citation_volume_pri"] = (
                    result["citation_volume_pri"][0]
                    if result["citation_volume_pri"]
                    else None
                )

            result["db_pubmed"] = [
                str(row.get("pdbx_database_id_PubMed"))
                for row in citation
                if row.get("pdbx_database_id_PubMed")
            ]
            result["db_doi"] = remove_null(
                [row.get("pdbx_database_id_DOI") for row in citation]
            )

        # Chain info
        if entity_poly:
            chain_types = clean_array(
                [row.get("type") for row in entity_poly if row.get("type")]
            )
            result["chain_type"] = chain_types
            result["chain_type_ids"] = clean_array(
                [
                    CHAIN_TYPE_MAPPING.get(t)
                    for t in chain_types
                    if t in CHAIN_TYPE_MAPPING
                ]
            )

        # Chain count
        entity = data.get("entity", [])
        polymer_counts = mmjson_at(
            entity, "pdbx_number_of_molecules", "type", "polymer"
        )
        if polymer_counts:
            result["chain_number"] = sum(int(c) for c in polymer_counts if c)
        else:
            result["chain_number"] = 0

        # Chain lengths
        result["chain_length"] = [
            len(seq.replace("\n", "").replace(" ", "")) for seq in sequences
        ]

        # Descriptor and title
        if entity:
            descriptions = [
                row.get("pdbx_description")
                for row in entity
                if row.get("pdbx_description")
            ]
            result["pdbx_descriptor"] = ", ".join(clean_array(descriptions))

        struct = data.get("struct", [])
        if struct:
            result["struct_title"] = struct[0].get("title")

        # Ligands
        chem_comp = data.get("chem_comp", [])
        if chem_comp:
            # Filter out standard linking types
            linking_types = {
                "peptide linking",
                "L-peptide linking",
                "DNA linking",
                "RNA linking",
            }
            lig_indices = [
                i
                for i, row in enumerate(chem_comp)
                if row.get("type") not in linking_types
            ]
            lig_info: list[str] = []
            for i in lig_indices:
                if chem_comp[i].get("name"):
                    lig_info.append(chem_comp[i]["name"])
                if chem_comp[i].get("pdbx_synonyms"):
                    lig_info.append(chem_comp[i]["pdbx_synonyms"])
                if chem_comp[i].get("id"):
                    lig_info.append(chem_comp[i]["id"])
            result["ligand"] = clean_array(lig_info)

        # IHM-specific: always "IHM" method
        result["exptl_method"] = ["IHM"]
        result["exptl_method_ids"] = [EXPTL_METHOD_MAPPING["IHM"]]

        # Species info
        entity_src_gen = data.get("entity_src_gen", [])
        entity_src_nat = data.get("entity_src_nat", [])
        pdbx_entity_src_syn = data.get("pdbx_entity_src_syn", [])

        species_parts: list[str] = []
        species_parts.extend(
            mmjson_get(entity_src_gen, "pdbx_gene_src_scientific_name") or []
        )
        species_parts.extend(mmjson_get(entity_src_gen, "gene_src_common_name") or [])
        species_parts.extend(mmjson_get(entity_src_nat, "common_name") or [])
        species_parts.extend(
            mmjson_get(entity_src_nat, "pdbx_organism_scientific") or []
        )
        species_parts.extend(
            mmjson_get(pdbx_entity_src_syn, "organism_common_name") or []
        )
        species_parts.extend(
            mmjson_get(pdbx_entity_src_syn, "organism_scientific") or []
        )
        result["biol_species"] = " ".join(clean_array(species_parts)) or None

        result["host_species"] = mmjson_get(
            entity_src_gen, "pdbx_host_org_scientific_name", 0
        )

        # Database references
        result["db_ec_number"] = clean_array(mmjson_get(entity, "pdbx_ec") or [])

        gene_ontology = data.get("gene_ontology_pdbmlplus", [])
        result["db_goid"] = clean_array(mmjson_get(gene_ontology, "goid") or [])

        struct_ref = data.get("struct_ref", [])
        struct_ref_pdbmlplus = data.get("struct_ref_pdbmlplus", [])
        result["db_uniprot"] = clean_array(
            mmjson_at(struct_ref, "pdbx_db_accession", "db_name", "UNP")
            + mmjson_at(
                struct_ref_pdbmlplus, "pdbx_db_accession", "db_name", "SIFTS_UNP"
            )
            + mmjson_at(struct_ref, "db_code", "db_name", "UNP")
        )

        result["db_genbank"] = clean_array(
            mmjson_at(struct_ref, "db_code", "db_name", "GB")
            + mmjson_at(struct_ref, "pdbx_db_accession", "db_name", "GB")
        )
        result["db_embl"] = clean_array(
            mmjson_at(struct_ref, "db_code", "db_name", "EMBL")
            + mmjson_at(struct_ref, "pdbx_db_accession", "db_name", "EMBL")
        )
        result["db_pir"] = clean_array(
            mmjson_at(struct_ref, "db_code", "db_name", "PIR")
            + mmjson_at(struct_ref, "pdbx_db_accession", "db_name", "PIR")
        )

        pdbx_database_related = data.get("pdbx_database_related", [])
        result["db_emdb"] = clean_array(
            mmjson_at(pdbx_database_related, "db_id", "db_name", "EMDB")
        )
        result["pdb_related"] = clean_array(
            mmjson_at(pdbx_database_related, "db_id", "db_name", "PDB")
        )

        # Sequence and keywords
        result["aaseq"] = "".join(sequences)
        result["update_date"] = None

        result["db_pfam"] = clean_array(
            mmjson_at(struct_ref_pdbmlplus, "pdbx_db_accession", "db_name", "Pfam")
        )

        # Plus fields with bu_mw
        result["plus_fields"] = json.dumps({"bu_mw": _calculate_mw_for_bu(data)})

        # Keywords - include pdb_XXXXXXXX format for 8-char IDs
        result["keywords"] = [f"pdb_{entry_id.rjust(8, '0')}"]

        return [result]

    def _transform_category(
        self,
        data: dict[str, Any],
        table: TableDef,
        entry_id: str,
    ) -> list[dict]:
        """Transform a category's data."""
        rows = data.get(table.name, [])
        return transform_category(rows, table, entry_id, "pdbid", normalize_column_name)


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
    logger: logging.Logger | None = None,
) -> list[LoaderResult]:
    """Run the IHM pipeline."""
    pipeline = IhmPipeline(settings, config, schema_def)
    return pipeline.run(limit, logger=logger)
