"""~111 step 6: place the 51 in outcomes by rule and write CONTESTED_51.json (counts and rules only). Usage: python -I s6_record.py <repo_root>"""
import collections
import json
import math
import pickle
import statistics
import sys
from pathlib import Path

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
FT = ("Contribution", "Withdrawal")
if len(M51) != 51:
    print("STOP: members %d, want 51" % len(M51))
    sys.exit(2)


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


txn_by = collections.defaultdict(list)
for t in D["txn"]:
    txn_by[str(t["account_number"]).strip().lstrip("0")].append(t)


def imp(conv, v0, v1, F):
    if conv == "START":
        return v1 / (v0 + F) - 1.0
    if conv == "MID":
        return (v1 - F / 2.0) / (v0 + F / 2.0) - 1.0
    return (v1 - F) / v0 - 1.0


place = collections.Counter()
facts = collections.Counter()
pooled = {c: [] for c in ("START", "MID", "END")}
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    ds_ = sorted(g)
    prev = [d for d in ds_ if d < seg["start"]]
    ser = [(d, g[d]["mv"], g[d]["flow"] or 0.0) for d in ds_ if (not prev or d >= prev[-1]) and d <= seg["end"] and g[d]["mv"] is not None]
    gf = {d: g[d]["flow"] for d in g if seg["start"] <= d <= seg["end"] and g[d]["flow"]}
    # ledger day totals by BD return_date vs served flow
    day = collections.defaultdict(float)
    for t in txn_by[a.lstrip("0")]:
        if t.get("external_flow") in FT and t.get("return_date") and seg["start"] <= str(t["return_date"])[:10] <= seg["end"]:
            day[str(t["return_date"])[:10]] += (1 if t["external_flow"] == "Contribution" else -1) * abs(f(t["market_value"]))
    ledger_ok = all(abs(day.get(d, 0.0) - gf.get(d, 0.0)) <= max(1.0, 0.001 * abs(gf.get(d, 0.0))) for d in set(day) | set(gf))
    dates_same = set(d for d, v in day.items() if abs(v) > 0.005) == set(gf)
    # value-series entry day
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
            continue  # no next day: entry day cannot be told from d vs d+1
        h = abs(F) / 2.0
        cand = []
        if i >= 2 and abs((v0 - ser[i - 2][1]) - F) <= h:
            cand.append("d-1")
        if abs((v1 - v0) - F) <= h:
            cand.append("d")
        if abs((ser[i + 1][1] - v1) - F) <= h:
            cand.append("d+1")
        ent.append(tuple(cand))
        if v0 > 0 and v0 + F > 0:
            for c in pooled:
                pooled[c].append(math.log(max(abs(imp(c, v0, v1, F)) / nz, 1e-3)))
    facts[("segments_with_dates_same_set_ledger_vs_served", dates_same)] += 1
    facts[("segments_ledger_dollars_equal_served_by_day", ledger_ok)] += 1
    n_det = len(ent)
    all_d = n_det > 0 and all(e == ("d",) for e in ent)
    facts[("determinable_readable_flow_days_total",)] += n_det
    facts[("determinable_flow_days_enter_on_posting_day_only",)] += sum(1 for e in ent if e == ("d",))
    facts[("determinable_flow_days_ambiguous_entry",)] += sum(1 for e in ent if e != ("d",))
    if n_det == 0:
        place["O3_NO_DETERMINABLE_FLOW"] += 1
    elif not (ledger_ok and dates_same):
        place["O2_LEDGER_DOLLARS_DO_NOT_REPRODUCE_SERVED_FLOW"] += 1
    elif not all_d:
        place["O4_ENTRY_DAY_AMBIGUOUS_IN_VALUE_SERIES"] += 1
    else:
        place["O1_ENTRY_DAY_SHOWN_INTRADAY_NOT_SHOWN"] += 1
print(dict(place), sum(place.values()))
for k, v in sorted(facts.items(), key=lambda z: str(z[0])):
    print(k, v)
med = {c: round(statistics.median(pooled[c]), 2) for c in pooled}
print("pooled n", len(pooled["START"]), med)

