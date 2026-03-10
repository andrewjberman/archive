"""
BD Gold Layer Lambda

Generates all gold layer JSON files after bd-merge-daily updates the silver parquet.
Invoked by bd-merge-daily Lambda after successful merge.

Runs the equivalent of:
1. 01_build_canonical_timeline.py → silver/bd_canonical_timeline.parquet
2. 02_generate_timeseries.py      → gold/timeseries/*.json (11 files)
3. 03_generate_snapshots.py       → gold/snapshots/*.json (7 files)
4. 04_generate_clients.py         → gold/clients/*.json (3 files)
5. 05_generate_filters.py         → gold/filters/dimensions.json
6. 06_generate_summary.py         → gold/summary/header_metrics.json

Total output: 23 files (1 parquet + 22 JSON)
"""

import boto3
import json
import os
from datetime import datetime, timezone, timedelta
from io import BytesIO
import traceback

import pandas as pd
import numpy as np

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    # Fallback if dateutil not available
    def relativedelta(months=0):
        return timedelta(days=months * 30)

# Configuration
S3_BUCKET = os.environ.get('S3_BUCKET', 'opal-data-bd')
FIRM_ID = '49financial'
FIRM_NAME = '49 Financial'

# Invalid relationship_id values that require fallback to account_id
INVALID_REL_IDS = {'', '0', 'nan', 'None', 'No Relationship'}

s3 = boto3.client('s3')


def lambda_handler(event, context):
    """
    Main Lambda handler - generate all gold layer files.
    """
    print(f"BD Gold Layer invoked at {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")

    try:
        # Load silver data
        print("\n=== Loading Silver Data ===")
        txns = load_parquet('silver/bd_transactions.parquet')
        print(f"Loaded {len(txns):,} transactions")

        accounts = load_parquet('silver/bd_accounts.parquet')
        print(f"Loaded {len(accounts):,} accounts")

        # Ensure trade_date is datetime
        txns['trade_date'] = pd.to_datetime(txns['trade_date'])

        # Step 1: Build canonical timeline
        print("\n=== Step 1: Building Canonical Timeline ===")
        timeline = build_canonical_timeline(txns)
        save_parquet(timeline, 'silver/bd_canonical_timeline.parquet')

        # Step 2: Generate timeseries
        print("\n=== Step 2: Generating Timeseries ===")
        generate_timeseries(txns, timeline)

        # Step 3: Generate snapshots
        print("\n=== Step 3: Generating Snapshots ===")
        generate_snapshots(accounts)

        # Step 4: Generate clients
        print("\n=== Step 4: Generating Clients ===")
        generate_clients(accounts, txns)

        # Step 5: Generate filters
        print("\n=== Step 5: Generating Filters ===")
        generate_filters(accounts)

        # Step 6: Generate summary
        print("\n=== Step 6: Generating Summary ===")
        generate_summary(accounts, txns)

        print("\n=== Gold Layer Generation Complete ===")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Gold layer generation complete',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'files_generated': 23
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        raise


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_client_key(row) -> str:
    """Generate client_key matching the canonical timeline format."""
    rel_id = str(row.get('relationship_id', '')).strip()
    if rel_id in INVALID_REL_IDS:
        return f"acct_{row['account_id']}"
    return f"rel_{rel_id}"


def get_display_name(row) -> str:
    """Get display name for a client (relationship_name with fallbacks)."""
    rel_name = str(row.get('relationship_name', '')).strip()
    if rel_name not in INVALID_REL_IDS and rel_name:
        return rel_name

    client_name = str(row.get('client_name', '')).strip()
    if client_name and client_name not in ('nan', 'None', ''):
        return client_name

    return f"Account {row.get('account_id', 'Unknown')}"


def add_client_key(df: pd.DataFrame) -> pd.DataFrame:
    """Add client_key and display_name columns to dataframe."""
    df = df.copy()
    df['client_key'] = df.apply(get_client_key, axis=1)
    df['display_name'] = df.apply(get_display_name, axis=1)
    return df


