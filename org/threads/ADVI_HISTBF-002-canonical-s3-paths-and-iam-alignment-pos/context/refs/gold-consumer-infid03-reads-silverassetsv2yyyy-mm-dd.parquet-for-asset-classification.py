#!/usr/bin/env python3
"""
INF_I_D03 -- Composition Artifacts Publisher (Inflection)

Builds per-asset-class top-holdings composition for firm and per-advisor views.
Mirrors BD D_03 adapted for INF (single custodian).

Asset classification (ADVI_INFLEC.DIAGFIX.010 — Orion-native, DS 2026-04-29):
  Source: silver/assets_v2/YYYY-MM-DD.parquet (built from the
  Orion REST endpoint /api/v1/Portfolio/Clients/{cid}/Assets/{date} — the same
  endpoint Orion's UI uses to render its asset-class panel). 100% coverage on
  product_category (broad: Equity / Bond / Money Market) and asset_class
  (Morningstar Category — "Large Blend", "Intermediate Core Bond", etc.).

  Bucket map: product_category -> {Equity: equity, Bond: fixed_income,
  Money Market: cash}. Alternatives are split out of the Equity bucket using
  asset_class keyword discriminator (Real Estate, *Allocation, Target-Date,
  Multi-Asset, Commodities, Hedged, Long-Short, Defined Outcome, etc.).

  Replaces the prior keyword regex + bd-securities DDB classifier — those are
  deleted entirely per Andrew 2026-04-29: "we shouldnt need to use our
  bd-securities or etf classifier or regex or any of that bullshit it should
  just be what orion uses here". No fallback paths.

Inputs:
  gold/holdings/{YYYY-MM-DD}.parquet           (I_B01 output, latest date)
  gold/views/rel_architect_lookup.parquet      (I_C07 output)

Outputs:
  platinum/firm/firm_composition.json
  platinum/advisors/{advisor_key}/composition.json

Output schema (canonical -- matches BD D_03 / 49F platinum):
  {
    "generated_at": "ISO",
    "data_as_of": "YYYY-MM-DD",
    "scope": {"firm_id": "inflection"},
    "total_market_value": float,
    "top_holdings": [{"key": str, "label": str, "asset_class": str,
                      "market_value": float, "pct": float}, ...],
    "other": {"market_value": float, "pct": float},
    "mix": [
      {"asset_class": str, "label": str, "market_value": float, "pct": float,
       "top_holdings": [...], "other": {"market_value": float, "pct": float}}
    ],
    "unclassified": {"count": int, "market_value": float}
  }

Usage:
  python3 INF_I_D03.composition_artifacts.py --upload
  python3 INF_I_D03.composition_artifacts.py --dry-run

Author: 0.4.0_DS_ClientPlatform
Project: ADVI_INFLEC
Date: 2026-04-22
"""

from __future__ import annotations
import argparse
import datetime
import json
import os
import re
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

import boto3
import pandas as pd

S3_BUCKET = 'opal-data-inf'
FIRM_ID = 'inflection'

# OUTPUT_PREFIX honor for INFSHIP.B3 inf-gold-qa-runner: PROD writes to platinum/,
# QA dispatch sets OUTPUT_PREFIX=qa/ to redirect into the QA scope (IAM DENY on
# platinum/* enforces this from the runner side as defense-in-depth).
OUTPUT_PREFIX = os.environ.get('OUTPUT_PREFIX', 'platinum/').rstrip('/') + '/'

# GOLD_ARTIFACTS_PREFIX honor for INFSHIP.B3-DEP-2 (AE 0.6.1~B option-b ruling
# 20260428T144900Z, CTO/COO ratified): the gold/artifacts/firm_mix_views.json
# side-write WOULD contaminate PROD if QA runs unmodified (gold/artifacts/* is
# outside the platinum/* IAM DENY scope). QA dispatch sets
# GOLD_ARTIFACTS_PREFIX=qa/gold-artifacts/ to fully isolate side-writes.
# INF_D_04 reads this same file (`FIRM_MIX_VIEWS_KEY = 'gold/artifacts/firm_mix_views.json'`)
# at a LITERAL path so QA reads PROD's real upstream artifact (asymmetric design
# load-bearing for cross-publisher fan-in; CTO 14:58Z ratified). DS~B
# precedent: 50d133c8 (INF_I_D04 GOLD_ARTIFACTS_HEADER_METRICS_KEY).
GOLD_ARTIFACTS_PREFIX = os.environ.get('GOLD_ARTIFACTS_PREFIX', 'gold/artifacts/').rstrip('/') + '/'

