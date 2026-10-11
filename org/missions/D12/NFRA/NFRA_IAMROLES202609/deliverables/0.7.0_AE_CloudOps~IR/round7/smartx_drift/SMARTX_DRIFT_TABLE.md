# SMARTX_DRIFT_TABLE -- NFRA_IAMROLES202609.TO-IAM-x-3 (row Z-S21, round-6 analysis Addendum 1 item E4)

**Cell:** IAM-x-3, **READ-ONLY**. Nothing was applied, deployed or reverted; every terraform run below is a
`plan` and every AWS call is a read. **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** `ROUND_ANALYSIS.round6.md` Addendum 1 @`48153f21bc` -> DECOMP_R7 section 7 -> the issuance.
**Measured:** 2026-10-11 ~09:5xZ-10:1xZ, shared tree, `-lock=false`.
**`1.0.0_SA_CTO~Z` rules the deploy-or-revert act on this table.**

---

## 1. THE REQUIRED LINES

```
DRIFT: assets_daily_pull: commit=01f54452a9 ran_live=yes rec=DEPLOY: the new S3 version is BYTE-IDENTICAL to the running one (same ETag, same size), so applying moves a pointer and changes no running code
DRIFT: jwt_refresher: commit=14a620d01e ran_live=yes rec=DEPLOY: same -- the new version is a re-upload of identical bytes, so the apply is a no-op on what executes
DRIFT: rest_pull: commit=46d0b98aef ran_live=no rec=HOLD: the new version has DIFFERENT bytes (6608 vs 6610) and NO COMMIT produced them, so deploying unreviewed code and discarding it are both unjustified until the 2026-08-19T01:34Z upload is attributed
OUTPUT: autostart_lambda_arn: cause=its output block was DELETED from the configuration by a3b36fd877 (Andrew-ratified @874b52729c) along with the whole autostart chain; the value survives only in state because nothing has applied since, so the null is that ratified removal completing, not a defect
OUTPUT: autostart_role_arn: cause=same commit, same ratified removal -- the role it read is gone from the configuration and absent from state
OUTPUT: eventbridge_rule_arn: cause=same commit; it read the smartx-daily-export-trigger rule, which that commit removed with the autostart chain and which is absent from state
```

> **THE HEADLINE IS NOT "THREE LAMBDA CODE DEPLOYS". IT IS ONE.** Row `Z-S21` describes this plan as carrying
> "three Lambda code deploys and three output removals that no cell authorized", and on the code half that is
> **too strong**: two of the three move a version POINTER at byte-identical content and change nothing that
> executes. Only `rest_pull` is a real code change, and it has never run. I am correcting my own row.

## 2. STEP 1 -- THE SAME SET, RE-CONFIRMED

```
$ terraform -chdir=infra/aws/terraform/smartx-pipeline plan -lock=false
Plan: 0 to add, 3 to change, 0 to destroy.
  # aws_lambda_function.assets_daily_pull will be updated in-place
  # aws_lambda_function.jwt_refresher     will be updated in-place
  # aws_lambda_function.rest_pull         will be updated in-place
Changes to Outputs:
  - autostart_lambda_arn = "arn:aws:lambda:us-east-1:313476888478:function:smartx-ec2-autostart" -> null
  - autostart_role_arn   = "arn:aws:iam::313476888478:role/smartx-ec2-autostart-20251222183942113900000002" -> null
  - eventbridge_rule_arn = "arn:aws:events:us-east-1:313476888478:rule/smartx-daily-export-trigger" -> null
```

rc=0, 0 destroys, 0 replaces. Every `s3_object_version` transition matches the cell text exactly, and
`rest_pull` is still the only one carrying a `source_code_hash` change. **Nothing changed since round 6.**

## 3. WHY NO COMMIT MOVED THE PLANNED VERSION -- the structural answer step 2 asks for

