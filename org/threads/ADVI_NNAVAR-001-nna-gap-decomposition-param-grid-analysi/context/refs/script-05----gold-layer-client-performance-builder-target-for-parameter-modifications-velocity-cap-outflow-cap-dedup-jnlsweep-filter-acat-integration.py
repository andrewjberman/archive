#!/usr/bin/env python3
"""
Build Client Performance — Household-Level AUA + Flows Timeseries

Produces a daily household (relationship_id) performance timeseries covering
2020-06-30 to present. This is the AUA and NNA analytics table — it does NOT
include cost_basis or accrued_gain (those are snapshot-in-time tax metrics
that belong to holdings_lots / client_tax_liability).

Data sources and their roles:
  gold/positions_cube/YYYY-MM-DD.parquet   — units per (account, asset) per day
    NOTE: date is the FILENAME, not a column. Each partition has only three
    columns: account_id, asset_name, units. Date is injected from the filename
    at load time. Without this injection, the join on (asset_name, date) fails.

  silver/prices/canonical_prices.parquet  — price per (asset_name, date)
    Joined on (asset_name, date) after date injection. Left join; any remaining
    null prices are forward-filled within each asset_name, then flagged as
    'carried_forward_05'. Positions with no price ever are valued at 0.

  gold/accounts_dimension_latest.parquet  — account → relationship + tax_status
    Provides relationship_id (household grouping) and tax_status for AUA
    breakdown by tax treatment. Accounts absent from dimension default to
    'taxable' and their own account_id as the relationship.

  silver/transactions/  — cash flow events (uniform daily partitions, single source)
    Source for cum_inflows, cum_outflows, nna. Only NNA-relevant transaction
    types are counted (Cash Deposit, Transfer In, Cash Withdrawal, Transfer Out).
    Cumulative flows are computed via daily groupby + cumsum, reindexed to the
    full positions_cube date spine.

Output schema (grain: one row per date × relationship_id):
  date                  date
  relationship_id       str
  total_aua             float  — sum(units × price) across all accounts
  aua_taxable           float  — AUA in taxable (non-qualified) accounts
  aua_tax_deferred      float  — AUA in traditional IRA/401k/SEP accounts
  aua_tax_exempt        float  — AUA in Roth accounts
  cum_inflows           float  — cumulative cash/transfer inflows since inception
  cum_outflows          float  — cumulative cash/transfer outflows since inception
  nna                   float  — cum_inflows − cum_outflows
  num_accounts          int    — distinct accounts with positions on this date
  num_positions         int    — distinct (account, asset) pairs on this date
  pct_priced            float  — fraction of AUA with a direct canonical price

Output: gold/client_performance.parquet

Memory optimization:
  positions_cube has ~172M rows across ~1500 date partitions. Loading all at
  once requires ~30GB+ RAM and OOM-kills on r6i.xlarge (32GB). This script
  processes one date partition at a time (~100K rows), aggregates to
  (date, relationship_id), and discards the partition. Peak memory: ~1GB.

Usage:
    python 05_build_client_performance.py --dry-run
    python 05_build_client_performance.py --upload

Author: Data Scientist (Claude)
Date: 2026-02-20
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


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))

# NNA-relevant transaction types (from FIELD_MAPPINGS.md + confirmed in live data)
INFLOW_TYPES  = frozenset({'Cash Deposit', 'Transfer In'})
OUTFLOW_TYPES = frozenset({'Cash Withdrawal', 'Transfer Out'})

# AUA-based outflow cap: clip daily outflows per relationship at prior-day AUA.
# Neutralises BD data quality issues where market_value on transactions is wildly
# wrong (e.g. 401(k) plan accounts with price = unit count, producing $3.6B phantom
# withdrawals on $2M accounts).  The per-event $50M cap in load_and_classify_flows
# catches the worst single events, but N capped events on the same day can still
# sum to 100x AUA.  This second pass caps the aggregate at the actual portfolio
# value — you cannot withdraw more than what was there.
# Toggle via --no-aua-outflow-cap CLI flag.
AUA_OUTFLOW_CAP_ENABLED = True

# Velocity cap: prevents churn patterns where money flows in, stays briefly,
# and flows out — each daily event passing the AUA cap but the cumulative effect
# producing outsized outflows relative to the relationship's actual size.
#
# Mechanism: over any trailing 90-calendar-day window, a relationship cannot
# register more cumulative outflows than VELOCITY_THRESHOLD * its average AUA
# over that window.  If today's outflow would breach the threshold, it is
# clipped to the remaining "budget" in the window.
#
# Example: relationship with avg AUA of $65M over 90 days and $40M already
# withdrawn in the prior 89 days.  Room = $65M * 1.0 - $40M = $25M.
# A $64.5M outflow on day 90 is capped to $25M.
#
# Toggle via --no-velocity-cap CLI flag.
VELOCITY_CAP_ENABLED = True
VELOCITY_WINDOW_DAYS = 90
VELOCITY_THRESHOLD = 1.0  # 100% of trailing avg AUA

# Price sources that count as "real" for pct_priced
REAL_PRICE_SOURCES = frozenset({
    'transaction_observed', 'yahoo_finance', 'linear_interpolation',
})


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def list_positions_cube_keys() -> list[str]:
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


def load_canonical_prices() -> pd.DataFrame:
    """Load canonical prices for (asset_name, date) → price lookup."""
    print("Loading canonical prices...", end=' ', flush=True)
    resp = s3.get_object(Bucket=S3_BUCKET,
                         Key='silver/prices/canonical_prices.parquet')
    prices = pd.read_parquet(BytesIO(resp['Body'].read()))
    prices['date'] = pd.to_datetime(prices['date'])
    print(f"{len(prices):,} rows | "
          f"{prices['asset_name'].nunique():,} assets")
    return prices[['date', 'asset_name', 'ticker', 'price', 'source']]


def load_accounts_dimension() -> pd.DataFrame:
    """Load accounts dimension for account → relationship_id + tax_status."""
    print("Loading accounts dimension...", end=' ', flush=True)
    try:
        resp = s3.get_object(Bucket=S3_BUCKET,
                             Key='gold/accounts_dimension_latest.parquet')
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        print(f"{len(df):,} accounts")
        cols = ['account_id', 'relationship_id']
        if 'tax_status' in df.columns:
            cols.append('tax_status')
        return df[cols].drop_duplicates(subset=['account_id'])
    except Exception as e:
        raise RuntimeError(
            f"accounts_dimension not found ({e}). "
            "Run 00_build_accounts_dimension.py --upload first."
        )


def load_flows_from_transactions() -> pd.DataFrame:
    """
    Compute daily NNA-relevant cash flows per (date, account_id) from transactions.

    Returns a DataFrame with columns:
      date, account_id, daily_inflow, daily_outflow

    Only Cash Deposit, Transfer In (inflows) and Cash Withdrawal, Transfer Out
    (outflows) are counted. All other transaction types are excluded from NNA.
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

    # Resolve transaction type column name (confirmed 'transaction_type' in silver)
    type_col = 'transaction_type' if 'transaction_type' in txns.columns else 'action'

    # Second-pass dedup: BD exports some events with two different transaction_ids
    # (same economic event, different IDs). The first-pass dedup (transaction_id)
    # removes overlap between bd_transactions and daily partitions for rows with
    # matching IDs. This composite dedup catches the same event stored with different
    # IDs or different market_value signs (e.g., one source stores outflows as
    # negative, another as positive — both pass the first dedup but are the same event).
    # We normalise market_value to its absolute value for dedup purposes only, then
    # use the signed value for the actual flow computation below.
    txns['_mv_abs'] = txns['market_value'].abs()
    _composite_key = ['account_id', 'trade_date', type_col, '_mv_abs']
    _before = len(txns)
    txns = txns.drop_duplicates(subset=_composite_key, keep='last')
    txns = txns.drop(columns=['_mv_abs'])
    _removed = _before - len(txns)
    if _removed > 0:
        print(f"\n  WARNING: {_removed:,} rows removed by composite dedup "
              f"(duplicate transaction_ids or sign-flipped market_value for same event)")

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

    # 1. Action-based: exclude internal journals (position moves between
    #    BD accounts — not real custodial transfers).
    _action_col = 'action' if 'action' in txns.columns else None
    if _action_col:
        _jnl_mask = txns[_action_col].isin({'JNL - LONG', 'JNL - SHORT'})
        txns = txns[~_jnl_mask]

    # 2. Description-based: exclude Schwab internal / operational cash events.
    if 'description' in txns.columns:
        _desc_upper = txns['description'].fillna('').str.upper()

        _internal_schwab = _desc_upper.str.contains('TRF BTWN SCH', regex=False)
        _sep_sweep       = _desc_upper.str.contains('TO SEP ACCT MGR', regex=False)
        _bank_sweep      = _desc_upper.str.contains('TRANSFER FUNDS TO SCHWAB BANK', regex=False)

        _desc_excl = _internal_schwab | _sep_sweep | _bank_sweep
        txns = txns[~_desc_excl]

    _excl_removed = _before_excl - len(txns)
    if _excl_removed > 0:
        print(f"\n  NNA EXCLUSIONS: {_excl_removed:,} non-NNA transactions removed "
              f"(journals, internal Schwab transfers, operational sweeps)")

    # Classify flows — only NNA-relevant types
    is_inflow  = txns[type_col].isin(INFLOW_TYPES)
    is_outflow = txns[type_col].isin(OUTFLOW_TYPES)
    flow_mask  = is_inflow | is_outflow
    flows = txns[flow_mask].copy()

    flows['daily_inflow']  = np.where(is_inflow[flow_mask],  flows['market_value'].abs(), 0.0)
    flows['daily_outflow'] = np.where(is_outflow[flow_mask], flows['market_value'].abs(), 0.0)

    # Diagnostic: verify flow classification looks reasonable before aggregating.
    # A healthy firm should have cum_inflows and cum_outflows in the same order of
    # magnitude. If either exceeds ~10x AUA, something is likely miscounted.
    _in_total  = flows['daily_inflow'].sum()
    _out_total = flows['daily_outflow'].sum()
    _n_in  = is_inflow[flow_mask].sum()
    _n_out = is_outflow[flow_mask].sum()
    print(f"\n  Flow classification:")
    print(f"    Inflow  events: {_n_in:>8,}   raw total: ${_in_total:>16,.0f}")
    print(f"    Outflow events: {_n_out:>8,}   raw total: ${_out_total:>16,.0f}")
    print(f"    Implied NNA:    ${_in_total - _out_total:>16,.0f}")
    print(f"  Top 5 largest single inflow  events:")
    for _, r in (flows[flows['daily_inflow'] > 0]
                 .nlargest(5, 'daily_inflow')
                 [['account_id', 'trade_date', type_col, 'market_value', 'daily_inflow']]
                 .iterrows()):
        print(f"    {r['account_id']}  {r['trade_date'].date()}  {r[type_col]}  "
              f"mv={r['market_value']:,.0f}  inflow={r['daily_inflow']:,.0f}")
    print(f"  Top 5 largest single outflow events:")
    for _, r in (flows[flows['daily_outflow'] > 0]
                 .nlargest(5, 'daily_outflow')
                 [['account_id', 'trade_date', type_col, 'market_value', 'daily_outflow']]
                 .iterrows()):
        print(f"    {r['account_id']}  {r['trade_date'].date()}  {r[type_col]}  "
              f"mv={r['market_value']:,.0f}  outflow={r['daily_outflow']:,.0f}")

    # Outlier guard: cap per-event flows at $50M to neutralise garbage data
    # (e.g. z0818656451/z0818656501 with $3.6B phantom withdrawals on 2024-08-07)
    FLOW_CAP = 50_000_000
    n_capped_in  = (flows['daily_inflow']  > FLOW_CAP).sum()
    n_capped_out = (flows['daily_outflow'] > FLOW_CAP).sum()
    if n_capped_in > 0 or n_capped_out > 0:
        flows['daily_inflow']  = flows['daily_inflow'].clip(upper=FLOW_CAP)
        flows['daily_outflow'] = flows['daily_outflow'].clip(upper=FLOW_CAP)
        print(f"\n  OUTLIER GUARD: capped {n_capped_in} inflows and "
              f"{n_capped_out} outflows at ${FLOW_CAP:,.0f}")

    daily = flows.groupby(
        ['trade_date', 'account_id'], sort=True
    ).agg(
        daily_inflow=('daily_inflow',  'sum'),
        daily_outflow=('daily_outflow', 'sum'),
    ).reset_index().rename(columns={'trade_date': 'date'})

    print(f"\n  {len(txns):,} transactions → {len(daily):,} account×date flow events")
    return daily


