#!/usr/bin/env python3
"""
Incremental Daily Merge - Smart Append-Only

Instead of reprocessing the entire silver parquet, this script:
1. Reads ONLY the new daily xlsx from forwardfill_v2/
2. Converts to parquet and saves to silver/daily/YYYY-MM/
3. Never touches old data - true incremental append

The silver layer is now:
  - silver/daily/YYYY-MM/*.parquet  (daily incremental files)
  - silver/bd_transactions.parquet  (compacted view - rebuilt weekly)

Reading the silver layer:
  pd.read_parquet('s3://opal-data-bd/silver/daily/')  # reads all partitions

S3 I/O is boto3-native (ADVI_BDAPIMIG D2b) -- no aws-cli shell-out -- so this runs on a BARE Lambda
(the bd-silver-merge Lambda) AND on EC2/local unchanged. Programmatic entry: run(tables) /
lambda_handler(event) (event {"tables":["all"]} or a subset). CLI entry: main() (below).

Usage:
    python3 merge-daily-incremental.py            # transactions incremental (default)
    python3 merge-daily-incremental.py --all      # ALL 4 tables (== run(None); use for the one-time
                                                  #   first-run reprocess-once reconcile OFF the Lambda)
    python3 merge-daily-incremental.py --compact  # weekly transactions compaction
"""

from __future__ import annotations

import os
import subprocess
import json
import sys
import argparse
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

try:
    import boto3
except ImportError:
    boto3 = None

# Install pandas if needed
try:
    import pandas as pd
