#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Generate SQL query examples documentation from processed JSON data."""

import json
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "pdbj_examples_processed.json"
OUTPUT_FILE = Path(__file__).parent.parent / "website" / "docs" / "examples" / "sql-examples.md"

# Category order
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

CATEGORY_LABELS = {
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

CATEGORY_DESCRIPTIONS = {
    "basic": "Simple queries to retrieve PDB entries by ID, count, or pattern matching.",
    "author": "Search entries by author names, journal information, DOIs, and PubMed IDs.",
    "date": "Filter entries by release date, deposition date, or publication year.",
    "entity": "Query polymer chains, chain types, residue counts, molecular weights, and sequence information.",
    "structure": "Look up experimental methods, resolution, unit cell parameters, keywords, and refinement statistics.",
    "assembly": "Retrieve biological assembly information including oligomeric state and generation details.",
    "xref": "Find entries by cross-reference identifiers such as UniProt, Gene Ontology, and EC numbers.",
    "chemical": "Search chemical components, ligands, and small molecules by various identifiers.",
    "advanced": "Complex queries combining multiple criteria or using advanced SQL features.",
}

# English titles and descriptions for each example (keyed by original number)
EXAMPLES_EN: dict[int, tuple[str, str]] = {
    # Basic
    5: (
        "List all PDB IDs",
        "Retrieves every PDB identifier from the summary table.",
    ),
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

    # Author & Citation
    3: (
        "Find entries by depositor or primary citation author",
        "Joins `citation_author` and `audit_author` to find entries where a specific person appears as either a primary citation author or a depositor. Uses `DISTINCT` to eliminate duplicates.",
    ),
    8: (
        "List all citation authors for a specific entry",
        "Retrieves all rows from the `citation_author` table for PDB entry 1gof.",
    ),
    9: (
        "Find entries by citation author name",
        "Uses the PostgreSQL array containment operator (`<@`) on the `citation_author` array column in `brief_summary`.",
    ),
    14: (
        "Find entries by multiple citation authors (AND)",
        "Uses `<@` with a multi-element array to find entries where both authors appear in the citation author list.",
    ),
    15: (
        "Find entries by primary citation author",
        "Searches the `citation_author_pri` array column, which contains only primary citation authors.",
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
        "Combines multiple array operators to filter by citation year, volume, and experimental method ID simultaneously.",
    ),
    21: (
        "Get DOI for a specific entry's citation",
        "Retrieves the DOI from the `citation` table. Note the quoted column name `\"pdbx_database_id_DOI\"` (case-sensitive).",
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
        "Uses `ILIKE` (case-insensitive) on the `citation_journal` array cast to text to find entries published in journals containing 'molecular cell'.",
    ),
    67: (
        "Search entries by keyword in title with sorting",
        "Finds entries whose structure title contains 'spliceosome' and sorts by total residue count in descending order. Demonstrates `ILIKE` and `ORDER BY` on a computed column.",
    ),
    72: (
        "Search by keyword in citation or structure title",
        "Joins `brief_summary` with `struct` to search for 'spike' in both citation titles and structure titles using `ILIKE`.",
    ),

    # Date-based
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
        "Finds entries with EC number starting with '2.7' (kinases) deposited in 2016. Joins `entity` with `struct_asym` and filters by `deposition_date`.",
    ),
    65: (
        "Get release dates for specific PDB IDs",
        "Uses `IN` to retrieve release dates for a list of specific PDB IDs.",
    ),

    # Entity & Chain
    4: (
        "Find entries containing both synthetic and natural polymers",
        "Uses a CTE with `LEFT JOIN` across three source tables (`pdbx_entity_src_syn`, `entity_src_nat`, `entity_src_gen`) to identify entries with both synthetic and non-synthetic polymer entities.",
    ),
    11: (
        "Find entries with the highest molecule copy counts",
        "Retrieves the top 5 polymer entities by `pdbx_number_of_molecules`, sorted in descending order using `ORDER BY ... DESC LIMIT`.",
    ),
    12: (
        "Find entries by EC number with chain IDs",
        "Uses `LEFT JOIN` between `entity` and `struct_asym` to get chain identifiers for entities with EC number 1.1.1.1.",
    ),
    27: (
        "Find entries containing D-polypeptide chains",
        "Uses the array containment operator (`<@`) to find entries where `chain_type_ids` contains type 1 (polypeptide(D)).",
    ),
    28: (
        "Find entries containing both D- and L-polypeptide chains",
        "Uses `<@` with a two-element array `{1,2}` to require both chain types.",
    ),
    29: (
        "Find entries containing D- or L-polypeptide chains",
        "Uses the array overlap operator (`&&`) to match entries with either chain type.",
    ),
    30: (
        "Find entries without DNA chains",
        "Uses `NOT` with `&&` to exclude entries whose `chain_type_ids` contains type 3 (polydeoxyribonucleotide).",
    ),
    31: (
        "Exclude entries containing both DNA and RNA",
        "Uses `NOT ... &&` to exclude entries with both chain type 3 (DNA) and 4 (RNA).",
    ),
    32: (
        "Find entries containing only D-polypeptide chains",
        "Combines `<@` (must contain type 1) with `NOT ... &&` (must not contain any other types) to find entries with exclusively D-polypeptide chains.",
    ),
    35: (
        "Calculate total molecular weight per entry",
        "Computes the sum of `pdbx_number_of_molecules * formula_weight` for polymer entities, grouped by PDB ID, ordered by weight descending.",
    ),
    36: (
        "Get entry metadata with unit cell and molecular weight",
        "Joins `cell`, `struct`, `struct_keywords`, and `entity` to produce a comprehensive summary including titles, unit cell parameters, chain count, and total molecular weight.",
    ),
    39: (
        "Count residues in a specific entry",
        "Uses a CTE to count residues per entity from `entity_poly_seq`, then multiplies by molecule count to get the total residue count.",
    ),
    41: (
        "Map entity IDs to chain IDs (label_asym_id / auth_asym_id)",
        "Joins `entity_poly` with `pdbx_poly_seq_scheme` to show the correspondence between entity IDs and both systematic (label) and author-assigned chain IDs.",
    ),
    43: (
        "Get detailed chain mapping for specific entities",
        "Uses a CTE to build a chain mapping from `struct_asym`, then joins with `pdbx_poly_seq_scheme` to get author chain IDs and non-polymer scheme information for specific entity IDs.",
    ),
    46: (
        "List large structure entries with polymer chain counts",
        "Joins `pdbx_database_status` (filtering `pdb_format_compatible='N'`) with `entity` to count polymer chains in large structures, sorted by chain count ascending.",
    ),
    48: (
        "List large structure entries with total molecular weight",
        "Similar to the chain count query, but sums `formula_weight` for polymer entities in large structures, sorted by weight descending.",
    ),
    59: (
        "Search entries by amino acid sequence and organism",
        "Finds entries containing a specific peptide sequence from a particular organism by joining `entity_poly` with `brief_summary` and filtering with `LIKE`.",
    ),
    61: (
        "Find entries with both peptide chains and non-water ligands",
        "Joins `brief_summary`, `entity`, and `pdbx_nonpoly_scheme` to find entries containing both polymer and non-polymer (non-water) components.",
    ),
    63: (
        "Find entries by entity name with chain IDs",
        "Uses a CTE and `ILIKE` to find entities named 'phospholipase C', then joins to get chain IDs from `struct_asym` and `pdbx_poly_seq_scheme`.",
    ),
    64: (
        "Find entries by entity name and organism",
        "Extends the entity name search with an additional join to `entity_src_gen` or `entity_src_nat` to filter by source organism (rat).",
    ),
    66: (
        "Get chain details and entity types for a specific entry",
        "Uses a CTE to retrieve all entities (polymer and non-polymer) for a specific entry, showing chain IDs, entity names, and entity types.",
    ),

    # Structural Properties
    1: (
        "Count entries per keyword (case-insensitive)",
        "Uses `LOWER()` and `GROUP BY` to aggregate keywords case-insensitively, then sorts by frequency using `ORDER BY COUNT(...) DESC`.",
    ),
    18: (
        "Find entries by experimental method",
        "Uses `ANY()` on the `exptl_method_ids` integer array to find entries determined by solution NMR (method ID 6). See `brief_summary` docs for the full method ID mapping.",
    ),
    20: (
        "Get crystal density for a specific entry",
        "Retrieves the solvent density percentage from the `exptl_crystal` table.",
    ),
    33: (
        "Get experimental method, unit cell, and crystal density for multiple entries",
        "Joins `exptl`, `cell`, and `exptl_crystal` to retrieve experimental details for two specific entries.",
    ),
    34: (
        "Find entries with resolution better than 2.0 Angstroms",
        "Filters the `refine` table by `ls_d_res_high <= 2.0`. Note that lower values indicate higher resolution.",
    ),
    51: (
        "Count entries per keyword (top N, case-insensitive)",
        "Same approach as example 1 but with `LIMIT` to restrict output to the top results.",
    ),
    73: (
        "Get resolution and R-free values",
        "Retrieves resolution and R-free refinement statistics. Uses quoted column names for case-sensitive identifiers.",
    ),

    # Biological Assembly
    37: (
        "List biological assembly information for all entries",
        "Joins `pdbx_struct_assembly` with `pdbx_struct_assembly_gen` to get oligomeric state, chain lists, and symmetry operations. Filters out entries without assembly details.",
    ),
    38: (
        "Get biological assembly information for a specific entry",
        "Same join as the all-entries query, but filtered to a single PDB entry (1nov).",
    ),
    47: (
        "Get biological assembly generation details for a specific entry",
        "Retrieves assembly generation information including chain lists and operator expressions for entry 1bbt.",
    ),

    # Cross-references
    2: (
        "Find entries by Gene Ontology biological process",
        "Queries the `gene_ontology_pdbmlplus` table to find entries annotated with a specific GO biological process (tricarboxylic acid cycle).",
    ),
    40: (
        "Map PDB entries to UniProt IDs",
        "Queries `struct_ref` to build a mapping between PDB entries and UniProt accession codes. Uses `DISTINCT` to remove duplicate rows.",
    ),
    70: (
        "Find entries by UniProt accession ID",
        "Filters `struct_ref` by UniProt database name and a specific accession ID.",
    ),
    71: (
        "Find entries by UniProt database code",
        "Similar to accession search, but uses `db_code` (e.g., 'CDK3_HUMAN') instead of accession number.",
    ),

    # Chemical Components
    13: (
        "Find entries containing a specific ligand",
        "Searches the `chem_comp` table for entries containing heme (HEM).",
    ),
    42: (
        "Find non-polymer entities missing from pdbx_nonpoly_scheme",
        "Uses `LEFT JOIN` and `IS NULL` to find non-polymer entities that have no corresponding entry in `pdbx_nonpoly_scheme`.",
    ),
    44: (
        "Get non-polymer component details with chain mapping",
        "Extends the chain mapping CTE to include non-polymer scheme information, showing component IDs and sequence numbers alongside chain identifiers.",
    ),
    55: (
        "Find entries containing a compound by InChIKey",
        "Joins `pdbj.chem_comp` with `cc.pdbx_chem_comp_descriptor` to find entries containing a compound identified by its InChIKey. Demonstrates cross-schema joins.",
    ),
    56: (
        "Find entries by CSD (Cambridge Structural Database) compound ID",
        "Joins across `pdbj`, `ccmodel`, and cross-references to find entries containing a compound identified by its CSD ID. Demonstrates multi-schema joins.",
    ),
    57: (
        "Find antibody entries with low molecular weight",
        "Joins `pdbx_molecule_features` with `prd.pdbx_reference_molecule` to find antibody entries where the formula weight is at most 1000 Da. Demonstrates cross-schema joins with the PRD schema.",
    ),
    60: (
        "List all chemical components with names, formulas, and InChIKeys",
        "Queries the `cc` schema to get a comprehensive listing of chemical components by joining `chem_comp` with `pdbx_chem_comp_descriptor` (filtered to InChIKey type).",
    ),

    # Advanced
    45: (
        "Find large structure entries incompatible with PDB format",
        "Queries `pdbx_database_status` for entries where `pdb_format_compatible='N'`, identifying structures too large for the legacy PDB format.",
    ),
}


