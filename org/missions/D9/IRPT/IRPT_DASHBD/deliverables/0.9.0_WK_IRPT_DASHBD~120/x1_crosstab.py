"""~120 step 1 (TO-DB-b-147): cross-tabulate the 51 contested segments from the private per-segment tables of workers 108, 111, 115.
No AWS, no write outside this folder. Prints counts only. Usage: python -I x1_crosstab.py
Outcome rule is copied from ~111 s6_record.py (O3, then O2, then O4, then O1); close flags from ~111 s2_per.pkl;
flow reproduction from ~115 c2_compare.py logic (each transaction id counted once, half a cent).
"""
import collections
import json
import pickle
import statistics

R = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/"
P = R + "0.9.0_WK_IRPT_DASHBD~108/"
OUT = R + "0.9.0_WK_IRPT_DASHBD~120/"
TOL = 0.005
FT = ("Contribution", "Withdrawal")
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
B = pickle.load(open(R + "0.9.0_WK_IRPT_DASHBD~115/c1_rows.pkl", "rb"))["rows"]
per = {s["idx"]: s for s in pickle.load(open(R + "0.9.0_WK_IRPT_DASHBD~111/s2_per.pkl", "rb"))}
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
assert len(M51) == 51 and len(per) == 51


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def sg(t):
    return (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))


def tie(p, q):
    return abs(p - q) <= max(1.0, 0.001 * max(abs(p), abs(q)))


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)
by = collections.defaultdict(list)
for t in B:
    by[str(t["account_number"]).strip().lstrip("0")].append(t)

table = []
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg, o, b = r["a"], r["seg"], r["o"], r["b"]
    g = D["gold"][a]
    ds_ = sorted(g)
    prev = [d for d in ds_ if d < seg["start"]]
    ser = [(d, g[d]["mv"], g[d]["flow"] or 0.0) for d in ds_ if (not prev or d >= prev[-1]) and d <= seg["end"] and g[d]["mv"] is not None]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    # outcome as ~111 (naive ledger, tolerance as ~111)
    day = collections.defaultdict(float)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]] += sg(t)
    ledger_ok = all(abs(day.get(d, 0.0) - gf.get(d, 0.0)) <= max(1.0, 0.001 * abs(gf.get(d, 0.0))) for d in set(day) | set(gf))
    dates_same = set(d for d, v in day.items() if abs(v) > 0.005) == set(gf)
    noise = [abs(ser[i][1] - ser[i - 1][1]) / ser[i - 1][1] for i in range(1, len(ser)) if ser[i][2] == 0.0 and ser[i - 1][1] and ser[i - 1][2] == 0.0]
    nz = statistics.median(noise) if len(noise) >= 5 else None
    ent = []
    for i in range(1, len(ser)):
        d, v1, F = ser[i]
        v0 = ser[i - 1][1]
        if F == 0.0 or not v0 or not nz or nz <= 0:
            continue
        rel = abs(F) / v0
        if rel < 5 * nz or rel < 0.01:
            continue
        if i + 1 >= len(ser):
            continue
        h = abs(F) / 2.0
        cand = []
        if i >= 2 and abs((v0 - ser[i - 2][1]) - F) <= h:
            cand.append("d-1")
        if abs((v1 - v0) - F) <= h:
            cand.append("d")
        if abs((ser[i + 1][1] - v1) - F) <= h:
            cand.append("d+1")
        ent.append(tuple(cand))
    n_det = len(ent)
    all_d = n_det > 0 and all(e == ("d",) for e in ent)
    if n_det == 0:
        oc = "O3"
    elif not (ledger_ok and dates_same):
        oc = "O2"
    elif not all_d:
        oc = "O4"
    else:
        oc = "O1"
    refined = "O3" if n_det == 0 else ("O4" if not all_d else "O1")
    # flow reproduction: each id once, at half a cent (as ~115)
    bday = collections.defaultdict(list)
    for t in by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            bday[str(t["return_date"])[:10]].append(t)
    n_days = 0
    bad = []
    bad_if_expense_left_out = []
    for dd in sorted(set(bday) | set(gf)):
        L = bday.get(dd, [])
        once = {}
        for i, t in enumerate(L):
            k = str(t.get("transaction_id")) if t.get("transaction_id") not in (None, "") else "NOID%d" % i
            once[k] = t
        ded = sum(sg(t) for t in once.values())
        ded_x = sum(sg(t) for t in once.values() if str(t.get("transaction_type")) != "Expense")
        sv = gf.get(dd, 0.0)
        n_days += 1
        if abs(ded - sv) > TOL:
            bad.append(dd)
            if abs(ded_x - sv) > TOL:
                bad_if_expense_left_out.append(dd)
    c = per[r["idx"]]["close"]
    ct = "both" if (c["START"] and c["MID"]) else ("START only" if c["START"] else ("MID only" if c["MID"] else "neither"))
    # do the four dollar items tie (DB-b-135)
    four = bool(tie(b["bmv"], o["bmv"]) and tie(b["emv"], o["emv"]) and tie(b["nadd"], o["flow"]) and tie(b["ngain"], o["gain"]))
    nflow = len(gf)
    # largest flow against prior value, by day (counts of days at or over 1 percent of the prior value)
    big = 0
    for i in range(1, len(ser)):
        if ser[i][2] != 0.0 and ser[i - 1][1] and abs(ser[i][2]) / ser[i - 1][1] >= 0.01:
            big += 1
    table.append({
        "idx": r["idx"], "outcome": oc, "refined": refined, "n_det": n_det, "reproduces_all_days": len(bad) == 0, "n_bad_days": len(bad),
        "reproduces_if_expense_row_left_out": len(bad_if_expense_left_out) == 0, "timing": ct, "end_closes": bool(c["END"]),
        "spread_lt_tol": per[r["idx"]]["spread_pp"] < 0.35, "four_tie": four, "flow_days": nflow, "n_days_compared": n_days,
        "days_flow_ge_1pct": big, "readable_flow_days": sum(1 for fl in per[r["idx"]]["flows"] if fl["readable"]),
        "fees_nonzero": bool(b["fees"]), "dates_same": dates_same, "end_in_ledger_all": True,
    })