def load_parquet(key: str) -> pd.DataFrame:
    """Load parquet from S3."""
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return pd.read_parquet(BytesIO(response['Body'].read()))
    except s3.exceptions.NoSuchKey:
        print(f"File not found: s3://{S3_BUCKET}/{key}")
        return pd.DataFrame()


def save_parquet(df: pd.DataFrame, key: str):
    """Save DataFrame to S3 as parquet."""
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, compression='snappy')
    buffer.seek(0)

    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buffer.getvalue())
    size_kb = len(buffer.getvalue()) / 1024
    print(f"  Saved: s3://{S3_BUCKET}/{key} ({size_kb:.1f} KB)")


def save_json(data: dict, key: str):
    """Save dict to S3 as JSON."""
    json_str = json.dumps(data, indent=2, default=str)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json_str.encode('utf-8'),
        ContentType='application/json'
    )
    print(f"  Saved: s3://{S3_BUCKET}/{key} ({len(json_str):,} bytes)")


# =============================================================================
# STEP 1: CANONICAL TIMELINE
# =============================================================================

def build_canonical_timeline(df: pd.DataFrame) -> pd.DataFrame:
    """Build canonical timeline tracking first-seen date for each client."""
    df = df.sort_values('trade_date').copy()
    df['client_key'] = df.apply(get_client_key, axis=1)

    first_txns = df.groupby('client_key').agg({
        'trade_date': 'min',
        'account_id': 'first',
        'architect': 'first',
        'relationship_id': 'first',
        'relationship_name': 'first',
        'client_name': 'first',
    }).reset_index()

    first_txns.columns = [
        'client_key', 'first_seen_date', 'first_account_id',
        'first_architect', 'relationship_id', 'relationship_name', 'client_name'
    ]

    # Get account counts
    account_counts = df.groupby('client_key')['account_id'].nunique().reset_index()
    account_counts.columns = ['client_key', 'total_accounts']
    first_txns = first_txns.merge(account_counts, on='client_key', how='left')

    first_txns['last_updated'] = datetime.now(timezone.utc).isoformat()
    first_txns['first_architect'] = first_txns['first_architect'].replace(
        'No Architect Value Assigned', 'House'
    )

    print(f"  Timeline records: {len(first_txns):,}")
    return first_txns


# =============================================================================
# STEP 2: TIMESERIES
# =============================================================================

def generate_timeseries(df: pd.DataFrame, timeline: pd.DataFrame):
    """Generate all timeseries JSON files."""
    df = df.copy()

    # Add period column
    df['period'] = df['trade_date'].dt.to_period('M').astype(str)

    # Identify NNA transactions
    NNA_INFLOW_TYPES = ['Cash Deposit', 'Transfer In', 'Wire In', 'Transfer']
    NNA_OUTFLOW_TYPES = ['Cash Withdrawal', 'Transfer Out', 'Wire Out']

    df['is_nna_inflow'] = (
        df['transaction_type'].isin(NNA_INFLOW_TYPES) |
        df['action'].str.contains('Deposit|Transfer In|Wire In', case=False, na=False)
    )
    df['is_nna_outflow'] = (
        df['transaction_type'].isin(NNA_OUTFLOW_TYPES) |
        df['action'].str.contains('Withdrawal|Transfer Out|Wire Out', case=False, na=False)
    )

    # Merge timeline to get is_new_client
    df['client_key'] = df.apply(get_client_key, axis=1)
    df = df.merge(
        timeline[['client_key', 'first_seen_date']],
        on='client_key',
        how='left'
    )
    df['first_seen_date'] = pd.to_datetime(df['first_seen_date'])
    df['is_new_client'] = df['trade_date'].dt.date == df['first_seen_date'].dt.date

    print(f"  NNA inflows: {df['is_nna_inflow'].sum():,}")
    print(f"  New client txns: {df['is_new_client'].sum():,}")

    # Generate total timeseries
    total_ts = generate_total_timeseries(df)
    save_json(total_ts, 'gold/timeseries/nna_total.json')

    # Generate category timeseries
    cat_ts = generate_category_timeseries(df)
    save_json(cat_ts, 'gold/timeseries/nna_by_category.json')

    # Generate dimension timeseries
    dimensions = {
        'architect': {'column': 'architect', 'transform': {'No Architect Value Assigned': 'House'}, 'top_n': None},
        'region': {'column': 'local_ops', 'transform': {'No Local Ops Value Assigned': 'Unassigned'}, 'top_n': None},
        'implementor': {'column': 'implementor', 'transform': {'No Implementor Value Assigned': 'Unassigned'}, 'top_n': 50},
        'account_type': {'column': 'account_owner_type', 'transform': {}, 'top_n': None},
        'tax_status': {'column': 'tax_status', 'transform': {}, 'top_n': None},
        'client_segment': {'column': 'is_new_client', 'transform': {True: 'New Client', False: 'Existing Client', 1: 'New Client', 0: 'Existing Client'}, 'top_n': None},
        'state': {'column': 'client_state', 'transform': {}, 'top_n': 49},
        'city': {'column': 'client_city', 'transform': {}, 'top_n': 50},
        'relationship': {'column': 'relationship_name', 'transform': {'No Relationship': 'Unassigned'}, 'top_n': 100},
    }

    for dim_name, config in dimensions.items():
        dim_ts = generate_dimension_timeseries(df, dim_name, config)
        if dim_ts:
            save_json(dim_ts, f'gold/timeseries/nna_by_{dim_name}.json')


