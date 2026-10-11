# ADVI_FIRMBKTS round 2 -- mapping table v2 (FB-e-1, worker 0.9.0_WK_ADVI_FIRMBKTS~4)

Human view of `mapping_v2.json`, which supersedes round 1's `mapping.json`. Client entity ids are written `{id}`.
Denominators: 444 census classes and 238,861 census objects (census listed_at 2026-10-09T20:36:32Z). The 226 round-1 FAULT classes were re-listed live on 2026-10-11T04:01:07Z: 114,349 objects (census 114,045 for the same classes; the drift is new objects written after 2026-10-09). Re-grid counts use the live listing.

## 1. Counts per disposition

| accounting | classes |
|---|---|
| round-1 placed, retired or decided, copied unchanged (1b) | 216 (MOVE 130, HOME 77, RETIRE 7, DECISION 2) |
| round-1 placed MOVE classes turned FAULT by the 1e overlap ruling (issuer commit 2ca0be7c81) | 2 |
| round-1 FAULT classes re-gridded (no own row; children below) | 24 parents |
| round-1 FAULT classes with an own row | 202 (RETIRE 73, MOVE 58, HOME 13, FAULT 58) |
| census classes accounted (216 copied + 2 overlap-FAULT + 226 round-1 FAULT) | 444 of 444 |

Rows in `mapping_v2.json`: 498 = 216 copied + 2 round-1 MOVE turned FAULT + 280 new (own rows 202, re-grid children 78). By disposition: MOVE 212, HOME 110, RETIRE 85, FAULT 89, DECISION 2.

Census objects in the own-row FAULT classes: 35,087 of 238,861. The re-grid parents keep FAULT remainders (section 3) and their live counts sit in the children rows.

## 2. Changed classes, per bucket (prefix, disposition, rule)

### opal-data-bd