pickle.dump(table, open(OUT + "x1_table.pkl", "wb"))
print("segments", len(table), "idx distinct", len({t["idx"] for t in table}))
print("outcomes", dict(collections.Counter(t["outcome"] for t in table)))
print("reproduces_all_days", dict(collections.Counter(t["reproduces_all_days"] for t in table)))
print("reproduces_if_expense_row_left_out", dict(collections.Counter(t["reproduces_if_expense_row_left_out"] for t in table)))
print("four_tie", dict(collections.Counter(t["four_tie"] for t in table)))
print("timing", dict(collections.Counter(t["timing"] for t in table)))
print("end_closes", dict(collections.Counter(t["end_closes"] for t in table)))
print("dates_same", dict(collections.Counter(t["dates_same"] for t in table)))
print("spread_lt_tol", dict(collections.Counter(t["spread_lt_tol"] for t in table)))
print("total flow days", sum(t["flow_days"] for t in table), "days compared", sum(t["n_days_compared"] for t in table))
print("CROSS-TAB: flow_reproduces_every_day / DB-b-138 outcome / timing closes the return")
ct = collections.Counter((t["reproduces_all_days"], t["outcome"], t["timing"]) for t in table)
for k in sorted(ct, key=str):
    print("  ", k, ct[k])
print("cells sum", sum(ct.values()))
print("PROFILE per outcome: segments with zero readable flow days / with >=1 day flow>=1pct / spread_lt_tol / fees_nonzero")
for oc in ("O1", "O2", "O3", "O4"):
    ts = [t for t in table if t["outcome"] == oc]
    if not ts:
        continue
    print("  ", oc, len(ts), sum(1 for t in ts if t["readable_flow_days"] == 0), sum(1 for t in ts if t["days_flow_ge_1pct"] > 0),
          sum(1 for t in ts if t["spread_lt_tol"]), sum(1 for t in ts if t["fees_nonzero"]))
print("PROFILE per timing: spread_lt_tol / O1 / O2 / O3")
for tm in ("both", "START only", "MID only", "neither"):
    ts = [t for t in table if t["timing"] == tm]
    if not ts:
        continue
    print("  ", tm, len(ts), sum(1 for t in ts if t["spread_lt_tol"]), sum(1 for t in ts if t["outcome"] == "O1"),
          sum(1 for t in ts if t["outcome"] == "O2"), sum(1 for t in ts if t["outcome"] == "O3"))
print("flow days in segments: min/median/max", min(t["flow_days"] for t in table), statistics.median(t["flow_days"] for t in table), max(t["flow_days"] for t in table))

print("REFINED (rule order re-applied with the ledger reproducing: O3, then O4, then O1):", dict(collections.Counter(t["refined"] for t in table)))
print("old -> refined:", dict(collections.Counter((t["outcome"], t["refined"]) for t in table)))
def grp(t):
    if not t["reproduces_all_days"]:
        return "G1_expense_row"
    if t["spread_lt_tol"]:
        return "G2_timing_immaterial"
    if t["timing"] != "both":
        return "G3_one_timing_only"
    return "G4_" + t["refined"]
gc = collections.Counter(grp(t) for t in table)
print("GROUPS", dict(gc), sum(gc.values()))
print("G3 split", dict(collections.Counter(t["timing"] for t in table if grp(t) == "G3_one_timing_only")))
print("G2 split by refined", dict(collections.Counter(t["refined"] for t in table if grp(t) == "G2_timing_immaterial")))
print("G1 timing/spread/refined", [(t["timing"], t["spread_lt_tol"], t["refined"]) for t in table if grp(t) == "G1_expense_row"])
print("G3 refined", dict(collections.Counter((t["timing"], t["refined"]) for t in table if grp(t) == "G3_one_timing_only")))
print("readable days total in O1/O3-refined:", sum(t["n_det"] for t in table))
print("segments with n_det==0:", sum(1 for t in table if t["n_det"] == 0), " n_det median", statistics.median(t["n_det"] for t in table))
pickle.dump(table, open(OUT + "x1_table.pkl", "wb"))
json.dump({"groups": dict(gc)}, open(OUT + "x1_groups.json", "w"))
