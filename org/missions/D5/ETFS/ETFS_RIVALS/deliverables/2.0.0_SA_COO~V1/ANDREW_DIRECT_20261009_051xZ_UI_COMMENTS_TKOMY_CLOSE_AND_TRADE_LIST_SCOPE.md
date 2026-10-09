# Andrew-direct 2026-10-09 ~05:1xZ at the 2.0.0_SA_COO~V1 terminal -- rivalfunds UI comments 1 and 2

Andrew opened https://mcp.opalinvest.dev/rivalfunds (page date 2026-10-08) to "make some random ui comments you can go
pursue in the interim". Recorded verbatim; each becomes round-29 work.

## Comment 1 -- VERBATIM

> "First thing i want to know is why are we showing Tokio Marine as $3 when its a ~$50 stock"

Screenshot: the IDVZ security dialog for Tokio Marine, 30d, headline "3.33 USD 2026-10-07 market close"; the curve sits at
about 50 from 7 Sep and drops to 3.33 on the last point.

### What was measured (2.0.0_SA_COO~V1, 05:2xZ)

- Served chart object `s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-08/charts/IDVZ.json`, security
  `TKOMY_US_Equity`: `[2026-10-05, 49.59, m]`, `[2026-10-06, 50.5, m]`, `[2026-10-07, 3.33, m]` (`m` = Bloomberg close).
  The page draws exactly what is stored.
- Gold security_market (`rivalfunds/etfs/gold/security_market/date=<D>/`), source `blp_client.reference_data`:

  | object | TKOMY US Equity (USD) | 8766 JP Equity (JPY) |
  |---|---|---|
  | date=2026-10-05 `market-20261006T123301Z` | 49.59 | 522.30 |
  | date=2026-10-06 `market-20261007T110920Z` | 50.50 | 516.00 |
  | date=2026-10-07 `market-20261008T122034Z` | **3.33** | 518.10 |

- The 10-07 object is the 12:20Z recovery re-pull of 2026-10-08 (after the signed-out 11:00Z run, row Z-S76). The daily
  leg reads `reference_data` PX_LAST at pull time, not a historical close for the date.
- **CAUSE (Andrew-direct, same session, VERBATIM):** "Ah I see what happened, they literaly had a corporate action on
  October 7 for a 15:1 stock split" -- and: "There is an update you can manage right there, adjusted history based on
  corporate action." 50.50 / 15 = 3.37: the 10-07 close of 3.33 is CORRECT post-split. The defect is that the chart (and
  any reader of the stored closes) draws pre-split history beside a post-split close, unadjusted. This seat's first
  reading (a yen price converted to USD) was WRONG and is withdrawn.

### Work (round 29)

1. **Split-adjusted price history:** every price series the page draws (the dialog's curve, the holding-implied points,
   trade-marker prices, and any period return read from closes) is adjusted for splits and other share-count corporate
   actions, from the corporate actions the enrichment leg already stores, so a split leaves a continuous curve. The
   adjustment factor and its source action are recorded with the series; the dialog states when a series is adjusted.
2. **Proof on this case:** TKOMY's 30d curve on the 2026-10-08 page reads about 3.3 to 3.5 across the window with no
   step at 2026-10-07; the factor 15 is read from a stored corporate-action row, never typed.
3. **Dramatic move -> look it up and adjust (Andrew-direct, VERBATIM):** "If you see a very dramatic action like that,
   there should be a google search for corporate action and an automatic refactoring of historical prices by the split
   multiple in the event of a split or merger or etcv". So: a close that moves past 3x or below 1/3 of the prior stored
   close triggers a web search for that security's corporate action on that date (egress is open except Bloomberg, law
   4d77a9c3ea). A split, reverse split or merger found with its ratio becomes a stored corporate-action row carrying its
   source URL and `claim` (`inferred` from search, never `measured`), and history is rescaled by that multiple. Found
   nothing: the point is a gap with its reason and a FAIL line, never drawn silently.
4. **Measured gap behind item 3:** the stored corporate actions hold NO TKOMY row: gold corporate_actions date=2026-10-06
   and date=2026-10-07 (`actions-2026100{6,7}-4b871bd81ab4`, 160 rows each, the same revision hash) carry 0 TKOMY or 8766
   rows, and no date=2026-10-08 object exists. So the split is absent from the store the adjustment would read.

## Comment 2 -- VERBATIM

> "Another thing, in the popup modal, "Trades in the Last 365 Days" was not fucking asked for if you're looking at the 30d
> Toggle. That should at the very least be behind a dropdown, and it should be scoped for the toggle value, not just
> arbitrarily 365d."

### Work (round 29)

The dialog's trade list follows the selected window (30d / 90d / 365d), its heading names that window, and it sits
collapsed behind a disclosure control that is closed by default. It is written from the chart object's markers, as
round 18 (RIV-tl-1) wrote it.
