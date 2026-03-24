#!/usr/bin/env python3
"""
Incremental Daily Allocation Merge - Smart Append-Only

Instead of rebuilding the entire allocation silver parquet daily, this script:
1. Reads ONLY the new daily xlsx from forwardfill_v2/allocations/
2. Converts to parquet and saves to silver/allocations/YYYY-MM-DD.parquet
3. Never touches old data - true incremental append

The silver layer structure:
  - silver/allocations/YYYY-MM-DD.parquet  (daily incremental files)
  - silver/bd_allocations.parquet  (compacted view - rebuilt weekly)

Reading the silver layer:
  pd.read_parquet('s3://opal-data-bd/silver/allocations/')  # reads all partitions

NOTE: This standalone script is DEPRECATED. The unified merge-daily-incremental.py
with --allocations flag is the preferred path. SSM allocation doc should invoke that instead.

Usage:
    python3 merge-daily-allocation-incremental.py
    python3 merge-daily-allocation-incremental.py --compact  # weekly compaction
"""

import subprocess
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Install pandas if needed
try:
    import pandas as pd
except ImportError:
    print("Installing pandas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "pyarrow", "openpyxl", "-q"])
    import pandas as pd

# Configuration
S3_BUCKET = "opal-data-bd"
FORWARDFILL_PREFIX = "forwardfill_v2/allocations"
SILVER_DAILY_PREFIX = "silver/allocations"  # Flat structure (reorganized 2026-02-17)
SILVER_COMPACTED_KEY = "silver/bd_allocations.parquet"
MANIFEST_KEY = "silver/allocation_incremental_manifest.json"
LOCAL_DIR = Path("/tmp/bd-alloc-incremental")


def run_cmd(cmd):
    """Run shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


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
    """Load incremental manifest from S3."""
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = LOCAL_DIR / "manifest.json"

    result = subprocess.run(
        f"aws s3 cp s3://{S3_BUCKET}/{MANIFEST_KEY} {manifest_path} 2>/dev/null",
        shell=True, capture_output=True
    )

    if result.returncode == 0:
        with open(manifest_path) as f:
            return json.load(f)
    return {
        'processed_files': [],
        'daily_partitions': [],
        'last_updated': None,
        'last_compaction': None,
        'total_rows_estimate': 0
    }


def save_manifest(manifest):
    """Save manifest to S3."""
    manifest_path = LOCAL_DIR / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    subprocess.run(
        f"aws s3 cp {manifest_path} s3://{S3_BUCKET}/{MANIFEST_KEY}",
        shell=True, capture_output=True
    )


def list_forwardfill_files():
    """List xlsx files in forwardfill_v2/allocations/."""
    output = run_cmd(f"aws s3 ls s3://{S3_BUCKET}/{FORWARDFILL_PREFIX}/ | grep xlsx | awk '{{print $4}}'")
    if output:
        return [f for f in output.split('\n') if f]
    return []


def process_xlsx_to_parquet(xlsx_filename):
    """
    Process a single allocation xlsx file and save as parquet to silver/daily_allocations/YYYY-MM/.
    Returns (partition_key, row_count) or (None, 0) on failure.
    """
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    # Download xlsx
    xlsx_path = LOCAL_DIR / xlsx_filename
    s3_xlsx_key = f"{FORWARDFILL_PREFIX}/{xlsx_filename}"

    result = subprocess.run(
        f"aws s3 cp s3://{S3_BUCKET}/{s3_xlsx_key} {xlsx_path}",
        shell=True, capture_output=True
    )

    if result.returncode != 0:
        print(f"  ✗ Failed to download {xlsx_filename}")
        return None, 0

    try:
        df = pd.read_excel(xlsx_path, sheet_name='Sheet1')

        # Normalize columns
        df.columns = [to_snake_case(c) for c in df.columns]

        # Convert mixed-type object columns to strings for pyarrow compatibility.
        # Preserve nulls as None — do NOT return float NaN or empty string for null values.
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

        # Parse date columns
        date_cols = ['as_of_date', 'start_date', 'trade_date', 'settle_date',
                     'entry_date', 'return_date', 'history_start_date',
                     'closed_date', 'performance_start_date', 'account_create_date',
                     'relationship_termination_date', 'relationship_inception_date']

        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Add metadata
        df['_source_file'] = xlsx_filename
        df['_ingested_at'] = datetime.now(timezone.utc).isoformat()

        # Determine partition (YYYY-MM based on filename or as_of_date)
        # Filename format: ALLOC_DAILY_YYYY-MM-DD.xlsx where date is DATA DATE (prior trading day)
        # Extract date from filename for flat structure (YYYY-MM-DD)
        try:
            import re
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', xlsx_filename)
            if date_match:
                file_date = date_match.group(1)  # Full YYYY-MM-DD
            elif 'as_of_date' in df.columns and not df['as_of_date'].isna().all():
                most_common_date = df['as_of_date'].mode()[0]
                file_date = most_common_date.strftime('%Y-%m-%d')
            else:
                file_date = datetime.now().strftime('%Y-%m-%d')
        except:
            file_date = datetime.now().strftime('%Y-%m-%d')

        # Deduplicate by (account_id, as_of_date) if both columns exist
        if 'account_id' in df.columns and 'as_of_date' in df.columns:
            before = len(df)
            df = df.drop_duplicates(subset=['account_id', 'as_of_date'], keep='last')
            after = len(df)
            if before != after:
                print(f"    Deduped: {before} -> {after} rows")

        # Save as parquet with simple date naming (flat structure, no month subdirs)
        parquet_filename = f"{file_date}.parquet"
        parquet_path = LOCAL_DIR / parquet_filename
        df.to_parquet(parquet_path, index=False, engine='pyarrow', compression='snappy')

        # Upload to silver/daily/allocations/ (flat structure)
        s3_parquet_key = f"{SILVER_DAILY_PREFIX}/{parquet_filename}"
        subprocess.run(
            f"aws s3 cp {parquet_path} s3://{S3_BUCKET}/{s3_parquet_key}",
            shell=True, capture_output=True
        )

        print(f"  ✓ {xlsx_filename} -> {s3_parquet_key} ({len(df)} rows)")
        return s3_parquet_key, len(df)

    except Exception as e:
        print(f"  ✗ Error processing {xlsx_filename}: {e}")
        return None, 0


def incremental_merge():
    """Process only new files, append to daily partitions."""
    print("=" * 60)
    print(f"BD Allocation Incremental Merge - {datetime.now().isoformat()}")
    print("=" * 60)

    manifest = load_manifest()
    processed = set(manifest.get('processed_files', []))
    print(f"Previously processed: {len(processed)} files")

    # List new files
    all_files = list_forwardfill_files()
    new_files = [f for f in all_files if f not in processed]

    if not new_files:
        print("No new files to process")
        return

    print(f"Found {len(new_files)} new files")
    print()

    # Process each new file
    total_rows = 0
    new_partitions = set(manifest.get('daily_partitions', []))

    for xlsx_file in new_files:
        partition_key, row_count = process_xlsx_to_parquet(xlsx_file)
        if partition_key:
            processed.add(xlsx_file)
            new_partitions.add(partition_key)
            total_rows += row_count

    # Update manifest
    manifest['processed_files'] = list(processed)
    manifest['daily_partitions'] = list(new_partitions)
    manifest['last_updated'] = datetime.now(timezone.utc).isoformat()
    manifest['total_rows_estimate'] = manifest.get('total_rows_estimate', 0) + total_rows
    save_manifest(manifest)

    print()
    print("=" * 60)
    print(f"INCREMENTAL MERGE COMPLETE")
    print(f"  New files processed: {len(new_files)}")
    print(f"  Rows added: {total_rows}")
    print(f"  Total partitions: {len(new_partitions)}")
    print("=" * 60)


def compact_silver_layer():
    """
    Weekly compaction: Read all daily partitions, dedupe, write single parquet.
    Run this on a schedule (weekly) to maintain query performance.
    """
    print("=" * 60)
    print(f"BD Allocation Silver Layer Compaction - {datetime.now().isoformat()}")
    print("=" * 60)

    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    # List all parquet files in silver/daily_allocations/
    output = run_cmd(f"aws s3 ls s3://{S3_BUCKET}/{SILVER_DAILY_PREFIX}/ --recursive | grep parquet | awk '{{print $4}}'")

    if not output:
        print("No daily partitions to compact")
        return

    parquet_files = [f for f in output.split('\n') if f]
    print(f"Found {len(parquet_files)} daily parquet files")

    # Download and combine
    dfs = []
    for pq_key in parquet_files:
        local_path = LOCAL_DIR / Path(pq_key).name
        subprocess.run(
            f"aws s3 cp s3://{S3_BUCKET}/{pq_key} {local_path}",
            shell=True, capture_output=True
        )
        try:
            df = pd.read_parquet(local_path)
            dfs.append(df)
            print(f"  Read {pq_key}: {len(df)} rows")
        except Exception as e:
            print(f"  ✗ Failed to read {pq_key}: {e}")

    if not dfs:
        print("No data to compact")
        return

    # Combine and dedupe
    combined = pd.concat(dfs, ignore_index=True)
    before = len(combined)

    # Deduplicate by (account_id, as_of_date) if both columns exist
    if 'account_id' in combined.columns and 'as_of_date' in combined.columns:
        combined = combined.drop_duplicates(subset=['account_id', 'as_of_date'], keep='last')

    after = len(combined)
    print(f"\nCombined: {before} -> {after} rows (deduped)")

    # Save compacted parquet
    compacted_path = LOCAL_DIR / "bd_allocations_compacted.parquet"
    combined.to_parquet(compacted_path, index=False, engine='pyarrow', compression='snappy')

    file_size_mb = compacted_path.stat().st_size / (1024 * 1024)
    print(f"Compacted size: {file_size_mb:.1f} MB")

    # Upload
    subprocess.run(
        f"aws s3 cp {compacted_path} s3://{S3_BUCKET}/{SILVER_COMPACTED_KEY}",
        shell=True
    )
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


def main():
    parser = argparse.ArgumentParser(description='BD Allocation Incremental Silver Layer Merge')
    parser.add_argument('--compact', action='store_true', help='Run weekly compaction')
    args = parser.parse_args()

    if args.compact:
        compact_silver_layer()
    else:
        incremental_merge()


if __name__ == "__main__":
    main()
