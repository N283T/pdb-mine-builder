# Plan: Make CIF Default, mmJSON Optional

## Summary

Swap the default format from mmJSON to CIF for dual-format pipelines (pdbj, cc, ccmodel, prd).

**Current**: `pdbj` = mmJSON, `pdbj-cif` = CIF
**New**: `pdbj` = CIF, `pdbj-json` = mmJSON

## Design Decision

Use `-json` suffix for mmJSON (not `--json` flag) because:
- Symmetric with current architecture
- Simpler dispatch logic
- Config file pipeline names remain simple strings

## Backward Compatibility (Confirmed)

Accept legacy `-cif` names with deprecation warning:
- `pdbj-cif` → `pdbj` (warning logged)
- `cc-cif` → `cc`
- `ccmodel-cif` → `ccmodel`
- `prd-cif` → `prd`

This allows existing scripts to continue working while encouraging migration.

## Files to Modify

### 1. `src/mine2/commands/update.py`

```python
AVAILABLE_PIPELINES = [
    "pdbj",        # CIF (new default)
    "pdbj-json",   # mmJSON (requires suffix)
    "cc",
    "cc-json",
    "ccmodel",
    "ccmodel-json",
    "prd",
    "prd-json",
    "vrpt",
    "contacts",
]

LEGACY_ALIASES = {
    "pdbj-cif": "pdbj",
    "cc-cif": "cc",
    "ccmodel-cif": "ccmodel",
    "prd-cif": "prd",
}

def _get_pipeline_runner(pipeline_name: str) -> tuple[str, str]:
    # mmJSON requires -json suffix
    json_pipelines = {
        "pdbj-json": ("pdbj", "run"),
        "cc-json": ("cc", "run"),
        "ccmodel-json": ("ccmodel", "run"),
        "prd-json": ("prd", "run"),
    }
    if pipeline_name in json_pipelines:
        return json_pipelines[pipeline_name]

    # Base names now use CIF (run_cif)
    cif_defaults = {"pdbj", "cc", "ccmodel", "prd"}
    if pipeline_name in cif_defaults:
        return (pipeline_name, "run_cif")

    return (pipeline_name, "run")
```

### 2. `src/mine2/commands/sync.py`

Rename sync targets:
- `pdbj` → CIF source (mmCIF)
- `pdbj-json` → mmJSON source
- Add legacy aliases

### 3. `src/mine2/cli.py`

Update help text to reflect new naming.

### 4. Tests

Update pipeline name references in:
- `tests/test_cc_cif.py`
- `tests/test_pdbj_cif.py`
- `tests/test_ccmodel_cif.py`
- `tests/test_prd_cif.py`

### 5. Documentation

Update README.md and CLAUDE.md with new pipeline naming.

## Implementation Order

1. Update `update.py` dispatch logic
2. Update `sync.py` targets
3. Update `cli.py` help text
4. Update test files
5. Update documentation

## Verification

```bash
# Test CIF default
pixi run mine2 update pdbj --limit 5

# Test mmJSON with suffix
pixi run mine2 update pdbj-json --limit 5

# Test legacy alias (should show deprecation warning)
pixi run mine2 update pdbj-cif --limit 5

# Run all tests
pixi run test
```

---
- [ ] **DONE** - Phase complete
