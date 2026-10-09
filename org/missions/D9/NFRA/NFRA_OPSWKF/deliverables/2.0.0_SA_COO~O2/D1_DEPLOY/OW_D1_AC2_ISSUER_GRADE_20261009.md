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

**Verdict: OW-d1-AC2 MET**, with R1 disclosed. OW-d-1 status: SERVED (the trade Lambdas are live with C-INITIATOR, the bridge, the
write-back and the C-NO-SEND fence). The live 409 for a ticket-origin Execute is OW-r-1's, after the ticket release R13.
