"""
BD Portal Advisor Publisher Lambda

Triggered by: S3 ObjectCreated on opal-data-bd/gold/pipeline-complete.json
              (same sentinel as bd-portal-publisher — both run in parallel)

Reads account_performance (the large parquet, ~350MB / 10M rows) to produce:
  - implementor_leaderboard.json   (LeaderboardResponse, by implementor)
  - advisors/{advisor_id}/book.json (AdvisorBookResponse, one per architect)
  - clients/{relationship_id}.json  (ClientDetailResponse, one per client)

Separated from bd-portal-publisher because account_performance is too large
to load alongside the other tables in a single Lambda execution.

Memory: 6144 MB  Timeout: 900 s  Runtime: Python 3.12
Layer:  pandas-pyarrow-layer
"""

import gc
import json
import os
import re
from datetime import datetime, timezone
from io import BytesIO

import boto3
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_BUCKET  = os.environ.get('INPUT_BUCKET',  'opal-data-bd')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'opal-data-bd')
FIRM_ID       = os.environ.get('FIRM_ID',       '49financial')
FIRM_NAME     = os.environ.get('FIRM_NAME',     '49 Financial')

s3 = boto3.client('s3', region_name='us-east-1')

WINDOWS = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _load_parquet(key: str, columns: list = None) -> pd.DataFrame:
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {}
    if columns:
        kwargs['columns'] = columns
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _save_json(data: dict, key: str) -> None:
    body = json.dumps(data, default=str, separators=(',', ':'))
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=body.encode('utf-8'),
        ContentType='application/json',
    )
    print(f"  Wrote {key} ({len(body):,} bytes)")


def _advisor_id(name: str) -> str:
    """Convert advisor display name to URL-safe ID: 'Travis Penfield' -> 'travis_penfield'."""
    clean = re.sub(r'[^a-z0-9_]+', '_', str(name).lower().strip())
    return clean.strip('_') or 'unknown'


def _today() -> pd.Timestamp:
    return pd.Timestamp.now(tz='UTC').normalize().tz_localize(None)


def _window_start(today: pd.Timestamp, days: int) -> pd.Timestamp:
    return today - pd.Timedelta(days=days)


