---
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

## Basic Queries (5)

Simple queries to retrieve PDB entries by ID, count, or pattern matching.


<details>
<summary>List all PDB IDs</summary>

Retrieves every PDB identifier from the summary table.

```sql
SELECT pdbid FROM pdbj.brief_summary
```

</details>


<details>
<summary>Count all PDB entries</summary>

Returns the total number of PDB entries in the database.

```sql
SELECT COUNT(pdbid) FROM pdbj.brief_summary
```

</details>


<details>
<summary>Find PDB IDs starting with '1g'</summary>

Uses `LIKE` with a wildcard pattern to match PDB IDs by prefix.

```sql
SELECT pdbid FROM pdbj.brief_summary WHERE pdbid like '1g%'
```

</details>


<details>
<summary>Get summary information for a specific entry</summary>

Retrieves the PDB ID and structure title for entry 1gof.

```sql
SELECT pdbid, struct_title FROM pdbj.brief_summary WHERE pdbid='1gof'
```

</details>


<details>
<summary>Find PDB IDs consisting of all numeric characters</summary>

Uses a regular expression (`~`) to match PDB IDs where all four characters are digits.

```sql
SELECT pdbid FROM pdbj.brief_summary WHERE pdbid ~ '[0-9]{4}'
```

</details>


## Author & Citation (15)

Search entries by author names, journal information, DOIs, and PubMed IDs.


<details>
<summary>Find entries by depositor or primary citation author</summary>

Joins `citation_author` and `audit_author` to find entries where a specific person appears as either a primary citation author or a depositor.

```sql
SELECT DISTINCT e1.pdbid FROM pdbj.citation_author e1
JOIN pdbj.audit_author e2 ON e1.pdbid=e2.pdbid
WHERE (e1.name='Roberts, R.J.' AND e1.citation_id='primary') OR e2.name='Roberts, R.J.'
```

</details>


<details>
<summary>List all citation authors for a specific entry</summary>

Retrieves all rows from the `citation_author` table for PDB entry 1gof.

```sql
SELECT * FROM pdbj.citation_author WHERE pdbid='1gof'
```

</details>


<details>
<summary>Find entries by citation author name</summary>

Uses the PostgreSQL array containment operator (`&lt;@`) on the `citation_author` array column.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE '{"Ito, N."}' <@ citation_author
```

</details>


<details>
<summary>Find entries by multiple citation authors (AND)</summary>

Uses `&lt;@` with a multi-element array to find entries where both authors appear in the citation list.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE '{"Ito, N.","Phillips, S.E.V."}' <@ citation_author
```

</details>


<details>
<summary>Find entries by primary citation author</summary>

Searches the `citation_author_pri` array column for primary citation authors only.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE '{"Ito, N."}' <@ citation_author_pri
```

</details>


<details>
<summary>Find entries by citation year</summary>

Uses the array overlap operator (`&&`) to match entries where the citation year array contains 2001.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE '{2001}' && citation_year
```

</details>


<details>
<summary>Find entries by journal volume number</summary>

Uses `&&` on the `citation_volume` array to find entries published in volume 555.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE '{"555"}' && citation_volume
```

</details>


<details>
<summary>Find entries by year, volume, and experimental method</summary>

Combines multiple array operators to filter by citation year, volume, and experimental method ID.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE '{1991}' && citation_year AND '{"266"}' && citation_volume
AND '{1}' && exptl_method_ids
```

</details>


<details>
<summary>Get DOI for a specific entry's citation</summary>

Retrieves the DOI from the `citation` table. Note the quoted column name (case-sensitive).

```sql
SELECT "pdbx_database_id_DOI" FROM pdbj.citation WHERE pdbid='1iqq'
```

</details>


<details>
<summary>Get PubMed ID for a specific entry's citation</summary>

Retrieves the PubMed ID from the `citation` table using a case-sensitive column name.

```sql
SELECT "pdbx_database_id_PubMed" FROM pdbj.citation WHERE pdbid='1iqq'
```

</details>


<details>
<summary>Get PubMed IDs for multiple entries</summary>

Retrieves PubMed IDs for two entries, filtering out rows where DOI is null.

```sql
SELECT pdbid, "pdbx_database_id_PubMed"
FROM pdbj.citation WHERE (pdbid='1ai9' OR pdbid='1ao8')
AND "pdbx_database_id_DOI" IS NOT NULL
```

</details>


<details>
<summary>Get DOIs for entries matching a PDB ID prefix</summary>

