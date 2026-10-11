# MDPF_CANON round 5 -- the Sunday 2026-10-11 fire read and the first new-home bronze read (2.0.0_SA_COO~D1, 13:3xZ)

Two issuer reads, both read-only. The CTO's round-4 analysis (item 3) says the Sunday fire is "read it, do not grade it"; item 4 grades FWD-7's first
feed. Instruments: `round4/checks/r4_daily.py` (the round-2 daily read with its own snapshot, taken 06:45Z before the fire) and
`round4/checks/r4_daily_bronze.py`.

## 1. The Sunday 13:30Z gold fire (read, not graded)

`python r4_daily.py read --fire 2026-10-11T13:30:00Z` at 13:37Z. Frontier read as 2026-10-09 (Friday).

| arm | verdict | detail |
|---|---|---|
| 1 CURRENT | FAIL (read, not graded) | 6 of 12 series at the frontier; behind by 1 trading day, newest 2026-10-08: 49financial, inflection and global `aggregate_aua_timeseries` and `aum_metrics` |
| 2 UNCHANGED | PASS | 547 of 547 snapshot keys kept their ETag; gone 0, rewritten 0 |
| 3 PARITY | PASS | 6 of 6 frontier partitions value-equal to the writer's records of their legacy JSON (global compared: 1) |
| 4 UNITS | FAIL (read, not graded) | global holds no `account_units` object (0 objects at the 06:45Z snapshot), so the arm reads 2 of 3; Saturday's read gave the same 2 of 3 (D1-S9) |

What the lambda's own log says for the fire (`/aws/lambda/mdpf-gold-lambda`, stream of 2026/10/11, last event 13:31:43Z):
- `SCOPE FAILED (isolated): global -- AssertionError: CROSS-AXIS COHERENCE GATE FAILED (global) -- REFUSING TO EMIT`, `(v) presence disagreement: 5 across 1 date(s)`;
- `gold parquet: PARTIAL -- built ['inflection'] of intended [...]`, `cycle complete: 12/16 A4 objects built; errors=['global']`;
- the 49financial and inflection cross-axis gates PASS; the global as-of stays 2026-10-08 (newest served `aggregate-aua-timeseries/2026-10-08.json`).

This is the D1-S10 ruling's predicted weekend behaviour, the same shape as Saturday's fire (row D1-S9): the value leg ends Thursday, the cross-axis gate
refuses global alone, firm scopes build and do not move. Nothing to cut; the grade is Monday's fire.

## 2. The first new-home bronze delivery (FWD-7)

`python r4_daily_bronze.py --run-date 2026-10-11 --since 2026-10-11T06:00:00Z` at 13:38Z, after the daily dispatch finished.

| arm | verdict | detail |
|---|---|---|
| 1 PULL | PASS | the builder's `date=2026-10-11` holds 9 `model_<id>.json` and 1 `_meta/pull_complete.json`, sentinel LastModified 12:52:46Z (written by the daily, after the 04:5xZ hand pull) |
| 2 STEP | PASS | runner run `mdpf_daily_20261011_125228` status complete, `STAGE0-BRONZE` ok |
| 3 FEEDER | PASS | the three Inflection feeds (`model_composition`, `model_aua_positions`, `non_model_aua`) newest 2026-10-11.parquet, written 12:52:52Z-12:52:53Z |
| 4 OLDHOME | PASS | 0 of 1030 old-prefix objects written at or after 06:00Z |

So the daily chain, on the code CloudOps deployed by hand at 05:0xZ, pulled to the builder's address, ran the feeder against it and wrote the feeds, with the
old home untouched. That is the first new-home daily delivery. Not shown: this is one run; the feeds' values were read against the live feed on the
2026-10-09 date by the CloudOps leg L7 (DELTA=0), not against today's run.

## 3. Still owed

Monday 2026-10-12 13:30Z: `python r4_daily.py read --fire 2026-10-12T13:30:00Z` (grades FWD-1, CN-a-2 AC3; closes D1-S9, D1-S10). CN-d-1's deploy
waits on `MDPF_STRATID.TO-APPLY-R2`'s L4 read.
