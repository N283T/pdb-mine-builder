# Phase 4: Missing Pipelines (EMDB, IHM)

## Goal
Port EMDB and IHM pipelines from original mine2updater.

## Background
Original has 8 pipelines, ng currently has 6 + SIFTS. Missing: EMDB, IHM.

## Tasks

### 4.1 EMDB Pipeline
- [ ] Create schema definition (emdb.def.yml)
- [ ] Implement XML parsing (xml2js → Python equivalent)
- [ ] Implement docid generation: `int(entry_id.split("-")[1])`
- [ ] Handle brief_summary with `content` field (entire mmJSON structure)
- [ ] Extract metadata: deposition_date, header_release_date, map_release_date, modification_date
- [ ] Add config entries
- [ ] Add tests

Original structure (pipelines/emdb.load.js):
```javascript
// Uses XML input
// docid = parseInt(entryId.split("-")[1])  // "EMD-1234" → 1234
// brief_summary.content = JSON.stringify(mmjson)
```

### 4.2 IHM Pipeline
- [ ] Create schema definition (ihm.def.yml) or extend pdbj
- [ ] Implement pipeline (similar to pdbj)
- [ ] Add IHM method mapping: `"IHM": 16`
- [ ] Handle pdbx_struct_assembly_gen with asym_id_list hashing
- [ ] Add config entries
- [ ] Add tests

Original structure (pipelines/ihm.load.js):
- Nearly identical to pdbj pipeline
- Uses same data structure (noatom + plus files)
- Extra method: IHM = 16

### 4.3 Test with sample data
- [ ] Obtain/create test fixtures for EMDB
- [ ] Obtain/create test fixtures for IHM
- [ ] Verify output matches original

## Files to Create
- `schemas/emdb.def.yml`
- `schemas/ihm.def.yml` (or extend pdbj)
- `src/mine2/pipelines/emdb.py`
- `src/mine2/pipelines/ihm.py`
- `tests/test_emdb.py`
- `tests/test_ihm.py`
- `data/emdb/` - Test fixtures
- `data/ihm/` - Test fixtures

## Dependencies
- Phase 2 (mmJSON utils) may be helpful
- Phase 3 (delta updates) can be done in parallel

## Acceptance Criteria
- Both pipelines load data successfully
- Output matches original mine2updater
- Tests pass with sample data

---
- [ ] **DONE** - Phase complete