def generate_total_timeseries(df: pd.DataFrame) -> dict:
    """Generate aggregate NNA timeseries."""
    nna = df[df['is_nna_inflow'] | df['is_nna_outflow']].copy()

    agg = nna.groupby('period').agg(
        inflow=('market_value', lambda x: x[nna.loc[x.index, 'is_nna_inflow']].sum()),
        outflow=('market_value', lambda x: x[nna.loc[x.index, 'is_nna_outflow']].sum()),
        txn_count=('transaction_id', 'count'),
    ).reset_index()

    agg['net'] = agg['inflow'] - agg['outflow']

    data = [
        {
            'period': row['period'],
            'inflow': float(row['inflow']),
            'outflow': float(row['outflow']),
            'net': float(row['net']),
            'txn_count': int(row['txn_count']),
        }
        for _, row in agg.iterrows()
    ]

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': df['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'data': sorted(data, key=lambda x: x['period']),
    }


def generate_category_timeseries(df: pd.DataFrame) -> dict:
    """Generate NNA timeseries by category (NMNC/NMEC)."""
    nna = df[df['is_nna_inflow']].copy()

    nna['category'] = nna['is_new_client'].map({
        True: 'NMNC', 1: 'NMNC',
        False: 'NMEC', 0: 'NMEC'
    }).fillna('NMEC')

    agg = nna.groupby(['period', 'category']).agg(
        value=('market_value', 'sum'),
        txn_count=('transaction_id', 'count'),
    ).reset_index()

    pivot = agg.pivot(index='period', columns='category', values='value').fillna(0)

    data = []
    for period in pivot.index:
        row = {'period': period}
        for cat in pivot.columns:
            row[cat.lower()] = float(pivot.loc[period, cat])
        row['total'] = sum(v for k, v in row.items() if k != 'period')
        data.append(row)

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': df['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'categories': ['nmnc', 'nmec'],
        'data': sorted(data, key=lambda x: x['period']),
    }


