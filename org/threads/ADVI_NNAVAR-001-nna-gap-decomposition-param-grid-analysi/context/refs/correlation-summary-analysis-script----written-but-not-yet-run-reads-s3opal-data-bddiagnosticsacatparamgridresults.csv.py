#!/usr/bin/env python3
"""
ACAT Correlation Summary Analysis

Reads the two S3 CSVs from diag_acat_param_grid.py and produces:
  - Ranked results table
  - Sensitivity analysis (holding one param, varying the other)
  - Sign agreement heatmap (text-based grid)
  - Final recommendation with justification

Can run locally OR on EC2. Output goes to local file then S3.
"""

import pandas as pd
import numpy as np
import boto3
from io import StringIO
import sys

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

# ===== FUNCTIONS =====

def load_results_from_s3():
    """Load results CSV from S3"""
    print("Loading results from S3...")
    s3 = boto3.client('s3')

    try:
        obj = s3.get_object(Bucket='opal-data-bd', Key='diagnostics/acat_param_grid_results.csv')
        results_df = pd.read_csv(obj['Body'])
        print(f"  Loaded {len(results_df)} result rows")
        return results_df
    except Exception as e:
        print(f"  Error loading from S3: {e}")
        print("  Attempting local fallback...")
        try:
            results_df = pd.read_csv('/tmp/acat_param_grid_results.csv')
            print(f"  Loaded {len(results_df)} result rows from local fallback")
            return results_df
        except Exception as e2:
            print(f"  Error loading local: {e2}")
            return None


def load_monthly_detail_from_s3():
    """Load monthly detail CSV from S3"""
    print("Loading monthly detail from S3...")
    s3 = boto3.client('s3')

    try:
        obj = s3.get_object(Bucket='opal-data-bd', Key='diagnostics/acat_param_grid_monthly_detail.csv')
        monthly_df = pd.read_csv(obj['Body'])
        print(f"  Loaded {len(monthly_df)} monthly detail rows")
        return monthly_df
    except Exception as e:
        print(f"  Error loading monthly detail from S3: {e}")
        return None


def generate_ranked_table(results_df, output):
    """Generate ranked results table sorted by Pearson r"""
    output.write("\n" + "="*140 + "\n")
    output.write("RANKED RESULTS — ALL PARAMETER COMBINATIONS (SORTED BY PEARSON R DESCENDING)\n")
    output.write("="*140 + "\n\n")

    # Sort by Pearson r descending
    df_sorted = results_df.sort_values('pearson_r', ascending=False).reset_index(drop=True)

    # Format table
    output.write(f"{'Rank':<5} {'Days':<6} {'Thresh':<7} {'Min$':<12} {'Pearson':<10} {'Spearman':<10} "
                 f"{'SignAgr':<10} {'RMSE($M)':<12} {'MAE($M)':<12} {'TotalGap($M)':<15} {'MaxOS($M)':<12} {'Accts':<8}\n")
    output.write("-" * 140 + "\n")

    for i, row in df_sorted.iterrows():
        output.write(f"{i+1:<5} {int(row['onboarding_days']):<6} {int(row['burst_threshold']):<7} "
                     f"${int(row['min_acat_estimate']):>10,} {row['pearson_r']:>9.3f} {row['spearman_r']:>9.3f} "
                     f"{int(row['sign_agreement_count'])}/13{'':<5} {row['rmse']/1e6:>10.1f}M  {row['mae']/1e6:>10.1f}M  "
                     f"{row['total_gap']/1e6:>+13.1f}M  {row['max_monthly_overshoot']/1e6:>10.1f}M  {int(row['accounts_flagged']):>7,}\n")

    return df_sorted


