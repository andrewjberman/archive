# Phase 3 Certification — COMP_LEARNS httpx runtime

**Role:** 2.1.0_SC_CompLearns  
**Date:** 2026-04-21  
**Phase boundary:** Phase 3 close (post-.027b Option A+)  
**Phase close commit:** `d047496a` (tag: `comp-learns-phase3-closed`)  
**Baseline report:** `org/tier2_senior/2.1.0_SC_CompLearns/deliverables/scorer_stability_baseline.md`

---

## 1. What Phase 3 committed to

Per `docs/architecture/COMP_LEARNS_RUNTIME_V1.md §14` success bar:
- Cache-bound primary_metric computation (CacheMissDuringPrimaryMetric on miss)
- schema_version=2 with judge_mode + benchmark_honest fields
- Three-key compare (primary_metric → structural_f1 → compiler_loc)
- TIED verdict that does not rewrite champion
- tied_at_best + winners_at_best + random_unique_win fields
- Benchmark-honest flag derivation (single authoritative path)
- End-to-end real-judge proving sequence

---

## 2. What actually shipped

| Deliverable | Commit | Tag |
|-------------|--------|-----|
| Cache-bound scoring (.023) | `41225ed9` | — |
| schema_version=2 + experiment_log v2 (.024) | `506a9466 + bcf47646` | — |
| AB cache instrumentation + CacheProvenance (.025) | `e7a12a12` | — |
| tied_at_best + winners_at_best + random_unique_win (.026) | `53386ec7` | — |
| Real-judge proving sequence + Option A+ reset (.027 + .027b) | `af89f12e + 1e5d67b2` | `comp-learns-v1-proving-complete` |
| Legacy decommission + inventory (.028 Phase 1-2) | `5622dad4 + 09f7e798` | — |
| SC role instantiation | `d047496a` | `comp-learns-phase3-closed` |

Proving sequence tags: `comp-learns-v1-proving-start` (d27790c1), `comp-learns-v1-proving-reset` (3fb8b694), `comp-learns-v1-proving-complete`.

---

## 3. Twelve-point checklist signoff (by reference)

All 12 checklist items run in full. See `scorer_stability_baseline.md` for complete evidence and verdicts.

| § | Item | Verdict |
|---|------|---------|
| 4.1 | Truth Surface | PASS |
| 4.2 | Score Identity | PASS with caveat (champion.json lacks judge_mode — v1.1 item) |
| 4.3 | Deterministic Core | PASS |
| 4.4 | Model-Mediated Scoring | PASS |
| 4.5 | Selector Integrity | PASS |
| 4.6 | Formula Simplicity | PASS |
| 4.7 | Champion / Compare Semantics | PASS with caveat (v1.1 judge_mode field) |
| 4.8 | Artifact Authority | PASS |
| 4.9 | Schema Discipline | PASS |
| 4.10 | Reproducibility Proof | PASS (5/5 demonstrations, AC#2 partial per pre-warming) |
| 4.11 | Benchmark Honesty Flag | PASS |
| 4.12 | Undocumented Load-Bearing Surfaces | PASS (1 known + 3 new findings; none blocking) |
| 4.13 | Context Isolation Integrity | NOT-YET-APPLICABLE (pre-parallel regime) |
| 4.14 | Scoring Regime Homogeneity | NOT-YET-APPLICABLE (pre-parallel regime) |
| 4.15 | Cross-Run Comparability Certification | NOT-YET-APPLICABLE (pre-parallel regime) |

---

## 4. Minimal Exit Bar

All 7 sequential criteria: PASS. See `scorer_stability_baseline.md §13`.

---

## 5. Caveats

**Caveat A — champion.judge_mode (v1.1 parking-lot):** `champion.json` does not carry a `judge_mode` field. The Option A+ reset (`d047496a`) wiped the mock-baseline champion and replaced it with a real-judge champion (sha=3fb8b69, pm=0.0664, benchmark_honest=true). The immediate mock/real divergence is resolved. Adding `champion.judge_mode` remains a v1.1 item. This SC endorses that prioritization. Re-open trigger: compare semantics + champion-state (see baseline §15).

**Caveat B — §12 new findings (pre-parallel documentation gap):** Three load-bearing surfaces identified in this review that are undocumented: (1) AB cache path double-nesting (`ab_cache/ab_cache/` not `ab_cache/`), (2) AB cache is not git-tracked despite docstring claim, (3) `Scorecard.__eq__` excludes judge_model_id. None block Phase 3/4 operations under the current sequential single-worktree workflow. All three must be documented before parallel-regime scoring begins (PARALLELIZATION_V1 operationalization), as fresh-worktree operations and cross-run comparisons are affected.

**Caveat C — proving sequence cold-cache gap:** AC#2 of the Option A+ proving run expected `warm_up_entries_written > 0` on Run A1. Actual: 0 (cache pre-warmed by VOID'd runs). Infrastructure correct; sequence setup condition only. A future re-baseline from cold cache should record this metric as a test of the warm-up path.

---

## 6. Signoff

Scorer stable for post-.027b httpx real-judge regime. Minimal Exit Bar satisfied (7/7). Items 13-15 not-yet-applicable (pre-parallel regime, no comparison events). This baseline becomes the reference artifact for Phase 4 and beyond.

**Recommendation: YELLOW** — Phase exit permitted. Caveats A and B must be resolved before PARALLELIZATION_V1 operationalization.

Comparability class: **Locally valid** (single certification run, pre-parallel regime, no cross-run comparison events yet).

*"Scorer stable for post-.027b real-judge regime. Minimal Exit Bar satisfied. Comparability class: locally-valid. Baseline report at org/tier2_senior/2.1.0_SC_CompLearns/deliverables/scorer_stability_baseline.md @ commit pending."*

— 2.1.0_SC_CompLearns, 2026-04-21
