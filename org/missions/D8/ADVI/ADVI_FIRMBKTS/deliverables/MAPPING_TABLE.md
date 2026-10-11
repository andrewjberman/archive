# ADVI_FIRMBKTS FB-t-2 -- the mapping table (one row per census class)

- Worker: `0.9.0_WK_ADVI_FIRMBKTS~1`; machine-readable form: `mapping.json` beside this file; the reading list is `reading_list.json`.
- Census: `census.json` listed_at `2026-10-09T20:36:32Z`; denominator **444 classes** (238861 objects) in 3 buckets: `opal-data-bd` 216 classes / 131391 objects, `opal-data-inf` 174 classes / 99668 objects, `opal-data-cot` 54 classes / 7802 objects.
- Every address in `mapping.json` is `lib/opal_naming.py address()` output for the class's sample key; none is typed.
- Client data: entity ids in sample keys are shown as `{id}` here; `mapping.json` and `reading_list.json` carry the real sample keys.

## Counts per disposition (census denominator 444)

| disposition | classes |
|---|---:|
| MOVE | 132 |
| HOME | 77 |
| RETIRE | 7 |
| DECISION | 2 |
| FAULT | 226 |
| **total** | **444** (census 444) |

Per bucket:

| bucket | MOVE | HOME | RETIRE | DECISION | FAULT | classes |
|---|---:|---:|---:|---:|---:|---:|
| `opal-data-bd` | 53 | 52 | 6 | 0 | 105 | 216 |
| `opal-data-inf` | 53 | 25 | 0 | 2 | 94 | 174 |
| `opal-data-cot` | 26 | 0 | 1 | 0 | 27 | 54 |

Rule key: the `rule` column shows the doctrine rule of the 1b row; `mapping.json` quotes the whole 1b cell. A MOVE or HOME
class is placed by ONE row of 1b that covers every kind of key in it; a class that mixes kinds no single row covers, or that no row
names, is a FAULT (issuer ruling on row ADVI_FIRMBKTS-D1-W1-S1). The FAULT row is `ADVI_FIRMBKTS-D1-W1-S2`.

## `opal-data-bd` (firm `49financial`)

