# Unify Pipeline Names with Config-Based Format Selection

## Context

Currently, dual-format pipelines (pdbj, cc, ccmodel, prd) have separate pipeline names
for CIF and mmJSON (`pdbj` vs `pdbj-json`, `cc` vs `cc-json`, etc.), each requiring
its own config entry. This is redundant since the schema/output is identical regardless
of format. We unify pipeline names and move format selection to a `format` field in config.

## Design

### Config Change

```yaml
# Before
pipelines:
  pdbj:
    data: .../mmCIF/
  pdbj-json:
    data: .../mmjson-noatom/

# After
pipelines:
  pdbj:
    format: cif          # "cif" (default) or "mmjson"
    data: .../mmCIF/
    data-plus: ...
```

- `format` defaults to `"cif"` when omitted
- Single-format pipelines (vrpt, contacts, sifts, emdb, ihm) ignore `format`

### Dispatch Logic Change

```
update command:
  pdbj + format=cif    → pipelines.pdbj.run_cif()
  pdbj + format=mmjson → pipelines.pdbj.run()

load command:
  pdbj + format=cif    → pipelines.pdbj.run_cif_load()
  pdbj + format=mmjson → pipelines.pdbj.run_load()  (new, needs adding)
```

## Files to Modify

### 1. `src/mine2/config.py` - Add `format` field

- Add `format: str = "cif"` to `PipelineConfig`
- Validate: must be `"cif"` or `"mmjson"`

### 2. `src/mine2/commands/update.py` - Simplify dispatch

- Remove `-json` entries from `AVAILABLE_PIPELINES`
- Remove `-json` entries from `PIPELINE_SCHEMA_MAP`
- Add legacy aliases: `pdbj-json` → `pdbj`, `cc-json` → `cc`, etc.
- Update `_get_pipeline_runner()`: read `format` from config to choose `run()` vs `run_cif()`
- Pass config to `_get_pipeline_runner()` so it can read format

### 3. `src/mine2/commands/load.py` - Add format support

- Read `format` from pipeline config
- Dispatch to `run_cif_load()` (cif) or `run_load()` (mmjson)
- Each dual-format pipeline needs a `run_load()` function (mmJSON bulk load)

### 4. `src/mine2/pipelines/{pdbj,cc,ccmodel,prd}.py` - Add `run_load()`

- Add `run_load()` for mmJSON bulk load (analogous to `run_cif_load()`)
- For pdbj: uses `PdbjPipeline` + `bulk_copy_entry` (no delta sync)
- For cc/ccmodel/prd: similar pattern

### 5. `src/mine2/cli.py` - Update help text

- Remove `-json` variants from help
- Update `update` argument: `"Pipelines: pdbj, cc, ccmodel, prd, vrpt, contacts, sifts, emdb, ihm"`
- update SIFTS `--tables` help text if needed

### 6. `config.yml` / `config.test.yml` - Update config structure

- Merge `pdbj` + `pdbj-json` into single `pdbj` entry with `format: cif`
- Same for cc, ccmodel, prd
- Remove `*-json` config entries

### 7. Tests - Update for new dispatch

- Update any tests that reference `-json` pipeline names
- Add test for format config field validation

## Task Order

1. Add `format` field to `PipelineConfig` (config.py)
2. Update config files (config.yml, config.test.yml)
3. Add legacy aliases for `-json` names (commands/update.py)
4. Refactor dispatch logic in update command (commands/update.py)
5. Add `run_load()` to each dual-format pipeline module
6. Refactor dispatch logic in load command (commands/load.py)
7. Update CLI help text (cli.py)
8. Update tests
9. Run all checks (lint, typecheck, tests)

## Verification

```bash
# Lint + tests
pixi run check
pixi run test --ignore=tests/integration

# Manual: verify CLI help
pixi run mine2 update --help
pixi run mine2 load --help

# Manual: verify legacy alias warning
pixi run mine2 update pdbj-json --limit 1  # should warn and run mmjson

# Manual: verify format dispatch
# config.yml with format: cif → runs CIF pipeline
# config.yml with format: mmjson → runs mmJSON pipeline
```

---
- [x] **DONE** - Phase complete
