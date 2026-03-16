-- RDKit SQL functions for unified chemical search (chem schema)
--
-- Searches across both CCD and PRD compounds in chem.compounds.
--
-- Prerequisites:
--   - RDKit extension enabled
--   - chem.compounds table with mol column

-- =============================================================================
-- Similarity Search Functions
-- =============================================================================

-- Tanimoto similarity search using Morgan fingerprints
CREATE OR REPLACE FUNCTION chem.similar_compounds(
    query_smiles TEXT,
    threshold FLOAT DEFAULT 0.7,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    id TEXT,
    source TEXT,
    name TEXT,
    smiles TEXT,
    similarity FLOAT
) AS $$
BEGIN
    PERFORM set_config('rdkit.tanimoto_threshold', threshold::TEXT, TRUE);

    RETURN QUERY
    SELECT
        c.id,
        c.source,
        c.name,
        c.canonical_smiles,
        tanimoto_sml(
            morganbv_fp(c.mol),
            morganbv_fp(mol_from_smiles(query_smiles::cstring))
        )::FLOAT AS similarity
    FROM chem.compounds c
    WHERE c.mol IS NOT NULL
      AND morganbv_fp(c.mol) % morganbv_fp(mol_from_smiles(query_smiles::cstring))
    ORDER BY similarity DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION chem.similar_compounds IS
'Find compounds (cc + prd) similar to query SMILES using Tanimoto similarity.
Arguments:
  query_smiles: SMILES string to search for
  threshold: Minimum Tanimoto similarity (default 0.7)
  limit_count: Maximum number of results (default 100)
Example:
  SELECT * FROM chem.similar_compounds(''CC(=O)Oc1ccccc1C(=O)O'', 0.7, 20);';


-- =============================================================================
-- Substructure Search Functions
-- =============================================================================

-- Substructure search using SMARTS pattern
CREATE OR REPLACE FUNCTION chem.substructure_search(
    query_smarts TEXT,
    limit_count INT DEFAULT 100
)
RETURNS TABLE (
    id TEXT,
    source TEXT,
    name TEXT,
    smiles TEXT
) AS $$
    SELECT c.id, c.source, c.name, c.canonical_smiles
    FROM chem.compounds c
    WHERE c.mol @> query_smarts::qmol
    LIMIT limit_count;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION chem.substructure_search IS
'Find compounds (cc + prd) containing the query substructure.
Arguments:
  query_smarts: SMARTS pattern to search for
  limit_count: Maximum number of results (default 100)
Example:
  SELECT * FROM chem.substructure_search(''c1ccccc1'', 50);';


-- Exact structure match
CREATE OR REPLACE FUNCTION chem.exact_match(
    query_smiles TEXT
)
RETURNS TABLE (
    id TEXT,
    source TEXT,
    name TEXT,
    smiles TEXT
) AS $$
    SELECT c.id, c.source, c.name, c.canonical_smiles
    FROM chem.compounds c
    WHERE c.mol @= mol_from_smiles(query_smiles::cstring);
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION chem.exact_match IS
'Find compounds with exact structure match across cc and prd.
Arguments:
  query_smiles: SMILES string to match exactly
Example:
  SELECT * FROM chem.exact_match(''CCO'');';
