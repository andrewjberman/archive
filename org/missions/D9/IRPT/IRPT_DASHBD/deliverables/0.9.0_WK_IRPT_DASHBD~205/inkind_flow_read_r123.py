"""IRPT_DASHBD round 123, workstream B-49F (worker 0.9.0_WK_IRPT_DASHBD~205) -- DB-b-251, the in-kind-as-flow read.

Question (CTO round-123 analysis, ruling 2): with no same-day delivery leg in the feed (round 122), do the IC|RO
receipts of the leading security on 2026-04-21, counted as EXTERNAL IN-KIND INFLOWS, reconcile the holdings guard
of the flagged accounts within the manifest tolerance? The same receipts counted as OUTFLOWS are the direction control.

  flagged = the GRADED_DISAGREED accounts of the Financial account_return_daily partition of 2026-04-21.
  S = the first security of round 121's top_securities.
  receipt value v = sum of quantity x price over the custodian fact_trn rows of 2026-04-21 with tr_cd IC, sb_cd RO
  and security S (cusip, else ticker_symbol).
  receipt_accounts = accounts, flagged or not, whose receipt value is positive.
  cohort = flagged accounts with a receipt, a gold row on 2026-04-20 whose market_value_eod is positive, a non-null
  holdings_price_return, and carried_days 1 on 2026-04-21.
  V1, V0 = market_value_eod on 2026-04-21 and 2026-04-20; F = external_flow on 2026-04-21 (null is 0);
  p = holdings_price_return + income_return (null income is 0); tol = the 2026-04-21 manifest tolerance.
  With carried_days 1 the producer's linked chain is the single endpoint term, so the return with flow X is
  r(X) = (V1 - X) / V0 - 1 and diff(X) = |r(X) - p|. The receipt is added as an inflow (X = F + v), or as an
  outflow (X = F - v) for the direction control.
  agree_* = cohort accounts with diff <= tol; improved_after_inflow = diff(F + v) < diff(F).
  verdict = IN_KIND_RECONCILES when agree_after_inflow >= 0.95 x cohort; NOT_RECONCILED when it is <= 0.05 x cohort;
  otherwise PARTIAL.

GET only. Money is used inside this script to compare values; no dollar figure is printed or recorded. Writes one
counts-only private file under the worker's private evidence folder, and nothing else.

Usage: python -I <this file> <repo_root>
"""
import hashlib
import io
import json
import os
import sys
from pathlib import Path

FIRM_KEY = "49financial"
DAY0 = "2026-04-20"
DAY1 = "2026-04-21"
GUARD_GD = "GRADED_DISAGREED"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
QTY_REL = ("org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
           "0.9.0_WK_IRPT_DASHBD~198/RD_QTY_CHANGE_0421_R121.json")
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~205"
PRIVATE_NAME = "inkind_flow_read_r123_counts.json"
GOLD_COLS = ["account_id", "market_value_eod", "external_flow", "income_return",
             "holdings_price_return", "guard_state", "carried_days"]
TRN_COLS = ["account_id", "cusip", "ticker_symbol", "tr_cd", "sb_cd", "quantity", "price"]
BUCKETS = ("le_1x", "le_2x", "le_10x", "gt_10x")


