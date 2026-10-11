# Bond accrual measure (ADVI_COTBKF.TO-CB-be-1, round 57)

Record: `BOND_ACCRUAL_MEASURE.json` beside this file. Read-only measurement; no code, config or S3 touched. No account id, size or amount appears here.

**Verdict: DIRTY. income_basis_for_bonds: FALSE (for a bond priced from the only store that prices bonds). No measured row holds a bond today, so no measured row is changed.**

## 1. Where the bond close comes from
- Value = quantity x the stored close of the (cusip, day): `commonwealth_daily_valuation.py:444`, price merged at `:440`. No par factor or accrued term; a bond close is read per unit (about 1.0 = par).
- Stores read, in order: `commonwealth_price_census.py:56-73`. Bonds are priced only by `gold-canonical-holdings` (`:61`, comment `:59` "the custodian mark on a held position"): 184 of 778 Fixed Income CUSIPs, 14,421 CUSIP-days, 2026-06-08 to 2026-10-06, every row source label `bd_snapshot`. The as-traded rebuild touches only store 1 (`commonwealth_daily_valuation.py:296`).
- No field name or documentation string states clean or dirty (columns: kind, key, day, price, source).

## 2. Counts (bond rule: silver transactions `Asset_Type == 'Fixed Income'`, `commonwealth_transactions.py:53`; 778 CUSIPs of 4,634, one type each)
| count | value | denominator |
|---|---|---|
| distinct bonds in measured rows | 0 | 252 distinct CUSIPs in 229,743 holding rows of the measured days |
| measured account-days with a bond | 0 | 107,316 measured account-days (return not null) |
| distinct bonds in the 988 held account-days | 16 | 16 Fixed Income CUSIPs held on those days; the hold list names 3, only 95000U2D4 has held days |
| held account-days with a bond | 988 | 988 (all hold 95000U2D4) |

All 141,555 account-days holding a Fixed Income CUSIP are blank (UNPRICED 141,379, FIRST_DAY 125, DVR_CLOSE_STEP 51). 95000U2D4 has no stored close on any of its 988 days (2022-06-08 to 2026-05-15; bond closes start 2026-06-08). Bond funds (24 of 252 CUSIPs carry a bond word) are funds and are not counted.

## 3. Saw-tooth test
- Tested 86 of 184 priced bonds: coupon rate and maturity month/day parsed from the description, so a semiannual coupon date falls inside the price window. Untested: 42 have no coupon date in the window, 53 have a truncated description, 3 are zero coupon.
- **Fall half shown: 81 of 86** fall 0.6 to 1.4 half-coupons within 4 days of the date (median 1.00, interquartile 0.96 to 1.05). Example 66285WM78 (coupon 5.0): 103.703 on 2026-06-30, 101.293 on 2026-07-08 per 100.
- Negative arm: 5 of 42 bonds with no coupon date in the window show a fall that large (12 percent against 94 percent).
- **Climb half not resolved.** Slope against coupon over 112 bonds: 0.00046 (se 0.00202) per coupon point per day against 0.00274 predicted; rate moves over 120 days swamp it. 5 of 86 do not fall, unexplained.

## 4. Why DIRTY, and its limit
A clean price has no coupon-sized step on a coupon date; this store's price has one in 81 of 86. The coupon therefore sits in the price before the pay date, and the pay-date cash posts against an equal price fall, so income does not enter value at the cash posting (row 3 `cash_when_received` is not true for these bonds). Limits: no accrual climb measured; no coupon cash date or trade falls inside the 2026-06-08 onward window to compare (cash `int` rows end 2026-06-01; 7,071 rows on 705 bond CUSIPs); no vendor documentation. A settling read, if wanted: the gold store's market_value against units x price, and the custodian statement's accrued-interest field, for one bond across one coupon date (an S3 read, outside this order).

Analysis scripts: `.scratch/w84/` in the worktree (gitignored, not committed). Row filed: ADVI_COTBKF-D2-W84-S1.