HOLDINGS_PREFIX = 'gold/canonical/'
HOLDINGS_FILENAME_PREFIX = 'holdings_'
REL_ARCHITECT_KEY = 'gold/views/rel_architect_lookup.parquet'
ACCOUNT_TEAM_KEY = 'gold/views/account_team.parquet'
FIRM_COMPOSITION_KEY = f'{GOLD_ARTIFACTS_PREFIX}firm_mix_views.json'
FIRM_COMPOSITION_PLATINUM_KEY = f'{OUTPUT_PREFIX}firm/firm_composition.json'
ADVISOR_COMPOSITION_KEY_TPL = f'{OUTPUT_PREFIX}advisors/{{advisor_key}}/composition.json'

SILVER_API_ASSETS_PREFIX = 'silver/api_dims/assets/'
SILVER_API_ASSETS_V2_PREFIX = 'silver/assets_v2/'

CLASSIFICATION_METHOD = 'orion_native_v1'
CLASSIFICATION_CAVEATS = (
    'product_category + asset_class sourced from Orion REST endpoint '
    '/api/v1/Portfolio/Clients/{cid}/Assets/{date} via silver/api_dims/assets_v2. '
    'Same source the Orion UI uses to render its asset-class panel.'
)

# Placeholder advisor_keys (firm-level routing buckets, not individual advisors).
# Andrew direction 2026-04-28 (via DE 0.4.0_DE_ClientPlatform 13:33Z): IWM
# (`inflection_wealth_management`) is now treated as a first-class drillable
# advisor entry — same as Peter Lee + Patrick Scanlan — with its own
# composition.json drilldown page. Removed from skip set; new_accounts_rep
# remains a placeholder (genuine routing bucket, no drilldown).
_PLACEHOLDER_KEYS = {'new_accounts_rep'}

TOP_N = 9
WRITE_WORKERS = 32

_ASSET_CLASS_LABELS = {
    'equity':       'Equities',
    'fixed_income': 'Fixed Income',
    'alternatives': 'Alternatives',
    'cash':         'Cash',
    'other':        'Other',
}

# Asset_class keyword discriminator for splitting alternatives out of Orion's
# 'Equity' product_category bucket. Orion's product_category has 3 native values
# (Equity / Bond / Money Market); this list pulls REIT / allocation funds / target-
# date / commodities / hedge / etc. into our alternatives bucket where our 4-bucket
# schema needs them. Match is case-insensitive substring against asset_class
# (Morningstar Category name).
_ALTERNATIVES_CATEGORY_KEYWORDS = (
    'real estate', 'allocation', 'target-date', 'multi-asset', 'commodities',
    'commodity', 'hedged', 'long-short', 'market neutral', 'macro trading',
    'multistrategy', 'systematic trend', 'event driven', 'defined outcome',
    'derivative income', 'alternative', 'digital asset', 'energy limited',
    'natural resources', 'trading--', 'infrastructure', 'precious metals',
)

s3 = boto3.client('s3', region_name='us-east-1')


def log(msg):
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f'[{ts}] {msg}', flush=True)


def _now_str():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def _read_s3(key):
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return pd.read_parquet(BytesIO(resp['Body'].read()))
    except Exception as e:
        if 'NoSuchKey' in str(e):
            return None
        raise


def _write_json_s3(obj, key):
    body = json.dumps(obj, default=str, separators=(',', ':'))
    s3.put_object(
        Bucket=S3_BUCKET, Key=key,
        Body=body.encode('utf-8'), ServerSideEncryption='AES256',
        ContentType='application/json',
    )
    return len(body)


