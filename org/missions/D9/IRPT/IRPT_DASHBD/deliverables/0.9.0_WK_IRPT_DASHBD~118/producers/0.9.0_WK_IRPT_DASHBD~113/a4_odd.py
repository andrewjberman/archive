"""~113 step 4: the two days with repeated identical rows that are NOT among the 50 (private console)."""
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
bad = {(d["idx"], d["day"]) for d in R["days50"]}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def key(t):
    return tuple(str(t.get(k)) for k in KEYS)


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    day = collections.defaultdict(list)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    for dd, L in day.items():
        cnt = collections.Counter(key(t) for t in L)
        if max(cnt.values()) > 1 and (r["idx"], dd) not in bad:
            tl = sum((1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"])) for t in L)
            print("ODD seg", r["idx"], "in18" if r["idx"] in set(R["segs18"]) else "in33", dd, "served", g.get(dd, {}).get("flow"), "bdtotal", tl, "n", len(L), "mult", dict(collections.Counter(cnt.values())))
            for t in L:
                print("    ", t["external_flow"][:4], t["action"], f(t["market_value"]), str(t["return_date"])[:10], str(t["trade_date"])[:10], str(t["settle_date"])[:10], t["transaction_sub_type"])