def generate_dimension_timeseries(df: pd.DataFrame, dim_name: str, config: dict) -> dict:
    """
    Generate NNA timeseries for a specific dimension.

    Output format (Recharts-compatible):
    {
        "dimension_values": ["House", "Travis Penfield", ...],
        "data": [
            {
                "period": "2021-01",
                "House": {"nmnc": 500000, "nmec": 6400000, "nna_net": 6920831, "outflow": 0, "txn_count": 349},
                "Travis Penfield": {"nmnc": 0, "nmec": 0, "nna_net": 0, "outflow": 0, "txn_count": 0}
            }
        ]
    }

    Key features:
    - Filters out empty/null dimension values
    - Includes NMNC (new money new client) and NMEC (new money existing client) breakdown
    - Pads sparse data so every dimension appears in every period (with zeros if no activity)
    """
    column = config['column']
    transform = config['transform']
    top_n = config['top_n']

    # Get both inflows and outflows for net calculation
    nna_inflow = df[df['is_nna_inflow']].copy()
    nna_outflow = df[df['is_nna_outflow']].copy()

    if column not in df.columns:
        print(f"  Skipping {dim_name}: column {column} not found")
        return None

    # Apply dimension value transformation
    nna_inflow['dim_value'] = nna_inflow[column].astype(str).replace(transform)
    nna_outflow['dim_value'] = nna_outflow[column].astype(str).replace(transform)

    # Filter out empty/null dimension values
    invalid_values = {'', 'nan', 'None', 'NaN', 'null'}
    nna_inflow = nna_inflow[~nna_inflow['dim_value'].isin(invalid_values)]
    nna_inflow = nna_inflow[nna_inflow['dim_value'].str.strip() != '']
    nna_outflow = nna_outflow[~nna_outflow['dim_value'].isin(invalid_values)]
    nna_outflow = nna_outflow[nna_outflow['dim_value'].str.strip() != '']

    # Get top N values by total inflow if specified
    if top_n:
        top_values = nna_inflow.groupby('dim_value')['market_value'].sum().nlargest(top_n).index.tolist()
        nna_inflow = nna_inflow[nna_inflow['dim_value'].isin(top_values)]
        nna_outflow = nna_outflow[nna_outflow['dim_value'].isin(top_values)]

    # Aggregate inflows with NMNC/NMEC breakdown (memory-efficient)
    # Add separate columns for NMNC and NMEC values
    nna_inflow['nmnc_value'] = nna_inflow['market_value'].where(nna_inflow['is_new_client'] == True, 0)
    nna_inflow['nmec_value'] = nna_inflow['market_value'].where(nna_inflow['is_new_client'] == False, 0)

    inflow_agg = nna_inflow.groupby(['period', 'dim_value']).agg(
        nmnc=('nmnc_value', 'sum'),
        nmec=('nmec_value', 'sum'),
        inflow_txn_count=('transaction_id', 'count'),
    ).reset_index()

    # Aggregate outflows
    outflow_agg = nna_outflow.groupby(['period', 'dim_value']).agg(
        outflow=('market_value', 'sum'),
        outflow_txn_count=('transaction_id', 'count'),
    ).reset_index()

    # Merge inflows and outflows
    agg = inflow_agg.merge(outflow_agg, on=['period', 'dim_value'], how='outer').fillna(0)

    # Calculate net NNA
    agg['nna_net'] = agg['nmnc'] + agg['nmec'] - agg['outflow']
    agg['txn_count'] = agg['inflow_txn_count'] + agg['outflow_txn_count']

    # Get all unique dimension values and periods
    dim_values = sorted(agg['dim_value'].unique().tolist())
    all_periods = sorted(agg['period'].unique().tolist())

    # Build data array with padding (every dimension in every period)
    data = []
    for period in all_periods:
        period_data = {'period': period}
        period_rows = agg[agg['period'] == period].set_index('dim_value')

        for dim_val in dim_values:
            if dim_val in period_rows.index:
                row = period_rows.loc[dim_val]
                period_data[dim_val] = {
                    'nmnc': float(row['nmnc']),
                    'nmec': float(row['nmec']),
                    'nna_net': float(row['nna_net']),
                    'outflow': float(row['outflow']),
                    'txn_count': int(row['txn_count']),
                }
            else:
                # Pad with zeros for dimensions with no activity this period
                period_data[dim_val] = {
                    'nmnc': 0.0,
                    'nmec': 0.0,
                    'nna_net': 0.0,
                    'outflow': 0.0,
                    'txn_count': 0,
                }

        data.append(period_data)

    print(f"  nna_by_{dim_name}.json: {len(dim_values)} values, {len(all_periods)} periods (padded)")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': df['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'dimension': dim_name,
        'dimension_values': dim_values,
        'data': data,
    }


