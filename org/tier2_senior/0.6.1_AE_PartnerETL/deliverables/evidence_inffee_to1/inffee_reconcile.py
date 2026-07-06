#!/usr/bin/env python3
"""Reconcile: served header_metrics/clients_tab vs fresh holdings/billing parquets.
Determine WHICH account universe = 868 vs 790, and what is served NOW."""
from __future__ import annotations
import io, json
import boto3
import pandas as pd

BUCKET = "opal-data-inf"
s3 = boto3.client("s3")

def get_json(key):
    r = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(r["Body"].read())

def _norm(s): return s.astype(str).str.strip().str.split(".").str[0]

# --- served platinum JSONs (what Andrew sees) ---
print("=== SERVED header_metrics.json#total ===")
try:
    hm = get_json("platinum/firm/header_metrics.json")
    tot = hm.get("total", hm)
    for k in ("account_count","fee_earning_account_count","non_fee_earning_account_count",
              "fee_earning_aua","non_fee_earning_aua","fee_earning_client_count",
              "non_fee_earning_client_count","total_aua","data_as_of","non_fee_earning_aua_status"):
        if k in tot: print(f"  {k}: {tot[k]}")
    print(f"  generated_at: {hm.get('generated_at')}")
except Exception as e:
    print("  ERR", e)

print("\n=== SERVED clients_tab.json#headline ===")
try:
    ct = get_json("platinum/firm/clients_tab.json")
    hl = ct.get("headline", {})
    for k in ("account_count","client_count","total_aua","data_as_of"):
        if k in hl: print(f"  {k}: {hl[k]}")
    print(f"  generated_at: {ct.get('generated_at')}")
    # how many households, sum of their account_count?
    rows = ct.get("clients", ct.get("rows", []))
    if rows and isinstance(rows, list):
        acct_sum = sum(r.get("account_count",0) for r in rows if isinstance(r,dict))
        print(f"  households(rows): {len(rows)} | SUM(row.account_count): {acct_sum}")
except Exception as e:
    print("  ERR", e)

# --- holdings partitions available ---
print("\n=== holdings partitions (gold/canonical/holdings_*.parquet) ===")
p = s3.get_paginator("list_objects_v2")
hk = []
for page in p.paginate(Bucket=BUCKET, Prefix="gold/canonical/holdings_"):
    for o in page.get("Contents", []):
        if o["Key"].endswith(".parquet"):
            hk.append((o["Key"], o["LastModified"]))
hk.sort(key=lambda x: x[1])
for k, lm in hk[-6:]:
    df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()), columns=["account_id","market_value"])
    df["account_id"] = _norm(df["account_id"])
    print(f"  {k}  | mod {lm:%Y-%m-%d %H:%M} | accts {df['account_id'].nunique()} | AUA ${df['market_value'].sum():,.0f}")

# --- accounts_v2 universe (candidate 868?) ---
print("\n=== accounts_v2 universe (is_active / all) ===")
def latest(prefix):
    kk=[]
    for page in p.paginate(Bucket=BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            if o["Key"].endswith(".parquet"): kk.append((o["Key"],o["LastModified"]))
    kk.sort(key=lambda x:x[1]); return kk[-1][0] if kk else None
ak = latest("silver/api_dims/accounts_v2/")
acc = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=ak)["Body"].read()))
acc["account_id"] = _norm(acc["account_id"])
print(f"  accounts_v2: {acc['account_id'].nunique()} distinct | is_active=True: {acc[acc['is_active']==True]['account_id'].nunique() if 'is_active' in acc else 'n/a'}")
if "account_status" in acc: print("  account_status:\n"+acc.drop_duplicates('account_id')['account_status'].value_counts(dropna=False).to_string())
if "is_managed" in acc: print("  is_managed:\n"+acc.drop_duplicates('account_id')['is_managed'].value_counts(dropna=False).to_string())