except ImportError:
    print("Installing pandas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "pyarrow", "openpyxl", "-q"])
    import pandas as pd

# Configuration
S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')
FORWARDFILL_PREFIX = "forwardfill_v2/transactions"
SILVER_DAILY_PREFIX = "silver/transactions"  # Flat structure (reorganized 2026-02-17)
SILVER_COMPACTED_KEY = "silver/bd_transactions.parquet"
SILVER_BD_ASSETS_DIM_KEY = "silver/bd_assets_dim.parquet"  # asset_id -> cusip bridge (CP-AE1, 2026-04-17)
MANIFEST_KEY = "silver/incremental_manifest.json"
LOCAL_DIR = Path("/tmp/bd-incremental")
CORRECT_COL_COUNT = 71

# Allocation configuration (mirrors transaction config)
FORWARDFILL_ALLOC_PREFIX = "forwardfill_v2/allocations"
SILVER_ALLOC_PREFIX = "silver/allocations"          # silver/allocations/YYYY-MM-DD.parquet
SILVER_ALLOC_COMPACTED_KEY = "silver/bd_allocations.parquet"
ALLOC_MANIFEST_KEY = "silver/incremental_allocation_manifest.json"
ALLOC_MIN_COL_COUNT = 30  # post-schema-change files have 94 cols; pre-change ~9 cols
                          # accept anything >= 30 to handle both
ALLOC_MIN_ROW_FRACTION = 0.5  # ADVI_ETLFIX bd stub-guard (2026-07-02): reject an allocations SNAPSHOT
                              # with < this fraction of the most-recent OTHER-date partition's rows --
                              # the intraday T-0 undersized-stub guard (see process_alloc_xlsx_to_parquet).

# Realized configuration
FORWARDFILL_REALIZED_PREFIX = "forwardfill_v2/realized"
SILVER_REALIZED_PREFIX = "silver/realized"
SILVER_REALIZED_COMPACTED_KEY = "silver/bd_realized.parquet"
REALIZED_MANIFEST_KEY = "silver/incremental_realized_manifest.json"
REALIZED_MIN_COL_COUNT = 10

# Unrealized configuration
FORWARDFILL_UNREALIZED_PREFIX = "forwardfill_v2/unrealized"
SILVER_UNREALIZED_PREFIX = "silver/unrealized"
SILVER_UNREALIZED_COMPACTED_KEY = "silver/bd_unrealized.parquet"
UNREALIZED_MANIFEST_KEY = "silver/incremental_unrealized_manifest.json"
UNREALIZED_MIN_COL_COUNT = 10

# BP-c-5 (ADVI_BDPRCE round 3, key ruled v1.1): lot-level unrealized. Lot key gains relationship_id.
# BP-b-6 (ADVI_BDPRCE round 2): lot-level unrealized. The template's Units (measure 15) and Cost Basis
# (measure 16) columns are routed to silver/unrealized_lots, de-duplicated on the LOT key. They never reach
# the legacy silver/unrealized table, which keeps its rows, columns and values.
LOT_MEASURE_COLS = ['units', 'cost_basis']
LOT_KEY_COLS = ['relationship_id', 'account_id', 'asset_id', 'open_date', 'unit_cost']  # BP-c-5: ruled key, PRD v1.1
LOT_DATASET = ('blackdiamond', '49financial', 'silver', 'unrealized_lots')


def build_unrealized_lots(df):
    """Lot-level rows from one export frame. Returns (lot_df, rows_before, rows_after) or (None, 0, 0)."""
    missing = [c for c in LOT_MEASURE_COLS + LOT_KEY_COLS if c not in df.columns]
    if missing:
        return None, 0, 0
    cols = LOT_KEY_COLS + LOT_MEASURE_COLS + [c for c in ('asset_name', '_source_file', '_ingested_at')
                                              if c in df.columns]
    lot = df[cols].copy()
    before = len(lot)
    lot = lot.drop_duplicates(subset=LOT_KEY_COLS, keep='first')
    return lot, before, len(lot)


def lot_address(file_date):
    """The lot partition address, from the naming builder (never typed). None if the builder is not importable."""
    try:
        from lib.opal_naming import address
    except Exception:
        return None
    return address(*LOT_DATASET, f'date={file_date}')


def _s3_upload_addr(local_path, address_uri):
    """Upload local_path to an s3:// address in any bucket (the lot table lives outside S3_BUCKET)."""
    c = _s3c()
    if c is None:
        return False
    bucket, key = address_uri[len('s3://'):].split('/', 1)
    try:
        c.upload_file(str(local_path), bucket, key + '/data.parquet')
        return True
    except Exception:
        return False


# ============================================================================
# boto3-native S3 I/O (ADVI_BDAPIMIG D2b) -- Lambda-runnable. Replaces the prior aws-cli
# subprocess shell-outs (aws s3 cp / aws s3 ls | grep | awk) so the merge runs on a BARE Lambda
# (no aws CLI) AND on EC2/local unchanged. Matches the bd-allocation-processor pure-boto3 pattern.
# ============================================================================
_S3_CLIENT = None


def _s3c():
    """Cached boto3 S3 client (Lambda-safe). None only if boto3 failed to import."""
    global _S3_CLIENT
    if _S3_CLIENT is None and boto3 is not None:
        _S3_CLIENT = boto3.client('s3', region_name='us-east-1')
    return _S3_CLIENT


def _s3_get_json(key):
    """Parse an S3 JSON object; None if absent/unreadable (replaces `aws s3 cp ... 2>/dev/null`)."""
    c = _s3c()
    if c is None:
        return None
    try:
        return json.loads(c.get_object(Bucket=S3_BUCKET, Key=key)['Body'].read())
    except Exception:
        return None


def _s3_put_json(key, obj):
    """Write a dict as an S3 JSON object (replaces the manifest `aws s3 cp` upload)."""
    c = _s3c()
    if c is None:
        return
    c.put_object(Bucket=S3_BUCKET, Key=key,
                 Body=json.dumps(obj, indent=2).encode('utf-8'),
                 ContentType='application/json')


def _s3_download(key, local_path):
    """Download S3 key -> local_path; True on success (replaces `aws s3 cp s3://.. local`)."""
    c = _s3c()
    if c is None:
        return False
    try:
        c.download_file(S3_BUCKET, key, str(local_path))
        return True
    except Exception:
        return False


def _s3_upload(local_path, key):
    """Upload local_path -> S3 key; True on success (replaces `aws s3 cp local s3://..`)."""
    c = _s3c()
    if c is None:
        return False
    try:
        c.upload_file(str(local_path), S3_BUCKET, key)
        return True
    except Exception:
        return False


def _s3_list_names(prefix, suffix='.xlsx'):
    """Basenames under prefix/ ending in suffix (replaces `aws s3 ls | grep | awk`)."""
    c = _s3c()
    if c is None:
        return []
    out = []
    for page in c.get_paginator('list_objects_v2').paginate(
            Bucket=S3_BUCKET, Prefix=prefix.rstrip('/') + '/'):
        for obj in page.get('Contents', []):
            name = obj['Key'].split('/')[-1]
            if name.endswith(suffix):
                out.append(name)
    return out


def _s3_list_keys(prefix, suffix='.parquet'):
    """Full keys under prefix/ ending in suffix, recursive (replaces `aws s3 ls --recursive | grep`)."""
    c = _s3c()
    if c is None:
        return []
    out = []
    for page in c.get_paginator('list_objects_v2').paginate(
            Bucket=S3_BUCKET, Prefix=prefix.rstrip('/') + '/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith(suffix):
                out.append(obj['Key'])
    return out


# ============================================================================
# CONTENT-KEYED (S3 ETag) RE-PROCESS SKIP -- HALF-2 freeze-class durable fix
# ADVI_BREAKS TO-6b / ADVI_BDAPIMIG D2 (CTO arch-ratified 2026-07-01 021037Z; mechanism
# source-confirmed). The prior skip keyed on bare FILENAME (`processed_files`): a same-filename
# bronze RE-LAND of FRESHER data -- BD's ~1-day lag re-delivers TRANSACTIONS_DAILY_{d}.xlsx with new
# trade_dates, or a restatement / D1 chunk re-pull overwrites a day -- was FILENAME-skipped, so
# silver froze BEHIND available data (the 06-26->06-29 49F freeze, source-confirmed 2026-06-30 by
# 0.6.0_AE; the same class hit cot/bd/inf 3x). FIX (mirrors the proven cot_silver_merge Cond-2,
# data/cot/scripts/bronze/tests/test_retry_net.py::TestCondCSilverEtagSkip): skip on the bronze
# object's S3 ETag (content identity), NOT the filename -- a re-land changes the ETag -> reprocess ->
# the per-date parquet is wholesale REPLACED. Rule-17-preserving: changes ONLY the skip predicate,
# never the merge content/dedup/columns. Auto-heals ANY re-land (daily lag, restatement, D1 chunk,
# manual backfill) with no bronze<->silver orchestration coupling. Applies to ALL 4 bd silver merges
# (transactions/allocations/realized/unrealized -- all shared the filename-skip root).
# Andrew 2026-07-02 directive: "monitor over a few days, logged extensively, no silent skips" -- so
# every per-file decision + a per-run summary are logged (see _select_target_files).
# ============================================================================

def _bronze_etag(forwardfill_prefix, filename):
    """Current S3 ETag (content identity) of the bronze forwardfill xlsx; None if absent/error.
    A re-landed (overwritten) object gets a NEW ETag = exactly the 'content changed -> reprocess'
    signal we want (and the ETag is stable for genuinely-unchanged content)."""
    if boto3 is None:
        return None
    key = f"{forwardfill_prefix}/{filename}"
    try:
        head = boto3.client('s3', region_name='us-east-1').head_object(Bucket=S3_BUCKET, Key=key)
        return str(head['ETag']).strip('"')
    except Exception:
        return None


def _load_processed_etags(manifest):
    """Return the {filename: etag} content-skip map. MIGRATES a legacy processed_files list (no
    etags) by seeding each filename as None = etag-UNKNOWN -> reprocess-ONCE (the real ETag is then
    stored, so subsequent UNCHANGED runs skip). The reprocess-once is deliberate + bounded: it
    self-heals any latent same-name-reland-not-propagated partition on the first post-deploy run AND
    reconciles the historical TXN_DAILY_* -> TRANSACTIONS_DAILY_* rename (the new names are simply new
    keys; the stale old names remain harmless orphans, never matched by list_forwardfill_files())."""
    pe = manifest.get('processed_etags')
    if isinstance(pe, dict):
        return dict(pe)
    return {f: None for f in manifest.get('processed_files', [])}


def _should_skip(filename, cur_etag, processed_etags):
    """Skip IFF we have a KNOWN prior ETag for this filename AND it matches the current bronze ETag.
    New file (absent), legacy-unknown (None), or a re-land (etag changed) -> do NOT skip. cur_etag
    None (bronze missing/unreadable) -> do NOT skip (let the download fail-close downstream)."""
    return cur_etag is not None and processed_etags.get(filename) == cur_etag


def _select_target_files(table_label, forwardfill_prefix, all_files, processed_etags):
    """Content-keyed file selection with EXTENSIVE per-file logging (Andrew 2026-07-02: 'monitor
    over a few days, logged extensively, no silent skips'). Logs each candidate's filename,
    recorded_etag, current_etag, and decision. Returns (target_files, cur_etags, counts):
      NEW                      -- filename never seen
      REPROCESS-legacy-unknown -- migrated legacy entry (etag None) reprocessing ONCE
      REPROCESS-etag-changed   -- same name, FRESHER content (the freeze this fixes)
      SKIP-unchanged           -- known filename, identical bronze ETag (no needless reprocess)"""
    target_files = []
    cur_etags = {}
    counts = {"new": 0, "reprocess": 0, "skip": 0}
    for f in all_files:
        cur = _bronze_etag(forwardfill_prefix, f)
        if _should_skip(f, cur, processed_etags):
            counts["skip"] += 1
            print(f"  [{table_label}] SKIP-unchanged {f} (etag={cur})")
            continue
        if f not in processed_etags:
            decision, rec = "NEW", "ABSENT"
            counts["new"] += 1
        elif processed_etags.get(f) is None:
            decision, rec = "REPROCESS-legacy-unknown", "None(migrated)"
            counts["reprocess"] += 1
        else:
            decision, rec = "REPROCESS-etag-changed", processed_etags.get(f)
            counts["reprocess"] += 1
        print(f"  [{table_label}] {decision} {f} (recorded_etag={rec} current_etag={cur})")
        cur_etags[f] = cur
        target_files.append(f)
    return target_files, cur_etags, counts


_BD_ASSETS_DIM_CACHE = None


def load_bd_assets_dim():
    """
    Load silver/bd_assets_dim.parquet and return a DataFrame with just
    [asset_id (str), cusip] for joining to silver/transactions rows.

    Cached per-process to avoid re-downloading when multiple xlsx files
    are processed in one run.
    """
    global _BD_ASSETS_DIM_CACHE
    if _BD_ASSETS_DIM_CACHE is not None:
        return _BD_ASSETS_DIM_CACHE
    if boto3 is None:
        return None
    try:
        _s3 = boto3.client('s3', region_name='us-east-1')
        body = _s3.get_object(Bucket=S3_BUCKET, Key=SILVER_BD_ASSETS_DIM_KEY)['Body'].read()
        dim = pd.read_parquet(BytesIO(body), columns=['asset_id', 'cusip'])
        dim['asset_id'] = dim['asset_id'].astype(str)
        # De-dup on asset_id; keep last-seen cusip (dim is one-row-per-asset_id already, but guard).
        dim = dim.drop_duplicates(subset='asset_id', keep='last')
        _BD_ASSETS_DIM_CACHE = dim
        return dim
    except Exception as e:
        print(f"    [enrich] bd_assets_dim load failed: {e}")
        return None


def enrich_with_cusip(df):
    """
    Left-join silver/bd_assets_dim.parquet on asset_id to add a `cusip` column.
    Idempotent: safe to call on DataFrames that already have cusip (overwrites
    with freshest dim value).

    Returns the DataFrame with `cusip` column added (nullable for rows whose
    asset_id isn't in the dim -- cash, synthetic, collective trusts, etc).
    Row count is preserved.
    """
    if 'asset_id' not in df.columns:
        print("    [enrich] no asset_id column; skipping cusip join")
        return df
    dim = load_bd_assets_dim()
    if dim is None or len(dim) == 0:
        print("    [enrich] bd_assets_dim unavailable; skipping cusip join")
        return df

    before = len(df)
    # Normalize asset_id to string for the join (left is often int from XLSX).
    # Preserve the original dtype on the way out.
    orig_dtype = df['asset_id'].dtype
    df = df.copy()
    df['_aid_str'] = df['asset_id'].astype(str)
    # Drop pre-existing cusip column so left-join doesn't create cusip_x/cusip_y.
    if 'cusip' in df.columns:
        df = df.drop(columns=['cusip'])
    merged = df.merge(
        dim.rename(columns={'asset_id': '_aid_str'}),
        on='_aid_str', how='left'
    )
    merged = merged.drop(columns=['_aid_str'])
    assert len(merged) == before, f"[enrich] row count drift: {before} -> {len(merged)}"
    # Restore original asset_id dtype (merge keeps it intact; explicit guard).
    if merged['asset_id'].dtype != orig_dtype:
        try:
            merged['asset_id'] = merged['asset_id'].astype(orig_dtype)
        except Exception:
            pass
    non_null = int(merged['cusip'].notna().sum())
    pct = (non_null / before * 100) if before else 0.0
    print(f"    [enrich] cusip: {non_null:,}/{before:,} non-null ({pct:.2f}%)")
    return merged


def read_timestamps_date(xlsx_path):
    """
    Read the canonical data date from the BD Timestamps sheet.

    All BD Data Mining exports have a second sheet called 'Timestamps' with
    metadata rows like:
        Start Date | 3/27/2026
        End Date   | 3/27/2026

    Uses End Date as the canonical as-of date. For single-day exports Start
    and End are identical; for multi-day ranges End Date is the most recent
    trading day covered by the export.

    Returns YYYY-MM-DD string, or None if not found.
    """
    try:
        ts_df = pd.read_excel(xlsx_path, sheet_name='Timestamps', header=None)
        for _, row in ts_df.iterrows():
            if str(row.iloc[0]).strip() == 'End Date':
                raw = row.iloc[1]
                dt = pd.to_datetime(raw, errors='coerce')
                if pd.notna(dt):
                    return dt.strftime('%Y-%m-%d')
    except Exception:
        pass
    return None


def to_snake_case(col):
    """Convert column name to snake_case."""
    col = str(col).strip().replace('%', 'pct').replace('49 House', 'house')
    col = col.replace(' ', '_').replace('.', '_').replace('-', '_')
    result = ''
    for i, c in enumerate(col):
        if c.isupper() and i > 0 and col[i - 1].islower():
            result += '_'
        result += c.lower()
    while '__' in result:
        result = result.replace('__', '_')
    return result.strip('_')


def load_manifest():
    """Load incremental manifest from S3 (boto3-native)."""
    m = _s3_get_json(MANIFEST_KEY)
    if m is not None:
        return m
    return {
        'processed_files': [],
        'daily_partitions': [],
        'last_updated': None,
        'last_compaction': None,
        'total_rows_estimate': 0
    }


def save_manifest(manifest):
    """Save manifest to S3 (boto3-native)."""
    _s3_put_json(MANIFEST_KEY, manifest)


def list_forwardfill_files():
    """List xlsx files in forwardfill_v2/transactions/ (boto3-native)."""
    return _s3_list_names(FORWARDFILL_PREFIX, '.xlsx')


def process_xlsx_to_parquet(xlsx_filename):
    """
    Process a single xlsx file and save as one parquet to silver/transactions/.
    Returns (partition_key, row_count) or (None, 0) on failure.

    Partition naming convention: silver/transactions/YYYY-MM-DD.parquet
      The date in the filename is the DATA DATE extracted from the BD XLSX
      filename -- the trading day the export covers -- not the date this script ran.
      BD names its exports with the data date:
        TXN_DAILY_2026-02-18.xlsx  ->  silver/transactions/2026-02-18.parquet

      IMPORTANT: A single BD export covers multiple trade_dates (today's trades
      plus retroactive corrections/additions for prior dates). We do NOT split by
      trade_date -- that would create incomplete partitions since BD continues to
      deliver corrections for past dates in future exports. All rows from the
      XLSX go into one parquet keyed by the export/data date.

      Downstream consumers load ALL partitions and deduplicate on transaction_id
      at query time. The filename date is irrelevant to gold scripts (00-08);
      bd-price-update Job 1 uses it to load T1 prices for a specific date.
    """
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    # Download xlsx
    xlsx_path = LOCAL_DIR / xlsx_filename
    s3_xlsx_key = f"{FORWARDFILL_PREFIX}/{xlsx_filename}"

    if not _s3_download(s3_xlsx_key, xlsx_path):
        print(f"  ERR: Failed to download {xlsx_filename}")
        return None, 0

    try:
        df = pd.read_excel(xlsx_path, sheet_name='Sheet1')

        if len(df.columns) != CORRECT_COL_COUNT:
            print(f"  ERR: {xlsx_filename}: {len(df.columns)} cols (expected {CORRECT_COL_COUNT})")
            return None, 0

        # Normalize columns
        df.columns = [to_snake_case(c) for c in df.columns]

        # Parse date columns as datetime64 (consistent with existing partitions)
        DATE_COLS = ['trade_date', 'settle_date', 'entry_date', 'return_date',
                     'start_date', 'account_create_date', 'performance_start_date',
                     'history_start_date', 'closed_date']
        for col in DATE_COLS:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Convert remaining mixed-type object columns to strings for pyarrow compatibility.
        # Preserve nulls as None -- do NOT convert NaN/None to empty string ''.
        # Turning nulls into '' causes pyarrow schema unification failures when downstream
        # readers try to cast '' to a numeric type (ArrowInvalid: Failed to parse string).
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

        # Add metadata
        df['_source_file'] = xlsx_filename
        df['_ingested_at'] = datetime.now(timezone.utc).isoformat()

        # Data date: read from BD Timestamps sheet (canonical), fall back to filename
        file_date = read_timestamps_date(xlsx_path)
        if file_date:
            print(f"    Data date from Timestamps sheet: {file_date}")
        else:
            import re
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', xlsx_filename)
            file_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
            print(f"    Data date from filename (Timestamps fallback): {file_date}")

        # Dedup against last 30 days of existing silver/transactions partitions.
        # BD occasionally re-sends prior transaction_ids in newer daily exports
        # (observed as 4-5x duplication starting 2026-01-27). Removing known
        # transaction_ids at ingestion keeps parquets clean so downstream scripts
        # don't need to load the full history to dedup.
        if 'transaction_id' in df.columns:
            before_dedup = len(df)
            cutoff = (pd.Timestamp(file_date) - pd.Timedelta(days=30)).strftime('%Y-%m-%d')
            seen_ids: set = set()
            if boto3 is not None:
                _s3 = boto3.client('s3', region_name='us-east-1')
                _pag = _s3.get_paginator('list_objects_v2')
                for _page in _pag.paginate(Bucket=S3_BUCKET, Prefix=SILVER_DAILY_PREFIX + '/'):
                    for obj in _page.get('Contents', []):
                        key = obj['Key']
                        if not key.endswith('.parquet'):
                            continue
                        key_date = key.split('/')[-1].replace('.parquet', '')
                        if key_date < cutoff or key_date >= file_date:
                            continue
                        try:
                            prior = pd.read_parquet(
                                BytesIO(_s3.get_object(Bucket=S3_BUCKET, Key=key)['Body'].read()),
                                columns=['transaction_id'])
                            seen_ids.update(prior['transaction_id'].dropna().astype(str).tolist())
                        except Exception:
                            pass
            if seen_ids:
                df = df[~df['transaction_id'].astype(str).isin(seen_ids)]
                removed = before_dedup - len(df)
                if removed > 0:
                    print(f"    Cross-date dedup: removed {removed:,} rows with "
                          f"transaction_ids seen in prior 30 days "
                          f"({before_dedup:,} -> {len(df):,})")

        # CP-AE1 (2026-04-17): enrich with cusip via bd_assets_dim asset_id bridge.
        # Nullable -- cash / CITs / synthetic rows legitimately have no CUSIP.
        df = enrich_with_cusip(df)

        # Write one parquet for the full XLSX -- all trade_dates included
        parquet_filename = f"{file_date}.parquet"
        parquet_path = LOCAL_DIR / parquet_filename
        df.to_parquet(parquet_path, index=False, engine='pyarrow', compression='snappy')

        s3_parquet_key = f"{SILVER_DAILY_PREFIX}/{parquet_filename}"
        _s3_upload(parquet_path, s3_parquet_key)

        print(f"  OK: {xlsx_filename} -> {s3_parquet_key} ({len(df):,} rows)")
        return s3_parquet_key, len(df)

    except Exception as e:
        print(f"  ERR: Error processing {xlsx_filename}: {e}")
        return None, 0


def incremental_merge():
    """Process new AND re-landed (bronze etag changed) files; append to daily partitions."""
    print("=" * 60)
    print(f"BD Incremental Merge [transactions] - {datetime.now().isoformat()}")
    print("=" * 60)

    manifest = load_manifest()
    migrated = 'processed_etags' not in manifest and bool(manifest.get('processed_files'))
    processed_etags = _load_processed_etags(manifest)
    if migrated:
        print(f"  [transactions] MIGRATION: legacy manifest ({len(processed_etags)} filenames, no "
              f"etags) -> etag-tracked; each reprocesses ONCE then etag-skips "
              f"(reconciles the TXN_DAILY_* -> TRANSACTIONS_DAILY_* rename).")
    print(f"Previously processed: {len(processed_etags)} files (etag-tracked)")

    all_files = list_forwardfill_files()
    target_files, cur_etags, counts = _select_target_files(
        "transactions", FORWARDFILL_PREFIX, all_files, processed_etags)

    if not target_files:
        print(f"No new or re-landed files to process  "
              f"[SUMMARY transactions: new=0 reprocess=0 skip={counts['skip']}]")
        return

    print(f"Found {len(target_files)} file(s) to process "
          f"(new={counts['new']} reprocess={counts['reprocess']} skip={counts['skip']})")
    print()

    # Process each target file (new + re-landed)
    total_rows = 0
    new_partitions = set(manifest.get('daily_partitions', []))
    failures = 0
    processed_dates = []

    for xlsx_file in target_files:
        partition_key, row_count = process_xlsx_to_parquet(xlsx_file)
        if partition_key:
            # Record the CONTENT identity we just processed (decision-time etag; fresh head only if
            # absent). A future re-land changes this -> reprocess -> REPLACE.
            processed_etags[xlsx_file] = cur_etags.get(xlsx_file) or _bronze_etag(FORWARDFILL_PREFIX, xlsx_file)
            new_partitions.add(partition_key)
            total_rows += row_count
            processed_dates.append(partition_key.split('/')[-1].replace('.parquet', ''))
        else:
            failures += 1

    # Update manifest (etag-tracked + back-compat filename list)
    manifest['processed_etags'] = processed_etags
    manifest['processed_files'] = sorted(processed_etags.keys())
    manifest['daily_partitions'] = list(new_partitions)
    manifest['last_updated'] = datetime.now(timezone.utc).isoformat()
    manifest['total_rows_estimate'] = manifest.get('total_rows_estimate', 0) + total_rows
    save_manifest(manifest)

    # Trigger bd-price-update Lambda now that new transaction data is in S3.
    # Only invoke if at least one partition was actually written this run (not just skipped).
    if total_rows > 0:
        print()
        print("Triggering bd-price-update...")
        # Pass the data date of the most-recently processed partition (this run only).
        latest_date = max(processed_dates)
        invoke_price_update(latest_date)

    max_data_date = max(processed_dates) if processed_dates else "(none)"
    print()
    print("=" * 60)
    print("INCREMENTAL MERGE COMPLETE [transactions]")
    print(f"  SUMMARY: {len(target_files)} processed | new={counts['new']} "
          f"reprocess={counts['reprocess']} skip={counts['skip']} | failures={failures} | "
          f"rows_added={total_rows} | max_data_date={max_data_date}")
    print("=" * 60)


def compact_silver_layer():
    """
    Weekly compaction: Read all daily partitions, dedupe, write single parquet.
    Run this on a schedule (weekly) to maintain query performance.
    """
    print("=" * 60)
    print(f"BD Silver Layer Compaction - {datetime.now().isoformat()}")
    print("=" * 60)

    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    # List all parquet files in silver/transactions/ (boto3-native)
    parquet_files = _s3_list_keys(SILVER_DAILY_PREFIX, '.parquet')

    if not parquet_files:
        print("No daily partitions to compact")
        return

    print(f"Found {len(parquet_files)} daily parquet files")

    # Download and combine
    dfs = []
    for pq_key in parquet_files:
        local_path = LOCAL_DIR / Path(pq_key).name
        _s3_download(pq_key, local_path)
        try:
            df = pd.read_parquet(local_path)
            dfs.append(df)
            print(f"  Read {pq_key}: {len(df)} rows")
        except Exception as e:
            print(f"  ERR: Failed to read {pq_key}: {e}")

    if not dfs:
        print("No data to compact")
        return

    # Combine and dedupe
    combined = pd.concat(dfs, ignore_index=True)
    before = len(combined)

    if 'transaction_id' in combined.columns:
        combined = combined.drop_duplicates(subset=['transaction_id'], keep='last')

    after = len(combined)
    print(f"\nCombined: {before} -> {after} rows (deduped)")

    # Save compacted parquet
    compacted_path = LOCAL_DIR / "bd_transactions_compacted.parquet"
    combined.to_parquet(compacted_path, index=False, engine='pyarrow', compression='snappy')

    file_size_mb = compacted_path.stat().st_size / (1024 * 1024)
    print(f"Compacted size: {file_size_mb:.1f} MB")

    # Upload (boto3-native)
    _s3_upload(compacted_path, SILVER_COMPACTED_KEY)
    print(f"Uploaded to s3://{S3_BUCKET}/{SILVER_COMPACTED_KEY}")

    # Update manifest
    manifest = load_manifest()
    manifest['last_compaction'] = datetime.now(timezone.utc).isoformat()
    manifest['compacted_rows'] = after
    save_manifest(manifest)

    print()
    print("=" * 60)
    print("COMPACTION COMPLETE")
    print("=" * 60)


# ============================================================================
# PRICE UPDATE TRIGGER
# ============================================================================

def invoke_price_update(date_str: str):
    """
    Invoke the bd-price-update Lambda asynchronously after new transaction
    data has been written to silver/transactions/.

    Invoked event-based (InvocationType='Event') -- we do not wait for the
    price update to complete. The Lambda will:
      - Load today's silver/transactions/YYYY-MM-DD.parquet for T1 prices
      - Read silver/historical_prices.parquet for T2 yfinance closes
      - Upsert new rows into silver/prices/canonical_prices.parquet

    Falls back gracefully if boto3 is unavailable or the invocation fails --
    the transaction merge is already committed to S3 regardless.
    """
    if boto3 is None:
        print("  WARNING: boto3 not available -- bd-price-update not triggered")
        return

    try:
        client = boto3.client('lambda', region_name='us-east-1')
        payload = json.dumps({'source': 'merge-daily-incremental', 'date': date_str})
        resp = client.invoke(
            FunctionName='bd-price-update',
            InvocationType='Event',   # async -- do not wait for response
            Payload=payload,
        )
        status = resp.get('StatusCode', 0)
        if status == 202:
            print(f"  OK: bd-price-update triggered (async) for {date_str}")
        else:
            print(f"  WARNING: bd-price-update invoke returned status {status}")
    except Exception as e:
        print(f"  WARNING: Could not invoke bd-price-update: {e}")
        print("           Canonical prices will not be updated automatically today.")


# ============================================================================
# ALLOCATION INCREMENTAL PROCESSING
# Mirrors transaction processing but targets silver/allocations/YYYY-MM-DD.parquet
# Deduplication key: (account_id, as_of_date) instead of transaction_id
# ============================================================================

def load_alloc_manifest():
    """Load allocation incremental manifest from S3 (boto3-native)."""
    m = _s3_get_json(ALLOC_MANIFEST_KEY)
    if m is not None:
        return m
    return {
        'processed_files': [],
        'daily_partitions': [],
        'last_updated': None,
        'last_compaction': None,
        'total_rows_estimate': 0,
    }


def save_alloc_manifest(manifest):
    """Save allocation manifest to S3 (boto3-native)."""
    _s3_put_json(ALLOC_MANIFEST_KEY, manifest)


def list_forwardfill_alloc_files():
    """List xlsx files in forwardfill_v2/allocations/ (boto3-native)."""
    return _s3_list_names(FORWARDFILL_ALLOC_PREFIX, '.xlsx')


def _latest_alloc_row_count(exclude_date):
    """Row count of the most-recent silver/allocations/{date}.parquet whose date != exclude_date --
    the completeness baseline for the intraday-stub reject. Returns None (caller fails OPEN) if there
    is no prior partition or it can't be read. Excludes exclude_date so a re-landed same-date stub is
    compared to the last GOOD day, not to itself / an already-landed stub of the same date."""
    keys = _s3_list_keys(SILVER_ALLOC_PREFIX, '.parquet')
    others = [k for k in keys if k.split('/')[-1].replace('.parquet', '') != exclude_date]
    if not others:
        return None
    latest = sorted(others, key=lambda k: k.split('/')[-1])[-1]
    c = _s3c()
    if c is None:
        return None
    try:
        body = c.get_object(Bucket=S3_BUCKET, Key=latest)['Body'].read()
    except Exception:
        return None
    try:
        return len(pd.read_parquet(BytesIO(body), columns=['account_id']))
    except Exception:
        try:
            return len(pd.read_parquet(BytesIO(body)))
        except Exception:
            return None


def process_alloc_xlsx_to_parquet(xlsx_filename):
    """
    Process a single allocation xlsx and save as parquet to silver/allocations/YYYY-MM-DD.parquet.

    Allocation files: ALLOC_YYYY-MM-DD.xlsx
    Output: silver/allocations/YYYY-MM-DD.parquet

    Key differences from transactions:
    - No strict column count check (schema changed 2026-01-19: 9 -> 94 cols)
    - Dedup key: (account_id, as_of_date) not transaction_id
    - Date for filename extracted from _source_date or as_of_date column

    Returns (s3_key, row_count) or (None, 0) on failure.
    """
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    # Download xlsx
    xlsx_path = LOCAL_DIR / xlsx_filename
    s3_xlsx_key = f"{FORWARDFILL_ALLOC_PREFIX}/{xlsx_filename}"

    if not _s3_download(s3_xlsx_key, xlsx_path):
        print(f"  ERR: Failed to download {xlsx_filename}")
        return None, 0

    try:
        df = pd.read_excel(xlsx_path, sheet_name='Sheet1')

        if len(df.columns) < ALLOC_MIN_COL_COUNT:
            print(f"  ERR: {xlsx_filename}: only {len(df.columns)} cols "
                  f"(expected >= {ALLOC_MIN_COL_COUNT}) -- skipping")
            return None, 0

        # Normalize columns to snake_case
        df.columns = [to_snake_case(c) for c in df.columns]

        # Parse date columns
        DATE_COLS = ['as_of_date', 'start_date', 'trade_date', 'settle_date',
                     'entry_date', 'return_date', 'history_start_date',
                     'closed_date', 'performance_start_date', 'account_create_date',
                     'relationship_termination_date', 'relationship_inception_date']
        for col in DATE_COLS:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Convert remaining object columns to strings for pyarrow compatibility.
        # Preserve nulls as None -- do NOT convert NaN/None to empty string ''.
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

        # Add metadata
        df['_source_file'] = xlsx_filename
        df['_ingested_at'] = datetime.now(timezone.utc).isoformat()

        # Data date: read from BD Timestamps sheet (canonical), fall back to filename
        file_date = read_timestamps_date(xlsx_path)
        if file_date:
            print(f"    Data date from Timestamps sheet: {file_date}")
        else:
            import re
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', xlsx_filename)
            file_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
            print(f"    Data date from filename (Timestamps fallback): {file_date}")

        # Dedup by (account_id, as_of_date) -- allocation snapshot key
        if 'account_id' in df.columns and 'as_of_date' in df.columns:
            before = len(df)
            df = df.drop_duplicates(subset=['account_id', 'as_of_date'], keep='first')
            removed = before - len(df)
            if removed:
                print(f"    Removed {removed:,} duplicate (account_id, as_of_date) pairs")

        # Completeness stub-reject (ADVI_ETLFIX bd stub-guard, 2026-07-02): BD returns an INTRADAY T-0
        # allocations SNAPSHOT as an undersized PARTIAL stub (the live 45KB 2026-07-02 leak vs the ~1.2MB
        # norm). The col-count check passes it, so it would land + shadow the good T-1 snapshot (silent
        # partial). Reject a snapshot whose row count is < ALLOC_MIN_ROW_FRACTION of the most-recent
        # OTHER-date partition. Fail-OPEN when there is no prior baseline (first-ever land) -- never
        # reject on uncertainty. Mirrors the unrealized 0-row skip + the holdings nzf floor;
        # Rule-17-consistent (rejects an incomplete SOURCE FILE, not a field-slim/row-filter within a
        # valid file). Returns None -> not marked processed -> re-checked next run -> self-heals when BD
        # lands a full snapshot (etag reprocess).
        baseline = _latest_alloc_row_count(file_date)
        if baseline and len(df) < ALLOC_MIN_ROW_FRACTION * baseline:
            print(f"  SKIP: {xlsx_filename}: {len(df):,} rows < {ALLOC_MIN_ROW_FRACTION:.0%} of the prior "
                  f"partition ({baseline:,}) -- undersized intraday T-0 STUB; NOT writing "
                  f"(prior complete snapshot stays; re-checked next run)")
            return None, 0

        # Write parquet
        parquet_filename = f"{file_date}.parquet"
        parquet_path = LOCAL_DIR / parquet_filename
        df.to_parquet(parquet_path, index=False, engine='pyarrow', compression='snappy')

        # Upload to silver/allocations/
        s3_key = f"{SILVER_ALLOC_PREFIX}/{parquet_filename}"
        _s3_upload(parquet_path, s3_key)

        print(f"  OK: {xlsx_filename} -> {s3_key} ({len(df)} rows, {len(df.columns)} cols)")
        return s3_key, len(df)

    except Exception as e:
        print(f"  ERR: Error processing {xlsx_filename}: {e}")
        return None, 0


def incremental_alloc_merge():
    """Process only new allocation files, write to silver/allocations/."""
    print("=" * 60)
    print(f"BD Allocation Incremental Merge - {datetime.now().isoformat()}")
    print("=" * 60)

    manifest = load_alloc_manifest()
    migrated = 'processed_etags' not in manifest and bool(manifest.get('processed_files'))
    processed_etags = _load_processed_etags(manifest)
    if migrated:
        print(f"  [allocations] MIGRATION: legacy manifest ({len(processed_etags)} filenames, no "
              f"etags) -> etag-tracked; each reprocesses ONCE then etag-skips.")
    print(f"Previously processed: {len(processed_etags)} allocation files (etag-tracked)")

    all_files = list_forwardfill_alloc_files()
    target_files, cur_etags, counts = _select_target_files(
        "allocations", FORWARDFILL_ALLOC_PREFIX, all_files, processed_etags)

    if not target_files:
        print(f"No new or re-landed allocation files to process  "
              f"[SUMMARY allocations: new=0 reprocess=0 skip={counts['skip']}]")
        return

    print(f"Found {len(target_files)} allocation file(s) to process "
          f"(new={counts['new']} reprocess={counts['reprocess']} skip={counts['skip']})")
    print()

    total_rows = 0
    new_partitions = set(manifest.get('daily_partitions', []))
    failures = 0
    processed_dates = []

    for xlsx_file in target_files:
        s3_key, row_count = process_alloc_xlsx_to_parquet(xlsx_file)
        if s3_key:
            processed_etags[xlsx_file] = cur_etags.get(xlsx_file) or _bronze_etag(FORWARDFILL_ALLOC_PREFIX, xlsx_file)
            new_partitions.add(s3_key)
            total_rows += row_count
            processed_dates.append(s3_key.split('/')[-1].replace('.parquet', ''))
        else:
            failures += 1

    manifest['processed_etags'] = processed_etags
    manifest['processed_files'] = sorted(processed_etags.keys())
    manifest['daily_partitions'] = list(new_partitions)
    manifest['last_updated'] = datetime.now(timezone.utc).isoformat()
    manifest['total_rows_estimate'] = manifest.get('total_rows_estimate', 0) + total_rows
    save_alloc_manifest(manifest)

    max_data_date = max(processed_dates) if processed_dates else "(none)"
    print()
    print("=" * 60)
    print("ALLOCATION INCREMENTAL MERGE COMPLETE")
    print(f"  SUMMARY: {len(target_files)} processed | new={counts['new']} "
          f"reprocess={counts['reprocess']} skip={counts['skip']} | failures={failures} | "
          f"rows_added={total_rows:,} | max_data_date={max_data_date}")
    print("=" * 60)


# ============================================================================
# REALIZED INCREMENTAL PROCESSING
# Mirrors allocation processing but targets silver/realized/YYYY-MM-DD.parquet
# Deduplication key: (account_id, asset_name, trade_date, unit_cost)
# Realized is INCREMENTAL -- each day adds that day's sells
# ============================================================================

def load_realized_manifest():
    """Load realized incremental manifest from S3 (boto3-native)."""
    m = _s3_get_json(REALIZED_MANIFEST_KEY)
    if m is not None:
        return m
    return {
        'processed_files': [],
        'daily_partitions': [],
        'last_updated': None,
        'last_compaction': None,
        'total_rows_estimate': 0,
    }


def save_realized_manifest(manifest):
    """Save realized manifest to S3 (boto3-native)."""
    _s3_put_json(REALIZED_MANIFEST_KEY, manifest)


def list_forwardfill_realized_files():
    """List xlsx files in forwardfill_v2/realized/ (boto3-native)."""
    return _s3_list_names(FORWARDFILL_REALIZED_PREFIX, '.xlsx')


def process_realized_xlsx_to_parquet(xlsx_filename):
    """
    Process a single realized xlsx and save as parquet to silver/realized/YYYY-MM-DD.parquet.

    Realized files: REALIZED_DAILY_YYYY-MM-DD.xlsx
    Output: silver/realized/YYYY-MM-DD.parquet

    Realized is INCREMENTAL -- each day's export contains that day's sells.
    Dedup key: (account_id, asset_name, trade_date, unit_cost)

    Returns (s3_key, row_count) or (None, 0) on failure.
    """
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    xlsx_path = LOCAL_DIR / xlsx_filename
    s3_xlsx_key = f"{FORWARDFILL_REALIZED_PREFIX}/{xlsx_filename}"

    if not _s3_download(s3_xlsx_key, xlsx_path):
        print(f"  FAIL: Failed to download {xlsx_filename}")
        return None, 0

    try:
        df = pd.read_excel(xlsx_path, sheet_name='Sheet1')

        if len(df.columns) < REALIZED_MIN_COL_COUNT:
            print(f"  FAIL: {xlsx_filename}: only {len(df.columns)} cols "
                  f"(expected >= {REALIZED_MIN_COL_COUNT}) -- skipping")
            return None, 0

        df.columns = [to_snake_case(c) for c in df.columns]

        DATE_COLS = ['trade_date', 'settle_date', 'entry_date', 'return_date',
                     'start_date', 'account_create_date', 'performance_start_date',
                     'history_start_date', 'closed_date', 'as_of_date',
                     'purchase_date', 'sell_date']
        for col in DATE_COLS:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

        df['_source_file'] = xlsx_filename
        df['_ingested_at'] = datetime.now(timezone.utc).isoformat()

        # Data date: read from BD Timestamps sheet (canonical), fall back to filename
        file_date = read_timestamps_date(xlsx_path)
        if file_date:
            print(f"    Data date from Timestamps sheet: {file_date}")
        else:
            import re
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', xlsx_filename)
            file_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
            print(f"    Data date from filename (Timestamps fallback): {file_date}")

        # Dedup by (account_id, asset_name, trade_date, unit_cost)
        dedup_cols = ['account_id', 'asset_name', 'trade_date', 'unit_cost']
        available_dedup = [c for c in dedup_cols if c in df.columns]
        if len(available_dedup) >= 2:
            before = len(df)
            df = df.drop_duplicates(subset=available_dedup, keep='first')
            removed = before - len(df)
            if removed:
                print(f"    Removed {removed:,} duplicate rows")

        parquet_filename = f"{file_date}.parquet"
        parquet_path = LOCAL_DIR / parquet_filename
        df.to_parquet(parquet_path, index=False, engine='pyarrow', compression='snappy')

        s3_key = f"{SILVER_REALIZED_PREFIX}/{parquet_filename}"
        _s3_upload(parquet_path, s3_key)

        print(f"  OK: {xlsx_filename} -> {s3_key} ({len(df)} rows, {len(df.columns)} cols)")
        return s3_key, len(df)

    except Exception as e:
        print(f"  FAIL: Error processing {xlsx_filename}: {e}")
        return None, 0


def incremental_realized_merge():
    """Process only new realized files, write to silver/realized/."""
    print("=" * 60)
    print(f"BD Realized Incremental Merge - {datetime.now().isoformat()}")
    print("=" * 60)

    manifest = load_realized_manifest()
    migrated = 'processed_etags' not in manifest and bool(manifest.get('processed_files'))
    processed_etags = _load_processed_etags(manifest)
    if migrated:
        print(f"  [realized] MIGRATION: legacy manifest ({len(processed_etags)} filenames, no "
              f"etags) -> etag-tracked; each reprocesses ONCE then etag-skips.")
    print(f"Previously processed: {len(processed_etags)} realized files (etag-tracked)")

    all_files = list_forwardfill_realized_files()
    target_files, cur_etags, counts = _select_target_files(
        "realized", FORWARDFILL_REALIZED_PREFIX, all_files, processed_etags)

    if not target_files:
        print(f"No new or re-landed realized files to process  "
              f"[SUMMARY realized: new=0 reprocess=0 skip={counts['skip']}]")
        return

    print(f"Found {len(target_files)} realized file(s) to process "
          f"(new={counts['new']} reprocess={counts['reprocess']} skip={counts['skip']})")
    print()

    total_rows = 0
    new_partitions = set(manifest.get('daily_partitions', []))
    failures = 0
    processed_dates = []

    for xlsx_file in target_files:
        s3_key, row_count = process_realized_xlsx_to_parquet(xlsx_file)
        if s3_key:
            processed_etags[xlsx_file] = cur_etags.get(xlsx_file) or _bronze_etag(FORWARDFILL_REALIZED_PREFIX, xlsx_file)
            new_partitions.add(s3_key)
            total_rows += row_count
            processed_dates.append(s3_key.split('/')[-1].replace('.parquet', ''))
        else:
            failures += 1

    manifest['processed_etags'] = processed_etags
    manifest['processed_files'] = sorted(processed_etags.keys())
    manifest['daily_partitions'] = list(new_partitions)
    manifest['last_updated'] = datetime.now(timezone.utc).isoformat()
    manifest['total_rows_estimate'] = manifest.get('total_rows_estimate', 0) + total_rows
    save_realized_manifest(manifest)

    max_data_date = max(processed_dates) if processed_dates else "(none)"
    print()
    print("=" * 60)
    print("REALIZED INCREMENTAL MERGE COMPLETE")
    print(f"  SUMMARY: {len(target_files)} processed | new={counts['new']} "
          f"reprocess={counts['reprocess']} skip={counts['skip']} | failures={failures} | "
          f"rows_added={total_rows:,} | max_data_date={max_data_date}")
    print("=" * 60)


# ============================================================================
# UNREALIZED INCREMENTAL PROCESSING
# Mirrors allocation processing but targets silver/unrealized/YYYY-MM-DD.parquet
# Deduplication key: (account_id, asset_name) -- daily snapshot, full replacement
# Unrealized is a SNAPSHOT -- each day's file is the complete picture
# ============================================================================

def load_unrealized_manifest():
    """Load unrealized incremental manifest from S3 (boto3-native)."""
    m = _s3_get_json(UNREALIZED_MANIFEST_KEY)
    if m is not None:
        return m
    return {
        'processed_files': [],
        'daily_partitions': [],
        'last_updated': None,
        'last_compaction': None,
        'total_rows_estimate': 0,
    }


def save_unrealized_manifest(manifest):
    """Save unrealized manifest to S3 (boto3-native)."""
    _s3_put_json(UNREALIZED_MANIFEST_KEY, manifest)


def list_forwardfill_unrealized_files():
    """List xlsx files in forwardfill_v2/unrealized/ (boto3-native)."""
    return _s3_list_names(FORWARDFILL_UNREALIZED_PREFIX, '.xlsx')


# Returned as the s3_key by process_unrealized_xlsx_to_parquet for a 0-data-row stub: a deliberate SKIP,
# not a failure (NFRA_MCPINDEX MX-s-16, row Z-S72).
_EMPTY_STUB = "__EMPTY_STUB__"


def process_unrealized_xlsx_to_parquet(xlsx_filename):
    """
    Process a single unrealized xlsx and save as parquet to silver/unrealized/YYYY-MM-DD.parquet.

    Unrealized files: UNREALIZED_DAILY_YYYY-MM-DD.xlsx
    Output: silver/unrealized/YYYY-MM-DD.parquet

    Unrealized is a daily SNAPSHOT -- each file is the full picture of open positions.
    Dedup key: (account_id, asset_name) -- one row per holding per account.

    Returns (s3_key, row_count) or (None, 0) on failure.
    """
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    xlsx_path = LOCAL_DIR / xlsx_filename
    s3_xlsx_key = f"{FORWARDFILL_UNREALIZED_PREFIX}/{xlsx_filename}"

    if not _s3_download(s3_xlsx_key, xlsx_path):
        print(f"  FAIL: Failed to download {xlsx_filename}")
        return None, 0

    try:
        df = pd.read_excel(xlsx_path, sheet_name='Sheet1')

        if len(df.columns) < UNREALIZED_MIN_COL_COUNT:
            print(f"  FAIL: {xlsx_filename}: only {len(df.columns)} cols "
                  f"(expected >= {UNREALIZED_MIN_COL_COUNT}) -- skipping")
            return None, 0

        # FRONTIER-SELECT robustness (ADVI_BREAKS TO-3, COO ruling 2026-06-30): BD emits the
        # freshest-date snapshot at T+N, so a latest-date file can be a 0-row stub (full header,
        # no data rows -- passes the col-count guard above). Skip it: do NOT write an empty silver
        # partition that would shadow the last good one. Keeps silver/unrealized always
        # latest-WITH-DATA; not marked processed, so it is re-checked until it lands data. Pairs
        # with the B_01 non-empty-unrealized resolve gate downstream.
        if len(df) == 0:
            print(f"  SKIP: {xlsx_filename}: 0 data rows (freshest-date-lag / empty stub) "
                  f"-- not writing an empty silver partition")
            return _EMPTY_STUB, 0

        df.columns = [to_snake_case(c) for c in df.columns]

        DATE_COLS = ['trade_date', 'settle_date', 'entry_date', 'return_date',
                     'start_date', 'account_create_date', 'performance_start_date',
                     'history_start_date', 'closed_date', 'as_of_date',
                     'purchase_date']
        for col in DATE_COLS:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

        df['_source_file'] = xlsx_filename
        df['_ingested_at'] = datetime.now(timezone.utc).isoformat()

        # Data date: read from BD Timestamps sheet (canonical), fall back to filename
        file_date = read_timestamps_date(xlsx_path)
        if file_date:
            print(f"    Data date from Timestamps sheet: {file_date}")
        else:
            import re
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', xlsx_filename)
            file_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
            print(f"    Data date from filename (Timestamps fallback): {file_date}")

        # BP-b-6: lot rows are built from the export BEFORE the legacy construction, and the measure
        # columns are dropped from the frame the legacy table is built from.
        lot_df, lot_before, lot_after = build_unrealized_lots(df)
        df = df.drop(columns=[c for c in LOT_MEASURE_COLS if c in df.columns])

        # Dedup by (account_id, asset_name) -- snapshot key
        dedup_cols = ['account_id', 'asset_name']
        available_dedup = [c for c in dedup_cols if c in df.columns]
        if len(available_dedup) >= 2:
            before = len(df)
            df = df.drop_duplicates(subset=available_dedup, keep='first')
            removed = before - len(df)
            if removed:
                print(f"    Removed {removed:,} duplicate rows")

        parquet_filename = f"{file_date}.parquet"
        parquet_path = LOCAL_DIR / parquet_filename
        df.to_parquet(parquet_path, index=False, engine='pyarrow', compression='snappy')

        s3_key = f"{SILVER_UNREALIZED_PREFIX}/{parquet_filename}"
        _s3_upload(parquet_path, s3_key)

        if lot_df is None:
            print("    SKIP: unrealized_lots -- export carries no Units/Cost Basis measure (template not switched on)")
        else:
            lot_uri = lot_address(file_date)
            if lot_uri is None:
                print("    FAIL: unrealized_lots -- naming builder not importable; lot table NOT written")
            else:
                lot_path = LOCAL_DIR / f"lots_{file_date}.parquet"
                lot_df.to_parquet(lot_path, index=False, engine='pyarrow', compression='snappy')
                if _s3_upload_addr(lot_path, lot_uri):
                    print(f"    OK: unrealized_lots -> {lot_uri} ({lot_before:,} lot rows in, "
                          f"{lot_after:,} lots after lot-key dedup)")
                else:
                    print(f"    FAIL: unrealized_lots upload to {lot_uri}")

        print(f"  OK: {xlsx_filename} -> {s3_key} ({len(df)} rows, {len(df.columns)} cols)")
        return s3_key, len(df)

    except Exception as e:
        print(f"  FAIL: Error processing {xlsx_filename}: {e}")
        return None, 0


def incremental_unrealized_merge():
    """Process only new unrealized files, write to silver/unrealized/."""
    print("=" * 60)
    print(f"BD Unrealized Incremental Merge - {datetime.now().isoformat()}")
    print("=" * 60)

    manifest = load_unrealized_manifest()
    migrated = 'processed_etags' not in manifest and bool(manifest.get('processed_files'))
    processed_etags = _load_processed_etags(manifest)
    if migrated:
        print(f"  [unrealized] MIGRATION: legacy manifest ({len(processed_etags)} filenames, no "
              f"etags) -> etag-tracked; each reprocesses ONCE then etag-skips.")
    print(f"Previously processed: {len(processed_etags)} unrealized files (etag-tracked)")

    all_files = list_forwardfill_unrealized_files()
    target_files, cur_etags, counts = _select_target_files(
        "unrealized", FORWARDFILL_UNREALIZED_PREFIX, all_files, processed_etags)

    if not target_files:
        print(f"No new or re-landed unrealized files to process  "
              f"[SUMMARY unrealized: new=0 reprocess=0 skip={counts['skip']}]")
        return

    print(f"Found {len(target_files)} unrealized file(s) to process "
          f"(new={counts['new']} reprocess={counts['reprocess']} skip={counts['skip']})")
    print()

    total_rows = 0
    new_partitions = set(manifest.get('daily_partitions', []))
    failures = 0
    processed_dates = []

    empty_stubs = 0
    for xlsx_file in target_files:
        s3_key, row_count = process_unrealized_xlsx_to_parquet(xlsx_file)
        if s3_key == _EMPTY_STUB:
            # 0-data-row stub (BD freshest-date lag / empty template): a deliberate SKIP. Record the
            # etag so it is not re-listed NEW (and counted a failure) on every run; NO partition is
            # written. A later re-land with data changes the etag -> reprocessed. (Row Z-S72.)
            processed_etags[xlsx_file] = cur_etags.get(xlsx_file) or _bronze_etag(FORWARDFILL_UNREALIZED_PREFIX, xlsx_file)
            empty_stubs += 1
        elif s3_key:
            processed_etags[xlsx_file] = cur_etags.get(xlsx_file) or _bronze_etag(FORWARDFILL_UNREALIZED_PREFIX, xlsx_file)
            new_partitions.add(s3_key)
            total_rows += row_count
            processed_dates.append(s3_key.split('/')[-1].replace('.parquet', ''))
        else:
            failures += 1

    manifest['processed_etags'] = processed_etags
    manifest['processed_files'] = sorted(processed_etags.keys())
    manifest['daily_partitions'] = list(new_partitions)
    manifest['last_updated'] = datetime.now(timezone.utc).isoformat()
    manifest['total_rows_estimate'] = manifest.get('total_rows_estimate', 0) + total_rows
    save_unrealized_manifest(manifest)

    max_data_date = max(processed_dates) if processed_dates else "(none)"
    print()
    print("=" * 60)
    print("UNREALIZED INCREMENTAL MERGE COMPLETE")
    print(f"  SUMMARY: {len(target_files)} processed | new={counts['new']} "
          f"reprocess={counts['reprocess']} skip={counts['skip']} | failures={failures} | "
          f"rows_added={total_rows:,} | max_data_date={max_data_date} | "
          f"empty_stub={empty_stubs}")
    print("=" * 60)


# ============================================================================
# INVOCATION CONTRACT (ADVI_BDAPIMIG D2b) -- the bd-silver-merge Lambda / SSM / one-shot entry
# ============================================================================

# Canonical order -- transactions first so its bd-price-update trigger fires before the snapshots.
_MERGE_ORDER = ['transactions', 'allocations', 'realized', 'unrealized']
_TABLE_MERGES = {
    'transactions': incremental_merge,
    'allocations': incremental_alloc_merge,
    'realized': incremental_realized_merge,
    'unrealized': incremental_unrealized_merge,
}


def run(tables=None):
    """Programmatic entry -- the bd-silver-merge Lambda / SSM / one-shot all invoke this (boto3-native,
    no aws-cli). `tables` = a list of table names (subset of transactions/allocations/realized/
    unrealized) or None / ['all'] = all 4, run in canonical order with per-table isolation.

    STEADY-STATE ON LAMBDA ONLY (1-5 new/changed files/table). The one-time first-run reprocess-once
    reconcile (the etag migration reprocesses EVERY current forwardfill xlsx -> minutes) must run OUT
    of the nightly Lambda path -- `python merge-daily-incremental.py --all` on SSM/local, or a bounded
    batch -- to dodge the Lambda 15-min cap. Returns {table: 'ok' | 'error: <msg>'}."""
    if not tables or (len(tables) == 1 and str(tables[0]).lower() == 'all'):
        selected = list(_MERGE_ORDER)
    else:
        want = {str(t).lower() for t in tables}
        selected = [t for t in _MERGE_ORDER if t in want]
    results = {}
    for t in selected:
        try:
            _TABLE_MERGES[t]()
            results[t] = 'ok'
        except Exception as e:  # noqa: BLE001 -- per-table isolation; one table must not sink the rest
            print(f"  ERROR: {t} merge failed: {e}")
            results[t] = f'error: {e}'
    return results


def lambda_handler(event, context):  # noqa: ARG001 -- AWS Lambda signature
    """bd-silver-merge Lambda entry (fired by the opal-data-bd bronze-complete EventBridge rule).

    EVENT CONTRACT: {"tables": ["all"]} (default = all 4) or a subset e.g. {"tables": ["transactions"]};
    an absent/empty event -> all 4. Firm-sep: reads BD_S3_BUCKET (opal-data-bd) only; no cot path.
    Raises on any table failure so the invocation is VISIBLY failed (CW + the per-table absence alarm
    are the durable signal)."""
    event = event or {}
    tables = event.get('tables')
    print(f"bd-silver-merge invoked {datetime.now(timezone.utc).isoformat()} "
          f"tables={tables or 'all'} bucket={S3_BUCKET}")
    results = run(tables)
    print(f"RESULT: {results}")
    failed = [t for t, r in results.items() if r != 'ok']
    if failed:
        raise RuntimeError(f"bd-silver-merge: {len(failed)} table(s) failed: {failed}")
    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='BD Incremental Silver Layer Merge')
    parser.add_argument('--compact', action='store_true',
                        help='Run weekly compaction for transactions')
    parser.add_argument('--allocations', action='store_true',
                        help='Process allocation files (silver/allocations/)')
    parser.add_argument('--realized', action='store_true',
                        help='Process realized capital gains files (silver/realized/)')
    parser.add_argument('--unrealized', action='store_true',
                        help='Process unrealized capital gains files (silver/unrealized/)')
    parser.add_argument('--all', action='store_true',
                        help='Process transactions, allocations, realized, and unrealized')
    args = parser.parse_args()

    if args.compact:
        compact_silver_layer()
    elif args.allocations:
        incremental_alloc_merge()
    elif args.realized:
        incremental_realized_merge()
    elif args.unrealized:
        incremental_unrealized_merge()
    elif args.all:
        incremental_merge()
        incremental_alloc_merge()
        incremental_realized_merge()
        incremental_unrealized_merge()
    else:
        # Default: transactions only (preserves existing behaviour)
        incremental_merge()


if __name__ == "__main__":
    main()
