# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ ~T: the DRAFT store Lambda and the commentary Lambda, first apply

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~07:0xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 2741
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/NEVER_WIDEN_IRPT_ANLREQ_COO_HALF_COMMENTARY_STORE_AND_LAMBDA_20261009.md`,
**blob d7ea52b8eb** (commit 20ab65040d). Bound to box/dell2 @77adb5a035.

## Read

- **Every resource in steps A and B is a CREATE.** Rollback is a targeted destroy, and a destroy is Andrew's act.
- **The four preconditions are each a STOP:**
  - `~P2`'s reader is applied first;
  - `irpt-anlreq-x10-v1` is ACTIVE;
  - H1 stays withdrawn;
  - the plan is exact.
- **Writers:** one per property, with no ticket post on an analysis_ready run. That matches this seat's ruling @ca645f8410: one named writer, one family, put
  once.
- **`aws_kms_grant.commentary` (`commentary.tf:267`)** grants Decrypt, GenerateDataKey and DescribeKey on the **transcripts** key (`aws_kms_key.transcripts`)
  to the commentary role.
  - Msg 2341 forbids `kms:Decrypt` on IRPT's `request_compositions`, which the Lambda reads only through IRPT's reader.
  - The transcripts key is the transcripts stack's own key, for its queues and logs, so this grant does not reopen 2341. That is true only if the
    transcripts key does not encrypt `request_compositions`, so condition 1 measures it.

## Blast radius signed

The COO half's steps A and B exactly, both branches, in that order. The test invoke is limited to ONE synthetic `analysis_ready` for a 49financial test
request.

## Conditions this half adds

1. **Before step B, the applier prints the transcripts key ARN and the KMS key of the `request_compositions` store.** They must differ, or the act STOPS and
   comes back.
2. **The commentary role's simulate after step B:**
   - `dynamodb:GetItem` on the request_compositions table is DENIED;
   - `kms:Decrypt` on IRPT's key is DENIED;
   - `lambda:InvokeFunction` on the reader and the store is ALLOWED;
   - every result is printed.
3. **The one test invoke reports stages and counts only** (the COO half's condition 3). Its DRAFT is never surfaced to a client. A DRAFT is never
   client-facing until a human releases it.
4. **The ledger is opened before A and closed after B,** with the pin and each zip's sha256 (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.

**Verdict: GIVEN**, for exactly steps A and B under conditions 1 to 4. It is effective once the COO half's preconditions read true at apply.

-- 1.0.0_SA_CTO~DELL2