Uses `LIKE` to find all entries starting with '1i' and returns their DOIs.

```sql
SELECT pdbid, "pdbx_database_id_DOI"
FROM pdbj.citation WHERE pdbid LIKE '1i%'
AND "pdbx_database_id_DOI" IS NOT NULL
```

</details>


<details>
<summary>Search entries by journal name</summary>

Uses `ILIKE` (case-insensitive) on the `citation_journal` array to find entries by journal name.

```sql
SELECT pdbid, citation_journal, citation_title
FROM pdbj.brief_summary
WHERE CAST(citation_journal AS text) ILIKE '%molecular cell%'
```

</details>


<details>
<summary>Search entries by keyword in title with sorting</summary>

Finds entries containing 'spliceosome' in the title, sorted by total residue count descending.

```sql
SELECT pdbid,
  struct_title AS title,
  deposit_author AS depositor,
  deposition_date,
  release_date,
  modification_date,
  exptl_method AS method,
  citation_title_pri AS primary_citation,
  (SELECT SUM(s) FROM UNNEST(chain_length) AS s) AS total_residues
FROM pdbj.brief_summary
WHERE struct_title ILIKE '%spliceosome%'
ORDER BY (SELECT SUM(s) FROM UNNEST(chain_length) AS s) DESC
```

</details>


<details>
<summary>Search by keyword in citation or structure title</summary>

Joins `brief_summary` with `struct` to search for 'spike' in both citation and structure titles.

```sql
SELECT b.pdbid, b.citation_title, s.title
FROM pdbj.brief_summary b
JOIN pdbj.struct s ON b.pdbid=s.pdbid
WHERE CAST(b.citation_title AS text) ILIKE '%spike%'
OR s.title ILIKE '%spike%'
```

</details>


## Date Search (4)

Filter entries by release date, deposition date, or publication year.


<details>
<summary>Find entries released after a specific date</summary>

Filters by `release_date` using a date comparison.

```sql
SELECT pdbid
FROM pdbj.brief_summary
WHERE release_date >= '2000-01-01'
```

</details>


<details>
<summary>Find entries by release date, deposition date, and PDB ID prefix</summary>

Combines date range filters with a `LIKE` pattern match on the PDB ID.

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE release_date >= '2003-01-01'
AND deposition_date >= '2001-01-01'
AND b.pdbid LIKE '2k%'
```

</details>


<details>
<summary>Find kinase entries deposited in a specific year</summary>

Finds entries with EC number '2.7' (kinases) deposited in 2016, joining `entity` with `struct_asym`.

```sql
SELECT entity.pdbid, entity.id, struct_asym.id AS label_asym_id, entity.pdbx_description FROM pdbj.entity
LEFT JOIN pdbj.struct_asym ON entity.pdbid=struct_asym.pdbid AND entity.id=struct_asym.entity_id
LEFT JOIN pdbj.pdbx_database_status ON entity.pdbid=pdbx_database_status.pdbid
WHERE entity.pdbx_ec LIKE '2.7.%'
AND pdbx_database_status.recvd_initial_deposition_date >= '2016-01-01'::DATE
AND pdbx_database_status.recvd_initial_deposition_date <= '2016-12-31'::DATE
```

</details>


<details>
<summary>Get release dates for specific PDB IDs</summary>

Uses `IN` to retrieve release dates for a list of specific PDB IDs.

```sql
SELECT pdbid,release_date FROM pdbj.brief_summary
WHERE pdbid IN ('1crn','2prg','1gof','1ubq')
```

</details>


## Entity & Chain (21)

Query polymer chains, chain types, residue counts, molecular weights, and sequences.


<details>
<summary>Find entries containing both synthetic and natural polymers</summary>

Uses a CTE with `LEFT JOIN` across three source tables to identify entries with both synthetic and non-synthetic polymer entities.

```sql
WITH pdbent AS (SELECT e1.pdbid, COUNT(e2.entity_id) syncount,
 COUNT(e3.entity_id) natcount, COUNT(e4.entity_id) gencount FROM pdbj.entity e1
 LEFT JOIN pdbj.pdbx_entity_src_syn e2 ON e1.pdbid=e2.pdbid AND e1.id=e2.entity_id
 LEFT JOIN pdbj.entity_src_nat e3 ON e1.pdbid=e3.pdbid AND e1.id=e3.entity_id
 LEFT JOIN pdbj.entity_src_gen e4 ON e1.pdbid=e4.pdbid AND e1.id=e4.entity_id
 WHERE e1.type='polymer'
 GROUP BY e1.pdbid)
