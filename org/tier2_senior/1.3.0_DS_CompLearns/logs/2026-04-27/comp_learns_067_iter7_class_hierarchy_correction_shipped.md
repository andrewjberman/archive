# Session Log — COMP_LEARNS.067 — iter-7 class_hierarchy_correction (q03-only)

**Agent:** 1.3.0_DS_CompLearns
**Date:** 2026-04-27
**TO:** COMP_LEARNS.067.iter7-class-hierarchy-correction.md
**Outcome:** SHIPPED

---

## Objective

1. Fix runner.py experiment_log path mismatch (Phase 0).
2. Author iter-7 click compiler mutation: replace hierarchy_summary with class_hierarchy_correction node (Command-perspective, NOT-exclusion signals, q03-only).
3. Pre-commit gates + pytest 458+ pass.
4. Commit + push CLOUD from feature_clb.
5. MCP COMPLETE to 2.1.0_SA_COO + CC 1.1.0_SA_CTO.

---

## Work Completed

### Phase 0 — runner.py experiment_log path fix

- Root cause: `log_path = target_dir / "experiment_log.jsonl"` resolved to `comp/targets/<target>/experiment_log.jsonl` (schema v2 location). v3 maintained log lives at `comp/results/<target>/experiment_log.jsonl`.
- Fix (3 LOC added to runner.py, after line 262):
  ```python
  _v3_log = workspace / "comp" / "results" / target / "experiment_log.jsonl"
  if _v3_log.parent.exists():
      log_path = _v3_log
  ```
- Non-breaking for other targets (only redirects when `comp/results/<target>/` directory exists).
- Commit: `f5095ac0` — author `1.3.0_DS_CompLearns`

### Phase 1 — iter-7 mutation (class_hierarchy_correction)

- Updated `comp/targets/click/compiler.py` v6 → v7.
- Replaced hierarchy_summary block with class_hierarchy_correction node per verbatim CTO P0 amendment:
  ```python
  graph.nodes.append(Node(
      id="hierarchy_correction:click",
      kind="class_hierarchy_correction",
      canonical_path="",
      attributes={
          "Command.direct_subclasses": ["_BaseCommand", "Group"],
          "_MultiCommand.parent_class": "Group (NOT a direct Command subclass)",
          "CommandCollection.parent_class": "Group (NOT a direct Command subclass)",
      },
  ))
  ```
- No q02/q11 numeric-fact nodes added — excluded per CVO R-CTO-1.
- Commit: `7ee0859c` — author `1.3.0_DS_CompLearns`

### Phase 2 — Gates

- ds-commit-gate.sh compiler.py: PASS
- ds-commit-gate.sh runner.py: PASS
- pytest 458 passed, 0 failed (pre-write: 42s; pre-commit: 83s)

### Phase 3 — Push

- Push: `69c7a0cc..7ee0859c CLOUD -> CLOUD` from feature_clb
- Phase 3 compiler mandate: 6 iters [1,2,3,4,5,6] intact post-commit — PASS

---

## Decisions Made

- Two separate commits (runner.py path fix preceding compiler mutation) for clean attribution and bisectability.
- NOT-exclusion strings encoded verbatim as attribute values: `"Group (NOT a direct Command subclass)"` — load-bearing per CTO note.
- `id="hierarchy_correction:click"` (vs iter-6 `hierarchy_summary:click`) to distinguish node in compiled graph.
- `kind="class_hierarchy_correction"` per TO node_type spec.
- Path fix uses `_v3_log.parent.exists()` guard (not `.exists()` on the log file itself) so the redirect applies even when the log is empty or freshly created by runner.

---

## Files Modified

| File | Change |
|------|--------|
| `comp/loop/runner.py` | Phase 0: 3-LOC path redirect to comp/results/<target>/experiment_log.jsonl |
| `comp/targets/click/compiler.py` | v7: docstring + replace hierarchy_summary with class_hierarchy_correction node |

---

## Blockers

None.

---

## Current State

COMP_LEARNS.067 COMPLETE. Both commits pushed. Awaiting SC scoring for iter-7.

---

## Next Steps

- SC scores iter-7. DS does not pre-score.
- Await COO routing for iter-8 or final plateau/CTO decision.

---

## Compiler Tools

| Phase | Run | Expected | Observed | Pass/Fail |
|-------|-----|----------|----------|-----------|
| Before write | `pytest comp/ --ignore=comp/targets -q --tb=no` | 458 passed, 0 failed | 458 passed in 42.45s | PASS |
| Before write | `python -c "...experiment_log iters"` | 6 [1,2,3,4,5,6] | 6 [1, 2, 3, 4, 5, 6] | PASS |
| Before commit | `.tools/ds-commit-gate.sh comp/targets/click/compiler.py` | All 3 checks exit 0 | All checks passed! OK | PASS |
| Before commit | `.tools/ds-commit-gate.sh comp/loop/runner.py` | All 3 checks exit 0 | All checks passed! OK | PASS |
| Before commit | `pytest comp/ --ignore=comp/targets -q --tb=short` | 458+ passed, 0 failed | 458 passed in 82.98s | PASS |
| After commit | `python -c "...experiment_log iters"` | 6 iters [1-6] intact | 6 [1, 2, 3, 4, 5, 6] | PASS |
