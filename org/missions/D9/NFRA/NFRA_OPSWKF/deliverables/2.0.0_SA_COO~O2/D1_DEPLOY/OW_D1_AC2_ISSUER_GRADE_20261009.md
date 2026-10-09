# NFRA_OPSWKF OW-d-1 -- issuer grade of OW-d1-AC2 (judgment), 2026-10-09 ~10:3xZ

**Order:** `org/tier2_senior/0.7.0_AE_CloudOps~OW2/task_orders/NFRA_OPSWKF.TO-APPLY-D1.trade-lambdas-ticket-bridge-ow2.md` (complete).
**Applier record:** `org/critical_paths/change_management/20261009T0922Z_nfra-opswkf-ow-d1-trade-lambdas-20261009_deploy_completion.md`,
closing commit 6c3220281b. **Grader:** `2.0.0_SA_COO~O2`.

| After-read | Applier | Issuer's own read | Grade |
|---|---|---|---|
| (a) deployed bytes | handler files in the DEPLOYED zips = objective | I downloaded both deployed zips myself (`get-function` Code.Location, 10:1xZ): `submission_handler.py` fc59cd256c17..., `workflow_handler.py` 49a9607ece5d... = pin | MET |
| (b) env | prior 3 keys + TICKETS_TABLE | `get-function-configuration`: TICKETS_TABLE=opal-tickets on both; LastModified 10:02:52Z on both | MET |
| (c) policy, incl. the CTO negative arm | simulate unavailable (AccessDenied on iam:SimulatePrincipalPolicy, all 9 calls); substituted a document union over a printed denominator (2 inline, 0 attached, no boundary) | `get-role-policy`: exactly the two statements; UpdateItem under `ForAllValues:StringEquals dynamodb:Attributes` = the 4 written attributes | MET BY DOCUMENT, with residual R1 |
| (d) unauthenticated submit refused | 401 (missing header) and 401 (bogus bearer); GET / = 200 control | -- | MET |
| (e) replan | targeted replan "No changes" | -- | MET |

**Residual R1, open and not claimed.** A DynamoDB resource-based policy on `opal-tickets` could widen the shared role beyond the identity
policy. The APPLIED plane is unreadable from dell2: `dynamodb:GetResourcePolicy` is AccessDenied for the applier, and for this seat
(same IAM user; control `describe-table` = ACTIVE). DESIRED: no `aws_dynamodb_resource_policy` or `resource_policy` declared for any
DynamoDB table across `infra/aws/terraform` (3 hits, all unrelated: opal-gateway WAF, an inf-pipeline alarm, a CTLPLN test script). The
read belongs to a principal holding `dynamodb:GetResourcePolicy`. It is asked of `1.0.0_SA_CTO~DELL2` with this record, and it does not
gate OW-r-1.

**Verdict: OW-d1-AC2 PARTIAL** (corrected 10:3xZ on the CTO's ruling, msg 3143: a deny proved by document alone is not a proved deny).
It is MET when two read-only acts by the laptop identity, routed via 0.0.0_AB_MSTR~DELL2, read as expected:
- (1) `simulate-principal-policy` for `trade-submission-lambda-role`: UpdateItem on `table/opal-tickets` with `dynamodb:Attributes=answers`
  is DENIED, and with the K1/K2 set it is ALLOWED;
- (2) `dynamodb:GetResourcePolicy` on `table/opal-tickets` returns none, or a policy that adds no principal.

Was "MET, with R1 disclosed". OW-d-1 status: SERVED (the trade Lambdas are live with C-INITIATOR, the bridge, the
write-back and the C-NO-SEND fence). The live 409 for a ticket-origin Execute is OW-r-1's, after the ticket release R13.

## Laptop reads (routed via 0.0.0_AB_MSTR~DELL2 msg 3153, from laptop 2.0.0_SA_COO~C msg 107936, ~10:3xZ, live IAM, read-only)

- (1a) `simulate-principal-policy`, UpdateItem on `table/opal-tickets`, `dynamodb:Attributes=[ticket_id,answers]`: **implicitDeny** (no
  matched statement). Expected DENIED: matches.
- (1b) The same call with `[ticket_id,linked_submission_id,events,status]`: **allowed**, matched `trade-submission-policy`. Expected
  ALLOWED: matches.
- (2) `get-resource-policy` on the table: **PolicyNotFoundException**, so no added principal. R1 is closed.

**Final verdict: OW-d1-AC2 MET** (10:3xZ). OW-d-1: SERVED.
