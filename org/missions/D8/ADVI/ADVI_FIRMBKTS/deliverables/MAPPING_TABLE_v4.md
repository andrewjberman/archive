# MAPPING TABLE v4 -- ADVI_FIRMBKTS round 4, cell FB-g-3 (rulings S2-S11)

Supersedes mapping_v3.json. Census listed_at 2026-10-09T20:36:32Z. Live listing for this table at 2026-10-11T12:28:17Z (LIST calls only).
Classes: 444 census classes (444 in census buckets, all 444 accounted: placed directly or re-gridded).
Census objects: 238,861. Live objects of the 29 re-grid parents at the listing: 41,028.

FAULT before: 84 (mapping_v3.json rows; the check's before reads mapping_v2.json, which carries 89)
FAULT after: 71

## Dispositions (rows and objects)

| disposition | rows | objects |
|---|---:|---:|
| MOVE | 363 | 33,368 |
| HOME | 2,918 | 27,307 |
| RETIRE | 93 | 42,247 |
| DECISION | 2 | 0 |
| FAULT | 71 | 11,840 |

## Ruling counts (one example each in the ruling line)

- S2: 41. overlap-0 merges name a destination table: 34 merge entries carry destination_table = table; the 7 overlap-0 FAULT rows name no table in the row or the groups, so they stay FAULT citing S2
- S3: 2. round-1 placed rows stay as placed: the 2 cot positions_cube rows return to their round-1 MOVE placement; the silver/_silver_complete/ and gold/meta/pull-complete.json placements are untouched (no kind field)
- S5: 4. state families named on 4 placed marker rows (cot bronze/, bronze/orion-api/, gold/eclipse/, silver/eclipse/); their v3 address and pattern are kept (S5 difference control)
- S6: 86. 86 QA-named rows judged by writer: production 75, qa-tool 6, unresolved 5 (qa-scratch/ x4 and bronze/orion-api/probe/ x1: no writer found in the pipeline code)
- S7: 0. 0 rows: no row can carry the *_SKIP.json tail without a second row at the same bronze/orion-api/ key; the 1,142 skip objects stay in their date-partition data children (surprise row filed)
- S8: 2. 2 rows: bronze/eclipse/ (writer pull_eclipse_portfolios.py) and bronze/eclipse_qa/ (writer inf-api-eclipse lambda) become state/bronze_complete markers partitioned by writing class
- S9: 21. 5 regrid parents re-listed with a moving count, 12 child counts re-derived, 3 new partition or folder rows, 1 excluded_markers re-derived
- S10: 1. 1 row: opal-data-bd gold/clients/ re-written at class grain (no partition token)
- S11: 10. 10 rows: the forwardfill _complete/ groups of bd and cot become state/bronze_complete markers partitioned by writing class (writer cot_bronze_ingest.py); marker_match is .json (the group's only tail)

## Re-grids (census, live, difference, children sum)

| bucket | parent | census | listed (live) | difference | children sum | moving |
|---|---|---:|---:|---:|---:|---|
| opal-data-bd | backfill_v2/ | 292 | 292 | 0 | 292 | no |
| opal-data-bd | bronze/ | 212 | 215 | 3 | 215 | no |
| opal-data-bd | forwardfill_v2/allocations/ | 146 | 148 | 2 | 148 | no |
| opal-data-bd | forwardfill_v2/realized/ | 245 | 249 | 4 | 249 | no |
| opal-data-bd | forwardfill_v2/transactions/ | 306 | 310 | 4 | 310 | no |
| opal-data-bd | forwardfill_v2/unrealized/ | 89 | 91 | 2 | 91 | no |
| opal-data-bd | gold/cohorts/ | 2 | 2 | 0 | 2 | no |
| opal-data-bd | gold/filters/ | 2 | 2 | 0 | 2 | no |
| opal-data-bd | gold/nna/ | 4 | 4 | 0 | 4 | no |
| opal-data-bd | gold/snapshots/ | 7 | 7 | 0 | 7 | no |
| opal-data-bd | gold/summary/ | 2 | 2 | 0 | 2 | no |
| opal-data-bd | gold/timeseries/ | 2,640 | 2,644 | 4 | 2,644 | no |
| opal-data-bd | logs/ | 9,107 | 9,239 | 132 | 9,239 | no |
| opal-data-bd | scripts/ | 154 | 154 | 0 | 154 | no |
| opal-data-bd | silver/transactions_enriched/ | 519 | 519 | 0 | 519 | no |
| opal-data-inf | gold/timeseries/ | 2 | 2 | 0 | 2 | no |
| opal-data-inf | platinum/clients/ | 4,199 | 4,202 | 3 | 4,202 | no |
| opal-data-cot | forwardfill_v2/account_attributes/ | 82 | 84 | 2 | 84 | no |
| opal-data-cot | forwardfill_v2/allocations/ | 199 | 201 | 2 | 201 | no |
| opal-data-cot | forwardfill_v2/holdings/ | 168 | 170 | 2 | 170 | no |
| opal-data-cot | forwardfill_v2/realized/ | 204 | 208 | 4 | 208 | yes: live count 206 (v3 listing 2026-10-11T06:30:42Z: 206) -> 208 (listing 2026-10-11T12:28:13Z |
| opal-data-cot | forwardfill_v2/transactions/ | 207 | 211 | 4 | 211 | yes: live count 209 (v3 listing 2026-10-11T06:30:42Z: 209) -> 211 (listing 2026-10-11T12:28:13Z |
| opal-data-cot | forwardfill_v2/unrealized/ | 199 | 201 | 2 | 201 | no |
| opal-data-cot | silver/ | 803 | 812 | 9 | 812 | yes: live count 809 (v3 listing 2026-10-11T06:30:42Z: 809) -> 812 (listing 2026-10-11T12:28:13Z |
| opal-data-inf | bronze/eclipse/ | 1,785 | 1,798 | 13 | 1,798 | no |
| opal-data-inf | bronze/eclipse_qa/ | 858 | 884 | 26 | 884 | yes: live count 871 (v3 listing 2026-10-11T06:56:05Z: 871) -> 884 (listing 2026-10-11T12:28:13Z |
| opal-data-inf | bronze/orion-api/ | 17,151 | 17,188 | 37 | 17,188 | yes: live count 17170 (v3 listing 2026-10-11T06:56:06Z: 17170) -> 17188 (listing 2026-10-11T12: |
| opal-data-inf | gold/eclipse/ | 525 | 529 | 4 | 529 | no |
| opal-data-inf | silver/eclipse/ | 655 | 660 | 5 | 660 | no |

## Remaining FAULT classes by reason (owner 1.0.0_SA_CTO~DELL1 on every row)

- 1 x RHN: forwardfill root file whose name is not TXN_*.xlsx
  - opal-data-bd backfill_v2/
- 7 x destination-key overlap N of N keys with the group
  - opal-data-bd bronze/; opal-data-bd gold/advisor_rolling_flows.json; opal-data-bd gold/architect_leaderboard.json; opal-data-bd gold/perf_report.json; opal-data-bd gold/pipeline-complete.json; opal-data-cot gold/firm_composition.json; opal-data-cot silver/
- 12 x market-price silver: {vendor} is not derivable from the key and is not the bucket's feed vendor
  - opal-data-bd canonical/silver/dim_account/; opal-data-bd canonical/silver/fact_position/; opal-data-bd silver/historical_dividends.parquet; opal-data-bd silver/historical_prices.parquet; opal-data-bd silver/historical_prices_20260213.parquet; opal-data-bd silver/historical_prices_final.parquet; opal-data-bd silver/interpolated_prices.parquet; opal-data-bd silver/interpolated_prices_summary.json; opal-data-bd silver/prices/; opal-data-inf silver/historical_prices.parquet; opal-data-inf silver/prices/; opal-data-cot silver/prices/
- 2 x destination-key overlap N of N keys with gold/timeseries/account_performance.parquet
  - opal-data-bd gold/account_performance.parquet; opal-data-cot gold/account_performance.parquet
- 1 x destination-key overlap N of N keys with gold/timeseries/account_quality_tiers.parquet
  - opal-data-bd gold/account_quality_tiers.parquet
- 1 x destination-key overlap N of N keys with platinum/advisors/
  - opal-data-bd gold/advisors/
- 2 x destination-key overlap N of N keys with gold/timeseries/client_performance.parquet
  - opal-data-bd gold/client_performance.parquet; opal-data-cot gold/client_performance.parquet
- 8 x destination-key overlap N of N keys with gold/artifacts/
  - opal-data-bd gold/clients_tab.json; opal-data-bd gold/firm_composition.json; opal-data-bd gold/firm_mix_views.json; opal-data-bd gold/firm_mix_views_daily.json; opal-data-bd gold/implementor_leaderboard.json; opal-data-bd gold/timeseries_chart.json; opal-data-cot gold/firm_mix_views.json; opal-data-cot gold/firm_mix_views_daily.json
- 7 x no repair rule places it
  - opal-data-bd gold/config/; opal-data-bd schwab/silver/rps/; opal-data-inf gold/canonical/; opal-data-inf gold/classification/; opal-data-inf gold/dimensions/_aor_exercise/aor_attribution_comparison/; opal-data-inf gold/dimensions/aor_ledger/events/; opal-data-inf gold/dimensions/dim_inf_advisor_office.csv
- 1 x RGN dir whose object is not a date-named parquet
  - opal-data-bd gold/consolidated/
- 1 x destination-key overlap N of N keys with gold/timeseries/synthetic_positions_index.parquet
  - opal-data-bd gold/synthetic_positions_index.parquet
- 2 x destination-key overlap N of N keys with gold/account_performance.parquet
  - opal-data-bd gold/timeseries/account_performance.parquet; opal-data-cot gold/timeseries/account_performance.parquet
- 1 x destination-key overlap N of N keys with gold/account_quality_tiers.parquet
  - opal-data-bd gold/timeseries/account_quality_tiers.parquet
- 2 x destination-key overlap N of N keys with gold/client_performance.parquet
  - opal-data-bd gold/timeseries/client_performance.parquet; opal-data-cot gold/timeseries/client_performance.parquet
- 1 x destination-key overlap N of N keys with gold/synthetic_positions_index.parquet
  - opal-data-bd gold/timeseries/synthetic_positions_index.parquet
- 3 x Lambda deployment artifacts: RN is not applied to them (PRD CONTRACTS)
  - opal-data-bd lambda-deploy/; opal-data-bd lambda-layers/; opal-data-bd lambda-packages/
- 1 x code: scripts are not data
  - opal-data-bd scripts/
- 4 x silver/bronze root file, no data directory
  - opal-data-bd silver/aua_validation_log.parquet; opal-data-cot silver/cot_allocations.parquet; opal-data-cot silver/cot_holdings.parquet; opal-data-cot silver/cot_transactions.parquet
- 1 x a live credential: moving it breaks the chain that refreshes it (FWD-N's class)
  - opal-data-bd smartx/jwt/
- 3 x leading-slash key
  - opal-data-inf /advisors/; opal-data-inf /clients/; opal-data-inf /firm/
- 2 x runtime telemetry whose reader is unnamed
  - opal-data-inf telemetry/inf-gold-layer-runner/history/; opal-data-inf telemetry/inf-gold-layer-runner/status.json
- 1 x RHN nested deeper than kind/file
  - opal-data-cot forwardfill_v2/transactions/_dryrun/
- 1 x N root-level JSON objects of gold/timeseries/ (no '/' after the class prefix): the placeholder is RETIRED by (
  - opal-data-bd gold/timeseries/
- 2 x non-date folder of re-gridded class bronze/eclipse/: not a date partition and not a completion marker
  - opal-data-inf bronze/eclipse/_history/; opal-data-inf bronze/eclipse/_meta/
- 3 x non-date folder of re-gridded class bronze/orion-api/: not a date partition and not a completion marker
  - opal-data-inf bronze/orion-api/backfill_results/; opal-data-inf bronze/orion-api/latest/; opal-data-inf bronze/orion-api/2026-10-11/_markers/
- 1 x non-date folder of re-gridded class gold/eclipse/: not a date partition and not a completion marker
  - opal-data-inf gold/eclipse/_meta/

