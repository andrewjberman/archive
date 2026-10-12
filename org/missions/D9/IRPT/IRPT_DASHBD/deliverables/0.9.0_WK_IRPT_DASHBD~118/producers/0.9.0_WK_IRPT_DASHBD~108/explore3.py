import pickle
import collections
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
rows = pickle.load(open(OUT + "table90.pkl", "rb"))
D = pickle.load(open(OUT + "read90.pkl", "rb"))
TOL = 0.35


def tie(p, q, ab=1.0, rel=0.001):
    return abs(p - q) <= max(ab, rel * max(abs(p), abs(q)))


for r in rows:
    o, b = r["o"], r["b"]
    r["grp"] = (tie(b["bmv"], o["bmv"]), tie(b["emv"], o["emv"]), tie(b["nadd"], o["flow"]), tie(b["ngain"], o["gain"]))
    r["acc"] = b["eacc"] - b["bacc"]
    r["gg"] = b["ngain"] - o["gain"]
    g = D["gold"][r["a"]]
    seg = r["seg"]
    r["days"] = [d for d in sorted(g) if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None]
    r["mvs"] = [g[d]["mv"] or 0.0 for d in r["days"]]

A = [r for r in rows if r["grp"] == (True, True, True, True)]
B = [r for r in rows if r["grp"] != (True, True, True, True)]
print("A", len(A), "B", len(B))
# fee-base options for A and all
def gap_pp(r, add):
    v = r["v2"]
    gross = (1 + v["bdr"]) * (1 + add) - 1
    return abs(gross - v["opal"]) * 100


for nm, S in (("A", A), ("B", B), ("ALL", rows)):
    c = collections.Counter()
    for r in S:
        o, b = r["o"], r["b"]
        fee = b["fees"]
        bases = {"bmv": o["bmv"], "emv": o["emv"], "avg2": (o["bmv"] + o["emv"]) / 2, "daily_mean": o["mean"], "peak": o["peak"]}
        for k, base in bases.items():
            if base and base > 0 and gap_pp(r, fee / base) <= TOL:
                c[k] += 1
        if gap_pp(r, 0.0) <= TOL:
            c["no_fee_already_within"] += 1
    print(nm, "fee-base closes gap:", dict(c))
# net vs gross: is the raw BD twr within tol of opal (i.e. v2 fee add-back created the gap)?
c = collections.Counter()
for r in rows:
    v = r["v2"]
    c[(abs(v["bdr"] - v["opal"]) * 100 <= TOL, r["grp"] == (True, True, True, True), abs(r["b"]["fees"]) > 0.005)] += 1
print("raw bd twr vs opal within tol (rawwithin, alltie, fees!=0):", dict(c))
# size of flows
c = collections.Counter()
for r in A:
    o = r["o"]
    c["flow_share>=5%" if o["mean"] and abs(o["flow"]) / o["mean"] >= 0.05 else "flow_small"] += 1
print("A flow share", dict(c))
c = collections.Counter()
for r in A:
    o = r["o"]
    # volatility of balance across the segment
    mvs = r["mvs"]
    rng = (max(mvs) - min(mvs)) / (o["mean"] or 1)
    c["bal_range>=20%" if rng >= 0.2 else "bal_range<20%"] += 1
print("A balance range", dict(c))
# opal gross price-only link (income removed) vs BD gross
g = D["gold"]
c = collections.Counter()
for r in rows:
    gd = g[r["a"]]
    px = 1.0
    for d in r["days"]:
        px *= 1 + (gd[d]["r"] - gd[d]["inc"])
    px -= 1
    c[abs(r["v2"]["gross"] - px) * 100 <= TOL] += 1
print("price-only link within tol of BD gross:", dict(c))
# accrual restatement of the opal return (ratio form)
c = collections.Counter()
for r in rows:
    o, b = r["o"], r["b"]
    if o["emv"] > 0 and o["bmv"] > 0:
        adj = (1 + r["v2"]["opal"]) * ((o["emv"] + b["eacc"]) / o["emv"]) / ((o["bmv"] + b["bacc"]) / o["bmv"]) - 1
        c[(r["grp"] == (True, True, True, True), abs(r["v2"]["gross"] - adj) * 100 <= TOL)] += 1
    else:
        c[("nobase", r["grp"] == (True, True, True, True))] += 1
print("accrual-restated opal within tol of BD gross (alltie?, ok):", dict(c))
print("accrual terms nonzero among A:", sum(1 for r in A if abs(r["b"]["bacc"]) > 0.005 or abs(r["b"]["eacc"]) > 0.005), "of", len(A))
