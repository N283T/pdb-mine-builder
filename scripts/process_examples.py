#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Process raw PDBj examples: fix schema prefixes, filter unavailable tables, categorize."""

import json
import re
from pathlib import Path

RAW_FILE = Path(__file__).parent / "pdbj_examples_raw.json"
OUTPUT_FILE = Path(__file__).parent / "pdbj_examples_processed.json"

# Tables available in pdb-mine-builder (pdbj schema only for these examples)
# The examples mostly use pdbj schema tables
PDBJ_TABLES = {
    "align_pdbjplus", "atom_sites", "atom_sites_footnote", "atom_type",
    "audit", "audit_author", "audit_conform",
    "brief_summary", "cell", "cell_measurement",
    "chem_comp", "chem_comp_atom", "chem_comp_bond", "chem_link",
    "citation", "citation_author", "citation_editor", "citation_pdbmlplus",
    "database_2", "database_PDB_caveat", "database_PDB_matrix", "database_PDB_tvect",
    "diffrn", "diffrn_detector", "diffrn_measurement", "diffrn_radiation",
    "diffrn_radiation_wavelength", "diffrn_reflns", "diffrn_source",
    "entity", "entity_keywords", "entity_name_com", "entity_name_sys",
    "entity_poly", "entity_poly_seq", "entity_src_gen", "entity_src_nat",
    "entry", "exptl", "exptl_crystal", "exptl_crystal_grow",
    "gene_ontology_pdbmlplus",
    "pdbx_entity_nonpoly", "pdbx_entity_src_syn",
    "pdbx_nonpoly_scheme", "pdbx_poly_seq_scheme",
    "pdbx_struct_assembly", "pdbx_struct_assembly_gen", "pdbx_struct_assembly_prop",
    "pdbx_database_status", "pdbx_database_related",
    "pdbx_sifts_unp_segments", "pdbx_sifts_xref_db", "pdbx_sifts_xref_db_segments",
    "refine", "refine_hist", "refine_ls_shell",
    "reflns", "reflns_shell",
    "software", "space_group",
    "struct", "struct_asym", "struct_conn", "struct_keywords",
    "struct_ref", "struct_ref_seq", "struct_ref_seq_dif",
}

CC_TABLES = {
    "brief_summary", "chem_comp", "chem_comp_atom", "chem_comp_bond",
    "pdbx_chem_comp_descriptor", "pdbx_chem_comp_identifier",
    "pdbx_chem_comp_related", "pdbx_chem_comp_synonyms",
}

# Tables that exist in sifts.* namespace (not available in pdb-mine-builder)
UNAVAILABLE_TABLES = {"sifts.pdb_chain_go", "sifts.pdb_chain_uniprot"}

# Category assignments based on content
CATEGORIES = {
    "basic": "Basic Queries",
    "author": "Author & Citation Search",
    "date": "Date-based Search",
    "entity": "Entity & Chain Information",
    "structure": "Structural Properties",
    "assembly": "Biological Assembly",
    "xref": "Cross-references (UniProt, GO, EC)",
    "chemical": "Chemical Components",
    "advanced": "Advanced Queries",
}


def categorize(num: int, title: str, sql: str) -> str:
    """Assign a category based on content."""
    sql_lower = sql.lower()
    title_lower = title.lower()

    # Check for cross-references
    if any(kw in sql_lower for kw in ["uniprot", "unp", "go_id", "gene_ontology", "ec_number", "db_uniprot", "db_goid", "db_ec_number"]):
        return "xref"
    if any(kw in sql_lower for kw in ["struct_ref"]) and "db_name" in sql_lower:
        return "xref"

    # Chemical components
    if any(kw in sql_lower for kw in ["cc.", "chem_comp", "inchikey", "formula_weight"]) and "entity" not in sql_lower:
        return "chemical"
    if any(kw in title_lower for kw in ["chemical component", "hem", "化合物", "inchikey"]):
        return "chemical"

    # Author / citation
    if any(kw in sql_lower for kw in ["citation_author", "audit_author", "citation_title", "citation_journal",
                                       "pubmed", "doi", "db_pubmed", "db_doi"]):
        return "author"
    if "著者" in title or "文献" in title or "雑誌" in title:
        return "author"

    # Date-based
    if any(kw in sql_lower for kw in ["release_date", "deposition_date", "modification_date"]):
        return "date"
    if "公開日" in title or "登録日" in title or "日" in title and "年" in title:
        return "date"

    # Biological assembly
    if "assembly" in sql_lower or "生物学的単位" in title:
        return "assembly"

    # Entity / chain
    if any(kw in sql_lower for kw in ["entity", "chain_type", "struct_asym", "poly_seq"]):
        return "entity"
    if any(kw in title_lower for kw in ["entity", "chain", "鎖", "高分子", "ポリペプチド", "残基"]):
        return "entity"

    # Structural properties
    if any(kw in sql_lower for kw in ["cell.", "refine", "exptl", "resolution", "density", "space_group",
                                       "struct_keywords", "struct.", "pdbx_descriptor"]):
        return "structure"
    if any(kw in title_lower for kw in ["分解能", "実験手法", "キーワード", "格子", "密度"]):
        return "structure"

    # Basic
    if num in (5, 6, 7, 10) or sql_lower.strip().startswith("select pdbid from brief_summary"):
        return "basic"

    return "advanced"


