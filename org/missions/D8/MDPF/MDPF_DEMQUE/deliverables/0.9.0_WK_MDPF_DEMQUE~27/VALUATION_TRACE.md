# DQ-t-35 valuation trace (read-only), 2026-10-11, worker 0.9.0_WK_MDPF_DEMQUE~27

Machine form: `VALUATION_TRACE.json` beside this file. Denominator: FTHSX 4, PFORX 11, total 15 (positions snapshot `silver/positions/date=2026-06-23`). RPIFX has 0 held positions.

## The path (price file to client page), as read

1. Price store: `s3://opal-data-assets/yahoo/global/silver/price_history/cusip=<CUSIP>/prices.parquet` (+ `lock.json`). Written by `data/mdpf/scripts/demque/price_store.py` `write()`. FTHSX lock: LOCKED, claim `held`, yahoo_symbol FTHSX.
2. Lander: `data/mdpf/scripts/demque/land_cot.py` `plan()` and `apply_plan()` (L117-175, L257-274) write LOCKED as-traded closes to `opal-data-cot silver/historical_prices.parquet`. That object returns 404 now.
3. Ticker map: `opal-data-cot config/ticker_lookup.json` returns 404. `build_canonical_prices_v2.py` (L539-563) then warns and skips Tier 2 (Yahoo), using `YF_OVERRIDES` only. No FTHSX, PFORX or RPIFX entry exists in `ticker_overrides.py`.
4. Canonical table: `build_canonical_prices_v2.py` OUTPUT_KEY, `opal-data-cot silver/prices/canonical_prices.parquet` (present, 2026-10-09). It is keyed by asset_name.
5. Value artifact: `data/cot/scripts/gold/B_01.holdings_lots.py` gives market_value = units x latest price by asset_name (L29-30, L316-380). It overrides the price with the custodian RPS closing price where the account has RPS coverage (L636-661). The prefix `gold/timeseries/holdings_lots/` is empty in opal-data-cot. Dated objects exist in opal-data-bd.
6. Served: `data/cot/scripts/gold/D_04.client_portal_summary.py` writes client concentration (top-N by ticker, rest "Other") and advisor positions.json (top 25). The served advisor folder `cottonwood_capital_advisors` has no positions.json.
7. Route and firm: `/api/scoped/advisor-intelligence/platinum/clients/{hhId}/composition.json` and `detail.json` (`portal/src/api/endpoints/advisor-intelligence.ts` L489, L1156-1161). Firm: cottonwood. Read from source, not the deployed edge.

## Counts (15 position rows)

- Read by a page: **0 of 15** (FTHSX 0 of 4; PFORX 0 of 11).
- Reason: the custodian AccountNumbers match no `account_id` in `gold/dimensions/accounts_dimension_latest.parquet` (exact match, 1000 rows). The custodian-to-account crosswalk was not read. No served household or account artifact for these 15 was read.

## Candidates (existing resolvers; C-IDENTITY)

- **FTHSX 14064D865**: no candidate. `resolve_tickers.py` chains return nothing for the snapshot name. The stores carry FTHSX as the only ticker for this family. Control: served-file agreement 40.7 (n 627).
- **PFORX 693390882**: PFBPX 42.9 (n 513), PFONX 42.5 (n 506), PFUIX 0.0 (n 513). None reaches 90, so there is no proposed correction. The candidates came from a name-stem match over the two stores, not from a resolver output. PFBPX matches PFORX's served 42.9 with n 513, so a class swap does not move it.
- **RPIFX 77958B402**: no candidate. No name for it appears in the snapshot, the queue files, or any store's CUSIP field. Control: served-file agreement 39.2 (n 651).

Pulls: 3 of 6 (scratch pacer). Nothing was written to any store, queue, page or pacer.

## Not read

Served household or account JSON; the custodian-to-account crosswalk; the latest holdings_lots object; RPS coverage per account; the full price history; the deployed portal edge; current-symbol Yahoo closes (the served file is the control). No Bloomberg call.
