#!/usr/bin/env python3
"""
Validate AUA: Gold vs Silver — Daily Cross-Check

Runs daily in the BD gold pipeline after 05_build_client_performance.py,
before 05d_write_aua_certification.py.

Compares gold AUA (positions cube x canonical prices, from client_performance.parquet)
against silver AUA (BD-reported market values, from silver/allocations/{date}.parquet).

Produces gold/validation/aua_validation_{date}.json with:
  - Aggregate gap (gold vs silver)
  - Account-level decomposition (missing accounts + price divergence estimate)
  - Liability type breakdown
  - PASS / WARN / FAIL status

Thresholds:
  PASS: abs(gap_pct) <= 0.5%  AND  accounts_missing_from_gold <= 10
  WARN: abs(gap_pct) <= 1.0%  OR   accounts_missing_from_gold <= 50
  FAIL: abs(gap_pct) > 1.0%   OR   accounts_missing_from_gold > 50

Non-blocking: any error logs at ERROR and exits 0. FAIL is a signal for
investigation, not a pipeline halt.

Output: s3://opal-data-bd/gold/validation/aua_validation_{date}.json

Can be run standalone for backfill:
  python3 05c_validate_aua_vs_silver.py --date 2026-03-09
  python3 05c_validate_aua_vs_silver.py --backfill  (all available silver dates)
"""

import sys
import json
import datetime
import io
import argparse

import boto3
import pandas as pd

S3_BUCKET = "opal-data-bd"
LIABILITY_TYPES = ["CreditCard", "Mortgage", "Loans", "Insurance", "TermLife", "Annuity"]

# Thresholds
PASS_GAP_PCT = 0.005      # 0.5%
WARN_GAP_PCT = 0.01       # 1.0%
PASS_MISSING_ACCOUNTS = 10
WARN_MISSING_ACCOUNTS = 50


def log(msg):
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def s3_object_exists(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except s3_client.exceptions.ClientError:
        return False
    except Exception:
        return False


def read_parquet_from_s3(s3_client, bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    buf = io.BytesIO(response["Body"].read())
    return pd.read_parquet(buf)


def list_silver_dates(s3_client):
    """List all available silver allocation dates from S3."""
    paginator = s3_client.get_paginator("list_objects_v2")
    dates = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix="silver/allocations/"):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".parquet"):
                # Extract date from silver/allocations/YYYY-MM-DD.parquet
                basename = key.rsplit("/", 1)[-1]
                date_str = basename.replace(".parquet", "")
                try:
                    datetime.date.fromisoformat(date_str)
                    dates.append(date_str)
                except ValueError:
                    continue
    return sorted(dates)


def determine_status(gap_pct, missing_count):
    """Determine PASS/WARN/FAIL based on thresholds."""
    abs_gap = abs(gap_pct)

    # FAIL: either metric exceeds WARN threshold
    if abs_gap > WARN_GAP_PCT or missing_count > WARN_MISSING_ACCOUNTS:
        return "FAIL"

    # PASS: both metrics within tight threshold
    if abs_gap <= PASS_GAP_PCT and missing_count <= PASS_MISSING_ACCOUNTS:
        return "PASS"

    # WARN: everything else (between PASS and FAIL thresholds)
    return "WARN"


def validate_date(s3_client, run_date, client_perf_df, accounts_dim_df):
    """
    Run validation for a single date.

    Returns: (result_dict, status_str) or (None, "SKIP") if no silver data.
    """
    silver_key = f"silver/allocations/{run_date}.parquet"
    if not s3_object_exists(s3_client, S3_BUCKET, silver_key):
        log(f"SKIP: no silver allocation for {run_date} -- validation deferred")
        return None, "SKIP"

    # Load silver allocations for this date
    silver_df = read_parquet_from_s3(s3_client, S3_BUCKET, silver_key)

    required_cols = {"account_market_value", "account_type"}
    missing = required_cols - set(silver_df.columns)
    if missing:
        log(f"ERROR: silver parquet for {run_date} missing columns: {missing}")
        return None, "ERROR"

    # Use account_id for decomposition — both silver and gold have this column.
    # Do NOT use account_number: silver has it but gold does not, and the ID
    # spaces are different (account_number is BD's external ID, account_id is
    # the internal z-prefixed ID used across both datasets).
    acct_col = "account_id" if "account_id" in silver_df.columns else None

    # --- Liability breakdown ---
    liability_breakdown = {}
    for lt in LIABILITY_TYPES:
        mask = silver_df["account_type"] == lt
        subset = silver_df[mask]
        liability_breakdown[lt] = {
            "count": int(mask.sum()),
            "mv": float(round(subset["account_market_value"].sum(), 2)),
        }

    # --- Silver AUA (all accounts) ---
    silver_aua = float(silver_df["account_market_value"].sum())

    # --- Silver AUA excluding liabilities ---
    excl_mask = silver_df["account_type"].isin(LIABILITY_TYPES)
    silver_eligible = silver_df[~excl_mask]
    silver_aua_excl_liabilities = float(silver_eligible["account_market_value"].sum())

    # --- Gold AUA for this date ---
    cp_today = client_perf_df[client_perf_df["_date_str"] == run_date]
    if cp_today.empty:
        log(f"WARN: no client_performance rows for date={run_date} -- gold_aua=0")
    gold_aua = float(cp_today["total_aua"].sum()) if not cp_today.empty else 0.0

    # --- Gap computation ---
    gap_abs = gold_aua - silver_aua
    gap_pct = (gap_abs / silver_aua) if silver_aua != 0 else 0.0

    # --- Account-level decomposition ---
    accounts_missing_from_gold = 0
    accounts_missing_mv = 0.0

    if acct_col is not None and accounts_dim_df is not None:
        # Get unique account IDs from silver
        silver_accounts = set(silver_df[acct_col].dropna().unique())

        # Get unique account IDs from gold accounts dimension (also uses account_id)
        gold_acct_col = "account_id"
        if gold_acct_col in accounts_dim_df.columns:
            gold_accounts = set(accounts_dim_df[gold_acct_col].dropna().unique())
            missing_accounts = silver_accounts - gold_accounts

            # Sum MV of accounts in silver that are missing from gold
            missing_mask = silver_df[acct_col].isin(missing_accounts)
            accounts_missing_from_gold = int(len(missing_accounts))
            accounts_missing_mv = float(round(
                silver_df[missing_mask]["account_market_value"].sum(), 2
            ))

    price_divergence_estimate = float(round(gap_abs + accounts_missing_mv, 2))

    # --- Status determination ---
    status = determine_status(gap_pct, accounts_missing_from_gold)

    result = {
        "date": run_date,
        "gold_aua": round(gold_aua, 2),
        "silver_aua": round(silver_aua, 2),
        "silver_aua_excl_liabilities": round(silver_aua_excl_liabilities, 2),
        "gap_abs": round(gap_abs, 2),
        "gap_pct": round(gap_pct, 6),
        "accounts_missing_from_gold": accounts_missing_from_gold,
        "accounts_missing_mv": round(accounts_missing_mv, 2),
        "price_divergence_estimate": round(price_divergence_estimate, 2),
        "status": status,
        "liability_types_in_silver": liability_breakdown,
    }

    log(f"{status}: date={run_date} gold={gold_aua:,.0f} silver={silver_aua:,.0f} "
        f"gap={gap_abs:+,.0f} ({gap_pct:+.4%}) missing_accts={accounts_missing_from_gold} "
        f"missing_mv={accounts_missing_mv:,.0f} price_div={price_divergence_estimate:+,.0f}")

    return result, status