SELECT pdbid FROM pdbent
WHERE syncount > 0
AND (natcount + gencount) > 0
```

</details>


<details>
<summary>Find entries with the highest molecule copy counts</summary>

Retrieves the top 5 polymer entities by `pdbx_number_of_molecules` using `ORDER BY ... DESC LIMIT`.

```sql
SELECT pdbid,id,pdbx_number_of_molecules FROM pdbj.entity
WHERE type='polymer' ORDER BY pdbx_number_of_molecules DESC LIMIT 5
```

</details>


<details>
<summary>Find entries by EC number with chain IDs</summary>

Uses `LEFT JOIN` between `entity` and `struct_asym` to get chain identifiers for entities with a specific EC number.

```sql
SELECT entity.pdbid, entity.id, struct_asym.id AS label_asym_id, entity.pdbx_description FROM pdbj.entity
LEFT JOIN pdbj.struct_asym ON entity.pdbid=struct_asym.pdbid AND entity.id=struct_asym.entity_id
WHERE entity.pdbx_ec='1.1.1.1'
```

</details>


<details>
<summary>Find entries containing D-polypeptide chains</summary>

Uses the array containment operator (`&lt;@`) to find entries where `chain_type_ids` contains type 1.

```sql
SELECT pdbid FROM pdbj.brief_summary WHERE '{1}' <@ chain_type_ids
```

</details>


<details>
<summary>Find entries containing both D- and L-polypeptide chains</summary>

Uses `&lt;@` with `\{1,2\}` to require both chain types are present.

```sql
SELECT pdbid FROM pdbj.brief_summary WHERE '{1,2}' <@ chain_type_ids
```

</details>


<details>
<summary>Find entries containing D- or L-polypeptide chains</summary>

Uses the array overlap operator (`&&`) to match entries with either chain type.

```sql
SELECT pdbid FROM pdbj.brief_summary WHERE ('{1,2}' && chain_type_ids)
```

</details>


<details>
<summary>Find entries without DNA chains</summary>

Uses `NOT` with `&&` to exclude entries whose `chain_type_ids` contains type 3 (DNA).

```sql
SELECT pdbid FROM pdbj.brief_summary WHERE NOT ('{3}' && chain_type_ids)
```

</details>


<details>
<summary>Exclude entries containing both DNA and RNA</summary>

Uses `NOT ... &&` to exclude entries with both chain type 3 (DNA) and 4 (RNA).

```sql
SELECT pdbid
FROM pdbj.brief_summary
WHERE NOT ('{3,4}' && chain_type_ids)
```

</details>


<details>
<summary>Find entries containing only D-polypeptide chains</summary>

Combines `&lt;@` (must contain type 1) with `NOT ... &&` (must not contain any other types).

```sql
SELECT pdbid
FROM pdbj.brief_summary
WHERE ('{1}' <@ chain_type_ids) AND NOT ('{2,3,4,5,6,7,8,9}' && chain_type_ids)
```

</details>


<details>
<summary>Calculate total molecular weight per entry</summary>

Computes `SUM(pdbx_number_of_molecules * formula_weight)` for polymer entities, grouped by PDB ID.

```sql
SELECT pdbid, SUM(pdbx_number_of_molecules*formula_weight) AS weight
FROM pdbj.entity
WHERE type = 'polymer'
GROUP BY pdbid
ORDER BY weight DESC
```

</details>


<details>
<summary>Get entry metadata with unit cell and molecular weight</summary>

Joins `cell`, `struct`, `struct_keywords`, and `entity` for a comprehensive summary with unit cell parameters.

```sql
SELECT cell.pdbid, struct.pdbx_descriptor, struct_keywords.pdbx_keywords,
cell.length_a, cell.length_b, cell.length_c,
cell.angle_alpha, cell.angle_beta, cell.angle_gamma,
SUM(entity.pdbx_number_of_molecules) AS number_of_molecules,
SUM(entity.pdbx_number_of_molecules * entity.formula_weight) AS weight
FROM pdbj.cell
JOIN pdbj.struct ON cell.pdbid = struct.pdbid
JOIN pdbj.struct_keywords ON cell.pdbid = struct_keywords.pdbid
JOIN pdbj.entity ON cell.pdbid = entity.pdbid
WHERE entity.type = 'polymer'
GROUP BY cell.pdbid, struct.pdbx_descriptor, struct_keywords.pdbx_keywords,
cell.length_a, cell.length_b, cell.length_c, cell.angle_alpha,
cell.angle_beta, cell.angle_gamma
```

</details>


<details>
<summary>Count residues in a specific entry</summary>

Uses a CTE to count residues per entity from `entity_poly_seq`, then multiplies by molecule count.

```sql
WITH slen(pdbid, entity_id, len) AS
(select pdbid, entity_id, count(*)
 FROM pdbj.entity_poly_seq
 WHERE pdbid='1a14'
 GROUP BY pdbid, entity_id)
