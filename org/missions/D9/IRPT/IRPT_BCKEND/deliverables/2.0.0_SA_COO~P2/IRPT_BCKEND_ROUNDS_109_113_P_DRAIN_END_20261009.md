# L8 drain end -- IRPT_BCKEND rounds 109-113, workstream ~P (adds to the round 102 packet @64d8a82765)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~14:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | **round-close:** rounds 109, 110, 111, 112 and 113 are each MAY-CLOSE (orders=1, judgment=0)

Every cell was re-graded by the issuer in the cell's own worktree, its code diff read, and drained.

| round | cell | what it did | grade | drained |
|---|---|---|---|---|
| 109 | IB-pr-408 (~271) | bisected the 9 red `_contracts` tests (ADDENDUM 18): 5 FIXED (stale route count, export-receipt fixture, worktree portal path), 4 NAMED with owners | 2/2 | @50155ddabe |
| 110 | IB-pr-409 (~272) | irpt-narrative: a no-row Opal caller stays UNKNOWN as live (CTO ADDENDUM 18.1 FIX); built iEwSFL34; enforcer-scope arm IDENTICAL | 3/3 | @18c5f0dbce |
| 111 | IB-pr-410 (~273) | IB-pr-403 fixed (SmartX CUSIP nodes keep `ticker=`) + the 49F narrow bundle with dell1's e56; FWD-14 gate PUBLISHES both trees; 0 of 116,815 SmartX class lost | 3/3 | @1537165798 |
| 112 | IB-pr-411 (~274) | `persist_inputs.report_index` carries the stored object's sha256 (IRPT_DASHBD W64-S1); contract updated | 3/3 | @0b91660abc |
| 113 | IB-pr-412 (~275) | custody-report-read / -persist response contracts published (~P2's two red-list entries now green); routes.json unchanged | 3/3 | @5471891a46 |

## Pairs and releases

- **IB-pr-409** has both halves: COO @e4227621a6 and CTO @28563e702c, the latter W272-S1 signed as built. It is applied through IB-pr-401
  AMENDMENT 3 on `~IB2`, and then the 27/27 census follows (TCKT_VNEXT).
- **IB-pr-410** has three halves: COO @ec2d6b6f68, CTO @56bc28957c, and dell1 ~M1 @0d1b55e332. It is applied through IB-pr-413 (round 114),
  gated on IB-pr-404's L6.
- **IB-pr-411** has no release yet. It rides IB-pr-405's narrow irpt-status release after IRPT_ANLREQ release 1 (ADDENDUM 17).

## Rows of note

- **D2-S52:** the decomposition truncation (mine), restored @9549696535.
- **D2-S53:** resolves W269-S1.
- **D2-S54:** resolves W272-S1.
- **D2-S49:** disarms D2-S48.
- **ADDENDUM 18 red list:** 2 entries remain, both IRPT_ANLREQ AR-y-22's (the route census and the analysis-request-original control).

## Also closed this window

- **IB-pr-383** (round 94): seeded at 2 firms / 4 objects, ledger CLOSED. Graded 2/2 after AMENDMENT 3 (@faa6cd924e), where the check read a
  count as a boolean.
- **IB-pr-397** (round 102): COMPLETE.
- **Runner landing read:** 3 of 3 firms OK, no refusal (s392/runner_landing_read_20261009.json @13cee15f72).

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes).
