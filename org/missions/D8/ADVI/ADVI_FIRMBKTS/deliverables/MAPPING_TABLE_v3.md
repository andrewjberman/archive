# ADVI_FIRMBKTS round 3 -- mapping table v3 (FB-f-2, worker 0.9.0_WK_ADVI_FIRMBKTS~12)

Human view of `mapping_v3.json`, which supersedes round 2's `mapping_v2.json` under the CTO grain ruling (`ledger/ROUND_ANALYSIS.round2.md` section 2 item 3, rules (a)-(e)). Client entity ids are written `{id}`; no object key is printed.

Denominators: 444 census classes and 238,861 census objects (census listed_at 2026-10-09T20:36:32Z). Live total: 239,506 objects from the full listings of the three buckets (bd 131,894 at 2026-10-11T06:29:53Z, inf 99,779 at 2026-10-11T06:30:24Z, cot 7,833 at 2026-10-11T06:30:42Z), difference live minus census +645. The live listings are read-only ListObjectsV2.

FAULT before: 89
FAULT after: 93

## 1. Counts per disposition

| disposition | own-row classes | re-grid child rows | live objects |
|---|---|---|---|
| MOVE | 188 | 2972 | 118,415 |
| HOME | 90 | 20 | 44,719 |
| RETIRE | 80 | 12 | 42,475 |
| DECISION | 2 | 0 | 2 |
| FAULT | 59 | 34 | 33,895 |
| total | 419 | 3038 | 239,506 |

Census classes accounted: 419 own-row classes + 25 re-grid parents = 444 of 444. Re-grid parents keep no own row; their objects sit in the child rows above. Rows in `mapping_v3.json`: 3457 (copied non-FAULT rows from v2: 409).

## 2. Rule applications

- **(a) zero-byte folder placeholders, RETIRE (7 rows):** bd `gold/cohorts/`, `gold/filters/`, `gold/nna/`, `gold/snapshots/`, `gold/summary/`, `gold/timeseries/` (each the marker child of its re-grid) and bd `gold/clients/` (the marker child of its new re-grid). Each is a zero-byte object whose key equals its prefix on the live listing; AC2 arm T1 reads each with a HEAD call.
- **(a) gold/clients/ re-grid (new, 2,948 children):** the class's other 2,948 objects are root JSON files, one child row each, placed by RG3 to `platinum/clients/`. Collision entry merge at overlap 0 (see section 4).
- **(a) gold/timeseries/ re-grid (11 children, FAULT):** the remainder's root JSON objects (`nna_*.json` and `nna_total.json`) are re-gridded out of the marker remainder. No repair rule places them (round-2 judgment carried), so they stay FAULT with owner `1.0.0_SA_CTO~DELL1`.
- **(b) completion markers:** no row carries `kind: marker` in v3. The round-2 copied rows are unchanged by rule (step 4), and the `_complete/` markers of the forwardfill families sit beside data in their own re-grids, which (b) refuses (surprise `ADVI_FIRMBKTS-D1-W12-S1`). The one standalone marker class, cot `bronze/` (113 objects, all `_BRONZE_COMPLETE.json`), has no named state family, so it stays FAULT (surprise `ADVI_FIRMBKTS-D1-W12-S4`). Round-1 and round-2 placed marker rows are copied unchanged (surprise `ADVI_FIRMBKTS-D1-W12-S3`).
- **(c) interleaved classes:** the five round-2 classes (inf `bronze/eclipse/`, `bronze/eclipse_qa/`, `bronze/orion-api/`, `gold/eclipse/`, `silver/eclipse/`) stay FAULT. Their reason no longer cites a child limit (the limit is not a rule). The per-date re-grid is not executed, because the (b) split it needs is not representable (surprise `ADVI_FIRMBKTS-D1-W12-S1`).
- **(d) collisions:** 29 entries, all `merge` at overlap 0: round 2's 28 plus the new platinum `clients` entry (measured 0). No `split` entry. Overlap above 0 stays FAULT, owner `1.0.0_SA_CTO~DELL1`. Overlap-0 new classes that round 2 left FAULT (eight rows) are not placed, because their shared destination is not recorded in v2 (surprise `ADVI_FIRMBKTS-D1-W12-S2`; the eighth, cot `bronze/`, is `-S4`).
- **(e) denominators:** every re-grid prints its census objects, live objects, difference and children sum (section 3).

## 3. Re-grids: census, live and difference