class Reader(object):
    """GET only. There is deliberately no method that changes a remote object."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0

    def body(self, bucket, key):
        self.gets += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def table(body, cols):
    import pyarrow.parquet as pq
    return pq.read_table(io.BytesIO(body), columns=cols).to_pydict()


def fl(x):
    return None if x is None else float(x)


def chain_diff(r, p, flow):
    """The producer's endpoint return with external flow `flow`, against the guard's comparison return p."""
    return abs((r["V1"] - flow) / r["V0"] - 1.0 - p)


def counts(rows, receipts, tol):
    """rows: {account: state, V1, V0, F, price_r, income_r, carried}; receipts: {account: receipt value}."""
    cohort = []
    for a, v in receipts.items():
        r = rows.get(a)
        if r is None or not v > 0:
            continue
        if r["state"] != GUARD_GD or r["V0"] is None or not r["V0"] > 0:
            continue
        if r["price_r"] is None or r["carried"] != 1 or r["V1"] is None:
            continue
        cohort.append((r, v))
    out = {"receipt_accounts": sum(1 for v in receipts.values() if v > 0), "cohort": len(cohort),
           "agree_before": 0, "agree_after_inflow": 0, "agree_after_outflow": 0,
           "improved_after_inflow": 0, "diff_buckets_after_inflow": dict((k, 0) for k in BUCKETS)}
    for r, v in cohort:
        p = r["price_r"] + (r["income_r"] or 0.0)
        f = r["F"] or 0.0
        d0 = chain_diff(r, p, f)
        d1 = chain_diff(r, p, f + v)
        d2 = chain_diff(r, p, f - v)
        out["agree_before"] += 1 if d0 <= tol else 0
        out["agree_after_inflow"] += 1 if d1 <= tol else 0
        out["agree_after_outflow"] += 1 if d2 <= tol else 0
        out["improved_after_inflow"] += 1 if d1 < d0 else 0
        if d1 <= tol:
            k = "le_1x"
        elif d1 <= 2 * tol:
            k = "le_2x"
        elif d1 <= 10 * tol:
            k = "le_10x"
        else:
            k = "gt_10x"
        out["diff_buckets_after_inflow"][k] += 1
    n = out["cohort"]
    a = out["agree_after_inflow"]
    if n and a >= 0.95 * n:
        out["verdict"] = "IN_KIND_RECONCILES"
    elif n and a <= 0.05 * n:
        out["verdict"] = "NOT_RECONCILED"
    else:
        out["verdict"] = "PARTIAL"
    return out


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    sys.path.insert(0, repo)
    from lib import opal_naming
    security = json.loads(Path(repo, QTY_REL).read_bytes().decode("utf-8"))["top_securities"][0]["security"]
    src = json.loads(Path(repo, SOURCES_REL).read_bytes().decode("utf-8"))
    hits = [v for v in src.values() if isinstance(v, dict) and "positions_prefix" in v]
    if len(hits) != 1:
        print("STOP: sources.json carries %d entries with positions_prefix; exactly one is required" % len(hits))
        return 3
    ent = hits[0]
    reader = Reader()
    gold = {}
    tol = None
    for day in (DAY1, DAY0):
        addr = opal_naming.address("irpt", FIRM_KEY, "gold", "account_return_daily", "date=%s" % day)
        gbucket, _sep, gkey = addr[len("s3://"):].partition("/")
        prefix = gkey.rstrip("/") + "/"
        cols = GOLD_COLS if day == DAY1 else ["account_id", "market_value_eod"]
        gold[day] = table(reader.body(gbucket, prefix + "data.parquet"), cols)
        if day == DAY1:
            manifest = json.loads(reader.body(gbucket, prefix + "manifest.json").decode("utf-8"))
            tol = float(manifest["thresholds"]["tolerance"])
    g1, g0 = gold[DAY1], gold[DAY0]
    i0 = {a: i for i, a in enumerate(g0["account_id"])}
    rows = {}
    for i, a in enumerate(g1["account_id"]):
        j = i0.get(a)
        v0 = fl(g0["market_value_eod"][j]) if j is not None else None
        rows[a] = {"state": g1["guard_state"][i], "V1": fl(g1["market_value_eod"][i]), "V0": v0,
                   "F": fl(g1["external_flow"][i]), "price_r": fl(g1["holdings_price_return"][i]),
                   "income_r": fl(g1["income_return"][i]), "carried": g1["carried_days"][i]}
    flagged = sum(1 for s in g1["guard_state"] if s == GUARD_GD)
    t = table(reader.body(ent["bucket"], "%sdate=%s/data.parquet" % (ent["transactions_prefix"], DAY1)), TRN_COLS)
    receipts = {}
    trn_rows = len(t["account_id"])
    for i, a in enumerate(t["account_id"]):
        sec = t["cusip"][i] or t["ticker_symbol"][i]
        if t["tr_cd"][i] != "IC" or t["sb_cd"][i] != "RO" or sec != security:
            continue
        if t["quantity"][i] is None or t["price"][i] is None:
            continue
        receipts[a] = receipts.get(a, 0.0) + float(t["quantity"][i]) * float(t["price"][i])
    res = counts(rows, receipts, tol)
    res["tolerance"] = tol
    res["security"] = security
    res["flagged"] = flagged
    res["trn_rows"] = trn_rows
    res["receipts_outside_cohort"] = res["receipt_accounts"] - res["cohort"]
    res["flagged_with_receipt"] = sum(1 for a, v in receipts.items()
                                      if v > 0 and rows.get(a, {}).get("state") == GUARD_GD)
    res["s3_gets"] = reader.gets
    res["analysis_sha256"] = hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest()
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print("flagged=%d trn_rows=%d s3_gets=%d tolerance=%s" % (flagged, trn_rows, reader.gets, tol))
    for k in ("receipt_accounts", "flagged_with_receipt", "cohort", "agree_before", "agree_after_inflow",
              "agree_after_outflow", "improved_after_inflow", "receipts_outside_cohort", "verdict"):
        print("%s=%s" % (k, res[k]))
    print("diff_buckets_after_inflow=%s" % json.dumps(res["diff_buckets_after_inflow"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
