# Outliers on a real base (round 68, TO-CB-bp-5) -- 179 measured days above 10 percent on a prior value of 100.00 or more

Worker 0.9.0_WK_ADVI_COTBKF~105. A measurement; no code changed. The record is `OUTLIERS_ON_A_REAL_BASE.json` (days named by an index; no account id, amount, quantity or per-account return).

**Set.** Rebuilt from the served `daily_returns.parquet`: 179 days, 57 above 1.00 and 122 from 0.10 to 1.00 (round 65's table: 179 / 57 / 122). 77 days read row by row (transactions and holdings side by side), 102 placed by rule; unclassed 0.

| # | Class (cause) | Days | above 1.00 | 0.10-1.00 | Kind | Hand-checked |
|---|---|---|---|---|---|---|
| 1 | Income paid after the holdings left | 119 | 35 | 84 | FORM | 45 |
| 2 | Fee refund (Fee Rebate / Reversal) credited after the assets left | 43 | 21 | 22 | FORM | 15 |
| 3 | Real price move on a full base | 10 | 0 | 10 | TRUE_RETURN | 10 |
| 4 | Tax withholding takes the whole balance (no lo) | 2 | 0 | 2 | FORM | 2 |
| 5 | Management fee debit on a cash-only account | 1 | 0 | 1 | TRUE_RETURN | 1 |
| 6 | Fee owed elsewhere (ManAltT) taken as a drag on cash | 1 | 0 | 1 | FORM | 1 |
| 7 | Custodian 12b1 credit on a residual base | 1 | 0 | 1 | FORM | 1 |
| 8 | Sale at the traded price against a split-adjusted close (CHPT) | 1 | 0 | 1 | PRICE | 1 |
| 9 | In-kind contribution valued on a mis-scaled close (CTVA) | 1 | 1 | 0 | PRICE | 1 |

**What the base is.** Of the 162 days in classes 1 and 2 the prior-day base is cash only on 154 and one holding on 8. It is 100.00 or more in dollars (100-1,000 on 122, 1,000-10,000 on 38) but it is a median 0.1 percent of the money that left the account in the prior 30 rows (152 of 162 have an outflow of 100 times or more; 161 of 10 times or more), left by a full withdrawal or in-kind transfer out; a later withdrawal of at least the base follows within 10 rows on 130 and the account's rows end within 10 rows on 111.

**Why it is not a flow.** Income (class 1): per-share amounts equal the peers' rate within 1 percent on 71 of 99 equity-type rows, and sit at 0.30 to 0.95 of it on 93 of 114 mutual-fund rows (daily accrual for part of the month), so it is earned on the account's own earlier holdings. Fee refund (class 2): on 41 of 42 days the rebate equals the quarter fraction its note's period covers of the account's last man debit; the form took that debit as a drag of 0.05 percent of the then value and takes the refund on the residual.

**Round 65.** Its record has counts only; by count its 100-or-more days (A2 35, E 21, G 1) are my class 1 (35), class 2 (21) and class 9 (1). The one FORM day (index 48, 2026-02-18): I agree with the day and the mechanism; I class it PRICE, not FORM, because the store's CTVA closes are 6.58 / 6.59 / 6.64 / 6.63 times below the traded price on all four priced trades 2020-2026. `agrees_with_round_65_form_day` is false for the kind only.

**Not established** (full list in the record): record and ex-dates were not read; the destination of the exited accounts; the right treatment of classes 1, 2 and 7 (policy; no rule was run); method_r29 was not run on class 4; the 2026 price days were checked against the price store only; whether other securities carry the CTVA scale defect; round 65's days matched by count, not by day.

Observation for the threshold, not a ruling: a prior value of 100.00 does not separate the classes; the account's own prior outflow does (all 152 days with an outflow of 100 times the base or more are in classes 1 and 2; none of the 17 other days has one).