| class | IV.3 class | disposition | dest_pattern | rule |
|---|---|---|---|---|
| `GOOD_RUN_2026-01-21_1015AM/` | - | FAULT | none | no row |
| `_rollback/49f-20260630-preflip/` | - | FAULT | none | no row |
| `ajb_workspace/logs/sessions/` | - | FAULT | none | no row |
| `backfill_v2/` | - | FAULT | none | no row |
| `blackdiamond/49f/` | c | MOVE | `blackdiamond/{firm}/state/session/trigger-mode.json` | R21 |
| `blackdiamond/49financial/bronze/assets_dim_rest/` | d | HOME | `blackdiamond/{firm}/bronze/{table}/{partition}/{object}` | R4, R9 |
| `bronze/` | - | FAULT | none | no row |
| `canonical/schwab/gold/account_gains/` | b | MOVE | `advi/{firm}/gold/account_gains/period={P}/data.parquet` | - |
| `canonical/schwab/gold/account_performance/` | b | MOVE | `advi/{firm}/gold/account_performance/date={P}/data.parquet` | - |
| `canonical/schwab/gold/advisor_attribution/` | b | MOVE | `advi/{firm}/gold/advisor_attribution/date={P}/data.parquet` | - |
| `canonical/schwab/gold/advisor_fee_efficiency/` | b | MOVE | `advi/{firm}/gold/advisor_fee_efficiency/date={P}/data.parquet` | - |
| `canonical/schwab/gold/advisor_split_reconciliation/` | b | MOVE | `advi/{firm}/gold/advisor_split_reconciliation/date={P}/data.parquet` | - |
| `canonical/schwab/gold/advisor_split_reconciliation_firm/` | b | MOVE | `advi/{firm}/gold/advisor_split_reconciliation_firm/date={P}/data.parquet` | - |
| `canonical/schwab/gold/canonical_holdings/` | b | MOVE | `advi/{firm}/gold/canonical_holdings/date={P}/data.parquet` | - |
| `canonical/schwab/gold/canonical_lots/` | b | MOVE | `advi/{firm}/gold/canonical_lots/date={P}/data.parquet` | - |
| `canonical/schwab/gold/canonical_nna/` | b | MOVE | `advi/{firm}/gold/canonical_nna/date={P}/data.parquet` | - |
| `canonical/schwab/gold/client_performance/` | b | MOVE | `advi/{firm}/gold/client_performance/date={P}/data.parquet` | - |
| `canonical/schwab/gold/client_tax_liability/` | b | MOVE | `advi/{firm}/gold/client_tax_liability/date={P}/data.parquet` | - |
| `canonical/schwab/gold/firm_composition/` | b | MOVE | `advi/{firm}/gold/firm_composition/date={P}/data.parquet` | - |
| `canonical/schwab/gold/partner_analytics/` | b | MOVE | `advi/{firm}/gold/partner_analytics/date={P}/data.parquet` | - |
| `canonical/schwab/gold/portal_aggregates/` | b | MOVE | `advi/{firm}/gold/portal_aggregates/date={P}/data.parquet` | - |
| `canonical/schwab/gold/realized_gains/` | b | MOVE | `advi/{firm}/gold/realized_gains/date={P}/data.parquet` | - |
| `canonical/schwab/silver/dim_account/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/dim_advisor_fee/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/dim_advisor_role/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/dim_asset/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/dim_relationship/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_account/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_billing/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_billing_extract/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_lot_realized/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_lot_unrealized/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_lot_unrealized_tax/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_position/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_position_pending/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_position_pending_tax/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_realized_rlu/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_realized_rlw/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_realized_rly/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_realized_rtu/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_realized_rty/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_securities/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_tax_1099div/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/schwab/silver/fact_transaction/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `canonical/silver/dim_account/` | - | FAULT | none | no row |
| `canonical/silver/fact_position/` | - | FAULT | none | no row |
| `code/` | f | MOVE | `advi/{firm}/code/{built_tier}/{tail}` | R16, key.code; CENSUS.md collapses code/ to ONE kind (code), which row f covers whole |
| `config/` | c | MOVE | `advi/{firm}/state/config/{file}` | R21 |
| `debug/download-button-error.png` | - | FAULT | none | no row |
| `debug/download-daily-error.png` | - | FAULT | none | no row |
| `debug/error-final.png` | - | FAULT | none | no row |
| `debug/txn-debug-211841/` | - | FAULT | none | no row |
| `debug/txn-query-timeout.png` | - | FAULT | none | no row |
| `diagnostics/` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-16.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-19.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-21.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-22.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-23.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-26.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/TXN_2026-01-27.xlsx` | - | FAULT | none | no row |
| `forwardfill_v2/_perm_probe_1782839405.txt` | - | FAULT | none | no row |
| `forwardfill_v2/allocations/` | - | FAULT | none | no row |
| `forwardfill_v2/assets/` | - | FAULT | none | no row |
| `forwardfill_v2/realized/` | - | FAULT | none | no row |
| `forwardfill_v2/transactions/` | - | FAULT | none | no row |
| `forwardfill_v2/unrealized/` | - | FAULT | none | no row |
| `gldrst/preflight/` | - | FAULT | none | no row |
| `gold/.checkpoints/` | - | FAULT | none | no row |
| `gold/_deprecated/` | - | FAULT | none | no row |
| `gold/_parity/account_gains/` | c | MOVE | `advi/{firm}/state/parity/account_gains/{tail}` | R21 |
| `gold/_parity/advisor_assignments/` | c | MOVE | `advi/{firm}/state/parity/advisor_assignments/{tail}` | R21 |
| `gold/_parity/canonical_lots/` | c | MOVE | `advi/{firm}/state/parity/canonical_lots/{tail}` | R21 |
| `gold/_parity/fee_rate_history/` | c | MOVE | `advi/{firm}/state/parity/fee_rate_history/{tail}` | R21 |
| `gold/_parity/holdings_lots/` | c | MOVE | `advi/{firm}/state/parity/holdings_lots/{tail}` | R21 |
| `gold/_parity/load_flows/` | c | MOVE | `advi/{firm}/state/parity/load_flows/{tail}` | R21 |
| `gold/_parity/positions_cube/` | c | MOVE | `advi/{firm}/state/parity/positions_cube/{tail}` | R21 |
| `gold/_regen_backup_20260706T1923Z/` | - | FAULT | none | no row |
| `gold/_state/advisor_assignments/` | c | MOVE | `advi/{firm}/state/watermarks/advisor_assignments/{tail}` | R21 |
| `gold/_state/load_flows/` | c | MOVE | `advi/{firm}/state/watermarks/load_flows/{tail}` | R21 |
| `gold/account_performance.parquet` | - | FAULT | none | no row |
| `gold/account_quality_tiers.parquet` | - | FAULT | none | no row |
| `gold/account_quality_tiers_2026-03-31.json` | e | RETIRE | none | R17, R18 |
| `gold/account_quality_tiers_2026-04-02.json` | e | RETIRE | none | R17, R18 |
| `gold/accounts_dimension_latest.parquet` | - | FAULT | none | no row |
| `gold/advisor_assignments_history.parquet` | - | FAULT | none | no row |
| `gold/advisor_rolling_flows.json` | - | FAULT | none | no row |
| `gold/advisors/` | - | FAULT | none | no row |
| `gold/architect_leaderboard.json` | - | FAULT | none | no row |
| `gold/artifacts/` | a | MOVE | `advi/{firm}/platinum/artifacts/{tail}` | R12 |
| `gold/aua_certification/` | - | FAULT | none | no row |
| `gold/canonical/account_gains/` | b | MOVE | `advi/{firm}/gold/account_gains/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/advisor_fee_detail/` | b | MOVE | `advi/{firm}/gold/advisor_fee_detail/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/holdings/` | b | MOVE | `advi/{firm}/gold/holdings/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/holdings_gaps/` | b | MOVE | `advi/{firm}/gold/holdings_gaps/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/lots_realized/` | b | MOVE | `advi/{firm}/gold/lots_realized/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/lots_unrealized/` | b | MOVE | `advi/{firm}/gold/lots_unrealized/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/nna/` | b | MOVE | `advi/{firm}/gold/nna/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/nna_atomic/` | b | MOVE | `advi/{firm}/gold/nna_atomic/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/nna_validation/` | - | FAULT | none | no row |
| `gold/canonical/performance/` | b | MOVE | `advi/{firm}/gold/performance/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/role_aua/` | b | MOVE | `advi/{firm}/gold/role_aua/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/watermarks.json` | c | MOVE | `advi/{firm}/state/watermarks/watermarks.json` | R21 |
| `gold/client_dimension.parquet` | - | FAULT | none | no row |
| `gold/client_performance.parquet` | - | FAULT | none | no row |
| `gold/client_timeseries/` | - | FAULT | none | no row |
| `gold/clients/` | - | FAULT | none | no row |
| `gold/clients_tab.json` | - | FAULT | none | no row |
| `gold/cohorts/` | - | FAULT | none | no row |
| `gold/config/` | - | FAULT | none | no row |
| `gold/consolidated/` | - | FAULT | none | no row |
| `gold/daily/positions/` | - | FAULT | none | no row |
| `gold/dimensions/` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/entities/accounts/` | a | MOVE | `advi/{firm}/platinum/entities/accounts/{tail}` | R12 |
| `gold/entities/advisors/` | a | MOVE | `advi/{firm}/platinum/entities/advisors/{tail}` | R12 |
| `gold/entities/clients/` | a | MOVE | `advi/{firm}/platinum/entities/clients/{tail}` | R12 |
| `gold/filters/` | - | FAULT | none | no row |
| `gold/firm_composition.json` | - | FAULT | none | no row |
| `gold/firm_mix_views.json` | - | FAULT | none | no row |
| `gold/firm_mix_views_daily.json` | - | FAULT | none | no row |
| `gold/holdings_lots/` | - | FAULT | none | no row |
| `gold/holdings_lots_v2_dryrun/` | e | RETIRE | none | R17, R18 |
| `gold/implementor_leaderboard.json` | - | FAULT | none | no row |
| `gold/logs/` | - | FAULT | none | no row |
| `gold/manifests/` | c | MOVE | `advi/{firm}/state/manifests/{file}` | R21 |
| `gold/meta/` | c | MOVE | `advi/{firm}/state/watermarks/{name}_watermark.json` | R21 |
| `gold/nna/` | - | FAULT | none | no row |
| `gold/partner_analytics/` | - | FAULT | none | no row |
| `gold/perf_history/` | - | FAULT | none | no row |
| `gold/perf_report.json` | - | FAULT | none | no row |
| `gold/perf_report_qa_2026-04-17_single_b01.json` | e | RETIRE | none | R17, R18 |
| `gold/perf_report_qa_bcd_2026-04-17.json` | e | RETIRE | none | R17, R18 |
| `gold/pipeline-complete.json` | - | FAULT | none | no row |
| `gold/platinum/firm/` | a | MOVE | `advi/{firm}/platinum/firm/{tail}` | R12 |
| `gold/positions_cube/` | b | MOVE | `advi/{firm}/gold/positions_cube/date={D}/data.parquet` | R5, R11 |
| `gold/snapshots/` | - | FAULT | none | no row |
| `gold/summary/` | - | FAULT | none | no row |
| `gold/synthetic_positions_index.parquet` | - | FAULT | none | no row |
| `gold/timeseries/` | - | FAULT | none | no row |
| `gold/timeseries_chart.json` | - | FAULT | none | no row |
| `gold/validation/` | e | RETIRE | none | R17, R18 |
| `gold/views/` | a | MOVE | `advi/{firm}/platinum/views/{tail}` | R12 |
| `investor-reporting/directory/` | - | FAULT | none | no row |
| `investor-reporting/qa/directory/` | - | FAULT | none | no row |
| `investor-reporting/qa/holdings/` | - | FAULT | none | no row |
| `lambda-deploy/` | - | FAULT | none | no row |
| `lambda-layers/` | - | FAULT | none | no row |
| `lambda-packages/` | - | FAULT | none | no row |
| `logs/` | - | FAULT | none | no row |
| `platinum/49financial/` | a | MOVE | `advi/{firm}/platinum/49financial/{tail}` | R6 |
| `platinum/accounts/` | a | MOVE | `advi/{firm}/platinum/accounts/{tail}` | R6 |
| `platinum/advisors/` | a | MOVE | `advi/{firm}/platinum/advisors/{tail}` | R6 |
| `platinum/clients/` | a | MOVE | `advi/{firm}/platinum/clients/{tail}` | R6 |
| `platinum/firm/` | a | MOVE | `advi/{firm}/platinum/firm/{tail}` | R6 |
| `qa-scratch/ds1_run5_log.txt` | - | FAULT | none | no row |
| `qa-scratch/ds1_run6_log.txt` | - | FAULT | none | no row |
| `qa-scratch/ds1_validate/` | - | FAULT | none | no row |
| `qa-scratch/gate2_unit_delta_run7.parquet` | - | FAULT | none | no row |
| `runs/` | - | FAULT | none | no row |
| `schwab/bronze/` | d | HOME | `schwab/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `schwab/silver/acc/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `schwab/silver/account_xref/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `schwab/silver/rld/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `schwab/silver/rps/` | - | FAULT | none | no row |
| `schwab/silver/trn/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `schwab/silver/trn_nna/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `schwab/silver/uln/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `schwab/silver/ult/` | d | HOME | `schwab/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `scripts/` | - | FAULT | none | no row |
| `silver/allocations/` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/assets/` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/aua_validation_log.parquet` | - | FAULT | none | no row |
| `silver/bd_allocations.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_assets.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_assets_dim.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_aua_timeseries.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_canonical_timeline.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_nna_by_architect.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_nna_daily.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/bd_transactions_backup_2026-01-20.parquet` | - | FAULT | none | no row |
| `silver/bd_transactions_backup_2026-01-28.parquet` | - | FAULT | none | no row |
| `silver/bd_transactions_metadata.json` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/daily_aua.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/daily_aua_firm.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/daily_flows.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/daily_positions.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/fees/` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/historical_dividends.parquet` | - | FAULT | none | no row |
| `silver/historical_prices.parquet` | - | FAULT | none | no row |
| `silver/historical_prices_20260213.parquet` | - | FAULT | none | no row |
| `silver/historical_prices_final.parquet` | - | FAULT | none | no row |
| `silver/incremental_allocation_manifest.json` | - | FAULT | none | no row |
| `silver/incremental_allocation_manifest.json.bak-20260630T1900Z` | - | FAULT | none | no row |
| `silver/incremental_allocation_manifest.json.bak-20260630T1916Z` | - | FAULT | none | no row |
| `silver/incremental_manifest.json` | - | FAULT | none | no row |
| `silver/incremental_realized_manifest.json` | - | FAULT | none | no row |
| `silver/incremental_unrealized_manifest.json` | - | FAULT | none | no row |
| `silver/interpolated_prices.parquet` | - | FAULT | none | no row |
| `silver/interpolated_prices_summary.json` | - | FAULT | none | no row |
| `silver/nna_timeseries.parquet` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/prices/` | - | FAULT | none | no row |
| `silver/realized/` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/transactions/` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/transactions_enriched/` | - | FAULT | none | no row |
| `silver/unrealized/` | d | HOME | `blackdiamond/{firm}/silver/{table}/{partition}` | R4, R9 |
| `smartx/bronze/model_aum/` | d | HOME | `smartx/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `smartx/bronze/model_holdings/` | d | HOME | `smartx/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `smartx/jwt/` | - | FAULT | none | no row |
| `smartx/raw/enterprises_aum/` | - | FAULT | none | no row |
| `smartx/raw/holdings/` | - | FAULT | none | no row |
| `smartx/raw/models/` | - | FAULT | none | no row |
| `ssm-output/` | - | FAULT | none | no row |
| `status/` | - | FAULT | none | no row |
| `temp/` | - | FAULT | none | no row |
| `tmp/` | - | FAULT | none | no row |
| `v4_output/` | - | FAULT | none | no row |

