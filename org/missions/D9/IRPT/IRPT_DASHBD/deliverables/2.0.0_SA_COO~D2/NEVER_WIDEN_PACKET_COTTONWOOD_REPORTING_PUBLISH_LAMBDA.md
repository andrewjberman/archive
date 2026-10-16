# NEVER-WIDEN PACKET -- the first Cottonwood series publish (IRPT_DASHBD round 147, workstream B-49F + contract): ONE new Terraform root, FOUR new resources, a DRY-RUN event, a ONE-ACCOUNT upload, then the full upload of the series and manifests

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~04:2xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, PRD ADDENDUM v0.16 item 4 and the boundary ruling (msg 8803: "The first Cottonwood series publish is ~D2's cell, under its own pair and in one drain with the contract field").
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_LAMBDA_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is applied and no event is invoked until both halves are SIGNED on one sha256.**

## 1. The acts (four, in order; each has its own stop)

**Act 1 -- build, upload, apply.** The AE applier builds the bundle of `irpt-cot-reporting-publish-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-reporting-publish-lambda` (the source-map entry is pinned and hashed by `DB-b-281`; the applier writes nothing into the map except the two fields the upload script itself writes), then ONE Terraform apply of `infra/aws/terraform/investor-reporting/reporting-publish-iso/` through `.tools/safe-apply.sh` (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 4 to add, 0 to change, 0 to destroy, on exactly these four addresses; any other line STOPS the act:**

| address | what it is |
|---|---|
| `module.irpt_reporting_publish_iso.aws_lambda_function.this` | `irpt-cot-reporting-publish-lambda`: python3.12, `handler.lambda_handler`, timeout 900, **memory 1024**, no reserved concurrency, no environment variable, **one layer: `irpt-performance-native-layer` (a data source; not a plan line)**, artifact key `investor-reporting/irpt-cot-reporting-publish-lambda.zip` |
| `module.irpt_reporting_publish_iso.aws_cloudwatch_log_group.lambda` | its log group, retention 14 days |
| `aws_iam_role.irpt_reporting_publish_iso_execution` | `irpt-cot-reporting-publish-execution-role` (matches the Cottonwood bucket policy's `role/*-cot-*` admission) |
| `aws_iam_role_policy.irpt_reporting_publish_iso_execution` | `irpt-cot-reporting-publish-execution-policy`: five statements, explicit actions, no wildcard action, no delete, no lambda action (below) |

There is **no schedule, no scheduler role, no event rule, no topic and no mail**: the function is invoked by hand.

**The execution policy's five statements (read line by line from `iam.tf`):** `ListGoldReturnsAndPlatinumReportingOnly` (`s3:ListBucket` on `opal-data-cottonwood` under `s3:prefix` `irpt/cottonwood/gold/account_return_daily/*` and `irpt/cottonwood/platinum/reporting/*`); `ReadGoldReturnsOnly` (`s3:GetObject` on `irpt/cottonwood/gold/account_return_daily/*`, no other gold table); `WriteThePlatinumReportingPrefixOnly` (`s3:PutObject` on `irpt/cottonwood/platinum/reporting/*`, the ONLY PutObject statement); `ReadBackThePlatinumReportingPrefixOnly` (`s3:GetObject` on the same prefix, for the size read-back); `OwnLogStreamOnly` (`logs:CreateLogStream`, `logs:PutLogEvents` on its own log group). Plus the assume-role document `ExecutionRoleAssumedByLambdaService`.

**Act 2 -- ONE DRY-RUN event, the first run.** After Act 1's after-read, the applier invokes the function ONCE, synchronously (`RequestResponse`, `--cli-read-timeout 0`), with payload `{}` (the default is a dry run: it reads and builds and writes NOTHING). **Branch A expected:** `uploaded` false; `floor` "2026-07-10"; `first` "2026-07-10"; `partitions` the count of gold date partitions from the floor to the newest (65 at 2026-10-14); `accounts_seen` about 979 (the 2026-10-14 read; the run re-measures); `published` plus `refused` equal `accounts_named`; every `refusals` key a reason text with its count; `skipped_null_account` a whole number; and `unreported_trading_days` exactly the trading days from 2026-07-10 to the newest partition with no partition, which at 2026-10-14 are 2026-08-19, 2026-09-24 and 2026-09-25 (the report-build function's own list, read record `RD_COT_ABSENT_DAYS_READ_R136.json`). The after-read reads the REPORT line's `Max Memory Used` and duration. **Stop** if `refused` exceeds 10 percent of `accounts_named`, if any refusal reason is not recorded, or on any error.

**Act 3 -- ONE-ACCOUNT upload.** Only after Act 2 passes: ONE synchronous event `{"upload": true, "accounts": ["<one id>"]}`. The applier picks ONE account whose first value day is 2026-07-10 (the first account, sorted, among those in the floor partition) and records only the first 12 hex of the sha256 of its id in the ledger, never the id. It writes two objects, `irpt/cottonwood/platinum/reporting/account=<id>/series.json.gz` and `manifest.json`. **After-read:** both keys exist; the stored `series.json.gz` size equals the manifest's `byte_sizes`; the decompressed series validates against the series contract 0.3.0 (`required` keys, equal-length arrays, the pair present, `unreported_trading_days` exactly the three days of Act 2, `unreported_trading_days_basis` the fixed text, `income` all null); the manifest's `firm` is the registry-derived firm and `publisher_version` is "0.2.0".

**Act 4 -- the full upload.** Only after Act 3's after-read passes: ONE synchronous event `{"upload": true}`. It writes the series and manifest of every account that builds (at most `published` of Act 2, so at most about 2 x 979 objects). The after-read counts the objects under the prefix, equal to 2 x `published`, samples ten series (by sorted position, recorded as hash prefixes) against the Act 3 checks, and reads `Max Memory Used` and duration.

**NOT in this packet:** any schedule or automatic run (the CTO's separate word); any change to the 49 Financial roots or to a Cottonwood input table; any portal or other reader of the new prefix; the class object (`class_series.json.gz`, a later contract and cell); deleting any object.

## 2. Pins

Code at tree `8dce40fd77` or later on `box/dell2` (LOCAL); the merge `220c9c63f3` landed chain B with the series contract. sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `iam.tf` `2f4e40b2a667` (4,193), `lambda.tf` `4b06e81c4119` (2,708), `locals.tf` `fb2e7936b6d0` (2,691), `main.tf` `5b49dd311dbf` (1,844), `reporting-publish-cot/handler.py` `d201d6fee1d7` (7,289), `reporting-publish/publisher.py` `6cb94a9281f7` (28,468), `org/standards/IRPT_DASHBD_SERIES_CONTRACT.json` `09e98980902d` (14,535; version 0.3.0). The source-map entry holds 12 staged members (each pinned and hashed) plus `handler.py`. **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `HDgIzQoXMyUNBxeyqgLXcplD1c01QwVsASRoMJbd4hk=`; the applier's real build must print the same or STOP.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-reporting-publish-lambda`: ABSENT. **Execution role** and its **policy**: ABSENT (`NoSuchEntity`). **Log group** `/aws/lambda/irpt-cot-reporting-publish-lambda`: 0 found. **Artifact** `investor-reporting/irpt-cot-reporting-publish-lambda.zip` in `opal-313476888478-lambda-artifacts`: ABSENT, the key's first object, so there is no previous version to roll back to.
- **Layer** `irpt-performance-native-layer`: latest version 1, python3.12 (the version the sibling Cottonwood functions run).
- **Target prefix** `irpt/cottonwood/platinum/reporting/` in `opal-data-cottonwood`: **EMPTY** (0 objects, LIST by this seat). The platinum tables present are `holdings/` and `holdings_qa/`; `reporting/` is new, so nothing existing can be overwritten.
- **Input.** `gold/account_return_daily/` for the floor era (2026-07-10 to 2026-10-14): 65 date partitions, 52,468 rows, 979 accounts, `market_value_eod` and `external_flow` present on every row, `income_received` null on every row (the Black Diamond-computed method states no income; row IRPT_DASHBD-D2-S104; the series carries it as null, never 0.0).

## 4. What each act changes in the world

- **Act 1:** nothing served moves; four resources are created, none writes anything; no schedule exists.
- **Act 2:** nothing: a dry run writes no object.
- **Act 3 and 4:** NEW SERVED OUTPUT: objects in an EMPTY prefix, two per published account. Whether any reader opens `platinum/reporting/` for this firm is not established by this seat: the deployed reporting read function is the 49 Financial one; the portal reads series through its own path (`~C2`'s cell (a) is built against a fixture and exercised on this publish).

## 5. Writers of the changed property, counted

The property is the content of `irpt/cottonwood/platinum/reporting/`. **After Act 1, ONE rule in this pair writes it: the handler's `put_object` (the only PutObject in the function and the only PutObject statement in its role).** Entry paths: a hand invocation only (no schedule, no event). N = 1 rule, 1 entry path. Read: the repo's `.tf` files naming a platinum `reporting` prefix are this root and the 49 Financial `reporting-publish` root, which writes another firm's bucket. Not established: any operator who wrote this prefix by hand; the LIST shows it empty.

## 6. Both branches (Acts 2 to 4)

- **Branch A:** as Acts 2 to 4 state it.
- **Branch B (an account refuses):** `build_series` or the contract guard refuses it (for example no positive market value): it is counted by reason, nothing is written for it, the run goes on; refusals above 10 percent STOP at Act 2.
- **Branch C (no half-state):** an account's series is written before its manifest; a run that dies between them leaves a series without its manifest for that account until the event is run again (a re-run rewrites both, same bytes for the series, a new `built_at` in the manifest). The reader contract names both files; the after-read counts each.
- **Branch D (out of memory or time):** `Runtime.OutOfMemory` or `Task timed out`: nothing further is written; the local figures are small (about 52,000 rows, 65 partitions) but the Lambda is python3.12 and **unmeasured**: the line is 70 percent of 1,024 MB, 717 MB. If Act 2's `Max Memory Used` exceeds 717 MB, Act 3 and 4 do not start and the next change is the single `memory_size` line, in its own pair. The 900 s ceiling is the same stop.
- **Branch E (the run is repeated):** the handler overwrites an account's two keys with the same series bytes; acceptable inside the prefix this pair owns, stated so it is not a surprise.
- **The plan is not the world.** `terraform plan` has NEVER been run for this root. The applier's plan is the first reading; the gate above is the check.

## 7. Rollback, per key

- **Four resources:** a `safe-apply` destroy of this one root's four resources by the applier, with the CTO's word (they hold no data). The zip is the key's first object; deleting it is an S3 delete and so Andrew's act; it is inert once the function is destroyed, so it is LEFT.
- **Objects written by Acts 3 and 4:** each is removed ONLY by an explicit listed-key delete with Andrew's word; never a wildcard prefix delete. The prefix was empty, so the rollback of the whole act is the listed keys the ledger records (counts and the hash prefixes of the sampled ones).

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-cottonwood-reporting-publish-20261016` with legs L1 git (the tree commit and each file's sha256), L2 build (the build line equal to section 2's), L3 terraform (the plan 4/0/0 on the four addresses, then the apply, recorded by `infra/aws/lambda/ci/record-terraform-deploy.sh`), L4 dry run (Act 2), L5 canary (Act 3), L6 full upload (Act 4). Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE before the apply. **Live state re-read at the moment of the apply** and equal to section 3, else STOP. **Step 0 of Act 1:** read the layer live (latest version, compatible runtimes, pyarrow in its zip) and confirm it is the version the sibling functions run, else STOP.
3. **Each event only after the previous leg's after-read is recorded in the ledger;** payloads and returned bodies are quoted by counts and words, never by an account id. **Stop at once** on a `Max Memory Used` above 717 MB, a `Task timed out`, a PutObject `AccessDenied`, or a refusal reason not recorded at Act 2.
4. **Nothing named here is scheduled or enabled.**
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object.** The applier is an AE seat the gates admit, not a worker.
6. **A receipt** after Act 4: counts, memory, duration, the object count, the Act 3 checks, and the words "NOT a page render" and "no reader of the prefix established".

## 9. Questions for the CTO's half

1. **A one-account canary, then the full upload, in this pair?** Accept, or cover Acts 1 and 2 only and take the uploads as their own word.
2. **The python3.12 memory** is unmeasured: accept 1,024 MB with Act 2's `Max Memory Used` as the first reading and the one-line raise as the remedy?
3. **Series for every account in the floor-era gold (about 979), including accounts the page may never open:** accept (the prefix is new and read by no established reader), or limit Act 4 to a named set?

## 10. Not established, and so not covered

A `terraform plan`; the function's real memory and time on python3.12; whether the new role can read every input object (Act 2 is the first reading); which reader will open `platinum/reporting/` for this firm and how it prints the unreported-day statement (`~C2`'s cell); the value of any published series beyond the checks above; the trading calendar's source on the Lambda (the repo calendar answers from its hardcoded NYSE fallback when `pandas_market_calendars` is absent, as it does in the worker's box; row W226-S1; the three expected days are checked against the report-build function's own list at Act 2).

-- 2.0.0_SA_COO~D2
