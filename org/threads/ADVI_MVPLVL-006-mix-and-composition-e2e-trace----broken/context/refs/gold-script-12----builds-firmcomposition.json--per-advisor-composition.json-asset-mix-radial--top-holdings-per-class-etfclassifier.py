#!/usr/bin/env python3
"""
Build Composition Artifacts — per-class top holdings for firm (N1) and advisors (L2)

Produces portal-ready JSON at:
    s3://opal-data-bd/gold/views/firm_composition.json
    s3://opal-data-bd/gold/advisors/{advisor_id}/composition.json

Serves GET /api/scoped/partners/books/firm/all/composition
and    GET /api/scoped/partners/books/advisor/{id}/composition
via opal-partners-data (pure S3 proxy -- zero Lambda compute).

Why pre-computed:
    Firm and advisor books contain thousands of unique positions.
    Sending all holdings over the wire is prohibitive. Script 12 runs
    on EC2 where full parquet access is available, collapses each book
    to a small per-class top-9 JSON artifact, and the Lambda serves it
    as a static file with Cache-Control: no-store.

Inputs (must exist in S3 before running):
    gold/holdings_lots/YYYY-MM-DD.parquet   -- from 03_build_holdings_lots.py
    gold/views/rel_architect_lookup.parquet -- from 08b_build_architect_attribution.py
    gold/client_dimension.parquet           -- fallback for architect assignment

Run sequence (run_gold_layer.sh):
    08b (rel_architect_lookup written) --> 12 (this script) --> 06b

Output schema (canonical per ADVI_BKSCMP_PRD.md §3):
    {
      "data_as_of":          "YYYY-MM-DD",
      "generated_at":        "ISO8601Z",
      "scope":               {"firm_id": "49financial"},
      "total_market_value":  float,
      "top_holdings":        [ConcentrationItem x9],   # global, pct = mv / total_mv
      "other":               {"market_value": float, "pct": float},
      "mix": [
        {
          "asset_class": str, "label": str,
          "market_value": float, "pct": float,          # pct = class_mv / total_mv
          "top_holdings": [ConcentrationItem x9],        # pct = holding_mv / class_mv
          "other": {"market_value": float, "pct": float} # pct = class_other_mv / class_mv
        }, ...
      ],
      "unclassified": {"count": int, "market_value": float}
    }

Usage:
    python 12_build_composition_artifacts.py              # dry run (no upload)
    python 12_build_composition_artifacts.py --upload     # write to S3
    python 12_build_composition_artifacts.py --dry-run    # compute only, no write

Author: 0.4.0_DS_ClientPlatform
Date: 2026-03-19
"""

import argparse
import gc
import json
import re
import sys
from datetime import datetime, timezone
from io import BytesIO

import boto3
import pandas as pd

from lib.etf_classifier import ETFClassifier

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BUCKET      = 'opal-data-bd'
FIRM_ID     = '49financial'
TOP_N       = 9   # top holdings per asset class + global

s3 = boto3.client('s3', region_name='us-east-1')

_ASSET_CLASS_LABELS = {
    'equity':       'Equities',
    'fixed_income': 'Fixed Income',
    'alternatives': 'Alternatives',
    'cash':         'Cash',
    'other':        'Other',
}

# ---------------------------------------------------------------------------
# Classification -- delegates to DynamoDB-backed ETFClassifier (lib.etf_classifier)
# Same classifier that 06b uses. Keeps cash/other distinction that ETFClassifier
# does not make (it returns '' for both cash-like and truly unknown securities).
# ---------------------------------------------------------------------------


