#!/usr/bin/env python3
"""
Generate Partner Analytics — header_metrics.json (Multi-Granularity)

CHANGE (2026-03-05): Now generates NMNC/NMEC classifications at all three
granularities (quarterly, monthly, annual) to support frontend toggles.

Produces three portal-ready JSONs to S3:
    s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json
    s3://opal-data-bd/gold/partner_analytics/header_metrics_monthly.json
    s3://opal-data-bd/gold/partner_analytics/header_metrics_annual.json

Each JSON has granularity-appropriate NMNC/NMEC classifications:
- NMNC (New Client Assets) = first_seen_date > period_start_ts
- Period boundaries are quarterly (Q1/Q2/Q3), monthly (m1/m2/m3), or annual (y1/y2/y3)

Data sources (all from s3://opal-data-bd):
    gold/client_performance.parquet           -- primary AUA source (daily x relationship)
    gold/account_performance.parquet          -- account-level AUA for distributions (~90MB)
    gold/accounts_dimension_latest.parquet    -- city/state/architect metadata
    gold/client_dimension.parquet             -- relationship display names
    gold/views/nna_aua_by_geography.parquet   -- pre-aggregated state-level AUA
    gold/views/nna_aua_by_advisor.parquet     -- pre-aggregated advisor-level AUA

Output JSON shape (same for all granularities, only period labels differ):
    {
      "generated_at": "...",
      "data_as_of": "YYYY-MM-DD",
      "firm_id": "49financial",
      "firm_name": "49 Financial",
      "granularity": "quarterly|monthly|annual",
      "periods": { "current": {...}, "q1|m1|y1": {...}, ... },
      "views": {
        "aua": { ... },                    // AUA by tax status donut
        "nna": { ... },                    // Period-differenced NNA
        "geo": { ... },                    // AUA by state donut + cities
        "adv": { ... },                    // AUA by architect donut + clients
        "cla": { ... }                     // NMNC/NMEC lifecycle decomposition
      }
    }

Usage:
    python 09_generate_partner_analytics.py               # local test, all 3 granularities
    python 09_generate_partner_analytics.py --upload      # write all 3 to S3
    python 09_generate_partner_analytics.py --granularity quarterly --upload  # only quarterly
    python 09_generate_partner_analytics.py --dry-run     # compute only, no write
    python 09_generate_partner_analytics.py -v            # verbose output

Author: Data Scientist (Claude)
Date: 2026-02-27
Revision: 2026-03-05 (multi-granularity support)
"""

import argparse
import json
import os
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

S3_BUCKET = 'opal-data-bd'
S3_OUTPUT_KEY = 'gold/partner_analytics/header_metrics.json'
DEFAULT_LOCAL_OUTPUT = './gold/partner_analytics/header_metrics.json'

NUM_HISTOGRAM_BINS = 20  # log-spaced bins for bell curve shape
NNA_MATERIALITY_THRESHOLD = 1_000  # $1K -- below this is fees/dividends/rounding, not real flows

MAX_SEGMENTS = 8        # max geo states or advisors in donut
MAX_CITIES = 9          # max cities nested under a state
MAX_CLIENTS_PER_ADVISOR = 15

GEO_COLORS  = ['#F44336', '#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4', '#795548', '#607D8B']
CITY_COLORS = ['#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#2196F3']
ADV_COLORS  = ['#5e72e4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316']
OTHER_COLOR = '#757575'

MODAL_NULLS = frozenset({
    '', 'none', 'nan', 'unassigned', 'unknown', 'n/a',
    'no architect value assigned', 'no state',
})

