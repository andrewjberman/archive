#!/usr/bin/env python3
"""
Generate Advisor Rolling Flows — advisor_rolling_flows.json

Produces the portal-ready JSON at:
    s3://opal-data-bd/gold/advisor_rolling_flows.json

Served via CloudFront: shared-advisor-router:3 rewrites
    /api/scoped/advisor-intelligence/advisor_rolling_flows.json -> /gold/advisor_rolling_flows.json

Two views for the Advisors tab on Advisor Intelligence:

  1. NNA Summary (default view — donut chart)
     MTD, QTD, YTD NNA per advisor as donut-ready segments.
     Shows which advisors are driving net new asset growth in the
     current month, quarter, and year-to-date.

  2. Rolling Flows (time series view)
     Per-advisor rolling NNA, Inflows, and Outflows for trailing
     30-day, 90-day, and 1-year windows. Each data point is a
     cumulative diff: roll_val[D] = cum_val[D] - cum_val[D - W_days].

Data sources (from s3://opal-data-bd):
    gold/views/nna_aua_by_advisor.parquet      -- daily cum_inflows/cum_outflows/nna per architect
    gold/client_performance.parquet             -- household daily cumulative flows
    gold/accounts_dimension_latest.parquet      -- relationship -> implementor mapping

Architects: pre-aggregated in nna_aua_by_advisor.parquet.
Implementors: no pre-built view exists — computed on-the-fly by assigning the
modal implementor per relationship from accounts_dimension_latest, then
aggregating client_performance to (date, implementor) grain.

Output JSON shape:
    {
      "generated_at": "...",
      "data_as_of": "YYYY-MM-DD",
      "firm_id": "49financial",

      -- LEGACY KEYS (unchanged) --
      "summary": {
        "architects":   { "mtd": {...}, "qtd": {...}, "ytd": {...} },
        "implementors": { "mtd": {...}, "qtd": {...}, "ytd": {...} }
      },
      "architects":   [{ "advisor_name", "advisor_id", "series": {"30d":[...], "90d":[...], "1Y":[...]} }],
      "implementors": [...]

      -- ADVI-005 A3: additive keys --
      "stacked_bar": {
        "qtd": { "architects": [AdvisorBarEntry], "implementors": [AdvisorBarEntry] },
        "ytd": { ... },
        "1y":  { ... },
        "3y":  { ... },
        "max": { ... }
      }
      AdvisorBarEntry = { advisor_name, advisor_id, inflows, outflows (positive), nna_net (signed) }
      Period boundaries: qtd/ytd calendar-anchored; 1y/3y trailing 365/1095 days; max = inception.

      "rolling_1y": {
        "architects":   [AdvisorRolling1YSeries],
        "implementors": [AdvisorRolling1YSeries]
      }
      AdvisorRolling1YSeries = { advisor_name, advisor_id, series: [{date, nna, inflows, outflows}] }
      Fixed 1Y rolling window; daily points; full history emitted (frontend slices by period toggle).
      Data history: 2020-06-30 to present (~5.5Y). First valid 1Y point: ~2021-07-01.
      3Y and Max x-axis coverage: complete (data exceeds required 4Y lookback).
    }

Usage:
    python 10_generate_advisor_rolling_flows.py               # local test
    python 10_generate_advisor_rolling_flows.py --upload      # write to S3
    python 10_generate_advisor_rolling_flows.py --dry-run     # compute only, no write
    python 10_generate_advisor_rolling_flows.py -v            # verbose

Author: Data Scientist (Claude)
Date: 2026-02-27
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import boto3
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INPUT_BUCKET  = 'opal-data-bd'
OUTPUT_BUCKET = 'opal-data-bd'
OUTPUT_KEY    = 'gold/advisor_rolling_flows.json'
DEFAULT_LOCAL_OUTPUT = './gold/advisor_rolling_flows.json'

FIRM_ID = '49financial'

# Rolling windows: label -> trailing days (legacy rolling series)
WINDOWS = {'30d': 30, '90d': 90, '1Y': 365}

# Stacked bar periods: ordered display sequence (ADVI-005 A3)
STACKED_BAR_PERIODS = ('qtd', 'ytd', '1y', '3y', 'max')

# Donut chart colors (matches ADV palette in script 09)
DONUT_COLORS = ['#5e72e4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
                '#06B6D4', '#84CC16', '#F97316']
OTHER_COLOR  = '#757575'
MAX_DONUT_SEGMENTS = 8

MODAL_NULLS = frozenset({
    '', 'none', 'nan', 'unassigned', 'unknown', 'n/a',
    'no architect value assigned', 'no implementor value assigned', 'no state',
})

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _read_parquet(key: str, columns: list = None, verbose: bool = False) -> pd.DataFrame:
    s3 = boto3.client('s3', region_name='us-east-1')
    if verbose:
        print(f"  Loading s3://{INPUT_BUCKET}/{key}")
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {'columns': columns} if columns else {}
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    if verbose:
        print(f"    {len(df):,} rows")
    return df


def load_data(verbose: bool = False) -> tuple:
    """
    Load 3 gold tables needed for this script.
    Returns: (adv_ts, client_perf, acct_dim)

    adv_ts:       nna_aua_by_advisor (pre-aggregated architect daily flows)
    client_perf:  client_performance (household daily cumulative flows)
    acct_dim:     accounts_dimension_latest (for implementor assignment)
    """
    print("Loading gold tables from S3...")

    adv_ts = _read_parquet(
        'gold/views/nna_aua_by_advisor.parquet',
        columns=['date', 'architect', 'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
                 'num_relationships'],
        verbose=verbose
    )
    adv_ts['date'] = pd.to_datetime(adv_ts['date']).astype('datetime64[ns]')

    client_perf = _read_parquet(
        'gold/client_performance.parquet',
        columns=['date', 'relationship_id', 'total_aua', 'cum_inflows', 'cum_outflows', 'nna'],
        verbose=verbose
    )
    client_perf['date'] = pd.to_datetime(client_perf['date']).astype('datetime64[ns]')

    acct_dim = _read_parquet(
        'gold/accounts_dimension_latest.parquet',
        columns=['relationship_id', 'implementor'],
        verbose=verbose
    )

    client_dim = _read_parquet(
        'gold/client_dimension.parquet',
        columns=['relationship_id', 'first_seen_date', 'primary_architect', 'primary_implementor'],
        verbose=verbose
    )
    if 'first_seen_date' in client_dim.columns:
        client_dim['first_seen_date'] = pd.to_datetime(client_dim['first_seen_date']).astype('datetime64[ns]')

    return adv_ts, client_perf, acct_dim, client_dim


# ---------------------------------------------------------------------------
# Implementor view builder (no pre-aggregated gold view exists)
# ---------------------------------------------------------------------------

def _modal_str(series: pd.Series, default: str = 'Unassigned') -> str:
    """Return the most common non-null, non-empty value in a Series."""
    clean = series.dropna().astype(str).str.strip()
    clean = clean[~clean.str.lower().isin(MODAL_NULLS)]
    if clean.empty:
        return default
    return clean.mode().iloc[0]


def build_implementor_daily(client_perf: pd.DataFrame,
                             acct_dim: pd.DataFrame,
                             verbose: bool = False) -> pd.DataFrame:
    """
    Aggregate client_performance to (date, implementor) grain using modal
    implementor per relationship from accounts_dimension_latest.

    Output columns: date, implementor, cum_inflows, cum_outflows, nna, num_relationships
    """
    print("Building implementor daily timeseries...")

    if 'implementor' not in acct_dim.columns:
        print("  WARN: 'implementor' column not found in accounts_dimension_latest -- skipping")
        return pd.DataFrame(columns=['date', 'implementor', 'cum_inflows', 'cum_outflows',
                                     'nna', 'num_relationships'])

    # Compute modal implementor per relationship
    rel_impl = (
        acct_dim.groupby('relationship_id', sort=False)['implementor']
        .agg(lambda s: _modal_str(s, 'Unassigned'))
        .reset_index()
        .rename(columns={'implementor': 'implementor'})
    )

    n_distinct = rel_impl[rel_impl['implementor'] != 'Unassigned']['implementor'].nunique()
    n_unassigned = (rel_impl['implementor'] == 'Unassigned').sum()
    if verbose:
        print(f"  {len(rel_impl):,} relationships | {n_distinct} distinct implementors | "
              f"{n_unassigned} unassigned")

    # Join to client_performance
    joined = client_perf.merge(rel_impl, on='relationship_id', how='left')
    joined['implementor'] = joined['implementor'].fillna('Unassigned')

    # Aggregate to (date, implementor) grain
    impl_daily = (
        joined.groupby(['date', 'implementor'], sort=False)
        .agg(
            total_aua=('total_aua', 'sum'),
            cum_inflows=('cum_inflows', 'sum'),
            cum_outflows=('cum_outflows', 'sum'),
            nna=('nna', 'sum'),
            num_relationships=('relationship_id', 'nunique')
        )
        .reset_index()
    )

    if verbose:
        n_impl_advisors = impl_daily[impl_daily['implementor'] != 'Unassigned']['implementor'].nunique()
        print(f"  Built {len(impl_daily):,} rows across {n_impl_advisors} implementors")

    return impl_daily


# ---------------------------------------------------------------------------
# Rolling window computation
# ---------------------------------------------------------------------------

def _slugify(name: str) -> str:
    """Convert an advisor name to a lowercase underscore slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    return slug


