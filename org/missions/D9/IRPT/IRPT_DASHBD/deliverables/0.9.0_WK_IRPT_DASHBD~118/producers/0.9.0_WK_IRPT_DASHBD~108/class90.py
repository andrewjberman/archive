"""TO-DB-b-135: class the 90 by cause from the two-sided dollar read. Reads private pickles only (no AWS). Usage: python -I class90.py <repo_root>
Rules are applied in the order listed; the first that holds takes the segment. Counts only go to the repo record.
"""
import collections
import json
import pickle
from pathlib import Path

OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~108/UNCLASSED_90.json"
TOL_PP = 0.35
D = pickle.load(open(OUT + "read90.pkl", "rb"))
rows = pickle.load(open(OUT + "table90.pkl", "rb"))


def tie(p, q):
    return abs(p - q) <= max(1.0, 0.001 * max(abs(p), abs(q)))


def relink(days, conv):
    p = 1.0
    for i, d in enumerate(days):
        if i == 0 or not d.get("mv") or not days[i - 1].get("mv") or d.get("flow") is None:
            p *= 1.0 + d["r"]
            continue
        v0, v1, f = days[i - 1]["mv"], d["mv"], d["flow"]
        if conv == "START":
            den = v0 + f
            r = v1 / den - 1.0 if den else d["r"]
        elif conv == "MID":
            den = v0 + f / 2.0
            r = (v1 - f / 2.0) / den - 1.0 if den else d["r"]
        else:
            r = (v1 - f) / v0 - 1.0
        p *= 1.0 + r
    return p - 1.0


C_ACC = "BD_ACCRUED_INCOME_IN_VALUES_AND_GAINS"
C_FLOW = "FLOW_TIMING_CONVENTION_DOLLARS_TIE"
members = collections.defaultdict(list)
info = collections.Counter()
for r in rows:
    o, b, v = r["o"], r["b"], r["v2"]
    g = D["gold"][r["a"]]
    seg = r["seg"]
    dd = [dict(g[d], date=d) for d in sorted(g) if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None]
    tb, te, tn, tg = tie(b["bmv"], o["bmv"]), tie(b["emv"], o["emv"]), tie(b["nadd"], o["flow"]), tie(b["ngain"], o["gain"])
    dacc = b["eacc"] - b["bacc"]
    ident = False
    if tn and not (tb and te and tg):
        ok_b = tb or abs((b["bmv"] - o["bmv"]) - b["bacc"]) <= max(1.0, 0.001 * abs(b["bacc"]))
        ok_e = te or abs((b["emv"] - o["emv"]) - b["eacc"]) <= max(1.0, 0.001 * abs(b["eacc"]))
        ok_g = abs((b["ngain"] - o["gain"]) - dacc) <= max(1.0, 0.001 * abs(dacc))
        ident = ok_b and ok_e and ok_g
    base = o["mean"]
    add = b["fees"] / base if base > 0 else 0.0
    gross = (1 + v["bdr"]) * (1 + add) - 1
    close_acc = {}
    for conv in ("START", "MID", "END"):
        op = relink(dd, conv)
        close_acc[conv] = bool(o["emv"] > 0 and o["bmv"] > 0 and abs(gross - ((1 + op) * ((o["emv"] + b["eacc"]) / o["emv"]) / ((o["bmv"] + b["bacc"]) / o["bmv"]) - 1)) * 100 <= TOL_PP)
    close_flow = {conv: abs(gross - relink(dd, conv)) * 100 <= TOL_PP for conv in ("START", "MID")}
    if ident and any(close_acc.values()):
        c = C_ACC
        info[("acc_closing_by", "END only" if (close_acc["END"] and not (close_acc["START"] or close_acc["MID"])) else "START_or_MID")] += 1
        info[("acc_END_closes", close_acc["END"])] += 1
    elif tb and te and tn and tg and any(close_flow.values()):
        c = C_FLOW
        info[("flow_START", close_flow["START"])] += 1
        info[("flow_MID", close_flow["MID"])] += 1
        info[("flow_END_also_closes_with_dmean", abs(gross - relink(dd, "END")) * 100 <= TOL_PP)] += 1
    else:
        c = "REMAINDER"
        if ident:
            info[("rem", "accrual identity holds, restated return outside 0.35pp")] += 1
        elif tb and te and tn and tg:
            info[("rem", "dollars tie, START/MID flow timing does not close")] += 1
        else:
            info[("rem", "dollar gap not equal to BD accrual terms")] += 1
    members[c].append(r["idx"])
n = {c: len(v) for c, v in members.items()}
print(n, sum(n.values()))
for k, v in sorted(info.items(), key=lambda z: str(z[0])):
    print(k, v)
# ledger agreement (supplementary, counts only): BD landed transaction rows vs the BD point and vs the served flow
led = collections.Counter()
for r in rows:
    led[("ledger_flow_equals_bd_net_additions", tie(r["t"]["flow"], r["b"]["nadd"]))] += 1
    led[("ledger_flow_equals_served_flow", tie(r["t"]["flow"], r["o"]["flow"]))] += 1
    led[("segment_has_ledger_rows", r["t"]["n"] > 0)] += 1
    led[("bd_days_equal_linked_days", r["b"]["held"] == r["o"]["days"])] += 1
for k, v in sorted(led.items(), key=lambda z: str(z[0])):
    print(k, v)
pickle.dump({c: v for c, v in members.items()}, open(OUT + "members90.pkl", "wb"))
Path(OUT + "class90_counts.json").write_bytes((json.dumps({"n": n, "info": [[str(k), v] for k, v in info.items()], "ledger": [[str(k), v] for k, v in led.items()]}, indent=1) + "\n").encode("utf-8"))
