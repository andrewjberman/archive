# NEVER-WIDEN PACKET -- the Cottonwood account-return landing function: the CODE UPDATE (history_scope derived per account, the explicit rewrite event) and the REWRITE of the 66 landed gold days (IRPT_DASHBD round 149, cells DB-b-294, DB-b-296, DB-b-297)

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~13:5xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, msg 9226 (history_scope derived per account, `history_scope_claim` inferred), msg 9264 (the correction route: an explicit, signed rewrite event, route (c), no delete) and the round 148/149 analysis @231f28c622 (the writers are drained, NOT deployed). The producer change and the rewrite event (`DB-b-294`, `DB-b-296`) and the entry re-pin (`DB-b-297`) are drained; the contracts are `DB-b-293`, whose page mirror is `DB-c-30`.
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The AE applier builds `irpt-cot-account-return-daily-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-return-daily-lambda` (the entry key; its `artifact_s3_key` is `investor-reporting/irpt-cot-account-return-daily-lambda.zip`, read from the map, never typed). The build-only hash is in section 2; the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key in `opal-313476888478-lambda-artifacts` (versioned; the current version `UnMNWDhcC3KpERDmGYdKAl83whx1oNFW`, 148,909 bytes, is the rollback target) and updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/account-return-daily/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 1 to change, 0 to destroy:** `module.irpt_account_return_daily.aws_lambda_function.this`, by CODE attributes only (the artifact version and its hash). Memory 1,024, timeout 900, handler, runtime, role, the one layer, reserved concurrency 1 and no environment stay as they are; the execution role and policy (five statements, no grant change), the scheduler role and policy, the schedule and the log group do not appear in the plan. Any other line, any other attribute, any destroy, STOPS the act.

**Act 3 -- a DRY RUN of the rewrite on the first range, `{"rewrite": {"start": "2026-07-10", "end": "2026-08-13"}, "dry_run": true}`** (synchronous; `RequestResponse`, `--cli-read-timeout 0`). The handler derives every day of the range through the new producer and writes nothing. **Expected:** `ok` true; `held` 0; 25 days; each day's `rows` equals the landed partition's row count; Max Memory Used at most 819 MB (80 percent of 1,024) and the duration at most 720 s; the bucket's object versions unchanged (a LIST of versions: still 2 per day for the range). **STOP** on a `Task timed out`, a Max Memory Used above 819 MB (no resize inside this pair: a resize is its own pair), a held day, a row-count difference or any function error.

**Act 4 -- the REWRITE, four explicit events, oldest first, each only after the previous one's after-read is recorded** (all `{"rewrite": {"start": ..., "end": ...}}`, no `dry_run`):

| event | start | end | trading days |
|---|---|---|---|
| 1 | 2026-07-10 | 2026-08-13 | 25 |
| 2 | 2026-08-14 | 2026-08-18 | 3 |
| 3 | 2026-08-20 | 2026-09-23 | 24 |
| 4 | 2026-09-28 | 2026-10-15 | 14 |

The four ranges together are the 66 landed trading days from the floor 2026-07-10 to 2026-10-15; they are cut around the three trading days with no partition (2026-08-19, 2026-09-24, 2026-09-25: the adapter's `presence_hold` holds a day with no `fact_transactions` partition; row `IRPT_DASHBD-D2-S122`), because the handler refuses a range holding a day that is not landed. Each event overwrites the two keys of each named day (`data.parquet`, then `manifest.json`) at the SAME keys; the bucket is versioned and nothing is deleted. **Before each event** the applier reads each named day's landed partition (counts and column hashes only). **After each event, for every day of the event:** the row count equals the landed one; every value column (every column but `history_scope` and `history_scope_claim`) is identical (one sha256 over the rows sorted by `account_id`); `history_scope_claim` = `inferred` on every row; `history_scope` is PARTIAL_HISTORY on exactly the accounts with a positive summed value on the FLOOR day's `fact_allocations` partition (2026-07-10, computed by the applier with the adapter's own `day_values`) and FULL on the rest; the manifest differs from the landed one only in `columns` (it gains `history_scope_claim`, 21 columns); each of the two keys holds one more version than before and the prior version is kept. **STOP** (no further event) on any held day, any differing value column, any `Task timed out`, a Max Memory Used above 819 MB or a duration above 720 s.

**Act 5 -- the whole-prefix after-read.** The prefix `irpt/cottonwood/gold/account_return_daily/` in `opal-data-cottonwood` still holds 3,391 `date=` partitions (the 3,325 history days, first 2013-04-03, last 2026-06-22, are byte-identical: the applier compares the key list and the version count of a sample of ten by position; and the 66), no partition on the three held days, no new key outside the 66 days' two files. The function's schedule is ENABLED and untouched.

**Act 6 -- the receipt** with the plan counts, the dry run's and each event's rows, held count, PARTIAL and FULL counts, memory and duration, and the words "history scope derived for the 66 landed Cottonwood days; the series are republished by a separate pair", "schedule ENABLED and untouched" and "the 3 held days stay unlanded".

**NOT in this packet:** the Cottonwood publish function and its republish (a separate pair after this one); the three held days; any day before 2026-07-10 (never); the schedule; the summaries pass; any reader change; any delete of any object or version.

## 2. Pins

