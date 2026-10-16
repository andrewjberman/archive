# FWD-3 one-account exercise (CB-cw-1), worker 0.9.0_WK_ADVI_COTBKF~190

Record: `FWD3_EXERCISE_RECORD.json` (beside this file). Read script: `cw1_fwd3_exercise_read.py` (read-only, two `get_object` calls at the pinned VersionIds).

| Item | Count |
|---|---|
| Account (rule: most graded months; hash8) | `e4fe52f8` (82 graded months, no tie) |
| Span | 2016-02-02 to 2023-02-01 |
| Days | 1,763 (4 blank: 1 FIRST_DAY, 3 NON_POSITIVE_BASE) |
| Months | 85 |
| Strung equals served computed (order item 3(a), both-absent counted as equal) | 85 (83 present and equal, 2 both absent) |
| Matched reported monthly figure (within 0.05 points) | 82 |
| Differ | 0 |
| Ungradable | 3 (2016-02, 2023-01 blank day and reported span not one calendar month; 2023-02 no reported monthly figure) |
| Readable reported / benchmark (month, year, since-inception) | 82 / 84 / 85 ; 82 / 84 / 85 |
| Table population (months; match, diff, ungradable; days; blank days) | 82,593; 3,678, 288, 78,622 (+5 null verdict); 1,691,729; 1,584,413 |

The issuer's recompute (`cw1_fwd3_recompute.py`) agrees on every count except `strung_equals_served`, which it counts as 83 (present and equal only). That definitional difference is filed as channel row `ADVI_COTBKF-D1-W190-S1`; AC2 therefore reads `strung_equal=False` and the order is not flipped.
