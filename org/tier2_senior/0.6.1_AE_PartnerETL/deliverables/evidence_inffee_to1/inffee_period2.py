from __future__ import annotations
import io, boto3, pandas as pd
BUCKET="opal-data-inf"; s3=boto3.client("s3")
def _norm(s): return s.astype(str).str.strip().str.split(".").str[0]
def latest(prefix):
    kk=[]; p=s3.get_paginator("list_objects_v2")
    for page in p.paginate(Bucket=BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            if o["Key"].endswith(".parquet"): kk.append((o["Key"],o["LastModified"]))
    kk.sort(key=lambda x:x[1]); return kk[-1][0] if kk else None
def load(k): return pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET,Key=k)["Body"].read()))
bill=load(latest("silver/api_dims/billing/")); bill["account_id"]=_norm(bill["account_id"])
bd=bill.drop_duplicates("account_id",keep="last").set_index("account_id")
hold=load("gold/canonical/holdings_2026-07-06.parquet"); hold["account_id"]=_norm(hold["account_id"])
hmv=hold.groupby("account_id")["market_value"].sum()
fee=bd[bd["is_fee_earning"].astype(bool)]
cmp=pd.DataFrame({"hold_mv":hmv, "bill_emv":fee["ending_mv"]}).dropna()
cmp["delta"]=cmp["hold_mv"]-cmp["bill_emv"]; cmp["ratio"]=cmp["bill_emv"]/cmp["hold_mv"]
print("top 10 fee accts by |delta| (holdings mv - billing ending_mv):")
print(cmp.reindex(cmp["delta"].abs().sort_values(ascending=False).index).head(10).to_string(float_format=lambda x:f"{x:,.2f}"))
print(f"\nfee-in-holdings ({len(cmp)}): hold_mv ${cmp['hold_mv'].sum():,.0f} | bill_emv ${cmp['bill_emv'].sum():,.0f} | overall ratio {cmp['bill_emv'].sum()/cmp['hold_mv'].sum():.3f}")
print(f"accts where bill_emv==0 but hold_mv>0: {((cmp['bill_emv']==0)&(cmp['hold_mv']>0)).sum()} | their hold_mv ${cmp.loc[(cmp['bill_emv']==0)&(cmp['hold_mv']>0),'hold_mv'].sum():,.0f}")
print(f"accts bill_emv within 1% of hold_mv: {(cmp['ratio'].between(0.99,1.01)).sum()}")
print(f"median per-acct ratio: {cmp['ratio'].median():.3f}")
# the fee_amount check on the 78 zero-holdings (are they billing fees on $0?)
acc=load(latest("silver/api_dims/accounts_v2/")); acc["account_id"]=_norm(acc["account_id"])
A=set(acc.drop_duplicates("account_id")["account_id"]); H=set(hold["account_id"])
ah=A-H
ahb=bd.reindex([a for a in ah if a in bd.index])
print(f"\n78 zero-holdings accts that ARE billed ({ahb.shape[0]}): fee_amount sum ${pd.to_numeric(ahb['fee_amount'],errors='coerce').sum():,.2f} | bill_emv sum ${pd.to_numeric(ahb['ending_mv'],errors='coerce').sum():,.2f}")
