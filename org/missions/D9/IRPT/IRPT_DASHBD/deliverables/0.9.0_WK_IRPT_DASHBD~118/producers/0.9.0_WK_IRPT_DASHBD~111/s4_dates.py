"""~111 step 4: posting-date agreement between BD's transaction rows (return_date / trade_date / settle_date) and the served flow dates,
per segment; plus per-segment placement. Counts only (private pickles, no AWS)."""
import collections
import datetime as dt
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~111/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
FT = ("Contribution", "Withdrawal")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def ds(x):
    return None if x is None else str(x)[:10]


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)

C = collections.Counter()
res = {}
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    tr = [t for t in txn_by[a.lstrip("0")] if t.get("external_flow") in FT]
    by = {"return_date": collections.defaultdict(float), "trade_date": collections.defaultdict(float), "settle_date": collections.defaultdict(float)}
    for t in tr:
        amt = (1.0 if t["external_flow"] == "Contribution" else -1.0) * abs(f(t["market_value"]))
        for k in by:
            if t.get(k) is not None and seg["start"] <= ds(t["return_date"]) <= seg["end"]:
                by[k][ds(t[k])] += amt
    out = {}
    for k, m in by.items():
        days = set(d for d, v in m.items() if abs(v) > 0.005)
        same = all(abs(m.get(d, 0.0) - gf.get(d, 0.0)) <= max(1.0, 0.001 * abs(gf.get(d, 0.0))) for d in days | set(gf))
        out[k] = same
        C[(k + "_day_totals_equal_served_flow_days", same)] += 1
    # in-window return_date days with a BD flow row but no served flow on that day / vice versa
    rdays = set(d for d, v in by["return_date"].items() if abs(v) > 0.005)
    C[("bd_return_days_only", len(rdays - set(gf)) > 0)] += 1
    C[("served_days_only", len(set(gf) - rdays) > 0)] += 1
    # offsets of the served flow date vs the other BD dates (calendar days) for unmatched served days
    for d in gf:
        if abs(by["return_date"].get(d, 0.0) - gf[d]) > max(1.0, 0.001 * abs(gf[d])):
            found = None
            for k in ("trade_date", "settle_date"):
                if abs(by[k].get(d, 0.0) - gf[d]) <= max(1.0, 0.001 * abs(gf[d])):
                    found = k
            near = None
            for off in (-3, -2, -1, 1, 2, 3):
                d2 = (dt.date.fromisoformat(d) + dt.timedelta(days=off)).isoformat()
                if abs(by["return_date"].get(d2, 0.0) - gf[d]) <= max(1.0, 0.001 * abs(gf[d])):
                    near = off
            C[("unmatched_served_flow_day", "matches_other_BD_field=" + str(found), "return_date_offset=" + str(near))] += 1
    res[r["idx"]] = out
for k, v in sorted(C.items(), key=lambda z: str(z[0])):
    print(k, v)
pickle.dump(res, open(OUT + "s4_dates.pkl", "wb"))
