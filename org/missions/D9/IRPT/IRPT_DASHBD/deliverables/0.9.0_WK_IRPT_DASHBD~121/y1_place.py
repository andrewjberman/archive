"""~121 (TO-DB-b-148): re-derive, from the private per-segment tables of worker 108 only, the facts the two-axis proposal rests on.
Does not read ~111 s2_per.pkl or ~120 x1_table.pkl as inputs: closes are recomputed from the daily served series and the custodian point
(definitions: START/MID/END relink and TOL_PP 0.35 as in ~108 class90.py and ~111 s2_read.py; four-item dollar tie as ~108 table90.py/class90.py;
flow-day set equality as ~120 x1_crosstab.py). It then COMPARES to the earlier records' flags and prints any difference.
No AWS, no write inside the repo. Prints counts only. Usage: python -I y1_place.py
"""
import collections
import json
import pickle

R = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/"
P = R + "0.9.0_WK_IRPT_DASHBD~108/"
OUT = R + "0.9.0_WK_IRPT_DASHBD~121/"
TOL_PP = 0.35
FT = ("Contribution", "Withdrawal")

mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
per111 = {s["idx"]: s for s in pickle.load(open(R + "0.9.0_WK_IRPT_DASHBD~111/s2_per.pkl", "rb"))}
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
M31 = set(mem["BD_ACCRUED_INCOME_IN_VALUES_AND_GAINS"])
M8 = set(mem["REMAINDER"])
assert len(M51) == 51 and len(M31) == 31 and len(M8) == 8 and len(rows) == 90


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def tie(p, q):
    return abs(p - q) <= max(1.0, 0.001 * max(abs(p), abs(q)))


def relink(days, conv):
    p = 1.0
    for i, d in enumerate(days):
        if i == 0 or not d.get("mv") or not days[i - 1].get("mv") or d.get("flow") is None:
            p *= 1.0 + d["r"]
            continue
        v0, v1, fl = days[i - 1]["mv"], d["mv"], d["flow"]
        if conv == "START":
            den = v0 + fl
            r = v1 / den - 1.0 if den else d["r"]
        elif conv == "MID":
            den = v0 + fl / 2.0
            r = (v1 - fl / 2.0) / den - 1.0 if den else d["r"]
        else:
            r = (v1 - fl) / v0 - 1.0
        p *= 1.0 + r
    return p - 1.0


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)


def sg(t):
    return (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))


tab = []
for r in rows:
    a, seg, o, b, v = r["a"], r["seg"], r["o"], r["b"], r["v2"]
    g = D["gold"][a]
    dd = [dict(g[d], date=d) for d in sorted(g) if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None]
    base = o["mean"]
    add = b["fees"] / base if base > 0 else 0.0
    gross = (1 + v["bdr"]) * (1 + add) - 1
    rl = {c: relink(dd, c) for c in ("START", "MID", "END")}
    close = {c: abs(gross - rl[c]) * 100 <= TOL_PP for c in rl}
    spread = (max(rl.values()) - min(rl.values())) * 100
    gap_pp = {c: abs(gross - rl[c]) * 100 for c in rl}
    four = bool(tie(b["bmv"], o["bmv"]) and tie(b["emv"], o["emv"]) and tie(b["nadd"], o["flow"]) and tie(b["ngain"], o["gain"]))
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    day = collections.defaultdict(float)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]] += sg(t)
    days_same = set(d for d, x in day.items() if abs(x) > 0.005) == set(gf)
    grp = "M51" if r["idx"] in M51 else ("M31" if r["idx"] in M31 else "M8")
    tab.append({"idx": r["idx"], "grp": grp, "close": close, "n_close": sum(close.values()), "spread": spread, "gap_pp": gap_pp,
                "four": four, "days_same": days_same})

# --- comparison with the earlier records' flags (51)
diff = 0
for t in tab:
    if t["grp"] == "M51":
        c = per111[t["idx"]]["close"]
        if c != t["close"] or abs(per111[t["idx"]]["spread_pp"] - t["spread"]) > 1e-9:
            diff += 1
