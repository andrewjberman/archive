STATUS: WRITTEN, NOT SENT

# Price request: Yahoo Finance (equity, ETF and fund securities)

**Size: 3,102 securities, 1,556,036 security-days of daily prices.** Nothing has been sent or fetched.

## What is asked
A daily closing price for each security in `PRICE_REQUEST_YAHOO.csv`, for the dates it is held with no price. Dates run from 2013-04-08 to 2026-06-22 across the list; each security's own first and last date are in the csv. This is Andrew's word: Yahoo Finance for equity, ETF and fund securities (ADVI_COTBKF_PRD.md, v0.4 Addendum 2, lines 214-220).

## Which securities
3,102 securities, grouped the way the build groups them (commonwealth_price_need_file.py:41 and :45-46): Equity, ETF, Mutual Fund, Mutual Fund (Closed End), Unit Investment Trust. Each is held unpriced on at least one date.

| Kind | Securities | Without a symbol | Security-days | Unpriced position rows |
|---|---|---|---|---|
| ETF | 265 | 0 | 145,212 | 1,186,111 |
| Equity | 1,718 | 38 | 798,348 | 3,387,552 |
| Mutual Fund | 963 | 28 | 490,095 | 10,056,038 |
| Mutual Fund (Closed End) | 98 | 2 | 106,651 | 195,464 |
| Unit Investment Trust | 58 | 56 | 15,730 | 40,350 |

- **124 securities have no symbol** (56 of them unit investment trusts). A symbol request cannot name them. The delivery carries their 9-character CUSIP, and the csv lists that CUSIP as the identifier (`identifier_type` = cusip). Someone must map them to a Yahoo symbol, or they stay unpriced.
- 210 of the securities with a symbol share one of 103 symbols with another CUSIP in this list. The csv `cusip` column keeps them apart. The build credits no price to a symbol claimed by more than one CUSIP, so those need a decision before they are priced.
- 603 of the 3,102 securities are priced on some dates already; the request is for their unpriced dates only. The span still runs first to last unpriced date, so a span can contain dates that are already priced.

## Size
- 1,556,036 security-days (a security counted once per date it is held unpriced).
- If each security's whole first-to-last span is requested: 2,047,718 points. No Yahoo limit was read.
- 14,865,515 unpriced position rows, of 15,993,996 unpriced in the table of 21,102,041.

## Where the prices land
In the securities history that MDPF_SECHIST owns (ADVI_COTBKF_PRD.md lines 220-221: "Prices land once per security in the securities history MDPF_SECHIST owns"). This project does not own it and writes nothing there. A security neither source prices leaves its days unpriced (same lines).

## What it would unblank (upper bound)
Of 1,559,722 account-days that are blank for price:
- **1,257,183 (80.60 percent) would be fully priced by this request alone**, because every unpriced row in them is in this list.
- A further 183,461 (11.76 percent) need this request and the Bloomberg one.
- These are UPPER BOUNDS. Yahoo may not price every security asked for, and a return also needs the prior day's value.

## What is not established
- That Yahoo prices any of these securities; nothing was requested.
- Any Yahoo limit or terms of use; none was read.
- Whether the symbol in the transactions cache was the symbol on every date held, 2013 to 2026.
- Whether MDPF_SECHIST accepts this delivery; its owner has not seen it.
- Whether the denominator matches the returns table's own NOT_MEASURABLE count.

Measured from `account_day_value.parquet` (21,102,041 rows) and the silver transactions cache. Detail: `PRICE_REQUESTS.json`.
