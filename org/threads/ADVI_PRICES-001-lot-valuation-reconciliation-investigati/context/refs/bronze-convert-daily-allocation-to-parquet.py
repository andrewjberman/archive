#!/usr/bin/env python3
"""
Convert Daily Allocation XLSX to Parquet

Takes the most recent ALLOC_DAILY_*.xlsx file from forwardfill_v2/allocations/
and converts it to parquet in silver/daily_allocations/

This runs as part of the EC2 daily ETL pipeline.

Usage:
    python3 convert_daily_allocation_to_parquet.py

Environment:
    AWS credentials configured (EC2 role)

Exit codes:
    0 - Success
    1 - No new file to process
    2 - Processing error
"""

import pandas as pd
import boto3
import sys
from datetime import datetime
from pathlib import Path

S3_BUCKET = 'opal-data-bd'
SOURCE_PREFIX = 'forwardfill_v2/allocations'
TARGET_PREFIX = 'silver/daily_allocations'

s3 = boto3.client('s3')

def find_latest_alloc_daily_file():
    """Find the most recent ALLOC_DAILY_*.xlsx file."""
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f'{SOURCE_PREFIX}/')

    alloc_files = []
    for obj in response.get('Contents', []):
        key = obj['Key']
        if 'ALLOC_DAILY_' in key and key.endswith('.xlsx'):
            alloc_files.append((key, obj['LastModified']))

    if not alloc_files:
        return None

    # Sort by last modified, return most recent
    alloc_files.sort(key=lambda x: x[1], reverse=True)
    return alloc_files[0][0]

def check_if_already_processed(date_str):
    """Check if this date has already been processed."""
    year_month = '-'.join(date_str.split('-')[:2])
    parquet_key = f'{TARGET_PREFIX}/{year_month}/ALLOC_DAILY_{date_str}.parquet'

    try:
        s3.head_object(Bucket=S3_BUCKET, Key=parquet_key)
        return True
    except:
        return False

def main():
    print("=" * 60)
    print("Daily Allocation XLSX → Parquet Conversion")
    print("=" * 60)

    # Find latest file
    latest_file = find_latest_alloc_daily_file()
    if not latest_file:
        print("No ALLOC_DAILY files found in S3")
        sys.exit(1)

    print(f"\nLatest file: {latest_file}")

    # Extract date from filename
    filename = Path(latest_file).stem
    date_str = filename.split('_')[-1]  # "2026-01-28"
    year_month = '-'.join(date_str.split('-')[:2])  # "2026-01"

    print(f"Date: {date_str}")
    print(f"Year-Month: {year_month}")

    # Check if already processed
    if check_if_already_processed(date_str):
        print(f"\n✓ Already processed - parquet exists for {date_str}")
        sys.exit(0)

    # Download XLSX
    print(f"\nDownloading from S3...")
    local_file = f'/tmp/{Path(latest_file).name}'
    s3.download_file(S3_BUCKET, latest_file, local_file)
    print(f"  ✓ Downloaded to {local_file}")

    # Read Excel
    print(f"\nReading Excel file...")
    df = pd.read_excel(local_file)
    print(f"  Initial rows: {len(df):,}")

    # Deduplicate by AccountID
    if 'AccountID' in df.columns:
        df_dedup = df.drop_duplicates(subset=['AccountID'], keep='last')
        print(f"  After deduplication: {len(df_dedup):,} rows")
    else:
        df_dedup = df
        print("  Warning: No AccountID column - skipping deduplication")

    # Standardize column names
    df_dedup.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df_dedup.columns]
    print(f"  Columns standardized")

    # Convert ID columns to strings
    id_columns = ['relationship_id', 'portfolio_id', 'accountid', 'account_number', 'account_id']
    for col in id_columns:
        if col in df_dedup.columns:
            df_dedup[col] = df_dedup[col].astype(str)
            print(f"  Converted {col} to string")

    # Rename accountid to account_id
    if 'accountid' in df_dedup.columns:
        df_dedup = df_dedup.rename(columns={'accountid': 'account_id'})
        print(f"  Renamed accountid → account_id")

    # Save as parquet
    parquet_file = f'/tmp/ALLOC_DAILY_{date_str}.parquet'
    df_dedup.to_parquet(parquet_file, index=False)
    print(f"\n  Saved to {parquet_file}")

    # Upload to silver
    output_key = f'{TARGET_PREFIX}/{year_month}/ALLOC_DAILY_{date_str}.parquet'
    s3.upload_file(parquet_file, S3_BUCKET, output_key)
    print(f"  ✓ Uploaded to s3://{S3_BUCKET}/{output_key}")

    # Calculate AUM
    aum = 0
    if 'account_market_value' in df_dedup.columns:
        aum = df_dedup['account_market_value'].sum()

    print("\n" + "=" * 60)
    print(f"SUCCESS: Processed {len(df_dedup):,} accounts for {date_str}")
    print(f"Total AUM: ${aum:,.0f}")
    print("=" * 60)

    sys.exit(0)

if __name__ == '__main__':
    main()
