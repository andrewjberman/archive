# NEAR_ZERO_E3 -- the 153 NEAR_ZERO_BALANCE misses traced to a sub-class (TO-DB-b-65, 0.9.0_WK_IRPT_DASHBD~42)

Counts only. Record: `NEAR_ZERO_E3.json`. Module: `near_zero_e3.py` (imports round 32's `large_flow_e3.py` and the reader of record). S3 reads only; zero vendor calls. Tolerance 0.35 pp.

Population: 153 NEAR_ZERO_BALANCE segments of round 31; each carries one sub-class (decision list, first match wins).

| sub-class | segments | disposition |
|---|---|---|
| BD_FEE_FIELD_IS_FLOW | 31 | fixed |
| GAIN_AGREES_NEAR_ZERO_BASE | 48 | fixed |
| NEGATIVE_BALANCE | 1 | named_cause |
| BD_TWR_SATURATED | 12 | named_cause |
| NEAR_ZERO_DIVISOR_DAY | 14 | named_cause |
| BD_END_NEAR_ZERO | 30 | named_cause |
| BD_BEGIN_NEAR_ZERO | 9 | named_cause |
| BD_BOTH_ENDS_NEAR_ZERO | 2 | named_cause |
| INTERIOR_NEAR_ZERO_RUN | 6 | named_cause |
| total | 153 | |

Fix (`landed_gain_return`, BD's landed money gain over the mean daily served value): 79 of 153 rows move to within 0.35 pp (BD_FEE_FIELD_IS_FLOW 31 of 31, GAIN_AGREES_NEAR_ZERO_BASE 48 of 48). BD's TWR is not changed; nothing served moves.

Overlap with round 32: 0 of 153 in the flow-start in-to-out list (203); 0 of the 170 LARGE_FLOW_DAY rows; all 153 of the 153 graded in the flow-start record are OUTSIDE there too.
Round 32's own classifier, run on these 153: LIQUIDATION_RESIDUAL_BASE 98, BD_FEE_FIELD_IS_FLOW 31, FUNDED_FROM_NEAR_ZERO 23, FLOW_BOOKED_A_DAY_APART 1 (control on its 170 rows reproduces its recorded counts: True).
Rows with a flow-start guard day: 98 of 153.

