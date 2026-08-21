# CONSTRUCTED-KEY SWEEP -- raw per-site listing (MDPF_PROVCANON stage-3 CE half)

**Run:** 2026-08-21T17:01:17Z by `0.7.0_AE_CloudOps`  
**Requested by:** 2.0.0_SA_COO (65153, scoped) -- the CE half of postulate (i)  
**Question:** which writers/readers CONSTRUCT these artifacts' keys rather than NAMING them?  

**INSTRUMENT:** Python AST over boto3 S3 call sites (`put_object get_object copy_object
head_object delete_object delete_objects upload_file download_file upload_fileobj
download_fileobj list_objects list_objects_v2 generate_presigned_url`), classifying the
`Key` / `Prefix` / `CopySource` ARGUMENT.

**CLASSES.** `LITERAL` = a string constant (the ONLY class a token census can see).
`GENERATIVE` = f-string, concat/%, .format(), .join(), a call, or a ternary -- the key does
not exist in the source text. `NOT_MEASURABLE` = a bare variable/attribute this tracer could
not resolve (it follows same-function literal assignment, ONE hop). NOT_MEASURABLE is
**unresolved by this instrument, not absent** -- challenge these, do not count them clean.

**GENERATIVE != OPERATIVE.** A generative site is a CANDIDATE. Operativeness (does it
validate / reshape / assert a key set?) requires reading the body, which this sweep does NOT do.
Only surface 11 (`opal-assets-mdpf-portal-publisher`) was read and adjudicated.

**INSTRUMENT'S OWN DOMAIN (declared):** does NOT see shell/SSM `aws s3 cp` key building,
Terraform-declared prefixes, keys built inside an un-inlined helper, or non-Python producers.

## data/mdpf/scripts

DENOMINATOR: **50** .py files parsed, **109** key-arg call sites, 0 unparsed  
LITERAL **23** | GENERATIVE **55** | NOT_MEASURABLE **31**

