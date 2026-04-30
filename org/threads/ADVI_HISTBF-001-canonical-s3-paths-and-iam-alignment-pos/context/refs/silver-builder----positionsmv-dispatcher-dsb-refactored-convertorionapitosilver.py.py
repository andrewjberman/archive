#!/usr/bin/env python3
"""Convert Orion API bronze CSVs -> silver/api_dims/* parquet.

Reads bronze CSVs pulled via data/orion/manual_api/pull_*.py (currently local at
data/orion/manual_api/pulls/{YYYYMMDD}_{dim}.csv) and writes:

  silver/api_dims/household/snapshot_date=YYYY-MM-DD/data.parquet
  silver/api_dims/performance/snapshot_date=YYYY-MM-DD/data.parquet
  silver/api_dims/activity/snapshot_date=YYYY-MM-DD/data.parquet
  silver/api_dims/billing/snapshot_date=YYYY-MM-DD/data.parquet      (when bronze available)
  silver/api_dims/accounts_v2/snapshot_date=YYYY-MM-DD/data.parquet  (NewPortfolio JSON)

Output is INFGRD-filtered (rep_id IN {3, 11, 12}) and carries the standard
silver/api_dims/* envelope cols: snapshot_date, source_system='orion-api',
rep_id, advisor_firm.

Project: ADVI_INFSHIP Phase 1 L2
PRD: docs/architecture/ADVI_INFSHIP.md (commit 34d2b757), §4 row L2
Author: 0.4.0_DS_ClientPlatform~A

Bronze source mapping:
  household    <- 20260428_geo_verify.csv  (state/city) + 20260428_unified_account_dim.csv (AUA)
  performance  <- 20260428_performance_dim.csv
  activity     <- 20260428_unified_account_dim.csv  (3y window buckets)
  billing      <- 20260428_billing_dim_spike.csv  (NOT_INFLECTION_YET - gates on fresh pull)
  accounts_v2  <- 20260428_new_portfolio_accounts.json  (GET Portfolio/Accounts/NewPortfolio - 73 fields, sync 1.2s)

AUA reconciliation note (PRD §3.3): unified_account_dim Ending MV gives $199.4M for
Inflection rep_ids, matching silver post-INFGRD ($200M). geo_verify Activity.Value gives
$139.96M same accounts — likely missing activityOptionId=1. ALWAYS use unified_account_dim
for $-values; geo_verify supplies state/city ONLY.

Usage:
  python convert_orion_api_to_silver.py --dim household --snapshot-date 2026-04-28
  python convert_orion_api_to_silver.py --dim performance --snapshot-date 2026-04-28
  python convert_orion_api_to_silver.py --dim activity --snapshot-date 2026-04-28
  python convert_orion_api_to_silver.py --all --snapshot-date 2026-04-28        # all dims
  python convert_orion_api_to_silver.py --all --snapshot-date 2026-04-28 --upload  # + S3
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from io import BytesIO

import boto3
import pandas as pd

from _orion_api_silver_lib import (
    LOCAL_BRONZE_API_DIR,
    add_required_silver_cols,
    apply_aua_guard,
    filter_to_inflection,
    normalize_column_names,
    parse_dollar,
    parse_int_score,
    parse_orion_date,
    parse_percent_decimal,
    read_bronze_csv,
    write_silver_api_dim_parquet,
)

# Local S3 client for v2 silver builders (positions_mv). Other builders go via
# helpers in _orion_api_silver_lib that already hold their own client.
_s3_v2 = boto3.client("s3", region_name="us-east-1")
S3_BUCKET_V2 = os.environ.get("INF_S3_BUCKET", "opal-data-inf")


def build_household(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/household/.

    Joins geo_verify (state/city/country) with unified_account_dim (AUA Ending MV).
    AUA from unified, NOT geo, per PRD §3.3 reconciliation finding.
    """
    geo = read_bronze_csv(snapshot_date, 'geo_verify')
    unified = read_bronze_csv(snapshot_date, 'unified_account_dim')

    geo_keep = {
        'Account.Id': 'account_id',
        'Household.Id': 'household_id',
        'Household.Name': 'household_name',
        'Household.StateCode': 'state_code',
        'Household.City': 'city',
        'Household.Country': 'country',
        'Representative.Id': 'rep_id',
        'Representative.Name': 'rep_name',
    }
    geo_n = normalize_column_names(geo, geo_keep)

    unified_keep = {
        'Account ID': 'account_id',
        'Ending MV': 'account_aua_str',
    }
    unified_n = normalize_column_names(unified, unified_keep)
    unified_n['account_aua'] = unified_n['account_aua_str'].apply(parse_dollar)
    unified_n = unified_n[['account_id', 'account_aua']]

    merged = geo_n.merge(unified_n, on='account_id', how='left')
    merged['account_aua'] = merged['account_aua'].fillna(0.0)

    merged = filter_to_inflection(merged, 'rep_id')
    merged = add_required_silver_cols(merged, snapshot_date)

    apply_aua_guard(merged, 'account_aua', 'household')

    cols = ['account_id', 'household_id', 'household_name', 'state_code', 'city',
            'country', 'rep_id', 'rep_name', 'account_aua', 'snapshot_date',
            'source_system', 'advisor_firm']
    return merged[cols]


