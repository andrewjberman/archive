# Task Order: ADVI_INFETL.BRONZE-FIX (structural #2)
## _BRONZE_COMPLETE required-dim contract (kills the silent-partial-success class)

**Project:** ADVI_INFETL (bronze completion-gate hardening)
**Assigned to:** 0.6.0_AE_PartnerETL
**Priority:** P1 — structural prevention of the silent-partial class (CTO-assigned post-recovery TO #2)
**Authority:** CTO root-cause (relay 204522Z); Andrew live-P0 2026-06-12

---

## Context

In the 2026-06-12 inf-ADVI P0, the bronze run pulled all dims EXCEPT transactions (stale orchestrator missing it), yet `_BRONZE_COMPLETE` reported SUCCESS. That false-success is the dangerous part: gold correctly held fail-closed downstream, but only because gold had its own check — the bronze layer itself signaled complete on a PARTIAL pull. A missing required dim should make bronze report INCOMPLETE/FAIL, loudly, not silently succeed.

---

## Scope

1. **Define the required-dim contract per firm/pipeline:** the set of dims a bronze run MUST produce to be COMPLETE (inf: the full 8-dim set incl. transactions; cot/bd: their required sets). Source the contract from a declared config (not hardcoded), so it's auditable + extensible.
2. **`_BRONZE_COMPLETE` enforces it:** a run that produced fewer than the required dims → status INCOMPLETE (or a distinct PARTIAL state), NOT success. Loud log naming the missing dim(s). The success sentinel is withheld (so downstream correctly sees stale, like the cot realized/unrealized template-fail pattern did correctly).
3. **Surface the partial state** so it's visible (CloudWatch + the run report), not buried — a partial bronze should be as loud as a hard failure.
4. **Do NOT over-rotate:** if a dim is legitimately empty (0 rows, not 0 pulled), that's COMPLETE-with-empty, distinct from MISSING-dim. The contract checks the dim was ATTEMPTED+pulled, not that it's non-empty.

---

## Acceptance Criteria

- AC1: per-firm required-dim contract in a declared config (auditable)
- AC2: `_BRONZE_COMPLETE` returns INCOMPLETE/PARTIAL (not success) when a required dim is absent; loud log names it
- AC3: legitimately-empty dim = COMPLETE-with-empty (not a false INCOMPLETE) — the attempted-vs-nonempty distinction
- AC4: partial state visible in CloudWatch + run report
- AC5: replay of the 2026-06-12 inf scenario (orchestrator missing transactions) → bronze now reports INCOMPLETE, sentinel withheld

## RAVC2 to COO
Commit + the dim-contract config + the replay-test result (the incident scenario now caught). CC CTO + CVO.

---

*Dispatched by 2.0.0_SA_COO 20260612T204800Z — Andrew-direct full-drive (no slowdown)*
*CTO structural-TO #2*
