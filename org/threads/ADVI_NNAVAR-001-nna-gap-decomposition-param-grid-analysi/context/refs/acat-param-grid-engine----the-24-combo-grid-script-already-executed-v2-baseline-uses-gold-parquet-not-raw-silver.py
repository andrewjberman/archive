#!/usr/bin/env python3
"""
ACAT Parameter Grid Search v2 — Gold Baseline + Single-Pass ACAT Scan

Baseline NNA: loaded from gold/client_performance.parquet (production-grade,
all three cap layers already applied: $50M event clip, AUA-based outflow cap,
90-day velocity cap). Monthly NNA derived as delta of cumulative nna column
per relationship, summed firm-wide.

ACAT scan: loaded from silver/transactions (all partitions). Pre-computes
60-day onboarding superset, then evaluates 24 primary + 9 secondary parameter
combinations to find optimal ONBOARDING_DAYS and BURST_THRESHOLD.

Ground truth: Schwab's 13-month NNA (May 2024 - May 2025)
Output: CSV results + monthly detail + ranked table to stdout

v2 fix: replaces raw-silver baseline (which lacked production caps and computed
to ~-$15B, drowning the $50-100M ACAT signal) with gold parquet baseline.

v3 fix: pre-computes per-account aggregates at each window cutoff instead of
filtering on max_age_days. v2 excluded accounts with ANY activity beyond the
onboarding window, dropping ~60% of legitimate ACAT accounts (358 vs 867 for
D30_T3). v3 includes all accounts but only counts their within-window activity.
"""

import pandas as pd
import numpy as np
import boto3
import io
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ===== CONFIGURATION =====

SCHWAB_NNA = {
    '2024-05': 21_000_000,
    '2024-06':  9_000_000,
    '2024-07': 29_000_000,
    '2024-08': 22_000_000,
    '2024-09': 44_000_000,
    '2024-10': 64_000_000,
    '2024-11': 18_000_000,
    '2024-12': 46_000_000,
    '2025-01':  7_000_000,
    '2025-02':  9_000_000,
    '2025-03': 28_000_000,
    '2025-04': 46_000_000,
    '2025-05': 10_000_000,
}

ONBOARDING_DAYS_VALUES = [7, 14, 21, 30, 45, 60]
BURST_THRESHOLD_VALUES = [2, 3, 4, 5]
MIN_ACAT_ESTIMATE_VALUES = [0, 25_000, 100_000]

BUCKET = 'opal-data-bd'
GOLD_KEY = 'gold/client_performance.parquet'

# ===== BASELINE FROM GOLD PARQUET =====

def compute_baseline_nna_by_month():
    """
    Derives monthly firm-wide NNA from the production gold parquet.
    All caps (50M event, AUA-based, velocity) are already applied in this artifact.

    Pattern: same as script 09_generate_partner_analytics.py get_period_pairs().
    For each month, take the last available date per relationship, compute the
    delta of cumulative NNA vs the prior month's last date, sum across all
    relationships.
    """
    print("Loading gold/client_performance.parquet for baseline NNA...")
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=BUCKET, Key=GOLD_KEY)
    gold = pd.read_parquet(io.BytesIO(obj['Body'].read()))
    print(f"  Gold parquet loaded: {len(gold):,} rows, columns: {list(gold.columns)}")

    gold['date'] = pd.to_datetime(gold['date'])
    gold['ym'] = gold['date'].dt.to_period('M')

    # Last available date per (relationship, month) -- same pattern as script 09
    idx = gold.groupby(['relationship_id', 'ym'])['date'].idxmax()
    monthly = gold.loc[idx][['relationship_id', 'ym', 'nna']].copy()
    monthly = monthly.sort_values(['relationship_id', 'ym'])

    # Delta NNA per relationship per month (cumulative -> periodic)
    monthly['nna_delta'] = monthly.groupby('relationship_id')['nna'].diff().fillna(
        monthly['nna']  # first month for each relationship: use full cum value
    )

    # Sum across all relationships -> firm-wide monthly NNA
    baseline = monthly.groupby('ym')['nna_delta'].sum()
    baseline.index = baseline.index.astype(str)  # '2024-05', '2024-06', etc.

    # Convert to dict for downstream use
    baseline_dict = baseline.to_dict()

    # Print the 13 Schwab months for validation
    print("  Baseline monthly NNA (Schwab test window):")
    for m in sorted(SCHWAB_NNA.keys()):
        val = baseline_dict.get(m, 0)
        schwab_val = SCHWAB_NNA[m]
        print(f"    {m}: ${val/1e6:>+10.1f}M  (Schwab: ${schwab_val/1e6:>+10.1f}M)")

    print(f"  Total baseline months in gold: {len(baseline_dict)}")
    return baseline_dict