def _latest_holdings_lots_key() -> str | None:
    """Return the S3 key of the most recent holdings_lots snapshot."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=INPUT_BUCKET,
                                       Prefix='gold/holdings_lots/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet') and 'backfill' not in obj['Key']
    ])
    return keys[-1] if keys else None


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_sources() -> dict:
    """Load all three source parquets with column pruning."""
    print("Loading source parquets...")

    # account_performance: all dates needed for window calculations and timeseries
    acct = _load_parquet(
        'gold/account_performance.parquet',
        columns=[
            'date', 'account_id', 'relationship_id',
            'architect', 'implementor',
            'tax_status',
            'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
            'num_positions',
        ],
    )
    acct['date'] = pd.to_datetime(acct['date'])

    # client_tax_liability: for tax exposure per advisor book
    tax = _load_parquet(
        'gold/views/client_tax_liability.parquet',
        columns=[
            'relationship_id', 'account_id',
            'tax_status', 'qualified_flag',
            'asset_name', 'ticker',
            'purchase_year',
            'total_cost_basis', 'total_market_value', 'total_accrued_gain',
            'short_term_gain', 'long_term_gain',
            'num_open_lots',
        ],
    )

    # client_dimension: first_seen_date for new_clients + relationship names
    cdim = _load_parquet(
        'gold/client_dimension.parquet',
        columns=[
            'relationship_id', 'relationship_name',
            'first_seen_date',
            'primary_architect', 'primary_implementor',
        ],
    )
    cdim['first_seen_date'] = pd.to_datetime(cdim['first_seen_date'])

    # holdings_lots: latest snapshot for per-client open lot detail
    lots_key = _latest_holdings_lots_key()
    lots = pd.DataFrame()
    if lots_key:
        lots = _load_parquet(lots_key)
    else:
        print("  WARNING: no holdings_lots snapshot found")

    gc.collect()
    return dict(acct=acct, tax=tax, cdim=cdim, lots=lots)


# ---------------------------------------------------------------------------
# Shared computation helpers
# ---------------------------------------------------------------------------

def _snapshot_on(df: pd.DataFrame, date: pd.Timestamp, dim_col: str) -> pd.DataFrame:
    """Return a snapshot of df grouped by dim_col on the closest available date <= date."""
    dates_available = df['date'].unique()
    past = dates_available[dates_available <= date]
    snap_date = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates_available.min())
    snap = df[df['date'] == snap_date]
    return snap.groupby(dim_col).agg(
        total_aua=('total_aua', 'sum'),
        cum_inflows=('cum_inflows', 'sum'),
        cum_outflows=('cum_outflows', 'sum'),
        nna=('nna', 'sum'),
        num_accounts=('account_id', 'nunique'),
        num_relationships=('relationship_id', 'nunique'),
    ).reset_index()


def _nna_for_window(acct_dim: pd.DataFrame, dim_col: str, dim_val: str,
                     today: pd.Timestamp, days: int) -> float:
    """
    NNA for one advisor over a window.
    acct_dim is already filtered to this advisor's rows.
    NNA = (cum_inflows - cum_outflows) at end_date - at start_date, summed across accounts.
    """
    sub = acct_dim.copy()
    dates = sub['date'].sort_values().unique()
    end_date   = pd.Timestamp(dates.max())
    start_date = _window_start(today, days)

    past = dates[dates <= start_date]
    snap_start = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates.min())

    end_vals   = sub[sub['date'] == end_date].agg(
        cum_inflows=('cum_inflows', 'sum'), cum_outflows=('cum_outflows', 'sum'))
    start_vals = sub[sub['date'] == snap_start].agg(
        cum_inflows=('cum_inflows', 'sum'), cum_outflows=('cum_outflows', 'sum'))

    inflow_delta  = float(end_vals['cum_inflows'])  - float(start_vals['cum_inflows'])
    outflow_delta = float(end_vals['cum_outflows']) - float(start_vals['cum_outflows'])
    return inflow_delta - outflow_delta


# ---------------------------------------------------------------------------
# 1. Implementor leaderboard  (LeaderboardResponse)
# ---------------------------------------------------------------------------

def build_implementor_leaderboard(acct: pd.DataFrame, cdim: pd.DataFrame,
                                   today: pd.Timestamp) -> dict:
    """
    Same structure as architect_leaderboard from bd-portal-publisher.
    Uses account_performance grouped by implementor.
    """
    print("Building implementor_leaderboard.json...")

    latest_date = acct['date'].max()
    windows_data = {}

    for label, days in WINDOWS.items():
        w_start = _window_start(today, days)
        dates   = acct['date'].sort_values().unique()
        past    = dates[dates <= w_start]
        snap_start = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates.min())

        end_snap   = _snapshot_on(acct, latest_date, 'implementor')
        start_snap = _snapshot_on(acct, snap_start,  'implementor').set_index('implementor')

        entries = []
        for _, row in end_snap.iterrows():
            impl = str(row['implementor'])
            if not impl or impl.lower() in ('', 'nan', 'none', 'unassigned',
                                             'no implementor value assigned'):
                impl = 'Unassigned'

            total_aua     = float(row['total_aua'])
            client_count  = int(row['num_relationships'])
            account_count = int(row['num_accounts'])

            s_row      = start_snap.loc[impl] if impl in start_snap.index else None
            nna_end    = float(row['nna'])
            nna_start  = float(s_row['nna']) if s_row is not None else 0.0
            nna_window = nna_end - nna_start

            aua_start_val  = float(s_row['total_aua']) if s_row is not None else 0.0
            aua_growth_pct = (
                (total_aua - aua_start_val) / aua_start_val * 100
                if aua_start_val > 0 else 0.0
            )

            # New clients (relationships) whose primary_implementor matches and joined in window
            cdim_match = cdim[cdim['primary_implementor'] == impl]
            new_clients = int((cdim_match['first_seen_date'] >= w_start).sum())

            entries.append({
                'name':            impl,
                'nna':             round(nna_window, 2),
                'aua_growth_pct':  round(aua_growth_pct, 2),
                'new_clients':     new_clients,
                'total_aua':       round(total_aua, 2),
                'client_count':    client_count,
                'account_count':   account_count,
            })

        entries.sort(key=lambda x: x['nna'], reverse=True)
        for i, e in enumerate(entries):
            e['rank'] = i + 1

        total_nna = sum(e['nna'] for e in entries)
        total_aua_all = sum(e['total_aua'] for e in entries)
        windows_data[label] = {
            'entry_count': len(entries),
            'summary': {
                'total_nna':            round(total_nna, 2),
                'total_aua':            round(total_aua_all, 2),
                'total_new_clients':    sum(e['new_clients'] for e in entries),
                'positive_nna_count':   sum(1 for e in entries if e['nna'] >= 0),
                'negative_nna_count':   sum(1 for e in entries if e['nna'] < 0),
            },
            'entries': entries,
        }
        print(f"  Window {label}: {len(entries)} implementors")

    return {
        'generated_at':     datetime.now(timezone.utc).isoformat(),
        'data_as_of':       latest_date.strftime('%Y-%m-%d'),
        'firm_id':          FIRM_ID,
        'leaderboard_type': 'implementor',
        'available_windows': list(WINDOWS.keys()),
        'windows':          windows_data,
    }


# ---------------------------------------------------------------------------
# 2. Per-advisor book files  (AdvisorBookResponse)
# ---------------------------------------------------------------------------

def _build_advisor_tax_exposure(tax: pd.DataFrame, rel_ids: set) -> dict:
    """Tax exposure for a book of relationships from client_tax_liability."""
    book_tax = tax[tax['relationship_id'].isin(rel_ids)]

    if book_tax.empty:
        return {
            'taxable': 0.0, 'taxable_pct': 0.0,
            'tax_deferred': 0.0, 'tax_deferred_pct': 0.0,
            'tax_free': 0.0, 'tax_free_pct': 0.0,
            'qualified_aua': 0.0, 'qualified_pct': 0.0,
            'non_qualified_aua': 0.0, 'non_qualified_pct': 0.0,
            'non_qualified_cost_basis': 0.0,
            'non_qualified_unrealized_gain': 0.0,
            'short_term_gain': 0.0,
            'long_term_gain': 0.0,
        }

    taxable_mv  = float(book_tax.loc[book_tax['tax_status'] == 'taxable',
                                      'total_market_value'].sum())
    deferred_mv = float(book_tax.loc[book_tax['tax_status'] == 'tax_deferred',
                                      'total_market_value'].sum())
    exempt_mv   = float(book_tax.loc[book_tax['tax_status'] == 'tax_exempt',
                                      'total_market_value'].sum())
    total_mv    = taxable_mv + deferred_mv + exempt_mv

    qual_mv    = float(book_tax.loc[book_tax['qualified_flag'] == True,
                                     'total_market_value'].sum())
    nonqual_mv = float(book_tax.loc[book_tax['qualified_flag'] == False,
                                     'total_market_value'].sum())

    taxable_only = book_tax[book_tax['tax_status'] == 'taxable']
    nq_cost_basis   = float(taxable_only['total_cost_basis'].sum())
    nq_unreal_gain  = float(taxable_only['total_accrued_gain'].sum())
    st_gain         = float(taxable_only['short_term_gain'].sum())
    lt_gain         = float(taxable_only['long_term_gain'].sum())

    def pct(v): return round(v / total_mv * 100, 1) if total_mv > 0 else 0.0
    lot_total = qual_mv + nonqual_mv

    return {
        'taxable':                      round(taxable_mv, 2),
        'taxable_pct':                  pct(taxable_mv),
        'tax_deferred':                 round(deferred_mv, 2),
        'tax_deferred_pct':             pct(deferred_mv),
        'tax_free':                     round(exempt_mv, 2),
        'tax_free_pct':                 pct(exempt_mv),
        'qualified_aua':                round(qual_mv, 2),
        'qualified_pct':                round(qual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0,
        'non_qualified_aua':            round(nonqual_mv, 2),
        'non_qualified_pct':            round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0,
        'non_qualified_cost_basis':     round(nq_cost_basis, 2),
        'non_qualified_unrealized_gain': round(nq_unreal_gain, 2),
        'short_term_gain':              round(st_gain, 2),
        'long_term_gain':               round(lt_gain, 2),
    }


def _build_advisor_engagement(acct_book: pd.DataFrame, cdim: pd.DataFrame,
                               rel_ids: set, today: pd.Timestamp) -> dict:
    """Engagement metrics for one advisor's book."""
    ttm_cutoff = today - pd.Timedelta(days=365)
    dates = acct_book['date'].sort_values().unique()
    latest_date = pd.Timestamp(dates.max())

    past_ttm = dates[dates <= ttm_cutoff]
    ttm_start_date = (pd.Timestamp(past_ttm.max()) if len(past_ttm) > 0
                      else pd.Timestamp(dates.min()))

    end_snap   = acct_book[acct_book['date'] == latest_date]
    start_snap = acct_book[acct_book['date'] == ttm_start_date]

    inflows_ttm  = float(end_snap['cum_inflows'].sum())  - float(start_snap['cum_inflows'].sum())
    outflows_ttm = float(end_snap['cum_outflows'].sum()) - float(start_snap['cum_outflows'].sum())
    net_flows_ttm = inflows_ttm - outflows_ttm

    # Average tenure: days since first_seen_date for matching relationships
    book_cdim = cdim[cdim['relationship_id'].isin(rel_ids)]
    avg_tenure_days = 0
    if not book_cdim.empty and book_cdim['first_seen_date'].notna().any():
        tenure = (today - book_cdim['first_seen_date'].dropna()).dt.days
        avg_tenure_days = int(tenure.mean()) if len(tenure) > 0 else 0

    return {
        'net_flows_ttm':   round(net_flows_ttm, 2),
        'inflows_ttm':     round(inflows_ttm, 2),
        'outflows_ttm':    round(outflows_ttm, 2),
        'avg_tenure_days': avg_tenure_days,
    }


