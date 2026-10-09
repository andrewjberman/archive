# NFRA_OPSWKF OW-d-1 -- deploy packet and COO half (never-widen), 2026-10-09

**Issuer:** `2.0.0_SA_COO~O2` (dell2). **Applier:** `0.7.0_AE_CloudOps~DELL2`. **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**Cells served:** OW-e-1, OW-e-2, OW-e-3, OW-i-1 (all drained to box/dell2; e-chain @a633fdd355, e-3 @019c0d133c, i-1 @50117407d3).
**PRD:** v0.3, C-NO-SEND, C-INITIATOR, C-SHARED-SURFACE.

## 1. The act (write set = a literal key list)

| # | Key | Change | Writers of this property (counted) |
|---|---|---|---|
| K1 | Lambda `trade-submission-handler`, code | initiator from the authorizer token (403 on no context or a conflicting body); optional `ticket_id` bridge (a conditional bind on the ticket, then the put, reverting on a put failure) | 1: `infra/aws/terraform/trade-pipeline` via the versioned artifact `trade-pipeline/trade-submission-handler.zip` |
| K2 | Lambda `trade-workflow-handler`, code | ticket write-back on approve/reject (best effort); Execute refused 409 for `origin == "ticket"` BEFORE any write, S3 put or `send_brokerage_email` | 1: same stack, `trade-pipeline/trade-workflow-handler.zip` |
| K3 | the env of K1 and K2 | add `TICKETS_TABLE = "opal-tickets"` | 1: `lambdas.tf` |
| K4 | inline policy `trade-submission-policy` on `trade-submission-lambda-role` | add statement `TicketBridgeOpalTickets`: `dynamodb:GetItem` and `dynamodb:UpdateItem` on `table/opal-tickets` only | 1: `iam.tf` |

**NOT in this act:** the ticket Lambda `opal-ticket-api`. Its artifact is shared with TCKT_VNEXT and IRPT_ANLREQ, so OW-l-1's
`trade_request` entry rides that owner's next ticket deploy (asked of `2.0.0_SA_COO~V2`). OW-r-1 waits on both deploys.

## 2. Blast radius

- **K1, live path today.** The TradeSubmission page calls `POST /api/general/trades/submit`. Its route is
  `authorization_type = "CUSTOM"` with `portal_jwt` (`infra/aws/terraform/shared-infra/apigateway-portal/routes.tf:343-350`). The
  unauthenticated `/api/public/trades/*` family is REMOVED (`routes.tf:361`). So every current caller carries an authorizer
  context, and a page body's `initiator_email` equals the signed-in user's. Effect on today's callers: none, except a request
  whose body names someone other than the signer, which is now refused 403 (the intended C-INITIATOR fix).
- **K1, ticket path.** It is reachable only by a body carrying `ticket_id`. No client sends one until the OW-p-1 form lands on
  DEV. Its writes are one conditional `UpdateItem` on one ticket of type `trade_request` that the same signer created.
- **K2.** Approve/reject on a submission WITHOUT `ticket_id` makes no ticket call: every submission existing today has none.
  The Execute fence fires only on `origin == "ticket"`, which no existing submission carries. Non-ticket Execute is byte-for-byte
  unchanged, and the negative-control test proves the email path still fires there.
- **K3.** It adds one env key and removes or changes none.
- **K4.** The role is SHARED by six functions (submission, auth, dashboard, workflow, identifier, parquet; `iam.tf:14`), so all
  six gain GetItem/UpdateItem on `opal-tickets`. There is no delete, put, scan or index ARN. Accepted: two actions on one table,
  and only K1 and K2 call it.
- **C-NO-SEND.** No `BROKERAGE_EMAILS` value changes (every list is andrew@ + menachem@ today, `config.py:24-29`). No SES
  identity, template or permission changes.

## 3. Expected plan (both branches)

- **Branch A, proceed:** `0 to add, 3 to change, 0 to destroy`:
  - `aws_iam_role_policy.trade_submission_policy` (one statement added);
  - `aws_lambda_function.trade_submission_handler` (s3_object_version/source_code_hash + one env key);
  - `aws_lambda_function.trade_workflow_handler` (the same).
- **Branch B, STOP and report:** anything else, including any change on the other nine functions, the recon role, a bucket,
  a table or a route, or a destroy.

## 4. After-reads (the applier, each printed)

- **(a)** Both functions' `CodeSha256` equal the uploaded zips, and each zip's handler file hashes to the merged box/dell2 file.
- **(b)** Env: the prior keys are unchanged, plus `TICKETS_TABLE`.
- **(c)** `simulate-principal-policy` for the role: GetItem/UpdateItem on `table/opal-tickets` allowed; DeleteItem/PutItem/Scan
  on it denied (negative control).
- **(d)** An unauthenticated `POST /api/general/trades/submit` through CloudFront is refused 401/403 (the authorizer, unchanged).
- **(e)** The replan is 0-diff.

## 5. Rollback (per key)

- **K1/K2:** re-point each function to its PRIOR artifact `s3_object_version`, read and recorded at BEFORE.
- **K3:** it rides the same revert of `lambdas.tf`.
- **K4:** remove the statement and apply.

All of it is one `safe-apply` of the stack at the parent commit of the four merges, in the same window.

## 6. COO half

`2.0.0_SA_COO~O2` signs the blast radius above for keys K1-K4, for both plan branches, with the rollback per key. The ledger entry
is the applier's, opened at step 0 and closed at completion.
