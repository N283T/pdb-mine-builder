# Phase 3: Delta Detection and Transactional Updates

## Goal
Port deltaTable() and updateRDB() for proper change detection and transactional updates.

## Background
Current implementation uses simple bulk_upsert() which:
- Treats all rows as full upserts (no delta detection)
- No automatic update_date management
- No row-level change tracking
- Returns (len(rows), 0) without tracking actual updates

## Tasks

### 3.1 Analyze original deltaTable() logic
- [ ] Read rdb-helper.js deltaTable() implementation
- [ ] Document comparison logic for each type
- [ ] Identify edge cases (dates, arrays, nulls)

### 3.2 Implement delta detection
- [ ] Compare current DB data with new data
- [ ] Detect inserts (new PKs)
- [ ] Detect updates (changed values)
- [ ] Detect deletes (missing PKs)
- [ ] Add tests

### 3.3 Implement transactional updateRDB()
- [ ] Batch inserts (chunk size ~30,000 values)
- [ ] Handle UPDATE with changed columns only
- [ ] Handle DELETE with WHERE clauses
- [ ] Wrap in transaction (BEGIN/COMMIT/ROLLBACK)
- [ ] Track insert/update/delete counts separately
- [ ] Add tests

### 3.4 Auto-manage update_date
- [ ] Set update_date on brief_summary automatically
- [ ] Process brief_summary first (original behavior)
- [ ] Add tests

### 3.5 Integrate with existing loader
- [ ] Replace bulk_upsert() with new logic
- [ ] Maintain backward compatibility option
- [ ] Update LoaderResult to include detailed counts

## Files to Create/Modify
- `src/mine2/db/delta.py` - New module for delta detection
- `src/mine2/db/loader.py` - Integrate delta updates
- `tests/test_delta.py` - Comprehensive tests

## Complexity
This is the most complex phase - original deltaTable() is ~150 lines with intricate comparison logic.

## Acceptance Criteria
- Delta detection matches original behavior
- Transactions ensure data consistency
- Separate INSERT/UPDATE/DELETE counts reported
- Performance acceptable for large datasets

---
- [x] **DONE** - Phase complete (PR #32)
