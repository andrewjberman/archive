# OUTLIER_DAYS -- ADVI_COTBKF.TO-CB-bm-1 (round 65), 0.9.0_WK_ADVI_COTBKF~94, read 2026-10-11

Record: `OUTLIER_DAYS.json` (same folder). Read-only measurement; no account id, amount, quantity or per-account return is printed. Days are indexed 1..207 in date order.

OUTLIER-DAYS-RECORD measured_rows_positive_prior=107311 outliers=207 prior_under_1=55 prior_1_or_more=152 classes=5 class_sum=207 unexplained=0 threshold_rows=6

## Set
107,311 measured rows with a positive prior value; 207 with an absolute return above 1 (55 on a prior value under 1.00, 95 from 1.00 to under 100.00, 57 of 100.00 or more), on 170 accounts. Counts reproduced as pinned.

## Classes
| class | days | <1 | 1 to <100 | 100+ | kind | what carries the return |
|---|---|---|---|---|---|---|
| A income credited on the emptied day (round 64 name) | 3 | 3 | 0 | 0 | RESIDUAL_BASE | dividend on the leftover, leftover and income withdrawn, value 0 (`commonwealth_flows.py:59`; `commonwealth_daily_returns.py:271`) |
| A2 income credited to a leftover balance | 105 | 25 | 45 | 35 | RESIDUAL_BASE | same credit, account not emptied that day; a close-out left the base (`flows:59,62,69`) |
| E fee rebate credited to a leftover balance | 97 | 26 | 50 | 21 | RESIDUAL_BASE | `man` row with positive Amount, a drag so it raises the return (`flows:86,121`; `signs:75`); 89 of 97 on two dates |
| F fee owed elsewhere charged to a leftover balance | 1 | 1 | 0 | 0 | RESIDUAL_BASE | ManAltT taken at its Amount in the numerator (`flows:122,127`; `returns:136,271`) |
| G in-kind contribution valued from a close the sale contradicts | 1 | 0 | 0 | 1 | FORM | li valued at the price-store close, next-day sale 6.72 times it (`returns:150-152`) |

Unexplained: 0. The return of 205 of 207 is reproduced from the day's income, man and tax rows divided by the prior value (E2).

## Threshold table (all 107,311 measured rows; abs return strictly above the level)
| above | prior <1 | 1 to <100 | 100+ |
|---|---|---|---|
| 0.10 | 64 | 130 | 179 |
| 0.25 | 62 | 115 | 130 |
| 0.50 | 60 | 103 | 88 |
| 1.00 | 55 | 95 | 57 |
| 2.00 | 50 | 73 | 30 |
| 10.00 | 48 | 42 | 3 |

Band totals: 5,437 under 1.00, 6,471 from 1.00 to under 100.00, 95,403 of 100.00 or more.

## Checks
- Hand-checked: A 3 of 3, A2 17 of 105, E 9 of 97, F 1 of 1, G 1 of 1 (31 of 207).
- 147 of 207 are dated 2026-05-20 to 2026-06-10; five dates hold 144.
- Prior day cash only on 168 of 207; prior-20-row outflows 10 or more times the prior value on 201 of 207.

## Not established
See `not_established` in the record: no custodian return read; the 100.00-and-over leftovers are the CTO's threshold; why a rebate is credited to closed-out accounts; the record-date versus dating reading of A2; class F rests on one day; the cause of the class G close.