# ---------------------------------------------------------------------------
# Core builder — partition-by-date processing
# ---------------------------------------------------------------------------

def process_date_partition(
    key: str,
    prices_day: pd.DataFrame,
    accounts: pd.DataFrame,
    last_prices: dict,
) -> tuple[pd.DataFrame, dict]:
    """
    Process one date's positions_cube partition and return aggregated AUA
    per (date, relationship_id).

    last_prices: dict of {asset_name: (price, source)} for forward-fill of
    assets not in canonical_prices on this date. Updated in-place.

    Returns (daily_agg, last_prices).
    """
    # Extract date from key
    date_str = key.split('/')[-1].replace('.parquet', '')
    date = pd.Timestamp(date_str)

    # Load partition (~100K rows: account_id, asset_name, units)
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    pos = pd.read_parquet(BytesIO(resp['Body'].read()))

    if pos.empty:
        return pd.DataFrame(), last_prices

    # Merge with prices for this date
    if not prices_day.empty:
        pos = pos.merge(
            prices_day[['asset_name', 'price', 'source']],
            on='asset_name',
            how='left',
        )
        # Update last_prices with today's known prices
        known = prices_day[prices_day['price'].notna()]
        for _, row in known.iterrows():
            last_prices[row['asset_name']] = (row['price'], row['source'])
    else:
        pos['price'] = np.nan
        pos['source'] = None

    # Forward-fill from last_prices for assets missing today
    missing = pos['price'].isna()
    if missing.any():
        for idx in pos.index[missing]:
            asset = pos.at[idx, 'asset_name']
            if asset in last_prices:
                p, src = last_prices[asset]
                pos.at[idx, 'price'] = p
                pos.at[idx, 'source'] = 'carried_forward_05'

    # Remaining nulls → 0
    pos['price'] = pos['price'].fillna(0.0)

    # Market value
    pos['market_value'] = pos['units'] * pos['price']
    pos['is_priced'] = pos['source'].isin(REAL_PRICE_SOURCES)

    # Join accounts dimension
    pos = pos.merge(
        accounts,
        on='account_id',
        how='left',
    )
    no_rel = pos['relationship_id'].isna() | (pos['relationship_id'] == '')
    pos.loc[no_rel, 'relationship_id'] = 'acct_' + pos.loc[no_rel, 'account_id']
    if 'tax_status' not in pos.columns:
        pos['tax_status'] = 'taxable'
    pos['tax_status'] = pos['tax_status'].fillna('taxable')

    # Aggregate to relationship level
    agg = pos.groupby('relationship_id').agg(
        total_aua=('market_value', 'sum'),
        num_accounts=('account_id', 'nunique'),
        num_positions=('asset_name', 'nunique'),
        priced_aua=('market_value', lambda x: x[pos.loc[x.index, 'is_priced']].sum()),
    ).reset_index()

    agg['pct_priced'] = np.where(
        agg['total_aua'] > 0,
        agg['priced_aua'] / agg['total_aua'],
        1.0,
    )
    agg = agg.drop(columns=['priced_aua'])

    # AUA breakdown by tax_status
    for ts in ['taxable', 'tax_deferred', 'tax_exempt']:
        sub = (pos[pos['tax_status'] == ts]
               .groupby('relationship_id')['market_value']
               .sum()
               .reset_index()
               .rename(columns={'market_value': f'aua_{ts}'}))
        agg = agg.merge(sub, on='relationship_id', how='left')
        agg[f'aua_{ts}'] = agg[f'aua_{ts}'].fillna(0.0)

    agg['date'] = date
    return agg, last_prices


