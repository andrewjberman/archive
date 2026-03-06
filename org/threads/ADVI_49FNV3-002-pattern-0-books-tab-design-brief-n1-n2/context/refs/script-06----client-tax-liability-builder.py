#!/usr/bin/env python3
"""
Build Client Tax Liability View

Aggregates gold/holdings_lots to the position × purchase_year grain, producing
an advisor-intelligence view for tax planning conversations:

  - Qualified (tax_deferred / tax_exempt) vs non-qualified (taxable) split per client
  - For non-qualified accounts: FIFO cost basis + purchase year by asset and term
  - Short-term vs long-term capital gain breakdown at every level
  - Supports drill-down: household → account → asset → purchase_year

Yang's requirements addressed:
  1. Split of qualified vs non-qualified per client     → qualified_flag, tax_status columns
  2. Cost basis by asset, based on aggregated position  → total_cost_basis per position row
  3. Cost basis by asset, based on tax lot              → query holdings_lots directly (lot grain)
  4. Purchase year for both grains                      → purchase_year column

Grain: one row per (relationship_id, account_id, asset_name, purchase_year)
       This is the "aggregated position" level Yang requested.
       For lot-level detail, query gold/holdings_lots/ directly.

Schema:
  relationship_id            str
  relationship_name          str   (from accounts_dimension via timeline)
  account_id                 str
  account_name               str
  account_type               str   — 'IRA' | 'RothIRA' | 'Brokerage' | 'Joint' | etc.
  account_registration_type  str   — 'Contributory IRA' | 'Individual' | etc.
  tax_status                 str   — 'taxable' | 'tax_deferred' | 'tax_exempt'
  qualified_flag             bool  — False = taxable (non-qualified); True = retirement account
  asset_name                 str
  ticker                     str
  purchase_year              int   — year(acquisition_date) — cohort for tax planning
  num_open_lots              int   — number of open FIFO lots in this cohort
  total_units                float
  total_cost_basis           float — FIFO cost basis; meaningful for taxable accounts
  total_market_value         float
  total_accrued_gain         float — unrealized gain; taxable on sale for taxable accounts
  short_term_lots            int
  short_term_units           float
  short_term_cost_basis      float — held < 365 days → taxed at ordinary income rates
  short_term_market_value    float
  short_term_gain            float
  long_term_lots             int
  long_term_units            float
  long_term_cost_basis       float — held ≥ 365 days → taxed at preferential LTCG rates
  long_term_market_value     float
  long_term_gain             float
  snapshot_date              date

Input:
  - gold/holdings_lots/YYYY-MM-DD.parquet  (latest snapshot, built by 03_build_holdings_lots.py)

Output:
  - gold/views/client_tax_liability.parquet

Usage:
    python 06_build_client_tax_liability.py --dry-run
    python 06_build_client_tax_liability.py --upload

Author: Data Scientist (Claude)
Date: 2026-02-20
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO

import pandas as pd
import numpy as np
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_latest_holdings_lots() -> pd.DataFrame:
    """Load the most recent holdings_lots snapshot from gold layer."""
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading holdings lots...", end=' ', flush=True)

    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='gold/holdings_lots/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])

    if not keys:
        raise RuntimeError(
            "No holdings_lots snapshots found. "
            "Run 03_build_holdings_lots.py --upload first."
        )

    latest_key = sorted(keys)[-1]
    print(f"latest: {latest_key}...", end=' ', flush=True)
    resp = s3.get_object(Bucket=S3_BUCKET, Key=latest_key)
    df = pd.read_parquet(BytesIO(resp['Body'].read()))
    print(f"{len(df):,} lots")
    return df


# ---------------------------------------------------------------------------
# Build view
# ---------------------------------------------------------------------------

def build_tax_liability_view(lots: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate open holdings lots to the position × purchase_year grain.

    One row per (relationship_id, account_id, asset_name, purchase_year).
    Includes both all-accounts and per-term (short/long) breakdowns.
    """
    print("\n=== Building client tax liability view ===")

    # Work with open lots only — forward-looking tax liability
    open_lots = lots[lots['is_open']].copy()
    print(f"  Open lots: {len(open_lots):,} of {len(lots):,} total")

    if open_lots.empty:
        raise RuntimeError("No open lots found — run 03_build_holdings_lots.py first.")

    # Ensure required columns exist (graceful if accounts_dim wasn't available)
    for col, default in [
        ('relationship_id',           None),
        ('account_name',              ''),
        ('account_type',              ''),
        ('account_registration_type', ''),
        ('tax_status',                'taxable'),
        ('qualified_flag',            False),
        ('purchase_year',             open_lots['acquisition_date'].dt.year if 'acquisition_date' in open_lots.columns else 0),
    ]:
        if col not in open_lots.columns:
            open_lots[col] = default

    snapshot_date = open_lots['snapshot_date'].iloc[0]

    # ---------- helpers for conditional aggregation ----------
    def agg_term(df, term):
        """Aggregate lots for a specific term (short_term / long_term)."""
        sub = df[df['term'] == term]
        return sub.agg(
            lots=('lot_id', 'count'),
            units=('current_units', 'sum'),
            cost_basis=('cost_basis', 'sum'),
            market_value=('market_value', 'sum'),
            gain=('accrued_gain', 'sum'),
        )

    # ---------- group by position × purchase_year ----------
    group_keys = [
        'relationship_id', 'account_id', 'account_name',
        'account_type', 'account_registration_type',
        'tax_status', 'qualified_flag',
        'asset_name', 'ticker',
        'purchase_year',
    ]
    # Drop group keys that are missing entirely
    group_keys = [k for k in group_keys if k in open_lots.columns]

    print(f"  Grouping by: {group_keys}")

    grouped = open_lots.groupby(group_keys, dropna=False)

    # Total aggregation
    totals = grouped.agg(
        num_open_lots=('lot_id', 'count'),
        total_units=('current_units', 'sum'),
        total_cost_basis=('cost_basis', 'sum'),
        total_market_value=('market_value', 'sum'),
        total_accrued_gain=('accrued_gain', 'sum'),
    ).reset_index()

    # Short-term aggregation
    st = (open_lots[open_lots['term'] == 'short_term']
          .groupby(group_keys, dropna=False)
          .agg(
              short_term_lots=('lot_id', 'count'),
              short_term_units=('current_units', 'sum'),
              short_term_cost_basis=('cost_basis', 'sum'),
              short_term_market_value=('market_value', 'sum'),
              short_term_gain=('accrued_gain', 'sum'),
          ).reset_index())

    # Long-term aggregation
    lt = (open_lots[open_lots['term'] == 'long_term']
          .groupby(group_keys, dropna=False)
          .agg(
              long_term_lots=('lot_id', 'count'),
              long_term_units=('current_units', 'sum'),
              long_term_cost_basis=('cost_basis', 'sum'),
              long_term_market_value=('market_value', 'sum'),
              long_term_gain=('accrued_gain', 'sum'),
          ).reset_index())

    # Join all three aggregations
    result = totals.merge(st, on=group_keys, how='left')
    result = result.merge(lt, on=group_keys, how='left')

    # Fill NaN for positions with no short-term or long-term lots
    st_cols = ['short_term_lots', 'short_term_units', 'short_term_cost_basis',
               'short_term_market_value', 'short_term_gain']
    lt_cols = ['long_term_lots', 'long_term_units', 'long_term_cost_basis',
               'long_term_market_value', 'long_term_gain']
    for col in st_cols + lt_cols:
        if col in result.columns:
            result[col] = result[col].fillna(0.0)
    for col in ['short_term_lots', 'long_term_lots']:
        if col in result.columns:
            result[col] = result[col].fillna(0).astype(int)

    result['snapshot_date'] = snapshot_date

    # Final column order
    final_cols = [
        'relationship_id', 'account_id', 'account_name',
        'account_type', 'account_registration_type',
        'tax_status', 'qualified_flag',
        'asset_name', 'ticker',
        'purchase_year',
        'num_open_lots',
        'total_units', 'total_cost_basis', 'total_market_value', 'total_accrued_gain',
        'short_term_lots', 'short_term_units', 'short_term_cost_basis',
        'short_term_market_value', 'short_term_gain',
        'long_term_lots', 'long_term_units', 'long_term_cost_basis',
        'long_term_market_value', 'long_term_gain',
        'snapshot_date',
    ]
    result = result[[c for c in final_cols if c in result.columns]]
    result = result.sort_values(
        ['relationship_id', 'account_id', 'asset_name', 'purchase_year'],
        na_position='last',
    ).reset_index(drop=True)

    # Summary
    print(f"\n  Rows (position × purchase_year): {len(result):,}")
    print(f"  Unique relationships: {result['relationship_id'].nunique():,}")
    print(f"  Unique accounts:      {result['account_id'].nunique():,}")
    print(f"  Unique assets:        {result['asset_name'].nunique():,}")
    if 'tax_status' in result.columns:
        print(f"\n  By tax_status:")
        for ts, grp in result.groupby('tax_status', dropna=False):
            mv = grp['total_market_value'].sum()
            gain = grp['total_accrued_gain'].sum()
            print(f"    {str(ts):<14}  {len(grp):>8,} positions  "
                  f"MV=${mv:>14,.0f}  Accrued Gain=${gain:>12,.0f}")
    print(f"\n  Non-qualified (taxable) breakdown by term:")
    taxable = result[result['tax_status'] == 'taxable'] if 'tax_status' in result.columns else result
    for label, cb_col, gain_col in [
        ('Short-term', 'short_term_cost_basis', 'short_term_gain'),
        ('Long-term',  'long_term_cost_basis',  'long_term_gain'),
    ]:
        if cb_col in taxable.columns:
            cb = taxable[cb_col].sum()
            gain = taxable[gain_col].sum()
            print(f"    {label:<12}  Cost Basis=${cb:>14,.0f}  Gain=${gain:>12,.0f}")

    return result


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_view(df: pd.DataFrame, upload: bool = False):
    """Save client tax liability view to gold/views/."""
    print("\n=== Saving client tax liability view ===")

    output_key = 'gold/views/client_tax_liability.parquet'
    local_path = Path('/tmp/client_tax_liability.parquet')

    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.2f} MB")

    if upload:
        s3.upload_file(str(local_path), S3_BUCKET, output_key)
        print(f"  ✓ s3://{S3_BUCKET}/{output_key}")
    else:
        print(f"  [DRY RUN] Would upload to: s3://{S3_BUCKET}/{output_key}")

    local_path.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Build Client Tax Liability View (position × purchase_year grain)'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD CLIENT TAX LIABILITY VIEW")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load holdings lots ===")
    lots = load_latest_holdings_lots()

    print("\n=== Step 2: Build view ===")
    view = build_tax_liability_view(lots)

    print("\n=== Step 3: Save ===")
    if not args.dry_run:
        save_view(view, upload=args.upload)
    else:
        print("  [DRY RUN] Skipping save")

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(view):,} rows (position × purchase_year grain)")
    print(f"  Snapshot: {view['snapshot_date'].iloc[0].date() if len(view) else 'n/a'}")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
