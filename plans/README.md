# Migration Plan: mine2updater → mine2updater-ng

## Overview
Complete the port of functionality from original mine2updater (JavaScript) to mine2updater-ng (Python).

## Phases

| Phase | Name | Priority | Complexity | Status |
|-------|------|----------|------------|--------|
| 1 | [Type Coercion](phase-1-type-coercion.md) | HIGH | Low | ⬜ Not Started |
| 2 | [mmJSON Utils](phase-2-mmjson-utils.md) | MEDIUM | Low | ⬜ Not Started |
| 3 | [Delta Updates](phase-3-delta-updates.md) | CRITICAL | High | ⬜ Not Started |
| 4 | [Missing Pipelines](phase-4-missing-pipelines.md) | HIGH | Medium | ⬜ Not Started |
| 5 | [Advanced Features](phase-5-advanced-features.md) | LOW | Medium | ⬜ Not Started |

## Recommended Order

```
Phase 1 (Type Coercion)     ← Start here, foundational
    ↓
Phase 2 (mmJSON Utils)      ← Used by pipelines
    ↓
Phase 3 (Delta Updates)     ← Most complex, core functionality
    ↓
Phase 4 (Missing Pipelines) ← Can parallel with Phase 3
    ↓
Phase 5 (Advanced Features) ← As needed
```

## Dependencies

- Phase 1 → Phase 3 (type coercion needed for delta comparison)
- Phase 2 → Phase 4 (mmJSON utils used in pipelines)
- Phase 3 and 4 can be done in parallel after Phase 1+2

## Key Files Reference

### Original mine2updater
```
/home/nagaet/ghq/gitlab.com/pdbjapan/mine2updater/
├── modules/
│   ├── rdb-helper.js      # Core utilities (type coercion, delta, etc.)
│   └── cif.js             # CIF parsing
├── pipelines/
│   ├── pdbj.load.js       # Main PDB pipeline
│   ├── cc.load.js         # Chemical components
│   ├── emdb.load.js       # EMDB (missing)
│   └── ihm.load.js        # IHM (missing)
```

### mine2updater-ng
```
/home/nagaet/mine2updater-ng/
├── src/mine2/
│   ├── pipelines/base.py  # Type coercion goes here
│   ├── parsers/mmjson.py  # mmJSON utils go here
│   └── db/loader.py       # Delta updates go here
```

## Progress Tracking

Update this section as phases complete:

- [ ] Phase 1 complete
- [ ] Phase 2 complete
- [ ] Phase 3 complete
- [ ] Phase 4 complete
- [ ] Phase 5 complete
