# NEVER-WIDEN PACKET -- the Cottonwood report-build function to the cloud (IRPT_DASHBD rounds 131 to 137, workstream B-49F): ONE new Terraform root, SEVEN new resources, a DRY-RUN event, then the backfill of the filled report values

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-15 ~19:0xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, ROUND ANALYSIS IRPT_DASHBD B-49F rounds 130-132 @b3dc83e664 item 3 ("the deploy of `irpt-cot-reporting-gold-lambda` under its own never-widen pair ... whose first run proves the 14.0.2 load, with a receipt to CTO~DELL1"), and ADDENDUM 1 @3204c9ab6d (no sidecar write; the handler states the unreported days).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_REPORTING_GOLD_LAMBDA_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is applied and no event is invoked until both halves are SIGNED on one sha256.**

## 1. The acts (four, in order; each has its own stop)

**Act 1 -- build, upload, apply.** The AE applier `0.7.0_AE_CloudOps~DB2` builds the bundle of `irpt-cot-reporting-gold-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-reporting-gold-lambda` (the source-map entry is fully pinned and hashed by `DB-b-265`; the applier writes NOTHING into the map except the two fields the upload script itself writes), then ONE Terraform apply of `infra/aws/terraform/investor-reporting/reporting-gold-iso/` through `.tools/safe-apply.sh` (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 7 to add, 0 to change, 0 to destroy, on exactly these seven addresses; any other line STOPS the act:**

| address | what it is |
|---|---|
| `module.irpt_reporting_gold_iso.aws_lambda_function.this` | `irpt-cot-reporting-gold-lambda`: python3.12, `handler.lambda_handler`, timeout 900, **memory 1024**, **no reserved concurrency** (the chain invokes the function while the previous invocation still runs), no environment variable, **one layer: `irpt-performance-native-layer` (read by a data source; not a plan line)**, artifact key `investor-reporting/irpt-cot-reporting-gold-lambda.zip` |
| `module.irpt_reporting_gold_iso.aws_cloudwatch_log_group.lambda` | its log group, retention 14 days |
| `aws_iam_role.irpt_reporting_gold_iso_execution` | `irpt-cot-reporting-gold-execution-role` (matches the Cottonwood bucket policy's `role/*-cot-*` admission) |
| `aws_iam_role_policy.irpt_reporting_gold_iso_execution` | `irpt-cot-reporting-gold-execution-policy`: seven statements, explicit actions, no wildcard action, no delete (below) |
| `aws_iam_role.irpt_reporting_gold_iso_scheduler` | `irpt-cot-reporting-gold-scheduler-role` |
| `aws_iam_role_policy.irpt_reporting_gold_iso_scheduler` | `irpt-cot-reporting-gold-scheduler-policy`: `lambda:InvokeFunction` on the one function ARN |
| `aws_scheduler_schedule.irpt_reporting_gold_iso` | `irpt-cot-reporting-gold-daily`, `cron(15 9 ? * MON-FRI *)` America/New_York, **state DISABLED** |

**The execution policy's seven statements (read line by line from `iam.tf`):** `ListCottonwoodGoldInputsAndFilledOnly` (`s3:ListBucket` on `opal-data-cottonwood` under `s3:prefix` `irpt/cottonwood/gold/` `account_dim/*`, `account_return_daily/*`, `filled_report_values/*`); `ReadCottonwoodGoldInputsOnly` (`s3:GetObject` on `account_dim/*` and `account_return_daily/*`); `WriteTheFilledReportValuesPrefixOnly` (`s3:PutObject` on `filled_report_values/*`, the ONLY PutObject statement); `ReadBackTheFilledPrefixOnly` (`s3:GetObject` on `filled_report_values/*`, the no-overwrite `head_object`); `ReadTheServedModelSeriesObjectOnly` (`s3:GetObject` on the one object `json/benchmarks/model_portfolio_timeseries.json` in `opal-data-portal-v2`, derived from the adapter's constants); `InvokeOwnFunctionOnly` (`lambda:InvokeFunction` on the function's own ARN, for the chain); `OwnLogStreamOnly` (`logs:CreateLogStream`, `logs:PutLogEvents` on its own log group).

**Act 2 -- ONE DRY-RUN event, the first run.** After Act 1's after-read, the applier invokes the function ONCE, synchronously (`RequestResponse`, `--cli-read-timeout 0`, no async retry), with payload `{"day": "2026-10-14", "dry_run": true}`. A dry run builds the day's rows from the real inputs and writes NOTHING and chains NOTHING. **Branch A expected:** `result.rows` and `result.households` above 0, `dry_run` true, `returns_from` "2026-07-10", `contract` `{"contract_version": "0.3.0", "method_version": 2}`, `unreported_days` exactly the three trading days 2026-08-19, 2026-09-24 and 2026-09-25 and `statement` "3 trading days not reported by the source (2026-08-19, 2026-09-24, 2026-09-25)". A run that returns these proves, on the real runtime, that the layer's pyarrow loads and reads the Black Diamond partitions (the receipt below). The after-read LISTs the filled prefix and finds 0 objects.

**Act 3 -- the first real event.** Only after Act 2 passes: ONE synchronous event `{}` (no day). The handler builds the oldest day owed (2026-07-10, the floor) and chains the next owed days by asynchronous self-invoke, at most 10 days in all (`MAX_DAYS_PER_FIRE`). Each day writes ONE object, `irpt/cottonwood/gold/filled_report_values/date=<day>/data.parquet`, once, never over an existing key. The after-read counts the objects, reads the REPORT lines (`Max Memory Used`, duration) of every invocation of the chain, and checks that each `FILLED_SKIPPED` names one of the three absent days or 2026-07-10 with its reason.

**Act 4 -- the rest of the backfill.** Only after Act 3's after-read passes: further `{}` events, one at a time, each after the previous chain has ended and its after-read is recorded, until a response reads `NOTHING_OWED`. Expected end state: at most 65 objects (68 trading days from 2026-07-10 to 2026-10-14, less the three absent days; fewer only for a day the handler itself refuses, each named by `FILLED_SKIPPED`). A day that failed as the last day of a chain is retried by the next event; a day that failed before a landed day is not revisited (the handler never fills an absent day).

**NOT in this packet:** enabling the schedule (a separate change to `schedule.tf`, `DISABLED` to `ENABLED`, under its own ledger and the CTO's word); any change to the 49 Financial roots; any change to a Cottonwood input table; any portal reader of the new partitions; a sidecar of any kind.

## 2. Pins

Code at tree `002a88bdc3` or later on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `iam.tf` `0f5b9648df14` (6,956), `lambda.tf` `01da26d8bfb8` (2,932), `locals.tf` `f8d1c2effd9b` (2,969), `main.tf` `4252e4fe46c1` (1,808), `schedule.tf` `a19d6de6db84` (2,040), `handler.py` `e36e3155acb2` (18,981; round 137, which adds the unreported-day statement to round 135's contract guard). The source-map entry holds 18 staged members, each pinned to a full commit and hashed, plus `handler.py` from its source directory. **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `NGt2VnH3GioITy+bGudgPiiSGCluX7wvz3MGb3nR6Es=` (180K); the applier's real build must print the same value or STOP and say why.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-reporting-gold-lambda`: ABSENT (`ResourceNotFoundException`). **Execution role** and **scheduler role**: ABSENT (`NoSuchEntity`). **Schedule** `irpt-cot-reporting-gold-daily`: ABSENT. **Log group** `/aws/lambda/irpt-cot-reporting-gold-*`: 0 found. **Artifact** `investor-reporting/irpt-cot-reporting-gold-lambda.zip` in `opal-313476888478-lambda-artifacts`: ABSENT (404): the key's first object, so there is no previous version to roll back to.
- **Layer** `irpt-performance-native-layer`: latest version 1, python3.12; the sibling `irpt-cot-account-dim-lambda` runs python3.12 on exactly version 1.
- **Filled prefix** `irpt/cottonwood/gold/filled_report_values/` in `opal-data-cottonwood`: **EMPTY** (0 objects, LIST by this seat). This is a new prefix, so nothing existing can be overwritten.
- **Inputs.** `account_dim/`: partitions through 2026-10-14 (the handler reads the newest one's households, by design). `account_return_daily/date=2026-10-14/`: `data.parquet` and `manifest.json` both present; the table's Black Diamond era runs 2026-07-10 to 2026-10-14 with three trading days absent at the source (2026-08-19, 2026-09-24, 2026-09-25; read record `RD_COT_ABSENT_DAYS_READ_R136.json`).
- **Open ledgers.** None names this root. `irpt-dashbd-cottonwood-schedule-enable-20261015` (the landing schedule) stays open to tomorrow's first fire and is a different root.

## 4. What each act changes in the world

- **Act 1:** nothing served moves; seven resources are created, none writes anything; the schedule is DISABLED.
- **Act 2:** nothing: a dry run writes no object and chains no call.
- **Act 3 and 4:** new objects in an EMPTY prefix, one per trading day, each created once. Whether any served reader opens this prefix is the portal's and `2.0.0_SA_COO~P2`'s question; no reader is established by this seat.

## 5. Writers of the changed property, counted

The property is the content of `irpt/cottonwood/gold/filled_report_values/`. **After Act 1, ONE rule in this pair writes it: `build_day` (handler), whose `put_object` is the only PutObject in the function and the only PutObject statement in its role.** Entry paths: an explicit `day` event, a `{}` event, the chain's self-invoke and the schedule (DISABLED). N = 1 rule, 4 entry paths. Read: the repo's `.tf` files naming `filled_report_values` are this root and the 49 Financial reporting-gold root, which writes ANOTHER firm's bucket. Not established: any operator who wrote this prefix by hand; the LIST shows it empty.

## 6. Both branches (Acts 2 to 4)

- **Branch A:** as Act 2 and Act 3 state it; the after-read records the REPORT line's `Max Memory Used` and duration against 1,024 MB and 900 s, the object count, and the `FILLED_SKIPPED` lines.
- **Branch B (a day writes nothing):** the day is landed already (no-op `LANDED`), a refusal (no rows, an input absent, a contract mix) prints `FILLED_SKIPPED <day> <reason>` and returns `failed`; no object is written for that day and the chain goes on. The three absent days are expected in this branch.
- **Branch C (no half-partition):** a day is ONE object written by one `put_object`, so there is no half state. A retried asynchronous invocation re-checks `head_object` and finds the day landed.
- **Branch D (out of memory or time):** `Runtime.OutOfMemory` or `Task timed out` before the put: nothing is written for that day. The local peak was 408 MB (python 3 on Windows, pandas, pyarrow and boto3 loaded); the Lambda is python3.12 and is **unmeasured**: the line is 70 percent of 1,024 MB, 717 MB. If Act 2's or Act 3's `Max Memory Used` exceeds 717 MB, Act 3 or Act 4 does not start, and the next change is the single `memory_size` line, one standard size up, in its own pair.
- **Branch E (the chain breaks):** the self-invoke is asynchronous with the Lambda default of two retries. If an invocation dies, the chain stops there; the next `{}` event resumes at the oldest day owed. A failed `chain_next` is printed (`FILLED_CHAIN_FAILED`) and returned.
- **The plan is not the world.** `terraform plan` has NEVER been run for this root. The applier's plan is the first reading; the gate above is the check.

## 7. Rollback, per key

- **Seven resources:** a `safe-apply` destroy of this one root's seven resources by the applier, with the CTO's word (they hold no data). **Artifact:** the zip is the key's first object; remove it by a listed-key delete with the CTO's word, or leave it.
- **Filled objects written by Acts 3 and 4:** each is removed ONLY by an explicit listed-key delete with Andrew's word; never a wildcard prefix delete. The prefix was empty, so the rollback of the whole act is the listed keys the ledger records.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-cottonwood-reporting-gold-20261015` with legs L1 git (the tree commit and the sha256 of each file in section 2), L2 build (the build line equal to section 2's value), L3 terraform (the plan 7/0/0 on the seven addresses, then the apply, recorded by `infra/aws/lambda/ci/record-terraform-deploy.sh`), L4 dry run (Act 2 and its after-read), L5 backfill (Acts 3 and 4, one sub-leg per event). Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE before the apply. **Live state re-read at the moment of the apply** and equal to section 3 (function, roles, schedule, log group and artifact absent; filled prefix empty), else STOP. **Step 0 of Act 1:** read the layer live (latest version, compatible runtimes, that its zip holds `python/pyarrow/__init__.py` and its pyarrow version), and confirm it is the version the sibling function runs; else STOP.
3. **Act 3 and each Act 4 event** only after the previous leg's after-read is recorded in the ledger; the payload and the returned body are quoted by counts and words. **Stop at once** on a `Max Memory Used` above 717 MB, a `Task timed out`, a PutObject `AccessDenied`, or a `FILLED_SKIPPED` naming a day other than the three absent days or 2026-07-10.
4. **Nothing named here is enabled:** the schedule stays DISABLED through all four acts.
5. **No `update-function-code`, no bare `terraform apply`, no wildcard delete.** The applier is an AE seat the gates admit, not a worker.
6. **The receipt (the CTO's request).** After Act 2 passes, this seat sends the receipt to `1.0.0_SA_CTO~DELL1` through the MSTR relay `0.0.0_AB_MSTR~DELL2`: the dry run's returned counts and statement, the `Max Memory Used`, the duration, and the words "the layer's pyarrow loaded and read the Black Diamond partitions on python3.12". It is the ADVI_COTBKF un-park evidence the CTO owes.

## 9. Questions for the CTO's half

1. **A dry run first, then the real events, in this pair?** The round analysis names the deploy and a first run that proves the 14.0.2 load; this packet makes that run a DRY run (no write) and covers the backfill as Acts 3 and 4 under the stop conditions above. Accept, or cover Acts 1 and 2 only and take the backfill as its own word?
2. **The python3.12 memory** is unmeasured: accept 1,024 MB with Act 2's `Max Memory Used` as the first reading and the one-line raise as the remedy?
3. **Households as of the newest `account_dim`** for every backfilled day (the handler's design, measured in the local feasibility run): accept for the backfill, or hold Act 4?

## 10. Not established, and so not covered

A `terraform plan`; the function's real memory and time on python3.12; whether the new role can read every input object (the role policy is the grant; Act 2 is the first reading); whether any served reader opens the new partitions; how the served report prints the unreported-day statement (a report-contract change not made here); the value of any backfilled day beyond the CVO's 07-13 and 10-14 return-level grade on the landing table.

-- 2.0.0_SA_COO~D2
