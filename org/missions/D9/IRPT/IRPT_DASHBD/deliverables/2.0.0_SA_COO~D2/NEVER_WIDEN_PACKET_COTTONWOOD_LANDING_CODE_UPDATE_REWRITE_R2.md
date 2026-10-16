# NEVER-WIDEN PACKET -- the Cottonwood account-return landing function, REVISION 2: the CODE UPDATE (history_scope derived per account by the FIRST-ROW rule, the explicit rewrite event) and the REWRITE of the 66 landed gold days, which also takes in the late-arriving flows of ten October days (IRPT_DASHBD round 149, cells DB-b-294, DB-b-296, DB-b-303, DB-b-304)

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~18:0xZ (REVISION 2).
**Revision 2 supersedes revision 1 (sha256 `778009ecda403f17...`, both halves now VOID).** What changed from revision 1: (1) the adapter's scope rule is now the 49 Financial producer's, the FIRST ROW (cell `DB-b-303`, merge `d011411480`; the CTO's msg 9480: one meaning of `history_scope` across firms; 31 of the 867 floor-day accounts, 25 with a negative and 6 with a zero value, read FULL under revision 1's positive-value rule); (2) the value clause is restated and the CTO accepted the late inputs (msg 9487): **this rewrite is wider than the history scope** and says so in section 1, Act 4; (3) the applier is `0.7.0_AE_CloudOps~IB2` (Andrew-direct rule 34: one IRPT CloudOps lane per box; the CTO's msg of ~15:5xZ); (4) the entry is re-pinned (`DB-b-304`, merge `787619fad2`) and the build-only hash is new; (5) the section on the writers of the changed properties and the section naming what a client could read are added (the CTO's round 149 packet 4 analysis, items 2 and 3).
**Ordered by:** 1.0.0_SA_CTO~DELL2, msg 9226 (history_scope derived per account), msg 9264 (the correction route: an explicit, signed rewrite event, no delete), msgs 9480 and 9487 (one meaning across firms; the late inputs accepted with the exact counts below) and the round 148/149 analysis @231f28c622.
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The applier `0.7.0_AE_CloudOps~IB2` builds `irpt-cot-account-return-daily-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-return-daily-lambda` (the entry key; its `artifact_s3_key` is `investor-reporting/irpt-cot-account-return-daily-lambda.zip`, read from the map, never typed). The build-only hash is in section 2; the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key in `opal-313476888478-lambda-artifacts`. **The key's CURRENT version is `Amwu_BigtNXtPIwPXQIBPXmEFfKpg9RN`, an UNUSED upload of the superseded order (the old bundle, 151,936 bytes); the version the function RUNS is `UnMNWDhcC3KpERDmGYdKAl83whx1oNFW` (148,909 bytes) and is the rollback target.** The upload updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/account-return-daily/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 1 to change, 0 to destroy:** `module.irpt_account_return_daily.aws_lambda_function.this`, by CODE attributes only (the artifact version and its hash). Memory 1,024, timeout 900, handler, runtime, role, the one layer, reserved concurrency 1 and no environment stay as they are; the execution role and policy (five statements, no grant change), the scheduler role and policy, the schedule and the log group do not appear in the plan. Any other line, any other attribute, any destroy, STOPS the act.

**Act 3 -- a DRY RUN of the rewrite on the first range, `{"rewrite": {"start": "2026-07-10", "end": "2026-08-13"}, "dry_run": true}`** (synchronous; `RequestResponse`, `--cli-read-timeout 0`). The handler derives every day of the range through the new producer and writes nothing. **Expected:** `ok` true; `held` 0; 25 days; each day's `rows` equals the landed partition's row count; Max Memory Used at most 819 MB (80 percent of 1,024) and the duration at most 720 s; the object versions of the range unchanged. **STOP** on a `Task timed out`, a Max Memory Used above 819 MB (no resize inside this pair: a resize is its own pair), a held day, a row-count difference or any function error.