def _bucket_from_orion(product_category, asset_class) -> str:
    """Map (product_category, asset_class) from Orion to our 4-bucket schema.

    product_category native values: Equity / Bond / Money Market.
    Alternatives are split out of Equity using asset_class keyword discriminator
    (see _ALTERNATIVES_CATEGORY_KEYWORDS). Returns '' for null product_category
    (caller treats as unclassified — empty string lands in the existing
    unclassified bucket per _build_composition's `df['asset_class'] == ''` filter).
    """
    pc = str(product_category).strip() if pd.notna(product_category) else ''
    ac = str(asset_class).strip().lower() if pd.notna(asset_class) else ''
    if pc == 'Money Market':
        return 'cash'
    if pc == 'Bond':
        return 'fixed_income'
    if pc == 'Equity':
        if any(kw in ac for kw in _ALTERNATIVES_CATEGORY_KEYWORDS):
            return 'alternatives'
        return 'equity'
    return ''


def _load_assets_v2_classifier() -> pd.DataFrame:
    """Load latest silver/api_dims/assets_v2 partition. Returns DataFrame with
    join-ready columns: account_id (string), ticker (uppercase string),
    product_category (string), mstar_asset_class (string — Morningstar Category
    from Orion). Renamed asset_class -> mstar_asset_class to avoid collision
    with the bucket-name asset_class column used downstream.
    """
    latest_key = _latest_silver_partition(SILVER_API_ASSETS_V2_PREFIX)
    if latest_key is None:
        raise RuntimeError(
            f'No silver/api_dims/assets_v2 partitions found at {SILVER_API_ASSETS_V2_PREFIX}. '
            'Run pull_inflection_assets_v2.py + convert_assets_v2_to_silver.py first.'
        )
    df = _read_s3(latest_key)
    if df is None or df.empty:
        raise RuntimeError(f'silver assets_v2 partition empty: {latest_key}')
    log(f'Loaded silver assets_v2 classifier: {len(df):,} rows from {latest_key}')

    out = df[['account_id', 'ticker', 'product_category', 'asset_class']].copy()
    out['account_id'] = out['account_id'].astype('string').str.strip()
    out['ticker'] = out['ticker'].astype('string').str.strip().str.upper()
    out = out.rename(columns={'asset_class': 'mstar_asset_class'})
    return out


def _holding_key(ticker, asset_name):
    t = str(ticker).strip() if pd.notna(ticker) else ''
    if t and t.upper() not in ('NAN', 'NONE', ''):
        return t.upper()
    name = str(asset_name).strip() if pd.notna(asset_name) else ''
    return re.sub(r'\s+', '_', name.lower())[:40] or 'unknown'


def _holding_label(ticker, asset_name):
    t = str(ticker).strip() if pd.notna(ticker) else ''
    if t and t.upper() not in ('NAN', 'NONE', ''):
        return t.upper()
    name = str(asset_name).strip() if pd.notna(asset_name) else ''
    return name[:30] or 'Unknown'


