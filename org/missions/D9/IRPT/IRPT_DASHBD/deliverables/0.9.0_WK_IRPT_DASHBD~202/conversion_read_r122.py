"""IRPT_DASHBD round 122, workstream B-49F (worker 0.9.0_WK_IRPT_DASHBD~202) -- DB-b-248, the 2026-04-21 conversion read.

For each in-kind receipt of the leading security of 2026-04-21 (the IC|RO rows that round 121 counted), is there a
same-day delivery of another security in the same account, of matching value? The definitions are the ones in the
round-122 checker's docstring (issuer checks/r122/p122_conv.py); they are copied here, never imported.

  flagged = the GRADED_DISAGREED accounts of the Financial account_return_daily partition of 2026-04-21.
  S = the first security of round 121's top_securities.
  receipts = accounts whose sum of quantity x price over the IC|RO rows of S on 2026-04-21 is positive.
  legs = for each receipt account, the sum of (q0 - q1) x closing_price(04-20) over its other securities whose
  quantity fell between 2026-04-20 and 2026-04-21.
  Money is used only to compare values inside this script; no dollar figure is printed or recorded.

READ-ONLY. GET only: the account_return_daily data.parquet of 2026-04-21 (address from lib/opal_naming.py), the
custodian dim_position data.parquet of 2026-04-20 and 2026-04-21, and the custodian fact_trn data.parquet of
2026-04-21. The bucket and the prefixes are read FROM data/assets/scripts/gold/irpt_reporting/sources.json.
Writes: one counts-only private file under the worker's private evidence folder. Nothing else.

Usage: python -I <this file> <repo_root>
"""
import hashlib
import io
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

FIRM_KEY = "49financial"
DAY0 = "2026-04-20"
DAY1 = "2026-04-21"
GUARD_GD = "GRADED_DISAGREED"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
QTY_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~198/RD_QTY_CHANGE_0421_R121.json"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~202"
PRIVATE_NAME = "conversion_read_r122_counts.json"
TOL_PRIMARY = 0.01
TOL_SECONDARY = 0.05
TOP_N = 5
POS_COLS = ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled", "closing_price"]
TRN_COLS = ["account_id", "cusip", "ticker_symbol", "tr_cd", "sb_cd", "quantity", "price"]


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


def column_names(body):
    import pyarrow.parquet as pq
    return list(pq.ParquetFile(io.BytesIO(body)).schema_arrow.names)


def fl(x):
    return None if x is None else float(x)


def positions(t, dis):
    """(account, security) -> (quantity, closing_price) for the flagged accounts; a later row for a pair replaces an earlier one."""
    out = {}
    for i, a in enumerate(t["account_id"]):
        sec = t["cusip"][i] or t["ticker_symbol"][i]
        if a in dis and sec:
            out[(a, sec)] = (fl(t["quantity_settled_unsettled"][i]), fl(t["closing_price"][i]))
    return out


def transactions(t, dis):
    rows = []
    for i, a in enumerate(t["account_id"]):
        if a in dis:
            sec = (t["cusip"][i] or t["ticker_symbol"][i]) or None
            rows.append((a, sec, t["tr_cd"][i], t["sb_cd"][i], fl(t["quantity"][i]), fl(t["price"][i])))
    return rows


def tickers(t):
    """security -> ticker_symbol, read from the 04-20 position rows (public identifiers, used for words only)."""
    out = {}
    for i in range(len(t["account_id"])):
        sec = t["cusip"][i] or t["ticker_symbol"][i]
        if sec and t["ticker_symbol"][i]:
            out.setdefault(sec, t["ticker_symbol"][i])
    return out


