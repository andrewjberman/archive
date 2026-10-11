# IB-pr-438 -- the same reader over ALL the securities behind an outside-anchor row, one pass, and the account-days freed (counts only)

Read only. Same source partitions, price rule (Market Value / Units), tolerance (relative 1e-4), trading-day axis, row kinds, ordered claim rule and one-way account digest as IB-pr-435 / IB-pr-436 (their modules imported unchanged). 85 graded days, 2026-06-10 to 2026-10-09. **The same account-days were read: yes** -- under the cash rule UNGRADEABLE 43,310; ACCT_PRIOR_DATE 55; ACCT_OWN_DATE 19,832; NOTHING_TO_GRADE 13,599; present 76,796, equal to IB-pr-435; the v0.35 totals before the cash rule (42,967 / 55 / 20,138 / 13,636) also equal the re-count. 34,789 account-days hold an outside-anchor row after the cash rule, as IB-pr-435 counted. No account id, balance or single account's holding is written. Nothing is re-graded in the product (`claims_regraded_in_product: false`); no other source was asked (`other_sources_asked: 0`).

**1. The securities (basis: the cash rule in force, 737; IB-pr-435's 734 plus the rule's three additions).**

| class | securities | note |
|---|---|---|
| `no_ticker_to_ask_with` | 375 | the source's Ticker/Symbol is empty or is the security's own identifier (CUSIP-only bonds; the word CASH is the identifier of one). They sit on 27,735 security-account-days and **4,619 account-days**. Nothing was looked up or invented. |
| `asked_data_returned` | 356 | the ticker returned bars |
| `asked_no_data` | 6 | FPNIX (12,115 account-days), BRK.A (85; the source's dotted form, not altered), UHALB (32), JHG (16), MCR (8), QIWSQ (1) |

**Fetch.** 8 calls (7 of 50 tickers, 1 of 11), 361 distinct tickers (360 of securities plus the control VTI), 8 seconds between calls, none in parallel, none repeated (`tickers_asked_more_than_once: 0`); window 2026-06-08 to 2026-10-10, unadjusted Close, `fetch_yahoo` / `read_yahoo_close` unedited. 355 tickers returned bars, 6 returned nothing ("empty"), no rate limit. Two tickers (AMZE, GTBP) belong to two securities each and were asked once. A returned series means the TICKER returned bars; that it is the same instrument as the custodian's holding is not checked here.

**2-3. The account-days.** Each outside-anchor row is graded against the NAV of its day and the prior trading day (a date with no bar is no NAV). Each of the 34,789 account-days is in ONE outcome, first that applies:

| outcome | account-days |
|---|---|
| `one_or_more_with_no_nav` (no ticker, no data, or no bar on a needed date) | 17,410 |
| `one_or_more_at_neither` | 484 |
| `one_or_more_at_prior_day_nav_only` | 342 |
| `every_security_at_day_nav_or_unchanged` (**FREED**) | **16,553** (47.6 percent) |

Of the freed, **16,215** hold no other ungradeable kind (no NO_CUSIP, NEITHER_CLOSE, NEGATIVE_POSITION, no sixth-reason row). IB-pr-436's nine funds freed 563. The 17,410 split by what blocks them: no ticker only 3,799; no data only 11,851 (FPNIX is most of the no-data securities' weight); no bar only 887; mixes 873.

**4. Sizing under v0.36 (a sizing, not a claim anybody stamped).** IF every freed account-day with no other ungradeable kind took the claim its graded rows give (anchor-graded rows by the anchor as today, outside-anchor rows at the day's NAV: ACCT_OWN_DATE unless an anchor-graded row says ACCT_PRIOR_DATE), and an account-day with a prior-day-only row and nothing worse read ACCT_PRIOR_DATE, the claims would be UNGRADEABLE 26,914; ACCT_PRIOR_DATE 238; ACCT_OWN_DATE 36,045; NOTHING_TO_GRADE 13,599 (76,796). 16,213 move UNGRADEABLE to OWN and 183 to PRIOR.

| | rule in force | sized |
|---|---|---|
| eligible | 75,796 | 75,796 |
| served | 31,715 | 47,760 |
| blank | 44,081 | 28,036 |
| blank share | **58.157 percent** | **36.989 percent** |
| accounts never served | **382 of 999** | **181 of 999** |

ACCT_PRIOR_DATE is not a served claim under the serving rule, so the 238 stay blank.

**5. The prior-day rows.** 2,059 of 224,033 rows with a NAV (0.92 percent) equal only the prior day's NAV; 1,468 equal neither; 41,432 have no NAV (27,744 no ticker, 12,263 no data, 1,425 no bar). They fall on **61 of 85 days** and **blank 342 account-days** (181 of them hold no other ungradeable kind) -- the account-days whose only obstacle is a prior-day-only row. Cross-check on IB-pr-436's own basis (every priced row of the eight funds): 497 of 124,645 rows, 42 neither, 33 days -- reproduced exactly. **Do they cluster? Yes, in three ways, none traced to a cause:** by date (39 of 41 days from 2026-08-13 carry them, 22 of 44 before; the spike is 2026-07-02 with 179 rows); by security (34 securities with 10 or more rows and a prior-day rate of 20 percent or more hold 1,252 rows, 60.8 percent; fund-shaped tickers 0.84 percent of their rows, others 1.48 percent); with landing time (the 37 days whose last object landed in the 11 UTC hour carry them on 35 days and hold 1,498 rows; the 21 days landing in the 19 UTC hour carry them on 6).

**6. Control.** VTI (CUSIP 922908769, carried by the anchor every day): the reader's Close equals the anchor's `closing_price` on 85 of 85 days, largest relative difference 4.0e-08, none at the prior close only. The planted classifier / outcome-order / sizing control reads equal to planted.

**Not measured.** Whether a returned ticker is the same instrument as the holding; whether a NAV is the right price for a holding; the value weight of any account-day; FPNIX's NAV from any source; securities without a ticker; claims re-graded in the product; days after 2026-10-09; why the prior-day rows cluster. yfinance here is 1.7.0.
