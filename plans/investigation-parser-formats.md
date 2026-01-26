# Investigation: Parser Output Format Compatibility

**Date**: 2026-01-26
**Status**: FULLY COMPATIBLE

## Summary

Both CIF and mmJSON parsers produce structurally identical output. The parsers handle their format-specific issues internally, providing a unified interface for downstream processing.

## Parser Output Comparison

### CIF Parser (`parse_cif_file()`)

```python
# Input: path/to/file.cif.gz
# Output:
{
    "entry": [{"id": "100D"}],
    "entity": [{"id": "1", "formula_weight": "1000.0"}],
    "struct_asym": [{"id": "A", "entity_id": "1"}],
    "_block_name": "100D",
    "_block_names": ["100D"]  # All block names if multiple
}
```

### mmJSON Parser (`parse_mmjson_file()`)

```python
# Input: path/to/file.json.gz
# Output:
{
    "entry": [{"id": "100D"}],
    "entity": [{"id": "1", "formula_weight": "1000.0"}],
    "struct_asym": [{"id": "A", "entity_id": "1"}],
    "_block_name": "100D"
}
```

### Key Finding

Both parsers leverage gemmi's internal conversion. Gemmi automatically normalizes column names internally, so the output is already in a consistent format.

## Column Naming Strategy

| Format | Raw Format | Parser Output | Schema Matching |
|--------|-----------|---------------|-----------------|
| CIF | Plain names (`atom_site.id`) | Plain names | Direct match |
| mmJSON | Bracket notation (`column[1][2]`) | Plain names (gemmi normalizes) | Direct match |

### normalize_column_name() Usage

The function in `mine2/parsers/mmjson.py`:

```python
def normalize_column_name(name: str) -> str:
    """Converts bracket notation to concatenated digits."""
    return re.sub(r"\[(\d+)\]", r"\1", name)
```

**Usage Pattern** in `transform_category()`:
- **mmJSON pipelines**: Pass `normalize_fn=normalize_column_name` (defensive)
- **CIF pipelines**: Pass `normalize_fn=None` (not needed)

This is a **defensive measure** rather than strictly necessary - gemmi already normalizes internally.

## Structural Differences

| Aspect | CIF | mmJSON |
|--------|-----|--------|
| Value Types | All strings | All strings |
| Special Values | `?` → None, `.` → None | Handled by gemmi |
| Multi-block Support | `_block_names` list | Single block or `parse_mmjson_file_blocks()` |
| Compression | .gz automatic | .gz automatic |
| Metadata | `_block_name`, `_block_names` | `_block_name` |

## transform_category() Compatibility

The function handles both formats identically:

```python
def transform_category(
    rows: list[dict[str, Any]],
    table: TableDef,
    pk_value: str,
    pk_col: str,
    normalize_fn: Callable[[str], str] | None = None,  # Optional
) -> list[dict[str, Any]]:
```

**Process**:
1. Collects all column names from rows
2. If `normalize_fn` provided, normalizes each column name
3. Validates against schema (filters to valid columns only)
4. Orders columns consistently (PK first, then schema order)
5. Type-coerces values based on schema column type
6. Returns rows with consistent column ordering

**Result**: Identical output structure regardless of input format

## Special Cases

### Multiple Blocks (PRD files)

| Format | Handler |
|--------|---------|
| CIF | `parse_cif_document()` merges all blocks |
| mmJSON | `parse_mmjson_file_blocks()` returns `{block_name: data}` |

### Plus Data Merging

`merge_data()` in `mmjson.py` works on any row-oriented data:
- Used by both pipelines: CIF + plus data, mmJSON + plus data
- Plus data takes precedence for overlapping columns

## Test Coverage Verification

Tests in `tests/test_parsers.py` verify:
- CIF and mmJSON produce identical row-oriented format
- Both handle multiple rows correctly
- `merge_data()` works for overlapping/non-overlapping categories
- Special CIF values (?, .) convert to None properly

## Conclusion

Both parsers produce structurally identical output:

1. **Same format**: Row-oriented dict of categories → list of row dicts
2. **Same column names**: Plain names (gemmi handles conversion internally)
3. **Same value handling**: All strings, special values normalized to None
4. **Same metadata**: `_block_name` consistent

The architecture is **correctly designed** with proper abstraction.
