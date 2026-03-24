#!/usr/bin/env python3
"""
Inject Scoped Price Overrides into canonical_prices.parquet

Adds a scoped section of manually-derived prices for assets that cannot be
priced through the standard Yahoo Finance / interpolation pipeline. These are
structured notes, model portfolio sleeves, and private funds where the
asset_name in the positions cube resolves to a wrong public ticker.

Prices are derived by reverse-engineering silver allocations (BD's own reported
account_market_value) against correctly-priced positions in the same account.
See DS session log 2026-03-17 for full methodology.

Source tag: 'scoped_override' -- distinguishable from all other sources in
canonical_prices. The 05_build_client_performance.py pipeline treats these
identically to any other price source; no code changes needed downstream.

IMPORTANT: The single source of truth for override prices and tickers is
_SCOPED_PRICE_OVERRIDES in bd_price_update.py. This script reads from that
list. Inception dates (needed only for historical backfill) are maintained
here in _INCEPTION_DATES. To add a new override: add it to bd_price_update.py
first, then add the inception_date here, then run this script.

bd_price_update.py enforces overrides inline on every daily run, so new dates
are always covered. This script is only needed for HISTORICAL BACKFILL of
override rows into canonical_prices (e.g., after adding a new override asset).

Process:
  1. Reads current canonical_prices.parquet from S3
  2. Removes any existing 'scoped_override' rows (idempotent)
  3. Generates daily price rows for each overridden asset from inception to latest date
  4. Appends to canonical_prices and re-uploads

Usage:
    python inject_scoped_overrides.py --dry-run     # show what would change
    python inject_scoped_overrides.py --upload       # inject and upload

Author: 0.4.0_DS_ClientPlatform
Date: 2026-03-17 (updated 2026-03-19: reads from bd_price_update.py)
"""

import argparse
import io
import sys
from datetime import datetime, timezone

import boto3
import pandas as pd
import numpy as np

S3_BUCKET = "opal-data-bd"
CANONICAL_KEY = "silver/prices/canonical_prices.parquet"
SOURCE_TAG = "scoped_override"

s3 = boto3.client("s3", region_name="us-east-1")

# ============================================================================
# SCOPED OVERRIDE REGISTRY
#
# Each entry generates a flat daily price row from inception_date through
# the latest date in canonical_prices. The ticker field is a synthetic ID
# (not a real ticker) to prevent confusion with public instruments.
#
# To add a new override:
#   1. Run the reverse-engineering analysis to derive the per-unit price
#   2. Add an entry below with the exact asset_name from positions_cube
#   3. Run this script with --upload
# ============================================================================

# Import the canonical override list from bd_price_update.py (single source of truth)
from bd_price_update import _SCOPED_PRICE_OVERRIDES

# Inception dates for historical backfill — only needed by this script, not by
# bd_price_update.py (which only writes the current target_date).
_INCEPTION_DATES = {
    "Waldrop Donor Advised Fund":               "2023-09-13",
    "BNP PARIBAS SA":                           "2024-12-06",
    "DESTINATIONS LARGE CAP EQUITY I":          "2025-10-02",
    "DESTINATIONS INTERNATIONAL EQUITY I":      "2025-10-02",
    "JPMORGAN CHASE FINL CO LLC 0% 02/14/2029": "2024-04-10",
}

# Build the OVERRIDES list expected by generate_override_rows()
OVERRIDES = []
for entry in _SCOPED_PRICE_OVERRIDES:
    inception = _INCEPTION_DATES.get(entry["asset_name"])
    if not inception:
        print(f"WARNING: no inception_date for {entry['asset_name']} -- skipping")
        continue
    OVERRIDES.append({
        "asset_name": entry["asset_name"],
        "ticker": entry["ticker"],
        "price": entry["price"],
        "inception_date": inception,
    })


def load_canonical() -> pd.DataFrame:
    """Load current canonical_prices from S3."""
    print("Loading canonical_prices.parquet...")
    resp = s3.get_object(Bucket=S3_BUCKET, Key=CANONICAL_KEY)
    df = pd.read_parquet(io.BytesIO(resp["Body"].read()))
    df["date"] = pd.to_datetime(df["date"])
    print(f"  {len(df):,} rows, {df['asset_name'].nunique():,} assets, "
          f"{df['date'].min().date()} to {df['date'].max().date()}")
    return df


