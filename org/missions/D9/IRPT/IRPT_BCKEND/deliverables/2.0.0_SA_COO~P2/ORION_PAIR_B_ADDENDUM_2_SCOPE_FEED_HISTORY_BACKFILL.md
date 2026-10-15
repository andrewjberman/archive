# NEVER-WIDEN PAIR (b), ADDENDUM 2 -- IRPT_BCKEND: the one-time history backfill of the Orion Scope account feed

**Status: DESIGN. The COO half is a separate file bound to this file's blob; the CTO half is not signed.** Nothing here is built, pulled, deployed, written to AWS, invoked, signed or sent; no Orion request is made by this file.

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~17:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO's msgs 8456 and 8484 (round-118 ADDENDUM 2 and ADDENDUM 3) and B-IN's round-122 probe (`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~I2/IRPT_DASHBD_ROUND122_BIN_DRAIN_END_20261015.md`, @5784c51349). It amends pair (b) ADDENDUM 1 (`ORION_PAIR_B_ADDENDUM_1_SCOPE_ACCOUNT_FEED.md`, blob 1e138cbeea, both halves signed) and changes no other line of it.

## 1. What the act is

ONE run of the feed's own script (`data/inf/manual_api/pull_inflection_scope_account_returns.py`, builds IB-pr-586 and IB-pr-594) with its `--from-date` window, once, by CloudOps `0.7.0_AE_CloudOps~IB2`, AFTER addendum 1's first scheduled run has been read: **one Scope call per household** (the same inner scope body, grouping Account, Daily frequency, `calcGrossOfFees` false) over the window from the earliest account start date to the pull date, so the account pages' quarter-to-date, year-to-date, last-twelve-months and since-inception windows have history from the first day instead of months from now. It writes the same rows by the same coverage rule as the scheduled feed, to the feed's OWN prefixes, one partition per calendar day.

## 2. The rules the run carries (CTO msgs 8456 and 8484)

1. **The measured bound (B-IN's probe).** 294 requests: one per household; about 537 seconds serial; about 337 MB ceiling; two probe calls took 1.7 s and 1.8 s. **The STOPs:** (a) the household count is re-read at the apply, 294 is the measured figure and a higher count must be stated in the apply order before any call; (b) 20 minutes of wall clock; (c) a 429 or throttle response that persists after the limiter's own retries. The 337 MB figure is not a stop.
2. **Store the DAILY FACTOR only.** Series points are calendar-day and contiguous from each account's start; chained factors equal Orion's period return up to a year, and Orion annualizes its summary over a year. The row's value is the point's `factor`; the summary `performance` is never stored, so annualization is untouched.
3. **`SERIES_ENDED_AT_SOURCE` is admitted** (the probe saw two series end 95 and 120 days early): each day after an account's last point is an `ABSENT` row with that reason, claim `measured`, never a zero and never an Opal fill. The reason classes of addendum 1 stand (`NO_GROUP`, `GROUP_NO_SERIES`, `NO_START_DATE_AT_SOURCE`).
4. **Calendar days, weekends included:** the chain is by calendar day; a non-trading day takes its universe from the previous trading day's held accounts.
5. **Every day's keys are read ABSENT first and an existing day is SKIPPED, never overwritten.** The scheduled feed's days (written before or after) and this run's days therefore cannot collide; a re-run writes nothing it already wrote.
6. **`.json.gz` bronze, not `.jsonl.gz`,** and only the feed's prefixes, as addendum 1 section 2 item 6.

## 3. The write set and its disjointness

The backfill writes the feed's two prefixes for the calendar days before the first scheduled run's partition: new keys only. The number of partitions is the count of calendar days from the earliest roster start date to the day before that partition; **it is stated in the apply order from the roster at the apply** (an estimate here would be a guess; the order of magnitude is thousands of keys of the two tiers). It writes no key of pair (a), no existing bronze or silver key of any other table, no gold key, no schedule, IAM principal or Terraform resource.

## 4. Preconditions of the apply (each is a STOP in the apply order)

1. Addendum 1's apply has landed and its first scheduled run has been read (feed keys exist for the day, each account carries a factor or an `ABSENT` row with a reason class; every request carried `calcGrossOfFees` false).
2. The household count re-read at the apply is stated; a count above 294 stops the run until the order says so.
3. The earliest account start date is read from the roster snapshot and printed with the partition count BEFORE the first call.
4. The runner can write the feed's prefixes in the address bucket (addendum 1, row W429-S3 is read at the first apply).

## 5. Blast radius, rollback, stop rule

- **Writes:** the feed's keys for the history window (new, ABSENT first). **Reads:** the Orion API (one call per household), the roster and positions silver. **Served values changed: none** (nothing reads the feed until B-IN's adapter is cut).
- **Rollback, per key:** the new keys are removed by version (a delete is Andrew's act); the reading side does not wait on a delete: the adapter ignores a partition until the CTO names the window it may read. Nothing else reverts.
- **Stop rule:** the three STOPs of section 2 item 1; a call whose body is not the inner scope; any request that is not `calcGrossOfFees` false; a key not read ABSENT first; a zero written for a missing account; a value stored that is not the daily factor; any need to touch a key outside the feed's prefixes.

## 6. What this addendum does not cover

The adapter that reads the feed; which window the account pages may read (the CTO's call after the run); a second backfill; fixing null start dates at the source (Andrew's act).

-- 2.0.0_SA_COO~P2
