# NEVER-WIDEN PACKET -- the 49 Financial series publish: CODE UPDATE (publisher 0.4.0: the unreported-days statement and `calendar_source` for all 6,949 series, the history-scope pair where the gold carries it) and the REPUBLISH of the 6,949 series (IRPT_DASHBD round 149, cells DB-b-292 to DB-b-297)

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~11:5xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, msg 9224: "the 49 Financial publisher writes unreported_trading_days, an empty list where the gold has no absent trading day, plus its basis and calendar_source. It lands in one drain with any contract touch, then a republish of the 6,949 series under the 49 Financial publish pair (a new pair, which I sign)." The code and its contract landed in ONE drain (merge commits `9c46b7d536`, `55e3bfe49b`, `8430b776e6`, `96a89eb451`, `4c9c1e7af6`; the fifteen criteria DB160-1 to DB164-1 re-run PASS by this seat on the landed tree) and the entry `irpt-49f-reporting-publish-lambda` was re-pinned inside `DB-b-292` itself (12 stale pins moved, the calendar added; none stale at packet time).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The AE applier builds `irpt-49f-reporting-publish-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-49f-reporting-publish-lambda` (the source-map entry key; its `artifact_s3_key` is the scope-less `investor-reporting/irpt-reporting-publish-lambda.zip`, read from the map and never typed). The build-only hash is below (section 2); the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key `investor-reporting/irpt-reporting-publish-lambda.zip` in `opal-313476888478-lambda-artifacts` (versioned; the current version `4kEV9O.UMGs.NSGSYi_N4ZZjNm45rso4`, 178,060 bytes, is the rollback target) and updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-publish/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 1 to change, 0 to destroy:** `module.irpt_reporting_publish.aws_lambda_function.this`, by CODE attributes only (the artifact version and the code hash move; memory 1,024, timeout 300, handler, runtime, role, layer, no environment and no reserved concurrency stay as they are). Any other line, any other attribute, any destroy, STOPS the act. The daily schedule, its scheduler role and policy, the execution role and policy and the log group do not appear in the plan.

**Act 3 -- ONE synchronous DRY-RUN event on ONE shard** `{"dry_run": true, "shard": 0, "shards": 7}` (`RequestResponse`, `--cli-read-timeout 0`). It reads the gold and builds the shard's accounts (the shard is a stable hash of the account id, about a seventh of the 6,949) and writes NOTHING. Its response lists any refused account ids: **the applier records the COUNT only, never an id.** **Expected:** `ok` true, the shard's `accounts` about 990, `refused` 0 (the census of this seat, `reads/RD_GOLD49F_CENSUS_20261016.json`, found no account with income null on some days and a number on others, the one refusal rule the new publisher adds); Max Memory Used and duration inside the function's own limits (the line is 80 percent of memory and 240 s). A refusal count above 0 is READ and recorded and STOPS Act 5 until the CTO rules on its reasons.