def compute_rolling_series(daily_df: pd.DataFrame,
                            advisor_col: str,
                            advisor_prefix: str,
                            verbose: bool = False) -> list:
    """
    Given a daily timeseries with cumulative cum_inflows, cum_outflows, nna
    per advisor, compute rolling window series for each non-Unassigned advisor.

    Rolling method:
        For each date D and window W (in days):
            Find the latest data date <= (D - W days) for this advisor.
            roll_val[D] = cum_val[D] - cum_val[that_past_date]
        Data points where no past date exists are excluded (insufficient history).

    Returns list of advisor dicts matching the output schema.
    """
    advisors_out = []

    sorted_df = daily_df.sort_values(['date']).reset_index(drop=True)
    unique_advisors = (
        sorted_df[sorted_df[advisor_col] != 'Unassigned'][advisor_col].unique()
    )

    if verbose:
        print(f"  Computing rolling series for {len(unique_advisors)} {advisor_prefix}s...")

    for advisor_name in unique_advisors:
        adv = (
            sorted_df[sorted_df[advisor_col] == advisor_name]
            .sort_values('date')
            .reset_index(drop=True)
        )

        if adv.empty:
            continue

        series = {}
        for window_label, window_days in WINDOWS.items():
            window_td = pd.Timedelta(days=window_days)

            # Build "past" lookup: for each row, find cum values ~W days ago
            # merge_asof finds the latest row with date <= (current_date - window_td)
            adv_lookup = adv[['date', 'cum_inflows', 'cum_outflows', 'nna']].copy()
            adv_current = adv[['date', 'cum_inflows', 'cum_outflows', 'nna']].copy()
            adv_current['target_date'] = adv_current['date'] - window_td

            lagged = pd.merge_asof(
                adv_current.sort_values('target_date'),
                adv_lookup.rename(columns={
                    'date': 'past_date',
                    'cum_inflows': 'past_inflows',
                    'cum_outflows': 'past_outflows',
                    'nna': 'past_nna'
                }).sort_values('past_date'),
                left_on='target_date',
                right_on='past_date',
                direction='backward'
            )

            # Drop rows with no valid past date (insufficient history for this window)
            valid = lagged[lagged['past_date'].notna()].copy()

            valid['roll_inflows']  = valid['cum_inflows']  - valid['past_inflows']
            valid['roll_outflows'] = valid['cum_outflows'] - valid['past_outflows']
            valid['roll_nna']      = valid['nna']          - valid['past_nna']

            # Outflows are stored as positive cumulative sums; rolling diff stays positive
            series[window_label] = [
                {
                    'date':     row['date'].strftime('%Y-%m-%d'),
                    'nna':      round(float(row['roll_nna']), 2),
                    'inflows':  round(float(row['roll_inflows']), 2),
                    'outflows': round(float(row['roll_outflows']), 2)
                }
                for _, row in valid.sort_values('date').iterrows()
            ]

        advisor_id = f"{advisor_prefix}_{_slugify(advisor_name)}"
        advisors_out.append({
            'advisor_name': str(advisor_name),
            'advisor_id':   advisor_id,
            'series':       series
        })

    # Sort by most recent AUA (use length of series as proxy for history richness)
    # Primary sort: descending by 1Y series length, then by name for stability
    advisors_out.sort(key=lambda x: (-len(x['series'].get('1Y', [])), x['advisor_name']))

    if verbose:
        for a in advisors_out:
            pts_30d = len(a['series'].get('30d', []))
            pts_1Y  = len(a['series'].get('1Y', []))
            print(f"    {a['advisor_name']}: 30d={pts_30d} pts, 1Y={pts_1Y} pts")

    return advisors_out


