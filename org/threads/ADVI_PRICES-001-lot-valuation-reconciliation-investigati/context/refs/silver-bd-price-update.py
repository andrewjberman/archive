#!/usr/bin/env python3
"""
bd-price-update Lambda — Incremental Canonical Prices Maintainer v5

Runs daily in pipeline chain (after BD transaction silver layer is updated).

TWO JOBS:

  JOB 1: Incremental canonical_prices update
    a. Load silver/prices/canonical_prices.parquet  (current full table)
    b. Load silver/historical_prices.parquet        (T2 source, written at 9 AM by EC2 scheduler)
    c. Load today's transaction file from silver/transactions/
    d. Extract T1 prices from today's transactions  (observed: |market_value|/|units|)
    e. Read T2 closes from historical_prices.parquet (7-day window lookup, no live API call)
    f. Build one row per existing asset for target_date (T1 -> T2 -> carry_forward)
    g. Detect new assets: in today's transactions but not yet in canonical
    h. Backfill new assets: full T1 from all transactions + T2 from historical_prices.parquet
    i. Upsert all new rows into canonical, deduplicate on (date, asset_name)
    j. Save canonical_prices.parquet back to S3

  JOB 2: Update interpolated_prices.parquet
    Extracts transaction-observed prices for last 30 days, appends to running table.
    This remains the T1 source for build_canonical_prices_v2.py emergency full rebuilds.

Dependency chain (daily):
  9:00 AM ET  — historical-prices-scheduler EC2 writes historical_prices.parquet (T2 source)
  4:51 PM ET  — bd-price-update runs, reads historical_prices.parquet for T2 prices

NOTE on yfinance: Does NOT call yfinance directly. T2 prices are provided by
historical_prices.parquet (written by the EC2 scheduler at 9 AM).

EC2 execution: python3 scripts/silver/bd_price_update.py [--date YYYY-MM-DD]
Migrated from Lambda (bd-price-update) due to Runtime.OutOfMemory at 10240 MB ceiling.
"""

import json
import logging
from datetime import datetime, timedelta
from io import BytesIO

import boto3
import numpy as np
import pandas as pd
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

s3 = boto3.client('s3')
S3_BUCKET = 'opal-data-bd'

# Sanity ceiling for transaction-derived prices
MAX_UNIT_PRICE = 100_000

# Source quality rank (lower = higher priority when deduplicating)
SOURCE_RANK = {
    'scoped_override':      -1,
    'transaction_observed':  0,
    'yahoo_finance':         1,
    'linear_interpolation':  2,
    'carry_forward':         3,
}

# ---------------------------------------------------------------------------
# Scoped price overrides — structured notes, model sleeves, and private funds
#
# These assets resolve to the wrong public ticker in Yahoo Finance.  The
# override price is derived from reverse-engineering silver allocations
# (BD's own account_market_value) against correctly-priced positions.
#
# This is the SINGLE SOURCE OF TRUTH.  inject_scoped_overrides.py reads
# from this list.  bd_price_update enforces overrides inline during
# build_target_date_rows so that Yahoo/carry-forward can never win.
#
# See DS session log 2026-03-17 for derivation methodology.
# ---------------------------------------------------------------------------
_SCOPED_PRICE_OVERRIDES: list[dict] = [
    {
        "asset_name": "Waldrop Donor Advised Fund",
        "ticker": "WALDROP_DAF",
        "price": 1.95,
    },
    {
        "asset_name": "BNP PARIBAS SA",
        "ticker": "BNP_STRUCT_DEP",
        "price": 0.75,
    },
    {
        "asset_name": "DESTINATIONS LARGE CAP EQUITY I",
        "ticker": "DEST_LCAP_I",
        "price": 13.30,
    },
    {
        "asset_name": "DESTINATIONS INTERNATIONAL EQUITY I",
        "ticker": "DEST_INTL_I",
        "price": 13.30,
    },
    {
        "asset_name": "JPMORGAN CHASE FINL CO LLC 0% 02/14/2029",
        "ticker": "JPM_STRUCT_0029",
        "price": 2.55,
    },
]

# Quick lookup: {asset_name: (price, ticker)}
_SCOPED_OVERRIDE_MAP: dict[str, tuple[float, str]] = {
    o["asset_name"]: (o["price"], o["ticker"]) for o in _SCOPED_PRICE_OVERRIDES
}