def generate_sensitivity_analysis(results_df, output):
    """Generate sensitivity analysis by holding one param and varying the other"""
    output.write("\n" + "="*100 + "\n")
    output.write("SENSITIVITY ANALYSIS\n")
    output.write("="*100 + "\n\n")

    # Find best primary combo (ignoring MIN_ACAT_ESTIMATE=0)
    primary_only = results_df[results_df['min_acat_estimate'] == 0].copy()
    if len(primary_only) > 0:
        best_combo = primary_only.loc[primary_only['pearson_r'].idxmax()]
        best_days = int(best_combo['onboarding_days'])
        best_threshold = int(best_combo['burst_threshold'])

        output.write(f"Best primary combo: ONBOARDING_DAYS={best_days}, BURST_THRESHOLD={best_threshold}\n")
        output.write(f"Pearson r: {best_combo['pearson_r']:.3f}, Sign agreement: {int(best_combo['sign_agreement_count'])}/13\n\n")

        # Sensitivity: vary ONBOARDING_DAYS, hold BURST_THRESHOLD=best
        output.write(f"1. VARYING ONBOARDING_DAYS (holding BURST_THRESHOLD={best_threshold}):\n")
        output.write(f"   {'Days':<8} {'Pearson':<12} {'Change':<12} {'SignAgr':<12} {'TotalGap($M)':<15}\n")
        output.write(f"   {'-'*60}\n")

        sensitivity_days = primary_only[primary_only['burst_threshold'] == best_threshold].sort_values('onboarding_days')
        for _, row in sensitivity_days.iterrows():
            days_val = int(row['onboarding_days'])
            pearson = row['pearson_r']
            change = pearson - best_combo['pearson_r']
            sign_agr = int(row['sign_agreement_count'])
            total_gap = row['total_gap'] / 1e6
            output.write(f"   {days_val:<8} {pearson:>10.3f} {change:>+10.3f}  {sign_agr}/13{'':<5} {total_gap:>+13.1f}M\n")

        output.write(f"\n2. VARYING BURST_THRESHOLD (holding ONBOARDING_DAYS={best_days}):\n")
        output.write(f"   {'Thresh':<8} {'Pearson':<12} {'Change':<12} {'SignAgr':<12} {'TotalGap($M)':<15}\n")
        output.write(f"   {'-'*60}\n")

        sensitivity_threshold = primary_only[primary_only['onboarding_days'] == best_days].sort_values('burst_threshold')
        for _, row in sensitivity_threshold.iterrows():
            thresh_val = int(row['burst_threshold'])
            pearson = row['pearson_r']
            change = pearson - best_combo['pearson_r']
            sign_agr = int(row['sign_agreement_count'])
            total_gap = row['total_gap'] / 1e6
            output.write(f"   {thresh_val:<8} {pearson:>10.3f} {change:>+10.3f}  {sign_agr}/13{'':<5} {total_gap:>+13.1f}M\n")


def generate_sign_agreement_heatmap(results_df, output):
    """Generate text-based heatmap of sign agreement rates"""
    output.write("\n" + "="*100 + "\n")
    output.write("SIGN AGREEMENT HEATMAP (Days × Threshold, Min$=0 only)\n")
    output.write("="*100 + "\n\n")

    primary_only = results_df[results_df['min_acat_estimate'] == 0].copy()

    if len(primary_only) == 0:
        output.write("No primary results available\n")
        return

    # Create pivot table: Days × Threshold, values = sign agreement rate
    pivot = primary_only.pivot_table(
        values='sign_agreement_rate',
        index='onboarding_days',
        columns='burst_threshold',
        aggfunc='first'
    )

    output.write("     Threshold:\n")
    output.write("Days:    2        3        4        5\n")
    output.write("-" * 35 + "\n")

    for days in sorted(pivot.index):
        row_str = f"{int(days):<5}"
        for thresh in sorted(pivot.columns):
            if pd.notna(pivot.loc[days, thresh]):
                rate = pivot.loc[days, thresh]
                # Color code: >=10/13 (77%) is good
                if rate >= 10/13:
                    marker = "✓"  # or other indicator
                else:
                    marker = " "
                row_str += f" {rate*13:>4.0f}/13{marker}  "
            else:
                row_str += "     -    "
        output.write(row_str + "\n")

    output.write("\n✓ = Sign agreement ≥ 10/13 (77%)\n")


