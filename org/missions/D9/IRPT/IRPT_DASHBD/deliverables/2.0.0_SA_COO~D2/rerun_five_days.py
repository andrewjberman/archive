"""Issuer's own re-run for row IRPT_DASHBD-D2-W111-S1 (CTO ROUND-75 ANALYSIS item 1).

Five of the 50 differing flow days, chosen by the issuer, across at least three of the 18 segments. BOTH sides are read fresh from S3
(not from any worker's pickle): the custodian's transactions copy, each transaction id counted once, against the served day flow,
to the cent. Prints counts and booleans only: no account id, no amount. Usage: python -I rerun_five_days.py
"""
import collections
import io
import json
import pickle
from concurrent.futures import ThreadPoolExecutor

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

W113 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/2.0.0_SA_COO~D2/"
BD_BUCKET, BD_PREFIX = "opal-data-assets", "blackdiamond/49financial/silver_legacy/transactions/"
GOLD_BUCKET, GOLD_PREFIX = "opal-data-49financial", "irpt/49financial/gold/account_return_daily/"
FT = ("Contribution", "Withdrawal")

# The ONLY thing taken from the worker: WHICH (segment, account, day) pairs are the 50. Their truth is re-read below.
days50 = sorted(pickle.load(open(W113 + "a1_days.pkl", "rb"))["days50"], key=lambda d: (d["idx"], d["day"]))
assert len(days50) == 50, len(days50)
PICK = [3, 14, 27, 38, 46]  # the issuer's choice of positions in that order, fixed before any read
chosen = [days50[i] for i in PICK]
segs = sorted({d["idx"] for d in chosen})
if len(segs) < 3:  # widen deterministically until three segments are covered
    seen = {d["idx"] for d in chosen}
    for i, d in enumerate(days50):
        if d["idx"] not in seen:
            chosen[len(seen) % 5] = d
            seen = {x["idx"] for x in chosen}
        if len(seen) >= 3:
            break
print("chosen days: %d across %d segment(s) of the 18" % (len(chosen), len({d["idx"] for d in chosen})))
want_acct = {d["a"].lstrip("0") for d in chosen}
want_days = {d["day"] for d in chosen}

s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))

# ---- side 1: the served day flow, read from the served gold partition of each chosen day -------------------------------
served = {}
gold_cols = None
for day in sorted(want_days):
    key = "%sdate=%s/data.parquet" % (GOLD_PREFIX, day)
    t = pq.read_table(io.BytesIO(s3.get_object(Bucket=GOLD_BUCKET, Key=key)["Body"].read()))
    gold_cols = t.schema.names
    flow_col = [c for c in gold_cols if c in ("flow", "net_flow", "external_flow", "flow_amount")]
    assert "account_id" in gold_cols and flow_col, gold_cols
    for r in t.select(["account_id", flow_col[0]]).to_pylist():
        a = str(r["account_id"]).strip().lstrip("0")
        if a in want_acct:
            served[(a, day)] = float(r[flow_col[0]] or 0.0)
print("served gold: %d day partition(s) read; flow column %r; %d of %d chosen (account, day) pairs found"
      % (len(want_days), flow_col[0], sum(1 for d in chosen if (d["a"].lstrip("0"), d["day"]) in served), len(chosen)))

# ---- side 2: the custodian's transactions copy, every date object, filtered to the chosen accounts ---------------------
tops = []
for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BD_BUCKET, Prefix=BD_PREFIX, Delimiter="/"):
    tops += [cp["Prefix"] for cp in p.get("CommonPrefixes", [])]
NEED = ["account_number", "return_date", "external_flow", "market_value", "transaction_id", "portfolio_group"]
nobj = [0]


def one(pref):
    out = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BD_BUCKET, Prefix=pref):
        for o in pg.get("Contents", []):
            if not o["Key"].endswith(".parquet"):
                continue
            t = pq.read_table(io.BytesIO(s3.get_object(Bucket=BD_BUCKET, Key=o["Key"])["Body"].read()))
            have = [c for c in NEED if c in t.schema.names]
            for r in t.select(have).to_pylist():
                if str(r.get("account_number")).strip().lstrip("0") in want_acct and r.get("external_flow") in FT \
                        and str(r.get("return_date"))[:10] in want_days:
                    out.append(r)
            nobj[0] += 1
    return out


rows = []
with ThreadPoolExecutor(24) as ex:
    for out in ex.map(one, tops):
        rows += out
print("custodian copy: %d date prefix(es), %d object(s) read, %d flow row(s) kept for the chosen accounts and days" % (len(tops), nobj[0], len(rows)))
missing_id = sum(1 for r in rows if r.get("transaction_id") in (None, ""))
print("rows with no transaction id: %d of %d" % (missing_id, len(rows)))


def signed(r):
    return (1 if r["external_flow"] == "Contribution" else -1) * abs(float(r["market_value"] or 0.0))


result = []
for n, d in enumerate(chosen, 1):
    a, day = d["a"].lstrip("0"), d["day"]
    L = [r for r in rows if str(r["account_number"]).strip().lstrip("0") == a and str(r["return_date"])[:10] == day]
    once = {}
    for r in L:
        once[str(r["transaction_id"])] = r
    naive = sum(signed(r) for r in L)
    dedup = sum(signed(r) for r in once.values())
    sv = served.get((a, day))
    counts = collections.Counter(str(r["transaction_id"]) for r in L)
    groups = len({str(r.get("portfolio_group")) for r in L})
    row = {"day_no": n, "segment_no": segs.index(d["idx"]) + 1 if d["idx"] in segs else None,
           "served_found": sv is not None, "ledger_rows": len(L), "distinct_transaction_ids": len(once),
           "copies_per_id": sorted(set(counts.values())), "portfolio_groups_on_the_day": groups,
           "naive_sum_equals_served_to_cent": (sv is not None and abs(naive - sv) <= 0.005),
           "each_id_once_equals_served_to_cent": (sv is not None and abs(dedup - sv) <= 0.005)}
    result.append(row)
    print(json.dumps(row))
ok = sum(1 for r in result if r["each_id_once_equals_served_to_cent"])
naive_ok = sum(1 for r in result if r["naive_sum_equals_served_to_cent"])
print("RESULT: each transaction id counted once reproduces the served day flow to the cent on %d of %d chosen days; the naive sum does on %d of %d"
      % (ok, len(result), naive_ok, len(result)))
json.dump({"picked_positions": PICK, "days": result, "reproduced": ok, "of": len(result), "naive_reproduced": naive_ok,
           "objects_read": nobj[0], "segments_covered": len({d["idx"] for d in chosen})}, open(OUT + "rerun_five_days.result.json", "w"), indent=1)
