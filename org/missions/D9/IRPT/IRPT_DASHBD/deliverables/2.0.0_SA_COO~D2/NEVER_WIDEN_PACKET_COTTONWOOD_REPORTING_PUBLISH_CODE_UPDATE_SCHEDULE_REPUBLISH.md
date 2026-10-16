# NEVER-WIDEN PACKET -- the Cottonwood series publish: CODE UPDATE (writer 0.3.0), the DAILY SCHEDULE created DISABLED, and the REPUBLISH of the 939 series (IRPT_DASHBD rounds 148 and 149)

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~08:4xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, ROUNDS 147P/148 ANALYSIS @5daaee121d (msg 9158): "the 939 series are republished under the signed publish pair's branch E" and "the schedule pair is still owed before any reader"; the first publish pair is `NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_LAMBDA.md` (sha256 `0c9b495ce2f7`, both halves signed, applied and closed).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The AE applier builds `irpt-cot-reporting-publish-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-reporting-publish-lambda`. The entry is re-pinned and the build-only hash is below (section 2); the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key `investor-reporting/irpt-cot-reporting-publish-lambda.zip` (the bucket is versioned; the current version `9s6sk2dVtf6Ygi2JOGUxtwuiSNXCfKDa` is the rollback target) and updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-publish-iso/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 3 to add, 1 to change, 0 to destroy:**

| address | what it is |
|---|---|
| `aws_iam_role.irpt_reporting_publish_iso_scheduler` (add) | `irpt-cot-reporting-publish-scheduler-role`, assumed by `scheduler.amazonaws.com` only |
| `aws_iam_role_policy.irpt_reporting_publish_iso_scheduler` (add) | `irpt-cot-reporting-publish-scheduler-policy`: ONE statement `InvokeThePublishFunctionOnly`, `lambda:InvokeFunction` on the one function ARN |
| `aws_scheduler_schedule.irpt_reporting_publish_iso` (add) | `irpt-cot-reporting-publish-daily`, `cron(30 9 ? * MON-FRI *)` America/New_York, flexible window OFF, input `{"upload": true}`, **state DISABLED** |
| `module.irpt_reporting_publish_iso.aws_lambda_function.this` (change) | the CODE only: the artifact version and its hash move; memory 1024, timeout 900, handler, runtime, role, layer, no reserved concurrency and no environment stay exactly as they are |

Any other line, any other attribute on the function, any destroy, STOPS the act. The execution role and policy of the function, the log group and the layer data source do not appear in the plan.

**Act 3 -- ONE synchronous DRY-RUN event `{}`** (`RequestResponse`, `--cli-read-timeout 0`). It reads and builds and writes nothing. **Expected:** `uploaded` false; 65 partitions from 2026-07-10 to the newest (2026-10-14 unless the 12:15Z landing fire has added 2026-10-15, then 66); `published` 939 and `refused` 40 (the first publish's counts; a different count is read, recorded, and STOPS only above the 10 percent refusal line); `unreported_trading_days` beginning with 2026-08-19, 2026-09-24, 2026-09-25 and equal to the trading calendar minus the live gold partitions (the CTO's condition 3 of the first pair); Max Memory Used at most 717 MB. The dry run's returned body also proves the new code is live: the function's `CodeSha256` equals the uploaded zip's.

**Act 4 -- ONE-ACCOUNT republish** `{"upload": true, "accounts": ["<one id>"]}`: the same account rule as the first pair (the first account, sorted, in the 2026-07-10 partition with a positive market value; the id is never recorded, only 12 hex of its sha256). Two objects at the SAME keys as before. **After-read:** the stored series validates against series contract 0.3.2 as bundled; it carries `income_claim` = `absent` beside null income, the unreported pair equal to Act 3's list, and the series size equals the manifest's; the manifest carries `calendar_source` (`pandas_market_calendars` or `fallback_2010_2027`, whichever answered), `publisher_version` "0.3.0" and the same firm; the prior version of each of the two keys is still present (versioned bucket).

**Act 5 -- the FULL republish** `{"upload": true}` (branch E of the first pair: same prefix, same keys; 939 series and 939 manifests overwritten with new versions). Counts equal Act 3's `published`; the object count of the prefix stays 1,878; the after-read samples ten series (by sorted position, recorded as hash prefixes) against the Act 4 checks.

**Act 6 -- the read for row S104.** A served Cottonwood series shows the claim: the sampled series carry `income_claim` = `absent` with every `income` entry null, under series contract 0.3.2 whose `fixed_reason` is `RETURN_METHOD_DOES_NOT_SEPARATE_INCOME`; a count of series with the claim equals `published`. This is the evidence the CTO named for disarming S104.

