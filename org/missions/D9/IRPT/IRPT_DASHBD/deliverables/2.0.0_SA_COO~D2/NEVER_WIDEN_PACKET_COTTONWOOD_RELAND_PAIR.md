# NEVER-WIDEN PACKET -- the Cottonwood gold days REWRITTEN from the carrier's re-landed allocations (four days and the four days that follow them), and the series republished ONCE (IRPT_DASHBD round 150; CTO ruling after msg 10575)

**Packet author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-17 ~15:0xZ. **Applier:** `0.7.0_AE_CloudOps~IB2` (the one IRPT CloudOps lane, rule 34). **Halves:** the COO half and the CTO half, each bound to this file's sha256 (printed in each half). **Order:** the apply order to IB2, cut after both halves are signed. **Reads behind it:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/reads/RD_COT_RELANDING_BASELINE_20261017T0930Z.json` @d3103b18ce (before dell1's lane) and `.../RD_COT_RELANDING_AFTER_DELL1_20261017.json` (after the re-pull; the convert of 07-27 and 07-29 read at 14:26Z).
**DAYS:** 2026-07-22, 2026-07-27, 2026-07-29, 2026-08-03

**What this pair does, in one paragraph.** The Cottonwood series is missing 7 trading days. For four of them (the DAYS above) the carrier's `fact_allocations` partition was partial (157, 3, 1 and 159 accounts against about 880), so the gold `account_return_daily` day holds only those rows; dell1's re-pull and the convert then landed those four allocations partitions in full (894, 897, 896 and 901 accounts), and `fact_transactions` is present for all four. **The trading day after each of them (07-23, 07-28, 07-30, 08-04) was derived against the partial day, so its own gold rows are NOT_MEASURABLE (734, 878, 880 and 740 of about 880).** The pair (1) re-runs those EIGHT gold days one at a time through the function's own explicit rewrite event, dry run first, each as a NEW VERSION of its object (every prior version kept), and (2) republishes the Cottonwood series ONCE, so each account that has a row on a re-landed day gains the day and the following day's return becomes measurable. **The write set is the eight gold days and the series/manifest objects the republish rewrites; no other gold day, no schedule, no code, no role.** The three days with no transactions partition (08-19, 09-24, 09-25) are NOT touched: the function holds them, and they wait on a separate ask to dell1 (CTO ruling).

## 1. The acts (nine, in order; each has its own stop)

**Act 0 -- gates and the ledger.** Packet sha256 and both halves; no open leg on the surface; the live state equals section 2. Open the NEVER-2 ledger naming the applier BEFORE any write.

**Act 1 -- before reads (read only).** (a) The gold table `irpt/cottonwood/gold/account_return_daily/`: the partition list (count and the newest); for each of the eight days (the DAYS and 2026-07-23, 07-28, 07-30, 08-04) the object, its VersionId list, its row count and its count of `day_quality` NOT_MEASURABLE rows; the row count of the full neighbour `date=2026-07-21` (879) and the sum over all partitions; (b) the published prefix `irpt/cottonwood/platinum/reporting/`: the `account=` prefixes (939) and the object and version counts; (c) the two functions' CodeSha256 and environments; (d) the schedules (`irpt-cot-account-return-daily-daily` ENABLED; `irpt-cot-reporting-publish-daily` DISABLED); (e) the silver counts for the four DAYS: `fact_allocations` accounts and `fact_transactions` rows (the read tool `reads/cot_relanding_state_read.py`).

**Act 2 -- the DRY RUNS of the gold days.** Eight synchronous events to `irpt-cot-account-return-daily-lambda`, one per day, `{"rewrite": {"start": "<day>", "end": "<day>"}, "dry_run": true}` (`--cli-read-timeout 0 --invocation-type RequestResponse --log-type Tail`), in ascending date order. **Expected:** `ok` true, `days` [that day], `held` 0, and the day's rows between 840 and 960 (the allocations hold 894, 897, 896 and 901 accounts on the DAYS and about 880 on the next days). **STOP** on `held` above 0, a row count outside that band, an exception, a timeout, a Max Memory Used above 819 MB or a duration above 600 s. Nothing is written (the applier reads the gold prefix object and version counts before and after: EQUAL).