def build_advisor_books(acct: pd.DataFrame, tax: pd.DataFrame,
                         cdim: pd.DataFrame, today: pd.Timestamp) -> list:
    """
    Build one AdvisorBookResponse per architect and return a list of (key, dict) pairs.
    """
    print("Building advisor book files...")

    latest_date  = acct['date'].max()
    all_dates    = acct['date'].sort_values().unique()

    # Identify all architect values present in latest snapshot
    latest_snap = acct[acct['date'] == latest_date]
    architects  = latest_snap['architect'].dropna().unique().tolist()
    print(f"  {len(architects)} architects to process")

    # Pre-compute quarterly NNA start dates
    def _qstart(quarters_back: int) -> pd.Timestamp:
        today_q_month = ((today.month - 1) // 3) * 3 + 1
        month = today_q_month - quarters_back * 3
        year  = today.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        return pd.Timestamp(year=year, month=month, day=1)

    ytd_start = pd.Timestamp(today.year, 1, 1)
    qtd_start = _qstart(0)
    mtd_start = pd.Timestamp(today.year, today.month, 1)

    books = []

    for architect in architects:
        arch_str = str(architect)
        adv_id   = _advisor_id(arch_str)

        # All rows for this architect across all dates
        acct_arch = acct[acct['architect'] == architect]
        if acct_arch.empty:
            continue

        # Relationships in this book (from latest snapshot)
        rel_ids = set(latest_snap.loc[latest_snap['architect'] == architect,
                                       'relationship_id'].unique())

        # ---- Summary (latest date) ----
        snap_latest = acct_arch[acct_arch['date'] == latest_date]
        total_aua     = float(snap_latest['total_aua'].sum())
        account_count = int(snap_latest['account_id'].nunique())
        client_count  = int(snap_latest['relationship_id'].nunique())

        # ---- NNA (ytd / qtd / mtd) ----
        def _nna_since(start_ts: pd.Timestamp) -> float:
            past = all_dates[all_dates <= start_ts]
            snap_start_date = (pd.Timestamp(past.max()) if len(past) > 0
                               else pd.Timestamp(all_dates.min()))
            end_v   = acct_arch[acct_arch['date'] == latest_date]
            start_v = acct_arch[acct_arch['date'] == snap_start_date]
            inf_d  = float(end_v['cum_inflows'].sum())  - float(start_v['cum_inflows'].sum())
            out_d  = float(end_v['cum_outflows'].sum()) - float(start_v['cum_outflows'].sum())
            return inf_d - out_d

        nna_ytd = _nna_since(ytd_start)
        nna_qtd = _nna_since(qtd_start)
        nna_mtd = _nna_since(mtd_start)

        # ---- AUA growth (YTD, QTD) ----
        def _aua_at(start_ts: pd.Timestamp) -> float:
            past = all_dates[all_dates <= start_ts]
            snap_date = (pd.Timestamp(past.max()) if len(past) > 0
                         else pd.Timestamp(all_dates.min()))
            rows = acct_arch[acct_arch['date'] == snap_date]
            return float(rows['total_aua'].sum())

        aua_ytd_start = _aua_at(ytd_start)
        aua_qtd_start = _aua_at(qtd_start)
        ytd_growth_pct = ((total_aua - aua_ytd_start) / aua_ytd_start * 100
                          if aua_ytd_start > 0 else 0.0)
        qtd_growth_pct = ((total_aua - aua_qtd_start) / aua_qtd_start * 100
                          if aua_qtd_start > 0 else 0.0)

        # ---- Tax exposure ----
        tax_exposure = _build_advisor_tax_exposure(tax, rel_ids)

        # ---- Engagement ----
        engagement = _build_advisor_engagement(acct_arch, cdim, rel_ids, today)

        # ---- Client list (sorted by AUA desc) ----
        client_snap = (
            snap_latest
            .groupby('relationship_id')['total_aua']
            .sum()
            .reset_index()
            .merge(cdim[['relationship_id', 'relationship_name']],
                   on='relationship_id', how='left')
            .sort_values('total_aua', ascending=False)
        )
        clients = [
            {
                'client_key':  str(r['relationship_id']),
                'client_name': (str(r['relationship_name'])
                                if pd.notna(r['relationship_name'])
                                else str(r['relationship_id'])),
                'aua': round(float(r['total_aua']), 2),
            }
            for _, r in client_snap.iterrows()
        ]

        book = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'data_as_of':   latest_date.strftime('%Y-%m-%d'),

            'book_type': 'architect',
            'book_key':  adv_id,
            'book_name': arch_str,

            'summary': {
                'total_aua':    round(total_aua, 2),
                'client_count': client_count,
                'account_count': account_count,
            },

            'nna': {
                'ytd': round(nna_ytd, 2),
                'qtd': round(nna_qtd, 2),
                'mtd': round(nna_mtd, 2),
            },

            'growth': {
                'ytd_pct': round(ytd_growth_pct, 2),
                'qtd_pct': round(qtd_growth_pct, 2),
            },

            # Tax exposure from client_tax_liability
            # Includes Yang's qualified/non-qualified and cost basis fields
            'tax_exposure': tax_exposure,

            # Income & fees: not available from BD data
            'income_fees': {
                'income_total_ttm':      0.0,
                'avg_income_yield_pct':  0.0,
                'fees_total_ttm':        0.0,
                'avg_fee_rate_pct':      0.0,
            },

            # Portfolio composition: asset class taxonomy not in BD data
            'portfolio_composition': {
                'asset_allocation':  [],
                'avg_expense_ratio': 0.0,
            },

            'engagement': engagement,
            'clients':    clients,
        }

        books.append((_advisor_output_key(adv_id), book))
        print(f"  {arch_str}: AUA=${total_aua:,.0f}, {client_count} clients, "
              f"{account_count} accounts, NNA_YTD=${nna_ytd:,.0f}")

    return books


