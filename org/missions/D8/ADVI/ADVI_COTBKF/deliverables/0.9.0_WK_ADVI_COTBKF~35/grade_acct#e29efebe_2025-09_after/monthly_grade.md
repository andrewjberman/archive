# Commonwealth monthly grade

Tolerance: 0.05 percentage points (MATCH when abs(diff) <= tolerance). Unpriced or blank is never filled.

MONTHLY-GRADE months=1 match=0 diff=1 ungradable=0 tolerance_pct=0.05

| account | month | computed_pct | reported_pct | diff_pct | grade | reason |
|---|---|---|---|---|---|---|
| acct#e29efebe | 2025-09 | 0.76642 | 0.84 | -0.07358 | DIFF | computed 0.7664 vs reported 0.84: diff -0.0736 pct points exceeds 0.05 |