SELECT entity.pdbid, SUM(entity.pdbx_number_of_molecules*s.len) AS NumberOfResidues
FROM pdbj.entity
JOIN slen AS s ON s.pdbid = entity.pdbid and s.entity_id = entity.id
GROUP BY entity.pdbid
```

</details>


<details>
<summary>Map entity IDs to chain IDs (label/auth)</summary>

Joins `entity_poly` with `pdbx_poly_seq_scheme` to map entity IDs to both systematic and author chain IDs.

```sql
SELECT DISTINCT e1.entity_id,
e2.asym_id AS label_asym_id,
e2.pdb_strand_id AS auth_asym_id FROM pdbj.entity_poly e1
LEFT JOIN pdbj.pdbx_poly_seq_scheme e2 ON e1.pdbid=e2.pdbid
AND e1.entity_id=e2.entity_id
WHERE e1.pdbid='1a14'
ORDER BY e1.entity_id ASC
```

</details>


<details>
<summary>Get detailed chain mapping for specific entities</summary>

Uses a CTE to build a chain mapping from `struct_asym` with non-polymer scheme information.

```sql
WITH chain(pdbid,entity_id,label_asym_id) AS
(SELECT e1.pdbid, e1.entity_id, e1.id AS label_asym_id
 FROM pdbj.struct_asym AS e1
 WHERE e1.pdbid='1p8j'
 AND (e1.entity_id='4' OR e1.entity_id='7'))