Step 2 asks me to "name the commit that moved the planned package / object version". **Measured answer: NO
COMMIT DID, and none can.** The configuration derives both attributes from a live data source:

```hcl
data "aws_s3_object" "rest_pull_artifact" { ... }        # and the same shape for the other two
  s3_object_version = data.aws_s3_object.rest_pull_artifact.version_id
  source_code_hash  = data.aws_s3_object.rest_pull_artifact.metadata["content-sha256"]
```
`rest-pull.tf:50-51, 98-99`, `assets-pull-lambda.tf:45-46`.

**So the plan drifts the moment anyone uploads a new object version, with no commit involved at all.** And the
git record confirms that is what happened: **0 commits touched any of the three source directories in the
2026-08-15..2026-08-22 window**, while all three S3 objects were re-uploaded within **11 seconds** of each other
on **2026-08-19T01:34Z** -- one batch action, not three events.

The `commit=` field in each line above is therefore the **last commit to that function's SOURCE**, which is the
most meaningful sha available and is, for all three, exactly the source map's own `last_deployed_commit`:

| function | last source commit | map `last_deployed_commit` | agree |
|---|---|---|---|
| `assets_daily_pull` | `01f54452a9` (2026-07-17) | `01f54452a9` | yes |
| `jwt_refresher` | `14a620d01e` (2026-05-15) | `14a620d01e` | yes |
| `rest_pull` | `46d0b98aef` (2026-06-11) | `46d0b98aef` | yes |

**There is consequently nothing to "revert" in the git sense for any of the three** -- the drift is between S3's
current object version and what the function is running, and no commit sits between them. A `REVERT`
recommendation could only mean "re-upload the prior object version", which is why none of the three is `REVERT`.

## 4. STEP 3 -- DID THE PLANNED CODE EVER RUN? The decisive measurement is the OBJECT, not the hash field

`source_code_hash` appears in the plan only for `rest_pull`, which already tells us the other two are
content-stable. But that is an inference from an absent diff line, so the two object VERSIONS were compared
directly -- `head-object` per version id, which is Rule 22a's "diff deployed bytes against the BUILD INPUT":

| function | OLD version ETag / size / uploaded | NEW version ETag / size / uploaded | same bytes? |
|---|---|---|---|
| `assets_daily_pull` | `42ff605c...` / 44216 / 2026-07-24T02:21:52Z | `42ff605c...` / 44216 / 2026-08-19T01:34:18Z | **YES** |
| `jwt_refresher` | `c01c49cc...` / 2137 / 2026-06-05T19:03:03Z | `c01c49cc...` / 2137 / 2026-08-19T01:34:07Z | **YES** |
| **`rest_pull`** | `684cf928...` / **6610** / 2026-06-05T19:03:06Z | `f7c396c7...` / **6608** / 2026-08-19T01:34:11Z | **NO** |

And the three hash planes agree on where each function actually is:

| function | live `CodeSha256` | state `source_code_hash` | source map `artifact_sha256` | verdict |
|---|---|---|---|---|
| `assets_daily_pull` | `4Iw0TWcez71...` | `4Iw0TWcez71...` | `4Iw0TWcez71...` | all three agree; running == planned |
| `jwt_refresher` | `MCsLEpIgbLt...` | `MCsLEpIgbLt...` | `MCsLEpIgbLt...` | all three agree; running == planned |
| **`rest_pull`** | `SnPiO8B8AxA...` | `SnPiO8B8AxA...` | **`lM6cnuZTetk...`** | **THE MAP DISAGREES WITH THE WORLD** |

> **`rest_pull`'s live `CodeSha256` IS the plan's "before" value, and the source map's `artifact_sha256` IS the
> plan's "after" value.** So the map records the NEWER artifact as the deployed one while the function runs the
> older bytes. This is exactly the state `cloud-ops` Rule 4 warns the map cannot detect -- *"it does NOT compare
> deployed bytes to built-from bytes"*, and *"running-bytes-older-than-built passes every rung"*. The map's
> `last_deployed_at` for `rest_pull` is 2026-07-14T08:26:13Z, which also **predates the 2026-08-19 upload**, so
> the map is stale against the object as well as against the function.

