"""TO-DB-b-31 (IRPT_DASHBD round 20, E1): measure the 226 inferred FLOW_TIMING segments. READ-ONLY (S3 list/get only; zero vendor calls).

Usage: python flow_measured_e1.py <repo_root> [--cache <pickle>]
Per segment: Modified Dietz over BD's bmv/emv/netAdditions with each Opal dated flow (gold column external_flow) weighted by the
fraction of the segment remaining after its date; midpoint control = every flow at weight 0.5; guard flows_match on the flow totals.
"""
import io
import json
import pickle
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R19 = P + "0.9.0_WK_IRPT_DASHBD~15/RESIDUE_NONCLOSURE_E2.json"
GROSS = P + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
PLAN = P + "0.9.0_WK_IRPT_DASHBD~6/BD_POPULATION_PLAN_E3.json"
TOL = 0.35
BASE_UNEXPLAINED = 3053
FLOW_COLUMN = "external_flow"
BRONZE_BUCKET = "opal-data-assets"
BRONZE_PREFIX = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/"
GOLD_BUCKET = "opal-data-49financial"
GOLD_PREFIX = "irpt/49financial/gold/account_return_daily/"


def _d(s):
    return date.fromisoformat(s)


def dietz(bmv, emv, na, flows, start, end, midpoint=False):
    """Modified Dietz. flows = [(date_str, amount)]; weight = days remaining after the flow date / segment days (0.5 at midpoint)."""
    span = (_d(end) - _d(start)).days
    if span <= 0:
        return None
    den = bmv
    for ds, f in flows:
        w = 0.5 if midpoint else (_d(end) - _d(ds)).days / span
        den += w * f
    if not den:
        return None
    return (emv - bmv - na) / den


def grade(acct, seg, bd_gross, point, flows):
    """One E1 row. point = {bmv, emv, na} (BD) or None; flows = [(date, amount)] from Opal's gold."""
    row = {"account": acct, "segment": seg, "bd_gross_return": bd_gross, "dietz_return": None, "abs_diff_pp_dietz": None,
           "abs_diff_pp_midpoint": None, "opal_flow_sum": None, "bd_net_additions": None, "flows_match": False,
           "verdict": "UNEXPLAINED"}
    if point is None or bd_gross is None:
        return row
    s = sum(f for _, f in flows)
    na = point["na"]
    row["opal_flow_sum"], row["bd_net_additions"] = s, na
    row["flows_match"] = bool(abs(s - na) <= max(1.00, 0.005 * abs(na)))
    dr = dietz(point["bmv"], point["emv"], na, flows, seg["start"], seg["end"])
    mr = dietz(point["bmv"], point["emv"], na, flows, seg["start"], seg["end"], midpoint=True)
    if dr is not None:
        row["dietz_return"] = dr
        row["abs_diff_pp_dietz"] = abs(dr - bd_gross) * 100.0
    if mr is not None:
        row["abs_diff_pp_midpoint"] = abs(mr - bd_gross) * 100.0
    if row["flows_match"] and row["abs_diff_pp_dietz"] is not None and row["abs_diff_pp_dietz"] <= TOL:
        row["verdict"] = "MEASURED_FLOW_TIMING"
    return row


def tally(rows):
    meas = sum(1 for r in rows if r["verdict"] == "MEASURED_FLOW_TIMING")
    ret = len(rows) - meas
    mid = sum(1 for r in rows if r["abs_diff_pp_midpoint"] is not None and r["abs_diff_pp_midpoint"] <= TOL)
    return {"segments": len(rows), "measured": meas, "returned_unexplained": ret,
            "unexplained_measured_basis": BASE_UNEXPLAINED + ret, "negative_control_within": mid}


def _key(a, s):
    return (a, s["start"], s["end"])


def read_bronze(s3, bd_accounts):
    from concurrent.futures import ThreadPoolExecutor

    def one(a):
        k = "%sacct=%s.json" % (BRONZE_PREFIX, a)
        for att in range(6):
            try:
                return a, json.loads(s3.get_object(Bucket=BRONZE_BUCKET, Key=k)["Body"].read().decode("utf-8"))
            except Exception:
                if att == 5:
                    raise
    out = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        for a, resp in ex.map(one, sorted(bd_accounts)):
            pts = {}
            for lv in resp.get("levels") or []:
                d = lv.get("descriptor") or {}
                if d.get("level") != "Account" or str(d.get("levelId")) != str(a):
                    continue
                for p in lv.get("dateRangePoints") or []:
                    dr = p.get("dateRange") or {}
                    if None in (p.get("beginningMarketValue"), p.get("endingMarketValue"), p.get("netAdditions")):
                        continue
                    pts[(str(dr.get("startDate"))[:10], str(dr.get("endDate"))[:10])] = {
                        "bmv": float(p["beginningMarketValue"]), "emv": float(p["endingMarketValue"]),
                        "na": float(p["netAdditions"])}
            out[str(a)] = pts
    return out


def read_gold(s3, accounts):
    import pyarrow.parquet as pq
    from concurrent.futures import ThreadPoolExecutor
    dates = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=GOLD_BUCKET, Prefix=GOLD_PREFIX, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("date="):
                dates.append(seg[5:])
    dates.sort()
    want = set(accounts)

    def one(d):
        for att in range(6):
            try:
                body = s3.get_object(Bucket=GOLD_BUCKET, Key="%sdate=%s/data.parquet" % (GOLD_PREFIX, d))["Body"].read()
                break
            except Exception:
                if att == 5:
                    raise
        return pq.read_table(io.BytesIO(body), columns=["account_id", "business_date", FLOW_COLUMN]).to_pylist()

    out = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for rows in ex.map(one, dates):
            for r in rows:
                if r["account_id"] in want and r[FLOW_COLUMN]:
                    out.setdefault(r["account_id"], []).append((str(r["business_date"])[:10], float(r[FLOW_COLUMN])))
    return out, len(dates)


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None

    def load(rel):
        return json.loads((root / rel).read_bytes().decode("utf-8"))

    flow_rows = [r for r in load(R19)["rows"] if r["reason"] == "FLOW_TIMING"]
    gross = {_key(r["account"], r["segment"]): r.get("bd_gross_return") for r in load(GROSS)["segments"]}
    bd_acct = {r["account"]: str(r["bd_account"]) for r in load(PLAN)["request_list"]}
    accts = sorted({r["account"] for r in flow_rows})
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            bronze, gold, nparts = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        bronze = read_bronze(s3, {bd_acct[a] for a in accts})
        gold, nparts = read_gold(s3, accts)
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((bronze, gold, nparts), f)
    rows = []
    for r in flow_rows:
        a, seg = r["account"], r["segment"]
        fl = [(d, f) for d, f in gold.get(a, []) if seg["start"] <= d <= seg["end"]]
        pt = (bronze.get(bd_acct[a]) or {}).get((seg["start"], seg["end"]))
        rows.append(grade(a, seg, gross.get(_key(a, seg)), pt, sorted(fl)))
    counts = tally(rows)
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~16", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-31",
           "tolerance_pp": TOL, "vendor_calls": 0, "counts": counts,
           "inputs": {"flow_column": FLOW_COLUMN, "gold_partitions_read": nparts,
                      "gold_prefix": "s3://%s/%s" % (GOLD_BUCKET, GOLD_PREFIX),
                      "bronze_prefix": "s3://%s/%s" % (BRONZE_BUCKET, BRONZE_PREFIX), "bd_accounts_read": len(bronze)},
           "rows": rows}
    (HERE / "FLOW_MEASURED_E1.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
