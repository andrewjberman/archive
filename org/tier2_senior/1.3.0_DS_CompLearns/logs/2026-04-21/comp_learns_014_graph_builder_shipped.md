# 1.3.0_DS_CompLearns — Session Log
**Date:** 2026-04-21
**TO:** COMP_LEARNS.014 — Graph Builder v0
**Status:** COMPLETE
**Commit:** 69b43374

---

## Objective

Implement Graph Builder v0 per §5.2 + §5.3. Consume `list[SubtypeRecord]` from ImportsSubtype;
produce `BuildResult(graph, ambiguity_sidecar, conflicts_sidecar, summary)` with full R1-R5
conflict resolution, GraphDiff, and GraphSummary.

---

## Startup

- Registered at PID 9344. Inbox watched throughout.
- Phase 1 gate: `.011` confirmed at `257d19df`, `.013` confirmed at `dcdfa5a0`.
- GO received from `2.1.0_SA_COO` after `.013` shipped.
- New protocol noted: COMP_LEARNS DS agents own `git push` to CLOUD (no DT wait).

---

## Work Completed

**Implementation files (all new):**

| File | Purpose |
|------|---------|
| `comp/graph_builder/build.py` | `build()` entry + `Builder` class + `__main__` CLI |
| `comp/graph_builder/canonicalize.py` | NodeRef format validation + path normalization |
| `comp/graph_builder/dedup.py` | `make_dedup_key()` + `canonical_dedup()` |
| `comp/graph_builder/conditions.py` | `ConditionNode` materialization from ConditionRefs |
| `comp/graph_builder/ambiguity.py` | confidence separation + `AmbiguousEdge` sidecar |
| `comp/graph_builder/conflicts.py` | R1-R5 rules + `ConflictingProvenanceError` |
| `comp/graph_builder/diff.py` | `diff(old, new)` — entity-stream delta, manifest-agnostic |
| `comp/graph_builder/summary.py` | `compute()` — per-kind counts + fractions |

**Test files (TDD — written before implementation):**

| File | Coverage |
|------|---------|
| `test_conflict_policy.py` | R1/R2/R3/R4/R5 — 11 tests |
| `test_build_dedup.py` | dedup invariant — 5 tests |
| `test_diff.py` | GraphDiff invariants + manifest-agnostic — 7 tests |
| `test_conflict_sidecar_schema.py` | ConflictedEdge schema — 6 tests |
| `test_summary_fractions.py` | fraction math + edge/node counts — 9 tests |
| `test_end_to_end_httpx.py` | httpx integration — 6 tests + conflict_fraction==0 |

**Total: 51/51 tests pass.**

---

## Decisions Made

1. **Attribute-priority merge for R2**: `guard` (unconditional > conditional) and `binding`
   (resolved > unresolved) are resolved by priority during R2 merge — no sidecar entry emitted.
   `resolution` (static vs dynamic) has no priority and triggers R5 if contradictory.
   **Rationale**: httpx legitimately imports the same module at top-level (unconditional) AND
   inside a function (conditional). Without priority merge, these 3 cases triggered false R5
   conflicts and violated the single-subtype invariant. The fix is principled: unconditional
   dominates conditional (the dependency always exists if any occurrence is unconditional).

2. **R2 no sidecar**: Successful R2 merges do NOT produce `conflicts_sidecar` entries.
   The sidecar tracks genuine conflicts (R1 losers, R5 elevations) that affect the bench
   penalty metric. A clean merge is not a conflict.

3. **comp-xref N/A**: `comp-xref` indexes the production pipeline graph (`data/black_diamond/`);
   it does not index `comp/` research modules. Module visibility verified via Phase 1 import
   check and 51 passing tests. Noted per mandate.

---

## Files Modified

- `comp/graph_builder/build.py` (new)
- `comp/graph_builder/canonicalize.py` (new)
- `comp/graph_builder/dedup.py` (new)
- `comp/graph_builder/conditions.py` (new)
- `comp/graph_builder/ambiguity.py` (new)
- `comp/graph_builder/conflicts.py` (new)
- `comp/graph_builder/diff.py` (new)
- `comp/graph_builder/summary.py` (new)
- `comp/graph_builder/tests/test_conflict_policy.py` (new)
- `comp/graph_builder/tests/test_build_dedup.py` (new)
- `comp/graph_builder/tests/test_diff.py` (new)
- `comp/graph_builder/tests/test_conflict_sidecar_schema.py` (new)
- `comp/graph_builder/tests/test_summary_fractions.py` (new)
- `comp/graph_builder/tests/test_end_to_end_httpx.py` (new)
- `org/tier2_senior/1.3.0_DS_CompLearns/task_orders/COMP_LEARNS.014.graph-builder.md` (staged→complete)

---

## Compiler Tools

| Phase | Run | Observed | Pass/Fail |
|-------|-----|----------|-----------|
| 1 | `python -c "from comp.graph_builder import GraphBuilder, BuildResult, GraphDiff, ConflictedEdge; from comp.compiler_subtypes.imports import ImportsSubtype; from comp.parsers.python import PythonParser; print('deps ok')"` | `deps ok` | PASS |
| 1 | `pytest comp/graph_builder/tests/test_conflict_policy.py -v` | ImportError (no impl yet — expected) | PASS (fixtures exist, fail as expected) |
| 1 | SubtypeRecord construct check | Prints `imports` | PASS |
| 2 | `pytest comp/graph_builder/tests/test_conflict_policy.py -v` | 11/11 pass | PASS |
| 2 | `pytest comp/graph_builder/tests/test_diff.py -v` | 7/7 pass | PASS |
| 2 | `pytest comp/graph_builder/tests/test_end_to_end_httpx.py -v` | 6/6 pass (after attribute-priority fix) | PASS |
| 2 | `pytest comp/graph_builder/ -v` | 51/51 pass | PASS |
| 2 | `.tools/ds-commit-gate.sh <14 files>` | OK: pre-commit gate clean | PASS |
| 3 | `python -m comp.graph_builder.build --records /tmp/imports_records.jsonl --target-root comp/targets/httpx/ --summary-only` | edge_count=211, conflict_fraction=0.0 | PASS |
| 3 | `comp-xref` | N/A — indexes prod pipeline, not comp/ research modules | N/A (noted) |

---

## httpx Graph Summary (end-to-end, `httpx/` subdirectory only)

```json
{
  "node_count": 76,
  "edge_count": 211,
  "condition_count": 0,
  "per_node_kind": {"module": 76},
  "per_edge_kind": {"imports": 211},
  "heuristic_fraction": 0.0,
  "ambiguous_fraction": 0.0,
  "conflict_fraction": 0.0
}
```

---

## Blockers

None.

---

## Current State

COMP_LEARNS.014 COMPLETE. `.015 bench-scorecard-ab` (1.4.0_DS_CompLearns) was unblocked
by this commit per COO dispatch message. `.017 e2e-v0-ratchet-httpx` (my next TO) is staged;
still gated on `.015` + `.020` + `.021` landing.

---

## Next Steps

1. Push to CLOUD (protocol: DS owns push).
2. MCP COMPLETE to `2.1.0_SA_COO`.
3. Stand by for `.017` GO — blocked until `.015`/`.020`/`.021` ship.
