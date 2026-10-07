"""IRPT_DASHBD TO-DB-b-37 (round 24, workstream B) -- the E2 re-grade of the activity identity. LOCAL; S3 is READ, never written.

Runs the fixed producer `account_activity_lots.py` over the SAME 100 accounts and 24 trading days as round 23
(deliverables/0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json), grades the window identity of each account that has every term,
and writes IDENTITY_REGRADE_E2.json beside this file. Run from the worktree root:

    python <this file>                 # reads S3 cold (about 3 minutes); writes nothing to S3

`account_return_daily.py` is imported read-only. ASCII only.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "lib"))
import account_activity_lots as aal  # noqa: E402
import account_return_daily as ard  # noqa: E402
import boto3  # noqa: E402
import pandas as pd  # noqa: E402
from botocore.config import Config  # noqa: E402

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R23 = ROOT / D / "0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"
E1 = ROOT / D / "0.9.0_WK_IRPT_DASHBD~21/GAP_DIAGNOSIS_E1.json"
OUT = ROOT / D / "0.9.0_WK_IRPT_DASHBD~21/IDENTITY_REGRADE_E2.json"
TOLERANCE = 0.05            # the order's ROUNDING tolerance, unchanged from DB-b-36
TERMS = ("beginning_value", "contributions", "withdrawals", "realized", "unrealized_change", "income", "ending_value")
CONTROL_DAYS = ("2026-09-02", "2026-09-09", "2026-09-17")      # days that carry CONDITIONAL rows of the sample


def window_of(rows, account, days):
    """The window over the account's own rows: its first graded day to the last day."""
    mine = sorted(r["business_date"] for r in rows if r["account_id"] == account)
    return aal.window_reconciliation(rows, account, mine[0], days[-1]) if mine else None


def classify_failure(account, gap, e1_rows, rows, lots, days):
    """Class and cause of one failing window: ROUNDING within the tolerance, MISSING-TERM where DB-b-36 named the cause and the gap is
    unchanged, otherwise OTHER with the day-level signature that explains it (or the statement that nothing does)."""
    if abs(gap) <= TOLERANCE:
        return "ROUNDING", "|gap| <= %.2f: rounding of the daily figures over %d trading days" % (TOLERANCE, len(days))
    e1 = e1_rows.get(account)
    if e1 and e1["class"] == "MISSING-TERM" and set(e1.get("cause_types") or []) <= {"LOT_BASIS_ABOVE_ORIGINAL_COST"} \
            and abs(gap - e1["gap"]) <= 0.01:
        return "MISSING-TERM", "LOT_BASIS_ABOVE_ORIGINAL_COST, unchanged by E2 (gap equals DB-b-36's to 0.01): " + e1["cause"].split(";")[0]
    gap_days = sorted(r["business_date"] for r in rows if r["account_id"] == account and r["coverage"] == aal.COV_GAP)
    by_day = defaultdict(lambda: {"cb": 0.0, "q": 0.0})
    for r in lots:
        if r["account_id"] == account:
            by_day[r["business_date"]]["cb"] += r["custodian_cost_basis"]
            by_day[r["business_date"]]["q"] += r["quantity"]
    notes, explained = [], 0.0
    ordered = sorted(by_day)
    gaps = {d: next(r for r in rows if r["account_id"] == account and r["business_date"] == d)["identity_gap"] for d in gap_days}
    paired = set()
    for d1, d2 in zip(days, days[1:]):          # a lot table that trails the balance by a trading day: the two days net to zero
        if d1 in gaps and d2 in gaps and abs(gaps[d1] + gaps[d2]) <= TOLERANCE:
            paired |= {d1, d2}
            notes.append("%s and %s: the lot table trails the balance by a trading day, day gaps %.2f and %.2f net to %.4f over the "
                         "two days" % (d1, d2, gaps[d1], gaps[d2], gaps[d1] + gaps[d2]))
    for d in gap_days:
        if d in paired:
            continue
        row = next(r for r in rows if r["account_id"] == account and r["business_date"] == d)
        i = ordered.index(d) if d in ordered else -1
        if i > 0:
            dcb = by_day[d]["cb"] - by_day[ordered[i - 1]]["cb"]
            dq = by_day[d]["q"] - by_day[ordered[i - 1]]["q"]
            if abs(row["identity_gap"] + dcb) <= TOLERANCE and abs(dq) <= 1e-3 and not row["contributions"] and not row["withdrawals"] \
                    and not row["realized"]:
                notes.append("%s: custodian cost basis restated by %.2f with the share count unchanged, no flow, no sale (lots "
                             "re-selected after an in-kind departure); the day's gap is that figure" % (d, dcb))
                explained += row["identity_gap"]
                continue
        notes.append("%s: day gap %.2f is not explained by a basis restatement" % (d, row["identity_gap"]))
    net_rest = round(gap - explained, 4)
    if explained and abs(net_rest) <= TOLERANCE:
        return "OTHER", "CUSTODIAN_BASIS_RESTATED_WITHOUT_VALUE_MOVEMENT (window gap equals the restated basis, residual %.4f); %s" % (
            net_rest, "; ".join(notes))
    return "OTHER", "NO SINGLE CAUSE NAMED: %s" % ("; ".join(notes) or "no gap day carries a signature")


