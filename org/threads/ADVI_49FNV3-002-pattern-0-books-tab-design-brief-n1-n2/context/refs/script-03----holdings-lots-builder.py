#!/usr/bin/env python3
"""
Build Holdings Lots — Individual Lot Tracking for Tax Calculations

Produces a lot-level snapshot of all open positions, enabling:
  - Short-term vs long-term capital gain classification
  - Tax liability estimation per account and household
  - Drill-down: household → account → position → lot

Schema:
  lot_id                    str   — "{account_id}:{asset_name}:{lot_index}:{buy_date}"
  snapshot_date             date  — date of this snapshot (today's date)
  account_id                str
  relationship_id           str   — household key (from accounts_dimension)
  account_name              str   — display name (from accounts_dimension)
  account_type              str   — e.g. 'IRA', 'RothIRA', 'Brokerage' (from BD allocations)
  account_registration_type str   — e.g. 'Contributory IRA', 'Individual' (from BD allocations)
  tax_status                str   — 'taxable' | 'tax_deferred' | 'tax_exempt'
  qualified_flag            bool  — False = taxable (non-qualified); True = retirement account
  asset_name                str
  ticker                    str   (may be null for unmapped assets)
  acquisition_date          date  — when this lot was purchased
  purchase_year             int   — year(acquisition_date)
  lot_index                 int   — FIFO order within this position (1 = oldest)
  original_units            float — units purchased in this lot
  current_units             float — units remaining after FIFO sells
  cost_per_unit             float — per-unit purchase price
  cost_basis                float — current_units × cost_per_unit
  current_price             float — latest canonical price
  market_value              float — current_units × current_price
  accrued_gain              float — market_value − cost_basis
  holding_period_days       int   — snapshot_date − acquisition_date
  term                      str   — 'short_term' (< 365 days) | 'long_term' (≥ 365)
  is_open                   bool  — True if current_units > 0
  price_quality             str   — price source label

Input:
  - silver/transactions/                    — deduplicated transaction history
  - silver/prices/                          — canonical daily prices
  - gold/accounts_dimension_latest.parquet  — account metadata (tax_status, qualified_flag, etc.)

Output:
  - gold/holdings_lots/YYYY-MM-DD.parquet  (snapshot for today)
  - gold/holdings_lots/backfill_YYYY-MM-DD_to_YYYY-MM-DD.parquet  (--full)

Usage:
    python 03_build_holdings_lots.py --dry-run
    python 03_build_holdings_lots.py --upload
    python 03_build_holdings_lots.py --upload --full   (backfill all dates)

Author: Data Scientist (Claude)
Date: 2026-02-19
"""

import argparse
import gc
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, date
from pathlib import Path
from io import BytesIO
from typing import List, Optional

import pandas as pd
import numpy as np
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')
MAX_WORKERS = 64

SHORT_TERM_DAYS = 365  # < 365 days -> short-term capital gain

# Transaction types matched to silver/transactions/ values
BUY_TYPES = frozenset({
    'Buy', 'Reinvestment', 'Dividend Reinvestment',
    'Income Reinvestment', 'Capital Gains Reinvestment',
    'Transfer In', 'Buy to Close',
    'Option Exercise', 'Short Cover',
})
SELL_TYPES = frozenset({
    'Sale', 'Short Sale', 'Transfer Out',
    'Expiration', 'Option Exercise (sell)',
})

# Corporate Action sub-types (from transaction_sub_type column).
# Canonical reference: 02_build_positions_cube.py defines these identically.
# See docs/data/transaction_type_canonical_reference.md for the full taxonomy.
CA_BUY_SUBTYPES = frozenset({
    'Conversion In',   # new share class appears (paired with Conversion Out)
    'Spinoff',         # new position spun off from parent
    'Split',           # additional units from stock split
})
CA_SELL_SUBTYPES = frozenset({
    'Merger',          # old ticker ceases to exist -- units exit
    'Conversion Out',  # old share class leaves (paired with Conversion In)
    'Cash in Lieu',    # fractional share cleanup -- small unit removal
    'Reverse Split',   # units reduced by reverse split
})


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_transactions() -> pd.DataFrame:
    """Load all deduplicated transactions with parallel I/O."""
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading transactions (parallel)... ", end='', flush=True)

    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/transactions/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])

    if not keys:
        raise RuntimeError("No transaction parquet files found")

    t0 = datetime.now(timezone.utc)
    dfs = [None] * len(keys)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_read_parquet_from_s3, k): i for i, k in enumerate(keys)}
        done = 0
        for future in as_completed(futures):
            dfs[futures[future]] = future.result()
            done += 1
            if done % 500 == 0:
                print(f"[{done:,}/{len(keys):,}]", end=' ', flush=True)

    df = pd.concat(dfs, ignore_index=True)
    del dfs; gc.collect()
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()

    if 'transaction_id' in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=['transaction_id'], keep='last')
        removed = before - len(df)
        print(f"{len(df):,} rows ({removed:,} dupes) in {elapsed:.1f}s")
    else:
        print(f"{len(df):,} rows in {elapsed:.1f}s")

    df['trade_date'] = pd.to_datetime(df['trade_date'])
    return df


