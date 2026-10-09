# ADOPTION_PLAN_TEN -- the ten rows of IAM-v-2, grouped by the module that should own each

**By:** `0.7.0_AE_CloudOps~Z`, 2026-10-09, under `NFRA_IAMROLES202609.TO-IAM-v-2` (cell `IAM-v-2`, outcome
`FWD-4`). **Owner of record** per `1.0.0_SA_CTO~Z` `@fa8ec0e726`.
**NO APPLY. The plan is text.** No `.tf` file is written, no `import` is applied, no role is deleted, and not one
permission is narrowed (`C-TWO-REMEDIES`). No Access Analyzer call (`C-ANALYZER-PRICED-FIRST`, `G-25`); no alert,
alarm, monitor or schedule (`G-21`).

---

## 0. The live survey this plan is built on

Every role below was read live on 2026-10-09, not taken from the disposition's text. Per role: existence, trust
principal, inline policy names, attached managed policies, `RoleLastUsed`, creation date; consumers were built
from `lambda list-functions` and grouped client-side, **denominator 233 functions scanned**.

| # | role | trust | inline | managed | consumers | RoleLastUsed | created |
|---|---|---|---|---|---|---|---|
| 1 | `bd-merge-daily-lambda-role` | lambda | 1 | 0 | 0 | **EMPTY** | 2026-01-15 |
| 2 | `bd-pipeline-task-role` | ecs-tasks | 1 | 0 | 0 | 2026-02-02 | 2026-01-29 |
| 3 | `codebuild-semantic-clustering-role` | codebuild | 1 | 0 | 0 | **2026-09-11** | 2026-02-17 |
| 5 | `finbert-ec2-backfill-role` | ec2 | 1 | 0 | 0 | 2025-12-15 (us-east-2) | 2025-12-15 |
| 6 | `lambda-ec2-runtime-monitor-role` | lambda | 1 | 1 | **1** (`ec2-runtime-monitor`) | **2026-10-09T09:51Z** | 2026-02-06 |
| 7 | `lambda-test-role` | lambda | 0 | 1 | 0 | **EMPTY** | 2026-02-19T16:00:44 |
| 9 | `opal-smartx-lambda-role` | lambda | 3 | 0 | 0 | 2025-12-30 | 2025-11-20 |
| 11 | `portfolio-management-lambda-role` | lambda | 1 | 1 | 0 | **EMPTY** | 2026-02-19T16:00:38 |
| 14 | `sentiment_query_api-role` | lambda | 1 | 1 | **1** (`sentiment_query_api`) | 2026-01-02 (us-east-2) | 2025-11-24 |
| 16 | `workspace-sync-lambda-role` | lambda | 1 | 0 | 0 | 2025-12-30 | 2025-12-05 |

**All ten exist, and none of the ten is declared in Terraform.** That second half is a measured absence, not a
failed search: one `grep` over `infra/aws/terraform/**/*.tf` for all ten names returns **zero** matches, and the
SAME grep over the same corpus for the six sibling roles in section 1 returns eighteen matches across five
files. The instrument discriminates, so the zero is an absence.

## 1. THE PRECEDENT THIS ESTATE HAS ALREADY SET, and it decides most of this plan

Rows 7 and 11 were created in an eight-second window on 2026-02-19, and they are not alone. A census of all
**292** roles in the account shows **nine** minted between `16:00:37` and `16:00:44` -- a scripted batch, three
of them carrying the literal description `Scoped Lambda role - created 2026-02-19 IAM audit`:

```
16:00:37  bd-processor-lambda-role                 -> DECLARED  bd-pipeline/iam.tf:216
16:00:38  portfolio-management-lambda-role         -> row 11, undeclared
16:00:39  portal-auth-lambda-role                  -> row 10 (IAM-v-1, accepted by this seat)
16:00:40  infrastructure-ops-lambda-role           -> DECLARED  shared-infra/iam_legacy.tf:43
16:00:41  market-data-generator-lambda-role        -> DECLARED  market-overview/iam_legacy.tf:16
16:00:42  historical-prices-lambda-role            -> DECLARED  bd-pipeline/iam.tf:1010
16:00:42  semantic-news-lambda-role                -> DECLARED  news-pipeline/iam.tf:306
16:00:43  news-sentiment-lambda-role               -> DECLARED  news-pipeline/iam.tf:259
16:00:44  lambda-test-role                         -> row 7, undeclared
```

**Six of the nine were subsequently adopted into their own domain's module. Three were not, and all three are
disposition rows.** That is the pattern to follow rather than invent: a role from this batch goes into the
module that owns its domain.

**And the estate has already decided the hard sub-case.** `news-pipeline/iam.tf` declares two of those six with
the comment `orphaned - no Lambda currently attached` (`:256`, `:303`) -- it DECLARES a role with zero consumers
rather than retire it. So "nothing uses it" is NOT this estate's reason to delete a role; it is compatible with
declaring it. That bears directly on row 11 (0 consumers, never used) and on `IAM-v-1`'s row 10, and it is why
only row 7 is proposed for retirement below -- row 7's distinguishing fact is not that it is unused but that it
is *empty and generic*.