def build_performance(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/performance/.

    Per-account TWR + risk metrics from performance_dim.
    Sharpe/Sortino/Beta/Capture currently return integer scores (1-N), not raw values —
    flagged in PATH_DISCOVERY.md, requires statisticalOptionId fix in pull config. Stored
    as int_score columns for now; raw values blocked until pull fixed.
    """
    perf = read_bronze_csv(snapshot_date, 'performance_dim')

    keep = {
        'Account Id': 'account_id',
        'Account Number': 'account_number',
        'Account Name': 'account_name',
        'Household Id': 'household_id',
        'Representative Id': 'rep_id',
        'Representative Name': 'rep_name',
        'Performance Value': 'twr_value_str',
        'Performance CalcMethod': 'twr_calc_method',
        'Performance TaxMethod': 'twr_tax_method',
        'Performance FeeMethod': 'twr_fee_method',
        'Performance AnnualizedMethod': 'twr_annualized',
        'Performance SharpeRatio': 'sharpe_score_str',
        'Performance SortinoRatio': 'sortino_score_str',
        'Performance Drawdown': 'drawdown_str',
        'Performance StandardDeviation': 'std_deviation_str',
        'Performance UpsideCaptureRatio': 'upside_capture_score_str',
        'Performance DownsideCaptureRatio': 'downside_capture_score_str',
        'Performance BetaCoefficient': 'beta_score_str',
        'Performance RSquared': 'r_squared_str',
        'Performance Mean': 'mean_return_str',
        'Performance Variance': 'variance_str',
        'DateRange Name': 'date_range_name',
        'DateRange StartDate': 'date_range_start_str',
        'DateRange EndDate': 'date_range_end_str',
    }
    df = normalize_column_names(perf, keep)

    df['twr_value'] = df['twr_value_str'].apply(parse_percent_decimal)
    df['drawdown'] = df['drawdown_str'].apply(parse_percent_decimal)
    df['std_deviation'] = df['std_deviation_str'].apply(parse_percent_decimal)
    df['r_squared'] = df['r_squared_str'].apply(parse_percent_decimal)
    df['mean_return'] = df['mean_return_str'].apply(parse_percent_decimal)
    df['variance'] = df['variance_str'].apply(parse_percent_decimal)
    df['sharpe_score'] = df['sharpe_score_str'].apply(parse_int_score)
    df['sortino_score'] = df['sortino_score_str'].apply(parse_int_score)
    df['upside_capture_score'] = df['upside_capture_score_str'].apply(parse_int_score)
    df['downside_capture_score'] = df['downside_capture_score_str'].apply(parse_int_score)
    df['beta_score'] = df['beta_score_str'].apply(parse_int_score)
    df['date_range_start'] = df['date_range_start_str'].apply(parse_orion_date)
    df['date_range_end'] = df['date_range_end_str'].apply(parse_orion_date)

    df = filter_to_inflection(df, 'rep_id')
    df = add_required_silver_cols(df, snapshot_date)

    cols = [
        'account_id', 'account_number', 'account_name', 'household_id', 'rep_id', 'rep_name',
        'twr_value', 'twr_calc_method', 'twr_tax_method', 'twr_fee_method', 'twr_annualized',
        'sharpe_score', 'sortino_score', 'drawdown', 'std_deviation',
        'upside_capture_score', 'downside_capture_score', 'beta_score', 'r_squared',
        'mean_return', 'variance', 'date_range_name', 'date_range_start', 'date_range_end',
        'snapshot_date', 'source_system', 'advisor_firm',
    ]
    return df[cols]


def build_activity(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/activity/.

    Per-account 3y-window activity buckets from unified_account_dim. Includes
    Ending MV, Beginning MV, and 6 cashflow buckets (contributions, distributions,
    advisory fees, dividends, etc.). The window is fixed at Rolling 3-Year per the
    pull config; daily timeseries requires a separate per-day pull.
    """
    unified = read_bronze_csv(snapshot_date, 'unified_account_dim')

    keep = {
        'Account ID': 'account_id',
        'Account Number': 'account_number',
        'Household ID': 'household_id',
        'Rep ID': 'rep_id',
        'Rep Name': 'rep_name',
        'Ending MV': 'ending_mv_str',
        'Beginning MV': 'beginning_mv_str',
        'Contributions (3y)': 'contributions_3y_str',
        'Distributions (3y)': 'distributions_3y_str',
        'Net Div/Int Withdrawn (3y)': 'net_div_int_withdrawn_3y_str',
        'Advisory Fees Paid (3y)': 'advisory_fees_paid_3y_str',
        'Dividends + Interest (3y)': 'dividends_interest_3y_str',
        'Div Int Reinvested (3y)': 'div_int_reinvested_3y_str',
        'Net Amount Invested (3y)': 'net_amount_invested_3y_str',
        'Date Range Name': 'window_name',
        'Start Date': 'window_start_str',
        'End Date': 'window_end_str',
    }
    df = normalize_column_names(unified, keep)

    dollar_cols = [
        ('ending_mv_str', 'ending_mv'),
        ('beginning_mv_str', 'beginning_mv'),
        ('contributions_3y_str', 'contributions_3y'),
        ('distributions_3y_str', 'distributions_3y'),
        ('net_div_int_withdrawn_3y_str', 'net_div_int_withdrawn_3y'),
        ('advisory_fees_paid_3y_str', 'advisory_fees_paid_3y'),
        ('dividends_interest_3y_str', 'dividends_interest_3y'),
        ('div_int_reinvested_3y_str', 'div_int_reinvested_3y'),
        ('net_amount_invested_3y_str', 'net_amount_invested_3y'),
    ]
    for src, dst in dollar_cols:
        df[dst] = df[src].apply(parse_dollar)

    df['window_start'] = df['window_start_str'].apply(parse_orion_date)
    df['window_end'] = df['window_end_str'].apply(parse_orion_date)

    df = filter_to_inflection(df, 'rep_id')
    df = add_required_silver_cols(df, snapshot_date)

    apply_aua_guard(df, 'ending_mv', 'activity')

    cols = [
        'account_id', 'account_number', 'household_id', 'rep_id', 'rep_name',
        'ending_mv', 'beginning_mv',
        'contributions_3y', 'distributions_3y', 'net_div_int_withdrawn_3y',
        'advisory_fees_paid_3y', 'dividends_interest_3y', 'div_int_reinvested_3y',
        'net_amount_invested_3y',
        'window_name', 'window_start', 'window_end',
        'snapshot_date', 'source_system', 'advisor_firm',
    ]
    return df[cols]


def build_billing(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/billing/.

    Currently BLOCKED — billing_dim_spike was a Keil-only test pull, no Inflection rows.
    DS~B / AE need to re-pull billing dim with Inflection entityIds [3, 11, 12].

    When fresh pull lands, schema:
      account_id, household_id, rep_id, account_aua_billing,
      included_in_billing_and_fees (bool), annual_fee_pct, average_fee_pct,
      fee_amount, fee_schedule_name, asset_level_fee_schedule, asset_level_tier_info,
      bill_period_start, bill_period_end, bill_cycle, days_in_cycle,
      days_in_cycle_no_cashflows, snapshot_date, source_system, advisor_firm
    """
    billing = read_bronze_csv(snapshot_date, 'billing_dim_spike')
    if 'Account ID' not in billing.columns:
        raise ValueError("billing_dim_spike.csv missing 'Account ID' column")

    keep = {
        'Account ID': 'account_id',
        'Account Number': 'account_number',
        'Household ID': 'household_id',
        'Activity: Ending Market Value': 'account_aua_str',
        'Included In Billing and Fees': 'included_in_billing_str',
        'Billing Annual Fee Percent': 'annual_fee_pct_str',
        'Billing Average Fee Percent': 'average_fee_pct_str',
        'Billing Fee Amount': 'fee_amount_str',
        'Billing Fee Schedule Name': 'fee_schedule_name',
        'Billing Asset Level Fee Schedule Name': 'asset_level_fee_schedule',
        'Billing Asset Level Fee Schedule Tier Info': 'asset_level_tier_info',
        'Billing Period Start Date': 'bill_period_start_str',
        'Billing Period End Date': 'bill_period_end_str',
        'Billing Cycle': 'bill_cycle',
        'Billing Days In Cycle': 'days_in_cycle',
        'Billing Days in Cycle without Cash Flows': 'days_in_cycle_no_cashflows',
    }
    df = normalize_column_names(billing, keep)

    df['account_aua_billing'] = df['account_aua_str'].apply(parse_dollar)
    df['annual_fee_pct'] = df['annual_fee_pct_str'].apply(parse_percent_decimal)
    df['average_fee_pct'] = df['average_fee_pct_str'].apply(parse_percent_decimal)
    df['fee_amount'] = df['fee_amount_str'].apply(parse_dollar)
    df['bill_period_start'] = df['bill_period_start_str'].apply(parse_orion_date)
    df['bill_period_end'] = df['bill_period_end_str'].apply(parse_orion_date)
    df['included_in_billing'] = df['included_in_billing_str'].apply(
        lambda s: True if str(s).strip().lower() == 'true' else (False if str(s).strip().lower() == 'false' else None)
    )

    if 'rep_id' not in df.columns:
        unified = read_bronze_csv(snapshot_date, 'unified_account_dim')
        unified_keep = {'Account ID': 'account_id', 'Rep ID': 'rep_id', 'Rep Name': 'rep_name'}
        unified_n = normalize_column_names(unified, unified_keep)
        df = df.merge(unified_n, on='account_id', how='left')

    df = filter_to_inflection(df, 'rep_id')

    if len(df) == 0:
        raise RuntimeError(
            "BILLING DIM HAS ZERO INFLECTION ROWS. billing_dim_spike was a Keil-only "
            "test pull. DS~B / AE need to re-pull billing with entityIds=[3,11,12] "
            "before this dim can ship to silver. Cluster E gate (PRD §3.3 / INFLEC_ENRICH_SCOPE.md) "
            "is the highest-leverage Orion pull priority."
        )

    df = add_required_silver_cols(df, snapshot_date)

    cols = [
        'account_id', 'account_number', 'household_id', 'rep_id', 'rep_name',
        'account_aua_billing', 'included_in_billing',
        'annual_fee_pct', 'average_fee_pct', 'fee_amount',
        'fee_schedule_name', 'asset_level_fee_schedule', 'asset_level_tier_info',
        'bill_period_start', 'bill_period_end', 'bill_cycle',
        'days_in_cycle', 'days_in_cycle_no_cashflows',
        'snapshot_date', 'source_system', 'advisor_firm',
    ]
    return df[cols]


def build_accounts_v2(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/accounts_v2/.

    Source: GET /api/v1/Portfolio/Accounts/NewPortfolio (synchronous, ~1.2s, 73 fields).
    Bronze JSON pulled by data/orion/manual_api/pull_inflection_new_portfolio.py.

    INFGRD scope filter: custodian IN ('Fidelity_Inflection', 'Fidelity_LH'). Expanded from
    Fidelity_Inflection-only per AUM reconciliation 20260430 — Fidelity_LH is a second Orion
    custodian code covering 9 Inflection-rep households (~$1.1M AUA) that were previously
    excluded, causing a deterministic $1M gap vs Orion UI. Sanity-check assertion compares
    custodian-filtered count vs full INFLECTION_REP_IDS cohort from silver/api_dims/household;
    <5% divergence = pass.

    NMNC signal: accountStartDate is the recommended field (account inception / first trading
    activity). createdDate reflects Orion-row-creation (data load timing), not relationship
    start -- can be 6+ years AFTER accountStartDate for legacy accounts.
    """
    date_str = snapshot_date.strftime('%Y%m%d')
    json_path = os.path.join(LOCAL_BRONZE_API_DIR, f'{date_str}_new_portfolio_accounts.json')
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Bronze JSON not found at {json_path}. Run "
            f"`python data/orion/manual_api/pull_inflection_new_portfolio.py --date {date_str}` "
            f"or pass --snapshot-date matching an existing pull."
        )

    with open(json_path, 'r', encoding='utf-8') as f:
        rows = json.load(f)

    df = pd.DataFrame(rows)

    inf_mask = df['custodian'].isin(['Fidelity_Inflection', 'Fidelity_LH'])
    inf_df = df[inf_mask].copy()

    keep = {
        'id': 'account_id',
        'accountNumber': 'account_number',
        'name': 'account_name',
        'accountType': 'account_type',
        'accountStatus': 'account_status',
        'accountStatusId': 'account_status_id',
        'isActive': 'is_active',
        'clientId': 'household_id',
        'registrationId': 'registration_id',
        'custodian': 'custodian',
        'custodianId': 'custodian_id',
        'createdDate': 'orion_row_created_at',
        'accountStartDate': 'account_start_date',
        'accountStartValue': 'account_start_value',
        'currentValue': 'current_value',
        'representativeName': 'representative_name',
        'isManaged': 'is_managed',
        'isSweepAccount': 'is_sweep_account',
        'isSleeveAccount': 'is_sleeve_account',
        'isOriginalSMCAccount': 'is_original_smc_account',
        'isTradingBlocked': 'is_trading_blocked',
        'managementStyle': 'management_style',
        'managementStyleId': 'management_style_id',
        'modelName': 'model_name',
        'modelGroupNumber': 'model_group_number',
        'fundFamily': 'fund_family',
        'fundFamilyId': 'fund_family_id',
        'feeSchedule': 'fee_schedule',
        'feeScheduleId': 'fee_schedule_id',
        'billFrequency': 'bill_frequency',
        'billStartDate': 'bill_start_date',
        'masterPayoutSchedule': 'master_payout_schedule',
        'masterPayoutScheduleId': 'master_payout_schedule_id',
        'payMethod': 'pay_method',
        'cycleMonth': 'cycle_month',
        'shareClass': 'share_class',
        'shareClassId': 'share_class_id',
        'state': 'state',
        'city': 'city',
        'zip': 'zip',
        'lastName': 'last_name',
    }
    out = normalize_column_names(inf_df, keep)
    for col in ['account_id', 'household_id', 'registration_id', 'custodian_id',
                'account_status_id', 'management_style_id', 'fund_family_id',
                'fee_schedule_id', 'master_payout_schedule_id', 'cycle_month',
                'share_class_id']:
        if col in out.columns:
            out[col] = out[col].astype('Int64', errors='ignore')
    out['account_id'] = out['account_id'].astype(str)
    out['household_id'] = out['household_id'].astype(str)

    out['orion_row_created_at'] = pd.to_datetime(out['orion_row_created_at'], errors='coerce', utc=True)
    out['account_start_date'] = pd.to_datetime(out['account_start_date'], errors='coerce').dt.date
    if 'bill_start_date' in out.columns:
        out['bill_start_date'] = pd.to_datetime(out['bill_start_date'], errors='coerce').dt.date

    out['snapshot_date'] = snapshot_date
    out['source_system'] = 'orion-api'
    out['advisor_firm'] = 'inflection_wealth_management'

    # DIAGFIX.011: populate rep_id + override representative_name from servicing-rep
    # mapping when available. Fall back to NewPortfolio's primary representativeName
    # if mapping bronze isn't pulled yet for this snapshot_date.
    rep_map_path = HOUSEHOLD_REP_LOCAL_BRONZE_PATH_TPL.format(snap=snapshot_date.isoformat())
    if os.path.exists(rep_map_path):
        rep_map = build_household_rep_mapping(snapshot_date)[
            ['household_id', 'rep_id', 'rep_name']
        ].rename(columns={'rep_name': 'rep_name_servicing'})
        rep_map['household_id'] = rep_map['household_id'].astype(str)
        out = out.merge(rep_map, on='household_id', how='left')
        # Override representative_name with servicing rep when available; keep
        # NewPortfolio value as fallback for households outside the mapping.
        out['representative_name'] = out['rep_name_servicing'].combine_first(
            out['representative_name']
        )
        out = out.drop(columns=['rep_name_servicing'])
    else:
        out['rep_id'] = pd.array([pd.NA] * len(out), dtype='Int64')

    apply_aua_guard(out, 'current_value', 'accounts_v2')

    return out


# --------------------------------------------------------------------------
# DIAGFIX.011 — representatives + household_rep_mapping (Andrew 2026-04-29)
# --------------------------------------------------------------------------
# Bronze: data/orion/manual_api/pulls/{YYYY-MM-DD}_representatives.json (18 reps)
#         data/orion/manual_api/pulls/{YYYY-MM-DD}_household_rep_mapping.json (~270 pairs)
#   pulled by data/orion/manual_api/pull_inflection_representatives.py
#
# Silver:
#   silver/api_dims/representatives/snapshot_date={date}/data.parquet
#     -- 18-row rep master
#   silver/api_dims/household_rep_mapping/snapshot_date={date}/data.parquet
#     -- ONE row per household, with primary servicing rep picked via priority below
#
# Priority for picking primary rep when a household appears under multiple reps:
#   1. Individual servicing rep (6, 10, 11, 12) — Brandenburg / Soderblom / Scanlan / Lee
#   2. Joint placeholder rep (7, 8) — Brandenburg/IWM, Brandenburg/Lee
#   3. Firm-level rep (3) — Inflection Wealth Management catch-all
# This preserves "specific advisor wins" so Joe Brandenburg's 21 households surface
# as his book rather than rolling into the firm bucket.
# --------------------------------------------------------------------------
SERVICING_REP_IDS = {6, 10, 11, 12}
JOINT_PLACEHOLDER_REP_IDS = {7, 8}
FIRM_REP_ID = 3
HOUSEHOLD_REP_LOCAL_BRONZE_PATH_TPL = os.path.join(
    LOCAL_BRONZE_API_DIR, '{snap}_household_rep_mapping.json'
)
REPS_LOCAL_BRONZE_PATH_TPL = os.path.join(
    LOCAL_BRONZE_API_DIR, '{snap}_representatives.json'
)


def _pick_primary_rep_id(rep_ids: list[int]) -> int | None:
    rids = {int(r) for r in rep_ids if r is not None}
    if not rids:
        return None
    for rid in sorted(rids & SERVICING_REP_IDS):
        return rid
    for rid in sorted(rids & JOINT_PLACEHOLDER_REP_IDS):
        return rid
    if FIRM_REP_ID in rids:
        return FIRM_REP_ID
    return min(rids)


def build_representatives(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/representatives/.

    Source: GET /api/v1/Portfolio/Representatives (18 rows).
    Bronze JSON pulled by data/orion/manual_api/pull_inflection_representatives.py.
    """
    snap_iso = snapshot_date.isoformat()
    json_path = REPS_LOCAL_BRONZE_PATH_TPL.format(snap=snap_iso)
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Bronze JSON not found at {json_path}. Run "
            f"`python data/orion/manual_api/pull_inflection_representatives.py "
            f"--date {snap_iso} --upload-bronze` first."
        )
    with open(json_path, 'r', encoding='utf-8') as f:
        rows = json.load(f)

    df = pd.DataFrame(rows)
    keep = {
        'id': 'rep_id',
        'repNo': 'rep_no',
        'fullName': 'full_name',
        'firstName': 'first_name',
        'lastName': 'last_name',
        'isActive': 'is_active',
        'status': 'status',
        'brokerDealer': 'broker_dealer',
        'brokerDealerId': 'broker_dealer_id',
        'riaName': 'ria_name',
        'riaId': 'ria_id',
        'households': 'household_count',
        'createdDate': 'created_date',
        'editedDate': 'edited_date',
        'startDate': 'start_date',
        'globalId': 'global_id',
    }
    out = normalize_column_names(df, keep)
    if 'rep_id' in out.columns:
        out['rep_id'] = pd.to_numeric(out['rep_id'], errors='coerce').astype('Int64')
    if 'household_count' in out.columns:
        out['household_count'] = pd.to_numeric(out['household_count'], errors='coerce').astype('Int64')
    if 'is_active' in out.columns:
        out['is_active'] = out['is_active'].astype('boolean')
    for c in ['created_date', 'edited_date', 'start_date']:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors='coerce', utc=True)

    out['snapshot_date'] = snapshot_date
    out['source_system'] = 'orion-api'
    return out


def build_household_rep_mapping(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/household_rep_mapping/.

    Source: GET /api/v1/Portfolio/Clients?representativeId={N} for each Inflection
    rep_id in scope. Bronze emits one row per (household_id, rep_id) pair; this
    builder dedupes to ONE row per household using _pick_primary_rep_id priority.

    Schema: household_id, rep_id (primary), rep_name (primary), additional_rep_ids
    (semicolon-joined list when household has joint coverage), snapshot_date,
    source_system.
    """
    snap_iso = snapshot_date.isoformat()
    json_path = HOUSEHOLD_REP_LOCAL_BRONZE_PATH_TPL.format(snap=snap_iso)
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Bronze JSON not found at {json_path}. Run "
            f"`python data/orion/manual_api/pull_inflection_representatives.py "
            f"--date {snap_iso} --upload-bronze` first."
        )
    with open(json_path, 'r', encoding='utf-8') as f:
        rows = json.load(f)

    if not rows:
        # Empty mapping — emit empty DataFrame with proper schema
        return pd.DataFrame(columns=[
            'household_id', 'rep_id', 'rep_name', 'additional_rep_ids',
            'snapshot_date', 'source_system',
        ])

    raw = pd.DataFrame(rows)
    raw['household_id'] = raw['household_id'].astype(str).str.strip()
    raw['rep_id'] = pd.to_numeric(raw['rep_id'], errors='coerce').astype('Int64')
    raw['rep_name'] = raw['rep_name'].astype(str)

    # Per-household: compute primary rep via priority + collect additional rep_ids.
    grouped = raw.groupby('household_id', sort=False)
    out_rows = []
    for hh_id, sub in grouped:
        rep_ids = sorted({int(r) for r in sub['rep_id'].dropna().astype(int)})
        primary_rep_id = _pick_primary_rep_id(rep_ids)
        if primary_rep_id is None:
            continue
        primary_rep_name = sub.loc[sub['rep_id'] == primary_rep_id, 'rep_name'].iloc[0]
        additional = [r for r in rep_ids if r != primary_rep_id]
        out_rows.append({
            'household_id':       hh_id,
            'rep_id':             primary_rep_id,
            'rep_name':           primary_rep_name,
            'additional_rep_ids': ';'.join(str(r) for r in additional) if additional else '',
        })

    out = pd.DataFrame(out_rows)
    out['rep_id'] = out['rep_id'].astype('Int64')
    out['snapshot_date'] = snapshot_date
    out['source_system'] = 'orion-api'
    return out


# --------------------------------------------------------------------------
# DIAGFIX.012 — positions_mv (Phase 2 silver dim)
# --------------------------------------------------------------------------
# Bronze: s3://opal-data-inf/bronze/orion-api-v2/{date}/positions.parquet
#   pulled by data/orion/manual_api/pull_inflection_positions_daily.py
#   (per-account /Portfolio/Clients/{cid}/Assets/{date} — same endpoint as
#    DIAGFIX.010 assets_v2 but iterated across a date range)
#
# Silver:
#   silver/api_dims/positions_mv/snapshot_date={date}/data.parquet
#     — one row per (account_id, ticker, snapshot_date)
#     — 58 native Orion fields camelCase->snake_case, types coerced
#     — silver envelope cols added (snapshot_date, source_system, advisor_firm)
#
# Replaces TRN-as-price reconstruction in INF_B_00 (Phase 3 of DIAGFIX.012).
# market_value at snapshot_date = positions_mv.current_value (DIRECT from Orion).
# --------------------------------------------------------------------------

POSITIONS_BRONZE_KEY_TPL = "bronze/positions/{snap}.parquet"

# Field type buckets (from convert_assets_v2_to_silver — same endpoint, same schema).
POSITIONS_INT_FIELDS = {
    "id", "accountId", "accountStatusId", "clientId", "productId",
    "registrationId", "status", "assetLevelStrategyId",
}
POSITIONS_FLOAT_FIELDS = {
    "currentShares", "currentValue", "currentPrice", "costBasis",
    "assetPercentOfAccount", "excludeAmount",
}
POSITIONS_BOOL_FIELDS = {
    "isManaged", "isCustodialCash", "is13FReportable", "isActive",
    "isAdvReportable", "isFeeExcluded", "excludeFromMargin",
    "isGlobalExcluded", "isDataSharingEntity", "isAdvisorOnly",
    "isOrionVision", "isRebalance", "isStrategyOverride",
}
POSITIONS_DATE_FIELDS = {
    "asOfDate", "createdDate", "editedDate", "lastReconDate",
}


def _camel_to_snake_str(name: str) -> str:
    """accountId -> account_id, productCategoryAbbreviation -> product_category_abbreviation."""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def _coerce_positions_types(df: pd.DataFrame) -> pd.DataFrame:
    """Apply type coercions per the field-bucket map. Returns a copy of df."""
    out = df.copy()
    for f in POSITIONS_INT_FIELDS:
        if f in out.columns:
            out[f] = pd.to_numeric(out[f], errors="coerce").astype("Int64")
    for f in POSITIONS_FLOAT_FIELDS:
        if f in out.columns:
            out[f] = pd.to_numeric(out[f], errors="coerce").astype("float64")
    for f in POSITIONS_BOOL_FIELDS:
        if f in out.columns:
            out[f] = out[f].astype("boolean")
    for f in POSITIONS_DATE_FIELDS:
        if f in out.columns:
            out[f] = pd.to_datetime(out[f], errors="coerce", utc=True)
    typed = (POSITIONS_INT_FIELDS | POSITIONS_FLOAT_FIELDS |
             POSITIONS_BOOL_FIELDS | POSITIONS_DATE_FIELDS)
    # Ignore the snapshot_date column added by the bronze pull — leave it as-is.
    for c in out.columns:
        if c not in typed and c != "snapshot_date":
            out[c] = out[c].astype("string")
    return out


def build_positions_mv(snapshot_date: date) -> pd.DataFrame:
    """silver/api_dims/positions_mv/.

    One row per (account_id, ticker, snapshot_date). Reads the per-day bronze
    parquet produced by pull_inflection_positions_daily.py (same Orion endpoint
    as assets_v2, but iterated across a date range for backfill).

    Schema: 58 source cols camelCase->snake_case, plus silver envelope
    (snapshot_date, source_system, advisor_firm). Types per
    POSITIONS_INT_FIELDS / FLOAT_FIELDS / BOOL_FIELDS / DATE_FIELDS.

    Replaces TRN-as-price reconstruction in INF_B_00 — market_value at any
    snapshot_date is now positions_mv.current_value (direct from Orion).
    """
    snap_iso = snapshot_date.isoformat()
    key = POSITIONS_BRONZE_KEY_TPL.format(snap=snap_iso)
    obj = _s3_v2.get_object(Bucket=S3_BUCKET_V2, Key=key)
    df = pd.read_parquet(BytesIO(obj["Body"].read()))

    if df.empty:
        raise RuntimeError(
            f"positions_mv bronze empty at s3://{S3_BUCKET_V2}/{key}. "
            f"Run pull_inflection_positions_daily.py --date {snap_iso} --upload-bronze first."
        )

    df = _coerce_positions_types(df)
    rename_map = {c: _camel_to_snake_str(c) for c in df.columns if c != "snapshot_date"}
    df = df.rename(columns=rename_map)

    df["snapshot_date"] = snapshot_date
    df["source_system"] = "orion-api"
    df["advisor_firm"] = "inflection_wealth_management"

    return df


DIM_BUILDERS = {
    'household': build_household,
    'performance': build_performance,
    'activity': build_activity,
    'billing': build_billing,
    'accounts_v2': build_accounts_v2,
    'representatives': build_representatives,
    'household_rep_mapping': build_household_rep_mapping,
    'positions_mv': build_positions_mv,
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dim', choices=list(DIM_BUILDERS.keys()),
                   help='Build a single dim. Mutually exclusive with --all.')
    p.add_argument('--all', action='store_true', help='Build all dims.')
    p.add_argument('--snapshot-date', required=True,
                   help='Bronze pull date (YYYY-MM-DD). Used as silver partition key.')
    p.add_argument('--upload', action='store_true', help='Also upload to S3.')
    p.add_argument('--dry-run', action='store_true', help='Build but do not write parquet.')
    args = p.parse_args()

    if not args.dim and not args.all:
        p.error('one of --dim or --all is required')
    if args.dim and args.all:
        p.error('--dim and --all are mutually exclusive')

    snapshot_date = datetime.strptime(args.snapshot_date, '%Y-%m-%d').date()
    dims = list(DIM_BUILDERS.keys()) if args.all else [args.dim]

    results = []
    for dim in dims:
        builder = DIM_BUILDERS[dim]
        try:
            df = builder(snapshot_date)
        except Exception as e:
            print(f"DIM {dim}: BUILD FAILED -- {e}")
            results.append((dim, 0, None, None, str(e)))
            continue
        if args.dry_run:
            print(f"DIM {dim}: {len(df)} rows (dry-run)")
            results.append((dim, len(df), None, None, 'dry-run'))
        elif dim == 'positions_mv':
            date_str = snapshot_date.strftime('%Y-%m-%d')
            local_path = os.path.join(
                os.path.dirname(__file__), "local_silver", "positions_mv", f"{date_str}.parquet"
            )
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            df.to_parquet(local_path, index=False)
            s3_key: str | None = None
            if args.upload:
                s3_key = f"silver/positions_mv/{date_str}.parquet"
                buf = BytesIO()
                df.to_parquet(buf, index=False)
                buf.seek(0)
                _s3_v2.put_object(
                    Bucket=S3_BUCKET_V2, Key=s3_key, Body=buf.read(),
                    ContentType="application/octet-stream", ServerSideEncryption="AES256",
                )
            print(f"DIM {dim}: {len(df)} rows -> {local_path}" + (f" + s3://{s3_key}" if s3_key else ""))
            results.append((dim, len(df), local_path, s3_key, 'OK'))
        else:
            local_path, s3_key = write_silver_api_dim_parquet(
                df, dim, snapshot_date, upload_s3=args.upload,
            )
            print(f"DIM {dim}: {len(df)} rows -> {local_path}" + (f" + s3://{s3_key}" if s3_key else ""))
            results.append((dim, len(df), local_path, s3_key, 'OK'))

    failures = [r for r in results if r[4] not in ('OK', 'dry-run')]
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for dim, _, _, _, err in failures:
            print(f"  {dim}: {err}")
        sys.exit(1)


if __name__ == '__main__':
    main()