| prefix | disposition | rule | note |
|---|---|---|---|
| GOOD_RUN_2026-01-21_1015AM/ | RETIRE | RA |  |
| _rollback/49f-20260630-preflip/ | RETIRE | RA |  |
| ajb_workspace/logs/sessions/ | RETIRE | RB |  |
| backfill_v2/assets/ | HOME | RH2 | child of backfill_v2/ |
| backfill_v2/ | FAULT | 1c | child of backfill_v2/ excludes backfill_v2/assets/ |
| bronze/bi/ | HOME | RH4 | child of bronze/ |
| bronze/fees/ | HOME | RH4 | child of bronze/ |
| bronze/ | FAULT | 1e collision | child of bronze/ excludes bronze/bi/, bronze/fees/ |
| canonical/silver/dim_account/ | FAULT | 1c |  |
| canonical/silver/fact_position/ | FAULT | 1c |  |
| debug/download-button-error.png | RETIRE | RB |  |
| debug/download-daily-error.png | RETIRE | RB |  |
| debug/error-final.png | RETIRE | RB |  |
| debug/txn-debug-211841/ | RETIRE | RB |  |
| debug/txn-query-timeout.png | RETIRE | RB |  |
| diagnostics/ | RETIRE | RB |  |
| forwardfill_v2/TXN_2026-01-16.xlsx | HOME | RH3 |  |
| forwardfill_v2/TXN_2026-01-19.xlsx | HOME | RH3 |  |
| forwardfill_v2/TXN_2026-01-21.xlsx | HOME | RH3 |  |
| forwardfill_v2/TXN_2026-01-22.xlsx | HOME | RH3 |  |
| forwardfill_v2/TXN_2026-01-23.xlsx | HOME | RH3 |  |
| forwardfill_v2/TXN_2026-01-26.xlsx | HOME | RH3 |  |
| forwardfill_v2/TXN_2026-01-27.xlsx | HOME | RH3 |  |
| forwardfill_v2/_perm_probe_1782839405.txt | RETIRE | RB |  |
| forwardfill_v2/allocations/_complete/ | FAULT | 1e collision | child of forwardfill_v2/allocations/ |
| forwardfill_v2/allocations/ | HOME | RH2 | child of forwardfill_v2/allocations/ excludes forwardfill_v2/allocations/_complete/ |
| forwardfill_v2/assets/ | HOME | RH2 |  |
| forwardfill_v2/realized/_complete/ | FAULT | 1e collision | child of forwardfill_v2/realized/ |
| forwardfill_v2/realized/ | HOME | RH2 | child of forwardfill_v2/realized/ excludes forwardfill_v2/realized/_complete/ |
| forwardfill_v2/transactions/_complete/ | FAULT | 1e collision | child of forwardfill_v2/transactions/ |
| forwardfill_v2/transactions/ | HOME | RH2 | child of forwardfill_v2/transactions/ excludes forwardfill_v2/transactions/_complete/ |
| forwardfill_v2/unrealized/_complete/ | FAULT | 1e collision | child of forwardfill_v2/unrealized/ |
| forwardfill_v2/unrealized/ | HOME | RH2 | child of forwardfill_v2/unrealized/ excludes forwardfill_v2/unrealized/_complete/ |
| gldrst/preflight/ | RETIRE | RB |  |
| gold/.checkpoints/ | MOVE | RS1 |  |
| gold/_deprecated/ | RETIRE | RC |  |
| gold/_regen_backup_20260706T1923Z/ | RETIRE | RA |  |
| gold/account_performance.parquet | FAULT | 1e collision |  |
| gold/account_quality_tiers.parquet | FAULT | 1e collision |  |
| gold/accounts_dimension_latest.parquet | MOVE | RG2 |  |
| gold/advisor_assignments_history.parquet | MOVE | RG2 |  |
| gold/advisor_rolling_flows.json | FAULT | 1e collision |  |
| gold/advisors/ | FAULT | 1e collision |  |
| gold/architect_leaderboard.json | FAULT | 1e collision |  |
| gold/aua_certification/ | MOVE | RG3 |  |
| gold/canonical/nna_validation/ | MOVE | RG3 |  |
| gold/client_dimension.parquet | MOVE | RG2 |  |
| gold/client_performance.parquet | FAULT | 1e collision |  |
| gold/client_timeseries/ | MOVE | RG3 |  |
| gold/clients/ | FAULT | 1c |  |
| gold/clients_tab.json | FAULT | 1e collision |  |
| gold/cohorts/cohorts.json | MOVE | RG3 | child of gold/cohorts/ |
| gold/cohorts/ | FAULT | 1c | child of gold/cohorts/ excludes gold/cohorts/cohorts.json |
| gold/config/ | FAULT | 1c |  |
| gold/consolidated/ | FAULT | 1c |  |
| gold/daily/positions/ | MOVE | RG4 |  |
| gold/filters/dimensions.json | MOVE | RG3 | child of gold/filters/ |
| gold/filters/ | FAULT | 1c | child of gold/filters/ excludes gold/filters/dimensions.json |
| gold/firm_composition.json | FAULT | 1e collision |  |
| gold/firm_mix_views.json | FAULT | 1e collision |  |
| gold/firm_mix_views_daily.json | FAULT | 1e collision |  |
| gold/holdings_lots/ | MOVE | RG4 |  |
| gold/implementor_leaderboard.json | FAULT | 1e collision |  |
| gold/logs/ | RETIRE | RB |  |
| gold/nna/breakdown.json | MOVE | RG3 | child of gold/nna/ |
| gold/nna/summary.json | MOVE | RG3 | child of gold/nna/ |
| gold/nna/timeseries.json | MOVE | RG3 | child of gold/nna/ |
| gold/nna/ | FAULT | 1c | child of gold/nna/ excludes gold/nna/breakdown.json, gold/nna/summary.json, gold/nna/timeseries.json |
| gold/partner_analytics/ | MOVE | RG3 |  |
| gold/perf_history/ | MOVE | RG3 |  |
| gold/perf_report.json | FAULT | 1e collision |  |
| gold/pipeline-complete.json | FAULT | 1e collision |  |
| gold/snapshots/aua_by_account_type.json | MOVE | RG3 | child of gold/snapshots/ |
| gold/snapshots/aua_by_architect.json | MOVE | RG3 | child of gold/snapshots/ |
| gold/snapshots/aua_by_region.json | MOVE | RG3 | child of gold/snapshots/ |
| gold/snapshots/aua_by_relationship.json | MOVE | RG3 | child of gold/snapshots/ |
| gold/snapshots/aua_by_state.json | MOVE | RG3 | child of gold/snapshots/ |
| gold/snapshots/aua_by_tax_status.json | MOVE | RG3 | child of gold/snapshots/ |
| gold/snapshots/ | FAULT | 1c | child of gold/snapshots/ excludes gold/snapshots/aua_by_account_type.json, gold/snapshots/aua_by_architect.json, gold/snapshots/aua_by_region.json, gold/snapshots/aua_by_relationship.json, gold/snapshots/aua_by_state.json, gold/snapshots/aua_by_tax_status.json |
| gold/summary/header_metrics.json | MOVE | RG3 | child of gold/summary/ |
| gold/summary/ | FAULT | 1c | child of gold/summary/ excludes gold/summary/header_metrics.json |
| gold/synthetic_positions_index.parquet | FAULT | 1e collision |  |
| gold/timeseries/account_performance.parquet | FAULT | 1e collision | child of gold/timeseries/ |
| gold/timeseries/account_quality_tiers.parquet | FAULT | 1e collision | child of gold/timeseries/ |
| gold/timeseries/client_performance.parquet | FAULT | 1e collision | child of gold/timeseries/ |
| gold/timeseries/holdings_lots/ | MOVE | RG4 | child of gold/timeseries/ |
| gold/timeseries/holdings_lots_shadow/ | MOVE | RG4 | child of gold/timeseries/ |
| gold/timeseries/positions_cube/ | MOVE | RG4 | child of gold/timeseries/ |
| gold/timeseries/synthetic_positions_index.parquet | FAULT | 1e collision | child of gold/timeseries/ |
| gold/timeseries/ | FAULT | 1c | child of gold/timeseries/ excludes gold/timeseries/account_performance.parquet, gold/timeseries/account_quality_tiers.parquet, gold/timeseries/client_performance.parquet, gold/timeseries/holdings_lots/, gold/timeseries/holdings_lots_shadow/, gold/timeseries/positions_cube/, gold/timeseries/synthetic_positions_index.parquet |
| gold/timeseries_chart.json | FAULT | 1e collision |  |
| investor-reporting/directory/ | MOVE | RI1 |  |
| investor-reporting/qa/directory/ | MOVE | RI1 |  |
| investor-reporting/qa/holdings/ | MOVE | RI1 |  |
| lambda-deploy/ | FAULT | 1c |  |
| lambda-layers/ | FAULT | 1c |  |
| lambda-packages/ | FAULT | 1c |  |
| logs/ssm-runs/ | RETIRE | RA | child of logs/ |
| logs/ | RETIRE | RB | child of logs/ excludes logs/ssm-runs/ |
| qa-scratch/ds1_run5_log.txt | RETIRE | RB |  |
| qa-scratch/ds1_run6_log.txt | RETIRE | RB |  |
| qa-scratch/ds1_validate/ | RETIRE | RB |  |
| qa-scratch/gate2_unit_delta_run7.parquet | RETIRE | RB |  |
| runs/ | RETIRE | RA |  |
| schwab/silver/rps/ | FAULT | 1c |  |
| scripts/diagnostics/ | RETIRE | RB | child of scripts/ |
| scripts/ | FAULT | 1c | child of scripts/ excludes scripts/diagnostics/ |
| silver/aua_validation_log.parquet | FAULT | 1c |  |
| silver/bd_transactions_backup_2026-01-20.parquet | RETIRE | RA |  |
| silver/bd_transactions_backup_2026-01-28.parquet | RETIRE | RA |  |
| silver/historical_dividends.parquet | FAULT | 1c |  |
| silver/historical_prices.parquet | FAULT | 1c |  |
| silver/historical_prices_20260213.parquet | FAULT | 1c |  |
| silver/historical_prices_final.parquet | FAULT | 1c |  |
| silver/incremental_allocation_manifest.json | MOVE | RS2 |  |
| silver/incremental_allocation_manifest.json.bak-20260630T1900Z | RETIRE | RA |  |
| silver/incremental_allocation_manifest.json.bak-20260630T1916Z | RETIRE | RA |  |
| silver/incremental_manifest.json | MOVE | RS2 |  |
| silver/incremental_realized_manifest.json | MOVE | RS2 |  |
| silver/incremental_unrealized_manifest.json | MOVE | RS2 |  |
| silver/interpolated_prices.parquet | FAULT | 1c |  |
| silver/interpolated_prices_summary.json | FAULT | 1c |  |
| silver/prices/ | FAULT | 1c |  |
| silver/transactions_enriched/_DIAGNOSTIC_ARTIFACT.txt | RETIRE | RB | child of silver/transactions_enriched/ |
| silver/transactions_enriched/ | HOME | RH4 | child of silver/transactions_enriched/ excludes silver/transactions_enriched/_DIAGNOSTIC_ARTIFACT.txt |
| smartx/jwt/ | FAULT | 1c |  |
| smartx/raw/enterprises_aum/ | HOME | RH1 |  |
| smartx/raw/holdings/ | HOME | RH1 |  |
| smartx/raw/models/ | HOME | RH1 |  |
| ssm-output/ | RETIRE | RB |  |
| status/ | MOVE | RS3 |  |
| temp/ | RETIRE | RB |  |
| tmp/ | RETIRE | RB |  |
| v4_output/ | RETIRE | RA |  |

