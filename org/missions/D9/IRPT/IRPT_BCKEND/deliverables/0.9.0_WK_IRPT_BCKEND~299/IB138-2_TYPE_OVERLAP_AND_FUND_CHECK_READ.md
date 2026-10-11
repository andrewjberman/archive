# IB138-2 -- both witnesses per instrument type, and each priced fund trade beside the reader's bars (IB-pr-441, round 138)

READ ONLY. Counts only. No class is admitted by this cell, nothing is built or served, no claim is re-graded, no other source was asked. `RIC/BDC` below is the source's value `Securities Issued by Registered Investment Companies or Business Development Companies`.

## The join (type from the transactions table, by CUSIP)

- Securities both witnesses carry: **894** (IB-pr-439 counted 894). Found ONE type: **840**; found NO transaction row: **0**; found MORE THAN ONE type (put under `MIXED`): **54**.
- How a type is taken: all de-duplicated (on TransactionID) transaction rows of the CUSIP are read, of every transaction kind and every date; the set of distinct (SEC Asset Type, Share Class Type) pairs is taken, a blank value written '<blank>'. One pair -> that pair is the type. No row for the CUSIP -> NO_TYPE. More than one pair -> MIXED (the combinations and counts are in mixed_combinations).
- The `MIXED` combinations (securities): Exchange-Traded Equity Securities / Not Available + Not Available / Not Available = 38; Not Available / Inst + RIC/BDC / Inst = 6; Not Available / Not Available + RIC/BDC / Not Available = 6; Not Available / A + RIC/BDC / A = 3; Not Available / Other + RIC/BDC / Other = 1.
- Transactions table: 121 date partitions (2026-03-09 to 2026-10-11), 1042552 rows read, 99723 distinct TransactionIDs.

## Table 1 -- the reader's bar for day t against the anchor's close for day t, per type (85 trading days, 2026-06-10 to 2026-10-09)

| type (SEC Asset Type / Share Class Type) | securities | security-days | equal | one_day_off | neither | no_bar | equal on days the close moved | securities with any one_day_off |
|---|---|---|---|---|---|---|---|---|
| Cash and Cash Equivalents / Not Available | 1 | 85 | 83 | 0 | 0 | 2 | 0 | 0 |
| Exchange-Traded Equity Securities / Not Available | 479 | 36863 | 36247 | 0 | 337 | 279 | 35933 | 0 |
| MIXED | 54 | 3633 | 3587 | 0 | 46 | 0 | 3505 | 0 |
| Not Available / Not Available | 141 | 9882 | 9838 | 0 | 19 | 25 | 9734 | 0 |
| RIC/BDC / A | 6 | 411 | 411 | 0 | 0 | 0 | 407 | 0 |
| RIC/BDC / ETF | 28 | 2137 | 2135 | 0 | 2 | 0 | 2072 | 0 |
| RIC/BDC / Inst | 31 | 1474 | 1469 | 2 | 3 | 0 | 1264 | 2 |
| RIC/BDC / Inv | 2 | 91 | 85 | 0 | 0 | 6 | 83 | 0 |
| RIC/BDC / No Load | 10 | 391 | 391 | 0 | 0 | 0 | 379 | 0 |
| RIC/BDC / Not Available | 123 | 8596 | 8501 | 3 | 92 | 0 | 8100 | 2 |
| RIC/BDC / Other | 15 | 857 | 857 | 0 | 0 | 0 | 834 | 0 |
| RIC/BDC / Retirement | 4 | 116 | 116 | 0 | 0 | 0 | 107 | 0 |
| **all types** | **894** | **64536** | **63720** | **5** | **499** | **312** | **62418** | **4** |

- A security-day is a day on which the anchor carries the security (the comparison needs its close). Rule: For a security and a trading day t of the 85 (2026-06-10 to 2026-10-09) on which the anchor carries it: the reader's bar for t is compared with the anchor's closing_price for t at relative 1e-4. equal = within that tolerance. Not equal, and the reader's bar for t is within that tolerance of the anchor's close for the PRIOR or the NEXT trading day = one_day_off. Otherwise neither. No reader bar for t (the ticker returned nothing, or no bar that day) = no_bar. A day on which the anchor does not carry the security is not a security-day (counted in anchor_days_not_carried).
- When the anchor's close for t equals its close for the prior or next trading day, the reader's bar equals the anchor's for t and the day is `equal` (tested first), never one_day_off; it is counted in `equal` but NOT in `equal_on_days_the_close_moved`, because on an unchanged day a correct date label and a shifted one read the same.
- Types whose one_day_off column is EMPTY (and equal above 0): Cash and Cash Equivalents / Not Available; Exchange-Traded Equity Securities / Not Available; MIXED; Not Available / Not Available; RIC/BDC / A; RIC/BDC / ETF; RIC/BDC / Inv; RIC/BDC / No Load; RIC/BDC / Other; RIC/BDC / Retirement.
- Edges: the comparison for 2026-10-09 has no next-trading-day value on the anchor side (the anchor partition for 2026-10-12 is absent) and the reader's latest bar is 2026-10-09; the prior day of 2026-06-10 is 2026-06-09, present on both sides

