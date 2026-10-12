"""~117 step 3: naive vs each-transaction-id-once, same window/filter/tie as ~108 table90.py lines 44-47 and class90.py line 17. Counts only."""
import collections
import json
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OD = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~117/"
rows90 = pickle.load(open(P + "table90.pkl", "rb"))
D = pickle.load(open(OD + "s2_rows.pkl", "rb"))
by = collections.defaultdict(list)
for r in D["rows"]:
    by[str(r["account_number"]).strip().lstrip("0")].append(r)


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def tie(p, q):
    return abs(p - q) <= max(1.0, 0.001 * max(abs(p), abs(q)))


C = collections.Counter()
mv = collections.Counter()
noid = 0
conflict = 0
for r in rows90:
    seg = r["seg"]
    tr = [t for t in by[r["a"].lstrip("0")] if t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]]
    fl = [t for t in tr if t.get("external_flow") in ("Contribution", "Withdrawal")]
    naive = sum(f(t["market_value"]) for t in fl)
    seen = {}
    once = 0.0
    for i, t in enumerate(fl):
        tid = t.get("transaction_id")
        if tid is None or str(tid).strip() == "":
            noid += 1
            key = ("NOID", i)
        else:
            key = ("ID", str(tid))
        if key in seen:
            if abs(seen[key] - f(t["market_value"])) > 0.005:
                conflict += 1
            continue
        seen[key] = f(t["market_value"])
        once += f(t["market_value"])
    nb = tie(naive, r["b"]["nadd"])
    ob = tie(once, r["b"]["nadd"])
    C[("naive_matches_108", nb == tie(r["t"]["flow"], r["b"]["nadd"]))] += 1
    C[("naive", nb)] += 1
    C[("id_once", ob)] += 1
    if nb != ob:
        mv["to_tie" if ob else "to_not_tie"] += 1
    C[("seg_with_dup_ids", len(seen) != len(fl))] += 1
for k, v in sorted(C.items(), key=lambda z: str(z[0])):
    print(k, v)
print("moved", dict(mv), "flow rows without id", noid, "same id different amount", conflict)
res = {"naive_tie": C[("naive", True)], "naive_not": C[("naive", False)], "once_tie": C[("id_once", True)], "once_not": C[("id_once", False)],
       "moved_to_tie": mv["to_tie"], "moved_to_not_tie": mv["to_not_tie"], "noid": noid, "conflict": conflict,
       "naive_matches_108": C[("naive_matches_108", True)], "dup_segments": C[("seg_with_dup_ids", True)],
       "objects": D["objects"], "prefixes": D["prefixes"], "rows": len(D["rows"])}
open(OD + "s3_result.json", "w").write(json.dumps(res))
print(res)
