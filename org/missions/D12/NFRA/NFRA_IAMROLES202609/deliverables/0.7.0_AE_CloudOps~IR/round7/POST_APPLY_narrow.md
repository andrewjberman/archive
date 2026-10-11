# POST_APPLY -- NFRA_IAMROLES202609.TO-IAM-x-2 PHASE B, ACTS 1 AND 2

**Cell:** IAM-x-2 (round 7, FWD-4 enrichment; round-6 analysis E2), as **amendment A3-r7** @`12e053a1de` rules it
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z`
**Authority:** GO `2.0.0_SA_COO~ZI` msg 33227. Halves: COO @`12e053a1de`, CTO @`2ac0309870`.
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x2b`, Terraform v1.15.8.

> **THIS CELL IS A PERMISSION NARROWING, the first in the project.** Every other act in rounds 6 and 7 moved
> custody only. Here two grants were deleted and a third lost one resource. Nothing was added; no trust and no
> tag moved anywhere.

> **TARGET 4 IS HELD AND NOT COVERED.** `sentiment_query_api-role`'s `DynamoDBAccess` is untouched: A3-r7 sends it
> to the CTO as a product call (delete vs repoint), because the survey showed the table is alive in **us-east-1**
> and a DynamoDB ARN carries no squatting hazard. Its inert declaration is removed, not applied.

---

## 1. THE REQUIRED LINES

```
POST-APPLY-PLAN: infra/aws/terraform/news-pipeline: 0 to add, 0 to change, 0 to destroy
```

Terraform renders a clean plan as a sentence, so the verbatim output is quoted beside the canonical line:

```
$ terraform -chdir=infra/aws/terraform/news-pipeline plan ... -target=aws_iam_role_policy.codebuild_semantic_clustering_policy
No changes. Your infrastructure matches the configuration.
```

**AC2 expects 3 and this file carries 1. That is the correct count for the cell as A3-r7 re-cut it, not a
shortfall:**

| module | why it has no `POST-APPLY-PLAN` line |
|---|---|
| `smartx-pipeline` | ACT 1 ran through the **IAM API**, not Terraform. A3-r7 ruled it so and ordered the inert declaration removed -- *"no Terraform runs in smartx-pipeline"*. There is no plan to record, by design: that is what keeps the three `Z-S21` Lambda drifts out of this act entirely. |
| `market-overview` | Target 4 is **HELD**. Nothing was applied, so there is nothing to re-plan. |

AC3 likewise reads `closed=2`, not 3, for the same reason: two ledger entries were opened because two acts ran.

## 2. ACT 1 -- two inline policies DELETED through the IAM API

Ledger `iamroles-r7-narrow-smartx`, opened before the first delete, closed after the read-back.

| read | result |
|---|---|
| `list-role-policies` BEFORE | **3** -- `['opal-smartx-logs', 'opal-smartx-s3-access', 'opal-smartx-secrets']` |
| `delete-role-policy opal-smartx-s3-access` | rc=0 |
| `delete-role-policy opal-smartx-secrets` | rc=0 |
| `list-role-policies` AFTER | **1** -- `['opal-smartx-logs']` |
| `get-role-policy opal-smartx-s3-access` | **NoSuchEntity** (rc=254) |
| `get-role-policy opal-smartx-secrets` | **NoSuchEntity** (rc=254) |
| **POSITIVE CONTROL -- `get-role-policy opal-smartx-logs`** | **rc=0, returned its document (1 statement)** |

**THE CONTROL IS WHAT MAKES THE TWO `NoSuchEntity` READINGS EVIDENCE.** A failed retrieval returns a value: an
IAM call that could not reach the service, or a mistyped role, would also produce `NoSuchEntity`. Running the
same call shape against the policy that must *survive* is what makes the absence a fact about those two
policies rather than about the instrument.

**THE ROLE IS UNTOUCHED,** read live after both deletes: trust still `lambda.amazonaws.com`, path `/`,
`max_session_duration` 3600, `PermissionsBoundary` None, description still
`Lambda role for SmartX query functions`, 0 attached managed policies, and `list-role-tags` returns exactly the
four round-6 tags (`System=SmartXPipeline`).

**WHAT WAS ACTUALLY CLOSED, and only one of the two was a hazard:**

- `opal-smartx-s3-access` granted `s3:GetObject`+`s3:ListBucket` on `opal-data-smartx`, `opal-data-smartx/*`,
  `opal-code-smartx`, `opal-code-smartx/*` -- **all four 404, re-confirmed at the act.** An S3 bucket name is
  GLOBAL, so while that Allow existed, anyone creating either bucket name in any account would have received
  read access through this role. **This is the one genuine squatting hazard in the round-7 set, and it is now
  shut.**
- `opal-smartx-secrets` granted `secretsmanager:GetSecretValue` on a **us-east-2** ARN in a region holding **0
  secrets**, while the secret itself is alive in us-east-1. Wrong-region tidiness on an orphan role, with no
  squatting hazard (a Secrets Manager ARN is account- and region-scoped). Recorded as such rather than dressed
  up as risk reduction.

Both sat on a role row `Z-S24` established is an **orphan no Lambda assumes**, which is why deleting rather than
repointing was safe.

## 3. ACT 2 -- one Resource element removed, in Terraform

Ledger `iamroles-r7-narrow-news-pipeline`. The declaration was **committed before the import** (`b739b2b49b`,
A4-r6 order), then the `-target` apply, then the drain in the same session.

`Apply complete! Resources: 1 imported, 0 added, 1 changed, 0 destroyed.`