### What is behind every non-empty one_day_off entry

- **RIC/BDC / Inst**: 2 one_day_off security-days, on 2 securities, on 2 dates; dates with 3 or more securities at once: 0.
- **RIC/BDC / Not Available**: 3 one_day_off security-days, on 2 securities, on 3 dates; dates with 3 or more securities at once: 0.

| type | ticker | date | the reader's bar for t equals the anchor close of the | that ticker's one_day_off days | securities one_day_off that date |
|---|---|---|---|---|---|
| RIC/BDC / Not Available | SHM | 2026-06-30 | prior day | 2 | 1 |
| RIC/BDC / Not Available | SHM | 2026-07-20 | prior day | 2 | 1 |
| RIC/BDC / Inst | MEIIX | 2026-07-02 | prior day | 1 | 1 |
| RIC/BDC / Inst | MISIX | 2026-10-09 | prior day | 1 | 1 |
| RIC/BDC / Not Available | PZA | 2026-07-31 | prior and the next day | 1 | 1 |

Every date is one security alone (no date has 3 or more at once), so none is a calendar or holiday effect; each is a single security on a single date (a corporate action, a distribution day or a bad bar -- the data here do not say which; INFERRED, not tested). 

## Table 2 -- every priced fund trade beside the reader's bars

- Fund = a row of the transactions table (de-duplicated on TransactionID) with Transaction Type Buy or Sale, Price above 0, SEC Asset Type 'Securities Issued by Registered Investment Companies or Business Development Companies' and Share Class Type neither 'ETF' nor 'Not Available'; the fund is the CUSIP
- Unit: TRADES (rows, de-duplicated by TransactionID) whose Trade Date is one of the 85 graded trading days; fund_dates = distinct (fund, trade date) pairs among them. IB-pr-439 counted 1,099 fund-dates over 103 funds, 1,044 inside the 85 days; this cell: 1044 fund-dates over 103 funds with a Trade Date inside the 85 days; over all dates 6280 trades on 1099 fund-dates over 103 funds (the 131 trades before 2026-06-10 are not compared: the reader's window is fixed at 2026-06-05 to 2026-10-13).
- Date column: Trade Date (mm/dd/yyyy); the second line uses Settle Date (same format). Tolerance: relative 1e-4 of the larger of the trade Price and the reader's bar (the instrument's tolerance); the same six counts to the cent (both rounded to 2 decimals, equal) are in to_the_cent

| basis | trades | same_day_only | prior_day_only | next_day_only | more_than_one | none | no_bar |
|---|---|---|---|---|---|---|---|
| trade date, relative 1e-4 | 6149 | 4490 | 28 | 0 | 1102 | 245 | 284 |
| trade date, to the cent | 6149 | 4744 | 34 | 3 | 901 | 183 | 284 |
| settle date, relative 1e-4 | 5827 | 476 | 4012 | 0 | 814 | 234 | 291 |
| settle date, to the cent | 5827 | 499 | 4245 | 3 | 616 | 173 | 291 |

1044 fund-dates, 103 funds. Settle line: 322 trades whose settle date lies outside the reader's window are left out. `no_bar` = the fund's ticker returned nothing (FPNIX: 284 trades) -- the reader has a bar for no other fund-date asked.

### Where the off-day trades concentrate

- `prior_day_only` (28 trades, 5 funds; to the cent 34 trades): by fund [['NCHRX', 13], ['NHMRX', 7], ['NSIOX', 4], ['FLTRX', 3], ['VWIUX', 1]]; by trade date [['2026-09-01', 9], ['2026-10-01', 9], ['2026-08-03', 7], ['2026-07-01', 2], ['2026-08-31', 1]]; kinds {'Buy / Dividend Reinvestment': 28}. All are dividend-reinvestment buys.
- `next_day_only` (0 trades; to the cent 3 trades, funds [['VWIUX', 1], ['PFMIX', 1], ['NHMRX', 1]], dates [['2026-06-30', 2], ['2026-07-01', 1]], kinds {'Buy / Dividend Reinvestment': 3}).
- `more_than_one` (1102 trades, 47 funds): by fund [['EIBIX', 262], ['PFORX', 226], ['FSMAX', 226], ['CDSIX', 39], ['VWIUX', 37], ['PFMIX', 35]]; by trade date [['2026-07-14', 672], ['2026-07-31', 71], ['2026-06-30', 49], ['2026-09-29', 44]]; kinds {'Sale / Sale': 904, 'Buy / Buy': 54, 'Buy / Dividend Reinvestment': 144}. A bar that did not move across the days it matches.
- `none` (245 trades, 30 funds): by fund [['DFSTX', 23], ['FKGRX', 23], ['RLBFX', 23], ['JATTX', 23], ['VWIUX', 15], ['PFMIX', 11]]; by trade date [['2026-06-30', 31], ['2026-07-31', 21], ['2026-08-31', 19], ['2026-09-04', 18]]; kinds {'Buy / Buy': 145, 'Buy / Dividend Reinvestment': 90, 'Sale / Sale': 10}. Relative difference to the trade-date bar: {'median': 0.00879858883641174, 'p10': 0.0001503735493290499, 'p90': 1.8943497986362228}; 95 of them are under 0.1 percent.
- Trade kinds, all 6149 trades: {'Sale / Sale': 4968, 'Buy / Buy': 651, 'Buy / Dividend Reinvestment': 530}. Funds with any prior_day_only or next_day_only trade: 5 of 103.

