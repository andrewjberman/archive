import collections
rows = tie = relink = TOL = None  # all four are defined by the exec on the next line (static-scan declaration only)
exec(open("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/explore4.py").read().split("A = [r for r")[0])
B = [r for r in rows if r["grp"] != (True, True, True, True)]
print("B", len(B))
c = collections.Counter()
detail = collections.Counter()
for r in B:
    o, b, v = r["o"], r["b"], r["v2"]
    acc = b["eacc"] - b["bacc"]
    accrule = abs(r["o"]["gain"] + acc - b["ngain"]) <= max(1.0, 0.001 * abs(b["ngain"]))
    base = o["mean"]
    add = b["fees"] / base if base > 0 else 0.0
    gross = (1 + v["bdr"]) * (1 + add) - 1
    ok_conv = set()
    for conv in ("START", "MID", "END"):
        op = relink(r["dd"], conv)
        if abs(gross - op) * 100 <= TOL:
            ok_conv.add(conv + "_noaccr")
        if o["emv"] > 0 and o["bmv"] > 0:
            adj = (1 + op) * ((o["emv"] + b["eacc"]) / o["emv"]) / ((o["bmv"] + b["bacc"]) / o["bmv"]) - 1
            if abs(gross - adj) * 100 <= TOL:
                ok_conv.add(conv + "_accr")
    c[(accrule, bool(ok_conv))] += 1
    detail[(accrule, tuple(sorted(ok_conv)))] += 1
print("(accrual identity holds, closed by some convention/accrual restatement):", dict(c))
for k, v in sorted(detail.items(), key=lambda z: -z[1]):
    print(v, k)
# the dollars-identity per component
cmp = collections.Counter()
for r in B:
    o, b = r["o"], r["b"]
    comp = []
    if not tie(b["bmv"], o["bmv"]):
        comp.append("bmv=bacc" if abs((b["bmv"] - o["bmv"]) - b["bacc"]) <= max(1.0, 0.001 * abs(b["bacc"])) else "bmv_other")
    if not tie(b["emv"], o["emv"]):
        comp.append("emv=eacc" if abs((b["emv"] - o["emv"]) - b["eacc"]) <= max(1.0, 0.001 * abs(b["eacc"])) else "emv_other")
    acc = b["eacc"] - b["bacc"]
    comp.append("gain=dacc" if abs((b["ngain"] - o["gain"]) - acc) <= max(1.0, 0.001 * abs(acc)) else "gain_other")
    cmp[tuple(comp)] += 1
print(dict(cmp))
# accrual terms nonzero but values tie (group A)
A = [r for r in rows if r["grp"] == (True, True, True, True)]
print("A with nonzero accrual terms:", sum(1 for r in A if abs(r["b"]["bacc"]) > 0.005 or abs(r["b"]["eacc"]) > 0.005))
print("A: bd emv equal opal emv and eacc nonzero", sum(1 for r in A if abs(r["b"]["eacc"]) > 1.0))
