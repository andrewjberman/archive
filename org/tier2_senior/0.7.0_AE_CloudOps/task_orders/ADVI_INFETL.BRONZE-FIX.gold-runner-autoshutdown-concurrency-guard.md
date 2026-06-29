# Task Order: ADVI_INFETL.BRONZE-FIX (structural #9 / follow-up h)

> **[CLOSED — COMPLETE-SUPERSEDED 2026-06-29, COO 2.0.0_SA_COO]** Absorbed into Andrew-confirmed-closed ADVI_INFETL (closed 2026-05-25). Safety-net backstop: 0.7.0_AE_CloudOps~A is spot-checking this guard against the LIVE inf gold runner; if genuinely ABSENT it re-files under NFRA_INFRPT so the hardening is not buried. MSTR-delegated orphan cleanup (20260629T130229Z).
## Gold-runner auto-shutdown concurrency guard (the 21:27Z near-miss that nearly killed the recovery)

**Project:** ADVI_INFETL (runner lifecycle safety)
**Assigned to:** 0.7.0_AE_CloudOps (EC2/runner infra)
**Priority:** P1 — a near-miss that almost killed the LIVE recovery mid-flight. Real catastrophic-race risk.
**Authority:** DS recovery report a3f53eeb7 follow-up (h); the 21:25-21:27Z near-miss

---

## Context — the near-miss

During the recovery, DS pre-landed the eclipse trio via `--chain eclipse` (concurrent with the full gold chain still running). **The eclipse chain's completion ARMED the gold-runner's 2-minute auto-shutdown — while the full chain was still in flight.** DS caught it and cancelled the shutdown via SSM (SHUTDOWN-CANCELLED) at 21:27Z; the full chain was confirmed alive. But it was a NEAR-MISS: had it not been caught, the auto-shutdown would have killed the in-flight recovery chain, prolonging the P0.

Root: the gold-runner's auto-shutdown arms on ANY chain completion WITHOUT checking whether OTHER chains are still running on the instance.

---

## Scope

1. **Concurrency-aware shutdown:** the auto-shutdown must check for OTHER running chains/processes on the instance before arming. If any chain is in-flight, DO NOT arm (or defer the shutdown until all chains complete).
2. **Shutdown-arm visibility:** an armed auto-shutdown should be observable (log/metric) so a concurrent operator (or the FATAL-channel from #7) can see it coming.
3. **Idempotent cancel:** the SSM SHUTDOWN-CANCELLED path DS used should be a first-class, idempotent operation (not an ad-hoc save).
4. **Applies to all chain-bearing runners** (gold, eclipse, bronze-runner) — consistency mandate.

---

## Acceptance Criteria

- AC1: auto-shutdown checks for other running chains before arming; in-flight chain → no-arm/defer
- AC2: an armed shutdown emits an observable signal (log + metric)
- AC3: replay the 21:25Z scenario (eclipse completes while full chain runs) → shutdown does NOT arm (full chain protected)
- AC4: idempotent cancel path documented
- AC5: covers gold + eclipse + bronze-runner runners

## RAVC2 to COO
Commit + the concurrency-guard logic + AC3 replay (the near-miss scenario now safe). TF/runner change via Rule-2 cycle (this is infra). CC CTO + CVO.

---

*Dispatched by 2.0.0_SA_COO 20260612T213200Z — Andrew-direct full-drive*
*DS recovery report a3f53eeb7 follow-up (h); the 21:27Z near-miss that nearly killed the recovery*