# ===== SILVER TRANSACTIONS (for ACAT scan only) =====

def load_transactions_parallel():
    """Load all silver/transactions partitions"""
    print("Loading silver/transactions partitions for ACAT scan...")
    s3 = boto3.client('s3')

    partitions = []
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix='silver/transactions/')

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.parquet'):
                    partitions.append(obj['Key'])

    print(f"  Found {len(partitions)} partitions, loading...")

    dfs = []
    for i, partition_key in enumerate(partitions):
        if (i + 1) % 500 == 0:
            print(f"  [{i+1}/{len(partitions)}]")
        try:
            df = pd.read_parquet(f's3://{BUCKET}/{partition_key}')
            dfs.append(df)
        except Exception as e:
            print(f"  Warning: failed to load {partition_key}: {e}")

    print(f"  Concatenating {len(dfs)} partitions...")
    txns = pd.concat(dfs, ignore_index=True)
    print(f"  Total rows: {len(txns):,}")
    return txns


def apply_canonical_exclusions(txns):
    """Apply JNL and sweep exclusions per canonical_nna_logic.md"""
    print("Applying canonical NNA exclusions...")
    initial = len(txns)

    # Exclude JNL - LONG / JNL - SHORT
    if 'action' in txns.columns:
        txns = txns[~txns['action'].isin(['JNL - LONG', 'JNL - SHORT'])]

    # Exclude description patterns
    if 'description' in txns.columns:
        patterns = ['TRF BTWN SCH', 'TO SEP ACCT MGR', 'TRANSFER FUNDS TO SCHWAB BANK']
        mask = ~txns['description'].str.contains('|'.join(patterns), regex=False, na=False)
        txns = txns[mask]

    excluded = initial - len(txns)
    print(f"  Excluded {excluded:,} rows, {len(txns):,} remaining")
    return txns.reset_index(drop=True)


# ===== ACAT SUPERSET & ESTIMATION =====

