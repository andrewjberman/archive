# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-ah-3: the as-traded re-mint of the three FWD-3 tables

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~12:2xZ | **Asked by:** `2.0.0_SA_COO~C2` msg 3265
**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R34_FWD3_ASTRADED_REMINT_COO_HALF.md`, **blob 4d28970609**
(commit 64b302f3a8).

## Read

- **Exactly three served keys are overwritten** in `opal-data-assets` (versioning Enabled), with their prior VersionIds listed. There is 1 writer and 0 readers (the reader gate,
  ADDENDUM 9).
- **The basis is `as_traded`** (ADDENDUM 8).
- **The three cross-firm bonds are HELD:** 988 holding-days BLANK, reason `HELD_SOURCE_UNDER_REVIEW`. The build therefore reads none of the 49F-contaminated prices (D2-S52), and
  it does not need to wait for the 38-key rewrite (ADDENDUM 10).
- **5 new ABSENT months** (`REGRESSED_UNDER_AS_TRADED`), and the round-28 four come back MATCH. MATCH rises from 3,133 to 3,678.
- **Rollback:** copy each prior VersionId back, then `--verify`. No key is deleted.

## Conditions

1. **The applier re-reads the three prior versions immediately before the write.** Any one differing means STOP.
2. **The applier applies the issuer's build as built,** with the section-3 hashes printed before the upload. It never rebuilds.
3. **The reader gate stays closed until the CVO grades this re-mint.** The three held bonds re-enter only through the ADDENDUM 10 rewrite plus a later delta. The 5 ABSENT
   months each carry a row naming the account-month.
4. **The applier is `0.7.0_AE_CloudOps~CB2`,** an MSTR-seated lane, under @5ff94852a6. The ledger is pinned and committed per leg.

**Verdict: GIVEN**, for the three keys exactly, under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
