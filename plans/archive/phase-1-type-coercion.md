# Phase 1: Type Coercion Functions

## Goal
Port missing type coercion functions from original mine2updater's `rdb-helper.js`.

## Background
Currently `_coerce_array_value()` handles array types, but other type coercions are missing or incomplete.

## Tasks

### 1.1 enforceDate() - Date normalization
- [ ] Handle 2-digit year conversion (99 → 1999, 01 → 2001)
- [ ] Zero-pad month and day
- [ ] Add tests

Original logic (rdb-helper.js:663-675):
```javascript
function enforceDate(i) {
  if (i) {
    i = i.split("-");
    if (i[0].length < 4) {
      if (parseInt(i[0]) < 50) i[0] = "20"+i[0];
      else i[0] = "19"+i[0];
    }
    if (i[1].length < 2) i[1] = "0"+i[1];
    if (i[2].length < 2) i[2] = "0"+i[2];
    i = i.join("-");
  }
  return i;
}
```

### 1.2 enforceBoolean() - Boolean parsing
- [ ] Handle string "true"/"false" → Python bool
- [ ] Handle None/null
- [ ] Add tests

### 1.3 enforceFloat() with precision
- [ ] Add toPrecision(15) equivalent
- [ ] Handle None/invalid values
- [ ] Add tests

### 1.4 Update _coerce_array_value() to use type handlers
- [ ] Refactor to dispatch to type-specific handlers
- [ ] Support `boolean[]`, `real[]` etc.

## Files to Modify
- `src/mine2/pipelines/base.py` - Add coercion functions
- `tests/test_base.py` - Add tests

## Acceptance Criteria
- All type coercions match original behavior
- Tests cover edge cases (None, invalid values, 2-digit years)
- Existing pipelines still pass

---
- [x] **DONE** - Phase complete (PR #30)
