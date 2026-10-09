# ACCEPTANCE -- the ten rows of IAM-v-2

**By:** `0.7.0_AE_CloudOps~Z`, 2026-10-09, under `NFRA_IAMROLES202609.TO-IAM-v-2` (cell `IAM-v-2`, outcome
`FWD-4`). **Owner of record** per `1.0.0_SA_CTO~Z` `@fa8ec0e726`.
**ALL TEN ROWS ACCEPTED.** None refused. Nothing applied, no AWS write call, no `.tf` written, no role deleted,
not one permission narrowed.

This document is my acceptance of record, per amendment A1 `@193ee5ac41` (row `Z-S19`). The row edits in
`GOVERNANCE_DISPOSITION.md` are its carrier and are left UNCOMMITTED for the issuer to land, because that file
sits under another serial's deliverables folder and the owned-paths lane refuses this seat there. **I did not
take an author override** -- the same reasoning as `IAM-v-1`: it would forge the authorship the cell exists to
establish.

**What I accept on every row below, uniformly:** custody of the role AND of the adoption decision for it.
**What I do NOT accept on any of them:** the apply. Moving any declaration into a live `.tf`, or deleting any
role, is a separate WORLD act under its own never-widen pair, outside this round's `NO APPLY` bound. The
per-family mechanics, the order of application, and the two things that do not travel with the text are in
`ADOPTION_PLAN_TEN.md`; this file is the acceptance and the per-role reasoning.

**Common to all ten, and the one technical condition I attach to every future pair:** every declaration must
leave `inline_policy` and `managed_policy_arns` ABSENT. Both are Optional+Computed; set, they become
authoritative and detach anything unlisted. Nine of these ten carry at least one live inline or managed policy,
so for nine of them a "completed" block is an outage rather than a tidy-up.

Every figure below is a live read taken 2026-10-09, with consumers measured from `lambda list-functions`
(**denominator 233 functions**) rather than asserted. None of the ten is declared in Terraform: one grep over
`infra/aws/terraform/**/*.tf` for all ten names returns zero, while the same grep for the six sibling roles in
`ADOPTION_PLAN_TEN.md` section 1 returns eighteen matches -- so the zero is a measured absence and not a broken
pattern.

---

## Row 1 -- `bd-merge-daily-lambda-role` (ADOPT)
Live: lambda trust, 1 inline `bd-merge-daily-policy`, 0 managed, 0 consumers, `RoleLastUsed` **EMPTY**, created
2026-01-15. Accepted. Its inline policy names the Black Diamond merge job, and `bd-pipeline/iam.tf` already
declares two roles from the 2026-02-19 batch with a numbered inventory at its head, so custody is an extension
of an existing list rather than a new claim. **Never used and I am still accepting rather than retiring:** this
estate's own pattern is that unused is not a delete warrant -- `news-pipeline/iam.tf:256,303` declares two roles
it explicitly annotates `orphaned - no Lambda currently attached`. **Not accepted:** the apply.

## Row 2 -- `bd-pipeline-task-role` (ADOPT)
Live: **`ecs-tasks.amazonaws.com` trust** -- the only non-Lambda trust of the ten -- 1 inline
`BDPipelineTaskPolicy`, 0 managed, 0 Lambda consumers (expected: it is an ECS task role, so the Lambda map
cannot see its consumers and a 0 there is NOT evidence of disuse), `RoleLastUsed` 2026-02-02, created
2026-01-29. Accepted, same custody home as row 1. **The condition I attach:** its pair must state the
`assume_role_policy` principal explicitly, because the `ecs-tasks` principal is precisely the field a
copy-paste from a sibling Lambda role gets silently wrong, and a wrong trust principal is a role nothing can
assume. **Not accepted:** the apply.