**A check I ran that did NOT find a problem, recorded because a confirming result is also evidence.** If those
six siblings had been undeclared too, the disposition's 16-row domain would have been the wrong population and
`FWD-4`'s closure would be measured against it. I hunted the uncovered member by subtraction from the printed
292 rather than forward-listing: all six resolve in Terraform, so the domain holds against this probe. The
disposition is 16 rows because the other 276 roles are in code, and this batch is a fair sample of that claim.

## 2. THE FAMILIES, and the order I would apply them in

Grouped by the module that should own each. Within each family the adopting act is the same shape as round 2's
candidate: one `resource "aws_iam_role"` block plus one `import` block per role, resource labels FULLY
NAMESPACED to the role name, and `inline_policy` / `managed_policy_arns` **DELIBERATELY ABSENT**.

> **The omission is the whole safety property and it is not stylistic.** Both arguments are Optional+Computed in
> the AWS provider: OMITTED they are unmanaged and live attachments are left alone; SET -- even to a list that
> looks complete -- they become AUTHORITATIVE and anything unlisted is detached on the next run. Every role below
> carries at least one live inline or managed policy except row 7, so for every one of them "completing" the
> block is an outage, not a tidy-up. Any seat moving these declarations into a live file must not complete them.

**What does not travel with the text, for every family** (ADOPTION_PLAN section 7's two items, and they are
module-scoped, so they change per family): **(i) the state key** the declaration lands in, and **(ii) the
provider `default_tags`** the module inherits. The second is the sharper one and I met it for real today: the
`data-refresh` root's `default_tags` keys are `Environment`, `ManagedBy`, `Project`, and `safe-apply`'s
tag-authorization gate printed `*** KEY COLLISION: ['Project'] are BOTH default_tags keys AND authorization
keys` for that root. **Nine of these ten roles carry 0 tags today**, so an adoption would be the first act to
put `default_tags` onto them -- the one way a declaration that "changes nothing" could change an authorization
decision. Each family's pair must name its own module's `default_tags` keys and say whether any is an
authorization key.

### Family A -- Black Diamond pipeline: `infra/aws/terraform/bd-pipeline/`
Rows **1** `bd-merge-daily-lambda-role` and **2** `bd-pipeline-task-role`.

Custody home is settled rather than argued: that module already declares two roles from the same 2026-02-19
batch (`bd-processor-lambda-role:216`, `historical-prices-lambda-role:1010`) and its `iam.tf` opens with a
numbered inventory of the roles it owns, so these two extend an existing list. Row 1's inline policy is named
`bd-merge-daily-policy` and row 2's `BDPipelineTaskPolicy` -- both name the pipeline, not a generic function.

Row 2 is the only **non-Lambda** trust in this family (`ecs-tasks.amazonaws.com`), so its declaration is an ECS
task role, not a Lambda execution role, and its pair should say so explicitly: the `assume_role_policy`
principal is the one field a copy-paste from a sibling Lambda role would silently get wrong.

### Family B -- SmartX: `infra/aws/terraform/smartx-pipeline/`
Row **9** `opal-smartx-lambda-role`.

The only role of the ten with **three** inline policies (`opal-smartx-logs`, `opal-smartx-s3-access`,
`opal-smartx-secrets`), all three named for the pipeline, and a module of that exact name already exists in this
seat's declared pipeline set. One role, one family, cleanest adoption of the ten. Its omission discipline matters
most here in proportion: three inline policies to lose if the block is "completed".

### Family C -- live, consumer-bearing roles: highest stakes, adopt LAST
Rows **6** `lambda-ec2-runtime-monitor-role` and **14** `sentiment_query_api-role`.

These two are the only ones of the ten with a **live Lambda consumer**, and row 6 was used at
**2026-10-09T09:51Z -- fifteen minutes before I read it**. Treating row 6 as a dormant role would be the error
this family exists to prevent. Row 14's consumer `sentiment_query_api` and its last use are both in
**us-east-2**, a second region, which is a fact its pair must carry because the module it lands in has a
provider region.

Custody home for row 6 is an open question I am NOT closing here: `ec2-runtime-monitor` is a cross-cutting
operational function and no module obviously owns it; `shared-infra/iam_legacy.tf` is the honest candidate
(it already holds `infrastructure-ops-lambda-role` from the same batch), but "legacy" in the filename argues the
opposite. Named as the one placement call in this family.

### Family D -- EC2 one-shot backfill: no home proposed
Row **5** `finbert-ec2-backfill-role`.