**Act 4 -- the REWRITE, four explicit events, oldest first, each only after the previous one's after-read is recorded** (all `{"rewrite": {"start": ..., "end": ...}}`, no `dry_run`):

| event | start | end | trading days |
|---|---|---|---|
| 1 | 2026-07-10 | 2026-08-13 | 25 |
| 2 | 2026-08-14 | 2026-08-18 | 3 |
| 3 | 2026-08-20 | 2026-09-23 | 24 |
| 4 | 2026-09-28 | 2026-10-15 | 14 |

The four ranges are the 66 landed trading days from the floor 2026-07-10 to 2026-10-15; they are cut around the three trading days with no partition (2026-08-19, 2026-09-24, 2026-09-25: the adapter holds a day with no `fact_transactions` partition; row `IRPT_DASHBD-D2-S122`; the CTO ruled them to stay unlanded), because the handler refuses a range holding a day that is not landed. Each event overwrites the two keys of each named day (`data.parquet`, then `manifest.json`) at the SAME keys; the bucket is versioned and nothing is deleted.

**The rewrite is wider than the history scope, and the CTO accepted it (msg 9487): the gold reads the source as it stands.** The landing guard would otherwise keep stale flows forever. Read-only, by this seat's offline diff of the producer against the current silver (`reads/RD_COT_REWRITE_OFFLINE_DIFF_20261016.json` @`599ae8c14b`), 56 of the 66 days are identical in every column but `history_scope` and its claim, and **ten October days differ in `external_flow` (844 rows in all) and in `total_return_daily` (798 rows in all) and in no other column**; no row appears or disappears. The per-day counts, which are the ceilings:

| day | `external_flow` rows | `total_return_daily` rows |
|---|---|---|
| 2026-10-01 | 3 | 2 |
| 2026-10-02 | 38 | 33 |
| 2026-10-05 | 44 | 41 |
| 2026-10-06 | 17 | 14 |
| 2026-10-07 | 20 | 14 |
| 2026-10-08 | 22 | 17 |
| 2026-10-09 | 616 | 601 |
| 2026-10-12 | 24 | 21 |
| 2026-10-13 | 34 | 31 |
| 2026-10-14 | 26 | 24 |

**After each event, for every day of the event:** the row count equals the landed one; the set of `account_id` and every `market_value_eod` are identical to the previous version's; `external_flow` and `total_return_daily` differ from the previous version ONLY on the ten days above and on NO MORE rows per day than the table (a day with no entry has none); every other column but `history_scope` and `history_scope_claim` is identical; `history_scope_claim` = `inferred` on every row; `history_scope` is PARTIAL_HISTORY on exactly the accounts that have a ROW on the FLOOR day 2026-07-10 in `fact_allocations` (whatever the row's value; 867 accounts at packet time, computed by the applier with the adapter's own `_key` over the partition's `AccountID` column) and FULL on the rest; the manifest differs from the previous version's only in `columns` (it gains `history_scope_claim`, 21 columns); each of the day's two keys holds one more version than before. **Per event the receipt prints the PARTIAL and FULL counts and the floor-day account count.** Today every landed row reads PARTIAL_HISTORY, so only PARTIAL to FULL flips can occur; **any FULL to PARTIAL flip STOPS the next event** (the rule cannot produce it). **STOP** (no further event) on any held day, any column outside the allowance, any count above the table, a `Task timed out`, a Max Memory Used above 819 MB or a duration above 720 s.

