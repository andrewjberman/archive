# NEVER-WIDEN PACKET -- the Cottonwood gold day 2026-07-27 REWRITTEN from the now-full carrier delivery, and the series republished (IRPT_DASHBD round 150; CTO msgs 10344, 10354)

**Packet author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-17 ~07:0xZ. **Applier:** `0.7.0_AE_CloudOps~IB2` (the one IRPT CloudOps lane, rule 34). **Halves:** the COO half and the CTO half, each bound to this file's sha256 (printed in each half). **Order:** the apply order to IB2, cut after both halves are signed. **Read behind it:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/reads/RD_COT_CARRIER_ABSENT_DAYS_20261017.json` @5e3c0c1d92.
**What this pair does, in one paragraph.** The Cottonwood series is missing 7 trading days. For ONE of them, 2026-07-27, the carrier's landed silver is FULL on every table (holdings 918 accounts, transactions 12,519 rows, realized 100,604, unrealized 66,460) while the gold `account_return_daily` day holds only 3 rows (a build that ran on a partial delivery and was never rerun). The pair (1) re-runs that ONE day through the function's own explicit rewrite event, dry run first, which overwrites the day's gold partition as a NEW VERSION (every prior version kept), and (2) republishes the Cottonwood series, so each account that has a row on that day gains the day and the following trading day's return becomes measurable. **The write set is the gold day 2026-07-27 and the series/manifest objects the republish rewrites; no other gold day, no schedule, no code, no role.** The other 6 absent days (07-22, 07-29, 08-03 partial; 08-19, 09-24, 09-25 not delivered) are NOT touched: they wait on dell1's carrier lane (CTO msg 10354).

## 1. The acts (nine, in order; each has its own stop)

**Act 0 -- gates and the ledger.** Packet sha256 and both halves; no open leg on the surface; the live state equals section 2. Open the NEVER-2 ledger naming the applier BEFORE any write.

**Act 1 -- before reads (read only).** (a) The gold table `irpt/cottonwood/gold/account_return_daily/`: the partition list (count and the newest), the object, its VersionId list and row count for `date=2026-07-27` (expected 3 rows, 1 object), and the row counts of the full neighbours `date=2026-07-21` (879 rows) and the sum over all partitions; (b) the published prefix `irpt/cottonwood/platinum/reporting/`: the `account=` prefixes (939) and the object and version counts; (c) the two functions' CodeSha256 and environments; (d) the schedules (`irpt-cot-account-return-daily-daily` ENABLED; `irpt-cot-reporting-publish-daily` DISABLED); (e) the silver counts for 2026-07-27 as in the read file.

**Act 2 -- the DRY RUN of the gold day.** One synchronous `{"rewrite": {"start": "2026-07-27", "end": "2026-07-27"}, "dry_run": true}` to `irpt-cot-account-return-daily-lambda` (`--cli-read-timeout 0 --invocation-type RequestResponse --log-type Tail`). **Expected:** `ok` true, `days` ["2026-07-27"], `held` 0, and the day's rows between 840 and 920 (a full day is about 879). **STOP** on `held` above 0, a row count outside that band, an exception, a timeout, a Max Memory Used above 819 MB or a duration above 600 s. Nothing is written (the applier reads the gold prefix object and version counts before and after: EQUAL).

**Act 3 -- the REWRITE of the gold day.** The same event WITHOUT `dry_run`. **Expected:** the same rows as the dry run. After: `date=2026-07-27` holds the new rows as the CURRENT version and the 3-row version is KEPT as the previous one (version count +1 for that key set); every other gold partition's object and version counts are EQUAL to Act 1; the schedules are untouched.

**Act 4 -- the pre-write read of the republish (read only).** Run the read tool `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/reads/cot_publish_offline_diff.py` (it reads the gold and the published series and reports, by count, what a republish would change). **Expected:** the accounts that GAIN a day equal the rewritten day's rows minus those already present; **STOP before any republish** if any field other than `total_return_daily`, `day_quality` and `return_basis` changes on a day present in both versions, if any day other than 2026-07-28 changes in those three fields, if a day is REMOVED from any series, or if the refused count is above 0.

**Act 5 -- the dry run of the republish.** One synchronous `{}` (a dry build, nothing uploaded) to `irpt-cot-reporting-publish-lambda`: `published` 939, `refused` equal to the earlier republish's count (40). STOP above the 10 percent line.

**Act 6 -- the canary.** ONE synchronous `{"upload": true, "accounts": ["<one id>"]}` for the first account (sorted) that gains the day; its id is never recorded, only the first 12 hex of its sha256. Read the series back in memory: the dates gained are exactly {2026-07-27}; every common day's numeric fields equal the PREVIOUS VERSION of the same object; only 2026-07-28's `total_return_daily`, `day_quality` and `return_basis` differ. The manifest's `publisher_version`, `history_scope` and claim stay as before.

