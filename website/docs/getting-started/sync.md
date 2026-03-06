---
sidebar_position: 3
---

# Syncing Data

The `sync` command downloads data from PDBj (Protein Data Bank Japan) servers using rsync.

## How It Works

pdb-mine-builder mirrors data from PDBj's public rsync servers into your local data directory. Only changed files are transferred on subsequent runs, making incremental syncs fast.

## Usage

```bash
# Sync all targets
pixi run pmb sync

# Sync specific targets
pixi run pmb sync pdbj cc prd

# Preview what would be synced (no actual download)
pixi run pmb sync --dry-run
pixi run pmb sync pdbj --dry-run
```

## Available Sync Targets

### CIF Targets (Default)

| Target | Source | Description |
|--------|--------|-------------|
| `pdbj` | `rsync.pdbj.org::ftp_data/structures/divided/mmCIF/` | mmCIF structure files (~248k files) |
| `cc` | `rsync.pdbj.org::ftp_data/monomers/components.cif.gz` | Chemical component dictionary (single file) |
| `ccmodel` | `rsync.pdbj.org::ftp_data/component-models/complete/chem_comp_model.cif.gz` | Chemical component models (single file) |
| `prd` | `rsync.pdbj.org::ftp_data/bird/prd/` | BIRD reference dictionary |
| `vrpt` | `rsync.pdbj.org::ftp_data/validation_reports/` | Validation reports (`*_validation.cif.gz` only) |

### mmJSON Targets

| Target | Source | Description |
|--------|--------|-------------|
| `pdbj-json` | `rsync.pdbj.org::ftp_data/structures/divided/mmjson-noatom/` | Structure data in mmJSON format |
| `cc-json` | `rsync.pdbj.org::ftp_data/component-models/complete/chem_comp-mmjson/` | Chemical components in mmJSON |
| `ccmodel-json` | `rsync.pdbj.org::ftp_data/component-models/complete/chem_comp_model-mmjson/` | Component models in mmJSON |
| `prd-json` | `rsync.pdbj.org::ftp_data/bird/mmjson/` | BIRD data in mmJSON |

### Other Targets

| Target | Source | Description |
|--------|--------|-------------|
| `pdbj-plus` | `rsync.pdbj.org::mine/ftp_data/mine_data/mmjson-plus/` | PDBj-specific plus annotations (mmJSON) |
| `contacts` | `rsync.pdbj.org::mine/ftp_data/mine_data/contacts/` | Protein-protein contact data (JSON) |
| `schemas` | `rsync.pdbj.org::mine/ftp_data/mine_data/sql/pdb/schemas/` | Database schema definitions |

:::tip
You only need to sync the targets that match your chosen format. If you use CIF (the default), you do not need the `-json` targets.
:::

## Data Directory Structure

After syncing, data is stored under the `data_dir` configured in your settings. A typical layout looks like:

```
<data_dir>/
├── data/
│   ├── structures/divided/mmCIF/   # pdbj (CIF)
│   ├── mmjson-noatom/              # pdbj-json
│   ├── monomers/                   # cc (CIF)
│   ├── cc/                         # cc-json
│   ├── component-models/complete/  # ccmodel (CIF)
│   ├── ccmodel/                    # ccmodel-json
│   ├── bird/prd/                   # prd (CIF)
│   ├── prd/                        # prd-json
│   └── contacts/                   # contacts
├── pdbj/pdbjplus/                  # pdbj-plus
├── validation_reports/             # vrpt
└── schemas/                        # schemas
```

## CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--config` | `-c` | Path to config file (default: `config.yml`) |
| `--dry-run` | `-n` | Show what would be synced without downloading |

## Disk Space Considerations

The full PDBj dataset is large. Approximate sizes:

- **pdbj** (mmCIF): ~100 GB (248k+ compressed files)
- **vrpt**: ~50 GB
- **cc**: ~1 GB (single compressed file)
- **contacts**: ~10 GB

:::note
Start with a small subset using the `update --limit` flag before syncing the full dataset. You can sync specific targets incrementally as needed.
:::
