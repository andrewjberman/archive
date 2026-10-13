# ANNOUNCE -- NFRA_MCPINDEX MX-s-19 PHASE A (0.7.0_AE_CloudOps~MI, under amendment A7)

PHASE A as A7 scopes it: ONE saved targeted plan moving `bd-transaction-pipeline-trigger` and
`bd-realized-pipeline-trigger` from ENABLED to DISABLED and nothing else, plus this document. **No publish, no apply,
no ledger, no S3 write, no SSM document version, no Lambda invoke.** PHASE A under A2 did not exist at HEAD; this is
its first build.

Worktree `C:/Users/Opal Bloomberg/Desktop/wk-mcpindex-r7-s19-mi`, branch `wk-mcpindex-r7-s19-mi` cut from `box/sitez`
HEAD `cc938ca6d2` (A7: not `wk-mcpindex-r7-24`). Sparse cone, widened four times by what Terraform actually reads:
`infra/aws/terraform/{bd-pipeline,modules}`, `infra/aws/{ssm,ec2}`, `infra/logic`,
`data/black_diamond/scripts/gold`, `lib`, `.tools`, `org/{ref,critical_paths}`,
`org/missions/D9/NFRA/NFRA_MCPINDEX`, `org/tier2_senior/0.7.0_AE_CloudOps~MI`.
Push state: **LOCAL** (nothing pushed). Measured 2026-10-13 03:37-04:4xZ, every read outside 21:30-22:15Z and
23:45-00:45Z.

**Precondition, quoted.** MX-s-18's ledger
`org/critical_paths/change_management/20261007T0024Z_nfra-mcpindex-r7-bd-runner-sentinel_deploy_completion.md`:
`**Status:** CLOSED -- nothing stranded -- closed 20261008T222217Z`, log line
`- 20261008T222217Z CLOSED -- all 6 legs proven` (6 of 6 legs). A5's one read is the issuer's and A7 reports it:
`s19.PRE.sh` at 2026-10-13T03:06Z, `precondition dates passing 2 of 2 -- RESULT: PASS`. This seat did not re-run it;
the two dates are re-measured independently in section 3 below from S3 and CloudWatch, which is a different
instrument on the same question.

**ONE CRITERION IS REFUSED AS WRITTEN (BOUNDS item 3): `s19.AC1` cannot pass under A2's PHASE B.** Section 4. Row
`NFRA_MCPINDEX-Z-S101`, BLOCKING/ARMED, disarm owner `2.0.0_SA_COO~MI`.

---

## 1. THE PLAN

