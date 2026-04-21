# Session Log — COMP_LEARNS.025 — compare-explainability + cache-provenance

**Agent:** 1.3.0_DS_CompLearns
**Date:** 2026-04-21
**TO:** COMP_LEARNS.025.compare-explainability-and-cache-provenance
**Session type:** Phase 2 implementation

---

## Objective

Make every KEEP/TIED/DISCARD/FORKED verdict reconstructable from artifacts alone, and make the cache inspectable enough to tell whether a benchmark result was driven by warm-up, cache reuse, or actual model variance.

---

## Work Completed

### 1. `comp/bench/cache.py` — per-selector counters

Added `_hits_by_selector` and `_misses_by_selector` dicts to `ABCache.__init__` (zeroed on construction). Threaded `selector_name: str = ""` through `get()` and `require_hit()`. `get()` increments the hit counter on non-None return and the miss counter on None return. `require_hit()` delegates to `get()` with selector_name then raises `CacheMissDuringPrimaryMetric` on None. Added `hits_by_selector` and `misses_by_selector` read-only properties (return copies).

### 2. `comp/bench/ab.py` — thread selector_name through calls

- `warm_up_cache`: `cache.get(key, selector_name=selector.name)` — hit/miss tracked correctly per selector during warm-up.
- `run`: `cache.require_hit(..., selector_name=selector.name)` — hit/miss tracked per selector during primary-metric phase.

### 3. `comp/bench/scorecard.py` — CacheProvenance dataclass + Scorecard field

Added `CacheProvenance` dataclass (6 fields: `compiler_sha`, `target_version`, `judge_model_id`, `warm_up_entries_written`, `hits_by_selector`, `misses_by_selector`). Added `cache_provenance: CacheProvenance | None = None` to `Scorecard` (after `benchmark_honest` — all prior tests unaffected since default is None). Updated `scorecard_to_dict` to serialize as nested JSON dict (or null). Updated `scorecard_from_dict` to tolerate absent/null `cache_provenance` (loads as None — backward-compat).

### 4. `comp/bench/__init__.py` — export CacheProvenance

Added `CacheProvenance` to imports and `__all__`.

### 5. `comp/loop/ratchet.py` — three changes

**a. `_compiler_loc()` refinement (line 102):** replaced raw-line-count implementation with non-empty, non-comment line counter per TO §6 spec. Docstring-only lines inside `"""..."""` count as code (simpler heuristic, fine for tiebreak). Result: httpx compiler.py goes from 34 (raw) to 26 (refined). The absolute value changed as expected; subsequent runs on same file produce stable values.

**b. `compare_key_for()` function (new, module-level):** placed before `_default_selectors()`. Implements the three-key comparison order from `_compare()` to produce a human-readable verdict label. Returns "fork" | "primary_metric" | "structural_f1" | "compiler_loc". Unit-tested directly.

**c. `iterate()` updates:**
- Builds `CacheProvenance` at step 6 (after warm_up + ab_run, when counters are stable) and passes to `Scorecard` constructor via `cache_provenance=cache_prov`.
- Computes `compare_key = compare_key_for(verdict, candidate_sc, champion_data)` at step 11 start (champion_data is the pre-iteration snapshot — snapshot-timing rule preserved).
- Adds 9 new fields to `explog.append` extra dict: `compare_key`, `candidate_primary_metric`, `champion_primary_metric_before`, `candidate_structural_f1`, `champion_structural_f1_before`, `candidate_compiler_loc`, `champion_compiler_loc_before`, `cache_hits` (sum of hits_by_selector), `cache_misses` (sum of misses_by_selector).

### 6. Tests (3 new files, 22 new tests)

- `comp/loop/tests/test_compare_explainability.py` — 8 tests: all 4 verdict cases for compare_key_for, fork variants, snapshot semantics, no-champion case, REVERT case.
- `comp/bench/tests/test_cache_provenance.py` — 5 tests: hits_by_selector keys match selectors, cache_hits mirror, zero misses in primary-metric phase (warm cache), pre-.025 loader backward-compat, round-trip serialization.
- `comp/bench/tests/test_compiler_loc_refined.py` — 9 tests: code-only count, blank exclusion, comment-only returns 0, empty file, missing file, None, docstring lines count, inline-comment-suffix counts, stability.