# =============================================================================
# STEP 3: SNAPSHOTS
# =============================================================================

def generate_snapshots(accounts: pd.DataFrame):
    """Generate all snapshot JSON files."""
    accounts = add_client_key(accounts)

    dimensions = {
        'architect': {'column': 'architect', 'transform': {'No Architect Value Assigned': 'House'}, 'top_n': None},
        'region': {'column': 'local_ops', 'transform': {'No Local Ops Value Assigned': 'Unassigned'}, 'top_n': None},
        'account_type': {'column': 'account_owner_type', 'transform': {}, 'top_n': None},
        'tax_status': {'column': 'tax_status', 'transform': {}, 'top_n': None},
        'state': {'column': 'client_state', 'transform': {}, 'top_n': 49},
        'city': {'column': 'client_city', 'transform': {}, 'top_n': 50},
        'relationship': {'column': 'display_name', 'transform': {}, 'top_n': 100},
    }

    for dim_name, config in dimensions.items():
        snapshot = generate_snapshot(accounts, dim_name, config)
        if snapshot:
            save_json(snapshot, f'gold/snapshots/aua_by_{dim_name}.json')


def generate_snapshot(df: pd.DataFrame, dim_name: str, config: dict) -> dict:
    """Generate AUA snapshot for a specific dimension."""
    column = config['column']
    transform = config['transform']
    top_n = config['top_n']

    if column not in df.columns:
        print(f"  Skipping {dim_name}: column {column} not found")
        return None

    df = df.copy()
    df['dim_value'] = df[column].astype(str).replace(transform)
    df = df[df['dim_value'].notna() & (df['dim_value'] != '') & (df['dim_value'] != 'nan')]

    agg = df.groupby('dim_value').agg(
        aua=('emv', 'sum'),
        client_count=('client_key', 'nunique'),
        account_count=('account_id', 'nunique'),
    ).reset_index()

    agg = agg.sort_values('aua', ascending=False)

    if top_n:
        agg = agg.head(top_n)

    total_aua = agg['aua'].sum()
    agg['aua_pct'] = (agg['aua'] / total_aua * 100).round(1)

    data = [
        {
            'value': row['dim_value'],
            'aua': float(row['aua']),
            'aua_pct': float(row['aua_pct']),
            'client_count': int(row['client_count']),
            'account_count': int(row['account_count']),
        }
        for _, row in agg.iterrows()
    ]

    print(f"  aua_by_{dim_name}.json: {len(data)} values")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'dimension': dim_name,
        'total_aua': float(total_aua),
        'data': data,
    }


# =============================================================================
# STEP 4: CLIENTS
# =============================================================================

def generate_clients(accounts: pd.DataFrame, txns: pd.DataFrame):
    """Generate all client JSON files."""
    accounts = add_client_key(accounts)
    txns = add_client_key(txns)
    txns['trade_date'] = pd.to_datetime(txns['trade_date'])
    txns['period'] = txns['trade_date'].dt.to_period('M').astype(str)

    # Growth timeseries
    growth = generate_growth_timeseries(accounts, txns)
    save_json(growth, 'gold/clients/growth_timeseries.json')

    # Tax breakdown
    tax_breakdown = generate_tax_breakdown(accounts)
    save_json(tax_breakdown, 'gold/clients/tax_basis_breakdown.json')

    # Tax deferred candidates
    candidates = generate_tax_deferred_candidates(accounts, txns)
    save_json(candidates, 'gold/clients/tax_deferred_candidates.json')


