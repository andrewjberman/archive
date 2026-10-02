# Account 0027265115: the 1,498.38 USD flow residual, from landed data only (TO-DB-b-6)

**Conclusion.** The residual is not one leg and it is not on 2026-07-07. It is the exact whole-window net (2026-03-16 to 2026-08-28) of Black Diamond `netAdditions` 1,044,598.9077 minus Opal gold `external_flow` 1,043,100.5277 = 1,498.3800. It is the sum of four offsetting classes, so no single leg equals it. `leg_named` is `OTHER`.

**The issuer's inference is refuted.** The fee day 2026-07-07 matches to the cent: Opal `-2,423.40` (Schwab `TPFEE`, "TO ADVISOR") equals the Black Diamond fee `2,423.40` (account level, 07-01 to 08-28). It contributes zero. The 925.02 USD "fee leg" does not exist in the data.

| Class (vendor minus Opal) | USD | Opal class / vendor class |
|---|---|---|
| Eight in-kind transfers valued differently (HD -7,374.99, ACN -1,822.50, MMM -194.95, GOOG +1,304.25, NFLX +656.00, GOOGL +104.17, BRKB +73.00, META +2.86) | -7,252.16 | EXTERNAL both sides, different price |
| Margin interest: Schwab INTR 13,897.44 less S1INA rebates 3,173.13 | +10,724.31 | INTERNAL at Opal, EXTERNAL at vendor |
| 15 assets with a trade or merger difference over 100 (CHTR, LBRD, EA, CWEN, FDX, ...) | -3,780.14 | INTERNAL at Opal, net addition at vendor |
| 517 other assets, each under 100 | +502.66 | not attributable per row |
| Vendor CASH asset against Opal's two cash flows | +1,303.71 | derived |
| **Net** | **+1,498.38** | |

**Firmness.** MEASURED: both totals, the eight in-kind valuations, the margin-interest amount (to the cent from Schwab rows), the fee match. INFERRED: the per-asset trade comparison (asset netAdditions taken as buys minus sells, matched to Schwab `TRADE` rows by ticker) and therefore the last three rows; the CASH row is a derived remainder, not an itemised row. Black Diamond's own prices are not landed, so the in-kind difference cannot be traced below the asset.

**For the CTO's next ruling.** The largest single class is margin interest, which Opal treats as internal and the vendor as an external addition; the in-kind valuation difference is nearly as large and opposite in sign. Tolerating or closing the residual is a ruling on netting, not on a leg. Per-day detail would need the Black Diamond transactions or activity family, which is not landed (only `reporting_performance`, allocation, costbasis, fees and roster are).

Vendor calls: 0. Record: `FLOW_RESIDUAL_0027265115_R2.json` (net leg first, components flagged `is_residual` false).