**NOT in this packet:** enabling the schedule (the CTO's separate word; a later one-line change in its own pair); the 49 Financial `reporting-gold` function and the class producer's dated read (a separate code-update pair); any reader; any delete of any object or version.

## 2. Pins

Code at tree `e6d44ac5e8` or later on `box/dell2` (LOCAL); the writer and the rename landed as ONE drain `ff6c0633a7`, the schedule at `3832e62b2b`, the re-pin at `edf7999ebe`. sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `iam.tf` `0008681b0b01` (6,359), `lambda.tf` `4b06e81c4119` (2,708), `locals.tf` `fb2e7936b6d0` (2,691), `main.tf` `5b49dd311dbf` (1,844), `schedule.tf` `fc5867c7af69` (1,986), `reporting-publish-cot/handler.py` `ed630f8859de` (8,165), `reporting-publish/publisher.py` `3d32ffb84ea0` (31,303), `org/standards/IRPT_DASHBD_SERIES_CONTRACT.json` `42fc230550fe` (16,976; version 0.3.2). The source-map entry holds 12 staged members, each pinned to a full commit and hashed (re-pinned, none stale at packet time) plus `handler.py`. **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `GagDGBNGmPsmYaJR1B7qG/TvaPdQU3LiVAh6c+wt6jo=`.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-reporting-publish-lambda`: PRESENT; CodeSha256 `HDgIzQoXMyUNBxeyqgLXcplD1c01QwVsASRoMJbd4hk=` (the first pair's bundle); 1024 MB; one layer. **Artifact key:** current VersionId `9s6sk2dVtf6Ygi2JOGUxtwuiSNXCfKDa` (140,472 bytes); bucket versioning Enabled.
- **Schedules** named `irpt-cot-reporting-publish*`: NONE. The scheduler role and policy: absent (they are in the plan as adds).
- **Target prefix** `irpt/cottonwood/platinum/reporting/` in `opal-data-cottonwood`: **1,878 objects** (the first pair's fill: 939 series, 939 manifests); bucket versioning Enabled, so every overwrite keeps the prior version. Nothing reads the prefix as served.
- **Ledger:** the first pair's ledger is CLOSED (`6650d1aac6`); this pair opens its own.

## 4. What each act changes in the world

- **Act 1:** a new version of one artifact key; nothing served moves. **Act 2:** three resources are created (none writes anything; the schedule is DISABLED) and the function's code is replaced; nothing is served by the function yet. **Act 3:** nothing. **Acts 4 and 5:** the 1,878 objects of an UNREAD prefix are overwritten at the same keys with the same series plus `income_claim`, and manifests with `calendar_source` and `publisher_version` 0.3.0; the prior versions remain. **Act 6:** reads only.

## 5. Writers of the changed property, counted

The property is the content of `irpt/cottonwood/platinum/reporting/`. **ONE rule writes it: the handler's `put_object` (the only PutObject in the function and the only PutObject statement in its role).** Entry paths: a hand invocation, and the schedule once it is ENABLED (DISABLED here). N = 1 rule; 2 entry paths, one of them inert. Not established: any operator who wrote this prefix by hand; the first pair's after-reads counted 1,878 objects, all series or manifests.

## 6. Both branches (Acts 3 to 6)

- **Branch A:** as the acts state it; the after-read records memory, duration, counts and the sample checks.
- **Branch B (an account refuses):** counted by reason and skipped; refusals above 10 percent STOP at Act 3. A refused account keeps its prior objects (nothing is written for it).
- **Branch C (a run dies between an account's series and manifest):** the old manifest and the new series coexist for that account until the event is run again, which rewrites both; the reader contract names both files and `byte_sizes` in the manifest would differ from the stored size, which the after-read counts.
- **Branch D (out of memory or time):** nothing further is written; the first pair measured 293 to 297 MB and 99 s; the line is 717 MB and 900 s. Above it Acts 4 and 5 do not start.
- **Branch E (the run is repeated):** same keys, same series bytes, a new `built_at`; acceptable inside this prefix.
- **Branch F (the new code is wrong):** `build_series` or the validator refuses an account the first code accepted: counted by reason; the count of refusals differing from Act 3's expectation STOPS Act 5.
- **The plan is not the world** until read: the first pair's plan matched; this plan has a change line, which is the one the gate checks by attribute.

## 7. Rollback, per key

- **The code:** the previous artifact version `9s6sk2dVtf6Ygi2JOGUxtwuiSNXCfKDa` is the target. Reverting is a new upload of those bytes as the current version (a copy of the old version over the key, no delete) and a `safe-apply`, by the applier with the CTO's word.
- **The three schedule resources:** a `safe-apply` destroy of those three by the CTO's word (they hold no data).
- **The republished objects:** each key's prior version stays in the versioned bucket. Restoring is a listed-key copy of the prior version to the current key; deleting any version or object is Andrew's act and is never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-cottonwood-reporting-publish-codeupdate-20261016`, the applier named, legs L1 git (the tree commit and each file's sha256), L2 build (the line equal to section 2's), L3 terraform (the plan 3/1/0 by address, then the apply, recorded by `record-terraform-deploy.sh`), L4 dry run, L5 canary, L6 full republish and the S104 read. Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE. **Live state re-read at the moment of the apply** and equal to section 3, else STOP. The plan's function change must name `source_code_hash`/artifact version only.
3. **Each event only after the previous leg's after-read is recorded in the ledger;** payloads and bodies quoted by counts and words, never an account id. **Stop at once** on a Max Memory Used above 717 MB, a `Task timed out`, an `AccessDenied`, or a refusal count that differs from Act 3's beyond the recorded reasons.
4. **The schedule stays DISABLED through all six acts; nothing here enables it.**
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version.** The applier is an AE seat the gates admit, not a worker.
6. **The receipt** after Act 6: counts, memory, duration, the Act 4 checks, S104's read, and the words "NOT a page render", "no reader of the prefix established" and "schedule DISABLED".

## 9. Questions for the CTO's half

1. **One packet for the code update, the schedule's three resources and the republish?** Accept, or split the republish into its own word.
2. **The republish overwrites 1,878 objects of an unread prefix with a new version of each (versioned bucket, prior versions kept):** accept under branch E, with the rollback of section 7.
3. **The schedule is created DISABLED here and enabled only by the CTO's later word:** confirm that the enable is a separate one-line pair and not part of this one.

## 10. Not established, and so not covered

A `terraform plan` of this root with the schedule resources (none has run); which calendar the Lambda answers from (the manifest will say: `calendar_source`); whether any reader will open the prefix; the schedule's first fire (it is DISABLED); the 49 Financial `reporting-gold` function and the class producer's dated read (a separate pair).

-- 2.0.0_SA_COO~D2
