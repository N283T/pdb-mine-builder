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
| `pdbj` | `data.pdbj.org::ftp_data/structures/divided/mmCIF/` | mmCIF structure files (~248k files) |
| `cc` | `data.pdbj.org::ftp_data/monomers/components.cif.gz` | Chemical component dictionary (single file) |
| `ccmodel` | `data.pdbj.org::ftp_data/component-models/complete/` | Chemical component models |
| `prd` | `data.pdbj.org::ftp_data/bird/prd/` | BIRD reference dictionary |
| `prd-family` | `data.pdbj.org::ftp_data/bird/family/` | BIRD family data |
| `vrpt` | `data.pdbj.org::ftp/validation_reports/` | Validation reports (`*_validation.cif.gz` only) |

### mmJSON Targets

| Target | Source | Description |
|--------|--------|-------------|
| `pdbj-json` | `data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson/` | Structure data in mmJSON format |
| `cc-json` | `data.pdbj.org::rsync/pdbjplus/data/cc/mmjson/` | Chemical components in mmJSON |
| `ccmodel-json` | `data.pdbj.org::rsync/pdbjplus/data/ccmodel/` | Component models in mmJSON |
| `prd-json` | `data.pdbj.org::rsync/pdbjplus/data/prd/` | BIRD data in mmJSON |

### Plus Data Targets

| Target | Source | Description |
|--------|--------|-------------|
| `pdbj-plus` | `data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-plus/` | PDBjPlus annotations (Gene Ontology, citation metadata, etc.) |
| `nextgen-plus` | `data.pdbj.org::rsync/pdbjplus/data/pdb_nextgen/mmjson-plus/` | Nextgen PDBjPlus annotations (SIFTS cross-references, etc.) |

### Other Targets

| Target | Source | Description |
|--------|--------|-------------|
| `contacts` | `data.pdbj.org::rsync/pdbjplus/data/pdb/contacts/` | Protein-protein contact data (JSON) |

:::tip
You only need to sync the targets that match your chosen format. If you use CIF (the default), you do not need the `-json` targets.
:::

### Regional Mirrors

CIF targets default to PDBj (Japan) servers. If you prefer a different wwPDB mirror (e.g., RCSB for US, PDBe for Europe), you can override the source URLs in `config.yml`:

```yaml
sync-sources:
  pdbj: "rsync.rcsb.org::ftp_data/structures/divided/mmCIF/"
  cc: "rsync.rcsb.org::ftp_data/monomers/components.cif.gz"
```

See [Configuration - Sync Source Overrides](./configuration.md#sync-source-overrides) for details.

## Data Directory Structure

Sync destinations are derived from your pipeline `data` paths in `config.yml`. This ensures sync and pipeline always point to the same location. For targets without pipeline config (mmJSON, etc.), the destination falls back to `data_dir` + a default path.

A typical layout looks like:

```
<data_dir>/
├── data/
│   ├── structures/divided/mmCIF/       # pdbj (CIF)
│   ├── monomers/                       # cc (CIF)
│   ├── component-models/complete/      # ccmodel (CIF)
│   ├── bird/prd/                       # prd (CIF)
│   ├── bird/family/                    # prd-family (CIF)
│   ├── mmjson-noatom/                  # pdbj-json
│   ├── cc/                             # cc-json
│   ├── ccmodel/                        # ccmodel-json
│   ├── prd/                            # prd-json
│   ├── mmjson-plus/                    # pdbj-plus
│   ├── pdb_nextgen/mmjson-plus/        # nextgen-plus
│   └── contacts/                       # contacts
└── validation_reports/                 # vrpt
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