### opal-data-inf

| prefix | disposition | rule | note |
|---|---|---|---|
| /advisors/ | FAULT | 1c |  |
| /clients/ | FAULT | 1c |  |
| /firm/ | FAULT | 1c |  |
| _compare/unified_proof_20260630/ | RETIRE | RA |  |
| _pre_rebuild_backup/ | RETIRE | RA |  |
| _rebuild_status/ | RETIRE | RA |  |
| _scratch/indexbytes-face/ | RETIRE | RB |  |
| _toolprobe_scratch/comp-freshness/ | RETIRE | RB |  |
| _toolprobe_scratch/pk/silver/toolprobe/ | RETIRE | RB |  |
| backup/_restore_exercise_20260715T225000Z/ | RETIRE | RA |  |
| backup/aor_ledger_pre_reseed_20260716T012840Z/aor_ledger/events/ | RETIRE | RA |  |
| backup/aor_ledger_pre_reseed_20260716T012840Z/aor_ledger_state.parquet | RETIRE | RA |  |
| backup/gold_canonical_PRE_REDERIVE_20260713T1012Z/ | RETIRE | RA |  |
| backup/pre_exclusion_dispatch_20260715T2335Z/ | RETIRE | RA |  |
| backup/pre_pullheal_20260716T0218Z/ | RETIRE | RA |  |
| backup/pre_rescue_20260715T2259Z/ | RETIRE | RA |  |
| backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/advisors/ | RETIRE | RA |  |
| backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/firm/ | RETIRE | RA |  |
| backup/served_spine_PRE_TIMELOCK_2026-07-13T184646Z/ | RETIRE | RA |  |
| bronze/_parity-snapshot/ | RETIRE | RA |  |
| bronze/eclipse/ | FAULT | 1c |  |
| bronze/eclipse_qa/ | FAULT | 1c |  |
| bronze/logs/inf-bronze-runner/ | RETIRE | RB |  |
| bronze/logs/inf-gold-runner/ | RETIRE | RB |  |
| bronze/orion-api/ | FAULT | 1c |  |
| diagnostic/ | RETIRE | RB |  |
| eclipse/browser-profile/ | MOVE | RS8 |  |
| gold/_rebuild/ | RETIRE | RA |  |
| gold/canonical/ | FAULT | 1c |  |
| gold/classification/ | FAULT | 1c |  |
| gold/dimensions/_aor_exercise/aor_attribution_comparison/ | FAULT | 1c |  |
| gold/dimensions/aor_ledger/events/ | FAULT | 1c |  |
| gold/dimensions/dim_inf_advisor_office.csv | FAULT | 1c |  |
| gold/dispatch-lock.json | MOVE | RS9 |  |
| gold/eclipse/ | FAULT | 1c |  |
| gold/logs/ | RETIRE | RB |  |
| gold/meta/pipeline-failed.json | MOVE | RS9 |  |
| gold/meta/pull-complete.json | MOVE | RS9 |  |
| gold/meta/schemas/ | MOVE | RS9 |  |
| gold/meta/valgate-baseline/silver_transactions/ | MOVE | RS9 |  |
| gold/perf_report.json | MOVE | RG1 |  |
| gold/timeseries/client_performance.parquet | MOVE | RG5 | child of gold/timeseries/ |
| gold/timeseries/ | MOVE | RG5 | child of gold/timeseries/ excludes gold/timeseries/client_performance.parquet |
| investor-reporting/directory/ | MOVE | RI1 |  |
| investor-reporting/qa/directory/ | MOVE | RI1 |  |
| investor-reporting/qa/holdings/ | MOVE | RI1 |  |
| orion/backfill_progress_2a0c2a94-ab97-47bb-a22f-f194db318145.json | MOVE | RS5 |  |
| orion/backfill_progress_2f0abf97-249e-40d8-894a-c464578adbf4.json | MOVE | RS5 |  |
| orion/backfill_progress_4558ff63-5cd2-4eec-a3e4-7b575e74d319.json | MOVE | RS5 |  |
| orion/backfill_progress_56b947d9-c82a-43ea-8f85-7db8f0e5354d.json | MOVE | RS5 |  |
| orion/backfill_progress_d46faee5-ee79-42ff-85a5-b4d9c4f2ed0b.json | MOVE | RS5 |  |
| orion/backfill_progress_ea9e59a8-0527-4bc9-9871-e8edcb805b5d.json | MOVE | RS5 |  |
| orion/browser-profile/ | MOVE | RS8 |  |
| orion/jwt/trigger-mode.json | MOVE | RS7 |  |
| orion/rate_limit_state_accounts_v2.json | MOVE | RS6 |  |
| orion/rate_limit_state_activity.json | MOVE | RS6 |  |
| orion/rate_limit_state_assets_v2.json | MOVE | RS6 |  |
| orion/rate_limit_state_billing.json | MOVE | RS6 |  |
| orion/rate_limit_state_household.json | MOVE | RS6 |  |
| orion/rate_limit_state_household_rep_mapping.json | MOVE | RS6 |  |
| orion/rate_limit_state_performance.json | MOVE | RS6 |  |
| orion/rate_limit_state_performance_f1validate.json | MOVE | RS6 |  |
| orion/rate_limit_state_positions_mv.json | MOVE | RS6 |  |
| orion/rate_limit_state_probe.json | MOVE | RS6 |  |
| orion/rate_limit_state_transactions.json | MOVE | RS6 |  |
| otp/debug/ | RETIRE | RB |  |
| platinum/_rebuild/ | RETIRE | RA |  |
| platinum/clients/_quarantine_scope_bug_20260424/ | RETIRE | RA | child of platinum/clients/ |
| platinum/clients/ | MOVE | RP1 | child of platinum/clients/ excludes platinum/clients/_quarantine_scope_bug_20260424/ |
| platinum/firm/_meta/ | RETIRE | RB |  |
| platinum/firm/_quarantine_scope_bug_20260424/clients_tab.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/dashboard.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/filters/ | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/header_metrics.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/leaderboard.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/partner_analytics.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_annual.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_monthly.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/partner_analytics_quarterly.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/timeseries_chart.json | RETIRE | RA |  |
| platinum/firm/_quarantine_scope_bug_20260424/timeseries_overview.json | RETIRE | RA |  |
| platinum/firm/_rollback/ | RETIRE | RA |  |
| qa/_diag/ | RETIRE | RB |  |
| qa/advisors/ | RETIRE | RB |  |
| qa/artifacts/ | RETIRE | RB |  |
| qa/clients/ | RETIRE | RB |  |
| qa/firm/ | RETIRE | RB |  |
| qa/gold-artifacts/ | RETIRE | RB |  |
| silver/_parity-snapshot/positions_mv-2026-06-30/ | RETIRE | RA |  |
| silver/_silver_complete/ | HOME | RH4 |  |
| silver/api_dims/_chain_summary/ | HOME | RH4 |  |
| silver/eclipse/ | FAULT | 1c |  |
| silver/historical_prices.parquet | FAULT | 1c |  |
| silver/prices/ | FAULT | 1c |  |
| telemetry/inf-gold-layer-runner/history/ | FAULT | 1c |  |
| telemetry/inf-gold-layer-runner/status.json | FAULT | 1c |  |

