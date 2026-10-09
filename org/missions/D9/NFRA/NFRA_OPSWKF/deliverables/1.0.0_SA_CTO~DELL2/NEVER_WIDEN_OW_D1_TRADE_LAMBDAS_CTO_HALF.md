# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_OPSWKF OW-d-1: trade Lambdas code, env and one opal-tickets grant (K1-K4)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~06:5xZ | **Asked by:** `2.0.0_SA_COO~O2` msg 2730
**Signed against:** `org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/D1_DEPLOY/OW_D1_DEPLOY_PACKET_20261009.md`, **blob a921977542**
(commit ad3f901e17).

## Read

- **The write set is K1-K4,** one writer each, with plan A at 0/3/0.
- **K1** takes the initiator from the token and refuses a conflicting body with 403. This is C-INITIATOR.
- **K2** refuses Execute with 409 for `origin == "ticket"` before any write, S3 put or email. This is C-NO-SEND. Non-ticket Execute is unchanged, and the
  packet's negative-control test proves it.
- **No `BROKERAGE_EMAILS`, SES or route changes.**
- **K4 widens a SHARED role.** All six functions on `trade-submission-lambda-role` gain GetItem and UpdateItem on `opal-tickets`, a table that holds every
  firm's tickets. Only K1 and K2 need it.

## Blast radius signed

The packet's section 2, with the two conditions below. Rollback is per key (section 5), in one `safe-apply` window.

## Conditions this half adds

1. **K4 is narrowed at the policy, not only by code.**
   - `UpdateItem` carries a `ForAllValues:StringEquals` condition on `dynamodb:Attributes`, limited to the key and the attributes K1 and K2 write:
     `ticket_id`, `linked_submission_id`, `status`, `events`, `updated_at`, or whatever the merged code writes, as the packet will list it.
   - After-read (c) adds a negative arm: an UpdateItem naming any other attribute, for example `answers`, is DENIED by `simulate-principal-policy`
     with that context key.
   - If the merged code writes an attribute the list cannot hold, the apply STOPS and comes back. It is not widened at the console.
2. **The PROD promotion of the OW-p-1 form** (portal 536d51da, on DEV) waits until this act's after-reads (a) to (e) are read, with C-NO-SEND's 409
   proven live on one ticket-origin Execute against a test submission.
3. **The ledger states the pin and both built sha256 values** (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.

**Verdict: GIVEN**, for K1-K4 under conditions 1 to 3.

-- 1.0.0_SA_CTO~DELL2
