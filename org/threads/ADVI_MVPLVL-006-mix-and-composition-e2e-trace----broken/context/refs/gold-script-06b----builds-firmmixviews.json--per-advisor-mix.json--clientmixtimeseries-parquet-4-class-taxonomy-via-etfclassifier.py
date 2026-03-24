#!/usr/bin/env python3
"""
Build Client Mix + Concentration Timeseries

Joins positions_cube x canonical_prices x accounts_dimension to produce
one JSON per relationship containing full mix and concentration history.

Output pattern (consistent with gold/advisors/{advisor_id}/book.json):
    gold/client_timeseries/{relationship_id}.json   -- one per relationship

    {
      "generated_at": "...",
      "data_as_of":   "YYYY-MM-DD",
      "relationship_id": "...",
      "mix": [
        {"date":"YYYY-MM-DD","equity":0.72,"fixed_income":0.24,
         "structured_notes":0.02,"cash":0.02,"other":0.0},
        ...
      ],
      "concentration": [
        {"date":"YYYY-MM-DD","holdings":[
          {"asset_name":"...","ticker":"...","asset_class":"equity",
           "market_value":50000.0,"pct":0.15},
          ... (top 10 by market_value)
        ]},
        ...
      ]
    }

Watermark: gold/client_timeseries/_watermark.json
    {"data_as_of": "YYYY-MM-DD"}
    Written after each successful run. Incremental mode reads this to determine
    which positions_cube partitions to process.

AP active gate: excludes account_ids not present in account_performance within
45 days of the snapshot date (prevents ~$371M stale-holdings inflation).

pct sum validation: per (date, relationship_id) mix must sum to 1.0 (+-0.001).
Dates failing validation are excluded from the JSON output.

Concurrency: ThreadPoolExecutor for both partition processing and JSON writes.
Defaults: 32 process workers, 64 write workers (tuned for r6i.4xlarge).
Override via env vars O6B_PROCESS_WORKERS, O6B_WRITE_WORKERS, or --workers flag.
Daily incremental (1-10 partitions) runs fine on r6i.xlarge with low concurrency.

Usage:
    python3 06b_build_client_mix_timeseries.py --upload               # full rebuild
    python3 06b_build_client_mix_timeseries.py --upload --incremental # incremental
    python3 06b_build_client_mix_timeseries.py --upload --workers 8   # lower concurrency
    python3 06b_build_client_mix_timeseries.py --dry-run              # no write
    python3 06b_build_client_mix_timeseries.py --dry-run -v           # verbose

Author: 0.4.0_DS_ClientPlatform
Date:   2026-03-16
"""

import argparse
import gc
import json
import os
import pathlib
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from io import BytesIO

import boto3
import pandas as pd
from lib.etf_classifier import ETFClassifier

S3_BUCKET      = 'opal-data-bd'
OUTPUT_PREFIX  = 'gold/client_timeseries'
WATERMARK_KEY  = 'gold/client_timeseries/_watermark.json'
AP_GATE_DAYS         = 45
AP_GATE_DAYS_DEFAULT = 45   # standard gate for all accounts
PCT_TOL              = 0.001
TOP_N_CONC           = 10

# Firm/advisor mix views output paths
FIRM_ID          = os.environ.get('O6B_FIRM_ID', '49financial')
FIRM_MIX_KEY     = 'gold/firm_mix_views.json'
FIRM_DAILY_KEY   = 'gold/firm_mix_views_daily.json'
ADV_MIX_PREFIX   = 'gold/advisors'
REL_LOOKUP_KEY   = 'gold/views/rel_architect_lookup.parquet'

# Insurance account config -- loaded at startup from insurance_accounts.json
_INSURANCE_CONFIG_PATH = pathlib.Path(__file__).parent / 'insurance_accounts.json'


def _load_insurance_config() -> tuple[set, int]:
    """
    Load insurance_accounts.json.

    Returns:
        (insurance_account_ids: set[str], ap_gate_days_override: int)

    insurance_accounts.json format:
    {
        "insurance_account_ids": ["acc_xxx", "acc_yyy"],
        "ap_gate_days_override": 180,
        "_comment": "Add new accounts when new insurance products are onboarded."
    }

    Insurance/annuity accounts operate on quarterly statement cycles and update
    account_performance infrequently (monthly/quarterly). The standard 45-day AP
    gate incorrectly excludes them during inter-statement gaps, causing ~$60M of
    structured_notes to appear and disappear. These accounts receive an extended
    gate (default 180 days) instead of the global 45-day gate.

    To populate: run .tmp_insurance_ap_gate.py and copy the suggested
    insurance_account_ids into this file.
    """
    if not _INSURANCE_CONFIG_PATH.exists():
        return set(), AP_GATE_DAYS_DEFAULT
    try:
        cfg = json.loads(_INSURANCE_CONFIG_PATH.read_text())
        ids = set(str(x) for x in cfg.get('insurance_account_ids', []))
        days = int(cfg.get('ap_gate_days_override', AP_GATE_DAYS_DEFAULT))
        print(f"  Insurance gate override: {len(ids)} accounts, {days}-day gate")
        return ids, days
    except Exception as e:
        print(f"  WARN: could not load insurance_accounts.json: {e} -- using default gate")
        return set(), AP_GATE_DAYS_DEFAULT

