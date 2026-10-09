## Worked account-month: acct#e29efebe, 2025-09 (CB-q-1)

One account-month that contains a valued zero-Amount transfer and is fully priced. The row: Trade_Date 2025-09-24, type `lo`
(Withdrawal from Asset, direction -1), Amount 0, CUSIP 594918104, Quantity 21. That day's close for the CUSIP in
`security_day_price.parquet` is 508.037384 (store cottonwood-silver-canonical-prices), so the flow is
-1 x 21 x 508.037384 = -10668.785065.

Before (no price used, the Amount-0 row blanks its day): 2025-09-24 has `ret` null, reason FLOW_UNVALUED, so the month has 1
blank day of 21 and the monthly grade is UNGRADABLE (reported 0.84).

After: 2025-09-24 value 1188.40, flow -10668.785065, ret 0.001625 (computed from 11837.946173 the day before); the month has
no blank day, strings to 0.7664 percent against Commonwealth's reported 0.84, diff -0.0736 percentage points, which exceeds
the 0.05 tolerance, so the grade is DIFF. The transfer is now valued; the month does not match Commonwealth.

Grades written by `commonwealth_monthly_grade.py`: `grade_acct#e29efebe_2025-09_before/monthly_grade.csv` and
`grade_acct#e29efebe_2025-09_after/monthly_grade.csv` beside this report.

Across the whole run, 6 months moved from UNGRADABLE to graded on this change (ungradable 78,362 -> 78,356), all six DIFF
(DIFF 2,284 -> 2,290; MATCH 1,947 unchanged); all six carry `lo` or `li` rows, none a `trf*` row.