def _advisor_output_key(adv_id: str) -> str:
    return f'gold/advisors/{adv_id}/book.json'


# ---------------------------------------------------------------------------
# 3. Per-client detail files  (ClientDetailResponse)
# ---------------------------------------------------------------------------

def _build_headline(acct: pd.DataFrame) -> dict:
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date]
    return {
        'total_aua':        round(float(snap['total_aua'].sum()), 2),
        'account_count':    int(snap['account_id'].nunique()),
        'client_count':     1,
        'fee_rate_pct':     0.0,
        'income_yield_pct': 0.0,
    }


def _build_tax(acct: pd.DataFrame, tax: pd.DataFrame, lots: pd.DataFrame,
               today: pd.Timestamp) -> dict:
    """Full tax section for one household."""
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date]

    total_aua    = float(snap['total_aua'].sum())
    aua_taxable  = float(snap.loc[snap['tax_status'] == 'taxable',   'total_aua'].sum())
    aua_deferred = float(snap.loc[snap['tax_status'] == 'tax_deferred', 'total_aua'].sum())
    aua_exempt   = float(snap.loc[snap['tax_status'] == 'tax_exempt', 'total_aua'].sum())

    def pct(v): return round(v / total_aua * 100, 1) if total_aua > 0 else 0.0

    # --- Qualified vs non-qualified from client_tax_liability ---
    tax_qual    = tax[tax['qualified_flag'] == True]
    tax_nonqual = tax[tax['qualified_flag'] == False]
    tax_taxable = tax[tax['tax_status'] == 'taxable']

    qual_mv    = float(tax_qual['total_market_value'].sum())
    nonqual_mv = float(tax_nonqual['total_market_value'].sum())
    lot_total  = qual_mv + nonqual_mv

    qual_pct    = round(qual_mv    / lot_total * 100, 1) if lot_total > 0 else 0.0
    nonqual_pct = round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0

    qual_acct_count    = int(tax_qual['account_id'].nunique())
    nonqual_acct_count = int(tax_nonqual['account_id'].nunique())

    nq_cost_basis  = float(tax_taxable['total_cost_basis'].sum())
    nq_market_val  = float(tax_taxable['total_market_value'].sum())
    nq_unrealized  = float(tax_taxable['total_accrued_gain'].sum())
    st_gain        = float(tax_taxable['short_term_gain'].sum())
    lt_gain        = float(tax_taxable['long_term_gain'].sum())

    # --- Cost basis by purchase year ---
    year_cols = ['purchase_year', 'total_cost_basis', 'total_market_value',
                 'total_accrued_gain', 'short_term_gain', 'long_term_gain', 'asset_name']
    year_cols_avail = [c for c in year_cols if c in tax_taxable.columns]
    if not tax_taxable.empty and 'purchase_year' in tax_taxable.columns:
        year_agg = (
            tax_taxable[year_cols_avail]
            .groupby('purchase_year', dropna=False)
            .agg(
                cost_basis=('total_cost_basis', 'sum'),
                market_value=('total_market_value', 'sum'),
                unrealized_gain=('total_accrued_gain', 'sum'),
                short_term_gain=('short_term_gain', 'sum'),
                long_term_gain=('long_term_gain', 'sum'),
                num_positions=('asset_name', 'nunique'),
            )
            .reset_index()
            .sort_values('purchase_year')
        )
        cost_basis_by_year = [
            {
                'purchase_year':   int(r['purchase_year']) if pd.notna(r['purchase_year']) else None,
                'cost_basis':      round(float(r['cost_basis']), 2),
                'market_value':    round(float(r['market_value']), 2),
                'unrealized_gain': round(float(r['unrealized_gain']), 2),
                'short_term_gain': round(float(r['short_term_gain']), 2),
                'long_term_gain':  round(float(r['long_term_gain']), 2),
                'num_positions':   int(r['num_positions']),
            }
            for _, r in year_agg.iterrows()
        ]
    else:
        cost_basis_by_year = []

    # --- Top gain positions ---
    if not tax_taxable.empty and 'asset_name' in tax_taxable.columns:
        pos_agg = (
            tax_taxable
            .groupby(['asset_name', 'ticker'], dropna=False)
            .agg(
                cost_basis=('total_cost_basis', 'sum'),
                market_value=('total_market_value', 'sum'),
                unrealized_gain=('total_accrued_gain', 'sum'),
                short_term_gain=('short_term_gain', 'sum'),
                long_term_gain=('long_term_gain', 'sum'),
                num_lots=('num_open_lots', 'sum'),
            )
            .reset_index()
            .sort_values('unrealized_gain', ascending=False)
            .head(20)
        )
        top_gain_positions = [
            {
                'asset_name':      str(r['asset_name']),
                'ticker':          str(r['ticker']) if pd.notna(r['ticker']) else None,
                'cost_basis':      round(float(r['cost_basis']), 2),
                'market_value':    round(float(r['market_value']), 2),
                'unrealized_gain': round(float(r['unrealized_gain']), 2),
                'short_term_gain': round(float(r['short_term_gain']), 2),
                'long_term_gain':  round(float(r['long_term_gain']), 2),
                'num_lots':        int(r['num_lots']),
            }
            for _, r in pos_agg.iterrows()
        ]
    else:
        top_gain_positions = []

    # --- Open lots (taxable only) ---
    open_lots = []
    if not lots.empty:
        taxable_open = lots[
            lots.get('is_open', pd.Series(True, index=lots.index)) == True
        ]
        if 'tax_status' in taxable_open.columns:
            taxable_open = taxable_open[taxable_open['tax_status'] == 'taxable']

        sort_cols = [c for c in ['account_id', 'asset_name', 'lot_index']
                     if c in taxable_open.columns]
        if sort_cols:
            taxable_open = taxable_open.sort_values(sort_cols)

        lot_cols = [
            'account_id', 'account_name',
            'asset_name', 'ticker',
            'acquisition_date', 'purchase_year', 'lot_index',
            'current_units', 'cost_per_unit', 'cost_basis',
            'current_price', 'market_value', 'accrued_gain',
            'holding_period_days', 'term',
        ]
        available = [c for c in lot_cols if c in taxable_open.columns]

        for _, row in taxable_open[available].iterrows():
            lot = {}
            for col in available:
                val = row[col]
                if isinstance(val, (pd.Timestamp,)):
                    lot[col] = val.strftime('%Y-%m-%d')
                elif isinstance(val, float) and pd.notna(val):
                    lot[col] = round(val, 4)
                elif pd.isna(val) if not isinstance(val, str) else False:
                    lot[col] = None
                else:
                    lot[col] = val
            open_lots.append(lot)

    return {
        'taxable':          round(aua_taxable, 2),
        'taxable_pct':      pct(aua_taxable),
        'tax_deferred':     round(aua_deferred, 2),
        'tax_deferred_pct': pct(aua_deferred),
        'tax_free':         round(aua_exempt, 2),
        'tax_free_pct':     pct(aua_exempt),
        'capital_gains_ttm': round(nq_unrealized, 2),
        'qualified_aua':               round(qual_mv, 2),
        'qualified_pct':               qual_pct,
        'non_qualified_aua':           round(nonqual_mv, 2),
        'non_qualified_pct':           nonqual_pct,
        'qualified_account_count':     qual_acct_count,
        'non_qualified_account_count': nonqual_acct_count,
        'non_qualified_cost_basis':      round(nq_cost_basis, 2),
        'non_qualified_market_value':    round(nq_market_val, 2),
        'non_qualified_unrealized_gain': round(nq_unrealized, 2),
        'short_term_gain':               round(st_gain, 2),
        'long_term_gain':                round(lt_gain, 2),
        'cost_basis_by_year': cost_basis_by_year,
        'top_gain_positions': top_gain_positions,
        'open_lots': open_lots,
        'open_lots_count': len(open_lots),
    }


