#!/usr/bin/env python3
"""
02_build_positions_cube.py — Daily Holdings Per Account

Stage 2 of the BD gold layer pipeline.

Builds gold/positions_cube/YYYY-MM-DD.parquet — one file per calendar day,
containing every (account_id, asset_name, units) where units > 0 on that day.
Derived entirely from silver/transactions/.

Output columns: date, account_id, asset_name, units

Memory strategy:
  - Process accounts sorted by first-transaction date (oldest first)
  - After each batch, flush date partitions that are "safe" — i.e., all
    remaining unprocessed accounts started after that date, so no more
    contributions can arrive for it
  - Use category dtypes for string columns to cut string memory ~10x
  - Peak memory ~2-4GB on typical BD dataset (r6i.xlarge safe)

Pipeline context:
  Stage 1: build_canonical_prices_v2.py  → silver/prices/canonical_prices.parquet
  Stage 2: THIS SCRIPT                   → gold/positions_cube/YYYY-MM-DD.parquet
  Stage 3: (join script, TBD)            → gold/valued_positions/YYYY-MM-DD.parquet

Usage:
    python 02_build_positions_cube.py                         # full rebuild
    python 02_build_positions_cube.py --date 2026-02-20       # single date
    python 02_build_positions_cube.py --start-date 2026-01-01 # from date onward
    python 02_build_positions_cube.py --dry-run               # stats, no writes
"""

import argparse
import gc
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import boto3
import numpy as np
import pandas as pd

S3_BUCKET = 'opal-data-bd'
S3_TXN_PREFIX = 'silver/transactions/'
S3_OUTPUT_PREFIX = 'gold/positions_cube/'

ACCOUNT_BATCH_SIZE = 500   # accounts processed per batch
LOCAL_TMP = Path('/tmp/positions_cube_batch.parquet')
MAX_WORKERS = 64           # parallel S3 read threads (I/O-bound)

s3 = boto3.client('s3', region_name='us-east-1')


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))

# Transaction types that change unit holdings (matched to silver/transactions/ values)
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
# Corporate Actions are classified as transaction_type='Corporate Action'
# but the sub-type determines whether units are added or removed.
CA_BUY_SUBTYPES = frozenset({
    'Conversion In',   # new share class appears (paired with Conversion Out)
    'Spinoff',         # new position spun off from parent
    'Split',           # additional units from stock split
})
CA_SELL_SUBTYPES = frozenset({
    'Merger',          # old ticker ceases to exist → units exit
    'Conversion Out',  # old share class leaves (paired with Conversion In)
    'Cash in Lieu',    # fractional share cleanup → small unit removal
    'Reverse Split',   # units reduced by reverse split
})



# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _load_open_account_ids(date_str: str) -> set:
    """
    Load silver/allocations/{date_str}.parquet and return the set of account_ids
    where account_is_open is True.

    Used by _compute_account_end_dates() to confirm which backfill-only accounts
    are still active according to BD's daily allocation snapshot. Backfill-only
    accounts confirmed open here are assigned global_end_date rather than being
    capped at their last transaction date.

    Returns an empty set if the allocation file is unavailable or missing the
    required columns -- the caller falls back to existing BKF cap behavior.
    """
    key = f'silver/allocations/{date_str}.parquet'
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        alloc = pd.read_parquet(BytesIO(resp['Body'].read()))
        if 'account_id' not in alloc.columns or 'account_is_open' not in alloc.columns:
            print(f"  WARN: allocations/{date_str}.parquet missing account_id or account_is_open -- BKF cap unchanged")
            return set()
        is_open = alloc['account_is_open'].astype(str).str.lower().isin(['true', '1', 'yes'])
        open_ids = set(alloc.loc[is_open, 'account_id'].dropna())
        print(f"  OK: allocations/{date_str} -- {len(open_ids):,} confirmed-open accounts")
        return open_ids
    except Exception as e:
        print(f"  WARN: allocations/{date_str}.parquet not available -- BKF cap unchanged: {e}")
        return set()


