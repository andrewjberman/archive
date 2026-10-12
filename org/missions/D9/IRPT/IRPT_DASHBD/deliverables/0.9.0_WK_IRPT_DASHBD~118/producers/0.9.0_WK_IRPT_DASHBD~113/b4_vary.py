"""~113 step 9: which landed columns differ between the k copies of a day's row? Names and counts only."""
import collections
import pickle

OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
R = pickle.load(open(OUT + "a1_days.pkl", "rb"))
B = pickle.load(open(OUT + "b2_rows.pkl", "rb"))["rows"]
by = collections.defaultdict(list)
for t in B:
    by[(str(t["account_number"]).strip().lstrip("0"), str(t["return_date"])[:10])].append(t)
varying = collections.Counter()
constant_all = None
ndays = 0
pos_contig = collections.Counter()
for d in R["days50"]:
    L = [t for t in by[(d["a"].lstrip("0"), d["day"])] if t.get("external_flow") in ("Contribution", "Withdrawal")]
    groups = collections.defaultdict(list)
    for t in L:
        flat = dict(t["_extra"])
        flat.update({k: v for k, v in t.items() if k not in ("_extra", "_pos", "_part")})
        groups[(t["action"], str(t["market_value"]), str(t["trade_date"]), str(t["settle_date"]))].append(flat)
    cols = set()
    for g, rr in groups.items():
        for c in rr[0]:
            if len({str(x.get(c)) for x in rr}) > 1:
                cols.add(c)
    for c in cols:
        varying[c] += 1
    ndays += 1
    pos = sorted(t["_pos"] for t in L)
    pos_contig[("positions_contiguous", pos[-1] - pos[0] + 1 == len(pos))] += 1
print("days", ndays)
print("columns that differ between copies (name: days of 50 on which it differs):", dict(varying))
print(dict(pos_contig))
# Is there a landed id column, and is it repeated?
ids = collections.Counter()
for d in R["days50"]:
    L = [t for t in by[(d["a"].lstrip("0"), d["day"])] if t.get("external_flow") in ("Contribution", "Withdrawal")]
    for c in ("transaction_id", "id", "txn_id", "account_id", "asset_id", "cusip", "description"):
        if c in L[0]["_extra"] or c in L[0]:
            vals = [str((t["_extra"].get(c) if c in t["_extra"] else t.get(c))) for t in L]
            ids[(c, "distinct_vals_ge_rows" if len(set(vals)) == len(vals) else "repeated")] += 1
print(dict(ids))
