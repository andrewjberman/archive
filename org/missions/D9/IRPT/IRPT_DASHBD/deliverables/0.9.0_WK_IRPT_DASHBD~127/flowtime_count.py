"""~127 (TO-DB-b-158): count the accounts and flow-bearing days behind the 51 segments and restate the closes per timing.
Reads worker 108's private tables by path (members90, read90, table90); the closes rule is the one in ~121 y1_place.py
(START/MID/END relink, TOL_PP 0.35, four-item dollar tie, flow-day set equality). Prints counts only; writes counts to a private file.
Flow-bearing day = a date inside the segment [start, end] on which the SERVED daily series (read90 gold, column "flow") is non-zero;
the same (account, date) shared by two segments of one account is counted once.
Usage: python -I flowtime_count.py
"""
import collections
import json
import pickle
import statistics

R = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/"
P = R + "0.9.0_WK_IRPT_DASHBD~108/"
OUT = R + "0.9.0_WK_IRPT_DASHBD~127/"
TOL_PP = 0.35
FT = ("Contribution", "Withdrawal")

mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])


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


segs = []
for r in rows:
    a, seg, o, b, v = r["a"], r["seg"], r["o"], r["b"], r["v2"]
    g = D["gold"][a]
    dd = [dict(g[d], date=d) for d in sorted(g) if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None]
    base = o["mean"]
    add = b["fees"] / base if base > 0 else 0.0
    gross = (1 + v["bdr"]) * (1 + add) - 1
    close = {c: abs(gross - relink(dd, c)) * 100 <= TOL_PP for c in ("START", "MID", "END")}
    four = bool(tie(b["bmv"], o["bmv"]) and tie(b["emv"], o["emv"]) and tie(b["nadd"], o["flow"]) and tie(b["ngain"], o["gain"]))
    gf = {d for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    day = collections.defaultdict(float)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]] += sg(t)
    same = {d for d, x in day.items() if abs(x) > 0.005} == gf
    segs.append({"idx": r["idx"], "a": a, "close": close, "n": sum(close.values()), "four": four, "same": same, "gf": gf,
                 "in51": r["idx"] in M51})

placed = [s for s in segs if s["n"] >= 1 and s["four"] and s["same"]]
s51 = [s for s in segs if s["in51"]]
print("segments read:", len(segs), "in the member list of 51:", len(s51), "placed RESTATED_CLOSES by the rule (all 90):", len(placed))
print("member-list 51 equals rule-placed set:", {s["idx"] for s in s51} == {s["idx"] for s in placed})
print("51 each satisfy the rule:", sum(1 for s in s51 if s["n"] >= 1 and s["four"] and s["same"]))

c = {k: sum(1 for s in s51 if s["close"][k]) for k in ("START", "MID", "END")}
both = sum(1 for s in s51 if s["close"]["START"] and s["close"]["MID"])
start_only = sum(1 for s in s51 if s["close"]["START"] and not s["close"]["MID"])
mid_only = sum(1 for s in s51 if s["close"]["MID"] and not s["close"]["START"])
end_any = sum(1 for s in s51 if s["close"]["END"])
cells = collections.Counter(
    ("START" if s["close"]["START"] else "MID" if s["close"]["MID"] else "END") if s["n"] == 1 else "NOT_DETERMINED" for s in s51)
print("closes per timing START/MID/END:", c, "both:", both, "start_only:", start_only, "mid_only:", mid_only, "segments closing under END:", end_any)
print("placement:", dict(cells))

accts = {s["a"] for s in s51}
days = {(s["a"], d) for s in s51 for d in s["gf"]}
per = collections.Counter(a for a, _ in days)
perlist = [per.get(a, 0) for a in accts]
sum_segdays = sum(len(s["gf"]) for s in s51)
res = {
    "accounts": len(accts), "flow_bearing_days": len(days), "segment_day_sum": sum_segdays,
    "per_account": {"min": min(perlist), "median": statistics.median(perlist), "max": max(perlist)},
    "accounts_with_one_flow_day": sum(1 for x in perlist if x == 1),
    "segments_per_account_max": max(collections.Counter(s["a"] for s in s51).values()),
    "closes": {"end": c["END"], "start": c["START"], "mid": c["MID"], "both": both, "start_only": start_only, "mid_only": mid_only},
    "cells": dict(cells),
}
print(json.dumps(res))
json.dump(res, open(OUT + "counts.json", "w"))
