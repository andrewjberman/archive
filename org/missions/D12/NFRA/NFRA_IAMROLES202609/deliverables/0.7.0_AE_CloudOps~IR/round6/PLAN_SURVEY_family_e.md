# PLAN_SURVEY -- Family E (row 11) and row 3, NFRA_IAMROLES202609.TO-IAM-w-3 PHASE A

**Cell:** IAM-w-3 (round 6, outcome FWD-4; round-5 analysis item E3)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority:** `ROUND_ANALYSIS.round5.md` @f77e32d7c3 E3; `ADOPTION_PLAN_TEN.md` @59112aafed Family E;
row 3's home per the round-5 analysis home table. **GO:** `2.0.0_SA_COO~ZI` msg 33054 (dependency met --
w-2 PHASE A drained @`68af906ee9`).
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** WORLD -- **PHASE A APPLIED NOTHING.**

**Measured:** 2026-10-10, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r6-w3` @`49baac8712`,
Terraform v1.15.8 (resolved on PATH; site Z has no `.tools/terraform.exe`), provider
`hashicorp/aws v5.100.0`. Every plan invocation `-input=false -lock=false`, read-only, saved with
`-out` and graded from `show -json`.

---

## 1. THE FOUR REQUIRED LINES, PER MODULE

```
PLAN: infra/aws/terraform/portfolio-management: Plan: 1 to import, 0 to add, 1 to change, 0 to destroy.
DEFAULT_TAGS: infra/aws/terraform/portfolio-management: ['Environment', 'ManagedBy', 'Project']
AUTH_KEY_COLLISION: infra/aws/terraform/portfolio-management:   *** KEY COLLISION: ['Project'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/portfolio-management: portfolio-management/tfstate

PLAN: infra/aws/terraform/news-pipeline: Plan: 1 to import, 0 to add, 1 to change, 0 to destroy.
DEFAULT_TAGS: infra/aws/terraform/news-pipeline: ['Environment', 'ManagedBy', 'Project', 'System']
AUTH_KEY_COLLISION: infra/aws/terraform/news-pipeline:   *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/news-pipeline: news-pipeline/tfstate
```

Both `STATE_KEY`s read from each module's own `backend "s3"` block in `main.tf`, bucket
`opal-313476888478-terraform-state`, region `us-east-1`. Both `AUTH_KEY_COLLISION` lines are
`.tools/comp-tagauthz`'s output verbatim, including leading spaces, from the invocation `safe-apply`
makes internally -- here reproduced WITH `--from-plan` against each saved plan, which Family A's survey
could not do because `bd-pipeline` does not plan.

## 2. >>> THE TWO MODULES DO NOT WRITE THE SAME TAGS. DO NOT CARRY ONE'S NUMBER TO THE OTHER. <<<

This is the single most important line in this survey for whoever writes the two never-widen halves.

| | `portfolio-management` | `news-pipeline` |
|---|---|---|
| `default_tags` keys | **3** | **4** |
| keys | `Environment`, `ManagedBy`, `Project` | `Environment`, `ManagedBy`, `Project`, `System` |
| `System` | **NOT DECLARED AT ALL** | `System = NewsPipeline` |
| tags the apply writes on its role | **3** | **4** |
| KEY COLLISION surface | `['Project']` only | `['Project', 'System']` |

Families B and A both wrote four tags, so "four default tags" is the number a reader arrives with and it
is **wrong for `portfolio-management`**, which declares no `System` key. The pair for that module must
name three keys, and a targeted plan there showing a fourth is a STOP, not a rounding difference. Read
from each provider block and confirmed against each plan's own `tags_all` delta, not inferred from the
sibling module.

## 3. THE TWO ROLES' LIVE STATE

Read at 2026-10-10 at write time (`get-role`, `list-role-policies`, `list-attached-role-policies`,
`list-role-tags`), and carried into the declarations as-live. **Both roles have ZERO tags.**

| attribute | `portfolio-management-lambda-role` (row 11) | `codebuild-semantic-clustering-role` (row 3) |
|---|---|---|
| tags | **0** (`{"Tags": []}`) | **0** (`{"Tags": []}`) |
| path | `/` | `/` |
| description | `Scoped Lambda role - created 2026-02-19 IAM audit` | **ABSENT** (the API omits the field) |
| max_session_duration | `3600` | `3600` |
| assume_role_policy principal | `lambda.amazonaws.com` | **`codebuild.amazonaws.com`** |
| inline policies | 1 -- `portfolio-s3-dynamodb` | 1 -- `CodeBuildSemanticClusteringPolicy` |
| **attached managed policies** | **1 -- `AWSLambdaBasicExecutionRole`** | 0 (`AttachedPolicies: []`) |
| permissions boundary | none | none |
| created | `2026-02-19T16:00:38Z` | `2026-02-17T17:51:43Z` |
| RoleLastUsed | **ABSENT -- never used** | `2026-09-11T16:36:04Z`, `us-east-1` -- **in active use** |

**ROW 11 IS THE FIRST ROLE IN THE ADOPTION PROGRAM WITH AN ATTACHED MANAGED POLICY, AND THAT IS WHERE
THE OMISSION RULE EARNS ITS KEEP.** Families B and A carried inline policies only, so omitting
`managed_policy_arns` there protected nothing actually attached. Here it protects
`arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole` -- the grant that gives this Lambda
role its CloudWatch Logs access. Setting `managed_policy_arns`, **even to `[]`, which reads like "no
opinion"**, makes it authoritative and the next run DETACHES it. The declaration omits it, and the
plan's own decomposition (section 4) shows it unchanged.

**Row 3 trusts CodeBuild, not Lambda**, which the cell calls out, and **row 3 is the one role in this
round that is actually in use** (last assumed 2026-09-11). That changes nothing about the act -- custody
only -- but it is why the trust clause is not theoretical: a copied Lambda trust would silently change
who may assume a role that something assumes weekly, and the plan SUMMARY would still read as one
import. Row 3 also has **no description**, so the argument is OMITTED rather than set to `""`.

**Row 11 has never been used** (`RoleLastUsed` absent, not merely old). A fact about usage, **not a
deletion warrant**: ABSENT is not EXERCISED-AGAINST. This cell adopts it as it stands.

## 4. WHAT IS MINE AND WHAT IS NOT -- and here, unlike Family B, NOTHING ELSE IS MOVING

**NEGATIVE CONTROL, per module.** With its adoption file MOVED OUT and nothing else changed:

```
portfolio-management, zz_adopt_family_e.tf held out:  No changes. Your infrastructure matches the configuration.
news-pipeline,        zz_adopt_row3.tf held out:      No changes. Your infrastructure matches the configuration.
```

**BOTH MODULES ARE AT ZERO PRE-EXISTING DRIFT.** This is the opposite of Family B, where the control
read `0 to add, 3 to change, 0 to destroy` and three unauthorized Lambda code deploys would have ridden
an unscoped apply (row `Z-S21`). Here the entire plan delta in each module -- 1 import plus 1 `tags_all`
change -- is attributable to this cell, and there is nothing else an apply could carry. **The `-target`
scoping the cell binds (A2-r6) is therefore belt-and-braces in these two modules rather than load-bearing
as it was in `smartx-pipeline`; it still binds, and PHASE B must still use it, because the control proves
the drift is zero TODAY and says nothing about the hour of the apply.**

**GRADED PER ATTRIBUTE, from `show -json` on the saved plans, not from the summary line.** The summary
`1 to import, 0 to add, 1 to change, 0 to destroy` is exactly what a trust-policy rewrite would also
print, so the summary cannot grade the act:

| | `portfolio-management` | `news-pipeline` |
|---|---|---|
| `resource_changes` total | 39 | 141 |
| non-no-op | **1** | **1** |
| the address | `aws_iam_role.portfolio_management_lambda_role` | `aws_iam_role.codebuild_semantic_clustering_role` |
| actions / import id | `['update']`, importing `portfolio-management-lambda-role` | `['update']`, importing `codebuild-semantic-clustering-role` |
| attributes that differ | **1** | **1** |
| the delta | `tags_all: {}` -> `{Environment=Production, ManagedBy=Terraform, Project=OpalPortal}` | `tags_all: {}` -> `{Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=NewsPipeline}` |
| `inline_policy` | unchanged | unchanged |
| `managed_policy_arns` | **unchanged** (the `AWSLambdaBasicExecutionRole` attachment survives) | unchanged |
| `assume_role_policy` | unchanged | **unchanged -- the CodeBuild principal is intact** |
| destroys | 0 | 0 |

Note the denominators: 39 and 141 resource_changes, of which exactly one each is non-no-op. A plan
containing 141 addresses is not a small plan, and reading only its summary line is how an unintended
address rides along unnoticed.

## 5. THE TAG-AUTHORIZATION READ

`comp-tagauthz --from-plan` ran in **MODE: GATE** for both modules (a real plan exists, unlike Family A)
and exited **rc=0**. Both scoped to **0 candidate resources**, with the RESULT line stating it:

```
MODE: GATE. Scoped to 0 candidate resource(s) this tree would manage.
RESULT: none of the 0 candidate(s) carries a tag that <module>'s default_tags [...] would overwrite.
```

**That is a pass over an EMPTY DENOMINATOR and by itself says nothing about either role** -- the gate
scopes to resources whose tags are authorization-bearing, and no IAM role is one. Recording the rc
without the denominator would be the bare zero reading as "no problem exists".

**So the question is answered on the same two independent grounds as Families B and A**, and the
underlying sweep was re-run by this instrument today: `iam get-account-authorization-details` over
**301 roles, 78 local+attached policies, 9 users, 2 groups**; SCPs NOT APPLICABLE, the account is not in
an AWS Organization -- stated, not implied.

1. **Zero `aws:PrincipalTag/*` conditions exist account-wide.** Tagging a role cannot act through a
   principal-tag condition because there are none.
2. The only two non-AWS-service tag conditions are both `aws:ResourceTag` and **neither reaches an IAM
   role** -- each is scoped to EC2 instances and SSM documents: `System = CottonwoodPipeline`
   (`cot-bd-session-trigger-lambda-role`) and `Project = NFRA_WEBSITE` (`website-estate-admin`).
3. **The values do not match either**, independently of resource type: these modules write
   `Project = OpalPortal` and, for `news-pipeline` only, `System = NewsPipeline`.

**Conclusion, on two independent grounds: the tags these two applies would add -- three on row 11, four
on row 3 -- can neither widen nor narrow any authorization decision in this account.** The KEY COLLISION
is a true statement about the key NAMES and a false alarm for these two resources.

> **Carried forward from Family A, unresolved and not re-derived:** `comp-tagauthz` reports
> `tag-conditioned statements found: 9 (4 ours, 5 AWS service-linked)`, where this seat's hand sweep of
> the same API response in PHASE A of w-1 resolved to 4 distinct `(policy, condition-kind, key)` triples.
> The two scans dedupe and attribute differently. The conclusion above rests on the *scoping* of the
> conditions, quoted from the raw response, not on either count.

## 6. SURFACED, NOT MINE, AND NOT FIXED

`terraform fmt -check` fails in **both** modules, on files this cell did not write:

```
infra/aws/terraform/portfolio-management:  main.tf
infra/aws/terraform/news-pipeline:         cross-firm-secret-deny.tf, eventbridge.tf, iam.tf, lambdas.tf
```

**This cell's two files are fmt-clean** (`terraform fmt -check <file>` rc=0 on each, run per file so the
verdict is about my bytes and not the directory's). The five pre-existing files are outside this order's
`<paths>` and formatting them would be a rider on a WORLD cell, so they are surfaced here rather than
touched. Worth knowing before PHASE B, because a module-wide `fmt -check` in a later gate will fail on
them and the cause will not be the adoption.

## 7. STATE OF THE WRITE SURFACE AT THE END OF PHASE A

- `infra/aws/terraform/portfolio-management/zz_adopt_family_e.tf.proposed` -- committed, **inert**.
- `infra/aws/terraform/news-pipeline/zz_adopt_row3.tf.proposed` -- committed, **inert**.
- Both carry one `aws_iam_role` + one `import` block. `inline_policy` and `managed_policy_arns` ABSENT
  from both; `description` additionally absent from row 3, as live. AC1's grep over both files
  returns **0**.
- **Labels fully namespaced, and the collision question MEASURED:**
  `resource "aws_iam_role" "` matches **270 times across 834 files** scanned under
  `infra/aws/terraform`, and `portfolio_management_lambda_role` / `codebuild_semantic_clustering_role`
  match **0 of them**.
- **Neither role is declared anywhere in Terraform at the cut:** a measured **0 hits across 834 files**
  for both names together. The denominator is printed because a bare zero reads as "the term does not
  exist"; 70 binary and 9 ephemeral-floor files in scope were not searched and the zero does not cover
  them.
- Both `.tf` copies -- `zz_adopt_family_e.tf` and `zz_adopt_row3.tf` -- are **REMOVED.** They existed
  only for the four plan runs and are not committed. Both modules' tracked `.tf` sets are unchanged.
- No deploy-ledger entry opened: PHASE B opens `iamroles-r6-family-e`, **one per module**, first.
- **Nothing applied. No tag, policy, trust relationship, instance or Lambda touched.**

## 8. WHAT PHASE B INHERITS

1. **Two modules means two of everything** -- two ledger entries, two applies, two never-widen pairs, and
   AC2 expects **2** `POST-APPLY-PLAN` lines where w-1's expected 1 and AC3 expects `closed=` 2 or more.
2. **The tag counts differ: 3 for `portfolio-management`, 4 for `news-pipeline`** (section 2). The plan
   to match is `1 to import, 0 to add, 1 to change, 0 to destroy` per module, the one change being
   `tags_all` alone -- and unlike Family A's, these shapes are **MEASURED here**, not predicted.
3. **The order of acts is ruled** -- A4-r6 @`7af7a24e9f` and A5-r6 @`f37fb5892d`: commit the renamed
   `.tf` FIRST on the worktree branch, carrying only that file and the placement override's audit row,
   with `# naming-place-override:` naming the role, its live `CreateDate` and `Z-S25`; **take NO author
   override** (the audit row's path is lane ANY @`b7c27ef5b0`, which closed `Z-S26`); then the `-target`
   apply; then the drain in the same session; then an untargeted shared-tree plan recorded at
   `0 to destroy`. Ledger, proof and `POST_APPLY_family_e.md` in separate commits without the override.
4. **Both roles keep their live names** -- Rule 30's existing-pipeline non-application, ruled by the
   issuer; the gate fix for `Z-S25` is `1.0.0_SA_CTO~Z`'s and is parked at dell1.
5. **Two stop conditions, not hopes:** row 3's `assume_role_policy` must show NO change (CodeBuild
   principal), and row 11's `managed_policy_arns` must show NO change (the `AWSLambdaBasicExecutionRole`
   attachment must survive). Both are verified live after the apply, not from the apply's own output.

**PHASE A ends here, per the order's step 3.**
