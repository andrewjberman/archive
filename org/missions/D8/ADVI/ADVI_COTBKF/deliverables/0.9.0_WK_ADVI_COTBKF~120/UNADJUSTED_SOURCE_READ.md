# UNADJUSTED_SOURCE_READ -- round 72 CB-bt-2 (0.9.0_WK_ADVI_COTBKF~120)

A read of data already on disk. Nothing was fetched: no network call, no vendor call, no census run. No code, test, config or manifest changed.
Record: `UNADJUSTED_SOURCE_READ.json` (same folder). Funds are named by ticker.

## Answer

**On the reinvestment row's own date, no source on disk reproduces the custodian's reinvestment price on the nine.** The nearest, the Yahoo cache's unadjusted `Close`, is within 0.5 percent on 45 of 93 dates (CPXIX 17 of 17; the other eight each under a majority) and within 2 percent on 88 of 93, median ratio 1.000, worst 0.962.

**Read one trading day earlier, the same `Close` reproduces it:** 88 of 93 within 0.5 percent and 93 of 93 within 2 percent, every one of the nine a majority (AMCPX 4/4, AMRMX 11/11, CWGIX 11/11, WGIFX 12/12, FINFX 12/12, NEWFX 3/3, AWSHX 11/11, WMFFX 12/12, CPXIX 12/17). The pattern follows Yahoo's own ex-date: for eight funds the custodian's `dvr` row is dated the trading day after the day Yahoo's Adj Close / Close ratio steps, and its price equals `Close` on the step day; for CPXIX the row is dated on the step day. Using the step day gives 93 of 93 within 0.5 percent. This is stated in `reproduces` as a QUALIFIED name, not as a same-date match. Why the dates differ was not read from any custodian field (see not established).

## Yardstick

1,121 `dvr` rows for the nine CUSIPs; price = Amount / Quantity, shares >= 0.05 (0 rows fell under it), pooled across accounts by median to one price per (fund, date). 221 (fund, date) cells over all history; **93** fall on or after 2020-06-29, the first day any source on disk holds for the nine (the issuer expected about 92). The other 128 (2013-05-01 to 2020-06-26) precede every source and are not compared. Spread across accounts inside a cell: median 0.005 percent, one cell over 0.5 percent (NEWFX 2020-12-18, 0.57 percent); 35 of the 93 cells rest on one row.

## Each source against the yardstick (same date; nine funds, 93 cells)

| source | funds | compared | within 0.5% | within 2% | median ratio | worst | previous trading day, within 0.5% |
|---|---|---|---|---|---|---|---|
| (a) Yahoo cache Close | 9 | 93 | 45 | 88 | 1.000 | 0.962 | 88 of 93 |
| (b) Yahoo cache Adj Close | 9 | 93 | 1 | 2 | 0.820 | 0.630 | 0 of 93 |
| (c) silver store, yahoo_finance rows | 9 | 92 | 4 | 6 | 0.719 | 0.470 | 6 of 92 |
| (c) silver store, linear_interpolation / transaction_observed | 0 | 0 | -- | -- | -- | -- | -- |
| (c) gold holdings store (bd_snapshot) | 0 | 0 | -- | -- | -- | -- | holds 5 of the nine only 2026-06-08 to 2026-10-06, after the last yardstick date |
| (c) bbg testpull, rivalfunds | 0 | 0 | -- | -- | -- | -- | no row for any of the nine |
| (c) bbg fund daily, portal return daily | 0 | 0 | -- | -- | -- | -- | stores hold 0 rows |
| (d) build's present close | 9 | 92 | 4 | 6 | 0.719 | 0.470 | 6 of 92 |

The baselines fail as expected: (d) equals the silver store's yahoo_finance rows (same 4 of 92), and Adj Close is too low (median 0.82). The "within one trading day" columns (previous and next day) are in the JSON per source and per fund; the next trading day gives 32 of 93 for (a).

## Why the build did not use it

