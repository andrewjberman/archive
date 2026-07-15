"""Shared utilities for Orion API bronze -> silver/api_dims converters.

Used by every silver/api_dims/* converter (household, performance, activity, billing)
and by sibling lane scripts (L1 tax/cost basis via DS~B, L4 assets via DS~D) so all
silver/api_dims/* parquet share the same partition layout, advisor_firm derivation,
INFGRD allowlist, and Orion CSV value parsing.

Project: ADVI_INFSHIP Phase 1 L2 (silver pipeline extension)
Author: 0.4.0_DS_ClientPlatform~A
"""

from __future__ import annotations

import os
import re
from datetime import date, datetime
from io import BytesIO
from pathlib import Path

import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

S3_BUCKET = os.environ.get('INF_S3_BUCKET', 'opal-data-inf')
BRONZE_API_PREFIX = 'bronze/orion-api/'
SILVER_API_DIMS_PREFIX = 'silver/api_dims/'


def _resolve_local_bronze_dir() -> str:
    """Locate the bronze pulls directory across local-dev + EC2-runner layouts.

    Resolution order (first match wins):
      1. `$OPAL_BRONZE_PULLS_DIR` env override (operator dispatch hint)
      2. `<silver_lib SCRIPT_DIR>/pulls/` — EC2 runner where `sync_scripts` flattens
         pull_inflection_*.py + this lib into `/tmp/orion_gold_scripts/`. The pull
         scripts write to `SCRIPT_DIR/pulls/` via their own
         `Path(__file__).resolve().parent / "pulls"` pattern, which lands inside
         the same flattened dir.
      3. `data/inf/manual_api/pulls` — repo-relative local-dev layout where the
         pull scripts live at `data/inf/manual_api/` and write to their adjacent
         `pulls/` subdir; this lib at `data/inf/scripts/silver/` cannot reach it
         via SCRIPT_DIR so we fall through to the canonical relative path.

    Existence check on candidate 2 is REQUIRED — silver_lib's SCRIPT_DIR/pulls/
    exists ONLY on EC2 (where the pull script wrote there before this silver step
    fires). On local-dev `data/inf/scripts/silver/pulls/` doesn't exist, so we
    correctly fall through to candidate 3.

    Pre-fix incident 2026-05-11 23:36Z: chain INF_API_SILVER_REPS failed because
    silver hardcoded `data/inf/manual_api/pulls` while pull_inflection_*.py
    wrote to `/tmp/orion_gold_scripts/pulls/` via SCRIPT_DIR. Boot dispatcher
    (AE 0.7 commit 6a916cccb) got the chain to run; this lib fix resolves the
    path mismatch so silver can find the bronze JSON regardless of cwd.
    """
    env_override = os.environ.get('OPAL_BRONZE_PULLS_DIR', '').strip()
    if env_override:
        return env_override
    script_dir = Path(__file__).resolve().parent
    flat_candidate = script_dir / 'pulls'
    if flat_candidate.is_dir():
        return str(flat_candidate)
    return 'data/inf/manual_api/pulls'


LOCAL_BRONZE_API_DIR = _resolve_local_bronze_dir()


def _resolve_local_silver_dims_dir() -> str:
    """Locate the silver api_dims WRITE directory across local-dev + EC2-runner layouts.

    Resolution order (first match wins):
      1. `$OPAL_SILVER_DIMS_DIR` env override (operator dispatch hint)
      2. `data/inf/silver/api_dims` — local-dev cwd is repo-root; detected via
         `os.path.isdir('data')` (true on local-dev where the repo's data/ subdir
         exists adjacent to cwd; false on EC2 runner cwd=/tmp/orion_gold_scripts
         where no `data` dir exists nor is creatable due to /tmp ownership).
      3. `<silver_lib SCRIPT_DIR>/silver_api_dims/` — EC2 runner fallback. The
         tmpfs at SCRIPT_DIR is writeable; this gives the write a safe target
         without leaning on relative-path-from-cwd resolution which fails when
         cwd has no `data/` subdir.

    Existence check on candidate 2 is REPLACED with `os.path.isdir('data')` —
    UNLIKE the bronze read-side helper, silver is a WRITE target where the
    final destination dir doesn't exist YET. We can't use `is_dir()` on the
    silver dir itself. Instead detect the runtime layout by checking if `data/`
    (the parent shared with bronze, present at repo-root in local-dev) exists.

    Pre-fix incident 2026-05-11 23:50Z: chain INF_API_SILVER_REPS reached
    build_representatives (via DS~C 650f91a0b READ fix), parsed 18 reps + 310
    hh-rep mappings, then failed at `write_silver_api_dim_parquet:301` —
    `os.makedirs('data')` raised PermissionError on EC2 (cwd=/tmp/orion_gold_scripts).
    Same fix-class as 650f91a0b READ side; this WRITE-side mirror plus the
    READ-side covers the full silver-builder surface.
    """
    env_override = os.environ.get('OPAL_SILVER_DIMS_DIR', '').strip()
    if env_override:
        return env_override
    if os.path.isdir('data'):
        return 'data/inf/silver/api_dims'
    script_dir = Path(__file__).resolve().parent
    return str(script_dir / 'silver_api_dims')


