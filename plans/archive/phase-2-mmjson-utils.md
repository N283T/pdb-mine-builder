# Phase 2: mmJSON Utility Functions

## Goal
Port missing mmJSON utility functions from original mine2updater.

## Background
These utilities are used extensively in pipelines for data extraction and cleanup.

## Tasks

### 2.1 mmjsonAt() - Conditional row search
- [ ] Find rows in category matching condition
- [ ] Return matching rows or None
- [ ] Add tests

Original logic:
```javascript
function mmjsonAt(mmj, category, condition) {
  // Returns rows where condition(row) is true
  if (!mmj[category]) return null;
  return mmj[category].filter(condition);
}
```

### 2.2 mmjsonAt_IC() - Case-insensitive version
- [ ] Same as mmjsonAt but case-insensitive key matching
- [ ] Add tests

### 2.3 mmjsonGet() - Safe value retrieval
- [ ] Get value with default fallback
- [ ] Handle nested paths
- [ ] Add tests

### 2.4 cleanArray() - Array cleanup
- [ ] Remove null/undefined values
- [ ] Remove duplicates
- [ ] Sort results
- [ ] Add tests

Original logic:
```javascript
function cleanArray(arr) {
  return [...new Set(arr.filter(x => x != null))].sort();
}
```

### 2.5 removeNull() - Simple null filter
- [ ] Filter null values from array
- [ ] Add tests

## Files to Create/Modify
- `src/mine2/parsers/mmjson.py` - Add utility functions
- `tests/test_mmjson.py` - Add tests

## Usage in Pipelines
- pdbj: cleanArray() 15+ times, mmjsonAt() 10+ times
- cc: mmjsonAt_IC() for SMILES/InChI extraction
- Multiple: removeNull() for citation cleanup

## Acceptance Criteria
- Functions match original behavior
- Used in refactored pipeline code where applicable
- Tests cover edge cases

---
- [x] **DONE** - Phase complete (PR #31)