def precompute_account_superset(txns):
    """
    Pre-compute per-account aggregates at EACH onboarding window cutoff.

    v2 bug fix: v2 filtered accounts by max_age_days <= onboarding_days, which
    excluded accounts with ANY transaction beyond the window. This dropped accounts
    that ACAT'd in early but continued trading -- exactly the accounts we want.
    v3 (the reference scan) correctly used all accounts' first-N-day transactions.

    Fix: for each account, pre-aggregate buy_count/total_buys/total_sells/nna_inflows
    at each window cutoff (7, 14, 21, 30, 45, 60 days). The parameter loop then
    selects the correct window's aggregates without excluding active accounts.

    Returns: dict keyed by onboarding_days -> DataFrame with per-account aggregates
             plus first_date for month bucketing.
    """
    print("Pre-computing per-window account onboarding superset...")

    txns['trade_date'] = pd.to_datetime(txns['trade_date'])

    # Step 1: Get first activity date per account
    first_dates = txns.groupby('account_id')['trade_date'].min()
    txns['first_date'] = txns['account_id'].map(first_dates)

    # Step 2: Compute account age in days
    txns['account_age_days'] = (txns['trade_date'] - txns['first_date']).dt.days

    # Step 3: Filter to 60-day superset (outer bound)
    txns_60 = txns[txns['account_age_days'] <= 60].copy()

    # Step 4: Classify transaction types
    nna_types = {'Cash Deposit', 'Cash Withdrawal', 'Transfer In', 'Transfer Out'}
    inflow_types = {'Cash Deposit', 'Transfer In'}
    txns_60['is_nna'] = txns_60['transaction_type'].isin(nna_types)
    txns_60['is_inflow'] = txns_60['transaction_type'].isin(inflow_types)
    txns_60['is_buy'] = (~txns_60['is_nna']) & (txns_60['market_value'] > 0)
    txns_60['is_sell'] = (~txns_60['is_nna']) & (txns_60['market_value'] < 0)

    # Step 5: For each window cutoff, aggregate per account using only
    # transactions within that window. Accounts with activity beyond the
    # window are INCLUDED (using only their within-window transactions).
    supersets = {}
    for window in ONBOARDING_DAYS_VALUES:
        txns_w = txns_60[txns_60['account_age_days'] <= window]

        # Buy count per account
        buy_counts = txns_w[txns_w['is_buy']].groupby('account_id').size()

        # Total buys (positive market_value where is_buy)
        total_buys = txns_w[txns_w['is_buy']].groupby('account_id')['market_value'].sum()

        # Total sells (abs of negative market_value where is_sell)
        total_sells = txns_w[txns_w['is_sell']].groupby('account_id')['market_value'].apply(
            lambda x: x.abs().sum()
        )

        # NNA inflows (abs market_value where is_nna and is_inflow)
        nna_inflows = txns_w[txns_w['is_nna'] & txns_w['is_inflow']].groupby(
            'account_id'
        )['market_value'].apply(lambda x: x.abs().sum())

        # Build superset for this window
        # Start with all accounts that have ANY transaction in this window
        accounts_in_window = txns_w['account_id'].unique()
        sup = pd.DataFrame({'account_id': accounts_in_window})
        sup['first_date'] = sup['account_id'].map(first_dates)
        sup['buy_count'] = sup['account_id'].map(buy_counts).fillna(0).astype(int)
        sup['total_buys'] = sup['account_id'].map(total_buys).fillna(0)
        sup['total_sells'] = sup['account_id'].map(total_sells).fillna(0)
        sup['nna_inflows'] = sup['account_id'].map(nna_inflows).fillna(0)

        supersets[window] = sup
        print(f"  Window {window:>2}d: {len(sup):,} accounts, "
              f"{int(sup['buy_count'].sum()):,} buys, "
              f"${sup['total_buys'].sum()/1e6:.1f}M buy volume")

    return supersets


def compute_acat_estimates(supersets, onboarding_days, burst_threshold, min_acat_estimate=0):
    """
    For a given parameter combo, compute ACAT estimates for flagged accounts.

    Uses the pre-computed superset for the specified onboarding window.
    All accounts with transactions in that window are considered; the filter
    is on buy_count (burst threshold) and acat_estimate (minimum), not on
    whether the account has later activity.

    ACAT_estimate = max(0, buys - sells - nna_inflows)  within onboarding window
    """
    sup = supersets[onboarding_days]
    subset = sup[sup['buy_count'] >= burst_threshold].copy()
    subset['acat_estimate'] = (
        subset['total_buys'] - subset['total_sells'] - subset['nna_inflows']
    ).clip(lower=0)
    subset = subset[subset['acat_estimate'] >= min_acat_estimate].copy()

    subset['first_month'] = subset['first_date'].dt.strftime('%Y-%m')
    acat_by_month = subset.groupby('first_month')['acat_estimate'].sum().to_dict()

    return acat_by_month, len(subset), subset['acat_estimate'].sum()


# ===== METRICS =====

def compute_pearson_r(vec1, vec2):
    """Compute Pearson correlation coefficient (no scipy)"""
    if len(vec1) < 2 or len(vec2) < 2:
        return np.nan
    try:
        mask = ~(np.isnan(vec1) | np.isnan(vec2))
        if mask.sum() < 2:
            return np.nan
        return np.corrcoef(vec1[mask], vec2[mask])[0, 1]
    except Exception:
        return np.nan


def compute_spearman_r(vec1, vec2):
    """Compute Spearman rank correlation (no scipy)"""
    try:
        if len(vec1) < 2:
            return np.nan
        ranks1 = pd.Series(vec1).rank().values
        ranks2 = pd.Series(vec2).rank().values
        return np.corrcoef(ranks1, ranks2)[0, 1]
    except Exception:
        return np.nan


