# FLAGGED_DAYS -- ADVI_COTBKF.TO-CB-bl-3 (round 64), 0.9.0_WK_ADVI_COTBKF~92, read 2026-10-11

Record: `FLAGGED_DAYS.json` (same folder). Read-only measurement; no account id, amount, quantity or per-account return is printed. Days are indexed 1..24 in date order.

FLAGGED-DAYS-RECORD emptied_measured_days=1757 flagged=24 above_100pct=3 classes=4 class_sum=24 unexplained=0

## Set
107,316 measured rows in 3,325 day files; 1,757 have no row in `account_day_value.parquet` for the account and day (all with value 0); 24 have an absolute return above 1%; 3 above 100%. Counts reproduced as pinned.

With value 0 the day return is outflow / prior value - 1 (`commonwealth_daily_returns.py:271`). On the other 1,733 days the ratio is 1.00 +- 0.01. Each flagged cell therefore says where outflow and prior value disagree.

## Classes
| class | flagged | above 100% | other emptied days with the row type | kind | what disagrees | code |
|---|---|---|---|---|---|---|
| A income credited on the emptied day | 8 (idx 3,4,5,6,7,8,20,21) | 3 (4,7,8) | 16 | TRUE | outflow exceeds prior value by the day's income; prior value was a residual (under $1 on 4 of 8) | `commonwealth_flows.py:59,69`; form `commonwealth_daily_returns.py:271` |
| B management fee takes the residual | 2 (1,9) | 0 | 0 | TRUE | outflow below prior value by the fee (fee is a drag, not a flow) | `commonwealth_flows.py:86,121` |
| C in-kind withdrawal valued at the day close | 12 (11-19,22-24) | 0 | 28 | TRUE | outflow at the day close vs prior value at the prior close: the shares' price move; rebuilt to 3 decimals on 12 of 12 | `commonwealth_daily_returns.py:150-152` |
| D withholding with no withdrawal row | 2 (2,10) | 0 | 0 | FORM | the ftax that took the whole balance is not counted as an outflow; counted as one the return is 0.00 | `commonwealth_flows.py:172,213`; `commonwealth_daily_returns.py:118` |

Unexplained: 0. Overlap of A and C among the other days: 10.

## Checks
- Prior day (24 of 24): previous trading day, value present, no unpriced position; own return measured on 23 (one inherits UNPRICED). Prior positions: 1 (cash only) on 11, 2-4 on 8, 5+ on 5.
- No position-transfer type within 2 days of any flagged day (0 of 24); a flow dated a day off appears on 2 and does not explain the ratio.
- The DVR_CLOSE_STEP blank is keyed to day-end holdings (`commonwealth_daily_valuation.py:633-634`), so an emptied day is never blanked by it; none of the 5 rows tested is a close-step day.

## Not established
See `not_established` in the record: no custodian day return was read; class A accrual timing is inferred; class C closes are the r34 price table's, not tested as-traded; class D cannot tell a missing withdrawal row from a full withholding; the "other days" counts are presence of a row type, not effect.
