# ETFS_RIVALS round 21 -- read R3 (ROUND_ANALYSIS.round20 @c9a9e27770): why 11 of 393 month strips disagree with their markers

`2.0.0_SA_COO~RV`, 2026-10-07 ~13:3xZ. Read-only (`round21/read_s59_cause.py`; record `round21/s59_cause.json`): the
round-19 real run's page and chart objects for day 2026-10-06, and live gold trade_schedule (G5: 276 partitions, 13,376
rows). Nothing written to S3. Row ETFS_RIVALS-Z-S59.

**Eleven strips, four causes** (the strip is drawn from gold buying_trend's month mark; the markers from G5 rows under the
chart key):

| # | Cause | Strips | Read |
|---|---|---|---|
| A | **The page day.** The strip counts a trade whose window ends ON the page day; the chart object's markers stop at the as-of day (the previous trading day) | 2: GQGU 857477103, IDVZ TKOMY | Each has one G5 `add` with window 2026-10-05 -> 2026-10-06 and a non-zero notional ($2.17m, $3.78m); the strip shows October, no marker ends in October |
| B | **A part first month.** The strip belongs to a 90-day section; its first cell is July, but the window starts 2026-07-08, and the marker is a trade ending 2026-07-01 | 3: CGIC AEM CN, BASG CARR, PCLG LLY | Each has one `trim` with window 2026-06-30 -> 2026-07-01. The strip is right for its window; the comparison counted the whole month. This is the part-month case of ruling R3 |
| C | **Zero-dollar trims drawn as markers.** G5 carries `trim` rows with `est_notional` -0.0; the trend counts a zero as no trade, the markers draw each one | 2: TXUE BTRW LN (Feb, Mar), SCHY VOD LN (Apr, May) | 9 and 7 G5 rows in those months, `trim` and `exit`, the trims at -0.0 and one row per security with a null notional |
| D | **No G5 row under the chart's key.** The trend shows a trade the fund made under another key that the trend's identity join folds into this one; the markers read G5 by the chart key alone | 4: BASG GOOG (May), BASG SPCX (June), GQGU IBKR (Oct), GQGU META (Oct) | 0 G5 rows under the key in the month. Which other key holds each trade was not traced; GQGU reports by CUSIP, so its two are candidates for the CUSIP-keyed rows |

**What follows from the cause** (the issuer's cut, round 22, inside the surfaces of cells RIV-tm-1 and RIV-co-1):
- A: the chart object's markers run through the page day, as the trend does (prices stay through the as-of day).
- C: a trade with a zero or null notional is not a marker.
- D: the markers for a key gather the fund's G5 rows by the same identity join the trend uses. To be confirmed at the
  cut by tracing the four to their other keys.
- B: nothing to repair in the data; the strip's first cell is marked as a part month (ruling R3).

Not established: whether these four causes also explain the 41 buying-section counts the CVO found off by one or two
trades at a window's edge (ADJUDICATION_v20); A and B are both edge effects, so they are candidates.