| file | line | call | arg | class | evidence |
|---|---|---|---|---|---|
| `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` | 308 | get_object | Key | **NOT_MEASURABLE** | var _key (unresolved in-function) |
| `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` | 637 | put_object | Key | **LITERAL** | var JSON_TIMESERIES_KEY <- 'json/mdpf/aggregate-aua-timeseries.json' |
| `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` | 668 | put_object | Key | **GENERATIVE** | var json_key <- f-string |
| `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` | 201 | get_object | Key | **LITERAL** | var LEGACY_AUM_KEY <- 'json/portfolios/aum-timeseries.json' |
| `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` | 210 | get_object | Key | **LITERAL** | var LEGACY_NM_KEY <- 'json/portfolios/non_model_assets.json' |
| `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` | 253 | get_object | Key | **GENERATIVE** | var mpa_key <- f-string |
| `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` | 255 | get_object | Key | **GENERATIVE** | var full_key <- f-string |
| `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` | 295 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/backfill/build_mdpf_count_backfill_pre0518.py` | 94 | get_object | Key | **LITERAL** | var LEGACY_KEY <- 'json/portfolios/aum-timeseries.json' |
| `data/mdpf/scripts/backfill/build_mdpf_inflection_history_from_spine.py` | 119 | get_object | Key | **LITERAL** | var INF_CLIENT_PERF_KEY <- 'gold/timeseries/client_performance.parquet' |
| `data/mdpf/scripts/backfill/build_mdpf_inflection_history_from_spine.py` | 172 | list_objects_v2 | Prefix | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/build_mdpf_inflection_history_from_spine.py` | 185 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/build_mdpf_process_backfill.py` | 167 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/backfill/build_mdpf_process_backfill.py` | 199 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/backfill/build_mdpf_process_backfill.py` | 207 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/backfill/build_mdpf_process_backfill.py` | 224 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/backfill/build_mdpf_process_backfill.py` | 268 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/backfill/build_mdpf_v0_bandaid_backfill.py` | 358 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/build_mdpf_wsc_inflection_nonmodel_backfill.py` | 113 | get_object | Key | **LITERAL** | var JWT_KEY <- 'orion/jwt/current.json' |
| `data/mdpf/scripts/backfill/build_mdpf_wsc_inflection_nonmodel_backfill.py` | 138 | get_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `data/mdpf/scripts/backfill/build_mdpf_wsc_inflection_nonmodel_backfill.py` | 238 | list_objects_v2 | Prefix | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/build_mdpf_wsc_inflection_nonmodel_backfill.py` | 252 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/eclipse_vintage_reconstruction.py` | 163 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/eclipse_vintage_reconstruction.py` | 466 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/eclipse_vintage_reconstruction.py` | 469 | head_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/orion_0806_fact_assets_backfill.py` | 54 | head_object | Key | **LITERAL** | var DST_KEY <- 'orion/inflection/silver/fact_assets/date=2026-08-06/data.parquet' |
| `data/mdpf/scripts/backfill/orion_0806_fact_assets_backfill.py` | 62 | get_object | Key | **LITERAL** | var SRC_KEY <- 'bronze/assets/2026-08-06.parquet' |
| `data/mdpf/scripts/backfill/orion_0806_fact_assets_backfill.py` | 67 | get_object | Key | **LITERAL** | var CONTRACT_KEY <- 'orion/inflection/silver/fact_assets/date=2026-08-13/data.parquet' |
| `data/mdpf/scripts/backfill/orion_0806_fact_assets_backfill.py` | 92 | put_object | Key | **LITERAL** | var DST_KEY <- 'orion/inflection/silver/fact_assets/date=2026-08-06/data.parquet' |
| `data/mdpf/scripts/backfill/orion_0806_fact_assets_backfill.py` | 93 | head_object | Key | **LITERAL** | var DST_KEY <- 'orion/inflection/silver/fact_assets/date=2026-08-06/data.parquet' |
| `data/mdpf/scripts/backfill/patch_mdpf_per_date_partitions.py` | 104 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/backfill/patch_mdpf_per_date_partitions.py` | 116 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/backfill/patch_mdpf_per_date_partitions.py` | 235 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/bronze/pull_orion_model_composition.py` | 106 | get_object | Key | **LITERAL** | var S3_JWT_FALLBACK_KEY <- 'orion/jwt/current.json' |
| `data/mdpf/scripts/bronze/pull_orion_model_composition.py` | 183 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/bronze/pull_orion_model_composition.py` | 207 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/feeders/verify_wsd2_clears_identity2.py` | 49 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py` | 248 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/feeders/wsc_inflection_held_etf.py` | 169 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/feeders/wsc_inflection_held_etf.py` | 232 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/feeders/wsd_partner_held_etf.py` | 142 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/feeders/wsd_partner_held_etf.py` | 194 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/build_mdpf_etf_ownership_timeseries.py` | 134 | get_object | Key | **GENERATIVE** | var key <- call _aggregate_key |
| `data/mdpf/scripts/gold/build_mdpf_etf_ownership_timeseries.py` | 442 | put_object | Key | **GENERATIVE** | var key <- call _artifact_key |
| `data/mdpf/scripts/gold/build_mdpf_spine.py` | 113 | get_object | Key | **LITERAL** | 'gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json' |
| `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py` | 145 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py` | 176 | list_objects_v2 | Prefix | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py` | 182 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py` | 240 | get_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py` | 350 | get_object | Key | **LITERAL** | var INF_CLIENT_PERF_KEY <- 'gold/timeseries/client_performance.parquet' |
| `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py` | 461 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/build_mdpf_wsd2_etf_netassets_feeder.py` | 99 | get_object | Key | **LITERAL** | var ETFS_NETASSETS_KEY <- 'silver/netassets_daily.parquet' |
| `data/mdpf/scripts/gold/build_mdpf_wsd2_etf_netassets_feeder.py` | 178 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py` | 204 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py` | 508 | get_object | Key | **GENERATIVE** | var cert_key <- f-string |
| `data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py` | 702 | put_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/build_portal_gold_accrual.py` | 227 | get_object | Key | **GENERATIVE** | var src_key <- f-string |
| `data/mdpf/scripts/gold/build_portal_gold_accrual.py` | 283 | head_object | Key | **NOT_MEASURABLE** | var dst (unresolved in-function) |
| `data/mdpf/scripts/gold/build_portal_gold_accrual.py` | 290 | put_object | Key | **NOT_MEASURABLE** | var dst (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` | 88 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` | 91 | list_objects_v2 | Prefix | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` | 152 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` | 384 | get_object | Key | **LITERAL** | var COTTONWOOD_UNITS_KEY <- 'gold/mdpf_revamp/cottonwood/account_units.json' |
| `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | 290 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | 547 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | 692 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | 761 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | 1948 | get_object | Key | **LITERAL** | var key <- 'gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json' |
| `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py` | 114 | get_object | Key | **LITERAL** | var AGG_GLOBAL_KEY <- 'gold/mdpf_revamp/global/aggregate_aua_timeseries.json' |
| `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py` | 119 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py` | 594 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py` | 87 | get_object | Key | **LITERAL** | var AGG_GLOBAL_KEY <- 'gold/mdpf_revamp/global/aggregate_aua_timeseries.json' |
| `data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py` | 92 | get_object | Key | **LITERAL** | var SERVED_KEY <- 'json/portfolios/aum-timeseries.json' |
| `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py` | 145 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py` | 222 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py` | 436 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` | 253 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` | 537 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` | 571 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` | 1361 | get_object | Key | **NOT_MEASURABLE** | var key <- Tuple |
| `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` | 1378 | put_object | Key | **NOT_MEASURABLE** | var key <- Tuple |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 493 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 545 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 555 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 557 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 606 | get_object | Key | **GENERATIVE** | concat/% |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 904 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 907 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 1025 | put_object | Key | **GENERATIVE** | var mkey <- f-string |
| `data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py` | 137 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py` | 160 | get_object | Key | **GENERATIVE** | format() |
| `data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py` | 184 | get_object | Key | **GENERATIVE** | format() |
| `data/mdpf/scripts/gold/stage_mdpf_revamp_trio.py` | 79 | put_object | Key | **NOT_MEASURABLE** | var key <- attr/subscript |
| `data/mdpf/scripts/gold/stage_mdpf_revamp_trio.py` | 81 | get_object | Key | **NOT_MEASURABLE** | var key <- attr/subscript |
| `data/mdpf/scripts/gold/validate_schwab_native_custody.py` | 77 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/gold/verify_mdpf_revamp_conditions.py` | 54 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/mdpf/scripts/probes/mdpf011_bd_validate.py` | 82 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/probes/mdpf011_bd_validate.py` | 133 | get_object | Key | **GENERATIVE** | f-string |
| `data/mdpf/scripts/probes/mdpf011_fingerprint_probe.py` | 106 | get_object | Key | **LITERAL** | var RPS_KEY <- 'schwab/silver/rps/date=20260515/data.parquet' |
| `data/mdpf/scripts/probes/mdpf011_full_match.py` | 195 | get_object | Key | **LITERAL** | var RPS_KEY <- 'schwab/silver/rps/date=20260515/data.parquet' |
| `data/mdpf/scripts/probes/mdpf011_match.py` | 83 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `data/mdpf/scripts/probes/mdpf011_rematch.py` | 63 | head_object | Key | **GENERATIVE** | var silver <- f-string |
| `data/mdpf/scripts/probes/mdpf011_rematch.py` | 65 | get_object | Key | **GENERATIVE** | var silver <- f-string |
| `data/mdpf/scripts/probes/mdpf011_rematch.py` | 70 | get_object | Key | **GENERATIVE** | var raw_key <- f-string |
| `data/mdpf/scripts/probes/mdpf012_smartx_bucket_history_probe.py` | 44 | get_object | Key | **LITERAL** | 'consolidated/smartx_allocations.parquet' |
| `data/mdpf/scripts/probes/mdpf012_smartx_bucket_history_probe.py` | 84 | get_object | Key | **NOT_MEASURABLE** | var sample_key <- attr/subscript |
| `data/mdpf/scripts/probes/mdpf012_smartx_bucket_history_probe.py` | 121 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/mdpf/scripts/probes/mdpf012_smartx_bucket_history_probe.py` | 135 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/mdpf/scripts/probes/rc1_version_concordance_check.py` | 97 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |

