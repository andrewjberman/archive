"""~113 step 10: test the rule 'count each transaction_id once' on EVERY BD flow day of the 18 segments (and the 50 differing days). Counts only."""
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


def sg(t):
    return (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))


by = collections.defaultdict(list)
for t in B:
    by[str(t["account_number"]).strip().lstrip("0")].append(t)
C = collections.Counter()
segok = collections.Counter()
kmatch = collections.Counter()
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
    allok = True
    for dd in sorted(set(day) | set(gf)):
        L = day.get(dd, [])
        ids = {}
        for t in L:
            ids[str(t["_extra"].get("transaction_id"))] = t
        tot = sum(sg(t) for t in ids.values())
        sv = gf.get(dd, 0.0)
        ok = abs(tot - sv) <= 0.005
        C[("differing" if (r["idx"], dd) in bad else "matching_before", "txnid_rule_reproduces_to_cent", ok)] += 1
        allok &= ok
    segok[allok] += 1
    # k vs number of portfolio groups of the account
    pg = {str(t["_extra"].get("portfolio_group")) for t in by[a.lstrip("0")]}
    ks = set()
    for dd, L in day.items():
        if (r["idx"], dd) in bad:
            cnt = collections.Counter(str(t["_extra"].get("transaction_id")) for t in L)
            ks |= set(cnt.values())
    kmatch[(len(ks) == 1, "k_equals_n_portfolio_groups_of_account" if ks == {len(pg)} else "k_differs:%s_vs_%d" % (sorted(ks), len(pg)))] += 1
for k, v in sorted(C.items(), key=str):
    print(k, v)
print("segments where the rule reproduces EVERY flow day to the cent:", segok[True], "of", segok[True] + segok[False])
print("k vs account portfolio-group count:", dict(kmatch))
# transaction_id uniqueness: distinct ids per (id) mapping to >1 different amounts?
amt = collections.defaultdict(set)
for t in B:
    if t.get("external_flow") in FT:
        amt[str(t["_extra"].get("transaction_id"))].add((str(t["market_value"]), t["external_flow"], str(t["return_date"])[:10]))
print("transaction_ids in the 17 accounts' flow rows:", len(amt), "ids with >1 distinct (amount, direction, return_date):", sum(1 for v in amt.values() if len(v) > 1))
