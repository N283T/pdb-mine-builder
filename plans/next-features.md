# Next Features Plan

## Overview

Features to implement:
1. ~~RDKit SQL functions for chemical similarity search~~ ✅ PR #24
2. ~~RDKit molecular descriptors (MW, LogP, TPSA, etc.)~~ ✅ PR #25
3. SIFTS data pipeline investigation and implementation

---

## Task 1: RDKit SQL Functions for Chemical Similarity Search

### Current State

RDKit PostgreSQL extension is already installed with:
- `mol` column in `cc.brief_summary` (generated from `canonical_smiles`)
- GiST index on `mol` column for substructure searches
- Functions: `tanimoto_sml`, `dice_sml`, `morganbv_fp`, `atompair_fp`, etc.

### Goal

Create SQL views and functions for easy chemical similarity searches.

### Implementation

#### Phase 1: SQL Functions/Views

Create `scripts/rdkit_functions.sql`:

```sql
-- Tanimoto similarity search (Morgan fingerprint)
CREATE OR REPLACE FUNCTION cc.similar_compounds(
    query_smiles TEXT,
    threshold FLOAT DEFAULT 0.7,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    comp_id TEXT,
    name TEXT,
    smiles TEXT,
    similarity FLOAT
) AS $$
    SELECT
        comp_id,
        name,
        canonical_smiles,
        tanimoto_sml(morganbv_fp(mol), morganbv_fp(mol_from_smiles(query_smiles::cstring))) AS similarity
    FROM cc.brief_summary
    WHERE mol IS NOT NULL
      AND morganbv_fp(mol) % morganbv_fp(mol_from_smiles(query_smiles::cstring))
    ORDER BY similarity DESC
    LIMIT limit_count;
$$ LANGUAGE SQL STABLE;

-- Substructure search wrapper
CREATE OR REPLACE FUNCTION cc.substructure_search(
    query_smarts TEXT,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    comp_id TEXT,
    name TEXT,
    smiles TEXT
) AS $$
    SELECT comp_id, name, canonical_smiles
    FROM cc.brief_summary
    WHERE mol @> query_smarts::mol
    LIMIT limit_count;
$$ LANGUAGE SQL STABLE;
```

#### Phase 2: Fingerprint Index (Optional)

For better performance on large datasets:

```sql
-- Pre-computed fingerprint column
ALTER TABLE cc.brief_summary
ADD COLUMN IF NOT EXISTS morgan_fp bfp
GENERATED ALWAYS AS (morganbv_fp(mol)) STORED;

-- GiST index for similarity search
CREATE INDEX IF NOT EXISTS brief_summary_morgan_fp_idx
ON cc.brief_summary USING gist(morgan_fp);
```

### Usage Examples

```sql
-- Find compounds similar to aspirin (Tanimoto >= 0.7)
SELECT * FROM cc.similar_compounds('CC(=O)Oc1ccccc1C(=O)O', 0.7, 20);

-- Find compounds containing benzene ring
SELECT * FROM cc.substructure_search('c1ccccc1', 50);

-- Find compounds similar to ATP
SELECT * FROM cc.similar_compounds(
    (SELECT canonical_smiles FROM cc.brief_summary WHERE comp_id = 'ATP'),
    0.6
);
```

### Tasks

- [x] Create `scripts/rdkit_functions.sql`
- [x] Add to `_ensure_rdkit_setup()` in `cc.py`
- [x] Add documentation to README
- [x] Add tests for SQL functions

> **Status**: Completed in PR #24

---

## Task 2: SIFTS Data Pipeline

### Current State

SIFTS data exists at `/mnt/c/pdb/pdbj/pdbjplus/data/sifts/rdf/`:

