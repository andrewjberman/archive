#!/usr/bin/env python3
"""Build silver/api_dims/assets/ from canonical holdings (Path C source).

ADVI_INFSHIP Phase 1 L4 -- silver layer.

PATH C SOURCE NOTE (CTO 2026-04-28 pre-authorization):
  v0 plan was to read bronze CSV produced by data/inf/manual_api/pull_inflection_assets.py.
  That bronze pull failed 4x: Orion API Generate POST timed out at Asset grouping
  regardless of date window (3y / 7d) or entity scope (firm / entityIds=[3,11,12]).
  Sanity-tested API itself with GET /Verbose?top=1 -> 200 in 0.9s; only Asset grouping
  Generate is broken.

  Path C ships canonical-sourced silver instead:
  - Source: s3://opal-data-inf/gold/canonical/holdings_{date}.parquet (latest)
  - source_system tag: 'canonical_silver' (distinct from 'orion-api')
  - snapshot_date = canonical parquet date (so partition reflects data freshness)
  - 8-day staleness acceptable for v1 ship (CTO call) -- composition logic, not snapshot freshness, is L4's purpose

  Follow-up: INFSHIP.A2 backlog item to debug Orion API Asset-grouping timeout
  with vendor; if/when fixed, this script switches to bronze CSV source.

INFGRD Filter:
  canonical_2026-04-20 is PRE-INFGRD-chain-rerun (INFGRD.004 on hold per Andrew
  2026-04-27 23:48Z). Multi-firm contamination ($133.7M total includes Keil et al.).
  Apply advisor_key allowlist here at silver layer:
    advisor_key IN {inflection_wealth_management, peter_lee, patrick_scanlan}
  Filtered AUA: ~$91.8M / 781 accounts / 728 distinct tickers (within AUA guard bounds).

Schema (matches DS~A's silver/api_dims envelope + L4 PKs):
  account_id      int / string  (canonical Account.Id)
  asset_id        string        (synthesized = ticker; assets without ticker get NAME::{slug})
  asset_ticker    string        (canonical ticker)
  asset_name      string        (canonical product_name)
  position_mv     float         (canonical market_value)
  rep_id          string        (mapped from advisor_key: 3 / 11 / 12)
  snapshot_date   date          (canonical parquet date)
  source_system   string        ('canonical_silver')
  advisor_firm    string        ('inflection_wealth_management' for all post-filter rows)

Project: ADVI_INFSHIP Phase 1 L4
PRD: docs/architecture/ADVI_INFSHIP.md (commit 34d2b757) -- §4 row L4
Author: 0.4.0_DS_ClientPlatform~D
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from io import BytesIO

import boto3
import pandas as pd

from _orion_api_silver_lib import (
    GUARD_B_AUA_LOWER,
    GUARD_B_AUA_UPPER,
    coerce_silver_ids,
    write_silver_api_dim_parquet,
)

S3_BUCKET = 'opal-data-inf'
CANONICAL_PREFIX = 'gold/canonical/'
CANONICAL_FILENAME_PREFIX = 'holdings_'

# advisor_key -> rep_id mapping (per INFGRD INFLECTION_REP_IDS = {3, 11, 12})
# TODO(advisor-of-record 2026-07-10): noel_soderblom is NOT in this allowlist and has no
# servicing rep_id, so if/when this (currently frozen / DI-8) producer is re-activated it
# will DROP Noel's ~61 advisor-of-record mover accounts from silver/api_dims/assets --
# under-counting his top_holdings/assets cross-check and firm AUA. This producer also
# applies a business-row-filter at the silver layer (advisor_key.isin allowlist), which is
# a Rule-17 violation. Do NOT patch the allowlist in isolation: noel needs the
# advisor-of-record capture at silver (raw udf7ADVISOROF passthrough) + a dynamic /
# fold-aware allowlist before this is reactivated. See lib/inflection_rep_scope.py and the
# advisor-of-record re-key in INF_C_07/INF_B_00.
ADVISOR_KEY_TO_REP_ID = {
    'inflection_wealth_management': '3',
    'joe_brandenburg': '6',
    'peter_lee': '11',
    'patrick_scanlan': '12',
}
INFLECTION_ADVISOR_KEYS = set(ADVISOR_KEY_TO_REP_ID.keys())
INFLECTION_ADVISOR_FIRM = 'inflection_wealth_management'
SOURCE_SYSTEM_TAG = 'canonical_silver'

_s3 = boto3.client('s3', region_name='us-east-1')


def _find_latest_canonical_date() -> date:
    """Return the date of the latest canonical/holdings_*.parquet."""
    paginator = _s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=CANONICAL_PREFIX)
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
        and obj['Key'].split('/')[-1].startswith(CANONICAL_FILENAME_PREFIX)
    ])
    if not keys:
        raise RuntimeError(f"No canonical holdings parquet at s3://{S3_BUCKET}/{CANONICAL_PREFIX}")
    latest_key = keys[-1]
    date_str = (latest_key.split('/')[-1]
                .replace(CANONICAL_FILENAME_PREFIX, '')
                .replace('.parquet', ''))
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def _read_canonical(canonical_date: date) -> pd.DataFrame:
    key = f"{CANONICAL_PREFIX}{CANONICAL_FILENAME_PREFIX}{canonical_date.isoformat()}.parquet"
    obj = _s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(obj['Body'].read()))


_TICKER_SAFE_RE = re.compile(r'[A-Z0-9._\-]+')


def _synth_asset_id(ticker: str | None, asset_name: str | None) -> str:
    """Synthesize asset_id from ticker (preferred) or NAME::slug (fallback)."""
    if ticker is not None:
        t = str(ticker).strip().upper()
        if t and t not in ('NAN', 'NONE', '') and _TICKER_SAFE_RE.fullmatch(t):
            return t
    name = str(asset_name or '').strip()
    if not name:
        return 'UNKNOWN'
    slug = re.sub(r'[^A-Z0-9]+', '_', name.upper()).strip('_')[:60]
    return f'NAME::{slug}' if slug else 'UNKNOWN'


def build_assets(canonical_date: date) -> pd.DataFrame:
    """silver/api_dims/assets/ from canonical/holdings_{canonical_date}.parquet.

    Applies INFGRD advisor_key allowlist filter at silver layer (canonical pre-dates
    INFGRD chain rerun -- contains multi-firm contamination).
    """
    canonical = _read_canonical(canonical_date)

    required = {'account_id', 'ticker', 'product_name', 'advisor_key', 'market_value'}
    missing = required - set(canonical.columns)
    if missing:
        raise RuntimeError(f"canonical missing required cols: {missing}; have {list(canonical.columns)}")

    # Apply INFGRD filter at silver (pre-chain-rerun; canonical still multi-firm)
    df = canonical[canonical['advisor_key'].isin(INFLECTION_ADVISOR_KEYS)].copy()

    # Project / synthesize
    df['asset_ticker'] = df['ticker'].astype(str).fillna('').replace({'nan': '', 'None': ''})
    df['asset_name'] = df['product_name'].astype(str).fillna('').replace({'nan': '', 'None': ''})
    df['position_mv'] = df['market_value'].astype(float).fillna(0.0)
    df['asset_id'] = df.apply(
        lambda r: _synth_asset_id(r.get('asset_ticker'), r.get('asset_name')), axis=1,
    )
    # SILVER-ID-DTYPE-UNIFY (2026-05-11): account_id was cast to str; canonical
    # convention is Int64 (nullable). coerce_silver_ids before return enforces.
    df['rep_id'] = df['advisor_key'].map(ADVISOR_KEY_TO_REP_ID)
    df['snapshot_date'] = canonical_date
    df['source_system'] = SOURCE_SYSTEM_TAG
    df['advisor_firm'] = INFLECTION_ADVISOR_FIRM

    total_aua = float(df['position_mv'].sum())
    if total_aua < GUARD_B_AUA_LOWER or total_aua > GUARD_B_AUA_UPPER:
        raise ValueError(
            f"INFGRD Guard B FAIL [assets/canonical]: filtered AUA ${total_aua:,.0f} outside "
            f"[${GUARD_B_AUA_LOWER:,.0f}, ${GUARD_B_AUA_UPPER:,.0f}] sanity bounds."
        )

    cols = [
        'account_id', 'asset_id', 'asset_ticker', 'asset_name', 'position_mv',
        'rep_id', 'snapshot_date', 'source_system', 'advisor_firm',
    ]
    df = coerce_silver_ids(df)
    return df[cols].reset_index(drop=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--canonical-date', default=None,
                   help='Canonical holdings date (YYYY-MM-DD). Default: latest in s3.')
    p.add_argument('--upload', action='store_true', help='Also upload to S3.')
    p.add_argument('--dry-run', action='store_true', help='Build but do not write parquet.')
    args = p.parse_args()

    if args.canonical_date:
        canonical_date = datetime.strptime(args.canonical_date, '%Y-%m-%d').date()
    else:
        canonical_date = _find_latest_canonical_date()
        print(f"[auto] using latest canonical: {canonical_date}")

    try:
        df = build_assets(canonical_date)
    except Exception as e:
        print(f"DIM assets: BUILD FAILED -- {e}")
        return 1

    print(f"DIM assets: {len(df)} rows")
    print(f"  Total AUA:        ${df['position_mv'].sum():,.2f}")
    print(f"  Distinct accts:   {df['account_id'].nunique()}")
    print(f"  Distinct assets:  {df['asset_id'].nunique()}")
    print(f"  Distinct tickers: {df['asset_ticker'].replace('', None).dropna().nunique()}")
    print(f"  rep_id breakdown: {df['rep_id'].value_counts().to_dict()}")

    if args.dry_run:
        return 0

    # snapshot_date for the silver partition matches the canonical date (data freshness)
    local_path, s3_key = write_silver_api_dim_parquet(
        df, 'assets', canonical_date, upload_s3=args.upload,
    )
    print(f"DIM assets: -> {local_path}" + (f" + s3://{s3_key}" if s3_key else ""))
    return 0


if __name__ == '__main__':
    sys.exit(main())