def generate_growth_timeseries(accounts: pd.DataFrame, txns: pd.DataFrame) -> dict:
    """Generate client growth timeseries."""
    client_by_period = txns.groupby('period')['client_key'].nunique().reset_index()
    client_by_period.columns = ['period', 'active_clients']

    first_seen = txns.groupby('client_key')['trade_date'].min().reset_index()
    first_seen['period'] = first_seen['trade_date'].dt.to_period('M').astype(str)
    new_clients = first_seen.groupby('period').size().reset_index(name='new_clients')

    growth = client_by_period.merge(new_clients, on='period', how='left').fillna(0)
    growth = growth.sort_values('period')
    growth['cumulative_clients'] = growth['new_clients'].cumsum()

    total_aua = accounts['emv'].sum()
    total_clients = accounts['client_key'].nunique()

    data = [
        {
            'period': row['period'],
            'new_clients': int(row['new_clients']),
            'cumulative_clients': int(row['cumulative_clients']),
            'active_clients': int(row['active_clients']),
        }
        for _, row in growth.iterrows()
    ]

    print(f"  growth_timeseries.json: {len(data)} periods")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': txns['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'summary': {
            'total_clients': int(total_clients),
            'total_aua': float(total_aua),
            'avg_aua_per_client': float(total_aua / total_clients) if total_clients > 0 else 0,
        },
        'data': sorted(data, key=lambda x: x['period']),
    }


def generate_tax_breakdown(accounts: pd.DataFrame) -> dict:
    """Generate tax basis breakdown for pie charts."""
    charts = {}

    if 'tax_status' in accounts.columns:
        tax_agg = accounts.groupby('tax_status').agg(
            value=('emv', 'sum'),
            count=('account_id', 'nunique'),
        ).reset_index()

        total = tax_agg['value'].sum()
        tax_agg['pct'] = (tax_agg['value'] / total * 100).round(1)

        colors = {
            'Taxable': '#4CAF50',
            'Tax-Exempt': '#2196F3',
            'Tax-Deferred': '#FF9800',
            'Other': '#9E9E9E',
        }

        charts['tax_status'] = {
            'title': 'AUA by Tax Status',
            'data': [
                {
                    'label': row['tax_status'],
                    'value': float(row['value']),
                    'pct': float(row['pct']),
                    'count': int(row['count']),
                    'color': colors.get(row['tax_status'], '#9E9E9E'),
                }
                for _, row in tax_agg.iterrows()
            ]
        }

    if 'account_owner_type' in accounts.columns:
        type_agg = accounts.groupby('account_owner_type').agg(
            value=('emv', 'sum'),
            count=('account_id', 'nunique'),
        ).reset_index()

        total = type_agg['value'].sum()
        type_agg['pct'] = (type_agg['value'] / total * 100).round(1)

        colors = {'Sole': '#2196F3', 'Joint': '#9C27B0', 'Trust': '#FF5722'}

        charts['account_type'] = {
            'title': 'AUA by Account Type',
            'data': [
                {
                    'label': row['account_owner_type'],
                    'value': float(row['value']),
                    'pct': float(row['pct']),
                    'count': int(row['count']),
                    'color': colors.get(row['account_owner_type'], '#9E9E9E'),
                }
                for _, row in type_agg.iterrows()
            ]
        }

    print(f"  tax_basis_breakdown.json: {len(charts)} charts")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'charts': charts,
    }


