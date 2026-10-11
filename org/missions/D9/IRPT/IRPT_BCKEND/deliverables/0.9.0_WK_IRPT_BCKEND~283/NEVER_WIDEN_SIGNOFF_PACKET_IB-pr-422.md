# Never-widen sign-off packet -- IB-pr-422: the adapter role gains two single-secret vendor session reads

Prepared by 0.9.0_WK_IRPT_BCKEND~283 for 2.0.0_SA_COO~P2 and 1.0.0_SA_CTO, on TO IRPT_BCKEND.TO-IB-pr-422 (AMENDMENT 1), ordered by 1.0.0_SA_CTO~DELL2 msg 4488 and msg 4509. **Nothing was applied.** Terraform PLAN ONLY, plus AWS reads through the `.tools/aws` shim (`iam list-role-policies`). No secret value was read (`get-secret-value` was never run), no vendor was called, no Lambda code or environment changed. No client data is in this packet.

## READ THIS FIRST

1. **This is an IAM WIDENING of ONE role by TWO single-secret reads.** The role `irpt-performance-adapter-role` today holds 7 inline policies and none reads a secret. After the apply it holds 9: the same 7 plus two, each granting `secretsmanager:GetSecretValue` on exactly one secret ARN (no wildcard, no other action).
2. **It is one release with IB-pr-421.** IB-pr-421's zip (packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~282/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-421.md`, built `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=`) calls the vendor with stored credentials; without these two policies it would write a use row and then fail the credential read (row `IRPT_BCKEND-D2-W282-S1`). Apply the policies first, then the zip, in one sitting.
3. **The plan variable is not set.** The two policies are ungated by removing their `count`, not by setting `var.approved_performance_plan`. The variable declaration, the plan environment variables and every other use of `performance_plan_firm` are untouched. No `count` remains on the four blocks for another reason.

## The change (Terraform commit `d435105a39`, `infra/aws/terraform/investor-reporting/performance/retained.tf`)

The four session blocks keep their addresses and lose their `count`: `data.aws_secretsmanager_secret.performance_cot_session`, `aws_iam_role_policy.performance_approved_session`, `data.aws_secretsmanager_secret.performance_inf_session`, `aws_iam_role_policy.performance_approved_inf_session`. No `lambda.tf` edit (CTO msg 4509).

## The two grants (read from the targeted plan JSON, not typed)

| policy address | policy name | action | the ONE secret ARN |
|---|---|---|---|
| `aws_iam_role_policy.performance_approved_session` | `irpt-performance-approved-session-policy` | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/cot/session-jnzOyC` (Black Diamond, Cottonwood session) |
| `aws_iam_role_policy.performance_approved_inf_session` | `irpt-performance-approved-orion-session-policy` | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:orion/jwt/current-ewrBtp` (Orion token) |

Both attach to `irpt-performance-adapter-role`. Census: `IB120-1_plan_census.json`.

## The plans

| plan | command | adds | changes | destroys |
|---|---|---|---|---|
| TARGETED (the one to apply first) | `terraform plan -input=false -lock=false -no-color -target=aws_iam_role_policy.performance_approved_session -target=aws_iam_role_policy.performance_approved_inf_session` | 2 (the two policies above) | 0 | 0 |
| UNTARGETED (full root, after the edit) | same without `-target` | 2 (the same two) | 1 (`module.irpt_performance_adapter.aws_lambda_function.this`) | 0 |
| UNEDITED tree (baseline) | same without `-target`, before the edit | 0 | 0 | 0 ("No changes") |

Text: `IB120-1_plan_targeted.txt`, `IB120-1_plan_after_edit.txt`, `IB120-1_plan_baseline_unedited.txt`.

**Cause of the untargeted change:** `lambda.tf:62-65` makes the adapter module `depends_on` `aws_iam_role_policy.performance_approved_session`. While that policy is a pending add, Terraform defers the module's artifact data read, so the function prints as an update. It is a plan-time artifact, not a code change. Once the policy exists, the full-root plan shows the function change only when the zip hash differs (see Branch A step 2).

## Naming limb

`python .tools/naming-apply-gate.py --plan-json <targeted plan, terraform show -json> --root infra/aws/terraform/investor-reporting/performance`: rc 0, `NAMING-PLAN: PASS 3 graded`; both new policy names CONFORMANT as IAM_POLICY. The same limb on the untargeted plan JSON also ran rc 0 (earlier, @d435105a39 session).

## Branch A -- two steps, one sitting, one ledger entry (`org/critical_paths/change_management/`, opened at start, closed at completion)

1. **Targeted plan and apply at the two addresses.** `terraform plan` with both `-target` flags must read exactly 2 adds, 0 changes, 0 destroys; then apply that plan. After-read: `aws iam get-role-policy` for each policy shows the one secret ARN above and `GetSecretValue` only; `list-role-policies` shows 9 names (the 7 below plus the two).
2. **Full-root plan with a KNOWN hash, then apply.** The zip hash is set to IB-pr-421's built `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=`. The plan must read exactly 1 change: the function `irpt-performance-adapter`, and nothing else. Apply. After-read: the function's CodeSha256 equals `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=`.

With step 1 landed and the OLD zip still live, the new grant is **unused**: the old code refuses at its plan check (no installed one-use plan) before any secret read. So step 1 alone widens the role's permission but not what the function does.

## Branch B -- rollback

- Step 2 rolls back to the prior digest `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` (S3 version `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn`, re-read at apply), per IB-pr-421's Branch B.
- If step 1 landed and step 2 cannot land, the two policies are removed by a **targeted destroy** of the two addresses, **pre-authorised by the CTO for that case only** (msg 4509). The same result is reached by reverting commit `d435105a39` and applying; the role returns to exactly the 7 policies listed below.
- Role policy list read before (`aws iam list-role-policies --role-name irpt-performance-adapter-role`, re-read at plan time, identical to the earlier read): `irpt-performance-adapter-directory-read-policy`, `irpt-performance-adapter-logs`, `irpt-performance-adapter-ownership-map-read-policy`, `irpt-performance-adapter-selection-read-policy`, `irpt-performance-adapter-service-profile-read-policy`, `irpt-performance-render-grant-read-policy`, `irpt-performance-retained-policy`.

## Blast radius

The role `irpt-performance-adapter-role` only: two new inline policies. No other role, resource, function, environment variable, route or table changes. Rollback per policy: delete the policy (targeted destroy), no data to restore.

## What is NOT exercised

No `terraform apply`, no `terraform destroy`. No secret was read and no vendor was called; the two secrets were resolved only by name to ARN (data source, plan time). The full-root plan with the known zip hash (Branch A step 2) has NOT been run: it needs the policies to exist first, so its "exactly 1 change" is a stated expectation, measured only in its untargeted form. IAM propagation after the apply and the post-apply `get-role-policy` reads are not exercised. The live function was not touched.
