# NEVER-WIDEN PACKET -- the Cottonwood account-return landing function to the cloud (IRPT_DASHBD rounds 120 to 126, workstream B-49F): ONE new Terraform root, SEVEN new resources, ONE explicit first event into an occupied gold prefix

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-15 ~15:3xZ (REVISION 3).
**Revision 3 supersedes revision 2 (sha256 `a1b080c5fe06...`, both halves now VOID) and revision 1 (`c63702ade4df...`, VOID).** Revision 3 changes ONE thing from revision 2: the AE applier's `safe-apply` was refused by the naming-plan gate (rc 7, nothing written, msg 8351) because the scheduler role's inline policy took the ROLE's name; round 129 `DB-b-261` (merged `039c4807c5`) gives it its own builder name `irpt-cot-account-return-daily-scheduler-policy`, and the real gate in plan mode now grades the six named resources CONFORMANT (`DB129-1-AC2`, `AC3` PASS on the landed tree). The plan stays 7/0/0; `iam.tf` hashes `be6fe3f38597`. Revision 2's text follows, unchanged except where marked.
**Revision 2 supersedes revision 1 (sha256 `c63702ade4df...`, both halves now VOID).** Revision 1 described a function with no Lambda layer; the adapter imports pyarrow at module level and the python3.12 runtime carries no pyarrow (row `IRPT_DASHBD-D2-S84`, found by this seat before any apply). Round 127 `DB-b-259` (merged `54e4a0036a`) adds the read-only data source for the existing `irpt-performance-native-layer` and one `layers` line. Everything else in revision 1 is unchanged except the pins, the live state and the conditions marked below, and the CTO's added condition (msg 8287) is condition 2. **Ordered by:** 1.0.0_SA_CTO~DELL2, CTO round-120 analysis @5e358b0a8f (landing facts), round-124 @4285776c5c ruling 1 (the guard and the floor), round-126 @2cf3e13682 ruling 1 (the pair at 1,024 MB; one 2026-07-10 event first, then explicit `days`, never a day at or before 2026-06-22; the schedule DISABLED until the after-read).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is applied and no event is invoked until both halves are SIGNED on one sha256.**

## 1. The acts (three, in order; each has its own stop)

