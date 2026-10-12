# IAM-z-3 PHASE A -- market_data_v2: the declaration and the Allow

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-3` - **Risk:** WORLD
**Read time:** 2026-10-12 00:5xZ - 01:3xZ. Every live value below was measured in that window.
**Standing (Z-S40):** this survey names its read time; the act re-reads its baseline before it applies.
**Worktree:** `C:/tmp/iam-r9-z3`, branch `wk-iamroles-r9-z3`, cut from `box/sitez` HEAD (verified equal).
**Authority:** the CTO's E3 ruling authorises TF-debt A7, which this lane declined in July as unauthorized
(row Z-S43).

---

## 1. THE STATE READ, AND THE ANSWER TO THE CELL'S PIVOTAL QUESTION

The cell asks: *do the four `market_data_v2` addresses exist in STATE? If they do, removing the
declaration plans a DESTROY of an absent bucket: say what the plan does with it, verbatim.*

**They do exist in state -- and the plan does NOT plan a destroy.**

`terraform state list` in `market-overview` (**55** addresses total) holds all four:

```
aws_s3_bucket.market_data_v2
aws_s3_bucket_public_access_block.market_data_v2
aws_s3_bucket_server_side_encryption_configuration.market_data_v2
aws_s3_bucket_versioning.market_data_v2
```

The bucket is absent in the world: `s3api get-bucket-location --bucket opal-market-data-v2` ->
**rc=254, code `NoSuchBucket`**; control `opal-data-portal-v2` -> **rc=0** in the same run.

**What the plan actually does with them, read out of `show -json` rather than inferred:**

| where the four addresses appear | count |
|---|---|
| stored `state list` (unrefreshed) | **4** |
| the plan's `prior_state` (post-refresh) | **0** |
| the plan's `configuration` | **0** (my edit removed them) |
| the plan's `resource_changes` | **0** -- no create, no destroy, not even a no-op |
| the plan's **`resource_drift`** | **4**, each `actions=["delete"]`, `after=None` |

So the sequence is: the refresh reads the world, finds all four gone, and records them in
**`resource_drift` as `delete`** -- Terraform's own notation for *this was in state and has vanished*.
Because the configuration no longer declares them either, there is nothing left to create and nothing to
destroy, and they drop out of `resource_changes` entirely. **The apply will prune four stale state
entries and make no API call about them.** The plan's own summary line, verbatim:

```
PLAN: market-overview: Plan: 0 to add, 1 to change, 0 to destroy.
```

> **This is the exact inverse of round 7's reading, and that is the point of the act.** Round 7 recorded
> market-overview as **"4 to add"** -- Terraform wanting to *resurrect* a bucket Andrew ruled deleted
> (row Z-S43), which `safe-apply`'s tombstone-gate would have refused. Removing the declaration turns
> those 4 adds into **0 adds and 0 destroys**. The hazard is not traded for a different hazard; it is
> closed.

---

## 2. BOTH PLANS, GRADED PER ATTRIBUTE (step 2)

### UNTARGETED (the one that matters here)

```
PLAN: market-overview: Plan: 0 to add, 1 to change, 0 to destroy.
  43 resource_changes   histogram {no-op: 42, update: 1}
  to add 0 / to change 1 / to destroy 0
  market_data_v2 in resource_changes: 0
  resource_drift: 5 entries -- the 4 market_data_v2 (delete) + aws_iam_role.market_update_lambda_role (see section 4)
  applyable=True complete=True errored=False

  update aws_iam_role_policy.market_data_generator_permissions
    attributes that move: 1 -> ['policy']        <- only the document
    statements 5 -> 5                            <- none added, none dropped
    ARNs 11 -> 9   REMOVED 2, ADDED 0
      - [S3MarketDataWrite] arn:aws:s3:::opal-market-data-v2/*   DEAD
      - [S3MarketDataList]  arn:aws:s3:::opal-market-data-v2     DEAD
    Sids before: ['S3MarketDataWrite','S3MarketDataList','DynamoDBMarketData','CloudFrontInvalidation','SecretsExternalAPIs']
    Sids after:  ['S3MarketDataWrite','S3MarketDataList','DynamoDBMarketData','CloudFrontInvalidation','SecretsExternalAPIs']
    actions changed on any surviving statement: NONE
```

### TARGETED, beside it

```
PLAN: market-overview -target=aws_iam_role_policy.market_data_generator_permissions:
      Plan: 0 to add, 1 to change, 0 to destroy.
  2 resource_changes   histogram {no-op: 1, update: 1}
  update aws_iam_role_policy.market_data_generator_permissions
```

**This matches the cell's expected shape exactly** -- *"the four adds vanish; the role policy is 1 change
losing exactly the two ARNs; nothing else"* -- so there is no other planned change to name and **no reason
to target**. The untargeted plan is the signed shape. I ran the targeted one anyway because the cell asks
for both, and it confirms the same single change in isolation.

The four `opal-data-portal-v2` ARNs in `S3MarketDataWrite`, the one in `S3MarketDataList`, and all five
statements' actions are untouched. `aws_iam_role.market_data_generator` is **not** in the change set: the
role itself stays, per BOUNDS.

### Rollback

`.../market_data_v2/ROLLBACK_market-data-generator-permissions.json`, 1961 bytes, captured live:
**5 statements, 11 ARNs**, of which exactly **2** name `opal-market-data-v2`. Captured with
`--query PolicyDocument` and passed through a **shape guard** that refuses a wrapped
`{RoleName,PolicyName,PolicyDocument}` response and refuses zero statements in a live policy -- the guard
exists because that exact wrapped shape produced a confident, vacuous verdict in z-1 an hour earlier.

---

## 3. THE EDIT

```
2 files changed, 5 insertions(+), 30 deletions(-)
  removed resource blocks:    4     (the four market_data_v2 declarations in s3.tf)
  removed arn:aws:s3 lines:   2     (the two dead ARNs in iam_legacy.tf)
  added arn:aws:s3 lines:     0
  added COMMENT lines:        5     (a tombstone note replacing the removed block)
  added NON-comment lines:    0
terraform validate: Success! The configuration is valid.
```

The five added lines are a comment in `s3.tf` recording why the declaration is gone (the ruling, the
tombstone, and that keeping it made every plan want to resurrect the bucket), so a later reader does not
re-add it. **Nothing executable is added.**

`tombstones.json` is **not** touched in PHASE A: the cell has its `declaration_removed` line cite the
apply commit, which does not exist yet.

### An unintended change I made and reverted, stated because it was in the act's diff

While inspecting the formatting I ran `terraform fmt -diff <file>` **without `-check`**. `terraform fmt`
**writes by default** (`-write=false` is what disables it; `-check` is what makes it read-only), so that
command silently re-aligned three lines (`Sid`/`Effect`/`Action` in `S3MarketDataList`) in **both** the
worktree copy and the **shared tree** copy. Consequences and remedy:

- The act's diff briefly contained **3 added non-comment lines** that were a formatting fix, not the act.
  Reverted; the pre-existing deviation is left exactly as HEAD has it. The diff now reads **0** added
  non-comment lines.
- The shared tree's `infra/aws/terraform/market-overview/iam_legacy.tf` was modified outside any act.
  Reverted with `git checkout --` after confirming its diff was *only* that hunk. `git status` under
  `infra/` now shows no modified `.tf` -- only `.terraform.lock.hcl`, which `terraform init` rewrites and
  which was already modified before this session's work began.
- **The plan was re-run after the revert and is byte-for-byte the same verdict** (`0 to add, 1 to change,
  0 to destroy`; 43 changes, 42 no-op; 0 `market_data_v2` in `resource_changes`; 4 in `resource_drift`),
  so the graded plan does not depend on the whitespace.

### A SECOND defect in my own earlier deliverable: two rollbacks were not restorable

Auditing every round-9 rollback document by SHAPE (13 files at the time) found **2 in the WRAPPED
`get-role-policy` response form** -- `{RoleName, PolicyName, PolicyDocument}` -- rather than the policy
document itself. Both were written at 19:21:45Z, by my own earlier capture in this session:

| file | shape then |
|---|---|
| `market_data_v2/ROLLBACK_market-data-generator-lambda-role_market-data-generator-permissions.json` | WRAPPED |
| `schwab/ROLLBACK_bd-exporter-ec2-role_schwab-bucket-access.json` (IAM-z-2's) | WRAPPED |

**A wrapped file is not a rollback.** `put-role-policy --policy-document` takes the document; handed the
envelope it fails, so the artifact whose entire job is to restore a permission could not have restored
it. This is the same shape that produced a vacuous verdict in IAM-z-1 an hour earlier, which is how I
thought to audit for it.

**The control I had run on these files validated the wrong property.** I had proven each rollback *equal
to a fresh re-fetch* (7 of 7, canonical `sort_keys`). That proves the file matches what the API
returns -- and the wrapped form matches what the API returns perfectly. It says nothing about whether the
file matches what the RESTORE INTERFACE accepts, which is the only property a rollback needs. A rollback
must be validated against its CONSUMER, not against its producer.

Re-captured all of them with `--query PolicyDocument`; re-audited: **14 files, 0 WRAPPED, 14 DOCUMENT**.
Both legacy filenames were overwritten in place rather than deleted, so nothing that cites them breaks.
Fixed in the same turn it was found, before any pair read this survey.

The deviation `fmt` wants in this file is **pre-existing**: the *same hunk* is flagged at HEAD in the
shared tree (`@@ -51,9` there, `@@ -50,9` in my worktree -- identical content, shifted one line by the ARN
removal above it). I am not fixing it inside this act, because an unsigned whitespace change in a
never-widen act is exactly the kind of thing a pair should not have to adjudicate.

---

## 4. AN INCIDENTAL DRIFT FINDING: THE OMISSION RULE PREVENTING A SILENT RE-WIDENING

The plan's `resource_drift` carries a **fifth** entry that has nothing to do with my act:

```
aws_iam_role.market_update_lambda_role   actions=update
  inline_policy:        state has 2 policies  ->  LIVE has 3 (extra: market-update-dynamodb-scoped)
  managed_policy_arns:  state has 3           ->  LIVE has 1
      state: market-update-lambda-policy, AmazonDynamoDBFullAccess, AmazonS3FullAccess
      live:  market-update-lambda-policy
```

Someone has detached **`AmazonDynamoDBFullAccess`** and **`AmazonS3FullAccess`** from that role and added
a scoped inline policy (`market-update-dynamodb-scoped`, naming `table/market-updates` and a query-only
grant on `table/opal-news-trending-daily`). That is a least-privilege improvement, and Terraform's state
still carries the two wide attachments.

**And `resource_changes` reads `no-op` for that role, which is the finding.** Terraform is *not* trying
to re-attach the two full-access policies. The reason is THE OMISSION RULE, verified against the
declaration: `resource "aws_iam_role" "market_update_lambda_role"` is 12 lines and declares only `name`,
`path` and `assume_role_policy` -- **`inline_policy` and `managed_policy_arns` are OMITTED.** Both are
Optional+Computed, so with them absent Terraform has nothing to enforce and the live narrowing survives.

> **Had that declaration named `managed_policy_arns`, this act's untargeted apply would have re-attached
> `AmazonS3FullAccess` and `AmazonDynamoDBFullAccess` to a production role** -- a silent privilege
> re-widening, inside an apply whose stated purpose is to *remove* a permission, and one the plan summary
> `0 to add, 1 to change, 0 to destroy` would not have hinted at. It did not happen, and the reason it
> did not is a rule this project already established. Recorded here because a control that is only ever
> observed working is the one people stop believing in.

Out of scope and not acted on: the drift is informational, the role is not in my `<paths>`, and the state
entry will reconcile on whatever apply next touches that role. Named rather than swept.

---

## 5. WHAT PHASE A DID AND DID NOT DO

**Did:** the state read (4 of 4 present, 55 total) with the live `NoSuchBucket` re-read and a live
control; the rollback document behind a shape guard; both removals in my own worktree; `terraform
validate`; the untargeted and targeted plans, graded per attribute, per Sid and per ARN from `show
-json`, plus `prior_state` / `configuration` / `resource_drift` read explicitly to establish *why* there
is no destroy; and the revert of an unintended `fmt` write in two trees.

**Did NOT:** apply anything, create anything, touch `tombstones.json`, open a NEVER-2 entry, or commit
any edit. **Never created the bucket** (BOUNDS). The `market-data-generator-lambda-role` role itself is
untouched -- its orphan status (`RoleLastUsed` null, no Lambda node) is row Z-S43's, not this act's.

**For the pair:** the blast radius is one IAM policy document (losing exactly 2 of 11 ARNs, 5 statements
preserved) plus the pruning of 4 stale state entries for a bucket that does not exist. Both branches:
**(A)** the apply reports `1 changed` and the live document differs from the rollback by exactly those 2
ARNs, with `opal-market-data-v2` still returning `NoSuchBucket` afterwards (nothing re-created);
**(B)** if the apply instead reports any create or destroy, that is outside the signed shape and the act
stops -- the tombstone-gate is a second net under it, since a planned create of `opal-market-data-v2`
would match the tombstone list that `safe-apply` checks.
