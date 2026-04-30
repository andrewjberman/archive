#!/usr/bin/env python3
"""
INF_B_00 -- Canonical Holdings (positions_mv pass-through)

Pulls daily per-(account_id, ticker) market values DIRECTLY from
silver/api_dims/positions_mv (sourced from Orion REST
/Portfolio/Clients/{cid}/Assets/{date}). No TRN-as-price reconstruction.

Joined with silver/api_dims/accounts_v2 for advisor attribution
(DIAGFIX.011 representative_name + rep_id servicing-rep priority).

ARCHAEOLOGY: prior implementation reconstructed positions from
silver/transactions, accumulating units per (account_id, ticker) and using
nav_price last-seen-wins from TRN. That approach corrupted prices on
non-trade events (advisory fees, journals, distributions with nav_price=0)
-- 40.2% of holdings rows had market_value=$0 before the DIAGFIX.002b
nav>0 guard at commit 127fe2a17. Even with the guard, prices used were the
LAST TRADE price, potentially days/weeks stale. DIAGFIX.009-NEW Phase 1
(commit 91da4d6a1) + DIAGFIX.012 Phase 2.5 durability check (2026-04-30)
confirmed Orion's per-day endpoint serves real per-position MV with 100%
200 OK and historical depth to -180d. TRN feed is preserved for INF_B_01
(lots) / INF_B_02 (canonical_lots) / INF_B_03 (account_gains) -- TRN is a
transaction log, not a price source.

Inputs:
  silver/api_dims/positions_mv/snapshot_date={date}/data.parquet
  silver/api_dims/accounts_v2/snapshot_date={latest}/data.parquet

Output:
  gold/canonical/holdings_{YYYY-MM-DD}.parquet per snapshot date

Columns per output file (schema preserved for INF_B_01/B_02/B_03/I_D03 etc):
  date, account_id, ticker, product_name, advisor_key, rep_bucket,
  custodian, units, nav_price, market_value

Usage:
  python3 INF_B_00.canonical_holdings.py --date 2026-04-30 --upload
  python3 INF_B_00.canonical_holdings.py --start-date 2026-04-01 --end-date 2026-04-30 --upload
  python3 INF_B_00.canonical_holdings.py --upload                   # all available dates

Author: 0.4.0_DS_ClientPlatform
Project: ADVI_INFLEC.DIAGFIX.012 Phase 4
Date: 2026-04-30
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
import traceback
from io import BytesIO

import boto3
import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

S3_BUCKET = 'opal-data-inf'
POSITIONS_MV_PREFIX = 'silver/positions_mv/'
ACCOUNTS_V2_PREFIX = 'silver/api_dims/accounts_v2/'
GOLD_HOLDINGS_PREFIX = 'gold/canonical/'

s3 = boto3.client('s3', region_name='us-east-1')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f'[{ts}] {msg}', flush=True)


def _read_s3(key):
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


def _write_s3(df, key):
    buf = BytesIO()
    df.to_parquet(buf, index=False, engine='pyarrow', compression='snappy')
    buf.seek(0)
    s3.put_object(
        Bucket=S3_BUCKET, Key=key,
        Body=buf.getvalue(), ServerSideEncryption='AES256',
    )


def _holdings_key(date_str):
    return f'{GOLD_HOLDINGS_PREFIX}holdings_{date_str}.parquet'


# ---------------------------------------------------------------------------
# Advisor attribution helpers (mirror silver/convert_orion_to_silver._advisor_key
# / _rep_bucket so gold doesn't import silver code paths)
# ---------------------------------------------------------------------------

FIRM_REPS = {'inflection wealth management'}
ROUTING_REPS = {'new accounts rep'}


def _advisor_key(rep_name) -> str:
    if not isinstance(rep_name, str) or not rep_name.strip():
        return 'unknown'
    s = rep_name.strip().lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or 'unknown'


def _rep_bucket(rep_name) -> str:
    if not isinstance(rep_name, str):
        return 'firm'
    name = rep_name.strip().lower()
    if not name:
        return 'firm'
    if name in FIRM_REPS:
        return 'firm'
    if name in ROUTING_REPS:
        return 'routing'
    return 'individual'


CUSTODIAN_NORMALIZE = {
    'fidelity_inflection': 'fidelity',
    'fidelity':            'fidelity',
    'schwab':              'schwab',
}


def _normalize_custodian(val) -> str:
    if not isinstance(val, str):
        return ''
    v = val.strip().lower()
    return CUSTODIAN_NORMALIZE.get(v, v)


# ---------------------------------------------------------------------------
# Silver loaders
# ---------------------------------------------------------------------------

def list_positions_mv_dates() -> dict[str, str]:
    """Return {snapshot_date_str: s3_key} for every positions_mv partition."""
    paginator = s3.get_paginator('list_objects_v2')
    dates = {}
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=POSITIONS_MV_PREFIX):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if not key.endswith('.parquet'):
                continue
            m = re.search(r'(\d{4}-\d{2}-\d{2})\.parquet$', key)
            if m:
                dates[m.group(1)] = key
    return dict(sorted(dates.items()))


def latest_accounts_v2_key() -> str:
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=ACCOUNTS_V2_PREFIX)
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('/data.parquet')
    ])
    if not keys:
        raise RuntimeError('No silver/api_dims/accounts_v2 partitions found.')
    return keys[-1]


def load_accounts_v2() -> pd.DataFrame:
    """Per-account advisor attribution from DIAGFIX.011 silver dim."""
    key = latest_accounts_v2_key()
    log(f'Loading accounts_v2 from s3://{S3_BUCKET}/{key}')
    df = _read_s3(key)
    for col in ('account_id', 'representative_name'):
        if col not in df.columns:
            raise RuntimeError(f'accounts_v2 missing {col}; got {list(df.columns)}')
    df = df[['account_id', 'representative_name', 'rep_id']].copy()
    df['account_id'] = df['account_id'].astype(str)
    # accounts_v2 already has one row per account; drop_duplicates is defensive
    df = df.drop_duplicates(subset=['account_id'], keep='first')
    log(f'  rows={len(df):,} | distinct reps={df["representative_name"].nunique()}')
    return df


# ---------------------------------------------------------------------------
# Holdings build (positions_mv pass-through)
# ---------------------------------------------------------------------------

def build_snapshot(snap_date_str: str, accounts: pd.DataFrame) -> pd.DataFrame:
    key = f'{POSITIONS_MV_PREFIX}snapshot_date={snap_date_str}/data.parquet'
    pos = _read_s3(key)
    n_initial = len(pos)
    pos = pos[pos['current_shares'].fillna(0).astype(float) > 1e-9].copy()
    log(f'  [{snap_date_str}] positions_mv: {n_initial:,} -> {len(pos):,} (units>0)')
    if pos.empty:
        return pd.DataFrame()

    pos['account_id'] = pos['account_id'].astype('Int64').astype(str)
    merged = pos.merge(accounts, on='account_id', how='left')

    # Default representative_name when account isn't in accounts_v2 (e.g., custodian
    # other than Fidelity_Inflection -- accounts_v2 silver filters to that custodian).
    merged['representative_name'] = merged['representative_name'].fillna(
        'Inflection Wealth Management'
    )

    out = pd.DataFrame({
        'date':         pd.to_datetime(snap_date_str),
        'account_id':   merged['account_id'].astype(str),
        'ticker':       merged['ticker'].astype(str),
        'product_name': merged['name'].fillna('').astype(str),
        'advisor_key':  merged['representative_name'].apply(_advisor_key),
        'rep_bucket':   merged['representative_name'].apply(_rep_bucket),
        'custodian':    merged['custodian'].apply(_normalize_custodian),
        'units':        merged['current_shares'].astype(float),
        'nav_price':    merged['current_price'].astype(float),
        'market_value': merged['current_value'].astype(float),
    })

    # Drop rows with empty / null tickers (cash-like entries with no symbol)
    out = out[out['ticker'].str.strip() != '']
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description='INF_B_00: Canonical Holdings (positions_mv pass-through)')
    p.add_argument('--date', type=str, default=None,
                   help='Single snapshot date YYYY-MM-DD')
    p.add_argument('--start-date', type=str, default=None)
    p.add_argument('--end-date', type=str, default=None)
    p.add_argument('--upload', action='store_true', help='Write outputs to S3')
    p.add_argument('--dry-run', action='store_true', help='Stats only, no writes')
    args = p.parse_args()

    dry_run = args.dry_run or not args.upload

    log('=' * 70)
    log('INF_B_00: CANONICAL HOLDINGS (positions_mv pass-through)')
    log(f'Mode: {"DRY RUN" if dry_run else "UPLOAD"}')
    log('=' * 70)

    available = list_positions_mv_dates()
    if not available:
        log('ERROR: no silver/api_dims/positions_mv partitions found. '
            'Run pull_inflection_positions_daily + convert_orion_api_to_silver --dim positions_mv first.')
        sys.exit(1)
    log(f'Available positions_mv snapshots: {len(available)} '
        f'({min(available)} -> {max(available)})')

    if args.date:
        if args.date not in available:
            log(f'ERROR: --date {args.date} not in available positions_mv snapshots.')
            sys.exit(1)
        dates = [args.date]
    elif args.start_date or args.end_date:
        start = args.start_date or min(available)
        end = args.end_date or max(available)
        dates = [d for d in available if start <= d <= end]
    else:
        dates = list(available.keys())

    if not dates:
        log('No snapshot dates in requested range. Exiting.')
        return
    log(f'Dates to emit: {len(dates)} ({dates[0]} -> {dates[-1]})')

    accounts = load_accounts_v2()

    written = 0
    total_rows = 0
    for snap in dates:
        snap_df = build_snapshot(snap, accounts)
        if snap_df.empty:
            log(f'  [{snap}] empty snapshot; skipping')
            continue
        n_acct = snap_df['account_id'].nunique()
        n_tkr = snap_df['ticker'].nunique()
        mv = snap_df['market_value'].sum()
        log(f'  [{snap}] rows={len(snap_df):,} | accounts={n_acct} | tickers={n_tkr} | mv=${mv:,.0f}')
        total_rows += len(snap_df)
        if not dry_run:
            _write_s3(snap_df, _holdings_key(snap))
            written += 1

    log('=' * 70)
    log('SUMMARY')
    log('=' * 70)
    log(f'Dates emitted: {len(dates):,}')
    log(f'Total rows:    {total_rows:,}')
    log(f'Mode:          {"DRY RUN" if dry_run else f"UPLOADED {written} files"}')
    log('INF_B_00 complete.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        print(f'[{ts}] ERROR: INF_B_00 failed: {exc}', flush=True)
        traceback.print_exc()
        sys.exit(1)
