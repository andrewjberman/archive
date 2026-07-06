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
def loadp(k): return pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET,Key=k)["Body"].read()))
# fee accts with bill_emv==0 but holdings>0
bill=loadp(latest("silver/api_dims/billing/")); bill["account_id"]=_norm(bill["account_id"])
bd=bill.drop_duplicates("account_id",keep="last").set_index("account_id")
hold=loadp("gold/canonical/holdings_2026-07-06.parquet"); hold["account_id"]=_norm(hold["account_id"])
hmv=hold.groupby("account_id")["market_value"].sum()
fee=bd[bd["is_fee_earning"].astype(bool)]
zero_emv=[a for a in fee.index if a in hmv.index and float(fee.loc[a,"ending_mv"] or 0)==0 and hmv[a]>0]
print(f"268-check: {len(zero_emv)} fee accts with bill_emv==0 & holdings>0")
# bronze billing raw
br=pd.read_csv(io.BytesIO(s3.get_object(Bucket=BUCKET,Key="bronze/orion-api/2026-07-06/billing.csv")["Body"].read()),dtype=str)
aidc=next(c for c in br.columns if c.lower() in ("account id","account_id"))
emvc=next((c for c in br.columns if "ending market value" in c.lower()),None)
schc=next((c for c in br.columns if "fee schedule" in c.lower()),None)
amtc=next((c for c in br.columns if "fee amount" in c.lower()),None)
inclc=next((c for c in br.columns if "included in billing" in c.lower()),None)
br["_aid"]=_norm(br[aidc])
print(f"bronze cols: emv={emvc!r} sched={schc!r} amt={amtc!r} incl={inclc!r}")
sub=br[br["_aid"].isin(set(zero_emv))].drop_duplicates("_aid")
print(f"bronze rows for the zero-emv accts: {len(sub)}")
if emvc:
    ev=sub[emvc].fillna("").astype(str)
    print(f"  bronze ending-MV: blank/empty {((ev.str.strip()=='')|(ev.str.strip()=='$0.00')|(ev.str.strip()=='0')).sum()} of {len(sub)}")
    print("  sample bronze ending-MV values:", sub[emvc].head(8).tolist())
if inclc: print("  'Included In Billing' breakdown:\n"+sub[inclc].value_counts(dropna=False).head().to_string())
if schc: print("  fee_schedule sample:", sub[schc].head(4).tolist())
if amtc: print("  fee_amount sample:", sub[amtc].head(4).tolist())
