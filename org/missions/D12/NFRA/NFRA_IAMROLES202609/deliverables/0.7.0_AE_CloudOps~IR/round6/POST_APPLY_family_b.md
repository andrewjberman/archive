# POST_APPLY -- Family B (row 9, SmartX), NFRA_IAMROLES202609.TO-IAM-w-1 PHASE B

**Cell:** IAM-w-1 (round 6, outcome FWD-4; round-5 analysis item E1)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority for PHASE B:** GO from `2.0.0_SA_COO~ZI` (msg 32975, re-affirmed msg 33017), both never-widen halves
SIGNED as files -- COO @`f2c325cac8`, CTO @`f5444083a8`; `-target` scope per amendment A2-r6 @`3293b97a90`.
**Measured:** 2026-10-10, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r6-w1b` @`a528bf9175`,
Terraform v1.15.8 (resolved on PATH; site Z has no `.tools/terraform.exe`), provider `hashicorp/aws v5.100.0`,
backend state key `smartx-pipeline/tfstate`.

---

## 1. THE REQUIRED LINE

```
POST-APPLY-PLAN: infra/aws/terraform/smartx-pipeline: 0 to add, 0 to change, 0 to destroy
```

That is the TARGETED re-plan, which is what AC2 asks for. Terraform renders a clean plan as a sentence rather
than a count, so its verbatim output is quoted here beside the canonical line and nothing is paraphrased:

```
$ terraform -chdir=infra/aws/terraform/smartx-pipeline plan -input=false -no-color -lock=false \
    -target=aws_iam_role.opal_smartx_lambda_role
No changes. Your infrastructure matches the configuration.
```

## 2. THE UNTARGETED MODULE PLAN, RECORDED BESIDE IT

The cell requires the untargeted plan here so the pre-existing drift stays visible rather than disappearing
behind a scoped pass:

```
UNTARGETED-MODULE-PLAN: infra/aws/terraform/smartx-pipeline: 0 to add, 3 to change, 0 to destroy
  # aws_lambda_function.assets_daily_pull will be updated in-place
  # aws_lambda_function.jwt_refresher     will be updated in-place
  # aws_lambda_function.rest_pull         will be updated in-place
Changes to Outputs:
  - autostart_lambda_arn = "arn:aws:lambda:us-east-1:313476888478:function:smartx-ec2-autostart" -> null
  - autostart_role_arn   = "arn:aws:iam::313476888478:role/smartx-ec2-autostart-20251222183942113900000002" -> null
  - eventbridge_rule_arn = "arn:aws:events:us-east-1:313476888478:rule/smartx-daily-export-trigger" -> null
```

**This is the SAME three-change plan PHASE A's negative control measured before this act** (`0 to add, 3 to
change, 0 to destroy`), and it is unchanged by PHASE B. That is the point: the adoption's own delta was the
`1 to import` plus the one `tags_all` change, and the three Lambda code drifts plus the three output removals
belong to the module, not to this cell. They stay with `smartx-pipeline`'s owner on row `Z-S20`'s route
(`Z-S21` disarmed by the issuer in `Z-S24`, the `-target` scope being the disarm).

## 3. THE PLAN THAT WAS APPLIED, GRADED BEFORE THE APPLY

The plan was SAVED (`-out`) and the apply ran that file, so the applied plan IS the graded plan. Graded from
`terraform show -json` by decomposing every `resource_change`, not by reading the summary line -- a summary
of `1 import / 0 add / 1 change / 0 destroy` would read identically if the one change had been a trust-policy
rewrite:

| graded property | measured | the pair's condition | verdict |
|---|---|---|---|
| `resource_changes` total | 1 | only the role | MET |
| non-no-op changes | 1 -- `aws_iam_role.opal_smartx_lambda_role`, `actions=['update']`, `importing id=opal-smartx-lambda-role` | the role, imported | MET |
| attributes that differ | **1** -- `tags_all` only | `tags_all` is the only change | MET |
| `tags_all` delta | `{}` -> `Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=SmartXPipeline` | exactly those four keys, no fifth | MET |
| `assume_role_policy`, `inline_policy`, `managed_policy_arns` | absent from the delta (unchanged) | untouched | MET |
| destroys | 0 | 0 | MET |
| any `aws_lambda_function` address | **0 present in the plan at all** | none of the three Z-S21 drifts listed | MET |
| other `.open_deploys/` entry on this module | 0 (`deploy_ledger.py list`: 30 entries, 0 matching `smartx\|iamroles`) | none | MET |

Summary line, verbatim: `Plan: 1 to import, 0 to add, 1 to change, 0 to destroy.`
Apply result, verbatim: `Apply complete! Resources: 1 imported, 0 added, 1 changed, 0 destroyed.`

`safe-apply`'s own gates on the way through: `comp-tagauthz` PASSED (and, as in PHASE A, over **0 candidate
resources** -- an IAM role is not a tag-authorization-bearing resource in its scope, so that pass is recorded
with its denominator and is not what answers the KEY COLLISION); `tombstone-gate` CLEAN over 0 creates against
7 tombstones.

## 4. BRANCH A, READ FROM THE WORLD RATHER THAN FROM THE APPLY

The pair names two branches. This is Branch A, and every value below is a live AWS read taken after the apply,
not the apply's self-report:

| read | result |
|---|---|
| `aws iam list-role-tags --role-name opal-smartx-lambda-role` | exactly four: `Environment=Production`, `ManagedBy=Terraform`, `Project=OpalPortal`, `System=SmartXPipeline` |
| `aws iam list-role-policies` | `["opal-smartx-logs","opal-smartx-s3-access","opal-smartx-secrets"]` -- all **3 still attached, 0 detachments** |
| `aws iam list-attached-role-policies` | `{"AttachedPolicies": []}` -- unchanged |
| `aws iam get-role` path / description / max_session / trust / permissions boundary | `/` ; `Lambda role for SmartX query functions` ; `3600` ; `lambda.amazonaws.com` + `sts:AssumeRole` ; `None` -- **all unchanged from the PHASE A survey** |

**THE OMISSION RULE HELD IN THE WORLD, not only in a plan.** PHASE A could only show the plan enumerating the
three inline policies as unchanged. This is the live read after the import: the three policies are still on the
role. Had `inline_policy` been set, this read is where the detachment would have shown.

**No permission moved.** The role's policy set, its trust and its usage are byte-identical to the pre-act reads.
Four tags were added to a role that carried none, and the survey named all four before the pair was signed.
`Project` and `System` are the KEY COLLISION keys, and the two sweeps that answer it (PHASE A's identity sweep,
0 `aws:PrincipalTag` conditions over 298 roles / 78 policies / 9 users / 2 groups; the CTO half's resource-policy
plane) both stand unchanged by this act.

## 5. ROLLBACK, AVAILABLE AND UNUSED

The pair's rollback is `terraform state rm aws_iam_role.opal_smartx_lambda_role` (state only, no AWS change) plus
`aws iam untag-role --tag-keys Environment ManagedBy Project System` and reverting the rename. It was not needed
and was not run. Nothing is stranded.

## 6. THE LEDGER

`iamroles-r6-family-b` opened BEFORE the apply (@`a528bf9175`, three legs: TF, TAGS, REPLAN) and closed after
this record, per NEVER-2. One module, one entry.

**PHASE B ends here, per the order's step 6.**