Per fund (`by_fund`, ticker, trades and the six counts) is in the json: 103 rows.

## Fetch, control, bounds

- Yahoo Finance through `fetch_yahoo` / `read_yahoo_close` (unedited), unadjusted Close, window 2026-06-05 to 2026-10-13 (end exclusive 2026-10-14): **19 calls, 948 distinct tickers, each asked once** (944 with bars, 4 with none); none rate-limited. Pause 8 s between calls, no parallel call. Ticker list: 890 first tickers of the securities both witnesses carry and 103 tickers of the funds with a priced trade inside the 85 days; the two lists overlap in 45.
- Control (planted, read equal: True): a series shifted one day late and one a day early read one_day_off on the days the price moved; the unshifted reads equal; three planted trades (the same day's bar, the prior day's bar, a price matching none) read `same_day_only`, `prior_day_only`, `none`; the other three outcomes are planted too.
- `claims_regraded_in_product` false; `other_sources_asked` 0; `classes_admitted_by_this_cell` 0.

## Reading (marked INFERRED where it is)

- Table 1: of 64,536 security-days, 63,720 are equal (62,418 of them on days the anchor's close moved, so they can tell a right date label from a shifted one), 5 are one_day_off (4 securities, 5 dates, never two securities on one date), 499 are neither and 312 are no_bar. Ten of the twelve types have an EMPTY one_day_off column, including `Exchange-Traded Equity Securities / Not Available` (479 securities, 36,863 security-days, 0 one_day_off) and `MIXED`. Only two types are not empty: RIC/BDC / Inst (2 days) and RIC/BDC / Not Available (3 days). The `neither` days (499) are not a one-day shift of the label; their cause was not examined. The 312 no_bar come from 4 tickers the reader returned nothing for and from days the reader has no bar.
- Table 2: a mutual-fund trade is struck at the trade date's NAV. By trade date, 4,490 of 6,149 trades read same_day_only; 28 read prior_day_only; 0 read next_day_only (3 to the cent). If the reader labelled a fund's value one day LATE, the trade price would equal the reader's bar for the NEXT day and next_day_only would pile up; it is 0. INFERRED: the reader's fund labels show no late shift on these trades; this cell grades no claim and admits no class.
- The 28 prior_day_only trades (34 to the cent) are all dividend-reinvestment buys in 5 funds, and 27 of the 28 fall on the first business day of a month (2026-07-01, 08-03, 09-01, 10-01; one on 08-31); no Sale and no ordinary Buy reads prior_day_only. INFERRED: a reinvestment booked a business day after the NAV it was struck at, a trade-side date, not the reader's label.
- more_than_one (1,102): the bar did not move across the days the price matches. 672 of them are on one trade date, 2026-07-14, and three funds carry 714 of the 1,102 (262, 226, 226); relative 1e-4 is wider than a cent for a NAV above $100, so the to-the-cent line reads more_than_one 901 and same_day_only 4,744. Neither line separates the label from an unmoved bar for these.
- none (245 trades, 30 funds): four funds carry all 23 of theirs (no trade matches any of three bars); the median relative gap to the trade-date bar is 0.88 percent and 95 of the 245 are within 0.1 percent. The cause was not examined (a distribution day, a price that is not the NAV, or a bar that differs from the custodian's).
- no_bar (284) is one fund, whose ticker the reader returned nothing for.
- By settle date, 4,012 trades read prior_day_only: a settle date is typically one business day after the trade date (INFERRED from the rows seen, not counted), so the trade's price equals the bar of the day before the settle date. Same fact as the trade-date line, not a second witness.
- Bounds met: the 85-day window; for 2026-10-09 neither side has a next-trading-day value (anchor partition and reader bar for 2026-10-12 absent), so a next-day match is impossible on that date and that date's trades count under the other outcomes.
- All 54 MIXED securities pair the source's value 'Not Available' with one stated value (38 pair the exchange-traded value, 16 the RIC/BDC value); taking the stated value over 'Not Available' would move them into those types. That rule was NOT applied (the order puts disagreeing rows under MIXED); the 54 are 3,633 security-days, none one_day_off.

