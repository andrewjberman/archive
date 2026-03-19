#!/usr/bin/env python3
"""
Build Accounts Dimension — Account Metadata

Data source philosophy:
  PRIMARY:    silver/transactions/ (full time series, 2020-present)
              The only source that covers ALL accounts ever seen — open, closed,
              pre-2026, everything. Takes the latest transaction row per account_id
              to extract current metadata. tax_status_1 field is the authoritative
              tax classification (confirmed 100% aligned with allocations, zero
              mismatches across all tested accounts).

  ENRICHMENT: silver/allocations/ latest snapshot (left join, Jan 2026+ accounts only)
              Adds account_type and account_registration_type — the only two fields
              not present in the transaction schema. These are static labels (an IRA
              registered in 2020 is still an IRA today), so using the latest snapshot
              as a retroactive label is correct. Accounts absent from allocations
              (closed pre-2026) receive null for these two fields — acceptable.

  NEVER:      Allocation market_value, historical allocation data, or any allocation
              field used for time-series computation. Allocations are a snapshot,
              not a time series. They are only collected daily from Jan 2026 onward.

Output: gold/accounts_dimension_latest.parquet

Usage:
    python 00_build_accounts_dimension.py --dry-run
    python 00_build_accounts_dimension.py --upload

Author: Data Scientist (Claude)
Date: 2026-02-20  (rewritten — transactions as primary source)
"""

import argparse
import gc
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO

import pandas as pd
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')
MAX_WORKERS = 64


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))

# Columns to extract from transactions for account metadata.
# These are the account-level fields present in the 73-col transaction schema.
# Excludes all transaction-specific fields (asset_name, units, price, etc.).
TXN_ACCOUNT_COLS = [
    'account_id',
    'account_name',
    'account_display_name',
    'relationship_id',
    'relationship_name',
    'relationship_display_name',
    'relationship_sec_client_type',
    'tax_status_1',          # authoritative tax classification — rename to tax_status
    'architect',
    'implementor',
    'local_ops',
    'client_city',
    'client_state',
    'client_country',
    'client_zip_code',
    'account_is_open',
    'start_date',            # account inception date — take min per account_id
    'closed_date',
    'account_owner_type',
    'account_owner',
    'manager',
    'investment_strategy_name',
    'portfolio_group',
    'trade_date',            # used for latest-row selection and first_seen_date; dropped at output
]

