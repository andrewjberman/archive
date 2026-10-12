"""~111 step 2: per-segment read of the 51 against BD's own transaction rows and the daily value series (private pickles only, no AWS).
Prints counts only. Usage: python -I s2_read.py
"""
import collections
import pickle
import statistics

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~111/"
TOL_PP = 0.35
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
FLOWTYPES = ("Contribution", "Withdrawal")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


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
        elif conv == "END":
            r = (v1 - fl) / v0 - 1.0
        else:
            r = d["r"]
        p *= 1.0 + r
    return p - 1.0


def dstr(x):
    return None if x is None else str(x)[:10]


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)

per = []
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg, o, b, v = r["a"], r["seg"], r["o"], r["b"], r["v2"]
    g = D["gold"][a]
    ds = sorted(g)
    inseg = [d for d in ds if seg["start"] <= d <= seg["end"]]
    prev = [d for d in ds if d < seg["start"]]
    dd = [dict(g[d], date=d) for d in inseg if g[d]["r"] is not None]
    # gross as in class90
    base = o["mean"]
    add = b["fees"] / base if base > 0 else 0.0
    gross = (1 + v["bdr"]) * (1 + add) - 1
    rl = {c: relink(dd, c) for c in ("START", "MID", "END", "SERVED")}
    close = {c: abs(gross - rl[c]) * 100 <= TOL_PP for c in ("START", "MID", "END")}
    spread_pp = (max(rl[c] for c in ("START", "MID", "END")) - min(rl[c] for c in ("START", "MID", "END"))) * 100
    # daily value series: change on non-flow days = noise scale
    series = [(d, g[d]["mv"], g[d]["flow"] or 0.0) for d in ds if (not prev or d >= prev[-1]) and d <= seg["end"] and g[d]["mv"] is not None]
    noise = []
    for i in range(1, len(series)):
        if series[i][2] == 0.0 and series[i - 1][1]:
            noise.append(abs(series[i][1] - series[i - 1][1]) / series[i - 1][1])
    nz = statistics.median(noise) if noise else None
    # BD ledger flow rows in window
    tr = [t for t in txn_by[a.lstrip("0")] if t.get("external_flow") in FLOWTYPES and t.get("return_date")
          and seg["start"] <= dstr(t["return_date"]) <= seg["end"]]
    bd_by_ret = collections.defaultdict(float)
    for t in tr:
        amt = abs(f(t["market_value"]))
        bd_by_ret[dstr(t["return_date"])] += amt if t["external_flow"] == "Contribution" else -amt
    flow_days = [(i, s) for i, s in enumerate(series) if s[2] != 0.0 and i > 0 and seg["start"] <= s[0] <= seg["end"]]
    seg_out = {"idx": r["idx"], "n_gold_flow_days": len(flow_days), "n_bd_flow_rows": len(tr), "n_bd_flow_days": len(bd_by_ret),
               "close": close, "spread_pp": spread_pp, "noise": nz, "flows": []}
    for i, s in flow_days:
        d, v1, F = s
        v0 = series[i - 1][1]
        dlt = v1 - v0
        nxt = (series[i + 1][1] - v1) if i + 1 < len(series) else None
        # BD rows matching this amount (+-max(1, 0.1%)) by which date field
        match = {"return": False, "trade": False, "settle": False, "ret_next": False, "ret_prev": False}
        tol = max(1.0, 0.001 * abs(F))
        for t in tr:
            amt = abs(f(t["market_value"]))
            sg = 1.0 if t["external_flow"] == "Contribution" else -1.0
            if abs(sg * amt - F) <= tol or abs(sg * amt + F) <= tol and False:
                match["return"] |= dstr(t["return_date"]) == d
                match["trade"] |= dstr(t.get("trade_date")) == d
                match["settle"] |= dstr(t.get("settle_date")) == d
        # same-day total by return_date vs gold flow
        match["day_total_return"] = abs(bd_by_ret.get(d, 0.0) - F) <= tol
        # readability: flow big against the account's own non-flow daily moves
        rel = abs(F) / v0 if v0 else None
        readable = bool(nz is not None and v0 and rel >= 5 * nz and rel >= 0.01)
        enters = None
        if readable and nxt is not None:
            on_d = abs(dlt - F) <= abs(F) / 2
            on_n = abs(nxt - F) <= abs(F) / 2
            enters = "d" if (on_d and not on_n) else ("d+1" if (on_n and not on_d) else "both_or_neither")
        seg_out["flows"].append({"day": d, "readable": readable, "enters": enters, "match": match})
    per.append(seg_out)

print("segments", len(per))
C = collections.Counter()
for s in per:
    C[("close", tuple(sorted(c for c, v in s["close"].items() if v)))] += 1
    C[("has_gold_flow", s["n_gold_flow_days"] > 0)] += 1
    C[("has_bd_flow_rows", s["n_bd_flow_rows"] > 0)] += 1
    C[("spread_lt_0.35pp", s["spread_pp"] < TOL_PP)] += 1
    C[("spread_lt_0.7pp", s["spread_pp"] < 2 * TOL_PP)] += 1
    rd = [fl for fl in s["flows"] if fl["readable"]]
    C[("n_readable_flows>0", len(rd) > 0)] += 1
    for fl in s["flows"]:
        C[("flow_enters", fl["enters"] if fl["readable"] else "not_readable")] += 1
        for k, vv in fl["match"].items():
            C[("flow_match_" + k, bool(vv))] += 1
for k, v in sorted(C.items(), key=lambda z: str(z[0])):
    print(k, v)
print("flows total", sum(len(s["flows"]) for s in per))
pickle.dump(per, open(OUT + "s2_per.pkl", "wb"))
