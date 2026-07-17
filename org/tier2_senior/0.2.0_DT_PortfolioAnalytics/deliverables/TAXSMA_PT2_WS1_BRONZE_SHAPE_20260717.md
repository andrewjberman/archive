# WS-1 Bronze Output Shape (OPAL_TAXSMA_PT2) -- for WS-2 silver (DS)

**Producer:** `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py`
**Author:** 0.2.0_DT_PortfolioAnalytics · 2026-07-17 · DRY-built + validated (see `dry_test.py`).
**Status:** DRY-COMPLETE. The live pull is gated on Andrew's vendor-egress word (`DRY_RUN=1` blocks all
network calls until flipped). This documents the bronze shape so WS-2 (silver) can be cut in parallel.

## >> CONTRACT PROPERTY (load-bearing, COO-ratified 220432Z): BD REVISES CLOSED-PERIOD FIGURES <<
BD numbers are **AS-OF-DATED, not immutable**. Live verify 2026-07-17: for the CLOSED Q2 window, the
realized figure was stable to the cent (realizedShortTerm -61,933.73) but the valuation-date-sensitive
fields drifted vs the 07-15 HAR -- netGains -86,790.78 (was -87,061.19, ~0.03pct), TWR -0.081799 (was
-0.082053), unrealizedTotal 822,456.41 (was 822,189.90). This is BD mark-to-market/revision (Andrew's
pre-stated "I don't know the revisions" concern made concrete), NOT a mechanism change. **WS-2/WS-3
implication:** treat every BD number as as-of-dated; carry the pull_asof; a re-pull of a quarter CAN change
"closed" numbers -- so silver must key on (schwab_account, period-window, **pull_asof**), never assume a
quarter's numbers are frozen.

## Bronze keys (monolith grammar, Rule 17a RAW byte-for-byte)

One raw JSON object per (feed, account, report-window), **partitioned by PULL DATE** (COO cond c -- so a
re-pull on a later day never silently overwrites a prior valuation snapshot):
```
blackdiamond/49f/bronze/reporting_performance/{pull_date}/reporting_performance_{bdAccountId}_{q_end}.json
blackdiamond/49f/bronze/reporting_costbasis/{pull_date}/reporting_costbasis_{bdAccountId}_{q_end}.json
blackdiamond/49f/bronze/reporting_allocation/{pull_date}/reporting_allocation_{bdAccountId}_{q_end}.json
```
`{pull_date}` = ingestion date (e.g. `2026-07-17`); `{q_end}` = report-window end (e.g. `2026-06-30`);
`{bdAccountId}` = BD INTERNAL numeric account id (e.g. 22596361 = Chiles -- NOTE: distinct from the xref's
`bd_account_id` which is the EXTERNAL `z08...` form; discovery must resolve the internal id). S3 object
Metadata stamps `pull-asof`, `report-window-end`, `bd-account-id`. Bodies are the BD responses UNMODIFIED --
they carry client PII (accountName); PII is dropped at the silver->gold boundary (WS-3), NEVER bronze/silver.

## Response structure per feed (the fields WS-2 will parse; validated vs the Chiles HAR, reconciles to cent)

**reporting_performance** (`performancePeriod`): `levels[0].dateRangePoints[]` -- one per window
(Custom quarter, trailing CalendarYears, Since Inception). Per window:
`beginningMarketValue, endingMarketValue, netGains, netAdditions, fees, income,
timeWeightedReturns.return (TWR), moneyWeightedReturns.return (MWR), benchmarks[].{benchmarkId,return,difference}`.
Also `levels[0].accountInfo.{accountId,accountName,accountNumber,externalId}` + `asOfDatePoints.marketValue`.

**reporting_costbasis** (`costBasis`): `levels[0].metrics` --
`realizedShortTerm(Gain/Loss), realizedLongTerm(Gain/Loss), realizedTotal,
unrealizedShortTerm(Gain/Loss), unrealizedLongTerm(Gain/Loss), unrealizedTotal,
marketValue, accrual, unrealizedCostBasis, realizedCostBasis, proceeds`. Nested `levels[]` = Class/Segment/Asset.

**reporting_allocation** (`allocation`): `levels[0].allocationOfTotal/allocationOfParent.{beginningMarketValue,...}`
+ nested `levels[]` by Class/Segment/Asset -> sector + holding weights + market values (top-N by weight).

## Account key bridge (for WS-2/WS-3)
The BD responses key by BD `accountId`/`externalId`. Alyssa keys off the **Schwab account number** -- bridge
via `blackdiamond/49f/silver/dim_account_xref` (BD accountId <-> schwab_account_id). Chiles: BD 22596361 /
ext z0822596361 <-> Schwab 0027265115.

## For WS-2 silver `fact_taxsma_report`
Parse each feed's response to a complete `fact_` table (dedup + dtype ONLY, Rule 17 -- keep ALL fields incl.
accountName), one logical row-set per (schwab_account, period-window). The gold `dim_taxsma_report` (WS-3) then
drops PII + selects the report fields, per-account, anonymized -- the single-prefix read surface for Alyssa.
