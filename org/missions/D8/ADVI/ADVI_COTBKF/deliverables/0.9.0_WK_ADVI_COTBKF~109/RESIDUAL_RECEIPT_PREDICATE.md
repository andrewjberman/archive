# A receipt after an account's assets have left -- the exact predicate, tested (round 69, TO-CB-bq-4)

Worker 0.9.0_WK_ADVI_COTBKF~109. A measurement; no code changed. The record is `RESIDUAL_RECEIPT_PREDICATE.json`. No account id, amount, quantity or per-account return appears in either file. The setting below is a RECOMMENDATION of the measuring worker, not a ruling.

## The predicate (apply it by hand)

Take one account and one day. The day reads **blank with reason `RECEIPT_AFTER_EXIT`** when all three hold.

**(a) The account had a full outflow in the last 28 calendar days.**
1. B = the account's value at the close of its previous row (the prior value the return divides by). If B is not positive, stop: the predicate does not apply.
2. For each calendar day from 28 days before today up to yesterday, take that day's net external outflow: withdrawals (`lo`), in-kind transfers out (`trfo`, `trco`), `LIX`, short contributions (`si`), and the charge flows and riding tax withholdings the form counts as flows, each valued as the form values them (a zero-Amount row at the close). A day with a deposit and a withdrawal counts only what is left of the withdrawal after the deposit. A day with a net inflow counts 0. Today is not counted.
3. O = the sum of those days. The account had a full outflow when **O / (O + B) is at least 0.99** (the same as: O is at least 99 times B).

**(b) The day is a receipt day.**
1. At least one row today is a receipt:
   - income: `dv`, `dvlt`, `dvst`, `int`, `roy`, `ileu`, `dvr`, `ac`, or the cancels `DVX`, `INTX`, `DVRX` (`commonwealth_flows.py` lines 59-70, all internal, kept inside the return);
   - a fee refund: `man` with a positive Amount (lines 86, 121);
   - a 12b1 credit: `12b1` (line 85). It belongs: it is a fee credit of the refund's shape. It changes 2 of the 410 blanked days.
2. Every other row today is one of: a sweep buy or sweep sell of a listed sweep (the same money, internal by `commonwealth_flows.internal_sweep_trade`); a `lo` of the cash balance (the withdrawal of the receipt: a receipt plus a sweep-out of the account is still a receipt on a residual); `frntax` (foreign tax out of the same income).
3. Any other row makes the day not a receipt day: a buy or sell of a security (`by`, `sl`, `cs`, `ss`, `BYX`, `pyd`, `leu`); a deposit or transfer in (`li`, `LISU`, `trfi`, `TRFIR`, `trci`, `TRCISU`, `LOX`, `so`, `ci`); a withdrawal or transfer of a security (`lo` of a security, `trfo`, `trco`); a corporate action (`lica`, `licar`, `LICASU`, `loca`, `QA`, `CAF`, `CAE`, `acca`, `accal`); a fee debit or tax (negative `man`, `ManAltT`, `misc`, `fch`, `ftax`, and the other charges). A day with a real contribution is a contribution day, not a receipt day.

**(c) Reads as:** blank, reason `RECEIPT_AFTER_EXIT` (the style of `UNPRICED`, `INKIND_UNDERSTATED`, `DVR_CLOSE_STEP`). Where another blank reason already applies, that reason stands.

**No number in it is a dollar amount, a prior-value threshold or a return threshold.**

**Worked example (invented ratios, not an account).** Over the last 28 calendar days an account shows one cash withdrawal of 400 times its value at yesterday's close (B = 1). O / (O + B) = 400 / 401 = 0.998, at least 0.99. Today's rows are one dividend and one sweep buy. Both are allowed. The day is blank, `RECEIPT_AFTER_EXIT`. Had today also carried a sale of a stock, or had the withdrawal been 50 times B (50 / 51 = 0.98), the day would be computed as before.

## The constants and where they come from

