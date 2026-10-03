# AMGT_RESAPP round 66 -- `AMGT-ap-2` drain = THE DAILY JOB'S DEPLOY, never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-03 ~22:2xZ

**The act (ONE):** `2.0.0_SA_COO~Z` drains `wk-AMGT_RESAPP-218` (ap-2, `c549695b69` + `db56406c8e`) into CLOUD in the shared tree
with `.tools/safe-merge.sh`.
- The scheduled task `\OPAL_BBGTML_daily_pull` runs `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd` from the working
  tree. The cmd calls `price_axis_pull.py` with no arguments, so **the drain IS the deploy of the daily job's change.**
- Authority: ANDREW-DIRECT ~20:5xZ "your rec is approved" (ROUND_ANALYSIS.round65.md ADDENDUM 2 @205bd13011).
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-ap-2.price-history-build.md`.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| CLOUD HEAD | `72f2c9be42` |
| `price_axis_pull.py` blob at HEAD | `f173bdd833809b0145a517a3bd61621f3ee0ec3d` (after the drain: `cb73d6c64a0d506d227712d02f5acdf664da91b7`) |
| scheduled task | `\OPAL_BBGTML_daily_pull`, Ready; last run 2026-10-03 11:00:01Z, result 0; **next run 2026-10-04 11:00Z** |
| 30-day pointers, as_of 2026-10-02 | TRENDING_PRICE `20261003T110628Z-4ff62071cb80` COMPLETE 94 rows; BREAKOUT_PRICE `20261003T110629Z-d4cfe7cba7f3` COMPLETE 94 rows (run `R20261003T110628Z`) |
| 90/365 pointers | TRENDING_PRICE_90D, BREAKOUT_PRICE_90D, TRENDING_PRICE_365D, BREAKOUT_PRICE_365D: **NO POINTER** |
| S3 history | `s3://opal-data-harvest/bloomberg/harvest/bronze/price_history_px_last/`: not yet written (the `--plan` read) |

## THE FILE LIST (`git diff 72f2c9be42...db56406c8e`, 9 code files, +1287 / -0)

| file | change | effect after the drain |
|---|---|---|
| `integrations/bloomberg/research/price_axis_pull.py` | +17: one guarded call to `price_series_persist.run_daily_window_step`, after the 30-day writes and before the exit-code logic | each scheduled run then does the two steps below |
| `integrations/bloomberg/research/price_series_persist.py` | NEW | the history writer and the daily 90/365 step |
| `integrations/bloomberg/research/price_history_pull.py` | NEW | runs only by hand (ap-3) |
| `lib/research/price/generation.py` | +168 / -0 (additive: `window_series`, `compute_price_window_axes`) | the 30-day path's functions are unedited; the existing price tests pass unchanged (42 passed) |
| `lib/research/api/scoped_amgt.py`, `rolling_windows.py` | +79, +22 | the `?days=90|365` route read; serves nothing until ap-4 redeploys the function |
| tests (3 files) | new / +2 | none |

**What each scheduled run does after the drain:**
1. Persist that run's already-fetched 30-day series as `.../date=<as_of>/daily_30d.json`, write-once.
2. Build the 90/365 generations from the stored history.

Any other changed file at drain time is a STOP.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

The writers of each property (N writers means N rules read):
- 30-day partitions: 2 writers, `price_axis_pull.py` (daily) and `backfill_legacy_generation.py` (manual). Neither 30-day rule
  changes.
- 90/365 partitions: 2 writers after the act, the daily step and `price_history_pull.py --live`. Both go through ONE rule,
  `generation.compute_price_window_axes`.
- S3 history: 2 callers of ONE writer, `persist_series`, which is write-once.

| what | MAY touch | rollback |
|---|---|---|
| the drain | the shared tree's files in the list above | `git revert` of the drain commit on CLOUD (a new commit, no history rewrite) BEFORE the next scheduled run; the job then runs the prior code |
| each scheduled run after it | ONE S3 object per as_of under `bloomberg/harvest/bronze/price_history_px_last/date=<as_of>/daily_30d.json` (write-once, never overwritten); the four 90/365 partitions and their `_CURRENT` pointers in `opal-harvest-security-metrics` | additive and inert: no deployed reader until ap-4. A revert stops further writes. Removing written objects or partitions is an S3/table delete and needs Andrew's word, so nothing here deletes |

**NEVER written by this act:** the 30-day partitions TRENDING_PRICE# and BREAKOUT_PRICE#, their pointers, and the leg's exit codes
(0 / 3 / other).

## EXPECTED OUTCOME -- both branches, for the next scheduled run (2026-10-04 11:00Z, as_of 2026-10-02: Sunday's T-1 is Friday)

| | branch A: ap-3's year pull HAS landed before the run | branch B: it has NOT |
|---|---|---|
| 30-day leg | a new COMPLETE generation for TRENDING_PRICE and BREAKOUT_PRICE (94 rows each, as today); exit code 0 | identical |
| persist | `daily_30d.json` for 2026-10-02 written once | identical |
| 90/365 step | the four 90/365 generations for 2026-10-02 built from the history | skipped, with the logged reason "no year history" |
| deployed function (`lPTMo20T`) | DELTA=0: it reads no 90/365 partition | identical |

These are read from the producer's own code, not predicted from the input's shape:
- `run_daily_window_step` never raises; its result is not read by the exit-code logic.
- `NoYearHistory` means a skip.
- `persist_series` refuses a different body for an existing as_of.

**Failure branch:** any of these means `git revert` of the drain before the following run, and a row:
- the 30-day leg's exit code differs from 0;
- its row counts move from the run's own universe (95 covered, 94 ranked);
- any write lands in a 30-day partition.

## WHAT THIS HALF DOES NOT COVER

- Any of these in the drain is a STOP: a vendor request (the daily step adds none: `price_series_persist.py` imports no blpapi),
  an edit to `scheduled_daily_pull.cmd`, a schedule change, an S3 delete, an IAM change.
- The one-time `--live` year pull is ap-3's act.
- The function redeploy is ap-4's, under its own pair.
