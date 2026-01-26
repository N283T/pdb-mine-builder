-- RDKit SQL functions for chemical similarity search
--
-- NOTE: This is AUTO-EXECUTED by the cc/cc-cif pipeline after RDKit setup.
-- Manual execution: psql -d mine2 -f scripts/rdkit_functions.sql
--
-- Prerequisites:
--   - RDKit extension enabled
--   - cc.brief_summary table with mol column

-- =============================================================================
-- Similarity Search Functions
-- =============================================================================

-- Tanimoto similarity search using Morgan fingerprints
-- Returns compounds similar to the query SMILES above the threshold
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
BEGIN
    -- Set similarity threshold for the % operator
    PERFORM set_config('rdkit.tanimoto_threshold', threshold::TEXT, TRUE);

    RETURN QUERY
    SELECT
        b.comp_id,
        b.name,
        b.canonical_smiles,
        tanimoto_sml(
            morganbv_fp(b.mol),
            morganbv_fp(mol_from_smiles(query_smiles::cstring))
        )::FLOAT AS similarity
    FROM cc.brief_summary b
    WHERE b.mol IS NOT NULL
      AND morganbv_fp(b.mol) % morganbv_fp(mol_from_smiles(query_smiles::cstring))
    ORDER BY similarity DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION cc.similar_compounds IS
'Find compounds similar to query SMILES using Tanimoto similarity (Morgan fingerprints).
Arguments:
  query_smiles: SMILES string to search for
  threshold: Minimum Tanimoto similarity (default 0.7)
  limit_count: Maximum number of results (default 100)
Example:
  SELECT * FROM cc.similar_compounds(''CC(=O)Oc1ccccc1C(=O)O'', 0.7, 20);';


-- Dice similarity search using Morgan fingerprints
-- Alternative to Tanimoto, often preferred for fragment-based searches
CREATE OR REPLACE FUNCTION cc.similar_compounds_dice(
    query_smiles TEXT,
    threshold FLOAT DEFAULT 0.5,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    comp_id TEXT,
    name TEXT,
    smiles TEXT,
    similarity FLOAT
) AS $$
BEGIN
    -- Set dice threshold for the # operator
    PERFORM set_config('rdkit.dice_threshold', threshold::TEXT, TRUE);

    RETURN QUERY
    SELECT
        b.comp_id,
        b.name,
        b.canonical_smiles,
        dice_sml(
            morganbv_fp(b.mol),
            morganbv_fp(mol_from_smiles(query_smiles::cstring))
        )::FLOAT AS similarity
    FROM cc.brief_summary b
    WHERE b.mol IS NOT NULL
      AND morganbv_fp(b.mol) # morganbv_fp(mol_from_smiles(query_smiles::cstring))
    ORDER BY similarity DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION cc.similar_compounds_dice IS
'Find compounds similar to query SMILES using Dice similarity (Morgan fingerprints).
Arguments:
  query_smiles: SMILES string to search for
  threshold: Minimum Dice similarity (default 0.5)
  limit_count: Maximum number of results (default 100)
Example:
  SELECT * FROM cc.similar_compounds_dice(''c1ccccc1'', 0.5, 20);';


-- =============================================================================
-- Substructure Search Functions
-- =============================================================================

-- Substructure search using SMARTS pattern
CREATE OR REPLACE FUNCTION cc.substructure_search(
    query_smarts TEXT,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    comp_id TEXT,
    name TEXT,
    smiles TEXT
) AS $$
    SELECT b.comp_id, b.name, b.canonical_smiles
    FROM cc.brief_summary b
    WHERE b.mol @> query_smarts::qmol
    LIMIT limit_count;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION cc.substructure_search IS
'Find compounds containing the query substructure (SMARTS pattern).
Arguments:
  query_smarts: SMARTS pattern to search for
  limit_count: Maximum number of results (default 100)
Examples:
  -- Find compounds with benzene ring
  SELECT * FROM cc.substructure_search(''c1ccccc1'', 50);
  -- Find compounds with carboxylic acid
  SELECT * FROM cc.substructure_search(''C(=O)O'', 100);';


-- Exact structure match
CREATE OR REPLACE FUNCTION cc.exact_match(
    query_smiles TEXT
)
RETURNS TABLE (
    comp_id TEXT,
    name TEXT,
    smiles TEXT
) AS $$
    SELECT b.comp_id, b.name, b.canonical_smiles
    FROM cc.brief_summary b
    WHERE b.mol @= mol_from_smiles(query_smiles::cstring);
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION cc.exact_match IS
'Find compounds with exact structure match.
Arguments:
  query_smiles: SMILES string to match exactly
Example:
  SELECT * FROM cc.exact_match(''CCO'');  -- Find ethanol';


-- =============================================================================
-- Utility Functions
-- =============================================================================

-- Get compound by ID with similarity to a reference
CREATE OR REPLACE FUNCTION cc.compound_similarity(
    target_comp_id TEXT,
    reference_smiles TEXT
)
RETURNS FLOAT AS $$
    SELECT tanimoto_sml(
        morganbv_fp(b.mol),
        morganbv_fp(mol_from_smiles(reference_smiles::cstring))
    )::FLOAT
    FROM cc.brief_summary b
    WHERE b.comp_id = target_comp_id
      AND b.mol IS NOT NULL;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION cc.compound_similarity IS
'Calculate Tanimoto similarity between a compound and a reference SMILES.
Arguments:
  target_comp_id: Component ID (e.g., ''ATP'')
  reference_smiles: SMILES string to compare against
Example:
  SELECT cc.compound_similarity(''ADP'', (SELECT canonical_smiles FROM cc.brief_summary WHERE comp_id = ''ATP''));';


-- Find similar compounds to an existing component
CREATE OR REPLACE FUNCTION cc.similar_to_compound(
    reference_comp_id TEXT,
    threshold FLOAT DEFAULT 0.7,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    comp_id TEXT,
    name TEXT,
    smiles TEXT,
    similarity FLOAT
) AS $$
DECLARE
    ref_smiles TEXT;
BEGIN
    -- Get SMILES for reference compound
    SELECT canonical_smiles INTO ref_smiles
    FROM cc.brief_summary
    WHERE comp_id = reference_comp_id;

    IF ref_smiles IS NULL THEN
        RAISE EXCEPTION 'Compound % not found or has no SMILES', reference_comp_id;
    END IF;

    RETURN QUERY
    SELECT * FROM cc.similar_compounds(ref_smiles, threshold, limit_count)
    WHERE similar_compounds.comp_id != reference_comp_id;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION cc.similar_to_compound IS
'Find compounds similar to an existing component by ID.
Arguments:
  reference_comp_id: Component ID to find similar compounds for
  threshold: Minimum Tanimoto similarity (default 0.7)
  limit_count: Maximum number of results (default 100)
Example:
  SELECT * FROM cc.similar_to_compound(''ATP'', 0.6, 50);';
