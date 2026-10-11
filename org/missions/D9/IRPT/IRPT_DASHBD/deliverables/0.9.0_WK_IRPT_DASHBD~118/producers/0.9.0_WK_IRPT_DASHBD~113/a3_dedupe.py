"""~113 step 3: test candidate cause 'identical BD transaction rows are present k>1 times on a day; the served flow counts the distinct row once'.
Counts only."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
R = pickle.load(open(OUT + "a1_days.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
mem = pickle.load(open(P + "members90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
FT = ("Contribution", "Withdrawal")
KEYS = ["account_number", "action", "external_flow", "income", "market_value", "return_date", "settle_date", "trade_date",
        "transaction_fee", "transaction_sub_type", "transaction_type", "account_fee"]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def sgn(t):
    return (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))


def key(t):
    return tuple(str(t.get(k)) for k in KEYS)


def tol(sv):
    return 0.005  # to the cent


C = collections.Counter()
per_seg = collections.defaultdict(list)
for d in R["days50"]:
    cnt = collections.Counter(key(t) for t in d["rows"])
    uniq = {}
    for t in d["rows"]:
        uniq[key(t)] = t
    ds = sum(sgn(t) for t in uniq.values())
    ok = abs(ds - d["served"]) <= 0.005
    mults = sorted(set(cnt.values()))
    C[("distinct_rows_sum_equals_served_to_cent", ok)] += 1
    C[("uniform_multiplicity", len(mults) == 1)] += 1
    per_seg[d["idx"]].append((ok, tuple(mults)))
    if not ok:
        print("UNREPRODUCED day", d["idx"], "served", d["served"], "distinct", ds, "mults", mults, "n", len(d["rows"]))
for k, v in sorted(C.items(), key=str):
    print(k, v)
print("segments fully reproduced by distinct-row rule:", sum(1 for s, L in per_seg.items() if all(o for o, _ in L)), "of", len(per_seg))
# multiplicity per segment
print("segment multiplicity sets:", sorted(set(tuple(sorted(set(m for _, mm in L for m in mm))) for L in per_seg.values())))
# in the 18 segments, ALL BD days (including matching): multiplicity
segs18 = set(R["segs18"])
txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)
M = collections.Counter()
for r in rows:
    if r["idx"] not in segs18:
        continue
    a, seg = r["a"], r["seg"]
    day = collections.defaultdict(list)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    for dd, L in day.items():
        cnt = collections.Counter(key(t) for t in L)
        M[("max_mult", max(cnt.values()))] += 1
print("BD flow-days in the 18 segments by max row multiplicity:", sorted(M.items()))
# the same for the 33 segments that reproduce
M2 = collections.Counter()
for r in rows:
    if r["idx"] not in M51 or r["idx"] in segs18:
        continue
    a, seg = r["a"], r["seg"]
    day = collections.defaultdict(list)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    for dd, L in day.items():
        cnt = collections.Counter(key(t) for t in L)
        M2[("max_mult", max(cnt.values()))] += 1
print("BD flow-days in the other 33 segments by max row multiplicity:", sorted(M2.items()))