## Row 3 -- `codebuild-semantic-clustering-role` (ADOPT)
Live: `codebuild.amazonaws.com` trust, 1 inline `CodeBuildSemanticClusteringPolicy`, 0 managed, 0 Lambda
consumers (again expected -- CodeBuild, not Lambda), `RoleLastUsed` **2026-09-11**, created 2026-02-17.
Accepted. **This is the most recently used role of the ten after row 6**, four weeks before this reading, so it
is live infrastructure and not a leftover. **The open call I name rather than close:** its home. It is a
BUILD-plane role, and the module that owns the semantic/news RUNTIME (`news-pipeline/`) is not obviously the
module that should own a CodeBuild project's role. I accept custody of the role and of the decision; I do not
assert the module, and I would not let a pair land it into `news-pipeline/` just because the names rhyme.
**Not accepted:** the apply.

## Row 5 -- `finbert-ec2-backfill-role` (ADOPT as the row stands -- with an adopt-or-retire call named)
Live: `ec2.amazonaws.com` trust, 1 inline `DynamoDBAccessPolicy`, 0 managed, `RoleLastUsed` 2025-12-15 in
**us-east-2**, created 2025-12-15. Accepted as owner of record. **The whole of its lifetime is about one hour**:
created 14:23Z and last used 15:20Z on the same day, never since -- the signature of a one-shot backfill.
**I propose no custody home, and that is deliberate**, not an omission: adopting a role whose job is finished is
the wrong act, and retiring it is a WORLD decision nobody has asked for. The decision owed is which of the two
it is, and the evidence that settles it -- whether the finbert backfill is repeatable or completed -- sits with
whoever owns that workload. I hold the row so it is no longer `NO-ACCEPTING-SEAT`, and I name the call instead
of silently leaving it in the ADOPT column. **Not accepted:** the apply, and any retirement.

## Row 6 -- `lambda-ec2-runtime-monitor-role` (ADOPT)
Live: lambda trust, 1 inline `EC2RuntimeMonitorPolicy`, 1 managed `AWSLambdaBasicExecutionRole`, **1 consumer
`ec2-runtime-monitor`**, `RoleLastUsed` **2026-10-09T09:51:30Z -- fifteen minutes before I read it**, created
2026-02-06. Accepted. **This is a running production role and the acceptance says so loudly**, because the one
error this row invites is treating an undeclared role as a dormant one. **The open call I name:**
`ec2-runtime-monitor` is a cross-cutting operational function and no module obviously owns it;
`shared-infra/iam_legacy.tf` is the honest candidate since it already holds `infrastructure-ops-lambda-role`
from the same 2026-02-19 batch, but the word "legacy" in that filename argues against putting live
infrastructure there. I accept custody and the decision; the placement is open. **Not accepted:** the apply --
and for this row and row 14 the omission condition above is not a formality: a completed `inline_policy` block
here reaches a function that ran this morning.

## Row 7 -- `lambda-test-role` (RETIRE)
Live: lambda trust, **0 inline**, 1 managed `AWSLambdaBasicExecutionRole`, 0 consumers, `RoleLastUsed`
**EMPTY**, created 2026-02-19T16:00:44 in the nine-role scripted batch. Accepted as owner of record, **and I
accept the RETIRE disposition as the right one** -- the only retirement I propose among the ten.
**Why this one and not the other unused roles,** since four of the ten are unused or long-unused: row 7 grants
nothing beyond CloudWatch Logs, its name identifies no workload so no pipeline is identifiable as its owner, and
it has never been used. Rows 11 and 14 fail that test on every count, which is why I adopt them.
**What I do NOT accept:** the delete itself, and anything that treats this acceptance as authorizing it. The
retirement plan -- the four things that must prove nothing assumes it, including an ABSENT negative control
against a role known to be in use, and the rollback from the recorded trust document -- is in
`ADOPTION_PLAN_TEN.md` Family F. It is a WORLD act needing its own order and pair.

