#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Generate static JSON data for the SQL examples React page."""

import json
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "pdbj_examples_processed.json"
OUTPUT_FILE = (
    Path(__file__).parent.parent / "website" / "static" / "data" / "sqlExamples.json"
)

CATEGORY_ORDER = [
    "basic",
    "author",
    "date",
    "entity",
    "structure",
    "assembly",
    "xref",
    "chemical",
    "advanced",
]

CATEGORY_META = {
    "basic": {
        "label": "Basic Queries",
        "description": "Simple queries to retrieve PDB entries by ID, count, or pattern matching.",
    },
    "author": {
        "label": "Author & Citation",
        "description": "Search entries by author names, journal information, DOIs, and PubMed IDs.",
    },
    "date": {
        "label": "Date Search",
        "description": "Filter entries by release date, deposition date, or publication year.",
    },
    "entity": {
        "label": "Entity & Chain",
        "description": "Query polymer chains, chain types, residue counts, molecular weights, and sequences.",
    },
    "structure": {
        "label": "Structure",
        "description": "Experimental methods, resolution, unit cell parameters, keywords, and refinement.",
    },
    "assembly": {
        "label": "Biological Assembly",
        "description": "Biological assembly information including oligomeric state and generation details.",
    },
    "xref": {
        "label": "Cross-references",
        "description": "Find entries by UniProt, Gene Ontology, and EC number identifiers.",
    },
    "chemical": {
        "label": "Chemical Components",
        "description": "Search chemical components, ligands, and small molecules by various identifiers.",
    },
    "advanced": {
        "label": "Advanced",
        "description": "Complex queries combining multiple criteria or using advanced SQL features.",
    },
}

