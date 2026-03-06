---
sidebar_position: 2
---

# Configuration

pdb-mine-builder uses a YAML configuration file to define database connections and pipeline settings.

## config.yml

Create `config.yml` in the project root (it is gitignored). Here is a full example:

```yaml
rdb:
  nworkers: 8
  constring: "dbname='pmb' user='pdbj' port=5433"

pipelines:
  pdbj:
    format: cif
    data: /data/pdb/structures/divided/mmCIF/
    data-plus: /data/pdb/mmjson-plus/
  cc:
    format: cif
    data: /data/pdb/monomers/
  ccmodel:
    format: cif
    data: /data/pdb/component-models/complete/
  prd:
    format: cif
    data: /data/pdb/bird/prd/
  vrpt:
    data: /data/pdb/validation_reports/
  contacts:
    data: /data/pdb/contacts/
```

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
| `data` | Path to the data directory or file |
| `format` | `cif` (default) or `mmjson` -- only for dual-format pipelines |

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

The `pdbj` pipeline optionally merges PDBj-specific annotations (Gene Ontology, UniProt references, etc.) from plus data:

```yaml
pipelines:
  pdbj:
    format: cif
    data: /data/pdb/structures/divided/mmCIF/
    data-plus: /data/pdb/mmjson-plus/          # Optional
```

When `data-plus` is omitted, only standard structure data is loaded.

## Variable Expansion

The special variable `${CWD}` expands to the repository root directory. This is useful for test configurations or portable setups:

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