**Act 1 -- build, upload, apply.** The AE applier `0.7.0_AE_CloudOps~DB2` builds the bundle of `irpt-cot-account-return-daily-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-return-daily-lambda` (the source-map entry is fully pinned and hashed by `DB-b-257`, so the applier writes NOTHING into the map except the two fields the upload script itself writes, `artifact_s3_key` unchanged and `artifact_sha256`), then ONE Terraform apply of `infra/aws/terraform/investor-reporting/account-return-daily/` through `.tools/safe-apply.sh` (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 7 to add, 0 to change, 0 to destroy, on exactly these seven addresses; any other line STOPS the act:**

| address | what it is |
|---|---|
| `module.irpt_account_return_daily.aws_lambda_function.this` | `irpt-cot-account-return-daily-lambda`: python3.12, `handler.lambda_handler`, timeout 900, **memory 1024**, reserved concurrency 1, no environment variable, **one layer: `irpt-performance-native-layer` (read by a data source, which creates nothing and is not a plan line; it resolves to the layer's latest version, 1 at packet time)**, artifact key `investor-reporting/irpt-cot-account-return-daily-lambda.zip` |
| `module.irpt_account_return_daily.aws_cloudwatch_log_group.lambda` | its log group, retention 14 days |
| `aws_iam_role.irpt_account_return_daily_execution` | `irpt-cot-account-return-daily-execution-role` (matches the Cottonwood bucket policy's `role/*-cot-*` admission) |
| `aws_iam_role_policy.irpt_account_return_daily_execution` | `irpt-cot-account-return-daily-execution-policy`: five statements, explicit actions, no wildcard action, no delete (below) |
| `aws_iam_role.irpt_account_return_daily_scheduler` | `irpt-cot-account-return-daily-scheduler-role` |
| `aws_iam_role_policy.irpt_account_return_daily_scheduler` | named `irpt-cot-account-return-daily-scheduler-policy` (revision 3: its own builder name); `lambda:InvokeFunction` on the one function ARN |
| `aws_scheduler_schedule.irpt_account_return_daily` | `irpt-cot-account-return-daily-daily`, `cron(15 8 ? * MON-FRI *)` America/New_York, **state DISABLED** |

**The execution policy's five statements (recounted from `iam.tf`):** `ListSilverTablePrefixesOnly` (`s3:ListBucket` on `opal-data-assets` under `s3:prefix` `blackdiamond/cottonwood/silver/fact_allocations/*` and `.../fact_transactions/*`); `ReadTwoBlackDiamondSilverTablesOnly` (`s3:GetObject` on those two prefixes); `WriteTheOneAccountReturnDailyGoldPrefixOnly` (`s3:PutObject` on `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/*`, the ONLY PutObject statement); `ListTheOneAccountReturnDailyGoldPrefixOnly` (`s3:ListBucket` on `opal-data-cottonwood` under `s3:prefix` `irpt/cottonwood/gold/account_return_daily/*`, which the no-overwrite guard needs); `OwnLogStreamOnly` (`logs:CreateLogStream`, `logs:PutLogEvents` on its own log group).

**Act 2 -- ONE real event.** After Act 1's after-read, the applier invokes the function ONCE, synchronously (`RequestResponse`, no async retry), with payload `{"day": "2026-07-10"}`. The handler's floor is 2026-07-10; the adapter's guard LISTs the day partition first and refuses with no put if either key exists. It writes ONE new partition: `irpt/cottonwood/gold/account_return_daily/date=2026-07-10/data.parquet` then `manifest.json` (two puts, data first).

**Act 3 -- catch-up, explicit `days` events.** Only after Act 2's after-read PASSES: events `{"days": [...]}` of at most 25 trading days each, naming ONLY days after 2026-07-10 and at or before the newest Black Diamond silver partition the applier reads at that moment; oldest first; one after-read per event. The handler refuses any day before the floor, more than 25 days, or a day whose partition exists, before any write.

**NOT in this packet:** enabling the schedule (a separate change to `schedule.tf`, `DISABLED` to `ENABLED`, under its own ledger and the CTO's word after Act 3); any day at or before 2026-06-22 (never); any change to the 3,325 existing partitions; any other root.

## 2. Pins

Code at or after trunk merges `1e8ac2180e` and `1e78f951eb` (`box/dell2`, LOCAL; this revision was written with the tree at `039c4807c5`, which also carries `DB-b-259` and `DB-b-261`). sha256 (first 12 hex) and bytes of the files at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `iam.tf` `be6fe3f38597` (6,756), `lambda.tf` `736826f6e6d8` (3,647), `locals.tf` `8414bb4980d4` (2,824), `main.tf` `72245428da82` (1,674), `schedule.tf` `0f8fd4e67d01` (2,038), `handler.py` `ee037720618a` (6,885), the adapter `73a94a06a296` (27,357). The source-map entry holds 15 staged members, each pinned to a full commit and hashed (15 distinct commits; `DB126-1-AC2` PASS on the landed tree). **The build-only package** (`BUILD_ONLY=1`, nothing uploaded; rebuilt at `54e4a0036a`: unchanged, the layer is not in the zip) has 16 members and base64 sha256 `fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs=`; the applier's real build must print the same value or STOP and say why.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-account-return-daily-lambda`: ABSENT (`ResourceNotFoundException`). **Execution role** `irpt-cot-account-return-daily-execution-role`: ABSENT (`NoSuchEntity`). **Schedule** `irpt-cot-account-return-daily-daily`: ABSENT. **Artifact** `investor-reporting/irpt-cot-account-return-daily-lambda.zip` in `opal-313476888478-lambda-artifacts`: ABSENT (404), so this is the key's first object and there is no previous version to roll back to.
- **Layer** `irpt-performance-native-layer` (read by this seat): latest version 1, compatible runtime python3.12, about 70 MB; the sibling `irpt-cot-account-dim-lambda` runs python3.12 on exactly version 1 (`DB127-1-AC2`, `AC3` PASS on the landed tree: the bundle's import-time third-party imports are pyarrow plus the runtime's boto3/botocore, and the layer's zip holds `python/pyarrow/__init__.py`).
- **Gold prefix** `irpt/cottonwood/gold/account_return_daily/` in `opal-data-cottonwood`: **OCCUPIED, 3,325 date partitions, first 2013-04-03, last 2026-06-22** (LIST by this seat). The guard and floor make the occupied prefix safe for the days after it; they are the reason this pair exists in this shape.
- **Bucket policies.** `opal-data-cottonwood`: four statements; `DenyForeignFirmPrincipals` admits `role/*-cot-*` (the new roles match) plus named human and operator principals; the restricted-prefix denies name only `commonwealth/cottonwood/bronze/crm/`. `opal-data-assets` (the silver bucket): two statements, neither a principal deny; the role's own policy is the grant.
- **Silver.** The two Black Diamond silver tables hold `fact_allocations`/`fact_transactions` partitions from 2026-07-10 (the day measured at round 125) through the newest listed day; the gap 2026-04-25 to 2026-07-09 is empty and is why the floor exists.
- **Open ledgers read:** `irpt-dashbd-cottonwood-account-dim-20261015` and `irpt-dashbd-cottonwood-holdings-performance-20261015` (other Cottonwood roots, not this one) and `irpt-dashbd-hop1-filled-report-values-20261015` (open at L6 to tomorrow's fire, the 49 Financial reporting-gold root). None names this root.

## 4. What each act changes in the world

- **Act 1:** nothing served moves; seven resources are created, none of them writes anything; the schedule is DISABLED.
- **Act 2:** ONE new partition (two objects) at `date=2026-07-10` of a prefix whose newest existing partition is 2026-06-22. Nothing existing is overwritten (the guard). Whether any served reader opens this prefix is the portal's and `2.0.0_SA_COO~P2`'s question; no reader of the new partition is established by this seat.
- **Act 3:** the same, one new partition per trading day named, none existing.

## 5. Writers of the changed property, counted

The property is the content of the Cottonwood gold prefix `account_return_daily`. **After Act 1, ONE rule in this pair writes it, `write_day` (adapter), entered by three paths:** an explicit `day` event, an explicit `days` event, and the schedule (DISABLED). Terraform grants no other principal a write on the prefix (read: the repo's `.tf` files that name `account_return_daily` are this root and the 49 Financial roots, which write another firm's bucket). **Not established:** the 3,325 history partitions were written by an operator path (the producer run by a named human or operator principal that the bucket policy admits); that path has no scheduled entry in the repo, and this pair neither uses nor changes it. N = 1 rule in scope, 3 entry paths; the operator path is a second writer this seat cannot exclude.

## 6. Both branches (Acts 2 and 3)

- **Branch A:** the event returns the day written; `data.parquet` and `manifest.json` exist at the builder address; the after-read records the REPORT line's `Max Memory Used` and duration against 1,024 MB and 900 s, the partition's account and row counts, and the `source` column in words.
- **Branch B (the event writes nothing):** the guard refuses (a key exists); the silver presence hold returns the day held (an input absent); the day is before the floor. In each the function returns the reason and writes no object.
- **Branch C (the invocation dies between the two puts):** `data.parquet` exists and `manifest.json` does not. The guard then REFUSES a re-run of that day (either key exists), so the half partition stays until an **explicit listed-key delete of that one object with Andrew's word**. Chance is low (two puts in one call) and the run is synchronous, so the applier sees the failure at once.
- **Branch D (out of memory or time):** the invocation reports `Runtime.OutOfMemory` or `Task timed out`; before the puts nothing is written. The measured peak was 654.5 MB (2026-07-10) and 547.7 MB (2026-10-13), under 70 percent of 1,024 MB (717 MB). **The measurement ran on Python 3.14 on Windows; the Lambda is python3.12 (row `W210-S2`, ARMED, disarm owner this seat):** if Act 2's `Max Memory Used` exceeds 717 MB the next change is the single `memory_size` line, one standard size up, in its own pair; no Act 3 event runs before that is read.
- **The plan is not the world.** `terraform plan` has NEVER been run for this root (the box this seat works on has no terraform binary). The applier's plan is the first reading; the gate above is the check.

## 7. Rollback, per key

- **Seven resources:** a `safe-apply` destroy of this one root's seven resources by the applier, with the CTO's word (they hold no data). **Artifact:** the zip is the key's first object; remove its version by a listed-key delete with the CTO's word, or leave it (an unreferenced artifact does nothing).
- **Gold partitions written by Acts 2 and 3:** each is removed ONLY by an explicit listed-key delete (both objects of the day) with Andrew's word; never a wildcard prefix delete. The 3,325 history partitions are never touched by any act here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-cottonwood-account-return-daily-20261015` with legs L1 git (the tree commit and the sha256 of each file in section 2), L2 build (the build line equal to section 2's sha256), L3 terraform (the plan 7/0/0 on the seven addresses, then the apply, recorded by `infra/aws/lambda/ci/record-terraform-deploy.sh`), L4 event (Act 2 and its after-read), L5 catch-up (Act 3, one sub-leg per event). Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate (revision 3):** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE, 6 named resources CONFORMANT, before the apply. **Live state re-read at the moment of the apply** and equal to section 3 (function, roles, schedule and artifact absent; gold prefix 3,325 partitions last 2026-06-22), else STOP. **Added by the CTO (msg 8287), step 0 of Act 1:** read the layer `irpt-performance-native-layer` live (its latest version, its compatible runtimes, and that its zip holds `python/pyarrow/__init__.py`) and confirm it carries pyarrow for python3.12 and is the version the sibling function runs; if not, STOP. The plan stays 7/0/0 and the function's `layers` attribute names the layer.
3. **Act 2 and each Act 3 event** only after the previous leg's after-read is recorded in the ledger; the event payload and its returned body are quoted in the ledger by counts and words.
4. **Nothing named here is enabled:** the schedule stays DISABLED through all three acts.
5. **No `update-function-code`, no bare `terraform apply`, no wildcard delete.** The applier is an AE seat the gates admit, not a worker.

## 9. Questions for the CTO's half

1. **Acts 2 and 3 in this pair?** The round-126 ruling names the first event and the explicit `days` that follow; this packet covers both under the conditions above (Act 3 only after Act 2's after-read, 25 days at most per event, each after-read recorded). Accept, or cover Act 2 only and take Act 3 as its own word?
2. **The python3.14 versus python3.12 gap** (row `W210-S2`): accept 1,024 MB with Act 2's `Max Memory Used` as the first reading and the one-line raise as the remedy?
3. **The operator writer** (section 5): accept that the prefix's history was written by a path this pair neither changes nor excludes, with the guard and the floor as the protection?

## 10. Not established, and so not covered

A `terraform plan`; the function's real memory and time on python3.12; the layer's pyarrow version against the one the adapter was measured with at round 125; whether the new roles can read the silver objects (the role policy is the grant; the first event is the first reading); whether any served reader opens the new partitions; the identity of every principal that has ever written the prefix.

-- 2.0.0_SA_COO~D2
