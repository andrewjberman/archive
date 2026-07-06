#!/usr/bin/env python3
"""ADVI_INFFEE TO-1 -- DECISIVE set algebra across the 4 universes + characterize the 78."""
from __future__ import annotations
import io
import boto3
import pandas as pd

BUCKET = "opal-data-inf"
s3 = boto3.client("s3")
def _norm(s): return s.astype(str).str.strip().str.split(".").str[0]
def latest(prefix):
    kk=[]; p=s3.get_paginator("list_objects_v2")
    for page in p.paginate(Bucket=BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            if o["Key"].endswith(".parquet"): kk.append((o["Key"],o["LastModified"]))
    kk.sort(key=lambda x:x[1]); return kk[-1][0] if kk else None
def load(key): return pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()))

# universes
acc = load(latest("silver/api_dims/accounts_v2/")); acc["account_id"]=_norm(acc["account_id"])
acc1 = acc.drop_duplicates("account_id")
hold = load("gold/canonical/holdings_2026-07-06.parquet"); hold["account_id"]=_norm(hold["account_id"])
bill = load(latest("silver/api_dims/billing/")); bill["account_id"]=_norm(bill["account_id"])
if "period_end" in bill:
    bill["period_end"]=pd.to_datetime(bill["period_end"],errors="coerce")
    billd = bill.sort_values(["account_id","period_end"]).drop_duplicates("account_id",keep="last")
else: billd = bill.drop_duplicates("account_id",keep="last")

A = set(acc1["account_id"])                       # master 868
H = set(hold["account_id"])                        # holdings 790
B = set(billd["account_id"])                       # billing 890
Bf = set(billd.loc[billd["is_fee_earning"].astype(bool),"account_id"])   # fee-billed 789
Bn = B - Bf                                         # non-fee-billed

print("=== SET SIZES ===")
print(f"  A master(accounts_v2)   |A|={len(A)}")
print(f"  H holdings              |H|={len(H)}")
print(f"  B billing               |B|={len(B)}  (fee {len(Bf)} / nonfee {len(Bn)})")
print("=== RELATIONSHIPS ===")
print(f"  A - H (master, NO holdings)  = {len(A-H)}   <- the '78'?")
print(f"  H - A (holdings, not master) = {len(H-A)}")
print(f"  A - B (master, NO billing)   = {len(A-B)}")
print(f"  H - B (holdings, NO billing) = {len(H-B)}")
print(f"  B - A (billing, not master)  = {len(B-A)}")
print(f"  B - H (billing, no holdings) = {len(B-H)}")
print(f"  Bf - H (fee-billed, no hold) = {len(Bf-H)}")

# holdings AUA map
haua_s = hold.groupby("account_id")["market_value"].sum()
def haua(ids): return haua_s.reindex([i for i in ids if i in haua_s.index]).sum()
# billing ending_mv map (latest period)
baua_s = billd.set_index("account_id")["ending_mv"]
def baua_of(ids): return baua_s.reindex([i for i in ids if i in baua_s.index]).fillna(0).sum()

print("\n=== VALUATION: fee-earning accts, holdings mv vs billing ending_mv ===")
fee_in_h = Bf & H
print(f"  fee-billed AND in holdings: {len(fee_in_h)} accts")
print(f"    holdings market_value sum: ${haua(fee_in_h):,.2f}")
print(f"    billing ending_mv sum:     ${baua_of(fee_in_h):,.2f}")
print(f"    DELTA (hold - bill):       ${haua(fee_in_h)-baua_of(fee_in_h):,.2f}")
print(f"  ALL billing fee ending_mv (789): ${baua_of(Bf):,.2f}  (header_metrics fee_earning_aua)")

print("\n=== TRUE POSITIVE three-way on HOLDINGS (790) universe ===")
h_fee = H & Bf; h_non = H & Bn; h_unb = H - B
print(f"  fee-earning:        {len(h_fee):4d} | holdings-AUA ${haua(h_fee):>15,.2f}")
print(f"  non-fee (marked):   {len(h_non):4d} | holdings-AUA ${haua(h_non):>15,.2f}")
print(f"  unbilled:           {len(h_unb):4d} | holdings-AUA ${haua(h_unb):>15,.2f}")
print(f"  TOTAL:              {len(H):4d} | holdings-AUA ${haua(H):>15,.2f}")

print("\n=== TRUE three-way on MASTER (868) universe ===")
a_fee = A & Bf; a_non = A & Bn; a_unb = A - B
print(f"  fee-billed:         {len(a_fee):4d}")
print(f"  non-fee-billed:     {len(a_non):4d}")
print(f"  unbilled(no B row): {len(a_unb):4d}")
print(f"  master total:       {len(A):4d}")

print("\n=== CHARACTERIZE A-H (master accts with NO holdings) ===")
ah = A - H
sub = acc1[acc1["account_id"].isin(ah)]
print(f"  count: {len(ah)}")
for col in ["is_managed","is_sweep_account","is_sleeve_account","account_type","management_style","is_trading_blocked"]:
    if col in sub:
        print(f"  {col}:"); print(sub[col].value_counts(dropna=False).head(8).to_string())
if "current_value" in sub:
    cv = pd.to_numeric(sub["current_value"], errors="coerce")
    print(f"  current_value: sum ${cv.sum():,.0f} | median ${cv.median():,.0f} | <=$0: {(cv<=0).sum()} | >0: {(cv>0).sum()}")
if "account_start_date" in sub:
    sd = pd.to_datetime(sub["account_start_date"], errors="coerce")
    print(f"  account_start_date: min {sd.min()} max {sd.max()} | opened in last 30d: {(sd > pd.Timestamp('2026-06-06')).sum()}")
# are these 78 billed / fee-earning?
print(f"  of A-H: in billing {len(ah & B)} | fee-billed {len(ah & Bf)} | non-fee-billed {len(ah & Bn)}")

print("\n=== CHARACTERIZE the 12 is_managed=False master accts ===")
nm = acc1[acc1["is_managed"]==False]
print(f"  count {len(nm)} | in holdings {len(set(nm['account_id'])&H)} | in billing {len(set(nm['account_id'])&B)} | fee-billed {len(set(nm['account_id'])&Bf)}")
if "current_value" in nm:
    print(f"  current_value sum ${pd.to_numeric(nm['current_value'],errors='coerce').sum():,.0f}")
