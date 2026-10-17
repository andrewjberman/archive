# NEVER-WIDEN PACKET (DRAFT, not yet bound) -- every landed Cottonwood gold day from 2026-07-10 REWRITTEN with the late-posting reader (66 days in four events), and the series republished ONCE (IRPT_DASHBD round 150; CTO rulings msgs 10587, 10591, 10598 and 10627)

**Packet author:** 2.0.0_SA_COO~D2. **Status:** DRAFT. It is bound (a sha256 printed in each half) only AFTER `~F2`'s transaction pair has applied the code release, because section 2 pins the post-release function code. **Applier:** `0.7.0_AE_CloudOps~IB2` (the one IRPT CloudOps lane, rule 34). **Halves:** the COO half and the CTO half, each bound to this file's sha256. **Order:** the apply order to IB2, cut after both halves are signed. **Replaces:** `TO-DB-b-332` (the eight-day re-land pair, superseded; its CTO half @e5d081d262 is suspended, not withdrawn). **Reads behind it:** `reads/RD_COT_ALLDAYS_STATE_20261017.json` @5559b3be93 (the days and the four events), `reads/RD_COT_ALLDAYS_DRY_20261017.json` @b07bdf34e0 (a read-only derivation of all 66 days with the trunk adapter), `reads/cot_alldays_state_read.py`, `reads/cot_alldays_dry_read.py`.