def write_validation_to_s3(s3_client, result):
    """Write a single validation result to S3."""
    run_date = result["date"]
    key = f"gold/validation/aua_validation_{run_date}.json"
    body = json.dumps(result, indent=2)
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/json",
    )
    log(f"OK: validation written to s3://{S3_BUCKET}/{key}")


def main():
    parser = argparse.ArgumentParser(description="Validate gold AUA vs silver allocations")
    parser.add_argument("--date", type=str, default=None,
                        help="Run date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--backfill", action="store_true",
                        help="Backfill all available silver dates.")
    args = parser.parse_args()

    log("OK: 05c_validate_aua_vs_silver started")

    s3 = boto3.client("s3", region_name="us-east-1")

    # --- Load gold client_performance (shared across all dates) ---
    gold_cp_key = "gold/client_performance.parquet"
    log("OK: loading gold/client_performance.parquet...")
    cp_df = read_parquet_from_s3(s3, S3_BUCKET, gold_cp_key)

    if "date" not in cp_df.columns or "total_aua" not in cp_df.columns:
        log("ERROR: client_performance.parquet missing required columns (date, total_aua)")
        sys.exit(0)

    # Normalize date column for string comparison
    cp_df["_date_str"] = pd.to_datetime(cp_df["date"]).dt.strftime("%Y-%m-%d")
    log(f"OK: client_performance loaded: {len(cp_df):,} rows, "
        f"date range {cp_df['_date_str'].min()} to {cp_df['_date_str'].max()}")

    # --- Load gold accounts dimension (for missing-account decomposition) ---
    accounts_dim_key = "gold/accounts_dimension_latest.parquet"
    accounts_dim_df = None
    if s3_object_exists(s3, S3_BUCKET, accounts_dim_key):
        log("OK: loading gold/accounts_dimension_latest.parquet...")
        accounts_dim_df = read_parquet_from_s3(s3, S3_BUCKET, accounts_dim_key)
        log(f"OK: accounts_dimension loaded: {len(accounts_dim_df):,} rows")
    else:
        log("WARN: accounts_dimension_latest.parquet not found -- missing-account decomposition unavailable")

    # --- Determine dates to validate ---
    if args.backfill:
        log("OK: backfill mode -- listing all silver allocation dates...")
        dates = list_silver_dates(s3)
        log(f"OK: found {len(dates)} silver dates to validate")
    elif args.date:
        dates = [args.date]
    else:
        dates = [datetime.date.today().strftime("%Y-%m-%d")]

    # --- Run validation for each date ---
    summary = {"PASS": 0, "WARN": 0, "FAIL": 0, "SKIP": 0, "ERROR": 0}

    for run_date in dates:
        result, status = validate_date(s3, run_date, cp_df, accounts_dim_df)
        summary[status] = summary.get(status, 0) + 1

        if result is not None:
            write_validation_to_s3(s3, result)

    # --- Summary ---
    log(f"OK: validation complete -- "
        f"PASS={summary['PASS']} WARN={summary['WARN']} FAIL={summary['FAIL']} "
        f"SKIP={summary['SKIP']} ERROR={summary['ERROR']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        import traceback
        print(f"ERROR: 05c_validate_aua_vs_silver failed: {exc}", flush=True)
        traceback.print_exc()
        sys.exit(0)  # non-blocking -- pipeline continues
