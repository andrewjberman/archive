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

# Top N clients per architect in adv_drill (per-client AUA drill-down)
TOP_N_CLIENTS_PER_ARCH = 8

# Top N cities per state in cla.geo_city_drill
MAX_CLA_CITIES = 9

# For filters/snapshots
TOP_N_CITIES      = 50
TOP_N_IMPLEMENTOR = 50
TOP_N_STATE       = 49
TOP_N_RELATIONSHIP = 100

# Top positions by unrealized gain shown in tax section
TOP_GAIN_POSITIONS = 20

# ---------------------------------------------------------------------------
# Y3: Asset class classification (name-pattern based)
# ---------------------------------------------------------------------------
# Order matters: more specific patterns checked first.
_CASH_PATTERNS = (
    'cash', 't-bill', 'treasury bill', 'money market', 'mm fund',
    'sweep', 'fdic', 'savings',
)
_FIXED_INCOME_PATTERNS = (
    'bond', 'treasury', 'credit', 'clo', 'duration', 'fixed income',
    'aggregate', 'high yield', 'investment grade', 'tips', 'muni',
    'corporate', 'govt', 'government', 'floating rate', 'loan',
    'mortgage', 'mbs', 'abs', 'securitized',
)
_REAL_ESTATE_PATTERNS = (
    'reit', 'real estate', 'property', 'mortgage reit',
)
_ALTERNATIVES_PATTERNS = (
    'gold', 'commodity', 'vix', 'infrastructure',
    'hedge', 'private', 'alternative', 'merger', 'arbitrage',
    'mlp', 'pipeline', 'timber', 'farmland',
)
_INTL_EQUITY_PATTERNS = (
    'eafe', 'emerging', 'international', 'global', 'world', 'foreign',
    'europe', 'asia', 'japan', 'china', 'em ', 'intl', 'developed markets',
    'ex-us', 'ex us', 'non-us', 'non us', 'acwi',
)
_EQUITY_PATTERNS = (
    's&p', 'nasdaq', 'dividend', 'equity', 'value', 'growth', 'stock',
    'large cap', 'mid cap', 'small cap', 'total market', 'russell',
    'dow', 'bluechip', 'sector', 'technology', 'healthcare', 'financial',
    'energy', 'consumer', 'industrial', 'utilities', 'materials',
    'vti', 'voo', 'spy', 'qqq', 'iwm', 'dia',
)

ASSET_CLASS_LABELS = {
    'equities':     'Equities',
    'fixed_income': 'Fixed Income',
    'real_estate':  'Real Estate',
    'alternatives': 'Alternatives',
    'cash':         'Cash',
    'other':        'Other',
}


