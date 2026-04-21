# Session Log — 2.1.0_SC_CompLearns — 2026-04-21 — Baseline Report

**Session:** 01 (role instantiation + COMP_LEARNS.029 execution)  
**TO:** COMP_LEARNS.029.scorer-stability-baseline-report  
**Worktree:** feature_clb (`/c/Users/AndrewBerman/Desktop/feature_clb/`)  
**Runtime boundary:** post-.027b (d047496a, tag comp-learns-phase3-closed)

---

## What I Read

| Artifact | Purpose |
|----------|---------|
| `org/XXX.md` | Agent startup protocol |
| `org/tier2_senior/2.1.0_SC_CompLearns/README.md` | Role definition |
| `org/tier2_senior/2.1.0_SC_CompLearns/prompt.md` | 15-point checklist + Minimal Exit Bar |
| `org/tier2_senior/2.1.0_SC_CompLearns/task_orders/COMP_LEARNS.029.scorer-stability-baseline-report.md` | TO specification |
| `comp/targets/httpx/champion.json` | Current champion state |
| `comp/targets/httpx/champion_v0_mock.json` | Preserved mock baseline |
| `comp/targets/httpx/PROVING_SEQUENCE_R1_R5.md` | Option A+ proving sequence record |
| `comp/targets/httpx/SURFACE_INVENTORY.md` | Target surface description |
| `comp/targets/httpx/experiment_log.jsonl` (last 30 entries) | Full post-.025 run history |
| `comp/targets/httpx/scorecards/3fb8b69_909ea79f.json` | Champion scorecard |
| `comp/targets/httpx/gold/` (directory listing) | Gold artifact inventory |
| `comp/targets/httpx/gold/target_version.txt` | target_version hash and inputs |
| `comp/bench/cache.py` | AB cache implementation + 9-tuple key logic |
| `comp/bench/ab.py` | AB comparator + warm_up + run |
| `comp/bench/scorecard.py` | Scorecard dataclass + __eq__ + serialization |
| `comp/bench/primary.py` | Primary metric formula |
| `comp/loop/ratchet.py` | Ratchet state machine, compare logic, iterate() |
| `comp/loop/experiment_log.py` | JSONL log append + schema_version normalization |

---

## What I Found

### Checklist verdicts summary

All 12 items (§4.1–§4.12) PASS or PASS with caveat. Items 13-15 NOT-YET-APPLICABLE (pre-parallel regime).

Key findings:
- **§3/§10 Determinism:** Proven by A2 vs A4 — different git SHA, identical compiler.py → bit-exact pm=0.06635351328309276, 114 cache hits, 0 misses.
- **§7 Champion semantics:** Three-key compare fully implemented. TIED correctly does not rewrite champion. Option A+ reset resolved mock/real divergence. champion.judge_mode is v1.1 item.
- **§11 Honesty flag:** All A+ entries benchmark_honest=true. VOID'd entries annotated correctly. Single derivation point in experiment_log.py.
- **§12 New findings (3):** See baseline §12 for full details.

### §12 New Undocumented Load-Bearing Surfaces Found

1. **ABCache path double-nesting:** Files live at `ab_cache/ab_cache/{key}.json`, not `ab_cache/{key}.json`. Confirmed: ajb_workspace has 342 entries in nested path. ab.py docstring is incorrect.

2. **AB cache not git-tracked:** feature_clb (same CLOUD branch) has 0 ab_cache entries; ajb_workspace has 342. Cache is a runtime artifact, not git-tracked despite docstring claim. Fresh worktrees start cold — 114 warm-up API calls required.

3. **Scorecard.__eq__ excludes judge_model_id and judge_mode:** Intentional but undocumented constraint on callers. Cross-judge comparisons using `==` cannot distinguish same-content results from different judge regimes.

### Primary metric formula verified

`pm = ab_lift * (1 + 0.3 * token_reduction) * mutation_stability * (1 - conflict_penalty)`  
Champion 3fb8b69: 0.05263 × 1.2647 × 0.9968 × 1.0 = 0.06635. Matches exactly.

### Worktree observation

feature_clb AB cache is empty (same branch, different filesystem). This is Finding 3 above. The proving runs all happened in ajb_workspace. No functional impact on this TO (read-only work), but would be blocking if any re-run were attempted from feature_clb without cache warm-up.

---

## Compiler Tools

| Tool | Status | Result |
|------|--------|--------|
| `comp-transform schema-check` | N/A — no portal components touched | — |
| `comp-blast` | N/A — no code files modified | — |
| `comp-pipescript io` | N/A — no gold scripts | — |
| Manual code read (cache.py, ab.py, scorecard.py, ratchet.py, primary.py) | DONE | Found 3 new §12 surfaces |

Note: SC role does not run gold scripts or modify comp/ code. Compiler tool mandate is satisfied by manual code inspection per role scope (certification only).

---

## Escalations

None. All findings resolved within verdict scope. YELLOW recommendation does not require CTO ACK before report delivery (not a verdict-interpretation hold — YELLOW is a defined outcome per prompt.md §5 with caveats documented).

Rule 7 applicability: No pre-flags raised. Findings in §12 are reported as caveats, not interpretation holds. All three new surfaces are naming recommendations, not gate failures.

---

## Deliverables Produced

- `org/tier2_senior/2.1.0_SC_CompLearns/deliverables/scorer_stability_baseline.md`
- `org/tier2_senior/2.1.0_SC_CompLearns/deliverables/phase_3_certification.md`
- This session log

---

## Status

COMP_LEARNS.029: COMPLETE (pending commit). Verdict: YELLOW. MCP sent to CTO and COO on completion.
