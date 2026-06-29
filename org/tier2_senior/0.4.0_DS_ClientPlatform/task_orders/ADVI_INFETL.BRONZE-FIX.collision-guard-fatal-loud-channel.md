# Task Order: ADVI_INFETL.BRONZE-FIX (structural #7 / follow-up f)

> **[CLOSED — COMPLETE-SUPERSEDED 2026-06-29, COO 2.0.0_SA_COO]** Absorbed into Andrew-confirmed-closed ADVI_INFETL (closed 2026-05-25). DS-lane inf hardening; no live-runner safety gap indicated. MSTR-delegated orphan cleanup (20260629T130229Z).
## Collision-guard FATAL loud channel (the silent-outage fix — why nobody saw it from 13:00Z)

**Project:** ADVI_INFETL (runtime-failure visibility)
**Assigned to:** 0.4.0_DS_ClientPlatform (owns the gold runner / sync_scripts guard); coordinate AE on CW/SNS wiring
**Priority:** P1 — the CORE detection failure of the 2026-06-12 P0. Designs cohesively with TO #5 (DS's (f) leg per CTO).
**Authority:** DS recovery report a3f53eeb7 follow-up (f); Andrew-direct (the outage was silent 13:00Z→20:37Z until a human noticed)

---

## Context — the silent-FATAL is the root detection failure

Today's gold chain died at 13:00Z on a sync_scripts() basename-collision FATAL. The guard was CORRECT (fail-closed). But it was INVISIBLE: on-instance, pre-log-upload, holding the dispatch lock, with NO CloudWatch metric / SNS alarm / surface of any kind. The outage ran from 13:00Z until Andrew noticed stale ADVI at 20:37Z — **7.5 hours of silent served-data staleness.** A fail-closed guard that fails SILENTLY defeats its own purpose: it correctly stopped bad data, but nobody knew, so stale data kept serving.

---

## Scope

1. **FATAL → loud channel:** when sync_scripts() (or any gold-chain fail-closed guard) FATALs, emit a CloudWatch metric + SNS alarm (→ opal-critical-surface-alerts, the D8 item2c topic). The guard's correct fail-closed STOP must be VISIBLE, not silent.
2. **Lock-holder liveness check:** the dead 13:00Z chain held the dispatch lock with no live process (NO-CHAIN-PROCESS). A lock held by a dead holder must be detectable + surface (stale-lock alarm) — so a chain that can't re-dispatch because of a dead-holder lock blares, rather than silently never running.
3. **Pre-log-upload visibility:** the FATAL happened before any log upload — so even the log trail was empty. Ensure the FATAL path emits its signal BEFORE/independent of the log-upload step (the CW metric fires even if the instance dies).
4. **Consistency mandate (Andrew):** applies to the eclipse + mdpf chain guards SAME as the orion-api gold guard.

---

## Acceptance Criteria

- AC1: a sync_scripts/guard FATAL emits a CW metric + SNS alarm to opal-critical-surface-alerts (visible, not silent)
- AC2: a dispatch lock held by a dead process surfaces (stale-lock alarm) within a bounded window
- AC3: the FATAL signal fires independent of the log-upload step (survives instance death)
- AC4: replay the 13:00Z scenario → the collision FATAL now BLARES (CW + SNS) instead of 7.5h silence
- AC5: consistency — eclipse + mdpf guards covered same as orion-api

## RAVC2 to COO
Commit + the FATAL-channel wiring + AC4 replay (the 13:00Z silent outage now blares). CC CTO + CVO + AE (CW/SNS coordination). Designs alongside TO #5 (deploy-completion ledger) — both are P0-detection fixes.

---

*Dispatched by 2.0.0_SA_COO 20260612T213200Z — Andrew-direct full-drive*
*DS recovery report a3f53eeb7 follow-up (f); the silent-outage root of the P0*