## `opal-data-inf` (firm `inflection`)

| class | IV.3 class | disposition | dest_pattern | rule |
|---|---|---|---|---|
| `/advisors/` | - | FAULT | none | no row |
| `/clients/` | - | FAULT | none | no row |
| `/firm/` | - | FAULT | none | no row |
| `_compare/unified_proof_20260630/` | - | FAULT | none | no row |
| `_pre_rebuild_backup/` | - | FAULT | none | no row |
| `_rebuild_status/` | - | FAULT | none | no row |
| `_scratch/indexbytes-face/` | - | FAULT | none | no row |
| `_toolprobe_scratch/comp-freshness/` | - | FAULT | none | no row |
| `_toolprobe_scratch/pk/silver/toolprobe/` | - | FAULT | none | no row |
| `backup/_restore_exercise_20260715T225000Z/` | - | FAULT | none | no row |
| `backup/aor_ledger_pre_reseed_20260716T012840Z/aor_ledger/events/` | - | FAULT | none | no row |
| `backup/aor_ledger_pre_reseed_20260716T012840Z/aor_ledger_state.parquet` | - | FAULT | none | no row |
| `backup/gold_canonical_PRE_REDERIVE_20260713T1012Z/` | - | FAULT | none | no row |
| `backup/pre_exclusion_dispatch_20260715T2335Z/` | - | FAULT | none | no row |
| `backup/pre_pullheal_20260716T0218Z/` | - | FAULT | none | no row |
| `backup/pre_rescue_20260715T2259Z/` | - | FAULT | none | no row |
| `backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/advisors/` | - | FAULT | none | no row |
| `backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/firm/` | - | FAULT | none | no row |
| `backup/served_spine_PRE_TIMELOCK_2026-07-13T184646Z/` | - | FAULT | none | no row |
| `bronze/_parity-snapshot/` | - | FAULT | none | no row |
| `bronze/assets/` | d | HOME | `orion/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `bronze/eclipse/` | - | FAULT | none | no row |
| `bronze/eclipse_qa/` | - | FAULT | none | no row |
| `bronze/logs/inf-bronze-runner/` | - | FAULT | none | no row |
| `bronze/logs/inf-gold-runner/` | - | FAULT | none | no row |
| `bronze/orion-api-v2/` | d | HOME | `orion/{firm}/bronze/{table}/{partition}/{object}` | R4, R9 |
| `bronze/orion-api/` | - | FAULT | none | no row |
| `bronze/orion/` | d | HOME | `orion/{firm}/bronze/{table}/{partition}/{object}` | R4, R9 |
| `bronze/performance/` | d | HOME | `orion/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `bronze/positions/` | d | HOME | `orion/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `bronze/transactions/` | d | HOME | `orion/{firm}/bronze/{table}/{partition}` | R4, R9 |
| `code/` | f | MOVE | `advi/{firm}/code/{built_tier}/{tail}` | R16, key.code; CENSUS.md collapses code/ to ONE kind (code), which row f covers whole |
| `config/` | c | MOVE | `advi/{firm}/state/config/{file}` | R21 |
| `diagnostic/` | - | FAULT | none | no row |
| `eclipse/browser-profile/` | - | FAULT | none | no row |
| `gold/_rebuild/` | - | FAULT | none | no row |
| `gold/account_gains/` | b | MOVE | `advi/{firm}/gold/account_gains/date={D}/data.parquet` | R5, R11 |
| `gold/artifacts/` | a | MOVE | `advi/{firm}/platinum/artifacts/{tail}` | R12 |
| `gold/cache/` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/canonical/` | - | FAULT | none | no row |
| `gold/classification/` | - | FAULT | none | no row |
| `gold/dimensions/_aor_exercise/aor_attribution_comparison/` | - | FAULT | none | no row |
| `gold/dimensions/accounts_dimension_latest.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/advisor_assignments.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/aor_ledger/events/` | - | FAULT | none | no row |
| `gold/dimensions/aor_ledger_state.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/aor_resolution.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/client_dimension.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/dim_inf_advisor_office.csv` | - | FAULT | none | no row |
| `gold/dimensions/fee_rate_history.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dispatch-lock.json` | - | FAULT | none | no row |
| `gold/eclipse/` | - | FAULT | none | no row |
| `gold/holdings/` | b | MOVE | `advi/{firm}/gold/holdings/date={D}/data.parquet` | R5, R11 |
| `gold/logs/` | - | FAULT | none | no row |
| `gold/lots/` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/manifests/` | c | MOVE | `advi/{firm}/state/manifests/{file}` | R21 |
| `gold/meta/pipeline-complete.json` | - | DECISION | none; FWD-7 | Door 6 |
| `gold/meta/pipeline-failed.json` | - | FAULT | none | no row |
| `gold/meta/pull-complete.json` | - | FAULT | none | no row |
| `gold/meta/schemas/` | - | FAULT | none | no row |
| `gold/meta/valgate-baseline/silver_transactions/` | - | FAULT | none | no row |
| `gold/perf_report.json` | - | FAULT | none | no row |
| `gold/positions_cube/` | b | MOVE | `advi/{firm}/gold/positions_cube/date={D}/data.parquet` | R5, R11 |
| `gold/timeseries/` | - | FAULT | none | no row |
| `gold/views/` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `investor-reporting/directory/` | - | FAULT | none | no row |
| `investor-reporting/qa/directory/` | - | FAULT | none | no row |
| `investor-reporting/qa/holdings/` | - | FAULT | none | no row |
| `orion/backfill_progress_2a0c2a94-ab97-47bb-a22f-f194db318145.json` | - | FAULT | none | no row |
| `orion/backfill_progress_2f0abf97-249e-40d8-894a-c464578adbf4.json` | - | FAULT | none | no row |
| `orion/backfill_progress_4558ff63-5cd2-4eec-a3e4-7b575e74d319.json` | - | FAULT | none | no row |
| `orion/backfill_progress_56b947d9-c82a-43ea-8f85-7db8f0e5354d.json` | - | FAULT | none | no row |
| `orion/backfill_progress_d46faee5-ee79-42ff-85a5-b4d9c4f2ed0b.json` | - | FAULT | none | no row |
| `orion/backfill_progress_ea9e59a8-0527-4bc9-9871-e8edcb805b5d.json` | - | FAULT | none | no row |
| `orion/browser-profile/` | - | FAULT | none | no row |
| `orion/jwt/current.json` | - | DECISION | none; FWD-8 | B2 |
| `orion/jwt/trigger-mode.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_accounts_v2.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_activity.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_assets_v2.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_billing.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_household.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_household_rep_mapping.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_performance.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_performance_f1validate.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_positions_mv.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_probe.json` | - | FAULT | none | no row |
| `orion/rate_limit_state_transactions.json` | - | FAULT | none | no row |
| `otp/debug/` | - | FAULT | none | no row |
| `otp/state.json` | c | MOVE | `orion/inflection/state/otp/state.json` | R21 |
| `platinum/_rebuild/` | - | FAULT | none | no row |
| `platinum/advisors/` | a | MOVE | `advi/{firm}/platinum/advisors/{tail}` | R6 |
| `platinum/clients/` | - | FAULT | none | no row |
| `platinum/firm/_meta/` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/clients_tab.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/dashboard.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/filters/` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/header_metrics.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/leaderboard.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_annual.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_monthly.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_quarterly.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/timeseries_chart.json` | - | FAULT | none | no row |
| `platinum/firm/_quarantine_scope_bug_20260424/timeseries_overview.json` | - | FAULT | none | no row |
| `platinum/firm/_rollback/` | - | FAULT | none | no row |
| `platinum/firm/activity_scan.json` | a | MOVE | `advi/{firm}/platinum/firm/activity_scan.json` | R6 |
| `platinum/firm/activity_scan_1y.json` | a | MOVE | `advi/{firm}/platinum/firm/activity_scan_1y.json` | R6 |
| `platinum/firm/activity_scan_max.json` | a | MOVE | `advi/{firm}/platinum/firm/activity_scan_max.json` | R6 |
| `platinum/firm/activity_scan_qtd.json` | a | MOVE | `advi/{firm}/platinum/firm/activity_scan_qtd.json` | R6 |
| `platinum/firm/activity_scan_ytd.json` | a | MOVE | `advi/{firm}/platinum/firm/activity_scan_ytd.json` | R6 |
| `platinum/firm/advisor_nna_canonical.json` | a | MOVE | `advi/{firm}/platinum/firm/advisor_nna_canonical.json` | R6 |
| `platinum/firm/cash_drag.json` | a | MOVE | `advi/{firm}/platinum/firm/cash_drag.json` | R6 |
| `platinum/firm/cash_drag_1y.json` | a | MOVE | `advi/{firm}/platinum/firm/cash_drag_1y.json` | R6 |
| `platinum/firm/cash_drag_max.json` | a | MOVE | `advi/{firm}/platinum/firm/cash_drag_max.json` | R6 |
| `platinum/firm/cash_drag_qtd.json` | a | MOVE | `advi/{firm}/platinum/firm/cash_drag_qtd.json` | R6 |
| `platinum/firm/cash_drag_ytd.json` | a | MOVE | `advi/{firm}/platinum/firm/cash_drag_ytd.json` | R6 |
| `platinum/firm/client_directory.json` | a | MOVE | `advi/{firm}/platinum/firm/client_directory.json` | R6 |
| `platinum/firm/clients-tab-slim.json` | a | MOVE | `advi/{firm}/platinum/firm/clients-tab-slim.json` | R6 |
| `platinum/firm/clients_tab.json` | a | MOVE | `advi/{firm}/platinum/firm/clients_tab.json` | R6 |
| `platinum/firm/concentration_risk.json` | a | MOVE | `advi/{firm}/platinum/firm/concentration_risk.json` | R6 |
| `platinum/firm/cumulative_chart.json` | a | MOVE | `advi/{firm}/platinum/firm/cumulative_chart.json` | R6 |
| `platinum/firm/dashboard.json` | a | MOVE | `advi/{firm}/platinum/firm/dashboard.json` | R6 |
| `platinum/firm/fee_efficiency.json` | a | MOVE | `advi/{firm}/platinum/firm/fee_efficiency.json` | R6 |
| `platinum/firm/filters/` | a | MOVE | `advi/{firm}/platinum/firm/filters/{tail}` | R6 |
| `platinum/firm/firm_composition.json` | a | MOVE | `advi/{firm}/platinum/firm/firm_composition.json` | R6 |
| `platinum/firm/firm_concentrations.json` | a | MOVE | `advi/{firm}/platinum/firm/firm_concentrations.json` | R6 |
| `platinum/firm/header_metrics.json` | a | MOVE | `advi/{firm}/platinum/firm/header_metrics.json` | R6 |
| `platinum/firm/header_metrics_fresh.json` | a | MOVE | `advi/{firm}/platinum/firm/header_metrics_fresh.json` | R6 |
| `platinum/firm/leaderboard.json` | a | MOVE | `advi/{firm}/platinum/firm/leaderboard.json` | R6 |
| `platinum/firm/mix_summary.json` | a | MOVE | `advi/{firm}/platinum/firm/mix_summary.json` | R6 |
| `platinum/firm/nmec_nmnc_nna.json` | a | MOVE | `advi/{firm}/platinum/firm/nmec_nmnc_nna.json` | R6 |
| `platinum/firm/partner_analytics.json` | a | MOVE | `advi/{firm}/platinum/firm/partner_analytics.json` | R6 |
| `platinum/firm/partner_analytics_annual.json` | a | MOVE | `advi/{firm}/platinum/firm/partner_analytics_annual.json` | R6 |
| `platinum/firm/partner_analytics_monthly.json` | a | MOVE | `advi/{firm}/platinum/firm/partner_analytics_monthly.json` | R6 |
| `platinum/firm/partner_analytics_quarterly.json` | a | MOVE | `advi/{firm}/platinum/firm/partner_analytics_quarterly.json` | R6 |
| `platinum/firm/snapshots/` | a | MOVE | `advi/{firm}/platinum/firm/snapshots/{tail}` | R6 |
| `platinum/firm/timeseries_chart.json` | a | MOVE | `advi/{firm}/platinum/firm/timeseries_chart.json` | R6 |
| `platinum/firm/timeseries_overview.json` | a | MOVE | `advi/{firm}/platinum/firm/timeseries_overview.json` | R6 |
| `platinum/firm/top_holdings.json` | a | MOVE | `advi/{firm}/platinum/firm/top_holdings.json` | R6 |
| `qa/_diag/` | - | FAULT | none | no row |
| `qa/advisors/` | - | FAULT | none | no row |
| `qa/artifacts/` | - | FAULT | none | no row |
| `qa/clients/` | - | FAULT | none | no row |
| `qa/firm/` | - | FAULT | none | no row |
| `qa/gold-artifacts/` | - | FAULT | none | no row |
| `silver/_parity-snapshot/positions_mv-2026-06-30/` | - | FAULT | none | no row |
| `silver/_silver_complete/` | - | FAULT | none | no row |
| `silver/accounts_dim/` | d | HOME | `orion/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/api_dims/_chain_summary/` | - | FAULT | none | no row |
| `silver/api_dims/accounts_v2/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/activity/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/assets/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/assets_v2/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/billing/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/household/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/household_rep_mapping/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/performance/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/positions_mv/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/representatives/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/tax_realized/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/api_dims/tax_unrealized/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/assets_v2/` | d | HOME | `orion/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/eclipse/` | - | FAULT | none | no row |
| `silver/historical_prices.parquet` | - | FAULT | none | no row |
| `silver/meta/` | c | MOVE | `advi/{firm}/state/manifests/{file}` | R21 |
| `silver/orion-rest/performance_weekly/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/orion-rest/transactions/` | d | HOME | `orion/{firm}/silver/{table}/{partition}/{object}` | R4, R9 |
| `silver/performance/` | d | HOME | `orion/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/performance_dim/` | d | HOME | `orion/{firm}/silver/{table}/{partition}` | R4, R9 |
| `silver/prices/` | - | FAULT | none | no row |
| `silver/transactions/` | d | HOME | `orion/{firm}/silver/{table}/{partition}` | R4, R9 |
| `telemetry/inf-gold-layer-runner/history/` | - | FAULT | none | no row |
| `telemetry/inf-gold-layer-runner/status.json` | - | FAULT | none | no row |

## `opal-data-cot` (firm `cottonwood`)

| class | IV.3 class | disposition | dest_pattern | rule |
|---|---|---|---|---|
| `blackdiamond/cot/` | c | MOVE | `blackdiamond/{firm}/state/session/trigger-mode.json` | R21 |
| `bronze/` | - | FAULT | none | no row |
| `code/` | f | MOVE | `advi/{firm}/code/{built_tier}/{tail}` | R16, key.code; CENSUS.md collapses code/ to ONE kind (code), which row f covers whole |
| `forwardfill_v2/_retry_net/` | - | FAULT | none | no row |
| `forwardfill_v2/account_attributes/` | - | FAULT | none | no row |
| `forwardfill_v2/allocations/` | - | FAULT | none | no row |
| `forwardfill_v2/holdings/` | - | FAULT | none | no row |
| `forwardfill_v2/realized/` | - | FAULT | none | no row |
| `forwardfill_v2/transactions/` | - | FAULT | none | no row |
| `forwardfill_v2/unrealized/` | - | FAULT | none | no row |
| `gold/account_performance.parquet` | - | FAULT | none | no row |
| `gold/accounts_dimension_latest.parquet` | - | FAULT | none | no row |
| `gold/advisor_assignments_history.parquet` | - | FAULT | none | no row |
| `gold/artifacts/` | a | MOVE | `advi/{firm}/platinum/artifacts/{tail}` | R12 |
| `gold/canonical/account_gains/` | b | MOVE | `advi/{firm}/gold/account_gains/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/holdings/` | b | MOVE | `advi/{firm}/gold/holdings/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/nna/` | b | MOVE | `advi/{firm}/gold/nna/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/nna_atomic/` | b | MOVE | `advi/{firm}/gold/nna_atomic/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/nna_validation/` | - | FAULT | none | no row |
| `gold/canonical/performance/` | b | MOVE | `advi/{firm}/gold/performance/date={D}/data.parquet` | R5, R11 |
| `gold/canonical/watermarks.json` | c | MOVE | `advi/{firm}/state/watermarks/watermarks.json` | R21 |
| `gold/client_dimension.parquet` | - | FAULT | none | no row |
| `gold/client_performance.parquet` | - | FAULT | none | no row |
| `gold/client_timeseries/` | - | FAULT | none | no row |
| `gold/dimensions/accounts_dimension_latest.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/advisor_assignments_history.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/dimensions/assets_dim/` | b | MOVE | `advi/{firm}/gold/assets_dim/date={D}/data.parquet` | R5, R11 |
| `gold/dimensions/client_dimension.parquet` | b | MOVE | `advi/{firm}/gold/{table}/data.parquet` | R5, R11; undated source file, so the partition is the named leaf data.parquet |
| `gold/entities/accounts/` | a | MOVE | `advi/{firm}/platinum/entities/accounts/{tail}` | R12 |
| `gold/entities/advisors/` | a | MOVE | `advi/{firm}/platinum/entities/advisors/{tail}` | R12 |
| `gold/entities/clients/` | a | MOVE | `advi/{firm}/platinum/entities/clients/{tail}` | R12 |
| `gold/firm_composition.json` | - | FAULT | none | no row |
| `gold/firm_mix_views.json` | - | FAULT | none | no row |
| `gold/firm_mix_views_daily.json` | - | FAULT | none | no row |
| `gold/logs/` | - | FAULT | none | no row |
| `gold/meta/` | c | MOVE | `advi/{firm}/state/watermarks/{name}_watermark.json` | R21 |
| `gold/partner_analytics/` | - | FAULT | none | no row |
| `gold/platinum/firm/` | a | MOVE | `advi/{firm}/platinum/firm/{tail}` | R12 |
| `gold/positions_cube/` | b | MOVE | `advi/{firm}/gold/positions_cube/date={D}/data.parquet` | R5, R11 |
| `gold/timeseries/account_performance.parquet` | - | FAULT | none | no row |
| `gold/timeseries/client_performance.parquet` | - | FAULT | none | no row |
| `gold/timeseries/positions_cube/` | b | MOVE | `advi/{firm}/gold/positions_cube/date={D}/data.parquet` | R5, R11 |
| `gold/validation/` | e | RETIRE | none | R17, R18 |
| `gold/views/` | a | MOVE | `advi/{firm}/platinum/views/{tail}` | R12 |
| `investor-reporting/directory/` | - | FAULT | none | no row |
| `investor-reporting/qa/directory/` | - | FAULT | none | no row |
| `investor-reporting/qa/holdings/` | - | FAULT | none | no row |
| `logs/` | - | FAULT | none | no row |
| `platinum/advisors/` | a | MOVE | `advi/{firm}/platinum/advisors/{tail}` | R6 |
| `platinum/clients/` | a | MOVE | `advi/{firm}/platinum/clients/{tail}` | R6 |
| `platinum/cottonwood/` | a | MOVE | `advi/{firm}/platinum/cottonwood/{tail}` | R6 |
| `platinum/firm/` | a | MOVE | `advi/{firm}/platinum/firm/{tail}` | R6 |
| `platinum/satellites/` | a | MOVE | `etfs/{firm}/platinum/satellites/{tail}` | R6; source etfs |
| `silver/` | - | FAULT | none | no row |

## FAULT classes (row `ADVI_FIRMBKTS-D1-W1-S2`)

| bucket | class | reason | fault_row |
|---|---|---|---|
| `opal-data-bd` | `GOOD_RUN_2026-01-21_1015AM/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `_rollback/49f-20260630-preflip/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `ajb_workspace/logs/sessions/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `backfill_v2/` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `bronze/` | MIXED: dated _BRONZE_COMPLETE.json completion markers (state kind, class c; 1b has no row for them) beside fees/ and bi/ bronze data (class d HOME); no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `canonical/silver/dim_account/` | canonical silver with no vendor in its key: 1b's HOME needs a {vendor} and the key does not give one | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `canonical/silver/fact_position/` | canonical silver with no vendor in its key: 1b's HOME needs a {vendor} and the key does not give one | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `debug/download-button-error.png` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `debug/download-daily-error.png` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `debug/error-final.png` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `debug/txn-debug-211841/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `debug/txn-query-timeout.png` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `diagnostics/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-16.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-19.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-21.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-22.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-23.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-26.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/TXN_2026-01-27.xlsx` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/_perm_probe_1782839405.txt` | raw vendor download files (xlsx/txt) under forwardfill_v2/ or backfill_v2/; no 1b row names them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/allocations/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/assets/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/realized/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/transactions/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `forwardfill_v2/unrealized/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gldrst/preflight/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/.checkpoints/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/_deprecated/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/_regen_backup_20260706T1923Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/account_performance.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/account_quality_tiers.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/accounts_dimension_latest.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/advisor_assignments_history.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/advisor_rolling_flows.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/advisors/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/architect_leaderboard.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/aua_certification/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/canonical/nna_validation/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/client_dimension.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/client_performance.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/client_timeseries/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/clients/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/clients_tab.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/cohorts/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/config/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/consolidated/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/daily/positions/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/filters/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/firm_composition.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/firm_mix_views.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/firm_mix_views_daily.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/holdings_lots/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/implementor_leaderboard.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/logs/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/nna/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/partner_analytics/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/perf_history/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/perf_report.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/pipeline-complete.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/snapshots/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/summary/` | MIXED (named in CENSUS.md): a zero-byte directory-marker key beside the directory's own children, and no 1b row names this directory | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/synthetic_positions_index.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/timeseries/` | MIXED: positions_cube/ and holdings_lots/ (class b gold tables), holdings_lots_shadow/ (class e RETIRE candidate, R18) and 16 json/parquet files directly under timeseries/ (not the `{t}/...` shape), plus a directory-marker key; no single 1b row covers every kind; named exception: holdings_lots_shadow/ (RETIRE) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `gold/timeseries_chart.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `investor-reporting/directory/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `investor-reporting/qa/directory/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `investor-reporting/qa/holdings/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `lambda-deploy/` | Lambda deployment artifacts: key.code admits them as code-tier keys, but no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `lambda-layers/` | Lambda deployment artifacts: key.code admits them as code-tier keys, but no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `lambda-packages/` | Lambda deployment artifacts: key.code admits them as code-tier keys, but no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `logs/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `qa-scratch/ds1_run5_log.txt` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `qa-scratch/ds1_run6_log.txt` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `qa-scratch/ds1_validate/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `qa-scratch/gate2_unit_delta_run7.parquet` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `runs/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `schwab/silver/rps/` | the sample key is a completion marker or diagnostic artifact (state or diagnostic kind); 1b gives only the eclipse completion markers a state row, so no row places this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `scripts/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/aua_validation_log.parquet` | load manifest or validation log inside silver/: state or validation kind; 1b names only silver/meta/gap_manifest.json for state | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/bd_transactions_backup_2026-01-20.parquet` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/bd_transactions_backup_2026-01-28.parquet` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/historical_dividends.parquet` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/historical_prices.parquet` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/historical_prices_20260213.parquet` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/historical_prices_final.parquet` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/incremental_allocation_manifest.json` | load manifest or validation log inside silver/: state or validation kind; 1b names only silver/meta/gap_manifest.json for state | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/incremental_allocation_manifest.json.bak-20260630T1900Z` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/incremental_allocation_manifest.json.bak-20260630T1916Z` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/incremental_manifest.json` | load manifest or validation log inside silver/: state or validation kind; 1b names only silver/meta/gap_manifest.json for state | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/incremental_realized_manifest.json` | load manifest or validation log inside silver/: state or validation kind; 1b names only silver/meta/gap_manifest.json for state | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/incremental_unrealized_manifest.json` | load manifest or validation log inside silver/: state or validation kind; 1b names only silver/meta/gap_manifest.json for state | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/interpolated_prices.parquet` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/interpolated_prices_summary.json` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/prices/` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `silver/transactions_enriched/` | the sample key is a completion marker or diagnostic artifact (state or diagnostic kind); 1b gives only the eclipse completion markers a state row, so no row places this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `smartx/jwt/` | smartx JWT credential key: 1b decides only orion/jwt/current.json (FWD-8); no row places this one | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `smartx/raw/enterprises_aum/` | smartx raw API dumps: raw is not a tier in 1b and the table does not say whether it is bronze | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `smartx/raw/holdings/` | smartx raw API dumps: raw is not a tier in 1b and the table does not say whether it is bronze | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `smartx/raw/models/` | smartx raw API dumps: raw is not a tier in 1b and the table does not say whether it is bronze | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `ssm-output/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `status/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `temp/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `tmp/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-bd` | `v4_output/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `/advisors/` | leading-slash key; 1b places no leading-slash key | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `/clients/` | leading-slash key; 1b places no leading-slash key | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `/firm/` | leading-slash key; 1b places no leading-slash key | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `_compare/unified_proof_20260630/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `_pre_rebuild_backup/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `_rebuild_status/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `_scratch/indexbytes-face/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `_toolprobe_scratch/comp-freshness/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `_toolprobe_scratch/pk/silver/toolprobe/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/_restore_exercise_20260715T225000Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/aor_ledger_pre_reseed_20260716T012840Z/aor_ledger/events/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/aor_ledger_pre_reseed_20260716T012840Z/aor_ledger_state.parquet` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/gold_canonical_PRE_REDERIVE_20260713T1012Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/pre_exclusion_dispatch_20260715T2335Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/pre_pullheal_20260716T0218Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/pre_rescue_20260715T2259Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/advisors/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/firm/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `backup/served_spine_PRE_TIMELOCK_2026-07-13T184646Z/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `bronze/_parity-snapshot/` | parity snapshot, QA copy, completion marker or chain-summary output under bronze/ or silver/: not bronze or silver data by what it is, and no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `bronze/eclipse/` | MIXED: dated eclipse bronze dirs (class d HOME) beside _history/ history copies (no 1b row); no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `bronze/eclipse_qa/` | parity snapshot, QA copy, completion marker or chain-summary output under bronze/ or silver/: not bronze or silver data by what it is, and no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `bronze/logs/inf-bronze-runner/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `bronze/logs/inf-gold-runner/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `bronze/orion-api/` | the sample key is a completion marker or diagnostic artifact (state or diagnostic kind); 1b gives only the eclipse completion markers a state row, so no row places this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `diagnostic/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `eclipse/browser-profile/` | browser profile state; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/_rebuild/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/canonical/` | MIXED: flat parquet files directly under gold/canonical/ (not the `{t}/...` shape) beside role_aua/ (class b `{t}/...`); no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/classification/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/dimensions/_aor_exercise/aor_attribution_comparison/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/dimensions/aor_ledger/events/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/dimensions/dim_inf_advisor_office.csv` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/dispatch-lock.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/eclipse/` | MIXED (by the 1b table itself): `_meta/dispatch_eclipse_status.json` and eclipse gold output beside `{*}/_meta/gold_complete.json` markers that 1b gives to state (class c, `eclipse/inflection/state/complete/**`); the sample key is not a gold_complete.json; no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/logs/` | MIXED: flat chain logs beside inf-exporter/ output; logs, and no 1b row places logs | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/meta/pipeline-failed.json` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/meta/pull-complete.json` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/meta/schemas/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/meta/valgate-baseline/silver_transactions/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/perf_report.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `gold/timeseries/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `investor-reporting/directory/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `investor-reporting/qa/directory/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `investor-reporting/qa/holdings/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/backfill_progress_2a0c2a94-ab97-47bb-a22f-f194db318145.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/backfill_progress_2f0abf97-249e-40d8-894a-c464578adbf4.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/backfill_progress_4558ff63-5cd2-4eec-a3e4-7b575e74d319.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/backfill_progress_56b947d9-c82a-43ea-8f85-7db8f0e5354d.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/backfill_progress_d46faee5-ee79-42ff-85a5-b4d9c4f2ed0b.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/backfill_progress_ea9e59a8-0527-4bc9-9871-e8edcb805b5d.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/browser-profile/` | browser profile state; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/jwt/trigger-mode.json` | trigger-mode state: 1b places blackdiamond/{49f,cot}/session-trigger-mode.json and decides orion/jwt/current.json, but names no orion/jwt/trigger-mode.json | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_accounts_v2.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_activity.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_assets_v2.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_billing.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_household.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_household_rep_mapping.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_performance.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_performance_f1validate.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_positions_mv.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_probe.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `orion/rate_limit_state_transactions.json` | orion rate-limit or backfill-progress state: state kind, but 1b names only otp/state.json and the trigger-mode files, so no row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `otp/debug/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/_rebuild/` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/clients/` | MIXED: entity-id client JSON (class a platinum) beside _quarantine_scope_bug_20260424/ quarantined copies (995 objects; not served platinum, no 1b row); no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_meta/` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/clients_tab.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/dashboard.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/filters/` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/header_metrics.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/leaderboard.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_annual.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_monthly.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_quarterly.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/timeseries_chart.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_quarantine_scope_bug_20260424/timeseries_overview.json` | rebuild staging, rollback, quarantine or reconciliation-output copies under platinum/: not served platinum by what they are, and no 1b row places them | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `platinum/firm/_rollback/` | backup or rollback copy; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `qa/_diag/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `qa/advisors/` | no 1b row names this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `qa/artifacts/` | no 1b row names this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `qa/clients/` | no 1b row names this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `qa/firm/` | no 1b row names this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `qa/gold-artifacts/` | no 1b row names this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `silver/_parity-snapshot/positions_mv-2026-06-30/` | parity snapshot, QA copy, completion marker or chain-summary output under bronze/ or silver/: not bronze or silver data by what it is, and no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `silver/_silver_complete/` | parity snapshot, QA copy, completion marker or chain-summary output under bronze/ or silver/: not bronze or silver data by what it is, and no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `silver/api_dims/_chain_summary/` | parity snapshot, QA copy, completion marker or chain-summary output under bronze/ or silver/: not bronze or silver data by what it is, and no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `silver/eclipse/` | MIXED (by the 1b table itself): silver eclipse data (class d HOME) beside `{*}/_meta/silver_complete.json` markers that 1b gives to state (class c, `eclipse/inflection/state/complete/**`); no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `silver/historical_prices.parquet` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `silver/prices/` | market-price silver: its {vendor} is not derivable from the key and is not the bucket's feed vendor, and 1b's HOME needs a {vendor} | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `telemetry/inf-gold-layer-runner/history/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-inf` | `telemetry/inf-gold-layer-runner/status.json` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `bronze/` | the sample key is a completion marker or diagnostic artifact (state or diagnostic kind); 1b gives only the eclipse completion markers a state row, so no row places this class | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/_retry_net/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/account_attributes/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/allocations/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/holdings/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/realized/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/transactions/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `forwardfill_v2/unrealized/` | MIXED (named in CENSUS.md): dated forwardfill data files beside _complete/ markers (state kind), and no 1b row names forwardfill_v2/ | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/account_performance.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/accounts_dimension_latest.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/advisor_assignments_history.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/canonical/nna_validation/` | a gold/ path that no 1b row names | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/client_dimension.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/client_performance.parquet` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/client_timeseries/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/firm_composition.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/firm_mix_views.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/firm_mix_views_daily.json` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/logs/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/partner_analytics/` | a gold/ root file or directory that no 1b row names (1b names specific gold directories only) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/timeseries/account_performance.parquet` | a parquet file directly under gold/timeseries/: the 1b cell is `gold/timeseries/{t}/...` (a table directory), so this shape is not placed | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `gold/timeseries/client_performance.parquet` | a parquet file directly under gold/timeseries/: the 1b cell is `gold/timeseries/{t}/...` (a table directory), so this shape is not placed | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `investor-reporting/directory/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `investor-reporting/qa/directory/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `investor-reporting/qa/holdings/` | no 1b row names investor-reporting/ (the note says its source is irpt, but gives no tier, class or disposition for it) | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `logs/` | log, diagnostic, scratch or run output; no 1b row places it | `ADVI_FIRMBKTS-D1-W1-S2` |
| `opal-data-cot` | `silver/` | MIXED: silver table dirs (class d HOME) beside dated {date}/_meta/ marker dirs (state kind, class c; 1b has no row for them); no single 1b row covers every kind | `ADVI_FIRMBKTS-D1-W1-S2` |
