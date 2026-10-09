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

## Comments 4-6 -- the CGIC audit (Andrew-direct ~05:2xZ), VERBATIM

> "Another thing I'm noticing is in the Audit section. What is happening here, with Tokyo Electron being "excluded" becuse
> its a cash management operation? is that saying it got a dividend? Also i want to know why we're seemingly marking trades
> way less than 20bps in delta. Go throught the CGIC audit report here and identify if anything here looks weird or is
> otherwise off pattern"

Read by 2.0.0_SA_COO~V1 from the pasted CGIC audit (latest report 2026-10-06, dataset revision 20261008T122342Z-6ea2fb54eece):

4. **The exclusion line reads as if it named the trade below it.** Window 2026-10-02 to 2026-10-05: "1 money-market line(s)
   traded: cash management ..." counts the fund's cash-sweep line, not Tokyo Electron and not a dividend; Tokyo Electron is
   the one trade shown (trim 164,600 -> 128,600). Work: the exclusion names the excluded line (security and amount) and sits
   apart from the trade table, so it cannot be read as the row under it.
5. **Trades far below 20 bps, and trades that are not trades.** No code applies Andrew's 20 bps tolerance (PRD v0.21 FWD-10
   SOURCE: "at a 20bps tolerance it's immediately clear who is discretionary and who is systematic"); 20 bps appears only as
   the smallest marker size (PRD :1096). In the pasted audit, 12 rows show an UNCHANGED share count with a nonzero inferred
   trade, all "flow adjusted": MediaTek 428,000 -> 428,000 (-1,442), Renault 277,771 -> 277,771 (-936 and -2,361), SMC 10,700
   -> 10,700 (-36), Jentech 23,000 -> 23,000 (-77), Taisei 56,900 -> 56,900 (-192), Aura 46,976 -> 46,976 (-158 and -399),
   Grifols 120,713 -> 120,713 (-407 and -1,026), Tokyo Electron 205,000 -> 205,000 (-1,743). The flow adjustment subtracts a
   holding's pro-rata share of creations/redemptions, so an untouched holding in a flow window becomes a trade. Inferred
   shares also differ from the actual change where shares did move (TSM -12,720 actual vs -13,927 inferred; Standard
   Chartered +143,405 vs +140,638; Tokyo Electron -40,400 vs -41,090). Work: an unchanged share count is never a trade; and
   a trade below the 20 bps tolerance (of fund weight) is not shown as a trade (kept in the audit as below tolerance).
6. **Trades on "repeat" days.** The day strip marks 10-01, 10-02, 10-05 and 10-06 "BBG repeat" (and 10-07 a gap), yet the
   10-02 -> 10-05 and 10-05 -> 10-06 windows carry trades (Tokyo Electron's trim; Vale's entry). A repeated report cannot
   produce a trade, so either the label or the windows are wrong. Work: read which, and make the two agree.

## Comment 7 -- the Period bar (Andrew-direct ~05:3xZ), VERBATIM

> "Also we do not need this "Period" component in the top of the page anymore because its handled where the actual ranking
> components are"

Work: remove the PERIOD row (30d / 90d / 365d with their dates) from the page header; the ranking panels' own period
controls stay.

## Comment 8 -- the Direction Verdict accounts (Andrew-direct ~05:3xZ), VERBATIM

> "if you look in the "Direction Verdict" more than half of the analyses lead with something like "These trades mostly
> support rather than contradict the longer record." That is not a bad phrase on its own, but when every single fund is
> saying the same thing, its not very interesting for the reader, and they may tune it out. We may need to give more token
> budget or more specific prompting for this function to delve deeper."

Work: the direction-verdict prompt (`ai_accounts.py`, `P_DIRECTION`) leads with what is specific to the fund (the names,
sizes and dates that decide the verdict), forbids the stock opening, and gets the token budget it needs; a check counts
opening sentences across the 13 funds and fails when more than a quarter share the same lead. This touches `ai_accounts.py`,
which round 28's aw-1 deploy carries: it waits until that deploy is read at the 13:00Z sweep.
