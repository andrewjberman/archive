# VBTLX read date by date -- round 75 CB-bw-4 (0.9.0_WK_ADVI_COTBKF~135)

Nothing was fetched. The round-74 file for VBTLX (1,579 rows) was read as it sits, beside the build's close (r34 after and before, which are identical on every date), the custodian transaction cache, the price-store caches and the round-74 serve files.

**Shared dates 1,482; off dates (|ratio - 1| > 0.02) 144 in 20 stretches.** Lowest ratio 0.1823 on 2022-08-11.

| Depth | Stretches | Dates | Ratio |
|---|---|---|---|
| deep (min below 0.9) | 3: 2022-08-01 to 08-30, 2022-10-06 to 10-28, 2024-04-02 to 04-17 | 51 | 0.1823 to 0.9657 |
| moderate (0.91 to 0.98) | 4: 2023-04-03, 2023-07-03, 2023-08-01, 2024-06-11 starts | 59 | 0.9134 to 0.9795 |
| marginal (within 3.3 percent) | 13 | 34 | 0.9756 to 1.0326 |

Every off stretch is a straight-line ramp, not a constant: the build's price falls linearly from an ordinary stored price to one stored price far below the fund (1.8232 on 2022-08-11, 5.2299 on 2022-10-12, 5.2500 on 2024-04-04; milder 8.9109, 8.7044, 8.6335, 9.0721 in 2023-2024) and rises linearly to the next ordinary one. 135 of the 144 off dates are interpolated, 9 are stored observed prices. All in one store: cottonwood-silver-canonical-prices, kind ticker, key VBTLX.

**Which side is wrong: not established.** No custodian trade or reinvestment price lies in any of the 20 stretches (0 of 20). The only custodian prices in the shared window are 3 dates in 2025 (9.5600, 9.6801, 9.5978), 56 or more days from a stretch; there the custodian equals the fetched close to 0.03 percent and the build is 0.5 to 1.3 percent below it.

**Behind the security.** One CUSIP, one symbol (VBTLX), one description (Admiral Shares), 909 custodian rows 2016-07-07 to 2025-07-31, no hand-over; no other CUSIP carries the ticker. Sibling class by ticker: BND (ETF Shares), own CUSIP, 7.5 to 7.6 times the fetched VBTLX close on 1,478 shared dates, so the 0.18 level is not a class price. No other store holds a row for VBTLX.

**Cause: not_named.** Not a unit (six different anchor ratios), not a class price, not a class change. A wrong symbol behind the key cannot be shown or excluded: the 120 stored observed anchors in 2020-2026 have no custodian row behind them (the cache holds no VBTLX row 2018-2024). To settle it, read the price builder's input row for each of the six low-anchor dates.

**Rest of the series.** Away from the off stretches the build's close is the fetched unadjusted close (observed anchors: median difference 0.009 percent, 89 percent within 0.5 percent), so `looks unadjusted` holds for the rest.

**What rests on the off dates: nothing.** 0 priced holding account-days and 0 measured account-days. The fund's 38 priced account-days are all 2025-05-29 to 2025-07-23, off none. Round 70 class: AGREES (on its 2025 custodian prints, outside every stretch). Excluded from counts: true.