---

## Smoke Test Results (AC 6)

```
python comp/bin/comp-learns-ratchet httpx --judge mock --max-iter 1
exit=MAX_ITER  verdict=kept  compare_key=compiler_loc
champion: sha=53386ec primary_metric=1.2439 structural_f1=0.5743 loc=26
```

Resulting scorecard (53386ec_909ea79f.json):
```json
"cache_provenance": {
  "compiler_sha": "53386ec",
  "target_version": "909ea79f63e9...",
  "judge_model_id": "gold-aware-mock",
  "warm_up_entries_written": 0,
  "hits_by_selector": {"centrality": 38, "keyword": 38, "random": 38},
  "misses_by_selector": {}
}
```

Experiment log last entry extra:
```
compare_key: compiler_loc
candidate_primary_metric: 1.2439
champion_primary_metric_before: 1.2439
candidate_structural_f1: 0.5743
champion_structural_f1_before: 0.5743
candidate_compiler_loc: 26
champion_compiler_loc_before: 34
cache_hits: 114
cache_misses: 0
```

AC 7 check: `cache_hits=114 == sum(38+38+38)=114` ✓
AC 8 check: `cache_misses=0` ✓ (fully warm cache, zero primary-metric misses)

---

## Acceptance Criteria Status

| AC | Description | Status |
|----|-------------|--------|
| 1 | compare_key correctness — four cases (unit tests) | PASS |
| 2 | Snapshot values match champion-before state | PASS |
| 3 | No-champion case: all champion_*_before fields null, compare_key="primary_metric" | PASS |
| 4 | Refined LoC: blank/comment exclusion, edge cases | PASS |
| 5 | LoC in experiment log; stable subsequent runs | PASS |
| 6 | cache_provenance non-null with all 6 fields after mock run | PASS |
| 7 | cache_hits == sum(hits_by_selector.values()) | PASS |
| 8 | Primary-metric-only path: misses_by_selector all zeros | PASS |
| 9 | Pre-.025 scorecards load without error, cache_provenance=None | PASS |
| 10 | Existing tests green (198 passed) | PASS |
| 11 | Pre-commit gate: ds-commit-gate.sh clean on all 8 .py files | PASS |

---

## Decisions Made

- `_compiler_loc` implemented exactly per TO wire contract. Docstring lines count as code (simpler heuristic). `champion_compiler_loc_before=34` on first post-refinement run reflects old raw count stored in champion.json — this is expected per TO operational notes.
- `cache_provenance` set in Scorecard constructor at step 6 (after ab_run counters are stable). No post-construction mutation needed.
- `compare_key_for` is module-level (not inner function) to enable direct unit testing.
- TO file is untracked; not committed per COO instruction — CTO will commit as initial commit per RAVC.

---

## Files Modified

| File | Action |
|------|--------|
| `comp/bench/cache.py` | Modified — per-selector counters + selector_name params |
| `comp/bench/scorecard.py` | Modified — CacheProvenance dataclass + Scorecard field + serialization |
| `comp/bench/ab.py` | Modified — selector_name threaded through cache calls |
| `comp/bench/__init__.py` | Modified — CacheProvenance export |
| `comp/loop/ratchet.py` | Modified — _compiler_loc refinement + compare_key_for + iterate() updates |
| `comp/loop/tests/test_compare_explainability.py` | Created — 8 tests |
| `comp/bench/tests/test_cache_provenance.py` | Created — 5 tests |
| `comp/bench/tests/test_compiler_loc_refined.py` | Created — 9 tests |

---

## Compiler Tools

| Phase | Tool | Run | Result |
|-------|------|-----|--------|
| Before write | `comp-blast ratchet` | Before starting | No graph node match for "ratchet" (script nodes have no edges — expected per table note). Proceeded. |
| Before commit | `ds-commit-gate.sh` | All 8 .py files | OK: pre-commit gate clean for 8 file(s) |
| After commit | `pytest comp/loop/tests/ comp/bench/tests/ -q` | 198 tests | 198 passed, 0 failed |

---

## Current State

COMP_LEARNS.025 COMPLETE. All 11 AC green. 22 new tests + 198 total tests passing. Commit pending — see commit sha in TO status field.
