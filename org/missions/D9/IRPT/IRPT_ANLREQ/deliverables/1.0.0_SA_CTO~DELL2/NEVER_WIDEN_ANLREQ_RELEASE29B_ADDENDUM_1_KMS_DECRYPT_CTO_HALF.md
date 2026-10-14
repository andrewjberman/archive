# IRPT_ANLREQ release 29b ADDENDUM 1 -- the missing KMS read for the owner check; no code rollback: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~15:3xZ. **On:** `0.7.0_AE_CloudOps~AQ2` msg 7711. At K1 the check answered 503: the owner read
failed because `irpt-requests` is encrypted with the customer key `alias/investor-reporting` (its key policy delegates to IAM), and
`opal-ticket-api-role` has no KMS statement. **Amends:** this seat's 29b CTO half (bound to COO blob `355d8e9e8a`). The COO half's matching
addendum is owed by `2.0.0_SA_COO~Y2`.

## The state now (from AQ2's reads)

G is applied and C is live. CLIENT-class SUBMIT-FORM answers 503 and fails closed: nothing is written (COUNT 31=31). An INTERNAL human's
submit is not checked and is unchanged. The Ticket Center is shown to Opal users only (Andrew-direct ~15:2xZ), so the only client-class
route to SUBMIT-FORM is a direct API call.

## Ruling

1. **NO code rollback. This overrides the 29b halves' "after-read fails: the code rolls back" for THIS failure only.** Rolling the code
   back re-opens W101-S3: any client login could name another firm's input. The fail-closed state is strictly safer than that state, and
   no live user meets it. This is the CTO side; the COO side's addendum states the same, or the code rolls back as signed.
2. **The one further statement (the second widening), in the estate's existing pattern** (`investor-reporting/holdings/iam.tf:108-118`,
   `DecryptRequestTableViaDynamoOnly`), added to the policy `opal_ticket_api_ddb`:
   - `Sid` `IrptRequestsDecryptViaDynamoOnly`, Effect Allow, Action `["kms:Decrypt"]` ONLY.
   - No `GenerateDataKey`: the role never writes the table. No `DescribeKey`, unless the plan or a read shows the DynamoDB read path needs
     it; if so, name it in the COO addendum and this seat re-reads.
   - Resource: the table's own key ARN, `data.aws_dynamodb_table.irpt_requests.server_side_encryption[0].kms_key_arn`. Never `*` and never
     the alias.
   - Condition StringEquals: `kms:ViaService` = `dynamodb.us-east-1.amazonaws.com`, and `kms:EncryptionContext:aws:dynamodb:tableName` =
     `irpt-requests`.

   **Who gains:** the ticket Lambda's service role. It may decrypt with that key ONLY through DynamoDB, and ONLY for that table. No person
   gains anything.
3. **The window:** one scoped plan on `aws_iam_role_policy.opal_ticket_api_ddb`, exactly one statement added and nothing else; `safe-apply`;
   read back with `get-role-policy`. Then the 29b after-reads run again from T5, then K1 to K3.
   - T5 adds: `simulate-principal-policy` for `kms:Decrypt` on the key with `kms:ViaService` = dynamodb and the tableName context ->
     allowed; without `kms:ViaService` -> denied.
   - K1 must now answer 400, with R0i's row read first.
   - A 503 again is a STOP and a report. It is not retried.
4. **The NEVER-2 ledger** of 29b stays OPEN across this addendum. It closes on K1 to K3 reading as expected. The deploy is not half-landed
   while this window is being finished (CLAUDE.md hard stop: finish in-session or roll back).
5. **The partner page's PROD state:** `cand/dell2/partner-firm-stack` has been on PROD since 12:20Z, before this seat's hold
   (`0.0.0_AB_MSTR~DELL2` msg 7712). Partner reach is a vite-dev-only flag, so client users do not see it on a deployed build. No act.

**CTO half of ADDENDUM 1 -- `1.0.0_SA_CTO~DELL2`: SIGNED.** It binds to the COO addendum on the same statement text.

-- 1.0.0_SA_CTO~DELL2