**`ran_live=yes` for two and `no` for one follows directly:** where the new object is byte-identical, the running
code IS the planned code; where it differs, the running code is the OLD object and the planned bytes have never
executed.

## 5. STEP 4 -- THE THREE NULL OUTPUTS, AND THEY ARE NOT A DEFECT

The cause is one commit, and it was ratified:

```
a3b36fd877  2026-08-14  0.7.0_AE_CloudOps
kill(OPAL_MDPFCLEANUP.TO-3 apply-4): remove smartx K1 sets -- autostart chain + model_monthly_pull chain
(17 blocks incl. the scheduler-role companions + 3 dangling outputs)
  ... + outputs autostart_lambda_arn/autostart_role_arn/eventbridge_rule_arn.
  terraform validate: Success. Andrew-ratified @874b52729c; both fns 74d invocation-silent.
```

Measured, not taken from the message:

- **The three output names appear NOWHERE in the module's configuration** -- `comp-find` over
  `infra/aws/terraform/smartx-pipeline` returns **0 hits across 21 files**. A deleted `output` block is planned
  to `null`; that is terraform doing exactly what it should.
- **The resources they read are absent from state.** Of the module's **58** state addresses, the only
  autostart-shaped entry is `data.aws_s3_object.autostart_artifact`, and that name is declared in **0 of 21**
  configuration files too -- a pure state leftover the next apply drops.
- **The output VALUES still show in `terraform output`** (12 outputs listed, including all three) purely because
  nothing has applied in this module since 2026-08-14.

> **So the "three output removals that no cell authorized" in row `Z-S21` were authorized** -- by
> `OPAL_MDPFCLEANUP.TO-3`, Andrew-ratified, with `terraform validate: Success` and both functions measured
> 74 days invocation-silent before the kill. The nulls are that act's state cleanup still pending. Applying
> them completes a ratified removal rather than performing a new one. **This is the second correction this table
> makes to my own row.**

## 6. WHAT THE CTO IS ACTUALLY CHOOSING BETWEEN

| | `assets_daily_pull` + `jwt_refresher` | `rest_pull` | the three outputs |
|---|---|---|---|
| what an apply does | moves a version pointer to identical content | **replaces running code with bytes nobody committed** | completes a ratified removal |
| risk of applying | effectively none; Lambda re-fetches the same bytes | **unknown** -- unreviewed 2-byte-smaller artifact | none |
| risk of NOT applying | the plan stays dirty and masks future real drift | the same, plus the map keeps claiming the new artifact is deployed | the outputs keep reporting dead ARNs |
| my recommendation | **DEPLOY** | **HOLD** | (not mine to recommend; they ride whichever apply happens) |

**One thing the CTO should know before choosing: this module will drift again.** Because `s3_object_version`
reads the live object, ANY future re-upload re-opens exactly this plan with no commit behind it. Deploying
re-syncs until the next upload; it does not close the class. Whether that configuration shape should change --
pinning the version, or deriving it from a build artifact -- is a design decision for the module's owner, and
**no project owns `smartx-pipeline`**, which is the actual gap here. I am not proposing a fix, because the
candidates differ in meaning rather than syntax.

**The missing fact for `rest_pull` is cheap for the right owner and is not in the repo:** what ran at
**2026-08-19T01:34Z** and re-uploaded all three artifacts. Until that is attributed, `HOLD` is the only
defensible verdict for a 2-byte difference with no commit behind it.

**READ-ONLY. Nothing was applied, deployed, reverted, tagged or state-edited. No ledger was opened, which is
what AC3's `0` records (0 smartx sentinels over a 27-entry `.open_deploys/`).**
