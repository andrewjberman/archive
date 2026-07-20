# MDPF_REVAMP gold `dim_*` build -- DS grounding notes (2026-07-20)

Author: 0.4.0_DS_ClientPlatform (this session). Dispatch: 1.0.0_SA_CTO
(20260720T201254Z). Spec v1.1 @6edc1b89a; baseline @84d22bb4d. Live state read
this session (opal-data-assets silver + opal-data-portal-v2 served).

## Parity-target producers (LEGACY -- shapes to reproduce; my new code reads monolith silver)
- A5/A6 `aggregate-aua-timeseries.json` (global 441KB + per-firm): `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` -- `build(s3)` + `slice_per_firm()`; reads `platinum/mdpf/aggregate_aua/{date}.json` dailies (produced by `data/mdpf/scripts/gold/mdpf_aggregate_aua.py`).
- A3/A7 `account-distribution.json`: `data/smartx/scripts/compute_per_firm_account_distribution.py` (reads mdpf feeds model_aua_positions; by_model keyed by DISPLAY_NAME; emits generated_at = F6).
- A4 `non_model_assets.json`: `data/smartx/scripts/backfill_non_model_assets.py` (5-segment A-D stitch + daily appender). "v0_9"/"2025-12-23" are NOT literals here -- F3 "preserve v0_9 verbatim" = reproduce THIS backfill's segment methodology, do not recompute.
- A1/A2 `aum-metrics.json` + `aum-timeseries.json`: `data/smartx/scripts/generate_smartx_timeseries_and_metrics.py` (uses LEGACY display strings -- reconcile to F5-canonical).

## Silver schema (opal-data-assets `smartx/platform/silver/{table}/date=YYYY-MM-DD/`; parser `opal-assets-silver-smartx/silver.py`)
- `fact_model_aum_daily`: rmid, run_date, enterprise_id, enterprise_name, total_aum (MIS-SCALED, IGNORE), **day (date32, the history axis)**, performance_ts, performance_date_friendly, **closing_equity (per-day value)**, _ingested_at. NO model_id/model_name -- identity = **rmid**. day-col = full history (1223 days for the oldest model, >= the 429 served floor). Natural key (rmid, day, run_date). F1 CONFIRMED intra-partition.
- `fact_model_allocation_roster`: **model_id (=registry smartx_model_id)**, model_name, **rmid**, allocation_id (distinct = account_count), advisor_id, **advisor_name (="49 Financial Group")**, advisor_crd, **value (Sigma by model = 5-core basis)**, **status (open/close/workingClose; filter open)**, opened_ts, opened_date_friendly, run_date. Carries BOTH model_id AND rmid -> the live rmid<->model_id bridge.
- `fact_allocation_account_map`: model_id, rmid, allocation_id, account_id, **account_number (byte-faithful; zfill(10)==RPS account_id @96.4%)**, account_name, aum_value, run_date. The RPS-custody join edge; also carries model_id+rmid.
- `fact_allocation_valuation`: allocation_id, owner_id, as_of, run_date, equity, **long_equity (Andrew canonical basis = long_equity+cash)**, short_equity, cash, accrued_*, position counts. NO model id -- join via roster/map on allocation_id. (TO-3 distribution source.)
- `fact_rps` (schwab 08242234 silver): account_id, ticker_symbol, cusip, closing_price, quantity, l_s, **market_value_settled_unsettled (position MV)** + 54 more. Model<->RPS = gold join account_map.account_number.zfill(10)->fact_rps.account_id.

## Crosswalk (TO-0) -- SOLVED, F5-compliant
Chain: registry v4 `model_id`(smartx_model_id) -> canonical model_key [STATIC anchor, F5 key] ; live bridge roster/account_map `rmid`->`model_id` ; aum_daily.rmid -> (bridge) model_id -> (registry) canonical + display_name ; RAISE on unknown model_id.
- rmid<->model_id verified 1:1 both ways; all 8 aum_daily rmids present in roster.
- The 8th model = "Opal Global All Equity Total Return" model_id `4a4b2089-8f9a-4fbe-aa7b-af8edd9d573d` / rmid `4d85401b-...` -- UNKNOWN to registry v4, ~$0 equity, NO open 49F allocations -> correctly absent from served by_model{7}. Needs registry entry (raise-on-unknown would fire if it activates).
- 843d875b display-name trap (Pathfinder Focused Opportunities = Opal Equity Growth SMA) -- handled by keying on model_id, never name.
- 7 live model_ids (49F/open) all match registry smartx_model_id exactly.

## 49F(open) live roster decomposition (2026-07-20 run) -- F2 grounding
LTC(Opal Conservative Growth) $749.94M/3202 . INT $292.20M/1599 . LTA $201.83M/1388 . ST $106.70M/691 . UST $44.74M/170 . div_sma $18.84M/40 . growth_sma(Pathfinder) $4.62M/45. 5-core=$1,395.41M ; +SMA $23.46M ; total $1,418.86M. vs served $1,397.30M (5-core) -- the F2 delta is daily value drift + open/close churn between 07-18 served and my 07-20 read (spec cited $1,401.3M @07-18 -> $4.1M).

## Served 49F artifact F4 shape (json/mdpf/49financial/aggregate-aua-timeseries.json)
firm_id, partner_name, as_of_first, as_of_last, source_vintage_last{overall,status,age_hours_at_generation,threshold_hours,lag_vs_as_of_days,vintage_bearing_feeders[],by_feeder{5 feeders},semantics}, n_dates=429, dates[429], model_aua[429], non_model_aua[429], partner_custody_total[429], cohort_provenance[429]=None, by_model{7 model_keys:{display_name,cohort_class,model_value[429],account_count[429]}}, meta{backfill_methods[],cohort0_historical_backfill,contract,source_prefix,generated_at,slice,basis_provenance{...}}.
- The 2 SMA by_model entries carry model_value=[None]*429 + account_count=[None]*429 (F8 fold: SMAs are keys-present-null in the spine).
- Verified: model_aua[0]=$353.80M = Sigma(5 core by_model.model_value[0]); non_model_aua[0]=$422.37M = partner_custody_total[0]$776.17M - model_aua[0].

## THE HISTORY-PARITY GAP (measured aum_daily 5-core vs served 49F model_aua[])
| date | measured | served | gap |
|---|---|---|---|
| 2024-11-01 | $436.84M | $353.80M | +$83.0M (+23.5%) |
| 2025-01-16 | $633.50M | $454.75M | +$178.8M (+39.3%) |
| 2025-07-01 | $821.26M | $737.75M | +$83.5M (+11.3%) |
| 2026-01-15 | $1,155.22M | $1,152.77M | +$2.4M (+0.2%) |
| 2026-07-17 | $1,397.28M | $1,398.58M | -$1.3M (-0.1%) |
Served HISTORY is a rederived/interpolated backfill (meta.basis_provenance: schwab_canonical_rederived, interpolated_1c, .031 2024depth rederive) that understates the true measured SmartX series 10-40% in 2024-2025, CONVERGING to tie by 2026. Latest cross-section ties to ~0.1%. aum_daily = the clean measured series (F1 source). => historical divergence is intrinsic to the source swap; adjudication needed (Option A latest+shape parity / named-delta history vs Option B replicate the backfill).

## Global = firm-sum (baseline consistency, exact)
Global model_aua $1,534.47M = 49F $1,397.30M + Inflection $137.17M. Global spine non_model_aua $312.17M = 49F $247.69M + Inflection $64.48M. by_model global (9) = 49F/inflection smartx 7 + 2 eclipse blends (blend_5050_int_ltc, blend_5050_st_int; eclipse_id 28/29).
