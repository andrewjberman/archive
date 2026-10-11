import pickle
import collections
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
rows = pickle.load(open(OUT + "table90.pkl", "rb"))
D = pickle.load(open(OUT + "read90.pkl", "rb"))


def tie(p, q, ab=1.0, rel=0.001):
    return abs(p - q) <= max(ab, rel * max(abs(p), abs(q)))


def near(p, q, tol=1.0):
    return abs(p - q) <= tol


for r in rows:
    o, b = r["o"], r["b"]
    r["grp"] = (tie(b["bmv"], o["bmv"]), tie(b["emv"], o["emv"]), tie(b["nadd"], o["flow"]), tie(b["ngain"], o["gain"]))
    r["resid"] = b["emv"] - b["bmv"] - b["nadd"] - b["ngain"]
    r["gg"] = b["ngain"] - o["gain"]
    r["acc"] = b["eacc"] - b["bacc"]

B = [r for r in rows if r["grp"] != (True, True, True, True)]
c = collections.Counter()
for r in B:
    cands = {"neg_fees": -r["b"]["fees"], "fees": r["b"]["fees"], "income": r["b"]["inc"], "neg_income": -r["b"]["inc"],
             "accrual_change": r["acc"], "neg_accrual_change": -r["acc"], "bd_resid": r["resid"], "neg_bd_resid": -r["resid"],
             "gap_bmv": r["b"]["bmv"] - r["o"]["bmv"], "neg_gap_bmv": r["o"]["bmv"] - r["b"]["bmv"],
             "gap_emv": r["b"]["emv"] - r["o"]["emv"], "neg_gap_emv": r["o"]["emv"] - r["b"]["emv"]}
    hit = tuple(sorted(k for k, v in cands.items() if near(v, r["gg"], max(1.0, 0.001 * abs(r["gg"])))))
    c[(r["grp"], hit)] += 1
for k, v in sorted(c.items(), key=lambda z: -z[1]):
    print(v, k)
print("---- BD own identity: emv-bmv-nadd-ngain tie-zero:", sum(1 for r in rows if abs(r["resid"]) <= 1.0), "of", len(rows))
print("---- bd resid ~ -(eacc-bacc):", sum(1 for r in rows if near(r["resid"], -r["acc"], 1.0)), " resid ~ +acc", sum(1 for r in rows if near(r["resid"], r["acc"], 1.0)))
# for dollar-gap segments, do the BD-side values equal a custodian/ledger quantity?
print("---- gap in bmv or emv: for each, gap vs accrual terms")
for nm, key in (("bmv", "bacc"), ("emv", "eacc")):
    n = m = 0
    for r in rows:
        gap = r["b"][nm] - r["o"][nm]
        if abs(gap) > max(1.0, 0.001 * abs(r["o"][nm])):
            n += 1
            if near(gap, r["b"][key], max(1.0, 0.001 * abs(gap))):
                m += 1
    print(nm, "gaps", n, "equal to BD accrual term", m)