## data/assets/scripts/gold

DENOMINATOR: **72** .py files parsed, **51** key-arg call sites, 0 unparsed  
LITERAL **6** | GENERATIVE **31** | NOT_MEASURABLE **14**

| file | line | call | arg | class | evidence |
|---|---|---|---|---|---|
| `data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py` | 173 | list_objects_v2 | Prefix | **GENERATIVE** | var prefix <- f-string |
| `data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py` | 196 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py` | 710 | get_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py` | 736 | put_object | Key | **LITERAL** | var STAGING_KEY <- 'gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries_interpolated.jso |
| `data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py` | 738 | list_objects_v2 | Prefix | **LITERAL** | var STAGING_KEY <- 'gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries_interpolated.jso |
| `data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` | 388 | put_object | Key | **GENERATIVE** | var key <- f-string |
| `data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` | 390 | list_objects_v2 | Prefix | **GENERATIVE** | var key <- f-string |
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | 211 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | 384 | get_object | Key | **GENERATIVE** | f-string |
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | 815 | get_object | Key | **GENERATIVE** | var ONEOFF_BACKFILL_KEY <- concat/% |
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | 981 | put_object | Key | **GENERATIVE** | var SLICE_KEY <- concat/% |
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | 983 | head_object | Key | **GENERATIVE** | var SLICE_KEY <- concat/% |
| `data/assets/scripts/gold/build_dim_model_portfolio.py` | 103 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/build_dim_model_portfolio.py` | 535 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `data/assets/scripts/gold/build_dim_model_portfolio.py` | 536 | head_object | Key | **GENERATIVE** | var key <- concat/% |
| `data/assets/scripts/gold/build_dim_taxsma_report.py` | 108 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/build_dim_taxsma_report.py` | 277 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `data/assets/scripts/gold/cottonwood_aua.py` | 118 | get_object | Key | **GENERATIVE** | var key <- format() |
| `data/assets/scripts/gold/cottonwood_aua.py` | 147 | get_object | Key | **LITERAL** | var CASH_KEY <- 'gold/platinum/firm/cash_coverage_summary.json' |
| `data/assets/scripts/gold/runners_49f/a00_runner.py` | 80 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/a00_runner.py` | 91 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/a00_runner.py` | 166 | put_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/a00_runner.py` | 167 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/a01_runner.py` | 71 | put_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/a01_runner.py` | 82 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/a07_dim_asset_classification.py` | 83 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/bd49f_dim_portfolio_group.py` | 356 | head_object | Key | **GENERATIVE** | var key <- concat/% |
| `data/assets/scripts/gold/runners_49f/c00_runner.py` | 164 | put_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/c00_runner.py` | 172 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/c01_runner.py` | 121 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/c01_runner.py` | 127 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/c02_runner.py` | 119 | put_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/c02_runner.py` | 123 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/c03_runner.py` | 60 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/c03_runner.py` | 154 | put_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/c03_runner.py` | 160 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/d00_served_shape_census.py` | 149 | head_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/d00_served_shape_census.py` | 154 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/d06_firm_mix_summary.py` | 242 | get_object | Key | **LITERAL** | 'platinum/firm/mix_summary.json' |
| `data/assets/scripts/gold/runners_49f/d_publisher_port.py` | 431 | head_object | Key | **GENERATIVE** | var serve_key <- f-string |
| `data/assets/scripts/gold/runners_49f/d_publisher_port.py` | 446 | list_objects_v2 | Prefix | **GENERATIVE** | var serve_key <- f-string |
| `data/assets/scripts/gold/runners_49f/d_publisher_port.py` | 558 | put_object | Key | **GENERATIVE** | var mkey <- f-string |
| `data/assets/scripts/gold/runners_49f/d_publisher_port.py` | 560 | put_object | Key | **GENERATIVE** | f-string |
| `data/assets/scripts/gold/runners_49f/dryfit_driver.py` | 105 | get_object | Key | **LITERAL** | var SEED_ATTRIB_KEY <- 'canonical/schwab/gold/advisor_attribution/date=2026-07-06/data.parque |
| `data/assets/scripts/gold/runners_49f/dryfit_driver.py` | 106 | get_object | Key | **LITERAL** | var XREF_KEY <- 'blackdiamond/49f/silver/dim_account_xref/date=2026-07-14/data.parquet |
| `data/assets/scripts/gold/runners_49f/fit_harness.py` | 105 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/runner_common.py` | 82 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `data/assets/scripts/gold/runners_49f/runner_common.py` | 124 | put_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/runner_common.py` | 125 | put_object | Key | **GENERATIVE** | var man_key <- f-string |
| `data/assets/scripts/gold/runners_49f/runner_common.py` | 134 | get_object | Key | **GENERATIVE** | var data_key <- f-string |
| `data/assets/scripts/gold/runners_49f/runner_common.py` | 151 | get_object | Key | **GENERATIVE** | var key <- f-string |