| Constant | Value | Source in the data |
|---|---|---|
| Look-back | 28 calendar days | Target days blanked (of 162) at share 0.99: 128 at 14 days, 145 at 21, 147 at 22 and 23, 148 at 24, and the same 148 at every look-back from 24 to 180 days; the total blanked on all measured rows keeps rising (399 at 24, 410 at 28, 414 at 30, 431 at 60, 474 at 180). 28 is the smallest whole number of weeks on the plateau. 20 of the account's own rows gives 148 / 413. |
| Share left | 0.99 | Marginal yield of each step down (look-back 28): 0.999 to 0.995 adds 59 target days and 123 blanked days (48 percent targets); 0.995 to 0.99 adds 12 / 23 (52 percent); 0.99 to 0.95 adds 6 / 46 (13 percent); 0.95 to 0.90 adds 3 / 19 (16 percent); 0.90 to 0.80 adds 0 / 30. Below 0.99 the added days are mostly not targets. It is the same as an outflow of 99 times the base, and the round-68 worker's 100-times observation. |

Why the share is against `O + B` and not against the pre-outflow value: the value before the first outflow is blank in the table (`UNPRICED`) on 152 of the 157 receipt-only target days that have an outflow in the window, known on 5. A share of the pre-outflow value cannot be computed there; `O` and `B` always can.

Formulations compared (targets of 162 / total of 107,311): F1 share against `O + B` in calendar days 148 / 410 (chosen); the same in 20 own rows 148 / 413; F2 outflow at least K times the base in 30 rows, K = 10 / 100 / 1000: 157 / 148 / 79 and 499 / 423 / 275 (the same family as F1); F3 share of pre-outflow value: not computable on 152 of 157; F4 value fell to at most 0.01 / 0.05 / 0.10 of its 28-day peak: 7 / 10 / 14 targets (the peak is blank for the same reason); F0 any outflow at all: 157 targets but 1,320 blanked.

## On the 179 days (recommended setting)

| Cause (round 68) | Days | Blanked | Left |
|---|---|---|---|
| Income paid after the holdings left | 119 | 113 | 6 |
| Fee refund credited after the assets left | 43 | 35 | 8 |
| Real price move on a full base | 10 | 0 | 10 |
| Tax withholding takes the whole balance | 2 | 0 | 2 |
| Management fee debit on a cash-only account | 1 | 0 | 1 |
| Fee owed elsewhere taken as a drag on cash | 1 | 0 | 1 |
| Custodian 12b1 credit on a residual base | 1 | 0 | 1 |
| Sale against a split-adjusted close | 1 | 0 | 1 |
| In-kind contribution on a mis-scaled close | 1 | 0 | 1 |
| **All** | **179** | **148** | **31** |

**Targets blanked: 148 of 162. Other days blanked: 0 of 17.** The 10 real price-move days and the 2 withholding days are not blanked; nothing outside the two target causes is blanked.

**What it misses (14 target days).** 4 carry other activity beside the receipt: a sale of a security (a fee-refund day), a `misc` charge, a cash deposit, a cash transfer in and out. 9 have a share left below 0.99: 0.92, 0.93, 0.94, 0.97 (twice), 0.98 (twice), 0.988 and 0.989, a remainder of 1 to 8 percent of what was in the account; 1 (a fee refund) has no outflow in the 28 days before (it has one at 365 days, share 1.00). Lowering the share to 0.95 gains 6 of them, to 0.90 gains 9 (and 46 and 65 more blanked days; see the sensitivity).

**Which other days pass the receipt test but not the outflow test.** The receipt test alone selects 5,602 measured days (158 targets and 2 of the other 17: the one real price-move day that carries a `dvr`, and the 12b1 day). The outflow test removes 5,192 of them, including both of those two.

## On all 107,311 measured rows with a positive prior value

Blanked by the recommended predicate: **410** (0.38 percent). Rows (measured / blanked):

| abs(return) \ prior value | under 1.00 | 1.00 to under 100.00 | 100.00 or more | all |
|---|---|---|---|---|
| at or below 0.10 | 5,373 / 14 | 6,341 / 25 | 95,224 / 61 | 106,938 / 100 |
| 0.10 to 1.00 | 9 / 3 | 35 / 28 | 122 / 96 | 166 / 127 |
| above 1.00 | 55 / 50 | 95 / 81 | 57 / 52 | 207 / 183 |
| all | 5,437 / 67 | 6,471 / 134 | 95,403 / 209 | 107,311 / 410 |

5 other measured rows have a missing prior value in this table (none non-positive); the predicate is not applied and blanks none (2 of them carry a receipt row).