Diff on the branch -- **exactly two lines**, `infra/aws/terraform/bd-pipeline/eventbridge.tf`:111 and :220,
`state = "ENABLED"` -> `state = "DISABLED"`. `git diff --stat`: `1 file changed, 2 insertions(+), 2 deletions(-)`.
Nothing else in that file and no other file was edited (the 10 `infra/aws/ec2/smartx-exporter/.../*.py` paths that
`git diff` also prints in this worktree are a CRLF checkout artifact of the sparse-cone widening, not an edit; they
are outside this commit's pathspec and were never touched).

Census of the file's `state` lines, so the two changed lines are placed against their denominator: 12 `state =` lines
before (7 ENABLED, 5 DISABLED), 12 after (5 ENABLED, 7 DISABLED).

Cut from the worktree with `TF_DATA_DIR` = the worktree's `.scratch/tfdata`, `TF_PLUGIN_CACHE_DIR` = the shared
tree's existing `bd-pipeline/.terraform/providers` (aws v5.100.0 reused from cache, nothing downloaded, the shared
tree's own `.terraform` never written), `-lock=false`, `-input=false`, `-no-color`, state read-only:

```
terraform plan -input=false -lock=false -no-color \
  -target=aws_cloudwatch_event_rule.bd_realized_pipeline \
  -target=aws_cloudwatch_event_rule.bd_transaction_pipeline \
  -out=<worktree>/.scratch/mx-s-19.tfplan
```

- **Summary line, verbatim: `Plan: 0 to add, 2 to change, 0 to destroy.`**
- Both actions are `~ update in-place`, and in each the only changed attribute is `~ state = "ENABLED" -> "DISABLED"`
  with `# (9 unchanged attributes hidden)`. The schedule expressions, targets and Lambda permissions are not in the
  plan. **0 to destroy.** No BLOCKING row is owed on the plan's shape.
- Files: `mx-s-19.plan.txt` (tracked render, `terraform show -no-color`, 1,264 B, 32 lines, sha256
  `bd04f33085afc5defab7e15afe5f3dd56ca6f7ad3603adaac9d9badb39eebe4a`);
  `<worktree>/.scratch/mx-s-19.tfplan` (binary, 202,274 B, sha256
  `f69eae52ebc6483947c3ea0bac98e1bb00bab94f52f25a168530b7be23ec1680`, gitignored by `.gitignore:417` `**/*.tfplan`,
  local to this worktree -- the same arrangement MX-s-16 used).
- **NEGATIVE CONTROL, run in this same worktree so the control and the subject share one `TF_DATA_DIR` and one state
  read.** `eventbridge.tf` restored to HEAD bytes (`git checkout --`, `git diff` empty), the SAME two targets planned:
  `Terraform has compared your real infrastructure against your configuration and found no differences, so no changes
  are needed.` The edit was then restored and the file's sha256 read back equal to its pre-control value
  (`2ef321f93fc8b9989b4d1ed91a5b653062812df80bf94611edd95e249d3dc63b` both times). So the plan's 2 changes are
  produced by this edit alone, and live state matched HEAD at the cut.
- **`terraform fmt`: a deviation exists and it is PRE-EXISTING; it was NOT fixed inside this act.** `fmt -check`
  (read-only; `-diff` and bare `fmt` were never run, because both WRITE) flags `eventbridge.tf` identically at HEAD
  bytes in the shared tree and post-edit in the worktree, and the directory-level `-check` at HEAD flags **9 of the
  dir's files**: `alarms.tf`, `api-gateway.tf`, `bd-49f-interim.tf`, `ec2.tf`, `eventbridge.tf`, `lambdas.tf`,
  `s3-notifications.tf`, `secrets-opal-bd.tf`, `secrets.tf`. Same file list before and after, so the flag is not this
  edit's.

## 2. LIVE BASE STATE (the BASE-MOVED inputs; read 2026-10-13 ~04:0xZ)

| rule | State | ScheduleExpression | target | bus |
|---|---|---|---|---|
| `bd-realized-pipeline-trigger` | **ENABLED** | `cron(45 21 ? * MON-FRI *)` | `bd-realized-trigger` | default |
| `bd-transaction-pipeline-trigger` | **ENABLED** | `cron(53 21 ? * MON-FRI *)` | `bd-transactions-trigger` | default |

Per A2 no SSM document version is published this round, so there is no document-version read to guard and no document
rollback leg. The two documents stay at their current default versions, untouched.

**At the GO, re-read both rows above.** If either `State` is no longer ENABLED, or either schedule differs, the saved
plan is stale: re-cut it with the same two-target command and re-issue both sha256 values before any apply. Terraform
refuses a stale saved plan at apply, so this read is a courtesy; the guard is Terraform itself.

## 3. EXPECTED SERVED DELTA: **0**, and it is MEASURED, not predicted

A7 states the DELTA as "0 on a normal day; on a Mon/Tue the partitions now land from `bd-silver-merge` at ~00:10Z
instead of the document at ~21:50Z". Measured on the two acceptance-precondition dates, the delta is **0 on both**,
because the two evening documents **already write nothing**:

**(a) The legs RAN on Monday 2026-10-12 -- the chain is not broken, it is idle.**
`bd-realized-trigger` invoked 21:45:16Z (rule event id `13ce38f0-a934-78df-8623-489295c3f802`), started
`i-0800437d1dbb0b5cc`, sent SSM `1a53ac57-f068-4818-9f2a-3d771554c5b6` (`opal-bd-realized-download`).
`bd-transactions-trigger` invoked 21:53:04Z, started `i-00c7568bc510f7423`, sent SSM
`b974ccac-5950-4c2f-beb9-d6354199f3d7` (`opal-bd-transaction-download`). Both invocations `Status: Success`.

**(b) Both documents' own stdout says they merged nothing.** Verbatim:
- realized (ended 21:46:10.635Z): `Previously processed: 157 realized files` / `No new realized files to process` /
  `Merge exit code: 0`
- transactions (ended 21:53:56.580Z): `Previously processed: 208 files` / `No new files to process` /
  `Merge exit code: 0`

**(c) S3 agrees, with its denominator printed.** Versions written under `silver/transactions/` or `silver/realized/`
in `2026-10-12T20:00Z..2026-10-13T00:00Z` (the whole evening-document window): **0**, over **2,336** transactions
versions and **1,388** realized versions scanned (`list-object-versions`, per-page counts 1000+996+340 and 1000+388,
the filter applied per page).

**(d) The mechanism, and how long it has held.** Both legs run the stale S3 script
`s3://opal-data-bd/scripts/merge-daily-incremental.py` (42.5 KiB, downloaded in both runs) whose processed-file
manifests are `silver/incremental_manifest.json` (transactions) and `silver/incremental_realized_manifest.json`
(realized) -- the same two keys `bd-silver-merge` maintains. Version history of those keys:

| key | latest write | prior writes | last write in an EVENING window |
|---|---|---|---|
| `silver/incremental_manifest.json` | 2026-10-13T00:14:51Z | 10-12 00:17:25Z, 10-11 00:18:42Z, 10-10 00:18:39Z, 10-09 00:14:13Z, 10-08 00:16:48Z, 10-07 00:23:09Z | **2026-10-06T21:54:00Z** |
| `silver/incremental_realized_manifest.json` | 2026-10-13T00:15:17Z | 10-12 00:17:50Z, 10-11 00:19:34Z, 10-10 00:19:05Z, 10-09 00:14:34Z, 10-08 00:17:08Z, 10-07 00:23:33Z | **2026-10-06T21:46:16Z** |

Each manifest write timestamp equals its table's silver partition write timestamp to the second, and every write
since 2026-10-07 is at 00:1x-00:2xZ -- `bd-silver-merge`'s time, not the documents'. The documents' trigger Lambdas
have **4** weekday log streams since then (10-07, 10-08, 10-09, 10-12; 10-10 and 10-11 are Sat/Sun and the rules are
MON-FRI), so **4 of 4 weekday evening runs since 2026-10-07 wrote 0 manifest versions and 0 silver partitions.**

CLAIM GRADES, stated separately because they are not the same strength:
- **MEASURED:** the 4-of-4 no-op record above, and the 0-of-2,336 / 0-of-1,388 window census.
- **MEASURED BY WRITE-TIME COINCIDENCE, not by reading the deployed script's bytes:** that the documents write those
  two manifest keys. The evidence is that the only two evening-window versions in the retained history sit at
  21:54:00Z and 21:46:16Z on 2026-10-06, each about one minute after its document's 21:53Z / 21:45Z fire. The
  deployed S3 script's source was not read, and the repo copy at
  `data/black_diamond/scripts/silver/merge-daily-incremental.py` is a LATER revision: it prints
  `Previously processed: N files (etag-tracked)`, and the deployed one printed that line without the suffix.
- **INFERRED:** that the no-op holds on every FUTURE weekday. The mechanism makes it so for as long as
  `bd-silver-merge` runs first and keeps recording etags in the shared manifest -- which is what MX-s-18's sentinel
  fix guarantees and what `s19.AC2` re-measures on 2026-10-19 and 2026-10-20.

**BOTH BRANCHES of what the disable removes, so the DELTA covers everything the act touches:**
1. Served silver: **nothing**. No partition added, removed or changed; `bd-silver-merge` is already the only writer in
   fact on both tables.
2. Not served, and it does stop: two EC2 instance starts per weekday (`i-0800437d1dbb0b5cc`, `i-00c7568bc510f7423`,
   each booted then self-shut-down after 2 minutes), and the two daily log objects
   `s3://opal-data-bd/logs/{realized,transaction}-download-<date>.log` (520 B and 499 B on 10-12).
   **UNMEASURED: whether any consumer reads those two log keys.** They are the documents' only remaining write, so if
   a consumer exists, that is the DELTA. A `comp-estate --resource logs/realized-download` read settles it; this seat
   did not run it because it is outside PHASE A's two deliverables, and it is named here rather than left silent.

## 4. REFUSED CRITERION -- `s19.AC1` is unsatisfiable under A2's PHASE B (row Z-S101)

`s19.AC1` expects `WRITER CENSUS: 4 of 4 BD silver tables have exactly 1 writer -- RESULT: PASS -- exit=0`. It
delegates to round 6's `s16.AC1.sh`, whose header states it counts, per table, "each SSM document
`opal-bd-{...}-download` whose `$LATEST` AND DEFAULT content still runs `merge-daily-incremental`". The census reads
`ssm get-document` content and `get-bucket-notification-configuration`. **It never reads an EventBridge rule.**

Run at the base, read-only, 2026-10-13 ~04:3xZ:

```
NOT-ONE: transactions: 2 writer(s) ['ssm:opal-bd-transaction-download(latest=True,default=True)', 'lambda:bd-silver-merge']
NOT-ONE: realized: 2 writer(s) ['ssm:opal-bd-realized-download(latest=True,default=True)', 'lambda:bd-silver-merge']
OK: unrealized: 1 writer(s) ['lambda:bd-silver-merge']
OK: allocations: 1 writer(s) ['lambda:bd-silver-merge']
WRITER CENSUS: 2 of 4 BD silver tables have exactly 1 writer; graded 2 of 4 (transactions realized unrealized allocations)
RESULT: FAIL
```

A2 narrowed PHASE B to the rule disable and said so twice: "**PHASE B is the rule disable only**" and "No document
version is published"; "Retiring the documents, trigger Lambdas and instances is a later order after one observed
week." The only input the apply changes is each rule's `State`, and the census does not read it. **So the number
cannot move: it reads 2 of 4 before the apply and 2 of 4 after it.** That is not a prediction about the world -- it is
a property of the instrument, read from its source.

**The issuer's call, three options; this seat recommends (b).**
- **(a)** Widen PHASE B to publish both no-op document versions. Meets AC1 as written, and reverses A2's explicit
  deferral and Andrew's "we need to confirm the shape first before making that move" -- so it is not taken on this
  seat's word.
- **(b) RECOMMENDED: amend AC1 to count a document writer only while its trigger rule is ENABLED** (one
  `aws events describe-rule` limb per document). This matches the check's own declared intent -- "Writers counted on
  the APPLIED plane" -- since a document whose only schedule is DISABLED cannot write on the scheduled plane. State
  the bound in the amendment: an ad-hoc `send-command` can still invoke the document, so the amended criterion grades
  the SCHEDULED plane, never reachability.
- **(c)** Defer AC1 to the later retirement order and grade this round on AC2 and AC3 only.

Under (b) the expected post-apply read is `4 of 4 ... RESULT: PASS`; under (c), AC1 is NOT_EVALUATED for round 7.
`s19.AC2` and `s19.AC3` are unaffected either way and need no change.

## 5. ROLLBACK (A7: re-enable each rule through the same targeted path)

Nothing is deleted and no document version is published, so the rollback is the inverse of the one edit. Per table,
independently:

| table | revert | re-plan target | expected |
|---|---|---|---|
| realized | `eventbridge.tf`:111 `"DISABLED"` -> `"ENABLED"` | `-target=aws_cloudwatch_event_rule.bd_realized_pipeline` | `Plan: 0 to add, 1 to change, 0 to destroy`, sole attribute `state` |
| transactions | `eventbridge.tf`:220 `"DISABLED"` -> `"ENABLED"` | `-target=aws_cloudwatch_event_rule.bd_transaction_pipeline` | same shape |
| both | revert both lines | both targets | `Plan: 0 to add, 2 to change, 0 to destroy` |

Then `.tools/safe-apply.sh` (never bare `terraform apply`), and read back `aws events describe-rule --name <rule>`
expecting `"State": "ENABLED"` and the schedule unchanged (`cron(45 21 ? * MON-FRI *)` realized,
`cron(53 21 ? * MON-FRI *)` transactions -- the values in section 2). The rollback restores the rule only; because the
documents are idempotent against the shared manifest (section 3d), a re-enabled rule resumes as a no-op, not as a
duplicate write.

## 6. PHASE B, when the GO comes (not done here)

1. Open the NEVER-2 ledger `nfra-mcpindex-r7-bd-doc-retire`, naming BOTH
   `org/critical_paths/change_management/<ts>_nfra-mcpindex-r7-bd-doc-retire_deploy_completion.md` AND
   `org/critical_paths/.open_deploys/nfra-mcpindex-r7-bd-doc-retire.json`.
2. `.tools/safe-apply.sh` of the saved plan (re-cut first if section 2's reads moved), outside both windows.
3. Read back `describe-rule` on both rules expecting `DISABLED`; re-plan for 0-diff.
4. Leave the ledger OPEN until `s19.AC2` reads 2026-10-19 and 2026-10-20. On 2 of 2 close it; on a failure roll back
   that table per section 5 and report.
5. `s19.AC2`'s dates stand at 2026-10-19 / 2026-10-20 if the disable lands before 2026-10-19T00:00Z (A7); otherwise
   the issuer re-dates them.

**NOT cleared at PHASE A, and it must be read at the GO rather than assumed:** `comp-schedule` was run per
`<preflight>` and did NOT clear the deploy-ledger carrier. C1 SENTINEL is DECIDABLE, denominator 23, **0 armed
gates**; C2 DEPLOY-LEDGER reached its native denominator (11, then 13 on the resume) and scanned **0 of them** before
the 90 s budget, printing `answer-state=PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE ... must be rerun, never read as
zero or complete`; C3-C6 read `NOT-SCANNED`. So at the GO the open-deploys read is done directly under NEVER-2 --
union `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/` over EVERY live worktree
(`git worktree list --porcelain` read **18** at this session's start), with the per-tree denominator printed, using
`ls-tree`/`ls -a` because `ls -1` hides `.unindexed_red_state.json`.

## 7. ROWS FILED THIS PHASE

| id | class | standing | one line |
|---|---|---|---|
| `NFRA_MCPINDEX-Z-S101` | BLOCKING | ARMED (`2.0.0_SA_COO~MI`) | `s19.AC1` reads 2 of 4 before and after the apply: the census grades SSM document CONTENT and never a rule's State, which is the only thing A2's PHASE B changes. |
| `NFRA_MCPINDEX-Z-S102` | OBSERVATION | ARMED (`2.0.0_SA_COO~MI`) | `silver/transactions/2026-10-10.parquet` was re-written by the 2026-10-13 merge at 58,226 B, down from 4,462,340 B -- a 76x shrink on a re-write, while 2026-10-09's re-write GREW. Not caused by this order and not in its path; named because it is a possible silent partition truncation in the writer this retirement makes sole. |

## 8. OPEN FOR THE ISSUER

1. The two never-widen halves on this plan's pin (`mx-s-19.plan.txt` sha256 `bd04f330...`, binary sha256
   `f69eae52...`), then the PHASE B GO.
2. **Rule on `s19.AC1` (section 4) before the GO, not after the apply** -- otherwise the round's acceptance is owed a
   criterion that cannot pass whatever the world does.
3. Disposition `Z-S102` or route it; it is a `bd-silver-merge` question, not a trigger-rule question.
4. The UNMEASURED item in section 3: whether anything consumes
   `s3://opal-data-bd/logs/{realized,transaction}-download-<date>.log`.
