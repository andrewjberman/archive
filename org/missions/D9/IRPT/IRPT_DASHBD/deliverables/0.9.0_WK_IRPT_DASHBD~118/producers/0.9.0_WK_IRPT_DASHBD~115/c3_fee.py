"""~115 step 3: the not-reproduced day and the 3 ids with more than one distinct tuple. Private console; prints types, flags, counts (no ids, no amounts)."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~115/"
FT = ("Contribution", "Withdrawal")
D = pickle.load(open(P + "read90.pkl", "rb"))
rows90 = pickle.load(open(P + "table90.pkl", "rb"))
B = pickle.load(open(OUT + "c1_rows.pkl", "rb"))["rows"]
det = pickle.load(open(OUT + "c2_detail.pkl", "rb"))
(idx, day), = det["nonrep"]
r = [x for x in rows90 if x["idx"] == idx][0]
a = r["a"].lstrip("0")
print("nonrep day: segment-has-days-in-window", r["seg"]["start"] <= day <= r["seg"]["end"])
L = [t for t in B if str(t["account_number"]).strip().lstrip("0") == a and str(t["return_date"])[:10] == day]
print("all ledger rows on that return_date for the account:", len(L))
for t in L:
    print("  ", {k: (t.get(k) if k in ("external_flow", "transaction_type", "transaction_sub_type", "action") else ("set" if t.get(k) not in (None, 0, 0.0, "") else t.get(k)))
                 for k in ("external_flow", "transaction_type", "transaction_sub_type", "action", "account_fee", "transaction_fee")},
          "pg_set", t.get("portfolio_group") not in (None, ""))
# how many 'Expense' external_flow rows exist at all in the 51 accounts' rows
c = collections.Counter((t.get("external_flow"), t.get("transaction_type"), t.get("transaction_sub_type")) for t in B if t.get("external_flow") in FT)
print("flow-labelled (external_flow, type, subtype) counts over the 49 accounts, all dates:")
for k, v in sorted(c.items(), key=str):
    print("  ", k, v)
# collision check within an (account, day)
grp = collections.defaultdict(lambda: collections.defaultdict(set))
for t in B:
    if t.get("external_flow") in FT:
        grp[(str(t["account_number"]).lstrip("0"), str(t["return_date"])[:10])][str(t.get("transaction_id"))].add((str(t["market_value"]), t["external_flow"]))
print("ids with >1 distinct (amount, direction) inside one (account, day):", sum(1 for g in grp.values() for v in g.values() if len(v) > 1))
