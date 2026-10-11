# POST_APPLY -- Family C, NFRA_IAMROLES202609.TO-IAM-x-1 PHASE B -- ROW 14 ONLY

**Cell:** IAM-x-1 (round 7, FWD-4 enrichment; round-6 analysis E1)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z`
**Authority:** GO `2.0.0_SA_COO~ZI` msg 33208, **ROW 14 ONLY**. Halves: COO @`af187b410b`, CTO @`1e7ff2decd`.
Home ruled by A1-r7 @`af187b410b`. Order of acts per A4-r6 @`7af7a24e9f` / A5-r6 @`f37fb5892d`.
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x1b` @`7a72582e79`,
Terraform v1.15.8, provider `hashicorp/aws v5.100.0`.

> **BOTH ROWS ARE NOW APPLIED AND THIS ORDER IS COMPLETE.** Row 14 landed first
> (`market-overview`, 2026-10-11 ~06:0xZ); row 6 (`lambda-ec2-runtime-monitor-role`, `shared-infra`)
> landed at ~09:33Z once its blocker cleared, under GO msg 33247 and halves COO @`4309620d05` /
> CTO @`85cbea7549`. AC1 now reads `files=2` then `0`, AC2 reads **2**, AC3 reads `open=0 closed=2`.
>
> **WHAT CHANGED BETWEEN THE TWO APPLIES IS NOT THIS LANE'S WORK AND SHOULD BE READ THAT WAY:**
> `shared-infra` could not init or plan at all at PHASE A -- a fail-closed `one()` guard at
> `s3-lgic-firm-buckets.tf:197` -- and `ADVI_COTBKF` @`8c6fc7652a` DISPOSED it (an explicit per-row
> field selecting `cottonwood`) rather than widening it, which is what survey section 4 asked for.
> The re-survey is section 4a of `PLAN_SURVEY_family_c.md`; the row is `Z-S38`.

---

## 1. THE REQUIRED LINE -- ONE OF TWO

```
POST-APPLY-PLAN: infra/aws/terraform/market-overview: 0 to add, 0 to change, 0 to destroy
POST-APPLY-PLAN: infra/aws/terraform/shared-infra: 0 to add, 0 to change, 0 to destroy
```

That is the TARGETED re-plan. Terraform renders a clean plan as a sentence, so its verbatim output is
quoted beside the canonical line rather than silently reshaped:

```
$ terraform -chdir=infra/aws/terraform/market-overview plan ... -target=aws_iam_role.sentiment_query_api_role
No changes. Your infrastructure matches the configuration.
```

**BOTH LINES ARE NOW PRESENT, SO AC2 READS 2.** The second one is row 6's, added 2026-10-11 ~09:4xZ.
Terraform renders both clean plans as the same sentence, quoted verbatim beside each canonical line
rather than silently reshaped:

```
$ terraform -chdir=infra/aws/terraform/shared-infra plan ... -target=aws_iam_role.lambda_ec2_runtime_monitor_role
No changes. Your infrastructure matches the configuration.
```

## 2. THE UNTARGETED MODULE PLAN -- and here "unchanged" is the test, not "clean"

```
UNTARGETED-MODULE-PLAN: infra/aws/terraform/market-overview: Plan: 4 to add, 0 to change, 0 to destroy.
```

**This module was NOT at zero drift before the act and is not after it, and that is the expected result.**
PHASE A's negative control read the same `4 to add` (survey section 5): an S3 bucket the module manages,
`market_data_v2`, has been deleted out of band, and the four adds would recreate it with its
`public_access_block`, `server_side_encryption_configuration` and `versioning`.

So the REPLAN leg was written to require the drift **UNCHANGED, not absent** -- `4 to add, 0 to destroy`
before and after. A record that reported "No changes" here would mean this act had absorbed four
resources nobody signed.

