# IB-pr-436 -- nine mutual funds by 85 trading days: the custodian's mark against an independent daily NAV (counts only)

Read only. Same source partitions, price rule (Market Value / Units), tolerance (relative 1e-4), trading-day axis and one-way account digest as IB-pr-435; the same 76,796 account-days were read (v0.35 totals equal the re-count). 85 graded days, 2026-06-10 to 2026-10-09. No account id, balance or single account's holding is written. Nothing is re-graded (`claims_regraded: false`).

**NAV source.** Yahoo Finance, unadjusted Close, through the cell-named reader: `fetch_yahoo` (silver `commonwealth_price_basis_census.py`) and `read_yahoo_close` (silver `commonwealth_daily_valuation.py`), neither edited. ONE fetch call, ten tickers (nine funds plus the control), window 2026-06-08 to 2026-10-10. It returned bars (87 each, 2026-06-08 to 2026-10-09) for nine of ten; FPNIX returned nothing ("possibly delisted; no price data found"), so its 85 fund-days are `no_nav_found`; no retry, no other source. Already held in the other cell's cache before this fetch: FSMAX with 1,578 rows (equal to this fetch on 86 of 86 common dates), FPNIX as a none-marker, the other seven no file. `yfinance` here is 1.7.0 (the order says 1.2.0).

**Rule.** The mark of a fund-day is the cluster of rows (equal within 1e-4) holding the most rows, its median; a tie goes to the lower mark (0 ties). 23 to 33 of the 85 days per fund hold a second mark. Tolerance: 1e-4 relative serves cent-quoted NAVs (a one-cent step on a NAV near 10 is 1e-3 relative); the one-cent count of `equals_neither` is 0 for every fund because no fund-day is `equals_neither`.

| fund | fund-days | day NAV only | prior-day NAV only | both (NAV unchanged) | neither | no NAV | NAV days found of needed |
|---|---|---|---|---|---|---|---|
| FLCOX | 85 | 81 | 0 | 4 | 0 | 0 | 86 of 86 |
| MFEIX | 85 | 85 | 0 | 0 | 0 | 0 | 86 of 86 |
| CEMIX | 85 | 83 | 0 | 2 | 0 | 0 | 86 of 86 |
| FSGGX | 85 | 82 | 0 | 3 | 0 | 0 | 86 of 86 |
| FSMAX | 85 | 83 | 0 | 2 | 0 | 0 | 86 of 86 |
| FXNAX | 85 | 74 | 0 | 11 | 0 | 0 | 86 of 86 |
| FSPGX | 85 | 83 | 0 | 2 | 0 | 0 | 86 of 86 |
| CDSIX | 85 | 71 | 0 | 14 | 0 | 0 | 86 of 86 |
| FPNIX | 85 | 0 | 0 | 0 | 0 | 85 | 0 of 86 |
| **total** | **765** | **642** | **0** | **38** | **0** | **85** | |

**Prior-day marks: by day or by fund?** At the fund-day level there are none (0 of 680 fund-days with both NAVs). The majority mark is always the day's NAV, so nothing clusters there. At the ROW level, beside the rule, 497 of 124,645 rows with a NAV equal only the prior day's NAV and 42 equal neither; these hide inside the majority rule. They cluster by DAY and not by fund: 33 of 85 days carry them, 2 to 22 rows a day (mostly 12 to 22, about 16, spread evenly over the funds) on 30 days from 2026-08-26 on, and 17 on 2026-06-22, 41 on 2026-07-02 (5 per fund) and 3 on 2026-07-31 before that; each of the eight funds has 50 to 67 such rows, so no fund stands out. The 42 `neither` rows are 14 rows on each of 2026-09-01, 2026-10-01 and 2026-10-02. Landing time does not separate those days: 29 of the 33 days landed the calendar day after D, and so did 13 days without any; 17 early days landed in one 19:00 UTC batch up to 34 days late.

**Is Yahoo's fund Close the NAV of that day?** Answer: probably yes for the eight funds answered. Claim: `inferred`. Evidence: 642 + 38 of 680 fund-days with both NAVs agree with the day's NAV and none with only the prior day's, across all eight funds and all five weekdays; the control below shows the reader's date convention matches the anchor's for a public close; FSMAX agrees with the other cell's cache on 86 of 86 dates. It stays inferred, not measured: the custodian's mark is not a second public statement of the NAV (the CTO ruled it cannot grade itself), and no second public source was permitted by the bound.

**Control.** VTI (CUSIP 922908769, held by the accounts and in the anchor on every one of the 86 days): the reader's Close equals the anchor's `closing_price` of the same partition day on 85 of 85 trading days, largest relative difference 4.0e-08; 0 days equal the prior day's Close only.

**Account-day effect (an upper bound; nothing re-graded).** Under the cash rule in force, 583 account-days have no outside-anchor row other than these nine funds (600 before the cash rule). Of those 583: 579 have every fund row at the day's NAV or both; 1 has one or more rows at the prior day's NAV only; 3 have a row with neither a NAV nor a match (all three hold FPNIX, no NAV found). Of the 579, 563 hold no other ungradeable kind. Each fund row of an account-day is graded by its own mark (not the fund-day's chosen mark). The 583 are 1.7 percent of the 34,789 account-days holding an outside-anchor row: the other account-days hold other outside-anchor securities beside these funds.

**Not measured.** Whether any NAV is the right price for the holding; FPNIX's NAV from any source (the reader returned nothing; one source only was allowed); whether Yahoo's date for a fund equals a second public source's (none permitted); the value weight of any account-day; claims re-graded with a NAV; days after 2026-10-09; the other 725 securities of the ranking; why 2026-08-26 on carries a steady prior-day row set (the rows are counted, not traced to an account).
