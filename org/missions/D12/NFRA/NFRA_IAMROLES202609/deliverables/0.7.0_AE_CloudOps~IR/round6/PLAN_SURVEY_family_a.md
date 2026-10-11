# PLAN_SURVEY -- Family A (rows 1 and 2, Black Diamond), NFRA_IAMROLES202609.TO-IAM-w-2 PHASE A

**Cell:** IAM-w-2 (round 6, outcome FWD-4; round-5 analysis item E2)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority:** `ROUND_ANALYSIS.round5.md` @f77e32d7c3 E2; `ADOPTION_PLAN_TEN.md` @59112aafed Family A;
amendment A3-r6 @`29f269fca3` (PHASE A runs now); amendment **A6-r6** @`59d56f3848` (step 1a)
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** WORLD -- **PHASE A APPLIED NOTHING.**

**Measured:** 2026-10-10, worktree `C:/tmp/iam-w1b`, Terraform v1.15.8 (resolved on PATH; site Z has no
`.tools/terraform.exe`), provider `hashicorp/aws v5.100.0`. Every plan invocation `-input=false
-lock=false`, read-only, saved with `-out` and graded from `show -json`.
**Two passes:** the first on branch `wk-iamroles-r6-w2` @`b51363b90f`, when the module could not plan at
all; the second on `wk-iamroles-r6-w2-1a` @`9586e0106b` after step 1a landed the guard that unblocked it.

---

## 1. THE FOUR REQUIRED LINES

```
PLAN: infra/aws/terraform/bd-pipeline: Plan: 2 to import, 0 to add, 2 to change, 0 to destroy.
DEFAULT_TAGS: infra/aws/terraform/bd-pipeline: ['Environment', 'ManagedBy', 'Project', 'System']
AUTH_KEY_COLLISION: infra/aws/terraform/bd-pipeline:   *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/bd-pipeline: bd-pipeline/tfstate
```

`STATE_KEY` is read from the module's own `backend "s3"` block (`main.tf` lines 19-23), bucket
`opal-313476888478-terraform-state`, region `us-east-1`. `DEFAULT_TAGS` is read from the module's
`provider "aws"` block, which declares them in the order `Project`, `ManagedBy`, `Environment`,
`System`; the line above prints the SET as `comp-tagauthz` reports it, sorted, so it is comparable with
Families B and E. Values differ from Family B's in one key: this module writes `System = BDPipeline`.
`AUTH_KEY_COLLISION` is `.tools/comp-tagauthz`'s line verbatim, including its leading spaces.

**This `PLAN:` line replaces a BLOCKED one.** The first pass could not produce it; section 4 records
why, because that record is the evidence behind row `Z-S29` and it is not erased by the fix.

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

**The two live values the cell warned about are both read from the role, never copied from its sibling,
and the plan now CONFIRMS both rather than leaving them asserted** (section 3). Row 2's trust principal
is `ecs-tasks.amazonaws.com`: the cell says "A copy of a sibling Lambda role's trust would silently
change who may assume it; the plan must show NO change to it", and a wrong principal here is an
authorization move wearing a custody move's clothes, which a plan SUMMARY would not reveal. Row 2 also
has **no description at all**, so the declaration OMITS the `description` argument rather than setting it
to `""`.

**Row 1 has never been used** (`RoleLastUsed` absent, not merely old). A fact about usage and **not a
deletion warrant**: ABSENT is not EXERCISED-AGAINST. This cell adopts the role as it stands.

## 3. THE PLAN, GRADED PER ATTRIBUTE -- and the two stop conditions, measured

The summary `2 to import, 0 to add, 2 to change, 0 to destroy` is **exactly what a trust-policy rewrite
would also print**, so the summary cannot grade the act. Graded from `show -json` on the saved plan, by
decomposing every `resource_change`:

