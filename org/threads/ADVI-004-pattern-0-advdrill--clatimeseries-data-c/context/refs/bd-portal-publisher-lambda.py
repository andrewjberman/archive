"""
BD Portal Publisher Lambda

Triggered by: S3 ObjectCreated on opal-data-bd/gold/pipeline-complete.json
              (written by bd-gold-layer-runner EC2 at end of gold pipeline run)

Reads validated gold parquets, generates all aggregate static JSON files
consumed by the Advisor Intelligence portal (Leaderboard tab + Clients tab).

Outputs (all written to opal-data-bd):
  gold/timeseries_chart.json              -> CumulativeChartResponse
  gold/architect_leaderboard.json         -> LeaderboardResponse
  gold/clients_tab.json                   -> ClientsTabResponse (with Yang tax fields)
  gold/summary/header_metrics.json        -> HeaderMetricsResponse
  gold/partner_analytics/header_metrics.json -> PartnerAnalyticsResponse
  gold/filters/dimensions.json            -> FiltersResponse
  gold/snapshots/aua_by_architect.json    -> SnapshotResponse
  gold/snapshots/aua_by_state.json        -> SnapshotResponse
  gold/snapshots/aua_by_tax_status.json   -> SnapshotResponse
  gold/snapshots/aua_by_region.json       -> SnapshotResponse

Memory: 4096 MB  Timeout: 900 s  Runtime: Python 3.12
Layer:  pandas-pyarrow-layer
"""

import gc
import json
import os
from datetime import datetime, date, timedelta, timezone
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

# Time windows for leaderboard (label -> calendar days)
WINDOWS = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}

# Top N architects/states to show individually; rest collapse to "Other"
TOP_N_ADV = 8
TOP_N_GEO = 8

# For filters/snapshots
TOP_N_CITIES      = 50
TOP_N_IMPLEMENTOR = 50
TOP_N_STATE       = 49
TOP_N_RELATIONSHIP = 100