Code at tree `c2b2f1e950` or later on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `handler.py` `b22affd4933c` (9,736), the adapter `7b64f270edad` (30,235), and the Terraform root's `iam.tf` `be6fe3f38597` (6,756), `lambda.tf` `736826f6e6d8` (3,647), `locals.tf` `8414bb4980d4` (2,824), `main.tf` `72245428da82` (1,674), `schedule.tf` `8bcf2a5295a5` (2,037; not in the plan). The source-map entry `irpt-cot-account-return-daily-lambda` holds 15 staged members, each pinned to a full commit and hashed; 14 equal the working tree and `lib/trading_calendar.py` is pinned at its older content `9bc467c6ce4d` (the working file adds one unrelated function; the build uses the pin). **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `FH4+ZDunLNxCc2pb03bx9U10iAcmQQrvYPaBx5xnjew=`; the deployed package is `fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs=`.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-account-return-daily-lambda`: PRESENT; CodeSha256 `fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs=`; 1,024 MB; timeout 900 s; reserved concurrency 1; one layer (`irpt-performance-native-layer:1`); no environment; last modified 2026-10-15T15:23:47Z. **Artifact key** `investor-reporting/irpt-cot-account-return-daily-lambda.zip`: current VersionId `UnMNWDhcC3KpERDmGYdKAl83whx1oNFW` (148,909 bytes, 2026-10-15T13:23:43Z); bucket versioning Enabled.
- **Execution policy** `irpt-cot-account-return-daily-execution-policy`: five statements (`ListSilverTablePrefixesOnly`, `ReadTwoBlackDiamondSilverTablesOnly`, `WriteTheOneAccountReturnDailyGoldPrefixOnly`, `ListTheOneAccountReturnDailyGoldPrefixOnly`, `OwnLogStreamOnly`). The write and list statements already admit the rewrite (PutObject and ListBucket on the one gold prefix); nothing in the policy changes.
- **Schedule** `irpt-cot-account-return-daily-daily`: ENABLED, `cron(15 8 ? * MON-FRI *)` America/New_York (12:15Z in October). It keeps firing and is untouched: with the new code it lands T-1 with the derived scope; the guard still refuses any day that is landed.
- **Gold** `irpt/cottonwood/gold/account_return_daily/` in `opal-data-cottonwood`: 3,391 `date=` partitions, first 2013-04-03, newest 2026-10-15; 66 from 2026-07-10 on (69 NYSE trading days in 2026-07-10 to 2026-10-15; the three held days are 2026-08-19, 2026-09-24, 2026-09-25); bucket versioning Enabled; each landed key holds one version. A landed day carries 20 columns (no claim column) and `history_scope` PARTIAL_HISTORY on every row (2026-07-10: 867 rows; 2026-10-15: 860 rows).
- **Silver.** `fact_allocations` 146 partitions (2026-04-22 to 2026-10-15), `fact_transactions` 126 partitions (2026-03-09 to 2026-10-16); the floor day's allocations partition 2026-07-10 is present.

## 4. What each act changes in the world

- **Act 1:** a new version of one artifact key. **Act 2:** the function's code is replaced; the next invocation, scheduled or by hand, runs the new code. **Act 3:** nothing is written. **Act 4:** the 66 landed days' two keys each are overwritten at the same keys (new versions, prior versions kept); the rows differ only in `history_scope` and one added column; the Cottonwood series are unchanged until the republish pair. **Act 5, 6:** reads only.

## 5. Writers of the changed properties, counted

The gold partition keys: ONE rule writes them (`write_day`, the only two `put_object` calls of the adapter), entered by the scheduled fire, the `day`/`days` events (guard on) and the rewrite event (guard inverted: the day must be landed). N = 1 per property.

## 6. Both branches

- **Branch A:** as the acts state it. **Branch B (a held or differing day):** a day whose silver has changed since it landed is held (nothing written for it) or its value columns differ; STOP before the next event; the prior versions are the rollback. **Branch C (memory or time):** the dry run is the measurement; a peak above 80 percent stops the pair before any write and no resize is made inside it. **Branch D (the scheduled fire overlaps an event):** kept out by the condition below (reserved concurrency 1 would throttle the later invocation). **Branch E (a repeated event):** same keys, same bytes; acceptable.

## 7. Rollback, per key

- **The code:** the previous artifact version `UnMNWDhcC3KpERDmGYdKAl83whx1oNFW` is the target: a new upload of those bytes as the current version (a copy of the old version over the key, no delete) and a `safe-apply`, by the applier with the CTO's word.
- **A rewritten day:** each key's prior version stays in the versioned bucket. Restoring is a listed-key copy of the prior version to the current key. Deleting any version or object is Andrew's act and is never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-cottonwood-landing-codeupdate-rewrite-20261016`, the applier named, legs git, build, terraform, dry run, rewrite events, receipt. Read every live worktree's `.open_deploys/` first and print the denominator; the 49 Financial pairs' ledgers are other surfaces.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE. **Live state re-read at the moment of the apply** and equal to section 3, else STOP.
3. **Keep Acts 2 to 4 out of the daily landing fire window** (12:05Z to 12:45Z on a trading weekday; the fire runs at 12:15Z).
4. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 819 MB, or a count that differs from the act's expectation.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule, no event naming a day before 2026-07-10 or a held day.**
6. **The receipt** after Act 6 carries the three phrases of Act 6.

## 9. Questions for the CTO's half

1. **One packet for the code update, the dry run and the four-event rewrite?** Each act has its own stop; accept, or split the rewrite from the code update.
2. **The three held days stay unlanded** (the adapter's rule holds a day whose `fact_transactions` partition is absent; the fix, if any, is a ruling on that rule and a separate pair): accept, or rule otherwise.
3. **The dry-run event before the first write** (the handler's `dry_run` derives and writes nothing): accept as the measurement of memory and time.

## 10. Not established, and so not covered

The Lambda's memory and time on a 25-day range (no run has measured it; the dry run is the first); whether any landed day's silver has changed since it landed (a changed day is held or differs, and stops the pair); the Cottonwood series (published by the next pair); a reader's treatment of the pair (the page mirror `DB-c-30` takes it and prints nothing).

-- 2.0.0_SA_COO~D2
