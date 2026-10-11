# POST_APPLY -- Family E (row 11) and row 3, NFRA_IAMROLES202609.TO-IAM-w-3 PHASE B

**Cell:** IAM-w-3 (round 6, outcome FWD-4; round-5 analysis item E3)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority for PHASE B:** GO from `2.0.0_SA_COO~ZI` (msg 33102). Both never-widen halves SIGNED as files:
COO @`9586e0106b`, CTO @`8453026444`. Both halves' "w-2 PHASE B lands first" line was **RELEASED IN PLACE**
by A7-r6 @`7c213215bd` (row Z-S36) and struck in the CTO half by `1.0.0_SA_CTO~Z` on msg 33103 -- the two
acts write different modules with separate state keys and zero pre-existing drift, so the sequencing was
the COO's plan order and never a condition of the blast radius. `-target` scope per A2-r6; order of acts
per A4-r6 @`7af7a24e9f` and A5-r6 @`f37fb5892d`.
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r6-w3-b` @`1df69456eb`,
Terraform v1.15.8, provider `hashicorp/aws v5.100.0`.

---

## 1. THE REQUIRED LINES -- ONE PER MODULE

```
POST-APPLY-PLAN: infra/aws/terraform/portfolio-management: 0 to add, 0 to change, 0 to destroy
POST-APPLY-PLAN: infra/aws/terraform/news-pipeline: 0 to add, 0 to change, 0 to destroy
```

AC2 expects exactly 2 and these are they. Both are the TARGETED re-plan. Terraform renders a clean plan as
a sentence rather than a count, so its verbatim output is quoted here beside the canonical lines and
nothing is paraphrased silently:

```
$ terraform -chdir=infra/aws/terraform/portfolio-management plan ... -target=aws_iam_role.portfolio_management_lambda_role
No changes. Your infrastructure matches the configuration.

