# PLAN_SURVEY -- Family A (rows 1 and 2, Black Diamond), NFRA_IAMROLES202609.TO-IAM-w-2 PHASE A

**Cell:** IAM-w-2 (round 6, outcome FWD-4; round-5 analysis item E2)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority:** `ROUND_ANALYSIS.round5.md` @f77e32d7c3 E2; `ADOPTION_PLAN_TEN.md` @59112aafed Family A;
amendment A3-r6 @`29f269fca3` (PHASE A runs now, ahead of w-1's PHASE B)
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** WORLD -- **PHASE A APPLIED NOTHING.**

**Measured:** 2026-10-10, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r6-w2` @`b51363b90f`,
Terraform v1.15.8 (resolved on PATH; site Z has no `.tools/terraform.exe`), provider
`hashicorp/aws v5.100.0`. Every plan invocation `-input=false -lock=false`, read-only.

---

## 0. HEADLINE: ONE OF THE FOUR REQUIRED LINES CANNOT BE PRODUCED, AND THE CAUSE IS NOT THIS CELL

`infra/aws/terraform/bd-pipeline` **cannot be planned at HEAD AT ALL** -- with or without this cell's
adoption file. So the `PLAN:` line is recorded as BLOCKED with its cause rather than invented, and the
never-widen pair for PHASE B cannot be written against a plan until the module plans. The other three
required lines are measured and are below. Filed as surprise row **`NFRA_IAMROLES202609-Z-S29`**.

## 1. THE FOUR REQUIRED LINES

```
PLAN: infra/aws/terraform/bd-pipeline: BLOCKED -- the module cannot plan at HEAD. `terraform plan` exits with 4 x "Error: Unsupported attribute" in bd-served-vintage-alarm.tf lines 30 and 32 (NOT in this cell's file). See section 3.
DEFAULT_TAGS: infra/aws/terraform/bd-pipeline: ['Environment', 'ManagedBy', 'Project', 'System']
AUTH_KEY_COLLISION: infra/aws/terraform/bd-pipeline:   *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/bd-pipeline: bd-pipeline/tfstate
```

`STATE_KEY` is read from the module's own `backend "s3"` block (`main.tf` lines 19-23), bucket
`opal-313476888478-terraform-state`, region `us-east-1`. `DEFAULT_TAGS` is read from the module's
`provider "aws"` block (`main.tf` lines 26-36), which declares them in the order `Project`,
`ManagedBy`, `Environment`, `System`; the line above prints the SET as `comp-tagauthz` reports it,
sorted, so it is comparable with Family B's line. Their VALUES differ from Family B's in one key:
this module writes `System = BDPipeline` where `smartx-pipeline` writes `System = SmartXPipeline`.
`AUTH_KEY_COLLISION` is `.tools/comp-tagauthz`'s line verbatim, including its leading spaces.

## 2. THE TWO ROLES' LIVE STATE

Read at 2026-10-10 at write time (`get-role`, `list-role-policies`, `list-attached-role-policies`,
`list-role-tags`), and carried into the declaration as-live. **Both roles have ZERO tags.**

| attribute | `bd-merge-daily-lambda-role` (row 1) | `bd-pipeline-task-role` (row 2) |
|---|---|---|
| tags | **0** (`{"Tags": []}`) | **0** (`{"Tags": []}`) |
| path | `/` | `/` |
| description | `Role for BD Merge Daily Lambda` | **ABSENT** (the API omits the field) |
| max_session_duration | `3600` | `3600` |
| assume_role_policy principal | `lambda.amazonaws.com` | **`ecs-tasks.amazonaws.com`** |
| inline policies | 1 -- `bd-merge-daily-policy` | 1 -- `BDPipelineTaskPolicy` |
| attached managed policies | 0 (`AttachedPolicies: []`) | 0 (`AttachedPolicies: []`) |
| permissions boundary | none | none |
| created | `2026-01-15T07:38:28Z` | `2026-01-29T19:03:54Z` |
| RoleLastUsed | **ABSENT -- never used** | `2026-02-02T16:17:56Z`, `us-east-1` |

**The two live values the cell warned about are both read from the role, never copied from its sibling.**
Row 2's trust principal is `ecs-tasks.amazonaws.com`: the cell says "A copy of a sibling Lambda role's
trust would silently change who may assume it; the plan must show NO change to it", and a wrong principal
here is an authorization move wearing a custody move's clothes, which a plan SUMMARY would not reveal.
Row 2 also has **no description at all**, so the declaration OMITS the `description` argument rather than
setting it to `""` -- setting it would write a field that currently has no value.

**Row 1 has never been used** (`RoleLastUsed` absent, not merely old). That is a fact about usage and
**not a deletion warrant**: ABSENT is not EXERCISED-AGAINST. This cell adopts the role as it stands.

## 3. WHY THE MODULE CANNOT PLAN -- measured, with a negative control

`terraform plan` in `bd-pipeline` fails before producing any plan:

```
Error: Unsupported attribute
  on bd-served-vintage-alarm.tf line 30, in locals:
  30:       as_of_field    = e.as_of_field
This object does not have an attribute named "as_of_field".

Error: Unsupported attribute
  on bd-served-vintage-alarm.tf line 32, in locals:
  32:       page_threshold = e.frontier_page_trading_days
This object does not have an attribute named "frontier_page_trading_days".
```

(four errors: two attributes, each reported for two offending entries)

**NEGATIVE CONTROL -- this is not this cell's file.** With `zz_adopt_family_a.tf` MOVED OUT of the module
and nothing else changed, `terraform plan` emits the **same 4 errors**. The adoption file is not
implicated, and the module was already unplannable before this cell touched it.

**SECOND CONTROL, so this is not read as a defect of a sparse checkout.** An earlier plan attempt in the
worktree failed on a *different* error -- `no file exists at ".../data/black_diamond/scripts/gold/gold_freshness_config.yaml"`
-- which WAS an artifact of my sparse cone and was fixed by widening it. The four `Unsupported attribute`
errors then reproduced in the **shared tree's full checkout**, which has every path. So the finding is
about the repository, not about my working copy.

**THE CAUSE, and it is cross-project.** `bd-served-vintage-alarm.tf` builds a map by comprehension over
every entry of `data/black_diamond/scripts/gold/gold_freshness_config.yaml`, filtering on
`try(e.freshness_basis, "") == "trading-day-frontier"` and then reading `e.as_of_field` and
`e.frontier_page_trading_days` **unguarded** (`try()` protects the filter key only). Commit
**`3d7fb62105`** (2026-10-01, `0.9.0_WK_NFRA_MCPINDEX~25`, "weekly trading-day-frontier basis for the two
weekly BD silver tables") added `freshness_basis: trading-day-frontier` to `bd_silver_allocations` and
`bd_silver_unrealized` -- moving both to `cadence: weekly` -- **without** adding either attribute the
consumer reads. Those two entries now pass the filter and have neither key.

Measured before and after that commit, by the field and not by substring:

| state | entries with `freshness_basis: trading-day-frontier` | of those, missing either attribute |
|---|---|---|
| at `3d7fb62105~1` | 5 | **0** -- the module planned |
| at HEAD | 7 | **2** -- `bd_silver_allocations` (line 107), `bd_silver_unrealized` (line 131) |

2 offending entries x 2 attributes = **4**, which reconciles exactly with Terraform's 4 errors.

> **A count I corrected rather than published.** A first pass over the YAML read "7 trading-day-frontier
> entries, 2 offending"; a second, written differently, read 8 and 3, adding `bd_gold_ticker_resolution`.
> The two disagreed, so neither was quoted until the disagreement was resolved: the second pass matched
> the string `trading-day-frontier` anywhere in an entry's block, and `bd_gold_ticker_resolution`'s match
> is inside a **comment**, not in its `freshness_basis` field. The field-anchored count is the right one,
> and the tell was that only 2-offending reconciles with Terraform's own 4 errors.

**Who owns it:** not this cell and not this lane. The consumer `bd-served-vintage-alarm.tf` is the BD
pipeline's; the edit that broke it belongs to `NFRA_MCPINDEX` cell MX-f-1, authored by worker
`0.9.0_WK_NFRA_MCPINDEX~25` (a worker cannot be messaged; its COO is `2.0.0_SA_COO~MI`). Routed to
`2.0.0_SA_COO~ZI` in row Z-S29 for a cross-project disposition, because a cross-fabric call is not an
AE's to adjudicate. **This cell changed nothing in either file.**

**What it blocks, precisely:** step 2's `PLAN:` line, and therefore the never-widen pair for w-2 PHASE B,
which is written against this survey's plan. It does **not** block the declaration (section 5), the live
reads (section 2), the label census (section 5) or the tag-authorization read (section 4).

## 4. THE TAG-AUTHORIZATION READ -- and here the KEY COLLISION is NOT dismissed as fast as Family B's

`.tools/comp-tagauthz check --default-tags-tree infra/aws/terraform/bd-pipeline` exits **rc=0** in
**MODE: ADVISORY** (no `--candidate`/`--from-state`, because no plan exists to supply them). It swept the
account in one call: **301 roles, 78 local+attached policies, 9 users, 2 groups**; SCPs NOT APPLICABLE,
the account is not in an AWS Organization (`AWSOrganizationsNotInUseException`) -- stated, not implied.
It names what it did NOT sweep: S3 bucket policies, KMS key policies, permission boundaries, session
policies, resource policies generally.

**It surfaced a live instance, which Family B's run did not:**

```
[TAG-AUTHORIZED] i-0643a5bee8a8feabf (stopped)
    System=CottonwoodPipeline  grants access via role/cot-bd-session-trigger-lambda-role:inline:cot-bd-session-trigger-policy  <-- this tree's default_tags WOULD OVERWRITE THIS
```

That is a real conditional grant: `System=CottonwoodPipeline` is what authorizes `ec2:StartInstances` and
`ssm:SendCommand` for the Cottonwood session trigger, and this tree's `default_tags` would write
`System=BDPipeline`. **So the question had to be answered rather than waved away: does `bd-pipeline`
MANAGE that instance?** The tool says what it can and cannot see -- "a tree only endangers a resource it
actually MANAGES" -- and in ADVISORY mode it lists the account's tag-authorized instances, not this
tree's.

**MEASURED, from the module's own state, with a positive control:**

```
bd-pipeline state: 223 entries, 7 of them aws_instance --
  aws_instance.bd_allocations            = i-0800437d1dbb0b5cc
  aws_instance.bd_assets                 = i-0e6f6dc014fdcf1cd
  aws_instance.bd_fees                   = i-0868fc7e7ebec26f2
  aws_instance.bd_gold_detail_generator  = i-074bfc40ee049dc62
  aws_instance.bd_gold_layer_runner      = i-01003b035d2988dfb
  aws_instance.bd_gold_qa_runner         = i-0090b823a4a0997e3
  aws_instance.bd_transactions           = i-00c7568bc510f7423

matches of i-0643a5bee8a8feabf among the 7:  0
positive control (the same comparison against an id known to be in the set):  1
```

The control matters: a loop that can never match reads `0` identically to a true absence. It matched a
known id once, so the zero is a measurement. `i-0643a5bee8a8feabf` is `cot-exporter`, a Cottonwood
instance (`describe-instances`: `Name=cot-exporter`, `System=CottonwoodPipeline`,
`Purpose=BDSessionRefreshAndBronzeIngest`), and **`bd-pipeline` does not manage it**. So this tree's
`default_tags` cannot reach it and the advisory is a false alarm **for this tree**.

**And for THIS CELL the question is narrower still, which is the part that matters for the pair.** This
cell adopts two **IAM roles**. Both account-wide tag conditions are `aws:ResourceTag` scoped to EC2
instances and SSM documents (`System = CottonwoodPipeline`; `Project = NFRA_WEBSITE`), and there are
**0 `aws:PrincipalTag` conditions account-wide** -- Family B's sweep, re-reported here by the same
instrument over 301 roles. An IAM role is not an EC2 instance and not an SSM document, and the values
this module writes (`Project = OpalPortal`, `System = BDPipeline`) match neither condition's required
value. **So the four tags this cell's apply would add to these two roles can neither widen nor narrow
any authorization decision in this account**, on the same two independent grounds as Family B.

> **Recorded as a limit, not resolved:** `tag-conditioned statements found: 9 (4 ours, 5 AWS
> service-linked)` is comp-tagauthz's own count, and PHASE A's Family B survey recorded that this seat's
> hand sweep of the same API response resolved to 4 distinct triples rather than 9. That disagreement is
> unchanged and is not re-derived here. It does not bear on the conclusion, which rests on the
> *scoping* of the conditions (quoted above) rather than on either count.

## 5. THE DECLARATION, AND WHAT WAS COMMITTED

- `infra/aws/terraform/bd-pipeline/zz_adopt_family_a.tf.proposed` -- committed, **inert**. Two
  `aws_iam_role` blocks and two `import` blocks, one per role. `inline_policy` and
  `managed_policy_arns` are ABSENT from both (THE OMISSION RULE); `description` is additionally absent
  from row 2, as live. `terraform fmt -check` clean.
- `grep -c -E '^[[:space:]]*(inline_policy|managed_policy_arns)'` on it returns **0** -- AC1's shape,
  against the `.tf` name once PHASE B lands it.
- **Labels are FULLY NAMESPACED and the collision question was measured, not assumed:**
  `resource "aws_iam_role" "` matches **270 times across 833 files** scanned under
  `infra/aws/terraform`, and `bd_merge_daily_lambda_role` / `bd_pipeline_task_role` match **0 of them**.
  Round 2's battery recorded short labels (`orchestrator`, `scheduler`) reused across three modules and
  silently mis-linking their inline policies, which is why this is checked rather than trusted.
- **Neither role is declared anywhere in Terraform at the cut**: a measured **0 hits across 833 files**
  for both names together. The denominator is printed because a bare zero would read as "the term does
  not exist"; 70 binary and 9 ephemeral-floor files in scope were not searched and the zero does not
  cover them. (First attempt at this census used `\|`, which python `re` reads as a LITERAL -- it
  returned a zero that was the pattern, not the world. comp-find's own warning caught it; re-run with a
  bare pipe.)
- `infra/aws/terraform/bd-pipeline/zz_adopt_family_a.tf` -- **REMOVED.** The `.tf` copy existed only for
  the plan attempts and is not committed. The module's tracked `.tf` set is unchanged.
- No deploy-ledger entry opened. PHASE B opens `iamroles-r6-family-a` first.
- **Nothing applied. No tag, policy, trust relationship, instance or Lambda touched.**

## 6. WHAT PHASE B INHERITS

1. **Its order of acts is already ruled** -- amendment A4-r6 @`7af7a24e9f` rewrote step 5 of this order
   after w-1's PHASE B measured three hazards (rows Z-S25, Z-S26, Z-S27, carried by Z-S28): commit the
   renamed `.tf` on the worktree branch FIRST, carrying only that file and the placement override's audit
   row, under `GIT_COMMIT_AUTHOR_OVERRIDE=GOVERNANCE_AUDIT` with `# naming-place-override:` naming both
   roles, their live `CreateDate`s and Z-S25; THEN the `-target` apply; THEN the drain in the same
   session; THEN an untargeted shared-tree plan recorded as reading `0 to destroy`. The ledger, proof and
   `POST_APPLY_family_a.md` land in separate commits under neither override.
2. **Both roles keep their live names** -- `bd-merge-daily-lambda-role` and `bd-pipeline-task-role`. The
   naming canon will ask for other forms; the issuer ruled Rule 30's existing-pipeline non-application,
   and the gate fixes belong to `1.0.0_SA_CTO~Z`, not to this cell.
3. **The `-target` list is TWO addresses**, not one: `aws_iam_role.bd_merge_daily_lambda_role` and
   `aws_iam_role.bd_pipeline_task_role`. The plan to match is `2 to import, 0 to add, 2 to change,
   0 to destroy`, where each change is `tags_all` alone -- **but that shape is PREDICTED from the shape
   of Family B's measured plan, not measured here, because the module does not plan.** It must be
   rendered and read against live state at PHASE B. Row 2's `assume_role_policy` showing NO change is a
   stop condition, not a hope.
4. **Z-S29 must be closed first.** Until `bd-pipeline` plans, there is no plan for the pair to sign.

**PHASE A ends here, per the order's step 3, with step 2's `PLAN:` line BLOCKED and its cause named.**