# Thread-local S3 clients (boto3 clients are not thread-safe)
_thread_local = threading.local()

def _get_s3():
    if not hasattr(_thread_local, 's3'):
        _thread_local.s3 = boto3.client('s3', region_name='us-east-1')
    return _thread_local.s3

# Main-thread client for setup/teardown
s3 = boto3.client('s3', region_name='us-east-1')

# Concurrency settings (r6i.xlarge: 4 vCPU, 32GB -- I/O bound, safe to oversubscribe)
PROCESS_WORKERS = int(os.environ.get('O6B_PROCESS_WORKERS', '128'))
WRITE_WORKERS   = int(os.environ.get('O6B_WRITE_WORKERS', '128'))


# =============================================================================
# Classification (ETFClassifier-backed, GLDPRE 4-class taxonomy)
# =============================================================================

_MIX_ASSET_CLASSES = ['equity', 'fixed_income', 'alternatives']


def classify_holding(ticker, asset_name) -> str:
    """Classify a holding using DynamoDB-backed ETFClassifier."""
    cls = ETFClassifier.instance().classify(ticker, asset_name)
    if cls:  # 'equity', 'fixed_income', or 'alternatives'
        return cls
    # Unclassified with valid ticker -> conservative equity default
    if ticker:
        t = str(ticker).strip().upper()
        if t and t not in ('NONE', 'NAN', '') and t.isalpha() and 1 <= len(t) <= 5:
            return 'equity'
    return 'equity'  # ultimate fallback for positions


def classify_series(ticker_series: pd.Series, name_series: pd.Series) -> pd.Series:
    """Classify a series of holdings using DynamoDB-backed ETFClassifier.

    Returns a Series with values in {'equity', 'fixed_income', 'alternatives'}.
    Unclassified positions default to 'equity' (conservative fallback).
    """
    classifier = ETFClassifier.instance()
    result = pd.Series('equity', index=ticker_series.index, dtype='object')
    for idx in ticker_series.index:
        ticker = ticker_series[idx]
        name = name_series[idx]
        cls = classifier.classify(
            str(ticker) if pd.notna(ticker) else '',
            str(name) if pd.notna(name) else '',
        )
        if cls:
            result[idx] = cls
        # else: stays 'equity' (default)
    return result


# =============================================================================
# S3 helpers
# =============================================================================

def _read_parquet(key: str) -> pd.DataFrame:
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


def _list_positions_cube_keys() -> list:
    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='gold/positions_cube/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])
    return sorted(keys)


def _parse_date(key: str) -> str:
    return key.rsplit('/', 1)[-1].replace('.parquet', '')


def _load_watermark() -> str | None:
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=WATERMARK_KEY)
        data = json.loads(resp['Body'].read())
        wm = data.get('data_as_of')
        print(f"  Watermark: {wm}")
        return wm
    except Exception:
        return None


def _write_watermark(data_as_of: str, rel_count: int, dry_run: bool) -> None:
    body = json.dumps({'data_as_of': data_as_of, 'relationship_count': rel_count}).encode()
    if not dry_run:
        s3.put_object(Bucket=S3_BUCKET, Key=WATERMARK_KEY, Body=body,
                      ContentType='application/json')
    print(f"  Watermark -> {data_as_of} ({rel_count} relationships)")


def _write_relationship_json(rel_id: str, payload: dict, dry_run: bool) -> None:
    key = f'{OUTPUT_PREFIX}/{rel_id}.json'
    body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        _get_s3().put_object(Bucket=S3_BUCKET, Key=key, Body=body,
                             ContentType='application/json',
                             CacheControl='public, max-age=300, s-maxage=3600')


def _read_relationship_json(rel_id: str) -> dict | None:
    try:
        resp = _get_s3().get_object(Bucket=S3_BUCKET, Key=f'{OUTPUT_PREFIX}/{rel_id}.json')
        return json.loads(resp['Body'].read())
    except Exception:
        return None