LOCAL_SILVER_API_DIMS_DIR = _resolve_local_silver_dims_dir()

DEFAULT_PREFER_S3 = os.environ.get('INF_PREFER_S3', '').strip().lower() in ('1', 'true', 'yes')

PARTNER_FIRM_TAGS = {
    'inflection': 'inflection_wealth_management',
}
INFLECTION_ADVISOR_FIRM_TAG = PARTNER_FIRM_TAGS['inflection']
INFLECTION_REP_IDS = {3, 6, 11, 12}

GUARD_B_AUA_LOWER = 150_000_000
GUARD_B_AUA_UPPER = 300_000_000

_s3 = boto3.client('s3', region_name='us-east-1')


def derive_advisor_firm(rep_id) -> str:
    if rep_id is None or rep_id == '':
        return 'unknown'
    try:
        rid = int(rep_id)
    except (ValueError, TypeError):
        try:
            rid = int(float(rep_id))
        except (ValueError, TypeError):
            return 'unknown'
    if rid in INFLECTION_REP_IDS:
        return INFLECTION_ADVISOR_FIRM_TAG
    return 'other'


def parse_dollar(s) -> float:
    if s is None:
        return 0.0
    txt = str(s).strip()
    if not txt or txt.lower() in {'nan', 'n/a', 'none', 'error:not supported'} or txt.startswith('Error:') or txt.startswith('{ERROR'):
        return 0.0
    cleaned = txt.replace('$', '').replace(',', '').replace('%', '').strip()
    if not cleaned or cleaned == '-':
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_percent_decimal(s) -> float:
    """Parse Orion percent strings like '12.85 %' -> 0.1285 (decimal form)."""
    txt = str(s).strip() if s is not None else ''
    if not txt or txt.lower() in {'nan', 'n/a', 'none'} or txt.startswith('Error:') or txt.startswith('{ERROR'):
        return float('nan')
    cleaned = txt.replace('%', '').replace(',', '').strip()
    try:
        return float(cleaned) / 100.0
    except ValueError:
        return float('nan')


def parse_int_score(s) -> int:
    """Parse Orion integer score strings (Sharpe / Sortino / Beta currently return int score)."""
    txt = str(s).strip() if s is not None else ''
    if not txt or txt.lower() in {'nan', 'n/a', 'none'} or txt.startswith('Error:') or txt.startswith('{ERROR'):
        return 0
    try:
        return int(float(txt.replace(',', '').strip()))
    except ValueError:
        return 0


def parse_orion_date(s):
    """Parse Orion date strings like '4/29/2023 12:00 AM' -> python date.

    Handles:
      - '1/15/2025 12:00:00 AM'  (Custom Reports/28198 transactions feed; seconds)
      - '4/29/2023 12:00 AM'     (legacy ExcelReports/Verbose; minutes only)
      - '4/29/2023'              (date-only)
      - '2023-04-29'             (ISO)

    Bug fix 2026-05-08T17:31Z (DS~A JOE-TXN-BACKFILL incident): the seconds
    variant `MM/DD/YYYY HH:MM:SS AM/PM` was missing — Orion's transactions
    Custom Report 28198 returns dates with seconds, causing all silver
    `trans_date` to land as None and INF_C_01 to drop ~99% of rows on
    NaT-guard. Add the seconds format first (most common in current data).
    """
    txt = str(s).strip() if s is not None else ''
    if not txt or txt.lower() in {'nan', 'n/a', 'none'} or txt.startswith('Error:'):
        return None
    for fmt in (
        '%m/%d/%Y %I:%M:%S %p',
        '%m/%d/%Y %I:%M %p',
        '%m/%d/%Y',
        '%Y-%m-%d',
    ):
        try:
            return datetime.strptime(txt, fmt).date()
        except ValueError:
            continue
    return None


def parse_int(s) -> int | None:
    if s is None:
        return None
    txt = str(s).strip()
    if not txt or txt.lower() in {'nan', 'n/a', 'none'}:
        return None
    try:
        return int(float(txt))
    except ValueError:
        return None