def generate_tax_deferred_candidates(accounts: pd.DataFrame, txns: pd.DataFrame) -> dict:
    """Generate list of clients who may benefit from tax-deferred strategies."""
    if 'tax_status' not in accounts.columns:
        return {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'firm_id': FIRM_ID,
            'candidates': [],
        }

    taxable = accounts[accounts['tax_status'] == 'Taxable'].copy()

    rel_agg = taxable.groupby('client_key').agg(
        relationship_id=('relationship_id', 'first'),
        display_name=('display_name', 'first'),
        taxable_aua=('emv', 'sum'),
        account_count=('account_id', 'nunique'),
        architect=('architect', 'first'),
    ).reset_index()

    MIN_AUA = 500000
    candidates = rel_agg[rel_agg['taxable_aua'] >= MIN_AUA].copy()

    # Simple priority score
    candidates['priority_score'] = (
        (candidates['taxable_aua'] >= 2000000).astype(int) * 40 +
        (candidates['taxable_aua'] >= 1000000).astype(int) * 30 +
        (candidates['taxable_aua'] >= 500000).astype(int) * 20 +
        (candidates['account_count'] >= 4).astype(int) * 20 +
        (candidates['account_count'] >= 2).astype(int) * 10 +
        30  # Base points
    )

    candidates = candidates.sort_values('priority_score', ascending=False)
    candidates['architect'] = candidates['architect'].replace('No Architect Value Assigned', 'House')

    candidate_list = [
        {
            'client_key': row['client_key'],
            'relationship_id': row['relationship_id'],
            'display_name': row['display_name'],
            'architect': row['architect'],
            'taxable_aua': float(row['taxable_aua']),
            'account_count': int(row['account_count']),
            'priority_score': int(row['priority_score']),
        }
        for _, row in candidates.head(100).iterrows()
    ]

    print(f"  tax_deferred_candidates.json: {len(candidate_list)} candidates")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'scan_criteria': {'min_taxable_aua': MIN_AUA, 'tax_status': 'Taxable'},
        'summary': {
            'total_candidates': len(candidates),
            'total_opportunity_aua': float(candidates['taxable_aua'].sum()),
        },
        'candidates': candidate_list,
    }


# =============================================================================
# STEP 5: FILTERS
# =============================================================================

def generate_filters(accounts: pd.DataFrame):
    """Generate filter dimensions JSON."""
    accounts = add_client_key(accounts)

    dimensions = {}

    def gen_dim_values(df, column, transform=None, top_n=None, include_aua=True):
        if column not in df.columns:
            return []

        df = df.copy()
        df['dim_value'] = df[column].astype(str)
        if transform:
            df['dim_value'] = df['dim_value'].replace(transform)

        df = df[df['dim_value'].notna() & (df['dim_value'] != '') &
                (df['dim_value'] != 'nan') & (df['dim_value'] != 'None')]

        agg = df.groupby('dim_value').agg(
            aua=('emv', 'sum'),
            client_count=('client_key', 'nunique'),
            account_count=('account_id', 'nunique'),
        ).reset_index()

        agg = agg.sort_values('aua', ascending=False)
        if top_n:
            agg = agg.head(top_n)

        def to_id(value):
            return str(value).lower().replace(' ', '_').replace('&', 'and').replace(',', '')

        values = []
        for _, row in agg.iterrows():
            value = {'id': to_id(row['dim_value']), 'name': row['dim_value']}
            if include_aua:
                value['aua'] = float(row['aua'])
                value['client_count'] = int(row['client_count'])
            values.append(value)

        return values

    dimensions['architect'] = {
        'label': 'Architect',
        'column': 'architect',
        'values': gen_dim_values(accounts, 'architect', {'No Architect Value Assigned': 'House'}),
    }

    dimensions['region'] = {
        'label': 'Region',
        'column': 'local_ops',
        'values': gen_dim_values(accounts, 'local_ops', {'No Local Ops Value Assigned': 'Unassigned'}),
    }

    dimensions['implementor'] = {
        'label': 'Implementor',
        'column': 'implementor',
        'values': gen_dim_values(accounts, 'implementor', {'No Implementor Value Assigned': 'Unassigned'}, top_n=50),
    }

    dimensions['account_type'] = {
        'label': 'Account Type',
        'column': 'account_owner_type',
        'values': gen_dim_values(accounts, 'account_owner_type'),
    }

    dimensions['tax_status'] = {
        'label': 'Tax Status',
        'column': 'tax_status',
        'values': gen_dim_values(accounts, 'tax_status'),
    }

    dimensions['state'] = {
        'label': 'State',
        'column': 'client_state',
        'values': gen_dim_values(accounts, 'client_state', top_n=49),
    }

    dimensions['city'] = {
        'label': 'City',
        'column': 'client_city',
        'values': gen_dim_values(accounts, 'client_city', top_n=50),
    }

    dimensions['relationship'] = {
        'label': 'Household',
        'column': 'display_name',
        'values': gen_dim_values(accounts, 'display_name', top_n=100),
    }

    filters = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'firm_id': FIRM_ID,
        'dimensions': dimensions,
    }

    print(f"  dimensions.json: {len(dimensions)} dimensions")
    save_json(filters, 'gold/filters/dimensions.json')


