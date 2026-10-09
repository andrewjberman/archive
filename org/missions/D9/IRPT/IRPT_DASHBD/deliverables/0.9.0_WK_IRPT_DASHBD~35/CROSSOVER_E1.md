# CROSSOVER_E1 -- the 181 segments that tied under the additive fee basis and miss under the compounded one (TO-DB-b-57, 0.9.0_WK_IRPT_DASHBD~35)

Counts only. Record: `CROSSOVER_E1.json`. Reader: `crossover_e1.py`; fix: `tieout_compound_v2.py`. S3 reads only; zero vendor calls.

Population: segments WITHIN in round 18 (additive) and OUTSIDE in round 30 (compounded): 181.

| cause class | segments | compounding defect |
|---|---|---|
| FEE_BASE_BALANCE_PATH | 134 | yes |
| FLOW_TIMING_RESIDUE | 23 | no |
| ADDITIVE_TIE_COINCIDENCE | 22 | no |
| NEGATIVE_FEE_ADDBACK | 2 | no |
| total | 181 | |

Defect judgment: FEE_BASE_BALANCE_PATH. The compounding formula is sound; its fee base, (bmv + emv) / 2, is not the average balance when the
balance moves through the segment. The other classes are an exposed additive coincidence, a negative-fee total, or flow-convention residue.

Fix: `tieout_compound_v2.py` forms the add-back on the mean served daily value of the linked days. Full re-grade of 9078 segments:

| | within 0.35 pp | outside |
|---|---|---|
| round 30 (two-point base) | 7,459 | 1,619 |
| v2 (daily-mean base) | 8088 | 990 |

Per-segment moves vs round 30: unchanged 8183, OUTSIDE_to_WITHIN 762, WITHIN_to_OUTSIDE 133.
Of the 181, 134 are WITHIN again under v2.