print("51: close flags or spread differing from ~111 s2_per.pkl:", diff)

t51 = [t for t in tab if t["grp"] == "M51"]
print("segments in the domain (dollars and flow days read both sides): ", len(tab), dict(collections.Counter(t["grp"] for t in tab)))
print("four dollar items tie, by group:", {g: sum(1 for t in tab if t["grp"] == g and t["four"]) for g in ("M51", "M31", "M8")})
print("flow-day sets equal, by group:", {g: sum(1 for t in tab if t["grp"] == g and t["days_same"]) for g in ("M51", "M31", "M8")})
print("plain return closes under >=1 of START/MID/END (no accrual scaling), by group:",
      {g: sum(1 for t in tab if t["grp"] == g and t["n_close"] >= 1) for g in ("M51", "M31", "M8")})
print("RECONCILES rule (>=1 timing closes AND four tie AND flow-day sets equal), by group:",
      {g: sum(1 for t in tab if t["grp"] == g and t["n_close"] >= 1 and t["four"] and t["days_same"]) for g in ("M51", "M31", "M8")})
print("51: closes per timing START/MID/END:", [sum(1 for t in t51 if t["close"][c]) for c in ("START", "MID", "END")])
print("51: n timings closing:", dict(collections.Counter(t["n_close"] for t in t51)))
exact = collections.Counter(tuple(c for c in ("START", "MID", "END") if t["close"][c]) for t in t51)
print("51: set of closing timings:", {"+".join(k) or "none": v for k, v in exact.items()})
print("TIMING cells (exactly-one rule):", dict(collections.Counter(
    ("TIMING_" + [c for c in ("START", "MID", "END") if t["close"][c]][0]) if t["n_close"] == 1 else "TIMING_NOT_DETERMINED" for t in t51)))
three = [t for t in t51 if t["spread"] < TOL_PP]
print("the three (spread of START/MID/END restated returns under 0.35 pp):", len(three))
for k, t in enumerate(three):
    print("  seg", k + 1, "START closes", t["close"]["START"], "MID closes", t["close"]["MID"], "END closes", t["close"]["END"],
          "four tie", t["four"], "days same", t["days_same"], "min gap to custodian across timings (pp, 2dp):",
          round(min(t["gap_pp"].values()), 2), "gaps S/M/E:", [round(t["gap_pp"][c], 2) for c in ("START", "MID", "END")])
print("51 segments by spread<tol:", dict(collections.Counter(t["spread"] < TOL_PP for t in t51)))
# placement cells
cells = collections.Counter()
for t in tab:
    reconciles = t["n_close"] >= 1 and t["four"] and t["days_same"]
    if not reconciles:
        cells[("RECONCILES_NO", "NOT_APPLICABLE")] += 1
    elif t["n_close"] == 1:
        cells[("RECONCILES_YES", "TIMING_" + [c for c in ("START", "MID", "END") if t["close"][c]][0])] += 1
    else:
        cells[("RECONCILES_YES", "TIMING_NOT_DETERMINED")] += 1
print("PLACEMENT of the 90 (counts):", {" / ".join(k): v for k, v in sorted(cells.items())}, sum(cells.values()))
cells51 = collections.Counter()
for t in t51:
    reconciles = t["n_close"] >= 1 and t["four"] and t["days_same"]
    key = ("RECONCILES_YES" if reconciles else "RECONCILES_NO",
           ("TIMING_" + [c for c in ("START", "MID", "END") if t["close"][c]][0]) if t["n_close"] == 1 else "TIMING_NOT_DETERMINED")
    cells51[key] += 1
print("PLACEMENT of the 51:", {" / ".join(k): v for k, v in sorted(cells51.items())}, sum(cells51.values()))
# the 51 split by the earlier group labels, for the decomposition of NOT_DETERMINED
json.dump({"cells51": {" / ".join(k): v for k, v in cells51.items()}, "cells90": {" / ".join(k): v for k, v in cells.items()}},
          open(OUT + "y1_cells.json", "w"))
