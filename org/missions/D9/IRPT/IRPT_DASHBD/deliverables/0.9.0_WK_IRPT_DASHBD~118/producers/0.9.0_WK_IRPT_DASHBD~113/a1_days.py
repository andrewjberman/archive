"""~113 step 1: reproduce the 18 segments and 50 differing flow days; dump the day detail privately. Usage: python -I a1_days.py"""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
FT = ("Contribution", "Withdrawal")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)

segs18 = []
days50 = []
tot_flow_days = 0
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    tot_flow_days += len(gf)
    day = collections.defaultdict(list)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    tot_l = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for L in day.values() for t in L)
    tot_s = sum(gf.values())
    ok = abs(tot_l - tot_s) <= max(1.0, 0.001 * abs(tot_s))
    if ok:
        continue
    segs18.append(r["idx"])
    for d in sorted(set(day) | set(gf)):
        L = day.get(d, [])
        tl = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for t in L)
        sv = gf.get(d, 0.0)
        if abs(tl - sv) > max(1.0, 0.001 * abs(sv)):
            days50.append({"idx": r["idx"], "a": a, "day": d, "seg": seg, "served": sv, "bd_total": tl, "rows": L})
print("segments", len(segs18), "differing days", len(days50), "flow days of the 51", tot_flow_days)
print("flow days (served nonzero) in the 18:", sum(1 for r in rows if r["idx"] in set(segs18) for d, v in D["gold"][r["a"]].items() if r["seg"]["start"] <= d <= r["seg"]["end"] and v["flow"]))
pickle.dump({"segs18": segs18, "days50": days50}, open(OUT + "a1_days.pkl", "wb"))
print("row keys", sorted(days50[0]["rows"][0].keys()) if days50[0]["rows"] else None)
c = collections.Counter(d["idx"] for d in days50)
print("days per segment", sorted(c.values()))
c2 = collections.Counter((len(d["rows"]), d["served"] == 0.0) for d in days50)
print("(n_bd_rows, served_zero)", sorted(c2.items()))