def load_transactions() -> pd.DataFrame:
    """Load full transaction history from silver/transactions/ with parallel I/O."""
    print("Loading transactions (parallel)... ", end='', flush=True)

    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_TXN_PREFIX)
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])

    if not keys:
        raise RuntimeError("No transaction parquet files found in silver/transactions/")

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

    df['trade_date'] = pd.to_datetime(df['trade_date'])

    if 'transaction_id' in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=['transaction_id'], keep='last')
        removed = before - len(df)
        print(f"{len(df):,} rows ({removed:,} dupes) in {elapsed:.1f}s")
    else:
        print(f"{len(df):,} rows in {elapsed:.1f}s")

    return df


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_unit_events(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to unit-changing transactions and compute cumulative units
    per (account_id, asset_name) over time.

    Handles three categories:
      1. Standard buy/sell types (Buy, Sale, Transfer In/Out, etc.)
      2. Corporate Actions — classified by transaction_sub_type:
         - Merger, Conversion Out, Cash in Lieu, Reverse Split → sell (subtract units)
         - Conversion In, Spinoff, Split → buy (add units)
      3. Corporate Action Adjustment — treated as a unit correction (added as-is)

    Returns DataFrame: account_id, asset_name, trade_date, cum_units
    Sorted by (account_id, asset_name, trade_date).
    """
    type_col = 'transaction_type' if 'transaction_type' in transactions.columns else 'action'
    sub_col = 'transaction_sub_type' if 'transaction_sub_type' in transactions.columns else None

    # Standard buy/sell classification
    is_buy  = transactions[type_col].isin(BUY_TYPES)
    is_sell = transactions[type_col].isin(SELL_TYPES)

    # Corporate Action classification via sub-type
    is_ca = transactions[type_col] == 'Corporate Action'
    if sub_col and is_ca.any():
        is_ca_buy  = is_ca & transactions[sub_col].isin(CA_BUY_SUBTYPES)
        is_ca_sell = is_ca & transactions[sub_col].isin(CA_SELL_SUBTYPES)
        n_ca_buy  = is_ca_buy.sum()
        n_ca_sell = is_ca_sell.sum()
        n_ca_unclassified = is_ca.sum() - n_ca_buy - n_ca_sell
        print(f"  Corporate Actions: {is_ca.sum():,} total "
              f"(buy={n_ca_buy:,}, sell={n_ca_sell:,}, "
              f"unclassified={n_ca_unclassified:,})")
    else:
        is_ca_buy  = pd.Series(False, index=transactions.index)
        is_ca_sell = pd.Series(False, index=transactions.index)

    # Combine: standard + CA
    all_buy  = is_buy | is_ca_buy
    all_sell = is_sell | is_ca_sell

    unit_txns = transactions[all_buy | all_sell].copy()
    unit_txns = unit_txns[unit_txns['asset_name'].notna() & (unit_txns['units'] != 0)]

    print(f"  Unit-changing transactions: {len(unit_txns):,} "
          f"(buys: {all_buy.sum():,}, sells: {all_sell.sum():,})")

    unit_txns['signed_units'] = np.where(
        unit_txns.index.isin(transactions.index[all_buy]),
        unit_txns['units'].abs(),
        -unit_txns['units'].abs(),
    )

    # Sum same-day transactions per (account, asset), then cumsum
    daily = (
        unit_txns
        .groupby(['account_id', 'asset_name', 'trade_date'], sort=True)['signed_units']
        .sum()
        .reset_index()
    )
    daily = daily.sort_values(['account_id', 'asset_name', 'trade_date'])
    daily['cum_units'] = (
        daily.groupby(['account_id', 'asset_name'], sort=False)['signed_units']
        .cumsum()
    )

    n_pairs = daily.groupby(['account_id', 'asset_name']).ngroups
    print(f"  Unique (account, asset) pairs: {n_pairs:,}")

    return daily[['account_id', 'asset_name', 'trade_date', 'cum_units']]



def expand_pairs_to_daily(
        unit_events: pd.DataFrame,
        global_end_date: pd.Timestamp,
        account_end_dates: dict | None = None,
        expand_start_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """
    Expand (account_id, asset_name) cumulative unit events to a continuous
    daily timeline. Forward-fills cum_units between transaction dates.
    Keeps only rows where units > 0 (position is open).

    Forward-fill end date per account:
      - Accounts present in daily transaction exports: fill to global_end_date
        (these are confirmed active by the live pipeline).
      - Accounts that exist ONLY in the backfill: fill to their own last
        transaction date. These accounts left the active universe before the
        daily pipeline started — continuing to forward-fill creates phantom
        AUA that grows indefinitely.

    The account_end_dates dict maps account_id → end_date. Accounts not in
    the dict default to global_end_date (the safe default for active accounts).

    expand_start_date: if provided, only materialize dates >= this date.
    The full cumulative unit history is still computed from the first
    transaction, but only dates in the target window are emitted. This
    saves memory during partial rebuilds (--start-date) while preserving
    buy-and-hold positions that had no recent transactions.

    Returns DataFrame: date, account_id, asset_name, units
    Uses category dtypes for string columns to reduce memory ~10x.
    """
    results = []

    for (account_id, asset_name), group in unit_events.groupby(
            ['account_id', 'asset_name'], sort=False):

        first_date = group['trade_date'].min()
        # Per-account end date: backfill-only accounts stop at their last txn,
        # active accounts fill to global_end_date
        if account_end_dates is not None and account_id in account_end_dates:
            last_date = account_end_dates[account_id]
        else:
            last_date = global_end_date

        if last_date < first_date:
            continue

        dates = pd.date_range(first_date, last_date, freq='D')

        units_series = (
            group.set_index('trade_date')['cum_units']
            .reindex(dates, method='ffill')
        )

        open_mask = units_series > 0
        if not open_mask.any():
            continue

        # Clip to expansion window — cumulative units are correct because
        # the full history was used for reindex+ffill above, but we only
        # emit dates in the target range to save memory during partial rebuilds.
        if expand_start_date is not None:
            open_mask = open_mask & (units_series.index >= expand_start_date)
            if not open_mask.any():
                continue

        results.append(pd.DataFrame({
            'date':       units_series.index[open_mask],
            'account_id': account_id,
            'asset_name': asset_name,
            'units':      units_series.values[open_mask],
        }))

    if not results:
        return pd.DataFrame(columns=['date', 'account_id', 'asset_name', 'units'])

    df = pd.concat(results, ignore_index=True)
    del results; gc.collect()

    # Category dtypes cut string memory ~10x
    df['account_id'] = df['account_id'].astype('category')
    df['asset_name']  = df['asset_name'].astype('category')

    return df


# ---------------------------------------------------------------------------
# Partition I/O
# ---------------------------------------------------------------------------

def write_partition(date_str: str, frames: list, dry_run: bool = False) -> int:
    """Concat frames, write to S3 as gold/positions_cube/YYYY-MM-DD.parquet."""
    df = pd.concat(frames, ignore_index=True)

    # Restore plain strings for parquet compatibility
    for col in ('account_id', 'asset_name'):
        if hasattr(df[col], 'cat'):
            df[col] = df[col].astype(str)

    df = df[['account_id', 'asset_name', 'units']].sort_values(
        ['account_id', 'asset_name']
    ).reset_index(drop=True)

    if dry_run:
        return len(df)

    df.to_parquet(LOCAL_TMP, index=False, engine='pyarrow', compression='snappy')
    s3.upload_file(str(LOCAL_TMP), S3_BUCKET, f'{S3_OUTPUT_PREFIX}{date_str}.parquet')
    return len(df)


def flush_safe_dates(date_buffers: dict, safe_before: str,
                     dry_run: bool, stats: dict):
    """Write all buffered date partitions with date_str < safe_before."""
    to_flush = sorted(d for d in date_buffers if d < safe_before)
    for date_str in to_flush:
        n = write_partition(date_str, date_buffers.pop(date_str), dry_run)
        stats['rows_written'] += n
        stats['partitions_written'] += 1
        if stats['partitions_written'] % 100 == 0:
            print(f"  ... {stats['partitions_written']:,} partitions written "
                  f"({stats['rows_written']:,} rows total)")


def _compute_account_end_dates(transactions: pd.DataFrame,
                               open_account_ids: set | None = None) -> dict:
    """
    Determine the forward-fill end date for each account based on whether
    the account appears in daily transaction export files.

    Signal: the _source_file column distinguishes backfill data (empty string
    or non-TXN_DAILY filenames) from live daily exports (TXN_DAILY_*.xlsx).

    - Accounts with at least one daily export transaction -> None (use global_end_date)
    - Accounts with ONLY backfill transactions -> evaluated against open_account_ids:
        - If account appears in open_account_ids (confirmed open by BD allocations):
          use global_end_date. BD's daily allocation snapshot is the liveness signal
          that the TXN_DAILY feed normally provides for active accounts.
        - Otherwise: cap at last transaction date to prevent phantom AUA from accounts
          that genuinely left the active universe.

    open_account_ids: set of account_ids confirmed open by silver/allocations/{date}.
      Load via _load_open_account_ids(). Pass None or empty set to preserve the
      original cap-all-backfill behavior (safe fallback when allocations unavailable).

    Returns dict of {account_id: pd.Timestamp} for backfill-only accounts that are
    still capped. Accounts NOT in the dict should use global_end_date.
    """
    if '_source_file' not in transactions.columns:
        print("  WARNING: no _source_file column — cannot determine account liveness")
        print("  All accounts will use global_end_date (no backfill-only filtering)")
        return {}

    # Classify each transaction as daily-export vs backfill
    is_daily = transactions['_source_file'].str.contains('TXN_DAILY', na=False)

    # Accounts that have at least one daily-export transaction are "active"
    accounts_with_daily = set(transactions.loc[is_daily, 'account_id'].unique())

    # Accounts that appear ONLY in backfill data
    all_accounts = set(transactions['account_id'].unique())
    backfill_only_accounts = all_accounts - accounts_with_daily

    # Cross-reference BKF accounts against BD allocation confirmed-open set.
    # Accounts confirmed open by allocations are treated as active: they hold
    # real positions BD can see but haven't generated a TXN_DAILY record
    # (buy-and-hold clients). Cap only the remainder.
    if open_account_ids:
        bkf_alloc_confirmed = backfill_only_accounts & open_account_ids
        bkf_still_capped = backfill_only_accounts - bkf_alloc_confirmed
    else:
        bkf_alloc_confirmed = set()
        bkf_still_capped = backfill_only_accounts

    # For still-capped accounts, end date = their last transaction date
    last_txn = (
        transactions[transactions['account_id'].isin(bkf_still_capped)]
        .groupby('account_id')['trade_date']
        .max()
    )

    account_end_dates = last_txn.to_dict()

    n_active = len(accounts_with_daily)
    n_alloc_extended = len(bkf_alloc_confirmed)
    n_capped = len(account_end_dates)
    print(f"  Accounts with daily export data (active):         {n_active:,} -> use global_end_date")
    print(f"  Accounts backfill-only, confirmed open by alloc:  {n_alloc_extended:,} -> use global_end_date")
    print(f"  Accounts backfill-only (capped):                  {n_capped:,} -> fill to last txn date")
    if account_end_dates:
        dates = list(account_end_dates.values())
        earliest = min(dates)
        latest = max(dates)
        print(f"  Capped end-date range: {earliest.date()} -> {latest.date()}")

    return account_end_dates


# ---------------------------------------------------------------------------
# Full rebuild
# ---------------------------------------------------------------------------

def build_full(dry_run: bool = False,
               start_date: str | None = None,
               end_date:   str | None = None):
    """
    Full (or date-range) rebuild of gold/positions_cube/.

    Accounts are processed sorted by first-transaction date so early date
    partitions can be flushed to S3 before all accounts are done, keeping
    peak memory bounded.
    """
    print("=" * 70)
    print("BUILD POSITIONS CUBE — FULL REBUILD" + (" [DRY RUN]" if dry_run else ""))
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    if start_date:
        print(f"Range:   {start_date} → {end_date or 'present'}")
    print("=" * 70)

    # --- Load ---
    print("\n=== Step 1: Load transactions ===")
    transactions = load_transactions()

    print("\n=== Step 2: Compute unit events ===")
    unit_events = compute_unit_events(transactions)

    print("\n=== Step 2b: Load BD allocations for BKF liveness confirmation ===")
    # Use the max trade date in unit_events as the allocation date to check
    # (capped by --end-date if specified). Backfill-only accounts confirmed open
    # by that allocation file are extended to global_end_date rather than capped.
    _alloc_date = unit_events['trade_date'].max()
    if end_date:
        _alloc_date = min(_alloc_date, pd.Timestamp(end_date))
    open_account_ids = _load_open_account_ids(_alloc_date.strftime('%Y-%m-%d'))

    print("\n=== Step 2c: Determine per-account forward-fill end dates ===")
    account_end_dates = _compute_account_end_dates(transactions, open_account_ids)

    del transactions; gc.collect()

    # NOTE: --start-date does NOT filter unit_events. All transactions are
    # needed to compute correct cumulative units for buy-and-hold positions.
    # The date window is applied inside expand_pairs_to_daily() so only
    # dates >= start_date are materialized, but cum_units are computed from
    # the full history. This prevents the old bug where partial rebuilds
    # dropped accounts with no recent transactions.
    expand_start_dt = pd.Timestamp(start_date) if start_date else None

    if end_date:
        unit_events = unit_events[
            unit_events['trade_date'] <= pd.Timestamp(end_date)
        ].copy()

    # --- Sort accounts by first-txn date for early flushing ---
    print("\n=== Step 3: Expand to daily timeline ===")
    # global_end_date: every open position is forward-filled to this date.
    # Using the last transaction date ensures "buy and hold" positions
    # (no transactions since purchase) still appear in all subsequent partitions.
    global_end_date = unit_events['trade_date'].max()
    if end_date:
        global_end_date = min(global_end_date, pd.Timestamp(end_date))
    print(f"  Global end date (forward-fill target): {global_end_date.date()}")

    first_dates = (
        unit_events.groupby('account_id')['trade_date']
        .min()
        .sort_values()
    )
    accounts_sorted = first_dates.index.tolist()
    n_accounts = len(accounts_sorted)
    n_batches  = (n_accounts + ACCOUNT_BATCH_SIZE - 1) // ACCOUNT_BATCH_SIZE
    print(f"  Accounts: {n_accounts:,}  →  {n_batches:,} batches of {ACCOUNT_BATCH_SIZE}")

    date_buffers: dict[str, list] = defaultdict(list)
    stats = {'rows_written': 0, 'partitions_written': 0}

    for batch_i in range(n_batches):
        batch_accounts = accounts_sorted[
            batch_i * ACCOUNT_BATCH_SIZE : (batch_i + 1) * ACCOUNT_BATCH_SIZE
        ]
        batch_events = unit_events[
            unit_events['account_id'].isin(set(batch_accounts))
        ]

        batch_df = expand_pairs_to_daily(batch_events, global_end_date, account_end_dates,
                                         expand_start_date=expand_start_dt)
        if len(batch_df) == 0:
            continue

        # Apply end-date window (start_date already handled by expand_start_date)
        if end_date:
            batch_df = batch_df[batch_df['date'] <= pd.Timestamp(end_date)]

        # Accumulate into date buffers
        for date_val, day_df in batch_df.groupby('date'):
            date_str = date_val.strftime('%Y-%m-%d')
            date_buffers[date_str].append(
                day_df[['account_id', 'asset_name', 'units']].copy()
            )
        del batch_df; gc.collect()

        # Flush dates that no remaining account can contribute to
        next_idx = (batch_i + 1) * ACCOUNT_BATCH_SIZE
        if next_idx < n_accounts:
            safe_before = first_dates.iloc[next_idx].strftime('%Y-%m-%d')
            flush_safe_dates(date_buffers, safe_before, dry_run, stats)

        if (batch_i + 1) % 10 == 0 or (batch_i + 1) == n_batches:
            print(f"  Batch {batch_i+1:,}/{n_batches:,} — "
                  f"buffered dates: {len(date_buffers):,}, "
                  f"written: {stats['partitions_written']:,}")

    # --- Flush everything remaining ---
    print("\n=== Step 4: Flush remaining partitions ===")
    flush_safe_dates(date_buffers, '9999-12-31', dry_run, stats)

    print("\n" + "=" * 70)
    print("DONE" + (" [DRY RUN]" if dry_run else ""))
    print(f"  Partitions : {stats['partitions_written']:,}")
    print(f"  Rows       : {stats['rows_written']:,}")
    if not dry_run:
        print(f"  Output     : s3://{S3_BUCKET}/{S3_OUTPUT_PREFIX}")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Single date snapshot
# ---------------------------------------------------------------------------

def build_single_date(target_date: str, dry_run: bool = False):
    """
    Build (or rebuild) one date partition.

    Takes the latest cumulative unit balance per (account_id, asset_name)
    as of target_date, keeps units > 0.
    """
    print("=" * 70)
    print(f"BUILD POSITIONS CUBE — {target_date}" + (" [DRY RUN]" if dry_run else ""))
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    target_dt = pd.Timestamp(target_date)

    print("\n=== Step 1: Load transactions ===")
    transactions = load_transactions()

    print("\n=== Step 2: Snapshot as of target date ===")
    type_col = 'transaction_type' if 'transaction_type' in transactions.columns else 'action'

    is_unit = (
        transactions[type_col].isin(BUY_TYPES) |
        transactions[type_col].isin(SELL_TYPES)
    )
    unit_txns = transactions[
        is_unit &
        transactions['asset_name'].notna() &
        (transactions['units'] != 0) &
        (transactions['trade_date'] <= target_dt)
    ].copy()
    del transactions; gc.collect()

    print(f"  Unit-changing transactions ≤ {target_date}: {len(unit_txns):,}")

    if len(unit_txns) == 0:
        print("  No transactions — writing empty partition")
        result = pd.DataFrame(columns=['date', 'account_id', 'asset_name', 'units'])
    else:
        unit_txns['signed_units'] = np.where(
            unit_txns[type_col].isin(BUY_TYPES),
            unit_txns['units'].abs(),
            -unit_txns['units'].abs(),
        )

        daily = (
            unit_txns
            .groupby(['account_id', 'asset_name', 'trade_date'], sort=True)['signed_units']
            .sum()
            .reset_index()
            .sort_values(['account_id', 'asset_name', 'trade_date'])
        )
        daily['cum_units'] = (
            daily.groupby(['account_id', 'asset_name'], sort=False)['signed_units']
            .cumsum()
        )

        snapshot = (
            daily.groupby(['account_id', 'asset_name'])['cum_units']
            .last()
            .reset_index()
            .rename(columns={'cum_units': 'units'})
        )
        snapshot = snapshot[snapshot['units'] > 0].copy()
        snapshot['date'] = target_dt
        result = snapshot[['date', 'account_id', 'asset_name', 'units']]

    print(f"  Open positions on {target_date}: {len(result):,}")
    print(f"  Unique accounts: {result['account_id'].nunique():,}")
    print(f"  Unique assets:   {result['asset_name'].nunique():,}")

    if dry_run:
        print("\n[DRY RUN] No writes.")
        return

    print("\n=== Step 3: Write partition ===")
    out = result[['account_id', 'asset_name', 'units']].sort_values(
        ['account_id', 'asset_name']
    ).reset_index(drop=True)

    out.to_parquet(LOCAL_TMP, index=False, engine='pyarrow', compression='snappy')
    size_kb = LOCAL_TMP.stat().st_size / 1024
    s3.upload_file(str(LOCAL_TMP), S3_BUCKET, f'{S3_OUTPUT_PREFIX}{target_date}.parquet')
    LOCAL_TMP.unlink()

    print(f"  ✓ s3://{S3_BUCKET}/{S3_OUTPUT_PREFIX}{target_date}.parquet  ({size_kb:.0f} KB)")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Build Positions Cube')
    parser.add_argument('--date',       help='Single date partition (YYYY-MM-DD)')
    parser.add_argument('--start-date', help='Range start date (YYYY-MM-DD)')
    parser.add_argument('--end-date',   help='Range end date (YYYY-MM-DD)')
    parser.add_argument('--dry-run',    action='store_true', help='Stats only, no writes')
    parser.add_argument('--upload',     action='store_true', help='No-op (script always uploads unless --dry-run)')
    args = parser.parse_args()

    try:
        if args.date:
            build_single_date(args.date, dry_run=args.dry_run)
        else:
            build_full(
                dry_run=args.dry_run,
                start_date=args.start_date,
                end_date=args.end_date,
            )
        return 0
    except Exception as e:
        print(f"\nFATAL: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
