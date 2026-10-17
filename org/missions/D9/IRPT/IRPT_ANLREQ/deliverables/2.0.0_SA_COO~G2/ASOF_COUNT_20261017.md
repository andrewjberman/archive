# The pricing as_of pair: how many reports change (row IRPT_ANLREQ-D2-S163; CTO msg 10242 item 1)

`2.0.0_SA_COO~G2`, 2026-10-17 ~03:3xZ. READ ONLY; counts and dates only; no holdings, names or request ids were printed or kept.

## Question

Under the trading-calendar T-1 rule (`prev_trading_day(expected_last_trading_day(day))`, `lib/trading_calendar.py`) instead of today's weekday rule (`reports/resident_installed.py:379-385`, `_t_minus_1`), how many DELIVERED reports (and queued requests) would print a different price as_of?

## Measured

Method: `asof_count_read.py` (this folder; output `ASOF_COUNT_OUTPUT_20261017.txt`). For each firm bucket (`cottonwood`, `49financial`, `inflection`; bucket and key from `lib/opal_naming.py address()`), list `irpt/<firm>/state/ycharts_runs/request=*/run.json`, read each, read `settings.price_as_of`.

| firm | run.json objects | priced (`settings.price_as_of` present) |
|---|---|---|
| cottonwood | 14 | 0 |
| 49financial | 2 | 0 |
| inflection | 0 | 0 |
| **all** | **16 listed, 16 read, 0 unreadable** | **0** |

The newest run record was written 2026-10-15T17:00:42Z. The price stage was switched on by r34g (2026-10-16), so no delivered report carries a price as_of: **0 of 0 priced reports would change.** The generation queue `irpt-generation` read 0 messages and 0 not visible at 03:31Z, and IB2's V1 at r34k read the resident queue 0 0: **no queued request** would change. The `irpt-jobs` table holds 57 rows (22 READY, 24 ATTENTION, 8 FAILED, 3 stateless); the READY ones are the YCharts-vendor path with no Opal price as_of.

## The prospective effect (what the pair would change from the first priced report)

Computed from the two rules, by day of the run (UTC date `d`):

| run day | weekday rule prints | calendar rule prints | differs |
|---|---|---|---|
| Tuesday to Friday, not after a holiday | d-1 | d-1 (the same trading day) | no |
| Monday | Friday | Friday | no |
| Saturday | Friday | Thursday | YES (one trading day earlier; the close read changes) |
| Sunday | Friday | Thursday | YES (the same) |
| a trading day right after a holiday (Tuesday after a Monday holiday) | the holiday's own date (no row) | the trading day before the holiday | YES in the PRINTED date; the price read is the same row (the reader ends on the last row at or before the date) |
| a holiday that falls on a weekday | the day before | the trading day before the previous trading day | YES (one trading day earlier) |
| the day before a holiday | d-1 | d-1 | no |

So a report run on a Saturday, a Sunday or a weekday holiday reads one trading day earlier under the calendar rule; a report run the day after a holiday prints a different date and reads the same close. Everything else is unchanged. The first priced report is window 5 (held).

## What this does not cover

- Reports delivered by a path that writes no `run.json` (none known: every Opal run files one, `runner.py:398-403`).
- A request received after 03:31Z.
- The pair itself is not cut; this is the count it needs. Recommendation: with a count of 0 and the first priced report still ahead, the change has no retrospective client effect; build it with the next release that touches `resident_installed.py`, and have the CTO rule whether Saturday and Sunday runs should print Thursday or Friday (the calendar frontier says Thursday).
