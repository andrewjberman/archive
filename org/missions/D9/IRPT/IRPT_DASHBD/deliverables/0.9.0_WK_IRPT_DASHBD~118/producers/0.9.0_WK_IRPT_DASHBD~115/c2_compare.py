"""~115 step 2: the comparison at the cent (half a cent) over all 51 segments. Counts and type names only on the console; day detail kept private.
Usage: python -I c2_compare.py"""
import collections
import json
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

# cross-check against ~108's first download (no id): same flow rows for the 51's accounts, naive?
txn108 = collections.defaultdict(list)
for t in D["txn"]:
    txn108[str(t["account_number"]).strip().lstrip("0")].append(t)

segs = [r for r in rows90 if r["idx"] in M51]
print("segments", len(segs))
no_id = sum(1 for t in B if t.get("external_flow") in FT and t.get("transaction_id") in (None, ""))
print("flow rows with no transaction id:", no_id)
seg_differ = 0
tot_days = 0
naive_diff = 0
rep = 0
nonrep = []
days_state = collections.Counter()
detail = []
seg_naive_differ = 0
seg_id_differ = 0
for r in segs:
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    day = collections.defaultdict(list)
    for t in by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]].append(t)
    nd = 0
    idd = 0
    for dd in sorted(set(day) | set(gf)):
        L = day.get(dd, [])
        once = {}
        for i, t in enumerate(L):
            k = str(t.get("transaction_id")) if t.get("transaction_id") not in (None, "") else "NOID%d" % i
            once[k] = t
        naive = sum(sg(t) for t in L)
        ded = sum(sg(t) for t in once.values())
        sv = gf.get(dd, 0.0)
        tot_days += 1
        n_ok = abs(naive - sv) <= TOL
        d_ok = abs(ded - sv) <= TOL
        if not n_ok:
            naive_diff += 1
            nd += 1
            if d_ok:
                rep += 1
            else:
                types = sorted({"%s|%s" % (t.get("transaction_type"), t.get("transaction_sub_type")) for t in L})
                nonrep.append((r["idx"], dd))
                detail.append({"idx": r["idx"], "day": dd, "rows": len(L), "ids": len(once), "served_zero": sv == 0.0, "types": types,
                               "naive_minus_served": naive - sv, "ids_minus_served": ded - sv})
        if not d_ok:
            idd += 1
    seg_naive_differ += 1 if nd else 0
    seg_id_differ += 1 if idd else 0
    if nd:
        seg_differ += 1
print("flow days (served nonzero or ledger-labelled), all 51:", tot_days)
print("segments with a naive-sum day differing at the cent:", seg_differ, " of 51; agree:", 51 - seg_differ)
print("segments where the id-once rule leaves a differing day:", seg_id_differ)
print("naive differing days:", naive_diff, "reproduced by id-once:", rep, "not reproduced:", len(nonrep))
print("not-reproduced days per segment count:", len(set(i for i, _ in nonrep)))
for d in detail:
    print("  rows", d["rows"], "ids", d["ids"], "served_zero", d["served_zero"], "types", d["types"])
# id sanity
amt = collections.defaultdict(set)
for t in B:
    if t.get("external_flow") in FT:
        amt[str(t.get("transaction_id"))].add((str(t["market_value"]), t["external_flow"], str(t["return_date"])[:10], str(t["account_number"]).lstrip("0")))
print("flow-row transaction ids:", len(amt), "ids with >1 distinct (amount, direction, day, account):", sum(1 for v in amt.values() if len(v) > 1))
# copies per id in segments naive-differing vs not
pickle.dump({"detail": detail, "nonrep": nonrep}, open(OUT + "c2_detail.pkl", "wb"))
summary = {"segments_total": len(segs), "segments_differ_naive": seg_differ, "segments_id_differ": seg_id_differ, "flow_days": tot_days,
           "naive_differing": naive_diff, "reproduced": rep, "not_reproduced": len(nonrep), "no_id_flow_rows": no_id}
json.dump(summary, open(OUT + "c2_summary.json", "w"), indent=1)
