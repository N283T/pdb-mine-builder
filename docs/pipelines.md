# Pipeline Development Guide

## Creating a New Pipeline

### 1. Define Schema

Create `schemas/<name>.def.yml`:

```yaml
schema_name: mydata
primary_key: entry_id

tables:
  - name: brief_summary
    primary_key: [entry_id]
    columns:
      - [entry_id, TEXT]
      - [title, TEXT]

  - name: detail
    primary_key: [entry_id, seq_id]
    columns:
      - [entry_id, TEXT]
      - [seq_id, INTEGER]
      - [value, REAL]
```

### 2. Add Configuration

Edit `config.yml`:

```yaml
pipelines:
  mydata:
    deffile: ${CWD}schemas/mydata.def.yml
    data: /path/to/data/
```

### 3. Create Pipeline Module

Create `src/mine2/pipelines/mydata.py`:

```python
"""My data pipeline."""

import traceback
from pathlib import Path
from typing import Any

from rich.console import Console

from mine2.config import PipelineConfig, Settings
from mine2.db.loader import Job, LoaderResult, SchemaDef, TableDef, bulk_upsert
from mine2.parsers.cif import parse_mmjson_file
from mine2.parsers.mmjson import normalize_column_name
from mine2.pipelines.base import BasePipeline, transform_category

console = Console()


class MydataPipeline(BasePipeline):
    """Pipeline for loading my data."""

    name = "mydata"
    file_pattern = "*.json.gz"

    def extract_entry_id(self, filepath: Path) -> str:
        """Extract entry ID from filename."""
        name = filepath.name
        if name.endswith(".json.gz"):
            name = name[:-8]
        return name

    def process_job(
        self,
        job: Job,
        schema_def: SchemaDef,
        conninfo: str,
    ) -> LoaderResult:
        """Process a single entry."""
        try:
            data = parse_mmjson_file(job.filepath)
            rows_inserted = 0

            # Load brief_summary
            brief_rows = self._generate_brief_summary(data, job.entry_id)
            if brief_rows:
                columns = list(brief_rows[0].keys())
                inserted, _ = bulk_upsert(
                    conninfo,
                    schema_def.schema_name,
                    "brief_summary",
                    columns,
                    [tuple(r[c] for c in columns) for r in brief_rows],
                    ["entry_id"],
                )
                rows_inserted += inserted

            # Load other tables
            for table in schema_def.tables:
                if table.name == "brief_summary":
                    continue

                rows = data.get(table.name, [])
                category_rows = transform_category(
                    rows, table, job.entry_id, schema_def.primary_key, normalize_column_name
                )
                if category_rows:
                    columns = list(category_rows[0].keys())
                    inserted, _ = bulk_upsert(
                        conninfo,
                        schema_def.schema_name,
                        table.name,
                        columns,
                        [tuple(r[c] for c in columns) for r in category_rows],
                        table.primary_key,
                    )
                    rows_inserted += inserted

            return LoaderResult(
                entry_id=job.entry_id,
                success=True,
                rows_inserted=rows_inserted,
            )

        except Exception as e:
            error_msg = f"{e}\n{traceback.format_exc()}"
            return LoaderResult(
                entry_id=job.entry_id,
                success=False,
                error=error_msg,
            )

    def _generate_brief_summary(
        self, data: dict[str, Any], entry_id: str
    ) -> list[dict]:
        """Generate brief_summary from data."""
        rows = data.get("main_category", [])
        if not rows:
            return [{"entry_id": entry_id}]

        return [
            {
                "entry_id": entry_id,
                "title": rows[0].get("title"),
            }
        ]


def run(
    settings: Settings,
    config: PipelineConfig,
    schema_def: SchemaDef,
    limit: int | None = None,
) -> list[LoaderResult]:
    """Run the mydata pipeline."""
    pipeline = MydataPipeline(settings, config, schema_def)
    return pipeline.run(limit)
```

### 4. Register Pipeline

Edit `src/mine2/cli.py` to add the pipeline name to `PIPELINES` list.

## Pipeline Patterns

### mmJSON Data (Standard)

Use for most PDBj data:

```python
from mine2.parsers.cif import parse_mmjson_file
from mine2.parsers.mmjson import normalize_column_name

data = parse_mmjson_file(filepath)  # Row-oriented dict
rows = data.get("category_name", [])
```

### CIF Data

Use for validation reports:

```python
from mine2.parsers.cif import parse_cif_file

data = parse_cif_file(filepath)  # Row-oriented dict (same format as mmJSON)
rows = data.get("category_name", [])
```

### Custom JSON Format

For non-mmJSON data like contacts:

```python
import gzip
import json

with gzip.open(filepath, "rt") as f:
    data = json.load(f)
```

### Multiple Data Blocks

For files with multiple data blocks (like PRD):

```python
from mine2.parsers.cif import parse_mmjson_file_blocks

blocks = parse_mmjson_file_blocks(filepath)
# Returns: {"PRD_000001": {...}, "PRDCC_000001": {...}}

prd_data = blocks.get(f"PRD_{entry_id}", {})
prdcc_data = blocks.get(f"PRDCC_{entry_id}", {})
```

### Custom File Discovery

Override `find_jobs()` for nested directories:

```python
def find_jobs(self, limit: int | None = None) -> list[Job]:
    data_dir = Path(self.config.data)
    jobs = []

    for subdir in sorted(data_dir.iterdir()):
        if not subdir.is_dir():
            continue
        for filepath in subdir.glob(self.file_pattern):
            entry_id = self.extract_entry_id(filepath)
            jobs.append(Job(entry_id=entry_id, filepath=filepath))
            if limit and len(jobs) >= limit:
                return jobs

    return jobs
```

## Testing

Test your pipeline:

```bash
# Test with 10 entries
pixi run mine2 update mydata --limit 10

# Check row counts
pixi run psql -c "SELECT COUNT(*) FROM mydata.brief_summary;"
```

## Column Name Normalization

mmJSON uses bracket notation: `matrix[1][2]`

Use `normalize_column_name()` to convert to schema names:

```python
from mine2.parsers.mmjson import normalize_column_name

# matrix[1][2] -> matrix12
normalized = normalize_column_name(col_name)
```

Pass it to `transform_category()`:

```python
rows = transform_category(rows, table, pk_value, pk_col, normalize_column_name)
```

For CIF data (no brackets), pass `None`:

```python
rows = transform_category(rows, table, pk_value, pk_col)
```
