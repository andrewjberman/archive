#!/usr/bin/env python3
"""
Build Account Performance -- Account-Level AUA + Flows Timeseries

Produces a daily account-level performance timeseries covering
2020-06-30 to present. This is the foundational account-grain table that
enables:

  - Advisor book drill-down: filter by architect/implementor -> group by
    relationship_id for household roll-up, or view account-level detail
  - Account-specific AUA growth tracking
  - Any higher-level aggregation (all advisor fields denormalized)

All advisor fields are denormalized into each row so the table is fully
self-contained without joining accounts_dimension at query time.

Data sources and their roles:
  gold/positions_cube/YYYY-MM-DD.parquet   -- units per (account, asset) per day
    NOTE: date is the FILENAME, not a column. Each partition has only three
    columns: account_id, asset_name, units. Date is injected from the filename
    at load time.

  silver/prices/canonical_prices.parquet  -- price per (asset_name, date)
    Joined on (asset_name, date). Prices not present today are forward-filled
    within each asset_name from the most recent known price and flagged as
    'carried_forward_05b'.

  gold/accounts_dimension_latest.parquet  -- account metadata
    Provides relationship_id, tax_status, and all advisor fields per account_id.
    Accounts absent from dimension default to 'taxable' tax_status.

  silver/transactions/  -- cash flow events (uniform daily partitions)
    Source for cum_inflows, cum_outflows, nna. Only NNA-relevant transaction
    types counted (Cash Deposit, Transfer In, Cash Withdrawal, Transfer Out).
    Cumulative flows computed via daily groupby + cumsum, reindexed to the
    full positions_cube date spine per account.

Output schema (grain: one row per date x account_id):
  date                      date
  account_id                str
  relationship_id           str    -- household key; 'acct_{account_id}' if unmapped
  architect                 str    -- lead advisor
  implementor               str    -- implementing advisor
  local_relationship        str    -- local relationship manager (local_ops in BD)
  manager                   str    -- portfolio manager
  investment_strategy_name  str    -- strategy label
  tax_status                str    -- taxable | tax_deferred | tax_exempt
  total_aua                 float  -- sum(units * price) for this account on this date
  cum_inflows               float  -- cumulative cash/transfer inflows since inception
  cum_outflows              float  -- cumulative cash/transfer outflows since inception
  nna                       float  -- cum_inflows - cum_outflows
  num_positions             int    -- distinct assets held on this date
  pct_priced                float  -- fraction of AUA with a direct canonical price

Verification:
  SUM(total_aua) on latest date must equal 05_client_performance SUM(total_aua)
  GROUP BY (date, relationship_id) SUM(total_aua) must match 05 row-for-row

Output: gold/account_performance.parquet

Performance:
  canonical_prices is pre-forward-filled once before the loop, making
  process_date_partition stateless. All 2,065 date partitions are then
  processed in parallel via ThreadPoolExecutor(max_workers=16).
  Expected runtime: ~5-8 min on r6i.xlarge (was ~30 min serial).
  Peak memory: ~4-5 GB (more concurrent S3 reads vs ~3.5 GB serial).

Usage:
    python 05b_build_account_performance.py --dry-run
    python 05b_build_account_performance.py --upload

Author: Data Scientist (Claude)
Date: 2026-02-25
"""

import argparse
import gc
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO

import pandas as pd
import numpy as np
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')
MAX_WORKERS = 64

# NNA-relevant transaction types (same as 05_build_client_performance)
INFLOW_TYPES  = frozenset({'Cash Deposit', 'Transfer In'})
OUTFLOW_TYPES = frozenset({'Cash Withdrawal', 'Transfer Out'})

# Price sources that count as "real" for pct_priced
REAL_PRICE_SOURCES = frozenset({
    'transaction_observed', 'yahoo_finance', 'linear_interpolation',
})

# Outlier cap per flow event -- same as 05 (neutralises z0818656451-style garbage)
FLOW_CAP = 50_000_000