| bucket | parent | census objects | live objects | difference | children objects | listed_at |
|---|---|---|---|---|---|---|
| -bd | backfill_v2/ | 292 | 292 | +0 | 292 | 2026-10-11T06:29:53Z |
| -bd | bronze/ | 212 | 215 | +3 | 215 | 2026-10-11T06:29:53Z |
| -bd | forwardfill_v2/allocations/ | 146 | 148 | +2 | 148 | 2026-10-11T06:29:53Z |
| -bd | forwardfill_v2/realized/ | 245 | 249 | +4 | 249 | 2026-10-11T06:29:53Z |
| -bd | forwardfill_v2/transactions/ | 306 | 310 | +4 | 310 | 2026-10-11T06:29:53Z |
| -bd | forwardfill_v2/unrealized/ | 89 | 91 | +2 | 91 | 2026-10-11T06:29:53Z |
| -bd | gold/clients/ | 2,949 | 2,949 | +0 | 2,949 | 2026-10-11T06:29:53Z |
| -bd | gold/cohorts/ | 2 | 2 | +0 | 2 | 2026-10-11T06:29:53Z |
| -bd | gold/filters/ | 2 | 2 | +0 | 2 | 2026-10-11T06:29:53Z |
| -bd | gold/nna/ | 4 | 4 | +0 | 4 | 2026-10-11T06:29:53Z |
| -bd | gold/snapshots/ | 7 | 7 | +0 | 7 | 2026-10-11T06:29:53Z |
| -bd | gold/summary/ | 2 | 2 | +0 | 2 | 2026-10-11T06:29:53Z |
| -bd | gold/timeseries/ | 2,640 | 2,644 | +4 | 2,644 | 2026-10-11T06:29:53Z |
| -bd | logs/ | 9,107 | 9,239 | +132 | 9,239 | 2026-10-11T06:29:53Z |
| -bd | scripts/ | 154 | 154 | +0 | 154 | 2026-10-11T06:29:53Z |
| -bd | silver/transactions_enriched/ | 519 | 519 | +0 | 519 | 2026-10-11T06:29:53Z |
| -cot | forwardfill_v2/account_attributes/ | 82 | 84 | +2 | 84 | 2026-10-11T06:30:42Z |
| -cot | forwardfill_v2/allocations/ | 199 | 201 | +2 | 201 | 2026-10-11T06:30:42Z |
| -cot | forwardfill_v2/holdings/ | 168 | 170 | +2 | 170 | 2026-10-11T06:30:42Z |
| -cot | forwardfill_v2/realized/ | 204 | 206 | +2 | 206 | 2026-10-11T06:30:42Z |
| -cot | forwardfill_v2/transactions/ | 207 | 209 | +2 | 209 | 2026-10-11T06:30:42Z |
| -cot | forwardfill_v2/unrealized/ | 199 | 201 | +2 | 201 | 2026-10-11T06:30:42Z |
| -cot | silver/ | 803 | 809 | +6 | 809 | 2026-10-11T06:30:42Z |
| -inf | gold/timeseries/ | 2 | 2 | +0 | 2 | 2026-10-11T06:30:24Z |
| -inf | platinum/clients/ | 4,199 | 4,202 | +3 | 4,202 | 2026-10-11T06:30:24Z |

## 4. Collisions by verdict

merge 29, split 0. Every entry is measured at overlap_keys 0 (merge requires 0).

## 5. Remaining FAULT rows, grouped by reason, with owner

Owner of every row: `1.0.0_SA_CTO~DELL1`.