### opal-data-cot

| prefix | disposition | rule | note |
|---|---|---|---|
| bronze/ | FAULT | 1e collision |  |
| forwardfill_v2/_retry_net/ | MOVE | RS10 |  |
| forwardfill_v2/account_attributes/_complete/ | FAULT | 1e collision | child of forwardfill_v2/account_attributes/ |
| forwardfill_v2/account_attributes/ | HOME | RH2 | child of forwardfill_v2/account_attributes/ excludes forwardfill_v2/account_attributes/_complete/ |
| forwardfill_v2/allocations/_complete/ | FAULT | 1e collision | child of forwardfill_v2/allocations/ |
| forwardfill_v2/allocations/ | HOME | RH2 | child of forwardfill_v2/allocations/ excludes forwardfill_v2/allocations/_complete/ |
| forwardfill_v2/holdings/_complete/ | FAULT | 1e collision | child of forwardfill_v2/holdings/ |
| forwardfill_v2/holdings/ | HOME | RH2 | child of forwardfill_v2/holdings/ excludes forwardfill_v2/holdings/_complete/ |
| forwardfill_v2/realized/_complete/ | FAULT | 1e collision | child of forwardfill_v2/realized/ |
| forwardfill_v2/realized/ | HOME | RH2 | child of forwardfill_v2/realized/ excludes forwardfill_v2/realized/_complete/ |
| forwardfill_v2/transactions/_complete/ | FAULT | 1e collision | child of forwardfill_v2/transactions/ |
| forwardfill_v2/transactions/_dryrun/ | FAULT | 1c | child of forwardfill_v2/transactions/ |
| forwardfill_v2/transactions/ | HOME | RH2 | child of forwardfill_v2/transactions/ excludes forwardfill_v2/transactions/_complete/, forwardfill_v2/transactions/_dryrun/ |
| forwardfill_v2/unrealized/_complete/ | FAULT | 1e collision | child of forwardfill_v2/unrealized/ |
| forwardfill_v2/unrealized/ | HOME | RH2 | child of forwardfill_v2/unrealized/ excludes forwardfill_v2/unrealized/_complete/ |
| gold/account_performance.parquet | FAULT | 1e collision |  |
| gold/accounts_dimension_latest.parquet | MOVE | RG2 |  |
| gold/advisor_assignments_history.parquet | MOVE | RG2 |  |
| gold/canonical/nna_validation/ | MOVE | RG3 |  |
| gold/client_dimension.parquet | MOVE | RG2 |  |
| gold/client_performance.parquet | FAULT | 1e collision |  |
| gold/client_timeseries/ | MOVE | RG3 |  |
| gold/firm_composition.json | FAULT | 1e collision |  |
| gold/firm_mix_views.json | FAULT | 1e collision |  |
| gold/firm_mix_views_daily.json | FAULT | 1e collision |  |
| gold/logs/ | RETIRE | RB |  |
| gold/partner_analytics/ | MOVE | RG3 |  |
| gold/positions_cube/ | FAULT | 1e overlap | destination-key overlap 342 of 342 keys with gold/timeseries/positions_cube/ (round-1 MOVE turned FAULT; owner 1.0.0_SA_CTO~DELL1; issuer ruling 2ca0be7c81) |
| gold/timeseries/account_performance.parquet | FAULT | 1e collision |  |
| gold/timeseries/client_performance.parquet | FAULT | 1e collision |  |
| gold/timeseries/positions_cube/ | FAULT | 1e overlap | destination-key overlap 342 of 342 keys with gold/positions_cube/ (round-1 MOVE turned FAULT; owner 1.0.0_SA_CTO~DELL1; issuer ruling 2ca0be7c81) |
| investor-reporting/directory/ | MOVE | RI1 |  |
| investor-reporting/qa/directory/ | MOVE | RI1 |  |
| investor-reporting/qa/holdings/ | MOVE | RI1 |  |
| logs/ | RETIRE | RB |  |
| silver/account_attributes/ | HOME | RH4 | child of silver/ |
| silver/allocations/ | HOME | RH4 | child of silver/ |
| silver/cot_allocations.parquet | FAULT | 1c | child of silver/ |
| silver/cot_holdings.parquet | FAULT | 1c | child of silver/ |
| silver/cot_incremental_manifest_account_attributes.json | MOVE | RS2 | child of silver/ |
| silver/cot_incremental_manifest_allocations.json | MOVE | RS2 | child of silver/ |
| silver/cot_incremental_manifest_holdings.json | MOVE | RS2 | child of silver/ |
| silver/cot_incremental_manifest_realized.json | MOVE | RS2 | child of silver/ |
| silver/cot_incremental_manifest_transactions.json | MOVE | RS2 | child of silver/ |
| silver/cot_incremental_manifest_unrealized.json | MOVE | RS2 | child of silver/ |
| silver/cot_transactions.parquet | FAULT | 1c | child of silver/ |
| silver/holdings/ | HOME | RH4 | child of silver/ |
| silver/prices/ | FAULT | 1c | child of silver/ |
| silver/realized/ | HOME | RH4 | child of silver/ |
| silver/transactions/ | HOME | RH4 | child of silver/ |
| silver/unrealized/ | HOME | RH4 | child of silver/ |
| silver/ | FAULT | 1e collision | child of silver/ excludes silver/account_attributes/, silver/allocations/, silver/cot_allocations.parquet, silver/cot_holdings.parquet, silver/cot_incremental_manifest_account_attributes.json, silver/cot_incremental_manifest_allocations.json, silver/cot_incremental_manifest_holdings.json, silver/cot_incremental_manifest_realized.json, silver/cot_incremental_manifest_transactions.json, silver/cot_incremental_manifest_unrealized.json, silver/cot_transactions.parquet, silver/holdings/, silver/prices/, silver/realized/, silver/transactions/, silver/unrealized/ |

