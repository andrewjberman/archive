# Task Order: ADVI_INFETL.BRONZE-FIX (structural #4)

**Status:** COMPLETE-SUPERSEDED

> **[CLOSED — COMPLETE-SUPERSEDED 2026-06-29, COO 2.0.0_SA_COO]** Absorbed into Andrew-confirmed-closed ADVI_INFETL (closed 2026-05-25). Safety-net backstop: 0.7.0_AE_CloudOps~A is spot-checking this guard against the LIVE inf gold runner; if genuinely ABSENT it re-files under NFRA_INFRPT so the hardening is not buried. MSTR-delegated orphan cleanup (20260629T130229Z).
## MDPF source-vintage stamping (kills the fresh-timestamp-over-stale-value display)

**Project:** ADVI_INFETL (provenance hardening, F1-class)
**Assigned to:** 0.7.0_AE_CloudOps (MDPF lane)
**Priority:** P1 — structural prevention of the stale-value-fresh-timestamp class (CTO-assigned post-recovery TO #4)
**Authority:** CTO root-cause (relay 204522Z); Andrew live-P0 2026-06-12

---

## Context

In the 2026-06-12 inf-ADVI P0, MDPF stamped a 7:30a runtime over STALE inf inputs (platinum frozen at 06-11 because the bronze transactions dim never landed). The display showed a FRESH timestamp on STALE values — exactly the misleading signal that makes a stranded-deploy hard to spot from the served surface (you trust the fresh timestamp). MDPF stamps its OWN runtime, not the VINTAGE of the source data it consumed.

---

## Scope

1. **Stamp SOURCE VINTAGE, not (just) runtime.** MDPF outputs should carry the vintage of the upstream data they consumed (the inf platinum / gold vintage), so a 7:30a run over 06-11 inputs displays "source vintage 06-11" not "fresh 7:30a." Keep the runtime too, but the SOURCE vintage is the load-bearing provenance.
2. **Propagate the vintage** from the consumed artifacts (read their F6-marker / vintage stamp) through MDPF's transforms to the served output.
3. **Surface a staleness signal** when source vintage lags runtime by > threshold (e.g. source > 26h older than run) — same class as the GLOBGRPH staleness routing (D8-AE B3). A fresh run over stale inputs should be VISIBLE as stale, not silently displayed as fresh.
4. **This is the F1-provenance class** — align with the GLOBGRPH freshness-contract pattern (provenance header semantics: current/BEHIND/UNKNOWN-VINTAGE).

---

## Acceptance Criteria

- AC1: MDPF served output carries SOURCE vintage (upstream data vintage), not just its own runtime
- AC2: vintage propagates from consumed artifacts through MDPF transforms
- AC3: source-vintage-lags-runtime > threshold → staleness signal surfaced (not silent)
- AC4: replay the 2026-06-12 scenario (7:30a run over 06-11 inputs) → display shows source vintage 06-11 + staleness flag, not misleading fresh 7:30a
- AC5: zero served-value change (this is a provenance/display addition, not a data change — never-widen clean)

## RAVC2 to COO
Commit + vintage-propagation proof + the replay (stale inputs now display stale). CC CTO + CVO.

---

*Dispatched by 2.0.0_SA_COO 20260612T204800Z — Andrew-direct full-drive (no slowdown)*
*CTO structural-TO #4; F1-provenance class, GLOBGRPH freshness-contract aligned*
