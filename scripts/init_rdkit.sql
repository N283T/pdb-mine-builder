-- RDKit PostgreSQL Cartridge initialization
-- Run this after creating the database and before loading data

-- Enable RDKit extension
CREATE EXTENSION IF NOT EXISTS rdkit;

-- Add mol column to brief_summary (derived from canonical_smiles)
-- This column stores the RDKit molecule object for chemical searches
DO $$
BEGIN
    -- Check if column exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'cc'
        AND table_name = 'brief_summary'
        AND column_name = 'mol'
    ) THEN
        ALTER TABLE cc.brief_summary
        ADD COLUMN mol mol GENERATED ALWAYS AS (
            CASE
                WHEN canonical_smiles IS NOT NULL AND is_valid_smiles(canonical_smiles)
                THEN mol_from_smiles(canonical_smiles::cstring)
                ELSE NULL
            END
        ) STORED;
    END IF;
END $$;

-- Create GiST index for substructure/similarity searches
CREATE INDEX IF NOT EXISTS brief_summary_mol_idx
ON cc.brief_summary USING gist(mol);

-- Create index on Morgan fingerprints for similarity searches
-- Note: morganbv_fp() computes fingerprint on-the-fly from mol column
-- For frequent similarity searches, consider a materialized fingerprint column

-- Example queries:
--
-- Substructure search:
--   SELECT comp_id, name FROM cc.brief_summary
--   WHERE mol @> 'c1ccccc1'::mol;
--
-- Similarity search (Tanimoto > 0.8):
--   SELECT comp_id, name, tanimoto_sml(morganbv_fp(mol), morganbv_fp('CCO'::mol)) as similarity
--   FROM cc.brief_summary
--   WHERE morganbv_fp(mol) % morganbv_fp('CCO'::mol)
--   ORDER BY similarity DESC;
--
-- Valid SMILES check:
--   SELECT comp_id, canonical_smiles
--   FROM cc.brief_summary
--   WHERE canonical_smiles IS NOT NULL AND NOT is_valid_smiles(canonical_smiles);