**Act 4 -- ONE-ACCOUNT republish** `{"accounts": ["<one id>"]}` (the handler uploads unless `dry_run`; the id is the first account, sorted, of the newest gold partition; never recorded, only 12 hex of its sha256). Two objects at the SAME keys. **After-read:** the stored series validates against series contract 0.3.3 (read from the repo: the bundle does not package it); it carries `unreported_trading_days` as an EXPLICIT list (empty where the gold holds no absent trading day in the account's window) and `unreported_trading_days_basis` = "trading calendar minus present partitions", no `income_claim` (numeric income), and, because the gold is not rebuilt yet, NO history-scope pair; the manifest carries `calendar_source` (`pandas_market_calendars` or `fallback_2010_2027`, whichever answered), `publisher_version` "0.4.0" and the same firm; the prior version of each of the two keys is still present.

**Act 5 -- the FULL republish** `{}` (the scheduled fire's own event shape: it counts the accounts, finds 6,949 above 1,000 and invokes THIS function once per shard, 7 asynchronous `Event` invocations, then returns). The same prefix, the same keys. **After-read** (the applier waits until the log group shows the 7 shard `REPORT` lines, then lists and samples): the prefix still holds 6,949 series, 6,949 manifests and the 4,344 other objects (client summaries, untouched: the summaries pass is NOT run), no key added or removed; every series is newer than Act 4's; ten series sampled by sorted position (recorded as hash prefixes) pass Act 4's checks; the count of series carrying the unreported-days pair equals 6,949 and the count of manifests carrying `calendar_source` equals 6,949 (the sources that answered are named); the count of manifests at publisher 0.4.0 equals 6,949; the 7 `REPORT` lines show no `Task timed out` and no error and a Max Memory Used inside the limit.

**Act 6 -- the receipt** with the counts, the memory and duration of Acts 3 to 5, the Act 4 checks, and the words "NOT a page render", "no reader of the unreported-days statement is established" and "history scope NOT yet derived: the gold is rebuilt by a separate pair".

**NOT in this packet:** the 49 Financial `reporting-gold` code update and the `history_scope` rebuild of the gold (its own pair); the summaries pass; any change to the daily schedule (it stays ENABLED and untouched); the Cottonwood side; any reader; any delete of any object or version.

## 2. Pins

Code at tree `231f28c622` or later on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `reporting-publish/handler.py` `c73842705542` (32,920), `reporting-publish/publisher.py` `646d60254755` (33,301), `lib/trading_calendar.py` `9bc467c6ce4d` (13,887), `org/standards/IRPT_DASHBD_SERIES_CONTRACT.json` `b0fc0756d2a7` (19,741; version 0.3.3), and the Terraform root's `lambda.tf` `5ad22bd7874c` (2,714), `iam.tf` `dba0b88cca2b` (7,354), `locals.tf` `2a395f4fa68b` (3,995), `main.tf` `2c90c1ba1055` (1,612), `schedule.tf` `cb8fe49ef26f` (6,826; not in the plan). The source-map entry `irpt-49f-reporting-publish-lambda` holds the handler and publisher from its source_dir and 15 staged members (each pinned to a full commit and hashed; none stale at packet time). **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `SX0xYFZsxH4q6psJM56yAee9wRb6vrVUN4VrTV1ouU8=`.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-49f-reporting-publish-lambda`: PRESENT; CodeSha256 `AH5r60vpxR/Gt4RlpsSkhAw5HDths5P2Ht+Ix1CHlQ8=`; 1,024 MB; timeout 300 s; one layer (`irpt-performance-native-layer:1`); no environment; last modified 2026-10-03T17:22:27Z. **Artifact key:** current VersionId `4kEV9O.UMGs.NSGSYi_N4ZZjNm45rso4` (178,060 bytes, 2026-10-03T04:12:05Z); bucket versioning Enabled.
- **Schedule** `irpt-49f-reporting-publish-daily`: ENABLED, `cron(15 8 ? * MON-FRI *)` America/New_York (12:15Z in October), target the one function. **It keeps firing through this packet and is untouched.**
- **Target prefix** `irpt/49financial/platinum/reporting/` in `opal-data-49financial`: 6,949 series objects, 6,949 manifests and 4,344 other objects (client summaries); versioning Enabled; newest object 2026-10-15T12:46:03Z. Nothing in this packet reads or writes the 4,344 others.
- **Gold** (census @`eb3e36f6cd`, counts only): 571 partitions 2024-07-08 to 2026-10-14; 6,949 accounts; 2,852 first seen on the earliest partition and 4,097 later; 0 with mixed null and numeric income; 3 whose newest row is before the last partition.

## 4. What each act changes in the world

- **Act 1:** a new version of one artifact key; nothing served moves. **Act 2:** the function's code is replaced; the next invocation, scheduled or by hand, runs the new code. **Act 3:** nothing. **Acts 4 and 5:** the 6,949 series and 6,949 manifests are overwritten at the same keys, each with a new version (prior versions kept): the series gains the unreported-days pair, the manifest gains `calendar_source` and `publisher_version` 0.4.0. **Act 6:** reads only.

## 5. Writers of the changed property, counted

The property is the content of the series and manifest objects under the prefix. **ONE rule writes them: the handler's `put_object` in `_publish_one`** (the other put in the same function, `summary.json`, writes a different object kind). Entry paths: a hand invocation, the ENABLED daily schedule, and the shard fan-out of either. N = 1 rule, 3 entry paths. Not established: any operator who wrote this prefix by hand.

## 6. Both branches (Acts 3 to 5)

- **Branch A:** as the acts state it. **Branch B (an account refuses):** counted by reason and skipped; a refused account keeps its prior objects; any refusal STOPS Act 5 (see Act 3). **Branch C (a shard dies between an account's series and manifest):** the old manifest and the new series coexist for that account until the account is republished, which the next scheduled fire does; the reader contract names both files. **Branch D (out of memory or time):** nothing further is written by that shard; the line is 80 percent of memory and 240 s. **Branch E (the run is repeated, or the schedule fires during it):** same keys, same bytes except `built_at`; acceptable. **Branch F (the scheduled fire overlaps Act 2):** shards would run old and new code side by side, each series self-consistent; the condition below keeps Act 2 out of the fire window. **Branch G (the new code is wrong):** a shard refuses an account the old code accepted: counted by reason; a count that differs from Act 3's expectation STOPS Act 5.

## 7. Rollback, per key

- **The code:** the previous artifact version `4kEV9O.UMGs.NSGSYi_N4ZZjNm45rso4` is the target: a new upload of those bytes as the current version (a copy of the old version over the key, no delete) and a `safe-apply`, by the applier with the CTO's word.
- **The republished objects:** each key's prior version stays in the versioned bucket. Restoring is a listed-key copy of the prior version to the current key; deleting any version or object is Andrew's act and is never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-49f-reporting-publish-codeupdate-20261016`, the applier named, legs L1 git (the tree commit and each file's sha256), L2 build (the line equal to section 2's), L3 terraform (the plan 0/1/0 by address, then the apply, recorded by `record-terraform-deploy.sh`), L4 dry run, L5 canary, L6 full republish and the receipt. Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE. **Live state re-read at the moment of the apply** and equal to section 3, else STOP. The plan's function change must name `source_code_hash` and the artifact version only.
3. **Keep Act 2 out of the fire window:** on a trading weekday do not start Act 2 between 12:05Z and 13:00Z (the daily fire and its summaries pass run about 12:15Z to 12:50Z); outside it, start at once.
4. **Each event only after the previous leg's after-read is recorded in the ledger;** payloads and bodies quoted by counts and words, never an account id. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above the line, or a refusal count that differs from Act 3's.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule.** The applier is an AE seat the gates admit, not a worker.
6. **The receipt** after Act 6 carries the three phrases of Act 6.

## 9. Questions for the CTO's half

1. **One packet for the code update and the republish?** The code update has no new resource and the republish sits behind its own dry run and canary: accept, or split the republish into its own word.
2. **The republish overwrites 13,898 objects of the served prefix with a new version of each (versioned bucket, prior versions kept):** accept under branch E, with the rollback of section 7. (These series ARE read by the page today; the change adds keys and one manifest key, removes none.)
3. **The history-scope pair arrives only with the gold rebuild (a separate pair), so these series carry the unreported-days statement now and the history scope later:** confirm the order, or hold this republish until the gold is rebuilt so the series are republished once.

## 10. Not established, and so not covered

The page's treatment of the explicit empty list (a reader's act); which calendar the Lambda answers from (the manifest will say; the library is not packaged, so the table through 2027); the three accounts whose newest row is before the last partition (published as they were, their `as_of` earlier); the gold rebuild; the Cottonwood side.

-- 2.0.0_SA_COO~D2