def compute_metrics(adjusted_monthly_nna, schwab_monthly_nna):
    """Compute all 7 metrics between adjusted monthly NNA and Schwab ground truth"""
    months_in_order = sorted(schwab_monthly_nna.keys())

    our_vector = np.array([adjusted_monthly_nna.get(m, 0) for m in months_in_order], dtype=float)
    schwab_vector = np.array([schwab_monthly_nna[m] for m in months_in_order], dtype=float)

    pearson_r = compute_pearson_r(our_vector, schwab_vector)
    spearman_r = compute_spearman_r(our_vector, schwab_vector)

    sign_agreement_count = int((np.sign(our_vector) == np.sign(schwab_vector)).sum())
    sign_agreement_rate = sign_agreement_count / len(our_vector)

    rmse = float(np.sqrt(np.mean((our_vector - schwab_vector) ** 2)))
    mae = float(np.mean(np.abs(our_vector - schwab_vector)))
    total_gap = float(np.sum(our_vector) - np.sum(schwab_vector))
    max_monthly_overshoot = float(np.max(np.abs(our_vector - schwab_vector)))

    return {
        'pearson_r': pearson_r,
        'spearman_r': spearman_r,
        'sign_agreement_rate': sign_agreement_rate,
        'sign_agreement_count': sign_agreement_count,
        'rmse': rmse,
        'mae': mae,
        'total_gap': total_gap,
        'max_monthly_overshoot': max_monthly_overshoot,
    }


# ===== GRID SEARCH =====

def run_parameter_grid(supersets, baseline_monthly):
    """Run primary 24-combo grid"""
    print("\n=== PRIMARY GRID SEARCH (24 COMBINATIONS) ===\n")

    results = []
    combo_num = 0

    for onboarding_days in ONBOARDING_DAYS_VALUES:
        for burst_threshold in BURST_THRESHOLD_VALUES:
            combo_num += 1
            print(f"[{combo_num}/24] Days={onboarding_days}, Threshold={burst_threshold}...", end=' ')

            acat_by_month, num_flagged, total_acat = compute_acat_estimates(
                supersets, onboarding_days, burst_threshold, min_acat_estimate=0
            )

            adjusted_monthly = baseline_monthly.copy()
            for month, acat_val in acat_by_month.items():
                if month in adjusted_monthly:
                    adjusted_monthly[month] += acat_val

            metrics = compute_metrics(adjusted_monthly, SCHWAB_NNA)

            result = {
                'onboarding_days': onboarding_days,
                'burst_threshold': burst_threshold,
                'min_acat_estimate': 0,
                'accounts_flagged': num_flagged,
                'total_acat_estimate': total_acat,
                **metrics
            }
            results.append(result)
            print(f"Pearson={result['pearson_r']:.3f}, SignAgr={result['sign_agreement_count']}/13, "
                  f"Accts={num_flagged}, ACAT=${total_acat/1e6:.1f}M")

    return results


def identify_top_3_combos(results):
    """Identify top 3 combos by Pearson r for secondary testing"""
    df = pd.DataFrame(results)
    top_3 = df.nlargest(3, 'pearson_r')[['onboarding_days', 'burst_threshold']].values.tolist()
    print(f"\nTop 3 by Pearson r: {[(int(d), int(t)) for d, t in top_3]}")
    return top_3


def run_secondary_grid(supersets, baseline_monthly, top_3_combos):
    """Run secondary tests (MIN_ACAT_ESTIMATE) on top 3 combos"""
    print("\n=== SECONDARY GRID (MIN_ACAT_ESTIMATE ON TOP 3 COMBOS) ===\n")

    results = []
    combo_num = 0

    for onboarding_days, burst_threshold in top_3_combos:
        for min_acat_estimate in MIN_ACAT_ESTIMATE_VALUES:
            combo_num += 1
            print(f"[{combo_num}/9] Days={int(onboarding_days)}, Thresh={int(burst_threshold)}, "
                  f"MinEst=${min_acat_estimate:,}...", end=' ')

            acat_by_month, num_flagged, total_acat = compute_acat_estimates(
                supersets, int(onboarding_days), burst_threshold, min_acat_estimate
            )

            adjusted_monthly = baseline_monthly.copy()
            for month, acat_val in acat_by_month.items():
                if month in adjusted_monthly:
                    adjusted_monthly[month] += acat_val

            metrics = compute_metrics(adjusted_monthly, SCHWAB_NNA)

            result = {
                'onboarding_days': int(onboarding_days),
                'burst_threshold': int(burst_threshold),
                'min_acat_estimate': min_acat_estimate,
                'accounts_flagged': num_flagged,
                'total_acat_estimate': total_acat,
                **metrics
            }
            results.append(result)
            print(f"Pearson={result['pearson_r']:.3f}, SignAgr={result['sign_agreement_count']}/13, "
                  f"Accts={num_flagged}, ACAT=${total_acat/1e6:.1f}M")

    return results