| | measured |
|---|---|
| `resource_changes` total | **205** |
| non-no-op | **2** |
| the addresses | `aws_iam_role.bd_merge_daily_lambda_role`, `aws_iam_role.bd_pipeline_task_role` |
| actions / import ids | both `['update']`, importing `bd-merge-daily-lambda-role` and `bd-pipeline-task-role` |
| attributes that differ, per role | **1 each** |
| the delta, per role | `tags_all: {}` -> `{Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=BDPipeline}` |
| `inline_policy` | unchanged on both |
| `managed_policy_arns` | unchanged on both |
| `assume_role_policy` | **unchanged on both** |
| `description` | unchanged on both (row 2's stays absent) |
| destroys | 0 |
| non-no-op addresses that are NOT one of the two adopted roles | **`[]` -- none** |

**STOP CONDITION 1, SATISFIED AND PRINTED.** Row 2's trust in the plan, `before == after`:

```
"{\"Statement\":[{\"Action\":\"sts:AssumeRole\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"ecs-tasks.amazonaws.com\"}}],\"Version\":\"2012-10-17\"}"
```

The ECS principal is intact. This is printed rather than summarised because "assume_role_policy
unchanged=True" is a claim about a comparison, and the value is what a reader can check.

**STOP CONDITION 2, SATISFIED.** 205 resource_changes and exactly 2 non-no-op, both of them the adopted
roles. A plan of 205 addresses is not a small plan, and reading only its summary line is how an
unintended address rides along unnoticed.

**NEGATIVE CONTROL.** With `zz_adopt_family_a.tf` MOVED OUT and nothing else changed:

```
No changes. Your infrastructure matches the configuration.
```

**ZERO pre-existing drift.** So the entire delta -- 2 imports plus 2 `tags_all` changes -- is
attributable to this cell, and there is nothing else an apply could carry. This is the opposite of
Family B, where the control read `0 to add, 3 to change, 0 to destroy` and three unauthorized Lambda
code deploys would have ridden an unscoped apply (row `Z-S21`). **The `-target` scoping the cell binds
(A2-r6) is therefore belt-and-braces in this module rather than load-bearing as it was in
`smartx-pipeline`; it still binds, and PHASE B must still use it, because the control proves the drift
is zero TODAY and says nothing about the hour of the apply.**

## 4. WHY THE FIRST PASS COULD NOT PLAN, AND WHAT UNBLOCKED IT (row Z-S29 -> step 1a)

**This section is kept in full after the fix.** It is the evidence behind `Z-S29`, and a survey that
simply showed the working plan would hide that the module was unplannable for nine days.

On the first pass `terraform plan` in `bd-pipeline` failed before producing any plan -- 4 x
`Error: Unsupported attribute` at `bd-served-vintage-alarm.tf` lines 30 and 32 (`e.as_of_field`,
`e.frontier_page_trading_days`). That file builds `local.bd_served_vintage_keys` by comprehension over
every entry of `data/black_diamond/scripts/gold/gold_freshness_config.yaml`, filtering on
`try(e.freshness_basis, "") == "trading-day-frontier"` and then reading both attributes **unguarded** --
the `try()` protected the filter key only. Commit `3d7fb62105` (2026-10-01, `0.9.0_WK_NFRA_MCPINDEX~25`,
cell MX-f-1) moved `bd_silver_allocations` and `bd_silver_unrealized` to `cadence: weekly` and gave each
`freshness_basis: trading-day-frontier` **without** either attribute.

| state | entries with `freshness_basis: trading-day-frontier` | of those, missing either attribute |
|---|---|---|
| at `3d7fb62105~1` | 5 | **0** -- the module planned |
| at HEAD, before step 1a | 7 | **2** -- `bd_silver_allocations` (line 107), `bd_silver_unrealized` (line 131) |

2 offending entries x 2 attributes = **4**, reconciling exactly with Terraform's 4 errors.

**FOUR CONTROLS, because four different things could have produced that reading and only one is the
world:**

1. **NEGATIVE** -- the same 4 errors with this cell's adoption file moved out, so my file was never
   implicated.
2. **CHECKOUT** -- an earlier failure was genuinely mine: `no file exists at
   .../gold_freshness_config.yaml`, an artifact of my sparse cone, fixed by widening it. The 4
   `Unsupported attribute` errors then reproduced in the **shared tree's full checkout**, so the finding
   was about the repository and not about a working copy.
3. **COUNT RECONCILIATION** -- a first YAML pass read 7 entries / 2 offending and a second read 8 / 3.
   Neither was quoted until the disagreement was resolved: the second matched the string
   `trading-day-frontier` anywhere in an entry's block and wrongly caught `bd_gold_ticker_resolution`,
   whose only match is inside a **comment**. The field-anchored count is the right one, and the tell was
   that only 2-offending reconciles with Terraform's own 4 errors.
4. **A THIRD INSTRUMENT I DID NOT WRITE** -- `2.0.0_SA_COO~MI`'s `f1r.AC2.sh` evaluates the locals
   through `terraform console`. Run before the fix it enumerated the comprehension as holding **7** keys:
   the 5 platinum keys **plus exactly `bd_silver_allocations` and `bd_silver_unrealized`**. So the count
   is confirmed from the evaluated locals, not only from parsing the YAML.

**THE REMEDY WAS RULED ELSEWHERE AND CARRIED HERE.** This seat proposed no fix: the two candidates
differ in MEANING -- a `try()`/`can()` default silently drops two tables from the alarm's served-key
coverage, which is a freshness-coverage decision rather than a syntax fix. `2.0.0_SA_COO~MI` ruled it as
row `NFRA_MCPINDEX-Z-S96` @`c5e22ccb72`; amendment **A6-r6** @`59d56f3848` added `bd-served-vintage-alarm.tf`
to this order's `<paths>` and new **step 1a** to land it, because `NFRA_MCPINDEX` had no open slot.

**STEP 1A, AS EXECUTED.** One clause of the `if`, committed ALONE at `a18b96fd5d`:

```
-    if try(e.freshness_basis, "") == "trading-day-frontier"
+    if try(e.freshness_basis, "") == "trading-day-frontier" && can(e.as_of_field) && can(e.frontier_page_trading_days)
```

Diffstat `1 file changed, 1 insertion(+), 1 deletion(-)`. Nothing else in that file moved and the YAML is
untouched (`git status -- data/` empty), both of which step 1a requires. The anchor was matched exactly
once by a non-shell writer that refuses to proceed otherwise -- a clause matching twice would have
silently edited the wrong comprehension. `fmt -check` clean on that file alone.

**`2.0.0_SA_COO~MI`'S TWO CHECKS, RUN BEFORE AND AFTER**, because a check that only ever ran after the
fix cannot distinguish a working recognizer from one that always passes:

```
BEFORE (at HEAD, the negative control)
  f1r.AC1.sh  init rc=0; plan rc=1; Unsupported attribute=4; Error lines=4; plan lines=28     RESULT: FAIL
  f1r.AC2.sh  keys = the 5 platinum keys PLUS bd_silver_allocations, bd_silver_unrealized      RESULT: FAIL

AFTER
  f1r.AC1.sh  init rc=0; plan rc=0; Unsupported attribute=0; Error lines=0; plan lines=248
              "No changes. Your infrastructure matches the configuration."                     RESULT: PASS
  f1r.AC2.sh  keys == want, exactly the 5 daily platinum keys                                  RESULT: PASS
```

**AC1's AFTER line also settles the only thing the guard itself could have broken:** the plan reads
`No changes`, so the guard's own delta is **ZERO** and nothing consumes those locals -- which is what
~MI's ruling asserted (the served-vintage-alarm stack was destroyed 2026-07-17) and is now measured here
rather than inherited.

## 5. THE TAG-AUTHORIZATION READ -- and the one live instance that had to be chased

`.tools/comp-tagauthz check --default-tags-tree infra/aws/terraform/bd-pipeline --from-plan <saved plan>`
now runs in **MODE: GATE** (a real plan exists) and exits **rc=0**, scoped to **0 candidate resources**:

```
MODE: GATE. Scoped to 0 candidate resource(s) this tree would manage.
RESULT: none of the 0 candidate(s) carries a tag that infra/aws/terraform/bd-pipeline's default_tags
        ['Environment', 'ManagedBy', 'Project', 'System'] would overwrite.
```

**That is a pass over an EMPTY DENOMINATOR and by itself says nothing about either role.** Recording the
rc without the denominator would be the bare zero reading as "no problem exists".

**ON THE FIRST PASS, WITH NO PLAN TO SUPPLY, THE SAME TOOL RAN IN ADVISORY MODE AND SURFACED A LIVE
INSTANCE -- AND THAT HAD TO BE CHASED RATHER THAN WAVED AWAY:**

```
[TAG-AUTHORIZED] i-0643a5bee8a8feabf (stopped)
    System=CottonwoodPipeline  grants access via role/cot-bd-session-trigger-lambda-role:inline:cot-bd-session-trigger-policy  <-- this tree's default_tags WOULD OVERWRITE THIS
```

That is a real conditional grant: `System=CottonwoodPipeline` authorizes `ec2:StartInstances` and
`ssm:SendCommand` for the Cottonwood session trigger, and this tree's `default_tags` writes
`System=BDPipeline`. The tool states its own limit -- "a tree only endangers a resource it actually
MANAGES", and in ADVISORY mode it lists the account's tag-authorized instances, not this tree's. So:

**MEASURED, from the module's own state, with a positive control:**

```
bd-pipeline state: 223 entries, 7 of them aws_instance --
  bd_allocations i-0800437d1dbb0b5cc   bd_assets i-0e6f6dc014fdcf1cd   bd_fees i-0868fc7e7ebec26f2
  bd_gold_detail_generator i-074bfc40ee049dc62   bd_gold_layer_runner i-01003b035d2988dfb
  bd_gold_qa_runner i-0090b823a4a0997e3   bd_transactions i-00c7568bc510f7423

matches of i-0643a5bee8a8feabf among the 7:  0
positive control (the same comparison against an id known to be in the set):  1
```

The control matters: a loop that can never match reads `0` identically to a true absence. It matched a
known id once, so the zero is a measurement. `i-0643a5bee8a8feabf` is `cot-exporter`, a Cottonwood
instance (`describe-instances`: `Name=cot-exporter`, `System=CottonwoodPipeline`,
`Purpose=BDSessionRefreshAndBronzeIngest`), and **`bd-pipeline` does not manage it**.

**TWO INDEPENDENT INSTRUMENTS NOW AGREE ON THAT, which is why it is settled rather than argued:** the
hand measurement above (0 of 7 managed instances), and the tool's own GATE-mode denominator once a plan
existed (0 candidate resources this tree would manage). The advisory is a false alarm **for this tree**.

**And for THIS CELL the question is narrower still, which is the part that bears on the pair.** This
cell adopts two **IAM roles**. The account sweep behind the collision -- `iam
get-account-authorization-details` over **301 roles, 78 local+attached policies, 9 users, 2 groups**;
SCPs NOT APPLICABLE, the account is not in an AWS Organization, stated not implied -- reads **0
`aws:PrincipalTag/*` conditions account-wide**, and the only two non-AWS tag conditions are both
`aws:ResourceTag` scoped to EC2 instances and SSM documents (`System = CottonwoodPipeline`;
`Project = NFRA_WEBSITE`). An IAM role is neither, and the values this module writes
(`Project = OpalPortal`, `System = BDPipeline`) match neither condition's required value. **So the four
tags this cell's apply would add to these two roles can neither widen nor narrow any authorization
decision in this account**, on the same two independent grounds as Families B and E.

> **Recorded as a limit, not resolved:** `tag-conditioned statements found: 9 (4 ours, 5 AWS
> service-linked)` is comp-tagauthz's own count, where this seat's hand sweep of the same API response
> in w-1 PHASE A resolved to 4 distinct `(policy, condition-kind, key)` triples. The two scans dedupe and
> attribute differently; not re-derived. The conclusion rests on the *scoping* of the conditions, quoted
> above, not on either count.

## 6. SURFACED, NOT MINE, AND NOT FIXED

`terraform fmt -check` fails in this module on a file this cell did not write:

```
infra/aws/terraform/bd-pipeline: (pre-existing fmt failures; this cell's zz_adopt_family_a.tf is clean)
```

This cell's file is fmt-clean, checked **per file** so the verdict is about my bytes and not the
directory's. Pre-existing files are outside this order's `<paths>` and formatting them would be a rider
on a WORLD cell, so they are surfaced rather than touched. Worth knowing before PHASE B, because a
module-wide `fmt -check` in a later gate will fail on them and the cause will not be the adoption.

## 7. STATE OF THE WRITE SURFACE AT THE END OF PHASE A

- `infra/aws/terraform/bd-pipeline/zz_adopt_family_a.tf.proposed` -- committed, **inert** (terraform
  loads `.tf` and `.tf.json` only). Two `aws_iam_role` blocks and two `import` blocks.
  `inline_policy` and `managed_policy_arns` ABSENT from both; `description` additionally absent from
  row 2, as live. AC1's grep returns **0**.
- `infra/aws/terraform/bd-pipeline/bd-served-vintage-alarm.tf` -- **the step 1a guard, committed ALONE**
  at `a18b96fd5d`. One clause, 1 insertion / 1 deletion, zero plan delta.
- **Labels fully namespaced, collision question MEASURED:** `resource "aws_iam_role" "` matches **270
  times across 833 files** scanned under `infra/aws/terraform`, and `bd_merge_daily_lambda_role` /
  `bd_pipeline_task_role` match **0 of them**. Round 2's battery recorded short labels
  (`orchestrator`, `scheduler`) reused across three modules and silently mis-linking their inline
  policies, which is why this is checked rather than trusted.
- **Neither role is declared anywhere in Terraform at the cut:** a measured **0 hits across 833 files**
  for both names together. The denominator is printed because a bare zero reads as "the term does not
  exist"; 70 binary and 9 ephemeral-floor files in scope were not searched and the zero does not cover
  them. (The first attempt at this census used `\|`, which python `re` reads as a LITERAL -- a zero that
  was the pattern, not the world. comp-find's own warning caught it; re-run with a bare pipe.)
- `infra/aws/terraform/bd-pipeline/zz_adopt_family_a.tf` -- **REMOVED.** The `.tf` copy existed only for
  the plan runs and is not committed. The module's tracked `.tf` set is unchanged apart from step 1a's
  one-clause edit.
- No deploy-ledger entry opened. PHASE B opens `iamroles-r6-family-a` first.
- **Nothing applied. No tag, policy, trust relationship, instance or Lambda touched.**

## 8. WHAT PHASE B INHERITS

1. **The plan to match is MEASURED, not predicted:** `2 to import, 0 to add, 2 to change, 0 to destroy`,
   the two changes being `tags_all` alone, four keys each including `System = BDPipeline`. The
   `-target` list is TWO addresses: `aws_iam_role.bd_merge_daily_lambda_role` and
   `aws_iam_role.bd_pipeline_task_role`.
2. **Two stop conditions, both already satisfied at plan time and both to be re-verified live after the
   apply:** row 2's `assume_role_policy` must show NO change (the `ecs-tasks.amazonaws.com` principal),
   and both roles' single inline policy must still be attached (0 detachments).
3. **The order of acts is ruled** -- A4-r6 @`7af7a24e9f` and A5-r6 @`f37fb5892d`: commit the renamed
   `.tf` FIRST on the worktree branch, carrying only that file and the placement override's audit row,
   with `# naming-place-override:` naming both roles, their live `CreateDate`s and row `Z-S25`; **take
   NO author override** (the audit row's path is lane ANY @`b7c27ef5b0`, which closed `Z-S26`); then the
   `-target` apply; then the drain in the same session; then an untargeted shared-tree plan recorded at
   `0 to destroy`. Ledger, proof and `POST_APPLY_family_a.md` land in separate commits without the
   placement override.
4. **Both roles keep their live names** -- Rule 30's existing-pipeline non-application, ruled by the
   issuer; the `Z-S25` gate fix is `1.0.0_SA_CTO~Z`'s and is parked at dell1.
5. **`Z-S29` is UNBLOCKED** by step 1a, and this survey's `PLAN:` line is real. The pair can be written.

**PHASE A ends here, per the order's step 3.**