| File | Content | Size |
|------|---------|------|
| `pdb_chain_uniprot.ttl.gz` | PDB → UniProt (detailed) | 45MB |
| `pdb_chain_uniprot_short.ttl.gz` | PDB → UniProt (short) | 2.9MB |
| `pdb_chain_go.ttl.gz` | PDB → Gene Ontology | 18MB |
| `pdb_chain_pfam.ttl.gz` | PDB → Pfam | 2.6MB |
| `pdb_chain_interpro.ttl.gz` | PDB → InterPro | 9.7MB |
| `pdb_chain_enzyme.ttl.gz` | PDB → EC numbers | 2.0MB |
| `pdb_chain_taxonomy.ttl.gz` | PDB → NCBI Taxonomy | 2.2MB |
| `pdb_chain_cath_uniprot.ttl.gz` | PDB → CATH/UniProt | 2.0MB |
| `pdb_chain_scop_uniprot.ttl.gz` | PDB → SCOP/UniProt | 0.8MB |
| `pdb_pubmed.ttl.gz` | PDB → PubMed | 1.2MB |
| `uniprot_pdb.ttl.gz` | UniProt → PDB | 1.9MB |

### Data Format

RDF Turtle format with simple triples:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix pfam: <http://identifiers.org/pfam/> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso pfam:PF00042 .
<https://rdf.wwpdb.org/pdb/10GS/entity/1> rdfs:seeAlso pfam:PF02798 .
```

URI pattern: `https://rdf.wwpdb.org/pdb/{PDBID}/entity/{entity_id}`

### Investigation Tasks

- [ ] Understand relationship to existing `gene_ontology_pdbmlplus` in pdbj schema
- [ ] Determine if SIFTS should supplement or replace mmjson-plus GO data
- [ ] Check if PDBj uses SIFTS data in their RDB
- [ ] Identify which SIFTS files are most useful

### Potential Schema

```yaml
# schemas/sifts.def.yml
schema_name: sifts
primary_key: pdbid

tables:
  - name: pdb_uniprot
    columns:
      - [pdbid, text]
      - [entity_id, text]
      - [uniprot_id, text]
    primary_key: [pdbid, entity_id, uniprot_id]

  - name: pdb_go
    columns:
      - [pdbid, text]
      - [entity_id, text]
      - [go_id, text]
    primary_key: [pdbid, entity_id, go_id]

  - name: pdb_pfam
    columns:
      - [pdbid, text]
      - [entity_id, text]
      - [pfam_id, text]
    primary_key: [pdbid, entity_id, pfam_id]

  # ... more tables
```

### Implementation Approach

1. **Parser**: Create TTL parser (or use rdflib)
2. **Pipeline**: New `sifts` pipeline similar to existing ones
3. **Schema**: Define tables for each cross-reference type
4. **Sync**: Add rsync target for SIFTS data

### Questions to Resolve

1. Is this data already in mine2 through mmjson-plus?
2. What's the sync source URL for SIFTS data?
3. Are there any PDBj-specific transformations needed?

---

## Task 3: RDKit Molecular Descriptors

### Goal

Add molecular descriptors (物性値) calculated by RDKit to the database for chemical property searches.

### Available Descriptors (RDKit)

| Descriptor | Function | Description |
|------------|----------|-------------|
| mol_amw | `mol_amw(mol)` | Average molecular weight |
| mol_exactmw | `mol_exactmw(mol)` | Exact molecular weight |
| mol_logp | `mol_logp(mol)` | Wildman-Crippen LogP |
| mol_tpsa | `mol_tpsa(mol)` | Topological polar surface area |
| mol_hba | `mol_hba(mol)` | Hydrogen bond acceptors |
| mol_hbd | `mol_hbd(mol)` | Hydrogen bond donors |
| mol_numrotatablebonds | `mol_numrotatablebonds(mol)` | Rotatable bonds |
| mol_numrings | `mol_numrings(mol)` | Number of rings |
| mol_numatoms | `mol_numatoms(mol)` | Number of atoms |
| mol_numheavyatoms | `mol_numheavyatoms(mol)` | Number of heavy atoms |
| mol_formula | `mol_formula(mol)` | Molecular formula |
| mol_fractioncsp3 | `mol_fractioncsp3(mol)` | Fraction of sp3 carbons |
| mol_numheteroatoms | `mol_numheteroatoms(mol)` | Number of heteroatoms |