def build_client_performance(
        cube_keys: list[str],
        prices:    pd.DataFrame,
        accounts:  pd.DataFrame,
        flows:     pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the household daily AUA + flows timeseries.

    Processes positions_cube one date partition at a time to stay within
    memory limits (~1GB peak instead of ~30GB for all 172M rows).
    """
    print("\n=== Building client performance ===")

    # Pre-index prices by date for O(1) lookup
    print("  Indexing prices by date...")
    prices_by_date = {d: g for d, g in prices.groupby('date')}
    print(f"  {len(prices_by_date):,} dates in canonical_prices")

    # Ensure accounts has tax_status
    if 'tax_status' not in accounts.columns:
        accounts['tax_status'] = 'taxable'

    # Process each date partition
    print(f"  Processing {len(cube_keys):,} date partitions...")
    daily_aggs = []
    last_prices = {}  # Forward-fill state: {asset_name: (price, source)}
    total_positions = 0

    for i, key in enumerate(cube_keys):
        date_str = key.split('/')[-1].replace('.parquet', '')
        date = pd.Timestamp(date_str)
        prices_day = prices_by_date.get(date, pd.DataFrame())

        agg, last_prices = process_date_partition(key, prices_day, accounts, last_prices)
        if not agg.empty:
            daily_aggs.append(agg)
            total_positions += agg['num_positions'].sum()

        if (i + 1) % 100 == 0 or (i + 1) == len(cube_keys):
            print(f"    [{i+1}/{len(cube_keys)}] {date_str}  "
                  f"({len(daily_aggs):,} days aggregated)")

    print(f"  Partition processing complete: {len(daily_aggs):,} days")

    # Concat all daily aggregations
    agg_all = pd.concat(daily_aggs, ignore_index=True)

    # ------------------------------------------------------------------
    # Build cumulative flows per (date, relationship_id)
    # ------------------------------------------------------------------
    print("  Building cumulative flows...")

    # Join flows with accounts to get relationship_id
    flows_rel = flows.merge(
        accounts[['account_id', 'relationship_id']],
        on='account_id',
        how='left',
    )
    no_rel_f = flows_rel['relationship_id'].isna() | (flows_rel['relationship_id'] == '')
    flows_rel.loc[no_rel_f, 'relationship_id'] = 'acct_' + flows_rel.loc[no_rel_f, 'account_id']

    # Daily flows at relationship level
    daily_rel = flows_rel.groupby(
        ['date', 'relationship_id'], sort=True
    ).agg(
        daily_inflow=('daily_inflow', 'sum'),
        daily_outflow=('daily_outflow', 'sum'),
    ).reset_index()

    # Build full date × relationship spine so cumsum covers every day
    all_dates = agg_all[['date', 'relationship_id']].drop_duplicates()
    flow_spine = all_dates.merge(daily_rel, on=['date', 'relationship_id'], how='left')
    flow_spine['daily_inflow']  = flow_spine['daily_inflow'].fillna(0.0)
    flow_spine['daily_outflow'] = flow_spine['daily_outflow'].fillna(0.0)

    flow_spine = flow_spine.sort_values(['relationship_id', 'date'])

    # ------------------------------------------------------------------
    # AUA-based outflow cap (toggleable via AUA_OUTFLOW_CAP_ENABLED)
    # ------------------------------------------------------------------
    # Cap each relationship's daily outflow at its prior-day AUA.
    # You cannot withdraw more than the portfolio was worth yesterday.
    if AUA_OUTFLOW_CAP_ENABLED:
        print("  Applying AUA-based outflow cap...")
        flow_spine = flow_spine.merge(
            agg_all[['date', 'relationship_id', 'total_aua']],
            on=['date', 'relationship_id'],
            how='left',
        )
        flow_spine['prior_day_aua'] = (
            flow_spine
            .groupby('relationship_id')['total_aua']
            .shift(1)
            .fillna(0.0)
        )

        overcapped = flow_spine['daily_outflow'] > flow_spine['prior_day_aua']
        n_overcapped = overcapped.sum()
        if n_overcapped > 0:
            original_total = flow_spine.loc[overcapped, 'daily_outflow'].sum()
            flow_spine.loc[overcapped, 'daily_outflow'] = (
                flow_spine.loc[overcapped, 'prior_day_aua'].clip(lower=0)
            )
            capped_total = flow_spine.loc[overcapped, 'daily_outflow'].sum()
            print(f"    AUA-BASED OUTFLOW CAP: {n_overcapped:,} relationship-days capped")
            print(f"      Original total: ${original_total:>16,.0f}")
            print(f"      Capped total:   ${capped_total:>16,.0f}")
            print(f"      Eliminated:     ${original_total - capped_total:>16,.0f}")
        else:
            print("    AUA-based outflow cap: no adjustments needed")

        flow_spine = flow_spine.drop(columns=['prior_day_aua'])
        # Keep total_aua for velocity cap below
    else:
        print("  AUA-based outflow cap: SKIPPED (disabled)")
        # Still need total_aua for velocity cap
        flow_spine = flow_spine.merge(
            agg_all[['date', 'relationship_id', 'total_aua']],
            on=['date', 'relationship_id'],
            how='left',
        )

    # ------------------------------------------------------------------
    # Velocity cap: trailing 90-day outflow budget
    # ------------------------------------------------------------------
    # Prevents churn patterns where each daily event passes the AUA cap
    # but cumulative outflows over a quarter vastly exceed the relationship's
    # actual size.  See constants above for rationale.
    if VELOCITY_CAP_ENABLED:
        print("  Applying velocity cap (trailing 90-day outflow budget)...")
        flow_spine = flow_spine.sort_values(['relationship_id', 'date'])

        window_str = f'{VELOCITY_WINDOW_DAYS}D'

        # Compute trailing rolling outflow and avg AUA per relationship.
        # rolling() on a DatetimeIndex gives true calendar-day windows.
        orig_index = flow_spine.index.copy()
        flow_spine = flow_spine.set_index('date')

        trailing_out_incl = (
            flow_spine.groupby('relationship_id')['daily_outflow']
            .transform(lambda s: s.rolling(window_str, min_periods=1).sum())
        )
        trailing_avg_aua = (
            flow_spine.groupby('relationship_id')['total_aua']
            .transform(lambda s: s.rolling(window_str, min_periods=1).mean())
        )

        flow_spine = flow_spine.reset_index()

        # trailing_out_incl includes today's outflow.  Subtract it to get
        # what was already consumed in the prior (W-1) days.
        trailing_out_excl = trailing_out_incl.values - flow_spine['daily_outflow'].values

        # Budget: how much room is left in the trailing window
        allowed = trailing_avg_aua.values * VELOCITY_THRESHOLD
        room = (allowed - trailing_out_excl).clip(min=0)

        velocity_capped = flow_spine['daily_outflow'].values > room
        n_velocity_capped = velocity_capped.sum()

        if n_velocity_capped > 0:
            original_total = flow_spine.loc[velocity_capped, 'daily_outflow'].sum()
            flow_spine.loc[velocity_capped, 'daily_outflow'] = room[velocity_capped]
            capped_total = flow_spine.loc[velocity_capped, 'daily_outflow'].sum()

            # Show top relationships affected
            flow_spine['_vel_savings'] = 0.0
            flow_spine.loc[velocity_capped, '_vel_savings'] = (
                original_total - capped_total
            ) if n_velocity_capped == 1 else None
            # Recompute savings per row for reporting
            _orig = flow_spine['daily_outflow'].copy()
            _orig.loc[velocity_capped] = original_total / max(n_velocity_capped, 1)

            print(f"    VELOCITY CAP: {n_velocity_capped:,} relationship-days capped")
            print(f"      Original total: ${original_total:>16,.0f}")
            print(f"      Capped total:   ${capped_total:>16,.0f}")
            print(f"      Eliminated:     ${original_total - capped_total:>16,.0f}")
            print(f"      Window: {VELOCITY_WINDOW_DAYS} days, threshold: {VELOCITY_THRESHOLD:.0%}")

            if '_vel_savings' in flow_spine.columns:
                flow_spine = flow_spine.drop(columns=['_vel_savings'])
        else:
            print("    Velocity cap: no adjustments needed")
    else:
        print("  Velocity cap: SKIPPED (disabled)")

    # Drop AUA column used by caps (no longer needed)
    if 'total_aua' in flow_spine.columns:
        flow_spine = flow_spine.drop(columns=['total_aua'])

    flow_spine['cum_inflows']  = (flow_spine
                                  .groupby('relationship_id')['daily_inflow']
                                  .cumsum())
    flow_spine['cum_outflows'] = (flow_spine
                                  .groupby('relationship_id')['daily_outflow']
                                  .cumsum())
    flow_spine['nna'] = flow_spine['cum_inflows'] - flow_spine['cum_outflows']

    # ------------------------------------------------------------------
    # Join flows to AUA timeseries
    # ------------------------------------------------------------------
    result = agg_all.merge(
        flow_spine[['date', 'relationship_id', 'cum_inflows', 'cum_outflows', 'nna']],
        on=['date', 'relationship_id'],
        how='left',
    )
    for col in ['cum_inflows', 'cum_outflows', 'nna']:
        result[col] = result[col].fillna(0.0)

    # Final column order
    final_cols = [
        'date', 'relationship_id',
        'total_aua',
        'aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
        'cum_inflows', 'cum_outflows', 'nna',
        'num_accounts', 'num_positions',
        'pct_priced',
    ]
    result = result[[c for c in final_cols if c in result.columns]]
    result = result.sort_values(['date', 'relationship_id']).reset_index(drop=True)

    # Summary
    latest_date = result['date'].max()
    latest = result[result['date'] == latest_date]
    print(f"\n  Date range:   {result['date'].min().date()} → {latest_date.date()}")
    print(f"  Households:   {result['relationship_id'].nunique():,}")
    print(f"  Total rows:   {len(result):,}")
    print(f"\n  As of {latest_date.date()}:")
    print(f"    Total AUA:      ${latest['total_aua'].sum():>16,.0f}")
    print(f"      Taxable:      ${latest['aua_taxable'].sum():>16,.0f}")
    print(f"      Tax-deferred: ${latest['aua_tax_deferred'].sum():>16,.0f}")
    print(f"      Tax-exempt:   ${latest['aua_tax_exempt'].sum():>16,.0f}")
    print(f"    Cum NNA:        ${latest['nna'].sum():>16,.0f}")
    print(f"    Pct priced:     {latest['pct_priced'].mean()*100:>15.1f}%")

    return result


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_performance(df: pd.DataFrame, upload: bool = False):
    """Save client performance to gold layer."""
    print("\n=== Saving client performance ===")

    output_key = 'gold/client_performance.parquet'
    local_path = Path('/tmp/client_performance.parquet')

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
    parser = argparse.ArgumentParser(description='Build Client Performance')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    parser.add_argument('--no-aua-outflow-cap', action='store_true',
                        help='Disable AUA-based outflow cap (fall back to $50M per-event cap only)')
    parser.add_argument('--no-velocity-cap', action='store_true',
                        help='Disable trailing 90-day velocity cap')
    args = parser.parse_args()

    global AUA_OUTFLOW_CAP_ENABLED, VELOCITY_CAP_ENABLED
    if args.no_aua_outflow_cap:
        AUA_OUTFLOW_CAP_ENABLED = False
        print("  AUA-based outflow cap: DISABLED (--no-aua-outflow-cap)")
    else:
        print("  AUA-based outflow cap: ENABLED (default)")
    if args.no_velocity_cap:
        VELOCITY_CAP_ENABLED = False
        print("  Velocity cap: DISABLED (--no-velocity-cap)")
    else:
        print(f"  Velocity cap: ENABLED (window={VELOCITY_WINDOW_DAYS}d, threshold={VELOCITY_THRESHOLD:.0%})")

    print("=" * 70)
    print("BUILD CLIENT PERFORMANCE")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    cube_keys = list_positions_cube_keys()
    print(f"Positions cube: {len(cube_keys):,} date partitions")

    prices   = load_canonical_prices()
    accounts = load_accounts_dimension()
    flows    = load_flows_from_transactions()

    print("\n=== Step 2: Build performance timeseries ===")
    perf = build_client_performance(cube_keys, prices, accounts, flows)

    print("\n=== Step 3: Save ===")
    save_performance(perf, upload=args.upload and not args.dry_run)

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(perf):,} household×date rows")
    print(f"  {perf['relationship_id'].nunique():,} households")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