def add_required_silver_cols(df: pd.DataFrame, snapshot_date: date, rep_id_col: str = 'rep_id') -> pd.DataFrame:
    """Add the 4 columns every silver/api_dims/* parquet must carry.

    snapshot_date  - partition key (date the bronze CSV was pulled)
    source_system  - 'orion-api' literal
    rep_id_col     - existing rep_id column (renamed if not 'rep_id')
    advisor_firm   - derived from rep_id via INFGRD PARTNER_FIRM_TAGS
    """
    if rep_id_col != 'rep_id':
        df = df.rename(columns={rep_id_col: 'rep_id'})
    df['snapshot_date'] = snapshot_date
    df['source_system'] = 'orion-api'
    df['advisor_firm'] = df['rep_id'].apply(derive_advisor_firm)
    return df


# ----------------------------------------------------------------------------
# SILVER ID DTYPE CONVENTION (2026-05-11, ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY):
# All columns ending in _id MUST be Int64 (nullable). Use coerce_silver_ids()
# before `return df[cols]` in every build_* function. Removes cross-dim concat
# dtype drift at source. Gold layer has a belt-and-suspenders coerce_id_columns
# helper (data/inf/scripts/gold/lib/dtype_coerce.py) that defends against
# any reintroduced inconsistency; silver-side enforcement here is canonical.
# Excludes `additional_rep_ids` which is intentionally a `;`-separated string
# list (NOT a scalar ID).
# ----------------------------------------------------------------------------
DEFAULT_SILVER_ID_COLS: tuple[str, ...] = (
    "account_id",
    "household_id",
    "rep_id",
    "client_id",
    "registration_id",
    "custodian_id",
    "transaction_id",
    "trans_id",
)


def coerce_silver_ids(df: pd.DataFrame, cols=None) -> pd.DataFrame:
    """Coerce all canonical silver ID columns to pandas Int64 (nullable). Idempotent.

    Use immediately before `return df[cols]` in every silver build_* function.
    Default `cols` covers the full canonical set (DEFAULT_SILVER_ID_COLS).
    Missing columns are silently skipped. Non-numeric strings coerce to <NA>
    via pd.to_numeric(errors='coerce').

    Returns the same DataFrame with each present column coerced to Int64.
    """
    if cols is None:
        cols = DEFAULT_SILVER_ID_COLS
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    return df


def filter_to_inflection(df: pd.DataFrame, rep_id_col: str = 'rep_id') -> pd.DataFrame:
    """Apply INFGRD allowlist filter — return rows where rep_id IN INFLECTION_REP_IDS."""
    rep_ids_str = {str(r) for r in INFLECTION_REP_IDS}

    def _is_inf(v):
        if v is None or v == '':
            return False
        s = str(v).strip().split('.')[0]
        return s in rep_ids_str

    return df[df[rep_id_col].apply(_is_inf)].copy()


def apply_aua_guard(df: pd.DataFrame, value_col: str, source_desc: str) -> None:
    """No-op — Guard B retired per Andrew directive 2026-05-08T~13:48Z.

    Guard B was a hard $150M-$300M sanity band (ADVI_INFGRD.002 PRD §5.3).
    Andrew called it "vestigial guardrail not logical and we dont want it."
    Function kept as a no-op so existing callers across builders compile and
    run unchanged; observability log retained so AUA totals are still visible
    in builder output for spot-checks.
    """
    total = df[value_col].sum() if value_col in df.columns else 0.0
    print(
        f"  AUA observed [{source_desc}]: ${total:,.0f} ({len(df)} rows; Guard B retired)",
        flush=True,
    )


def bronze_api_local_path(snapshot_date: date, dim: str, suffix: str = '.csv') -> str:
    """Local bronze path: data/inf/manual_api/pulls/{YYYYMMDD}_{dim}{suffix}.

    Used pre-AE-S3-bronze-landing. Once L5 lands bronze in S3, switch to bronze_api_s3_key.
    """
    date_str = snapshot_date.strftime('%Y%m%d')
    return f"{LOCAL_BRONZE_API_DIR}/{date_str}_{dim}{suffix}"


def bronze_api_s3_key(snapshot_date: date, dim: str, suffix: str = '.csv') -> str:
    """S3 bronze key: bronze/orion-api/{YYYY-MM-DD}/{dim}{suffix} (per PRD §3.1 layout)."""
    date_str = snapshot_date.strftime('%Y-%m-%d')
    return f"{BRONZE_API_PREFIX}{date_str}/{dim}{suffix}"


