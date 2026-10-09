# STAGED (not issued) -- MDPF_SECHIST round 6 candidate: expiry for the depth-bound exhausted list (row D1-S1)

Source: 1.0.0_SA_CTO~DELL1 CTO half on SH-t-8's take, condition 2 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SECHIST_SH_T8_SITEZ_TAKE_20261009.md`,
msg 2848): "Round 6 cuts an expiry: an exhausted entry is retried after a stated number of trading days. Negative arm: a ticker with a
stored date and real zero rows stays off." Issued only on the round-5 analysis's enrichment list; staged so the cut is same-tick.

## The cell (worker-light; risk SERVED; LOCAL code + tests)

`integrations/bloomberg/pipeline/etf_daily_pull.py`: an entry in `history_backfill_exhausted` (ticker -> entry as-of, AMENDMENT 1 of
TO-SH-t19 @09b6a7d580) whose entry date is more than `EXHAUSTED_RETRY_TRADING_DAYS` trading days before the run's as-of is planned
again (trading days from `lib/trading_calendar.py`, the one frontier; the constant stated in the module, value proposed 20, ruled at
the analysis). A retried ticker that again returns zero rows re-enters the list with the NEW as-of. An entry with a null date (old list
form) is retried on the first run after the take. Pure function; fakes only.

## Criterion (dry-run at base e086d0b429: BAD on both names)

`python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECHIST_H1/R3_CHECKS/r3_named_tests.py PULLX integrations/bloomberg/pipeline/test_etf_daily_pull_history_plan.py test_exhausted_entry_retried_after_expiry test_exhausted_entry_kept_within_expiry`
-> `PULLX-TESTS-OK` (base: `PULLX-TESTS-BAD not-passed=both`).

## Paths

`integrations/bloomberg/pipeline/etf_daily_pull.py`, `integrations/bloomberg/pipeline/test_etf_daily_pull_history_plan.py`.

## Deploy note

A second site-Z take of the same file (a new blob), under its own pair; batch it with any other round-6 pull change so site Z takes once.