Rule ids: RA/RB/RC retire (R17, R18); RS1-RS10 state (R21); RH1-RH4 bronze/silver to opal-data-assets (R4, R9); RG1-RG5 and RP1 platinum and gold (R5, R11, R12); RI1 investor-reporting (R5). RP1 copies the bd `platinum/clients/` pattern. A class that no rule places, or whose builder call refuses, keeps a FAULT row with its reason.

## 3. Re-grids (1d)

| bucket | parent | children | parent objects (live) | children objects |
|---|---|---|---|---|
| -bd | backfill_v2/ | 2 | 292 | 292 |
| -bd | bronze/ | 3 | 215 | 215 |
| -bd | forwardfill_v2/allocations/ | 2 | 148 | 148 |
| -bd | forwardfill_v2/realized/ | 2 | 249 | 249 |
| -bd | forwardfill_v2/transactions/ | 2 | 310 | 310 |
| -bd | forwardfill_v2/unrealized/ | 2 | 91 | 91 |
| -bd | gold/cohorts/ | 2 | 2 | 2 |
| -bd | gold/filters/ | 2 | 2 | 2 |
| -bd | gold/nna/ | 4 | 4 | 4 |
| -bd | gold/snapshots/ | 7 | 7 | 7 |
| -bd | gold/summary/ | 2 | 2 | 2 |
| -bd | gold/timeseries/ | 8 | 2641 | 2641 |
| -bd | logs/ | 2 | 9209 | 9209 |
| -bd | scripts/ | 2 | 154 | 154 |
| -bd | silver/transactions_enriched/ | 2 | 519 | 519 |
| -inf | gold/timeseries/ | 2 | 2 | 2 |
| -inf | platinum/clients/ | 2 | 4202 | 4202 |
| -cot | forwardfill_v2/account_attributes/ | 2 | 84 | 84 |
| -cot | forwardfill_v2/allocations/ | 2 | 201 | 201 |
| -cot | forwardfill_v2/holdings/ | 2 | 170 | 170 |
| -cot | forwardfill_v2/realized/ | 2 | 206 | 206 |
| -cot | forwardfill_v2/transactions/ | 3 | 209 | 209 |
| -cot | forwardfill_v2/unrealized/ | 2 | 201 | 201 |
| -cot | silver/ | 17 | 809 | 809 |

