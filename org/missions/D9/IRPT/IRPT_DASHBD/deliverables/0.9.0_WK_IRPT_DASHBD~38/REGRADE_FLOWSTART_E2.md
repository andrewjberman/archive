# REGRADE_FLOWSTART_E2 -- counts only

Reader of record `tieout/tieout_reader.py` (sha256 in the record). Flow convention: start. Tolerance 0.35 pp. S3 reads only; zero vendor calls.

Graded 9078 of 9082 planned segments: within 8315, outside 763.

| outside reason | segments |
|---|---|
| UNEXPLAINED | 560 |
| FLOW_TIMING | 167 |
| INCOME_DATE | 31 |
| COVERAGE_DAYS | 4 |
| MISSING_PRICE | 1 |

Guard (denominator V_(t-1) + F_t below 2% of |V_(t-1)|; the day keeps its served return): 533 day(s) in 446 segment(s).

Within before (end-of-day, REGRADE_E1): 8088; within after (flow-start): 8315. Out to in: 430. In to out: 203.

| in-to-out reason class | segments |
|---|---|
| START_GUARD_DAY | 7 |
| START_LARGE_FLOW | 174 |
| START_SMALL_FLOW | 22 |
