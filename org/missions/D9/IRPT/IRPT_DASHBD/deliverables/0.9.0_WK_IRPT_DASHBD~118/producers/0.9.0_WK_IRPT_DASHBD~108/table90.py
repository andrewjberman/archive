"""Per-segment two-sided table for the 90 (private output). Usage: python -I table90.py"""
import json
import pickle
import collections
from pathlib import Path

OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
D = pickle.load(open(OUT + "read90.pkl", "rb"))
V2 = json.loads(Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~35/TIEOUT_COMPOUND_V2.json").read_bytes().decode("utf-8"))
v2 = {(x["account"], x["segment"]["start"], x["segment"]["end"]): x for x in V2["segments"]}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


txn_by = collections.defaultdict(list)
for r in D["txn"]:
    txn_by[str(r["account_number"]).strip().lstrip("0")].append(r)

rows = []
for s in D["segs"]:
    a, seg = s["account"], s["segment"]
    g = D["gold"][a]
    ds = sorted(g)
    inseg = [d for d in ds if seg["start"] <= d <= seg["end"]]
    days = [d for d in inseg if g[d]["r"] is not None]
    prev = [d for d in ds if d < seg["start"]]
    prevd = prev[-1] if prev else inseg[0]
    o_bmv = g[prevd]["mv"] or 0.0
    o_emv = g[days[-1]]["mv"] or 0.0
    o_flow = sum(g[d]["flow"] or 0.0 for d in days)
    o_gain = o_emv - o_bmv - o_flow
    o_inc = sum(g[d]["inc_recv"] or 0.0 for d in days)
    b = D["bd"][D["bdacct"][a]][(seg["start"], seg["end"])]
    bmv, emv, nadd, ngain = f(b.get("beginningMarketValue")), f(b.get("endingMarketValue")), f(b.get("netAdditions")), f(b.get("netGains"))
    fees, inc = f(b.get("fees")), f(b.get("income"))
    x = v2[(a, seg["start"], seg["end"])]
    mean = sum((g[d]["mv"] or 0.0) for d in days) / len(days)
    # BD ledger rows in window
    tr = [t for t in txn_by[a.lstrip("0")] if t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]]
    t_flow = sum(f(t["market_value"]) for t in tr if t.get("external_flow") in ("Contribution", "Withdrawal"))
    t_inc = sum(f(t["income"]) for t in tr)
    t_fee = sum(f(t.get("transaction_fee")) + f(t.get("account_fee")) for t in tr)
    rows.append({"idx": D["mem"][len(rows)], "a": a, "seg": seg, "o": {"bmv": o_bmv, "emv": o_emv, "flow": o_flow, "gain": o_gain, "inc": o_inc, "mean": mean,
                 "days": len(days), "peak": max([g[d]["mv"] or 0.0 for d in days] + [o_bmv])},
                 "b": {"bmv": bmv, "emv": emv, "nadd": nadd, "ngain": ngain, "fees": fees, "inc": inc, "held": b.get("daysHeld"), "twr": b.get("twr"),
                       "bacc": f(b.get("beginningAccrual")), "eacc": f(b.get("endingAccrual")), "perf_bmv": f(b.get("performingBmv")),
                       "perf_emv": f(b.get("performingEmv")), "pos_bmv": f(b.get("positionOnlyBmv")), "pos_emv": f(b.get("positionOnlyEmv"))},
                 "t": {"n": len(tr), "flow": t_flow, "inc": t_inc, "fee": t_fee},
                 "v2": {"opal": x["opal_return"], "gross": x["bd_gross_return"], "bdr": x["bd_return"], "diff_pp": x["abs_diff_pp"], "bd_days": x["bd_days_held"], "opal_days": x["opal_days"]}})
pickle.dump(rows, open(OUT + "table90.pkl", "wb"))
(Path(OUT + "table90.json")).write_bytes((json.dumps(rows, indent=1) + "\n").encode("utf-8"))


def tie(p, q, ab=1.0, rel=0.001):
    return abs(p - q) <= max(ab, rel * max(abs(p), abs(q)))


C = collections.Counter()
for r in rows:
    o, b = r["o"], r["b"]
    k = (tie(b["bmv"], o["bmv"]), tie(b["emv"], o["emv"]), tie(b["nadd"], o["flow"]), tie(b["ngain"], o["gain"]))
    C[k] += 1
print("ties (bmv, emv, nadd, ngain):")
for k, v in sorted(C.items(), key=lambda z: -z[1]):
    print(k, v)
print("n", len(rows), "no txn rows:", sum(1 for r in rows if r["t"]["n"] == 0))
