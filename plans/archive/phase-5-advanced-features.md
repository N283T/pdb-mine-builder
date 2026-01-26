# Phase 5: Advanced Features

## Goal
Port remaining advanced features for full feature parity.

## Background
These features are lower priority but needed for complete compatibility.

## Tasks

### 5.1 Hash Primary Keys (hex_sha256) ✅
- [x] Implement SHA256 hashing for assembly data
- [x] Use for pdbx_struct_assembly_gen.asym_id_list
- [x] Add to pdbj pipeline
- [x] Add tests

Original usage:
```javascript
tbl._hash_asym_id_list = tbl.asym_id_list.map(x => rdbHelper.hex_sha256(x));
```

### 5.2 calculateMW4BU() - Biological Unit Molecular Weight ✅
- [x] Parse assembly expressions: `(1,2-5)(1,2)` → expand combinations
- [x] Calculate molecular weights
- [x] Add to plus_fields generation
- [x] Add tests

Note: Implemented in mine2/utils/assembly.py, shared with IHM pipeline.

### 5.3 patch() - Entry-specific patches ✅
- [x] Implement patch mechanism for specific entries
- [x] Port 7ed1 patch (missing MET record)
- [x] Make extensible for future patches
- [x] Add tests

Original:
```javascript
function patch(entryId, mmjson) {
  if (entryId === "7ed1") {
    // Append missing chem_comp entry for MET
  }
  return mmjson;
}
```

### 5.4 CIF Dictionary-based Schema Generation (Optional)
- [ ] Parse CIF dictionary files (mmCIF type definitions)
- [ ] Extract type info from `item_type.code`
- [ ] Build foreign key relationships
- [ ] Generate schema YAML from dictionary

Note: Current approach (manual YAML) may be sufficient. This is optional.

### 5.5 brief_summary Ordering ✅
- [x] Process brief_summary FIRST (before other tables)
- [x] Ensure update_date is set before dependent tables
- [x] Add tests

Note: brief_summary is now processed before other tables in pdbj pipeline.

## Files to Create/Modify
- `src/mine2/utils/hash.py` - SHA256 utility
- `src/mine2/utils/mw.py` - Molecular weight calculation
- `src/mine2/utils/patch.py` - Entry patches
- `src/mine2/pipelines/pdbj.py` - Integrate features
- Tests for each

## Priority
- 5.1 (Hash PKs): Medium - needed for assembly data integrity
- 5.2 (MW calc): Low - enrichment feature, can defer
- 5.3 (Patches): Low - only affects specific entries
- 5.4 (CIF dict): Low - current YAML approach works
- 5.5 (Ordering): Medium - affects update consistency

## Acceptance Criteria
- Hash PKs work for assembly data
- Other features implemented as needed
- Tests pass

---
- [x] **DONE** - Phase complete (PR #34)