**Act 5 -- the whole-prefix after-read.** The prefix `irpt/cottonwood/gold/account_return_daily/` in `opal-data-cottonwood` still holds 3,391 `date=` partitions (or more only by the scheduled fire's own newer days): **the version count and the key list (with version ids) of ALL 3,325 history days (2013-04-03 to 2026-06-22) are read, not a sample, and equal the values read before Act 2**, the 66 days hold two versions of each key, the three held days are absent and no key outside the two files of a counted day is new. The schedule is ENABLED and untouched.

**Act 6 -- the receipt** with the plan counts, the dry run's and each event's rows, held count, PARTIAL and FULL counts, floor-day account count, the changed-row counts of `external_flow` and `total_return_daily` per day against the table, memory and duration, and the words "history scope derived for the 66 landed Cottonwood days by the first-row rule", "the ten October days restated in external_flow and total_return_daily at the counts of the table", "the series are republished by a separate pair", "schedule ENABLED and untouched" and "the 3 held days stay unlanded".

**NOT in this packet:** the Cottonwood publish function and its republish (a separate pair after this one, which names the returns that move on the Performance tab beside the "Returns from" count, the CTO's msg 9487); the three held days; any day before 2026-07-10 (never); the schedule; the summaries pass; any reader change; any delete of any object or version.

## 2. Pins

Code at tree `d58c1dda9c` or later on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `handler.py` `b22affd4933c` (9,736), the adapter `4ef97f84d39a` (30,580), and the Terraform root's `iam.tf` `be6fe3f38597` (6,756), `lambda.tf` `736826f6e6d8` (3,647), `locals.tf` `8414bb4980d4` (2,824), `main.tf` `72245428da82` (1,674), `schedule.tf` `8bcf2a5295a5` (2,037; not in the plan). The source-map entry `irpt-cot-account-return-daily-lambda` holds 15 staged members, each pinned to a full commit and hashed, re-pinned by `DB-b-304` (three members moved: the adapter, `lib/trading_calendar.py`, `infra/logic/registry/legacy_addresses.json`; none stale at packet time). **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=`; the deployed package is `fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs=`.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-account-return-daily-lambda`: PRESENT; CodeSha256 `fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs=`; 1,024 MB; timeout 900 s; reserved concurrency 1; one layer (`irpt-performance-native-layer:1`); no environment. **Artifact key** `investor-reporting/irpt-cot-account-return-daily-lambda.zip`: current VersionId `Amwu_BigtNXtPIwPXQIBPXmEFfKpg9RN` (the unused upload of the superseded order); the running version is `UnMNWDhcC3KpERDmGYdKAl83whx1oNFW`; bucket versioning Enabled.
- **Execution policy** `irpt-cot-account-return-daily-execution-policy`: five statements (`ListSilverTablePrefixesOnly`, `ReadTwoBlackDiamondSilverTablesOnly`, `WriteTheOneAccountReturnDailyGoldPrefixOnly`, `ListTheOneAccountReturnDailyGoldPrefixOnly`, `OwnLogStreamOnly`). The write and list statements already admit the rewrite; nothing in the policy changes.
- **Schedule** `irpt-cot-account-return-daily-daily`: ENABLED, `cron(15 8 ? * MON-FRI *)` America/New_York (12:15Z in October). It keeps firing and is untouched; with the new code it lands T-1 with the derived scope; the guard still refuses any day that is landed.
- **Gold** `irpt/cottonwood/gold/account_return_daily/` in `opal-data-cottonwood`: 3,391 `date=` partitions, first 2013-04-03, newest 2026-10-15; 66 from 2026-07-10 on (69 NYSE trading days in 2026-07-10 to 2026-10-15; the three held days are 2026-08-19, 2026-09-24, 2026-09-25); bucket versioning Enabled; each landed key holds one version. A landed day carries 20 columns (no claim column) and `history_scope` PARTIAL_HISTORY on every row (2026-07-10: 867 rows; 2026-10-15: 860 rows).
- **Silver.** `fact_allocations` 146 partitions (2026-04-22 to 2026-10-15), `fact_transactions` 126 partitions (2026-03-09 to 2026-10-16); the floor day's allocations partition 2026-07-10 holds 867 accounts, 836 with a positive value, 6 with zero and 25 with a negative one.

## 4. What each act changes in the world, and what a client could read

- **Act 1:** a new version of one artifact key. **Act 2:** the function's code is replaced; the next invocation, scheduled or by hand, runs the new code. **Act 3:** nothing is written. **Act 4:** the 66 landed days' two keys each are overwritten at the same keys (new versions, prior versions kept); the rows differ in `history_scope`, one added column and, on the ten October days, the two columns above. **Acts 5, 6:** reads only.
- **A client-facing sentence this pair can move: none, count 0 read before the write.** The Cottonwood series (`irpt/cottonwood/platinum/reporting/`, 939 series and 939 manifests, 1,878 objects at packet time) are not rewritten by this pair, so no served figure and no "Returns from <date>." sentence moves; nothing reads that prefix as served at packet time. The returns that DO move on the Performance tab, and the sentence count, are named by the Cottonwood republish pair, with its before-write flip count, as the CTO ruled.

## 5. Writers of the changed properties, counted

The gold partition keys: ONE rule writes them (`write_day`, the only two `put_object` calls of the adapter), entered by the scheduled fire (ONE enabled schedule, `irpt-cot-account-return-daily-daily`, 08:15 New York weekdays, found with 0 EventBridge rules targeting the function; `reads/RD_IRPT_REPORTING_WRITERS_COUNT_20261016.json` @`867d91f704`), the `day`/`days` events (guard on) and the rewrite event (guard inverted: the day must be landed); manual acts only under a signed pair. The reserved concurrency of 1 serializes them. N = 1 per property.

## 6. Both branches

- **Branch A:** as the acts state it. **Branch B (a held day, a column outside the allowance or a count above the table):** STOP before the next event; the prior versions are the rollback. **Branch C (memory or time):** the dry run is the measurement; a peak above 80 percent stops the pair before any write and no resize is made inside it. **Branch D (the scheduled fire overlaps an event):** kept out by the condition below (reserved concurrency 1 would throttle the later invocation). **Branch E (a repeated event):** same keys; acceptable.

## 7. Rollback, per key

- **The code:** the version the function runs, `UnMNWDhcC3KpERDmGYdKAl83whx1oNFW`, is the target: a new upload of those bytes as the current version (a copy of the old version over the key, no delete) and a `safe-apply`, by the applier with the CTO's word.
- **A rewritten day:** each key's prior version stays in the versioned bucket. Restoring is a listed-key copy of the prior version to the current key. Deleting any version or object is Andrew's act and is never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-cottonwood-landing-codeupdate-rewrite-r2-20261016`, the applier named, legs git, build, terraform, dry run, rewrite events, receipt. Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE. **Live state re-read at the moment of the apply** and equal to section 3, else STOP.
3. **Keep Acts 2 to 4 out of the daily landing fire window** (12:05Z to 12:45Z on a trading weekday; the fire runs at 12:15Z).
4. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 819 MB, or a count that differs from the act's expectation.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule, no event naming a day before 2026-07-10 or a held day.**
6. **The receipt** after Act 6 carries the words of Act 6.

## 9. Questions for the CTO's half

1. **The stale-flow restatement is part of this pair (as you ruled in msg 9487):** confirm the allowance as the table of section 1 (844 `external_flow` rows and 798 `total_return_daily` rows on ten days), or narrow it.
2. **One packet for the code update, the dry run and the four-event rewrite?** Each act has its own stop; accept, or split.
3. **The dry run before any write, on the largest range:** accept as the memory and time measurement.

## 10. Not established, and so not covered

The Lambda's memory and time on a 25-day range (no run has measured it; the dry run is the first); whether the silver of a landed day changes again between this packet and the apply (a day outside the allowance stops the pair); the Cottonwood series (published by the next pair); a reader's treatment of the pair (the page mirror takes key lists only and prints nothing).

-- 2.0.0_SA_COO~D2