SELECT e2.pdbid, chain.entity_id, chain.label_asym_id, e2.pdb_strand_id AS auth_asym_id, e2.mon_id AS residue_name
FROM pdbj.pdbx_nonpoly_scheme AS e2
JOIN chain ON chain.pdbid = e2.pdbid AND chain.label_asym_id=e2.asym_id
```

</details>


<details>
<summary>List large structure entries with polymer chain counts</summary>

Joins `pdbx_database_status` with `entity` to count polymer chains in large structures.

```sql
SELECT e1.pdbid, SUM(e2.pdbx_number_of_molecules) FROM pdbj.pdbx_database_status e1
JOIN pdbj.entity e2 ON e1.pdbid=e2.pdbid
WHERE e1.pdb_format_compatible='N'
AND e2.type='polymer'
GROUP BY e1.pdbid
ORDER BY SUM(e2.pdbx_number_of_molecules) ASC
```

</details>


<details>
<summary>List large structure entries with total molecular weight</summary>

Sums `formula_weight` for polymer entities in large structures, sorted by weight descending.

```sql
SELECT e1.pdbid, SUM(e2.formula_weight) AS total_formula_weight
FROM pdbj.pdbx_database_status e1
JOIN pdbj.entity e2 ON e1.pdbid=e2.pdbid
WHERE e1.pdb_format_compatible='N'
GROUP BY e1.pdbid
ORDER BY total_formula_weight DESC
```

</details>


<details>
<summary>Search entries by amino acid sequence and organism</summary>

Finds entries containing a specific peptide sequence from a particular organism using `LIKE`.

```sql
SELECT b.pdbid, e.pdbx_strand_id FROM pdbj.entity_poly e
LEFT JOIN pdbj.brief_summary b ON e.pdbid=b.pdbid
WHERE e.pdbx_seq_one_letter_code LIKE '%TVSFSWNKFVPKQPNMILQGDAIVTSSGKLQLNKVDENGTPKPSSLGR%'
AND b.biol_species LIKE '%Glycine max%'
```

</details>


<details>
<summary>Find entries with both peptide chains and non-water ligands</summary>

Joins `brief_summary`, `entity`, and `pdbx_nonpoly_scheme` to find entries with polymer and non-polymer components.

```sql
SELECT DISTINCT b.pdbid FROM pdbj.brief_summary b LEFT JOIN pdbj.entity e1 ON b.pdbid=e1.pdbid LEFT JOIN pdbj.pdbx_nonpoly_scheme e2 ON e1.pdbid=e2.pdbid AND e1.id=e2.entity_id WHERE ('{1,2}' && b.chain_type_ids) AND e1.type='non-polymer' AND NOT (e2.mon_id = ANY(array['HOH','DOD']))
```

</details>


<details>
<summary>Find entries by entity name with chain IDs</summary>

Uses a CTE and `ILIKE` to find entities named 'phospholipase C', then joins to get chain IDs.

```sql
WITH t1 AS
(SELECT DISTINCT e1.pdbid, e1.id entity_id, e1.pdbx_description chain_name FROM pdbj.entity e1
WHERE e1.pdbx_description ~* '.*phospholipase C.*')
SELECT t1.pdbid, t1.entity_id, array_agg(DISTINCT e2.pdb_strand_id) auth_asym_ids,
array_agg(DISTINCT e2.asym_id) label_asym_ids, t1.chain_name FROM t1
LEFT JOIN pdbj.pdbx_poly_seq_scheme e2 ON t1.pdbid=e2.pdbid
AND t1.entity_id=e2.entity_id GROUP BY t1.pdbid, t1.entity_id, t1.chain_name
```

</details>


<details>
<summary>Find entries by entity name and organism</summary>

Extends the entity name search with a join to filter by source organism (rat).

```sql
WITH t1 AS
(SELECT DISTINCT e1.pdbid,e1.id entity_id,e1.pdbx_description chain_name FROM pdbj.entity e1
WHERE e1.pdbx_description ~* '.*phospholipase C.*')
SELECT t1.pdbid, t1.entity_id, array_agg(DISTINCT e2.pdb_strand_id) auth_asym_ids,
array_agg(DISTINCT e2.asym_id) label_asym_ids, t1.chain_name FROM t1
LEFT JOIN pdbj.pdbx_poly_seq_scheme e2 ON t1.pdbid=e2.pdbid AND t1.entity_id=e2.entity_id
LEFT JOIN pdbj.brief_summary b ON e2.pdbid=b.pdbid
WHERE b.biol_species LIKE '%Rattus norvegicus%'
GROUP BY t1.pdbid,t1.entity_id,t1.chain_name,b.biol_species
```

</details>


<details>
<summary>Get chain details and entity types for a specific entry</summary>

Uses a CTE to retrieve all entities (polymer and non-polymer) with chain IDs and entity types.

```sql
WITH t1 AS
(SELECT DISTINCT e1.pdbid, e1.id entity_id, e1.pdbx_description chain_name, e1.type FROM pdbj.entity e1
WHERE e1.pdbid='4uv7')
SELECT t1.pdbid, t1.entity_id,
trim(both ',' from array_to_string(array_cat(array_agg(DISTINCT e2.pdb_strand_id),array_agg(DISTINCT e3.pdb_strand_id)),',')) auth_asym_ids,
trim(both ',' from array_to_string(array_cat(array_agg(DISTINCT e2.asym_id),array_agg(DISTINCT e3.asym_id)),',')) label_asym_ids,
t1.chain_name, t1.type FROM t1
LEFT JOIN pdbj.pdbx_poly_seq_scheme e2 ON t1.pdbid=e2.pdbid
AND t1.entity_id=e2.entity_id
LEFT JOIN pdbj.pdbx_nonpoly_scheme e3 ON t1.pdbid=e3.pdbid
AND t1.entity_id=e3.entity_id
GROUP BY t1.pdbid, t1.entity_id, t1.chain_name, t1.type
```

</details>


## Structure (7)

Experimental methods, resolution, unit cell parameters, keywords, and refinement.


<details>
<summary>Count entries per keyword (case-insensitive)</summary>

Uses `LOWER()` and `GROUP BY` to aggregate keywords, sorted by frequency with `ORDER BY COUNT(...) DESC`.

```sql
SELECT LOWER(pdbx_keywords), COUNT(entry_id) AS noe FROM pdbj.struct_keywords
GROUP BY LOWER(pdbx_keywords) ORDER BY COUNT(entry_id) DESC
```

</details>


<details>
<summary>Find entries by experimental method</summary>

Uses `ANY()` on `exptl_method_ids` to find entries by solution NMR (method ID 6).

```sql
SELECT pdbid
FROM pdbj.brief_summary b
WHERE 6 = ANY(exptl_method_ids)
```

</details>


<details>
<summary>Get crystal density for a specific entry</summary>

Retrieves the solvent density percentage from the `exptl_crystal` table.

```sql
SELECT density_percent_sol FROM pdbj.exptl_crystal WHERE pdbid='1iqq'
```

</details>


<details>
<summary>Get experimental method, unit cell, and crystal density</summary>

Joins `exptl`, `cell`, and `exptl_crystal` to retrieve experimental details for specific entries.

```sql
SELECT exptl.pdbid, exptl.method, cell.length_a, cell.length_b, cell.length_c, exptl_crystal.density_percent_sol
FROM pdbj.exptl
JOIN pdbj.cell ON exptl.pdbid = cell.pdbid
JOIN pdbj.exptl_crystal ON exptl.pdbid = exptl_crystal.pdbid
WHERE exptl.pdbid = '1iqq' OR exptl.pdbid = '1ioo'
```

</details>


<details>
<summary>Find entries with resolution better than 2.0 angstroms</summary>

Filters the `refine` table by `ls_d_res_high &lt;= 2.0`. Lower values = higher resolution.

```sql
SELECT pdbid, ls_d_res_high AS "resolution" FROM pdbj.refine WHERE ls_d_res_high <= 2.0
```

</details>


<details>
<summary>Count entries per keyword (top N)</summary>

Same approach as keyword counting but with `LIMIT` to restrict output to top results.

```sql
SELECT LOWER(pdbx_keywords), COUNT(entry_id) AS noe FROM pdbj.struct_keywords
GROUP BY LOWER(pdbx_keywords) ORDER BY COUNT(entry_id) DESC
LIMIT 10
```

</details>


<details>
<summary>Get resolution and R-free values</summary>

Retrieves resolution and R-free refinement statistics with quoted column names.

```sql
SELECT pdbid, ls_d_res_high AS "Resolution", "ls_R_factor_R_free" AS "R_free" FROM pdbj.refine
```

</details>


## Biological Assembly (3)

Biological assembly information including oligomeric state and generation details.


<details>
<summary>List biological assembly information for all entries</summary>

Joins `pdbx_struct_assembly` with `pdbx_struct_assembly_gen` to get oligomeric state and chain lists.

```sql
SELECT pdbx_struct_assembly.pdbid, pdbx_struct_assembly.details,
pdbx_struct_assembly.oligomeric_count, pdbx_struct_assembly.oligomeric_details,
pdbx_struct_assembly_gen.assembly_id, pdbx_struct_assembly_gen.asym_id_list,
pdbx_struct_assembly_gen.oper_expression
FROM pdbj.pdbx_struct_assembly
JOIN pdbj.pdbx_struct_assembly_gen
ON pdbx_struct_assembly.pdbid = pdbx_struct_assembly_gen.pdbid
AND pdbx_struct_assembly.id = pdbx_struct_assembly_gen.assembly_id
WHERE pdbx_struct_assembly.details IS NOT NULL
```

</details>


<details>
<summary>Get biological assembly for a specific entry</summary>

Same assembly join as above, filtered to a single PDB entry (1nov).

```sql
SELECT pdbx_struct_assembly.pdbid, pdbx_struct_assembly.details,
pdbx_struct_assembly.oligomeric_count, pdbx_struct_assembly.oligomeric_details,
pdbx_struct_assembly_gen.assembly_id, pdbx_struct_assembly_gen.asym_id_list,
pdbx_struct_assembly_gen.oper_expression
FROM pdbj.pdbx_struct_assembly
JOIN pdbj.pdbx_struct_assembly_gen
ON pdbx_struct_assembly.pdbid = pdbx_struct_assembly_gen.pdbid
AND pdbx_struct_assembly.id = pdbx_struct_assembly_gen.assembly_id
WHERE pdbx_struct_assembly.pdbid='1nov'
```

</details>


<details>
<summary>Get assembly generation details for a specific entry</summary>

Retrieves assembly chain lists and operator expressions for entry 1bbt.

```sql
SELECT e1.assembly_id, e1.asym_id_list, e1.oper_expression,
e2.oligomeric_details, e2.oligomeric_count
FROM pdbj.pdbx_struct_assembly_gen AS e1
LEFT JOIN pdbj.pdbx_struct_assembly AS e2
ON e1.pdbid=e2.pdbid AND e1.assembly_id=e2.id
WHERE e1.pdbid='1bbt'
```

</details>


## Cross-references (4)

Find entries by UniProt, Gene Ontology, and EC number identifiers.


<details>
<summary>Find entries by Gene Ontology biological process</summary>

Queries `gene_ontology_pdbmlplus` to find entries annotated with a specific GO process.

```sql
SELECT DISTINCT e.pdbid FROM pdbj.gene_ontology_pdbmlplus e
WHERE e.namespace='biological_process'
AND e.name='tricarboxylic acid cycle'
```

</details>


<details>
<summary>Map PDB entries to UniProt IDs</summary>

Queries `struct_ref` to build PDB-to-UniProt mapping using `DISTINCT`.

```sql
SELECT DISTINCT pdbid, entity_id, db_code, pdbx_db_accession
FROM pdbj.struct_ref
WHERE db_name='UNP' AND entity_id IS NOT NULL
```

</details>


<details>
<summary>Find entries by UniProt accession ID</summary>

Filters `struct_ref` by UniProt database name and a specific accession ID.

```sql
SELECT pdbid FROM pdbj.struct_ref WHERE struct_ref.db_name='UNP' AND struct_ref.pdbx_db_accession='Q00526'
```

</details>


<details>
<summary>Find entries by UniProt database code</summary>

Uses `db_code` (e.g., 'CDK3_HUMAN') instead of accession number.

```sql
SELECT pdbid FROM pdbj.struct_ref WHERE struct_ref.db_name='UNP' AND struct_ref.db_code='CDK3_HUMAN'
```

</details>


## Chemical Components (7)

Search chemical components, ligands, and small molecules by various identifiers.


<details>
<summary>Find entries containing a specific ligand</summary>

Searches `chem_comp` for entries containing heme (HEM).

```sql
SELECT pdbid FROM pdbj.chem_comp WHERE id='HEM'
```

</details>


<details>
<summary>Find non-polymer entities missing from pdbx_nonpoly_scheme</summary>

Uses `LEFT JOIN` and `IS NULL` to find non-polymer entities without corresponding scheme entries.

```sql
SELECT DISTINCT e1.pdbid, e1.id AS entity_id, e1.pdbx_description
FROM pdbj.entity AS e1
LEFT JOIN pdbj.pdbx_nonpoly_scheme e2 ON e1.pdbid=e2.pdbid AND e1.id=e2.entity_id
WHERE (e1.type='non-polymer' OR e1.type='water')
AND e2.entity_id IS NULL
ORDER BY e1.pdbid ASC
```

</details>


<details>
<summary>Get non-polymer component details with chain mapping</summary>

Extends chain mapping CTE to include non-polymer component IDs and sequence numbers.

```sql
WITH chain(pdbid,entity_id,label_asym_id) AS
(SELECT e1.pdbid, e1.entity_id, e1.id AS label_asym_id
 FROM pdbj.struct_asym AS e1
 WHERE e1.pdbid='1p8j'
 AND (e1.entity_id='4' OR e1.entity_id='7'))
