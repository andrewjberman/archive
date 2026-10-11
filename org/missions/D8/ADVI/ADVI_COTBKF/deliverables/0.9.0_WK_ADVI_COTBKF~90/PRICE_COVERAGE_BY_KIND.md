# Price coverage by kind, 2026-05-06 (ADVI_COTBKF.TO-CB-bl-1, round 64)

Worker 0.9.0_WK_ADVI_COTBKF~90. Read-only. Counts, shares, asset kinds only; no account figure. Record: `PRICE_COVERAGE_BY_KIND.json`.

**Totals (reproduced):** 826 securities, 459 unpriced; 10,090 position rows, 6,122 unpriced rows. A security is unpriced when every one of its rows has a null value (no security is partly priced).

| kind | securities | unpriced | rows | unpriced rows | custodian trade-derived price within 5 days | store price on the date | ruled source |
|---|---|---|---|---|---|---|---|
| Fixed Income | 184 | 184 | 233 | 233 | 5 | 0 | Bloomberg site Z |
| Mutual Fund | 113 | 89 | 6,635 | 5,458 | 29 | 0 (1 under a reused ticker) | Yahoo |
| Equity | 294 | 68 | 986 | 137 | 3 | 0 (22 under a reused ticker) | Yahoo |
| Cash Equivalent | 57 | 55 | 212 | 95 | 4 | 0 | Bloomberg site Z |
| ETF | 134 | 24 | 1,279 | 107 | 3 | 0 (9 under a reused ticker) | Yahoo |
| Mutual Fund (Closed End) | 28 | 24 | 108 | 63 | 2 | 0 | Yahoo |
| Annuity | 12 | 12 | 24 | 24 | 4 | 0 | Bloomberg site Z |
| Alternative Investment | 3 | 3 | 5 | 5 | 1 | 0 | Bloomberg site Z |
| Cash | 1 | 0 | 608 | 0 | 0 | n/a | n/a |
| **all** | **826** | **459** | **10,090** | **6,122** | | | |

**(a) The custodian's own data.** The positions table (469 rows, one date, 2026-06-23) carries Quantity only; the performance table carries returns only. No price or market-value column exists (0 of 459 for every kind). The transactions carry Amount and Quantity, from which a price PAID can be derived for by/sl/dvr rows. The build reads none of it for pricing (daily_valuation.py:83-98). Within 5 calendar days of the date: Fixed Income 5 of 184, Mutual Fund 29 of 89, Equity 3 of 68, Cash Equivalent 4 of 55, ETF 3 of 24, Closed End 2 of 24, Annuity 4 of 12, Alternative 1 of 3. Same day: Mutual Fund 4, all others 0. This is a trade price, not a close, and the build may not carry a price across days.

**(b) The stores the build reads.** Of the six stores (local cached copies), 0 of 459 unpriced securities have a price on the date by the build's match rule. Gold canonical holdings (the custodian mark on a held position) holds CUSIP-keyed rows for 428 of the 459, but only on 2026-06-08 to 2026-10-06. Silver canonical prices run 2020-06-30 to 2026-06-09 and hold nothing under any of the 459 by CUSIP or a clean ticker. One finding: 32 unpriced securities (Equity 22, ETF 9, Mutual Fund 1; 426 of 6,122 unpriced rows) have a price row on the date under a symbol that more than one CUSIP has listed; the build declines it (price_census.py:195-214). Whether it is the right security's price is not established.

**Ruled source (PRD lines 217-221):** Yahoo Finance for equity, ETF and fund; Bloomberg at site Z for fixed income and other. Not shown pulled for the unpriced securities (price-need file fetched=0).

**Not established:** see `not_established` in the record (9 items), among them the correctness of the 32 reused-ticker rows, the age of the cached store copies, the raw bronze headers, the unit of trade-derived bond prices, and whether MDPF_SECHIST holds anything.