| reason | rows | class prefixes or parents |
|---|---|---|
| market-price silver: {vendor} is not derivable from the key and is not the bucket's feed vendor | 12 | -bd canonical/silver/dim_account/; -bd canonical/silver/fact_position/; -bd silver/historical_dividends.parquet; -bd silver/historical_prices.parquet; -bd silver/historical_prices_20260213.parquet; -bd silver/historical_prices_final.parquet; -bd silver/interpolated_prices.parquet; -bd silver/interpolated_prices_summary.json; -bd silver/prices/; -inf silver/historical_prices.parquet; -inf silver/prices/; child of silver/ |
| root JSON object of gold/timeseries/, re-gridded out of the remainder by ruling (a); no repair rule places it | 11 | child of gold/timeseries/ (x11) |
| destination-key overlap 1 of 1 keys with gold/artifacts/ | 8 | -bd gold/clients_tab.json; -bd gold/firm_composition.json; -bd gold/firm_mix_views.json; -bd gold/firm_mix_views_daily.json; -bd gold/implementor_leaderboard.json; -bd gold/timeseries_chart.json; -cot gold/firm_mix_views.json; -cot gold/firm_mix_views_daily.json |
| no repair rule places it | 7 | -bd gold/config/; -bd schwab/silver/rps/; -inf gold/canonical/; -inf gold/classification/; -inf gold/dimensions/_aor_exercise/aor_attribution_comparison/; -inf gold/dimensions/aor_ledger/events/; -inf gold/dimensions/dim_inf_advisor_office.csv |
| destination-key overlap 0 of 1 keys with the group | 5 | -bd gold/advisor_rolling_flows.json; -bd gold/architect_leaderboard.json; -bd gold/perf_report.json; -bd gold/pipeline-complete.json; -cot gold/firm_composition.json |
| interleaved completion markers and data in the same directories; the (b) split is not representable at the prefix grain and (b) refuses a regrid of markers beside data (surprise ADVI_FIRMBKTS-D1-W12-S1) | 5 | -inf bronze/eclipse/; -inf bronze/eclipse_qa/; -inf bronze/orion-api/; -inf gold/eclipse/; -inf silver/eclipse/ |
| silver/bronze root file, no data directory; no rule places it | 4 | -bd silver/aua_validation_log.parquet; child of silver/ (x3) |
| Lambda deployment artifacts: R16 is not applied to them (PRD CONTRACTS); the home is not ruled | 3 | -bd lambda-deploy/; -bd lambda-layers/; -bd lambda-packages/ |
| leading-slash key; 1b places no leading-slash key | 3 | -inf /advisors/; -inf /clients/; -inf /firm/ |
| destination-key overlap 1 of 1 keys with gold/timeseries/account_performance.parquet | 2 | -bd gold/account_performance.parquet; -cot gold/account_performance.parquet |
| destination-key overlap 1 of 1 keys with gold/timeseries/client_performance.parquet | 2 | -bd gold/client_performance.parquet; -cot gold/client_performance.parquet |
| destination-key overlap 1 of 1 keys with gold/account_performance.parquet | 2 | child of gold/timeseries/; -cot gold/timeseries/account_performance.parquet |
| destination-key overlap 1 of 1 keys with gold/client_performance.parquet | 2 | child of gold/timeseries/; -cot gold/timeseries/client_performance.parquet |
| runtime telemetry whose reader is unnamed | 2 | -inf telemetry/inf-gold-layer-runner/history/; -inf telemetry/inf-gold-layer-runner/status.json |
| destination-key overlap 59 of 59 keys with forwardfill_v2/account_attributes/_complete/ (+4 more classes) | 2 | child of forwardfill_v2/allocations/; child of forwardfill_v2/unrealized/ |
| destination-key overlap 88 of 88 keys with forwardfill_v2/account_attributes/_complete/ (+4 more classes) | 2 | child of forwardfill_v2/realized/; child of forwardfill_v2/transactions/ |
| destination-key overlap 342 of 342 keys with gold/timeseries/positions_cube/ | 1 | -cot gold/positions_cube/ |
| destination-key overlap 342 of 342 keys with gold/positions_cube/ | 1 | -cot gold/timeseries/positions_cube/ |
| RH3: forwardfill root file whose name is not TXN_*.xlsx; no rule places it | 1 | child of backfill_v2/ |
| destination-key overlap 0 of 71 keys with the group | 1 | child of bronze/ |
| destination-key overlap 15 of 15 keys with forwardfill_v2/realized/_complete/ (+2 more classes) | 1 | child of forwardfill_v2/allocations/ |
| destination-key overlap 93 of 93 keys with forwardfill_v2/allocations/_complete/ (+2 more classes) | 1 | child of forwardfill_v2/realized/ |
| destination-key overlap 94 of 103 keys with forwardfill_v2/allocations/_complete/ (+2 more classes) | 1 | child of forwardfill_v2/transactions/ |
| destination-key overlap 15 of 15 keys with forwardfill_v2/allocations/_complete/ (+2 more classes) | 1 | child of forwardfill_v2/unrealized/ |
| destination-key overlap 1 of 1 keys with gold/timeseries/account_quality_tiers.parquet | 1 | -bd gold/account_quality_tiers.parquet |
| destination-key overlap 77 of 493 keys with platinum/advisors/ | 1 | -bd gold/advisors/ |
| RG4 dir whose object is not a date-named parquet; no rule places it | 1 | -bd gold/consolidated/ |
| destination-key overlap 1 of 1 keys with gold/timeseries/synthetic_positions_index.parquet | 1 | -bd gold/synthetic_positions_index.parquet |
| destination-key overlap 1 of 1 keys with gold/account_quality_tiers.parquet | 1 | child of gold/timeseries/ |
| destination-key overlap 1 of 1 keys with gold/synthetic_positions_index.parquet | 1 | child of gold/timeseries/ |
| code: scripts are not data; no tier holds them | 1 | child of scripts/ |
| a live credential: moving it breaks the chain that refreshes it (FWD-8's class) | 1 | -bd smartx/jwt/ |
| destination-key overlap 0 of 113 keys with the group | 1 | -cot bronze/ |
| destination-key overlap 42 of 42 keys with forwardfill_v2/allocations/_complete/ (+4 more classes) | 1 | child of forwardfill_v2/account_attributes/ |
| destination-key overlap 65 of 79 keys with forwardfill_v2/account_attributes/_complete/ (+4 more classes) | 1 | child of forwardfill_v2/holdings/ |
| RH2 nested deeper than kind/file; no rule places it | 1 | child of forwardfill_v2/transactions/ |
| destination-key overlap 0 of 107 keys with the group | 1 | child of silver/ |

