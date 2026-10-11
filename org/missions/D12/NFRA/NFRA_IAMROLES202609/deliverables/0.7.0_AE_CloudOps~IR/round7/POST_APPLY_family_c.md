# POST_APPLY -- Family C, NFRA_IAMROLES202609.TO-IAM-x-1 PHASE B -- ROW 14 ONLY

**Cell:** IAM-x-1 (round 7, FWD-4 enrichment; round-6 analysis E1)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z`
**Authority:** GO `2.0.0_SA_COO~ZI` msg 33208, **ROW 14 ONLY**. Halves: COO @`af187b410b`, CTO @`1e7ff2decd`.
Home ruled by A1-r7 @`af187b410b`. Order of acts per A4-r6 @`7af7a24e9f` / A5-r6 @`f37fb5892d`.
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x1b` @`7a72582e79`,
Terraform v1.15.8, provider `hashicorp/aws v5.100.0`.

> **THIS ORDER IS NOT COMPLETE AND MUST NOT BE FLIPPED. AC1 expects `files=2` and AC2 expects 2
> `POST-APPLY-PLAN` lines; this file carries ONE, because only row 14 was authorised.** Row 6
> (`lambda-ec2-runtime-monitor-role`, home `shared-infra`) remains HELD: that module cannot init or plan
> at all, routed to `1.0.0_SA_CTO~Z` (survey section 4). Row 14 was explicitly released from waiting on it.

---

## 1. THE REQUIRED LINE -- ONE OF TWO

```
POST-APPLY-PLAN: infra/aws/terraform/market-overview: 0 to add, 0 to change, 0 to destroy
```

That is the TARGETED re-plan. Terraform renders a clean plan as a sentence, so its verbatim output is
quoted beside the canonical line rather than silently reshaped:

```
$ terraform -chdir=infra/aws/terraform/market-overview plan ... -target=aws_iam_role.sentiment_query_api_role
No changes. Your infrastructure matches the configuration.
```

**OWED, NOT PRESENT:** `POST-APPLY-PLAN: infra/aws/terraform/shared-infra: ...`. It cannot exist until
`shared-infra` plans. AC2 therefore reads **1**, and that is the correct reading of a half-authorised cell,
not a defect in this record.

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

## 8. THE LEDGER, AND WHAT THIS ORDER STILL OWES

`iamroles-r7-family-c-market-overview` opened BEFORE the apply (3 legs: TF, MANAGED, REPLAN) and closed
after this record. **Row 6's entry, `iamroles-r7-family-c-shared-infra`, was never opened** -- correctly,
since its apply is not authorised and NEVER-2 opens an entry at the start of an act, not in advance of one.

**Still owed on this order, none of it this lane's to clear:**
1. `shared-infra` must plan before row 6's PHASE B exists at all (CTO~Z).
2. Then row 6's own never-widen pair.
3. Only then do AC1 read `files=2` and AC2 read 2, and only then can `<status>` flip.

**PHASE B for row 14 ends here.**
