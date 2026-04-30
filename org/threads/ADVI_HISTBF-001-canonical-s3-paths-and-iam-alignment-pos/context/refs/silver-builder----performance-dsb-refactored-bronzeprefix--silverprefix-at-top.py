#!/usr/bin/env python3
"""ADVI_HISTBF.006 -- Convert Inflection performance bronze parquet to silver.

Reads bronze/performance/{pull_date}.parquet (flat parquet of
weekly TWR factors per Inflection client from pull_inflection_performance_rest.py)
and produces a per-client-partitioned silver dataset with derived cumulative TWR.

Bronze schema (from pull_inflection_performance_rest.py):
  client_id (int), date (str YYYY-MM-DD), factor (float), pull_date (str YYYY-MM-DD)

Silver schema (output, per-client partition):
  client_id (str), week_date (date), twr_factor (float),
  cumulative_twr (float), inception_date (date), weeks_from_inception (int),
  snapshot_date (date), source_system (str), advisor_firm (str)

cumulative_twr: running product of twr_factor from inception (sorted ascending by
  week_date within each client). Value = prod(factors[:i]) - 1 so inception row = 0.0.

inception_date: earliest week_date for each client (constant per client in output).

weeks_from_inception: 0-indexed integer row number per client (0 = inception week).

Deduplication: on (client_id, week_date) — keeps last by sort order (safe for re-runs
  against the same bronze pull date).

Output: s3://opal-data-inf/silver/orion-rest/performance_weekly/
          client_id={client_id}/data.parquet  (one partition per client)

Usage:
  python3 convert_performance_to_silver.py --pull-date 2026-04-30 --upload
  python3 convert_performance_to_silver.py --pull-date 2026-04-30 --dry-run
  python3 convert_performance_to_silver.py --pull-date 2026-04-30 --snapshot-date 2026-04-30 --upload

Author: 0.4.0_DS_ClientPlatform_B
Project: ADVI_HISTBF.006
Date: 2026-04-30
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from io import BytesIO

import boto3
import pandas as pd

S3_BUCKET = "opal-data-inf"
BRONZE_PREFIX = "bronze/performance"
SILVER_PREFIX = "silver/performance"

ADVISOR_FIRM = "inflection"
SOURCE_SYSTEM = "orion-rest-performance"


def _log(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def _read_bronze(s3, pull_date: str) -> pd.DataFrame:
    key = f"{BRONZE_PREFIX}/{pull_date}.parquet"
    _log(f"Reading bronze: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(obj["Body"].read()))


def build_silver(
    bronze: pd.DataFrame,
    snapshot_date: dt.date,
) -> pd.DataFrame:
    df = bronze.copy()

    needed = {"client_id", "date", "factor"}
    missing = needed - set(df.columns)
    if missing:
        raise RuntimeError(f"Bronze missing required columns: {missing}. Got: {list(df.columns)}")

    df = df.rename(columns={"date": "week_date", "factor": "twr_factor"})
    df["client_id"] = df["client_id"].astype(str).str.strip()
    df["week_date"] = pd.to_datetime(df["week_date"]).dt.date
    df["twr_factor"] = df["twr_factor"].astype(float)

    # Deduplicate on (client_id, week_date) — keep last (stable for re-runs)
    before = len(df)
    df = df.drop_duplicates(subset=["client_id", "week_date"], keep="last")
    dropped = before - len(df)
    if dropped:
        _log(f"Deduped {dropped} duplicate (client_id, week_date) rows")

    # Sort chronologically per client
    df = df.sort_values(["client_id", "week_date"]).reset_index(drop=True)

    # Per-client derived columns.
    # twr_factor is a cumulative performance index from inception (inception week = 1.0),
    # NOT a weekly incremental multiplier. cumulative_twr = factor - 1 = total return from inception.
    # Weekly incremental return = factor[i] / factor[i-1] - 1 (not stored here; derivable).
    df["cumulative_twr"] = df["twr_factor"] - 1.0

    df["inception_date"] = (
        df.groupby("client_id")["week_date"]
        .transform("min")
    )

    df["weeks_from_inception"] = (
        df.groupby("client_id").cumcount()
    )

    df["snapshot_date"] = snapshot_date
    df["source_system"] = SOURCE_SYSTEM
    df["advisor_firm"] = ADVISOR_FIRM

    output_cols = [
        "client_id", "week_date", "twr_factor", "cumulative_twr",
        "inception_date", "weeks_from_inception",
        "snapshot_date", "source_system", "advisor_firm",
    ]
    return df[[c for c in output_cols if c in df.columns]]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--pull-date", required=True,
        help="Bronze pull date (YYYY-MM-DD). Reads bronze/performance/{date}.parquet.",
    )
    p.add_argument(
        "--snapshot-date", default=None,
        help="Silver snapshot_date value (default: same as --pull-date).",
    )
    p.add_argument(
        "--upload", action="store_true",
        help="Upload to s3://opal-data-inf/silver/performance/{date}.parquet",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Build silver in memory but do not write to S3.",
    )
    args = p.parse_args(argv)

    snapshot_date = dt.date.fromisoformat(args.snapshot_date or args.pull_date)

    s3 = boto3.client("s3", region_name="us-east-1")

    bronze = _read_bronze(s3, args.pull_date)
    _log(f"Bronze: {len(bronze):,} rows, {len(bronze.columns)} cols")

    client_count_bronze = bronze["client_id"].nunique() if "client_id" in bronze.columns else 0
    _log(f"Bronze clients: {client_count_bronze}")

    silver = build_silver(bronze, snapshot_date)
    _log(f"Silver: {len(silver):,} rows across {silver['client_id'].nunique()} clients")

    min_date = silver["week_date"].min() if len(silver) else "N/A"
    max_date = silver["week_date"].max() if len(silver) else "N/A"
    avg_weeks = len(silver) / max(silver["client_id"].nunique(), 1)
    _log(f"Week range: {min_date} to {max_date} (avg {avg_weeks:.1f} weeks/client)")

    cum_max = silver["cumulative_twr"].max() if len(silver) else 0.0
    cum_min = silver["cumulative_twr"].min() if len(silver) else 0.0
    _log(f"Cumulative TWR range: {cum_min:.4f} to {cum_max:.4f}")

    if args.dry_run:
        _log("DRY RUN: skipping write.")
        return 0

    if args.upload:
        silver_key = f"{SILVER_PREFIX}/{snapshot_date}.parquet"
        buf = BytesIO()
        silver.to_parquet(buf, index=False)
        buf.seek(0)
        s3.put_object(
            Bucket=S3_BUCKET, Key=silver_key, Body=buf.read(),
            ContentType="application/octet-stream", ServerSideEncryption="AES256",
        )
        _log(f"Uploaded: s3://{S3_BUCKET}/{silver_key} ({len(silver):,} rows)")
    else:
        _log("--upload not set; silver built but not uploaded to S3.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