The census (`price_basis_census.csv`, read, not re-run) classes a ticker by its store series: `as_traded` needs share_close >= 0.80; `dividend_adjusted` needs share_ra_c >= 0.80 and rc_spread > 0.005; `mixed` needs share_close or share_adj in [0.20, 0.80). `as_traded_store` substitutes only `dividend_adjusted` and `mixed`. All nine are `other: matches_neither`:

| fund | share_close | share_adj | share_ra_c | rc_spread | overlap days |
|---|---|---|---|---|---|
| AMCPX | 0.0828 | 0.0000 | 0.2617 | 0.7320 | 1437 |
| AMRMX | 0.0834 | 0.0000 | 0.1782 | 0.4832 | 1403 |
| CWGIX | 0.0792 | 0.0000 | 0.3390 | 0.5983 | 1478 |
| WGIFX | 0.0815 | 0.0000 | 0.3491 | 0.6107 | 1435 |
| CPXIX | 0.0331 | 0.0000 | 0.7876 | 0.2832 | 1389 |
| FINFX | 0.0782 | 0.0000 | 0.0863 | 0.8026 | 1483 |
| NEWFX | 0.0778 | 0.0778 | 0.3390 | 0.3662 | 1478 |
| AWSHX | 0.0778 | 0.0893 | 0.0866 | 0.8146 | 1478 |
| WMFFX | 0.0865 | 0.0993 | 0.0963 | 0.7968 | 1329 |

Each misses `as_traded` (share_close 0.03 to 0.09 against 0.80), `dividend_adjusted` (share_ra_c 0.09 to 0.35 against 0.80; CPXIX is nearest at 0.7876, 0.0124 short) and `mixed` (both shares under the 0.20 floor). The store is neither the traded close, nor a constant multiple of Adj Close, nor a partial blend; round 71 measured its adjustment as larger than Yahoo's own. A rule that substituted these would add class `other` (at least `matches_neither`) to SUBSTITUTE_CLASSES; this cell does not make it.

**What else is in `other`** (3,580 census tickers; 266 `other`, all 266 with a cache file holding a Close; 257 besides the nine): 239 `matches_neither` (the nine and 230 more; 228 of the 230 sit well under Close, median 0.74 -- the same shape; 64 are mutual funds held in the build, the rest of the 73 `other` fund series left on the store); 25 `no_dividend_window_store_off_close` (Close equals Adj Close, so no dividend; the store is off Close by a constant factor such as 5, 2, 0.1 -- CVNA, MNST, PRTS -- a split-type gap, where substituting could be wrong); 2 `overlap_lt_20` (one overlap day). Of the 257, 71 are securities in the build table (64 funds and 7 equities: AMCR and PYPL matches_neither, CVNA, MNST, PRTS and REZI split-type, MPX with one overlap day); 186 are not held.

## Coverage of the 197

Round 71's 270 / 73 / 197 reproduces (fund kinds on the custodian rows; 73 differ between r34 before and after). Of the 197 left on the store, **76 have an unadjusted Close in the Yahoo cache and 121 do not** (120 no cache file, 1 none-marker); by kind, 74 of 170 Mutual Fund and 2 of 27 Closed End. For the 76, the Close covers 96,421 of 139,626 held dates (69.06 percent; per series 68.5 to 72.1 percent), no series on every held date because held dates include interpolated non-trading days (71.7 percent of held dates are weekdays). So a read of held data reaches about two fifths of the 197 series, not all.

## Not established

See `not_established` in the JSON. In short: why the row date trails Yahoo's ex-date for eight funds (read only from Yahoo's step day, no custodian field); the same-date test is not met and the one-day readings were not the pre-stated comparison; 128 earlier cells and the gold holdings store are untested; the 76 cached Closes were not compared with any custodian price; the `other` counts rest on the committed census and the custodian Symbol link; the Yahoo cache is a file dated 2026-10-09, read as held.

UNADJUSTED-SOURCE-READ funds=9 dates=93 sources=12 reproduces=(a) Yahoo cache Close (unadjusted) -- QUALIFIED (previous trading day: 88 of 93; same date: 45 of 93) best=(a) Yahoo cache Close (unadjusted) coverage_with=76 coverage_without=121