def _build_engagement(acct: pd.DataFrame, cdim_row, today: pd.Timestamp) -> dict:
    """NNA flows TTM and relationship tenure."""
    dates = acct['date'].sort_values().unique()
    latest_date = pd.Timestamp(dates.max())

    ttm_cutoff = today - pd.Timedelta(days=365)
    past_ttm   = dates[dates <= ttm_cutoff]
    ttm_start  = (pd.Timestamp(past_ttm.max()) if len(past_ttm) > 0
                  else pd.Timestamp(dates.min()))

    end_snap   = acct[acct['date'] == latest_date]
    start_snap = acct[acct['date'] == ttm_start]

    inflows_ttm  = float(end_snap['cum_inflows'].sum())  - float(start_snap['cum_inflows'].sum())
    outflows_ttm = float(end_snap['cum_outflows'].sum()) - float(start_snap['cum_outflows'].sum())
    net_flows_ttm = inflows_ttm - outflows_ttm

    avg_relationship_years = 0.0
    if cdim_row is not None and pd.notna(cdim_row.get('first_seen_date')):
        days = (today - cdim_row['first_seen_date']).days
        avg_relationship_years = round(days / 365.25, 2)

    return {
        'trading_buys_ttm':      0,
        'trading_sells_ttm':     0,
        'net_flows_ttm':         round(net_flows_ttm, 2),
        'avg_relationship_years': avg_relationship_years,
        'active_clients_pct':    100.0,
    }