## infra/aws/lambda/opal-assets

DENOMINATOR: **76** .py files parsed, **112** key-arg call sites, 0 unparsed  
LITERAL **1** | GENERATIVE **61** | NOT_MEASURABLE **50**

| file | line | call | arg | class | evidence |
|---|---|---|---|---|---|
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py` | 165 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py` | 166 | list_objects_v2 | Prefix | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py` | 324 | get_object | Key | **LITERAL** | var PULL_STATE_KEY <- 'blackdiamond/49f/_ops/pull_state.json' |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py` | 341 | get_object | Key | **GENERATIVE** | call _sidecar_key |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py` | 510 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py` | 673 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/stream_parquet.py` | 136 | put_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py` | 240 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py` | 243 | list_objects_v2 | Prefix | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_registry.py` | 66 | get_object | Key | **GENERATIVE** | var ROSTER_KEY <- call get |
| `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_resolver.py` | 67 | get_object | Key | **GENERATIVE** | var key <- call _latest_xref_key |
| `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py` | 225 | get_object | Key | **GENERATIVE** | var key <- f-string |
| `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py` | 507 | get_object | Key | **GENERATIVE** | var COT_PAIR_SERIES_KEY <- call get |
| `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py` | 773 | get_object | Key | **GENERATIVE** | var key <- call _latest_partner_key |
| `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py` | 965 | get_object | Key | **GENERATIVE** | var key <- call _latest_partner_key |
| `infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py` | 369 | get_object | Key | **NOT_MEASURABLE** | var src_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py` | 477 | copy_object | CopySource | **NOT_MEASURABLE** | Dict |
| `infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py` | 477 | copy_object | Key | **GENERATIVE** | var dk <- call _dst_key |
| `infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py` | 487 | list_objects_v2 | Prefix | **GENERATIVE** | var dk <- call _dst_key |
| `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` | 117 | list_objects_v2 | Prefix | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` | 196 | get_object | Key | **GENERATIVE** | call _latest_pointer_key |
| `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` | 211 | get_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` | 236 | put_object | Key | **GENERATIVE** | var serve_key <- f-string |
| `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` | 328 | put_object | Key | **GENERATIVE** | var mkey <- f-string |
| `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` | 343 | put_object | Key | **GENERATIVE** | call _latest_pointer_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/backfill_status.py` | 226 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/backfill_status.py` | 246 | put_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/backfill_status.py` | 249 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 351 | put_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 352 | get_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 364 | head_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 478 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 508 | get_object | Key | **GENERATIVE** | var sc_key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 560 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 627 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 842 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` | 843 | get_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 366 | head_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 379 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 380 | head_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 451 | get_object | Key | **GENERATIVE** | call stamp_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 580 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 590 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py` | 604 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/stream_parquet.py` | 136 | put_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/backfill_status.py` | 226 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/backfill_status.py` | 246 | put_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/backfill_status.py` | 249 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 296 | put_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 297 | get_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 309 | head_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 328 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 359 | get_object | Key | **GENERATIVE** | var sc_key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 411 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 478 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 604 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` | 605 | get_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/stream_parquet.py` | 136 | put_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/backfill_status.py` | 226 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/backfill_status.py` | 246 | put_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/backfill_status.py` | 249 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/etf_conversion.py` | 227 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/etf_conversion.py` | 281 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/etf_conversion.py` | 393 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/etf_conversion.py` | 394 | get_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 298 | put_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 299 | get_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 311 | head_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 425 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 455 | get_object | Key | **GENERATIVE** | var sc_key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 507 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 574 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 700 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` | 701 | get_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-etf/stream_parquet.py` | 136 | put_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/backfill_status.py` | 226 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/backfill_status.py` | 246 | put_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/backfill_status.py` | 249 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 298 | put_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 299 | get_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 311 | head_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 425 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 455 | get_object | Key | **GENERATIVE** | var sc_key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 507 | get_object | Key | **NOT_MEASURABLE** | var k (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 574 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 700 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` | 701 | get_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-orion/stream_parquet.py` | 136 | put_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/backfill_status.py` | 226 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/backfill_status.py` | 246 | put_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/backfill_status.py` | 249 | get_object | Key | **GENERATIVE** | var key <- call status_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/conversion_manifest.py` | 126 | put_object | Key | **GENERATIVE** | var key <- call manifest_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/conversion_manifest.py` | 128 | head_object | Key | **GENERATIVE** | var key <- call manifest_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/schwab_conversion.py` | 255 | head_object | Key | **NOT_MEASURABLE** | var silver_key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/schwab_conversion.py` | 267 | put_object | Key | **NOT_MEASURABLE** | var skey (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/schwab_conversion.py` | 362 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/stream_parquet.py` | 136 | put_object | Key | **NOT_MEASURABLE** | attr/subscript |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/silver.py` | 1127 | put_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/smartx_conversion.py` | 70 | get_object | Key | **NOT_MEASURABLE** | var key (unresolved in-function) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/smartx_conversion.py` | 311 | put_object | Key | **GENERATIVE** | var key <- concat/% |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 100 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 108 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 111 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 121 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 123 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 129 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 138 | put_object | Key | **GENERATIVE** | call model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 140 | put_object | Key | **GENERATIVE** | call account_tier_model_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 151 | put_object | Key | **GENERATIVE** | call allocation_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 161 | put_object | Key | **GENERATIVE** | call account_tier_account_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 174 | put_object | Key | **GENERATIVE** | call account_tier_account_bronze_key |
| `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/test_smartx_conversion.py` | 182 | put_object | Key | **GENERATIVE** | call account_tier_platform_bronze_key |

## TOTALS

**198 files, 272 call sites** -- LITERAL **30** (11.0%), GENERATIVE **147** (54.0%), NOT_MEASURABLE **95** (34.9%)

**A token census over key names can see at most 11.0% of these call sites.**

## PORTAL READ PATH (portal/src, separate instrument)

393 .ts/.tsx files scanned, comment lines excluded; 12 artifact-URL expressions: 8 LITERAL, 4 GENERATIVE.

| file:line | expression | class |
|---|---|---|
| `portal/src/api/endpoints/adviKeyRepoint.ts:123` | `/api/scoped/advisor-intelligence/platinum/advi/${firm}/${leaf}` | **GENERATIVE** |
| `portal/src/api/endpoints/advisor-intelligence.ts:384` | `/api/scoped/advisor-intelligence/platinum/firm/partner_analytics_${suffix}.json` | **GENERATIVE** |
| `portal/src/api/endpoints/advisor-intelligence.ts:462` | `/api/scoped/advisor-intelligence/advisors/${advisorId}/mix-views?firmId=${mappedFirmId}` | **GENERATIVE** |
| `portal/src/hooks/useLambdaKeepWarm.ts:47` | `/api/scoped/advisor-intelligence/filters?warm=1${firmParam}&_=${Date.now()}` | **GENERATIVE** |

**The repoint DE flipped is itself generative** (`adviKeyRepoint.ts:123`), as is the publisher
that writes the twins (`serve_key` f-string, `opal-assets-mdpf-portal-publisher:236`).

> ### CORRECTION (0.4.0_DE_ClientPlatform, re-derived at this seat before accepting)
> This section originally read *"on BOTH ends of this change the artifact identity is generated,
> **never named**."* **That is wrong for the portal end and the correction sharpens the finding.**
>
> `adviKeyRepoint.ts` contains **all 15 key literals** as `leaf: '...'` values in its ADVI_REPOINT
> registry (re-measured here: 15 `leaf:` entries; `comp-find 'mix_summary.json' portal/src` returns
> 2 hits across 415 files, one of them this module). **A name census DOES find this file.**
>
> **WHAT IS INVISIBLE IS THE COMPOSITION, NOT THE MODULE.** A census can establish THAT the file
> mentions `mix_summary.json`; it cannot establish that the file REQUESTS
> `platinum/advi/49financial/mix_summary.json`. That full key never exists in the source -- only its
> two halves do.
>
> **THIS IS THE WORSE FAILURE, NOT THE MILDER ONE.** "Generative therefore invisible" implies the
> remedy is to find the file. The real gap is narrower and harder: the file is FINDABLE and its
> BEHAVIOUR is still unreadable by that instrument -- so a census that returned this module in its
> results could report the surface as COVERED and be wrong about what the surface does. A confident
> partial is harder to notice than a clean absence.
>
> **THEREFORE, READ THE 11% PRECISELY:** it is the share of CALL SITES whose key argument is a
> literal. It is **not** a claim about how many files a census can discover. Those are different
> populations, and conflating them is the same grain error this sweep exists to expose.

### GRADING NOTE for the estate-wide inventory (DE, and it should survive into its scope)
"Builds keys generatively" is not one behaviour. A component that **centralises** its key list in
one registry and composes at a single site (adviKeyRepoint: the centralisation is what makes the
10-flip / 4-held / 1-structural never-widen split enforceable, so a held key cannot prefer the twin)
has an **enumerable surface in one place**. A component that **scatters** interpolation across call
sites does not. Grading them the same would penalise the deliberate design and miss the diffuse one.

*(First portal pass matched only 2 sites because the regex assumed a bare `fetch(`; the real
reads go through `adviRead`. Recalibrated against the actual file rather than reporting the 2
as coverage -- recorded because a sweep that closes a blind spot while hiding its own is the
same defect one level up.)*
