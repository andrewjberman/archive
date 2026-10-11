# CB-bs-1 -- nine fund series against their own distributions, then the count over every fund series (round 71, 0.9.0_WK_ADVI_COTBKF~116)

A read-only measurement: no code, test, config or manifest changed; no AWS, vendor or network call (the Yahoo cache on disk was read as it stands). Records: `DIVIDEND_ADJUSTED_SERIES.json` (the named keys), `DIVIDEND_ADJUSTED_SERIES.csv` (the 81 series that read adjusted, funds 72, Equity 7, ETF 2), `DIVIDEND_ADJUSTED_SERIES_DETAIL.json` (each of the nine's pairs and daily steps).

**Headline.** In a table of 270 fund series (237 Mutual Fund, 33 Mutual Fund (Closed End)), 72 read DIVIDEND_ADJUSTED out of 73 tested, with 124 untested (and 73 were substituted with the as-traded close, all 73 of those reading not adjusted). All nine scanned series read adjusted. The adjustment is not the single dividend adjustment Yahoo or the custodian's distributions imply: it is 1.0 to 2.3 times as large (slope of log ratio on log implied factor), so no one constant or one factor undoes it.

## 1. The nine (AMCPX, AMRMX, CWGIX, WGIFX, CPXIX, FINFX, NEWFX, AWSHX, WMFFX)

These are the nine round-70 NOISY fund series (row ADVI_COTBKF-D2-W113-S1 and the round-70 detail: eight leaving TOO_FEW plus AMCPX, which was newly compared). All nine are one CUSIP each.

**Per-share distributions** come from the custodian's own dv and dvlt rows divided by the account's share balance just before the row (balance from the build's signs): 1,591 account-date rows, 8 dropped (balance not positive), 0 as outliers, 1,583 kept, in 229 events; 129 events rest on two or more accounts that agree within 0.12 percent, 100 on one account. The balance check: on the 55 dvlt rows that carry shares paid on, balance equals that Quantity on 55 of 55. The Yahoo cache has no dividend column (date, Close, Adj Close only); its dividend steps are read from Adj Close / Close. The custodian-implied factor reproduces Yahoo's own factor: correlation 0.9999 or better on 8 of 9 (FINFX 0.913), within 2 percent on 103 of 104 pairs. Full derivation is in `per_share_source`.

**Rule for a reading** (set after the first run; the first run showed the amplitude test below cannot be met): DIVIDEND_ADJUSTED when the observed ratio's daily steps (build close over the cached as-traded Close, steps over 0.3 percent) number at least 3, at least 90 percent sit within 2 trading days of a distribution (custodian row or Yahoo-implied step), none step down, and the pair ratio correlates with the custodian-implied factor at 0.90 or better. NOT_DIVIDEND_ADJUSTED would be a flat ratio or steps off distributions; otherwise UNDECIDED. **The face's example threshold (80 percent of pairs within 2 percent of the implied factor) is FAILED by all nine** (0 to 2 of 4 to 18 pairs): the observed ratio moves on every distribution but by more than the implied amount.

| ticker | pairs | within 2% of implied | corr | daily steps (on a distribution) | slope k | equals Close on | equals Adj Close x c on | reads |
|---|---|---|---|---|---|---|---|---|
| AMCPX | 4 | 0 | 0.999 | 9 (9) | 1.72 | 119 of 1,437 | 376 (c 0.885) | DIVIDEND_ADJUSTED |
| AMRMX | 11 | 0 | 0.976 | 22 (22) | 1.64 | 55 of 1,403 | 250 (c 0.890) | DIVIDEND_ADJUSTED |
| CWGIX | 13 | 0 | 0.973 | 19 (19) | 1.65 | 57 of 1,478 | 501 (c 0.848) | DIVIDEND_ADJUSTED |
| WGIFX | 13 | 2 | 0.994 | 21 (21) | 1.78 | 57 of 1,435 | 501 (c 0.848) | DIVIDEND_ADJUSTED |
| CPXIX | 18 | 0 | 1.000 | 65 (65) | 1.01 | 46 of 1,389 | 1,094 (c 1.031) | DIVIDEND_ADJUSTED |
| FINFX | 14 | 2 | 0.955 | 16 (16) | 2.27 | 55 of 1,483 | 128 (c 0.836) | DIVIDEND_ADJUSTED |
| NEWFX | 5 | 0 | 0.997 | 5 (5) | 1.85 | 115 of 1,478 | 501 (c 0.914) | DIVIDEND_ADJUSTED |
| AWSHX | 12 | 0 | 0.994 | 23 (23) | 1.76 | 55 of 1,478 | 128 (c 0.852) | DIVIDEND_ADJUSTED |
| WMFFX | 14 | 2 | 0.998 | 21 (21) | 1.85 | 55 of 1,329 | 128 (c 0.853) | DIVIDEND_ADJUSTED |

Every daily step is upward in time (no step down), all 201 sit on a distribution, 89 of them on a custodian distribution and 112 only on a Yahoo-implied one (the custodian holds the fund for part of the window only); of the 96 custodian distributions inside the nine's windows, 89 carry a step within 2 trading days (the 7 without: FINFX 5, CWGIX 1, NEWFX 1; not examined further). CPXIX is one clean single adjustment: its ratio over the implied factor is a constant 0.923 (the later monthly distributions the holdings do not cover). For the other eight the observed log adjustment is 1.6 to 2.3 times the implied one. Steps between pairs are in the JSON but are no test: every pair interval holds a distribution (base rate 100 percent).

## 2. The mechanism

The nine are NOT substituted. The as-traded basis (`as_traded_store`) replaces a ticker's store points with the cached Yahoo Close only for tickers the round-33/60 basis census (`price_basis_census.csv`, BASIS_CENSUS) classes `dividend_adjusted` or `mixed`. All nine are in the Yahoo cache with Close and Adj Close, but the census classed each `other: matches_neither` (store over Adj Close not constant, store over Close drifting across about 0.47 to 1.0): the rule demands store / Adj Close constant on 80 percent of days, which a series adjusted more than once cannot meet. A class outside the two substituted ones is left on the store, so after equals before on every date for all nine (0 dates changed). The store point is neither Close nor Adj Close times one constant: it equals Close on 3 to 8 percent of days (the last stretch, after the store's own pull) and Adj Close times one constant on at most 79 percent. All 72 fund series that read adjusted are census class `other`; the substituted 73 (60 `dividend_adjusted`, 13 `mixed`) all read not adjusted.

## 3. The whole table

| kind | series | substituted | left on store | tested | reads adjusted | reads not adjusted | untested | control: substituted read adjusted |
|---|---|---|---|---|---|---|---|---|
| Fund (Mutual Fund + Closed End) | 270 | 73 | 197 | 73 | **72** | 1 | **124** | 0 of 73 (73 not adjusted) |
| ETF | 276 | 234 | 42 | 4 | 2 | 2 | 38 | 0 of 222 tested (12 undecided) |
| Equity | 934 | 560 | 374 | 14 | 7 | 7 | 360 | 0 of 554 tested (6 undecided) |

Test (per left security, from the cache, no trade pairs): the build's yahoo_finance-labelled silver days against the cached Close and Adj Close; untested if no cache file, no Adj Close column, under 20 days, or Close equals Adj Close everywhere; not adjusted if the build equals Close within 0.1 percent on 80 percent of days; adjusted if on under 50 percent and the departure moves with Yahoo's own Adj/Close (log correlation 0.90 or better). The control passes: no substituted series reads adjusted.

Funds untested, 124: no cache file 120 (119 of the 124 are on the custodian-holdings store only, whose close is not a Yahoo series), cache marker with no bars 1, Close equal to Adj Close everywhere 2, undecided 1 (EGFIX). Their round-70 pair classes: AGREES 4, TOO_FEW 18, no pairs 102; none shows a shape, but that is not the cache test, and none is counted as not adjusted. Supporting the reading from the other side: of the 72 adjusted funds the round-70 classes are NOISY 28, CONSTANT_SCALE 3 (AMBFX, BALCX, OIEJX), TOO_FEW 15, no pairs 26, AGREES 0; the one left fund that reads not adjusted (ACTDX, census as_traded) has no pairs. Slope k over the 72: median 1.85, range 1.0 to 4.2; minimum build/Close ratio 0.03 to 0.88.

ETF and Equity: the 9 that read adjusted depart from Close by at most 1 percent (ratios 0.992 to 0.998): they pass the 0.1 percent test and are immaterial; they are in the CSV with their kind and not sized.

## 4. Reach (the 72 adjusted fund series)

48 of the 72 are held in the served window. Priced holding account-days resting on a close before the security's last distribution: 287,912 (of 289,855 priced holding account-days). **Measured account-days on them: 3,187** (distinct; 8,553 summed over securities; of 107,316 measured account-days served). On a distribution date of a held adjusted fund: **60** measured account-days (82 summed over securities). For ETF and Equity that read adjusted: 16,984 priced holding account-days, 327 measured, 0 on a distribution date. Direction: a close scaled down by each later distribution makes the return across a distribution date larger than the as-traded return, and the chain also credits the cash distribution as a flow, so those days count it twice; stated from the shape, no return was recomputed.

## Not established

See `not_established` in the JSON: the cause of the store's larger-than-Yahoo adjustment (its write history was not read); the 124 untested; ETF and Equity are counted but immaterial; no correction sized; kinds Fixed Income, Cash and Alternative were not tested; the cache is one pull dated 2026-10-09 and build rows after 2026-06-09 are outside the test; HLMEX (ratio to 0.03) is unexplained.
