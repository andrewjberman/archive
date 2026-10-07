# IRPT_DASHBD TO-DB-b-38 -- the lot-lag bound, measured (counts only)

Worker 0.9.0_WK_IRPT_DASHBD~22, round 25 workstream B, cell DB-b-38. S3 was read, never written. The evidence is
`LOT_LAG_E2.json` beside this file; `lot_lag_e2.py` regenerates it. No client figure, balance or account number is quoted here.

## What was measured

The same 91 graded accounts and window as round 24 (2026-09-01..2026-10-05, 24 trading days). For each trade that opens or relieves a
lot, the lag is the trading days between the day the transaction posts in `fact_trn` and the day its lot row posts in the lot tables.
The lot tables were read to 10 trading days past the window's last day (to the last partition that exists).

| kind | trades | matched | unmatched | lag 0 | lag 1 |
|---|---|---|---|---|---|
| sells (fact_rld, by order) | 108 | 108 | 0 | 108 | 0 |
| buys (open or closed lot of the trade date) | 765 | 765 | 0 | 765 | 0 |
| in-kind arrivals | 10 | 10 | 0 | 10 | 0 |
| in-kind departures | 4 | 4 | 0 | 3 | 1 |
| all | 887 | 887 | 0 | 886 | 1 |

- Percentiles over the 887 matched lags: p50 0, p90 0, p95 0, p99 0, max 1.
- Of the 765 buys, 758 match a lot acquired on the trade date and 7 (reinvested dividends) a lot whose original-purchase date is the
  trade date. A first pass keyed on the acquired date alone left those 7 unmatched; they are the same-day lots with an earlier
  acquired date.
- In-kind legs were matched by the producer's own matcher with the bound lifted to 30, so the lag they show is the data's, not the
  bound's. The matcher's one other listing (a sale of under one share that links to no single lot) is not a leg and is not counted.
- Unmatched trades: 0 of 887.

## The choice

`leg_lag_days` = 1, covering 100.00% of the 887 lags (the smallest whole number of trading days with every matched lag at or under
it; no margin added, because a leg past the bound is listed unmatched and never bent). Round 24's 3 was a bound the worker chose; the
data shows lags of 0 and one of 1.

`LEG_LAG_DAYS` in `account_activity_lots.py` is now 1. The producer's 31 tests pass.