# NNA blue/red color palettes (rank-ordered, darkest = largest magnitude)
NNA_BLUE_SHADES = ['#1E40AF', '#1D4ED8', '#2563EB', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE']
NNA_RED_SHADES  = ['#991B1B', '#B91C1C', '#DC2626', '#EF4444', '#F87171', '#FCA5A5', '#FECACA', '#FEE2E2']

# CLA lifecycle colors
CLA_NMNC_COLOR     = '#16A34A'   # Green  -- New Client Inflows
CLA_NMEC_POS_COLOR = '#2563EB'   # Blue   -- Existing Client Inflows
CLA_NMEC_NEG_COLOR = '#DC2626'   # Red    -- Existing Client Outflows

# ---------------------------------------------------------------------------
# Period computation
# ---------------------------------------------------------------------------

def get_periods(ref_date: pd.Timestamp, granularity: str = 'quarterly') -> dict:
    """
    Returns periods based on granularity.

    granularity='quarterly': 4 periods (current + 3 trailing completed quarters)
    granularity='monthly':   4 periods (current month + 3 trailing completed months)
    granularity='annual':    4 periods (current year + 3 trailing completed years)

    Example (ref_date = 2026-02-26):
      quarterly:
        current = 2026-02-26
        q1 = 2025-12-31, q2 = 2025-09-30, q3 = 2025-06-30
      monthly:
        current = 2026-02-26
        m1 = 2026-01-31, m2 = 2025-12-31, m3 = 2025-11-30
      annual:
        current = 2026-02-26
        y1 = 2025-12-31, y2 = 2024-12-31, y3 = 2023-12-31
    """
    if granularity == 'quarterly':
        return _get_periods_quarterly(ref_date)
    elif granularity == 'monthly':
        return _get_periods_monthly(ref_date)
    elif granularity == 'annual':
        return _get_periods_annual(ref_date)
    else:
        raise ValueError(f"Unknown granularity: {granularity}")


def _get_periods_quarterly(ref_date: pd.Timestamp) -> dict:
    """Returns 4 periods: current + 3 trailing completed quarter-ends."""
    qe_month_to_label = {3: 'Q1', 6: 'Q2', 9: 'Q3', 12: 'Q4'}

    quarter_ends = []
    dt = ref_date
    for _ in range(8):  # check up to 8 quarters back; we need 3 completed ones
        if dt.month <= 3:
            qe = pd.Timestamp(dt.year - 1, 12, 31)
        elif dt.month <= 6:
            qe = pd.Timestamp(dt.year, 3, 31)
        elif dt.month <= 9:
            qe = pd.Timestamp(dt.year, 6, 30)
        else:
            qe = pd.Timestamp(dt.year, 9, 30)

        if qe < ref_date and qe not in quarter_ends:
            quarter_ends.append(qe)
        dt = qe - pd.DateOffset(days=1)

        if len(quarter_ends) == 3:
            break

    def period_label(qe: pd.Timestamp) -> str:
        quarter_name = qe_month_to_label[qe.month]
        return f"{quarter_name} '{str(qe.year)[2:]}"  # e.g. "Q4 '25"

    q1, q2, q3 = quarter_ends[0], quarter_ends[1], quarter_ends[2]

    return {
        'current': {'date': ref_date.strftime('%Y-%m-%d'), 'label': 'Current', '_ts': ref_date},
        'q1':      {'date': q1.strftime('%Y-%m-%d'), 'label': period_label(q1), '_ts': q1},
        'q2':      {'date': q2.strftime('%Y-%m-%d'), 'label': period_label(q2), '_ts': q2},
        'q3':      {'date': q3.strftime('%Y-%m-%d'), 'label': period_label(q3), '_ts': q3},
    }


def _get_periods_monthly(ref_date: pd.Timestamp) -> dict:
    """Returns 4 periods: current month end + 3 trailing completed month-ends."""
    # Current month end
    if ref_date.month == 12:
        current_month_end = pd.Timestamp(ref_date.year, 12, 31)
    else:
        current_month_end = pd.Timestamp(ref_date.year, ref_date.month + 1, 1) - pd.DateOffset(days=1)

    # Find 3 trailing completed months
    month_ends = []
    dt = current_month_end
    for _ in range(6):  # look back up to 6 months to find 3 completed ones
        if dt < ref_date and dt not in month_ends:
            month_ends.append(dt)
        if len(month_ends) == 3:
            break
        # Move to previous month-end
        dt = pd.Timestamp(dt.year, dt.month, 1) - pd.DateOffset(days=1)

    def month_label(me: pd.Timestamp) -> str:
        month_name = me.strftime('%b')
        return f"{month_name} '{str(me.year)[2:]}"  # e.g. "Jan '26"

    m1, m2, m3 = month_ends[0], month_ends[1], month_ends[2]

    return {
        'current': {'date': ref_date.strftime('%Y-%m-%d'), 'label': 'Current', '_ts': ref_date},
        'm1':      {'date': m1.strftime('%Y-%m-%d'), 'label': month_label(m1), '_ts': m1},
        'm2':      {'date': m2.strftime('%Y-%m-%d'), 'label': month_label(m2), '_ts': m2},
        'm3':      {'date': m3.strftime('%Y-%m-%d'), 'label': month_label(m3), '_ts': m3},
    }


def _get_periods_annual(ref_date: pd.Timestamp) -> dict:
    """Returns 4 periods: current year-end + 3 trailing completed year-ends."""
    current_year_end = pd.Timestamp(ref_date.year, 12, 31)

    # Find 3 trailing completed years
    year_ends = []
    dt = current_year_end
    for _ in range(6):  # look back up to 6 years
        if dt < ref_date and dt not in year_ends:
            year_ends.append(dt)
        if len(year_ends) == 3:
            break
        dt = pd.Timestamp(dt.year - 1, 12, 31)

    def year_label(ye: pd.Timestamp) -> str:
        return f"{ye.year}"

    y1, y2, y3 = year_ends[0], year_ends[1], year_ends[2]

    return {
        'current': {'date': ref_date.strftime('%Y-%m-%d'), 'label': 'Current', '_ts': ref_date},
        'y1':      {'date': y1.strftime('%Y-%m-%d'), 'label': year_label(y1), '_ts': y1},
        'y2':      {'date': y2.strftime('%Y-%m-%d'), 'label': year_label(y2), '_ts': y2},
        'y3':      {'date': y3.strftime('%Y-%m-%d'), 'label': year_label(y3), '_ts': y3},
    }


def get_period_pairs(periods: dict, granularity: str = 'quarterly') -> dict:
    """
    For each period, determine (end_ts, start_ts) for NNA period differencing.

    Period NNA = cum_nna(end) - cum_nna(start).  Start is the prior period-end.
    NMNC classification: first_seen_date > start_ts.

    Mapping varies by granularity:
      quarterly:  current→q1→q2→q3→(prior quarter)
      monthly:    current→m1→m2→m3→(prior month)
      annual:     current→y1→y2→y3→(prior year)
    """
    keys = list(periods.keys())  # ['current', 'q1'/'m1'/'y1', 'q2'/'m2'/'y2', 'q3'/'m3'/'y3']
    pairs = {}
    for i, key in enumerate(keys):
        end_ts = periods[key]['_ts']
        if i + 1 < len(keys):
            start_ts = periods[keys[i + 1]]['_ts']
        else:
            # Last period's prior: compute one more period-end back
            last_ts = periods[keys[-1]]['_ts']
            if granularity == 'quarterly':
                # One more quarter back
                if last_ts.month == 3:
                    start_ts = pd.Timestamp(last_ts.year - 1, 12, 31)
                elif last_ts.month == 6:
                    start_ts = pd.Timestamp(last_ts.year, 3, 31)
                elif last_ts.month == 9:
                    start_ts = pd.Timestamp(last_ts.year, 6, 30)
                else:
                    start_ts = pd.Timestamp(last_ts.year, 9, 30)
            elif granularity == 'monthly':
                # One more month back
                start_ts = pd.Timestamp(last_ts.year, last_ts.month, 1) - pd.DateOffset(days=1)
            elif granularity == 'annual':
                # One more year back
                start_ts = pd.Timestamp(last_ts.year - 1, 12, 31)
            else:
                raise ValueError(f"Unknown granularity: {granularity}")
        pairs[key] = {'end': end_ts, 'start': start_ts}
    return pairs


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(verbose: bool = False) -> tuple:
    """
    Load all required gold tables from S3.
    Returns: (client_perf, acct_perf, acct_dim, client_dim, geo_ts, adv_ts)

    account_performance is ~90MB — read once, filter to target dates in memory.
    """
    s3 = boto3.client('s3', region_name='us-east-1')

    def _read(key: str) -> pd.DataFrame:
        if verbose:
            print(f"  Loading s3://{S3_BUCKET}/{key}")
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return pd.read_parquet(BytesIO(resp['Body'].read()))

    client_perf = _read('gold/client_performance.parquet')
    acct_perf   = _read('gold/account_performance.parquet')
    acct_dim    = _read('gold/accounts_dimension_latest.parquet')
    client_dim  = _read('gold/client_dimension.parquet')
    geo_ts      = _read('gold/views/nna_aua_by_geography.parquet')
    adv_ts      = _read('gold/views/nna_aua_by_advisor.parquet')
    rel_lookup_df = _read('gold/views/rel_architect_lookup.parquet')

    # Normalize date columns to pd.Timestamp
    for df in (client_perf, acct_perf, geo_ts, adv_ts):
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

    # Convert lookup to Series indexed by relationship_id (same interface as before)
    rel_arch_lookup = rel_lookup_df.set_index('relationship_id')['architect']

    return client_perf, acct_perf, acct_dim, client_dim, geo_ts, adv_ts, rel_arch_lookup


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def _build_rel_geo_lookup(acct_dim: pd.DataFrame) -> pd.Series:
    """
    Derive relationship_id -> modal state from accounts dimension.

    Same logic as script 07 (modal non-null state per relationship).
    Returns a Series indexed by relationship_id with values = state string.
    """
    if 'client_state' not in acct_dim.columns:
        return pd.Series(dtype=str, name='state')

    def _modal_state(s: pd.Series) -> str:
        clean = s.dropna().astype(str).str.strip()
        clean = clean[~clean.str.lower().isin(MODAL_NULLS)]
        return clean.mode().iloc[0] if not clean.empty else 'Unknown'

    return (
        acct_dim
        .groupby('relationship_id')['client_state']
        .agg(_modal_state)
        .rename('state')
    )


def _build_rel_city_lookup(acct_dim: pd.DataFrame) -> pd.Series:
    """
    Derive relationship_id -> modal city from accounts dimension.

    Returns a Series indexed by relationship_id with values = city string.
    Used for Y6b city-level NNA distribution drill-down.
    """
    if 'client_city' not in acct_dim.columns:
        return pd.Series(dtype=str, name='city')

    def _modal_city(s: pd.Series) -> str:
        clean = s.dropna().astype(str).str.strip()
        clean = clean[~clean.str.lower().isin(MODAL_NULLS)]
        return clean.mode().iloc[0] if not clean.empty else 'Unknown'

    return (
        acct_dim
        .groupby('relationship_id')['client_city']
        .agg(_modal_city)
        .rename('city')
    )


# ---------------------------------------------------------------------------
# Distribution stats
# ---------------------------------------------------------------------------

def _fmt_currency(val: float) -> str:
    """Format a dollar value for bin labels ($1K, $250K, $1.2M etc.)."""
    sign = '-' if val < 0 else ''
    val = abs(val)
    if val >= 1_000_000:
        return f"{sign}${val / 1_000_000:.1f}M"
    elif val >= 1_000:
        return f"{sign}${val / 1_000:.0f}K"
    return f"{sign}${val:.0f}"


def calculate_distribution_stats(aua_values: pd.Series) -> dict:
    """
    Compute histogram + percentile stats for an array of AUA values.
    Uses log-spaced bins (same approach as Model Portfolios) so the bell
    curve is visible even when the median is low.

    Returns dict matching the portal's DistributionStats TypeScript interface.
    """
    vals = aua_values.dropna()
    vals = vals[vals > 0]

    if vals.empty:
        return {
            'count':   0,
            'total':   0,
            'mean':    None,
            'median':  None,
            'min':     None,
            'max':     None,
            'std_dev': None,
            'percentiles': {'p10': None, 'p25': None, 'p50': None, 'p75': None, 'p90': None},
            'histogram': {'bins': [], 'counts': [], 'bin_labels': []},
        }

    n = len(vals)

    # Log-spaced bins for proper bell curve shape
    min_val = max(float(vals.min()), 1_000)   # floor at $1K
    max_val = float(vals.max())

    # Guard: single-value or identical-value edge case (e.g. one-account relationship)
    # produces degenerate bins where all edges collapse to a single point.
    if max_val <= min_val:
        max_val = min_val * 2

    bin_edges = np.logspace(np.log10(min_val), np.log10(max_val), NUM_HISTOGRAM_BINS + 1)
    counts, _ = np.histogram(vals, bins=bin_edges)

    bin_labels = [
        f"{_fmt_currency(bin_edges[i])}-{_fmt_currency(bin_edges[i + 1])}"
        for i in range(len(bin_edges) - 1)
    ]

    return {
        'count':   n,
        'total':   round(float(vals.sum()), 2),
        'mean':    round(float(vals.mean()), 2),
        'median':  round(float(vals.median()), 2),
        'min':     round(float(vals.min()), 2),
        'max':     round(float(vals.max()), 2),
        'std_dev': round(float(vals.std()), 2) if n > 1 else None,
        'percentiles': {
            'p10': round(float(vals.quantile(0.10)), 2),
            'p25': round(float(vals.quantile(0.25)), 2),
            'p50': round(float(vals.quantile(0.50)), 2),
            'p75': round(float(vals.quantile(0.75)), 2),
            'p90': round(float(vals.quantile(0.90)), 2),
        },
        'histogram': {
            'bins':       [round(float(b), 2) for b in bin_edges],
            'counts':     [int(c) for c in counts],
            'bin_labels': bin_labels,
        }
    }


def calculate_nna_distribution_stats(nna_values: pd.Series) -> dict:
    """
    Compute histogram + percentile stats for per-relationship period NNA.

    Unlike AUA distribution (always positive, log-spaced), NNA can be negative.
    Uses symmetric log-spaced bins around zero so both inflows and outflows
    are visible.  Relationships below the materiality threshold are excluded
    (fees, dividend reinvestments, rounding -- not genuine flows).

    Returns dict matching the portal's DistributionStats TypeScript interface.
    """
    vals = nna_values.dropna()
    vals = vals[vals.abs() >= NNA_MATERIALITY_THRESHOLD]

    if vals.empty:
        return {
            'count':   0,
            'total':   0,
            'mean':    None,
            'median':  None,
            'min':     None,
            'max':     None,
            'std_dev': None,
            'percentiles': {'p10': None, 'p25': None, 'p50': None, 'p75': None, 'p90': None},
            'histogram': {'bins': [], 'counts': [], 'bin_labels': []},
        }

    n = len(vals)
    abs_max = float(vals.abs().max())
    abs_min = max(float(vals.abs().min()), 1_000)   # floor at $1K

    # Build log-spaced positive bins, then mirror for negatives
    half_bins = NUM_HISTOGRAM_BINS // 2
    pos_edges = np.logspace(np.log10(abs_min), np.log10(max(abs_max, abs_min * 2)), half_bins + 1)

    # Full bin edges: -pos_edges (reversed, excluding 0) + [0] + pos_edges
    neg_edges = -pos_edges[::-1]
    bin_edges = np.concatenate([neg_edges, [0], pos_edges])

    counts, _ = np.histogram(vals, bins=bin_edges)

    bin_labels = [
        f"{_fmt_currency(bin_edges[i])}-{_fmt_currency(bin_edges[i + 1])}"
        for i in range(len(bin_edges) - 1)
    ]

    # Split inflow/outflow percentiles ranked by absolute magnitude.
    # Outflows (negative NNA): rank by abs so P90+ = largest outflow magnitude.
    # Inflows (positive NNA): P90+ = largest inflow (natural order).
    inflows  = vals[vals > 0]
    outflows = vals[vals < 0].abs()  # positive magnitudes for ranking

    def _pctiles(s: pd.Series) -> dict:
        if s.empty:
            return {'p10': None, 'p25': None, 'p50': None, 'p75': None, 'p90': None}
        return {
            'p10': round(float(s.quantile(0.10)), 2),
            'p25': round(float(s.quantile(0.25)), 2),
            'p50': round(float(s.quantile(0.50)), 2),
            'p75': round(float(s.quantile(0.75)), 2),
            'p90': round(float(s.quantile(0.90)), 2),
        }

    return {
        'count':   n,
        'total':   round(float(vals.sum()), 2),
        'mean':    round(float(vals.mean()), 2),
        'median':  round(float(vals.median()), 2),
        'min':     round(float(vals.min()), 2),
        'max':     round(float(vals.max()), 2),
        'std_dev': round(float(vals.std()), 2) if n > 1 else None,
        'percentiles': {
            'p10': round(float(vals.quantile(0.10)), 2),
            'p25': round(float(vals.quantile(0.25)), 2),
            'p50': round(float(vals.quantile(0.50)), 2),
            'p75': round(float(vals.quantile(0.75)), 2),
            'p90': round(float(vals.quantile(0.90)), 2),
        },
        'inflow_percentiles':  _pctiles(inflows),
        'outflow_percentiles': _pctiles(outflows),
        'inflow_count':  len(inflows),
        'outflow_count': len(outflows),
        'histogram': {
            'bins':       [round(float(b), 2) for b in bin_edges],
            'counts':     [int(c) for c in counts],
            'bin_labels': bin_labels,
        }
    }


def _compute_rel_period_nna(
        cp_end: pd.DataFrame, cp_start: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute per-relationship period NNA from client_performance snapshots.

    Returns DataFrame with columns: relationship_id, period_nna
    """
    end_nna = cp_end[['relationship_id', 'nna']].copy()
    start_nna = cp_start[['relationship_id', 'nna']].rename(columns={'nna': 'nna_start'})
    merged = end_nna.merge(start_nna, on='relationship_id', how='left')
    merged['nna_start'] = merged['nna_start'].fillna(0)
    merged['period_nna'] = merged['nna'] - merged['nna_start']
    return merged[['relationship_id', 'period_nna']]


def _empty_view(title: str) -> dict:
    """Return a zeroed-out view structure for periods with no data."""
    empty_dist = calculate_distribution_stats(pd.Series([], dtype=float))
    return {
        'donut': {'title': title, 'total': 0, 'segments': []},
        'distribution': {'total': empty_dist, 'by_segment': {}},
        'metrics': {'aua': 0, 'client_count': 0}
    }


# ---------------------------------------------------------------------------
# GEO view
# ---------------------------------------------------------------------------

def build_geo_view(period_ts: pd.Timestamp,
                   geo_ts: pd.DataFrame,
                   acct_perf_day: pd.DataFrame,
                   acct_dim: pd.DataFrame) -> dict:
    """
    Build the GEO view for one period.

    State-level donut: geo_ts pre-aggregated view (fast, already summed).
    City drill-down:   join acct_perf_day + acct_dim -> group by (state, city).
    Distributions:     acct_perf_day total_aua per account, grouped by state.
    """
    # --- State-level aggregation ---
    geo_day = geo_ts[geo_ts['date'] == period_ts].copy()
    # Exclude non-US / unknown
    geo_day = geo_day[
        geo_day['state'].notna() &
        (geo_day['state'] != '') &
        (geo_day['state'] != 'Unknown')
    ]
    geo_day = geo_day.sort_values('total_aua', ascending=False)

    total_aua = float(geo_day['total_aua'].sum())

    # --- Account-level data for cities + distributions ---
    acct_geo = acct_perf_day.merge(
        acct_dim[['account_id', 'client_city', 'client_state']],
        on='account_id', how='left'
    )
    acct_geo['client_state'] = acct_geo['client_state'].fillna('Unknown').str.strip()
    acct_geo['client_city']  = acct_geo['client_city'].fillna('').str.strip()

    # --- Segments ---
    top_states   = geo_day.head(MAX_SEGMENTS)
    other_states = geo_day.iloc[MAX_SEGMENTS:]

    segments = []
    by_segment_dist = {}

    for i, (_, row) in enumerate(top_states.iterrows()):
        state = row['state']
        aua   = float(row['total_aua'])
        client_count = int(row.get('num_relationships', 0))

        state_accts = acct_geo[acct_geo['client_state'] == state]
        state_dist  = calculate_distribution_stats(state_accts['total_aua'])
        cities      = _build_cities(state_accts, state, aua)

        key = state.lower()
        segments.append({
            'key':          key,
            'label':        state,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': client_count,
            'color':        GEO_COLORS[i % len(GEO_COLORS)],
            'cities':       cities,
            'distribution': state_dist
        })
        by_segment_dist[key] = state_dist

    # Other bucket
    if not other_states.empty:
        other_aua          = float(other_states['total_aua'].sum())
        other_client_count = int(other_states['num_relationships'].sum())
        other_state_names  = other_states['state'].tolist()
        other_accts        = acct_geo[acct_geo['client_state'].isin(other_state_names)]
        other_dist         = calculate_distribution_stats(other_accts['total_aua'])

        if other_aua > 0:
            segments.append({
                'key':          'other',
                'label':        'Other States',
                'aua':          round(other_aua, 2),
                'aua_pct':      round(other_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
                'client_count': other_client_count,
                'color':        OTHER_COLOR,
                'cities':       [],
                'distribution': other_dist
            })
            by_segment_dist['other'] = other_dist

    total_dist = calculate_distribution_stats(acct_geo['total_aua'])

    return {
        'donut': {
            'title':    'AUA by State',
            'total':    round(total_aua, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'metrics': {
            'aua':          round(total_aua, 2),
            'client_count': int(geo_day['num_relationships'].sum())
        }
    }


def _build_cities(state_accts: pd.DataFrame, state: str, state_aua: float) -> list:
    """Build city drill-down list for one state."""
    if state_accts.empty:
        return []

    city_agg = (
        state_accts
        .groupby('client_city')
        .agg(aua=('total_aua', 'sum'), account_count=('account_id', 'count'))
        .reset_index()
        .sort_values('aua', ascending=False)
    )
    # Drop blank city names
    city_agg = city_agg[city_agg['client_city'].str.strip() != '']

    top_cities   = city_agg.head(MAX_CITIES)
    other_cities = city_agg.iloc[MAX_CITIES:]

    cities = []
    for i, (_, row) in enumerate(top_cities.iterrows()):
        city_name = str(row['client_city']).strip()
        aua       = float(row['aua'])
        city_accts = state_accts[state_accts['client_city'] == row['client_city']]
        city_dist  = calculate_distribution_stats(city_accts['total_aua'])

        cities.append({
            'key':          f"{city_name.lower().replace(' ', '_')}_{state.lower()}",
            'label':        city_name,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / state_aua * 100, 1) if state_aua > 0 else 0.0,
            'client_count': int(row['account_count']),
            'color':        CITY_COLORS[i % len(CITY_COLORS)],
            'distribution': city_dist
        })

    if not other_cities.empty and other_cities['aua'].sum() > 0:
        other_aua   = float(other_cities['aua'].sum())
        other_accts = state_accts[state_accts['client_city'].isin(other_cities['client_city'])]
        cities.append({
            'key':          f"other_{state.lower()}",
            'label':        f"Other {state} Cities",
            'aua':          round(other_aua, 2),
            'aua_pct':      round(other_aua / state_aua * 100, 1) if state_aua > 0 else 0.0,
            'client_count': int(other_cities['account_count'].sum()),
            'color':        OTHER_COLOR,
            'distribution': calculate_distribution_stats(other_accts['total_aua'])
        })

    return cities


# ---------------------------------------------------------------------------
# ADV view
# ---------------------------------------------------------------------------

def build_adv_view(period_ts: pd.Timestamp,
                   adv_ts: pd.DataFrame,
                   client_perf_day: pd.DataFrame,
                   acct_perf_day: pd.DataFrame,
                   acct_dim: pd.DataFrame,
                   client_dim: pd.DataFrame,
                   rel_arch_lookup: pd.Series) -> dict:
    """
    Build the ADV view for one period.

    Advisor-level donut:  adv_ts pre-aggregated view.
    Nested clients:       client_perf_day filtered to advisor, top N by AUA.
    Distributions:        acct_perf_day total_aua per account, grouped by advisor.
    """
    adv_day = adv_ts[adv_ts['date'] == period_ts].copy()
    adv_day = adv_day[adv_day['architect'].notna()]
    adv_day = adv_day.sort_values('total_aua', ascending=False)

    total_aua = float(adv_day['total_aua'].sum())

    # Client-level data: add architect assignment + display name
    client_day = client_perf_day.copy()
    client_day['architect'] = client_day['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

    if 'relationship_name' in client_dim.columns:
        name_map = client_dim.set_index('relationship_id')['relationship_name']
        client_day['relationship_name'] = (
            client_day['relationship_id'].map(name_map)
            .fillna(client_day['relationship_id'].astype(str))
        )
    else:
        client_day['relationship_name'] = client_day['relationship_id'].astype(str)

    # Account-level data: add architect
    acct_arch = acct_perf_day.copy()
    acct_arch['architect'] = acct_arch['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

    top_advisors   = adv_day.head(MAX_SEGMENTS)
    other_advisors = adv_day.iloc[MAX_SEGMENTS:]

    segments = []
    by_segment_dist = {}

    for i, (_, row) in enumerate(top_advisors.iterrows()):
        arch         = row['architect']
        aua          = float(row['total_aua'])
        client_count = int(row.get('num_relationships', 0))

        arch_clients = client_day[client_day['architect'] == arch]
        arch_accts   = acct_arch[acct_arch['architect'] == arch]

        adv_dist       = calculate_distribution_stats(arch_accts['total_aua'])
        arch_color     = ADV_COLORS[i % len(ADV_COLORS)]
        nested_clients = _build_clients(arch_clients, arch_accts, arch_aua=aua, arch_color=arch_color)

        key = arch.lower().replace(' ', '_').replace('-', '_')
        segments.append({
            'key':          key,
            'label':        arch,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': client_count,
            'color':        arch_color,
            'clients':      nested_clients,
            'distribution': adv_dist
        })
        by_segment_dist[key] = adv_dist

    if not other_advisors.empty:
        other_aua         = float(other_advisors['total_aua'].sum())
        other_arch_names  = other_advisors['architect'].tolist()
        other_clients_df  = client_day[client_day['architect'].isin(other_arch_names)]
        other_accts       = acct_arch[acct_arch['architect'].isin(other_arch_names)]
        other_dist        = calculate_distribution_stats(other_accts['total_aua'])

        if other_aua > 0:
            other_nested = _build_clients(other_clients_df, other_accts, arch_aua=other_aua, arch_color=OTHER_COLOR)
            segments.append({
                'key':          'other',
                'label':        'Other Architects',
                'aua':          round(other_aua, 2),
                'aua_pct':      round(other_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
                'client_count': int(other_advisors['num_relationships'].sum()),
                'color':        OTHER_COLOR,
                'clients':      other_nested,
                'distribution': other_dist
            })
            by_segment_dist['other'] = other_dist

    total_dist = calculate_distribution_stats(acct_arch['total_aua'])

    return {
        'donut': {
            'title':    'AUA by Architect',
            'total':    round(total_aua, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'metrics': {
            'aua':          round(total_aua, 2),
            'client_count': int(adv_day['num_relationships'].sum())
        }
    }


def _build_clients(arch_clients: pd.DataFrame,
                   arch_accts: pd.DataFrame,
                   arch_aua: float,
                   arch_color: str) -> list:
    """Build nested clients list for an advisor segment.

    Each client (relationship) gets an account-level distribution so the
    frontend can drill: Architect -> Relationship -> Account distribution.
    Mirrors the GEO pattern: State -> City -> account distribution.
    """
    if arch_clients.empty:
        return []

    top_clients = arch_clients.sort_values('total_aua', ascending=False).head(MAX_CLIENTS_PER_ADVISOR)

    clients = []
    for _, row in top_clients.iterrows():
        rel_id = row['relationship_id']
        aua    = float(row['total_aua'])
        name   = str(row.get('relationship_name', rel_id))

        # Account-level distribution for this relationship
        rel_accts = arch_accts[arch_accts['relationship_id'] == rel_id]
        rel_dist  = calculate_distribution_stats(rel_accts['total_aua'])

        clients.append({
            'key':          str(rel_id),
            'label':        name,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / arch_aua * 100, 1) if arch_aua > 0 else 0.0,
            'account_count': int(len(rel_accts)),
            'color':        arch_color,
            'distribution': rel_dist
        })

    return clients


# ---------------------------------------------------------------------------
# AUA view (tax status donut)
# ---------------------------------------------------------------------------

AUA_TAX_COLORS = {
    'taxable':      '#EF4444',   # Red — Non-Qualified
    'tax_deferred': '#F59E0B',   # Amber — Tax-Deferred
    'tax_free':     '#10B981',   # Green — Tax-Free (Roth)
}


def _build_aua_tax_view(cp_day: pd.DataFrame, client_dim: pd.DataFrame) -> dict:
    """
    Build AUA-by-tax-status donut for one period.

    Segments: Non-Qualified, Tax-Deferred, Tax-Free (Roth).
    Uses aua_taxable / aua_tax_deferred / aua_tax_exempt from client_performance.
    Client counts from client_dimension has_taxable / has_tax_deferred / has_tax_exempt.
    """
    total_aua    = float(cp_day['total_aua'].sum())
    aua_taxable  = float(cp_day['aua_taxable'].sum())  if 'aua_taxable'      in cp_day.columns else 0.0
    aua_deferred = float(cp_day['aua_tax_deferred'].sum()) if 'aua_tax_deferred' in cp_day.columns else 0.0
    aua_exempt   = float(cp_day['aua_tax_exempt'].sum())   if 'aua_tax_exempt'   in cp_day.columns else 0.0

    n_taxable  = int(client_dim['has_taxable'].sum())      if 'has_taxable'      in client_dim.columns else 0
    n_deferred = int(client_dim['has_tax_deferred'].sum())  if 'has_tax_deferred' in client_dim.columns else 0
    n_exempt   = int(client_dim['has_tax_exempt'].sum())    if 'has_tax_exempt'   in client_dim.columns else 0

    def _seg(key, label, aua, count, color):
        return {
            'key':          key,
            'label':        label,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': count,
            'color':        color,
        }

    segments = [
        _seg('taxable',      'Non-Qualified',   aua_taxable,  n_taxable,  AUA_TAX_COLORS['taxable']),
        _seg('tax_deferred', 'Tax-Deferred',    aua_deferred, n_deferred, AUA_TAX_COLORS['tax_deferred']),
        _seg('tax_free',     'Tax-Free (Roth)', aua_exempt,   n_exempt,   AUA_TAX_COLORS['tax_free']),
    ]

    total_clients = int(client_dim['relationship_id'].nunique()) if 'relationship_id' in client_dim.columns else 0

    return {
        'donut': {
            'title':    'AUA by Tax Status',
            'total':    round(total_aua, 2),
            'segments': segments
        },
        'distribution': {
            'total':      calculate_distribution_stats(pd.Series([], dtype=float)),
            'by_segment': {}
        },
        'metrics': {
            'aua':          round(total_aua, 2),
            'client_count': total_clients
        }
    }


# ---------------------------------------------------------------------------
# NNA views (period-differenced, blue/red by sign)
# ---------------------------------------------------------------------------

def _assign_nna_colors(segments: list) -> list:
    """
    Assign blue shades to positive-NNA segments and red shades to negative-NNA
    segments, rank-ordered by absolute magnitude within each group.
    """
    pos = [(i, s) for i, s in enumerate(segments) if s.get('_nna', 0) >= 0]
    neg = [(i, s) for i, s in enumerate(segments) if s.get('_nna', 0) < 0]

    # Sort each group by absolute NNA descending (darkest = largest magnitude)
    pos.sort(key=lambda x: abs(x[1].get('_nna', 0)), reverse=True)
    neg.sort(key=lambda x: abs(x[1].get('_nna', 0)), reverse=True)

    for rank, (idx, _) in enumerate(pos):
        segments[idx]['color'] = NNA_BLUE_SHADES[rank % len(NNA_BLUE_SHADES)]
    for rank, (idx, _) in enumerate(neg):
        segments[idx]['color'] = NNA_RED_SHADES[rank % len(NNA_RED_SHADES)]

    # Strip the internal _nna key
    for s in segments:
        s.pop('_nna', None)

    return segments


def build_nna_geo_view(end_ts: pd.Timestamp,
                       start_ts: pd.Timestamp,
                       geo_ts: pd.DataFrame,
                       cp_end: pd.DataFrame = None,
                       cp_start: pd.DataFrame = None,
                       rel_geo_lookup: pd.Series = None,
                       rel_city_lookup: pd.Series = None) -> dict:
    """
    Build NNA-mode GEO view: period-differenced NNA by state.

    Donut slices sized by abs(period_nna), colored blue (growth) / red (attrition).
    Distribution: per-relationship period NNA histogram (signed, symmetric log bins).
    """
    geo_end   = geo_ts[geo_ts['date'] == end_ts].copy()
    geo_start = geo_ts[geo_ts['date'] == start_ts]

    # Exclude non-US and blank states; keep 'Unknown' as a named segment
    geo_end = geo_end[
        geo_end['state'].notna() & (geo_end['state'] != '')
    ].copy()

    if geo_end.empty:
        return _empty_nna_view('NNA by State')

    # Merge start-of-period cumulative values to compute period flows
    start_cols = geo_start[['state', 'country', 'nna', 'cum_inflows', 'cum_outflows']].copy()
    start_cols = start_cols.rename(columns={
        'nna': 'nna_start', 'cum_inflows': 'inflows_start', 'cum_outflows': 'outflows_start'
    })
    merged = geo_end.merge(start_cols, on=['state', 'country'], how='left')
    merged['nna_start']     = merged['nna_start'].fillna(0)
    merged['inflows_start'] = merged['inflows_start'].fillna(0)
    merged['outflows_start'] = merged['outflows_start'].fillna(0)

    merged['period_nna']      = merged['nna']          - merged['nna_start']
    merged['period_inflows']  = merged['cum_inflows']  - merged['inflows_start']
    merged['period_outflows'] = merged['cum_outflows'] - merged['outflows_start']

    # Sort by absolute period NNA (biggest movers first)
    merged = merged.reindex(merged['period_nna'].abs().sort_values(ascending=False).index)

    total_abs_nna = float(merged['period_nna'].abs().sum())
    total_net_nna = float(merged['period_nna'].sum())

    top     = merged.head(MAX_SEGMENTS)
    others  = merged.iloc[MAX_SEGMENTS:]

    segments = []
    for _, row in top.iterrows():
        nna_val = float(row['period_nna'])
        segments.append({
            'key':             row['state'].lower(),
            'label':           row['state'],
            'aua':             round(abs(nna_val), 2),          # abs for donut slice sizing
            'aua_pct':         round(abs(nna_val) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
            'value':           round(nna_val, 2),               # signed NNA for display
            'client_count':    int(row.get('num_relationships', 0)),
            'period_inflows':  round(float(row['period_inflows']), 2),
            'period_outflows': round(float(row['period_outflows']), 2),
            'color':           '',                              # assigned below
            '_nna':            nna_val,                         # temp for color assignment
        })

    if not others.empty:
        other_nna      = float(others['period_nna'].sum())
        other_inflows  = float(others['period_inflows'].sum())
        other_outflows = float(others['period_outflows'].sum())
        other_count    = int(others['num_relationships'].sum())
        if abs(other_nna) > 0:
            segments.append({
                'key':             'other',
                'label':           'Other States',
                'aua':             round(abs(other_nna), 2),
                'aua_pct':         round(abs(other_nna) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
                'value':           round(other_nna, 2),
                'client_count':    other_count,
                'period_inflows':  round(other_inflows, 2),
                'period_outflows': round(other_outflows, 2),
                'color':           OTHER_COLOR,
                '_nna':            other_nna,
            })

    segments = _assign_nna_colors(segments)

    # --- Per-relationship NNA distribution ---
    empty_nna_dist = calculate_nna_distribution_stats(pd.Series([], dtype=float))
    total_dist = empty_nna_dist
    by_segment_dist = {}

    if cp_end is not None and cp_start is not None and rel_geo_lookup is not None:
        rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        rel_nna['state'] = rel_nna['relationship_id'].map(rel_geo_lookup).fillna('Unknown')

        # Filter to US with non-blank state; keep 'Unknown' matching geo_end treatment
        rel_nna = rel_nna[
            rel_nna['state'].notna() &
            (rel_nna['state'] != '')
        ]

        total_dist = calculate_nna_distribution_stats(rel_nna['period_nna'])

        # Top segment keys (state lowercase)
        seg_keys = {s['key']: s['label'] for s in segments if s['key'] != 'other'}
        for key, label in seg_keys.items():
            state_nna = rel_nna[rel_nna['state'].str.lower() == key]['period_nna']
            by_segment_dist[key] = calculate_nna_distribution_stats(state_nna)

    # --- Y6b: Per-state city-level NNA distribution drill-down ---
    geo_drill_dist = {}
    if (cp_end is not None and cp_start is not None
            and rel_geo_lookup is not None and rel_city_lookup is not None):
        # rel_nna already computed above; add city
        if 'period_nna' not in rel_nna.columns:
            rel_nna = _compute_rel_period_nna(cp_end, cp_start)
            rel_nna['state'] = rel_nna['relationship_id'].map(rel_geo_lookup).fillna('Unknown')
        rel_nna['city'] = rel_nna['relationship_id'].map(rel_city_lookup).fillna('Unknown')

        seg_keys = {s['key']: s['label'] for s in segments if s['key'] != 'other'}
        for key, label in seg_keys.items():
            state_rels = rel_nna[rel_nna['state'].str.lower() == key]
            if state_rels.empty:
                continue
            # Per-city distributions within this state
            city_dists = {}
            for city_name, city_group in state_rels.groupby('city'):
                if city_name == 'Unknown' or len(city_group) < 2:
                    continue
                city_key = city_name.lower().replace(' ', '_').replace('-', '_')
                city_dists[city_key] = calculate_nna_distribution_stats(city_group['period_nna'])
            if city_dists:
                geo_drill_dist[key] = {
                    'total': by_segment_dist.get(key, empty_nna_dist),
                    'by_city': city_dists,
                }

    return {
        'donut': {
            'title':    'NNA by State',
            'total':    round(total_net_nna, 2),
            'total_abs': round(total_abs_nna, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'drill': geo_drill_dist,
        'metrics': {
            'nna':          round(total_net_nna, 2),
            'client_count': int(merged['num_relationships'].sum())
        }
    }


def build_nna_adv_view(end_ts: pd.Timestamp,
                       start_ts: pd.Timestamp,
                       adv_ts: pd.DataFrame,
                       cp_end: pd.DataFrame = None,
                       cp_start: pd.DataFrame = None,
                       rel_arch_lookup: pd.Series = None,
                       client_dim: pd.DataFrame = None) -> dict:
    """
    Build NNA-mode ADV view: period-differenced NNA by architect.

    Same pattern as NNA GEO but keyed on architect instead of state.
    Distribution: per-relationship period NNA histogram (signed, symmetric log bins).
    """
    adv_end   = adv_ts[adv_ts['date'] == end_ts].copy()
    adv_start = adv_ts[adv_ts['date'] == start_ts]

    adv_end = adv_end[adv_end['architect'].notna()]

    if adv_end.empty:
        return _empty_nna_view('NNA by Architect')

    start_cols = adv_start[['architect', 'nna', 'cum_inflows', 'cum_outflows']].copy()
    start_cols = start_cols.rename(columns={
        'nna': 'nna_start', 'cum_inflows': 'inflows_start', 'cum_outflows': 'outflows_start'
    })
    merged = adv_end.merge(start_cols, on='architect', how='left')
    merged['nna_start']      = merged['nna_start'].fillna(0)
    merged['inflows_start']  = merged['inflows_start'].fillna(0)
    merged['outflows_start'] = merged['outflows_start'].fillna(0)

    merged['period_nna']      = merged['nna']          - merged['nna_start']
    merged['period_inflows']  = merged['cum_inflows']  - merged['inflows_start']
    merged['period_outflows'] = merged['cum_outflows'] - merged['outflows_start']

    merged = merged.reindex(merged['period_nna'].abs().sort_values(ascending=False).index)

    total_abs_nna = float(merged['period_nna'].abs().sum())
    total_net_nna = float(merged['period_nna'].sum())

    top    = merged.head(MAX_SEGMENTS)
    others = merged.iloc[MAX_SEGMENTS:]

    segments = []
    for _, row in top.iterrows():
        arch    = row['architect']
        nna_val = float(row['period_nna'])
        segments.append({
            'key':             arch.lower().replace(' ', '_').replace('-', '_'),
            'label':           arch,
            'aua':             round(abs(nna_val), 2),
            'aua_pct':         round(abs(nna_val) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
            'value':           round(nna_val, 2),
            'client_count':    int(row.get('num_relationships', 0)),
            'period_inflows':  round(float(row['period_inflows']), 2),
            'period_outflows': round(float(row['period_outflows']), 2),
            'color':           '',
            '_nna':            nna_val,
        })

    if not others.empty:
        other_nna      = float(others['period_nna'].sum())
        other_inflows  = float(others['period_inflows'].sum())
        other_outflows = float(others['period_outflows'].sum())
        other_count    = int(others['num_relationships'].sum())
        if abs(other_nna) > 0:
            segments.append({
                'key':             'other',
                'label':           'Other Architects',
                'aua':             round(abs(other_nna), 2),
                'aua_pct':         round(abs(other_nna) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
                'value':           round(other_nna, 2),
                'client_count':    other_count,
                'period_inflows':  round(other_inflows, 2),
                'period_outflows': round(other_outflows, 2),
                'color':           OTHER_COLOR,
                '_nna':            other_nna,
            })

    segments = _assign_nna_colors(segments)

    # --- Per-relationship NNA distribution ---
    empty_nna_dist = calculate_nna_distribution_stats(pd.Series([], dtype=float))
    total_dist = empty_nna_dist
    by_segment_dist = {}

    if cp_end is not None and cp_start is not None and rel_arch_lookup is not None:
        rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        rel_nna['architect'] = rel_nna['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

        total_dist = calculate_nna_distribution_stats(rel_nna['period_nna'])

        # Top segment keys (architect name -> key)
        seg_keys = {s['key']: s['label'] for s in segments if s['key'] != 'other'}
        for key, label in seg_keys.items():
            arch_nna = rel_nna[
                rel_nna['architect'].str.lower().str.replace(' ', '_').str.replace('-', '_') == key
            ]['period_nna']
            by_segment_dist[key] = calculate_nna_distribution_stats(arch_nna)

    # --- Y6d: Per-architect relationship-level NNA distribution drill-down ---
    adv_drill_dist = {}
    if cp_end is not None and cp_start is not None and rel_arch_lookup is not None:
        # rel_nna already computed above
        # Add relationship names for labeling
        name_map = None
        if client_dim is not None and 'relationship_name' in client_dim.columns:
            name_map = client_dim.set_index('relationship_id')['relationship_name']

        for key, label in seg_keys.items():
            arch_rels = rel_nna[
                rel_nna['architect'].str.lower().str.replace(' ', '_').str.replace('-', '_') == key
            ]
            if len(arch_rels) < 2:
                continue
            # Compute the distribution for all relationships under this architect
            arch_dist = calculate_nna_distribution_stats(arch_rels['period_nna'])
            adv_drill_dist[key] = {
                'distribution': arch_dist,
                'relationship_count': len(arch_rels),
            }

    return {
        'donut': {
            'title':    'NNA by Architect',
            'total':    round(total_net_nna, 2),
            'total_abs': round(total_abs_nna, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'drill': adv_drill_dist,
        'metrics': {
            'nna':          round(total_net_nna, 2),
            'client_count': int(merged['num_relationships'].sum())
        }
    }


def _empty_nna_view(title: str) -> dict:
    """Return a zeroed-out NNA view structure."""
    empty_dist = calculate_distribution_stats(pd.Series([], dtype=float))
    return {
        'donut': {'title': title, 'total': 0, 'total_abs': 0, 'segments': []},
        'distribution': {'total': empty_dist, 'by_segment': {}},
        'metrics': {'nna': 0, 'client_count': 0}
    }


# ---------------------------------------------------------------------------
# CLA views (NMNC/NMEC lifecycle decomposition per GEO/ADV segment)
# ---------------------------------------------------------------------------

def build_cla_view(end_ts: pd.Timestamp,
                   start_ts: pd.Timestamp,
                   client_perf: pd.DataFrame,
                   client_dim: pd.DataFrame,
                   rel_geo_lookup: pd.Series,
                   rel_arch_lookup: pd.Series,
                   verbose: bool = False) -> dict:
    """
    Build CLA view for one period: NMNC/NMEC decomposition within GEO and ADV segments.

    For each relationship:
      1. Compute period NNA = nna(end) - nna(start)
      2. Classify as NMNC (first_seen_date > start) or NMEC (first_seen_date <= start)
      3. Aggregate by (segment, lifecycle_bucket)

    Output is keyed by cohort ('geo', 'adv'), each containing a list of segments
    with nested nmnc/nmec objects. This powers the diverging stacked bar chart.
    """
    cp_end   = client_perf[client_perf['date'] == end_ts].copy()
    cp_start = client_perf[client_perf['date'] == start_ts][['relationship_id', 'nna', 'cum_inflows', 'cum_outflows']]

    if cp_end.empty:
        return _empty_cla_view()

    # Merge start-of-period values
    cp_start = cp_start.rename(columns={
        'nna': 'nna_start', 'cum_inflows': 'inflows_start', 'cum_outflows': 'outflows_start'
    })
    merged = cp_end.merge(cp_start, on='relationship_id', how='left')
    merged['nna_start']      = merged['nna_start'].fillna(0)
    merged['inflows_start']  = merged['inflows_start'].fillna(0)
    merged['outflows_start'] = merged['outflows_start'].fillna(0)

    merged['period_nna']      = merged['nna']          - merged['nna_start']
    merged['period_inflows']  = merged['cum_inflows']  - merged['inflows_start']
    merged['period_outflows'] = merged['cum_outflows'] - merged['outflows_start']

    # Join first_seen_date for lifecycle classification
    if 'first_seen_date' in client_dim.columns:
        fsd_map = client_dim.set_index('relationship_id')['first_seen_date']
        merged['first_seen_date'] = merged['relationship_id'].map(fsd_map)
        merged['first_seen_date'] = pd.to_datetime(merged['first_seen_date'])
    else:
        merged['first_seen_date'] = pd.NaT

    # NMNC = first appeared AFTER start of this period; NMEC = existed before
    merged['lifecycle'] = np.where(
        merged['first_seen_date'].notna() & (merged['first_seen_date'] > start_ts),
        'nmnc', 'nmec'
    )

    # Attach segment assignments
    merged['state']     = merged['relationship_id'].map(rel_geo_lookup).fillna('Unknown')
    merged['architect'] = merged['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

    if verbose:
        n_nmnc = (merged['lifecycle'] == 'nmnc').sum()
        n_nmec = (merged['lifecycle'] == 'nmec').sum()
        nmnc_nna = merged.loc[merged['lifecycle'] == 'nmnc', 'period_nna'].sum()
        nmec_nna = merged.loc[merged['lifecycle'] == 'nmec', 'period_nna'].sum()
        print(f"  CLA: {n_nmnc} NMNC rels (${nmnc_nna:,.0f} NNA), "
              f"{n_nmec} NMEC rels (${nmec_nna:,.0f} NNA)")

    geo_segments = _build_cla_segments(merged, 'state', 'Unknown')
    adv_segments = _build_cla_segments(merged, 'architect', 'Unassigned')

    firm_totals = _build_cla_totals(merged)

    return {
        'geo': {
            'segments': geo_segments,
            'totals':   firm_totals,
        },
        'adv': {
            'segments': adv_segments,
            'totals':   firm_totals,
        }
    }


def _build_cla_segments(df: pd.DataFrame, group_col: str, exclude_val: str) -> list:
    """
    Aggregate NMNC/NMEC lifecycle stats per segment (state or architect).

    Returns a list of segments sorted by absolute total NNA, each containing
    nested nmnc and nmec objects with flows and counts.
    """
    # Filter out unknown/unassigned
    filtered = df[df[group_col] != exclude_val].copy()

    # Aggregate per (segment, lifecycle)
    agg = (
        filtered
        .groupby([group_col, 'lifecycle'])
        .agg(
            nna=('period_nna', 'sum'),
            inflows=('period_inflows', 'sum'),
            outflows=('period_outflows', 'sum'),
            count=('relationship_id', 'nunique'),
        )
        .reset_index()
    )

    # Pivot to one row per segment
    seg_totals = (
        filtered.groupby(group_col)
        .agg(nna_total=('period_nna', 'sum'), rel_count=('relationship_id', 'nunique'))
        .reset_index()
        .sort_values('nna_total', key=lambda s: s.abs(), ascending=False)
    )

    top_segs   = seg_totals.head(MAX_SEGMENTS)
    other_segs = seg_totals.iloc[MAX_SEGMENTS:]

    segments = []
    for _, row in top_segs.iterrows():
        seg_name  = row[group_col]
        seg_key   = seg_name.lower().replace(' ', '_').replace('-', '_')
        nna_total = float(row['nna_total'])

        nmnc_data = agg[(agg[group_col] == seg_name) & (agg['lifecycle'] == 'nmnc')]
        nmec_data = agg[(agg[group_col] == seg_name) & (agg['lifecycle'] == 'nmec')]

        nmnc = _lifecycle_bucket(nmnc_data)
        nmec = _lifecycle_bucket(nmec_data)

        segments.append({
            'key':       seg_key,
            'label':     seg_name,
            'nna_total': round(nna_total, 2),
            'nmnc':      nmnc,
            'nmec':      nmec,
        })

    # Other bucket
    if not other_segs.empty:
        other_names = other_segs[group_col].tolist()
        other_agg   = agg[agg[group_col].isin(other_names)]

        other_nmnc_data = other_agg[other_agg['lifecycle'] == 'nmnc']
        other_nmec_data = other_agg[other_agg['lifecycle'] == 'nmec']

        other_nna = float(other_segs['nna_total'].sum())
        if abs(other_nna) > 0:
            segments.append({
                'key':       'other',
                'label':     'Other',
                'nna_total': round(other_nna, 2),
                'nmnc':      _lifecycle_bucket(other_nmnc_data),
                'nmec':      _lifecycle_bucket(other_nmec_data),
            })

    return segments


def _lifecycle_bucket(data: pd.DataFrame) -> dict:
    """Summarize one lifecycle bucket (NMNC or NMEC) from aggregated rows."""
    if data.empty:
        return {'nna': 0, 'inflows': 0, 'outflows': 0, 'count': 0}
    return {
        'nna':      round(float(data['nna'].sum()), 2),
        'inflows':  round(float(data['inflows'].sum()), 2),
        'outflows': round(float(data['outflows'].sum()), 2),
        'count':    int(data['count'].sum()),
    }


def _build_cla_totals(df: pd.DataFrame) -> dict:
    """Compute firm-wide CLA totals."""
    nmnc = df[df['lifecycle'] == 'nmnc']
    nmec = df[df['lifecycle'] == 'nmec']
    return {
        'nna':        round(float(df['period_nna'].sum()), 2),
        'nmnc_nna':   round(float(nmnc['period_nna'].sum()), 2),
        'nmec_nna':   round(float(nmec['period_nna'].sum()), 2),
        'nmnc_count': int(nmnc['relationship_id'].nunique()),
        'nmec_count': int(nmec['relationship_id'].nunique()),
    }


def _empty_cla_view() -> dict:
    """Return a zeroed-out CLA view structure."""
    empty = {
        'segments': [],
        'totals': {'nna': 0, 'nmnc_nna': 0, 'nmec_nna': 0, 'nmnc_count': 0, 'nmec_count': 0}
    }
    return {'geo': empty, 'adv': empty}


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def generate_header_metrics(verbose: bool = False, granularity: str = 'quarterly') -> dict:
    """
    Load all gold tables, compute 4-period views (AUA, NNA, GEO, ADV, CLA),
    return JSON-ready dict.

    granularity: 'quarterly' (default), 'monthly', or 'annual'
    NMNC/NMEC classification applies boundaries appropriate to each granularity.
    """
    print("Loading gold tables from S3...")
    client_perf, acct_perf, acct_dim, client_dim, geo_ts, adv_ts, rel_arch_lookup = load_data(verbose=verbose)

    ref_date = client_perf['date'].max()
    periods  = get_periods(ref_date, granularity=granularity)
    period_pairs = get_period_pairs(periods, granularity=granularity)

    data_as_of   = ref_date.strftime('%Y-%m-%d')

    # Collect all dates we need: 4 period ends + up to 4 period starts
    all_dates = set()
    for pp in period_pairs.values():
        all_dates.add(pp['end'])
        all_dates.add(pp['start'])
    target_dates = sorted(all_dates)

    print(f"Reference date: {data_as_of}")
    if verbose:
        for key, p in periods.items():
            pp = period_pairs[key]
            print(f"  {key}: {p['date']} ({p['label']}) | "
                  f"period start: {pp['start'].strftime('%Y-%m-%d')}")

    # Pre-filter to target dates (memory optimization)
    client_perf_filtered = client_perf[client_perf['date'].isin(target_dates)]
    acct_perf_filtered   = acct_perf[acct_perf['date'].isin(target_dates)]

    # account_performance may lag client_performance (05b excluded from incremental runs).
    # Build a fallback map: for each target date missing from acct_perf, use the closest
    # prior date that IS available. This keeps cities/distributions populated even when
    # account_performance hasn't been rebuilt yet.
    acct_dates_available = set(acct_perf['date'].unique())
    _acct_date_fallback = {}
    for td in target_dates:
        if td in acct_dates_available:
            _acct_date_fallback[td] = td
        else:
            # Find closest prior date in account_performance
            prior = acct_perf['date'][acct_perf['date'] <= td].max()
            if pd.notna(prior):
                _acct_date_fallback[td] = prior
                print(f"  NOTE: account_performance missing {td.date()} -- "
                      f"falling back to {prior.date()} for cities/distributions")
            else:
                _acct_date_fallback[td] = None

    # Extend acct_perf_filtered to include fallback dates
    all_acct_dates = set(target_dates) | {v for v in _acct_date_fallback.values() if v is not None}
    acct_perf_filtered = acct_perf[acct_perf['date'].isin(all_acct_dates)]

    # Build relationship -> state/city lookups for CLA-GEO and Y6b drill-down
    rel_geo_lookup = _build_rel_geo_lookup(acct_dim)
    rel_city_lookup = _build_rel_city_lookup(acct_dim)

    views = {'aua': {}, 'nna': {}, 'geo': {}, 'adv': {}, 'cla': {}}

    for period_key, period_info in periods.items():
        ts       = period_info['_ts']
        start_ts = period_pairs[period_key]['start']
        print(f"Building views for {period_key} ({period_info['date']})...")

        cp_day = client_perf_filtered[client_perf_filtered['date'] == ts]
        ap_date = _acct_date_fallback.get(ts, ts)
        ap_day = acct_perf_filtered[acct_perf_filtered['date'] == ap_date] if ap_date is not None else pd.DataFrame()

        if cp_day.empty:
            print(f"  WARN: No client_performance data for {period_info['date']} -- skipping period")
            views['aua'][period_key] = _empty_view('AUA by Tax Status')
            views['nna'][period_key] = _empty_nna_view('NNA by State')
            views['geo'][period_key] = _empty_view('AUA by State')
            views['adv'][period_key] = _empty_view('AUA by Architect')
            views['cla'][period_key] = _empty_cla_view()
            continue

        # --- AUA view: tax status donut (unchanged) ---
        views['aua'][period_key] = _build_aua_tax_view(cp_day, client_dim)

        # --- GEO view: AUA by State (unchanged) ---
        views['geo'][period_key] = build_geo_view(ts, geo_ts, ap_day, acct_dim)

        # --- ADV view: AUA by Architect (unchanged) ---
        views['adv'][period_key] = build_adv_view(
            ts, adv_ts, cp_day, ap_day, acct_dim, client_dim, rel_arch_lookup
        )

        # --- NNA view: period-differenced NNA by GEO + ADV (blue/red donuts) ---
        cp_start = client_perf_filtered[client_perf_filtered['date'] == start_ts]
        nna_geo = build_nna_geo_view(ts, start_ts, geo_ts,
                                      cp_end=cp_day, cp_start=cp_start,
                                      rel_geo_lookup=rel_geo_lookup,
                                      rel_city_lookup=rel_city_lookup)
        nna_adv = build_nna_adv_view(ts, start_ts, adv_ts,
                                      cp_end=cp_day, cp_start=cp_start,
                                      rel_arch_lookup=rel_arch_lookup,
                                      client_dim=client_dim)
        views['nna'][period_key] = {
            'geo': nna_geo,
            'adv': nna_adv,
        }

        # --- CLA view: NMNC/NMEC lifecycle decomposition (stacked bars) ---
        views['cla'][period_key] = build_cla_view(
            ts, start_ts, client_perf_filtered, client_dim,
            rel_geo_lookup, rel_arch_lookup, verbose=verbose
        )

        if verbose:
            aua_total = views['aua'][period_key]['donut']['total']
            geo_segs  = len(views['geo'][period_key]['donut']['segments'])
            adv_segs  = len(views['adv'][period_key]['donut']['segments'])
            geo_aua   = views['geo'][period_key]['donut']['total']
            adv_aua   = views['adv'][period_key]['donut']['total']
            nna_net   = nna_geo['metrics']['nna']
            cla_nmnc  = views['cla'][period_key]['geo']['totals']['nmnc_nna']
            cla_nmec  = views['cla'][period_key]['geo']['totals']['nmec_nna']
            print(f"  AUA: total ${aua_total:,.0f}")
            print(f"  GEO: {geo_segs} segments, total AUA ${geo_aua:,.0f}")
            print(f"  ADV: {adv_segs} segments, total AUA ${adv_aua:,.0f}")
            print(f"  NNA: net ${nna_net:,.0f} (GEO view)")
            print(f"  CLA: NMNC ${cla_nmnc:,.0f} | NMEC ${cla_nmec:,.0f}")

    # Strip internal _ts key from periods before output
    periods_out = {k: {'date': v['date'], 'label': v['label']} for k, v in periods.items()}

    return {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_as_of':   data_as_of,
        'firm_id':      '49financial',
        'firm_name':    '49 Financial',
        'granularity':  granularity,
        'periods':      periods_out,
        'views':        views
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


def write_s3(payload: dict, granularity: str = 'quarterly') -> None:
    """Write payload to S3 with granularity-specific path."""
    body = json.dumps(payload, separators=(',', ':'), default=str).encode('utf-8')
    s3 = boto3.client('s3', region_name='us-east-1')
    # Use granularity in path: header_metrics_quarterly.json, header_metrics_monthly.json, etc.
    key = f'gold/partner_analytics/header_metrics_{granularity}.json'
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=body,
        ContentType='application/json',
        CacheControl='public, max-age=300, s-maxage=3600'
    )
    print(f"OK: Uploaded to s3://{S3_BUCKET}/{key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate partner_analytics/header_metrics.json from gold tables'
    )
    parser.add_argument(
        '--upload', action='store_true',
        help='Upload outputs to S3 (generates quarterly, monthly, annual variants)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Compute and validate output but do not write anywhere'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help=f'Local output path (default: {DEFAULT_LOCAL_OUTPUT}). Will add _GRANULARITY suffix.'
    )
    parser.add_argument(
        '--granularity', type=str, choices=['quarterly', 'monthly', 'annual'], default=None,
        help='Generate only specific granularity (default: all three)'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose logging'
    )
    args = parser.parse_args()

    print('============================================================')
    print('09_generate_partner_analytics.py (Multi-Granularity)')
    print(f'Started: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('============================================================')

    # Determine which granularities to generate
    granularities = [args.granularity] if args.granularity else ['quarterly', 'monthly', 'annual']

    for granularity in granularities:
        print(f"\nGenerating {granularity} variant...")
        payload = generate_header_metrics(verbose=args.verbose, granularity=granularity)

        # Validate: check that current period has non-zero AUA and NNA data
        current_geo_aua = payload['views']['geo']['current']['donut']['total']
        current_adv_aua = payload['views']['adv']['current']['donut']['total']
        current_nna_net = payload['views']['nna']['current']['geo']['metrics']['nna']
        current_cla     = payload['views']['cla']['current']['geo']['totals']
        print(f"  Validation: GEO AUA=${current_geo_aua:,.0f}, ADV AUA=${current_adv_aua:,.0f}")
        print(f"    NNA net=${current_nna_net:,.0f}")
        print(f"    CLA: NMNC=${current_cla['nmnc_nna']:,.0f} ({current_cla['nmnc_count']} rels) | "
              f"NMEC=${current_cla['nmec_nna']:,.0f} ({current_cla['nmec_count']} rels)")

        if current_geo_aua == 0:
            print("    WARN: GEO current period AUA is zero -- check nna_aua_by_geography.parquet")
        if current_adv_aua == 0:
            print("    WARN: ADV current period AUA is zero -- check nna_aua_by_advisor.parquet")

        if args.dry_run:
            print(f"  OK: Dry run for {granularity} -- no output written")
            period_keys = list(payload['periods'].keys())
            for period_key in period_keys:
                g_total = payload['views']['geo'][period_key]['donut']['total']
                a_total = payload['views']['adv'][period_key]['donut']['total']
                n_net   = payload['views']['nna'][period_key]['geo']['metrics']['nna']
                cla_t   = payload['views']['cla'][period_key]['geo']['totals']
                label   = payload['periods'][period_key]['label']
                print(f"    {period_key} ({label}): GEO=${g_total:,.0f}  ADV=${a_total:,.0f}  "
                      f"NNA=${n_net:,.0f}  NMNC=${cla_t['nmnc_nna']:,.0f}  NMEC=${cla_t['nmec_nna']:,.0f}")
        elif args.upload:
            write_s3(payload, granularity=granularity)
        else:
            if args.output:
                # Insert granularity before .json extension
                output_path = args.output.replace('.json', f'_{granularity}.json')
            else:
                output_path = DEFAULT_LOCAL_OUTPUT.replace('.json', f'_{granularity}.json')
            write_local(payload, output_path)

    if args.dry_run:
        print("\nOK: Dry run complete -- no output written")
        sys.exit(0)

    print('\n============================================================')
    print(f'COMPLETE: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print(f'Generated {len(granularities)} variant(s): {", ".join(granularities)}')
    print('============================================================')


if __name__ == '__main__':
    main()
