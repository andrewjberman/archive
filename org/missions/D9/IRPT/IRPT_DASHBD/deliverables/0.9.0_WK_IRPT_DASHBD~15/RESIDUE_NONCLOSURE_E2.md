# RESIDUE_NONCLOSURE_E2 (IRPT_DASHBD.TO-DB-b-30) -- counts only

Set: GROSS UNEXPLAINED rows minus the +1-day-over-2025-01-09 rows = 980 non-closure segments. Denominator: 9,078 graded rows.
Zero vendor calls; BD bronze read only; the served Opal series was not read (fence).

| reason | segments |
|---|---|
| FLOW_TIMING | 226 |
| MISSING_PRICE | 0 |
| INCOME_DATE | 0 |
| COVERAGE_DAYS | 0 |
| UNEXPLAINED | 754 |
| total | 980 |

Final UNEXPLAINED: 754 of 9,078 graded (8.31 percent).

Evidence kinds used: FLOW_TIMING = BD Account-level point with flow share of the larger market value at least 0.25, and both Opal's
return and BD's gross return inside the Dietz envelope of that net flow placed at segment start vs end (+-0.35 pp); this shows the flow
day alone can carry the gap, an inferred (not measured) attribution. Tested and absent: day-count gaps (all 980 are 0), BD asset-level
positions held at zero value (MISSING_PRICE), asset-level partial days. INCOME_DATE could not be tested: BD gives income totals, not dates.
No reason outside the closed set was needed; no surprise row filed.
