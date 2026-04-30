"""ADVI_INFLEC.DIAGFIX.010 Phase 2 — bronze/orion-api-v2 -> silver/api_dims/assets_v2.

Reads bronze/orion-api-v2/{date}/assets.parquet (Phase 1 output from
data/orion/manual_api/pull_inflection_assets_v2.py) and writes silver in
Hive-partitioned format used by other silver dims:

    silver/api_dims/assets_v2/snapshot_date={date}/data.parquet

Schema preserves all 58 source columns from the Orion REST API. Field names
normalized from camelCase (API) to snake_case (silver convention). Types coerced:
  - currentValue / currentPrice / currentShares / costBasis / assetPercentOfAccount: float
  - integer IDs (accountId / clientId / productId / etc.): pandas nullable Int64
  - boolean flags (isManaged / isActive / etc.): bool
  - dates (createdDate / editedDate / asOfDate / lastReconDate): datetime64
  - everything else: string

The transformation is mechanical (no aggregation, no joins). Per CLAUDE.md Rule 15
the script begins with `from __future__ import annotations`.

Usage:
  python3 convert_assets_v2_to_silver.py --upload
  python3 convert_assets_v2_to_silver.py --date 2026-04-29 --dry-run

Author: 0.4.0_DS_ClientPlatform
Project: ADVI_INFLEC.DIAGFIX.010
Date: 2026-04-29
"""
from __future__ import annotations

import argparse
import re
import sys
import traceback
from datetime import datetime, timezone
from io import BytesIO

import boto3
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

S3_BUCKET = "opal-data-inf"
BRONZE_KEY_TPL = "bronze/assets/{snap}.parquet"
SILVER_KEY_TPL = "silver/assets_v2/{snap}.parquet"

# Field-type buckets.
INT_FIELDS = {
    "id", "accountId", "accountStatusId", "clientId", "productId",
    "registrationId", "status", "assetLevelStrategyId",
}
FLOAT_FIELDS = {
    "currentShares", "currentValue", "currentPrice", "costBasis",
    "assetPercentOfAccount", "excludeAmount",
}
BOOL_FIELDS = {
    "isManaged", "isCustodialCash", "is13FReportable", "isActive",
    "isAdvReportable", "isFeeExcluded", "excludeFromMargin",
    "isGlobalExcluded", "isDataSharingEntity", "isAdvisorOnly",
    "isOrionVision", "isRebalance", "isStrategyOverride",
}
DATE_FIELDS = {
    "asOfDate", "createdDate", "editedDate", "lastReconDate",
}

s3 = boto3.client("s3", region_name="us-east-1")


def _log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def _camel_to_snake(name: str) -> str:
    """accountId -> account_id, productCategoryAbbreviation -> product_category_abbreviation."""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def _read_bronze(snap_iso: str) -> pd.DataFrame:
    key = BRONZE_KEY_TPL.format(snap=snap_iso)
    _log(f"Reading bronze: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(obj["Body"].read()))


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Apply type coercions per the field-bucket map. Mutates a copy of df."""
    out = df.copy()

    for f in INT_FIELDS:
        if f in out.columns:
            out[f] = pd.to_numeric(out[f], errors="coerce").astype("Int64")

    for f in FLOAT_FIELDS:
        if f in out.columns:
            out[f] = pd.to_numeric(out[f], errors="coerce").astype("float64")

    for f in BOOL_FIELDS:
        if f in out.columns:
            # JSON booleans round-trip cleanly; nulls become NA which is fine for nullable bool
            out[f] = out[f].astype("boolean")

    for f in DATE_FIELDS:
        if f in out.columns:
            # Errors -> NaT; keeps timezone if present in the source
            out[f] = pd.to_datetime(out[f], errors="coerce", utc=True)

    # Everything not yet typed: cast to string (preserve nulls)
    typed = INT_FIELDS | FLOAT_FIELDS | BOOL_FIELDS | DATE_FIELDS
    for c in out.columns:
        if c not in typed:
            # Use pandas string dtype (nullable). object -> StringDtype keeps nulls as <NA>.
            out[c] = out[c].astype("string")

    return out


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """camelCase -> snake_case. accountId -> account_id, etc."""
    rename_map = {c: _camel_to_snake(c) for c in df.columns}
    return df.rename(columns=rename_map)


def _add_partition_column(df: pd.DataFrame, snap_iso: str) -> pd.DataFrame:
    """Add a snapshot_date column for explicit lineage at row level."""
    out = df.copy()
    out["snapshot_date"] = pd.to_datetime(snap_iso).date()
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None,
                        help="Snapshot date YYYY-MM-DD. Default: today UTC.")
    parser.add_argument("--upload", action="store_true",
                        help="Write silver parquet to S3.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute only, no write.")
    args = parser.parse_args(argv)
    if not args.upload and not args.dry_run:
        parser.error("one of --upload or --dry-run is required")

    if args.date:
        snap_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        snap_date = datetime.now(timezone.utc).date()
    snap_iso = snap_date.isoformat()
    _log(f"Snapshot: {snap_iso}")

    df = _read_bronze(snap_iso)
    _log(f"Bronze rows: {len(df):,} | columns: {len(df.columns)}")

    df_typed = _coerce_types(df)
    df_renamed = _normalize_columns(df_typed)
    df_final = _add_partition_column(df_renamed, snap_iso)

    # Sanity diagnostics
    asset_class_col = "asset_class"
    product_cat_col = "product_category"
    null_ac = df_final[asset_class_col].isna().sum() if asset_class_col in df_final.columns else len(df_final)
    null_pc = df_final[product_cat_col].isna().sum() if product_cat_col in df_final.columns else len(df_final)
    total_mv = float(df_final["current_value"].fillna(0).sum()) if "current_value" in df_final.columns else 0.0
    _log(f"Coverage: asset_class null={null_ac:,} | product_category null={null_pc:,}")
    _log(f"Total current_value: ${total_mv:,.2f}")

    # Schema dump
    _log(f"Final columns: {len(df_final.columns)}")
    for c in df_final.columns:
        _log(f"  {c:40s}  {df_final[c].dtype}")

    if args.dry_run:
        _log("DRY RUN: skipping S3 write.")
        return 0

    silver_key = SILVER_KEY_TPL.format(snap=snap_iso)
    buf = BytesIO()
    df_final.to_parquet(buf, index=False)
    buf.seek(0)
    body = buf.getvalue()
    s3.put_object(
        Bucket=S3_BUCKET, Key=silver_key, Body=body,
        ContentType="application/octet-stream",
        ServerSideEncryption="AES256",
    )
    _log(f"Wrote s3://{S3_BUCKET}/{silver_key} ({len(body):,} bytes)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"[{ts}] ERROR: convert_assets_v2_to_silver failed: {exc}", flush=True)
        traceback.print_exc()
        sys.exit(1)
