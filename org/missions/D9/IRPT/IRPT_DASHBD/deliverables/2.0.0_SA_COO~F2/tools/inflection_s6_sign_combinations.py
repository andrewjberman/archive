"""IRPT_DASHBD (workstream F-SHIP, ~F2): the SIGN COMBINATIONS of the two S6 legs (Dividend Paid from Cash, Income Paid) and their income-class partner on the LATEST Orion
snapshot, READ-ONLY and VALUES-FREE (counts only; GET only; no account id or amount is kept).

  python <this file> <out.json>
"""
import importlib.util
import io
import json
import sys
from collections import Counter
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402

spec = importlib.util.spec_from_file_location("iar", ROOT / "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
iar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iar)
con = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
income = {m["source_value"] for m in con["source_mapping"] if m["firm"] == "inflection" and m["flow_class"] == "INCOME"}
s3 = boto3.client("s3", config=Config(max_pool_connections=8))
bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
prefix = rest + "fact_transactions/"
day = ard.partition_days(s3, bucket, prefix)[-1]
tabs = []
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
    for o in page.get("Contents", []) or []:
        if o["Key"].endswith(".parquet"):
            tabs.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()), columns=["status", "transDate", "accountId", "transAmount", "transactionDescription"]))
df = pa.concat_tables(tabs, promote_options="default").to_pandas()
c = df[df["status"] == "Complete"]
a = c[c["transactionDescription"] == "Dividend Paid from Cash"]
b = c[c["transactionDescription"] == "Income Paid"]
inc = c[c["transactionDescription"].isin(income)]


def sg(x):
    return "neg" if x < 0 else ("pos" if x > 0 else "zero")


ia = {}
for r in inc.itertuples():
    ia.setdefault((r.accountId, r.transDate, round(abs(r.transAmount), 6)), []).append(sg(r.transAmount))
bk = {}
for r in b.itertuples():
    bk.setdefault((r.accountId, r.transDate, round(abs(r.transAmount), 6)), []).append(r.transAmount)
combos = Counter()
net_zero = events = 0
for r in a.itertuples():
    k = (r.accountId, r.transDate, round(abs(r.transAmount), 6))
    events += 1
    bs = bk.get(k, [])
    bsig = "/".join(sorted(set(sg(x) for x in bs))) or "none"
    isig = "/".join(sorted(set(ia.get(k, [])))) or "none"
    combos["A=%s B=%s INCOME_partner=%s" % (sg(r.transAmount), bsig, isig)] += 1
    if bs and abs(r.transAmount + bs[0]) < 1e-6:
        net_zero += 1
out = ({"snapshot": day, "a_rows": len(a), "b_rows": len(b), "events_keyed_on_leg_a": events, "legs_net_to_zero": net_zero, "sign_combinations": dict(combos),
       "reader": "values-free: counts of sign combinations only"})
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
print(json.dumps(out, indent=1))