def main():
    rec = json.loads(R23.read_bytes().decode("utf-8"))
    e1 = json.loads(E1.read_bytes().decode("utf-8"))
    e1_rows = {r["account_id"]: r for r in e1["gap_classes"]["rows"]}
    days, accounts = rec["days"], rec["accounts"]
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))

    tables, run = aal.compute_local(s3, days, accounts, workers=12)
    rows = tables[aal.TABLE_ACTIVITY]
    graded = {}
    for a in sorted({r["account_id"] for r in rows}):
        w = window_of(rows, a, days)
        if w:
            graded[a] = w
    passed = sorted(a for a, w in graded.items() if abs(w["gap"]) <= aal.CENT)
    failed = sorted(a for a in graded if a not in set(passed))
    failures = []
    for a in failed:
        cls, cause = classify_failure(a, graded[a]["gap"], e1_rows, rows, tables[aal.TABLE_UNREALIZED], days)
        failures.append({"account_id": a, "gap": graded[a]["gap"], "class": cls, "cause": cause,
                         "round_23_gap": next((float(x["gap"]) for x in rec["window_identity"]["accounts_above_one_cent"]
                                               if x["account_id"] == a), None)})
    r23_above = {x["account_id"]: float(x["gap"]) for x in rec["window_identity"]["accounts_above_one_cent"]}
    counts = defaultdict(int)
    for f in failures:
        counts[f["class"]] += 1

    # the exercise: a window that ties within one cent with realized AND a flow, chosen by the stated rule
    qualifying = []
    for a in passed:
        w = graded[a]
        if w["realized"] != 0 and (w["contributions"] != 0 or w["withdrawals"] != 0):
            qualifying.append(w)
    qualifying.sort(key=lambda w: -(abs(w["realized"]) + w["contributions"] + w["withdrawals"]))

    def exercise_of(w):
        mine = sorted((r for r in rows if r["account_id"] == w["account_id"] and r["business_date"] >= w["window"].split("..")[0]),
                      key=lambda r: r["business_date"])
        return {
            "account_id": w["account_id"], "window": w["window"], "beginning_value": w["beginning_value"],
            "contributions": w["contributions"], "withdrawals": w["withdrawals"], "realized": w["realized"],
            "unrealized_change": w["unrealized_change"], "income": w["income"], "ending_value": w["ending_value"], "gap": w["gap"],
            "unrealized_change_breakdown": {"lots": round(sum(r["unrealized_change"] - r["inkind_departure_gain"] for r in mine), 6),
                                            "inkind_departure_gain": round(sum(r["inkind_departure_gain"] for r in mine), 6)},
            "income_breakdown": {k: round(sum(r[k] for r in mine), 6) for k in ("income_gross", "income_fee_admin", "income_withheld_tax")},
            "days_graded": len(mine), "days_measured": sum(1 for r in mine if r["coverage"] == aal.COV_MEASURED),
            "daily": [{"business_date": r["business_date"], **{t: r[t] for t in TERMS}, "identity_gap": r["identity_gap"],
                       "coverage": r["coverage"]} for r in mine]}
    exercise = exercise_of(qualifying[0]) if qualifying else None

    # ---- controls (S3 reads only)
    state = {}
    with aal.served_runtime():
        state = aal.served_runtime_state()
        src = ard.source_entry(ard.load_declaration(), ard.declared_sources(ard.load_declaration())[0])
        ctable, keycols = ard.load_classification(src)
        same = {}
        for d in CONTROL_DAYS:
            base = ard.FlowCache(s3, src, ctable, keycols, accounts).get(d)
            mine = aal.ServedFlowCache(s3, src, ctable, keycols, accounts).get(d)
            same[d] = bool(base == mine)
    control_default = {}
    for d in CONTROL_DAYS[:2]:                  # the same served call on pandas' default string behaviour: the rows are dropped
        flow_default = ard.FlowCache(s3, src, ctable, keycols, accounts).get(d)[0]
        flow_served = run_flow_served(s3, src, ctable, keycols, accounts, d)
        control_default[d] = {"accounts_whose_flow_differs": sorted(a for a in set(flow_default) | set(flow_served)
                                                                    if abs(flow_default.get(a, 0.0) - flow_served.get(a, 0.0)) > 0.005)}

    record = aal.build_record(tables, run, accounts[0])
    out = {
        "task_order": "IRPT_DASHBD.TO-DB-b-37", "worker": "0.9.0_WK_IRPT_DASHBD~21", "window": "%s..%s" % (days[0], days[-1]),
        "environment": {"pandas": pd.__version__, "python": sys.version.split()[0], "served_runtime": state,
                        "producer_method_version": aal.METHOD_VERSION, "producer_schema_version": aal.SCHEMA_VERSION},
        "round_23_reference": {"graded": rec["window_identity"]["accounts_graded"],
                               "within_one_cent": rec["window_identity"]["accounts_within_one_cent"], "above_one_cent": len(r23_above)},
        "regrade": {"graded": len(graded), "passed": len(passed), "failed": len(failed), "tolerance": TOLERANCE,
                    "pass_rule": "the window gap is within one cent (0.01), as in round 23", "failures": failures,
                    "failures_by_class": dict(sorted(counts.items())),
                    "same_91_accounts_as_round_23": len(graded) == rec["window_identity"]["accounts_graded"]},
        "exercise": exercise,
        "exercise_selection": {"population": "the %d graded accounts of the round-23 sample" % len(graded),
                               "rule": "windows that tie within one cent with realized non-zero and a contribution or withdrawal non-zero; "
                                       "the one with the largest sum of |realized|, contributions and withdrawals",
                               "qualifying_windows": len(qualifying),
                               "others": [exercise_of(w) for w in qualifying[1:]]},
        "conditional_resolution": run["conditional_resolution"], "inkind": run["inkind"], "inkind_legs": run["inkind_legs"],
        "income_breakdown": record["income_breakdown"],
        "controls": {"served_flow_cache_equals_served_FlowCache_get": same,
                     "served_in_kind_rederivation_disagreements": run["served_inkind_control"],
                     "default_pandas_string_behaviour_drops_the_conditional_rows": control_default},
    }
    OUT.write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    print("graded %d passed %d failed %d %s" % (len(graded), len(passed), len(failed), dict(counts)))
    print("exercise", exercise["account_id"] if exercise else None, "qualifying", len(qualifying))
    print("controls", same, control_default)


def run_flow_served(s3, src, table, keycols, accounts, day):
    with aal.served_runtime():
        return ard.FlowCache(s3, src, table, keycols, accounts).get(day)[0]


if __name__ == "__main__":
    main()