# Tax status normalisation: BD native values → internal format
TAX_STATUS_MAP = {
    'Taxable':      'taxable',       # Brokerage/joint/trust — gains taxed on realisation
    'Tax-Deferred': 'tax_deferred',  # Traditional IRA/401k/SEP/SIMPLE — taxed on withdrawal
    'Non-Taxable':  'tax_exempt',    # Roth IRA/Roth 401k — tax-free growth and withdrawal
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_accounts_from_transactions() -> pd.DataFrame:
    """
    Build account metadata from the full transaction time series.

    Takes the latest transaction row per account_id as the source of current
    metadata. Also derives account_open_date (min trade_date per account) and
    relationship_first_seen_date (min trade_date per relationship_id).

    Returns one row per account_id covering all accounts from 2020 onward.
    """
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading transactions (parallel)... ", end='', flush=True)

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

    # Deduplicate on transaction_id
    if 'transaction_id' in txns.columns:
        txns = txns.drop_duplicates(subset=['transaction_id'], keep='last')

    txns['trade_date'] = pd.to_datetime(txns['trade_date'], errors='coerce')

    print(f"{len(txns):,} transactions across {txns['account_id'].nunique():,} accounts")

    # Keep only account-metadata columns that exist in this schema
    keep_cols = [c for c in TXN_ACCOUNT_COLS if c in txns.columns]
    txns = txns[keep_cols]

    # Latest row per account_id — gives current values for all metadata fields
    latest = (
        txns.sort_values('trade_date', ascending=False)
        .groupby('account_id', sort=False)
        .first()
        .reset_index()
    )

    # Advisor carry-forward: the latest transaction for an account may have a
    # blank architect/implementor (common on cash sweeps, dividends, fee entries)
    # even though earlier transactions carried a real name. For each advisor
    # field, find the most recent transaction with a non-null value and use that
    # instead of the latest-row value when the latest row is blank.
    _ADVISOR_NULLS = frozenset({
        '', 'none', 'nan', 'unassigned', 'unknown', 'n/a',
        'no architect value assigned',
    })
    for adv_col in ['architect', 'implementor']:
        if adv_col not in txns.columns:
            continue
        # Filter to transactions with a real (non-placeholder) value
        real_mask = (
            txns[adv_col].notna() &
            ~txns[adv_col].astype(str).str.strip().str.lower().isin(_ADVISOR_NULLS)
        )
        real_txns = txns.loc[real_mask, ['account_id', 'trade_date', adv_col]]
        if real_txns.empty:
            continue
        # Latest real value per account
        last_real = (
            real_txns.sort_values('trade_date', ascending=False)
            .groupby('account_id', sort=False)[adv_col]
            .first()
        )
        # Identify accounts where the latest-row value is blank/placeholder
        current_vals = latest.set_index('account_id')[adv_col].fillna('')
        is_blank = current_vals.str.strip().str.lower().isin(_ADVISOR_NULLS)
        # Carry forward: fill blanks with the last known real value
        filled = current_vals.copy()
        filled.loc[is_blank] = current_vals.index[is_blank].map(last_real)
        n_recovered = is_blank.sum() - filled.isna().sum() - (
            filled.fillna('').str.strip().str.lower().isin(_ADVISOR_NULLS).sum()
        )
        latest[adv_col] = filled.values
        if n_recovered > 0:
            print(f"  Advisor carry-forward ({adv_col}): recovered {n_recovered:,} accounts "
                  f"from historical transactions")

    # Account open date = earliest trade_date seen for that account
    # (start_date field from BD is more reliable if present, but supplement with min trade_date)
    earliest_trade = (
        txns.groupby('account_id')['trade_date']
        .min()
        .reset_index()
        .rename(columns={'trade_date': 'first_transaction_date'})
    )
    latest = latest.merge(earliest_trade, on='account_id', how='left')

    # Relationship first_seen_date — earliest trade across all accounts in household
    rel_first_seen = (
        txns.groupby('relationship_id')['trade_date']
        .min()
        .reset_index()
        .rename(columns={'trade_date': 'relationship_first_seen_date'})
    )
    latest = latest.merge(rel_first_seen, on='relationship_id', how='left')

    # Drop the trade_date used for ordering (not an output column)
    latest = latest.drop(columns=['trade_date'], errors='ignore')

    print(f"  → {len(latest):,} unique accounts extracted")
    return latest


def load_alloc_enrichment() -> pd.DataFrame:
    """
    Load account_type and account_registration_type from the latest allocation snapshot.

    These two fields are not present in the transaction schema. They are static
    account labels (registration type doesn't change) so the latest snapshot is
    valid as a retroactive label for all historical positions.

    Returns a small DataFrame: (account_id, account_type, account_registration_type).
    Accounts absent from allocations (e.g. closed pre-2026) simply won't join —
    those fields will be null in the output.
    """
    paginator = s3.get_paginator('list_objects_v2')
    alloc_keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/allocations/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                alloc_keys.append(obj['Key'])

    if not alloc_keys:
        print("  No allocation snapshots found — account_type/registration_type will be null")
        return pd.DataFrame(columns=['account_id', 'account_type', 'account_registration_type'])

    latest_key = sorted(alloc_keys)[-1]
    print(f"Loading allocation enrichment from {latest_key}...", end=' ', flush=True)
    resp = s3.get_object(Bucket=S3_BUCKET, Key=latest_key)
    alloc = pd.read_parquet(BytesIO(resp['Body'].read()))

    # Extract only the two enrichment fields — nothing else from allocations enters the dimension
    enrich_cols = ['account_id', 'account_type', 'account_registration_type']
    available = [c for c in enrich_cols if c in alloc.columns]
    enrichment = alloc[available].drop_duplicates(subset=['account_id'], keep='first')

    print(f"{len(enrichment):,} accounts with type/registration data")
    return enrichment


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_accounts_dimension(
    txn_accounts: pd.DataFrame,
    alloc_enrichment: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine transaction-derived account metadata with allocation enrichment.

    Args:
        txn_accounts:    One row per account from full transaction history (primary)
        alloc_enrichment: account_type + account_registration_type from latest
                          allocation snapshot (enrichment only — left join)

    Returns:
        Clean accounts dimension, one row per account_id.
    """
    print("\nBuilding accounts dimension...")

    accts = txn_accounts.copy()

    # Normalise relationship_id
    if 'relationship_id' in accts.columns:
        accts['relationship_id'] = accts['relationship_id'].astype(str).str.strip()
        accts.loc[accts['relationship_id'].isin(['None', 'nan', '']), 'relationship_id'] = None

    # Clean architect
    accts['architect'] = accts.get('architect', pd.Series(dtype=str)).fillna('Unassigned')
    accts['architect'] = accts['architect'].replace('No Architect Value Assigned', 'Unassigned')

    # Tax status — normalise from BD native values (tax_status_1 in transactions)
    # tax_status_1 confirmed authoritative: 100% diagonal match with allocations tax_status
    tax_col = 'tax_status_1' if 'tax_status_1' in accts.columns else 'tax_status'
    if tax_col in accts.columns:
        accts['tax_status'] = accts[tax_col].map(TAX_STATUS_MAP).fillna('taxable')
    else:
        accts['tax_status'] = 'taxable'

    # Drop the raw tax_status_1 column (we've normalised it into tax_status)
    accts = accts.drop(columns=['tax_status_1'], errors='ignore')

    # qualified_flag: True = IRA/Roth/401k/SEP/SIMPLE (retirement account)
    accts['qualified_flag'] = accts['tax_status'].isin(['tax_deferred', 'tax_exempt'])

    # Standardise location fields
    for field, aliases in [
        ('client_city',    ['client_city', 'city']),
        ('client_state',   ['client_state', 'state']),
        ('client_country', ['client_country', 'country']),
        ('client_zip',     ['client_zip_code', 'client_zip', 'zip']),
    ]:
        for alias in aliases:
            if alias in accts.columns:
                accts[field] = accts[alias].fillna('')
                if alias != field:
                    accts = accts.drop(columns=[alias], errors='ignore')
                break
        if field not in accts.columns:
            accts[field] = ''

    accts['client_country'] = accts['client_country'].replace('', 'USA').fillna('USA')

    # account_open_date: prefer BD's start_date field; coalesce with first_transaction_date
    # Must use fillna (not elif) because start_date column exists but is null for 41% of accounts
    if 'start_date' in accts.columns:
        accts['account_open_date'] = pd.to_datetime(accts['start_date'], errors='coerce')
        accts = accts.drop(columns=['start_date'], errors='ignore')
    else:
        accts['account_open_date'] = pd.NaT
    if 'first_transaction_date' in accts.columns:
        accts['account_open_date'] = accts['account_open_date'].fillna(
            pd.to_datetime(accts['first_transaction_date'], errors='coerce')
        )

    # Left join allocation enrichment (account_type, account_registration_type)
    if not alloc_enrichment.empty and 'account_id' in alloc_enrichment.columns:
        accts = accts.merge(alloc_enrichment, on='account_id', how='left')
        matched = accts['account_type'].notna().sum()
        print(f"  Allocation enrichment: {matched:,} of {len(accts):,} accounts matched "
              f"({matched/len(accts)*100:.1f}%) — remainder have null account_type (pre-2026 or closed)")
    else:
        accts['account_type'] = None
        accts['account_registration_type'] = None

    # Final column selection and order
    output_cols = [
        'account_id',
        'account_name',
        'account_display_name',
        'account_type',                  # from allocations enrichment (null if pre-2026/closed)
        'account_registration_type',     # from allocations enrichment (null if pre-2026/closed)
        'tax_status',                    # from transactions tax_status_1 — full coverage
        'qualified_flag',                # derived from tax_status — full coverage
        'account_open_date',             # from transactions start_date / first_transaction_date
        'first_transaction_date',        # earliest trade seen for this account
        'closed_date',
        'account_is_open',
        'account_owner_type',
        'account_owner',
        'relationship_id',
        'relationship_name',
        'relationship_display_name',
        'relationship_sec_client_type',
        'relationship_first_seen_date',  # earliest trade across all accounts in household
        'architect',
        'implementor',
        'local_ops',
        'manager',
        'investment_strategy_name',
        'portfolio_group',
        'client_city',
        'client_state',
        'client_country',
        'client_zip',
    ]

    available = [c for c in output_cols if c in accts.columns]
    result = accts[available].copy()
    result = result.rename(columns={'local_ops': 'local_relationship'})

    # Metadata
    result['data_as_of_date'] = pd.Timestamp.now(tz='UTC').date()
    result['updated_date'] = pd.Timestamp.now(tz='UTC')

    # Summary
    print(f"\n  Total accounts:         {len(result):,}")
    print(f"  With relationship_id:   {result['relationship_id'].notna().sum():,}")
    qual = result['qualified_flag'].sum()
    nonq = (~result['qualified_flag']).sum()
    print(f"  Qualified (retirement): {qual:,}  |  Non-qualified (taxable): {nonq:,}")
    print(f"  By tax_status:")
    for ts, cnt in result['tax_status'].value_counts().items():
        print(f"    {ts}: {cnt:,}")
    if 'account_type' in result.columns:
        print(f"  By account_type (top 8):  {result['account_type'].notna().sum():,} populated")
        for at, cnt in result['account_type'].value_counts().head(8).items():
            print(f"    {at}: {cnt:,}")

    return result


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_dimension(df: pd.DataFrame, upload: bool = False):
    """Save accounts dimension to gold layer."""
    print("\nSaving accounts dimension...")

    output_key = 'gold/accounts_dimension_latest.parquet'
    local_path = Path('/tmp/accounts_dimension.parquet')

    # Coerce mixed-type object columns to clean strings before parquet write.
    # Columns like client_zip can contain '' / numeric-looking values that
    # confuse pyarrow type inference (ArrowInvalid: tried to convert to double).
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        df[col] = df[col].where(df[col].notna() & (df[col] != ''), other=pd.NA)
        df[col] = df[col].astype('string')

    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.1f} MB")

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
    parser = argparse.ArgumentParser(description='Build Accounts Dimension')
    parser.add_argument('--dry-run', action='store_true', help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true', help='Upload to S3')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD ACCOUNTS DIMENSION")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    txn_accounts = load_accounts_from_transactions()

    print()
    alloc_enrichment = load_alloc_enrichment()

    print("\n=== Step 2: Build dimension ===")
    dimension = build_accounts_dimension(txn_accounts, alloc_enrichment)

    print("\n=== Step 3: Save ===")
    save_dimension(dimension, upload=args.upload and not args.dry_run)

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(dimension):,} accounts | {len(dimension.columns)} columns")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