# =============================================================================
# STEP 6: SUMMARY
# =============================================================================

def generate_summary(accounts: pd.DataFrame, txns: pd.DataFrame):
    """Generate header metrics summary."""
    accounts = add_client_key(accounts)
    txns['trade_date'] = pd.to_datetime(txns['trade_date'])
    as_of_date = txns['trade_date'].max()

    total_aua = float(accounts['emv'].sum())
    total_clients = accounts['client_key'].nunique()
    total_accounts = accounts['account_id'].nunique()

    # Calculate NNA
    today = as_of_date
    ytd_start = datetime(today.year, 1, 1)
    ttm_start = today - timedelta(days=365)

    def calc_nna(start, end):
        NNA_INFLOW_TYPES = ['Cash Deposit', 'Transfer In', 'Wire In', 'Transfer']
        NNA_OUTFLOW_TYPES = ['Cash Withdrawal', 'Transfer Out', 'Wire Out']

        mask = (txns['trade_date'] >= pd.Timestamp(start)) & (txns['trade_date'] <= pd.Timestamp(end))
        period_txns = txns[mask]

        inflow_mask = (
            period_txns['transaction_type'].isin(NNA_INFLOW_TYPES) |
            period_txns['action'].str.contains('Deposit|Transfer In|Wire In', case=False, na=False)
        )
        outflow_mask = (
            period_txns['transaction_type'].isin(NNA_OUTFLOW_TYPES) |
            period_txns['action'].str.contains('Withdrawal|Transfer Out|Wire Out', case=False, na=False)
        )

        return float(period_txns.loc[inflow_mask, 'market_value'].sum() -
                     period_txns.loc[outflow_mask, 'market_value'].sum())

    nna_ytd = calc_nna(ytd_start, today)
    nna_12m = calc_nna(ttm_start, today)

    # Build result
    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': as_of_date.strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'firm_name': FIRM_NAME,

        'header': {
            'total_aua': {'value': total_aua, 'label': 'Total AUA', 'format': 'currency'},
            'nna_ytd': {'value': nna_ytd, 'label': 'NNA YTD', 'format': 'currency'},
        },

        'summary': {
            'total_aua': total_aua,
            'nna_ytd': nna_ytd,
            'nna_12m': nna_12m,
            'client_count': total_clients,
            'account_count': total_accounts,
        },

        'by_architect': [],
    }

    # Top architects
    if 'architect' in accounts.columns:
        accounts['architect_display'] = accounts['architect'].replace('No Architect Value Assigned', 'House')
        arch_agg = accounts.groupby('architect_display').agg(
            aua=('emv', 'sum'),
            client_count=('client_key', 'nunique'),
            account_count=('account_id', 'nunique'),
        ).reset_index().sort_values('aua', ascending=False).head(10)

        for _, row in arch_agg.iterrows():
            result['by_architect'].append({
                'architect': row['architect_display'],
                'aua': float(row['aua']),
                'aua_pct': round(row['aua'] / total_aua * 100, 1),
                'client_count': int(row['client_count']),
                'account_count': int(row['account_count']),
            })

    print(f"  Total AUA: ${total_aua:,.0f}")
    print(f"  NNA YTD: ${nna_ytd:,.0f}")
    print(f"  NNA 12M: ${nna_12m:,.0f}")
    print(f"  Clients: {total_clients:,}")

    save_json(result, 'gold/summary/header_metrics.json')
