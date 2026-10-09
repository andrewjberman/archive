# LARGE_FLOW_E3 -- the 170 LARGE_FLOW_DAY misses traced to a sub-class (TO-DB-b-62, 0.9.0_WK_IRPT_DASHBD~39)

Counts only. Record: `LARGE_FLOW_E3.json`. Module: `large_flow_e3.py` (imports round 31's `unexplained_classes.py`). S3 reads only; zero vendor calls. Tolerance 0.35 pp.

Population: 170 LARGE_FLOW_DAY segments of round 31; each carries one sub-class (decision list, first match wins).

| sub-class | segments | disposition | within 0.35 pp under the class's rule |
|---|---|---|---|
| BD_FEE_FIELD_IS_FLOW | 26 | fixed | 23 of 26 on landed gain |
| FIRST_DAY_FLOW_AT_START | 4 | fixed | 4 of 4 on START |
| FLOW_DAY_RETURN_ZERO | 19 | named_cause | 19 of 19 on zero flow-day return |
| FLOW_START_OR_MID | 3 | named_cause | 2 of 3 on START or MID |
| FLOW_BOOKED_A_DAY_APART | 10 | named_cause | 10 of 10 on a one-day move |
| LIQUIDATION_RESIDUAL_BASE | 40 | named_cause | 0 of 40 on any re-link tested |
| FUNDED_FROM_NEAR_ZERO | 7 | named_cause | 0 of 7 on any re-link tested |
| ROUND_TRIP_FLOWS | 5 | named_cause | 0 of 5 on any re-link tested |
| MULTI_FLOW_COMPOUNDING | 18 | named_cause | 0 of 18 on any re-link tested |
| SINGLE_PARTIAL_FLOW | 38 | named_cause | 0 of 38 on any re-link tested |
| total | 170 | | |