def add_baseline_comparators(supersets, baseline_monthly):
    """Build BASELINE_NO_ACAT and V3_DEFAULT comparison rows"""
    comparators = []

    # BASELINE_NO_ACAT: no adjustment at all
    baseline_metrics = compute_metrics(baseline_monthly, SCHWAB_NNA)
    comparators.append({
        'onboarding_days': -1,
        'burst_threshold': -1,
        'min_acat_estimate': -1,
        'accounts_flagged': 0,
        'total_acat_estimate': 0,
        'label': 'BASELINE_NO_ACAT',
        **baseline_metrics
    })

    # V3_DEFAULT: ONBOARDING_DAYS=30, BURST_THRESHOLD=3, MIN_ACAT=0
    v3_acat, v3_flagged, v3_total = compute_acat_estimates(supersets, 30, 3, 0)
    v3_monthly = baseline_monthly.copy()
    for month, val in v3_acat.items():
        if month in v3_monthly:
            v3_monthly[month] += val
    v3_metrics = compute_metrics(v3_monthly, SCHWAB_NNA)
    comparators.append({
        'onboarding_days': -2,
        'burst_threshold': -2,
        'min_acat_estimate': -1,
        'accounts_flagged': v3_flagged,
        'total_acat_estimate': v3_total,
        'label': 'V3_DEFAULT',
        **v3_metrics
    })

    return comparators


def build_monthly_detail(supersets, baseline_monthly):
    """Build monthly detail CSV: one row per (combo, month) with baseline, acat, adjusted, schwab"""
    print("\nBuilding monthly detail CSV...")
    rows = []
    months_in_order = sorted(SCHWAB_NNA.keys())

    for onboarding_days in ONBOARDING_DAYS_VALUES:
        for burst_threshold in BURST_THRESHOLD_VALUES:
            acat_by_month, _, _ = compute_acat_estimates(
                supersets, onboarding_days, burst_threshold, 0
            )
            for m in months_in_order:
                base_val = baseline_monthly.get(m, 0)
                acat_val = acat_by_month.get(m, 0)
                rows.append({
                    'onboarding_days': onboarding_days,
                    'burst_threshold': burst_threshold,
                    'month': m,
                    'baseline_nna': base_val,
                    'acat_adjustment': acat_val,
                    'adjusted_nna': base_val + acat_val,
                    'schwab_nna': SCHWAB_NNA[m],
                    'gap': (base_val + acat_val) - SCHWAB_NNA[m],
                })

    # Also add baseline-only rows (no ACAT)
    for m in months_in_order:
        base_val = baseline_monthly.get(m, 0)
        rows.append({
            'onboarding_days': -1,
            'burst_threshold': -1,
            'month': m,
            'baseline_nna': base_val,
            'acat_adjustment': 0,
            'adjusted_nna': base_val,
            'schwab_nna': SCHWAB_NNA[m],
            'gap': base_val - SCHWAB_NNA[m],
        })

    detail_df = pd.DataFrame(rows)
    print(f"  Monthly detail: {len(detail_df)} rows")
    return detail_df


# ===== OUTPUT =====

def write_results_to_s3(results_df, monthly_detail_df):
    """Write results to S3"""
    print("\n=== WRITING RESULTS TO S3 ===\n")

    s3 = boto3.client('s3')

    results_csv = '/tmp/acat_param_grid_results.csv'
    results_df.to_csv(results_csv, index=False)
    s3.upload_file(results_csv, BUCKET, 'diagnostics/acat_param_grid_results.csv')
    print(f"  Uploaded: s3://opal-data-bd/diagnostics/acat_param_grid_results.csv ({len(results_df)} rows)")

    monthly_csv = '/tmp/acat_param_grid_monthly_detail.csv'
    monthly_detail_df.to_csv(monthly_csv, index=False)
    s3.upload_file(monthly_csv, BUCKET, 'diagnostics/acat_param_grid_monthly_detail.csv')
    print(f"  Uploaded: s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv ({len(monthly_detail_df)} rows)")