**Act 7 -- the full republish.** ONE synchronous `{"upload": true}` (900 s limit; a lost response is judged from the log). **Expected:** `published` 939, `refused` as in Act 5. The object count is unchanged (same keys, new versions); the version count rises by the number written.

**Act 8 -- the after-read.** The two functions: code hash, memory and environment unchanged; the schedules unchanged; the gold prefix: only the one day's key set gained a version; the published prefix: the same 939 `account=` prefixes and the same object count; a sample of 25 series (sorted positions) satisfies the Act 6 invariant against the previous version; the Thiessen-class check: a series that was missing 2026-07-27 now holds it (count of series holding the day, expected equal to the day's rows).

**Act 9 -- the receipt.** Counts, memory and duration; the words "the rewrite changed one gold day" and "the daily returns of 2026-07-28 moved from not measurable to measured".

## 2. Pins and live state, measured by this seat at packet time (read-only; the applier re-reads at each act)

- `irpt-cot-account-return-daily-lambda`: `CodeSha256` `+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=`, 1,024 MB, 900 s, no environment, last modified 2026-10-16T19:29:43Z; handler `infra/aws/lambda/investor-reporting/account-return-daily/handler.py` (the `_rewrite` path, DB-b-296: refuses a day before 2026-07-10, a day not already landed, more than 25 days, and any event that also names `day` or `days`).
- `irpt-cot-reporting-publish-lambda`: `CodeSha256` `vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE=`, 1,024 MB, 900 s.
- Gold `date=2026-07-27`: 3 rows against 879 on the full day 2026-07-21 (read by this seat). Carrier silver for 2026-07-27: holdings 918 accounts, transactions 12,519, realized 100,604, unrealized 66,460 (the read file).
- Schedules: `irpt-cot-account-return-daily-daily` ENABLED, `irpt-cot-reporting-publish-daily` DISABLED.
- The 939 published series: PARTIAL_HISTORY, claim `inferred` (the earlier signed republish).

## 3. What each act changes in the world

Acts 1, 2, 4, 5 write nothing. Act 3 writes ONE gold day (a new version of its object). Act 6 and Act 7 rewrite series and manifest objects at the same keys (new versions): **each account that has a row on 2026-07-27 gains that trading day, and the next trading day's daily return becomes measurable; nothing else about a series changes.** **A client-facing sentence this pair can move: the Performance tab of a Cottonwood account (viewed by Opal staff at Global) shows one more day, and the "no return can be measured" count falls by one for each account that gains the day.** The page, the route, the roles and every other gold day are untouched.

## 4. Writers of the changed properties, counted

The gold `account_return_daily` day has ONE producer: `irpt-cot-account-return-daily-lambda` (N = 1 writer; its scheduled fire owes only the days AFTER the newest landed day, so it never touches a landed day). The series and manifest objects have ONE writer: `irpt-cot-reporting-publish-lambda` (N = 1; its schedule is DISABLED).

## 5. Both branches

**Branch A:** every act returns what it states. **Branch B (a dry run outside its band, a held day, a pre-write read outside its STOP lines, a canary that breaks the invariant):** STOP before the next act; the prior versions are the rollback. **Branch C (memory or time):** above 819 MB or a duration above 600 s (gold) or 850 s (publish): STOP. **Branch D (a scheduled fire overlaps an act):** none between 12:05 and 13:15 UTC on a weekday; the account-return fire owes days after the newest landed day only.

## 6. Rollback, per key

Gold: the prior (3-row) version of the day's object is kept; the rollback is a COPY of that version over the key (a write, by the applier, under the ledger); no version is deleted. Series: every key has its prior version; the rollback is a per-key copy of the previous version, from the receipt's counts. No code, role or schedule changed, so none rolls back.

## 7. Conditions

1. **Ledger first,** bound to this packet's sha256; `.open_deploys/` read across every live worktree with the denominator printed.
2. **Live state re-read at the moment of each act;** a difference from section 2 other than the scheduled fires' own outputs is recorded before the act.
3. **Stop at once** on a timeout, an `AccessDenied`, a memory or duration line above, or a response outside the act's expectation. Counts and words only: never an account id, a name or a body.
4. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no schedule change, no other gold day, no environment variable.**

## 8. Questions for the CTO's half

1. Accept that the republish (Acts 6 and 7) is part of this pair although the rewrite's own write set is one gold day? 2. Accept the Act 4 STOP lines (only 2026-07-28's three fields may change on a common day)? 3. Accept that the other 6 days are not touched here?

## 9. Not established, and so not covered

That the rewrite produces about 879 rows (the dry run is the first run of this day against the full silver); that the carrier's own source holds a fuller delivery for the 6 other days (dell1's lane); the page.