def silver_api_dim_local_path(dim: str, snapshot_date: date) -> str:
    date_str = snapshot_date.strftime('%Y-%m-%d')
    return f"{LOCAL_SILVER_API_DIMS_DIR}/{dim}/snapshot_date={date_str}/data.parquet"


def silver_api_dim_s3_key(dim: str, snapshot_date: date) -> str:
    date_str = snapshot_date.strftime('%Y-%m-%d')
    return f"{SILVER_API_DIMS_PREFIX}{dim}/snapshot_date={date_str}/data.parquet"


def write_silver_api_dim_parquet(
    df: pd.DataFrame,
    dim: str,
    snapshot_date: date,
    upload_s3: bool = False,
) -> tuple[str, str | None]:
    """Write df to silver/api_dims/{dim}/snapshot_date=YYYY-MM-DD/data.parquet.

    Always writes local copy. If upload_s3=True, also uploads to S3.
    Returns (local_path, s3_key_or_None).
    """
    local_path = silver_api_dim_local_path(dim, snapshot_date)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, local_path, compression='snappy')

    s3_key: str | None = None
    if upload_s3:
        s3_key = silver_api_dim_s3_key(dim, snapshot_date)
        buf = BytesIO()
        pq.write_table(table, buf, compression='snappy')
        buf.seek(0)
        _s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=buf.getvalue())
    return local_path, s3_key


def read_bronze_csv(snapshot_date: date, dim: str, prefer_s3: bool | None = None) -> pd.DataFrame:
    """Read bronze CSV. Local default for DS workflows; flip to S3 in Lambda via env var.

    Resolution order for the prefer_s3 decision:
      1. Explicit caller argument (prefer_s3=True/False) — highest precedence
      2. INF_PREFER_S3 env var ('1'/'true'/'yes' → True; anything else → False)
      3. Default False (local read at LOCAL_BRONZE_API_DIR)

    AE 0.6.1~B B2 silver-chain Lambda sets INF_PREFER_S3=true at deploy so all silver
    builders read from s3://{INF_S3_BUCKET}/bronze/orion-api/{date}/{dim}.csv without
    code changes in convert_orion_api_to_silver.py / build_billing_dim.py / etc.
    """
    if prefer_s3 is None:
        prefer_s3 = DEFAULT_PREFER_S3
    if prefer_s3:
        key = bronze_api_s3_key(snapshot_date, dim)
        obj = _s3.get_object(Bucket=S3_BUCKET, Key=key)
        return pd.read_csv(BytesIO(obj['Body'].read()), dtype=str)
    local = bronze_api_local_path(snapshot_date, dim)
    if not os.path.exists(local):
        raise FileNotFoundError(
            f"Bronze CSV not found at {local}. "
            f"Either run the manual pull (data/inf/manual_api/pull_*.py), "
            f"set INF_PREFER_S3=true to read from S3, "
            f"or pass prefer_s3=True explicitly."
        )
    return pd.read_csv(local, dtype=str)


# --------------------------------------------------------------------------
# ADVI_ETLFIX WS-1 -- shared tolerated-source DEFER guard (CTO arch-gate 2026-07-02)
# --------------------------------------------------------------------------
# The uniform robustness contract for EVERY silver converter whose bronze source is a TOLERATED
# best-effort pull (INF_API_PULL_*): on an ABSENT bronze the converter DEFERs (carry-forward the
# prior silver partition) + fires a LOUD ChainStepDegraded metric + hard-stops past a staleness
# ceiling -- it NEVER hard-aborts the 63-step chain and NEVER silently serves stale. DRYs the
# arch-gate-PASSED inline txn (b7dc964db) + perf (c6332e5dd) guards into ONE place. FORMAT-AGNOSTIC:
# defer_guard_bronze does the presence-check + policy on a bronze KEY; the CALLER does its own
# format-specific read (.jsonl.gz gunzip / CSV) once the verdict is PROCEED. So ONE guard covers the
# 6 read_bronze_csv steps (reps/hhrep/accounts_v2/tax/billing/perf_dim) + assets_v2 + positions_mv.
CW_NAMESPACE = 'Inflection/GoldChain'   # the IAM-scoped namespace (runner iam.tf); any other = deny
CW_SERVICE = 'inf-gold-layer-runner'


