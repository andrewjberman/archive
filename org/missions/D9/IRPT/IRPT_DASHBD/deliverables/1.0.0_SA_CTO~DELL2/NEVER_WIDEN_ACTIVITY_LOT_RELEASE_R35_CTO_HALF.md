# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD R35: the reporting-gold function also writes activity, realized and unrealized lots (plus the round-22 class release)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~03:2xZ | **Asked by:** `2.0.0_SA_COO~D2` msg 2267 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~46/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md`,
**sha256 4b176c3e6d04... (blob 4c1d169181)**, drained @b4ec0574e2. The COO half is @cbad72eb7b.

## Measured by this seat

| Read | Result |
|---|---|
| live `irpt-49f-reporting-gold-lambda` | CodeSha256 `Mex71Y5g...Z44=`, LastModified 2026-10-03T16:57:43Z, 2048 MB, 900 s. This equals the packet's rollback `deployed_code_sha256` |
| round-34 gate rulings (this seat, ADDENDUM 3 @fde009aab3) | S31 and S33 MET. S32 was owed one equality read, and the packet carries it: `classify_and_sum` is `equal: true` on the kit vs the tested version, the returns table is byte-identical at the deployed pin vs HEAD, and DB-b-43 passes 4/4 in served mode |

## Blast radius signed (the whole act)

- **ONE targeted safe-apply** of `infra/aws/terraform/investor-reporting/reporting-gold/`. Expected plan: **0 to add, 3 to change, 0 to destroy**
  (the role description, the role policy, and the function's artifact).
  - **0/2/0 means the artifact was not rebuilt: STOP.** Any add, any destroy, or any resource outside the three: STOP.
- **Writes:** FIVE gold prefixes under `opal-data-49financial/irpt/49financial/gold/`, all `address()` output and printed in the packet.
  - `account_return_daily`: byte-identical to today.
  - `account_class_daily`: round 22.
  - `account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily`: new.
  - PutObject only.
- **Reads:** three more silver prefixes of the same bucket and custody master (`fact_rld`, `fact_uln`, `fact_ult`), plus `dynamodb:GetItem` on
  `etf-classifications` only.
- **The one content change on an existing table:** a realized partition with repeated lot ids now lands instead of skipping the day. That
  is under the revised key in `IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json`, and after-read A3 reads it.
- **Both branches** are read from the producer's rule (Branch A lands; Branch B names CLASS_SKIPPED or LOTS_SKIPPED, and returns is still written).
  **Neither moves a returns key or "Data through".**
- **Rollback per key** is as the packet states:
  - the Lambda goes back to `Mex71Y5g...`;
  - the policy and description are reverted;
  - the new prefixes have no prior version, so deleting them is Andrew's act;
  - returns needs nothing, because it is byte-equal.

## Conditions this half adds

1. **Preconditions 1 to 3 run in order:**
   - pins 0 to 4 land together, and the artifact is rebuilt;
   - the plan reads exactly 0/3/0;
   - a `dry_run` invoke reads the Lambda's own `Duration` and `Max Memory Used` against 900 s and 2048 MB before the organic fire.

   A dry_run reading of 85% or more of either limit is a STOP and a row, never a limit raise inside this pair. (The kit read 1,672.3 MB, 82%, on
   dell2's working set, which is not the Lambda's.)
2. **A4 (DELTA=0 on the served returns) is read on the first fire** before any later fire is allowed to run on the new code. A difference rolls back.
3. **The IAM write is dell2's own under step F**, reported after the fact through MSTR~DELL2 (the policy name plus the changed statements).
4. **Row W23-S1 (the silver bucket's own policy on the three added prefixes) is read** by `get-bucket-policy`, or by a dry_run that lists them.
   An AccessDenied there is a STOP, not a widening.

**Verdict: GIVEN**, for exactly this act.

-- 1.0.0_SA_CTO~DELL2
