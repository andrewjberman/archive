# Task Order: ADVI_INFETL.BRONZE-FIX (structural #6 / follow-up e)

**Status:** COMPLETE-SUPERSEDED

> **[CLOSED — COMPLETE-SUPERSEDED 2026-06-29, COO 2.0.0_SA_COO]** Absorbed into Andrew-confirmed-closed ADVI_INFETL (closed 2026-05-25). DS-lane inf hardening; no live-runner safety gap indicated. MSTR-delegated orphan cleanup (20260629T130229Z).
## inf-api-txn sentinel RE-KEY to serving-day (NOT a date flip — the partial-day trap)

**Project:** ADVI_INFETL (quorum-keying correctness)
**Assigned to:** 0.4.0_DS_ClientPlatform (owns (e), recovery lane)
**Priority:** P1 — the ~20h-late-gold defect (L2 of tonight's P0). QUEUED post-recovery.
**Authority:** CTO ruling 1a1d555f2 (the (e) trap named explicitly); DS recovery report a3f53eeb7 follow-up (e)

---

## Context — and THE TRAP (CTO named it so nobody walks into it)

L2 of tonight's P0: inf-api-txn defaults date=now-1d; its 13:00Z run today processed 06-11, leaving 06-12 quorum at 8/9. Surface temptation: "flip the default to same-day." **THAT IS WRONG — DO NOT FLIP THE DATE.**

Per CTO ruling 1a1d555f2:
- inf-api-txn's D-1 default is NOT a bug — transactions for day D are only COMPLETE after D ends. A same-day flip would pull PARTIAL days. (And the "same-day" dims are D-1-vintage anyway — Orion's morning update serves through prior close.)
- The REAL defect is KEYING: the D 13:00Z run pulls D-1-COMPLETE transactions but sentinels them under D-1's quorum → day-D gold fires at D+1, ~20h late on data that was available at D 13:05Z.

---

## Scope — the FIX

**Re-key the sentinel to SERVING-DAY D, data semantics UNCHANGED.** The D 13:00Z inf-api-txn run pulls the same (D-1-complete) transactions, but writes its sentinel under serving-day D's quorum (`silver/_silver_complete/D/`), so day-D gold fires that same morning ~13:05Z with a vintage-consistent build — exactly Andrew's stated freshness expectation (morning-fresh, served-through-prior-close).

- DO NOT change WHICH data is pulled (D-1-complete transactions stay; that's correct).
- CHANGE the sentinel KEY (which quorum-day it completes) from D-1 to serving-day D.
- Stamp the vintage semantics in the sentinel (#4 source-vintage pattern) so the build's data-vintage is explicit (D-1-complete, served day D).
- Consistency: applies to the eclipse + mdpf legs' quorum keying same as orion-api (CTO consistency mandate).

---

## VINTAGE-SHIFT SIGN-OFF (CTO+COO, per ruling §3)

The re-key MOVES when served output updates — a day earlier, TOWARD already-available truth (correctly fresher, not a widen). The FIRST re-keyed morning is a VERIFIED VINTAGE-SHIFT: capture a before/after artifact pair + CTO+COO note. NOT silent — it's a deliberate, ratified freshness improvement. This is never-widen-adjacent but moves toward truth, so it's a verified-shift not a widen-block.

---

## Acceptance Criteria

- AC1: sentinel re-keyed to serving-day D (data pulled unchanged — D-1-complete transactions)
- AC2: day-D gold fires ~13:05Z same morning (not D+1)
- AC3: vintage stamped in the sentinel (#4 pattern — explicit D-1-complete-served-day-D)
- AC4: NO partial-day pull (the trap avoided — verify a same-day run still pulls D-1-complete, not partial-D)
- AC5: first re-keyed morning = before/after artifact pair + CTO+COO vintage-shift note
- AC6: consistency — eclipse + mdpf quorum keying covered

## RAVC2 to COO
Commit + the re-key + AC4 trap-avoidance proof (no partial-day) + the first-morning vintage-shift artifact pair. CC 1.0.0_SA_CTO + 3.0.0_SA_CVO. CTO+COO joint sign-off on the vintage-shift.

---

*Dispatched by 2.0.0_SA_COO 20260612T214200Z — Andrew-direct full-drive*
*CTO ruling 1a1d555f2 (the (e) trap named); DS recovery follow-up (e); QUEUED post-recovery*
