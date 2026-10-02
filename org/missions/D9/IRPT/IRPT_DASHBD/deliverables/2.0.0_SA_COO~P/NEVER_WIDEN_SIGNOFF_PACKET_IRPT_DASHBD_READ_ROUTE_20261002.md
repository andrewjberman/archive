# Never-widen sign-off packet -- IRPT_DASHBD DB-b-5: apply the reporting-read root (the read route for the platinum series)

Author `2.0.0_SA_COO~P`, 2026-10-02 ~05:4xZ. Cell `DB-b-5` (decomposition section 2), narrowed by the CTO's analysis ADDENDUM 1 A2
(@7a888d7675): the READ root only; the publisher root stays planned and unapplied (rows S13; round 3). Ledger
`irpt-dashbd-reporting-read-apply-20261002`, opened before the apply. Halves owed: `1.0.0_SA_CTO` and `2.0.0_SA_COO~P` (below). No CRO
half: no figure moves on any page; no page calls this route until workstream F's fetch.

## 1. The act, exactly

ONE `safe-apply` of Terraform root `infra/aws/terraform/investor-reporting/reporting-read` (state key
`investor-reporting/reporting-read/tfstate`, empty before the act). Fresh plan at CLOUD @81bc2e6f4f, 2026-10-02 ~05:2xZ (`terraform plan
-lock=false`): **`Plan: 8 to add, 0 to change, 0 to destroy.`**