def generate_secondary_analysis(results_df, output):
    """Analyze secondary MIN_ACAT_ESTIMATE tests"""
    output.write("\n" + "="*100 + "\n")
    output.write("SECONDARY PARAMETER ANALYSIS (MIN_ACAT_ESTIMATE)\n")
    output.write("="*100 + "\n\n")

    secondary = results_df[results_df['min_acat_estimate'] > 0].copy()

    if len(secondary) == 0:
        output.write("No secondary results available\n")
        return

    output.write("Testing MIN_ACAT_ESTIMATE filter on top 3 combos:\n\n")

    for combo in secondary[['onboarding_days', 'burst_threshold']].drop_duplicates().values:
        days, thresh = int(combo[0]), int(combo[1])
        output.write(f"Days={days}, Threshold={thresh}:\n")
        output.write(f"   {'Min$':<15} {'Pearson':<12} {'SignAgr':<12} {'Accounts':<12} {'TotalACAT':<15}\n")
        output.write(f"   {'-'*65}\n")

        combo_rows = secondary[(secondary['onboarding_days'] == days) & (secondary['burst_threshold'] == thresh)]
        for _, row in combo_rows.sort_values('min_acat_estimate').iterrows():
            min_acat = int(row['min_acat_estimate'])
            pearson = row['pearson_r']
            sign_agr = int(row['sign_agreement_count'])
            accts = int(row['accounts_flagged'])
            total = row['total_acat_estimate']
            output.write(f"   ${min_acat:<14,} {pearson:>10.3f}  {sign_agr}/13{'':<5} {accts:>10,}  ${total:>13,.0f}\n")
        output.write("\n")


def generate_jan_2025_analysis(results_df, monthly_df, output):
    """Analyze how each combo handles January 2025"""
    output.write("\n" + "="*100 + "\n")
    output.write("JANUARY 2025 BEHAVIOR ANALYSIS\n")
    output.write("="*100 + "\n\n")

    output.write("Jan 2025 Schwab NNA: $7,000,000\n")
    output.write("(Phase 3 v3_default overshoot: $72.6M)\n\n")

    if monthly_df is None or len(monthly_df) == 0:
        output.write("Monthly detail CSV not available for detailed breakdown\n")
        return

    # Filter to Jan 2025
    jan_2025 = monthly_df[monthly_df['year_month'] == '2025-01'].copy()

    if len(jan_2025) == 0:
        output.write("No January 2025 detail available\n")
        return

    jan_2025 = jan_2025.sort_values('adjusted_nna', ascending=False)

    output.write(f"{'Days':<8} {'Thresh':<8} {'MinACTC':<12} {'Baseline':<15} {'ACAT':<15} {'Adjusted':<15} {'Overshoot':<15}\n")
    output.write("-" * 88 + "\n")

    for _, row in jan_2025.iterrows():
        days = int(row['onboarding_days'])
        thresh = int(row['burst_threshold'])
        min_acat = int(row['min_acat_estimate'])
        baseline = row['baseline_nna'] / 1e6
        acat = row.get('acat_adjustment', 0) / 1e6
        adjusted = row['adjusted_nna'] / 1e6
        overshoot = (adjusted * 1e6 - 7e6) / 1e6

        output.write(f"{days:<8} {thresh:<8} ${min_acat:<10,} ${baseline:>13.1f}M ${acat:>13.1f}M ${adjusted:>13.1f}M ${overshoot:>+13.1f}M\n")


