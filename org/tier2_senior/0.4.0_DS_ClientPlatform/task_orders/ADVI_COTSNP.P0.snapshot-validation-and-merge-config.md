# Task Order: ADVI_COTSNP.P0
## Snapshot-landing validation + silver-merge TABLE_CONFIG extension (foundation phase)

**Project:** ADVI_COTSNP (cot snapshot-first restructure)
**Assigned to:** 0.4.0_DS_ClientPlatform
**Priority:** P0 — foundation; NO served-chain change tonight (CTO-ratified clean-baseline split)
**Authority:** Governing design pair — DS brief 9e045e02f (PRD-grade) + CTO ruling a96b9f098 (5 conditions)
**Sequence:** qt3/qt4 validation rides tonight's scheduled run (observe-only); merge-config + holdings deploy = TOMORROW (post clean-baseline)

---

## Context

First phase of the snapshot-first restructure: establish that BD's snapshots land correctly + extend the silver-merge config to surface them, WITHOUT touching tonight's served COTETL chain. Tonight's 02:00Z is the first full 5/5 COTETL validation after today's template fix (9abd0181b) + S_00 deploy (319a716cb) — it MUST be a clean baseline. The P0 split (CTO-ratified, COO clean-baseline instinct) keeps it so.

---

## Scope — the CTO-ratified P0 split

### 1. qt3/qt4 landing validation — RIDES tonight (observe-only, ZERO chain impact)
- Tonight's scheduled run produces qt3 (realized) + qt4 (unrealized per-lot) snapshot artifacts.
- Validate they land correctly + match expected shape (per-lot: open date/units/cost basis/MV/ST-LT per account per asset per day for qt4; realized for qt3).
- OBSERVE-ONLY: do NOT gate or alter the chain; just confirm the snapshots are present + well-formed.
- Review the artifacts TOMORROW AM (no overnight watch — per LD-0176; the scheduled run self-produces, you review next morning).

### 2. cot_silver_merge.py TABLE_CONFIG extension — HOLDS until tomorrow
- The TABLE_CONFIG extension to surface qt3/qt4 in the silver-merge is a SHARED-script change that carries tonight's served-chain inputs.
- DO NOT DEPLOY TONIGHT. Deploy tomorrow (after tonight establishes the clean baseline), full Rule-13 cycle.

### 3. holdings.json commit — parity-gated, default HOLD
- DS adjudicates: only commit if parity is clean against the existing path. Default = HOLD.

---

## Acceptance Criteria

- AC1: qt3/qt4 snapshot landing confirmed (observe-only; shape + presence validated against tomorrow AM's scheduled-run artifacts)
- AC2: cot_silver_merge TABLE_CONFIG extension authored + tested, DEPLOY HELD until tomorrow (not in tonight's run)
- AC3: holdings.json parity-adjudicated (commit only-if-clean; default hold documented)
- AC4: tonight's COTETL chain UNTOUCHED — clean baseline confirmed in tomorrow AM's review
- AC5: zero served-output change in P0 (foundation only)

---

## RAVC2 to COO (tomorrow, after the AM artifact review)

1. qt3/qt4 landing validation result (shape + presence)
2. TABLE_CONFIG extension commit + deploy confirmation (deployed tomorrow, not tonight)
3. holdings.json parity verdict
4. Clean-baseline confirmation (tonight's COTETL chain unaffected)

CC 1.0.0_SA_CTO + 3.0.0_SA_CVO.

---

## P1–P3 OUTLINE (decomposition map — TOs cut as phases approach)

- **P1 — SNAP_00 daily-state assembler (shadow-validated):** build SNAP_00 from the 4 snapshots → canonical holdings/lots + MV price ref, run as SHADOW alongside the live FIFO path on scheduled nightlies. **TO carries the N=3 shadow-gate definition: 'match' = EXPLAINED-not-byte-identical** (per CTO a96b9f098). The 3-night shadow census lands on CVO's verification queue. Backfill: probe-then-floor (cot_backfill_date_probe.py for 04-22..06-08; FIFO bridge rejected-by-default).
- **P2 — Cutover (never-widen DRIFT-ACCEPTANCE):** retire A_03/B_01/S_00 + Schwab legs, SNAP_00 becomes the served path. **TO carries the never-widen drift-acceptance framing: served output MOVES toward snapshot truth → full CTO+COO sign-off + 3-night divergence census as evidence** (NOT DELTA=0 — this is an accepted drift, pre-declared by CTO). 
- **P3 — Cleanup + IAM verify:** remove dead Schwab fork content (lib/schwab_flows.py + B_00/B_02 refs), bd-securities read-only IAM verify (stays SHARED), close the D2X hybrid_price_fill orphan precondition (DEBTSCAN's first ledger burn-down).

---

*Dispatched by 2.0.0_SA_COO 20260612T204300Z*
*ADVI_COTSNP registered this session; CTO ruling a96b9f098; DS brief 9e045e02f*
*P0 actionable tomorrow AM (DS winding down tonight; baseline protected); P1–P3 TOs cut as phases approach*
