"""~111 step 5: why BD ledger flow day totals differ from served on some of the 51. Counts only."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
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
C = collections.Counter()
segtot = collections.Counter()
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    day = collections.defaultdict(list)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    tot_l = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for L in day.values() for t in L)
    tot_s = sum(gf.values())
    segtot[("segment_ledger_total_equals_served_total", abs(tot_l - tot_s) <= max(1.0, 0.001 * abs(tot_s)))] += 1
    for d, L in day.items():
        tl = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for t in L)
        if abs(tl - gf.get(d, 0.0)) > max(1.0, 0.001 * abs(gf.get(d, 0.0))):
            acts = tuple(sorted(set(t["action"] for t in L)))
            C[("mismatch_day", acts, "has_fee_row", any("Fee" in str(t["action"]) for t in L))] += 1
            # does excluding fee rows reconcile?
            tl2 = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for t in L if "Fee" not in str(t["action"]))
            C[("mismatch_day_reconciles_without_fee_rows", abs(tl2 - gf.get(d, 0.0)) <= max(1.0, 0.001 * abs(gf.get(d, 0.0))))] += 1
for k, v in sorted(list(C.items()) + list(segtot.items()), key=lambda z: str(z[0])):
    print(k, v)