**What this pair does, in one paragraph.** The landed Cottonwood gold `account_return_daily` sums every `fact_transactions` partition on or after a day, and those partitions are rolling pulls that repeat each trade, so the landed external flows are inflated up to 14 times (surprise row `IRPT_DASHBD-D2-S137`); four days were landed from partial allocations; the four days after them are 83 to 100 percent NOT_MEASURABLE. The code release (`TO-DB-b-334` re-pin; the late-posting reader of `TO-DB-b-333`; `~F2`'s stage) is applied before this pair. This pair (1) rewrites all 66 landed trading days from the claim floor 2026-07-10 through the function's explicit `rewrite` event, in FOUR events of landed trading days only (25, 3, 24 and 14 days), dry run first, each day a NEW VERSION of its object (every prior version kept), and (2) republishes the Cottonwood series ONCE. **The write set is the 66 gold days and the series/manifest objects the republish rewrites; no code, no schedule, no role, no other gold day.** Days not landed (08-19, 09-24, 09-25: no transactions partition, awaiting dell1's re-request; 10-16: owed to the scheduled fire) are NOT touched.

## 1. The acts (ten, in order; each has its own stop)

**Act 0 -- gates and the ledger.** Packet sha256 and both halves; no open leg on the surface; the live state equals section 2; `TO-DB-b-332` and its ledger closed (they are); `~F2`'s transaction pair applied and its ledger closed. Open the NEVER-2 ledger naming the applier BEFORE any write.

**Act 1 -- before reads (read only).** (a) The gold table `irpt/cottonwood/gold/account_return_daily/`: the partition list (66 days from the floor plus any landed since; count and newest), and for EACH day its VersionId list, row count, `day_quality` NOT_MEASURABLE count, and the sum of absolute `external_flow`; the sum of all partitions' rows; (b) the published prefix `irpt/cottonwood/platinum/reporting/`: the `account=` prefixes (939) and the object and version counts; (c) the function's CodeSha256, memory, timeout and environment (equal to section 2); (d) the schedules; (e) the read tools `reads/cot_alldays_state_read.py` and `reads/cot_alldays_dry_read.py` run by the applier from the trunk tree (read only), whose per-day rows must equal Act 2's dry runs.

**Act 2 -- the DRY RUNS.** (2a, scaling) ONE single-day synchronous event `{"rewrite": {"start": "2026-07-24", "end": "2026-07-24"}, "dry_run": true}` to measure the duration and Max Memory Used of one day. (2b) The four events, ascending, each `{"rewrite": {"start": "<first>", "end": "<last>"}, "dry_run": true}` (`--cli-read-timeout 0 --invocation-type RequestResponse --log-type Tail`): 2026-07-10..2026-08-13 (25 days), 2026-08-14..2026-08-18 (3), 2026-08-20..2026-09-23 (24), 2026-09-28..2026-10-15 (14). **If 2a shows a projected duration above 500 s for a 25-day event, the applier splits that event into ranges of landed trading days whose projection is at most 500 s and records the split before Act 3.** **Expected per day:** `held` 0 and the day's rows equal to the dry read of `RD_COT_ALLDAYS_DRY_20261017.json` (61 days equal their landed rows; 07-22 894, 07-27 897, 07-29 896, 08-03 901 and 10-15 956 are the five that differ). **STOP** on `held` above 0, a row count that differs from the dry read by more than 2 percent, an exception, a timeout, a Max Memory Used above 819 MB (80 percent) or a duration above 720 s (80 percent of 900 s). Nothing is written (the applier reads the gold prefix object and version counts before and after: EQUAL).

**Act 3 -- the REWRITES.** The same events WITHOUT `dry_run`, ascending. **Expected:** each returns its dry run's rows. After each event: every day of it holds the new rows as the CURRENT version and its previous version is KEPT (version count +1 for each key); then, after all events: every other gold partition's object and version counts EQUAL Act 1, the schedules are untouched, **each rewritten day holds at most 15 percent NOT_MEASURABLE rows EXCEPT the floor day 2026-07-10 (100 percent: it has no previous day)**, and **each day's sum of absolute external flows is at most its Act 1 value, except the five days whose rows differ (their sums may rise)**. **STOP before any republish** if a day fails either share or any other partition moved.

**Act 4 -- the pre-write read of the republish (read only).** Run `reads/cot_publish_offline_diff.py` (it reports, by count, what a republish would change). **Expected:** `total_return_daily`, `day_quality` and `return_basis` may change on common days (the flows are corrected, so a daily return moves on every day that had an external flow and on the next day's measurability), nothing else on a common day; the accounts that GAIN a day equal that day's rows minus those present; **STOP before any republish** if any field other than those three changes on a day present in both versions, if a day is REMOVED from any series, or if the refused count is above 40.

**Act 5 -- the dry run of the republish.** One synchronous `{}` to `irpt-cot-reporting-publish-lambda`: `published` 939, `refused` at most 40.

**Act 6 -- the canary.** ONE synchronous `{"upload": true, "accounts": ["<one id>"]}` for the first account (sorted) with a changed day; only the first 12 hex of its sha256 is recorded. Read the series back in memory against the PREVIOUS VERSION: dates gained are a subset of the five changed-row days; every common day's fields equal the previous version except the three movable fields; the manifest's `publisher_version`, `history_scope` and claim stay as before.

**Act 7 -- the full republish.** ONE synchronous `{"upload": true}` (900 s limit; a lost response is judged from the log). **Expected:** `published` 939, `refused` as in Act 5. Object count unchanged (same keys, new versions).

**Act 8 -- the after-read.** The function: code hash, memory and environment unchanged; schedules unchanged; the gold prefix: only the rewritten days' key sets gained a version; the published prefix: the same 939 prefixes and object count; a sample of 25 series (sorted positions) satisfies the Act 6 invariant; the count of series holding each of 07-22, 07-27, 07-29, 08-03 and 10-15 (each at least 1).

**Act 9 -- the receipt.** Counts, memory and duration per event; the words "the rewrite changed 66 gold days", "the external flows of the landed days are no longer summed across overlapping transaction partitions" and "the daily returns of the four days after the re-landed days moved from not measurable to measured"; and the YTD sentence ("the YTD return still reads Not measured while any of 08-19, 09-24 or 09-25 is in the window").

## 2. Pins and live state (TO BE MEASURED after `~F2`'s pair applies; the applier re-reads at each act)

- `irpt-cot-account-return-daily-lambda`: CodeSha256 = the release bundle (BUILD_ONLY `pa5JdBfOL2GUA6b/UU5sp9upDcj0JGjCQ4+xCOass9g=` at release commit 36da4e101f) as deployed by `~F2`'s pair; memory 1,024 MB; timeout 900 s; handler `infra/aws/lambda/investor-reporting/account-return-daily/handler.py` (the `_rewrite` path refuses a day before 2026-07-10, a day not landed and more than 25 days; the scheduled fire settles at most 5 landed days 14 trading days back, none before the floor).
- `irpt-cot-reporting-publish-lambda`: CodeSha256 `vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE=` (re-read), 1,024 MB, 900 s.
- Gold before: from `RD_COT_ALLDAYS_STATE_20261017.json` (70 allocations partitions, 66 landed days, 0 landed without allocations; 08-19, 09-24, 09-25, 10-16 have none) re-read at packet time.
- Schedules and the published series: re-read at packet time.

## 3. What each act changes in the world

Acts 1, 2, 4, 5 write nothing. Act 3 writes 66 gold days (a new version each). Acts 6 and 7 rewrite series and manifest objects at the same keys. **The client-facing change: Performance-tab daily returns of Cottonwood accounts MOVE on every day that had an external flow (the flows are no longer inflated up to 14 times), the four days after the re-landed days become measured, and four days gain rows. The YTD sentence and the page are unchanged.** This is why the CTO's half must accept that returns will move on common days.

## 4. Writers of the changed properties, counted

The gold day has ONE producer: `irpt-cot-account-return-daily-lambda` (N = 1; its scheduled fire owes days after the newest landed day and settles at most 5 landed days 14 trading days back, none of which a rewrite event conflicts with if no act overlaps a fire). The series and manifest have ONE writer: `irpt-cot-reporting-publish-lambda` (N = 1; schedule DISABLED, re-read).

## 5. Both branches

**A:** every act returns what it states. **B (a dry run outside its band, a held day, a share above 15 percent, a pre-write read outside its STOP lines, a canary that breaks the invariant):** STOP before the next act; the prior versions are the rollback. **C (memory above 819 MB or duration above 720 s gold / 850 s publish):** STOP. **D (a scheduled fire overlaps an act):** none between 12:05 and 13:15 UTC on a weekday.

## 6. Rollback, per key

Gold: the previous version of each rewritten day is kept; the rollback is a COPY of that version over the key (a write, by the applier, under the ledger); no version is deleted. Series: every key has its prior version; per-key copy from the receipt's counts. No code, role or schedule changed.

## 7. Conditions

1. **Ledger first,** bound to this packet's sha256; `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of each act.** 3. **Stop at once** on a timeout, `AccessDenied`, a memory or duration line above, or a response outside the act's expectation. Counts and words only: never an account id, name or body. 4. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no schedule change, no other gold day, no environment variable.** Outside the 11:30Z to 14:15Z weekday band. 5. **Order (CTO msg 10627):** the 49F read, Inflection, `~F2`'s pair, then this pair.

## 8. Questions for the CTO's half

1. Accept that the republish is part of this pair? 2. Accept that daily returns move on common days (the cure), with the Act 4 STOP lines as written? 3. Accept the floor-day exemption and the 15 percent line on the other 65 days? 4. Accept four events sized by Act 2a's duration projection (split allowed, never merged beyond 25 days)? 5. Accept that 08-19, 09-24, 09-25 and 10-16 are not touched?

## 9. Not established, and so not covered

The duration of a 25-day event on the function (Act 2a is the first measurement); that the post-release scheduled fire has produced no new landed day between this draft and the apply (re-read); that the page reads the new series as expected (a browser walk is owed before PROD); the transactions for the three held days (dell1's lane).
