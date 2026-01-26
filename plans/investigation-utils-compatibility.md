# Investigation: Shared Utilities Compatibility

**Date**: 2026-01-26
**Status**: FULLY COMPATIBLE

## Summary

The shared utilities in `mine2/utils/` are fully compatible with both mmJSON and CIF data formats. All utilities operate on row-oriented dictionaries which both parsers produce.

## Why There Are No Compatibility Issues

### 1. Both Parsers Produce Identical Row-Oriented Dictionaries

```python
# mmJSON parser output
{"category": [{"col": "val", ...}, ...], "_block_name": "..."}

# CIF parser output
{"category": [{"col": "val", ...}, ...], "_block_name": "..."}
```

### 2. Utilities Only Use Plain Column Names

They never access bracket notation like `column[1][2]`. Only use plain names:
- `assembly_id`
- `asym_id_list`
- `oper_expression`
- `entity_id`
- `formula_weight`

### 3. Column Name Normalization Happens Separately

The bracket-to-digit conversion (`column[1][2]` → `column12`) happens in `transform_category()`, AFTER utilities are called.

## Analysis of Each Utility

### hex_sha256()

```python
def hex_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
```

- **Input**: Plain string
- **Format dependency**: None
- **Status**: Fully compatible

### expand_oper_expression()

```python
def expand_oper_expression(expr: str) -> list[str]:
    # Parses "1-3" or "(1,2)(3,4)" to list of operations
```

- **Input**: String from `oper_expression` column
- **Format dependency**: None (column name is plain in both formats)
- **Status**: Fully compatible

### calculate_mw_for_bu()

```python
def calculate_mw_for_bu(mmjson: dict[str, Any]) -> float:
    # Uses: pdbx_struct_assembly_gen, pdbx_struct_assembly,
    #       entity, struct_asym, entity_poly
```

- **Input**: Row-oriented dict (same from both parsers)
- **Column names used**: All plain (no bracket notation)
- **Format dependency**: None
- **Status**: Fully compatible

### apply_patches()

```python
def apply_patches(entry_id: str, data: dict[str, Any]) -> dict[str, Any]:
    if entry_id == "7ed1":
        _patch_7ed1_met(data)
    return data
```

- **Input**: Row-oriented dict
- **Operations**: Adds/modifies categories and rows
- **Format dependency**: None
- **Status**: Fully compatible

## Code Evidence

Both pipelines use the same utilities identically:

| Operation | mmJSON (PdbjPipeline) | CIF (PdbjCifPipeline) |
|-----------|----------------------|----------------------|
| Patches | Line 102: `apply_patches(job.entry_id, data)` | Line 331: `apply_patches(job.entry_id, data)` |
| Hash | Lines 106-108: `hex_sha256(asym_id_list)` | Lines 334-337: `hex_sha256(asym_id_list)` |
| BU MW | Line 223: `calculate_mw_for_bu(data)` | Line 449: `calculate_mw_for_bu(data)` |

## Design Pattern

This is an excellent example of format abstraction:

```
┌─────────────┐     ┌─────────────┐
│   mmJSON    │     │     CIF     │
│   Parser    │     │   Parser    │
└──────┬──────┘     └──────┬──────┘
       │                   │
       │   Row-oriented    │
       └───────┬───────────┘
               │
               ▼
       ┌───────────────┐
       │ Shared Utils  │  ← Format-agnostic
       │ (assembly.py) │
       └───────┬───────┘
               │
               ▼
       ┌───────────────┐
       │ transform_    │  ← Handles normalization
       │ category()    │
       └───────────────┘
```

## Recommendations

### No Code Changes Required

The system is correctly designed.

### Optional Improvements

1. Rename `calculate_mw_for_bu()` parameter from `mmjson` to `data` for clarity
2. Update docstrings to explicitly state "works with both mmJSON and CIF formats"
3. Add integration tests comparing CIF vs mmJSON results for same entry

## Confidence Level: HIGH

The utilities are designed to be format-agnostic by operating on a common row-oriented dictionary structure.