**The pair named those four explicitly as NOT SIGNED, and the targeted plan contained ZERO
`market_data_v2` addresses** -- measured by filtering every `resource_change` address, not by reading the
summary. That is why `-target` is load-bearing in this module rather than belt-and-braces as it was in
round 6's clean modules.

## 3. THE PLAN THAT WAS APPLIED, GRADED BEFORE THE APPLY

Saved with `-out`; the apply ran that file. Graded from `terraform show -json` per `resource_change`,
because `1 to import, 0 to add, 1 to change, 0 to destroy` is exactly what a trust-policy rewrite would
also print.

| graded property | measured |
|---|---|
| `resource_changes` total | 1 |
| non-no-op | 1 -- `aws_iam_role.sentiment_query_api_role`, `['update']`, importing `sentiment_query_api-role` |
| non-no-op addresses that are NOT the adopted role | **`[]`** |
| **`market_data_v2` addresses present at all** | **0** |
| attributes that differ | **1** (`tags_all`) |
| `tags_all` delta | `{}` -> `Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=MarketOverview` |
| exact match to the 4 signed keys | **True**, count 4 |
| `assume_role_policy` / `inline_policy` / `managed_policy_arns` / `description` | unchanged |
| destroys | 0 |

Apply verbatim: `Apply complete! Resources: 1 imported, 0 added, 1 changed, 0 destroyed.`
`safe-apply` gates: `comp-tagauthz` PASSED (over 0 candidate resources -- an empty denominator, recorded
with it); `tombstone-gate` CLEAN.

## 4. THE CTO'S BYTE CONDITION -- met, after I had broken it myself

The CTO half conditions the apply on: *"the .tf committed into market-overview must EQUAL the draft blob
`01c492fb` at @`a921f7130f` (git hash-object to check)"*.

```
required : 01c492fbf4e21702df67b8163d313289eb54b80a
committed: 01c492fbf4e21702df67b8163d313289eb54b80a   (git hash-object, at 7a72582e79)   MET
```

**I had broken it, and the way I handled that is the part worth recording.** Moving the draft into the
module at `213ee20553` I re-pointed its header -- correct as prose, since the old header said the file
lived in the deliverables directory "until the issuer amends its module in", which the ruling had just
made false. But it changed the bytes: the file read `b85758d5`.

A diff of **non-comment lines was empty** -- the resource text the pair reviewed was never touched. **I did
not treat that as satisfying the condition.** The condition is byte equality, and the point of such a
condition is that the actor does not get to choose which bytes matter; "only comments differ" is precisely
the argument it exists to refuse. The draft bytes were restored verbatim from the pin at `43e9f30e05`, and
the header correction was re-ordered to land AFTER the apply, where it changes no plan -- the same sequence
w-1 used (pure rename at `c942b684bc`, header corrected at `b41c3a9e29` with a measured zero plan delta).

## 5. NO OVERRIDE OF ANY KIND WAS TAKEN -- a first for this program