def _build_accounts(acct: pd.DataFrame) -> list:
    """Per-account breakdown for the household drill-down panel."""
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date].copy()

    accounts = []
    for _, row in snap.sort_values('total_aua', ascending=False).iterrows():
        accounts.append({
            'account_id':    str(row['account_id']),
            'tax_status':    str(row.get('tax_status', 'taxable')),
            'total_aua':     round(float(row['total_aua']), 2),
            'cum_inflows':   round(float(row['cum_inflows']), 2),
            'cum_outflows':  round(float(row['cum_outflows']), 2),
            'nna':           round(float(row['nna']), 2),
            'num_positions': int(row.get('num_positions', 0)),
        })
    return accounts


def build_client_details(acct: pd.DataFrame, tax: pd.DataFrame,
                         lots: pd.DataFrame, cdim: pd.DataFrame,
                         today: pd.Timestamp) -> int:
    """Pre-generate gold/clients/{relationship_id}.json for every client."""
    print("Building client detail files...")

    latest_date = acct['date'].max()
    latest_snap = acct[acct['date'] == latest_date]
    all_rel_ids = latest_snap['relationship_id'].dropna().unique()
    print(f"  {len(all_rel_ids)} clients to process")

    count = 0
    for rel_id in all_rel_ids:
        rel_id_str = str(rel_id)

        # Filter each source to this relationship
        acct_r = acct[acct['relationship_id'] == rel_id].copy()
        tax_r  = tax[tax['relationship_id'] == rel_id].copy() if not tax.empty else pd.DataFrame()
        lots_r = lots[lots['relationship_id'] == rel_id].copy() if not lots.empty else pd.DataFrame()
        cdim_rows = cdim[cdim['relationship_id'] == rel_id]
        cdim_row  = cdim_rows.iloc[0] if len(cdim_rows) > 0 else None

        if acct_r.empty:
            continue

        # Client name
        client_name = rel_id_str
        if cdim_row is not None and pd.notna(cdim_row.get('relationship_name')):
            client_name = str(cdim_row['relationship_name'])

        # Build response sections
        headline   = _build_headline(acct_r)
        tax_sec    = _build_tax(acct_r, tax_r, lots_r, today)
        engagement = _build_engagement(acct_r, cdim_row, today)
        accounts   = _build_accounts(acct_r)

        response = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'data_as_of':   latest_date.strftime('%Y-%m-%d'),
            'firm_id':      FIRM_ID,
            'client_key':   rel_id_str,
            'client_name':  client_name,
            'headline':     headline,
            'tax':          tax_sec,
            'income_fees': {
                'dividends_ttm': 0.0, 'interest_ttm': 0.0,
                'total_income_ttm': 0.0, 'income_yield_pct': 0.0,
                'management_fees_ttm': 0.0, 'fee_rate_pct': 0.0,
            },
            'portfolio': {
                'allocation': [],
                'weighted_expense_ratio': 0.0,
                'unique_holdings': int(acct_r[acct_r['date'] == latest_date]['num_positions'].sum()),
                'top_5_concentration_pct': 0.0,
            },
            'engagement': engagement,
            'accounts':   accounts,
        }

        _save_json(response, f'gold/clients/{rel_id_str}.json')
        count += 1

    print(f"  Wrote {count} client detail files")
    return count


