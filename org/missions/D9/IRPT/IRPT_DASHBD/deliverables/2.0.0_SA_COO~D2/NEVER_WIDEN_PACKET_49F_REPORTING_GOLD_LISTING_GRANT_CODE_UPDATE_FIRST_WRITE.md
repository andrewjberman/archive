# NEVER-WIDEN PACKET -- the 49 Financial reporting-gold function: the LISTING GRANT for the filled prefix, the CODE UPDATE (history_scope derived per account), the hop-1 FIRST WRITE, a ONE-DAY backfill and the republish of the series (IRPT_DASHBD round 149, cells DB-b-294, DB-b-295, DB-b-297, DB-b-299)

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~12:5xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, msg 9226 (history_scope derived per account, `history_scope_claim` inferred) and the round 148/149 analysis @231f28c622 (rulings 1 and 4: the writers are drained, NOT deployed; two pairs next), and by hop 1's open ledger `irpt-dashbd-hop1-filled-report-values-20261015` leg L6 (the first scheduled fire, 2026-10-16 11:41Z, wrote 0 filled objects: `FILLED_CATCHUP_LIST_FAILED`, AccessDenied on `s3:ListBucket`; row `IRPT_BCKEND-D2-S219`). The producer change (`DB-b-294`), the publisher change (`DB-b-295`), the contracts (`DB-b-293`, whose page mirror is `DB-c-30`), the entry re-pin (`DB-b-297`) and the listing grant (`DB-b-299`, merge `79bfba852b`) are drained.
**Two halves, one packet:** the COO half is `NEVER_WIDEN_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The AE applier builds `irpt-49f-reporting-gold-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-49f-reporting-gold-lambda` (the entry key; its `artifact_s3_key` is `investor-reporting/irpt-reporting-gold-lambda.zip`, read from the map, never typed). The build-only hash is below (section 2); the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key in `opal-313476888478-lambda-artifacts` (versioned; the current version `My0rI3fwtMCZYPDLqRhPgJ7QH9HrE8L3`, 263,340 bytes, is the rollback target) and updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-gold/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 2 to change, 0 to destroy:**

| address | what changes |
|---|---|
| `aws_iam_role_policy.irpt_reporting_gold` (change) | in the ONE statement `ListExactlyTheSixGoldPrefixes` the `s3:prefix` condition values gain exactly ONE entry, `irpt/49financial/gold/filled_report_values/*`; the eleven statement ids, every other statement and every other value stay as they are. No read grant, no write grant. |
| `module.irpt_reporting_gold.aws_lambda_function.this` (change) | the CODE only (the artifact version and its hash); memory 8,192, timeout 900, handler, runtime, role, layer, no environment stay exactly as they are |

Any other line, any other attribute, any destroy, STOPS the act. The schedule, its role and policy and the log group do not appear in the plan.

**Act 3 -- the hop-1 FIRST WRITE, on demand.** ONE synchronous event `{"day": "2026-10-15"}` (the newest landed returns day; `RequestResponse`, `--cli-read-timeout 0`). It runs ONLY the filled stage for that day (no earlier stage), writes nothing if the day is already landed, and chains no next day (none is owed after the newest). **Expected:** `result` carries `rows` (a positive count) and `next` is null; the prefix `irpt/49financial/gold/filled_report_values/` holds one `date=2026-10-15/` partition where it held 0 objects; Max Memory Used and duration inside 80 percent of the function's limits (6,553 MB, 720 s). The ledger's leg L6 is the applier's to close on this write, not on the Monday fire.

**Act 4 -- a ONE-DAY backfill of the newest landed day** `{"backfill": {"start": "2026-10-15", "end": "2026-10-15"}, "accounts": "population"}` (synchronous). It rewrites that day's returns partition through the new producer, and the same day of the class, activity and lot tables (those hold 7 days, 2026-10-07 to 2026-10-15) from the producer's own rows, at the SAME keys. **Before the event** the applier reads the day's returns partition (counts and column hashes only) and computes, from the gold, how many accounts have their first value day on the earliest partition (2024-07-08) among the accounts that have a row on 2026-10-15; **after the event** the returns partition holds the same number of rows with every value column (every column but `history_scope` and the claim) identical, `history_scope_claim` = `inferred` on every row, `history_scope` PARTIAL_HISTORY on exactly the counted floor-start accounts and FULL on the rest; the class, activity and lot day partitions hold the same row counts. A different count STOPS Act 5.

**Act 5 -- the republish of the 6,949 series** `{}` on `irpt-49f-reporting-publish-lambda` (the function of the earlier signed pair, already on publisher 0.4.0; this act is NOT taken before that pair's ledger `irpt-dashbd-49f-reporting-publish-codeupdate-20261016` is CLOSED). The same prefix, the same keys. **After-read:** every series whose newest gold row is 2026-10-15 carries `history_scope_claim` = `inferred` and `history_scope_basis` = "first value day vs source floor"; their count equals the number of accounts with a row on 2026-10-15; the series carrying `history_scope` PARTIAL_HISTORY among them equal Act 4's floor-start count (the CTO's 2,852 less any floor-start account without a row that day); the 3 accounts whose newest row is before 2026-10-15 carry no pair; the prefix still holds the same series, manifests and other objects; the prior versions are kept.

**Act 6 -- the receipt** with the counts, memory and duration of Acts 3 to 5, the checks, and the words "read by the PROD Performance tab (row 92c0)", "history scope derived for the newest row of each account; older rows keep the old constant and no claim" and "hop 1's first write: filled_report_values date=2026-10-15".

**NOT in this packet:** a backfill of any other day; the Cottonwood side; the schedule of either function; the summaries pass; any reader change; any delete of any object or version.

## 2. Pins

Code at tree `db318e10bd` or later on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry: `reporting-gold/handler.py` `4fab1deca0dd` (59,554), `account_return_daily.py` `c7512188be7f` (134,472), `account_class_daily.py` `13cec16c16de` (37,303), and the Terraform root's `locals.tf` `1063ebb77489` (11,590), `iam.tf` `a9b82429beeb` (8,002), `lambda.tf` `a20ea4a0a21c` (4,557), `main.tf` `782bb1348099` (1,616), `schedule.tf` `6f92147a2a18` (5,573; not in the plan). The source-map entry `irpt-49f-reporting-gold-lambda` was re-pinned by `DB-b-297` (8 stale members moved; none stale at packet time). **The build-only package** (`BUILD_ONLY=1`, nothing uploaded, built by this seat at this tree) has base64 sha256 `JNTOivgNaJ8spRxoXSkXAYWhf1cLqXr350sTpH5ADg4=`.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-49f-reporting-gold-lambda`: PRESENT; CodeSha256 `jz6fRzL52EaI+3ZBI5cWHuDuGwiBDM/S5DPX/CmjeaM=`; 8,192 MB; timeout 900 s; ephemeral storage 512 MB; one layer (`irpt-performance-native-layer:1`); no environment; last modified 2026-10-15T11:49:38Z. **Artifact key** `investor-reporting/irpt-reporting-gold-lambda.zip`: current VersionId `My0rI3fwtMCZYPDLqRhPgJ7QH9HrE8L3` (263,340 bytes, 2026-10-15T11:09:14Z); bucket versioning Enabled.
- **Role policy** `irpt-49f-reporting-gold-policy`: eleven statements by id (`ListExactlyTheDeclaredSilverPrefixes`, `ReadDeclaredSilverPartitionsOnly`, `ListExactlyTheSixGoldPrefixes`, `ReadTheSixGoldPrefixesOnly`, `WriteTheFiveGoldPrefixesOnly`, `ReadTheServedModelSeriesObjectOnly`, `ListExactlyTheHouseholdCrosswalkPrefix`, `ReadTheHouseholdCrosswalkOnly`, `ReadTheClassTableByKeyOnly`, `OwnLogStreamOnly`, `InvokeOwnFunctionOnly`).
- **Schedule** `irpt-49f-reporting-gold-daily`: ENABLED, `cron(41 7 ? * MON-FRI *)` America/New_York (11:41Z in October). It keeps firing and is untouched.
- **Gold tables, day counts and newest day:** `account_return_daily` 572 partitions, 2024-07-08 to 2026-10-15; `account_class_daily` and `account_activity_daily` 7 each, 2026-10-07 to 2026-10-15; **`filled_report_values` 0**.
- **Census of the gold** (@eb3e36f6cd, counts only): 6,949 accounts, 2,852 first seen on the earliest partition, 4,097 later, 3 whose newest row is before the last partition.

## 4. What each act changes in the world

- **Act 1:** a new version of one artifact key. **Act 2:** the role policy gains one list pattern and the function's code is replaced; the next invocation runs the new code and the filled stage may list its own prefix. **Act 3:** one NEW filled partition at an EMPTY prefix. **Act 4:** one day of five served gold tables is overwritten at the same keys (new versions, prior versions kept); the returns rows differ only in `history_scope` and one added conditional column. **Act 5:** the 6,949 series and manifests are overwritten at the same keys (prior versions kept); the series of accounts with a row on 2026-10-15 gain the pair. **Act 6:** reads only.

## 5. Writers of the changed properties, counted

The filled prefix: ONE rule writes it (`filled_write`, one PutObject statement of the role), entered by the scheduled fire's filled stage, the one-day event, the chain of owed days and the backfill. The returns table: ONE rule (`emit_day`), entered by the scheduled fire and the backfill. The series and manifests: ONE rule (the publish handler's `put_object`), entered by a hand invocation and the ENABLED daily schedule. N = 1 per property.

## 6. Both branches

- **Branch A:** as the acts state it. **Branch B (the listing is still denied):** Act 3 returns a failed day; nothing else is written; the policy read-back is the first thing to read; STOP. **Branch C (the filled stage runs out of memory or time on its whole-history read):** Act 3 fails at the line; nothing is written; STOP and report the measured peak (the sizing of 8,192 MB was set before the stage ever ran). **Branch D (Act 4 changes a value column):** STOP before Act 5; the prior versions are the rollback. **Branch E (the scheduled fire overlaps an act):** kept out by the condition below. **Branch F (a repeated Act 4 or 5):** same keys, same bytes except `built_at`; acceptable.

## 7. Rollback, per key

- **The code:** the previous artifact version `My0rI3fwtMCZYPDLqRhPgJ7QH9HrE8L3` is the target: a new upload of those bytes as the current version (a copy of the old version over the key, no delete) and a `safe-apply`, by the applier with the CTO's word. The policy reverts with the same apply (the one pattern leaves).
- **The gold day and the series:** each key's prior version stays in the versioned buckets. Restoring is a listed-key copy of the prior version to the current key; the one new filled partition is left in place (deleting it is Andrew's act). Deleting any version or object is Andrew's act and is never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-49f-reporting-gold-listing-codeupdate-20261016`, the applier named, legs git, build, terraform, first write, one-day backfill, republish and receipt. Read every live worktree's `.open_deploys/` first and print the denominator. The earlier publish pair's ledger and the hop-1 ledger are READ (hop 1's leg L6 closes on Act 3).
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE. **Live state re-read at the moment of the apply** and equal to section 3, else STOP. The plan's policy change must be the one condition value; its function change must name `source_code_hash` and the artifact version only.
3. **Keep Acts 2 to 4 out of the daily fire window** (11:35Z to 12:00Z on a trading weekday: the gold fire runs about five minutes from 11:41Z, its chained filled days and the publish fire at 12:15Z follow); Act 5 outside 12:05Z to 13:00Z.
4. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 80 percent of the limit, or a count that differs from the act's expectation.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to either schedule.**
6. **The receipt** after Act 6 carries the three phrases of Act 6.

## 9. Questions for the CTO's half

1. **One packet for the listing grant, the code update, the first write, the one-day backfill and the republish?** Each act has its own stop; accept, or split.
2. **A ONE-DAY backfill of the newest landed day, instead of a rebuild of the 571 days:** the publisher reads `history_scope` and its claim from each account's newest row, and the scheduled fires write derived rows from now on; older rows keep the old constant and carry no claim (a row without the claim makes no statement). Accept, or rule a longer rewrite (it re-emits the class, activity and lot tables for each day it touches).
3. **Act 3 is a hand event for the hop-1 first write, instead of waiting for the next scheduled fire:** accept.

## 10. Not established, and so not covered

Whether the filled stage's 8,192 MB sizing holds on its whole-history read (no run has reached it); the three accounts whose newest row is before the newest day (published without a claim); the older rows of the gold (legacy); a reader's treatment of the pair (the page mirror `DB-c-30` takes it and prints nothing); the Cottonwood side.

-- 2.0.0_SA_COO~D2
