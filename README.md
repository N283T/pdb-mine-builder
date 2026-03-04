# MINE2 Updater

RDB updater for MINE2 database. Synchronizes structural biology data from PDBj (Protein Data Bank Japan) via rsync and loads it into PostgreSQL.

## Features

- Multi-process parallel data loading with configurable workers
- Schema-driven database management from YAML definitions
- Support for multiple data formats (CIF default, mmJSON optional)
- 10 data pipelines: CIF default for dual-format pipelines, `-json` suffix for mmJSON
- Works seamlessly with wwPDB/PDBj mirrored data

## Requirements

- Python 3.12+
- PostgreSQL 17+ with RDKit extension
- [Pixi](https://pixi.sh/) (package manager)
- rsync (for data synchronization)

## Installation

```bash
git clone https://github.com/N283T/mine2updater-ng.git
cd mine2updater-ng
pixi install
```

## Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Default PostgreSQL settings are in `pixi.toml` (`[activation.env]`).

## Configuration

Copy and edit `config.yml`:

```yaml
rdb:
  nworkers: 8
  constring: "dbname='mine2' user='pdbj' port=5433"

pipelines:
  pdbj:
    deffile: ${CWD}schemas/pdbj.def.yml
    data: /path/to/pdb/mmjson-noatom/
    data-plus: /path/to/pdb/mmjson-plus/
  cc:
    deffile: ${CWD}schemas/cc.def.yml
    data: /path/to/cc/mmjson/
  # ... other pipelines
```

- `${CWD}` resolves to the repository root
- `config.test.yml` is used for testing with limited data

## Usage

```bash
# Show help
pixi run mine2 --help

# Sync data from PDBj
pixi run mine2 sync [targets...]
# Targets: pdbj (CIF), pdbj-json (mmJSON), pdbj-plus, cc, cc-json,
#          ccmodel, ccmodel-json, prd, prd-json, vrpt, contacts,
#          sifts, schemas

# Update database
pixi run mine2 update [pipelines...]
# Pipelines: pdbj (CIF), pdbj-json (mmJSON), cc, cc-json, ccmodel,
#            ccmodel-json, prd, prd-json, vrpt, contacts, sifts

# Full update (sync + update)
pixi run mine2 all

# Test with limited data
pixi run mine2 test -p pdbj,cc -n 10
```

### Examples

```bash
# Sync all data
pixi run mine2 sync

# Sync specific targets
pixi run mine2 sync pdbj cc prd

# Update all pipelines
pixi run mine2 update

# Update specific pipelines
pixi run mine2 update pdbj cc

# Update with entry limit
pixi run mine2 update pdbj --limit 100
```

## Pipelines

### Default Pipelines (CIF)

CIF is the default format for dual-format pipelines:

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj | Main structure data from mmCIF (~248k files) | CIF |
| cc | Chemical component dictionary (components.cif.gz) | CIF |
| ccmodel | Chemical component models (chem_comp_model.cif.gz) | CIF |
| prd | BIRD data (prd-all.cif.gz + prdcc-all.cif.gz) | CIF |
| vrpt | Validation reports | CIF |
| contacts | Protein-protein contact data | JSON |
| sifts | Cross-references (Pfam, InterPro, GO, UniProt, etc.) | TTL (RDF) |

### mmJSON Pipelines (Optional)

For users who prefer mmJSON format, use the `-json` suffix:

| Pipeline | Description | Data Format |
|----------|-------------|-------------|
| pdbj-json | Main structure data (mmjson-noatom + mmjson-plus) | mmJSON |
| cc-json | Chemical component dictionary | mmJSON |
| ccmodel-json | Chemical component model data | mmJSON |
| prd-json | BIRD data | mmJSON |

### Backward Compatibility

Legacy pipeline names (`pdbj-cif`, `cc-cif`, etc.) are still accepted but deprecated.
They will emit a warning and run the corresponding CIF pipeline.

### Plus Data Support (pdbj pipeline)

Both CIF and mmJSON pdbj pipelines can merge PDBj-specific plus data when configured:

```yaml
# config.yml
pipelines:
  pdbj:
    deffile: ${CWD}schemas/pdbj.def.yml
    data: /path/to/mmCIF/             # CIF files
    data-plus: /path/to/mmjson-plus/  # Plus data (mmJSON format)
```

Plus data adds PDBj-specific annotations:
- `gene_ontology_pdbmlplus` - Gene Ontology (GO) annotations
- `struct_ref_pdbmlplus` - Additional UniProt reference data
- `citation_pdbmlplus`, `refine_pdbmlplus`, etc. (18 total categories)

| Configuration | CIF Pipeline | mmJSON Pipeline |
|---------------|--------------|-----------------|
| Without `data-plus` | Standard mmCIF only | `mmjson-noatom` only |
| With `data-plus` | CIF + plus data merged | `mmjson-noatom` + plus merged |

### Unsupported Pipelines

The following data types have schema definitions but are **not implemented** as pipelines:

| Schema | Status | Notes |
|--------|--------|-------|
| ihm | Not supported | Integrative/hybrid methods (I/HM) data |
| emdb | Not supported | Electron Microscopy Data Bank |

These may be added in future versions if needed.

### Removed from Original

The following feature from the original mine2updater is **not included**:

| Feature | Reason |
|---------|--------|
| `dictionaries` sync target | CIF dictionary files were used for type conversion during parsing. In mine2updater-ng, type information is defined in YAML schema files and gemmi handles CIF parsing internally, making the dictionaries unnecessary. |

## Database Management

```bash
# Initialize PostgreSQL data directory
pixi run db-init

# Start/stop/status
pixi run db-start
pixi run db-stop
pixi run db-status
```

### RDKit Extension Setup

RDKit extension, mol column, and SQL functions are **automatically configured** when running the `cc` or `cc-json` pipeline.

To setup RDKit functions independently (without running the full pipeline):

```bash
pixi run mine2 setup-rdkit
```

> **Note**: Requires superuser privileges for initial `CREATE EXTENSION rdkit`.
> If auto-setup fails, run manually: `psql -d mine2 -f scripts/init_rdkit.sql`

### Chemical Search Functions

The following SQL functions are available in the `cc` schema:

| Function | Description |
|----------|-------------|
| `cc.similar_compounds(smiles, threshold, limit)` | Tanimoto similarity search (Morgan FP) |
| `cc.similar_compounds_dice(smiles, threshold, limit)` | Dice similarity search |
| `cc.substructure_search(smarts, limit)` | Substructure search (SMARTS) |
| `cc.exact_match(smiles)` | Exact structure match |
| `cc.similar_to_compound(comp_id, threshold, limit)` | Find compounds similar to existing component |
| `cc.compound_similarity(comp_id, smiles)` | Calculate similarity between component and SMILES |

### Molecular Descriptors

The `cc.brief_summary` table includes RDKit-calculated molecular descriptors:

| Column | Type | Description |
|--------|------|-------------|
| `rdkit_mw` | double | Average molecular weight |
| `rdkit_logp` | double | Wildman-Crippen LogP |
| `rdkit_tpsa` | double | Topological polar surface area |
| `rdkit_hba` | int | Hydrogen bond acceptors |
| `rdkit_hbd` | int | Hydrogen bond donors |
| `rdkit_rotbonds` | int | Rotatable bonds |
| `rdkit_rings` | int | Number of rings |
| `rdkit_formula` | text | Molecular formula |

> **Note**: Descriptors are NULL when `mol` column is NULL (invalid SMILES).

### Usage Examples

```sql
-- Find compounds similar to aspirin (Tanimoto >= 0.7)
SELECT * FROM cc.similar_compounds('CC(=O)Oc1ccccc1C(=O)O', 0.7, 20);

-- Find compounds containing benzene ring
SELECT * FROM cc.substructure_search('c1ccccc1', 50);

-- Find compounds similar to ATP
SELECT * FROM cc.similar_to_compound('ATP', 0.6, 50);

-- Lipinski's Rule of Five filter (drug-like compounds)
SELECT comp_id, name, rdkit_mw, rdkit_logp, rdkit_hba, rdkit_hbd
FROM cc.brief_summary
WHERE rdkit_mw < 500
  AND rdkit_logp < 5
  AND rdkit_hba <= 10
  AND rdkit_hbd <= 5;

-- Combine similarity search with property filter
SELECT s.*, b.rdkit_mw, b.rdkit_logp
FROM cc.similar_compounds('c1ccccc1C(=O)O', 0.5, 100) s
JOIN cc.brief_summary b USING (comp_id)
WHERE b.rdkit_mw BETWEEN 100 AND 300;

-- Direct RDKit operators (for advanced queries)
SELECT comp_id, name FROM cc.brief_summary
WHERE mol @> 'C(=O)O'::qmol;  -- Carboxylic acid substructure
```

### SIFTS Cross-References

The SIFTS pipeline provides cross-references from PDB entries to external databases.
Data is sourced from [SIFTS (PDBe)](https://www.ebi.ac.uk/pdbe/docs/sifts/) via PDBj RDF/TTL files.

> **Note**: This is a mine2updater-ng specific feature. PDBj's original MINE2 database
> does not include SIFTS tables. We load the RDF/TTL data into PostgreSQL for convenient
> SQL access and JOINs with other pdbj tables.

| Table | Description |
|-------|-------------|
| `sifts.pdb_pfam` | PDB entity → Pfam domain |
| `sifts.pdb_interpro` | PDB entity → InterPro |
| `sifts.pdb_go` | PDB entity → Gene Ontology |
| `sifts.pdb_enzyme` | PDB entity → EC number |
| `sifts.pdb_taxonomy` | PDB entity → NCBI Taxonomy |
| `sifts.pdb_uniprot_short` | PDB entity → UniProt (simple) |
| `sifts.pdb_uniprot` | PDB entity → UniProt (residue range mapping) |
| `sifts.pdb_cath` | PDB entity → CATH |
| `sifts.pdb_scop` | PDB entity → SCOP |
| `sifts.pdb_pubmed` | PDB entry → PubMed |

#### Usage Examples

```sql
-- Find all Pfam domains for a structure
SELECT * FROM sifts.pdb_pfam WHERE pdbid = '1crn';

-- Find structures with a specific Pfam domain
SELECT DISTINCT pdbid FROM sifts.pdb_pfam WHERE pfam_id = 'PF00042';

-- Find human (taxonomy 9606) structures
SELECT DISTINCT pdbid FROM sifts.pdb_taxonomy WHERE taxonomy_id = 9606;

-- Find structures with GO molecular function annotation
SELECT DISTINCT pdbid FROM sifts.pdb_go WHERE go_id = '0004601';

-- Join with pdbj schema for structure details
SELECT p.pdbid, p.title, f.pfam_id
FROM pdbj.brief_summary p
JOIN sifts.pdb_pfam f ON p.pdbid = f.pdbid
WHERE p.resolution < 2.0;

-- UniProt residue range mapping (pdb_uniprot)
SELECT * FROM sifts.pdb_uniprot WHERE pdbid = '102l';
-- Returns: pdbid=102l, entity_id=1, pdb_start=1, pdb_end=40, uniprot_id=P00720, uniprot_start=1, uniprot_end=40
--          pdbid=102l, entity_id=1, pdb_start=42, pdb_end=165, uniprot_id=P00720, uniprot_start=41, uniprot_end=164
```

## Development

```bash
# Lint
pixi run lint

# Format
pixi run format

# Type check
pixi run typecheck

# Run tests
pixi run test

# All checks
pixi run check
```

## Project Structure

```
mine2updater-ng/
├── src/mine2/
│   ├── __main__.py      # CLI entry point
│   ├── cli.py           # Typer CLI commands
│   ├── config.py        # Configuration (Pydantic)
│   ├── db/
│   │   ├── connection.py # Connection pool
│   │   └── loader.py     # Parallel data loader
│   ├── parsers/
│   │   ├── cif.py       # Unified parser (CIF + mmJSON via gemmi)
│   │   └── mmjson.py    # Utilities (normalize_column_name, merge_data)
│   └── pipelines/
│       ├── base.py      # Base pipeline class
│       ├── pdbj.py      # PDB structure data
│       ├── cc.py        # Chemical components
│       ├── ccmodel.py   # Component models
│       ├── prd.py       # BIRD data
│       ├── vrpt.py      # Validation reports
│       └── contacts.py  # Contact data
├── schemas/             # Database schema definitions
├── tests/               # Unit tests (pytest)
├── scripts/             # Utility scripts
├── config.yml           # Production config
├── config.test.yml      # Test config
└── pixi.toml            # Pixi configuration
```

## License

GNU LGPLv3 - See [LICENSE](LICENSE) for details.