def format_sql(sql: str) -> str:
    """Clean up SQL formatting."""
    # Normalize whitespace
    lines = sql.split("\n")
    # Remove trailing whitespace
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


def generate_markdown() -> str:
    """Generate the full markdown document."""
    data = json.loads(INPUT_FILE.read_text())
    available = [ex for ex in data if ex["available"]]

    # Group by category
    grouped: dict[str, list] = {cat: [] for cat in CATEGORY_ORDER}
    for ex in available:
        cat = ex["category"]
        if cat in grouped:
            grouped[cat].append(ex)

    parts = []

    # Frontmatter
    parts.append("""---
sidebar_position: 1
---

# SQL Query Examples

A collection of SQL query examples for the pdb-mine-builder database. These examples are adapted from [PDBj Mine SQL examples](https://pdbj.org/help/mine-sql) with schema-prefixed table names.

:::tip How to run
Use `pmb query` or connect directly with `psql`:

```bash
# Using pmb query
pmb query "SELECT pdbid FROM pdbj.brief_summary LIMIT 5"

# Using psql (via pixi)
pixi run psql -c "SELECT pdbid FROM pdbj.brief_summary LIMIT 5"
```

Click the **copy button** (top-right of each code block) to copy a query to your clipboard.
:::

:::info PostgreSQL array operators
Many examples use PostgreSQL array operators on `brief_summary` columns:

| Operator | Meaning | Example |
|----------|---------|---------|
| `<@` | is contained by (all elements match) | `'{1,2}' <@ chain_type_ids` |
| `&&` | overlaps (any element matches) | `'{2001}' && citation_year` |
| `ANY()` | matches any array element | `6 = ANY(exptl_method_ids)` |

See the [brief_summary column reference](/docs/database/pdbj#brief_summary) for array column definitions and ID mappings.
:::
""")

    # Generate each category section
    for cat in CATEGORY_ORDER:
        examples = grouped[cat]
        if not examples:
            continue

        label = CATEGORY_LABELS[cat]
        desc = CATEGORY_DESCRIPTIONS[cat]
        count = len(examples)

        parts.append(f"\n## {label} ({count})\n")
        parts.append(f"{desc}\n")

        for ex in examples:
            num = ex["number"]
            sql = format_sql(ex["sql_fixed"])

            if num in EXAMPLES_EN:
                title, description = EXAMPLES_EN[num]
            else:
                # Fallback (should not happen)
                title = f"Example {num}"
                description = ex["title_ja"]

            parts.append(f"""
<details>
<summary>{title}</summary>

{description}

```sql
{sql}
```

</details>
""")

    return "\n".join(parts)


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    content = generate_markdown()
    OUTPUT_FILE.write_text(content)
    print(f"Generated {OUTPUT_FILE}")

    # Verify all available examples have English translations
    data = json.loads(INPUT_FILE.read_text())
    available = [ex for ex in data if ex["available"]]
    missing = [ex["number"] for ex in available if ex["number"] not in EXAMPLES_EN]
    if missing:
        print(f"WARNING: Missing English translations for: {missing}")
    else:
        print(f"All {len(available)} examples have English translations.")


if __name__ == "__main__":
    main()
