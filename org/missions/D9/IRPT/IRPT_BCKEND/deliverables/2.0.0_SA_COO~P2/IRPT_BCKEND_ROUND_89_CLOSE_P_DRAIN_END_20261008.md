# L8 drain end -- IRPT_BCKEND round 89 close, workstream ~P (adds to the rounds 88-90 packet @ab01735253)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~23:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | `round-close-check --round 89`: verdict=MAY-CLOSE (1 of 1 orders complete, proof_ok 1).

## Round 89 -- IB-pr-377: the r61 directory release (COMPLETE, applier 0.7.0_AE_CloudOps~DELL2, proof @dc3ff4c2c9)

- **Live after the apply:** refresh `RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=` and search `IV7P2AL43cGo9VfyY2ku0zEFAhQWq9BPxge754UynM8=`.
  Each equals its build. The whole-root re-plan has 0 diff, census 0 on both, not rolled back. The ledger is CLOSED 6 of 6, with the
  sentinel removed.
- **Graded by the issuer** at box/dell2 HEAD dc3ff4c2c9: IB89-1-AC1 PASS, IB89-1-AC2 PASS.
- **Arm (a), under AMENDMENT 2 (@b474f59a1b, CTO msg 1949; the issuer amended it and no gate limb graded the modification):**
  - 49financial READY: 19 added, 4719 entries.
  - inflection and cottonwood: REFRESH_FAILED + SAFE, prior directory served.
  - Cottonwood is read at its manifest's own as_of, 2026-10-07.
  - Arm (c) is discharged by AC2's offline five-arm drive.
- Detail: `deliverables/0.7.0_AE_CloudOps~DELL2/IB89-1_r61_release_after_reads.json`. Rows D2-S11, D2-S12, D2-S13.

## Round 91 issued -- IB-pr-379 (@b3a7b44fd4, worker 0.9.0_WK_IRPT_BCKEND~187)

- The CTO's first cell: why the inflection and cottonwood builds drop entries the previous build carried (row D2-S13). The cell
  diagnoses, fixes and packages the refresh release before those directories go OVER_AGE (`expiry.py`: more than 2 trading days).
- SOURCE_REMOVAL stops at the diagnosis with a row to the CTO.

## Round 90 -- IB-pr-378: still OPEN with the applier (it is proceeding).

**Push state:** LOCAL on box/dell2 (MSTR pushes :18/:48).