# ---------------------------------------------------------------------------
# Proprietary ETF ticker overrides
#
# Black Diamond stores Opal-branded and Pathfinder ETFs under their full fund
# names with no ticker field. config/ticker_lookup.json does not contain these
# entries because BD never emits a ticker for them in transaction data.
#
# These are merged into ticker_map in load_ticker_lookup() so that:
#   1. The `ticker` column in daily canonical price rows is correct.
#   2. Yahoo Finance T2 prices can be fetched for these assets.
#   3. New-asset backfill for these ETFs assigns the correct ticker.
#
# Keep this dict in sync with _OPAL_ETF_OVERRIDES in build_canonical_prices_v2.py.
# Use EXACT uppercase form as written in BD asset_name field.
# ---------------------------------------------------------------------------
_OPAL_ETF_OVERRIDES: dict = {
    'OPAL DIVIDEND INCOME ETF':                           'DIVZ',
    'POLEN DIVIDEND INCOME ETF':                          'DIVZ',  # filing/legacy name
    'OPAL INTERNATIONAL DIVIDEND INCOME ETF':             'IDVZ',
    'PATHFINDER DISCIPLINED US EQUITY ETF':               'PFDE',
    'PATHFINDER DISCIPLINED US EQUITIES ETF':             'PFDE',  # BD spelling variant
    'PATHFINDER FOCUSED OPPORTUNITIES ETF':               'PFOE',
    'POLEN HIGH INCOME ETF':                              'PCHI',
}


# ============================================================================
# SHARED LOADERS
# ============================================================================

def _load_parquet_bytes(key: str) -> pd.DataFrame:
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


def load_transactions_for_new_assets(new_assets: set) -> pd.DataFrame:
    """
    Load only the transaction files needed to backfill new assets.

    Scans backward from the most recent file, accumulating DataFrames until all
    new assets have been seen at least once, then continues for BOUNDARY_MARGIN
    more files to capture their full earliest history. Returns the combined
    result covering from the left boundary to today.

    Replaces load_all_transactions() for the new-asset backfill path.
    Memory: O(months since first appearance) instead of O(full history).
    """
    paginator = s3.get_paginator('list_objects_v2')
    all_keys = sorted(
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/transactions/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
        and not obj['Key'].split('/')[-1].startswith('backfill')
    )

    not_yet_found = set(new_assets)
    accumulated = []
    all_found = False
    files_after_all_found = 0
    BOUNDARY_MARGIN = 21  # ~1 month of business days past finding all assets

    logger.info(f"  Scanning backward for {len(new_assets)} new asset(s) "
                f"(total files available: {len(all_keys)})")

    for key in reversed(all_keys):
        try:
            df = _load_parquet_bytes(key)
            df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce')
        except Exception:
            continue

        accumulated.append(df)

        if not_yet_found and 'asset_name' in df.columns:
            not_yet_found -= set(df['asset_name'].dropna()) & not_yet_found

        if not not_yet_found and not all_found:
            all_found = True
            logger.info(f"  All new assets located. Loading {BOUNDARY_MARGIN} "
                        f"more files to capture full history...")

        if all_found:
            files_after_all_found += 1
            if files_after_all_found >= BOUNDARY_MARGIN:
                break

    if not accumulated:
        return pd.DataFrame()

    logger.info(f"  Loaded {len(accumulated)} transaction files "
                f"(vs {len(all_keys)} total)")

    combined = pd.concat(accumulated, ignore_index=True)
    if 'transaction_id' in combined.columns:
        combined = combined.drop_duplicates(subset=['transaction_id'], keep='last')
    return combined


def load_transactions_for_date(target_date: pd.Timestamp) -> pd.DataFrame:
    """Load the silver/transactions/ partition for a single date. Returns empty DF if absent."""
    key = f'silver/transactions/{target_date.strftime("%Y-%m-%d")}.parquet'
    try:
        df = _load_parquet_bytes(key)
        df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce')
        return df
    except Exception:
        return pd.DataFrame()


def load_ticker_lookup() -> dict:
    """Return {asset_name: ticker} for all assets with a real ticker.

    Merges _OPAL_ETF_OVERRIDES after loading so that Opal/Pathfinder branded
    ETFs always resolve to their correct tickers regardless of ticker_lookup.json.
    """
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key='config/ticker_lookup.json')
        records = json.loads(resp['Body'].read())
        mapping = {
            r['asset_name']: r['ticker']
            for r in records
            if r.get('asset_name') and r.get('ticker')
            and r['ticker'] not in ('UNKNOWN', '', None)
        }
    except Exception as e:
        logger.warning(f"Could not load ticker_lookup.json: {e}")
        mapping = {}
    mapping.update(_OPAL_ETF_OVERRIDES)
    return mapping


# ============================================================================
# JOB 1: INCREMENTAL CANONICAL PRICES
# ============================================================================