def load_latest_prices() -> pd.DataFrame:
    """Load most recent price for each asset from canonical prices."""
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading canonical prices...", end=' ', flush=True)

    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/prices/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])

    if not keys:
        raise RuntimeError("No canonical prices found. Run build_canonical_prices_v2.py first.")

    dfs = [pd.read_parquet(BytesIO(s3.get_object(Bucket=S3_BUCKET, Key=k)['Body'].read()))
           for k in sorted(keys)]
    prices = pd.concat(dfs, ignore_index=True)
    prices['date'] = pd.to_datetime(prices['date'])

    # Keep latest price per asset
    latest = (prices.sort_values('date', ascending=False)
              .drop_duplicates(subset=['asset_name'], keep='first')
              [['asset_name', 'ticker', 'price', 'source', 'date']])

    print(f"{len(prices):,} rows loaded → {len(latest):,} assets (latest price)")
    return latest


def load_accounts_dimension() -> pd.DataFrame:
    """Load gold/accounts_dimension_latest.parquet for account metadata enrichment.

    Returns DataFrame with account_id, relationship_id, account_name, account_type,
    account_registration_type, tax_status, qualified_flag.
    Returns empty DataFrame if not yet built (script degrades gracefully).
    """
    print("Loading accounts dimension...", end=' ', flush=True)
    key = 'gold/accounts_dimension_latest.parquet'
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        # Keep only the columns we need for enrichment
        keep = ['account_id', 'relationship_id', 'account_name', 'account_type',
                'account_registration_type', 'tax_status', 'qualified_flag']
        available = [c for c in keep if c in df.columns]
        df = df[available].drop_duplicates(subset=['account_id'], keep='first')
        print(f"{len(df):,} accounts")
        return df
    except Exception as e:
        print(f"not found ({e}) — lots will lack tax metadata")
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Core FIFO lot builder
# ---------------------------------------------------------------------------

def build_lots_for_group(
        account_id: str,
        asset_name: str,
        group_txns: pd.DataFrame,
) -> List[dict]:
    """
    Build open lot list for one (account, asset) position using FIFO.

    Process:
    1. Create one lot per buy transaction (sorted oldest first)
    2. Apply sells in chronological order, depleting oldest lots first
    3. Return all lots with remaining units (open lots)
       plus closed lots (for realized gain tracking)

    Expects a pre-classified '_is_buy' boolean column on group_txns
    (True = buy/CA-buy, False = sell/CA-sell).

    Returns list of lot dicts.
    """
    buys = (group_txns[group_txns['_is_buy']]
            .sort_values('trade_date')
            .reset_index(drop=True))
    sells = (group_txns[~group_txns['_is_buy']]
             .sort_values('trade_date')
             .reset_index(drop=True))

    if len(buys) == 0:
        return []

    # Initialize lots
    lots = []
    for lot_idx, (_, row) in enumerate(buys.iterrows(), start=1):
        units = abs(row['units'])
        if units == 0:
            continue
        mv = abs(row.get('market_value', 0) or 0)
        cost_per_unit = mv / units if units > 0 else 0.0
        lots.append({
            'lot_index': lot_idx,
            'acquisition_date': row['trade_date'],
            'original_units': units,
            'remaining_units': units,
            'cost_per_unit': cost_per_unit,
        })

    # Apply sells (FIFO: oldest lot first)
    sell_events = list(sells[['trade_date', 'units']].itertuples(index=False, name=None))

    lot_ptr = 0  # Index of oldest not-fully-depleted lot
    for sell_date, sell_units_raw in sell_events:
        remaining_to_sell = abs(sell_units_raw)

        i = lot_ptr
        while remaining_to_sell > 0 and i < len(lots):
            lot = lots[i]
            if lot['acquisition_date'] > sell_date:
                break  # Selling a lot that doesn't exist yet — data anomaly, skip
            consumed = min(lot['remaining_units'], remaining_to_sell)
            lot['remaining_units'] -= consumed
            remaining_to_sell -= consumed
            if lot['remaining_units'] <= 1e-8:
                lot['remaining_units'] = 0.0
                lot_ptr = i + 1  # This lot is fully consumed
            i += 1

    return lots