# ---------------------------------------------------------------------------
# MTD / QTD / YTD summary (donut chart data)
# ---------------------------------------------------------------------------

def _get_period_boundaries(ref_date: pd.Timestamp) -> dict:
    """
    Compute current + prior period boundaries for MTD, QTD, YTD.

    Returns dict with current and prior period dates for each label.
    Prior periods are the immediately preceding complete period of the same type.
    """
    # --- Current periods ---
    mtd_start = pd.Timestamp(ref_date.year, ref_date.month, 1)

    q_month = ((ref_date.month - 1) // 3) * 3 + 1
    qtd_start = pd.Timestamp(ref_date.year, q_month, 1)

    ytd_start = pd.Timestamp(ref_date.year, 1, 1)

    # --- Prior periods (complete, immediately preceding) ---
    # Prior month: full previous month
    if ref_date.month == 1:
        prior_mtd_start = pd.Timestamp(ref_date.year - 1, 12, 1)
        prior_mtd_end   = pd.Timestamp(ref_date.year - 1, 12, 31)
    else:
        prior_mtd_start = pd.Timestamp(ref_date.year, ref_date.month - 1, 1)
        prior_mtd_end   = mtd_start - pd.Timedelta(days=1)

    # Prior quarter: full previous quarter
    if q_month == 1:
        prior_qtd_start = pd.Timestamp(ref_date.year - 1, 10, 1)
        prior_qtd_end   = pd.Timestamp(ref_date.year - 1, 12, 31)
    else:
        prior_q_month   = q_month - 3
        prior_qtd_start = pd.Timestamp(ref_date.year, prior_q_month, 1)
        prior_qtd_end   = qtd_start - pd.Timedelta(days=1)

    # Prior YTD: same calendar range last year (Jan 1 to same day-of-year)
    prior_ytd_start = pd.Timestamp(ref_date.year - 1, 1, 1)
    prior_ytd_end   = pd.Timestamp(ref_date.year - 1, ref_date.month, min(ref_date.day, 28))
    # Use min(day, 28) to avoid Feb 29 issues; merge_asof will find closest available date

    def _label_month(dt):
        return dt.strftime('%b %Y')

    def _label_quarter(dt):
        return f"Q{(dt.month - 1) // 3 + 1} {dt.year}"

    return {
        'mtd': {
            'start': mtd_start,
            'display': _label_month(ref_date),
            'prior_start': prior_mtd_start,
            'prior_end': prior_mtd_end,
            'prior_display': _label_month(prior_mtd_start),
            'growth_label': 'MoM',
        },
        'qtd': {
            'start': qtd_start,
            'display': _label_quarter(ref_date),
            'prior_start': prior_qtd_start,
            'prior_end': prior_qtd_end,
            'prior_display': _label_quarter(prior_qtd_start),
            'growth_label': 'QoQ',
        },
        'ytd': {
            'start': ytd_start,
            'display': str(ref_date.year),
            'prior_start': prior_ytd_start,
            'prior_end': prior_ytd_end,
            'prior_display': str(ref_date.year - 1),
            'growth_label': 'YoY',
        },
    }


def _compute_nna_for_range(sorted_df: pd.DataFrame, advisor_col: str,
                            start_date: pd.Timestamp, end_date: pd.Timestamp) -> dict:
    """
    Compute NNA/inflows/outflows for each advisor over [start_date, end_date].
    Returns dict keyed by advisor_name -> {nna, inflows, outflows}.
    """
    all_dates = sorted_df['date'].sort_values().unique()

    # End snapshot: closest date <= end_date
    end_dates = all_dates[all_dates <= end_date]
    if len(end_dates) == 0:
        return {}
    actual_end = end_dates.max()

    # Base snapshot: closest date < start_date
    base_dates = all_dates[all_dates < start_date]
    if len(base_dates) == 0:
        actual_base = all_dates.min()
    else:
        actual_base = base_dates.max()

    end_snap  = sorted_df[sorted_df['date'] == actual_end].set_index(advisor_col)
    base_snap = sorted_df[sorted_df['date'] == actual_base].set_index(advisor_col)

    result = {}
    for adv_name in end_snap.index:
        if adv_name == 'Unassigned':
            continue
        end_row = end_snap.loc[adv_name]
        if isinstance(end_row, pd.DataFrame):
            end_row = end_row.iloc[0]

        nna_end = float(end_row.get('nna', 0) or 0)
        inf_end = float(end_row.get('cum_inflows', 0) or 0)
        out_end = float(end_row.get('cum_outflows', 0) or 0)

        if adv_name in base_snap.index:
            base_row = base_snap.loc[adv_name]
            if isinstance(base_row, pd.DataFrame):
                base_row = base_row.iloc[0]
            nna_base = float(base_row.get('nna', 0) or 0)
            inf_base = float(base_row.get('cum_inflows', 0) or 0)
            out_base = float(base_row.get('cum_outflows', 0) or 0)
        else:
            nna_base = inf_base = out_base = 0.0

        result[str(adv_name)] = {
            'nna':      round(nna_end - nna_base, 2),
            'inflows':  round(inf_end - inf_base, 2),
            'outflows': round(out_end - out_base, 2),
        }
    return result


def compute_period_summary(daily_df: pd.DataFrame,
                            advisor_col: str,
                            advisor_prefix: str,
                            latest_date: pd.Timestamp,
                            client_dim: pd.DataFrame = None,
                            advisor_map_col: str = None,
                            verbose: bool = False) -> dict:
    """
    Compute MTD/QTD/YTD summary with prior-period comparison, growth rates,
    AUA, new clients, and rank changes.

    Each period includes:
    - Current period NNA/inflows/outflows per advisor (donut segments)
    - Prior period NNA per advisor (for growth calculation)
    - MoM/QoQ/YoY growth percentages (total and per advisor)
    - Rank and rank_change vs prior period
    - AUA and client_count from latest snapshot
    - new_clients from client_dimension.first_seen_date
    """
    periods = _get_period_boundaries(latest_date)
    sorted_df = daily_df.sort_values(['date']).reset_index(drop=True)

    # Latest snapshot for AUA + client count
    latest_snap = sorted_df[sorted_df['date'] == latest_date].set_index(advisor_col)

    # New clients lookup: count of relationships with first_seen_date in period
    # Keyed by (advisor_name, period_start) -> count
    new_clients_cache = {}
    if client_dim is not None and advisor_map_col and advisor_map_col in client_dim.columns:
        for period_label, pinfo in periods.items():
            period_start = pinfo['start']
            new_in_period = client_dim[
                (client_dim['first_seen_date'] >= period_start) &
                (client_dim['first_seen_date'] <= latest_date)
            ]
            if not new_in_period.empty:
                counts = new_in_period.groupby(advisor_map_col)['relationship_id'].nunique()
                for adv_name, cnt in counts.items():
                    new_clients_cache[(str(adv_name), period_label)] = int(cnt)

    result = {}

    for period_label, pinfo in periods.items():
        # Current period
        current_data = _compute_nna_for_range(
            sorted_df, advisor_col, pinfo['start'], latest_date
        )

        # Prior period
        prior_data = _compute_nna_for_range(
            sorted_df, advisor_col, pinfo['prior_start'], pinfo['prior_end']
        )

        # Build segments sorted by current NNA
        segments = []
        for adv_name, cur in current_data.items():
            prior = prior_data.get(adv_name, {'nna': 0, 'inflows': 0, 'outflows': 0})

            # AUA + client count from latest snapshot
            aua = 0.0
            client_count = 0
            if adv_name in latest_snap.index:
                snap_row = latest_snap.loc[adv_name]
                if isinstance(snap_row, pd.DataFrame):
                    snap_row = snap_row.iloc[0]
                aua = float(snap_row.get('total_aua', 0) or 0)
                client_count = int(snap_row.get('num_relationships', 0) or 0)

            new_clients = new_clients_cache.get((adv_name, period_label), 0)

            # Growth: current vs prior NNA
            prior_nna = prior['nna']
            nna_growth_pct = (
                round((cur['nna'] - prior_nna) / abs(prior_nna) * 100, 1)
                if abs(prior_nna) > 100 else 0.0  # avoid div-by-near-zero
            )

            segments.append({
                'advisor_name':    adv_name,
                'advisor_id':      f"{advisor_prefix}_{_slugify(adv_name)}",
                'nna':             cur['nna'],
                'inflows':         cur['inflows'],
                'outflows':        cur['outflows'],
                'total_aua':       round(aua, 2),
                'client_count':    client_count,
                'new_clients':     new_clients,
                'prior_nna':       prior_nna,
                'nna_growth_pct':  nna_growth_pct,
            })

        # Sort by NNA descending, assign ranks
        segments.sort(key=lambda x: x['nna'], reverse=True)
        for i, seg in enumerate(segments):
            seg['rank'] = i + 1

        # Compute prior ranks for rank_change
        prior_ranked = sorted(segments, key=lambda x: x['prior_nna'], reverse=True)
        prior_rank_map = {s['advisor_name']: i + 1 for i, s in enumerate(prior_ranked)}
        for seg in segments:
            prior_rank = prior_rank_map.get(seg['advisor_name'], seg['rank'])
            seg['prior_rank']   = prior_rank
            seg['rank_change']  = prior_rank - seg['rank']  # positive = moved up

        # Totals
        total_nna      = sum(s['nna'] for s in segments)
        total_inflows  = sum(s['inflows'] for s in segments)
        total_outflows = sum(s['outflows'] for s in segments)
        prior_total_nna = sum(s['prior_nna'] for s in segments)

        total_growth_pct = (
            round((total_nna - prior_total_nna) / abs(prior_total_nna) * 100, 1)
            if abs(prior_total_nna) > 100 else 0.0
        )

        # nna_pct + colors on top segments, Other bucket for remainder
        abs_total = sum(abs(s['nna']) for s in segments)
        top_segments   = segments[:MAX_DONUT_SEGMENTS]
        other_segments = segments[MAX_DONUT_SEGMENTS:]

        for i, seg in enumerate(top_segments):
            seg['nna_pct'] = round(abs(seg['nna']) / abs_total * 100, 1) if abs_total > 0 else 0.0
            seg['color'] = DONUT_COLORS[i % len(DONUT_COLORS)]

        if other_segments:
            other_nna      = sum(s['nna'] for s in other_segments)
            other_inflows  = sum(s['inflows'] for s in other_segments)
            other_outflows = sum(s['outflows'] for s in other_segments)
            other_aua      = sum(s['total_aua'] for s in other_segments)
            other_clients  = sum(s['client_count'] for s in other_segments)
            other_new      = sum(s['new_clients'] for s in other_segments)
            other_prior    = sum(s['prior_nna'] for s in other_segments)
            other_growth   = (
                round((other_nna - other_prior) / abs(other_prior) * 100, 1)
                if abs(other_prior) > 100 else 0.0
            )
            top_segments.append({
                'advisor_name': 'Other',
                'advisor_id':   f'{advisor_prefix}_other',
                'nna':          round(other_nna, 2),
                'nna_pct':      round(abs(other_nna) / abs_total * 100, 1) if abs_total > 0 else 0.0,
                'inflows':      round(other_inflows, 2),
                'outflows':     round(other_outflows, 2),
                'total_aua':    round(other_aua, 2),
                'client_count': other_clients,
                'new_clients':  other_new,
                'prior_nna':    round(other_prior, 2),
                'nna_growth_pct': other_growth,
                'rank': MAX_DONUT_SEGMENTS + 1,
                'prior_rank': MAX_DONUT_SEGMENTS + 1,
                'rank_change': 0,
                'color':        OTHER_COLOR,
            })

        result[period_label] = {
            'period_start':   pinfo['start'].strftime('%Y-%m-%d'),
            'period_end':     latest_date.strftime('%Y-%m-%d'),
            'display':        pinfo['display'],
            'growth_label':   pinfo['growth_label'],
            'total_nna':      round(total_nna, 2),
            'total_inflows':  round(total_inflows, 2),
            'total_outflows': round(total_outflows, 2),
            'prior': {
                'period_start': pinfo['prior_start'].strftime('%Y-%m-%d'),
                'period_end':   pinfo['prior_end'].strftime('%Y-%m-%d'),
                'display':      pinfo['prior_display'],
                'total_nna':    round(prior_total_nna, 2),
            },
            'growth_pct':     total_growth_pct,
            'segments':       top_segments,
        }

        if verbose:
            n_pos = sum(1 for s in segments if s['nna'] >= 0)
            n_neg = len(segments) - n_pos
            print(f"  {period_label}: NNA ${total_nna:,.0f} ({pinfo['growth_label']} "
                  f"{total_growth_pct:+.1f}%) | {n_pos} positive, {n_neg} negative | "
                  f"top={top_segments[0]['advisor_name'] if top_segments else 'N/A'}")

    return result


# ---------------------------------------------------------------------------
# Stacked bar (ADVI-005 A3.1)
# ---------------------------------------------------------------------------

def compute_stacked_bar(daily_df: pd.DataFrame,
                         advisor_col: str,
                         advisor_prefix: str,
                         latest_date: pd.Timestamp,
                         verbose: bool = False) -> dict:
    """
    Compute period-aggregated inflows/outflows/nna_net per advisor for stacked bar.

    Returns dict keyed by STACKED_BAR_PERIODS ('qtd','ytd','1y','3y','max'),
    each mapping to a list of AdvisorBarEntry dicts:
        { advisor_name, advisor_id, inflows, outflows, nna_net }
    Outflows: positive magnitude (>= 0). nna_net: signed.

    Period boundaries:
        qtd, ytd: calendar-anchored via _get_period_boundaries().
        1y, 3y:   trailing windows (365 / 1095 days from latest_date).
        max:      inception-to-date (earliest date present in daily_df).
    """
    sorted_df = daily_df.sort_values('date').reset_index(drop=True)
    all_dates  = sorted_df['date'].sort_values().unique()
    inception  = pd.Timestamp(all_dates.min())
    cal        = _get_period_boundaries(latest_date)

    period_starts = {
        'qtd': cal['qtd']['start'],
        'ytd': cal['ytd']['start'],
        '1y':  latest_date - pd.Timedelta(days=365),
        '3y':  latest_date - pd.Timedelta(days=365 * 3),
        'max': inception,
    }

    result = {}
    for period_key in STACKED_BAR_PERIODS:
        start_date = period_starts[period_key]
        flows_by_advisor = _compute_nna_for_range(
            sorted_df, advisor_col, start_date, latest_date
        )
        entries = [
            {
                'advisor_name': adv_name,
                'advisor_id':   f"{advisor_prefix}_{_slugify(adv_name)}",
                'inflows':      round(data['inflows'], 2),
                'outflows':     round(data['outflows'], 2),   # positive magnitude
                'nna_net':      round(data['nna'], 2),        # signed
            }
            for adv_name, data in flows_by_advisor.items()
        ]
        result[period_key] = entries
        if verbose:
            total_nna = sum(e['nna_net'] for e in entries)
            print(f"  stacked_bar {period_key} ({advisor_prefix}): "
                  f"{len(entries)} advisors, total NNA ${total_nna:,.0f}")

    # Y13: Monthly granularity — per-month NNA entries for interval toggle
    # Each month key maps to a list of AdvisorBarEntry (same shape as period entries)
    monthly = {}
    all_months = sorted(set(pd.Timestamp(d).to_period('M') for d in all_dates))
    for ym in all_months:
        month_start = ym.start_time
        month_end_date = ym.end_time.normalize()
        # Use latest available date within this month
        month_dates = all_dates[(all_dates >= month_start) & (all_dates <= month_end_date)]
        if len(month_dates) == 0:
            continue
        actual_end = pd.Timestamp(month_dates.max())
        flows = _compute_nna_for_range(sorted_df, advisor_col, month_start, actual_end)
        month_entries = [
            {
                'advisor_name': adv_name,
                'advisor_id':   f"{advisor_prefix}_{_slugify(adv_name)}",
                'inflows':      round(data['inflows'], 2),
                'outflows':     round(data['outflows'], 2),
                'nna_net':      round(data['nna'], 2),
            }
            for adv_name, data in flows.items()
        ]
        monthly[str(ym)] = month_entries
    result['monthly'] = monthly

    if verbose:
        print(f"  stacked_bar monthly ({advisor_prefix}): {len(monthly)} months")

    return result


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def generate_advisor_rolling_flows(verbose: bool = False) -> dict:
    """
    Load data, compute rolling series for architects and implementors,
    return JSON-ready dict.
    """
    adv_ts, client_perf, acct_dim, client_dim = load_data(verbose=verbose)

    data_as_of = adv_ts['date'].max().strftime('%Y-%m-%d')
    latest_date = adv_ts['date'].max()
    print(f"Data as of: {data_as_of}")

    # --- Architects: use pre-aggregated nna_aua_by_advisor ---
    print("Processing architects...")
    adv_clean = adv_ts[
        adv_ts['architect'].notna() &
        ~adv_ts['architect'].str.strip().str.lower().isin(MODAL_NULLS)
    ].copy()
    architects = compute_rolling_series(adv_clean, 'architect', 'arch', verbose=verbose)

    # --- Implementors: build daily view on-the-fly, then compute rolling ---
    print("Processing implementors...")
    impl_daily = build_implementor_daily(client_perf, acct_dim, verbose=verbose)
    if impl_daily.empty or impl_daily['implementor'].nunique() <= 1:
        print("  WARN: No implementor data available -- implementors list will be empty")
        implementors = []
    else:
        impl_clean = impl_daily[
            impl_daily['implementor'].notna() &
            ~impl_daily['implementor'].str.strip().str.lower().isin(MODAL_NULLS)
        ].copy()
        implementors = compute_rolling_series(impl_clean, 'implementor', 'impl', verbose=verbose)

    # --- MTD/QTD/YTD summary (donut chart default view) ---
    print("Computing MTD/QTD/YTD summary for architects...")
    arch_summary = compute_period_summary(
        adv_clean, 'architect', 'arch', latest_date,
        client_dim=client_dim, advisor_map_col='primary_architect',
        verbose=verbose
    )

    if impl_daily.empty or impl_daily['implementor'].nunique() <= 1:
        impl_summary = {'mtd': _empty_period(), 'qtd': _empty_period(), 'ytd': _empty_period()}
    else:
        print("Computing MTD/QTD/YTD summary for implementors...")
        impl_summary = compute_period_summary(
            impl_clean, 'implementor', 'impl', latest_date,
            client_dim=client_dim, advisor_map_col='primary_implementor',
            verbose=verbose
        )

    # --- ADVI-005 A3.1: stacked_bar ---
    print("Computing stacked_bar for architects...")
    arch_stacked = compute_stacked_bar(adv_clean, 'architect', 'arch',
                                        latest_date, verbose=verbose)

    if not (impl_daily.empty or impl_daily['implementor'].nunique() <= 1):
        print("Computing stacked_bar for implementors...")
        impl_stacked = compute_stacked_bar(impl_clean, 'implementor', 'impl',
                                            latest_date, verbose=verbose)
    else:
        impl_stacked = {p: [] for p in STACKED_BAR_PERIODS}

    # Period-outer / role-inner nesting per task order A3.1 (CTO correction)
    stacked_bar = {
        period: {
            'architects':   arch_stacked[period],
            'implementors': impl_stacked[period],
        }
        for period in STACKED_BAR_PERIODS
    }

    # --- ADVI-005 A3.2: rolling_1y ---
    # Reuses existing 1Y window series from compute_rolling_series().
    # Full history emitted; frontend slices x-axis by period toggle.
    rolling_1y = {
        'architects': [
            {
                'advisor_name': a['advisor_name'],
                'advisor_id':   a['advisor_id'],
                'series':       a['series'].get('1Y', []),
            }
            for a in architects
        ],
        'implementors': [
            {
                'advisor_name': a['advisor_name'],
                'advisor_id':   a['advisor_id'],
                'series':       a['series'].get('1Y', []),
            }
            for a in implementors
        ],
    }
    print(f"rolling_1y: {len(rolling_1y['architects'])} architects, "
          f"{len(rolling_1y['implementors'])} implementors")

    # Validation
    if architects:
        sample = architects[0]
        sample_30d = sample['series'].get('30d', [])
        sample_1Y  = sample['series'].get('1Y', [])
        print(f"Validation: {len(architects)} architects, {len(implementors)} implementors")
        print(f"  Sample ({sample['advisor_name']}): 30d={len(sample_30d)} pts, 1Y={len(sample_1Y)} pts")
        if sample_30d:
            pt = sample_30d[-1]
            computed_nna = round(pt['inflows'] - pt['outflows'], 2)
            if abs(computed_nna - pt['nna']) > 1.0:
                print(f"  WARN: nna mismatch on sample point: "
                      f"inflows-outflows={computed_nna} vs nna={pt['nna']}")
            else:
                print(f"  OK: nna == inflows - outflows check passed on latest 30d point")

    if arch_summary.get('qtd'):
        qtd = arch_summary['qtd']
        print(f"  Summary QTD: {len(qtd['segments'])} segments, total NNA ${qtd['total_nna']:,.0f}")

    return {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_as_of':   data_as_of,
        'firm_id':      FIRM_ID,
        'summary': {
            'architects':   arch_summary,
            'implementors': impl_summary,
        },
        'architects':   architects,
        'implementors': implementors,
        'stacked_bar':  stacked_bar,   # ADVI-005 A3.1
        'rolling_1y':   rolling_1y,    # ADVI-005 A3.2
    }


def _empty_period() -> dict:
    """Return an empty period summary for when no data is available."""
    return {
        'period_start': '', 'period_end': '', 'display': '',
        'total_nna': 0, 'total_inflows': 0, 'total_outflows': 0,
        'segments': []
    }


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def write_local(payload: dict, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"OK: Written to {path} ({path.stat().st_size:,} bytes)")


def write_s3(payload: dict) -> None:
    body = json.dumps(payload, indent=2, default=str).encode('utf-8')
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=OUTPUT_KEY,
        Body=body,
        ContentType='application/json',
        CacheControl='public, max-age=300, s-maxage=3600'
    )
    print(f"OK: Uploaded to s3://{OUTPUT_BUCKET}/{OUTPUT_KEY} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate advisor_rolling_flows.json from gold tables'
    )
    parser.add_argument(
        '--upload', action='store_true',
        help=f'Upload output to s3://{OUTPUT_BUCKET}/{OUTPUT_KEY}'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Compute and validate but do not write anywhere'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help=f'Local output path (default: {DEFAULT_LOCAL_OUTPUT})'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose logging'
    )
    args = parser.parse_args()

    print('============================================================')
    print('10_generate_advisor_rolling_flows.py')
    print(f'Started: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('============================================================')

    payload = generate_advisor_rolling_flows(verbose=args.verbose)

    if args.dry_run:
        print("OK: Dry run complete -- no output written")
        # Summary preview
        for role in ('architects', 'implementors'):
            summary = payload['summary'][role]
            print(f"  {role} summary:")
            for period in ('mtd', 'qtd', 'ytd'):
                p = summary[period]
                n_seg = len(p.get('segments', []))
                print(f"    {period}: NNA=${p['total_nna']:,.0f} ({n_seg} segments)")
        # Rolling series preview (legacy)
        for adv_type in ('architects', 'implementors'):
            advisors = payload[adv_type]
            print(f"  {adv_type} rolling: {len(advisors)} advisors")
            for a in advisors[:3]:
                pts = {w: len(a['series'].get(w, [])) for w in ('30d', '90d', '1Y')}
                print(f"    {a['advisor_name']}: {pts}")
        # stacked_bar preview
        sb = payload.get('stacked_bar', {})
        print(f"  stacked_bar periods: {list(sb.keys())}")
        for period, roles in sb.items():
            n_arch = len(roles.get('architects', []))
            n_impl = len(roles.get('implementors', []))
            print(f"    {period}: {n_arch} architects, {n_impl} implementors")
        # rolling_1y preview
        ry = payload.get('rolling_1y', {})
        for role in ('architects', 'implementors'):
            advisors = ry.get(role, [])
            print(f"  rolling_1y {role}: {len(advisors)} advisors")
            for a in advisors[:3]:
                pts = len(a.get('series', []))
                first = a['series'][0]['date'] if a.get('series') else 'N/A'
                last  = a['series'][-1]['date'] if a.get('series') else 'N/A'
                print(f"    {a['advisor_name']}: {pts} pts | {first} -> {last}")
        sys.exit(0)

    if args.upload:
        write_s3(payload)
    else:
        output_path = args.output or DEFAULT_LOCAL_OUTPUT
        write_local(payload, output_path)

    print('============================================================')
    print(f'COMPLETE: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('============================================================')


if __name__ == '__main__':
    main()