def counts(S, p0, p1, trn):
    """p0, p1: {(account, security): (quantity, closing_price)}; trn: [(account, security_or_None, tr_cd, sb_cd, quantity, price)]."""
    v = defaultdict(float)
    for a, s, t, b, q, p in trn:
        if t == "IC" and b == "RO" and s == S and q is not None and p is not None:
            v[a] += q * p
    receipts = {a: x for a, x in v.items() if x > 0}
    legs = defaultdict(float)
    leg_acc = defaultdict(set)
    for (a, s), (q0, px0) in p0.items():
        if a not in receipts or s == S or q0 is None or px0 is None:
            continue
        q1 = (p1.get((a, s)) or (0.0, None))[0] or 0.0
        if q1 < q0:
            legs[a] += (q0 - q1) * px0
            leg_acc[s].add(a)
    n = len(receipts)
    with_leg = sum(1 for a in receipts if legs.get(a, 0.0) > 0)
    m1 = sum(1 for a, x in receipts.items() if abs(legs.get(a, 0.0) - x) <= TOL_PRIMARY * x)
    m5 = sum(1 for a, x in receipts.items() if abs(legs.get(a, 0.0) - x) <= TOL_SECONDARY * x)
    other_ic = len({a for a, s, t, b, q, p in trn if t == "IC" and s and s != S and a in receipts})
    top = sorted(leg_acc, key=lambda s: (-len(leg_acc[s]), s))[:TOP_N]
    trn_pairs = {(a, s) for a, s, _t, _b, _q, _p in trn if s}
    changed = {k for k in set(p0) | set(p1) if (p0.get(k) or (None,))[0] != (p1.get(k) or (None,))[0]}
    unexpl = Counter(s for (a, s) in changed if (a, s) not in trn_pairs)
    if n and m1 >= 0.95 * n:
        verdict = "EXCHANGE_LEGS_PRESENT"
    elif n and with_leg <= 0.05 * n:
        verdict = "CONVERSION_LEG_ABSENT"
    else:
        verdict = "MIXED"
    return {"receipts": n, "receipts_with_leg": with_leg, "matched_1pct": m1, "matched_5pct": m5,
            "receipts_with_other_ic_row": other_ic,
            "legs_by_security": [{"security": s, "accounts": len(leg_acc[s])} for s in top],
            "unexplained_by_security": [{"security": s, "pairs": unexpl[s]} for s in sorted(unexpl, key=lambda s: (-unexpl[s], s))],
            "verdict": verdict, "changed_pairs": len(changed), "changed_pairs_with_row": sum(1 for k in changed if k in trn_pairs)}


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
    bucket = ent["bucket"]
    addr = opal_naming.address("irpt", FIRM_KEY, "gold", "account_return_daily", "date=%s" % DAY1)
    gbucket, _sep, gkey = addr[len("s3://"):].partition("/")
    reader = Reader()
    g = table(reader.body(gbucket, gkey.rstrip("/") + "/data.parquet"), ["account_id", "guard_state"])
    dis = set(a for a, s in zip(g["account_id"], g["guard_state"]) if s == GUARD_GD)
    pos = {}
    tick = {}
    desc_cols = []
    for d in (DAY0, DAY1):
        body = reader.body(bucket, "%sdate=%s/data.parquet" % (ent["positions_prefix"], d))
        if d == DAY0:
            desc_cols = [c for c in column_names(body) if "desc" in c.lower() or "name" in c.lower()]
        t = table(body, POS_COLS)
        pos[d] = positions(t, dis)
        if d == DAY0:
            tick = tickers(t)
    trn = transactions(table(reader.body(bucket, "%sdate=%s/data.parquet" % (ent["transactions_prefix"], DAY1)), TRN_COLS), dis)
    res = counts(security, pos[DAY0], pos[DAY1], trn)
    res["flagged"] = len(dis)
    res["security"] = security
    res["legs_tickers"] = [tick.get(x["security"], "") for x in res["legs_by_security"]]
    res["unexplained_tickers"] = [{"ticker": tick.get(x["security"], ""), "pairs": x["pairs"]} for x in res["unexplained_by_security"]]
    res["desc_columns_on_positions"] = desc_cols
    res["s3_gets"] = reader.gets
    res["analysis_sha256"] = hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest()
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print("flagged=%d trn_rows=%d position_pairs_day0=%d position_pairs_day1=%d s3_gets=%d" % (len(dis), len(trn), len(pos[DAY0]), len(pos[DAY1]), reader.gets))
    for k in ("receipts", "receipts_with_leg", "matched_1pct", "matched_5pct", "receipts_with_other_ic_row", "verdict", "changed_pairs", "changed_pairs_with_row"):
        print("%s=%s" % (k, res[k]))
    print("legs_by_security=%s" % json.dumps(res["legs_by_security"]))
    print("legs_tickers=%s" % json.dumps(res["legs_tickers"]))
    print("unexplained_by_security=%s" % json.dumps(res["unexplained_by_security"]))
    print("unexplained_tickers=%s" % json.dumps(res["unexplained_tickers"]))
    print("desc_columns_on_positions=%s" % json.dumps(desc_cols))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