Every previous adoption in this project needed either the audited placement override (w-1, w-3) or an R20
declared exception (w-2, after Andrew's word). **Row 14 needed neither.** `4.0.0_SA_CRO~Z` added
`sentiment` to `infra/logic/registry/systems.json` `refused_keys.generic_noun` (confirmed at HEAD and in
the worktree the grade ran in: 80 entries, `sentiment` present), which turned the HOLE into a FIX
placement; and the name then graded **EXISTING**:

```
NAMING OUT-OF-PATTERN .../zz_adopt_family_c_row14.tf:69  sentiment_query_api-role -> {system}-sentiment-query-api-role
  why: EXISTING, touched, and OUT-OF-PATTERN as IAM_ROLE: WARN
(and the same at :100)        NAMING-GATE: WARN 2 graded
```

### 5a. THREE DRY-GRADE READINGS, two of them vacuous -- and that is the finding

The issuer asked for the dry-grade to be re-run before committing (msg 33211). Doing so exposed a
structural limit of the probe itself:

| reading | input | verdict | sound? |
|---|---|---|---|
| 1 | `git diff --cached -M` -- the **R100 rename** diff | `DENOMINATOR: 0 path(s)`, `PASS 0 graded` | **NO -- VACUOUS** |
| 2 | `git diff --cached --no-renames` -- 11291 bytes, 2 files, 4 name-carrying added lines | `WARN 2 graded`, EXISTING | yes |
| 3 | the commit itself (`safe-commit`, which computes its own diff) | `WARN 2 graded`, EXISTING | **authoritative** |

**`naming-gate.py --diff` GRADES ADDED LINES, AND A PURE RENAME ADDS NONE -- so the dry-grade is
STRUCTURALLY BLIND to exactly the act step 5 performs.** Reading 1 would have reported a pass that graded
nothing, on the one commit shape this cell is required to make. `--no-renames` is what makes the names
visible, because it renders the file as a deletion plus an addition.

**My own pre-check is what caught it**, and only because x-1 PHASE A had already taught me the lesson the
hard way: I print the diff's byte count, file count and name-carrying added-line count **before** reading
any verdict. Reading 1 printed `329 bytes, 0 files, 0 name-carrying lines`, so its `PASS` was discarded
unread. (In PHASE A the same trap caught me going the other way: I staged with `git add -N`, took
`git diff --cached`, got a 0-byte diff, and my own `||` fallback never fired because the redirect
succeeded.)

**Note also that readings 2 and 3 agree here but need not in general:** in round 6 a pure R100 rename was
graded **NEW and REFUSED** by `safe-commit` (row `Z-S34`), where a `-M` dry-grade would have seen nothing
at all. The commit is the only authoritative grade; the dry-grade is a cheap warning, and on a rename it
is cheap and blind.

## 6. BRANCH A, READ FROM THE WORLD

| read | result |
|---|---|
| `list-role-tags` | **exactly 4**: `Environment=Production`, `ManagedBy=Terraform`, `Project=OpalPortal`, `System=MarketOverview` |
| **STOP CONDITION -- `list-attached-role-policies`** | **1 -- `AWSLambdaBasicExecutionRole`**, exactly as before |
| `list-role-policies` | `['DynamoDBAccess']` -- unchanged |
| `get-role` trust / description / path / max session | `lambda.amazonaws.com` ; **`None`, still absent** ; `/` ; `3600` -- all unchanged |

**The omission rule held in the world on a role that carries a managed attachment** -- the third such role
in the program. Setting `managed_policy_arns`, even to `[]`, would have detached
`AWSLambdaBasicExecutionRole` and with it this role's CloudWatch Logs access.

**No permission moved.** Four tags added to a role that carried none; the survey named all four before
either half was signed.

## 7. ROLLBACK, AVAILABLE AND UNUSED

`terraform state rm aws_iam_role.sentiment_query_api_role` (state only, no AWS change), plus
`aws iam untag-role --tag-keys Environment ManagedBy Project System`, plus reverting the rename. Not
needed, not run.

## 7a. ROW 6 -- `lambda-ec2-runtime-monitor-role` ADOPTED INTO `shared-infra`

**Authority:** GO `2.0.0_SA_COO~ZI` msg 33247. Halves: COO @`4309620d05`, CTO @`85cbea7549`, both read as
FILES at HEAD before anything moved, beside a positive control proving an absent half reads absent.
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x1row6`.

### 7a.1 THE BYTE CONDITION, MET WITHOUT BREAKING IT THIS TIME

The CTO half names blob `0a0a37cf`; the COO half pins the declaration @`a921f7130f`. All four readings agree:

```
worktree before rename : 0a0a37cfdc556f3ea5ab298ed51d5af2b69ade60
at a921f7130f          : 0a0a37cfdc556f3ea5ab298ed51d5af2b69ade60
at my HEAD             : 0a0a37cfdc556f3ea5ab298ed51d5af2b69ade60
worktree after rename  : 0a0a37cfdc556f3ea5ab298ed51d5af2b69ade60
```

**The rename was pure and I did NOT re-point the header**, even though it still reads "PROPOSED TEXT -- NOT
LIVE. DO NOT RENAME THIS FILE TO `.tf`", which is now false. Row 14 is why (section 4): correcting that
header as prose is exactly what broke its byte equality. The header correction lands after the apply, where
it changes no plan -- the same ordering w-1 used.

Committed BEFORE the import at `fc621b99bb`, per A4-r6 and row `Z-S27`.

### 7a.2 THE PLAN THAT WAS APPLIED, GRADED BEFORE THE APPLY

Saved with `-out`; the apply ran that file. Graded from `terraform show -json` per `resource_change` and per
attribute, because `1 to import, 0 to add, 1 to change, 0 to destroy` is exactly what a trust-policy rewrite
would also print.

| graded property | measured |
|---|---|
| `resource_changes` / non-no-op | 1 / 1 |
| non-no-op addresses that are NOT the adopted role | **`[]`** |
| **`restricted_breakglass` addresses present at all** | **0** (the pair: ANY occurrence is NOT SIGNED) |
| destroys | **0** |
| attributes that differ | **1** (`tags_all`) |
| `tags_all` delta | `{}` -> `Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=SharedInfra` |
| exact equality to the 4 signed keys / key count | **True** / **4** (a fifth key is NOT SIGNED) |
| `assume_role_policy` / `inline_policy` / `managed_policy_arns` / `description` / `path` / `max_session_duration` / `name` | all **byte-identical** |

Apply verbatim: `Apply complete! Resources: 1 imported, 0 added, 1 changed, 0 destroyed.`

### 7a.3 `-target` WAS LOAD-BEARING HERE, AND FOR A SHARPER REASON THAN IN `market-overview`

The negative control (declaration held out) reads `Plan: 2 to add, 0 to change, 0 to destroy`:
`aws_iam_role.restricted_breakglass` and `aws_iam_role_policy.restricted_breakglass`, `ADVI_COTBKF`'s
declared-but-never-applied pair. **An untargeted apply here would CREATE AN IAM ROLE AND ITS POLICY** --
the very class of object this project exists to bring under custody. The COO half names both as NOT SIGNED,
and the targeted plan contains **zero** of their addresses, measured by filtering every `resource_change`
address rather than by reading the summary.

In `market-overview` the unsigned drift was four S3 resources; here it is IAM. Same mechanism, higher stakes.

### 7a.4 BRANCH A, READ FROM THE WORLD

| read | before | after |
|---|---|---|
| `list-role-tags` | `[]` | **exactly 4**: `Environment=Production`, `ManagedBy=Terraform`, `Project=OpalPortal`, `System=SharedInfra` |
| **STOP CONDITION -- `list-attached-role-policies`** | `['AWSLambdaBasicExecutionRole']` | **`['AWSLambdaBasicExecutionRole']`, still exactly 1** |
| `list-role-policies` | `['EC2RuntimeMonitorPolicy']` | **unchanged** |
| trust / path / description / max session | `lambda.amazonaws.com` / `/` / `null` / `3600` | **all unchanged** |

**The omission rule held in the world on the SECOND role in this program carrying a managed attachment**
(row 11 was the first). Setting `managed_policy_arns`, even to `[]`, would have detached
`AWSLambdaBasicExecutionRole` and with it this role's CloudWatch Logs access. **No permission moved.**

### 7a.5 THE CTO'S INVOCATION CONDITION -- met in substance by a STRONGER oracle, and the substitution is stated

The CTO half conditions on: *"the role's `RoleLastUsed` must advance past the apply time within the
function's next scheduled run. If it does not, a row is filed and nothing is rolled back blind."*

The consumer chain was read from the **served graph**, not guessed -- 6 nodes across 2892 scanned: Lambda
`ec2-runtime-monitor`, EventBridge rule `ec2-runtime-monitor-15min` (a 15-minute schedule), its log group,
the role, its inline policy and SNS topic `ec2-long-running-alerts`.

**THE FUNCTION RAN AFTER THE APPLY AND EXERCISED THE ROLE'S PERMISSIONS, not merely its trust:**

```
START RequestId: 91f03cbf-38e1-4b14-a357-5b60a0375812      epoch 1791711388178 = 2026-10-11T09:36:28Z
EC2 Runtime Monitor - Checking instances at 2026-10-11T09:36:28
bd-allocation: stopped (not running) / bd-transactions: stopped (not running) / bd-gold-layer-runner: stopped (not running)
  -> all instances within acceptable runtime limits
```

against an apply that completed ~`09:33Z`. **Enumerating those three instances REQUIRES
`ec2:DescribeInstances`, which is exactly what `EC2RuntimeMonitorPolicy` grants**, so the role's inline
permissions demonstrably still work. Errors in the window: **0**, over
`?ERROR ?Error ?Traceback ?AccessDenied ?Task timed out` -- and what would have made that non-zero is
precisely an `AccessDenied` had the apply disturbed the policy, so the zero carries its cause.

> **I AM NOT CLAIMING THE LITERAL CLAUSE IS SATISFIED YET.** `RoleLastUsed` reads
> **`2026-10-11T09:21:36Z`**, still BEFORE the apply, because **IAM last-used data is documented to lag by
> up to four hours**. The log plane is near-real-time and proves the stronger fact the clause exists to
> establish; `RoleLastUsed` is expected to catch up. Recording both readings, and which one I am leaning
> on, is the honest form -- quietly swapping the oracle would have read as the condition being met on its
> own terms. Nothing was rolled back, which is what the half directs on a non-advance.

### 7a.6 ROLLBACK, AVAILABLE AND UNUSED

`terraform state rm aws_iam_role.lambda_ec2_runtime_monitor_role` (state only, no AWS change), plus
`aws iam untag-role --tag-keys Environment ManagedBy Project System`, plus reverting the rename. Not needed,
not run.

### 7a.7 NO OVERRIDE OF ANY KIND -- the second such cell in this program

`NAMING-GATE: PASS 2 graded`, rc=0, both rows `NO-SYSTEM-ASKED as IAM_ROLE`. The canonical form equals the
live name, so neither the placement override nor an R20 exception is owed. Graded on the `.tf` form with
`--no-renames` per the COO half's own instruction, and the verdict read only **after** the staged diff was
confirmed non-empty (12785 bytes, 1 file, 3 name-carrying added lines). COVERAGE reported 1 blind path --
the `.tf.proposed` deletion side, whose extension is outside the gate's graded set; the `.tf` that matters
was graded, and the commit's own authoritative run agreed at `PASS 2 graded`.

## 8. THE LEDGER, AND WHAT THIS ORDER STILL OWES

`iamroles-r7-family-c-market-overview` opened BEFORE the apply (3 legs: TF, MANAGED, REPLAN) and closed
after this record. **Row 6's entry, `iamroles-r7-family-c-shared-infra`, was never opened** -- correctly,
since its apply is not authorised and NEVER-2 opens an entry at the start of an act, not in advance of one.

**ALL THREE OF THOSE ARE NOW DISCHARGED, and none of the first two by this lane:**
1. `shared-infra` plans -- `ADVI_COTBKF` @`8c6fc7652a` (survey section 4a, row `Z-S38`).
2. Row 6's never-widen pair is signed -- COO @`4309620d05`, CTO @`85cbea7549`.
3. AC1 reads `files=2` then `0`, AC2 reads **2**, AC3 reads `open=0 closed=2`.

Row 6's own entry, `iamroles-r7-family-c-shared-infra`, was opened BEFORE its apply with **FOUR**
legs rather than three -- TF, MANAGED, REPLAN and **INVOCATION**, the fourth being the CTO half's own
in-use condition (section 7a.5). All four closed on live reads.

**PHASE B FOR BOTH ROWS ENDS HERE, AND THIS ORDER IS COMPLETE.**