def load_canonical_prices() -> pd.DataFrame:
    logger.info("Loading canonical_prices.parquet...")
    try:
        df = _load_parquet_bytes('silver/prices/canonical_prices.parquet')
        df['date'] = pd.to_datetime(df['date'])
        logger.info(f"  OK: {len(df):,} rows | {df['asset_name'].nunique():,} assets | "
                    f"max date: {df['date'].max().date()}")
        return df
    except Exception as e:
        logger.warning(f"  Not found ({e}) — Job 1 will be skipped (run build_canonical_prices_v2.py to bootstrap)")
        return pd.DataFrame(columns=['date', 'asset_name', 'ticker', 'price', 'source'])


def extract_t1_prices(txns: pd.DataFrame) -> dict:
    """
    Derive transaction-observed prices from a set of transactions.
    price = |market_value| / |units|, median per asset_name across all rows.
    Returns {asset_name: price}.
    """
    if txns.empty:
        return {}
    valid = txns[
        txns['asset_name'].notna() &
        txns['units'].notna() & (txns['units'].abs() > 1e-8) &
        txns['market_value'].notna() & (txns['market_value'] != 0)
    ].copy()
    valid['calc_price'] = valid['market_value'].abs() / valid['units'].abs()
    valid = valid[(valid['calc_price'] > 0) & (valid['calc_price'] < MAX_UNIT_PRICE)]
    if valid.empty:
        return {}
    return valid.groupby('asset_name')['calc_price'].median().to_dict()


def load_historical_prices() -> pd.DataFrame:
    """
    Load silver/historical_prices.parquet — written daily at 9 AM by the
    historical-prices-scheduler EC2.  Contains all tickered assets since 2020.
    Returns DataFrame: (date, ticker, close, ...).
    """
    try:
        df = _load_parquet_bytes('silver/historical_prices.parquet')
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        logger.info(f"  OK: historical_prices loaded: {len(df):,} rows, "
                    f"{df['ticker'].nunique():,} tickers, "
                    f"max date: {df['date'].max().date()}")
        return df
    except Exception as e:
        logger.warning(f"  Could not load historical_prices.parquet: {e}")
        return pd.DataFrame(columns=['date', 'ticker', 'close'])


def fetch_yahoo_closes_for_date(tickers: list, target_date: pd.Timestamp,
                                 hist_prices: pd.DataFrame) -> dict:
    """
    Return {ticker: price} for each ticker on or before target_date.
    Reads from the pre-built historical_prices.parquet (written at 9 AM by EC2).
    Falls back to the most recent available row per ticker within a 7-day window.
    No live Yahoo API call — avoids the yfinance layer size constraint.
    """
    if not tickers or hist_prices.empty:
        return {}
    window_start = target_date - timedelta(days=7)
    recent = hist_prices[
        (hist_prices['ticker'].isin(tickers)) &
        (hist_prices['date'] >= window_start) &
        (hist_prices['date'] <= target_date)
    ]
    if recent.empty:
        return {}
    # Last available close per ticker on or before target_date
    results = (
        recent.sort_values('date')
        .groupby('ticker')['close']
        .last()
        .to_dict()
    )
    results = {t: float(p) for t, p in results.items() if pd.notna(p) and p > 0}
    logger.info(f"  OK: Yahoo closes (from historical_prices.parquet): "
                f"{len(results):,}/{len(tickers):,} tickers priced")
    return results


