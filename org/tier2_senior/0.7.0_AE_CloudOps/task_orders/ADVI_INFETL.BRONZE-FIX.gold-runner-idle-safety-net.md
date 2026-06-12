# Task Order: ADVI_INFETL.BRONZE-FIX (structural #10 / finding #9-F1)
## Gold-runner idle safety net — CW overrun alarm (now) + watchdog re-arm (trace-first)

**Project:** ADVI_INFETL (runner lifecycle safety + cost)
**Assigned to:** 0.7.0_AE_CloudOps (EC2/runner infra; pairs with #9)
**Priority:** P1 — stranded-runner cost leak (COSTRECON 2d class) + safety; tonight proved hard-crashed dispatches happen
**Authority:** CTO ruling 220545Z (#9-F1); AE 0.7's BRONZE-FIX #9 surfaced it (555ea1e44)

---

## Context — the gap #9 surfaced

run-gold-layer.sh REMOVES the watchdog timer at boot (stops + deletes unit files + daemon-reload). So the inf gold runner has NO idle safety net — the dispatch-completion arm (#9 made it concurrency-safe) is the ONLY normal shutdown path. A dispatch that crashes HARD (OOM/SIGKILL) before reaching its arm strands the instance running INDEFINITELY ($35.96/mo top cost node at part-time duty → a stranded indefinite-run multiplies it). CTO REJECTED accept: this is a silent cost leak + a real risk (tonight proved hard-crashes happen).

---

## Scope — TWO legs, TWO gates (CTO ruling: BOTH nets, not either/or)

### LEG A — CW running-past-window alarm (LANDS IMMEDIATELY — pure observability, zero instance-side risk)
- CloudWatch alarm on the gold runner instance running PAST its expected window → opal-critical-surface-alerts (the D8 item2c topic).
- Window = a GENEROUS multiple of the empirical chain envelope (06-11 precedent ~1h49m), MODE-AWARE (backfill runs longer than a daily — don't false-fire on a legitimate backfill).
- This is the INDEPENDENT net: it catches the watchdog itself dying, AND a hard-crash-before-arm, AND any other indefinite-run cause. Lands now via the normal Rule-2 TF cycle (+ completion-ledger entry).

### LEG B — watchdog re-arm, sequenced post-dispatch (TRACE-FIRST gate)
- **TRACE FIRST (binding):** verify WHY the watchdog was removed before re-arming. AE's hypothesis (debugging-era artifact — removed to stop premature shutdown before SSM dispatch arrival) is PLAUSIBLE but gets VERIFIED, not assumed. If the trace reveals a deeper incompatibility (long chains, multi-chain), SURFACE before implementing.
- Fix shape (post-trace): re-arm the watchdog SEQUENCED post-dispatch-arrival (fixes the original race by ORDERING, not deletion) + CARRY #9's concurrency guard (so the watchdog can't recreate the (h) near-miss). Self-skips while gold processes run (pgrep-stamp logic).
- Lands via the normal deploy cycle + a completion-ledger entry (deploy_ledger.py open).

---

## Acceptance Criteria

- AC1 (Leg A): CW overrun alarm live → critical-surface topic; window = generous mode-aware multiple; verified no-false-fire on a legitimate backfill envelope
- AC2 (Leg B trace): the watchdog-removal rationale traced + documented BEFORE the re-arm; deeper-incompatibility findings surfaced to CTO/COO
- AC3 (Leg B fix): watchdog re-armed sequenced post-dispatch-arrival, carrying #9's concurrency guard; self-skips during active gold processes; replay = hard-crash-before-arm → watchdog reaps the idle instance
- AC4: both legs covered by deploy-ledger entries (NO-HALF-DEPLOYS); Leg A lands now, Leg B post-trace
- AC5: stranded-runner replay (dispatch SIGKILL'd before arm) → CW alarm fires + (post-Leg-B) watchdog reaps

## RAVC2 to COO (per leg)
Leg A: alarm live + window rationale + no-false-fire proof. Leg B: the trace finding (rationale) + the sequenced re-arm + replay. CC CTO + CVO.

---

*Dispatched by 2.0.0_SA_COO 20260612T220600Z — Andrew-direct full-drive*
*CTO ruling 220545Z (#9-F1, BOTH-nets + trace-first); pairs BRONZE-FIX #9*
