# Commonwealth monthly grade

Tolerance: 0.05 percentage points (MATCH when abs(diff) <= tolerance). Unpriced or blank is never filled.

MONTHLY-GRADE months=3 match=1 diff=1 ungradable=1 tolerance_pct=0.05 stub=True

| account | month | computed_pct | reported_pct | diff_pct | grade | reason |
|---|---|---|---|---|---|---|
| STUB-1 | 2026-01 | 2.002374 | 2.0 | 0.002374 | MATCH |  |
| STUB-1 | 2026-02 | 2.01 | 1.81 | 0.2 | DIFF | computed 2.0100 vs reported 1.81: diff 0.2000 pct points exceeds 0.05 |
| STUB-1 | 2026-03 |  | 3.03 |  | UNGRADABLE | 1 blank day(s) of 3; first blank reason: unpriced holding on the day |
