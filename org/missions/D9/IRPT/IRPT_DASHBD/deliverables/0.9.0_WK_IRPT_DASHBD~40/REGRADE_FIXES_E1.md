# REGRADE_FIXES_E1 -- counts only

Reader of record `tieout/tieout_reader.py` (sha256 in the record). Flow convention: start. Tolerance 0.35 pp. S3 reads only; zero vendor calls.

Graded 9078 of 9082 planned segments: within 8385, outside 693.

| outside reason | segments |
|---|---|
| UNEXPLAINED | 481 |
| FLOW_TIMING | 178 |
| INCOME_DATE | 29 |
| COVERAGE_DAYS | 4 |
| MISSING_PRICE | 1 |

Guard (denominator V_(t-1) + F_t below 2% of |V_(t-1)|; the day keeps its served return): 533 day(s) in 446 segment(s).

Rules fired (segments): BD_FEE_FIELD_IS_FLOW 85; FIRST_DAY_FLOW_AT_START 144.

Within before (the prior record): 8315; within after: 8385. Out to in: 84. In to out: 14.

| in-to-out reason class | segments |
|---|---|
| FIRST_DAY_START_NOT_BD | 14 |