$ terraform -chdir=infra/aws/terraform/news-pipeline plan ... -target=aws_iam_role.codebuild_semantic_clustering_role
No changes. Your infrastructure matches the configuration.
```

## 2. THE UNTARGETED MODULE PLANS, RECORDED BESIDE THEM

```
UNTARGETED-MODULE-PLAN: infra/aws/terraform/portfolio-management: No changes. Your infrastructure matches the configuration.
UNTARGETED-MODULE-PLAN: infra/aws/terraform/news-pipeline: No changes. Your infrastructure matches the configuration.
```

**Both modules are fully absorbed, with nothing left over.** This is a cleaner result than Family B's,
where the untargeted plan still reads `0 to add, 3 to change, 0 to destroy` from three PRE-EXISTING Lambda
drifts that belong to `smartx-pipeline`'s owner. Here PHASE A's negative controls read "No changes" before
the act and the untargeted plans read "No changes" after it, so the adoption's whole delta -- one import
and one `tags_all` change per module -- is accounted for and the modules carry no residue.

## 3. THE PLANS THAT WERE APPLIED, GRADED BEFORE EITHER APPLY

Both plans were SAVED (`-out`) and each apply ran its own saved file, so the applied plan IS the graded
plan. Graded from `terraform show -json` by decomposing every `resource_change` -- the summary
`1 to import, 0 to add, 1 to change, 0 to destroy` would read identically if the one change had been a
trust-policy rewrite, which is precisely what the pair names as a stop condition for row 3.

| graded property | `portfolio-management` | `news-pipeline` |
|---|---|---|
| `resource_changes` total | 1 | 1 |
| non-no-op | 1 | 1 |
| the address | `aws_iam_role.portfolio_management_lambda_role` | `aws_iam_role.codebuild_semantic_clustering_role` |
| actions / import id | `['update']` / `portfolio-management-lambda-role` | `['update']` / `codebuild-semantic-clustering-role` |
| attributes that differ | **1** (`tags_all`) | **1** (`tags_all`) |
| the `tags_all` delta | `{}` -> `Environment=Production, ManagedBy=Terraform, Project=OpalPortal` | `{}` -> the same three **plus `System=NewsPipeline`** |
| key count, checked against the pair | **3**, and `System` absent | **4** |
| `assume_role_policy` | unchanged | **unchanged** |
| `inline_policy` | unchanged | unchanged |
| `managed_policy_arns` | **unchanged** | unchanged |
| `description` | unchanged | unchanged (stays absent) |
| destroys | 0 | 0 |
| non-no-op addresses that are NOT the adopted role | **`[]`** | **`[]`** |

**THE TAG COUNTS WERE CHECKED AGAINST THE PAIR'S PER-MODULE NUMBERS, NOT AGAINST EACH OTHER.** The grader
compared each module's `tags_all` to an expected dict written from that module's provider block: 3 keys for
`portfolio-management`, which declares no `System` key at all, and 4 for `news-pipeline`. Both matched
exactly, and `System` was confirmed ABSENT from module 1's delta. Families A and B both wrote four keys, so
four is the number a reader arrives with, and a fourth key in module 1 would have been NOT SIGNED.

Summary lines, verbatim: `Plan: 1 to import, 0 to add, 1 to change, 0 to destroy.` for each.
Apply results, verbatim: `Apply complete! Resources: 1 imported, 0 added, 1 changed, 0 destroyed.` for each.

`safe-apply`'s own gates, per module: `comp-tagauthz` PASSED (and, as in every cell of this round, the GATE
pass is over **0 candidate resources** -- an IAM role is not tag-authorization-bearing in its scope, so that
pass is recorded with its denominator and is NOT what answers the KEY COLLISION; both halves say the same);
`tombstone-gate` CLEAN over 0 creates against 7 tombstones.

## 4. BRANCH A, READ FROM THE WORLD -- INCLUDING BOTH STOP CONDITIONS

Every value below is a live AWS read taken after the applies, not the applies' self-report.

### Module 1 -- `portfolio-management-lambda-role`

| read | result |
|---|---|
| `list-role-tags` | **exactly 3**: `Environment=Production`, `ManagedBy=Terraform`, `Project=OpalPortal`. `System` present: **False** |
| **STOP CONDITION -- `list-attached-role-policies`** | **1 -- `AWSLambdaBasicExecutionRole`**, exactly as before the apply |
| `list-role-policies` | `['portfolio-s3-dynamodb']` -- unchanged |
| `get-role` path / description / max session / trust / boundary | `/` ; `Scoped Lambda role - created 2026-02-19 IAM audit` ; `3600` ; `lambda.amazonaws.com` ; `None` -- all unchanged |

**THIS IS WHERE THE OMISSION RULE FINALLY PROTECTED A MANAGED ATTACHMENT, AND IT IS PROVEN LIVE.** Row 11
is the only role in the adoption program carrying an attached AWS-managed policy. In Families B and A the
rule protected inline policies; omitting `managed_policy_arns` there left nothing at risk that was actually
attached. Here, setting it -- **even to `[]`, which reads like "no opinion"** -- would have made it
authoritative and detached `AWSLambdaBasicExecutionRole`, the grant that gives this Lambda role its
CloudWatch Logs access. The plan predicted no change and this read confirms it in the world: 1 attachment
before, the same 1 after.

### Module 2 -- `codebuild-semantic-clustering-role`

| read | result |
|---|---|
| `list-role-tags` | **exactly 4**: the three above **plus `System=NewsPipeline`** |
| **STOP CONDITION -- `get-role` trust principal** | **`{"Service": "codebuild.amazonaws.com"}`** -- unchanged |
| `get-role` description | **`None`** -- still absent, as the declaration intends |
| `list-role-policies` | `['CodeBuildSemanticClusteringPolicy']` -- unchanged |
| `list-attached-role-policies` | **0** -- unchanged |

**This stop condition was never theoretical.** Row 3 is the one role adopted this round that is in active
use (`RoleLastUsed` 2026-09-11), and it trusts CodeBuild rather than Lambda. A copied sibling trust would
have silently changed WHO MAY ASSUME a role that something actually runs on -- an authorization move wearing
a custody move's clothes -- and the plan summary would still have read as one import. The principal was
read from the live role at PHASE A, carried into the declaration, confirmed `before == after` in the graded
plan, and is confirmed again here from AWS.

**No permission moved in either module.** Both roles' policy sets, trusts, descriptions, paths, max session
durations and permissions boundaries are identical to the pre-act reads. Three tags were added to one role
and four to the other, and the survey named every one of them before either half was signed.

## 5. ROLLBACK, AVAILABLE AND UNUSED

Per module, as the COO half states: `terraform state rm <address>` (state only, no AWS change) plus
`aws iam untag-role --tag-keys ...` (three keys for module 1, four for module 2) and reverting the rename.
Neither was needed and neither was run. Nothing is stranded.

## 6. THE LEDGERS -- TWO, ONE PER MODULE

`iamroles-r6-family-e-portfolio-management` and `iamroles-r6-family-e-news-pipeline`, both opened BEFORE
their applies (3 legs each: TF, then the module's own stop condition as MANAGED / TRUST, then REPLAN) and
closed after this record, per NEVER-2.

> **A note on AC3, because its `closed=` limb cannot prove what it looks like it proves.** AC3 expects
> `open=0` and `closed=` 2 or greater. But `deploy_ledger.py open` writes the completion-record file into
> `change_management/` AT OPEN TIME, so the `closed=` count read **2 the moment both entries opened** and
> before anything was applied. The criterion is therefore sound only as a CONJUNCTION, and here it is the
> **`open=0`** limb that carries it. w-1's AC3 had the opposite shape: `open=0` alone read the same before
> the entry existed and after it closed, and `closed=1` carried it. Recorded so a reader does not take
> `closed=2` as evidence of closure.

**PHASE B ends here, per the order's step 6.**