def _classify_asset(name: str) -> str:
    """Classify an asset name into one of 6 asset classes."""
    if not name or (isinstance(name, float) and np.isnan(name)):
        return 'other'
    nl = name.lower()
    if any(p in nl for p in _CASH_PATTERNS):
        return 'cash'
    if any(p in nl for p in _FIXED_INCOME_PATTERNS):
        return 'fixed_income'
    if any(p in nl for p in _REAL_ESTATE_PATTERNS):
        return 'real_estate'
    if any(p in nl for p in _ALTERNATIVES_PATTERNS):
        return 'alternatives'
    if any(p in nl for p in _INTL_EQUITY_PATTERNS):
        return 'equities'
    if any(p in nl for p in _EQUITY_PATTERNS):
        return 'equities'
    return 'other'


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
        CacheControl='public, max-age=300, s-maxage=3600',
    )
    print(f"  Wrote {key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# AUA certification helpers  (ADVI_PSCFIX)
# ---------------------------------------------------------------------------

def _load_aua_certification(today_str: str):
    """
    Load gold/aua_certification/{today}.json from S3.
    Returns parsed dict if present, None otherwise (non-blocking).
    Schema: {date, certified_aua, gold_aua, gap_abs, gap_pct, liability_types_excluded}
    """
    key = f"gold/aua_certification/{today_str}.json"
    try:
        resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
        data = json.loads(resp['Body'].read())
        print(f"  AUA certification loaded: certified_aua={data.get('certified_aua'):,.2f}, "
              f"gold_aua={data.get('gold_aua'):,.2f}, gap_pct={data.get('gap_pct'):.4f}")
        return data
    except Exception as e:
        print(f"  AUA certification absent or unreadable ({e}) -- using gold totals")
        return None


def _build_static_aua_periods(perf: pd.DataFrame, cdim: pd.DataFrame) -> dict:
    """
    Compute static period-level NMNC/NMEC AUA for quarterly, monthly, annually.

    NMNC definition (static, period-bound): for a given period P with
    [period_start, period_end], NMNC contains clients whose first_seen_date
    falls within that specific period.  Once the period ends those clients
    become NMEC permanently in all subsequent periods.

    NMEC: all clients active at period_end whose first_seen_date is before
    period_start.

    Guarantee: NMNC + NMEC == total_aua at period_end snapshot (within float
    rounding) for every emitted period.

    # NOTE -- rolling/gradient NMNC definition (NOT used for aua view):
    # The old daily aua view used a trailing-12-month window:
    #   cohort = 'NMNC' if months_since_first <= 12 else 'NMEC'
    # This definition is preserved for future views that may need it
    # (e.g. a gradient lifecycle chart).  It must not be wired to any v1
    # portal view.  The static period-bound definition above is the correct
    # one for the Assets Overview AUA toggle.

    Period boundaries:
      Quarterly: Q1=Jan1-Mar31, Q2=Apr1-Jun30, Q3=Jul1-Sep30, Q4=Oct1-Dec31
      Monthly:   calendar month start/end
      Annually:  Jan1-Dec31

    Window: emit all periods from the earliest first_seen_date through
    current.  Frontend applies its own time-window filter on top.
    """
    perf_dates = sorted(perf['date'].unique())
    perf_ts = pd.DatetimeIndex(perf_dates)
    earliest_first_seen = cdim['first_seen_date'].dropna().min()
    latest_perf_date = perf_ts.max()

    def _snap_date(period_end: pd.Timestamp):
        """Last available perf date <= period_end; None if period pre-dates data."""
        candidates = perf_ts[perf_ts <= period_end]
        return candidates[-1] if len(candidates) > 0 else None

    def _periods_quarterly() -> list:
        first_year = earliest_first_seen.year
        first_q = (earliest_first_seen.month - 1) // 3
        cur_year = latest_perf_date.year
        cur_q = (latest_perf_date.month - 1) // 3
        results = []
        year, q = first_year, first_q
        while (year, q) <= (cur_year, cur_q):
            period_start = pd.Timestamp(year=year, month=q * 3 + 1, day=1)
            next_q_month = q * 3 + 4
            if next_q_month > 12:
                cal_end = pd.Timestamp(year=year + 1, month=1, day=1) - pd.Timedelta(days=1)
            else:
                cal_end = pd.Timestamp(year=year, month=next_q_month, day=1) - pd.Timedelta(days=1)
            is_current = (year == cur_year and q == cur_q)
            period_end = latest_perf_date if is_current else cal_end
            snap = _snap_date(period_end)
            if snap is not None:
                snap_df = perf[perf['date'] == snap][['relationship_id', 'total_aua']]
                nmnc_rels = set(cdim[
                    (cdim['first_seen_date'] >= period_start) &
                    (cdim['first_seen_date'] <= period_end)
                ]['relationship_id'])
                nmnc = float(snap_df[snap_df['relationship_id'].isin(nmnc_rels)]['total_aua'].sum())
                nmec = float(snap_df[~snap_df['relationship_id'].isin(nmnc_rels)]['total_aua'].sum())
                results.append({
                    'period':   f"{year}-Q{q + 1}",
                    'label':    f"Q{q + 1} '{str(year)[2:]}",
                    'end_date': period_end.strftime('%Y-%m-%d'),
                    'NMNC':     round(nmnc, 2),
                    'NMEC':     round(nmec, 2),
                })
            q += 1
            if q > 3:
                q = 0
                year += 1
        return results

    def _periods_monthly() -> list:
        first_ym = earliest_first_seen.to_period('M')
        cur_ym = latest_perf_date.to_period('M')
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        results = []
        ym = first_ym
        while ym <= cur_ym:
            period_start = ym.to_timestamp(how='start')
            cal_end = ym.to_timestamp(how='end').normalize()
            is_current = (ym == cur_ym)
            period_end = latest_perf_date if is_current else cal_end
            snap = _snap_date(period_end)
            if snap is not None:
                snap_df = perf[perf['date'] == snap][['relationship_id', 'total_aua']]
                nmnc_rels = set(cdim[
                    (cdim['first_seen_date'] >= period_start) &
                    (cdim['first_seen_date'] <= period_end)
                ]['relationship_id'])
                nmnc = float(snap_df[snap_df['relationship_id'].isin(nmnc_rels)]['total_aua'].sum())
                nmec = float(snap_df[~snap_df['relationship_id'].isin(nmnc_rels)]['total_aua'].sum())
                results.append({
                    'period':   str(ym),
                    'label':    f"{month_names[period_start.month - 1]} '{str(period_start.year)[2:]}",
                    'end_date': period_end.strftime('%Y-%m-%d'),
                    'NMNC':     round(nmnc, 2),
                    'NMEC':     round(nmec, 2),
                })
            ym += 1
        return results

    def _periods_annually() -> list:
        results = []
        for year in range(earliest_first_seen.year, latest_perf_date.year + 1):
            period_start = pd.Timestamp(year=year, month=1, day=1)
            cal_end = pd.Timestamp(year=year, month=12, day=31)
            is_current = (year == latest_perf_date.year)
            period_end = latest_perf_date if is_current else cal_end
            snap = _snap_date(period_end)
            if snap is not None:
                snap_df = perf[perf['date'] == snap][['relationship_id', 'total_aua']]
                nmnc_rels = set(cdim[
                    (cdim['first_seen_date'] >= period_start) &
                    (cdim['first_seen_date'] <= period_end)
                ]['relationship_id'])
                nmnc = float(snap_df[snap_df['relationship_id'].isin(nmnc_rels)]['total_aua'].sum())
                nmec = float(snap_df[~snap_df['relationship_id'].isin(nmnc_rels)]['total_aua'].sum())
                results.append({
                    'period':   str(year),
                    'label':    str(year),
                    'end_date': period_end.strftime('%Y-%m-%d'),
                    'NMNC':     round(nmnc, 2),
                    'NMEC':     round(nmec, 2),
                })
        return results

    aua_out = {}
    for gran, fn in (('quarterly', _periods_quarterly),
                     ('monthly',   _periods_monthly),
                     ('annually',  _periods_annually)):
        data = fn()
        aua_out[gran] = {'categories': ['NMNC', 'NMEC'], 'data': data}
        print(f"  aua static ({gran}): {len(data)} periods")
    return aua_out


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
                 'primary_city', 'primary_state', 'primary_country',
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
# Y3: Asset class AUA mix from holdings_lots snapshots
# ---------------------------------------------------------------------------

def _build_aua_mix(today: pd.Timestamp) -> list:
    """
    Load monthly holdings_lots snapshots, classify each lot by asset_name,
    and aggregate market_value by asset class per month.

    Returns list of {period, segments: [{label, value}, ...]}.
    """
    prefix = 'gold/holdings_lots/'
    # List available snapshot dates
    paginator = s3.get_paginator('list_objects_v2')
    snapshot_keys = []
    for page in paginator.paginate(Bucket=INPUT_BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            fname = key.split('/')[-1]
            # Only daily snapshots (YYYY-MM-DD.parquet), skip backfill files
            if fname.endswith('.parquet') and not fname.startswith('backfill'):
                try:
                    d = pd.Timestamp(fname.replace('.parquet', ''))
                    snapshot_keys.append((d, key))
                except Exception:
                    continue

    if not snapshot_keys:
        print("  WARN: no holdings_lots snapshots found -- aua_mix skipped")
        return []

    snapshot_keys.sort(key=lambda x: x[0])

    # Pick last snapshot per month
    monthly_picks = {}
    for d, key in snapshot_keys:
        ym = d.to_period('M')
        monthly_picks[ym] = (d, key)

    # Also compute quarterly and yearly aggregates from monthly data
    aua_mix_data = []
    monthly_class_totals = {}  # ym -> {class: value}

    for ym in sorted(monthly_picks.keys()):
        snap_date, snap_key = monthly_picks[ym]
        try:
            df = _load_parquet(snap_key, columns=['asset_name', 'market_value', 'is_open'])
            df = df[df['is_open'] == True]
            df['asset_class'] = df['asset_name'].apply(_classify_asset)
            class_agg = df.groupby('asset_class')['market_value'].sum()

            segments = []
            for cls_key in ASSET_CLASS_LABELS:
                val = float(class_agg.get(cls_key, 0.0))
                segments.append({
                    'label': ASSET_CLASS_LABELS[cls_key],
                    'value': round(val, 2),
                })
            aua_mix_data.append({'period': str(ym), 'segments': segments})
            monthly_class_totals[ym] = {cls_key: float(class_agg.get(cls_key, 0.0))
                                        for cls_key in ASSET_CLASS_LABELS}
        except Exception as e:
            print(f"  WARN: failed to load holdings_lots {snap_key}: {e}")
            continue

    print(f"  aua_mix: {len(aua_mix_data)} monthly snapshots loaded")
    return aua_mix_data


# ---------------------------------------------------------------------------
# 1. timeseries_chart.json  (CumulativeChartResponse)
# ---------------------------------------------------------------------------

def build_timeseries_chart(perf: pd.DataFrame, adv: pd.DataFrame, geo: pd.DataFrame,
                            cdim: pd.DataFrame, today: pd.Timestamp,
                            geo_city: pd.DataFrame = None,
                            cert: dict = None) -> dict:
    """
    4+1 views:
      aua           -- static period-level NMNC vs NMEC (quarterly/monthly/annually)
      nna           -- cumulative firm-level NNA (daily)
      geo           -- cumulative AUA by top states (stacked, daily)
      adv           -- cumulative AUA by top architects (stacked, daily)
      geo_drill     -- per-state city-level AUA timeseries (optional, daily)
      adv_drill     -- per-architect per-client AUA timeseries (ADVI-004 A1, daily)
      cla           -- NMNC/NMEC AUM at total/geo_drill/adv_drill/geo_city_drill grains (ADVI-004 A2, daily)

    cert: optional parsed gold/aua_certification/{today}.json dict; when
          present the current-period NMNC/NMEC values in each granularity are
          scaled so that NMNC+NMEC == certified_aua exactly.
    """
    print("Building timeseries_chart.json...")

    # ---- Metadata: new_clients per window ----
    new_clients_meta = {}
    for label, days in WINDOWS.items():
        cutoff = today - pd.Timedelta(days=days)
        new_clients_meta[label] = int((cdim['first_seen_date'] >= cutoff).sum())

    # ---- Extended merge: first_seen_date + dimensional attrs for adv_drill / cla ----
    perf_cohort = perf[['date', 'relationship_id', 'total_aua']].merge(
        cdim[['relationship_id', 'relationship_name', 'first_seen_date',
              'primary_architect', 'primary_state', 'primary_city']],
        on='relationship_id', how='left',
    )
    # Rolling/gradient cohort classification (trailing-12-month window).
    # This is the ROLLING definition -- NOT used for the aua view.
    # Used only for cla sub-views (ADVI-004 A2) and preserved here for
    # future views that may need it.  Must not be wired to any v1 portal
    # AUA bar chart.  See ADVI_PSCFIX_PRD.md for the two-definition system.
    perf_cohort['months_since_first'] = (
        (perf_cohort['date'] - perf_cohort['first_seen_date']).dt.days / 30.44
    )
    perf_cohort['cohort'] = np.where(
        perf_cohort['months_since_first'] <= 12,
        'NMNC',   # New Money New Clients (rolling: within trailing 12mo)
        'NMEC',   # New Money Existing Clients (rolling: older than 12mo)
    )

    # ---- AUA view: static period-level NMNC/NMEC (ADVI_PSCFIX) ----
    # Uses the STATIC period-bound definition: for each bar, NMNC = clients
    # whose first_seen_date falls within that specific period; NMEC = all
    # others.  Pre-aggregated at quarterly/monthly/annually granularities.
    # The old rolling daily array is replaced by this structure.
    aua_periods = _build_static_aua_periods(perf, cdim)

    # Apply certified_aua scaling to the current (last) period in each
    # granularity so that NMNC+NMEC == certified_aua exactly.
    if cert:
        for gran in ('quarterly', 'monthly', 'annually'):
            data = aua_periods[gran]['data']
            if not data:
                continue
            last = data[-1]
            gold_total = last['NMNC'] + last['NMEC']
            if gold_total > 0:
                scale = cert['certified_aua'] / gold_total
                last['NMNC'] = round(last['NMNC'] * scale, 2)
                last['NMEC'] = round(last['NMEC'] * scale, 2)
        print(f"  aua cert override applied: certified_aua={cert['certified_aua']:,.2f}")

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

    # ---- ADV DRILL (per-architect -> per-client AUA timeseries) ---- A1
    # Keys must match adv.categories exactly (architect display names).
    # Category string per client: "{relationship_name} ({relationship_id})"
    # to prevent collision if two clients share a name.
    def _client_cat_key(rid, name):
        clean = str(name).strip() if pd.notna(name) and str(name).strip() else ''
        return f"{clean} ({rid})" if clean else str(rid)

    adv_drill = {}
    drill_archs = [a for a in adv_categories if a != 'Other']
    for arch in drill_archs:
        arch_perf = perf_cohort[perf_cohort['primary_architect'] == arch].copy()
        if arch_perf.empty:
            continue

        # Top N clients by latest-date AUA
        latest_dt_arch = arch_perf['date'].max()
        top_clients = (
            arch_perf[arch_perf['date'] == latest_dt_arch]
            .nlargest(TOP_N_CLIENTS_PER_ARCH, 'total_aua')
            [['relationship_id', 'relationship_name']]
        )
        cat_key_map = {
            row['relationship_id']: _client_cat_key(row['relationship_id'], row['relationship_name'])
            for _, row in top_clients.iterrows()
        }
        top_ids = set(cat_key_map)

        arch_perf['_cat'] = arch_perf['relationship_id'].apply(
            lambda rid: cat_key_map.get(rid, 'Other')
        )
        arch_pivot = (
            arch_perf.groupby(['date', '_cat'])['total_aua']
            .sum()
            .unstack(fill_value=0)
            .sort_index()
            .reset_index()
        )
        # Preserve top-client order; append Other if present
        arch_categories = [
            cat_key_map[rid] for rid in top_clients['relationship_id']
            if cat_key_map[rid] in arch_pivot.columns
        ]
        if 'Other' in arch_pivot.columns:
            arch_categories.append('Other')

        arch_data = []
        for _, row in arch_pivot.iterrows():
            point = {'date': row['date'].strftime('%Y-%m-%d')}
            for cat in arch_categories:
                point[cat] = round(float(row.get(cat, 0)), 2)
            arch_data.append(point)

        adv_drill[arch] = {
            'description': f'Per-client AUA for architect {arch}',
            'categories': arch_categories,
            'data': arch_data,
        }
    print(f"  adv_drill: {len(adv_drill)} architects with client drill-down")

    # ---- CLA (Client Lifecycle Analysis: NMNC/NMEC AUA timeseries) ---- A2
    # NMNC/NMEC rule: same trailing-12-month vintage classification as aua view
    # (perf_cohort.cohort already computed above from months_since_first).
    # Produces: total, geo_drill, adv_drill, geo_city_drill sub-views.

    def _cla_view(df_subset):
        """Build a CumulativeChartView {categories, data} for NMNC/NMEC over time."""
        daily = (
            df_subset.groupby(['date', 'cohort'])['total_aua']
            .sum()
            .unstack(fill_value=0)
            .sort_index()
            .reset_index()
        )
        for col in ('NMNC', 'NMEC'):
            if col not in daily.columns:
                daily[col] = 0.0
        return {
            'categories': ['NMNC', 'NMEC'],
            'data': [
                {'date': r['date'].strftime('%Y-%m-%d'),
                 'NMNC': round(float(r['NMNC']), 2),
                 'NMEC': round(float(r['NMEC']), 2)}
                for _, r in daily.iterrows()
            ],
        }

    # cla.total: firm-wide NMNC/NMEC AUA (same source as aua view)
    cla_total = _cla_view(perf_cohort)
    cla_total['description'] = 'Firm-wide AUM by client vintage (NMNC=new <=12mo, NMEC=existing >12mo)'

    # cla.geo_drill[state]: per-state NMNC/NMEC AUA; keys match geo.categories
    drill_states_cla = [s for s in top_states if s != 'Other']
    cla_geo_drill = {}
    for state in drill_states_cla:
        state_rows = perf_cohort[perf_cohort['primary_state'] == state]
        if state_rows.empty:
            continue
        view = _cla_view(state_rows)
        view['description'] = f'AUM by client vintage for state {state}'
        cla_geo_drill[state] = view

    # cla.adv_drill[arch]: per-architect NMNC/NMEC AUA; keys match adv.categories
    cla_adv_drill = {}
    for arch in drill_archs:
        arch_rows = perf_cohort[perf_cohort['primary_architect'] == arch]
        if arch_rows.empty:
            continue
        view = _cla_view(arch_rows)
        view['description'] = f'AUM by client vintage for architect {arch}'
        cla_adv_drill[arch] = view

    # cla.geo_city_drill[state][city]: uses cdim.primary_city (CTO A2 correction)
    # State keys match geo.categories; city keys are city display names.
    cla_geo_city_drill = {}
    for state in drill_states_cla:
        state_rows = perf_cohort[
            (perf_cohort['primary_state'] == state) &
            perf_cohort['primary_city'].notna() &
            (perf_cohort['primary_city'] != '')
        ]
        if state_rows.empty:
            continue

        # Top cities by latest-date AUA for this state
        latest_dt_state = state_rows['date'].max()
        top_cities = (
            state_rows[state_rows['date'] == latest_dt_state]
            .groupby('primary_city')['total_aua'].sum()
            .nlargest(MAX_CLA_CITIES)
            .index.tolist()
        )
        if not top_cities:
            continue

        cla_geo_city_drill[state] = {}
        for city in top_cities:
            city_rows = state_rows[state_rows['primary_city'] == city]
            if city_rows.empty:
                continue
            view = _cla_view(city_rows)
            view['description'] = f'AUM by client vintage for {city}, {state}'
            cla_geo_city_drill[state][city] = view

        if not cla_geo_city_drill[state]:
            del cla_geo_city_drill[state]

    print(f"  cla: {len(cla_geo_drill)} state drill, {len(cla_adv_drill)} arch drill, "
          f"{len(cla_geo_city_drill)} state city-drill")

    # ---- Y5: Growth decomposition (monthly granularity) ----
    # market(month) = aua_end - aua_start - nna_net
    # total(month)  = aua_end - aua_start = market + nna
    #
    # IMPORTANT: use last-of-prior-month as aua_start/nna_start (not first-of-current-month).
    # The two differ when NNA flows occur at exact month boundaries (e.g. the 1st of a month).
    # Using last-of-prior-month ensures the sum of all monthly nna_net values telescopes to
    # the same result as the NNA view's year-endpoint diff:
    #   sum(nna_net_Jan..Dec) = nna(Dec_last) - nna(Dec_last_prev_year)
    # This keeps NNA view and GRO consistent across all granularities and time windows.
    daily_firm = (
        perf.groupby('date')[['total_aua', 'nna']].sum()
        .sort_index()
        .reset_index()
    )
    daily_firm['year_month'] = daily_firm['date'].dt.to_period('M')
    growth_data = []
    prev_aua: float | None = None
    prev_nna: float | None = None
    for ym, grp in daily_firm.groupby('year_month'):
        grp_sorted = grp.sort_values('date')
        aua_end = float(grp_sorted.iloc[-1]['total_aua'])
        nna_end = float(grp_sorted.iloc[-1]['nna'])
        if prev_aua is None:
            # First period: no prior-month endpoint available; fall back to
            # within-month diff for this period only (typically 1 day in June 2020).
            aua_start = float(grp_sorted.iloc[0]['total_aua'])
            nna_start = float(grp_sorted.iloc[0]['nna'])
        else:
            aua_start = prev_aua
            nna_start = prev_nna
        nna_net   = nna_end - nna_start
        total_chg = aua_end - aua_start
        market    = total_chg - nna_net
        growth_data.append({
            'period': str(ym),
            'market': round(market, 2),
            'nna':    round(nna_net, 2),
            'total':  round(total_chg, 2),
        })
        prev_aua = aua_end
        prev_nna = nna_end
    print(f"  growth_decomposition: {len(growth_data)} monthly periods")

    # ---- Y9: NNA at drill levels (cumulative per-category per-date) ----
    # nna_geo: per-state cumulative NNA, inflows, outflows
    geo_us_nna = geo[geo['country'].isin(['USA', 'US', '']) | geo['country'].isna()].copy()
    geo_us_nna = geo_us_nna[geo_us_nna['state'].notna() & (geo_us_nna['state'] != '')]
    geo_nna_pivot = geo_us_nna.copy()
    geo_nna_pivot['_state'] = geo_nna_pivot['state'].where(
        geo_nna_pivot['state'].isin(top_states), 'Other'
    )
    geo_nna_agg = (
        geo_nna_pivot.groupby(['date', '_state'])[['nna', 'cum_inflows', 'cum_outflows']]
        .sum()
        .sort_index()
        .reset_index()
    )
    nna_geo_data = []
    for dt, dt_grp in geo_nna_agg.groupby('date'):
        point = {'date': dt.strftime('%Y-%m-%d')}
        for _, row in dt_grp.iterrows():
            st = row['_state']
            point[st]              = round(float(row['nna']), 2)
            point[f'{st}_inflow']  = round(float(row['cum_inflows']), 2)
            point[f'{st}_outflow'] = round(float(row['cum_outflows']), 2)
        nna_geo_data.append(point)

    # nna_adv: per-architect cumulative NNA, inflows, outflows
    adv_nna_pivot = adv.copy()
    adv_nna_pivot['_arch'] = adv_nna_pivot['architect'].where(
        adv_nna_pivot['architect'].isin(top_architects), 'Other'
    )
    adv_nna_agg = (
        adv_nna_pivot.groupby(['date', '_arch'])[['nna', 'cum_inflows', 'cum_outflows']]
        .sum()
        .sort_index()
        .reset_index()
    )
    nna_adv_data = []
    for dt, dt_grp in adv_nna_agg.groupby('date'):
        point = {'date': dt.strftime('%Y-%m-%d')}
        for _, row in dt_grp.iterrows():
            arch = row['_arch']
            point[arch]                = round(float(row['nna']), 2)
            point[f'{arch}_inflow']    = round(float(row['cum_inflows']), 2)
            point[f'{arch}_outflow']   = round(float(row['cum_outflows']), 2)
        nna_adv_data.append(point)

    # nna_geo_drill: per-city cumulative NNA, inflows, outflows within top states
    nna_geo_drill = {}
    if geo_city is not None and not geo_city.empty:
        drill_states_nna = [s for s in top_states if s != 'Other']
        for state in drill_states_nna:
            state_city_nna = geo_city[geo_city['state'] == state].copy()
            if state_city_nna.empty:
                continue
            latest_city_nna = state_city_nna[state_city_nna['date'] == state_city_nna['date'].max()]
            top_cities_nna = latest_city_nna.nlargest(MAX_DRILL_CITIES, 'total_aua')['city'].tolist()
            state_city_nna['_city'] = state_city_nna['city'].where(
                state_city_nna['city'].isin(top_cities_nna), 'Other'
            )
            city_nna_agg = (
                state_city_nna.groupby(['date', '_city'])[['nna', 'cum_inflows', 'cum_outflows']]
                .sum()
                .sort_index()
                .reset_index()
            )
            city_cats = [c for c in top_cities_nna if c in city_nna_agg['_city'].unique()]
            if 'Other' in city_nna_agg['_city'].unique():
                city_cats.append('Other')
            city_nna_data = []
            for dt, dt_grp in city_nna_agg.groupby('date'):
                point = {'date': dt.strftime('%Y-%m-%d')}
                for _, row in dt_grp.iterrows():
                    city = row['_city']
                    point[city]                = round(float(row['nna']), 2)
                    point[f'{city}_inflow']    = round(float(row['cum_inflows']), 2)
                    point[f'{city}_outflow']   = round(float(row['cum_outflows']), 2)
                city_nna_data.append(point)
            nna_geo_drill[state] = {
                'categories': city_cats,
                'data': city_nna_data,
            }

    print(f"  nna_geo: {len(nna_geo_data)} days, nna_adv: {len(nna_adv_data)} days"
          + (f", nna_geo_drill: {len(nna_geo_drill)} states" if nna_geo_drill else ""))

    # ---- Y3: Asset class AUA mix from holdings_lots ----
    aua_mix_data = _build_aua_mix(today)

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
        'aua': aua_periods,
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
        'growth_decomposition': {
            'description': 'Monthly AUA change decomposed into market appreciation and NNA',
            'data': growth_data,
        },
        'nna_geo': {
            'description': 'Cumulative NNA, inflows, outflows by US state',
            'categories': geo_categories,
            'data': nna_geo_data,
        },
        'nna_adv': {
            'description': 'Cumulative NNA, inflows, outflows by architect',
            'categories': adv_categories,
            'data': nna_adv_data,
        },
    }

    # Only add geo_drill when populated (avoids empty key in JSON)
    if geo_drill:
        result['geo_drill'] = geo_drill

    # Y9: NNA geo drill (per-city NNA with inflow/outflow within top states)
    if nna_geo_drill:
        result['nna_geo_drill'] = nna_geo_drill

    # adv_drill: per-architect per-client AUA drill (ADVI-004 A1)
    if adv_drill:
        result['adv_drill'] = adv_drill

    # Y3: asset class AUA mix (monthly snapshots from holdings_lots)
    if aua_mix_data:
        result['aua_mix'] = {
            'description': 'AUA breakdown by asset class (monthly from holdings snapshots)',
            'categories': list(ASSET_CLASS_LABELS.values()),
            'data': aua_mix_data,
        }

    # cla: NMNC/NMEC timeseries at total/geo_drill/adv_drill/geo_city_drill (ADVI-004 A2)
    cla = {
        'total':     cla_total,
        'geo_drill': cla_geo_drill,
        'adv_drill': cla_adv_drill,
    }
    if cla_geo_city_drill:
        cla['geo_city_drill'] = cla_geo_city_drill
    result['cla'] = cla

    n_qtd = len(aua_periods['quarterly']['data'])
    print(f"  timeseries_chart: aua({n_qtd}q/{len(aua_periods['monthly']['data'])}m/"
          f"{len(aua_periods['annually']['data'])}y), "
          f"{len(adv_categories)} architects, {len(geo_categories)} states"
          + (f", {len(geo_drill)} state drill-downs" if geo_drill else "")
          + (f", {len(adv_drill)} arch client-drills" if adv_drill else "")
          + (f", cla({len(cla_geo_drill)}geo/{len(cla_adv_drill)}adv"
             + (f"/{len(cla_geo_city_drill)}citygeo" if cla_geo_city_drill else "") + ")")
          + (f", aua_mix: {len(aua_mix_data)} months" if aua_mix_data else ""))
    return result


# ---------------------------------------------------------------------------
# 2. Leaderboard helpers
# ---------------------------------------------------------------------------

def _leaderboard_entries(df_by_date: pd.DataFrame, dim_col: str,
                          cdim: pd.DataFrame, architect_col: str,
                          window_start: pd.Timestamp) -> list:
    """
    Build ranked LeaderboardEntry list for one time window.

    df_by_date: daily timeseries (adv or account-performance-based) with
                date, {dim_col}, total_aua, nna columns
    architect_col: column in cdim that maps to dim_col (e.g. 'primary_architect')
    window_start: start of the window (either rolling or calendar QTD/YTD)
    """
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
    # Rolling trailing windows
    for label, days in WINDOWS.items():
        w_start = today - pd.Timedelta(days=days)
        entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect', w_start)
        windows_data[label] = _leaderboard_window_data(entries)
        print(f"  Window {label}: {len(entries)} architects")
    # Calendar QTD window (Jan 1 / Apr 1 / Jul 1 / Oct 1)
    qtd_start = _quarter_start(today, 0)
    entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect', qtd_start)
    windows_data['qtd'] = _leaderboard_window_data(entries)
    print(f"  Window qtd: {len(entries)} architects (calendar start={qtd_start.date()})")
    # Calendar YTD window (Jan 1 of current year)
    # In Q1 (Jan-Mar), qtd and ytd have identical start dates (both Jan 1)
    ytd_start = pd.Timestamp(year=today.year, month=1, day=1)
    entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect', ytd_start)
    windows_data['ytd'] = _leaderboard_window_data(entries)
    print(f"  Window ytd: {len(entries)} architects (calendar start={ytd_start.date()})")

    latest_date = adv['date'].max()
    return {
        'generated_at':       datetime.now(timezone.utc).isoformat(),
        'data_as_of':         latest_date.strftime('%Y-%m-%d'),
        'firm_id':            FIRM_ID,
        'leaderboard_type':   'architect',
        'available_windows':  list(WINDOWS.keys()) + ['qtd', 'ytd'],
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
                          cdim: pd.DataFrame, today: pd.Timestamp,
                          cert: dict = None) -> dict:
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
        q_start  = _quarter_start(today, quarters_back)
        q_end    = _quarter_start(today, quarters_back - 1) - pd.Timedelta(days=1)
        prior_qe = q_start - pd.Timedelta(days=1)  # prior quarter-end (e.g. Sep 30) matches script 09
        nna_val = _nna_for_period((today - prior_qe).days) - (
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

    # Apply certified_aua override when available (simple replacement; NNA
    # values are flow metrics and are intentionally NOT overridden).
    display_aua = cert['certified_aua'] if cert else total_aua

    total = {
        'aua':                  round(display_aua, 2),
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

    print(f"  header_metrics: AUA={display_aua:,.0f} (gold={total_aua:,.0f}), NNA_12M={nna_12m:,.0f}")

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
                     geo: pd.DataFrame, adim: pd.DataFrame,
                     cert: dict = None) -> dict:
    """Returns dict of {output_key: response_dict} for each snapshot.

    cert: when present, total_aua in each snapshot is replaced with
    certified_aua and aua_pct per segment row is recomputed against it.
    Segment-level aua values are unchanged.
    """
    print("Building snapshot files...")

    latest_date  = adv['date'].max()
    perf_latest  = perf[perf['date'] == perf['date'].max()]
    adv_latest   = adv[adv['date'] == latest_date]
    geo_latest   = geo[geo['date'] == geo['date'].max()]
    gold_total_aua = float(perf_latest['total_aua'].sum())
    total_aua    = cert['certified_aua'] if cert else gold_total_aua
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
        'taxable':      ('Non-Qualified',   float(perf_latest['aua_taxable'].sum())),
        'tax_deferred': ('Tax-Deferred',    float(perf_latest['aua_tax_deferred'].sum())),
        'tax_exempt':   ('Tax-Free (Roth)', float(perf_latest['aua_tax_exempt'].sum())),
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

    # total_aua is already cert-overridden above when cert is present.
    # state_total (sum of top-N states) is replaced by total_aua for the
    # aua_by_state headline to match certified_aua. Segment-level aua values
    # and within-state aua_pct are unchanged.
    return {
        'gold/snapshots/aua_by_architect.json': _snapshot_response(
            'architect', arch_rows, total_aua, date_str),
        'gold/snapshots/aua_by_tax_status.json': _snapshot_response(
            'tax_status', tax_rows, total_aua, date_str),
        'gold/snapshots/aua_by_state.json': _snapshot_response(
            'state', state_rows, total_aua, date_str),
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
        # Step 1: Load all source parquets + AUA certification
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

        # Load AUA certification once; passed to each builder that outputs
        # total_aua.  Non-blocking: None means use gold-derived totals.
        cert = _load_aua_certification(today.strftime('%Y-%m-%d'))
        results_cert = 'applied' if cert else 'absent (gold totals)'

        # ------------------------------------------------------------------
        # Step 2: Build and write each output
        # ------------------------------------------------------------------
        print("\n=== Step 2: Build outputs ===")
        results = {}

        # timeseries_chart.json
        chart = build_timeseries_chart(perf, adv, geo, cdim, today,
                                        geo_city=geo_city, cert=cert)
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
        hm = build_header_metrics(perf, adv, cdim, today, cert=cert)
        _save_json(hm, 'gold/summary/header_metrics.json')
        results['header_metrics'] = 'ok'

        # DISABLED: EC2 gold script 09_generate_partner_analytics.py now owns this output.
        # The EC2 version includes nested cities, nested clients, and 4-period time machine.
        # Re-enabling the Lambda version would overwrite the richer EC2 output.
        # NOTE: script 09 also needs a certified_aua override for its donut totals
        # (views.aua/geo/adv.current.donut.total).  See ADVI_PSCFIX_PRD.md Deliverable 3.
        # That change is a separate DS deliverable to 09_generate_partner_analytics.py.
        # pa = build_partner_analytics(perf, adv, geo, cdim, today)
        # _save_json(pa, 'gold/partner_analytics/header_metrics.json')
        results['partner_analytics'] = 'disabled (EC2 script owns output)'

        # filters/dimensions.json
        filters = build_filters(adv, adim, today)
        _save_json(filters, 'gold/filters/dimensions.json')
        results['filters'] = 'ok'

        # snapshots
        snapshots = build_snapshots(perf, adv, geo, adim, cert=cert)
        for key, snap in snapshots.items():
            _save_json(snap, key)
        results['snapshots'] = f"{len(snapshots)} files"
        results['aua_certification'] = results_cert

        # ------------------------------------------------------------------
        # Step 3: Summary
        # ------------------------------------------------------------------
        print("\n=== Step 3: Complete ===")
        latest_date = perf['date'].max()
        total_aua   = float(perf[perf['date'] == latest_date]['total_aua'].sum())
        display_aua = cert['certified_aua'] if cert else total_aua
        print(f"  Data as of:  {latest_date.date()}")
        print(f"  Total AUA:   ${display_aua:,.0f} (gold=${total_aua:,.0f})")
        print(f"  Outputs:     {results}")
        print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 70)

        # Fan-out: capture version manifest after all gold/ writes are done.
        # Invoked AFTER writes complete (not at handler start) so the manifest
        # reflects the versions that were just written.
        # S3 does not allow two notification rules with the same prefix+suffix
        # filter, so this uses Lambda-to-Lambda async (same as advisor-publisher).
        capture_fn = os.environ.get('CAPTURE_VERSIONS_FUNCTION')
        if capture_fn:
            try:
                boto3.client('lambda', region_name='us-east-1').invoke(
                    FunctionName=capture_fn,
                    InvocationType='Event',
                    Payload=json.dumps(event).encode(),
                )
                print(f"Fan-out: invoked {capture_fn} async")
            except Exception as e:
                print(f"WARN: Could not invoke {capture_fn}: {e}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':       'success',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'data_as_of':   latest_date.strftime('%Y-%m-%d'),
                'total_aua':    round(display_aua, 2),
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