### Implementation Options

#### Option A: Add columns to `cc.brief_summary`

```sql
ALTER TABLE cc.brief_summary
ADD COLUMN mol_weight FLOAT GENERATED ALWAYS AS (mol_amw(mol)) STORED,
ADD COLUMN logp FLOAT GENERATED ALWAYS AS (mol_logp(mol)) STORED,
ADD COLUMN tpsa FLOAT GENERATED ALWAYS AS (mol_tpsa(mol)) STORED,
ADD COLUMN hba INT GENERATED ALWAYS AS (mol_hba(mol)) STORED,
ADD COLUMN hbd INT GENERATED ALWAYS AS (mol_hbd(mol)) STORED,
ADD COLUMN rotatable_bonds INT GENERATED ALWAYS AS (mol_numrotatablebonds(mol)) STORED,
ADD COLUMN num_rings INT GENERATED ALWAYS AS (mol_numrings(mol)) STORED,
ADD COLUMN formula TEXT GENERATED ALWAYS AS (mol_formula(mol)) STORED;
```

**Pros**: Simple, all data in one place
**Cons**: Many columns, schema change required

#### Option B: Create separate `cc.descriptors` table

```sql
CREATE TABLE cc.descriptors (
    comp_id TEXT PRIMARY KEY REFERENCES cc.brief_summary(comp_id),
    mol_weight FLOAT,
    logp FLOAT,
    tpsa FLOAT,
    hba INT,
    hbd INT,
    rotatable_bonds INT,
    num_rings INT,
    formula TEXT,
    -- Lipinski's Rule of Five
    lipinski_violations INT
);
```

**Pros**: Clean separation, easy to extend
**Cons**: Requires JOIN for queries

#### Option C: SQL View (no schema change)

```sql
CREATE VIEW cc.compound_properties AS
SELECT
    comp_id,
    name,
    canonical_smiles,
    mol_amw(mol) AS mol_weight,
    mol_logp(mol) AS logp,
    mol_tpsa(mol) AS tpsa,
    mol_hba(mol) AS hba,
    mol_hbd(mol) AS hbd,
    mol_numrotatablebonds(mol) AS rotatable_bonds,
    mol_numrings(mol) AS num_rings,
    mol_formula(mol) AS formula
FROM cc.brief_summary
WHERE mol IS NOT NULL;
```

**Pros**: No schema change, always up-to-date
**Cons**: Computed on every query (slower for large result sets)

### Usage Examples

```sql
-- Lipinski's Rule of Five filter
SELECT comp_id, name, mol_weight, logp, hba, hbd
FROM cc.compound_properties
WHERE mol_weight < 500
  AND logp < 5
  AND hba <= 10
  AND hbd <= 5;

-- Find drug-like compounds similar to aspirin
SELECT * FROM cc.similar_compounds('CC(=O)Oc1ccccc1C(=O)O', 0.6, 100) s
JOIN cc.compound_properties p USING (comp_id)
WHERE p.mol_weight < 500 AND p.logp BETWEEN -1 AND 5;
```

### Tasks

- [x] Decide on implementation approach (A/B/C) → **Option A**
- [x] Implement as GENERATED columns in `_ensure_rdkit_setup()`
- [x] Add documentation to README
- [x] Add tests

> **Status**: Completed in PR #25

---

## Priority

1. ~~**RDKit SQL functions**~~ ✅ Completed (PR #24)
2. ~~**RDKit descriptors**~~ ✅ Completed (PR #25)
3. **SIFTS investigation** - Research first, then implement

---

- [ ] **DONE** - Plan complete
