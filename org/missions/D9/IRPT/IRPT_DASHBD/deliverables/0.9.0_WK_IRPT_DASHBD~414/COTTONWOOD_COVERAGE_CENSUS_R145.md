# Cottonwood coverage census, R145 (DB-c-22)

Read only, UTC reads 2026-10-15T23:29Z to 23:30Z, by census_r145_read.py. Counts, dates and words only.

1. Where each table starts. The four gold tables do not share one start.
- filled_report_values: 65 partitions, 2026-07-10 to 2026-10-14. Tell the person the filled series starts 2026-07-10.
- account_return_daily: 3390 partitions, 2013-04-03 to 2026-10-14. Returns exist back to 2013; the person must be told about the absent days in section 3.
- holdings_performance_daily: 88 partitions, 2026-06-10 to 2026-10-14.
- account_dim: 2 partitions, 2026-10-13 and 2026-10-14.

2. The floor, 2026-07-10 (filled_report_values). Its first partition is 2026-07-10. The silver evidence is a candidate, not an established cause. Black Diamond fact_allocations has 145 partitions from 2026-04-22. 33 read 0 rows by footer: 22 on non-trading days, 11 on trading days between 2026-06-22 and 2026-07-09. 2026-07-10 is the first partition after the last empty one and has rows. Silver also has rows on 2026-04-22 to 2026-04-24 and on 38 trading days inside 2026-04-25 to 2026-07-09. The rule that starts the gold series was not read (NOT_ESTABLISHED).

3. Days that could not be measured (trading days, from lib/trading_calendar.py).
- filled_report_values: 3 absent days in 2 runs: 2026-08-19 (1 day) and 2026-09-24 to 2026-09-25 (2 days). Tell the person a figure on those days was not measured.
- account_return_daily: 15 absent days in 3 runs: 2026-06-23 to 2026-07-09 (12 days), 2026-08-19 (1 day), 2026-09-24 to 2026-09-25 (2 days).
- holdings_performance_daily and account_dim: no absent trading days inside their spans.

4. The twelve-day gap is found. account_return_daily has no partition for the 12 trading days 2026-06-23 to 2026-07-09, directly before the filled floor. holdings_performance_daily has partitions on those days.

5. Account histories, counts only (account_id compared as str(value).strip()).
- 1004 accounts in the newest account_dim partition (2026-10-14).
- 835 accounts with holdings rows on the floor day (2026-07-10).
- 166 accounts in the newest holdings partition (2026-10-14) with no row on the floor day. Their history starts after the floor: a partial history. Tell the person that before showing these accounts' figures.

6. Coverage state. account_return_daily.day_quality, newest partition 2026-10-14, 864 rows: MEASURED 827, NOT_MEASURABLE 37. A NOT_MEASURABLE day must be shown as not measured. filled_report_values.absent_kind, newest partition, 287600 rows: null 256965, INSUFFICIENT_HISTORY 10665, NO_SOURCE_YET 16722, SOURCE_BREAK 3248. Neither column's values name a fallback.

7. How current. The newest partition is 2026-10-14 in filled_report_values, account_return_daily and holdings_performance_daily, and account_dim's newest is 2026-10-14 as well.

8. Reads: 153 S3 list calls, 150 get calls, 0 head, 0 writes, 0 invokes. Not established: the start rule for the gold series, the cause of each absent day, and any fallback signal (other columns, not read).