SELECT chain.entity_id,
substring(string_agg(chain.label_asym_id,'-') from '^[0-9A-Za-z]+') label_asym_id,
substring(string_agg(e2.pdb_strand_id,'-') from '^[0-9A-Za-z]+') auth_asym_id,
string_agg(e2.mon_id,'-') AS sequence
FROM pdbj.pdbx_nonpoly_scheme AS e2
JOIN chain ON chain.pdbid = e2.pdbid AND chain.label_asym_id=e2.asym_id
GROUP BY chain.entity_id
```

</details>


<details>
<summary>Find entries containing a compound by InChIKey</summary>

Cross-schema join between `pdbj.chem_comp` and `cc.pdbx_chem_comp_descriptor` to search by InChIKey.

```sql
SELECT p.pdbid, p.id
FROM pdbj.chem_comp p
JOIN cc.pdbx_chem_comp_descriptor cc ON cc.comp_id = p.id
WHERE cc.type = 'InChIKey'
AND   cc.descriptor = 'ZKHQWZAMYRWXGA-KQYNXXCUSA-N'
```

</details>


<details>
<summary>Find entries by CSD compound ID</summary>

Multi-schema join across `pdbj`, `ccmodel`, and cross-references to find entries by CSD ID.

```sql
SELECT p.pdbid, p.id, p.name, r.db_code
FROM pdbj.chem_comp p
JOIN ccmodel.pdbx_chem_comp_model m ON m.comp_id = p.id
JOIN ccmodel.pdbx_chem_comp_model_reference r ON r.model_id = m.model_id
WHERE r.db_name = 'CSD' AND r.db_code = 'YARXEW'
```

</details>


<details>
<summary>Find antibody entries with low molecular weight</summary>

Joins `pdbx_molecule_features` with `prd.pdbx_reference_molecule` for antibodies &lt;= 1000 Da.

```sql
SELECT mf.pdbid, rm.name
FROM pdbj.pdbx_molecule_features mf
JOIN prd.pdbx_reference_molecule rm ON rm.prd_id = mf.prd_id
WHERE rm.class = 'Antibiotic'
AND rm.formula_weight < 1000.0
```

</details>


<details>
<summary>List all chemical components with names, formulas, and InChIKeys</summary>

Queries the `cc` schema joining `chem_comp` with `pdbx_chem_comp_descriptor` (InChIKey type).

```sql
SELECT c.id, c.name, c.formula, c.formula_weight, d.descriptor AS "InChIKey"
FROM cc.chem_comp c
JOIN cc.pdbx_chem_comp_descriptor d ON d.comp_id = c.comp_id
WHERE d.type = 'InChIKey'
```

</details>


## Advanced (1)

Complex queries combining multiple criteria or using advanced SQL features.


<details>
<summary>Find large structure entries incompatible with PDB format</summary>

Queries `pdbx_database_status` for entries where `pdb_format_compatible='N'`.

```sql
SELECT pdbid FROM pdbj.pdbx_database_status AS e
WHERE e.pdb_format_compatible='N'
```

</details>


## Chemical Search (RDKit) (8)

Structure-based chemical searches using the RDKit PostgreSQL cartridge. These queries use the `cc.brief_summary` table with its `mol` column and custom search functions.


<details>
<summary>Substructure search for benzene ring</summary>

Uses the RDKit substructure operator (`@&gt;`) to find chemical components containing a benzene ring.

```sql
SELECT comp_id, name, canonical_smiles
FROM cc.brief_summary
WHERE mol @> 'c1ccccc1'::qmol
LIMIT 20
```

</details>


<details>
<summary>Tanimoto similarity search (aspirin-like compounds)</summary>

Uses the `cc.similar_compounds` function to find compounds similar to aspirin (acetylsalicylic acid) using Tanimoto similarity with Morgan fingerprints. Default threshold is 0.7.

```sql
SELECT * FROM cc.similar_compounds(
  'CC(=O)Oc1ccccc1C(=O)O',  -- aspirin SMILES
  0.5,                       -- similarity threshold
  20                         -- max results
)
```

</details>


<details>
<summary>Dice similarity search (fragment-based)</summary>

Uses the `cc.similar_compounds_dice` function for fragment-based similarity search. Dice coefficient is often preferred over Tanimoto for small fragments.

```sql
SELECT * FROM cc.similar_compounds_dice(
  'c1ccccc1',  -- benzene SMILES
  0.5,         -- Dice similarity threshold
  20           -- max results
)
```

</details>


<details>
<summary>SMARTS substructure search (carboxylic acid)</summary>

Uses the `cc.substructure_search` function with a SMARTS pattern to find compounds containing a carboxylic acid group.

```sql
SELECT * FROM cc.substructure_search(
  '[CX3](=O)[OX2H1]',  -- carboxylic acid SMARTS
  50                    -- max results
)
```

</details>


<details>
<summary>Exact structure match by SMILES</summary>

Uses the `cc.exact_match` function to find the chemical component that exactly matches a given SMILES structure (ethanol in this example).

```sql
SELECT * FROM cc.exact_match('CCO')
```

</details>


<details>
<summary>Find compounds similar to an existing component (ATP)</summary>

Uses the `cc.similar_to_compound` function to find compounds structurally similar to ATP. The function looks up the reference SMILES automatically by component ID.

```sql
SELECT * FROM cc.similar_to_compound(
  'ATP',  -- reference component ID
  0.6,   -- Tanimoto similarity threshold
  20     -- max results
)
```

</details>


<details>
<summary>Calculate similarity between two compounds</summary>

Uses the `cc.compound_similarity` function to compute the Tanimoto similarity between ADP and ATP's SMILES structure.

```sql
SELECT cc.compound_similarity(
  'ADP',
  (SELECT canonical_smiles FROM cc.brief_summary WHERE comp_id = 'ATP')
)
```

</details>


<details>
<summary>Find PDB entries containing ligands similar to a query</summary>

Combines RDKit similarity search on `cc.brief_summary` with `pdbj.chem_comp` to find PDB entries that contain ligands structurally similar to a given SMILES.

```sql
SELECT DISTINCT pc.pdbid, sc.comp_id, sc.name, sc.similarity
FROM cc.similar_compounds('CC(=O)Oc1ccccc1C(=O)O', 0.6, 50) sc
JOIN pdbj.chem_comp pc ON pc.id = sc.comp_id
ORDER BY sc.similarity DESC
```

</details>