def generate_override_rows(latest_date: pd.Timestamp) -> pd.DataFrame:
    """Generate daily price rows for all scoped overrides."""
    all_rows = []

    for ovr in OVERRIDES:
        inception = pd.Timestamp(ovr["inception_date"])
        # Generate one row per business day from inception to latest_date
        dates = pd.bdate_range(start=inception, end=latest_date)

        rows = pd.DataFrame({
            "date": dates,
            "asset_name": ovr["asset_name"],
            "ticker": ovr["ticker"],
            "price": ovr["price"],
            "source": SOURCE_TAG,
        })
        all_rows.append(rows)
        print(f"  {ovr['asset_name'][:50]:50s}: {len(rows):>5,} rows @ ${ovr['price']:.2f}/unit "
              f"({inception.date()} to {latest_date.date()})")

    return pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()


def inject(df: pd.DataFrame, overrides: pd.DataFrame) -> pd.DataFrame:
    """
    Remove existing scoped_override rows, then remove any rows for overridden
    asset_names (to prevent the wrong canonical price from being used), then
    append the new override rows.
    """
    override_assets = set(overrides["asset_name"].unique())

    # Count what we're removing
    existing_scoped = df[df["source"] == SOURCE_TAG]
    existing_wrong = df[(df["asset_name"].isin(override_assets)) & (df["source"] != SOURCE_TAG)]

    print(f"\n  Removing {len(existing_scoped):,} existing scoped_override rows")
    print(f"  Removing {len(existing_wrong):,} wrong-source rows for overridden assets:")
    for asset in sorted(override_assets):
        wrong = existing_wrong[existing_wrong["asset_name"] == asset]
        if not wrong.empty:
            sources = wrong["source"].unique().tolist()
            print(f"    {asset[:50]:50s}: {len(wrong):>5,} rows (sources: {sources})")

    # Remove both scoped_override rows AND wrong-source rows for overridden assets
    keep_mask = (df["source"] != SOURCE_TAG) & (~df["asset_name"].isin(override_assets))
    cleaned = df[keep_mask].copy()

    # Append new overrides
    result = pd.concat([cleaned, overrides], ignore_index=True)
    result = result.sort_values(["date", "asset_name"]).reset_index(drop=True)

    print(f"\n  Before: {len(df):,} rows")
    print(f"  After:  {len(result):,} rows (net {len(result) - len(df):+,})")

    return result


def save(df: pd.DataFrame, upload: bool):
    """Save canonical_prices back to S3."""
    buf = io.BytesIO()
    df.to_parquet(buf, index=False, engine="pyarrow", compression="snappy")
    size_mb = buf.tell() / (1024 * 1024)

    if upload:
        buf.seek(0)
        s3.put_object(Bucket=S3_BUCKET, Key=CANONICAL_KEY, Body=buf.read())
        print(f"\n  Uploaded to s3://{S3_BUCKET}/{CANONICAL_KEY} ({size_mb:.1f} MB)")
    else:
        print(f"\n  [DRY RUN] Would upload to s3://{S3_BUCKET}/{CANONICAL_KEY} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Inject scoped price overrides into canonical_prices")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change, no upload")
    parser.add_argument("--upload", action="store_true", help="Inject and upload to S3")
    args = parser.parse_args()

    print("=" * 70)
    print("INJECT SCOPED PRICE OVERRIDES")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Load
    df = load_canonical()
    latest_date = df["date"].max()

    # Generate
    print(f"\nGenerating override rows (through {latest_date.date()}):")
    overrides = generate_override_rows(latest_date)
    print(f"  Total: {len(overrides):,} override rows for {len(OVERRIDES)} assets")

    # Inject
    print("\nInjecting:")
    result = inject(df, overrides)

    # Verify
    print("\nVerification:")
    scoped = result[result["source"] == SOURCE_TAG]
    print(f"  scoped_override rows in output: {len(scoped):,}")
    for asset in sorted(scoped["asset_name"].unique()):
        subset = scoped[scoped["asset_name"] == asset]
        print(f"    {asset[:50]:50s}: {len(subset):>5,} rows, "
              f"price=${subset['price'].iloc[0]:.2f}, "
              f"{subset['date'].min().date()} to {subset['date'].max().date()}")

    # Check no duplicate (date, asset_name) entries
    dupes = result.groupby(["date", "asset_name"]).size()
    dupes = dupes[dupes > 1]
    if len(dupes) > 0:
        print(f"\n  WARNING: {len(dupes)} duplicate (date, asset_name) entries found!")
        print(dupes.head(10))
    else:
        print(f"  No duplicate (date, asset_name) entries -- clean")

    # Save
    save(result, upload=args.upload and not args.dry_run)

    print(f"\nCompleted: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
