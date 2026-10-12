"""~113 step 5: population test of the uniform-multiplicity rule over every BD flow account-day in the private read (86 accounts with a served series).
Counts only."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
R = pickle.load(open(OUT + "a1_days.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
FT = ("Contribution", "Withdrawal")
KEYS = ["account_number", "action", "external_flow", "income", "market_value", "return_date", "settle_date", "trade_date",
        "transaction_fee", "transaction_sub_type", "transaction_type", "account_fee"]
bad = {(d["a"], d["day"]) for d in R["days50"]}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def key(t):
    return tuple(str(t.get(k)) for k in KEYS)


def sgn(t):
    return (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))


gold_by = {}
for a, g in D["gold"].items():
    gold_by[a.lstrip("0")] = g
by = collections.defaultdict(list)
for t in D["txn"]:
    if t.get("external_flow") in FT and t.get("return_date"):
        by[(str(t["account_number"]).strip().lstrip("0"), str(t["return_date"])[:10])].append(t)
C = collections.Counter()
ex = []
for (a, d), L in by.items():
    g = gold_by.get(a)
    if g is None or d not in g:
        C[("no_served_row_for_day",)] += 1
        continue
    sv = g[d]["flow"] or 0.0
    cnt = collections.Counter(key(t) for t in L)
    ks = set(cnt.values())
    tot = sum(sgn(t) for t in L)
    uniq = sum(sgn(t) for t in {key(t): t for t in L}.values())
    pat = "all_unique" if ks == {1} else ("uniform_k>1" if len(ks) == 1 else "mixed")
    eq_tot = abs(tot - sv) <= 0.005
    eq_uni = abs(uniq - sv) <= 0.005
    C[(pat, "served==total" if eq_tot else "", "served==distinct_sum" if eq_uni else "")] += 1
    if pat == "uniform_k>1" and eq_tot:
        ex.append((a, d, len(L), cnt.most_common(1)[0][1]))
for k, v in sorted(C.items(), key=str):
    print(k, v)
print("uniform_k>1 days where served equals the FULL total (counter-examples to the rule):", len(ex), "(n_rows,k):", [(n, k) for _, _, n, k in ex])