def fetch_yahoo_history(tickers: list, start_date: str,
                         hist_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Return daily close history for a list of tickers since start_date.
    Reads from historical_prices.parquet — no live API call.
    Used for new-asset backfill (T2 layer).
    """
    if not tickers or hist_prices.empty:
        return pd.DataFrame(columns=['date', 'ticker', 'close'])
    start_ts = pd.Timestamp(start_date)
    df = hist_prices[
        hist_prices['ticker'].isin(tickers) &
        (hist_prices['date'] >= start_ts)
    ][['date', 'ticker', 'close']].copy()
    df = df[df['close'] > 0]
    logger.info(f"  OK: Yahoo history (from historical_prices.parquet): "
                f"{len(df):,} rows for {df['ticker'].nunique() if len(df) else 0} tickers")
    return df


def build_target_date_rows(
    canonical: pd.DataFrame,
    t1_prices: dict,
    yahoo_closes: dict,
    ticker_map: dict,
    target_date: pd.Timestamp,
) -> pd.DataFrame:
    """
    Build one canonical row per existing asset for target_date.
    Scoped overrides -> T1 (transaction_observed) -> T2 (yahoo_finance) -> T3 (carry_forward).
    Assets with no price at all are skipped (extreme edge case).
    """
    if canonical.empty:
        return pd.DataFrame(columns=['date', 'asset_name', 'ticker', 'price', 'source'])

    # Last known price + ticker per asset for carry_forward
    last_known = (
        canonical.sort_values('date')
        .groupby('asset_name', sort=False)
        .last()[['price', 'ticker']]
    )

    n_overrides = 0
    rows = []
    for asset_name, last_row in last_known.iterrows():
        # Scoped overrides always win — structured notes, model sleeves, private funds
        if asset_name in _SCOPED_OVERRIDE_MAP:
            override_price, override_ticker = _SCOPED_OVERRIDE_MAP[asset_name]
            rows.append({'date': target_date, 'asset_name': asset_name,
                         'ticker': override_ticker, 'price': override_price,
                         'source': 'scoped_override'})
            n_overrides += 1
            continue

        ticker = ticker_map.get(asset_name) or (
            last_row['ticker'] if pd.notna(last_row.get('ticker')) else None
        )
        if asset_name in t1_prices:
            price, source = t1_prices[asset_name], 'transaction_observed'
        elif ticker and ticker in yahoo_closes:
            price, source = yahoo_closes[ticker], 'yahoo_finance'
        elif pd.notna(last_row['price']) and last_row['price'] > 0:
            price, source = float(last_row['price']), 'carry_forward'
        else:
            continue
        rows.append({'date': target_date, 'asset_name': asset_name,
                     'ticker': ticker, 'price': price, 'source': source})

    if n_overrides:
        logger.info(f"  Scoped overrides applied: {n_overrides} assets")

    df = pd.DataFrame(rows)
    if not df.empty:
        logger.info(
            f"  Rows for {target_date.date()}: {len(df):,}  "
            f"(override={(df['source']=='scoped_override').sum()}, "
            f"T1={(df['source']=='transaction_observed').sum()}, "
            f"T2={(df['source']=='yahoo_finance').sum()}, "
            f"ffill={(df['source']=='carry_forward').sum()})"
        )
    return df


def backfill_new_assets(
    new_assets: set,
    all_txns: pd.DataFrame,
    ticker_map: dict,
    hist_prices: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build full canonical price history for newly discovered assets.

    For each new asset, applies the same 4-tier hierarchy as build_canonical_prices_v2.py:
      T1: transaction-observed prices from full history (per-day median |mv|/|units|)
      T2: Yahoo Finance daily closes from first transaction date to today
      T3a: linear interpolation between bracketed known dates
      T3b: carry_forward for trailing gaps after last known price
    """
    if not new_assets or all_txns.empty:
        return pd.DataFrame(columns=['date', 'asset_name', 'ticker', 'price', 'source'])

    logger.info(f"  Backfilling {len(new_assets)} new asset(s): {sorted(new_assets)[:5]}"
                + (f" ...+{len(new_assets)-5}" if len(new_assets) > 5 else ""))

    asset_txns = all_txns[all_txns['asset_name'].isin(new_assets)].copy()

    # Build per-day T1 prices for each new asset
    t1_by_asset: dict[str, dict] = {}
    for (asset_name, trade_date), grp in asset_txns.groupby(['asset_name', 'trade_date']):
        prices = extract_t1_prices(grp)
        if asset_name in prices:
            t1_by_asset.setdefault(asset_name, {})[trade_date] = prices[asset_name]

    # Date ranges per new asset — spine extended to global end date
    asset_ranges = (
        asset_txns.groupby('asset_name')['trade_date']
        .agg(first_date='min', last_date='max')
    )
    global_end = all_txns['trade_date'].max()

    # T2: Yahoo history for tickered new assets — read from historical_prices.parquet
    new_tickers = [ticker_map[a] for a in new_assets if a in ticker_map]
    earliest = asset_ranges['first_date'].min().strftime('%Y-%m-%d')
    yahoo_hist = fetch_yahoo_history(new_tickers, start_date=earliest, hist_prices=hist_prices)
    # {ticker: {date: price}}
    yahoo_by_ticker: dict[str, dict] = {}
    for _, row in yahoo_hist.iterrows():
        yahoo_by_ticker.setdefault(row['ticker'], {})[row['date']] = row['close']

    all_rows = []
    for asset_name in new_assets:
        if asset_name not in asset_ranges.index:
            continue
        first_date = asset_ranges.loc[asset_name, 'first_date']
        ticker = ticker_map.get(asset_name)
        dates = pd.date_range(first_date, global_end, freq='D')

        # Populate known prices
        price_series  = pd.Series(np.nan, index=dates)
        source_series = pd.Series(None,   index=dates, dtype=object)

        for d in dates:
            t1 = t1_by_asset.get(asset_name, {}).get(d)
            t2 = yahoo_by_ticker.get(ticker, {}).get(d) if ticker else None
            if t1 is not None:
                price_series[d],  source_series[d] = t1,  'transaction_observed'
            elif t2 is not None:
                price_series[d],  source_series[d] = t2,  'yahoo_finance'

        # T3a: linear interpolation between known dates
        known = price_series.notna()
        interp = price_series.interpolate(method='index')
        new_interp = interp.notna() & ~known
        price_series = interp
        source_series[new_interp] = 'linear_interpolation'

        # T3b: carry_forward for trailing gaps
        ffilled = price_series.ffill()
        new_ffill = ffilled.notna() & price_series.isna()
        price_series = ffilled
        source_series[new_ffill] = 'carry_forward'

        # Drop leading rows with no price data at all
        valid = price_series.notna()
        for d in dates[valid]:
            all_rows.append({
                'date':       d,
                'asset_name': asset_name,
                'ticker':     ticker,
                'price':      float(price_series[d]),
                'source':     source_series[d],
            })

    df = (pd.DataFrame(all_rows) if all_rows
          else pd.DataFrame(columns=['date', 'asset_name', 'ticker', 'price', 'source']))
    logger.info(f"  OK: Backfilled {len(df):,} rows for {len(new_assets)} new asset(s)")
    return df


def upsert_canonical(canonical: pd.DataFrame, new_rows: pd.DataFrame) -> pd.DataFrame:
    """
    Append new_rows to canonical and deduplicate on (date, asset_name).
    When a conflict exists, keep the highest-quality source (lowest SOURCE_RANK).
    """
    if new_rows.empty:
        return canonical
    combined = pd.concat([canonical, new_rows], ignore_index=True)
    combined['_rank'] = combined['source'].map(SOURCE_RANK).fillna(99)
    combined = (combined
                .sort_values('_rank')
                .drop_duplicates(subset=['date', 'asset_name'], keep='first')
                .drop(columns=['_rank'])
                .sort_values(['date', 'asset_name'])
                .reset_index(drop=True))
    return combined


def save_canonical_prices(df: pd.DataFrame):
    buf = BytesIO()
    df.to_parquet(buf, index=False, engine='pyarrow', compression='snappy')
    buf.seek(0)
    s3.put_object(Bucket=S3_BUCKET, Key='silver/prices/canonical_prices.parquet',
                  Body=buf.getvalue())
    logger.info(f"  OK: Saved canonical_prices.parquet "
                f"({len(buf.getvalue()) / 1024**2:.1f} MB, {len(df):,} rows, "
                f"{df['asset_name'].nunique():,} assets, "
                f"max date: {df['date'].max().date()})")


def save_daily_prices_trigger(canonical: pd.DataFrame, target_date: pd.Timestamp):
    """Write today's price rows to silver/prices/YYYY-MM-DD.parquet.

    This daily file is the S3 event trigger for bd-gold-trigger Lambda, which
    starts the gold layer runner EC2. Writing canonical_prices.parquet does NOT
    trigger gold (the S3 filter uses prefix 'silver/prices/20' to match dated
    files only, excluding canonical_prices.parquet).
    """
    daily = canonical[canonical['date'] == target_date].copy()
    if daily.empty:
        logger.warning(f"  No price rows for {target_date.date()} - gold trigger file not written")
        return {'written': False, 'reason': 'no_rows'}

    daily_norm = daily[['date', 'asset_name', 'ticker', 'price', 'source']].copy()
    daily_norm['date'] = pd.to_datetime(daily_norm['date']).dt.normalize()
    daily_norm['asset_name'] = daily_norm['asset_name'].fillna('').astype(str)
    daily_norm['ticker'] = daily_norm['ticker'].fillna('').astype(str)
    daily_norm['source'] = daily_norm['source'].fillna('').astype(str)
    daily_norm['price'] = pd.to_numeric(daily_norm['price'], errors='coerce').round(8)
    daily_norm = daily_norm.sort_values(['asset_name', 'ticker']).reset_index(drop=True)
    daily_hash = pd.util.hash_pandas_object(daily_norm, index=False).sum()

    key = f'silver/prices/{target_date.date()}.parquet'
    try:
        existing_obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        existing_df = pd.read_parquet(BytesIO(existing_obj['Body'].read()))
        existing_norm = existing_df[['date', 'asset_name', 'ticker', 'price', 'source']].copy()
        existing_norm['date'] = pd.to_datetime(existing_norm['date']).dt.normalize()
        existing_norm['asset_name'] = existing_norm['asset_name'].fillna('').astype(str)
        existing_norm['ticker'] = existing_norm['ticker'].fillna('').astype(str)
        existing_norm['source'] = existing_norm['source'].fillna('').astype(str)
        existing_norm['price'] = pd.to_numeric(existing_norm['price'], errors='coerce').round(8)
        existing_norm = existing_norm.sort_values(['asset_name', 'ticker']).reset_index(drop=True)
        existing_hash = pd.util.hash_pandas_object(existing_norm, index=False).sum()
        if len(existing_norm) == len(daily_norm) and existing_hash == daily_hash:
            logger.info(
                f"  Daily prices unchanged for {target_date.date()} - "
                "skipping rewrite to avoid duplicate gold trigger"
            )
            return {'written': False, 'reason': 'unchanged'}
    except ClientError as e:
        if e.response.get('Error', {}).get('Code') not in ('NoSuchKey', '404'):
            raise
    except Exception as e:
        logger.warning(f"  Could not compare existing daily prices trigger file: {e}")

    buf = BytesIO()
    daily.to_parquet(buf, index=False, engine='pyarrow', compression='snappy')
    buf.seek(0)
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buf.getvalue())
    logger.info(f"  Gold trigger: s3://{S3_BUCKET}/{key} "
                f"({len(daily):,} rows, {len(buf.getvalue()):,} bytes) "
                f"- S3 event will fire bd-gold-trigger")
    return {'written': True, 'reason': 'updated'}


