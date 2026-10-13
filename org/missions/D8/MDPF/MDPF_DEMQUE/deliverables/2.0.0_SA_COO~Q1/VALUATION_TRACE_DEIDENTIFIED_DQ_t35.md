# DQ-t-35 valuation trace, DE-IDENTIFIED: the chain from the price file to the client page for FTHSX, PFORX and RPIFX (2.0.0_SA_COO~Q1, 2026-10-13)

Source: worker `0.9.0_WK_MDPF_DEMQUE~27`'s `VALUATION_TRACE.json` (as of 2026-10-11, revision re-open 2026-10-11: production bucket bound, bridge read, per-position production reads), which carried client account numbers and was moved out of the repo under the CTO containment ruling (see `MOVED_ACCOUNT_DATA.md`, sha256 recorded there). **This file keeps the chain, the counts and the keys; every account number is removed (a removed token reads `<account id removed>`).** For the CVO's L9 grade of `DQ9-t35-AC2` (judgment).

**Denominator:** 15 holding accounts traced: FTHSX 4, PFORX 11. Positions read by a served client page: **0 of 15**.

## The chain, hop by hop

| hop | what | key | what was read |
|---|---|---|---|
| 1 | per-CUSIP price store | opal-data-assets yahoo/global/silver/price_history/cusip=<CUSIP>/prices.parquet, lock.json | FTHSX prices.parquet 50116 B (2026-10-08); served-file controls read for all three CUSIPs; LOCKED, claim held |
| 2 | lander target silver/historical_prices.parquet (opal-data-cot) |  | HeadObject 404 (production bucket); land_cot.py apply_plan writes this key (L257-274) |
| 3 | ticker map config/ticker_lookup.json (opal-data-cot) |  | GetObject 404; build_canonical_prices_v2.py _load_tier2 falls back to YF_OVERRIDES only (L539-563); no FTHSX, PFORX or RPIFX entry in ticker_overrides.py |
| 4 | silver/prices/canonical_prices.parquet (opal-data-cot, name-keyed, ticker NaN for these names) |  | read: 11,289,398 rows, last date 2026-06-09. For the five FTHSX/PFORX-family asset names: sources only linear_interpolation (1196-2052 rows each) and transaction_observed; no yahoo_finance row. Last price FTHSX-family 49.58 / 45.64 (2026-06-09); PFORX-family 9.95 / 9.68 / 9.73. |
| 5 | value artifact gold/canonical/holdings/2026-10-09.parquet (B_00, opal-data-cot) |  | 21,299 rows. FTHSX 188 accounts (price 57.57-57.67, source bd_snapshot); PFORX 334 accounts (price 9.45-9.46, bd_snapshot). B_00 price = BD snapshot market value / units (B_00 L171-173), so these rows are not priced from the Yahoo or canonical path. gold/timeseries/holdings_lots/ not produced in production. |
| 6 | served household composition | opal-data-cot platinum/clients/<rel>/composition.json (top 9 holdings + other) | composition read for the three unapplied candidate households only: none names FTHSX, PFORX or RPIFX in its top 9; detail.json NoSuchKey |
| 7 | portal route and firm (firm cottonwood) | /api/scoped/advisor-intelligence/platinum/clients/{hhId}/composition.json (and detail.json) | portal/src/api/endpoints/advisor-intelligence.ts L489, L1156-1161 (source read) |

## Where the chain from the price file to a page breaks

- **The Yahoo price file never reaches the client page for these names.** Hop 1 (the per-CUSIP price store) is locked and correct; hop 2 (the lander target `silver/historical_prices.parquet` in the production bucket) does not exist (404); hop 3 (the ticker map) does not exist (404); hop 4 (canonical prices) carries no Yahoo row for the FTHSX/PFORX family; hop 5 (the value artifact) prices these positions from the Black Diamond snapshot (market value over units), not from Yahoo.
- **So the page value comes from the custodian's own mark, and the Yahoo price is not on the path.** None of the three names appears in the top 9 holdings of the three candidate households whose composition was read (hop 6).

## The bridge (custodian numbers to current accounts)

- Crosswalk `s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.parquet`; account links `s3://opal-data-assets/commonwealth/cottonwood/silver/account_links/date=2026-06-23/account_links.parquet`.
- Result: all 11 PFORX-holding custodian numbers and the 4 FTHSX-holding numbers in the 15 rows are `NOT_MATCHED` in the crosswalk (two `AWAITING_PERSON` with a near match score of 0.765; the rest `NO_CURRENT_ACCOUNT_HOLDS_POSITIONS`).

## Production binding

- **bucket:** opal-data-cot
- **how:** infra/aws/terraform/cot-pipeline/ssm.tf: SSM document opal-cot-gold-run (line ~304) exports BD_S3_BUCKET=opal-data-cot and FIRM_ID=cottonwood (line ~331); the COT silver merge document exports the same (line ~233); data/cot/scripts/gold/lib/config.py default is also opal-data-cot
- **firm_bucket_checked:** opal-data-cottonwood: HeadObject 404 for silver/historical_prices.parquet, config/ticker_lookup.json, silver/prices/canonical_prices.parquet; gold/timeseries/holdings_lots/ no objects
- **production_chain_excludes:** B_01 holdings_lots, B_01b, B_02, B_03 (ssm.tf comment line ~294; run_gold list line ~375-404)