# ---------------------------------------------------------------------------
# Lambda handler
# ---------------------------------------------------------------------------

def lambda_handler(event, context):
    print("=" * 70)
    print("BD PORTAL ADVISOR PUBLISHER")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")
    print("=" * 70)

    today = _today()

    try:
        # ------------------------------------------------------------------
        # Step 1: Load parquets
        # ------------------------------------------------------------------
        print("\n=== Step 1: Load parquets ===")
        data = load_sources()
        acct = data['acct']
        tax  = data['tax']
        cdim = data['cdim']
        lots = data['lots']

        # ------------------------------------------------------------------
        # Step 2: Implementor leaderboard
        # ------------------------------------------------------------------
        print("\n=== Step 2: Implementor leaderboard ===")
        impl_lb = build_implementor_leaderboard(acct, cdim, today)
        _save_json(impl_lb, 'gold/implementor_leaderboard.json')

        # ------------------------------------------------------------------
        # Step 3: Per-advisor book files
        # ------------------------------------------------------------------
        print("\n=== Step 3: Advisor book files ===")
        books = build_advisor_books(acct, tax, cdim, today)

        for key, book_data in books:
            _save_json(book_data, key)

        # ------------------------------------------------------------------
        # Step 4: Per-client detail JSONs
        # ------------------------------------------------------------------
        print("\n=== Step 4: Client detail files ===")
        client_count = build_client_details(acct, tax, lots, cdim, today)

        # ------------------------------------------------------------------
        # Step 5: Summary
        # ------------------------------------------------------------------
        latest_date = acct['date'].max()
        total_aua   = float(acct[acct['date'] == latest_date]['total_aua'].sum())

        print(f"\n=== Step 5: Complete ===")
        print(f"  Implementor leaderboard: written")
        print(f"  Advisor books:           {len(books)} files")
        print(f"  Client details:          {client_count} files")
        print(f"  Data as of:              {latest_date.date()}")
        print(f"  Total AUA (acct grain):  ${total_aua:,.0f}")
        print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 70)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':       'success',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'data_as_of':   latest_date.strftime('%Y-%m-%d'),
                'total_aua':    round(total_aua, 2),
                'advisor_books_written': len(books),
                'client_details_written': client_count,
            }),
        }

    except Exception as exc:
        import traceback
        print(f"\nFATAL: {exc}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'error', 'error': str(exc)}),
        }