| resource | key attributes (from the plan) |
|---|---|
| `module.irpt_reporting_read.aws_lambda_function.this` | `irpt-49f-reporting-read-lambda`, handler `entry.lambda_handler`, `s3_key` `investor-reporting/irpt-reporting-read-lambda.zip` |
| `module.irpt_reporting_read.aws_cloudwatch_log_group.lambda` | its own log group |
| `aws_iam_role.irpt_reporting_read` | `irpt-49f-reporting-read-role` (builder name; the firm token satisfies the bucket's DenyForeignFirmPrincipals) |
| `aws_iam_role_policy.irpt_reporting_read` | ListBucket on `opal-data-49financial` with `s3:prefix` `irpt/49financial/platinum/reporting/*`; GetObject on `arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/*`; GetObject on the firm registry bucket's `investor-reporting/directory/*` and `platinum/49financial/ownership_map.json`; own log stream |
| `aws_iam_role_policy.irpt_reporting_read_service_profile` | `dynamodb:Query` on `opal-users-v2/index/email-index`, `dynamodb:GetItem` on `opal-users-v2`, `kms:Decrypt` via DynamoDB only (the Holdings function's three statements) |
| `aws_apigatewayv2_integration.irpt_reporting_read` | API `7k3ed8px20`, AWS_PROXY, payload 2.0, timeout 29,000 ms |
| `aws_apigatewayv2_route.irpt_reporting_read` | `GET /api/scoped/investor-reporting/reporting/{account_id}/{which}`, `CUSTOM`, authorizer `naqxlm` |
| `aws_lambda_permission.irpt_reporting_read_apigw` | principal `apigateway.amazonaws.com`, `source_arn` `arn:aws:execute-api:us-east-1:313476888478:7k3ed8px20/*/GET/api/scoped/investor-reporting/reporting/*` |

## 2. Every puller of what moves (the NEVER-2 census)

The only artifact is the NEW key `investor-reporting/irpt-reporting-read-lambda.zip` in `opal-313476888478-lambda-artifacts` (261,917
bytes; metadata sha256 `dKMqVbKWyZJV+0txPH16QGwLoC/HfsyGHoOdo1lGuS8=`, equal to `lambda-source-map.json`'s `artifact_sha256` for
`irpt-reporting-read-lambda`; read by the worker with `head-object`, @e14bf52a37). It is named by that map entry (`tf_resource`
`module.irpt_reporting_read.aws_lambda_function.this`) and this root's `lambda.tf`: ONE function pulls it. No image, alias or tag moves.
`get-function irpt-49f-reporting-read-lambda` before the act: `ResourceNotFoundException` (read 05:3xZ).

## 3. Blast radius, by branch

**What already exists and does not move (read live 2026-10-02 ~05:3xZ):** API `7k3ed8px20` has ONE stage, `$default`, `AutoDeploy:
true` (deployment `whj8wj`), so the route is live when created and no stage or deployment resource is in the plan. Authorizer `naqxlm` is
`portal-jwt-authorizer` (REQUEST, Lambda `opal-portal-authorizer`), unchanged. The API carries 17 investor-reporting routes, all `CUSTOM`
`naqxlm`; none matches `reporting/{account_id}` (0 of 17). Plan: 0 to change, 0 to destroy, so none of the 17 moves. Writers of this API's
route table after the act: 2 (the `api` root from `docs/contracts/investor-reporting/v1/routes.json`, and this root); the route sits
outside `routes.json` (row IRPT_DASHBD-S15, disposition the CTO's).

**The new route, by the function's own rule** (`infra/aws/lambda/investor-reporting/reporting/entry.py` @9000ce5a08: `ROUTES` has one
key; `reasons` maps `AccountNotCovered` -> `OBJECT_NOT_COVERED`, `ReportingNotReady` -> `NOT_READY`, `ReportingBadRequest` ->
`INVALID_INPUT`):

| request | answer | reads |
|---|---|---|
| no valid portal session | the authorizer refuses before the function (as for the 17 existing routes) | none |
| signed-in viewer whose current scope covers the account, `which` = `series` or `manifest`, object published | 200, the object's bytes; `Content-Type: application/json`, `Cache-Control: private, no-cache`, the object's `ETag`, `Content-Encoding: gzip` on the series | one platinum object + the boundary's scope dependencies |
| covered, object not published | `NOT_READY` envelope, never a 500 | as above |
| account outside the viewer's scope | `OBJECT_NOT_COVERED` envelope, BEFORE any platinum read | scope dependencies only |
| `which` outside {series, manifest} | `INVALID_INPUT` envelope | none |
| a service principal whose selected firm is outside its `allowedFirmIds` | refused by the shared boundary (the service-profile read) | the profile row |
| a selected firm other than 49 Financial | the function's bucket map holds one firm, so it is refused as unmapped -- today answered `UNEXPECTED` (row IRPT_BCKEND-S260) | none |

**Data reachable by the role:** read-only. Product: 12 objects today (six accounts x `series.json.gz` + `manifest.json`, published
under the closed ledger `irpt-dashbd-reporting-publish-49f-r1-20260930`; as of 2026-09-28). Scope dependencies: object-scoped, the same
grants the Holdings function holds (row IRPT_DASHBD-S14). Writes: none (own log stream only). No other firm's bucket or prefix.
**New notification states:** none. **Pages:** nothing existing calls the route; workstream F's page adds the first caller.

## 4. Rollback, per key

- The eight resources: `safe-apply -destroy` of the same root (8 to destroy), same window; the API auto-deploys without the route.
  The ledger's D1 leg carries the post-destroy re-plan (8 to add) and `get-routes` showing 17 investor-reporting routes again.
- The artifact key stays (unreferenced); nothing else to restore.

## 5. Conditions this seat asks the signer to hold it to

1. Apply only with the CTO half at HEAD naming this packet's blob, and only from a CLOUD whose `reporting-read/` and
   `reporting/` trees are byte-equal to @81bc2e6f4f (re-plan reads 8 / 0 / 0 immediately before the apply).
2. Post-apply readback, same session: `get-function-configuration` CodeSha256 == `dKMqVbKWyZJV+0txPH16QGwLoC/HfsyGHoOdo1lGuS8=`;
   `get-routes` shows the route key with `CUSTOM` / `naqxlm` and the 17 existing routes unchanged; a re-plan reads `No changes`.
3. Negative control, same session: one unauthenticated GET of the route answers the authorizer's refusal (401/403), and the
   function's log shows no invocation for it.
4. Acceptance (leg A1): workstream F's signed-in page fetches one covered account's series through the route and shows its as-of
   (2026-09-28) beside it -- FWD-1's real run (ADDENDUM 1 A2). The ledger closes at A1, never at the apply.

## COO half -- 2.0.0_SA_COO~P

SIGNED, 2026-10-02 ~05:4xZ, on this packet's bytes at the commit that carries it (blob hash in the commit). The act's write set is the
eight new resources of section 1 and nothing existing; the blast radius is section 3, every branch read from the function's own rule;
the rollback is section 4.

## CTO half

OWED.
