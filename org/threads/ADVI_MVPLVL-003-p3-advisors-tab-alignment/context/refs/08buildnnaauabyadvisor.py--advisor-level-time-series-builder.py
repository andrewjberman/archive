#!/usr/bin/env python3
"""
Build NNA / AUA by Advisor — Architect Daily Timeseries

Rolls up the household-level client_performance timeseries by lead advisor
(architect), enabling dashboards to answer:

  - Which advisors have the largest AUM?
  - Which advisors are growing their NNA the fastest?
  - How does each advisor's book break down by qualified/taxable accounts?

Advisor assignment:
  - Each relationship is assigned to the modal architect across its accounts
    in accounts_dimension_latest (most common non-null, non-empty architect name).
  - Relationships where all accounts have 'Unassigned' or null architect
    fall into the 'Unassigned' (house) bucket.

Attribution note:
  This view uses CURRENT architect assignments (from accounts_dimension, which
  reflects the latest state of each account). It does NOT backfill historical
  advisor changes — if an advisor changed mid-period, the relationship's full
  NNA history is attributed to the current advisor. For point-in-time historical
  advisor attribution, query advisor_assignments_history directly and join on
  (account_id, date BETWEEN effective_date AND end_date).

pct_priced: AUA-weighted average of the per-relationship pct_priced metric.

Grain: one row per (date, architect)

Output schema:
  date                  date
  architect             str   — lead advisor name | 'Unassigned'
  total_aua             float
  aua_taxable           float — AUA in non-qualified (brokerage/joint) accounts
  aua_tax_deferred      float — AUA in traditional IRA/401k accounts
  aua_tax_exempt        float — AUA in Roth accounts
  cum_inflows           float — sum of cumulative inflows across relationships
  cum_outflows          float — sum of cumulative outflows across relationships
  nna                   float — sum of cumulative NNA across relationships
  num_relationships     int   — distinct household count for this advisor on this date
  num_accounts          int   — sum of active account counts on this date
  num_positions         int   — sum of position counts on this date
  pct_priced            float — AUA-weighted price coverage fraction

Input (must exist in S3 before running):
  gold/client_performance.parquet       — from 05_build_client_performance.py
  gold/accounts_dimension_latest.parquet — from 00_build_accounts_dimension.py

Output:
  gold/views/nna_aua_by_advisor.parquet

Usage:
    python 08_build_nna_aua_by_advisor.py --dry-run
    python 08_build_nna_aua_by_advisor.py --upload

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

# Values treated as "missing" when finding the modal advisor name
_MODAL_NULLS = frozenset({
    '', 'none', 'nan', 'unassigned', 'unknown', 'n/a',
    'no architect value assigned',
    'no state',   # included for symmetry with geography script
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def modal_str(series: pd.Series, default: str = 'Unknown') -> str:
    """
    Return the most common non-null, non-empty value in a Series.

    Falls back to `default` when the series contains only nulls / placeholder
    values (empty string, 'none', 'unassigned', etc.).
    """
    clean = series.dropna().astype(str).str.strip()
    clean = clean[~clean.str.lower().isin(_MODAL_NULLS)]
    if clean.empty:
        return default
    return clean.mode().iloc[0]


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_client_performance() -> pd.DataFrame:
    """Load the household daily AUA + NNA timeseries."""
    print("Loading client performance...", end=' ', flush=True)
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key='gold/client_performance.parquet')
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
    except Exception as e:
        raise RuntimeError(
            f"gold/client_performance.parquet not found ({e}). "
            "Run 05_build_client_performance.py --upload first."
        )
    df['date'] = pd.to_datetime(df['date'])
    print(f"{len(df):,} rows | "
          f"{df['date'].min().date()} -> {df['date'].max().date()} | "
          f"{df['relationship_id'].nunique():,} households")
    return df


def load_relationship_advisors() -> pd.DataFrame:
    """
    Derive (relationship_id -> architect) from accounts_dimension_latest.

    Each relationship may span multiple accounts (potentially with different
    architect assignments). We take the modal architect across all accounts in
    the household as the relationship's canonical advisor.

    Returns a DataFrame with columns:
      relationship_id, architect
    """
    print("Loading accounts dimension for advisor attribution...", end=' ', flush=True)
    try:
        resp = s3.get_object(Bucket=S3_BUCKET,
                             Key='gold/accounts_dimension_latest.parquet')
        accts = pd.read_parquet(BytesIO(resp['Body'].read()))
    except Exception as e:
        raise RuntimeError(
            f"gold/accounts_dimension_latest.parquet not found ({e}). "
            "Run 00_build_accounts_dimension.py --upload first."
        )

    print(f"{len(accts):,} accounts across {accts['relationship_id'].nunique():,} households")

    if 'architect' not in accts.columns:
        print("  WARNING: 'architect' column not found — all relationships map to 'Unassigned'")
        rel_ids = accts['relationship_id'].dropna().unique()
        return pd.DataFrame({
            'relationship_id': rel_ids,
            'architect': 'Unassigned',
        })

    # Aggregate to relationship level: modal architect across all accounts in household
    rel_advisors = (
        accts.groupby('relationship_id', sort=False)['architect']
        .agg(lambda s: modal_str(s, 'Unassigned'))
        .reset_index()
        .rename(columns={'architect': 'architect'})
    )

    n_advisors = rel_advisors[rel_advisors['architect'] != 'Unassigned']['architect'].nunique()
    n_unassigned = (rel_advisors['architect'] == 'Unassigned').sum()
    print(f"  -> {len(rel_advisors):,} households | {n_advisors} distinct advisors | "
          f"{n_unassigned} unassigned")
    return rel_advisors


# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------

def build_advisor_view(
        perf: pd.DataFrame,
        rel_advisors: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join performance with relationship->advisor mapping and aggregate to (date, architect).

    Steps:
      1. Left-join perf -> rel_advisors on relationship_id
      2. Fill missing advisor with 'Unassigned'
      3. Compute weighted priced AUA column (for weighted pct_priced)
      4. Aggregate to (date, architect) grain
      5. Compute AUA-weighted pct_priced
    """
    print("\n=== Building advisor view ===")

    # Step 1: Join advisor mapping
    joined = perf.merge(rel_advisors, on='relationship_id', how='left')
    no_advisor = joined['architect'].isna() | (joined['architect'] == '')
    if no_advisor.any():
        joined.loc[no_advisor, 'architect'] = 'Unassigned'
        print(f"  Relationships with no advisor match: "
              f"{joined.loc[no_advisor, 'relationship_id'].nunique():,} -> 'Unassigned'")

    # Step 2: Weighted priced AUA for computing weighted-avg pct_priced later
    joined['_priced_aua'] = joined['total_aua'] * joined['pct_priced'].fillna(1.0)

    # Step 3: Aggregate to (date, architect)
    print("  Aggregating to (date, architect)...")

    agg = joined.groupby(['date', 'architect'], sort=True).agg(
        total_aua         =('total_aua',       'sum'),
        aua_taxable       =('aua_taxable',      'sum'),
        aua_tax_deferred  =('aua_tax_deferred', 'sum'),
        aua_tax_exempt    =('aua_tax_exempt',   'sum'),
        cum_inflows       =('cum_inflows',      'sum'),
        cum_outflows      =('cum_outflows',     'sum'),
        nna               =('nna',              'sum'),
        num_relationships =('relationship_id',  'nunique'),
        num_accounts      =('num_accounts',     'sum'),
        num_positions     =('num_positions',    'sum'),
        _priced_aua_sum   =('_priced_aua',      'sum'),
    ).reset_index()

    # Step 4: AUA-weighted pct_priced
    agg['pct_priced'] = np.where(
        agg['total_aua'] > 0,
        agg['_priced_aua_sum'] / agg['total_aua'],
        1.0,
    )
    agg = agg.drop(columns=['_priced_aua_sum'])

    # Cast integer counts
    agg['num_accounts']      = agg['num_accounts'].fillna(0).astype(int)
    agg['num_positions']     = agg['num_positions'].fillna(0).astype(int)
    agg['num_relationships'] = agg['num_relationships'].astype(int)

    # Summary
    latest_date = agg['date'].max()
    latest = agg[agg['date'] == latest_date].copy()
    latest = latest.sort_values('total_aua', ascending=False)

    print(f"\n  Date range:     {agg['date'].min().date()} -> {latest_date.date()}")
    print(f"  Total rows:     {len(agg):,}")
    print(f"  Advisors:       {agg['architect'].nunique()}")
    print(f"\n  As of {latest_date.date()} — advisors by AUA:")
    for _, row in latest.iterrows():
        pct = row['total_aua'] / latest['total_aua'].sum() * 100 if latest['total_aua'].sum() > 0 else 0
        print(f"    {row['architect']:<30}  ${row['total_aua']:>16,.0f}  "
              f"({pct:4.1f}%)  "
              f"{row['num_relationships']:>5} households")
    print(f"\n  Total AUA:      ${latest['total_aua'].sum():>16,.0f}")
    print(f"  Cum NNA:        ${latest['nna'].sum():>16,.0f}")

    return agg


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_view(df: pd.DataFrame, upload: bool = False):
    """Save advisor view to gold/views/."""
    print("\n=== Saving advisor view ===")

    output_key = 'gold/views/nna_aua_by_advisor.parquet'
    local_path = Path('/tmp/nna_aua_by_advisor.parquet')

    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.2f} MB")

    if upload:
        s3.upload_file(str(local_path), S3_BUCKET, output_key)
        print(f"  OK: s3://{S3_BUCKET}/{output_key}")
    else:
        print(f"  [DRY RUN] Would upload to: s3://{S3_BUCKET}/{output_key}")

    local_path.unlink()


