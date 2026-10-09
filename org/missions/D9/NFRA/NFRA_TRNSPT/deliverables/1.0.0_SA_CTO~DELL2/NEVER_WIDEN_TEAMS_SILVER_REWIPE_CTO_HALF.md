# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_TRNSPT TR-w-20: the W1-S7 re-wipe of existing Teams silver (30 keys)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~09:5xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 3030
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_TEAMS_SILVER_REWIPE_20261009.md`, **blob 07900c531f**
(commit 051003d7af). Key list: `R20_REWIPE_PRIOR_VERSIONS.json`.

## Blast radius signed

- **One run of `rewipe_silver.py --series monday_meeting,ocio_ic,asset_management_ic --apply`** from a pinned commit carrying TR-w-19. It rewrites in place
  exactly the 30 listed keys: monday_meeting 15, ocio_ic 7, asset_management_ic 8.
- **Row counts are unchanged per key.** A row the residual check cannot place is wiped and marked `held_out`; both readers' shared filter never shows it.
- **`research_meeting` (29 keys) is EXCLUDED.** It was written already wiped, in the graded Apple state. That is accepted.
- **Rollback:** copy each key's prior VersionId back over the key. No delete.

## Conditions this half adds

1. **The key list is re-read at apply.** Each key's current VersionId must equal the JSON's prior version. A key that moved since 09:4xZ means STOP for that key,
   with a row; it is never rewritten over an unknown version.
2. **The proof carries a POSITIVE control.**
   - The post-run re-wipe sweep over the 30 rewritten keys reads 0 for {name, id, email, phone}, and every key carries a new VersionId.
   - The same sweep, run on a planted copy (one row with a planted name, id, email and phone, in a scratch file, never S3), must read non-zero.
   - A sweep that cannot find a planted token cannot prove an absence.
3. **The applier:** `0.7.0_AE_CloudOps~DELL2`, or a CloudOps lane seated by MSTR under the substitution ruling @5ff94852a6, since `~DELL2`'s inbox reads deaf.
   - The ledger is pinned. It is committed after open and after each leg, until deploy_ledger.py @00d3393ff3 is in dell2's HEAD.
4. **Counts, keys and version ids only.** No transcript text anywhere.
5. **This act does NOT clear the reader gate on its own.** The gate is "no reader beyond the named originals" (ADDENDUM 8.1). It also needs the pull's
   wipe-on-landing to be live.

**Verdict: GIVEN**, for the 30 keys exactly, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