# ============================================================================
# JOB 2: UPDATE INTERPOLATED_PRICES (unchanged from v4)
# ============================================================================

def extract_observed_prices(transactions_df: pd.DataFrame,
                             since_date: pd.Timestamp) -> pd.DataFrame:
    """Extract observed prices from recent transactions for interpolated_prices table."""
    recent = transactions_df[transactions_df['trade_date'] > since_date].copy()
    security = recent[~recent['asset_name'].isin(['CASH', 'Cash'])].copy()

    has_price = security['price'].notna() & (security['price'] > 0)
    security.loc[has_price, 'observed_price'] = security.loc[has_price, 'price']

    can_calculate = (
        ~has_price &
        security['market_value'].notna() &
        security['units'].notna() &
        (security['units'] != 0) &
        (security['market_value'] != 0)
    )
    security.loc[can_calculate, 'observed_price'] = (
        security.loc[can_calculate, 'market_value'] /
        security.loc[can_calculate, 'units']
    )

    priced = security[security['observed_price'].notna()].copy()
    observed = priced.groupby(['asset_name', 'trade_date']).agg(
        price=('observed_price', 'median'),
        num_observations=('transaction_id', 'count'),
    ).reset_index().rename(columns={'trade_date': 'date'})
    observed['data_quality'] = 'observed'

    logger.info(f"  Extracted {len(observed):,} asset x date observed prices")
    return observed