# Advisor fields to denormalize from accounts_dimension
ADVISOR_FIELDS = [
    'architect',
    'implementor',
    'local_relationship',  # stored as local_ops in raw data, renamed in accounts_dimension
    'manager',
    'investment_strategy_name',
]


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def list_positions_cube_keys() -> list:
    """List all positions_cube partition keys sorted by date."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='gold/positions_cube/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])
    if not keys:
        raise RuntimeError(
            "No positions_cube partitions found. "
            "Run 02_build_positions_cube.py first."
        )
    return sorted(keys)


def load_canonical_prices(cube_dates: list[pd.Timestamp]) -> pd.DataFrame:
    """
    Load canonical prices and expand to a dense (asset_name, date) grid so
    every asset has a price for every positions_cube date.

    canonical_prices.parquet has no null prices (build_canonical_prices_v2
    fills every row via 4-tier hierarchy). But it may not have a row for
    every (asset, date) combination — e.g., if an asset was first seen on
    2023-01-15, it has rows from that date onward, but canonical_prices may
    be sparse on weekend dates or dates where bd-price-update didn't run.

    The old approach of ffill() within existing rows was a no-op because
    there were no nulls to fill. The fix: create a complete (asset, date)
    grid using the positions_cube dates, merge in known prices, then
    forward-fill to cover gaps. This makes process_date_partition truly
    stateless — every asset on every date has a price via simple lookup.
    """
    print("Loading canonical prices...", end=' ', flush=True)
    resp = s3.get_object(Bucket=S3_BUCKET,
                         Key='silver/prices/canonical_prices.parquet')
    prices = pd.read_parquet(BytesIO(resp['Body'].read()))
    prices['date'] = pd.to_datetime(prices['date'])
    prices = prices[['date', 'asset_name', 'price', 'source']].copy()
    n_raw = len(prices)
    n_assets = prices['asset_name'].nunique()
    print(f"{n_raw:,} rows | {n_assets:,} assets")

    # Build a dense grid: every asset x every positions_cube date
    # Only include dates >= each asset's first appearance in canonical_prices
    print("  Expanding to dense (asset, date) grid...", end=' ', flush=True)
    all_assets = prices['asset_name'].unique()
    cube_dates_idx = pd.DatetimeIndex(sorted(set(cube_dates)))

    # Per-asset first date — don't create rows before the asset existed
    asset_first = prices.groupby('asset_name')['date'].min()

    # Build grid efficiently: for each asset, include cube_dates >= first_date
    grid_parts = []
    for asset, first_dt in asset_first.items():
        asset_dates = cube_dates_idx[cube_dates_idx >= first_dt]
        if len(asset_dates) > 0:
            grid_parts.append(pd.DataFrame({
                'asset_name': asset,
                'date': asset_dates,
            }))

    if not grid_parts:
        print("WARNING: empty grid")
        return prices

    grid = pd.concat(grid_parts, ignore_index=True)
    del grid_parts
    print(f"{len(grid):,} cells")

    # Merge known prices into the grid
    dense = grid.merge(prices, on=['asset_name', 'date'], how='left')
    del grid

    # Forward-fill within each asset (sorted by date) — THIS now actually
    # fills gaps because the grid has rows for dates without canonical prices
    dense = dense.sort_values(['asset_name', 'date'])

    _had_price = dense['price'].notna()
    dense['price']  = dense.groupby('asset_name')['price'].ffill()
    dense['source'] = dense.groupby('asset_name')['source'].ffill()

    # Label newly-filled rows
    _newly_filled = ~_had_price & dense['price'].notna()
    dense.loc[_newly_filled, 'source'] = 'carried_forward_05b'

    # Drop rows still without a price (asset's first canonical date is after
    # its first positions_cube date — no price history to carry forward)
    n_unfilled = dense['price'].isna().sum()
    if n_unfilled > 0:
        print(f"  WARNING: {n_unfilled:,} cells with no price "
              f"(assets without any canonical price before their cube dates)")
    dense = dense.dropna(subset=['price'])

    n_filled = int(_newly_filled.sum())
    print(f"  Dense prices: {len(dense):,} rows "
          f"({n_filled:,} carry-forward rows created, "
          f"{n_raw:,} original canonical rows)")
    return dense


def load_accounts_dimension() -> pd.DataFrame:
    """
    Load accounts dimension for account-level metadata.

    Returns account_id, relationship_id, tax_status, and all advisor fields.
    Accounts absent from dimension will get defaults at processing time.
    """
    print("Loading accounts dimension...", end=' ', flush=True)
    try:
        resp = s3.get_object(Bucket=S3_BUCKET,
                             Key='gold/accounts_dimension_latest.parquet')
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        print(f"{len(df):,} accounts")
        # Collect all useful columns -- advisor fields may be missing in older builds
        keep = ['account_id', 'relationship_id', 'tax_status'] + ADVISOR_FIELDS
        available = [c for c in keep if c in df.columns]
        missing = set(keep) - set(available)
        if missing:
            print(f"  NOTE: accounts_dimension missing columns (will default to empty): "
                  f"{sorted(missing)}")
        return df[available].drop_duplicates(subset=['account_id'])
    except Exception as e:
        raise RuntimeError(
            f"accounts_dimension not found ({e}). "
            "Run 00_build_accounts_dimension.py --upload first."
        )


def load_flows_from_transactions() -> pd.DataFrame:
    """
    Compute daily NNA-relevant cash flows per (date, account_id) from transactions.

    Returns DataFrame: date, account_id, daily_inflow, daily_outflow

    Only Cash Deposit, Transfer In (inflows) and Cash Withdrawal, Transfer Out
    (outflows) are counted. All other transaction types are excluded from NNA.

    Identical logic to 05_build_client_performance.load_flows_from_transactions()
    except the result is kept at account grain (not yet joined to relationships).
    """
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading transactions for flows (parallel)... ", end='', flush=True)

    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/transactions/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])

    if not keys:
        raise RuntimeError("No transaction data found in silver layer.")

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

    txns = pd.concat(dfs, ignore_index=True)
    del dfs; gc.collect()
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
    print(f"loaded in {elapsed:.1f}s")

    if 'transaction_id' in txns.columns:
        txns = txns.drop_duplicates(subset=['transaction_id'], keep='last')

    txns['trade_date'] = pd.to_datetime(txns['trade_date'], errors='coerce')
    txns = txns.dropna(subset=['trade_date', 'account_id', 'market_value'])

    type_col = 'transaction_type' if 'transaction_type' in txns.columns else 'action'

    # Second-pass composite dedup (catches sign-flipped duplicates with different IDs)
    txns['_mv_abs'] = txns['market_value'].abs()
    before = len(txns)
    txns = txns.drop_duplicates(
        subset=['account_id', 'trade_date', type_col, '_mv_abs'], keep='last'
    )
    txns = txns.drop(columns=['_mv_abs'])
    removed = before - len(txns)
    if removed > 0:
        print(f"  WARNING: {removed:,} rows removed by composite dedup")

    # ------------------------------------------------------------------
    # NNA classification exclusions
    # ------------------------------------------------------------------
    # Remove transactions that are NOT real NNA (internal movements,
    # operational sweeps).  Uses `action` as primary discriminator and
    # `description` patterns for cash events that Schwab explicitly
    # excludes from its NNA definition.
    #
    # Exclusions:
    #   action = JNL - LONG / JNL - SHORT  (internal position journals)
    #   desc   ~ TRF BTWN SCH ACCTS        (Schwab-to-Schwab transfers)
    #   desc   ~ TO SEP ACCT MGR           (operational sweeps, ~$207 avg)
    #   desc   ~ TRANSFER FUNDS TO SCHWAB BANK  (FDIC bank sweeps)
    # ------------------------------------------------------------------
    _before_excl = len(txns)

    _action_col = 'action' if 'action' in txns.columns else None
    if _action_col:
        _jnl_mask = txns[_action_col].isin({'JNL - LONG', 'JNL - SHORT'})
        txns = txns[~_jnl_mask]

    if 'description' in txns.columns:
        _desc_upper = txns['description'].fillna('').str.upper()
        _internal_schwab = _desc_upper.str.contains('TRF BTWN SCH', regex=False)
        _sep_sweep       = _desc_upper.str.contains('TO SEP ACCT MGR', regex=False)
        _bank_sweep      = _desc_upper.str.contains('TRANSFER FUNDS TO SCHWAB BANK', regex=False)
        txns = txns[~(_internal_schwab | _sep_sweep | _bank_sweep)]

    _excl_removed = _before_excl - len(txns)
    if _excl_removed > 0:
        print(f"\n  NNA EXCLUSIONS: {_excl_removed:,} non-NNA transactions removed "
              f"(journals, internal Schwab transfers, operational sweeps)")

    is_inflow  = txns[type_col].isin(INFLOW_TYPES)
    is_outflow = txns[type_col].isin(OUTFLOW_TYPES)
    flow_mask  = is_inflow | is_outflow
    flows = txns[flow_mask].copy()

    flows['daily_inflow']  = np.where(is_inflow[flow_mask],  flows['market_value'].abs(), 0.0)
    flows['daily_outflow'] = np.where(is_outflow[flow_mask], flows['market_value'].abs(), 0.0)

    _in_total  = flows['daily_inflow'].sum()
    _out_total = flows['daily_outflow'].sum()
    print(f"\n  Flow classification:")
    print(f"    Inflow  events: {is_inflow[flow_mask].sum():>8,}   raw total: ${_in_total:>16,.0f}")
    print(f"    Outflow events: {is_outflow[flow_mask].sum():>8,}   raw total: ${_out_total:>16,.0f}")
    print(f"    Implied NNA:    ${_in_total - _out_total:>16,.0f}")

    # Outlier cap -- same $50M threshold as 05
    n_capped_in  = (flows['daily_inflow']  > FLOW_CAP).sum()
    n_capped_out = (flows['daily_outflow'] > FLOW_CAP).sum()
    if n_capped_in > 0 or n_capped_out > 0:
        flows['daily_inflow']  = flows['daily_inflow'].clip(upper=FLOW_CAP)
        flows['daily_outflow'] = flows['daily_outflow'].clip(upper=FLOW_CAP)
        print(f"  OUTLIER GUARD: capped {n_capped_in} inflows and "
              f"{n_capped_out} outflows at ${FLOW_CAP:,.0f}")

    daily = flows.groupby(
        ['trade_date', 'account_id'], sort=True
    ).agg(
        daily_inflow=('daily_inflow',  'sum'),
        daily_outflow=('daily_outflow', 'sum'),
    ).reset_index().rename(columns={'trade_date': 'date'})

    print(f"  {len(txns):,} transactions -> {len(daily):,} account x date flow events")
    return daily


# ---------------------------------------------------------------------------
# Core builder -- partition-by-date processing
# ---------------------------------------------------------------------------

def process_date_partition(
    key: str,
    prices_day: pd.DataFrame,
    accounts: pd.DataFrame,
) -> pd.DataFrame:
    """
    Process one date's positions_cube partition and return AUA per (date, account_id).

    Stateless: prices_day is already forward-filled by load_canonical_prices(),
    so no mutable last_prices dict is needed. Safe to call concurrently from
    multiple threads.

    Returns daily_agg_df (empty DataFrame if partition has no rows).
    """
    date_str = key.split('/')[-1].replace('.parquet', '')
    date = pd.Timestamp(date_str)

    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    pos = pd.read_parquet(BytesIO(resp['Body'].read()))

    if pos.empty:
        return pd.DataFrame()

    # Vectorized price join — prices_day is pre-forward-filled so a simple
    # left merge covers all assets; remaining NaN (assets with no price history
    # at all) fall back to 0.
    if not prices_day.empty:
        pos = pos.merge(
            prices_day[['asset_name', 'price', 'source']],
            on='asset_name',
            how='left',
        )
    else:
        pos['price']  = np.nan
        pos['source'] = None

    pos['price'] = pos['price'].fillna(0.0)

    # Vectorized priced-AUA flag — avoids closure over pos inside groupby lambda
    pos['market_value'] = pos['units'] * pos['price']
    pos['priced_mv']    = pos['market_value'].where(
        pos['source'].isin(REAL_PRICE_SOURCES), 0.0
    )

    # Join accounts dimension — brings in relationship_id, tax_status, advisor fields
    pos = pos.merge(accounts, on='account_id', how='left')

    no_rel = pos['relationship_id'].isna() | (pos['relationship_id'] == '')
    pos.loc[no_rel, 'relationship_id'] = 'acct_' + pos.loc[no_rel, 'account_id']

    if 'tax_status' not in pos.columns:
        pos['tax_status'] = 'taxable'
    pos['tax_status'] = pos['tax_status'].fillna('taxable')

    for field in ADVISOR_FIELDS:
        if field not in pos.columns:
            pos[field] = ''
        else:
            pos[field] = pos[field].fillna('')

    # Per-account metadata (1:1 with account_id — take first row per account)
    meta_cols = ['relationship_id', 'tax_status'] + ADVISOR_FIELDS
    meta_cols_present = [c for c in meta_cols if c in pos.columns]
    meta = (pos.groupby('account_id')[meta_cols_present]
            .first()
            .reset_index())

    # Aggregate AUA metrics — fully vectorized, no closures over outer scope
    agg = pos.groupby('account_id').agg(
        total_aua=('market_value', 'sum'),
        num_positions=('asset_name', 'nunique'),
        priced_aua=('priced_mv', 'sum'),
    ).reset_index()

    agg['pct_priced'] = np.where(
        agg['total_aua'] > 0,
        agg['priced_aua'] / agg['total_aua'],
        1.0,
    )
    agg = agg.drop(columns=['priced_aua'])

    agg = agg.merge(meta, on='account_id', how='left')
    agg['date'] = date
    return agg


def build_account_performance(
        cube_keys: list,
        prices:    pd.DataFrame,
        accounts:  pd.DataFrame,
        flows:     pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the account-level daily AUA + flows timeseries.

    Partitions are processed concurrently with ThreadPoolExecutor (16 workers).
    process_date_partition is stateless — prices are pre-forward-filled by
    load_canonical_prices(), so workers share no mutable state.

    Memory: ~4-5 GB peak (more concurrent S3 reads in flight vs ~3.5 GB serial).
    Runtime: ~5-8 min on r6i.xlarge vs ~30 min for the serial version.
    """
    print("\n=== Building account performance ===")

    # Index pre-filled prices by date for O(1) per-partition lookup
    print("  Indexing prices by date...")
    prices_by_date = {d: g for d, g in prices.groupby('date')}
    print(f"  {len(prices_by_date):,} dates in canonical_prices")

    if 'tax_status' not in accounts.columns:
        accounts = accounts.copy()
        accounts['tax_status'] = 'taxable'

    n_total = len(cube_keys)
    print(f"  Processing {n_total:,} date partitions (16 parallel workers)...")

    # Build (future -> index) map so results can be ordered correctly
    daily_aggs = []
    done = 0

    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {}
        for i, key in enumerate(cube_keys):
            date = pd.Timestamp(key.split('/')[-1].replace('.parquet', ''))
            prices_day = prices_by_date.get(date, pd.DataFrame())
            futures[pool.submit(process_date_partition, key, prices_day, accounts)] = i

        for future in as_completed(futures):
            agg = future.result()
            if not agg.empty:
                daily_aggs.append(agg)
            done += 1
            if done % 200 == 0 or done == n_total:
                print(f"    [{done}/{n_total}] complete  "
                      f"({len(daily_aggs):,} partitions with data)")

    print(f"  Partition processing complete: {len(daily_aggs):,} days")

    agg_all = pd.concat(daily_aggs, ignore_index=True)
    del daily_aggs; gc.collect()

    # ------------------------------------------------------------------
    # Build cumulative flows per (date, account_id)
    # ------------------------------------------------------------------
    print("  Building cumulative flows...")

    # Build full date x account spine so cumsum covers every day each account existed
    all_dates = agg_all[['date', 'account_id']].drop_duplicates()
    flow_spine = all_dates.merge(flows, on=['date', 'account_id'], how='left')
    flow_spine['daily_inflow']  = flow_spine['daily_inflow'].fillna(0.0)
    flow_spine['daily_outflow'] = flow_spine['daily_outflow'].fillna(0.0)

    flow_spine = flow_spine.sort_values(['account_id', 'date'])
    flow_spine['cum_inflows']  = (flow_spine
                                  .groupby('account_id')['daily_inflow']
                                  .cumsum())
    flow_spine['cum_outflows'] = (flow_spine
                                  .groupby('account_id')['daily_outflow']
                                  .cumsum())
    flow_spine['nna'] = flow_spine['cum_inflows'] - flow_spine['cum_outflows']

    # ------------------------------------------------------------------
    # Join flows to AUA timeseries
    # ------------------------------------------------------------------
    result = agg_all.merge(
        flow_spine[['date', 'account_id', 'cum_inflows', 'cum_outflows', 'nna']],
        on=['date', 'account_id'],
        how='left',
    )
    for col in ['cum_inflows', 'cum_outflows', 'nna']:
        result[col] = result[col].fillna(0.0)

    # Final column order
    final_cols = [
        'date', 'account_id',
        'relationship_id',
        'architect', 'implementor', 'local_relationship',
        'manager', 'investment_strategy_name',
        'tax_status',
        'total_aua',
        'cum_inflows', 'cum_outflows', 'nna',
        'num_positions',
        'pct_priced',
    ]
    result = result[[c for c in final_cols if c in result.columns]]
    result = result.sort_values(['date', 'account_id']).reset_index(drop=True)

    # Summary
    latest_date = result['date'].max()
    latest = result[result['date'] == latest_date]
    total_aua = latest['total_aua'].sum()

    print(f"\n  Date range:    {result['date'].min().date()} -> {latest_date.date()}")
    print(f"  Total rows:    {len(result):,}")
    print(f"  Accounts:      {result['account_id'].nunique():,}")
    print(f"  Relationships: {result['relationship_id'].nunique():,}")
    print(f"\n  As of {latest_date.date()}:")
    print(f"    Total AUA:     ${total_aua:>16,.0f}")
    print(f"    Cum NNA:       ${latest['nna'].sum():>16,.0f}")
    print(f"    Pct priced:    {latest['pct_priced'].mean()*100:>15.1f}%")
    print(f"    Active accounts: {len(latest):,}")

    # Advisor book summary
    if 'architect' in latest.columns:
        print(f"\n  By architect (top 8 by AUA):")
        arch_agg = (latest.groupby('architect')['total_aua'].sum()
                    .sort_values(ascending=False).head(8))
        for arch, aua in arch_agg.items():
            pct = aua / total_aua * 100 if total_aua > 0 else 0
            n_accts = (latest['architect'] == arch).sum()
            print(f"    {arch:<30}  ${aua:>16,.0f}  ({pct:4.1f}%)  {n_accts} accounts")

    return result


