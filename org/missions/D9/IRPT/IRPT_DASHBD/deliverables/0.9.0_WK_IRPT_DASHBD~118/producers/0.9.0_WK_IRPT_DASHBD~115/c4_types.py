"""~115 step 4: per flow-labelled type, on how many in-window flow days does it appear, and does the served day flow include it (day reproduced with it counted)
vs reproduced if that type were left out. Counts and type names only."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~115/"
TOL = 0.005
FT = ("Contribution", "Withdrawal")
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows90 = pickle.load(open(P + "table90.pkl", "rb"))
B = pickle.load(open(OUT + "c1_rows.pkl", "rb"))["rows"]
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def sg(t):
    return (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))


by = collections.defaultdict(list)
for t in B:
    by[str(t["account_number"]).strip().lstrip("0")].append(t)
appear = collections.Counter()
with_ok = collections.Counter()
without_ok = collections.Counter()
for r in rows90:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    day = collections.defaultdict(dict)
    for t in by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]][str(t["transaction_id"])] = t
    for dd, L in day.items():
        sv = gf.get(dd, 0.0)
        full = sum(sg(t) for t in L.values())
        for ty in {(t["transaction_type"], t["transaction_sub_type"], t["action"]) for t in L.values()}:
            appear[ty] += 1
            if abs(full - sv) <= TOL:
                with_ok[ty] += 1
            wo = sum(sg(t) for t in L.values() if (t["transaction_type"], t["transaction_sub_type"], t["action"]) != ty)
            if abs(wo - sv) <= TOL:
                without_ok[ty] += 1
print("per (type, subtype, action): days it appears on | day reproduced with it counted | day reproduced if it were left out")
for ty, n in sorted(appear.items(), key=str):
    print("  ", ty, n, with_ok[ty], without_ok[ty])
