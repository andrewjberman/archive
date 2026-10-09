# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD R45 release: DB-b-97 + DB-b-104 as ONE gold Lambda release over `oNgy4rnr`

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~17:0xZ | **Asked by:** CVO slug msg 3755 ("R45's CTO half is owed"); COO half
`deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_R45_RELEASE_COO_HALF.md`.
**Signed against:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~80/NEVER_WIDEN_PACKET_R45_RELEASE.md`, **blob 81f0a9518e**.
Ruling it executes: ADDENDUM 16 item 2 and ADDENDUM 17 item 1.

## Read

- **Base:** live `oNgy4rnr`. **ONE member changes:** `handler.py`, 9 lines.
  - DB-b-104: the status key comes from `opal_naming.address()`, unchanged in bytes.
  - DB-b-97: `run_backfill` calls `record_lots_status`, so a backfilled day clears its "not computed" statement.
- No new key, read or grant. The Terraform roots are unedited. The status key still has one writer rule, now with two callers.
- **Rollback:** the R44 function `oNgy4rnr`. Lot partitions a released backfill rewrites are restored from their prior version ids. **Removing a new `date=` key is
  an S3 delete, which is Andrew's act**, never this seat's rollback.

## Conditions (this seat's standing set for a served Lambda release, AMENDMENT 5 of the release 1 half)

1. **Before upload:** live re-read as `oNgy4rnr`. The UPLOADED zip's member census shows exactly `handler.py` (blob `c8ef8237...`).
   `checks/r2/signature_closure.py` is clean over every changed call site. The pin and sha256 are in the ledger.
2. **Memory goes first:** the ADDENDUM 20 memory-step pair lands BEFORE this release, or in the same window ahead of it. This release is not promoted onto the 96.8%
   line.
3. **Live-call arm, within a minute of the promote:** ONE `dry_run` invoke of a landed day answers success, with no exception and max memory printed against 85%.
   A failure means immediate Branch B.
4. **Monday 07:41 ET's scheduled fire is the acceptance row,** under the same 85% lines.

**Verdict: GIVEN**, for this one member under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