def build_holdings_lots_snapshot(
        transactions: pd.DataFrame,
        latest_prices: pd.DataFrame,
        accounts_dim: pd.DataFrame,
        snapshot_date: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    """
    Build holdings lots snapshot for all open positions.

    Args:
        transactions:  All transactions (source of truth for positions)
        latest_prices: Latest canonical price per asset
        accounts_dim:  Accounts dimension (tax_status, qualified_flag, relationship_id, etc.)
        snapshot_date: Date for this snapshot (default: today)

    Returns:
        DataFrame with lot-level rows, enriched with account tax metadata.
    """
    if snapshot_date is None:
        snapshot_date = pd.Timestamp.now().normalize()

    print(f"\n=== Building holdings lots snapshot for {snapshot_date.date()} ===")

    type_col = 'transaction_type' if 'transaction_type' in transactions.columns else 'action'
    sub_col = 'transaction_sub_type' if 'transaction_sub_type' in transactions.columns else None

    # Filter to transactions on or before snapshot date
    txn = transactions[transactions['trade_date'] <= snapshot_date].copy()

    # Classify unit-changing transactions: standard buy/sell + Corporate Actions
    is_buy = txn[type_col].isin(BUY_TYPES)
    is_sell = txn[type_col].isin(SELL_TYPES)
    is_ca = txn[type_col] == 'Corporate Action'
    if sub_col and is_ca.any():
        is_ca_buy = is_ca & txn[sub_col].isin(CA_BUY_SUBTYPES)
        is_ca_sell = is_ca & txn[sub_col].isin(CA_SELL_SUBTYPES)
        n_ca = int(is_ca.sum())
        n_ca_buy = int(is_ca_buy.sum())
        n_ca_sell = int(is_ca_sell.sum())
        print(f"  Corporate Actions: {n_ca:,} total "
              f"(buy={n_ca_buy:,}, sell={n_ca_sell:,}, "
              f"unclassified={n_ca - n_ca_buy - n_ca_sell:,})")
    else:
        is_ca_buy = pd.Series(False, index=txn.index)
        is_ca_sell = pd.Series(False, index=txn.index)

    all_buy = is_buy | is_ca_buy
    all_sell = is_sell | is_ca_sell

    # Filter to unit-changing transactions with valid assets
    unit_mask = (all_buy | all_sell) & txn['asset_name'].notna() & (txn['units'] != 0)
    unit_txns = txn[unit_mask].copy()
    unit_txns['_is_buy'] = all_buy[unit_mask]

    groups = list(unit_txns.groupby(['account_id', 'asset_name'], sort=False))
    total = len(groups)
    print(f"  Processing {total:,} (account, asset) groups...")

    all_lots = []
    for i, ((account_id, asset_name), grp) in enumerate(groups):
        lots = build_lots_for_group(account_id, asset_name, grp)

        for lot in lots:
            # Only include lots with meaningful remaining units
            if lot['remaining_units'] < 1e-8:
                is_open = False
                lot['remaining_units'] = 0.0
            else:
                is_open = True

            holding_days = (snapshot_date - lot['acquisition_date']).days

            all_lots.append({
                'lot_id': (f"{account_id}:{asset_name}:"
                           f"{lot['lot_index']}:{lot['acquisition_date'].date()}"),
                'snapshot_date': snapshot_date,
                'account_id': account_id,
                'asset_name': asset_name,
                'acquisition_date': lot['acquisition_date'],
                'lot_index': lot['lot_index'],
                'original_units': lot['original_units'],
                'current_units': lot['remaining_units'],
                'cost_per_unit': lot['cost_per_unit'],
                'cost_basis': lot['remaining_units'] * lot['cost_per_unit'],
                'holding_period_days': holding_days,
                'term': 'short_term' if holding_days < SHORT_TERM_DAYS else 'long_term',
                'is_open': is_open,
            })

        if (i + 1) % 10000 == 0:
            print(f"    [{i+1:,}/{total:,}] {(i+1)/total*100:.0f}%")

    print(f"  Generated {len(all_lots):,} lots")

    if not all_lots:
        return pd.DataFrame()

    df = pd.DataFrame(all_lots)

    # Join latest prices
    df = df.merge(
        latest_prices[['asset_name', 'ticker', 'price', 'source']].rename(
            columns={'price': 'current_price', 'source': 'price_quality'}
        ),
        on='asset_name',
        how='left',
    )

    # Market value and accrued gain
    df['market_value'] = df['current_units'] * df['current_price']
    df['accrued_gain'] = df['market_value'].fillna(0.0) - df['cost_basis']

    # Enrich with account metadata (tax_status, qualified_flag, relationship_id, etc.)
    if not accounts_dim.empty:
        df = df.merge(accounts_dim, on='account_id', how='left')
    else:
        # Graceful degradation — populate with nulls so schema is consistent
        for col in ['relationship_id', 'account_name', 'account_type',
                    'account_registration_type', 'tax_status', 'qualified_flag']:
            df[col] = None

    # purchase_year — derived from acquisition_date; avoids repeated compute downstream
    df['purchase_year'] = df['acquisition_date'].dt.year.astype('Int64')

    # Column order
    cols = [
        'lot_id', 'snapshot_date',
        # Account context
        'account_id', 'relationship_id', 'account_name',
        'account_type', 'account_registration_type',
        'tax_status', 'qualified_flag',
        # Position identity
        'asset_name', 'ticker',
        # Lot detail
        'acquisition_date', 'purchase_year', 'lot_index',
        'original_units', 'current_units',
        'cost_per_unit', 'cost_basis',
        'current_price', 'market_value', 'accrued_gain',
        'holding_period_days', 'term', 'is_open', 'price_quality',
    ]
    df = df[[c for c in cols if c in df.columns]]
    df = df.sort_values(['account_id', 'asset_name', 'lot_index']).reset_index(drop=True)

    # Summary
    open_lots = df[df['is_open']]
    print(f"\n  Open lots:          {len(open_lots):,}")
    print(f"  Unique positions:   {open_lots.groupby(['account_id', 'asset_name']).ngroups:,}")
    print(f"  Total market value: ${open_lots['market_value'].sum():,.0f}")
    print(f"  Total cost basis:   ${open_lots['cost_basis'].sum():,.0f}")
    print(f"  Accrued gain:       ${open_lots['accrued_gain'].sum():,.0f}")
    if 'tax_status' in open_lots.columns:
        print(f"\n  By tax_status:")
        for ts, grp in open_lots.groupby('tax_status', dropna=False):
            mv = grp['market_value'].sum()
            print(f"    {str(ts):<14}  {len(grp):>8,} lots  MV=${mv:>12,.0f}")
    print(f"\n  By term:")
    for term, grp in open_lots.groupby('term'):
        mv = grp['market_value'].sum()
        gain = grp['accrued_gain'].sum()
        print(f"    {term:<12}  {len(grp):>8,} lots  "
              f"MV=${mv:>12,.0f}  Gain=${gain:>12,.0f}")

    return df


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_lots(df: pd.DataFrame, upload: bool = False, full: bool = False):
    """Save holdings lots to gold layer."""
    print("\n=== Saving holdings lots ===")

    snap_date = df['snapshot_date'].iloc[0].strftime('%Y-%m-%d')

    if full:
        output_key = f"gold/holdings_lots/backfill_{snap_date}.parquet"
    else:
        output_key = f"gold/holdings_lots/{snap_date}.parquet"

    local_path = Path(f'/tmp/holdings_lots_{snap_date}.parquet')
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
        description='Build Holdings Lots (FIFO lot tracking for tax)'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    parser.add_argument('--full', action='store_true',
                        help='Backfill mode (uses all history)')
    parser.add_argument('--date', type=str, default=None,
                        help='Snapshot date YYYY-MM-DD (default: today)')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD HOLDINGS LOTS")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    transactions = load_transactions()
    latest_prices = load_latest_prices()
    accounts_dim = load_accounts_dimension()

    snapshot_date = (pd.Timestamp(args.date) if args.date
                     else pd.Timestamp.now().normalize())

    print(f"\n  Snapshot date: {snapshot_date.date()}")

    lots = build_holdings_lots_snapshot(transactions, latest_prices, accounts_dim, snapshot_date)

    if len(lots) == 0:
        print("\nWARNING: No open lots found")
        return 0

    if not args.dry_run:
        save_lots(lots, upload=args.upload, full=args.full)

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(lots):,} lots | {lots['is_open'].sum():,} open")
    print(f"  Open AUA: ${lots[lots['is_open']]['market_value'].sum():,.0f}")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