def emit_chain_step_degraded(step: str, days_stale: int) -> None:
    """ChainStepDegraded=1 + a ChainStepStalenessDays gauge (keyed by the Step dim) to
    Inflection/GoldChain so a DEFERred/carried-forward converter is VISIBLE to ops -- degraded !=
    silent (CTO arch-gate). Uniform metric for ALL tolerated-source converters. Best-effort: the
    WARN log + the caller's return code are the load-bearing signals."""
    try:
        cw = boto3.client('cloudwatch', region_name='us-east-1')
        dims = [{'Name': 'Service', 'Value': CW_SERVICE}, {'Name': 'Step', 'Value': step}]
        cw.put_metric_data(Namespace=CW_NAMESPACE, MetricData=[
            {'MetricName': 'ChainStepDegraded', 'Value': 1.0, 'Unit': 'Count', 'Dimensions': dims},
            {'MetricName': 'ChainStepStalenessDays', 'Value': float(days_stale),
             'Unit': 'Count', 'Dimensions': dims},
        ])
    except Exception:  # noqa: BLE001 -- best-effort; the WARN + rc are the hard signals
        pass


def _latest_silver_partition_date(silver_prefix: str) -> date | None:
    """Newest {date}.parquet partition date under s3://{S3_BUCKET}/{silver_prefix}/ (or None).
    Handles both flat ({date}.parquet) and Hive (snapshot_date=YYYY-MM-DD/) partition layouts."""
    paginator = _s3.get_paginator('list_objects_v2')
    dates: list[date] = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=silver_prefix.rstrip('/') + '/'):
        for o in page.get('Contents', []):
            rel = o['Key'][len(silver_prefix.rstrip('/')) + 1:]
            token = rel.split('/', 1)[0]
            if token.startswith('snapshot_date='):
                token = token.split('=', 1)[1]
            elif token.endswith('.parquet'):
                token = token[:-len('.parquet')]
            else:
                continue
            try:
                dates.append(date.fromisoformat(token))
            except ValueError:
                continue
    return max(dates) if dates else None


def bronze_key_present(bronze_key: str) -> bool:
    """True if bronze_key exists on S3. NoSuchKey/404 -> False (a DEFER-able absence); any OTHER
    error re-raises (a real fault is not DEFER-able)."""
    try:
        _s3.head_object(Bucket=S3_BUCKET, Key=bronze_key)
        return True
    except Exception as e:  # noqa: BLE001 -- narrow: only absence -> False, else re-raise
        s = str(e)
        if 'NoSuchKey' in s or 'Not Found' in s or '404' in s:
            return False
        raise


def defer_guard_bronze(bronze_key: str, silver_prefix: str, pull_date: str, step: str,
                       n_ceiling: int = 2) -> str:
    """Shared tolerated-source DEFER policy (CTO arch-gate). Checks bronze_key presence; returns a
    verdict the caller acts on:
      'PROCEED' -- bronze present; caller does its normal read.
      'DEFER'   -- bronze ABSENT, latest silver partition <= n_ceiling trading days behind pull_date;
                   caller SKIPs its silver write + returns 0 (carry-forward the prior partition).
      'BLOCK'   -- bronze ABSENT AND (> n_ceiling trading days behind OR no prior silver partition);
                   caller returns 1 (fail-loud -- a persistent outage must not roll forward stale
                   indefinitely, and there is nothing to carry forward on a first-run gap).
    On any non-PROCEED it emits ChainStepDegraded=1 + ChainStepStalenessDays so the degrade is
    VISIBLE. FORMAT-AGNOSTIC (works for .jsonl.gz and CSV bronze). n_ceiling: N=2 default (gains/
    perf detail, self-correcting); tighter N=1 for served-AUA-feeding dims (positions_mv)."""
    if bronze_key_present(bronze_key):
        return 'PROCEED'
    pull_d = date.fromisoformat(pull_date)
    latest = _latest_silver_partition_date(silver_prefix)
    if latest is None:
        emit_chain_step_degraded(step, 9999)
        return 'BLOCK'   # nothing to carry forward
    days_stale = max(0, len(pd.bdate_range(latest, pull_d)) - 1)
    emit_chain_step_degraded(step, days_stale)
    return 'BLOCK' if days_stale > n_ceiling else 'DEFER'


def normalize_column_names(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """Rename selected columns. Drops any column not in mapping (keeps schema lean)."""
    keep = {src: dst for src, dst in mapping.items() if src in df.columns}
    df = df[list(keep.keys())].rename(columns=keep)
    return df


def slug_advisor_key(rep_name: str) -> str:
    """Snake-case slug from rep_name. Mirrors silver/convert_orion_to_silver._advisor_key."""
    if not rep_name or not isinstance(rep_name, str):
        return 'unknown'
    s = rep_name.strip().lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or 'unknown'