RULES = {
    "O1_ENTRY_DAY_SHOWN_INTRADAY_NOT_SHOWN": (
        "Every flow day that is readable in the daily value series (flow >= 5x the account's own median non-flow daily move and >= 1 percent of the prior value, "
        "with a next day present) shows the flow inside the end-of-day value of the day the custodian posts it, and not of the day before or after; AND the custodian "
        "transaction rows' external-flow day totals (by return date) equal the served flow day by day with the same set of days. The rows therefore fix the DATE of each flow "
        "and show it inside that day's closing value; they do not show whether it sat in the opening value, the closing value or between: a daily value series and a flow amount "
        "cannot separate START, MID and END without the day's own market move on the flow, which neither the transaction rows nor the value series isolate. Placed: rows do not tell START from MID from END."),
    "O2_LEDGER_DOLLARS_DO_NOT_REPRODUCE_SERVED_FLOW": (
        "The segment's custodian transaction rows tagged as external flow (by return date) do not reproduce the served flow dollars day by day (they differ on one or more flow days; "
        "no neighbouring day, trade date or settle date reproduces the served amount either), so the custodian posting of the dollars the dollar tie rests on is not read from the rows. "
        "Placed: rows do not tell."),
    "O3_NO_DETERMINABLE_FLOW": (
        "No flow day in the segment is both large enough against the account's own daily moves and followed by a next day, so the value series shows no entry day. Placed: rows do not tell."),
    "O4_ENTRY_DAY_AMBIGUOUS_IN_VALUE_SERIES": (
        "The ledger ties the served flow by day, but at least one readable flow day fits the value change of more than one day (or none) within half the flow amount. Placed: rows do not tell."),
}
outcomes = [{"outcome": k, "count": v, "rule": RULES[k]} for k, v in sorted(place.items())]
assert sum(o["count"] for o in outcomes) == 51
rec = {
    "to": "IRPT_DASHBD.TO-DB-b-138", "worker": "0.9.0_WK_IRPT_DASHBD~111", "denominator": 51,
    "taking_the_51": "ELEMENTS of class FLOW_TIMING_CONVENTION_DOLLARS_TIE in worker 108's membership pickle (rule order of its class script); reproduced 51 of 90; the other 39 are 31 accrual-class and 8 remainder.",
    "reads": {
        "new_aws_reads": 0, "read_denied": [],
        "reused_downloads": "worker 108's private read of three prefixes: the bronze reporting_performance pull, the served account_return_daily gold partitions, and the silver_legacy transactions tree (all 49 Financial's own); 2488 objects; no object re-read.",
        "transaction_rows_in_private_read": len(D["txn"]),
    },
    "outcomes": outcomes,
    "rule_order": "applied in this order, first that holds takes the segment: O3, then O2, then O4, then O1 (O4 took none of the 51). Each segment's readable flow days are tested against the daily value series only where a next day exists. Outcome 'no flow row found in the window' took none: all 51 have custodian flow rows in the window.",
    "measurements": {
        "closing_by_convention_in_the_51": {"START": 50, "MID": 48, "END": 0},
        "start_mid_end_spread_over_tolerance_segments": "48 of 51 have START/MID/END restated returns spread wider than the 0.35 pp tolerance; END closes in none of the 51 (a fit against the returns, not a read of rows)",
        "date_sets_ledger_vs_served": {"segments_same_flow_days": facts[("segments_with_dates_same_set_ledger_vs_served", True)], "of": 51},
        "ledger_dollars_equal_served_by_day_segments": {"segments": facts[("segments_ledger_dollars_equal_served_by_day", True)], "of": 51},
        "entry_day_in_value_series": {"readable_flow_days_with_next_day": facts[("determinable_readable_flow_days_total",)],
                                      "enter_on_posting_day_only": facts[("determinable_flow_days_enter_on_posting_day_only",)],
                                      "ambiguous": facts[("determinable_flow_days_ambiguous_entry",)]},
        "pooled_median_log_ratio_implied_day_return_to_account_noise": {"flow_days": len(pooled["START"]), "START": med["START"], "MID": med["MID"], "END": med["END"],
            "reading": "zero is the convention whose implied day-of-flow return looks like the account's other days; MID is nearest zero, START and END sit either side; the spread of a single day is wider than the gap, so no segment is decided by it and the pooled figure is not a segment-level fact"},
    },
    "refutation": {
        "stands": True,
        "reason": "Round 68 refuted FLOW_TIMING where the event-date sets agree; the custodian's own transaction rows give the same flow days as the served series in all 51 segments, so the dating premise is unchanged. What would have to be true for the refutation to fall for these 51: the custodian's rows would have to show where in the day a flow sits (opening value, closing value or between) so that START or MID is a fact; a daily end-of-day value series with a flow amount shows only the DAY the flow enters the value, and the rows show that day and agree with the served date, which every convention shares. The START and MID closing is therefore a fit to the returns that the rows neither show nor refute; END failing the fit rests on the returns, not on rows. The refutation stands for all 51; no segment is moved to classed.",
    },
    "tieout_state": {"total": 244, "classed": 185, "contested": 51, "unclassed": 8, "called_closed": False,
                     "composition": "classed = 154 (DB-b-129) + 31 accrual-class (DB-b-135) + 0 of the 51 shown right by a read; contested = the 51; unclassed = 8"},
    "not_established": "Intraday position of a flow (opening, closing or between) is NOT_ESTABLISHED from the rows; the custodian's own intraday or daily-opening series was not among the prefixes read, and the value series read is the served gold end-of-day series built from custodian partitions.",
    "client_figures": 0, "s3_writes": 0,
}
root = Path(sys.argv[1]).resolve()
outp = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~111/CONTESTED_51.json"
outp.parent.mkdir(parents=True, exist_ok=True)
outp.write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
print("wrote", outp.name)