def save_rel_lookup(rel_advisors: pd.DataFrame, upload: bool = False):
    """
    Write the canonical (relationship_id -> architect) mapping to S3.

    Downstream scripts (09_generate_partner_analytics, any future consumer)
    must read from this artifact rather than recomputing modal assignment
    independently. Script 08 is the single source of truth for architect
    attribution.
    """
    output_key = 'gold/views/rel_architect_lookup.parquet'
    local_path = Path('/tmp/rel_architect_lookup.parquet')

    rel_advisors[['relationship_id', 'architect']].to_parquet(
        local_path, index=False, engine='pyarrow', compression='snappy'
    )
    size_kb = local_path.stat().st_size / 1024
    print(f"  rel_architect_lookup: {len(rel_advisors):,} relationships | {size_kb:.1f} KB")

    if upload:
        s3.upload_file(str(local_path), S3_BUCKET, output_key)
        print(f"  OK: s3://{S3_BUCKET}/{output_key}")
    else:
        print(f"  [DRY RUN] Would upload to: s3://{S3_BUCKET}/{output_key}")

    local_path.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Build NNA/AUA by Advisor (architect, daily timeseries)'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD NNA / AUA BY ADVISOR")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    perf         = load_client_performance()
    rel_advisors = load_relationship_advisors()

    print("\n=== Step 2: Build advisor view ===")
    view = build_advisor_view(perf, rel_advisors)

    print("\n=== Step 3: Save ===")
    if not args.dry_run:
        save_view(view, upload=args.upload)
        save_rel_lookup(rel_advisors, upload=args.upload)
    else:
        print("  [DRY RUN] Skipping save")

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(view):,} rows | (date, architect) grain")
    print(f"  {view['architect'].nunique()} advisors | "
          f"{view['date'].min().date()} -> {view['date'].max().date()}")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
