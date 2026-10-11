# IB-pr-435 -- the securities the anchor does not carry, the cash rule counted, and the price stores the estate already holds (counts only)

Read only. Same source, anchor, price rule, tolerance and trading-day axis as the re-count of IB-pr-429 AMENDMENT 2. 85 graded days, 2026-06-10 to 2026-10-09. The same account-days were read: yes, this run's v0.35 totals equal the re-count file exactly (UNGRADEABLE 42,967; ACCT_OWN_DATE 20,138; NOTHING_TO_GRADE 13,636; ACCT_PRIOR_DATE 55; present 76,796). No account id, balance or single account's holding is written.

**Ranking (counted BEFORE the cash rule's additions; list, total and both cover counts are on that one basis).** 734 securities sit behind an OUTSIDE_ANCHOR row, carrying 264,720 security-account-days over 34,437 distinct account-days (the re-count read 34,437). 9 securities cover half of the carried security-account-days; 236 cover ninety percent.

| # | CUSIP | ticker | name | account-days | coverage (found of needed days) | best store |
|---|---|---|---|---|---|---|
| 1 | 31635V679 | FLCOX | FIDELITY LARGE CAP VALUE INDEX | 17,051 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |
| 2 | 552985863 | MFEIX | MFS GROWTH I | 15,801 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |
| 3 | 149498107 | CEMIX | CAUSEWAY EMERGING MARKETS INSTL | 15,775 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |
| 4 | 316146315 | FSGGX | FIDELITY GLOBAL EX US INDEX | 15,666 | every_needed_day (85 of 85) | own-firm-gold-canonical-holdings |
| 5 | 315911743 | FSMAX | FIDELITY EXTENDED MARKET INDEX | 15,118 | every_needed_day (84 of 84) | own-firm-gold-canonical-holdings |
| 6 | 316146356 | FXNAX | FIDELITY U.S. BOND INDEX | 14,553 | every_needed_day (85 of 85) | own-firm-gold-canonical-holdings |
| 7 | 31635V729 | FSPGX | FIDELITY LARGE CAP GROWTH IDX | 14,283 | every_needed_day (76 of 76) | own-firm-gold-canonical-holdings |
| 8 | 13161T401 | CDSIX | CALVERT SHORT DURATION INCOME I | 12,670 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |
| 9 | 30254T643 | FPNIX | FPA NEW INCOME - INSTITUTIONAL | 12,115 | every_needed_day (82 of 82) | own-firm-gold-canonical-holdings |
| 10 | 746745405 | PEIYX | PUTNAM LARGE CAP VALUE Y | 10,316 | every_needed_day (41 of 41) | own-firm-gold-canonical-holdings |
| 11 | 4812C0381 | WOBDX | JPMORGAN CORE BOND I | 9,199 | every_needed_day (47 of 47) | own-firm-gold-canonical-holdings |
| 12 | 316066752 | FSSZX | FIDELITY ADVISOR STOCK SELECTOR SM CP Z | 8,063 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |
| 13 | 14064D865 | FTHSX | FULLERTHALER BEHAVIORAL SM-CP EQ INST | 7,605 | every_needed_day (81 of 81) | own-firm-gold-canonical-holdings |
| 14 | 277907200 | EIBIX | EATON VANCE INCOME FUND OF BOSTON I | 5,321 | every_needed_day (60 of 60) | own-firm-gold-canonical-holdings |
| 15 | 648018745 | FFPNX | AMERICAN FUNDS NEW PERSPECTIVE 529-F-2 | 3,003 | some_needed_days (41 of 47) | own-firm-gold-canonical-holdings |
| 16 | 027681741 | FFMMX | AMERICAN FUNDS AMERICAN MUTUAL 529-F-2 | 2,962 | some_needed_days (41 of 47) | own-firm-gold-canonical-holdings |
| 17 | 649280740 | FNFWX | AMERICAN FUNDS NEW WORLD 529-F-2 | 2,932 | some_needed_days (41 of 47) | own-firm-gold-canonical-holdings |
| 18 | 097873749 | FFBOX | AMERICAN FUNDS BOND FUND OF AMER 529-F-2 | 2,663 | some_needed_days (41 of 47) | own-firm-gold-canonical-holdings |
| 19 | 69344A834 | PAAA | PGIM AAA CLO ETF | 2,447 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |
| 20 | 47103C704 | JBALX | JANUS HENDERSON BALANCED I | 2,181 | every_needed_day (86 of 86) | own-firm-gold-canonical-holdings |

**The cash rule, as ruled.** Of the 19,809 account-days the re-count named (31,307 hold a cash-flagged priced row outside the anchor): 19,466 keep every such row as cash (price equal in the day's partition and the prior trading day's); 0 have a row whose price differs and become OUTSIDE_ANCHOR; 343 cannot be compared because the row is absent from the prior trading day's partition. A not-comparable row is not cash ("only where measured"), so those 343 turn UNGRADEABLE in the primary counts (and the other treatment is counted beside). Across all 31,307 account-days: 30677 equal, 1 differs, 629 not comparable; by row: 31096 equal, 1 differs, 631 not comparable.

Four claims under the rule, 76,796 account-days: UNGRADEABLE 43,310 (re-count 42,967); ACCT_OWN_DATE 19,832 (20,138); NOTHING_TO_GRADE 13,599 (13,636); ACCT_PRIOR_DATE 55 (55). Serving: eligible 75,796, served 31,715, blank 44,081 = **58.157 percent** beside the re-count's 57.332 percent; accounts never served 382 of 999 (re-count 382 of 999). If the not-comparable rows stayed cash the counts equal the re-count's exactly. The securities the rule adds to OUTSIDE_ANCHOR: 3, adding 630 security-account-days (1 of them by a differing price) and taking the account-days holding an outside-anchor row from 34,437 to 34,789; they are not in the ranking above.

**Sixth reason.** 1 row (Units zero, Market Value above zero, not cash-flagged), 1 account-day, which reads UNGRADEABLE by its other rows. A refusal of the stamp, unchanged.

**The six stores** (found of needed security-days; needed = the day and the prior trading day of every account-day a ranked security is carried on, 45,216 in all; read through the census module's own readers; no other firm's store opened, barred calls 0):

- own-firm-silver-canonical-prices: opened, 2026-06-09 to 2026-06-09 in the window (store range 2020-06-30 to 2026-06-09), custodian_mark; 75 of 45,216 found (0.17 percent); 0 of 734 securities with every needed day. ticker key only; price_kind custodian_mark as grouped by 2.0.0_SA_COO~C2 (msg 5084), though the store's own source column mixes yahoo_finance, linear_interpolation and transaction_observed; it ends 2026-06-09, so it holds the prior-day close of the first graded day and nothing after, and no security can have every needed day from it.
- own-firm-gold-canonical-holdings: opened, 2026-06-09 to 2026-10-09 in the window (store range 2026-06-08 to 2026-10-09), custodian_mark; 44,837 of 45,216 found (99.16 percent); 502 of 734 securities with every needed day. the custodian's own mark on the held position (source bd_snapshot), the same value the source partition carries; NOT an independent close.
- rivalfunds-etfs-gold-security-market: opened, 2026-10-02 to 2026-10-02 in the window (store range 2026-10-02 to 2026-10-02), market_close; 1 of 45,216 found (0.0 percent); 0 of 734 securities with every needed day. a market store; one CUSIP of the ranking has a close here, on one date.
- etfs-bbg-testpull-ticker-history: opened, 2026-06-09 to 2026-08-24 in the window (store range 2020-12-31 to 2026-08-24), market_close; 143 of 45,216 found (0.32 percent); 1 of 734 securities with every needed day. Bloomberg-stored closes by ticker; ends 2026-08-24; a few tickers only.
- etfs-bbg-fund-daily: opened, no row for a ranked key in the window, market_close; 0 of 45,216 found (0.0 percent); 0 of 734 securities with every needed day. 36 daily CSVs of four ETFs (security column first token); none of the ranked tickers (the key declaration reaches it as declared; the first-token form was also checked: 0 overlap).
- portal-canon-return-daily-values: opened, no row for a ranked key in the window, market_close; 0 of 45,216 found (0.0 percent); 0 of 734 securities with every needed day. 87 index and currency series keyed by bbg_ticker (e.g. an index name); none of the ranked tickers (exact and first-token overlap both 0).
- LOCAL, not in the six: C:/dev/wk-cotbkf-81/.scratch/w99/proofA/after/security_day_price.parquet, 34,683 of 45,216 found (76.71 percent), 91 securities with every needed day. ADVI_COTBKF's derived table (cusip, date, price, store), read-only, another worker's scratch; a DERIVED table whose rows are copies of closes from the stores it names in its own `store` column, so it is not a seventh independent source; not served; not built here.

**Coverage by security** (union of the six stores): every needed day 502; some needed days 230; no needed day 2, of 734. **Upper bounds** (a found close does not say the holding sits at it; no claim re-graded): if every security with a close on every needed day from a market_close store were gradeable, 5 of the 34,437 account-days would stop being OUTSIDE_ANCHOR (5 of them holding no other ungradeable kind, so ungradeable no longer); with custodian_mark stores admitted as well, 28,836 (28,125). The custodian mark is the same custodian's value of the same holding, not an independent close.

**Control.** (1) The census module's own read_store read a 4-row fixture store: the planted present security-day read found, the planted absent one not found, a zero price not a close, an unasked key dropped; read equal to planted. (2) The cash rule on a 3-day, 4-account fixture with the equal, differs, absent-prior and inside-tolerance cases, claims known by construction; read equal to planted. (3) The inherited v0.35 claims control also reads equal.

**Not measured.** Whether any found close is the right price for the holding or sits where the account holds it; the value or balance weight of any blank; any claim re-graded with a store's price; any gold producer or anchor widening; days after 2026-10-09; the stores' content outside the ranked securities and the window; per-row claims (only per account-day).
