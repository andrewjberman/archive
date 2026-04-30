#!/usr/bin/env python3
"""ADVI_HISTBF.005 -- Convert Inflection transaction bronze parquet to silver.

Reads bronze/transactions/{pull_date}.parquet (flat parquet of all
Inflection account transactions from pull_inflection_transactions_rest.py) and
produces transaction-level silver rows with rep attribution derived from
accounts_v2 silver (current-state JOIN).

Bronze schema (f4190d327):
  id (int), accountId (int), clientId (int), householdId (int),
  transTypeId (int), transDate (str YYYY-MM-DD), amount (float),
  cashAmount (float), units (float), price (float), ticker (str|null),
  description (str), pull_date (str YYYY-MM-DD)

Silver schema (output):
  account_id (str), household_id (str), rep_id (str|null),
  rep_id_is_historical (bool = False), trans_id (str),
  trans_date (date), amount (float), trans_type_id (int),
  trans_type_desc (str), category (str: billing|activity|other),
  snapshot_date (date), source_system (str), advisor_firm (str)

category: transTypeId 24/110 -> billing; 8/51 -> activity; else -> other

rep_id_is_historical=False documents that rep attribution is current-state only.
Downstream gold scripts applying per-advisor views should note this limitation.

Output: s3://opal-data-inf/silver/orion-rest/transactions/snapshot_date={date}/data.parquet

Usage:
  python3 convert_transactions_to_silver.py --pull-date 2026-04-30 --upload
  python3 convert_transactions_to_silver.py --pull-date 2026-04-30 --snapshot-date 2026-04-30 --dry-run

Author: 0.4.0_DS_ClientPlatform_B
Project: ADVI_HISTBF.005
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
BRONZE_PREFIX = "bronze/transactions"
ACCOUNTS_V2_PREFIX = "silver/api_dims/accounts_v2/"
SILVER_PREFIX = "silver/transactions"

ADVISOR_FIRM = "inflection"
SOURCE_SYSTEM = "orion-rest-transactions"

TRANS_TYPE_DESC: dict[int, str] = {
    8: "Client Contribution",
    10: "Buy Exchange",
    14: "Income Reinvested",
    17: "Dividend to Cash",
    24: "Management Fee",
    29: "Trading Expense",
    34: "Long Term Gain to Cash",
    39: "Merge In from Other Account",
    40: "Merge In Exchange",
    42: "Merge Out to Other Account",
    43: "Merge Out Exchange",
    49: "Short Term Gain to Cash",
    51: "Client Distribution",
    53: "Sell Exchange",
    55: "Stock Split",
    104: "Interest Paid in Cash",
    110: "Fee Credit",
    157: "Decrease in Value",
    171: "Internal Account Journal Out",
    172: "Internal Account Journal In",
    174: "Income Paid",
    189: "Dividend Paid from Cash",
    204: "External Account Activity In",
}

BILLING_TYPES: frozenset[int] = frozenset({24, 110})
ACTIVITY_TYPES: frozenset[int] = frozenset({8, 51})


def _log(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def _latest_accounts_v2_key(s3) -> str:
    paginator = s3.get_paginator("list_objects_v2")
    keys = sorted([
        obj["Key"]
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=ACCOUNTS_V2_PREFIX)
        for obj in page.get("Contents", [])
        if obj["Key"].endswith("/data.parquet")
    ])
    if not keys:
        raise RuntimeError("No silver/api_dims/accounts_v2 partition found in S3.")
    return keys[-1]


def _load_rep_lookup(s3) -> pd.DataFrame:
    """Return DataFrame with account_id (str), household_id (str), rep_id (str)."""
    key = _latest_accounts_v2_key(s3)
    _log(f"accounts_v2 source: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    df = pd.read_parquet(BytesIO(obj["Body"].read()))
    needed = {"account_id", "household_id", "rep_id"}
    missing = needed - set(df.columns)
    if missing:
        raise RuntimeError(f"accounts_v2 missing columns: {missing}. Got: {list(df.columns)}")
    lookup = (
        df[["account_id", "household_id", "rep_id"]]
        .drop_duplicates("account_id")
        .copy()
    )
    lookup["account_id"] = lookup["account_id"].astype(str).str.strip()
    lookup["household_id"] = lookup["household_id"].astype(str).str.strip()
    lookup["rep_id"] = lookup["rep_id"].astype(str).str.strip()
    return lookup


def _read_bronze(s3, pull_date: str) -> pd.DataFrame:
    key = f"{BRONZE_PREFIX}/{pull_date}.parquet"
    _log(f"Reading bronze: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(obj["Body"].read()))


def _derive_category(trans_type_id_series: pd.Series) -> pd.Series:
    def _cat(tid: int) -> str:
        if tid in BILLING_TYPES:
            return "billing"
        if tid in ACTIVITY_TYPES:
            return "activity"
        return "other"
    return trans_type_id_series.apply(_cat)


def build_silver(
    bronze: pd.DataFrame,
    rep_lookup: pd.DataFrame,
    snapshot_date: dt.date,
) -> pd.DataFrame:
    df = bronze.copy()

    # Normalize bronze columns to snake_case silver names.
    # Live API returns transAmount (not amount) and transDate — Phase 0 HAR had different field names.
    df = df.rename(columns={
        "id": "trans_id",
        "accountId": "account_id",
        "clientId": "client_id_bronze",
        "householdId": "household_id_bronze",
        "transTypeId": "trans_type_id",
        "transDate": "trans_date",
        "transAmount": "amount",
    })

    # account_id must be str for the LEFT JOIN against rep_lookup
    df["account_id"] = df["account_id"].astype(str).str.strip()
    df["trans_id"] = df["trans_id"].astype(str)

    # Deduplicate on trans_id (idempotent re-run safety)
    before = len(df)
    df = df.drop_duplicates(subset=["trans_id"])
    dropped = before - len(df)
    if dropped:
        _log(f"Deduped {dropped} duplicate trans_id rows")

    # Rep attribution JOIN (current-state; rep_id_is_historical=False)
    df = df.merge(rep_lookup, on="account_id", how="left")

    # Prefer JOIN-derived household_id; fall back to bronze householdId
    if "household_id" not in df.columns:
        df["household_id"] = df.get("household_id_bronze", pd.Series(dtype="object")).astype(str)

    # Derived columns
    df["trans_type_desc"] = df["trans_type_id"].map(TRANS_TYPE_DESC).fillna("Unknown")
    df["category"] = _derive_category(df["trans_type_id"])
    df["trans_date"] = pd.to_datetime(df["trans_date"]).dt.date
    df["rep_id_is_historical"] = False
    df["snapshot_date"] = snapshot_date
    df["source_system"] = SOURCE_SYSTEM
    df["advisor_firm"] = ADVISOR_FIRM

    output_cols = [
        "account_id", "household_id", "rep_id", "rep_id_is_historical",
        "trans_id", "trans_date", "amount", "trans_type_id", "trans_type_desc",
        "category", "snapshot_date", "source_system", "advisor_firm",
    ]
    return df[[c for c in output_cols if c in df.columns]]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--pull-date", required=True,
        help="Bronze pull date (YYYY-MM-DD). Reads bronze/transactions/{date}.parquet.",
    )
    p.add_argument(
        "--snapshot-date", default=None,
        help="Silver snapshot_date partition key (default: same as --pull-date).",
    )
    p.add_argument(
        "--upload", action="store_true",
        help="Upload to s3://opal-data-inf/silver/orion-rest/transactions/snapshot_date={date}/data.parquet",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Build silver in memory but do not write.",
    )
    args = p.parse_args(argv)

    snapshot_date = dt.date.fromisoformat(args.snapshot_date or args.pull_date)

    s3 = boto3.client("s3", region_name="us-east-1")

    rep_lookup = _load_rep_lookup(s3)
    _log(f"Rep lookup: {len(rep_lookup)} accounts")

    bronze = _read_bronze(s3, args.pull_date)
    _log(f"Bronze: {len(bronze):,} rows, {len(bronze.columns)} cols")

    silver = build_silver(bronze, rep_lookup, snapshot_date)
    _log(f"Silver: {len(silver):,} rows")

    for cat in ("billing", "activity", "other"):
        subset = silver[silver["category"] == cat]
        _log(f"  {cat}: {len(subset):,} rows  amount=${subset['amount'].sum():,.0f}")

    rep_null = silver["rep_id"].isna().sum() if "rep_id" in silver.columns else 0
    if rep_null:
        _log(f"WARN: {rep_null} rows with null rep_id (accounts absent from accounts_v2 silver)")

    if args.dry_run:
        _log("DRY RUN: skipping write.")
        return 0

    buf = BytesIO()
    silver.to_parquet(buf, index=False)
    buf.seek(0)
    parquet_bytes = buf.read()

    if args.upload:
        silver_key = f"{SILVER_PREFIX}/{snapshot_date}.parquet"
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=silver_key,
            Body=parquet_bytes,
            ContentType="application/octet-stream",
            ServerSideEncryption="AES256",
        )
        _log(f"Uploaded: s3://{S3_BUCKET}/{silver_key} ({len(parquet_bytes):,} bytes, {len(silver):,} rows)")
    else:
        _log("--upload not set; parquet built but not uploaded to S3.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