EXAMPLES_EN: dict[int, tuple[str, str]] = {
    5: ("List all PDB IDs", "Retrieves every PDB identifier from the summary table."),
    6: (
        "Count all PDB entries",
        "Returns the total number of PDB entries in the database.",
    ),
    7: (
        "Find PDB IDs starting with '1g'",
        "Uses `LIKE` with a wildcard pattern to match PDB IDs by prefix.",
    ),
    10: (
        "Get summary information for a specific entry",
        "Retrieves the PDB ID and structure title for entry 1gof.",
    ),
    68: (
        "Find PDB IDs consisting of all numeric characters",
        "Uses a regular expression (`~`) to match PDB IDs where all four characters are digits.",
    ),
    3: (
        "Find entries by depositor or primary citation author",
        "Joins `citation_author` and `audit_author` to find entries where a specific person appears as either a primary citation author or a depositor.",
    ),
    8: (
        "List all citation authors for a specific entry",
        "Retrieves all rows from the `citation_author` table for PDB entry 1gof.",
    ),
    9: (
        "Find entries by citation author name",
        "Uses the PostgreSQL array containment operator (`<@`) on the `citation_author` array column.",
    ),
    14: (
        "Find entries by multiple citation authors (AND)",
        "Uses `<@` with a multi-element array to find entries where both authors appear in the citation list.",
    ),
    15: (
        "Find entries by primary citation author",
        "Searches the `citation_author_pri` array column for primary citation authors only.",
    ),
    16: (
        "Find entries by citation year",
        "Uses the array overlap operator (`&&`) to match entries where the citation year array contains 2001.",
    ),
    17: (
        "Find entries by journal volume number",
        "Uses `&&` on the `citation_volume` array to find entries published in volume 555.",
    ),
    19: (
        "Find entries by year, volume, and experimental method",
        "Combines multiple array operators to filter by citation year, volume, and experimental method ID.",
    ),
    21: (
        "Get DOI for a specific entry's citation",
        "Retrieves the DOI from the `citation` table. Note the quoted column name (case-sensitive).",
    ),
    22: (
        "Get PubMed ID for a specific entry's citation",
        "Retrieves the PubMed ID from the `citation` table using a case-sensitive column name.",
    ),
    23: (
        "Get PubMed IDs for multiple entries",
        "Retrieves PubMed IDs for two entries, filtering out rows where DOI is null.",
    ),
    24: (
        "Get DOIs for entries matching a PDB ID prefix",
        "Uses `LIKE` to find all entries starting with '1i' and returns their DOIs.",
    ),
    58: (
        "Search entries by journal name",
        "Uses `ILIKE` (case-insensitive) on the `citation_journal` array to find entries by journal name.",
    ),
    67: (
        "Search entries by keyword in title with sorting",
        "Finds entries containing 'spliceosome' in the title, sorted by total residue count descending. Note: column aliases have been translated to English from the original Japanese.",
    ),
    72: (
        "Search by keyword in citation or structure title",
        "Joins `brief_summary` with `struct` to search for 'spike' in both citation and structure titles.",
    ),
    25: (
        "Find entries released after a specific date",
        "Filters by `release_date` using a date comparison.",
    ),
    26: (
        "Find entries by release date, deposition date, and PDB ID prefix",
        "Combines date range filters with a `LIKE` pattern match on the PDB ID.",
    ),
    62: (
        "Find kinase entries deposited in a specific year",
        "Finds entries with EC number '2.7' (kinases) deposited in 2016, joining `entity` with `struct_asym`.",
    ),
    65: (
        "Get release dates for specific PDB IDs",
        "Uses `IN` to retrieve release dates for a list of specific PDB IDs.",
    ),
    4: (
        "Find entries containing both synthetic and natural polymers",
        "Uses a CTE with `LEFT JOIN` across three source tables to identify entries with both synthetic and non-synthetic polymer entities.",
    ),
    11: (
        "Find entries with the highest molecule copy counts",
        "Retrieves the top 5 polymer entities by `pdbx_number_of_molecules` using `ORDER BY ... DESC LIMIT`.",
    ),
    12: (
        "Find entries by EC number with chain IDs",
        "Uses `LEFT JOIN` between `entity` and `struct_asym` to get chain identifiers for entities with a specific EC number.",
    ),
    27: (
        "Find entries containing D-polypeptide chains",
        "Uses the array containment operator (`<@`) to find entries where `chain_type_ids` contains type 1.",
    ),
    28: (
        "Find entries containing both D- and L-polypeptide chains",
        "Uses `<@` with `{1,2}` to require both chain types are present.",
    ),
    29: (
        "Find entries containing D- or L-polypeptide chains",
        "Uses the array overlap operator (`&&`) to match entries with either chain type.",
    ),
    30: (
        "Find entries without DNA chains",
        "Uses `NOT` with `&&` to exclude entries whose `chain_type_ids` contains type 3 (DNA).",
    ),
    31: (
        "Exclude entries containing both DNA and RNA",
        "Uses `NOT ... &&` to exclude entries with both chain type 3 (DNA) and 4 (RNA).",
    ),
    32: (
        "Find entries containing only D-polypeptide chains",
        "Combines `<@` (must contain type 1) with `NOT ... &&` (must not contain any other types).",
    ),
    35: (
        "Calculate total molecular weight per entry",
        "Computes `SUM(pdbx_number_of_molecules * formula_weight)` for polymer entities, grouped by PDB ID.",
    ),
    36: (
        "Get entry metadata with unit cell and molecular weight",
        "Joins `cell`, `struct`, `struct_keywords`, and `entity` for a comprehensive summary with unit cell parameters.",
    ),
    39: (
        "Count residues in a specific entry",
        "Uses a CTE to count residues per entity from `entity_poly_seq`, then multiplies by molecule count.",
    ),
    41: (
        "Map entity IDs to chain IDs (label/auth)",
        "Joins `entity_poly` with `pdbx_poly_seq_scheme` to map entity IDs to both systematic and author chain IDs.",
    ),
    43: (
        "Get detailed chain mapping for specific entities",
        "Uses a CTE to build a chain mapping from `struct_asym` with non-polymer scheme information.",
    ),
    46: (
        "List large structure entries with polymer chain counts",
        "Joins `pdbx_database_status` with `entity` to count polymer chains in large structures.",
    ),
    48: (
        "List large structure entries with total molecular weight",
        "Sums `formula_weight` for polymer entities in large structures, sorted by weight descending.",
    ),
    59: (
        "Search entries by amino acid sequence and organism",
        "Finds entries containing a specific peptide sequence from a particular organism using `LIKE`.",
    ),
    61: (
        "Find entries with both peptide chains and non-water ligands",
        "Joins `brief_summary`, `entity`, and `pdbx_nonpoly_scheme` to find entries with polymer and non-polymer components.",
    ),
    63: (
        "Find entries by entity name with chain IDs",
        "Uses a CTE and `ILIKE` to find entities named 'phospholipase C', then joins to get chain IDs.",
    ),
    64: (
        "Find entries by entity name and organism",
        "Extends the entity name search with a join to filter by source organism (rat).",
    ),
    66: (
        "Get chain details and entity types for a specific entry",
        "Uses a CTE to retrieve all entities (polymer and non-polymer) with chain IDs and entity types.",
    ),
    1: (
        "Count entries per keyword (case-insensitive)",
        "Uses `LOWER()` and `GROUP BY` to aggregate keywords, sorted by frequency with `ORDER BY COUNT(...) DESC`.",
    ),
    18: (
        "Find entries by experimental method",
        "Uses `ANY()` on `exptl_method_ids` to find entries by solution NMR (method ID 6).",
    ),
    20: (
        "Get crystal density for a specific entry",
        "Retrieves the solvent density percentage from the `exptl_crystal` table.",
    ),
    33: (
        "Get experimental method, unit cell, and crystal density",
        "Joins `exptl`, `cell`, and `exptl_crystal` to retrieve experimental details for specific entries.",
    ),
    34: (
        "Find entries with resolution better than 2.0 angstroms",
        "Filters the `refine` table by `ls_d_res_high <= 2.0`. Lower values = higher resolution.",
    ),
    51: (
        "Count entries per keyword (top N)",
        "Same approach as keyword counting but with `LIMIT` to restrict output to top results.",
    ),
    73: (
        "Get resolution and R-free values",
        "Retrieves resolution and R-free refinement statistics with quoted column names.",
    ),
    37: (
        "List biological assembly information for all entries",
        "Joins `pdbx_struct_assembly` with `pdbx_struct_assembly_gen` to get oligomeric state and chain lists.",
    ),
    38: (
        "Get biological assembly for a specific entry",
        "Same assembly join as above, filtered to a single PDB entry (1nov).",
    ),
    47: (
        "Get assembly generation details for a specific entry",
        "Retrieves assembly chain lists and operator expressions for entry 1bbt.",
    ),
    2: (
        "Find entries by Gene Ontology biological process",
        "Queries `gene_ontology_pdbmlplus` to find entries annotated with a specific GO process.",
    ),
    40: (
        "Map PDB entries to UniProt IDs",
        "Queries `struct_ref` to build PDB-to-UniProt mapping using `DISTINCT`.",
    ),
    70: (
        "Find entries by UniProt accession ID",
        "Filters `struct_ref` by UniProt database name and a specific accession ID.",
    ),
    71: (
        "Find entries by UniProt database code",
        "Uses `db_code` (e.g., 'CDK3_HUMAN') instead of accession number.",
    ),
    13: (
        "Find entries containing a specific ligand",
        "Searches `chem_comp` for entries containing heme (HEM).",
    ),
    42: (
        "Find non-polymer entities missing from pdbx_nonpoly_scheme",
        "Uses `LEFT JOIN` and `IS NULL` to find non-polymer entities without corresponding scheme entries.",
    ),
    44: (
        "Get non-polymer component details with chain mapping",
        "Extends chain mapping CTE to include non-polymer component IDs and sequence numbers.",
    ),
    55: (
        "Find entries containing a compound by InChIKey",
        "Cross-schema join between `pdbj.chem_comp` and `cc.pdbx_chem_comp_descriptor` to search by InChIKey.",
    ),
    56: (
        "Find entries by CSD compound ID",
        "Multi-schema join across `pdbj`, `ccmodel`, and cross-references to find entries by CSD ID.",
    ),
    57: (
        "Find antibody entries with low molecular weight",
        "Joins `pdbx_molecule_features` with `prd.pdbx_reference_molecule` for antibodies <= 1000 Da.",
    ),
    60: (
        "List all chemical components with names, formulas, and InChIKeys",
        "Queries the `cc` schema joining `chem_comp` with `pdbx_chem_comp_descriptor` (InChIKey type).",
    ),
    45: (
        "Find large structure entries incompatible with PDB format",
        "Queries `pdbx_database_status` for entries where `pdb_format_compatible='N'`.",
    ),
}


def main():
    data = json.loads(INPUT_FILE.read_text())
    available = [ex for ex in data if ex["available"]]

    categories = []
    for cat_key in CATEGORY_ORDER:
        meta = CATEGORY_META[cat_key]
        examples = []
        for ex in available:
            if ex["category"] != cat_key:
                continue
            num = ex["number"]
            if num not in EXAMPLES_EN:
                continue
            title, description = EXAMPLES_EN[num]
            examples.append(
                {
                    "id": num,
                    "title": title,
                    "description": description,
                    "sql": ex["sql_fixed"],
                }
            )
        if examples:
            categories.append(
                {
                    "id": cat_key,
                    "label": meta["label"],
                    "description": meta["description"],
                    "count": len(examples),
                    "examples": examples,
                }
            )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(categories, ensure_ascii=False, indent=2))
    print(
        f"Generated {OUTPUT_FILE} ({sum(c['count'] for c in categories)} examples in {len(categories)} categories)"
    )


if __name__ == "__main__":
    main()