def _load_firm_daily() -> dict:
    """Load existing firm_mix_views_daily.json from S3. Returns {} on miss."""
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=FIRM_DAILY_KEY)
        return json.loads(resp['Body'].read())
    except Exception:
        return {}


def _write_firm_daily(daily_dict: dict, dry_run: bool) -> None:
    body = json.dumps(daily_dict, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        s3.put_object(Bucket=S3_BUCKET, Key=FIRM_DAILY_KEY, Body=body,
                      ContentType='application/json')


def _load_advisor_daily(advisor_id: str) -> dict:
    """Load existing mix_daily.json for an advisor. Returns {} on miss."""
    try:
        key = f'{ADV_MIX_PREFIX}/{advisor_id}/mix_daily.json'
        resp = _get_s3().get_object(Bucket=S3_BUCKET, Key=key)
        return json.loads(resp['Body'].read())
    except Exception:
        return {}


def _write_advisor_mix(advisor_id: str, advisor_name: str, data_as_of: str,
                       daily_dict: dict, now_str: str, dry_run: bool) -> None:
    """Write mix_daily.json (raw accumulator) and mix.json (period views) for one advisor."""
    # Raw daily accumulator
    raw_key = f'{ADV_MIX_PREFIX}/{advisor_id}/mix_daily.json'
    raw_body = json.dumps(daily_dict, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        _get_s3().put_object(Bucket=S3_BUCKET, Key=raw_key, Body=raw_body,
                             ContentType='application/json')

    # Period views
    views = compute_period_views(daily_dict)
    if not views['annually']:
        return  # Skip advisors with no annual data

    payload = {
        'generated_at': now_str,
        'data_as_of':   data_as_of,
        'advisor_id':   advisor_id,
        'advisor_name': advisor_name,
        'views':        views,
    }
    mix_key = f'{ADV_MIX_PREFIX}/{advisor_id}/mix.json'
    mix_body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        _get_s3().put_object(Bucket=S3_BUCKET, Key=mix_key, Body=mix_body,
                             ContentType='application/json',
                             CacheControl='public, max-age=300, s-maxage=3600')


def compute_period_views(daily_dict: dict, cp_daily_total=None) -> dict:
    """
    Compute quarterly, monthly, and annually period views from a daily dollar dict.

    Args:
        daily_dict: {date_str: {equity: $, fixed_income: $, structured_notes: $,
                                cash: $, other: $, total: $}}
                    Keys are YYYY-MM-DD strings.
        cp_daily_total: pd.Series indexed by date with firm-level total_aua from
                        client_performance.parquet. When provided, replaces the
                        positions_cube total with the authoritative total, keeping
                        class percentages from positions_cube. Cash is residual.

    Returns:
        {"quarterly": [...], "monthly": [...], "annually": [...]}

    Each period entry:
        {period, label, end_date, total_aua,
         equity: {value, pct}, fixed_income: {value, pct},
         structured_notes: {value, pct}, cash: {value, pct}, other: {value, pct}}

    Period logic mirrors PartnerAnalytics.tsx getPeriodInfo():
        quarterly: period="YYYY-Q#",  label="Q# 'YY"   (e.g. "Q4 '24")
        monthly:   period="YYYY-MM",  label="Mon 'YY"  (e.g. "Oct '24")
        annually:  period="YYYY",     label="YYYY"     (e.g. "2024")

    Takes the LAST date in each period as the end-of-period snapshot.
    pct values are 0-1.
    """
    _MONTH_SHORT = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec']

    def _period_key_label(date_str: str, granularity: str) -> tuple[str, str]:
        year  = int(date_str[:4])
        month = int(date_str[5:7])
        yy    = date_str[2:4]
        if granularity == 'quarterly':
            q = (month - 1) // 3 + 1
            return f'{year}-Q{q}', f"Q{q} '{yy}"
        elif granularity == 'monthly':
            return f'{year}-{month:02d}', f"{_MONTH_SHORT[month - 1]} '{yy}"
        else:  # annually
            return str(year), str(year)

    def _build_granularity(granularity: str) -> list:
        # Map period_key -> (last date_str, last entry)
        period_map: dict[str, tuple[str, dict]] = {}
        for date_str in sorted(daily_dict.keys()):
            entry = daily_dict[date_str]
            pk, pl = _period_key_label(date_str, granularity)
            # Always overwrite: last date in period wins (end-of-period snapshot)
            period_map[pk] = (date_str, entry, pl)

        result = []
        for pk in sorted(period_map.keys()):
            end_date, entry, pl = period_map[pk]
            cube_total = float(entry.get('total', 0.0))
            if cube_total <= 0:
                continue

            # Use client_performance total (authoritative) if available
            total = cube_total
            if cp_daily_total is not None:
                cp_val = cp_daily_total.get(pd.Timestamp(end_date))
                if cp_val is not None and cp_val > 0:
                    total = float(cp_val)

            row = {
                'period':    pk,
                'label':     pl,
                'end_date':  end_date,
                'total_aua': round(total, 2),
            }
            # Class pcts from positions_cube (correct ratios), scaled to
            # authoritative total from client_performance
            for ac in _MIX_ASSET_CLASSES:
                pct = float(entry.get(ac, 0.0)) / cube_total if cube_total > 0 else 0.0
                val = round(total * pct, 2)
                row[ac] = {
                    'value': val,
                    'pct':   round(pct, 6),
                }
            # Cash is residual: total - classified classes
            classified_sum = sum(row[ac]['value'] for ac in _MIX_ASSET_CLASSES)
            cash_val = max(0.0, round(total - classified_sum, 2))
            row['cash'] = {
                'value': cash_val,
                'pct':   round(cash_val / total, 6) if total > 0 else 0.0,
            }
            result.append(row)
        return result

    return {
        'quarterly': _build_granularity('quarterly'),
        'monthly':   _build_granularity('monthly'),
        'annually':  _build_granularity('annually'),
    }


# =============================================================================
# Static table loading
# =============================================================================


def _load_rel_architect_lookup() -> dict:
    """
    Load rel_architect_lookup.parquet from S3.

    Returns {relationship_id: advisor_name} dict.
    Returns {} and logs a warning if the file is missing (06b continues without
    advisor aggregation -- firm-level mix still runs normally).
    """
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=REL_LOOKUP_KEY)
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        if 'relationship_id' not in df.columns or 'architect' not in df.columns:
            print(f"  WARN: rel_architect_lookup.parquet missing expected columns "
                  f"(found: {list(df.columns)}) -- skipping advisor aggregation")
            return {}
        result = dict(zip(df['relationship_id'].astype(str), df['architect'].astype(str)))
        unique_advisors = len(set(result.values()))
        print(f"  rel_architect_lookup: {len(result):,} relationships, {unique_advisors} advisors")
        return result
    except Exception as e:
        print(f"  WARN: could not load rel_architect_lookup.parquet: {e} "
              f"-- skipping advisor aggregation")
        return {}

def load_static_tables(verbose: bool = False):
    print("Loading accounts_dimension... ", end='', flush=True)
    acct_dim = _read_parquet('gold/accounts_dimension_latest.parquet')
    acct_rel = acct_dim[['account_id', 'relationship_id']].dropna(subset=['relationship_id'])
    acct_rel_dict = dict(zip(
        acct_rel['account_id'].astype(str),
        acct_rel['relationship_id'].astype(str)
    ))
    print(f"{len(acct_rel_dict):,} accounts")

    print("Loading canonical_prices... ", end='', flush=True)
    canonical = _read_parquet('silver/prices/canonical_prices.parquet')
    canonical['date'] = pd.to_datetime(canonical['date'])
    canonical = canonical.sort_values('source').drop_duplicates(
        subset=['date', 'asset_name'], keep='first'
    )
    prices_grouped = canonical.groupby('date')
    print(f"{len(canonical):,} rows")
    del canonical
    gc.collect()

    print("Loading account_performance (AP gate)... ", end='', flush=True)
    ap = _read_parquet('gold/account_performance.parquet')
    ap['date'] = pd.to_datetime(ap['date'])
    ap_last_seen = ap.groupby('account_id')['date'].max().to_dict()
    max_ap_date = ap['date'].max().date()
    print(f"{len(ap_last_seen):,} accounts, max date {max_ap_date}")
    del ap
    gc.collect()

    print("Loading insurance account config... ", end='', flush=True)
    insurance_account_ids, insurance_gate_days = _load_insurance_config()

    print("Loading rel_architect_lookup (advisor mapping)...")
    rel_advisor_dict = _load_rel_architect_lookup()

    print("Loading client_performance (authoritative AUA totals)... ", end='', flush=True)
    cp = _read_parquet('gold/client_performance.parquet')
    cp['date'] = pd.to_datetime(cp['date'])
    cp_daily_total = cp.groupby('date')['total_aua'].sum()
    print(f"{len(cp_daily_total):,} dates")
    del cp
    gc.collect()

    return acct_rel_dict, prices_grouped, ap_last_seen, insurance_account_ids, insurance_gate_days, rel_advisor_dict, cp_daily_total


# =============================================================================
# Per-date processing — returns data keyed by relationship_id
# =============================================================================

def process_date(key, date_str, prices_grouped, acct_rel_dict, ap_last_seen, verbose=False,
                 insurance_account_ids=None, insurance_gate_days=AP_GATE_DAYS_DEFAULT):
    """
    Process one positions_cube partition.

    Returns dict: {relationship_id: {'mix': {asset_class: mv}, 'conc': [(mv, asset_name, ticker, cls)]}}
    or empty dict if the date has no usable data.

    AP gate: standard accounts use AP_GATE_DAYS (45). Accounts in insurance_account_ids
    use insurance_gate_days (default 180). Insurance/annuity accounts report on monthly or
    quarterly statement cycles -- the standard 45-day gate incorrectly excludes them during
    inter-statement gaps, causing structured_notes oscillation.
    """
    date_ts          = pd.Timestamp(date_str)
    std_cutoff       = date_ts - pd.Timedelta(days=AP_GATE_DAYS_DEFAULT)
    ins_cutoff       = date_ts - pd.Timedelta(days=insurance_gate_days)
    insurance_ids    = insurance_account_ids or set()

    resp = _get_s3().get_object(Bucket=S3_BUCKET, Key=key)
    pos = pd.read_parquet(BytesIO(resp['Body'].read()))

    if pos.empty:
        return {}

    # AP gate: vectorized per-account cutoff based on account type
    pos['account_id'] = pos['account_id'].astype(str)
    last_seen = pos['account_id'].map(ap_last_seen).fillna(pd.Timestamp.min)

    # Standard gate applies to all accounts
    standard_ok  = last_seen >= std_cutoff
    # Insurance override: extended gate for flagged accounts
    is_insurance = pos['account_id'].isin(insurance_ids)
    insurance_ok = is_insurance & (last_seen >= ins_cutoff)

    pos = pos[standard_ok | insurance_ok]
    if pos.empty:
        return {}

    # Resolve relationship_id
    pos['relationship_id'] = pos['account_id'].map(acct_rel_dict)
    pos = pos.dropna(subset=['relationship_id'])
    if pos.empty:
        return {}

    # Join prices
    try:
        prices_day = prices_grouped.get_group(date_ts)[['asset_name', 'ticker', 'price']].copy()
    except KeyError:
        if verbose:
            print(f"    SKIP {date_str}: no prices")
        return {}

    pos = pos.merge(prices_day, on='asset_name', how='left')
    pos['market_value'] = pos['units'] * pos['price']
    pos = pos.dropna(subset=['market_value'])
    pos = pos[pos['market_value'] > 0]
    if pos.empty:
        return {}

    # Classify (vectorized: C-level dict lookups + regex, Python fallback for edge cases)
    pos['asset_class'] = classify_series(pos['ticker'], pos['asset_name'])

    # Aggregate by relationship
    result = {}
    for rel_id, grp in pos.groupby('relationship_id', sort=False):
        total_mv = float(grp['market_value'].sum())
        if total_mv <= 0:
            continue

        # Mix: sum by asset_class
        mix_agg = grp.groupby('asset_class')['market_value'].sum()
        pct_sum = sum(mix_agg.values) / total_mv
        if abs(pct_sum - 1.0) > PCT_TOL:
            if verbose:
                print(f"    SKIP {rel_id} on {date_str}: pct sum {pct_sum:.4f}")
            continue

        mix = {}
        for ac in _MIX_ASSET_CLASSES:
            mix[ac] = round(float(mix_agg.get(ac, 0.0)) / total_mv, 6)

        # Concentration: group by (asset_name, ticker, asset_class), top-N by mv
        conc_grp = (
            grp.groupby(['asset_name', 'ticker', 'asset_class'], sort=False, dropna=False)
            ['market_value'].sum()
            .reset_index()
            .sort_values('market_value', ascending=False)
            .head(TOP_N_CONC)
        )
        holdings = []
        for _, row in conc_grp.iterrows():
            ticker_val = row['ticker']
            if not ticker_val or str(ticker_val).strip().upper() in ('NAN', 'NONE', ''):
                ticker_val = None
            holdings.append({
                'asset_name':  str(row['asset_name']),
                'ticker':      ticker_val,
                'asset_class': str(row['asset_class']),
                'market_value': round(float(row['market_value']), 2),
                'pct':          round(float(row['market_value']) / total_mv, 6),
            })

        result[rel_id] = {'mix': mix, 'conc': holdings, 'total_mv': total_mv}

    return result


# =============================================================================
# Build
# =============================================================================

def build(upload: bool, incremental: bool, dry_run: bool, verbose: bool) -> None:
    print("=" * 70)
    print("06b_build_client_mix_timeseries.py")
    print(f"Mode:    {'incremental' if incremental else 'full'}")
    print(f"Workers: {PROCESS_WORKERS} process / {WRITE_WORKERS} write")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Watermark
    watermark = None
    if incremental:
        watermark = _load_watermark()
        if watermark is None:
            print("  No watermark found -- falling back to full build")
            incremental = False

    # Static tables
    print("\nLoading static tables...")
    acct_rel_dict, prices_grouped, ap_last_seen, insurance_account_ids, insurance_gate_days, \
        rel_advisor_dict, cp_daily_total = load_static_tables(verbose=verbose)

    # Positions cube keys
    print("\nListing positions_cube partitions...")
    all_keys = _list_positions_cube_keys()
    keys_to_process = (
        [k for k in all_keys if _parse_date(k) > watermark]
        if incremental else all_keys
    )
    print(f"  Total: {len(all_keys):,}  To process: {len(keys_to_process):,}")

    if not keys_to_process:
        print("\n  No new partitions -- artifacts are current")
        return

    max_date_processed = None

    # Firm/advisor daily dollar accumulators (populated in both build paths)
    # {date_str: {equity: $, fixed_income: $, ..., total: $}}
    firm_daily_new: dict = {}
    # {advisor_name: {date_str: {equity: $, ..., total: $}}}
    advisor_daily_new: dict = {}

    if incremental:
        # --- INCREMENTAL: process new partitions in parallel, merge+write in parallel ---
        # For incremental (typically 1-10 dates), lower concurrency is fine
        inc_workers = min(PROCESS_WORKERS, max(len(keys_to_process), 1))
        print(f"\nProcessing {len(keys_to_process):,} new partition(s) ({inc_workers} workers)...")
        new_data = {}
        n_ok = n_skip = n_err = 0

        def _process_inc(idx_key):
            idx, key = idx_key
            date_str = _parse_date(key)
            try:
                result = process_date(key, date_str, prices_grouped,
                                      acct_rel_dict, ap_last_seen, verbose,
                                      insurance_account_ids=insurance_account_ids,
                                      insurance_gate_days=insurance_gate_days)
                return (idx, date_str, result, None)
            except Exception as e:
                return (idx, date_str, None, str(e))

        with ThreadPoolExecutor(max_workers=inc_workers) as pool:
            for idx, date_str, result, err in pool.map(_process_inc, enumerate(keys_to_process)):
                if verbose or idx % 50 == 0:
                    print(f"  [{idx+1}/{len(keys_to_process)}] {date_str}")
                if err:
                    print(f"  ERROR {date_str}: {err}")
                    n_err += 1
                    continue
                if not result:
                    n_skip += 1
                    continue
                for rel_id, data in result.items():
                    if rel_id not in new_data:
                        new_data[rel_id] = {}
                    new_data[rel_id][date_str] = data
                    # Accumulate firm/advisor daily dollar amounts
                    mv = data['total_mv']
                    if date_str not in firm_daily_new:
                        firm_daily_new[date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                        firm_daily_new[date_str]['total'] = 0.0
                    for _ac in _MIX_ASSET_CLASSES:
                        firm_daily_new[date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                    firm_daily_new[date_str]['total'] += mv
                    _adv = rel_advisor_dict.get(rel_id)
                    if _adv and _adv != 'Unresolved':
                        if _adv not in advisor_daily_new:
                            advisor_daily_new[_adv] = {}
                        if date_str not in advisor_daily_new[_adv]:
                            advisor_daily_new[_adv][date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                            advisor_daily_new[_adv][date_str]['total'] = 0.0
                        for _ac in _MIX_ASSET_CLASSES:
                            advisor_daily_new[_adv][date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                        advisor_daily_new[_adv][date_str]['total'] += mv
                max_date_processed = date_str
                n_ok += 1

        print(f"\n  {n_ok:,} dates OK, {n_skip:,} skipped, {n_err:,} errors")
        print(f"  {len(new_data):,} relationships with new data")

        if not new_data:
            print("  Nothing to write")
            return

        # Merge new dates into existing JSONs — parallel read+merge+write
        print(f"\nMerging and writing {len(new_data):,} relationship JSONs ({WRITE_WORKERS} workers)...")
        now_str = datetime.now(timezone.utc).isoformat() + 'Z'
        n_written = 0
        n_write_err = 0

        def _merge_and_write(item):
            rel_id, dated_entries = item
            existing = _read_relationship_json(rel_id)
            existing_mix  = {e['date']: e for e in (existing or {}).get('mix', [])}
            existing_conc = {e['date']: e for e in (existing or {}).get('concentration', [])}

            for ds, data in dated_entries.items():
                existing_mix[ds] = {'date': ds, **data['mix']}
                existing_conc[ds] = {'date': ds, 'holdings': data['conc']}

            mix_list  = sorted(existing_mix.values(),  key=lambda x: x['date'])
            conc_list = sorted(existing_conc.values(), key=lambda x: x['date'])
            data_as_of = mix_list[-1]['date'] if mix_list else watermark

            payload = {
                'generated_at':   now_str,
                'data_as_of':     data_as_of,
                'relationship_id': rel_id,
                'mix':             mix_list,
                'concentration':   conc_list,
            }
            _write_relationship_json(rel_id, payload, dry_run)
            return rel_id

        with ThreadPoolExecutor(max_workers=WRITE_WORKERS) as pool:
            futures = {pool.submit(_merge_and_write, item): item[0]
                       for item in new_data.items()}
            for future in as_completed(futures):
                try:
                    future.result()
                    n_written += 1
                except Exception as e:
                    n_write_err += 1
                    print(f"  WRITE ERROR {futures[future]}: {e}")

        print(f"  Written: {n_written:,} relationship JSONs ({n_write_err:,} errors)")

    else:
        # --- FULL BUILD: process all dates in parallel, write JSONs in parallel ---
        print(f"\nProcessing {len(keys_to_process):,} partitions (full build, {PROCESS_WORKERS} workers)...")
        all_data = {}  # {rel_id: {date_str: {mix, conc}}}
        n_ok = n_skip = n_err = 0
        lock = threading.Lock()

        def _process_one(idx_key):
            idx, key = idx_key
            date_str = _parse_date(key)
            try:
                result = process_date(key, date_str, prices_grouped,
                                      acct_rel_dict, ap_last_seen, verbose,
                                      insurance_account_ids=insurance_account_ids,
                                      insurance_gate_days=insurance_gate_days)
                return (idx, date_str, result, None)
            except Exception as e:
                return (idx, date_str, None, str(e))

        with ThreadPoolExecutor(max_workers=PROCESS_WORKERS) as pool:
            futures = pool.map(_process_one, enumerate(keys_to_process))
            for idx, date_str, result, err in futures:
                if (idx + 1) % 200 == 0 or idx == 0:
                    print(f"  [{idx+1}/{len(keys_to_process)}] {date_str}  "
                          f"(ok={n_ok} skip={n_skip} err={n_err})", flush=True)
                if err:
                    print(f"  ERROR {date_str}: {err}")
                    n_err += 1
                    continue
                if not result:
                    n_skip += 1
                    continue
                for rel_id, data in result.items():
                    if rel_id not in all_data:
                        all_data[rel_id] = {}
                    all_data[rel_id][date_str] = data
                    # Accumulate firm/advisor daily dollar amounts
                    mv = data['total_mv']
                    if date_str not in firm_daily_new:
                        firm_daily_new[date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                        firm_daily_new[date_str]['total'] = 0.0
                    for _ac in _MIX_ASSET_CLASSES:
                        firm_daily_new[date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                    firm_daily_new[date_str]['total'] += mv
                    _adv = rel_advisor_dict.get(rel_id)
                    if _adv and _adv != 'Unresolved':
                        if _adv not in advisor_daily_new:
                            advisor_daily_new[_adv] = {}
                        if date_str not in advisor_daily_new[_adv]:
                            advisor_daily_new[_adv][date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                            advisor_daily_new[_adv][date_str]['total'] = 0.0
                        for _ac in _MIX_ASSET_CLASSES:
                            advisor_daily_new[_adv][date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                        advisor_daily_new[_adv][date_str]['total'] += mv
                max_date_processed = date_str
                n_ok += 1

        print(f"\n  {n_ok:,} dates OK, {n_skip:,} skipped, {n_err:,} errors")
        print(f"  {len(all_data):,} relationships")

        if not all_data:
            print("  Nothing to write")
            return

        # Build payloads and write in parallel
        print(f"\nWriting {len(all_data):,} relationship JSONs ({WRITE_WORKERS} workers)...")
        now_str = datetime.now(timezone.utc).isoformat() + 'Z'
        n_written = 0
        n_write_err = 0

        def _build_and_write(item):
            rel_id, dated_entries = item
            mix_list  = []
            conc_list = []
            for ds in sorted(dated_entries.keys()):
                d = dated_entries[ds]
                mix_list.append({'date': ds, **d['mix']})
                conc_list.append({'date': ds, 'holdings': d['conc']})

            data_as_of = mix_list[-1]['date'] if mix_list else max_date_processed
            payload = {
                'generated_at':   now_str,
                'data_as_of':     data_as_of,
                'relationship_id': rel_id,
                'mix':             mix_list,
                'concentration':   conc_list,
            }
            _write_relationship_json(rel_id, payload, dry_run)
            return rel_id

        with ThreadPoolExecutor(max_workers=WRITE_WORKERS) as pool:
            futures = {pool.submit(_build_and_write, item): item[0]
                       for item in all_data.items()}
            for future in as_completed(futures):
                try:
                    future.result()
                    n_written += 1
                    if n_written % 500 == 0:
                        print(f"  Written: {n_written:,} / {len(all_data):,}", flush=True)
                except Exception as e:
                    n_write_err += 1
                    print(f"  WRITE ERROR {futures[future]}: {e}")

        del all_data
        gc.collect()
        print(f"  Written: {n_written:,} relationship JSONs ({n_write_err:,} errors)")

    # Watermark
    if max_date_processed:
        # Use max date across all S3 positions_cube files as watermark
        # (ensures we don't re-process files that had no usable data)
        watermark_date = _parse_date(all_keys[-1])
        _write_watermark(watermark_date, len(keys_to_process), dry_run)

    # -------------------------------------------------------------------------
    # Firm + Advisor mix views
    # -------------------------------------------------------------------------
    if firm_daily_new or advisor_daily_new:
        now_fa   = datetime.now(timezone.utc).isoformat() + 'Z'
        da_fa    = _parse_date(all_keys[-1]) if all_keys else (max_date_processed or '')

        # Firm: for incremental merge with existing daily, for full use new only
        if incremental:
            existing_firm = _load_firm_daily()
            existing_firm.update(firm_daily_new)
            firm_daily = existing_firm
        else:
            firm_daily = firm_daily_new

        if firm_daily:
            print("\nWriting firm mix views...")
            _write_firm_daily(firm_daily, dry_run)
            firm_views = compute_period_views(firm_daily, cp_daily_total=cp_daily_total)
            firm_payload = {
                'generated_at': now_fa,
                'data_as_of':   da_fa,
                'firm_id':      FIRM_ID,
                'views':        firm_views,
            }
            firm_body = json.dumps(firm_payload, separators=(',', ':')).encode('utf-8')
            if not dry_run:
                s3.put_object(Bucket=S3_BUCKET, Key=FIRM_MIX_KEY, Body=firm_body,
                              ContentType='application/json',
                              CacheControl='public, max-age=300, s-maxage=3600')
            print(f"  Firm mix views: "
                  f"{len(firm_views.get('quarterly', []))} quarters, "
                  f"{len(firm_views.get('monthly', []))} months, "
                  f"{len(firm_views.get('annually', []))} years")

        # Advisor: incremental merges per-advisor daily, full uses new only
        if advisor_daily_new:
            print(f"\nWriting advisor mix views ({len(advisor_daily_new)} advisors)...")

            def _write_one_advisor(adv_name: str) -> str:
                if incremental:
                    existing_adv = _load_advisor_daily(adv_name)
                    existing_adv.update(advisor_daily_new[adv_name])
                    adv_daily = existing_adv
                else:
                    adv_daily = advisor_daily_new[adv_name]
                _write_advisor_mix(adv_name, adv_name, da_fa, adv_daily, now_fa, dry_run)
                return adv_name

            n_adv_ok = n_adv_err = 0
            adv_pool_size = min(WRITE_WORKERS, max(len(advisor_daily_new), 1))
            with ThreadPoolExecutor(max_workers=adv_pool_size) as pool:
                adv_futures = {pool.submit(_write_one_advisor, adv): adv
                               for adv in advisor_daily_new}
                for future in as_completed(adv_futures):
                    try:
                        future.result()
                        n_adv_ok += 1
                    except Exception as exc:
                        n_adv_err += 1
                        print(f"  WARN advisor write {adv_futures[future]}: {exc}")
            print(f"  Advisor mix views: {n_adv_ok} written, {n_adv_err} errors")

    print("\n" + "=" * 70)
    print("DONE")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)


# =============================================================================
# Entry point
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Build client mix + concentration timeseries (per-relationship JSON)'
    )
    parser.add_argument('--upload',      action='store_true', help='Upload to S3')
    parser.add_argument('--incremental', action='store_true', help='Process only new dates')
    parser.add_argument('--dry-run',     action='store_true', help='Compute only, no write')
    parser.add_argument('--workers',     type=int, default=0, help='Override process worker count (0=use default)')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.workers > 0:
        global PROCESS_WORKERS, WRITE_WORKERS
        PROCESS_WORKERS = args.workers
        WRITE_WORKERS = args.workers * 2

    build(
        upload=args.upload,
        incremental=args.incremental,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


if __name__ == '__main__':
    main()
