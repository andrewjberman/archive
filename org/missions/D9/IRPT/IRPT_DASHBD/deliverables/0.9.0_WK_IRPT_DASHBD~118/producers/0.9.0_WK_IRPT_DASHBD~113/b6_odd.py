"""~113 step 11: the one non-differing flow day on which the transaction_id rule breaks (private console)."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
R = pickle.load(open(OUT + "a1_days.pkl", "rb"))
B = pickle.load(open(OUT + "b2_rows.pkl", "rb"))["rows"]
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
FT = ("Contribution", "Withdrawal")
segs18 = set(R["segs18"])
bad = {(d["idx"], d["day"]) for d in R["days50"]}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


by = collections.defaultdict(list)
for t in B:
    by[str(t["account_number"]).strip().lstrip("0")].append(t)
for r in rows:
    if r["idx"] not in segs18:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    day = collections.defaultdict(list)
    for t in by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    for dd in sorted(set(day) | set(gf)):
        L = day.get(dd, [])
        ids = {str(t["_extra"].get("transaction_id")): t for t in L}
        tot = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for t in ids.values())
        sv = gf.get(dd, 0.0)
        if abs(tot - sv) > 0.005 and (r["idx"], dd) not in bad:
            print("seg", r["idx"], dd, "served", sv, "idrule", tot, "rows", len(L), "ids", len(ids))
            pgs = {str(t["_extra"].get("portfolio_group")) for t in by[a.lstrip("0")]}
            print("account portfolio groups", len(pgs))
            for t in L:
                print("   ", t["external_flow"][:4], f(t["market_value"]), "txid=", str(t["_extra"].get("transaction_id")), "pg_hash=", hash(str(t["_extra"].get("portfolio_group"))) % 1000, "part", t["_part"], "pos", t["_pos"], str(t["_extra"].get("_source_file"))[-12:])