**Act 3 -- the REWRITES of the gold days.** The same eight events WITHOUT `dry_run`, in ascending date order. **Expected:** each returns its dry run's rows. After each day: the day holds the new rows as the CURRENT version and the previous version is KEPT (version count +1 for that key); then, after all eight: every other gold partition's object and version counts are EQUAL to Act 1, the schedules are untouched, **and each of the eight days holds at most 15 percent `day_quality` NOT_MEASURABLE rows** (a normal day holds about 3 percent). **STOP before any republish** if a day fails that share or any other partition moved.

**Act 4 -- the pre-write read of the republish (read only).** Run the read tool `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/reads/cot_publish_offline_diff.py` (it reads the gold and the published series and reports, by count, what a republish would change). **Expected:** the accounts that GAIN a DAYS day equal the rewritten day's rows minus those already present; **STOP before any republish** if any field other than `total_return_daily`, `day_quality` and `return_basis` changes on a day present in both versions, if any day other than the next trading day of a DAYS day (07-23, 07-28, 07-30, 08-04) changes in those three fields, if a day is REMOVED from any series, or if the refused count is above 40.

**Act 5 -- the dry run of the republish.** One synchronous `{}` (a dry build, nothing uploaded) to `irpt-cot-reporting-publish-lambda`: `published` 939, `refused` at most 40 (the earlier republish's count; a higher count is a STOP).

**Act 6 -- the canary.** ONE synchronous `{"upload": true, "accounts": ["<one id>"]}` for the first account (sorted) that gains a DAYS day; its id is never recorded, only the first 12 hex of its sha256. Read the series back in memory against the PREVIOUS VERSION of the same object: the dates gained are a non-empty subset of the DAYS; every common day's fields equal the previous version except the three movable fields on the next trading days; the manifest's `publisher_version`, `history_scope` and claim stay as before.

**Act 7 -- the full republish.** ONE synchronous `{"upload": true}` (900 s limit; a lost response is judged from the log). **Expected:** `published` 939, `refused` as in Act 5. The object count is unchanged (same keys, new versions); the version count rises by the number written.

**Act 8 -- the after-read.** The two functions: code hash, memory and environment unchanged; the schedules unchanged; the gold prefix: only the eight days' key sets gained a version; the published prefix: the same 939 `account=` prefixes and the same object count; a sample of 25 series (sorted positions) satisfies the Act 6 invariant against the previous version; the count of series holding each of the four DAYS (each at least 1).

**Act 9 -- the receipt.** Counts, memory and duration; the words "the rewrite changed eight gold days" and "the daily returns of the four days after the re-landed days moved from not measurable to measured" and "the YTD return still reads Not measured while any of the three days with no transactions partition is in the window".

## 2. Pins and live state, measured by this seat at packet time (read-only; the applier re-reads at each act)

- `irpt-cot-account-return-daily-lambda`: `CodeSha256` `+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=`, 1,024 MB, 900 s, no environment, last modified 2026-10-16T19:29:43Z; handler `infra/aws/lambda/investor-reporting/account-return-daily/handler.py` (the `_rewrite` path, DB-b-296: refuses a day before 2026-07-10, a day not already landed, more than 25 days, and any event that also names `day` or `days`; the function derives a day from the `fact_allocations` partitions of that day and the previous trading day and holds a day with no `fact_transactions` partition).
- `irpt-cot-reporting-publish-lambda`: `CodeSha256` `vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE=`, 1,024 MB, 900 s, no environment.
- Gold before (rows / versions / NOT_MEASURABLE): 07-22 157 / 2 / 12; 07-23 879 / 2 / 734; 07-27 3 / 2 / 3; 07-28 881 / 2 / 878; 07-29 1 / 2 / 0; 07-30 881 / 2 / 880; 08-03 159 / 2 / 12; 08-04 888 / 2 / 740; the full neighbour 07-21 879 rows.
- Silver now: `fact_allocations` accounts 07-22 894, 07-27 897, 07-29 896, 08-03 901; `fact_transactions` rows 11,620, 12,519, 3,771 and 5,789.
- Schedules: `irpt-cot-account-return-daily-daily` ENABLED, `irpt-cot-reporting-publish-daily` DISABLED. The 939 published series: PARTIAL_HISTORY, claim `inferred` (the earlier signed republish).

## 3. What each act changes in the world

Acts 1, 2, 4, 5 write nothing. Act 3 writes EIGHT gold days (a new version of each object). Act 6 and Act 7 rewrite series and manifest objects at the same keys (new versions): **each account that has a row on a re-landed day gains that trading day, and the next trading day's daily return becomes measurable; nothing else about a series changes.** **A client-facing sentence this pair can move: the Performance tab of a Cottonwood account (viewed by Opal staff at Global) shows up to four more days, and the "no return can be measured" count falls by the days it repairs.** The page, the route, the roles and every other gold day are untouched.

## 4. Writers of the changed properties, counted

The gold `account_return_daily` day has ONE producer: `irpt-cot-account-return-daily-lambda` (N = 1 writer; its scheduled fire owes only the days AFTER the newest landed day, so it never touches a landed day). The series and manifest objects have ONE writer: `irpt-cot-reporting-publish-lambda` (N = 1; its schedule is DISABLED). The transaction-stage code of another seat (`~F2`, DB-f-2605) is NOT deployed on this function; the CTO's order is this pair first, then that code.

## 5. Both branches

**Branch A:** every act returns what it states. **Branch B (a dry run outside its band, a held day, a gold day above the NOT_MEASURABLE share after Act 3, a pre-write read outside its STOP lines, a canary that breaks the invariant):** STOP before the next act; the prior versions are the rollback. **Branch C (memory or time):** above 819 MB or a duration above 600 s (gold) or 850 s (publish): STOP. **Branch D (a scheduled fire overlaps an act):** none between 12:05 and 13:15 UTC on a weekday; the account-return fire owes days after the newest landed day only.

## 6. Rollback, per key

Gold: the previous version of each rewritten day is kept; the rollback is a COPY of that version over the key (a write, by the applier, under the ledger); no version is deleted. Series: every key has its prior version; the rollback is a per-key copy of the previous version, from the receipt's counts. No code, role or schedule changed, so none rolls back.

## 7. Conditions

1. **Ledger first,** bound to this packet's sha256; `.open_deploys/` read across every live worktree with the denominator printed.
2. **Live state re-read at the moment of each act;** a difference from section 2 other than the scheduled fires' own outputs is recorded before the act.
3. **Stop at once** on a timeout, an `AccessDenied`, a memory or duration line above, or a response outside the act's expectation. Counts and words only: never an account id, a name or a body.
4. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no schedule change, no other gold day, no environment variable.** Outside the 11:30Z to 14:15Z weekday band.
5. **The CTO's ordering (msg 10391):** this pair applies BEFORE `~F2`'s transaction pair on this function; an open ledger of this pair on the account-return root stops that pair's Act 2.

## 8. Questions for the CTO's half

1. Accept that the republish (Acts 6 and 7) is part of this pair although the rewrites' own write set is eight gold days? 2. Accept the EIGHT days (the four re-landed days and the four after them: the gold rows of the four next days are NOT_MEASURABLE in the gold itself, so the republish alone cannot repair them)? 3. Accept the Act 3 stop line (at most 15 percent NOT_MEASURABLE on each of the eight days) and the Act 4 STOP lines (only the three movable fields on the four next days may change on a common day)? 4. Accept that the three days with no transactions partition are not touched here?

## 9. Not established, and so not covered

That each rewrite produces about 880 to 900 rows (the dry runs are the first runs of these days against the full allocations); that the dependent days become at least 85 percent MEASURED (Act 3's read is the first measurement); that the carrier's own source holds a transactions partition for the three held days (dell1's lane); the page.