**The quiet days.** 100 blanked days have abs(return) at or below 0.10. The policy has no return threshold, so it blanks them. They are the same phenomenon in kind: 98 of 100 sit on a cash-only base and 2 on one holding (none on two or more), 99 carry income and 1 a fee refund, every one has an outflow of 99 times the base or more in the 28 days before. They differ in that only 36 of 100 are followed by a withdrawal of the base within 10 rows (targets: 106 of 148) and 42 of 100 end within 10 rows (targets: 105 of 148): more of them are residuals on accounts that stay open. Sample of 20 of those 100 (seed 109; in the JSON, by month and type only): all 20 carry a receipt row (income types 19, one fee refund), all 20 on a cash-only base, 15 followed by a withdrawal of at least the base within 10 rows or by the account's rows ending within 10 rows (12 and 6), 10 on a prior value of 100.00 or more, 8 from 1.00 to under 100.00 and 2 under 1.00. Same phenomenon in kind, on a smaller receipt against the stub. Whether a 0.3 percent day of late interest on a stub that stays open should be blank is the CTO's.

All 262 blanked days outside the 179 are of the same kind (cash-only 226, one holding 36, none on two or more; 186 income, 74 fee refund, 2 carry a 12b1 credit); 162 of them have abs(return) above 0.10 and a prior value under 100.00, so they lie outside the 179 set by its definition.

By year the 410 are: 2013-2025 124, 2026 286 (141 in May, 133 in June).

## Sensitivity (look-back 28 days and share 0.99 unless moved; targets of 162 / other 17 of the 179 / total of 107,311 / total at or below 0.10)

Look-back: 14 days 128 / 0 / 336 / 69; 21 days 145 / 0 / 384 / 84; 24 days 148 / 0 / 399 / 92; **28 days 148 / 0 / 410 / 100**; 30 days 148 / 0 / 414 / 102; 45 days 148 / 0 / 424 / 110; 60 days 148 / 0 / 431 / 116; 90 days 148 / 1 / 445 / 129; 180 days 148 / 1 / 474 / 157. In rows: 10 rows 128 / 0 / 337; 20 rows 148 / 0 / 413; 30 rows 148 / 0 / 423; 60 rows 148 / 1 / 444; 120 rows 148 / 1 / 473. (The one other day at 90 days or more is the 12b1 residual day: an outflow exists that long before.)

Share left: 0.5 157 / 0 / 574 / 250; 0.8 157 / 0 / 505 / 182; 0.9 157 / 0 / 475 / 153; 0.95 154 / 0 / 456 / 138; **0.99 148 / 0 / 410 / 100**; 0.995 136 / 0 / 387 / 92; 0.999 77 / 0 / 264 / 48.

Receipt set: recommended 148 / 0 / 410; income only 113 / 0 / 299 (loses all fee refunds, 35); without 12b1 148 / 0 / 408; no row but the receipt (no sweep leg, no cash withdrawal) 17 / 0 / 83; also allowing cash deposits, cash transfers, fee debits and tax rows beside the receipt 151 / 0 / 457; any other activity allowed 152 / 0 / 462.

The full tables, with the split by abs(return) band and by prior-value band for every row, are in `sensitivity` in the JSON.

## Recommendation (marked: a recommendation, not a ruling)

Look-back **28 calendar days**, share left **0.99**, the receipt set above (12b1 in), reason `RECEIPT_AFTER_EXIT`. Why: the look-back is the smallest whole number of weeks on the plateau of target days; below 0.99 the added days are mostly not targets and above it targets are lost fast; none of the 17 other days among the 179 is blanked; every blanked day has a measured full outflow behind it. Its cost: 14 target days left and 100 quiet days blanked.

## What it does to months

Under the recommended setting **299 account-months of 6,922 (those with a measured day) lose at least one measured day**; in 10 of them every measured day is lost. 241 of the 1,054 accounts with a measured day are touched.

## Not established

See `not_established` in the JSON (10 lines). The main ones: the pre-outflow value is blank in the table, so the share is against outflow plus base; the 28-day window reads the served flow column, not transactions re-valued; deposits and withdrawals on one day are netted; the quiet blanked days are told from targets by description only; the predicate was not tested out of sample (286 of 410 blanked days are May-June 2026); the code, the reason code's precedence and the flow timing it assumes are not touched.
