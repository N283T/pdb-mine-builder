# Investigation: CIF Pipeline Test Coverage

**Date**: 2026-01-26
**Status**: GAPS IDENTIFIED

## Summary

CIF pipelines have dedicated test files with good coverage, but some critical gaps exist around Phase 5 features and integration testing.

## Current Test Coverage

### Dedicated CIF Test Files

| File | Tests | Lines | Coverage |
|------|-------|-------|----------|
| `test_pdbj_cif.py` | 22 | 641 | Good |
| `test_cc_cif.py` | 35 | 668 | Best |
| `test_prd_cif.py` | 18 | 456 | Good |
| `test_ccmodel_cif.py` | 15 | 330 | Minimal |
| **Total** | **90** | **2095** | - |

### Shared Utilities Test Coverage

| Utility | Test File | Tests |
|---------|-----------|-------|
| `hex_sha256` | `test_assembly.py` | 4 tests + 3 in IHM |
| `calculate_mw_for_bu` | `test_assembly.py` | 10 tests + 3 in IHM |
| `expand_oper_expression` | `test_assembly.py` | 12 tests |
| `apply_patches` | `test_patches.py` | 5 tests |

## Critical Gaps

### 1. No Assembly/BU MW Verification with CIF Data
- Utilities tested in isolation with synthetic dicts
- NOT tested in actual CIF processing pipeline
- `test_pdbj_cif.py` doesn't verify `_hash_asym_id_list` or `bu_mw`

### 2. No Real Database Integration Tests
- All `process_job` tests use mocked connections ("mock://test")
- Cannot verify actual table routing, column coercion, or upserts

### 3. Missing Error Handling Tests
- No corrupted gzip file tests
- No malformed CIF structure tests
- No missing required categories tests

### 4. CC Pipeline Gaps
- No CIF SMILES generation tests (only mmJSON)
- RDKit setup tests use mocks, not real DB
- No large-scale testing (components.cif has 40k+ blocks)

### 5. Plus Data Integration Incomplete
- Plus merge tests use mocked bulk_upsert
- Actual merge behavior not verified

### 6. CCMODEL Coverage Smallest
- Only 15 tests (17% of total)
- No multiple models per file testing
- No coordinate validation

## Recommended New Tests

### High Priority

```python
# test_pdbj_cif.py
class TestCifPhase5Features:
    def test_hash_asym_id_list_computed_for_cif(self):
        """Verify _hash_asym_id_list is computed for CIF data."""
        pass

    def test_bu_mw_calculated_for_cif(self):
        """Verify bu_mw is calculated and added to plus_fields."""
        pass

    def test_patches_applied_to_cif(self):
        """Verify entry-specific patches work with CIF data."""
        pass
```

### Medium Priority

```python
# test_cif_mmjson_parity.py
class TestFormatParity:
    def test_same_entry_produces_identical_output(self):
        """Verify CIF and mmJSON for same entry produce identical results."""
        pass
```

### Low Priority

- Large file performance tests
- Corrupted input handling
- Memory usage under load

## Test Distribution Chart

```
CC CIF:      ████████████████████ 39%
PDBJ CIF:    ████████████ 24%
PRD CIF:     ██████████ 20%
CCMODEL CIF: ████████ 17%
```

## Action Items

1. [ ] Add Phase 5 feature tests to `test_pdbj_cif.py`
2. [ ] Create `test_cif_mmjson_parity.py` for cross-format validation
3. [ ] Add error handling tests for malformed CIF
4. [ ] Expand CCMODEL test coverage