Each re-grid's children sum to its parent's live count (the check's denominator). A child prefix is either a sub-directory, a root key, or the parent prefix with `exclude_prefixes` naming the sibling children.

## 4. Remaining FAULT rows, by owner and reason

Owner `1.0.0_SA_CTO~DELL1` on all 89 FAULT rows.

| count | reason |
|---|---|
| 39 | destination-key overlap (new class FAULT by collision ruling 1e) |
| 2 | destination-key overlap 342 of 342 keys: round-1 cot `gold/positions_cube/` and `gold/timeseries/positions_cube/`, both FAULT by issuer ruling 2ca0be7c81 (1e) |
| 12 | market-price silver: {vendor} is not derivable from the key and is not the bucket's feed vendor |
| 7 | no repair rule places it |
| 5 | marker at the class prefix: a re-grid child cannot share its prefix, so the marker stays in the FAULT remainder |
| 4 | silver/bronze root file, no data directory; no rule places it |
| 3 | Lambda deployment artifacts: R16 is not applied to them (PRD CONTRACTS); the home is not ruled |
| 3 | leading-slash key; 1b places no leading-slash key |
| 2 | runtime telemetry whose reader is unnamed |
| 1 | RH3: forwardfill root file whose name is not TXN_*.xlsx; no rule places it |
| 1 | zero-byte directory marker at the class prefix (gold/clients/) cannot share its prefix with the root JSON children; a per-file re-grid would need 2948 |
| 1 | RG4 dir whose object is not a date-named parquet; no rule places it |
| 1 | marker at the class prefix: a re-grid child cannot share its prefix, so the marker stays in the FAULT remainder; no repair rule places it |
| 1 | code: scripts are not data; no tier holds them |
| 1 | a live credential: moving it breaks the chain that refreshes it (FWD-8's class) |
| 1 | interleaved completion markers and data in the same directories; a prefix re-grid would need 270 children (more than 25) |
| 1 | interleaved completion markers and data in the same directories; a prefix re-grid would need 134 children (more than 25) |
| 1 | interleaved completion markers and data in the same directories; a prefix re-grid would need 3488 children (more than 25) |
| 1 | interleaved completion markers and data in the same directories; a prefix re-grid would need 265 children (more than 25) |
| 1 | interleaved completion markers and data in the same directories; a prefix re-grid would need 264 children (more than 25) |
| 1 | RH2 nested deeper than kind/file; no rule places it |

## 5. Collisions (1e)

Round-1 and new MOVE/HOME classes were grouped by (bucket, source, scope, tier, table). A destination key string is the key the builder writes (source/scope/tier/table/partition[/object]); each group was measured on the live listing and every key compared with every other class of the group.

- 28 groups with overlap 0 are ruled `merge`; their entries are in `collisions` with `overlap_keys` 0.
- Groups where a NEW class overlapped another class were ruled by making every new class of the group FAULT (owner CTO, reason `destination-key overlap ...`). 39 new classes are FAULT by this ruling.
- Round-1 classes stay unchanged (1b) EXCEPT the one permitted change (1e, issuer ruling commit 2ca0be7c81): the round-1 MOVE classes `opal-data-cot` `gold/positions_cube/` and `gold/timeseries/positions_cube/`, which share the same 171 dated keys (342 of 342 keys shared, destination `advi/cottonwood/gold/positions_cube`), are both FAULT rows, owner `1.0.0_SA_CTO~DELL1`, reason `destination-key overlap 342 of 342 keys with <the other class>`. They have no collision entry: the group is no longer a group of MOVE/HOME rows. Surfaced earlier as surprise row ADVI_FIRMBKTS-D1-W4-S1.

## 6. Method notes (round-2 conventions, all surfaced as surprise rows where the spec did not say)

- Rules are applied to each live key, in 1c order (RA, RB, RC, RS, RH, RG, RP, RI, then FAULT owners). A class is one row when every key takes one rule and table; otherwise it is re-gridded (section 3).
- RS4 completion markers match on the class or child prefix: the first segment after it is the partition and the rest the object, so a date-level marker keeps its date (surprise ADVI_FIRMBKTS-D1-W4-S2).
- A zero-byte directory marker that equals its class prefix cannot share that prefix with its re-grid children. The marker and any FAULT remainder stay in one FAULT row; the MOVE children are split out (surprise S3).
- Classes whose markers and data interleave per file would need one child per marker. Above 25 children the class stays FAULT whole (surprise S5).
- RG2, RG5 use the file stem as the table; RG4 writes `date=<date>` as the partition and `data.parquet` as the object; a `/` in a directory becomes `-` in the table (`timeseries-holdings_lots`).
- RI1 uses the first segment after `investor-reporting/`, so `investor-reporting/qa/...` gets partition `qa`.
- RH2/RH3 pass a `TXN_*.xlsx` root file to table `transactions`; other forwardfill root files stay FAULT.
- Destination keys were checked with `lib/opal_naming.py` `address()`; no address is typed by hand. Every new MOVE and HOME row passed the builder on every one of its keys.