def _latest_silver_partition(prefix):
    """Return the latest S3 key under prefix ending in .parquet (flat or Hive layout)."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            k = obj['Key']
            if k.endswith('.parquet'):
                keys.append(k)
    if not keys:
        return None
    keys.sort()
    return keys[-1]


def load_assets_dim():
    """Load latest silver/api_dims/assets/snapshot_date=*/data.parquet (DS~D L4 INFSHIP).

    Returns (df, snapshot_date_str). df is empty + snapshot_date_str is None if absent
    (graceful degradation -- I_D03 still publishes top_holdings/mix without the
    cross-validation diagnostic).
    """
    try:
        latest_key = _latest_silver_partition(SILVER_API_ASSETS_PREFIX)
        if latest_key is None:
            log('WARN: no silver/api_dims/assets/ partitions found -- assets cross-val diagnostic will be omitted')
            return pd.DataFrame(), None
        snap = latest_key.split('snapshot_date=')[-1].split('/')[0]
        df = _read_s3(latest_key)
        log(f'Assets dim: {len(df):,} rows from {latest_key} (snapshot_date={snap})')
        return df, snap
    except Exception as e:
        log(f'WARN: silver/api_dims/assets/ load failed: {e} -- diagnostic omitted')
        return pd.DataFrame(), None


def _build_silver_assets_diagnostic(holdings, assets, holdings_data_as_of, assets_snapshot_date):
    """Cross-validation diagnostic comparing gold/canonical/holdings vs silver/api_dims/assets.

    Both are per-account x per-asset positions; expected to align (modulo snapshot date drift).
    Emits operational signals so ops can spot:
      - account coverage divergence (accts in one source but not other)
      - position count divergence
      - market value drift (per-position deltas; firm-level mv totals)
      - snapshot staleness (gold is live, silver may lag depending on DS~D + AE L5 cadence)

    Returns dict suitable for _meta.silver_assets_diagnostic key. Empty dict if either
    input is empty (no diagnostic surfaced).

    Per DS~A outlier policy 04:21Z: emit diagnostic only; no trim/winsorize at publisher.
    """
    if holdings is None or holdings.empty or assets is None or assets.empty:
        return {}

    h_cols_needed = {'account_id', 'ticker', 'market_value'}
    a_cols_needed = {'account_id', 'asset_ticker', 'position_mv'}
    if not h_cols_needed.issubset(set(holdings.columns)):
        return {}
    if not a_cols_needed.issubset(set(assets.columns)):
        return {}

    h = holdings[['account_id', 'ticker', 'market_value']].copy()
    h['account_id'] = h['account_id'].astype(str)
    h['ticker'] = h['ticker'].astype(str).str.upper()
    h_keyed = h.groupby(['account_id', 'ticker'], as_index=False)['market_value'].sum()
    h_keyed = h_keyed.rename(columns={'market_value': 'gold_mv'})

    a = assets[['account_id', 'asset_ticker', 'position_mv']].copy()
    a['account_id'] = a['account_id'].astype(str)
    a['ticker'] = a['asset_ticker'].astype(str).str.upper()
    a_keyed = a.groupby(['account_id', 'ticker'], as_index=False)['position_mv'].sum()
    a_keyed = a_keyed.rename(columns={'position_mv': 'silver_mv'})

    merged = h_keyed.merge(a_keyed, on=['account_id', 'ticker'], how='outer', indicator=True)

    in_both = merged[merged['_merge'] == 'both'].copy()
    gold_only = merged[merged['_merge'] == 'left_only'].copy()
    silver_only = merged[merged['_merge'] == 'right_only'].copy()

    in_both['gold_mv'] = in_both['gold_mv'].fillna(0.0)
    in_both['silver_mv'] = in_both['silver_mv'].fillna(0.0)
    in_both['mv_delta'] = in_both['gold_mv'] - in_both['silver_mv']
    in_both['mv_delta_abs'] = in_both['mv_delta'].abs()
    in_both['mv_delta_pct'] = in_both.apply(
        lambda r: (r['mv_delta'] / r['gold_mv'] * 100) if r['gold_mv'] else 0.0, axis=1
    )

    h_acct_set = set(h['account_id'].unique())
    a_acct_set = set(a['account_id'].unique())

    try:
        staleness_days = (pd.to_datetime(holdings_data_as_of) -
                          pd.to_datetime(assets_snapshot_date)).days if (holdings_data_as_of and assets_snapshot_date) else None
    except Exception:
        staleness_days = None

    return {
        'gold_source': f'gold/canonical/holdings_{holdings_data_as_of}.parquet',
        'silver_source': f'silver/api_dims/assets/snapshot_date={assets_snapshot_date}/data.parquet',
        'staleness_days': staleness_days,
        'staleness_note': 'staleness_days = gold_data_as_of - silver_snapshot_date; positive = silver is older',
        'account_coverage': {
            'gold_accts': len(h_acct_set),
            'silver_accts': len(a_acct_set),
            'in_both_accts': len(h_acct_set & a_acct_set),
            'gold_only_accts': len(h_acct_set - a_acct_set),
            'silver_only_accts': len(a_acct_set - h_acct_set),
        },
        'position_coverage': {
            'gold_positions': int(len(h_keyed)),
            'silver_positions': int(len(a_keyed)),
            'in_both_positions': int(len(in_both)),
            'gold_only_positions': int(len(gold_only)),
            'silver_only_positions': int(len(silver_only)),
        },
        'mv_delta': {
            'gold_total_mv': round(float(h_keyed['gold_mv'].sum()), 2),
            'silver_total_mv': round(float(a_keyed['silver_mv'].sum()), 2),
            'firm_level_delta': round(float(h_keyed['gold_mv'].sum() - a_keyed['silver_mv'].sum()), 2),
            'firm_level_delta_pct': round(
                (float(h_keyed['gold_mv'].sum() - a_keyed['silver_mv'].sum()) /
                 float(h_keyed['gold_mv'].sum()) * 100) if float(h_keyed['gold_mv'].sum()) else 0.0, 4
            ),
            'in_both_delta_p50_abs': round(float(in_both['mv_delta_abs'].quantile(0.50)), 2) if len(in_both) else None,
            'in_both_delta_p95_abs': round(float(in_both['mv_delta_abs'].quantile(0.95)), 2) if len(in_both) else None,
            'in_both_delta_max_abs': round(float(in_both['mv_delta_abs'].max()), 2) if len(in_both) else None,
        },
        'policy': 'No trim/winsorize at publisher per DS~A 2026-04-28. Cross-val diagnostic only; behavior unchanged. Operations watches firm_level_delta_pct + position_coverage divergence; expected to be >0 when staleness_days > 0 (silver lags gold).',
    }


def _build_composition(df, scope, data_as_of, assets_dim=None, assets_snapshot_date=None):
    """
    Build canonical composition artifact from a holdings DataFrame.
    df must have: ticker, asset_name, market_value, asset_class columns.
    """
    if df.empty:
        return None

    total_mv = float(df['market_value'].sum())
    if total_mv <= 0:
        return None

    # Build (key, label, asset_class) grain
    df = df.copy()
    df['_key'] = df.apply(lambda r: _holding_key(r['ticker'], r.get('asset_name', '')), axis=1)
    df['_label'] = df.apply(lambda r: _holding_label(r['ticker'], r.get('asset_name', '')), axis=1)

    holding_agg = (
        df.groupby(['_key', '_label', 'asset_class'], sort=False)['market_value']
        .sum()
        .reset_index()
        .sort_values('market_value', ascending=False)
    )

    mix_out = []
    for asset_class in _ASSET_CLASS_LABELS:
        cls_rows = holding_agg[holding_agg['asset_class'] == asset_class]
        if cls_rows.empty:
            continue
        class_mv = float(cls_rows['market_value'].sum())
        if class_mv <= 0:
            continue
        class_pct = round(class_mv / total_mv, 6)
        top_n = cls_rows.head(TOP_N)
        top_holdings_cls = [
            {
                'key':          row['_key'],
                'label':        row['_label'],
                'asset_class':  asset_class,
                'market_value': round(float(row['market_value']), 2),
                'pct':          round(float(row['market_value']) / class_mv, 6),
            }
            for _, row in top_n.iterrows()
        ]
        top_n_mv = float(top_n['market_value'].sum())
        class_other_mv = class_mv - top_n_mv
        mix_out.append({
            'asset_class':  asset_class,
            'label':        _ASSET_CLASS_LABELS[asset_class],
            'market_value': round(class_mv, 2),
            'pct':          class_pct,
            'top_holdings': top_holdings_cls,
            'other': {
                'market_value': round(class_other_mv, 2),
                'pct':          round(class_other_mv / class_mv, 6) if class_mv > 0 else 0.0,
            },
        })

    mix_out.sort(key=lambda x: x['market_value'], reverse=True)

    global_top_n = holding_agg.head(TOP_N)
    global_top_holdings = [
        {
            'key':          row['_key'],
            'label':        row['_label'],
            'asset_class':  row['asset_class'],
            'market_value': round(float(row['market_value']), 2),
            'pct':          round(float(row['market_value']) / total_mv, 6),
        }
        for _, row in global_top_n.iterrows()
    ]
    global_top_mv = float(global_top_n['market_value'].sum())
    global_other_mv = total_mv - global_top_mv

    unclassified = df[df['asset_class'].isna() | (df['asset_class'] == '')]
    unclassified_count = int(unclassified['_key'].nunique())
    unclassified_mv = float(unclassified['market_value'].sum())

    out = {
        'generated_at':           _now_str(),
        'data_as_of':             data_as_of,
        'classification_method':  CLASSIFICATION_METHOD,
        'classification_caveats': CLASSIFICATION_CAVEATS,
        'scope':                  scope,
        'total_market_value':     round(total_mv, 2),
        'top_holdings':           global_top_holdings,
        'other': {
            'market_value': round(global_other_mv, 2),
            'pct':          round(global_other_mv / total_mv, 6) if total_mv > 0 else 0.0,
        },
        'mix':          mix_out,
        'unclassified': {
            'count':        unclassified_count,
            'market_value': round(unclassified_mv, 2),
        },
    }

    if assets_dim is not None and not assets_dim.empty:
        diagnostic = _build_silver_assets_diagnostic(df, assets_dim, data_as_of, assets_snapshot_date)
        if diagnostic:
            out['_meta'] = {'silver_assets_diagnostic': diagnostic}

    return out


def main():
    parser = argparse.ArgumentParser(description='INF_I_D03: Composition Artifacts (Inflection)')
    parser.add_argument('--upload', action='store_true', help='Write to S3')
    parser.add_argument('--dry-run', action='store_true', help='Compute only, no write')
    args = parser.parse_args()
    dry_run = args.dry_run or not args.upload

    log('=' * 70)
    log('INF_I_D03: COMPOSITION ARTIFACTS (Inflection)')
    log(f'Mode: {"DRY RUN" if dry_run else "UPLOAD"}')
    log('=' * 70)

    # Find latest canonical holdings partition. Source = gold/canonical/holdings_*.parquet
    # (INF_B_00 output) which already carries advisor_key + rep_bucket per account and covers
    # all 2,755 firm accounts. Prior source (gold/holdings/) only contained the firm-level
    # placeholder subset and produced 0 individual-advisor compositions.
    paginator = s3.get_paginator('list_objects_v2')
    holdings_keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=HOLDINGS_PREFIX)
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
        and obj['Key'].split('/')[-1].startswith(HOLDINGS_FILENAME_PREFIX)
    ])

    if not holdings_keys:
        log(f'WARN: no canonical holdings partitions found in {HOLDINGS_PREFIX} -- skipping composition')
        log('  INF_B_00 (canonical_holdings) must run first')
        log('OK: INF_I_D03 exiting with 0 (no-op -- canonical holdings not yet available)')
        return 0

    latest_key = holdings_keys[-1]
    data_as_of = (latest_key.split('/')[-1]
                  .replace(HOLDINGS_FILENAME_PREFIX, '')
                  .replace('.parquet', ''))
    log(f'Loading canonical holdings: {latest_key}')

    lots = _read_s3(latest_key)
    if lots is None or lots.empty:
        log('WARN: holdings parquet is empty -- skipping')
        return 0

    # NaT guard on date
    if 'date' in lots.columns:
        lots['date'] = pd.to_datetime(lots['date'], errors='coerce')
        lots = lots.dropna(subset=['date'])

    log(f'Holdings: {len(lots):,} rows, ${lots["market_value"].sum():,.0f} total MV')

    # Load DS~D L4 silver/api_dims/assets/ for cross-validation diagnostic emission.
    # Graceful degradation: if absent, _meta block omitted; canonical top_holdings/mix unchanged.
    assets_dim, assets_snapshot_date = load_assets_dim()

    # Need account_id and ticker at minimum
    if 'ticker' not in lots.columns or 'market_value' not in lots.columns:
        log('ERROR: holdings missing required columns (ticker, market_value)')
        return 1

    # Ensure asset_name exists. canonical/holdings_* uses 'product_name'.
    if 'asset_name' not in lots.columns:
        if 'product_name' in lots.columns:
            lots['asset_name'] = lots['product_name']
        else:
            lots['asset_name'] = lots['ticker']

    # Classify assets via Orion-native silver/api_dims/assets_v2 lookup
    # (DIAGFIX.010 — replaces keyword regex + bd-securities DDB classifier).
    # Join keys: (account_id, ticker) — both string, ticker uppercased.
    log('Classifying assets via Orion-native silver/api_dims/assets_v2...')
    classifier = _load_assets_v2_classifier()
    lots['_join_account_id'] = lots['account_id'].astype('string').str.strip()
    lots['_join_ticker'] = lots['ticker'].astype('string').str.strip().str.upper()
    classifier = classifier.rename(
        columns={'account_id': '_join_account_id', 'ticker': '_join_ticker'}
    )
    lots = lots.merge(classifier, on=['_join_account_id', '_join_ticker'], how='left')
    lots['asset_class'] = [
        _bucket_from_orion(pc, mac)
        for pc, mac in zip(lots['product_category'], lots['mstar_asset_class'])
    ]
    unmatched_mask = lots['product_category'].isna() | (lots['product_category'].astype(str) == '')
    unmatched_mv = float(lots.loc[unmatched_mask, 'market_value'].fillna(0).sum())
    log(f'Classification: {dict(lots["asset_class"].value_counts(dropna=False))}')
    log(f'Unmatched on (account_id, ticker): {int(unmatched_mask.sum()):,} rows / ${unmatched_mv:,.0f} mv')
    lots = lots.drop(columns=['_join_account_id', '_join_ticker', 'product_category', 'mstar_asset_class'])

    # Resolve account -> advisor_key.
    # DIAGFIX.011: override the baked-in advisor_key from holdings parquet using the
    # current silver/api_dims/accounts_v2 dim. accounts_v2 now carries the servicing
    # rep (Brandenburg / Lee / Scanlan / IWM-firm) per DIAGFIX.011 Phase 3 augment.
    # Without this override, INF_I_D03 trusts the upstream-baked advisor_key from
    # whichever build of INF_B_00 produced the canonical holdings parquet — so until
    # INF_B_00 re-runs, Brandenburg's accounts still show as 'inflection_wealth_management'.
    accounts_v2_key = _latest_silver_partition('silver/api_dims/accounts_v2/')
    accounts_v2_df = _read_s3(accounts_v2_key) if accounts_v2_key else None
    overridden_via_accounts_v2 = False
    if (accounts_v2_df is not None and not accounts_v2_df.empty
            and 'account_id' in accounts_v2_df.columns
            and 'representative_name' in accounts_v2_df.columns
            and 'account_id' in lots.columns):
        rep_lookup = accounts_v2_df[['account_id', 'representative_name']].copy()
        rep_lookup['account_id'] = rep_lookup['account_id'].astype(str).str.strip()
        rep_lookup = rep_lookup.drop_duplicates(subset=['account_id'])
        rep_lookup['_advisor_key_override'] = (
            rep_lookup['representative_name']
            .fillna('')
            .astype(str)
            .str.lower()
            .str.replace(r'[^a-z0-9_]+', '_', regex=True)
            .str.strip('_')
            .str.slice(0, 60)
        )
        rep_lookup = rep_lookup[rep_lookup['_advisor_key_override'] != '']
        rep_lookup = rep_lookup[['account_id', '_advisor_key_override']]
        lots['account_id'] = lots['account_id'].astype(str).str.strip()
        before_unique = lots['advisor_key'].nunique() if 'advisor_key' in lots.columns else 0
        lots = lots.merge(rep_lookup, on='account_id', how='left')
        if 'advisor_key' in lots.columns:
            lots['advisor_key'] = lots['_advisor_key_override'].combine_first(lots['advisor_key'])
        else:
            lots['advisor_key'] = lots['_advisor_key_override']
        lots = lots.drop(columns=['_advisor_key_override'])
        after_unique = lots['advisor_key'].nunique()
        log(f'advisor_key override via accounts_v2: {before_unique} -> {after_unique} unique advisors')
        overridden_via_accounts_v2 = True

    if 'advisor_key' in lots.columns:
        log(f'advisor_key on lots: {lots["advisor_key"].nunique():,} advisor_keys '
            f'(overridden via accounts_v2={overridden_via_accounts_v2})')
        lots['architect'] = lots['advisor_key'].fillna('unassigned')
    else:
        account_team = _read_s3(ACCOUNT_TEAM_KEY)
        if account_team is not None and not account_team.empty and 'advisor_key' in account_team.columns:
            log(f'account_team: {account_team["advisor_key"].nunique():,} advisor_keys (merging on account_id)')
            lots = lots.merge(
                account_team[['account_id', 'advisor_key']],
                on='account_id', how='left',
            )
            lots['architect'] = lots['advisor_key'].fillna('unassigned')
        else:
            log('WARN: account_team not available -- attempting rel_architect_lookup fallback')
            rel_lookup = _read_s3(REL_ARCHITECT_KEY)
            if rel_lookup is None:
                rel_lookup = pd.DataFrame(columns=['relationship_id', 'architect'])
            has_hh_in_lots = 'household_id' in lots.columns
            has_rel_lookup = not rel_lookup.empty and 'relationship_id' in rel_lookup.columns
            if has_hh_in_lots and has_rel_lookup:
                lots = lots.merge(
                    rel_lookup[['relationship_id', 'architect']].rename(
                        columns={'relationship_id': 'household_id'}),
                    on='household_id', how='left',
                )
                lots['architect'] = lots['architect'].fillna('unassigned')
            else:
                lots['architect'] = 'unassigned'

    # Firm composition
    log('Building firm composition...')
    firm_comp = _build_composition(
        lots,
        scope={'firm_id': FIRM_ID},
        data_as_of=data_as_of,
        assets_dim=assets_dim,
        assets_snapshot_date=assets_snapshot_date,
    )
    if firm_comp is None:
        log('WARN: firm composition is empty')
    elif not dry_run:
        _write_json_s3(firm_comp, FIRM_COMPOSITION_KEY)
        log(f'Wrote {FIRM_COMPOSITION_KEY}')
        _write_json_s3(firm_comp, FIRM_COMPOSITION_PLATINUM_KEY)
        log(f'Wrote {FIRM_COMPOSITION_PLATINUM_KEY}')
    else:
        log(f'DRY RUN: would write {FIRM_COMPOSITION_KEY} + {FIRM_COMPOSITION_PLATINUM_KEY}')

    # Per-advisor composition. Exclude blanks/unassigned and firm-level placeholder
    # routing buckets (which are not individual advisors).
    advisors = [
        a for a in lots['architect'].dropna().unique()
        if str(a).strip().lower() not in ('', 'nan', 'none', 'unassigned')
        and a not in _PLACEHOLDER_KEYS
    ]
    log(f'Building composition for {len(advisors)} advisors...')

    def _advisor_key_slug(name):
        return re.sub(r'[^a-z0-9_]+', '_', str(name).lower().strip()).strip('_')[:60] or 'unknown'

    written = 0
    skipped = 0
    advisor_items = []
    for adv_name in advisors:
        adv_lots = lots[lots['architect'] == adv_name]
        adv_key = _advisor_key_slug(adv_name)
        comp = _build_composition(
            adv_lots,
            scope={'advisor_id': adv_key, 'firm_id': FIRM_ID},
            data_as_of=data_as_of,
            assets_dim=assets_dim,
            assets_snapshot_date=assets_snapshot_date,
        )
        if comp is None:
            skipped += 1
            continue
        advisor_items.append((comp, ADVISOR_COMPOSITION_KEY_TPL.format(advisor_key=adv_key)))

    if not dry_run and advisor_items:
        def _write_one(item):
            comp, key = item
            _write_json_s3(comp, key)
            return key

        with ThreadPoolExecutor(max_workers=min(len(advisor_items), WRITE_WORKERS)) as pool:
            futures = {pool.submit(_write_one, item): item for item in advisor_items}
            for fut in as_completed(futures):
                try:
                    fut.result()
                    written += 1
                except Exception as e:
                    log(f'WARN: advisor composition write failed: {e}')
        log(f'Wrote {written} advisor composition files, {skipped} skipped (empty book)')
    else:
        written = len(advisor_items)
        log(f'DRY RUN: would write {written} advisor composition files, {skipped} skipped')

    log('')
    log('=' * 70)
    log(f'Firm composition: {"written" if firm_comp and not dry_run else "dry-run"}')
    log(f'Advisor composition: {written} written, {skipped} skipped')
    log(f'Mode: {"DRY RUN" if dry_run else "UPLOADED"}')
    log('OK: INF_I_D03.composition_artifacts.py complete')
    log('=' * 70)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        print(f'[{ts}] ERROR: INF_I_D03 failed: {exc}', flush=True)
        traceback.print_exc()
        sys.exit(1)
