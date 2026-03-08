---
sidebar_position: 3
---

# Syncing Data

The `sync` command downloads data using rsync. All sync targets (source URLs, destinations, and rsync options) are defined in `config.yml` under the `sync` section. There are no hardcoded defaults -- you have full control.

## How It Works

pdb-mine-builder runs rsync for each configured sync target. Only changed files are transferred on subsequent runs, making incremental syncs fast.

## Usage

```bash
# Sync all configured targets
pixi run pmb sync

# Sync specific targets
pixi run pmb sync pdbj cc prd

# Preview what would be synced (no actual download)
pixi run pmb sync --dry-run
pixi run pmb sync pdbj --dry-run
```

## Configuring Sync Targets

All sync targets are defined in the `sync` section of `config.yml`. Each target specifies:

- **source** (or **sources**): rsync source URL(s)
- **dest**: local destination directory
- **options**: rsync options (default: `["-av", "--size-only"]`)

```yaml
sync:
  pdbj:
    source: "data.pdbj.org::ftp_data/structures/divided/mmCIF/"
    dest: ${DATA_DIR}/data/structures/divided/mmCIF/
    options: ["-av", "--delete", "--size-only"]
  cc:
    source: "data.pdbj.org::ftp_data/monomers/components.cif.gz"
    dest: ${DATA_DIR}/data/monomers/
  prd:
    sources:
      - "data.pdbj.org::ftp_data/bird/prd/prd-all.cif.gz"
      - "data.pdbj.org::ftp_data/bird/prd/prdcc-all.cif.gz"
    dest: ${DATA_DIR}/data/bird/prd/
```

See [Configuration - Sync Targets](./configuration.md#sync-targets) and `config.example.yml` for the full list of available targets.

:::tip
You only need to configure the targets that match your chosen format. If you use CIF (the default), you do not need the mmJSON targets.
:::

### Regional Mirrors

The default `config.example.yml` uses PDBj (Japan) servers. For CIF targets, you can use a regional wwPDB mirror by changing the source URLs:

| Region | Server |
|--------|--------|
| Japan (PDBj) | `data.pdbj.org::ftp_data/...` |
| US (RCSB) | `rsync.rcsb.org::ftp_data/...` |
| Europe (PDBe) | `rsync.ebi.ac.uk::pub/databases/pdb/data/...` |

```yaml
sync:
  pdbj:
    # Change source to RCSB (US)
    source: "rsync.rcsb.org::ftp_data/structures/divided/mmCIF/"
    dest: ${DATA_DIR}/data/structures/divided/mmCIF/
```

### Multiple Sources

Some targets (e.g., `prd`) need multiple files. Use the `sources` field (list) instead of `source`:

```yaml
sync:
  prd:
    sources:
      - "data.pdbj.org::ftp_data/bird/prd/prd-all.cif.gz"
      - "data.pdbj.org::ftp_data/bird/prd/prdcc-all.cif.gz"
    dest: ${DATA_DIR}/data/bird/prd/
```

### Custom rsync Options

Each target can have custom rsync options. The default is `["-av", "--size-only"]`:

```yaml
sync:
  pdbj:
    source: "data.pdbj.org::ftp_data/structures/divided/mmCIF/"
    dest: ${DATA_DIR}/data/structures/divided/mmCIF/
    options: ["-av", "--delete", "--size-only"]  # add --delete to remove stale files
  vrpt:
    source: "data.pdbj.org::ftp/validation_reports/"
    dest: ${DATA_DIR}/validation_reports/
    options: ["-av", "--size-only", '--include="*/"', '--include="*_validation.cif.gz"', '--exclude="*"']
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
