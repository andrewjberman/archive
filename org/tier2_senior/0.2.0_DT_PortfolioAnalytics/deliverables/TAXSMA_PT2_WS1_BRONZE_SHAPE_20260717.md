# WS-1 Bronze Output Shape (OPAL_TAXSMA_PT2) -- for WS-2 silver (DS)

**Producer:** `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py`
**Author:** 0.2.0_DT_PortfolioAnalytics · 2026-07-17 · DRY-built + validated (see `dry_test.py`).
**Status:** DRY-COMPLETE. The live pull is gated on Andrew's vendor-egress word (`DRY_RUN=1` blocks all
network calls until flipped). This documents the bronze shape so WS-2 (silver) can be cut in parallel.

## Bronze keys (monolith grammar, Rule 17a RAW byte-for-byte)

One raw JSON object per (feed, account, as_of). Three feeds:
```
blackdiamond/49f/bronze/reporting_performance/{as_of}/reporting_performance_{bdAccountId}_{as_of}.json
blackdiamond/49f/bronze/reporting_costbasis/{as_of}/reporting_costbasis_{bdAccountId}_{as_of}.json
blackdiamond/49f/bronze/reporting_allocation/{as_of}/reporting_allocation_{bdAccountId}_{as_of}.json
```
`{as_of}` = quarter-end (e.g. `2026-06-30`); `{bdAccountId}` = BD account id (e.g. 22596361 = Chiles).
Bodies are the BD `portfolioreporting/api/*` responses UNMODIFIED -- they carry client PII (accountName);
PII is dropped at the silver->gold boundary (WS-3), NEVER in bronze/silver.

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
