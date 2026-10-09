# NEAR_ZERO_SHIMFREE_E1 -- the 153 NEAR_ZERO_BALANCE rows re-run with no shim (TO-DB-b-66, 0.9.0_WK_IRPT_DASHBD~43)

Counts only. Record: `NEAR_ZERO_SHIMFREE_E1.json`. Module: `near_zero_e3.py --out-dir`. S3 reads only; zero vendor calls. Tolerance 0.35 pp.

shim_applied: false. The near-zero classifier uses the reader of record's own mean; round 32's classify binds the reader's `daily_mean_value` itself.

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

Fixed classes within 0.35 pp under the reader's mean: 79 of 79 (round 33: 79).
Tie-out: 9078 segments graded by the reader; within 0.35 pp with the shim-free near-zero result: 8433 (round 33: 8385); the reader alone: 8385, of which 31 are among the 153.
Sub-classes and rows identical to the round 33 record: True. Control (round 32's counts reproduced): True.