## Row 9 -- `opal-smartx-lambda-role` (ADOPT)
Live: lambda trust, **3 inline** (`opal-smartx-logs`, `opal-smartx-s3-access`, `opal-smartx-secrets`), 0
managed, 0 consumers, `RoleLastUsed` 2025-12-30, created 2025-11-20. Accepted. The cleanest adoption of the ten:
all three policies name the pipeline, and `infra/aws/terraform/smartx-pipeline/` exists (15 `.tf` files,
verified) and is in this seat's declared pipeline set. **The proportionate warning:** three inline policies is
the most of any role here, so this is where "completing" the block costs most. **Not accepted:** the apply.

## Row 11 -- `portfolio-management-lambda-role` (ADOPT)
Live: lambda trust, 1 inline `portfolio-s3-dynamodb`, 1 managed `AWSLambdaBasicExecutionRole`, 0 consumers,
`RoleLastUsed` **EMPTY**, created 2026-02-19T16:00:38 with the description `Scoped Lambda role - created
2026-02-19 IAM audit`. Accepted, and this is the best-precedented row of the ten. Six of its nine batch siblings
are already declared in their own domain modules, and its home
`infra/aws/terraform/portfolio-management/` exists (3 `.tf` files) and already declares the distinctly-named
sibling `portfolio-export-lambda-role` -- which I verified by printing the bytes at `main.tf:226-227` rather
than trusting the row's citation. Zero consumers and EMPTY last-use do not withhold the declaration, per the
`news-pipeline` orphan precedent. **Not accepted:** the apply.

## Row 14 -- `sentiment_query_api-role` (ADOPT)
Live: lambda trust, 1 inline `DynamoDBAccess`, 1 managed `AWSLambdaBasicExecutionRole`, **1 consumer
`sentiment_query_api`**, `RoleLastUsed` 2026-01-02 in **us-east-2**, created 2025-11-24. Accepted. A live
consumer-bearing role, so it belongs in Family C with row 6 and is adopted LAST of the adoptions.
**The condition I attach:** its pair must carry the REGION. Both its consumer and its last use are in
us-east-2, and the module it lands in has a provider region -- a declaration that silently assumes us-east-1
would be adopting a role whose workload lives elsewhere. **Not accepted:** the apply.

## Row 16 -- `workspace-sync-lambda-role` (ADOPT)
Live: lambda trust, 1 inline `workspace-sync-permissions`, 0 managed, 0 consumers, `RoleLastUsed` 2025-12-30,
created 2025-12-05. Accepted. Its inline policy names the workload. **The honest limit on this one:** it is the
row with the least distinguishing evidence of the ten -- a named policy and a named role, nine months idle, no
consumer and no obvious module -- so I accept custody without asserting a home, and I would want the workload's
owner named in its pair before a declaration lands anywhere. **Not accepted:** the apply.

---

## What this acceptance does NOT claim

- **It is not a narrowing recommendation for any row.** `C-TWO-REMEDIES` binds this project to governance only.
  Four of these roles are unused or long-unused and that is a true measurement which is NOT a deletion warrant:
  ABSENT is not EXERCISED-AGAINST, and cloud-ops names the under-reporting direction as the dangerous one
  precisely because it invites a cleanup to delete a needed grant as "unused". Row 7 is proposed for retirement
  on the strength of being EMPTY and generic, not on being unused.
- **It does not settle three placement questions**, each named at its row rather than buried: row 3's build-plane
  home, row 5's adopt-or-retire, row 6's home for a live cross-cutting function. `FWD-4` asks that every role
  have a named owner and a reason; "the placement is still open" is a reason an owner can hold, and it is a
  different thing from "nobody has been asked", which is what `NO-ACCEPTING-SEAT` recorded.
- **It does not re-open rows 4, 8, 10, 12, 13 or 15.** Rows 8 and 10 are `IAM-v-1`'s, already accepted by this
  seat; 4, 12 and 15 are `1.0.0_SA_CTO~Z`'s; 13 is DECLARED. The prepared edit touches my ten rows only, and
  that scope is asserted mechanically rather than promised.
