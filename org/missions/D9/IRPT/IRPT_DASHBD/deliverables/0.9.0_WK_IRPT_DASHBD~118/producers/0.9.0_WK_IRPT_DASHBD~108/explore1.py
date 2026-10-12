import pickle
import collections
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
rows = pickle.load(open(OUT + "table90.pkl", "rb"))
D = pickle.load(open(OUT + "read90.pkl", "rb"))


def tie(p, q, ab=1.0, rel=0.001):
    return abs(p - q) <= max(ab, rel * max(abs(p), abs(q)))


def grp(r):
    o, b = r["o"], r["b"]
    return (tie(b["bmv"], o["bmv"]), tie(b["emv"], o["emv"]), tie(b["nadd"], o["flow"]), tie(b["ngain"], o["gain"]))


for r in rows:
    r["grp"] = grp(r)
    o, b, v = r["o"], r["b"], r["v2"]
    g = D["gold"][r["a"]]
    seg = r["seg"]
    days = [d for d in sorted(g) if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None]
    r["nflowdays"] = sum(1 for d in days if abs(g[d]["flow"] or 0) > 0.005)
    r["nincdays"] = sum(1 for d in days if abs(g[d]["inc_recv"] or 0) > 0.005)
    r["signed_pp"] = (v["gross"] - v["opal"]) * 100
    r["gain_gap"] = b["ngain"] - o["gain"]
    r["gain_gap_over_mean_pp"] = (b["ngain"] - o["gain"]) / o["mean"] * 100 if o["mean"] else None
    r["minmv_over_peak"] = min([g[d]["mv"] or 0 for d in days] + [o["bmv"]]) / (o["peak"] or 1)
    r["bd_id_resid"] = b["emv"] - b["bmv"] - b["nadd"] - b["ngain"]
    r["fee_over_mean_pp"] = b["fees"] / o["mean"] * 100 if o["mean"] else None
    r["ret_gap_pp"] = v["diff_pp"]
print("group sizes", collections.Counter(r["grp"] for r in rows))
A = [r for r in rows if r["grp"] == (True, True, True, True)]
print("ALL-TIE n", len(A))
print(" flowdays>0", sum(1 for r in A if r["nflowdays"] > 0), " incdays>0", sum(1 for r in A if r["nincdays"] > 0), " fees!=0", sum(1 for r in A if abs(r["b"]["fees"]) > 0.005))
print(" minmv/peak<0.01", sum(1 for r in A if r["minmv_over_peak"] < 0.01), " <0.1", sum(1 for r in A if r["minmv_over_peak"] < 0.1))
print(" held==opal", sum(1 for r in A if r["b"]["held"] == r["v2"]["opal_days"]))
print(" bd twr None", sum(1 for r in A if r["b"]["twr"] is None))
print(" sign of signed_pp: bd>opal", sum(1 for r in A if r["signed_pp"] > 0), "bd<opal", sum(1 for r in A if r["signed_pp"] < 0))
print(" gap pp quantiles", sorted(round(r["ret_gap_pp"], 2) for r in A))
# dietz comparison
for nm, sel in (("ALLTIE", A),):
    c = collections.Counter()
    for r in sel:
        o, b = r["o"], r["b"]
        base = o["bmv"] if o["bmv"] else 0
        # simple (gain / bmv) and mean-balance
        dz = o["gain"] / o["mean"] if o["mean"] else None
        bd_g = r["v2"]["gross"]
        op = r["v2"]["opal"]
        c[("bd~dietzmean", abs(bd_g - dz) * 100 <= 0.35 if dz is not None else None, "opal~dietzmean", abs(op - dz) * 100 <= 0.35 if dz is not None else None)] += 1
    print(nm, c)
B = [r for r in rows if r["grp"] != (True, True, True, True)]
print("DOLLARGAP n", len(B))
c = collections.Counter()
for r in B:
    # does the gain gap over mean explain the signed return gap?
    ok = r["gain_gap_over_mean_pp"] is not None and abs(r["signed_pp"] - r["gain_gap_over_mean_pp"]) <= 0.35
    c[(r["grp"], ok)] += 1
print(c)
