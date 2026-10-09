# UNEXPLAINED_CLASSES_E2 -- the 1,203 UNEXPLAINED compounded misses, classed by cause (TO-DB-b-58, 0.9.0_WK_IRPT_DASHBD~36)

Counts only. Record: `UNEXPLAINED_CLASSES_E2.json`. Module: `unexplained_classes.py` (imports round 30's `tieout_compound.py`). S3 reads only; zero vendor calls. Tolerance 0.35 pp.

Population: 1203 compounded segments outside 0.35 pp with reason UNEXPLAINED; each carries one cause class (decision list, first match wins).

| cause class | segments |
|---|---|
| FEE_BASE_AVG_BALANCE | 618 |
| LARGE_FLOW_DAY | 170 |
| NEAR_ZERO_BALANCE | 153 |
| FLOW_TIMING_AFTER_FEE_BASE | 116 |
| VALUATION_BOUNDARY_MISMATCH | 47 |
| NO_SINGLE_CAUSE_RESIDUAL | 39 |
| FEE_ADDBACK_NOT_APPLICABLE | 38 |
| SEGMENT_FIRST_DAY | 20 |
| INCOME_TIMING | 2 |
| total | 1203 |

Top classes (smallest prefix reaching 80% = 962.4 of 1203): covered 1057 (87.9%).

| top class | disposition | segments |
|---|---|---|
| FEE_BASE_AVG_BALANCE | fixed | 618 |
| LARGE_FLOW_DAY | named_cause | 170 |
| NEAR_ZERO_BALANCE | named_cause | 153 |
| FLOW_TIMING_AFTER_FEE_BASE | named_cause | 116 |

Fix (FEE_BASE_AVG_BALANCE): fee add-back on the mean daily served value. Over all 9078 graded segments: within 0.35 pp 7459 -> 8088 (OUTSIDE to WITHIN 762, WITHIN to OUTSIDE 133). Of the 1203, 618 move to within.

