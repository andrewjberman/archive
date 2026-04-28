# Session: COMP_LEARNS.087 — awkward-array v2.9.0 Vendor + Question Pool

**Date:** 2026-04-28
**Task Order:** COMP_LEARNS.087
**Status:** COMPLETE
**Commit:** dd3ff06b

---

## Objective

Vendor awkward-array v2.9.0 under comp/targets/awkward_array/ and author a 12-question pool
at comp/backlog/benchmark/bl-awkward-array-001.yaml per V1.3 §7.4 guardrail. Parallel with
.086 SC pre-screen per COO direction — no waiting on .086 result.

---

## Compiler Tools

| Phase | Tool | Command | Result | Pass/Fail |
|-------|------|---------|--------|-----------|
| before commit | Gate-2 check 1 | python3 yaml count + families | PASS: 12 questions, 4 families: {C, D, B, A} | PASS |
| before commit | Gate-2 check 2 | python3 no legacy gold_answer | PASS: no legacy gold_answer fields | PASS |
| before commit | Gate-2 check 3 | python3 all provenance fields | PASS: all provenance fields present | PASS |
| before commit | Family A ceiling | python3 A count 3/12 25% | PASS: within 50% ceiling (6/12) | PASS |

No Python files modified; ds-commit-gate.sh not required per .087 TO mandate (YAML-only edit).

---

## Work Completed

### Phase 0 — Vendor and pin

Cloned awkward-array v2.9.0 from scikit-hep/awkward:
- Clone: comp/targets/awkward_array/_repo/ (depth 1, tag v2.9.0)
- PIN: e4be9febc76c610eea671ef3f0e3084cb206da49
- Source path confirmed: src/awkward/ (standard modern packaging layout)
- _repo/ self-gitignored per comp/targets/awkward_array/_repo/.gitignore pattern
- repo_pin.txt written: commit hash + tag v2.9.0 + date 2026-02-08

### Phase 1 — Question pool authoring

Explored key source surfaces:
- src/awkward/contents/ — 12 Content subclasses (one per .py file)
- src/awkward/_reducers.py — Reducer/KernelReducer hierarchy, 10 name:Final values
- src/awkward/highlevel.py — Array.__init__, ArrayBuilder.__init__
- src/awkward/behaviors/mixins.py — mixin_class + mixin_class_method decorators
- src/awkward/_meta/recordmeta.py — RecordMeta meta class for RecordArray
- src/awkward/operations/ak_sum.py — axis=None default

12 questions across 4 families:

| QID | Family | Type | Gold Answer | Source Line |
|-----|--------|------|-------------|-------------|
| awkward-array-001 | A | set_membership | {behavior, attrs, initial, resize} | highlevel.py:2714 |
| awkward-array-002 | A | set_membership | {BitMaskedArray, ByteMaskedArray} | bitmaskedarray.py:55 |
| awkward-array-003 | A | set_membership | {mixin_class, mixin_class_method} | mixins.py:10 |
| awkward-array-004 | B | enumerable | count_nonzero | _reducers.py:287 |
| awkward-array-005 | B | enumerable | RecordMeta | recordarray.py:114 |
| awkward-array-006 | B | enumerable | argmin | _reducers.py:134 |
| awkward-array-007 | C | code_extraction | None | ak_sum.py:26 |
| awkward-array-008 | C | code_extraction | False | highlevel.py:288 |
| awkward-array-009 | C | code_extraction | 1024 | highlevel.py:2714 |
| awkward-array-010 | D | numeric | 12 | contents/bitmaskedarray.py:55 |
| awkward-array-011 | D | numeric | 10 | _reducers.py:134 |
| awkward-array-012 | D | numeric | 2 | _reducers.py:133 |

### Phase 2 — Gate-2

All 3 checks PASS (see Compiler Tools table above).

### Phase 3 — Commit and push

Commit: dd3ff06b on CLOUD.
Push confirmed: f5e7f81c..dd3ff06b CLOUD -> CLOUD.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| _repo not committed | Self-gitignores per internal .gitignore pattern — consistent with httpx/click/sphinx/griffe targets |
| Use git commit --only (not safe-commit.sh) | safe-commit.sh is D (deleted) in feature_clb working tree per ADHC_OWNPTH.009 changes in flight |
| code_extraction type used for Family C | TO spec lists it as valid; semantic grader handles via fallback values[] path |
| q09 and q01 share same source line | Different attributes of same __init__ — q01 asks for set of param names, q09 asks for initial value specifically; no overlap in gold answers |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| comp/targets/awkward_array/repo_pin.txt | Created: commit hash + tag + date | dd3ff06b |
| comp/backlog/benchmark/bl-awkward-array-001.yaml | Created: 12-question pool | dd3ff06b |
| org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.087.awkward-array-vendor-pool.md | Status: complete | dd3ff06b |

_repo/ cloned locally at comp/targets/awkward_array/_repo/ (gitignored, not committed).

---

## Blockers

None.

---

## Current State

COMP_LEARNS.087 complete (dd3ff06b on CLOUD). MCP COMPLETE sent to 2.1.0_SA_COO.
COMP_LEARNS.086 SC pre-screen also landed complete (0ab95f7c) during this session.
Awaiting COO/CTO next dispatch (CTO pool review of bl-awkward-array-001.yaml per INTAKE_WAVE §4).

---

## Next Steps

1. Await CTO pool review (G2 gate per INTAKE_WAVE §4)
2. Await COO dispatch of next TO (SC awkward-array pre-screen or other work)
3. Continue watchdog at 270s cadence