def classify_series(ticker_series: pd.Series, name_series: pd.Series) -> pd.Series:
    """Classify each holding via ETFClassifier, with cash/other post-processing."""
    classifier = ETFClassifier.instance()

    def _classify(ticker, asset_name):
        result = classifier.classify(ticker, asset_name)
        if not result:
            # ETFClassifier returns '' for cash-like and unknown
            name = str(asset_name or '').upper()
            if any(kw in name for kw in ('CASH', 'SWEEP', 'MONEY MARKET', 'MMKT')):
                return 'cash'
            return 'other'
        return result  # 'equity' | 'fixed_income' | 'alternatives'

    return pd.Series(
        [_classify(t, n) for t, n in zip(
            ticker_series.fillna(''), name_series.fillna('')
        )],
        index=ticker_series.index,
        dtype='object'
    )


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _read_parquet(key: str, columns: list = None) -> pd.DataFrame:
    resp = s3.get_object(Bucket=BUCKET, Key=key)
    kwargs = {'columns': columns} if columns else {}
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _find_latest_holdings_lots() -> str | None:
    """Return S3 key of the most recent non-backfill holdings_lots snapshot."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=BUCKET, Prefix='gold/holdings_lots/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
        and 'backfill' not in obj['Key'].rsplit('/', 1)[-1]
    ])
    return keys[-1] if keys else None


def _write_json(data: dict, key: str, upload: bool) -> None:
    body = json.dumps(data, default=str, separators=(',', ':'))
    if upload:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=body.encode('utf-8'),
            ContentType='application/json',
            CacheControl='no-store, no-cache, must-revalidate',
        )
        print(f"  OK: s3://{BUCKET}/{key} ({len(body):,} bytes)")
    else:
        print(f"  [DRY RUN] Would write {key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# advisor_id sanitization
# Must match ClientsTab.tsx:383 exactly:
#   name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
# ---------------------------------------------------------------------------

def _advisor_id(name: str) -> str:
    return re.sub(r'[^a-z0-9_]+', '_', str(name).lower().strip()).strip('_')[:60] or 'unknown'


# ---------------------------------------------------------------------------
# Holding key / label helpers (PRD §3)
# ---------------------------------------------------------------------------

def _holding_key(ticker, asset_name) -> str:
    """Stable key for deduplication and frontend lookup."""
    t = str(ticker).strip() if pd.notna(ticker) else ''
    if t and t.upper() not in ('NAN', 'NONE', ''):
        return t.upper()
    name = str(asset_name).strip() if pd.notna(asset_name) else ''
    return re.sub(r'\s+', '_', name.lower())[:40] or 'unknown'


def _holding_label(ticker, asset_name) -> str:
    """Display label shown in the portal holdings list."""
    t = str(ticker).strip() if pd.notna(ticker) else ''
    if t and t.upper() not in ('NAN', 'NONE', ''):
        return t.upper()
    name = str(asset_name).strip() if pd.notna(asset_name) else ''
    return name[:30] or 'Unknown'


# ---------------------------------------------------------------------------
# Core composition builder
# ---------------------------------------------------------------------------

def _build_composition(df: pd.DataFrame, scope: dict, data_as_of: str) -> dict:
    """
    Build the canonical composition artifact from a filtered holdings DataFrame.

    df must have columns: ticker, asset_name, market_value, asset_class
    scope: e.g. {"firm_id": "49financial"} or {"advisor_id": "...", "firm_id": "..."}

    Pct conventions (all 0-1):
      mix[i].pct                  = class_mv / total_mv
      mix[i].top_holdings[j].pct  = holding_mv / class_mv   (per-class denominator)
      top_holdings[j].pct (root)  = holding_mv / total_mv
      other.pct (root)            = root_other_mv / total_mv
      mix[i].other.pct            = class_other_mv / class_mv
    """
    if df.empty:
        return None

    total_mv = float(df['market_value'].sum())
    if total_mv <= 0:
        return None

    # Build (key, label, asset_class, market_value) grain for aggregation
    df = df.copy()
    df['_key']   = df.apply(lambda r: _holding_key(r['ticker'], r['asset_name']), axis=1)
    df['_label'] = df.apply(lambda r: _holding_label(r['ticker'], r['asset_name']), axis=1)

    # Aggregate to (key, label, asset_class) grain
    holding_agg = (
        df.groupby(['_key', '_label', 'asset_class'], sort=False)['market_value']
        .sum()
        .reset_index()
        .sort_values('market_value', ascending=False)
    )

    # --- Per-class mix + top-9 ---
    mix_out = []
    for asset_class in _ASSET_CLASS_LABELS:
        cls_rows = holding_agg[holding_agg['asset_class'] == asset_class]
        if cls_rows.empty:
            continue

        class_mv = float(cls_rows['market_value'].sum())
        class_pct = round(class_mv / total_mv, 6)

        top_n_rows = cls_rows.head(TOP_N)
        top_holdings_cls = [
            {
                'key':          row['_key'],
                'label':        row['_label'],
                'asset_class':  asset_class,
                'market_value': round(float(row['market_value']), 2),
                'pct':          round(float(row['market_value']) / class_mv, 6),
            }
            for _, row in top_n_rows.iterrows()
        ]

        top_n_mv = float(top_n_rows['market_value'].sum())
        class_other_mv = class_mv - top_n_mv

        mix_out.append({
            'asset_class':   asset_class,
            'label':         _ASSET_CLASS_LABELS[asset_class],
            'market_value':  round(class_mv, 2),
            'pct':           class_pct,
            'top_holdings':  top_holdings_cls,
            'other': {
                'market_value': round(class_other_mv, 2),
                'pct':          round(class_other_mv / class_mv, 6) if class_mv > 0 else 0.0,
            },
        })

    # Sort mix by market_value desc
    mix_out.sort(key=lambda x: x['market_value'], reverse=True)

    # --- Global top-9 (pct relative to total_mv) ---
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

    # --- Unclassified ---
    unclassified = df[df['asset_class'].isin(['', None]) | df['asset_class'].isna()]
    unclassified_count = int(unclassified['_key'].nunique())
    unclassified_mv    = float(unclassified['market_value'].sum())

    return {
        'generated_at':      datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_as_of':        data_as_of,
        'scope':             scope,
        'total_market_value': round(total_mv, 2),
        'top_holdings':      global_top_holdings,
        'other': {
            'market_value': round(global_other_mv, 2),
            'pct':          round(global_other_mv / total_mv, 6) if total_mv > 0 else 0.0,
        },
        'mix':               mix_out,
        'unclassified': {
            'count':        unclassified_count,
            'market_value': round(unclassified_mv, 2),
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Build composition artifacts (firm + per-advisor)'
    )
    parser.add_argument('--upload',  action='store_true', help='Write results to S3')
    parser.add_argument('--dry-run', action='store_true', help='Compute but do not write')
    args = parser.parse_args()

    upload = args.upload and not args.dry_run

    print('=' * 70)
    print('12_build_composition_artifacts.py')
    print(f'Started: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print(f'Mode:    {"UPLOAD" if upload else "DRY RUN"}')
    print('=' * 70)

    # ------------------------------------------------------------------
    # Step 1: Load holdings_lots (latest snapshot)
    # ------------------------------------------------------------------
    print('\n=== Step 1: Load holdings_lots ===')
    holdings_key = _find_latest_holdings_lots()
    if not holdings_key:
        print('ERROR: No holdings_lots parquet found in s3://opal-data-bd/gold/holdings_lots/')
        return 1

    print(f'  Using: {holdings_key}')
    lots = _read_parquet(
        holdings_key,
        columns=['account_id', 'relationship_id', 'ticker', 'asset_name',
                 'market_value', 'is_open'],
    )

    # Filter to open positions only
    lots = lots[lots['is_open'].fillna(False) == True].copy()
    print(f'  Open positions: {len(lots):,} lots, '
          f'{lots["relationship_id"].nunique():,} relationships')

    # data_as_of from filename (gold/holdings_lots/YYYY-MM-DD.parquet)
    data_as_of = holdings_key.rsplit('/', 1)[-1].replace('.parquet', '')

    # ------------------------------------------------------------------
    # Step 2: Classify holdings (ETFClassifier handles ticker + name_alias resolution)
    # ------------------------------------------------------------------
    print('\n=== Step 2: Classify holdings ===')
    lots['asset_class'] = classify_series(lots['ticker'], lots['asset_name'])
    class_counts = lots['asset_class'].value_counts().to_dict()
    print(f'  Classification: {class_counts}')
    gc.collect()

    # ------------------------------------------------------------------
    # Step 3: Load architect lookup (rel_architect_lookup -> fallback to client_dimension)
    # ------------------------------------------------------------------
    print('\n=== Step 3: Load architect lookup ===')
    rel_lookup = None
    try:
        rel_lookup = _read_parquet(
            'gold/views/rel_architect_lookup.parquet',
            columns=['relationship_id', 'architect'],
        )
        print(f'  rel_architect_lookup: {rel_lookup["architect"].nunique()} architects')
    except Exception as e:
        print(f'  WARN: rel_architect_lookup not available ({e})')
        print('  Falling back to client_dimension.primary_architect...')
        try:
            cdim = _read_parquet(
                'gold/client_dimension.parquet',
                columns=['relationship_id', 'primary_architect'],
            )
            rel_lookup = cdim.rename(columns={'primary_architect': 'architect'})
            print(f'  client_dimension fallback: {rel_lookup["architect"].nunique()} architects')
        except Exception as e2:
            print(f'ERROR: client_dimension also unavailable ({e2})')
            return 1

    # ------------------------------------------------------------------
    # Step 4: Merge architect onto holdings
    # ------------------------------------------------------------------
    print('\n=== Step 4: Merge architect lookup ===')
    lots = lots.merge(
        rel_lookup[['relationship_id', 'architect']],
        on='relationship_id',
        how='left',
    )
    missing_arch = lots['architect'].isna().sum()
    if missing_arch > 0:
        lots['architect'] = lots['architect'].fillna('Unassigned')
        print(f'  {missing_arch:,} lots with no architect match -> Unassigned')
    print(f'  Architects after merge: {lots["architect"].nunique()}')
    gc.collect()

    # ------------------------------------------------------------------
    # Step 5: Build and write firm composition
    # ------------------------------------------------------------------
    print('\n=== Step 5: Firm composition ===')
    firm_comp = _build_composition(
        lots,
        scope={'firm_id': FIRM_ID},
        data_as_of=data_as_of,
    )
    if firm_comp is None:
        print('ERROR: Firm composition returned empty -- check holdings_lots content')
        return 1

    _write_json(firm_comp, 'gold/views/firm_composition.json', upload)
    total_mv = firm_comp['total_market_value']
    n_classes = len(firm_comp['mix'])
    print(f'  Total MV: ${total_mv:,.0f} | {n_classes} asset classes')

    # ------------------------------------------------------------------
    # Step 6: Build and write per-advisor composition
    # ------------------------------------------------------------------
    print('\n=== Step 6: Advisor composition ===')
    architects = [
        a for a in lots['architect'].dropna().unique()
        if str(a).strip().lower() not in ('', 'nan', 'none', 'unassigned')
    ]
    print(f'  Processing {len(architects)} architects...')

    written = 0
    skipped = 0
    for architect in architects:
        arch_lots = lots[lots['architect'] == architect]
        adv_id = _advisor_id(str(architect))

        adv_comp = _build_composition(
            arch_lots,
            scope={'advisor_id': adv_id, 'firm_id': FIRM_ID},
            data_as_of=data_as_of,
        )

        if adv_comp is None:
            skipped += 1
            continue

        _write_json(adv_comp, f'gold/advisors/{adv_id}/composition.json', upload)
        written += 1

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f'\n{"=" * 70}')
    print(f'OK: firm_composition.json written. '
          f'Advisors: {written} written, {skipped} skipped (empty book).')
    print(f'Completed: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