def print_ranked_results(results_df):
    """Print ranked results table to stdout"""
    print("\n" + "=" * 130)
    print("RANKED RESULTS -- SORTED BY PEARSON R (DESCENDING)")
    print("=" * 130)

    print(f"{'Rank':<6} {'Label':<18} {'Days':>5} {'Thresh':>7} {'MinEst':>10} "
          f"{'Pearson':>8} {'Spearman':>9} {'SignAgr':>8} "
          f"{'RMSE($M)':>10} {'MAE($M)':>10} {'TotalGap($M)':>14} {'MaxOS($M)':>10} {'Accts':>8} {'ACAT($M)':>10}")
    print("-" * 130)

    for i, row in results_df.iterrows():
        label = row.get('label', '')
        if not label:
            label = f"D{int(row['onboarding_days'])}_T{int(row['burst_threshold'])}"
            if row['min_acat_estimate'] > 0:
                label += f"_M{int(row['min_acat_estimate']/1000)}K"

        days_str = str(int(row['onboarding_days'])) if row['onboarding_days'] > 0 else '-'
        thresh_str = str(int(row['burst_threshold'])) if row['burst_threshold'] > 0 else '-'
        min_est_str = f"${int(row['min_acat_estimate']):,}" if row['min_acat_estimate'] >= 0 else '-'

        print(f"{i+1:<6} {label:<18} {days_str:>5} {thresh_str:>7} {min_est_str:>10} "
              f"{row['pearson_r']:>8.3f} {row['spearman_r']:>9.3f} "
              f"{int(row['sign_agreement_count']):>5}/13  "
              f"{row['rmse']/1e6:>9.1f}M {row['mae']/1e6:>9.1f}M "
              f"{row['total_gap']/1e6:>+13.1f}M {row['max_monthly_overshoot']/1e6:>9.1f}M "
              f"{int(row['accounts_flagged']):>7,} {row['total_acat_estimate']/1e6:>9.1f}M")


# ===== MAIN =====

def main():
    print("=" * 100)
    print("ACAT PARAMETER GRID SEARCH v2 -- Gold Baseline + Single-Pass ACAT Scan")
    print("=" * 100)
    print(f"Start time: {datetime.now().isoformat()}")
    print()

    # Step 1: Load baseline from gold parquet (production-capped NNA)
    baseline_monthly = compute_baseline_nna_by_month()

    # Step 2: Load silver transactions for ACAT scan
    txns = load_transactions_parallel()
    txns = apply_canonical_exclusions(txns)

    # Step 3: Pre-compute per-window supersets
    # Returns dict: {window_days: DataFrame} with per-account aggregates
    # at each cutoff. Fixes v2 bug where accounts with activity beyond the
    # window were excluded instead of using only their within-window txns.
    supersets = precompute_account_superset(txns)
    print(f"  Accounts in 60d superset: {len(supersets[60]):,}")

    # Step 4: Run primary 24-combo grid
    results_primary = run_parameter_grid(supersets, baseline_monthly)

    # Step 5: Identify top 3 and run secondary grid
    top_3 = identify_top_3_combos(results_primary)
    results_secondary = run_secondary_grid(supersets, baseline_monthly, top_3)

    # Step 6: Add baseline comparators
    comparators = add_baseline_comparators(supersets, baseline_monthly)

    # Step 7: Combine all results
    all_results = comparators + results_primary + results_secondary
    for r in all_results:
        if 'label' not in r:
            r['label'] = ''

    results_df = pd.DataFrame(all_results).sort_values('pearson_r', ascending=False).reset_index(drop=True)

    # Step 8: Print ranked results
    print_ranked_results(results_df)

    # Step 9: Build monthly detail
    monthly_detail_df = build_monthly_detail(supersets, baseline_monthly)

    # Step 10: Write to S3
    write_results_to_s3(results_df, monthly_detail_df)

    print(f"\nEnd time: {datetime.now().isoformat()}")
    print("=" * 100)


if __name__ == '__main__':
    main()