`ec2.amazonaws.com` trust, one inline `DynamoDBAccessPolicy`, created and last used on the SAME DAY
(2025-12-15, us-east-2) and never since -- the signature of a one-shot backfill, and the only role of the ten
whose entire lifetime is one hour. I do not propose a custody home, because adopting a role whose job is
finished is the wrong act and retiring it is a WORLD decision nobody has asked for. **The decision owed is
which of the two it is**, and the evidence that would settle it is whether the finbert backfill is a repeatable
act or a completed one -- which lives with whoever owns that workload, not with me. Declared as an open call, not
left silently in the ADOPT column.

### Family E -- the 2026-02-19 audit remainder: `portfolio-management`
Row **11** `portfolio-management-lambda-role`.

Section 1's precedent applies directly: same batch, same `Scoped Lambda role - created 2026-02-19 IAM audit`
description, and six of its nine siblings are declared. Home is
`infra/aws/terraform/portfolio-management/`, which the disposition's own row 11 already cites as declaring the
distinctly-named sibling `portfolio-export-lambda-role` at `main.tf:227`. So this is the narrow, well-precedented
case: a genuinely separate undeclared role alongside an already-declared one in the same module. Zero consumers
and `RoleLastUsed` EMPTY are NOT a reason to withhold the declaration -- `news-pipeline/iam.tf` declares two
explicitly-orphaned roles, so the house pattern is to declare and let usage be a separate question.

### Family F -- RETIRE, and it is the only one: row 7 `lambda-test-role`
The retirement plan the order asks for instead of an adoption plan.

**Why this one and not the other unused roles.** Four of the ten have never been used or have not been used in
nine months, and I am proposing retirement for exactly one. Row 7's distinguishing facts are that it carries
**zero inline policies** and only `AWSLambdaBasicExecutionRole`, so it grants nothing beyond CloudWatch Logs;
its name is generic (`lambda-test-role`) rather than naming a workload, so no pipeline is identifiable as its
owner; and `RoleLastUsed` is EMPTY since creation in the 2026-02-19 batch. It is a role with no permissions, no
consumer, no domain and no use. Rows 11 and 14 fail that test on every count, which is why they are adopted.

**What would prove nothing assumes it, before any delete:**
1. **No Lambda uses it** -- re-run the `lambda list-functions` role map with its denominator printed; today it
   reads 0 of 233. That is necessary and NOT sufficient, because the map only sees Lambda.
2. **Nothing else assumes it** -- its trust policy admits exactly `lambda.amazonaws.com`, so no human, no other
   service and no cross-account principal can assume it; that single-principal trust is what makes limb 1
   nearly decisive rather than merely suggestive. Read the trust document at delete time, not from this file.
3. **`RoleLastUsed` still EMPTY at the moment of deletion**, re-read then and not inherited from here. Note its
   own limit, stated rather than hidden: the field has a tracking-period bound and region scope, so EMPTY means
   "no recorded use this instrument can see", not a proof of never. Combined with limbs 1 and 2 it is enough;
   alone it is not.
4. **An ABSENT negative control** -- the same three reads against a role known to be in use (row 6, used today)
   must come back POSITIVE in the same run, or the reads are not discriminating and the verdict is the
   instrument.

**The delete, and what it is not:** `aws iam delete-role` after `delete-role-policy`/`detach-role-policy` for
what it carries (here: detach `AWSLambdaBasicExecutionRole`, no inline to delete). **Rollback is re-creation
from the recorded trust document and the one managed-policy attachment, both captured before the delete** --
cheap precisely because the role grants nothing. This is a WORLD act, outside this round's `NO APPLY` bound and
outside `C-TWO-REMEDIES`, so it needs its own order and its own never-widen pair. Nothing here deletes anything.

### Order of application, and why
1. **Family B (SmartX)** -- one role, one obvious module, three same-named policies; the cheapest real exercise
   of the omission discipline.
2. **Family A (BD)** -- two roles into a module that already carries this exact pattern, one of them the
   non-Lambda trust that is worth getting right while attention is high.
3. **Family E (portfolio-management)** -- the well-precedented single case.
4. **Family C (live consumers)** -- LAST of the adoptions, deliberately: by then the shape has been exercised
   three times, and these are the two where a mistaken `inline_policy` completion reaches a running function.
5. **Family F (row 7, RETIRE)** and **Family D (row 5)** -- neither is an adoption and neither belongs in this
   sequence. Row 7 needs its own WORLD order; row 5 needs a decision before it needs an act.

Each family is its own apply, its own ledger and its own never-widen pair. I would not batch them: the families
differ in trust principal, region, provider `default_tags` and blast radius, and a single pair covering all ten
would be a pair that names none of those differences.

## 3. Rows I am NOT accepting

**None.** All ten rows in this cell are accepted as owner of record; the per-row acceptances are in
`ACCEPTANCE_ROWS_TEN.md`. Two carry explicit open calls inside the acceptance rather than a refusal -- row 5's
adopt-or-retire question and row 6's custody home -- because the gap in both is a decision someone must make,
not a reason to leave `owner=NO-ACCEPTING-SEAT` standing. `FWD-4` asks that every role have a named owner and a
reason, and "the placement is still open" is a reason an owner can hold; "nobody has been asked" is not.
