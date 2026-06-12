# Task Order: ADVI_COTSNP.P0 — Clean-baseline split (protect tonight's COTETL 02:00Z baseline)

**Project:** ADVI_COTSNP (P0 decomposition; Andrew-direct cot snapshot-first restructure)
**Assigned to:** 0.4.0_DS_ClientPlatform
**Governing design (no re-authored PRD per CTO efficiency ruling):** DS brief 9e045e02f (PRD-grade) + CTO ruling a96b9f098 (5 conditions)
**Priority:** P0 — TONIGHT-relevant (governs the 02:00Z COTETL baseline); the rest of COTSNP (P1-P3) is queued behind it
**Sequencing:** DS picks up post-R5 (live P0 recovery first); but the P0 DISPOSITIONS below govern TONIGHT's run regardless of when DS reads this — they are HOLDS + observe-only, nothing to actively deploy tonight.

---

## Why P0 exists (COO clean-baseline instinct, CTO-ratified)

The cot snapshot-first restructure (retire txn-reverse-engineering, build SNAP_00 from BD snapshots) is a multi-phase change touching served cot output. Before any of that, P0 PROTECTS tonight's clean COTETL baseline so the restructure builds on a known-good reference — and so no shared-script change contaminates tonight's served chain.

## P0 dispositions (all HOLD / observe-only — zero active deploy tonight)

1. **`cot_silver_merge.py` TABLE_CONFIG deploy HOLDS until tomorrow.** The script is SHARED and carries tonight's served-chain inputs — deploying the restructure's TABLE_CONFIG change tonight would alter the served chain mid-baseline. HOLD. (Default state = no deploy; this just makes the hold explicit + gated.)
2. **qt3/qt4 landing validation RIDES tonight — OBSERVE-ONLY.** Validate the qt3 (realized) / qt4 (unrealized) snapshot landings as they arrive on tonight's run, ZERO chain impact (read/verify only, no write, no deploy). This is data-readiness observation for P1's SNAP_00 inputs, not a chain mutation.
3. **`holdings.json` commit PARITY-GATED — DS adjudicates, DEFAULT HOLD.** If a holdings.json change is staged, it does NOT auto-commit tonight; DS adjudicates parity vs the served baseline and DEFAULTS TO HOLD absent a clear never-widen-clean case.

**Net: tonight's 02:00Z COTETL run stays a CLEAN baseline** — no restructure code in the served chain, qt3/qt4 observed for P1 readiness, holdings held.

## ACs
- AC1: cot_silver_merge TABLE_CONFIG restructure change confirmed NOT deployed to the tonight-served chain (held for tomorrow).
- AC2: qt3/qt4 landing observed + readiness noted for P1 SNAP_00 inputs (observe-only, 0 chain impact verified).
- AC3: holdings.json default-held unless DS adjudicates a never-widen-clean parity case (documented either way).

## Carries forward (P1-P3 — authored separately, near-execution)
- **P1** = SNAP_00 daily-state assembler from BD snapshots (qt1 holdings + qt4 unrealized + qt3 realized + qt5 allocations); carries the **N=3 shadow gate** ('match' = EXPLAINED-not-byte-identical per CTO condition).
- **P2** = txns -> flows-only (NNA); **pre-declared never-widen DRIFT-ACCEPTANCE** (served output moves toward snapshot truth -> full CTO+COO sign-off + 3-night divergence census). Authored near-execution (drift framing needs current served state).
- **P3** = D2X hybrid_price_fill orphan close (DEBTSCAN first ledger burn-down); bd-securities stays SHARED read-only (IAM verify); backfill = probe-then-floor (FIFO bridge rejected-by-default).

## RAVC2 to COO
P0: the 3 dispositions confirmed (silver_merge held, qt3/qt4 observed + readiness, holdings adjudicated). CC CTO + CVO (CVO verification queue starts at P1's 3-night shadow census).

---

*Authored by 2.0.0_SA_COO 20260612T2248Z — /drive cycle; the registry's named "NEXT: COO P0-P3 decomposition" first leg. P0 = tonight-relevant baseline protection; P1-P3 near-execution. DS executes post-R5 but the HOLDS govern tonight regardless.*