def extract_tables_from_sql(sql: str) -> set[str]:
    """Extract table names referenced in SQL."""
    tables = set()
    # Match FROM/JOIN table_name patterns
    # Handle: FROM table, JOIN table ON, LEFT JOIN table ON
    pattern = r'(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)'
    for match in re.finditer(pattern, sql, re.IGNORECASE):
        table = match.group(1)
        # Skip aliases and SQL keywords
        if table.upper() in ("SELECT", "WHERE", "ON", "AND", "OR", "AS", "NOT", "NULL", "LEFT", "RIGHT", "INNER"):
            continue
        tables.add(table)
    return tables


def add_schema_prefix(sql: str) -> str:
    """Add pdbj. prefix to table names that don't have a schema prefix."""
    # Tables that should get pdbj. prefix
    result = sql

    # Find all table references after FROM/JOIN
    def replace_table(match):
        keyword = match.group(1)  # FROM/JOIN
        whitespace = match.group(2)
        table = match.group(3)

        # Skip if already has schema prefix
        if "." in table:
            return f"{keyword}{whitespace}{table}"

        # Skip CTE references and aliases
        if table.upper() in ("SELECT", "WHERE", "ON", "AND", "OR", "NOT"):
            return f"{keyword}{whitespace}{table}"

        # Check if it's a known pdbj table
        if table in PDBJ_TABLES:
            return f"{keyword}{whitespace}pdbj.{table}"

        return f"{keyword}{whitespace}{table}"

    result = re.sub(
        r'((?:FROM|JOIN))\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)',
        lambda m: replace_table_match(m),
        result,
        flags=re.IGNORECASE,
    )

    return result


def replace_table_match(match):
    keyword = match.group(1)
    table = match.group(2)

    if "." in table:
        return f"{keyword} {table}"

    if table in PDBJ_TABLES:
        return f"{keyword} pdbj.{table}"

    return f"{keyword} {table}"


def check_table_availability(sql: str) -> tuple[bool, list[str]]:
    """Check if all tables in SQL are available. Returns (available, missing_tables)."""
    tables = extract_tables_from_sql(sql)
    missing = []

    for table in tables:
        if "." in table:
            schema, name = table.split(".", 1)
            if schema == "sifts":
                missing.append(table)
            # Other schemas are OK
        else:
            # Unqualified table - check if it's a known pdbj table
            if table not in PDBJ_TABLES and table.lower() not in {"pdbent", "slen", "s"}:
                # Could be a CTE alias - skip
                pass

    return len(missing) == 0, missing


def translate_title(title: str) -> str:
    """Best-effort translation hint (will need manual review)."""
    # Keep as-is for now; the actual English titles will be written manually
    return title


def main():
    raw = json.loads(RAW_FILE.read_text())
    processed = []

    for ex in raw:
        num = ex["number"]
        sql = ex["sql"]
        title = ex["title"]

        # Check table availability
        available, missing = check_table_availability(sql)

        # Add schema prefix
        fixed_sql = add_schema_prefix(sql)

        # Categorize
        category = categorize(num, title, sql)

        processed.append({
            "number": num,
            "title_ja": title,
            "sql_original": sql,
            "sql_fixed": fixed_sql,
            "category": category,
            "category_label": CATEGORIES[category],
            "available": available,
            "missing_tables": missing,
        })

    # Summary
    avail_count = sum(1 for p in processed if p["available"])
    print(f"Total: {len(processed)}")
    print(f"Available: {avail_count}")
    print(f"Unavailable: {len(processed) - avail_count}")
    print()

    # Show unavailable
    for p in processed:
        if not p["available"]:
            print(f"  SKIP ex{p['number']:03d}: missing {p['missing_tables']} - {p['title_ja'][:50]}")
    print()

    # Category breakdown
    from collections import Counter
    cats = Counter(p["category"] for p in processed if p["available"])
    print("Category breakdown (available only):")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {CATEGORIES[cat]}: {count}")

    OUTPUT_FILE.write_text(json.dumps(processed, ensure_ascii=False, indent=2))
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