# Top positions by unrealized gain shown in tax section
TOP_GAIN_POSITIONS = 20


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _load_parquet(key: str, columns: list = None) -> pd.DataFrame:
    """Load a parquet from INPUT_BUCKET into a DataFrame."""
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {}
    if columns:
        kwargs['columns'] = columns
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _load_latest_parquet_in_prefix(prefix: str, columns: list = None) -> pd.DataFrame:
    """Load the lexicographically latest .parquet file under a prefix."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=INPUT_BUCKET, Prefix=prefix)
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])
    if not keys:
        raise RuntimeError(f"No parquet files found at s3://{INPUT_BUCKET}/{prefix}")
    return _load_parquet(keys[-1], columns=columns)


def _save_json(data: dict, key: str) -> None:
    """Write a dict as JSON to OUTPUT_BUCKET."""
    body = json.dumps(data, default=str, separators=(',', ':'))
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=body.encode('utf-8'),
        ContentType='application/json',
    )
    print(f"  Wrote {key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def _today() -> pd.Timestamp:
    return pd.Timestamp.now(tz='UTC').normalize().tz_localize(None)


def _window_start(days: int) -> pd.Timestamp:
    return _today() - pd.Timedelta(days=days)


def _find_nearest(series: pd.Series, target: pd.Timestamp) -> pd.Timestamp:
    """Return the value in series closest to target (always <= target)."""
    candidates = series[series <= target]
    if candidates.empty:
        return series.min()
    return candidates.max()


def _quarter_start(ref: pd.Timestamp, quarters_back: int) -> pd.Timestamp:
    """Return the first day of the quarter that is `quarters_back` quarters before ref."""
    q = (ref.month - 1) // 3 - quarters_back
    year = ref.year + q // 4
    q = q % 4
    return pd.Timestamp(year=year, month=q * 3 + 1, day=1)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_all(today: pd.Timestamp) -> dict:
    """
    Load all source parquets once and return as a dict.
    Column pruning reduces memory — only load what each output needs.
    """
    print("Loading gold parquets...")

    perf = _load_parquet(
        'gold/client_performance.parquet',
        columns=['date', 'relationship_id',
                 'total_aua', 'aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
                 'cum_inflows', 'cum_outflows', 'nna',
                 'num_accounts', 'num_positions', 'pct_priced'],
    )
    perf['date'] = pd.to_datetime(perf['date'])

    adv = _load_parquet(
        'gold/views/nna_aua_by_advisor.parquet',
        columns=['date', 'architect',
                 'total_aua', 'aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
                 'cum_inflows', 'cum_outflows', 'nna',
                 'num_relationships', 'num_accounts'],
    )
    adv['date'] = pd.to_datetime(adv['date'])

    geo = _load_parquet(
        'gold/views/nna_aua_by_geography.parquet',
        columns=['date', 'state', 'country',
                 'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
                 'num_relationships', 'num_accounts'],
    )
    geo['date'] = pd.to_datetime(geo['date'])

    cdim = _load_parquet(
        'gold/client_dimension.parquet',
        columns=['relationship_id', 'relationship_name', 'first_seen_date',
                 'primary_architect', 'primary_implementor',
                 'primary_state', 'primary_country',
                 'total_accounts', 'active_accounts',
                 'has_taxable', 'has_tax_deferred', 'has_tax_exempt'],
    )
    cdim['first_seen_date'] = pd.to_datetime(cdim['first_seen_date'])

    adim = _load_parquet(
        'gold/accounts_dimension_latest.parquet',
        columns=['account_id', 'relationship_id', 'account_name',
                 'architect', 'implementor', 'local_relationship',
                 'tax_status', 'qualified_flag',
                 'client_state', 'client_country',
                 'account_type', 'account_is_open'],
    )

    tax = _load_parquet(
        'gold/views/client_tax_liability.parquet',
        columns=['relationship_id', 'account_id',
                 'tax_status', 'qualified_flag',
                 'asset_name', 'ticker',
                 'purchase_year',
                 'total_units', 'total_cost_basis', 'total_market_value', 'total_accrued_gain',
                 'short_term_cost_basis', 'short_term_market_value', 'short_term_gain',
                 'long_term_cost_basis', 'long_term_market_value', 'long_term_gain',
                 'num_open_lots'],
    )

    # City-level geography for geo_drill in timeseries_chart.json
    # Optional: gracefully handle case where the file doesn't exist yet
    try:
        geo_city = _load_parquet(
            'gold/views/nna_aua_by_geography_city.parquet',
            columns=['date', 'state', 'city', 'total_aua',
                     'cum_inflows', 'cum_outflows', 'nna',
                     'num_relationships'],
        )
        geo_city['date'] = pd.to_datetime(geo_city['date'])
    except Exception as e:
        print(f"  WARN: nna_aua_by_geography_city.parquet not available ({e}) -- geo_drill skipped")
        geo_city = None

    gc.collect()

    return dict(perf=perf, adv=adv, geo=geo, geo_city=geo_city,
                cdim=cdim, adim=adim, tax=tax)


# ---------------------------------------------------------------------------
# 1. timeseries_chart.json  (CumulativeChartResponse)
# ---------------------------------------------------------------------------

def build_timeseries_chart(perf: pd.DataFrame, adv: pd.DataFrame, geo: pd.DataFrame,
                            cdim: pd.DataFrame, today: pd.Timestamp,
                            geo_city: pd.DataFrame = None) -> dict:
    """
    4+1 views, daily data points:
      aua       -- cumulative NMNC vs NMEC stacked
      nna       -- cumulative firm-level NNA
      geo       -- cumulative AUA by top states (stacked)
      adv       -- cumulative AUA by top architects (stacked)
      geo_drill -- per-state city-level AUA timeseries (optional)
    """
    print("Building timeseries_chart.json...")

    # ---- Metadata: new_clients per window ----
    new_clients_meta = {}
    for label, days in WINDOWS.items():
        cutoff = today - pd.Timedelta(days=days)
        new_clients_meta[label] = int((cdim['first_seen_date'] >= cutoff).sum())

    # ---- AUA view (New Clients / Existing Clients) ----
    # Use actual total_aua (market-valued) per relationship, classified by
    # client vintage.  A "New Client" is any relationship whose first_seen_date
    # is within trailing 12 months of the row date; everything else is
    # "Existing Client".  The stacked total ties exactly to firm-level AUA.
    perf_cohort = perf[['date', 'relationship_id', 'total_aua']].merge(
        cdim[['relationship_id', 'first_seen_date']],
        on='relationship_id', how='left',
    )
    perf_cohort['months_since_first'] = (
        (perf_cohort['date'] - perf_cohort['first_seen_date']).dt.days / 30.44
    )
    perf_cohort['cohort'] = np.where(
        perf_cohort['months_since_first'] <= 12,
        'NMNC',   # New Money New Clients (within trailing 12mo)
        'NMEC',   # New Money Existing Clients (older than 12mo)
    )

    daily_cohort = (
        perf_cohort
        .groupby(['date', 'cohort'])['total_aua']
        .sum()
        .unstack(fill_value=0)
        .sort_index()
        .reset_index()
    )
    # Ensure both columns exist even if one cohort is empty
    for col in ['NMNC', 'NMEC']:
        if col not in daily_cohort.columns:
            daily_cohort[col] = 0.0

    aua_data = [
        {'date': r['date'].strftime('%Y-%m-%d'),
         'NMNC': round(float(r['NMNC']), 2),
         'NMEC': round(float(r['NMEC']), 2)}
        for _, r in daily_cohort.iterrows()
    ]

    # ---- NNA view (cumulative firm-level NNA + inflows/outflows) ----
    # All three columns are cumulative from inception.
    # The frontend diffs adjacent period endpoints to get period-level flows:
    #   period_inflows  = last(Inflows)  - first(Inflows)
    #   period_outflows = last(Outflows) - first(Outflows)
    #   period_nna      = last(NNA)      - first(NNA)
    daily_nna = (
        perf.groupby('date')[['nna', 'cum_inflows', 'cum_outflows']].sum()
        .sort_index()
        .reset_index()
    )
    nna_data = [
        {
            'date':     r['date'].strftime('%Y-%m-%d'),
            'NNA':      round(float(r['nna']), 2),
            'Inflows':  round(float(r['cum_inflows']), 2),
            'Outflows': round(float(r['cum_outflows']), 2),
        }
        for _, r in daily_nna.iterrows()
    ]

    # ---- ADV view (AUA by architect, stacked) ----
    # Pick top N architects by AUA on latest date
    latest_date_adv = adv['date'].max()
    latest_adv = adv[adv['date'] == latest_date_adv]
    top_architects = (
        latest_adv.nlargest(TOP_N_ADV, 'total_aua')['architect'].tolist()
    )

    adv_pivot = adv.copy()
    adv_pivot['_arch'] = adv_pivot['architect'].where(
        adv_pivot['architect'].isin(top_architects), 'Other'
    )
    adv_by_date = (
        adv_pivot.groupby(['date', '_arch'])['total_aua']
        .sum()
        .unstack(fill_value=0)
        .sort_index()
        .reset_index()
    )
    adv_categories = [a for a in top_architects if a in adv_by_date.columns] + (
        ['Other'] if 'Other' in adv_by_date.columns else []
    )
    adv_data = []
    for _, row in adv_by_date.iterrows():
        point = {'date': row['date'].strftime('%Y-%m-%d')}
        for cat in adv_categories:
            point[cat] = round(float(row.get(cat, 0)), 2)
        adv_data.append(point)

    # ---- GEO view (AUA by state, stacked) ----
    # US-only, top N states by AUA on latest date
    geo_us = geo[geo['country'].isin(['USA', 'US', '']) | geo['country'].isna()].copy()
    latest_date_geo = geo_us['date'].max()
    latest_geo = geo_us[geo_us['date'] == latest_date_geo]
    top_states = (
        latest_geo[latest_geo['state'].notna() & (latest_geo['state'] != '') &
                   (latest_geo['state'] != 'Unknown')]
        .nlargest(TOP_N_GEO, 'total_aua')['state'].tolist()
    )

    geo_pivot = geo_us.copy()
    geo_pivot['_state'] = geo_pivot['state'].where(
        geo_pivot['state'].isin(top_states), 'Other'
    )
    geo_by_date = (
        geo_pivot.groupby(['date', '_state'])['total_aua']
        .sum()
        .unstack(fill_value=0)
        .sort_index()
        .reset_index()
    )
    geo_categories = [s for s in top_states if s in geo_by_date.columns] + (
        ['Other'] if 'Other' in geo_by_date.columns else []
    )
    geo_data = []
    for _, row in geo_by_date.iterrows():
        point = {'date': row['date'].strftime('%Y-%m-%d')}
        for cat in geo_categories:
            point[cat] = round(float(row.get(cat, 0)), 2)
        geo_data.append(point)

    # ---- GEO DRILL view (city-level AUA per top state) ----
    MAX_DRILL_CITIES = 9
    geo_drill = {}
    if geo_city is not None and not geo_city.empty:
        # Only drill into the top states that appear in geo_categories (excl "Other")
        drill_states = [s for s in top_states if s != 'Other']
        latest_date_city = geo_city['date'].max()

        for state in drill_states:
            state_city = geo_city[geo_city['state'] == state].copy()
            if state_city.empty:
                continue

            # Rank cities by AUA on latest date, keep top N
            latest_city = state_city[state_city['date'] == latest_date_city]
            top_cities = (
                latest_city.nlargest(MAX_DRILL_CITIES, 'total_aua')['city'].tolist()
            )

            # Bucket the rest as "Other"
            state_city['_city'] = state_city['city'].where(
                state_city['city'].isin(top_cities), 'Other'
            )
            city_by_date = (
                state_city.groupby(['date', '_city'])['total_aua']
                .sum()
                .unstack(fill_value=0)
                .sort_index()
                .reset_index()
            )
            city_categories = [c for c in top_cities if c in city_by_date.columns] + (
                ['Other'] if 'Other' in city_by_date.columns else []
            )
            city_data = []
            for _, row in city_by_date.iterrows():
                point = {'date': row['date'].strftime('%Y-%m-%d')}
                for cat in city_categories:
                    point[cat] = round(float(row.get(cat, 0)), 2)
                city_data.append(point)

            geo_drill[state] = {
                'categories': city_categories,
                'data': city_data,
            }

        print(f"  geo_drill: {len(geo_drill)} states with city drill-down")
    else:
        print("  geo_drill: skipped (no city data)")

    # ---- Assemble response ----
    all_dates = perf['date'].sort_values()
    date_start = all_dates.min().strftime('%Y-%m-%d')
    date_end   = all_dates.max().strftime('%Y-%m-%d')
    days_total = int((all_dates.max() - all_dates.min()).days)

    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   date_end,
        'firm_id':      FIRM_ID,
        'date_range': {'start': date_start, 'end': date_end, 'days': days_total},
        'metadata': {'new_clients': new_clients_meta},
        'aua': {
            'description': 'Total AUA by client vintage (NMNC=new <=12mo, NMEC=existing >12mo)',
            'categories': ['NMNC', 'NMEC'],
            'data': aua_data,
        },
        'nna': {
            'description': 'Cumulative firm-level net new assets, inflows, and outflows',
            'categories': ['NNA', 'Inflows', 'Outflows'],
            'data': nna_data,
        },
        'adv': {
            'description': 'Cumulative AUA by architect',
            'categories': adv_categories,
            'data': adv_data,
        },
        'geo': {
            'description': 'Cumulative AUA by US state',
            'categories': geo_categories,
            'data': geo_data,
        },
    }

    # Only add geo_drill when populated (avoids empty key in JSON)
    if geo_drill:
        result['geo_drill'] = geo_drill

    print(f"  timeseries_chart: {len(aua_data)} days, {len(adv_categories)} architects, "
          f"{len(geo_categories)} states"
          + (f", {len(geo_drill)} state drill-downs" if geo_drill else ""))
    return result


# ---------------------------------------------------------------------------
# 2. Leaderboard helpers
# ---------------------------------------------------------------------------

def _leaderboard_entries(df_by_date: pd.DataFrame, dim_col: str,
                          cdim: pd.DataFrame, architect_col: str,
                          today: pd.Timestamp, days: int) -> list:
    """
    Build ranked LeaderboardEntry list for one time window.

    df_by_date: daily timeseries (adv or account-performance-based) with
                date, {dim_col}, total_aua, nna columns
    architect_col: column in cdim that maps to dim_col (e.g. 'primary_architect')
    """
    window_start = today - pd.Timedelta(days=days)

    all_dates = df_by_date['date'].sort_values().unique()
    latest_date = all_dates.max()

    # Find the date in the data closest to window_start (looking back)
    past_dates = all_dates[all_dates <= window_start]
    start_date  = past_dates.max() if len(past_dates) > 0 else all_dates.min()

    end_snapshot   = df_by_date[df_by_date['date'] == latest_date].set_index(dim_col)
    start_snapshot = df_by_date[df_by_date['date'] == start_date].set_index(dim_col)

    entries = []
    for dim_val, end_row in end_snapshot.iterrows():
        if not dim_val or str(dim_val).strip() in ('', 'nan', 'None'):
            continue

        total_aua   = float(end_row.get('total_aua', 0) or 0)
        client_count = int(end_row.get('num_relationships', 0) or 0)
        account_count = int(end_row.get('num_accounts', 0) or 0)

        # NNA over window = nna_end - nna_start (cumulative from inception)
        start_row = start_snapshot.loc[dim_val] if dim_val in start_snapshot.index else None
        nna_end   = float(end_row.get('nna', 0) or 0)
        nna_start = float(start_row.get('nna', 0) or 0) if start_row is not None else 0.0
        nna_window = nna_end - nna_start

        # AUA growth % over window
        aua_start = float(start_row.get('total_aua', 0) or 0) if start_row is not None else 0.0
        aua_growth_pct = (
            (total_aua - aua_start) / aua_start * 100
            if aua_start > 0 else 0.0
        )

        # New clients in window (first_seen_date in window AND matching advisor)
        if architect_col in cdim.columns:
            matching = cdim[cdim[architect_col] == dim_val]
        else:
            matching = pd.DataFrame()
        new_clients = int(
            (matching['first_seen_date'] >= window_start).sum()
        ) if not matching.empty else 0

        entries.append({
            'name':            str(dim_val),
            'nna':             round(nna_window, 2),
            'aua_growth_pct':  round(aua_growth_pct, 2),
            'new_clients':     new_clients,
            'total_aua':       round(total_aua, 2),
            'client_count':    client_count,
            'account_count':   account_count,
        })

    # Rank by NNA descending
    entries.sort(key=lambda x: x['nna'], reverse=True)
    for i, e in enumerate(entries):
        e['rank'] = i + 1

    return entries


def _leaderboard_window_data(entries: list) -> dict:
    total_nna = sum(e['nna'] for e in entries)
    total_aua = sum(e['total_aua'] for e in entries)
    return {
        'entry_count': len(entries),
        'summary': {
            'total_nna':            round(total_nna, 2),
            'total_aua':            round(total_aua, 2),
            'total_new_clients':    sum(e['new_clients'] for e in entries),
            'positive_nna_count':   sum(1 for e in entries if e['nna'] >= 0),
            'negative_nna_count':   sum(1 for e in entries if e['nna'] < 0),
        },
        'entries': entries,
    }


def build_architect_leaderboard(adv: pd.DataFrame, cdim: pd.DataFrame,
                                 today: pd.Timestamp) -> dict:
    print("Building architect_leaderboard.json...")

    windows_data = {}
    for label, days in WINDOWS.items():
        entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect',
                                        today, days)
        windows_data[label] = _leaderboard_window_data(entries)
        print(f"  Window {label}: {len(entries)} architects")

    latest_date = adv['date'].max()
    return {
        'generated_at':       datetime.now(timezone.utc).isoformat(),
        'data_as_of':         latest_date.strftime('%Y-%m-%d'),
        'firm_id':            FIRM_ID,
        'leaderboard_type':   'architect',
        'available_windows':  list(WINDOWS.keys()),
        'windows':            windows_data,
    }


# ---------------------------------------------------------------------------
# 3. clients_tab.json  (ClientsTabResponse + Yang tax fields)
# ---------------------------------------------------------------------------

def _build_tax_section(perf_latest: pd.DataFrame, tax: pd.DataFrame) -> dict:
    """Build the full tax section combining client_performance and client_tax_liability."""

    # AUA split from client_performance (position-based, all accounts)
    total_aua      = float(perf_latest['total_aua'].sum())
    aua_taxable    = float(perf_latest['aua_taxable'].sum())
    aua_deferred   = float(perf_latest['aua_tax_deferred'].sum())
    aua_exempt     = float(perf_latest['aua_tax_exempt'].sum())
    pct = lambda x: round(x / total_aua * 100, 1) if total_aua > 0 else 0.0

    # Qualified vs non-qualified from client_tax_liability (open lots only, snapshot date)
    tax_taxable = tax[tax['tax_status'] == 'taxable']
    tax_qual    = tax[tax['qualified_flag'] == True]
    tax_nonqual = tax[tax['qualified_flag'] == False]

    qual_mv    = float(tax_qual['total_market_value'].sum())
    nonqual_mv = float(tax_nonqual['total_market_value'].sum())
    lot_total  = qual_mv + nonqual_mv

    qual_pct   = round(qual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0
    nonqual_pct = round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0

    # Account counts: unique accounts per qualified flag
    qual_acct_count    = int(tax_qual['account_id'].nunique())
    nonqual_acct_count = int(tax_nonqual['account_id'].nunique())

    # Non-qualified cost basis and gains (taxable positions only)
    nq_cost_basis     = float(tax_taxable['total_cost_basis'].sum())
    nq_market_value   = float(tax_taxable['total_market_value'].sum())
    nq_unrealized     = float(tax_taxable['total_accrued_gain'].sum())
    st_gain           = float(tax_taxable['short_term_gain'].sum())
    lt_gain           = float(tax_taxable['long_term_gain'].sum())

    # Cost basis by purchase year (taxable only)
    year_agg = (
        tax_taxable
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

    # Top gain positions (taxable, aggregated across purchase years per asset)
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
        .nlargest(TOP_GAIN_POSITIONS, 'unrealized_gain')
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

    return {
        # Standard fields (from client_performance — position-based AUA)
        'taxable':          round(aua_taxable, 2),
        'taxable_pct':      pct(aua_taxable),
        'tax_deferred':     round(aua_deferred, 2),
        'tax_deferred_pct': pct(aua_deferred),
        'tax_free':         round(aua_exempt, 2),
        'tax_free_pct':     pct(aua_exempt),
        'capital_gains_ttm': round(nq_unrealized, 2),  # total unrealized gain on taxable positions

        # Yang's fields: qualified vs non-qualified split
        'qualified_aua':              round(qual_mv, 2),
        'qualified_pct':              qual_pct,
        'non_qualified_aua':          round(nonqual_mv, 2),
        'non_qualified_pct':          nonqual_pct,
        'qualified_account_count':    qual_acct_count,
        'non_qualified_account_count': nonqual_acct_count,

        # Yang's fields: non-qualified cost basis and gains (aggregated position grain)
        'non_qualified_cost_basis':      round(nq_cost_basis, 2),
        'non_qualified_market_value':    round(nq_market_value, 2),
        'non_qualified_unrealized_gain': round(nq_unrealized, 2),
        'short_term_gain':               round(st_gain, 2),
        'long_term_gain':                round(lt_gain, 2),

        # Yang's fields: by purchase year (aggregated position grain)
        'cost_basis_by_year': cost_basis_by_year,

        # Yang's fields: top positions by unrealized gain (aggregated position grain)
        'top_gain_positions': top_gain_positions,

        # Flag for client detail endpoint (lot-level detail available there)
        'lots_available': True,
    }


def build_clients_tab(perf: pd.DataFrame, cdim: pd.DataFrame,
                       adim: pd.DataFrame, tax: pd.DataFrame,
                       today: pd.Timestamp) -> dict:
    print("Building clients_tab.json...")

    latest_date = perf['date'].max()
    perf_latest = perf[perf['date'] == latest_date]

    # Headline
    total_aua     = float(perf_latest['total_aua'].sum())
    account_count = int(perf_latest['num_accounts'].sum())
    client_count  = int(perf_latest['relationship_id'].nunique())

    headline = {
        'total_aua':        round(total_aua, 2),
        'account_count':    account_count,
        'client_count':     client_count,
        'fee_rate_pct':     0.0,   # not available from BD data
        'income_yield_pct': 0.0,   # not available from BD data
    }

    # Tax section
    tax_section = _build_tax_section(perf_latest, tax)

    # Engagement: net_flows TTM
    ttm_cutoff = today - pd.Timedelta(days=365)
    past_dates  = perf['date'][perf['date'] <= ttm_cutoff]
    ttm_start   = past_dates.max() if not past_dates.empty else perf['date'].min()

    perf_ttm_start = perf[perf['date'] == ttm_start]
    inflows_now   = float(perf_latest['cum_inflows'].sum())
    outflows_now  = float(perf_latest['cum_outflows'].sum())
    inflows_then  = float(perf_ttm_start['cum_inflows'].sum())
    outflows_then = float(perf_ttm_start['cum_outflows'].sum())
    net_flows_ttm = (inflows_now - inflows_then) - (outflows_now - outflows_then)

    # Avg relationship tenure from client_dimension
    cdim_active = cdim[cdim['first_seen_date'].notna()]
    avg_tenure_years = 0.0
    if not cdim_active.empty:
        avg_days = (today - cdim_active['first_seen_date']).dt.days.mean()
        avg_tenure_years = round(float(avg_days) / 365.25, 2)

    # Active clients pct: clients with at least 1 account in latest positions
    active_rel_ids = set(perf_latest['relationship_id'].unique())
    all_rel_ids    = set(cdim['relationship_id'].unique())
    active_pct = round(len(active_rel_ids) / len(all_rel_ids) * 100, 1) if all_rel_ids else 0.0

    engagement = {
        'trading_buys_ttm':    0,      # computable from silver but not loaded here
        'trading_sells_ttm':   0,
        'net_flows_ttm':       round(net_flows_ttm, 2),
        'avg_relationship_years': avg_tenure_years,
        'active_clients_pct':  active_pct,
    }

    # Income & Fees: zeroed (not available from BD transaction data)
    income_fees = {
        'dividends_ttm':       0.0,
        'interest_ttm':        0.0,
        'total_income_ttm':    0.0,
        'income_yield_pct':    0.0,
        'management_fees_ttm': 0.0,
        'fee_rate_pct':        0.0,
    }

    # Portfolio: zeroed (asset class taxonomy not available)
    portfolio = {
        'allocation':               [],
        'weighted_expense_ratio':   0.0,
        'unique_holdings':          0,
        'top_5_concentration_pct':  0.0,
    }

    # Client dropdown list (sorted by AUA desc)
    client_list_df = (
        perf_latest[['relationship_id', 'total_aua']]
        .merge(cdim[['relationship_id', 'relationship_name']], on='relationship_id', how='left')
        .sort_values('total_aua', ascending=False)
    )
    clients = [
        {
            'key':  str(r['relationship_id']),
            'name': str(r['relationship_name']) if pd.notna(r['relationship_name'])
                    else str(r['relationship_id']),
            'aua':  round(float(r['total_aua']), 2),
        }
        for _, r in client_list_df.iterrows()
    ]

    print(f"  clients_tab: {client_count} clients, total_aua={total_aua:,.0f}")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   latest_date.strftime('%Y-%m-%d'),
        'firm_id':      FIRM_ID,
        'headline':     headline,
        'tax':          tax_section,
        'income_fees':  income_fees,
        'portfolio':    portfolio,
        'engagement':   engagement,
        'clients':      clients,
    }


# ---------------------------------------------------------------------------
# 4. summary/header_metrics.json  (HeaderMetricsResponse)
# ---------------------------------------------------------------------------

def build_header_metrics(perf: pd.DataFrame, adv: pd.DataFrame,
                          cdim: pd.DataFrame, today: pd.Timestamp) -> dict:
    print("Building summary/header_metrics.json...")

    latest_date = perf['date'].max()
    perf_latest = perf[perf['date'] == latest_date]
    total_aua   = float(perf_latest['total_aua'].sum())

    def _nna_for_period(days: int) -> float:
        cutoff = today - pd.Timedelta(days=days)
        past   = perf['date'][perf['date'] <= cutoff]
        d_start = past.max() if not past.empty else perf['date'].min()
        start_rows = perf[perf['date'] == d_start]
        inf_end  = float(perf_latest['cum_inflows'].sum())
        out_end  = float(perf_latest['cum_outflows'].sum())
        inf_st   = float(start_rows['cum_inflows'].sum())
        out_st   = float(start_rows['cum_outflows'].sum())
        return (inf_end - inf_st) - (out_end - out_st)

    nna_12m = _nna_for_period(365)
    nna_ytd  = _nna_for_period((today - pd.Timestamp(today.year, 1, 1)).days)
    nna_qtd  = _nna_for_period((today - pd.Timestamp(today.year,
                                                       ((today.month - 1) // 3) * 3 + 1,
                                                       1)).days)
    nna_mtd  = _nna_for_period((today - pd.Timestamp(today.year, today.month, 1)).days)

    # Quarterly labels (q0=current quarter, q1=last quarter, etc.)
    def _quarter_label(ts: pd.Timestamp) -> str:
        q = (ts.month - 1) // 3 + 1
        return f"Q{q} '{str(ts.year)[2:]}"

    def _quarter_nna(quarters_back: int) -> dict:
        q_start = _quarter_start(today, quarters_back)
        q_end   = _quarter_start(today, quarters_back - 1) - pd.Timedelta(days=1)
        nna_val = _nna_for_period((today - q_start).days) - (
            _nna_for_period((today - q_end).days) if quarters_back > 0 else 0
        )
        return {'nna': round(nna_val, 2), 'label': _quarter_label(q_start)}

    # Architect breakdown (top 10)
    adv_latest = adv[adv['date'] == adv['date'].max()]
    by_arch = []
    for _, row in adv_latest.nlargest(10, 'total_aua').iterrows():
        arch_aua = float(row['total_aua'])
        by_arch.append({
            'architect':     str(row['architect']),
            'aua':           round(arch_aua, 2),
            'aua_pct':       round(arch_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count':  int(row['num_relationships']),
            'account_count': int(row['num_accounts']),
        })

    total = {
        'aua':                  round(total_aua, 2),
        'nna_mtd':              round(nna_mtd, 2),
        'nna_qtd':              round(nna_qtd, 2),
        'nna_ytd':              round(nna_ytd, 2),
        'nna_12m':              round(nna_12m, 2),
        'client_count':         int(perf_latest['relationship_id'].nunique()),
        'account_count':        int(perf_latest['num_accounts'].sum()),
        'new_client_count':     0,   # requires NMNC classification at position level
        'existing_client_count': 0,
        'new_client_aua':       0.0,
        'existing_client_aua':  0.0,
        'new_client_pct':       0.0,
        'q0': {'nna': round(nna_qtd, 2)},
        'q1': _quarter_nna(1),
        'q2': _quarter_nna(2),
        'q3': _quarter_nna(3),
    }

    print(f"  header_metrics: AUA={total_aua:,.0f}, NNA_12M={nna_12m:,.0f}")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   latest_date.strftime('%Y-%m-%d'),
        'firm_id':      FIRM_ID,
        'firm_name':    FIRM_NAME,
        'total':        total,
        'by_architect': by_arch,
    }


# ---------------------------------------------------------------------------
# 5. partner_analytics/header_metrics.json  (PartnerAnalyticsResponse)
# ---------------------------------------------------------------------------

def build_partner_analytics(perf: pd.DataFrame, adv: pd.DataFrame,
                              geo: pd.DataFrame, cdim: pd.DataFrame,
                              today: pd.Timestamp) -> dict:
    """
    Produces PartnerAnalyticsResponse for the partner analytics tab.
    Current period only (no time machine quarters — can be added later).
    """
    print("Building partner_analytics/header_metrics.json...")

    latest_date  = perf['date'].max()
    perf_latest  = perf[perf['date'] == latest_date]
    total_aua    = float(perf_latest['total_aua'].sum())

    def _segment(key, label, aua, client_count, color) -> dict:
        return {
            'key': key, 'label': label,
            'aua': round(float(aua), 2),
            'aua_pct': round(float(aua) / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': int(client_count),
            'color': color,
        }

    # AUA view: taxable / tax_deferred / tax_exempt
    aua_taxable  = float(perf_latest['aua_taxable'].sum())
    aua_deferred = float(perf_latest['aua_tax_deferred'].sum())
    aua_exempt   = float(perf_latest['aua_tax_exempt'].sum())

    # Client count per tax status (approximate from cdim)
    n_taxable  = int(cdim['has_taxable'].sum())
    n_deferred = int(cdim['has_tax_deferred'].sum())
    n_exempt   = int(cdim['has_tax_exempt'].sum())

    aua_segments = [
        _segment('taxable',      'Non-Qualified',  aua_taxable,  n_taxable,  '#EF4444'),
        _segment('tax_deferred', 'Tax-Deferred',   aua_deferred, n_deferred, '#F59E0B'),
        _segment('tax_free',     'Tax-Free (Roth)', aua_exempt,  n_exempt,   '#10B981'),
    ]

    # ADV view: by architect (top 8 + Other)
    adv_latest   = adv[adv['date'] == latest_date]
    top_arch     = adv_latest.nlargest(TOP_N_ADV, 'total_aua')
    other_aua    = total_aua - float(top_arch['total_aua'].sum())
    arch_colors  = ['#4CAF50', '#2196F3', '#F59E0B', '#EF4444',
                    '#8B5CF6', '#EC4899', '#14B8A6', '#F97316']
    adv_segments = [
        _segment(
            str(r['architect']).lower().replace(' ', '_'),
            str(r['architect']),
            r['total_aua'],
            r['num_relationships'],
            arch_colors[i % len(arch_colors)],
        )
        for i, (_, r) in enumerate(top_arch.iterrows())
    ]
    if other_aua > 0:
        adv_segments.append(_segment('other', 'Other', other_aua, 0, '#6B7280'))

    # GEO view: by state (top 8 + Other)
    geo_us       = geo[(geo['country'].isin(['USA', 'US', ''])) | geo['country'].isna()]
    geo_latest   = geo_us[geo_us['date'] == latest_date]
    top_states   = geo_latest.nlargest(TOP_N_GEO, 'total_aua')
    other_geo    = total_aua - float(top_states['total_aua'].sum())
    state_colors = arch_colors
    geo_segments = [
        _segment(
            str(r['state']).lower(),
            str(r['state']),
            r['total_aua'],
            r['num_relationships'],
            state_colors[i % len(state_colors)],
        )
        for i, (_, r) in enumerate(top_states.iterrows())
        if r['state'] not in ('Unknown', '', None)
    ]
    if other_geo > 0:
        geo_segments.append(_segment('other', 'Other', other_geo, 0, '#6B7280'))

    def _metrics(aua_val, client_count):
        return {
            'aua': round(float(aua_val), 2),
            'client_count': int(client_count),
        }

    def _donut(title, segments):
        return {
            'title': title,
            'total': round(sum(s['aua'] for s in segments), 2),
            'segments': segments,
        }

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   latest_date.strftime('%Y-%m-%d'),
        'firm_id':      FIRM_ID,
        'firm_name':    FIRM_NAME,
        'views': {
            'aua': {
                'current': {
                    'donut': _donut('AUA by Tax Status', aua_segments),
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
            'adv': {
                'current': {
                    'donut': _donut('AUA by Architect', adv_segments),
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
            'geo': {
                'current': {
                    'donut': _donut('AUA by Geography', geo_segments),
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
            'nna': {
                'current': {
                    'donut': _donut('AUA by Tax Status', aua_segments),  # fallback same as aua
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
        },
    }


# ---------------------------------------------------------------------------
# 6. filters/dimensions.json  (FiltersResponse)
# ---------------------------------------------------------------------------

def build_filters(adv: pd.DataFrame, adim: pd.DataFrame,
                   today: pd.Timestamp) -> dict:
    print("Building filters/dimensions.json...")

    latest_adv = adv[adv['date'] == adv['date'].max()]

    # AUA per architect from adv timeseries
    arch_aua = latest_adv.set_index('architect')['total_aua'].to_dict()

    def _dim_values(series: pd.Series, top_n=None, aua_map: dict = None) -> list:
        """Build filter value list from a string series."""
        counts = series.dropna().astype(str).str.strip()
        counts = counts[counts.str.lower().isin({'', 'nan', 'none', 'unassigned'}) == False]
        freq = counts.value_counts()
        if top_n:
            freq = freq.head(top_n)
        values = []
        for name, cnt in freq.items():
            v = {
                'id':   name.lower().replace(' ', '_').replace('&', 'and'),
                'name': name,
            }
            if aua_map and name in aua_map:
                v['aua']           = round(float(aua_map[name]), 2)
                v['client_count']  = int(cnt)
            values.append(v)
        return values

    # Build per-dimension AUA maps from accounts_dimension (static, latest)
    # We use adv timeseries for architect AUA; use adim counts for others
    # (no AUA per implementor/region/account_type from gold — use counts only)

    dimensions = {
        'architect': {
            'label': 'Architect',
            'column': 'architect',
            'values': _dim_values(adim['architect'], aua_map=arch_aua),
        },
        'region': {
            'label': 'Region',
            'column': 'local_ops',
            'values': _dim_values(adim['local_relationship']),
        },
        'implementor': {
            'label': 'Implementor',
            'column': 'implementor',
            'values': _dim_values(adim['implementor'], top_n=TOP_N_IMPLEMENTOR),
        },
        'account_type': {
            'label': 'Account Type',
            'column': 'account_owner_type',
            'values': _dim_values(adim['account_type']),
        },
        'tax_status': {
            'label': 'Tax Status',
            'column': 'tax_status',
            'values': _dim_values(adim['tax_status']),
        },
        'state': {
            'label': 'State',
            'column': 'client_state',
            'values': _dim_values(adim['client_state'], top_n=TOP_N_STATE),
        },
    }

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'firm_id':      FIRM_ID,
        'dimensions':   dimensions,
    }


# ---------------------------------------------------------------------------
# 7. Snapshots  (SnapshotResponse)
# ---------------------------------------------------------------------------

def _snapshot_response(dimension: str, rows: list, total_aua: float,
                        data_as_of: str) -> dict:
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   data_as_of,
        'firm_id':      FIRM_ID,
        'dimension':    dimension,
        'total_aua':    round(total_aua, 2),
        'data':         rows,
    }


def build_snapshots(perf: pd.DataFrame, adv: pd.DataFrame,
                     geo: pd.DataFrame, adim: pd.DataFrame) -> dict:
    """Returns dict of {output_key: response_dict} for each snapshot."""
    print("Building snapshot files...")

    latest_date  = adv['date'].max()
    perf_latest  = perf[perf['date'] == perf['date'].max()]
    adv_latest   = adv[adv['date'] == latest_date]
    geo_latest   = geo[geo['date'] == geo['date'].max()]
    total_aua    = float(perf_latest['total_aua'].sum())
    date_str     = latest_date.strftime('%Y-%m-%d')

    def _rows(df, val_col, aua_col, top_n=None, label_transform=None):
        agg = df.groupby(val_col)[aua_col].sum().sort_values(ascending=False)
        if top_n:
            agg = agg.head(top_n)
        total = float(agg.sum())
        rows = []
        for val, aua in agg.items():
            label = label_transform(val) if label_transform else str(val)
            if not label or label.lower() in ('nan', 'none', 'unknown', ''):
                continue
            rows.append({
                'value':         label,
                'aua':           round(float(aua), 2),
                'aua_pct':       round(float(aua) / total * 100, 1) if total > 0 else 0.0,
                'client_count':  0,  # populated below for architect
                'account_count': 0,
            })
        return rows

    # Architect snapshot (from adv timeseries — has num_relationships + num_accounts)
    arch_rows = []
    for _, row in adv_latest.sort_values('total_aua', ascending=False).iterrows():
        arch_aua = float(row['total_aua'])
        arch_rows.append({
            'value':         str(row['architect']),
            'aua':           round(arch_aua, 2),
            'aua_pct':       round(arch_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count':  int(row['num_relationships']),
            'account_count': int(row['num_accounts']),
        })

    # Tax status snapshot (from client_performance aua columns)
    tax_map = {
        'taxable':     ('Non-Qualified',  float(perf_latest['aua_taxable'].sum())),
        'tax_deferred': ('Tax-Deferred',  float(perf_latest['aua_tax_deferred'].sum())),
        'tax_exempt':  ('Tax-Free (Roth)', float(perf_latest['aua_tax_exempt'].sum())),
    }
    tax_rows = [
        {'value': label, 'aua': round(aua, 2),
         'aua_pct': round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
         'client_count': 0, 'account_count': 0}
        for _, (label, aua) in sorted(tax_map.items(), key=lambda x: -x[1][1])
    ]

    # State snapshot (from geo timeseries, US only)
    geo_us = geo_latest[
        (geo_latest['country'].isin(['USA', 'US', ''])) | geo_latest['country'].isna()
    ]
    state_agg = (
        geo_us.groupby('state')['total_aua']
        .sum()
        .sort_values(ascending=False)
        .head(TOP_N_STATE)
    )
    state_total = float(state_agg.sum())
    state_rows = [
        {'value': str(state), 'aua': round(float(aua), 2),
         'aua_pct': round(float(aua) / state_total * 100, 1) if state_total > 0 else 0.0,
         'client_count': 0, 'account_count': 0}
        for state, aua in state_agg.items()
        if str(state).lower() not in ('unknown', '', 'nan', 'none')
    ]

    # Region snapshot (from accounts_dimension local_relationship)
    region_agg = (
        adim.groupby('local_relationship')['account_id'].count()
        .sort_values(ascending=False)
    )
    region_rows = [
        {'value': str(region), 'aua': 0.0, 'aua_pct': 0.0,
         'client_count': 0, 'account_count': int(cnt)}
        for region, cnt in region_agg.items()
        if str(region).lower() not in ('', 'nan', 'none', 'unassigned')
    ]

    return {
        'gold/snapshots/aua_by_architect.json': _snapshot_response(
            'architect', arch_rows, total_aua, date_str),
        'gold/snapshots/aua_by_tax_status.json': _snapshot_response(
            'tax_status', tax_rows, total_aua, date_str),
        'gold/snapshots/aua_by_state.json': _snapshot_response(
            'state', state_rows, state_total, date_str),
        'gold/snapshots/aua_by_region.json': _snapshot_response(
            'region', region_rows, 0.0, date_str),
    }


# ---------------------------------------------------------------------------
# Lambda handler
# ---------------------------------------------------------------------------

def lambda_handler(event, context):
    print("=" * 70)
    print("BD PORTAL PUBLISHER")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")
    print("=" * 70)

    # Fan-out: invoke advisor publisher in parallel (S3 does not allow two
    # notification rules with the same prefix+suffix, so portal-publisher
    # fires advisor-publisher async and both run concurrently)
    advisor_fn = os.environ.get('ADVISOR_PUBLISHER_FUNCTION')
    if advisor_fn:
        try:
            lam = boto3.client('lambda', region_name='us-east-1')
            lam.invoke(
                FunctionName=advisor_fn,
                InvocationType='Event',
                Payload=json.dumps(event).encode(),
            )
            print(f"Fan-out: invoked {advisor_fn} async")
        except Exception as e:
            print(f"WARN: Could not invoke {advisor_fn}: {e}")

    today = _today()

    try:
        # ------------------------------------------------------------------
        # Step 1: Load all source parquets
        # ------------------------------------------------------------------
        print("\n=== Step 1: Load parquets ===")
        data = load_all(today)
        perf     = data['perf']
        adv      = data['adv']
        geo      = data['geo']
        geo_city = data['geo_city']
        cdim     = data['cdim']
        adim     = data['adim']
        tax      = data['tax']

        # ------------------------------------------------------------------
        # Step 2: Build and write each output
        # ------------------------------------------------------------------
        print("\n=== Step 2: Build outputs ===")
        results = {}

        # timeseries_chart.json
        chart = build_timeseries_chart(perf, adv, geo, cdim, today, geo_city=geo_city)
        _save_json(chart, 'gold/timeseries_chart.json')
        results['timeseries_chart'] = 'ok'

        # architect_leaderboard.json
        lb = build_architect_leaderboard(adv, cdim, today)
        _save_json(lb, 'gold/architect_leaderboard.json')
        results['architect_leaderboard'] = 'ok'

        # clients_tab.json
        clients = build_clients_tab(perf, cdim, adim, tax, today)
        _save_json(clients, 'gold/clients_tab.json')
        results['clients_tab'] = 'ok'

        # summary/header_metrics.json
        hm = build_header_metrics(perf, adv, cdim, today)
        _save_json(hm, 'gold/summary/header_metrics.json')
        results['header_metrics'] = 'ok'

        # DISABLED: EC2 gold script 09_generate_partner_analytics.py now owns this output.
        # The EC2 version includes nested cities, nested clients, and 4-period time machine.
        # Re-enabling the Lambda version would overwrite the richer EC2 output.
        # pa = build_partner_analytics(perf, adv, geo, cdim, today)
        # _save_json(pa, 'gold/partner_analytics/header_metrics.json')
        results['partner_analytics'] = 'disabled (EC2 script owns output)'

        # filters/dimensions.json
        filters = build_filters(adv, adim, today)
        _save_json(filters, 'gold/filters/dimensions.json')
        results['filters'] = 'ok'

        # snapshots
        snapshots = build_snapshots(perf, adv, geo, adim)
        for key, snap in snapshots.items():
            _save_json(snap, key)
        results['snapshots'] = f"{len(snapshots)} files"

        # ------------------------------------------------------------------
        # Step 3: Summary
        # ------------------------------------------------------------------
        print("\n=== Step 3: Complete ===")
        latest_date = perf['date'].max()
        total_aua   = float(perf[perf['date'] == latest_date]['total_aua'].sum())
        print(f"  Data as of:  {latest_date.date()}")
        print(f"  Total AUA:   ${total_aua:,.0f}")
        print(f"  Outputs:     {results}")
        print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 70)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':       'success',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'data_as_of':   latest_date.strftime('%Y-%m-%d'),
                'total_aua':    round(total_aua, 2),
                'outputs':      results,
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
