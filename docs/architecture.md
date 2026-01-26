# Architecture

## Overview

mine2updater is a data loading system that synchronizes structural biology data from PDBj and loads it into PostgreSQL. The system is designed for high-throughput parallel processing.

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

#### mmJSON Parser (`parsers/mmjson.py`)

Parses PDBj's mmJSON format:
```json
{
  "data_100D": {
    "category_name": {
      "column1": ["val1", "val2"],
      "column2": ["val1", "val2"]
    }
  }
}
```

Key functions:
- `load_mmjson_file()`: Load and extract data block
- `get_rows()`: Convert column arrays to row dicts
- `normalize_column_name()`: Convert `col[1][2]` to `col12`

#### CIF Parser (`parsers/cif.py`)

Uses gemmi library to parse CIF files directly:
```python
doc = gemmi.cif.read_string(content)
```

Returns dict of category -> list of row dicts.

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
