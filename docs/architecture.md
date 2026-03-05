# Architecture

## Overview

pdb-mine-builder is a data loading system that synchronizes structural biology data from PDBj and loads it into PostgreSQL. The system is designed for high-throughput parallel processing.

```
PDBj Servers
     │
     │ rsync
     ▼
Local Data Files (mmJSON/CIF/JSON)
     │
     │ parse
     ▼
Pipeline Processing (multi-process)
     │
     │ bulk upsert
     ▼
PostgreSQL Database
```

## Components

### CLI (`cli.py`)

Entry point using Typer. Provides commands:
- `sync`: rsync data from PDBj
- `update`: Run pipelines to load data
- `all`: Sync + update
- `test`: Test pipelines with limited data

### Configuration (`config.py`)

Pydantic-based configuration with:
- Database settings (workers, connection string)
- Pipeline definitions (schema file, data paths)
- Environment variable expansion (`${CWD}`)

### Parsers

Both CIF and mmJSON formats are parsed through gemmi, providing a unified row-oriented output format.

#### Unified Parser (`parsers/cif.py`)

Uses gemmi library to parse both CIF and mmJSON files:

```python
from pdbminebuilder.parsers.cif import parse_cif_file, parse_mmjson_file

# CIF files (supports .cif.gz automatically)
data = parse_cif_file(filepath)

# mmJSON files (supports .json.gz automatically)
data = parse_mmjson_file(filepath)

# Both return: {"category": [{"col": "val", ...}, ...], "_block_name": "..."}
```

Key functions:
- `parse_cif_file()`: Parse CIF files via `gemmi.cif.read()`
- `parse_mmjson_file()`: Parse mmJSON files via `gemmi.cif.read_mmjson()`
- `parse_mmjson_file_blocks()`: Parse multi-block mmJSON (for PRD files)

#### Utilities (`parsers/mmjson.py`)

Helper functions for data processing:
- `normalize_column_name()`: Convert `col[1][2]` to `col12`
- `merge_data()`: Merge row-oriented data dicts (for pdbj noatom + plus)

### Database Layer

#### Connection Pool (`db/connection.py`)

- Thread-safe connection pool using psycopg
- Configurable pool size
- Automatic connection recycling

#### Loader (`db/loader.py`)

Parallel data loading with ProcessPoolExecutor:

```python
with ProcessPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_job, job): job for job in jobs}
```

Key functions:
- `run_loader()`: Orchestrate parallel processing
- `ensure_schema()`: Create/update database schema
- `bulk_upsert()`: Insert or update rows efficiently

### Pipelines

Base class pattern with template method:

```python
class BasePipeline(ABC):
    def run(self, limit=None):
        jobs = self.find_jobs(limit)
        results = run_loader(jobs, self.process_job)
        return results

    @abstractmethod
    def process_job(self, job, schema_def, conninfo):
        pass
```

Each pipeline implements:
- `extract_entry_id()`: Get ID from filename
- `process_job()`: Parse file and load tables
- `find_jobs()` (optional): Custom file discovery

## Data Flow

1. **Job Discovery**: Find data files matching pattern
2. **Parallel Processing**: Distribute jobs to workers
3. **Parsing**: Convert file format to row dicts
4. **Transformation**: Normalize columns, add primary keys
5. **Loading**: Bulk upsert to database

## Schema Definition

YAML-based schema definitions:

```yaml
schema_name: pdbj
primary_key: pdbid

tables:
  - name: brief_summary
    primary_key: [pdbid]
    columns:
      - [pdbid, TEXT]
      - [title, TEXT]

  - name: entity
    primary_key: [pdbid, id]
    columns:
      - [pdbid, TEXT]
      - [id, TEXT]
      - [type, TEXT]
```

## Error Handling

- Per-entry error tracking with `LoaderResult`
- Traceback included in error messages
- Failed entries don't stop other processing
- Summary of success/failure at end

## Performance Considerations

1. **Parallel Processing**: Configurable worker count
2. **Bulk Operations**: `executemany` for batch inserts
3. **Connection Per Worker**: Avoid pool contention
4. **Sorted File Order**: Consistent processing order
