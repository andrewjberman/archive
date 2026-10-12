"""TO-DB-b-135 reader: read-only S3 GETs/LISTs of 49 Financial's own tree for the 90 segments. Output is private (outside the repo).
Reuses reader ~12 tieout_e2 (bd_points shape, gold columns) and the ~75/~81 reader key shapes; narrowed to the 90 accounts.
Usage: python -I read90.py <repo_root>
"""
import io
import json
import pickle
import sys
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/"
OUT = PRIV + "0.9.0_WK_IRPT_DASHBD~108/"
REC = PRIV + "0.9.0_WK_IRPT_DASHBD~86/RESTATED_TIEOUT.json"
MEM = PRIV + "0.9.0_WK_IRPT_DASHBD~104/membership.json"
PLAN_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/BD_POPULATION_PLAN_E3.json"
BRONZE_BUCKET = "opal-data-assets"
BRONZE_PREFIX = "blackdiamond/49financial/bronze/reporting_performance/pull=2026" + "1004/"
GOLD_BUCKET = "opal-data-49financial"
GOLD_PREFIX = "irpt/49financial/gold/account_return_daily/"
TXN_PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
TXN_COLS = ["return_date", "action", "transaction_type", "transaction_sub_type", "external_flow", "account_number", "market_value",
            "transaction_fee", "income", "account_fee", "trade_date", "settle_date"]


def jload(p):
    return json.loads(Path(p).read_bytes().decode("utf-8"))


def main():
    segs = jload(REC)["segments"]
    mem = jload(MEM)["REMAINDER"]
    if len(mem) != 90:
        print("STOP: membership REMAINDER %d, want 90" % len(mem))
        sys.exit(2)
    S = [segs[i] for i in mem]
    assert all(s["reason_after"] == "UNEXPLAINED" for s in S)
    plan = jload(OUT + "plan.json")
    bdacct = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
    accts = sorted({s["account"] for s in S})
    need = {}
    for s in S:
        need.setdefault(bdacct[s["account"]], set()).add((s["segment"]["start"], s["segment"]["end"]))
    print("segments", len(S), "accounts", len(accts))
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
    reads = {"prefixes": [], "objects": 0}

    # ---- BD bronze points (direct GET per account)
    def bdget(a):
        key = "%sacct=%s.json" % (BRONZE_PREFIX, a)
        b = json.loads(s3.get_object(Bucket=BRONZE_BUCKET, Key=key)["Body"].read().decode("utf-8"))
        out = {}
        for lv in b.get("levels") or []:
            dd = lv.get("descriptor") or {}
            if dd.get("level") != "Account" or str(dd.get("levelId")) != a:
                continue
            for p in lv.get("dateRangePoints") or []:
                k = (p["dateRange"]["startDate"][:10], p["dateRange"]["endDate"][:10])
                if k in need[a]:
                    pt = {kk: vv for kk, vv in p.items() if kk != "dateRange" and not isinstance(vv, (dict, list))}
                    pt["twr"] = (p.get("timeWeightedReturns") or {}).get("return")
                    out[k] = pt
        return a, out

    with ThreadPoolExecutor(16) as ex:
        bd = dict(ex.map(bdget, list(need)))
    reads["prefixes"].append(BRONZE_BUCKET + "/" + BRONZE_PREFIX)
    reads["objects"] += len(need)
    print("bd points", sum(len(v) for v in bd.values()), "keys of a point:", sorted(next(iter(next(iter(bd.values())).values())).keys()))

    # ---- served gold (Opal's own side), partitions from (min start - 20d) to max end
    lo = (dt.date.fromisoformat(min(s["segment"]["start"] for s in S)) - dt.timedelta(days=20)).isoformat()
    hi = max(s["segment"]["end"] for s in S)
    dates = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=GOLD_BUCKET, Prefix=GOLD_PREFIX, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("date=") and lo <= seg[5:] <= hi:
                dates.append(seg[5:])
    dates.sort()
    want = set(accts)
    cols = ["account_id", "business_date", "market_value_eod", "external_flow", "income_return", "income_received", "total_return_daily",
            "holdings_price_return_reason"]

    def num(v):
        return None if v is None or v != v else float(v)

    def goldone(d):
        body = s3.get_object(Bucket=GOLD_BUCKET, Key="%sdate=%s/data.parquet" % (GOLD_PREFIX, d))["Body"].read()
        t = pq.read_table(io.BytesIO(body))
        have = [c for c in cols if c in t.schema.names]
        return t.select(have).to_pylist()

    gold = {}
    with ThreadPoolExecutor(8) as ex:
        for rows in ex.map(goldone, dates):
            for r in rows:
                if r["account_id"] in want:
                    gold.setdefault(r["account_id"], {})[r["business_date"]] = {
                        "r": num(r.get("total_return_daily")), "mv": num(r.get("market_value_eod")), "flow": num(r.get("external_flow")),
                        "inc": num(r.get("income_return")) or 0.0, "inc_recv": num(r.get("income_received")) or 0.0,
                        "price_reason": r.get("holdings_price_return_reason")}
    reads["prefixes"].append(GOLD_BUCKET + "/" + GOLD_PREFIX)
    reads["objects"] += len(dates)
    print("gold partitions", len(dates), "accounts with series", len(gold), "of", len(accts))

    # ---- BD landed transactions (49 Financial's own silver_legacy), rows for the 90's accounts
    tdays = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BRONZE_BUCKET, Prefix=TXN_PREFIX, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            tdays.append(cp["Prefix"])
    wantn = {a.lstrip("0") for a in accts}
    nobj = [0]

    def txone(pref):
        r = s3.list_objects_v2(Bucket=BRONZE_BUCKET, Prefix=pref)
        out = []
        for o in r.get("Contents", []):
            if not o["Key"].endswith(".parquet"):
                continue
            t = pq.read_table(io.BytesIO(s3.get_object(Bucket=BRONZE_BUCKET, Key=o["Key"])["Body"].read()))
            have = [c for c in TXN_COLS if c in t.schema.names]
            for r2 in t.select(have).to_pylist():
                if str(r2.get("account_number")).strip().lstrip("0") in wantn:
                    out.append(r2)
            nobj[0] += 1
        return out

    txn = []
    with ThreadPoolExecutor(24) as ex:
        for rows in ex.map(txone, tdays):
            txn += rows
    reads["prefixes"].append(BRONZE_BUCKET + "/" + TXN_PREFIX)
    reads["objects"] += nobj[0]
    print("txn day partitions", len(tdays), "objects", nobj[0], "rows kept", len(txn))
    pickle.dump({"segs": S, "mem": mem, "bdacct": {a: bdacct[a] for a in accts}, "bd": bd, "gold": gold, "txn": txn, "reads": reads},
                open(OUT + "read90.pkl", "wb"))
    print("OK reads", {"prefixes": len(reads["prefixes"]), "objects": reads["objects"]})


if __name__ == "__main__":
    main()
