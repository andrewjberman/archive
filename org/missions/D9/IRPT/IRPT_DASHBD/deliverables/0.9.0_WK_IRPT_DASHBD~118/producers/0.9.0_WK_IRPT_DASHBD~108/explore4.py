import pickle
import collections
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
rows = pickle.load(open(OUT + "table90.pkl", "rb"))
D = pickle.load(open(OUT + "read90.pkl", "rb"))
TOL = 0.35


def tie(p, q, ab=1.0, rel=0.001):
    return abs(p - q) <= max(ab, rel * max(abs(p), abs(q)))


def relink(days, conv):
    p = 1.0
    for i, d in enumerate(days):
        if i == 0 or not d.get("mv") or not days[i - 1].get("mv") or d.get("flow") is None:
            p *= 1.0 + d["r"]
            continue
        v0, v1, f = days[i - 1]["mv"], d["mv"], d["flow"]
        if conv == "START":
            den = v0 + f
            r = v1 / den - 1.0 if den else d["r"]
        elif conv == "MID":
            den = v0 + f / 2.0
            r = (v1 - f / 2.0) / den - 1.0 if den else d["r"]
        else:
            r = (v1 - f) / v0 - 1.0
        p *= 1.0 + r
    return p - 1.0


for r in rows:
    o, b = r["o"], r["b"]
    r["grp"] = (tie(b["bmv"], o["bmv"]), tie(b["emv"], o["emv"]), tie(b["nadd"], o["flow"]), tie(b["ngain"], o["gain"]))
    g = D["gold"][r["a"]]
    seg = r["seg"]
    r["dd"] = [dict(g[d], date=d) for d in sorted(g) if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None]
A = [r for r in rows if r["grp"] == (True, True, True, True)]
res = collections.Counter()
per = {}
for r in rows:
    o, b, v = r["o"], r["b"], r["v2"]
    bases = {"none": None, "bmv": o["bmv"], "avg2": (o["bmv"] + o["emv"]) / 2, "dmean": o["mean"]}
    hit = set()
    for conv in ("START", "MID", "END"):
        op = relink(r["dd"], conv)
        for bn, base in bases.items():
            add = 0.0 if base is None else (b["fees"] / base if base > 0 else 0.0)
            gross = (1 + v["bdr"]) * (1 + add) - 1
            if abs(gross - op) * 100 <= TOL:
                hit.add((conv, bn))
    per[id(r)] = hit
    for h in hit:
        res[(r["grp"] == (True, True, True, True), h)] += 1
for k, v in sorted(res.items(), key=lambda z: (not z[0][0], -z[1])):
    print(k, v)
print("A segments closed by at least one (convention x fee base):", sum(1 for r in A if per[id(r)]), "of", len(A))
print("ALL closed by at least one:", sum(1 for r in rows if per[id(r)]), "of", len(rows))
# envelope test (~73): gross inside min/max over conventions +/- tol
c = collections.Counter()
for r in rows:
    alts = [relink(r["dd"], cv) for cv in ("START", "MID", "END")]
    lo, hi = min(alts) - TOL / 100, max(alts) + TOL / 100
    c[(r["grp"] == (True, True, True, True), lo <= r["v2"]["gross"] <= hi)] += 1
print("gross within START/MID/END envelope (alltie?, in):", dict(c))
