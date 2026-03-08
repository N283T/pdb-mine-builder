---
sidebar_position: 2
---

# Configuration

pdb-mine-builder uses a YAML configuration file to define database connections and pipeline settings.

## config.yml

Copy the example config to get started:

```bash
cp config.example.yml config.yml
# Edit config.yml with your data paths
```

`config.yml` is gitignored. Here is a full example:

```yaml
# Base directory for synced data (used by pmb sync)
# Also available as ${DATA_DIR} in path values below.
# Priority: data-dir config > DATA_DIR env variable > current directory
data-dir: /path/to/data

rdb:
  nworkers: 8
  constring: "host=localhost port=5433 dbname=pmb user=pdbj"

# Sync targets - define rsync sources, destinations, and options.
# Only targets listed here will be synced by `pmb sync`.
sync:
  pdbj:
    source: "data.pdbj.org::ftp_data/structures/divided/mmCIF/"
    dest: ${DATA_DIR}/data/structures/divided/mmCIF/
    options: ["-av", "--delete", "--size-only"]
  cc:
    source: "data.pdbj.org::ftp_data/monomers/components.cif.gz"
    dest: ${DATA_DIR}/data/monomers/
  # ... see config.example.yml for all targets

pipelines:
  pdbj:
    format: cif
    data: ${DATA_DIR}/data/structures/divided/mmCIF/
    data-plus: ${DATA_DIR}/data/mmjson-plus/
    data-nextgen-plus: ${DATA_DIR}/data/pdb_nextgen/mmjson-plus/
  cc:
    format: cif
    data: ${DATA_DIR}/data/monomers/components.cif.gz
  ccmodel:
    format: cif
    data: ${DATA_DIR}/data/component-models/complete/chem_comp_model.cif.gz
  prd:
    format: cif
    data: ${DATA_DIR}/data/bird/prd/prd-all.cif.gz
    prdcc: ${DATA_DIR}/data/bird/prd/prdcc-all.cif.gz
  prd_family:
    data: ${DATA_DIR}/data/bird/family/family-all.cif.gz
  vrpt:
    data: ${DATA_DIR}/validation_reports/
  contacts:
    data: ${DATA_DIR}/data/contacts/
```

## Data Directory

The `data-dir` field sets the base directory for synced data. It is also available as `${DATA_DIR}` in path values.

| Priority | Source | Description |
|----------|--------|-------------|
| 1 | `data-dir` in config | Explicit path in config.yml |
| 2 | `DATA_DIR` env variable | Environment variable |
| 3 | Current directory | Fallback to CWD |

## Database Connection

The `rdb` section controls database access:

| Field | Description | Default |
|-------|-------------|---------|
| `constring` | PostgreSQL connection string (libpq format) | Required |
| `nworkers` | Number of parallel worker processes | Auto-detected from CPU count |

The `nworkers` value can be overridden per-command with the `--workers` flag.

## Pipeline Configuration

Each pipeline entry under `pipelines` defines where to find the source data and which format to use.

### Common Fields

| Field | Description |
|-------|-------------|
| `data` | Path to data file or directory (file path recommended for single-file pipelines) |
| `format` | `cif` (default) or `mmjson` -- only for dual-format pipelines |
| `data-plus` | PDBjPlus supplementary data directory (pdbj pipeline only, optional) |
| `data-nextgen-plus` | Nextgen PDBjPlus supplementary data directory (pdbj pipeline only, optional) |
| `prdcc` | PRDCC CIF file path (prd pipeline only, optional) |

### Format Selection

Four pipelines support both CIF and mmJSON formats: `pdbj`, `cc`, `ccmodel`, and `prd`. The format is controlled by the `format` field:

```yaml
pipelines:
  pdbj:
    format: cif      # Parse mmCIF files (default)
    data: /data/pdb/structures/divided/mmCIF/

  # Or use mmJSON:
  # pdbj:
  #   format: mmjson
  #   data: /data/pdb/mmjson-noatom/
```

Other pipelines (`vrpt`, `contacts`) use a fixed format and ignore the `format` field.

### Plus Data (pdbj pipeline)

The `pdbj` pipeline optionally merges PDBj-specific annotations from supplementary mmJSON files. There are two sources:

| Field | Description | Data Source |
|-------|-------------|-------------|
| `data-plus` | PDBjPlus annotations (Gene Ontology, citation metadata, etc.) | `mmjson-plus/` directory |
| `data-nextgen-plus` | Nextgen PDBjPlus annotations (SIFTS cross-references, etc.) | `pdb_nextgen/mmjson-plus/` directory |

```yaml
pipelines:
  pdbj:
    format: cif
    data: /data/pdb/structures/divided/mmCIF/
    data-plus: /data/pdb/mmjson-plus/                    # Optional
    data-nextgen-plus: /data/pdb_nextgen/mmjson-plus/    # Optional
```

Both are optional. When omitted, only standard structure data is loaded. When both are specified, data is merged sequentially (`data-plus` first, then `data-nextgen-plus`).

## Sync Targets

The `sync` section defines all rsync targets for `pmb sync`. Each target specifies source URL(s), destination, and rsync options. Only targets listed here will be synced.

### Target Fields

| Field | Description |
|-------|-------------|
| `source` | rsync source URL (single source) |
| `sources` | rsync source URLs (list, for targets with multiple files) |
| `dest` | Local destination directory |
| `options` | rsync options (default: `["-av", "--size-only"]`) |

Use either `source` (single URL) or `sources` (list of URLs), not both.

### Example

```yaml
sync:
  pdbj:
    source: "data.pdbj.org::ftp_data/structures/divided/mmCIF/"
    dest: ${DATA_DIR}/data/structures/divided/mmCIF/
    options: ["-av", "--delete", "--size-only"]
  prd:
    sources:
      - "data.pdbj.org::ftp_data/bird/prd/prd-all.cif.gz"
      - "data.pdbj.org::ftp_data/bird/prd/prdcc-all.cif.gz"
    dest: ${DATA_DIR}/data/bird/prd/
```

See `config.example.yml` for a complete list of all available targets with their default URLs and options. See [Syncing Data](./sync.md) for usage details and regional mirror configuration.

## Variable Expansion

Config values support `${VAR}` placeholders that are resolved at load time:

| Variable | Description |
|----------|-------------|
| `${CWD}` | Current working directory |
| `${DATA_DIR}` | Resolved from `data-dir` config or `DATA_DIR` env variable |
| `${HOME}` | User home directory |

```yaml
pipelines:
  pdbj:
    data: ${CWD}/data/mmjson-noatom/
    data-plus: ${CWD}/data/plus/
```

## Test Configuration

The file `config.test.yml` is provided for running tests against a local test database. It uses `${CWD}` paths pointing to fixture data in the repository:

```yaml
rdb:
  constring: "host='127.0.0.1' dbname='pmb_test' user='pdbj' password='test_password' port=15433"

pipelines:
  pdbj:
    format: cif
    data: ${CWD}/data/mmjson-noatom/
    data-plus: ${CWD}/data/plus/
  cc:
    format: cif
    data: ${CWD}/data/cc/
  # ... other pipelines
```

:::tip
To run the test database, use the Docker-based test DB:

```bash
pixi run test-db-up       # Start test PostgreSQL (port 15433)
pixi run test-db-status   # Check status
pixi run test-db-down     # Stop
```
:::
