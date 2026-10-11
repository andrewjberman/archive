# CB-bp-4 -- method_r29 against the served table, at the served instant's pin

Worker 0.9.0_WK_ADVI_COTBKF~104, order ADVI_COTBKF.TO-CB-bp-4. Counts, dates and reason codes only. Nothing was written
remotely: no --apply, no --overwrite, no S3 put, no serve. Record: `R28_VS_R29_AT_PIN.json`; dates: `CHANGED_DATES_AT_PIN.csv`.

## Result

- The pin: `SPLIT-STORE-PIN ... as_of=2026-10-09T11:52:52Z listed=32 held=32 sha256=4aca4f1f...a362c7`, printed identically by both regrades.
- Control (run first): method_r28 at the pin, serve build, against the served `daily_returns.parquet` on (account, date, return to
  1e-12, blank_reason): 1,691,729 rows compared, 0 differing.
- method_r29 at the same pin against the SERVED table (r28 re-run and served table are equal, so this is also r29 against r28 at the pin):
  `both_measured_same` 107,314; `both_measured_different` 2; `measured_served_only` 0; `measured_r29_only` 0;
  `both_blank_same_reason` 1,584,413; `both_blank_reason_changed` 0; `row_served_only` 0; `row_r29_only` 0. Sum 1,691,729 = the union.
- Changed account-days: 2, on 2 dates: 2014-12-03 and 2020-11-13 (one each). These are round 66's two dates: `same_dates_as_round_66` true.
- Origin: both are among the 71 withholding account-days with no same-day CFNCASH withdrawal row (recomputed from the transaction cache:
  4,115 account-days carry a CFNCASH ftax or stax row, 71 without a same-day `lo`, 70 of the 71 on a row of the returns table).
  `same_account_other_day` 0; `other_account` 0.
- Month grades, served against the r29 build, 82,593 account-months keyed on both sides: verdict changes 0; ABSENT changes 0 (the same 5
  account-months are ABSENT in both, reason REGRESSED_UNDER_AS_TRADED); computed_pct changes in 1 account-month.
- Inputs: after/security_day_price.parquet of the two regrades equal row for row (2,124,908 rows).
- Spin-off events in the store at this pin: 0 of 4 (the sidecar lists 32 CUSIP partitions; 00206R102, 438516106, 460146103,
  717081103 are not among them). The CB-bp-3 claims (each UNAPPLIED_NO_HELD_DATE) change nothing at this pin. No mechanism was built.

## Round 66 against this

Round 66 compared on today's store (141 partitions) and found the same 2 account-days on the same 2 dates, 0 month changes. Moving the
pin back to the served instant does not change the list. The 30 drift account-days of round 66's control come from the store's growth
after the served instant; at the pin the control has 0.

## Runs (all local, from this worktree, COTBKF_SWEEPS_CONFIG on each command)

- r28 regrade 14:20:00Z-14:28:14Z (494 s); r28 serve build 14:29:10Z-14:37:27Z (497 s).
- r29 regrade 14:38:16Z-14:47:47Z (571 s); r29 serve build 14:48:04Z-14:56:04Z (480 s).
- Each run copied its own price cache from the pinned source; the Yahoo Close cache was this worktree's own scratch copy.