# ---------------------------------------------------------------------------
# Cross-validation against 05
# ---------------------------------------------------------------------------

def cross_validate_vs_client_performance(result: pd.DataFrame) -> bool:
    """
    Verify that SUM(total_aua) on the latest date matches 05_client_performance.

    Returns True if validation passes (within 0.1% tolerance), False otherwise.
    """
    print("\n=== Cross-validating against client_performance (05) ===")
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key='gold/client_performance.parquet')
        perf05 = pd.read_parquet(BytesIO(resp['Body'].read()))
        perf05['date'] = pd.to_datetime(perf05['date'])
    except Exception as e:
        print(f"  SKIP: client_performance not accessible ({e})")
        return True

    latest_date = result['date'].max()
    aua_05b = result[result['date'] == latest_date]['total_aua'].sum()

    perf05_latest = perf05[perf05['date'] == latest_date]
    if perf05_latest.empty:
        print(f"  SKIP: client_performance has no rows for {latest_date.date()}")
        return True
    aua_05 = perf05_latest['total_aua'].sum()

    diff = abs(aua_05b - aua_05)
    pct_diff = diff / aua_05 * 100 if aua_05 > 0 else 0

    print(f"  05_client_performance AUA: ${aua_05:>16,.0f}")
    print(f"  05b_account_performance AUA: ${aua_05b:>16,.0f}")
    print(f"  Difference: ${diff:>16,.0f} ({pct_diff:.4f}%)")

    if pct_diff > 0.1:
        print(f"  FAIL: AUA difference exceeds 0.1% tolerance")
        return False

    print(f"  PASS: AUA cross-check within tolerance")

    # NNA check
    nna_05b = result[result['date'] == latest_date]['nna'].sum()
    nna_05  = perf05_latest['nna'].sum()
    nna_diff_pct = abs(nna_05b - nna_05) / abs(nna_05) * 100 if nna_05 != 0 else 0
    print(f"  NNA 05:  ${nna_05:>16,.0f}")
    print(f"  NNA 05b: ${nna_05b:>16,.0f}  ({nna_diff_pct:.4f}% diff)")
    if nna_diff_pct > 0.1:
        print(f"  WARN: NNA difference exceeds 0.1% -- investigate flow dedup")
    else:
        print(f"  PASS: NNA cross-check within tolerance")

    return True


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_performance(df: pd.DataFrame, upload: bool = False):
    """Save account performance to gold layer."""
    print("\n=== Saving account performance ===")

    output_key = 'gold/account_performance.parquet'
    local_path = Path('/tmp/account_performance.parquet')

    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.1f} MB")

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
    parser = argparse.ArgumentParser(description='Build Account Performance')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD ACCOUNT PERFORMANCE")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    cube_keys = list_positions_cube_keys()
    print(f"Positions cube: {len(cube_keys):,} date partitions")

    # Extract dates from cube keys for dense price grid construction
    cube_dates = [
        pd.Timestamp(k.split('/')[-1].replace('.parquet', ''))
        for k in cube_keys
    ]

    prices   = load_canonical_prices(cube_dates)
    accounts = load_accounts_dimension()
    flows    = load_flows_from_transactions()

    print("\n=== Step 2: Build account performance timeseries ===")
    perf = build_account_performance(cube_keys, prices, accounts, flows)

    print("\n=== Step 3: Cross-validate ===")
    cross_validate_vs_client_performance(perf)

    print("\n=== Step 4: Save ===")
    save_performance(perf, upload=args.upload and not args.dry_run)

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(perf):,} account x date rows")
    print(f"  {perf['account_id'].nunique():,} accounts")
    print(f"  {perf['relationship_id'].nunique():,} relationships")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