def generate_final_recommendation(results_df, monthly_df, output):
    """Generate final parameter recommendation with rationale"""
    output.write("\n" + "="*100 + "\n")
    output.write("FINAL RECOMMENDATION\n")
    output.write("="*100 + "\n\n")

    # Find best combo overall
    best_idx = results_df['pearson_r'].idxmax()
    best_row = results_df.loc[best_idx]

    recommended_days = int(best_row['onboarding_days'])
    recommended_threshold = int(best_row['burst_threshold'])
    recommended_min_acat = int(best_row['min_acat_estimate'])

    output.write(f"RECOMMENDED PARAMETERS:\n")
    output.write(f"  ONBOARDING_DAYS: {recommended_days}\n")
    output.write(f"  BURST_THRESHOLD: {recommended_threshold}\n")
    output.write(f"  MIN_ACAT_ESTIMATE: ${recommended_min_acat:,}\n\n")

    output.write(f"PERFORMANCE METRICS:\n")
    output.write(f"  Pearson r: {best_row['pearson_r']:.3f}\n")
    output.write(f"  Spearman r: {best_row['spearman_r']:.3f}\n")
    output.write(f"  Sign agreement rate: {int(best_row['sign_agreement_count'])}/13 ({best_row['sign_agreement_rate']*100:.0f}%)\n")
    output.write(f"  RMSE: ${best_row['rmse']/1e6:.1f}M\n")
    output.write(f"  Total gap: ${best_row['total_gap']/1e6:+.1f}M\n")
    output.write(f"  Max monthly overshoot: ${best_row['max_monthly_overshoot']/1e6:.1f}M\n")
    output.write(f"  Accounts flagged: {int(best_row['accounts_flagged']):,}\n")
    output.write(f"  Total ACAT estimate: ${best_row['total_acat_estimate']:,.0f}\n\n")

    output.write(f"RATIONALE:\n")
    output.write(f"  This combination maximizes Pearson correlation ({best_row['pearson_r']:.3f})\n")
    output.write(f"  while maintaining strong sign agreement ({int(best_row['sign_agreement_count'])}/13).\n")
    output.write(f"  The parameter set balances sensitivity and specificity across all 13 months.\n\n")

    # Compare to baselines
    output.write(f"COMPARISON TO BASELINES:\n")
    # TODO: include BASELINE_NO_ACAT and V3_DEFAULT rows


def main():
    print("="*100)
    print("ACAT PARAMETER CORRELATION SUMMARY ANALYSIS")
    print("="*100)

    # Load data
    results_df = load_results_from_s3()
    if results_df is None or len(results_df) == 0:
        print("ERROR: Could not load results")
        sys.exit(1)

    monthly_df = load_monthly_detail_from_s3()

    # Generate output
    output = StringIO()

    output.write("="*100 + "\n")
    output.write("ACAT PARAMETER OPTIMIZATION — ANALYSIS SUMMARY\n")
    output.write("="*100 + "\n")

    # Sections
    generate_ranked_table(results_df, output)
    generate_sensitivity_analysis(results_df, output)
    generate_sign_agreement_heatmap(results_df, output)
    generate_secondary_analysis(results_df, output)
    generate_jan_2025_analysis(results_df, monthly_df, output)
    generate_final_recommendation(results_df, monthly_df, output)

    # Write to file and S3
    summary_text = output.getvalue()

    # Local file
    output_file = '/tmp/diag_acat_correlation_summary_output.txt'
    with open(output_file, 'w') as f:
        f.write(summary_text)
    print(f"\nWrote summary to {output_file}")

    # Upload to S3
    try:
        s3 = boto3.client('s3')
        s3.upload_file(output_file, 'opal-data-bd', 'diagnostics/acat_correlation_summary.txt')
        print(f"Uploaded to s3://opal-data-bd/diagnostics/acat_correlation_summary.txt")
    except Exception as e:
        print(f"Warning: could not upload to S3: {e}")

    # Print to stdout
    print("\n" + summary_text)


if __name__ == '__main__':
    main()