**GRADED BY DECOMPOSING THE POLICY PER `Sid`, before the apply and again live afterwards.** A policy is ONE
opaque string attribute: a bare `1 to change` would read identically if a different resource had been dropped or
another statement widened. The same decomposition was run twice -- against the plan, and against the committed
rollback.

| `Sid` | rollback -> live | resources removed | actions changed |
|---|---|---|---|
| `CloudWatchLogs` | 1 -> 1 | none | none |
| `ECRAccess` | 1 -> 1 | none | none |
| `LambdaUpdate` | 1 -> 1 | none | none |
| **`S3Access`** | **2 -> 1** | **`arn:aws:s3:::codebuild-semantic-clustering-artifacts/*`** | none |

```
Sids: four before, four after. None added, none removed.
STATEMENTS THAT DIFFER AT ALL: 1   (the expected count)
```

`arn:aws:s3:::opal-data-news-v2/*` is **retained** -- it was the live control (FOUND, us-east-1), and it is the
grant this role actually uses.

**THE ROLE IS IN USE (`RoleLastUsed` 2026-09-11) AND IS UNTOUCHED:** trust still `codebuild.amazonaws.com`,
description still absent, the four round-6 tags exactly (`System=NewsPipeline`), and `list-role-policies` still
returns the single `CodeBuildSemanticClusteringPolicy`.

**THE HAZARD HERE WAS THE SHARPEST IN THE SET AND IS NOW SHUT.**
`codebuild-semantic-clustering-artifacts` is a GLOBAL S3 name and the statement granted `s3:GetObject` **and
`s3:PutObject`** on `.../*` -- so whoever created that bucket name would have had read AND WRITE through a role
that is actively used and can also `lambda:UpdateFunctionCode` on a live function. PHASE A reported that the
cell's own rule of removal could not reach it, because the dead ARN shared a statement with a live one; A3-r7
ruled the narrower act (one element, in Terraform, `-target`), which is what closed it.

## 4. THE ROLLBACKS -- committed BEFORE the first delete, which was the binding condition

The CTO half carried one emphasis: *"the rollback files are written and committed BEFORE the first delete, and
each is read back as valid JSON equal to `get-role-policy`'s document."* Discharged at **`af85a44c38`**, before
anything was removed:

| file | statements | document == live |
|---|---|---|
| `ROLLBACK_smartx_opal-smartx-s3-access.json` | 1 | **True** |
| `ROLLBACK_smartx_opal-smartx-secrets.json` | 1 | **True** |
| `ROLLBACK_news_CodeBuildSemanticClusteringPolicy.json` | 4 | **True** |

**EQUALITY WAS PROVEN AGAINST A FRESH LIVE RE-FETCH, not against the file being written.** Each document was
pulled again into a scratch path outside the repo and compared canonically (`sort_keys`). Comparing a saved file
to itself would have proven nothing -- that ordering is the whole value of the check.

Each file carries `RoleName` and `PolicyName` as well as the document, so a future `put-role-policy` has an
unambiguous target. **One hygiene fix:** the shim's stdout arrives CRLF on this device (22, 14 and 55 CR bytes).
JSON is whitespace-insensitive so the rollbacks would have worked either way, but these are committed repo
files, so all three were rewritten LF-only with content preserved and re-validated (CR=0, non-ASCII=0).

**No rollback was needed and none was run.** All three remain available, and ACT 1's are the only route back for
the two deleted policies -- which is exactly why they were committed first.

## 5. THE INERT DECLARATIONS, REMOVED PER A3-r7

| file | why removed |
|---|---|
| `smartx-pipeline/zz_narrow_z_s23.tf.proposed` | ACT 1 ran via the IAM API; **no Terraform runs in that module**, so the declaration would never be applied. Removing it also means the canon collision PHASE A found (`smartx-s3-access` vs `opal-smartx-s3-access`, survey section 6) **never occurs** -- A3-r7 chose the IAM-API route partly for that reason. |
| `market-overview/zz_narrow_row14.tf.proposed` | target 4 HELD, referred to the CTO as a product call. |
| `news-pipeline/zz_narrow_z_s32.tf.proposed` | superseded by the live `.tf` this act committed. |

## 6. ONE INSTRUMENT CORRECTION, WITH ITS CONTROL

`terraform fmt -check` read **rc=3** on the ACT 2 `.tf`. A control proved it was **not** the narrowing: the
**unedited** as-live file scored rc=3 as well, so the non-canonical formatting came from **my own generator**,
which emitted JSON-style `"key": value` inside `jsonencode()` where HCL wants `key = value`. Fixed with
`terraform fmt` and re-verified at rc=0 with the ARN set intact and 4 `Sid`s present.

Worth separating from the earlier reading: **rc=2 means `fmt` refused the EXTENSION** (`.tf.proposed` is not a
`.tf`), while **rc=3 means genuinely non-canonical formatting**. Those are different verdicts and I had conflated
them earlier in the session.

## 7. THE LEDGERS AND WHAT THIS ORDER STILL OWES

Both entries CLOSED with every leg proven: `iamroles-r7-narrow-smartx` (DELETE, READBACK, UNTOUCHED) and
`iamroles-r7-narrow-news-pipeline` (TF, LIVEDIFF, REPLAN). Nothing of this lane's is open.

**Owed, and not this lane's:** the CTO's product call on target 4 (delete vs repoint the us-east-2 DynamoDB ARN).
Until it lands, AC2 reads 1 and AC3 reads `closed=2`, and **this order is not complete and is not flipped.**

**ACTS 1 AND 2 END HERE.**