def update_interpolated_prices(new_observations: pd.DataFrame,
                                existing: pd.DataFrame) -> pd.DataFrame:
    """Append new observations to interpolated_prices, keeping observed over interpolated."""
    combined = pd.concat([existing, new_observations], ignore_index=True)
    combined['_q'] = combined['data_quality'].map(
        {'observed': 0, 'direct_observation': 0, 'interpolated': 1}
    ).fillna(1)
    combined = (combined
                .sort_values('_q')
                .drop_duplicates(subset=['asset_name', 'date'], keep='first')
                .drop(columns=['_q'])
                .sort_values(['asset_name', 'date'])
                .reset_index(drop=True))
    logger.info(f"  interpolated_prices: {len(combined):,} rows, "
                f"{combined['asset_name'].nunique():,} assets, "
                f"max date: {combined['date'].max().date() if len(combined) else 'n/a'}")
    return combined


# ============================================================================
# MAIN HANDLER
# ============================================================================

def lambda_handler(event, context):
    start = datetime.now()
    logger.info("=" * 80)
    logger.info("BD-PRICE-UPDATE v5 -- INCREMENTAL CANONICAL PRICES")
    logger.info("=" * 80)

    # Allow date override via event payload for backfills: {"date": "2026-02-23"}
    if event and event.get('date'):
        target_date = pd.Timestamp(event['date']).normalize()
        logger.info(f"Target date: {target_date.date()} (override from event)")
    else:
        target_date = pd.Timestamp.now().normalize() - timedelta(days=1)
        logger.info(f"Target date: {target_date.date()}")

    manifest = {
        'version': '5.0-incremental',
        'timestamp': start.isoformat(),
        'target_date': str(target_date.date()),
        'job1_canonical': {},
        'job2_interpolated': {},
        'status': 'in_progress',
    }

    try:
        # ------------------------------------------------------------------ #
        # JOB 1: Incremental canonical_prices update
        # ------------------------------------------------------------------ #
        logger.info("\n" + "=" * 80)
        logger.info("JOB 1: INCREMENTAL CANONICAL PRICES")
        logger.info("=" * 80)

        canonical = load_canonical_prices()

        if canonical.empty:
            logger.warning("canonical_prices.parquet is empty -- skipping Job 1. "
                           "Run build_canonical_prices_v2.py on EC2 to bootstrap.")
            manifest['job1_canonical']['skipped'] = 'bootstrap required'
        else:
            max_canonical_date = canonical['date'].max()

            if target_date <= max_canonical_date:
                logger.info(f"canonical_prices already covers {target_date.date()} -- "
                            f"checking for new assets only")

            # Step 1a: Load today's transactions for T1 extraction + new-asset detection
            logger.info("Step 1a: Load today's transactions...")
            today_txns = load_transactions_for_date(target_date)
            logger.info(f"  {len(today_txns):,} transactions for {target_date.date()}")

            ticker_map = load_ticker_lookup()

            # Step 1b: Detect new assets
            existing_assets = set(canonical['asset_name'].unique())
            today_assets = (set(today_txns['asset_name'].dropna().unique())
                            if not today_txns.empty else set())
            new_assets = today_assets - existing_assets
            logger.info(f"  Today's assets: {len(today_assets):,}  "
                        f"new (not in canonical): {len(new_assets)}")

            new_rows_list = []

            # Load historical_prices once -- used by both Step 1c and 1d
            hist_prices = load_historical_prices()

            # Step 1c: Build today's row for ALL existing assets
            # Run if target_date is new, OR if coverage is thin (e.g., weekend
            # dates where a prior run only wrote 1-2 rows instead of ~N assets).
            # Threshold: if < 50% of known assets have a price on target_date,
            # rebuild carry-forward rows for all assets on that date.
            existing_on_date = canonical[canonical['date'] == target_date]
            coverage_pct = (len(existing_on_date) / len(existing_assets) * 100
                            if existing_assets else 100)
            needs_rebuild = (target_date > max_canonical_date
                             or coverage_pct < 50)

            if needs_rebuild:
                if target_date <= max_canonical_date:
                    logger.info(f"Step 1c: {target_date.date()} has only "
                                f"{len(existing_on_date):,}/{len(existing_assets):,} "
                                f"assets ({coverage_pct:.0f}%) -- rebuilding carry-forwards")
                else:
                    logger.info("Step 1c: Fetching closes for today from historical_prices...")

                all_tickers = list({
                    t for a, t in ticker_map.items()
                    if a in existing_assets
                })
                yahoo_today = fetch_yahoo_closes_for_date(all_tickers, target_date, hist_prices)

                t1_today = extract_t1_prices(today_txns)
                today_rows = build_target_date_rows(
                    canonical, t1_today, yahoo_today, ticker_map, target_date
                )
                new_rows_list.append(today_rows)
            else:
                logger.info(f"Step 1c: Skipped -- {target_date.date()} already has "
                            f"{len(existing_on_date):,}/{len(existing_assets):,} "
                            f"assets ({coverage_pct:.0f}% coverage)")

            # Step 1d: Backfill new assets
            if new_assets:
                logger.info("Step 1d: Backfilling new assets...")
                all_txns = load_transactions_for_new_assets(new_assets)
                backfill_rows = backfill_new_assets(new_assets, all_txns, ticker_map, hist_prices)
                new_rows_list.append(backfill_rows)
            else:
                logger.info("Step 1d: No new assets -- backfill skipped")

            # Step 1e: Upsert and save
            if new_rows_list:
                all_new = pd.concat(new_rows_list, ignore_index=True)
                rows_before = len(canonical)
                canonical = upsert_canonical(canonical, all_new)
                logger.info(f"  Upserted {len(all_new):,} rows "
                            f"({len(canonical) - rows_before:,} net new after dedup)")
                logger.info("Step 1e: Saving canonical_prices.parquet...")
                save_canonical_prices(canonical)
                trigger_result = save_daily_prices_trigger(canonical, target_date)
            else:
                logger.info("Step 1e: Nothing to save -- canonical is already current")
                trigger_result = save_daily_prices_trigger(canonical, target_date)

            manifest['job1_canonical'] = {
                'target_date':      str(target_date.date()),
                'rows_total':       len(canonical),
                'assets_total':     canonical['asset_name'].nunique(),
                'new_assets_found': len(new_assets),
                'max_date':         str(canonical['date'].max().date()),
                'daily_trigger_written': trigger_result.get('written'),
                'daily_trigger_reason': trigger_result.get('reason'),
            }

        # ------------------------------------------------------------------ #
        # JOB 2: Update interpolated_prices.parquet
        # ------------------------------------------------------------------ #
        logger.info("\n" + "=" * 80)
        logger.info("JOB 2: UPDATE INTERPOLATED_PRICES")
        logger.info("=" * 80)

        since_date = target_date - timedelta(days=30)
        logger.info(f"Processing transactions since {since_date.date()}...")

        # Only load daily partition files whose YYYY-MM-DD filename is >= since_date.
        # Skip the backfill file (named backfill_*.parquet) -- it predates the 30-day
        # window on all normal runs and is 144 MB we don't need.
        since_str = since_date.strftime('%Y-%m-%d')
        paginator = s3.get_paginator('list_objects_v2')
        all_txn_keys = sorted(
            obj['Key']
            for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/transactions/')
            for obj in page.get('Contents', [])
            if obj['Key'].endswith('.parquet')
        )
        txn_keys = [
            k for k in all_txn_keys
            if (fname := k.split('/')[-1]) and not fname.startswith('backfill')
            and fname[:10] >= since_str
        ]
        logger.info(f"  Loading {len(txn_keys)} daily partition file(s) "
                    f"(of {len(all_txn_keys)} total) for last-30-day window")
        recent_txns = pd.concat(
            [_load_parquet_bytes(k) for k in txn_keys],
            ignore_index=True,
        ) if txn_keys else pd.DataFrame()
        if not recent_txns.empty:
            recent_txns['trade_date'] = pd.to_datetime(recent_txns['trade_date'], errors='coerce')
            if 'transaction_id' in recent_txns.columns:
                recent_txns = recent_txns.drop_duplicates(subset=['transaction_id'], keep='last')

        new_observations = extract_observed_prices(recent_txns, since_date)

        try:
            existing_interp = _load_parquet_bytes('silver/interpolated_prices.parquet')
            existing_interp['date'] = pd.to_datetime(existing_interp['date'])
        except Exception:
            existing_interp = pd.DataFrame(
                columns=['asset_name', 'date', 'price', 'data_quality', 'num_observations']
            )

        updated_interp = update_interpolated_prices(new_observations, existing_interp)

        buf = BytesIO()
        updated_interp.to_parquet(buf, index=False, engine='pyarrow', compression='snappy')
        buf.seek(0)
        s3.put_object(Bucket=S3_BUCKET, Key='silver/interpolated_prices.parquet',
                      Body=buf.getvalue())
        logger.info(f"  OK: Saved interpolated_prices.parquet")

        manifest['job2_interpolated'] = {
            'rows_total':        len(updated_interp),
            'assets_total':      int(updated_interp['asset_name'].nunique()),
            'new_observations':  len(new_observations),
            'max_date':          str(updated_interp['date'].max().date() if len(updated_interp) else 'n/a'),
        }

        # ------------------------------------------------------------------ #
        # Audit manifest
        # ------------------------------------------------------------------ #
        manifest['status'] = 'success'
        manifest['duration_seconds'] = (datetime.now() - start).total_seconds()
        manifest_key = f'logs/price_updates/manifest_{target_date.strftime("%Y-%m-%d")}.json'
        s3.put_object(Bucket=S3_BUCKET, Key=manifest_key,
                      Body=json.dumps(manifest, indent=2),
                      ContentType='application/json')

        logger.info("\n" + "=" * 80)
        logger.info("COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Duration: {manifest['duration_seconds']:.1f}s")
        if manifest['job1_canonical']:
            logger.info(f"canonical_prices: {manifest['job1_canonical'].get('rows_total', 'n/a'):,} rows, "
                        f"max date: {manifest['job1_canonical'].get('max_date', 'n/a')}")
        logger.info(f"interpolated_prices: {manifest['job2_interpolated']['rows_total']:,} rows")

        return {'statusCode': 200, 'body': json.dumps(manifest)}

    except Exception as e:
        import traceback
        logger.error(f"FAILED: {e}\n{traceback.format_exc()}")
        manifest['status'] = 'failed'
        manifest['error'] = str(e)
        try:
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=f'logs/price_updates/error_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json',
                Body=json.dumps(manifest, indent=2),
                ContentType='application/json',
            )
        except Exception:
            pass
        return {'statusCode': 500, 'body': json.dumps(manifest)}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', default=None,
                        help='Target date YYYY-MM-DD (default: yesterday)')
    args = parser.parse_args()
    event = {'date': args.date} if args.date else {}
    result = lambda_handler(event, None)
    print(json.dumps(json.loads(result['body']), indent=2))
