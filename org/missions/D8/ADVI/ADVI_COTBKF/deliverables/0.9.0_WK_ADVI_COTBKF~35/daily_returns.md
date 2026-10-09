# Daily returns per account (CB-p-2)

ret = (value_t - flow_t) / value_(t-1) - 1, flows at end of day, after fees (a fee is not a flow). A transaction on a non-trading day counts on the next trading day. A day that cannot be worked out is null with its reason; nothing is filled.

- account_days: 1691729 over 1533 account(s)
- computed: 127396
- blank: 1564333
- days carrying an external flow: 40319
- flow rows landing on no value day (outside the account's value span): 0
- zero-Amount external-flow rows: 20403, valued as abs(Quantity) x that day's price: 5017, blank for no price: 15386
- written: C:\dev\wk-cotbkf-35\.scratch\advi_cotbkf\fwd3\daily_returns.parquet

## Blank reasons

- FIRST_DAY: 1533
- UNPRICED: 1560217
- ZERO_BASE: 2578
- FLOW_UNVALUED: 5
- FLOW_UNDECIDED: 0

## Flow table (61 of 61 types decided)

EXTERNAL (15): LISU, LIX, LOX, TRCISU, TRFIR, ftax, li, lo, si, so, stax, trci, trco, trfi, trfo
INTERNAL (46): everything else, including every fee.

| type | decision | direction | reason |
|---|---|---|---|
| 12b1 | INTERNAL | | 12(b)-1 Expense: a fund fee credit booked on the cash sweep; a fee, not a flow |
| ASF | INTERNAL | | ASF fee: a fee |
| BYX | INTERNAL | | Cancel Buy: reverses a trade inside the account |
| CAE | INTERNAL | | Capital Adjustment Estimation: corporate action share adjustment inside the account |
| CAF | INTERNAL | | Capital Adjustment Final: corporate action share adjustment inside the account |
| DVRX | INTERNAL | | Cancel Reinvestment: reverses dvr inside the account |
| DVX | INTERNAL | | Cancel Dividend Received: reverses income inside the account |
| INTX | INTERNAL | | Cancel Interest Income: reverses income inside the account |
| LICASU | INTERNAL | | Corporate Action Contribution: shares received in a corporate action exchange |
| LISU | EXTERNAL | +1 | Contribution to Asset (same description as li): the client puts securities into the account |
| LIX | EXTERNAL | -1 | Cancel Contribution to Asset: reverses li, so the contributed value leaves again |
| LOX | EXTERNAL | +1 | Cancel Withdrawal from Asset: reverses lo, so the withdrawn value returns |
| ManAltF | INTERNAL | | Withdraw ManAlt Fee payment: a fee payment (judgment: if it pays another account's fee it is a transfer to that account; the order says every fee is internal) |
| ManAltT | INTERNAL | | Management Fee paid by Alt account: a fee, so part of the return (same judgment as ManAltF) |
| ManCheck | INTERNAL | | Management Fee paid by check: a fee, so part of the return |
| QA | INTERNAL | | Quantity Adjustment Transaction: the custodian corrects a quantity inside the account |
| TRCISU | EXTERNAL | +1 | Position Transfer In (same description as trfi): securities arrive from outside |
| TRFIR | EXTERNAL | +1 | Position Transfer In with Rin Tag: securities arrive from another account or custodian |
| ac | INTERNAL | | Return of Capital: cash paid by a holding into the same account, so value stays inside |
| acca | INTERNAL | | Adjust Cost Corporate Action: cost basis only, no value crosses the boundary |
| accal | INTERNAL | | Adjust Cost Corporate Action (lot): cost basis only, no value crosses the boundary |
| bcf | INTERNAL | | Bounced Check Fee: a fee |
| by | INTERNAL | | Buy: cash becomes securities inside the account |
| cbf | INTERNAL | | Checkbook Fee: a fee |
| ci | INTERNAL | | Contribution to Income: income already in the account buys shares (not a client contribution) |
| cs | INTERNAL | | Buy to Cover Short: a trade inside the account |
| csltfee | INTERNAL | | Consulting Fee Expense: a fee (the vendor type carries a trailing space, kept exactly) |
| dv | INTERNAL | | Dividend Received: income earned by the account, part of the return |
| dvlt | INTERNAL | | Long Term Capital Gain distribution: income earned by the account |
| dvr | INTERNAL | | Reinvestment: income already in the account buys shares |
| dvst | INTERNAL | | Short Term Capital Gain distribution: income earned by the account |
| fch | INTERNAL | | IRA Maintenance Expenses: a fee |
| fco | INTERNAL | | IRA Close Expenses: a fee |
| fee | INTERNAL | | IRA Expense: a fee |
| frntax | INTERNAL | | Foreign Tax: withheld at source from the holding's own income, so a cost inside the return |
| ftax | EXTERNAL | -1 | Federal Tax Withholding: client money paid to the tax authority out of the account, not a cost of managing it (a judgment: if it is withheld from a dividend before the account books it, the return reads low by that amount) |
| genmain | INTERNAL | | General Maintenance Fee: a fee |
| ileu | INTERNAL | | Cash in Lieu Income: income record of a fraction the corporate action paid in cash |
| int | INTERNAL | | Interest Income: earned by the account |
| leu | INTERNAL | | Cash in Lieu: a share fraction sold for cash inside the account |
| li | EXTERNAL | +1 | Contribution to Asset: the client puts cash or securities into the account |
| lica | INTERNAL | | Corporate Action Contribution: shares received in a corporate action exchange (paired with loca), no new money |
| licar | INTERNAL | | Corporate Action Contribution with Rin Tag: shares received in a corporate action exchange |
| lo | EXTERNAL | -1 | Withdrawal from Asset: the client takes cash or securities out of the account |
| loca | INTERNAL | | Corporate Action Withdrawal: shares given up in a corporate action exchange, no money leaves |
| man | INTERNAL | | Management Fee: a fee, so part of the return |
| misc | INTERNAL | | Miscellaneous Expenses: an expense charged to the account |
| pcf | INTERNAL | | PCF Expenses: an expense charged to the account |
| pyd | INTERNAL | | Paydown: bond principal returned as cash inside the account |
| roy | INTERNAL | | Royalty Payment: income earned by the account |
| si | EXTERNAL | -1 | Short Contribution: a short position is contributed in, which lowers the account's value |
| sl | INTERNAL | | Sell: securities become cash inside the account |
| so | EXTERNAL | +1 | Short Withdrawal: a short position is taken out, which raises the account's value |
| ss | INTERNAL | | Short Sell: a trade inside the account |
| stax | EXTERNAL | -1 | State Tax Withholding: client money paid to the tax authority out of the account (same judgment as ftax) |
| stp | INTERNAL | | Stop Payment Expense: a fee |
| term | INTERNAL | | Termination Fee: a fee |
| trci | EXTERNAL | +1 | Position Transfer In (same description as trfi): securities arrive from outside |
| trco | EXTERNAL | -1 | Position Transfer Out (same description as trfo): securities leave |
| trfi | EXTERNAL | +1 | Position Transfer In: securities arrive from another account or custodian |
| trfo | EXTERNAL | -1 | Position Transfer Out: securities leave to another account or custodian |

## Worked account-month: acct#e29efebe, 2025-09 (CB-q-1)

One account-month that contains a valued zero-Amount transfer and is fully priced. The row: Trade_Date 2025-09-24, type `lo`
(Withdrawal from Asset, direction -1), Amount 0, CUSIP 594918104, Quantity 21. That day's close for the CUSIP in
`security_day_price.parquet` is 508.037384 (store cottonwood-silver-canonical-prices), so the flow is
-1 x 21 x 508.037384 = -10668.785065.

Before (no price used, the Amount-0 row blanks its day): 2025-09-24 has `ret` null, reason FLOW_UNVALUED, so the month has 1
blank day of 21 and the monthly grade is UNGRADABLE (reported 0.84).

After: 2025-09-24 value 1188.40, flow -10668.785065, ret 0.001625 (computed from 11837.946173 the day before); the month has
no blank day, strings to 0.7664 percent against Commonwealth's reported 0.84, diff -0.0736 percentage points, which exceeds
the 0.05 tolerance, so the grade is DIFF. The transfer is now valued; the month does not match Commonwealth.

Grades written by `commonwealth_monthly_grade.py`: `grade_acct#e29efebe_2025-09_before/monthly_grade.csv` and
`grade_acct#e29efebe_2025-09_after/monthly_grade.csv` beside this report.

Across the whole run, 6 months moved from UNGRADABLE to graded on this change (ungradable 78,362 -> 78,356), all six DIFF
(DIFF 2,284 -> 2,290; MATCH 1,947 unchanged); all six carry `lo` or `li` rows, none a `trf*` row.

Flow sign: direction x |Amount| per flow row (the vendor's Amount sign convention is not relied on). To be checked against real rows at the first real run.

DAILY-RETURNS account_days=1691729 computed=127396 blank=1564333 flow_types=61 of 61 zero_amount=20403 valued=5017 blank_no_price=15386
