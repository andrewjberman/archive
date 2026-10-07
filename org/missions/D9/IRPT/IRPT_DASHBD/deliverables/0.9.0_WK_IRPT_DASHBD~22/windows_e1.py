"""IRPT_DASHBD TO-DB-b-39 (round 25, workstream B) -- the four windows round 24 left, read against the custodian's lot events and the
91 windows re-run. LOCAL; S3 is READ, never written.

Runs the producer `account_activity_lots.py` (LEG_LAG_DAYS from DB-b-38) over the SAME 100 accounts and 24 trading days as rounds 23
and 24, grades the window identity of each account that has every term, names what explains each of round 24's four non-ROUNDING
windows from the lot rows, and writes WINDOWS_E1.json beside this file. Run from the worktree root:

    python <this file>                 # about 8 minutes cold; writes nothing to S3

The negative control re-runs the four accounts with the two rules switched off (the wash-sale basis and the re-selection true-up)
and must give back round 24's gaps. ASCII only.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "lib"))
import account_activity_lots as aal  # noqa: E402
import account_return_daily as ard  # noqa: E402
import boto3  # noqa: E402
from botocore.config import Config  # noqa: E402

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R23 = ROOT / D / "0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"
R24 = ROOT / D / "0.9.0_WK_IRPT_DASHBD~21/IDENTITY_REGRADE_E2.json"
E1 = ROOT / D / "0.9.0_WK_IRPT_DASHBD~21/GAP_DIAGNOSIS_E1.json"
OUT = ROOT / D / "0.9.0_WK_IRPT_DASHBD~22/WINDOWS_E1.json"
TOLERANCE = 0.05            # the order's ROUNDING tolerance, unchanged from rounds 23 and 24


def load(path):
    return json.loads(path.read_bytes().decode("utf-8"))


def window_of(rows, account, days):
    mine = sorted(r["business_date"] for r in rows if r["account_id"] == account)
    return aal.window_reconciliation(rows, account, mine[0], days[-1]) if mine else None


def grade(tables, days):
    rows = tables[aal.TABLE_ACTIVITY]
    graded = {}
    for a in sorted({r["account_id"] for r in rows}):
        w = window_of(rows, a, days)
        if w:
            graded[a] = w
    return rows, graded


def classify(account, gap, rows, days):
    """ROUNDING within the order's tolerance; otherwise OTHER with the gap days that carry it (no single cause is named from a number)."""
    if abs(gap) <= TOLERANCE:
        return "ROUNDING", "|gap| <= %.2f: rounding of the daily figures over %d trading days" % (TOLERANCE, len(days))
    over = sorted((r["business_date"], r["identity_gap"]) for r in rows
                  if r["account_id"] == account and r["coverage"] == aal.COV_GAP)
    return "OTHER", "NO CAUSE NAMED from the rows; days above their allowance: %s" % (over or "none")


def lots_first_seen(tables, account, kind, first_day):
    """{lot_id: first business_date} of the account's lots of one basis_source first seen after `first_day` (the window's first day)."""
    seen = {}
    for r in sorted(tables[aal.TABLE_UNREALIZED], key=lambda r: r["business_date"]):
        if r["account_id"] == account and r["basis_source"] == kind:
            seen.setdefault(r["lot_id"], r["business_date"])
    return {k: v for k, v in seen.items() if v > first_day}


def main():
    rec, r24, e1 = load(R23), load(R24), load(E1)
    days, accounts = rec["days"], rec["accounts"]
    before = {f["account_id"]: f for f in r24["regrade"]["failures"]}
    four = sorted(a for a, f in before.items() if f["class"] != "ROUNDING")
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))

    tables, run = aal.compute_local(s3, days, accounts, workers=12)
    rows, graded = grade(tables, days)
    passed = sorted(a for a, w in graded.items() if abs(w["gap"]) <= aal.CENT)
    failed = sorted(a for a in graded if a not in set(passed))
    failures = []
    for a in failed:
        cls, cause = classify(a, graded[a]["gap"], rows, days)
        failures.append({"account_id": a, "gap": graded[a]["gap"], "class": cls, "cause": cause})
    counts = Counter(f["class"] for f in failures)
    new_failures = [a for a in failed if a not in before]
    worse = [f["account_id"] for f in failures if abs(f["gap"]) > abs(before.get(f["account_id"], {"gap": 0.0})["gap"]) + 1e-9]

    # ---- the four windows, each read against its lot events
    first_day = str(aal.tc.prev_trading_day(days[0]))[:10]
    inkind = run["inkind"]
    e1_rows = {r["account_id"]: r for r in e1["gap_classes"]["rows"]}
    windows = []
    for a in four:
        wash_open = lots_first_seen(tables, a, aal.BASIS_WASH, days[0])
        wash_closed = [r for r in tables[aal.TABLE_REALIZED] if r["account_id"] == a and r["basis_source"] == aal.BASIS_WASH]
        resel = [x for x in inkind["reselections"] if x["account_id"] == a]
        events = ["account_lot_unrealized_daily/date=%s/lot=%s" % (d, lot) for lot, d in sorted(wash_open.items(), key=lambda kv: kv[1])]
        events += ["account_lot_realized/date=%s/lot=%s" % (r["business_date"], r["lot_id"]) for r in wash_closed]
        if resel:
            x = resel[0]
            events = [ev["row"] for ev in e1_rows[a]["evidence_rows"] if ev["row"].startswith("fact_trn/date=%s" % x["departure_day"])]
            events += ["account_lot_unrealized_daily/date=%s/lot=%s" % (r["business_date"], r["lot_id"])
                       for r in tables[aal.TABLE_UNREALIZED]
                       if r["account_id"] == a and r["cusip"] == x["cusip"] and first_day <= r["business_date"] <= x["day"]
                       and r["business_date"] in (aal.tc.prev_trading_day(x["departure_day"]).isoformat(), x["departure_day"], x["day"])]
            cause = ("CUSTODIAN_RESELECTED_THE_LOTS_RELIEVED_BY_AN_IN_KIND_DEPARTURE: the leg of %.0f shares posts on %s with one selection of "
                     "lots; on %s the table shows another selection (%d lots out, %d in) of the same security with the share count "
                     "unchanged at %.0f, no leg and no sale, and the remaining basis moved by %.2f. The shares relieved are the leg's; the "
                     "basis relieved is the table's before the departure less its basis after the re-selection, so the departure gain is "
                     "trued up by that change on the day of the re-selection (the quantity ties to the leg on both days)" % (
                         x["departure_quantity"], x["departure_day"], x["day"], x["lots_out"], x["lots_in"], x["remaining_quantity"],
                         x["basis_moved"]))
        else:
            cause = ("WASH_SALE_CARRY_OVER: %d lot(s) opened after the window's first day carry a custodian basis above the cash paid by the loss "
                     "disallowed on an earlier sale (disallowed_loss_amount, acquired_date tacked back before orgpurch_date), a basis "
                     "no cash moved for; %d closed lot(s) of the window carried one. Each is measured from the cash paid "
                     "(cost_basis_unamortized less disallowed_loss_amount) on every day it is open and where it closes; the "
                     "custodian's figure stays in custodian_cost_basis" % (len(wash_open), len(wash_closed)))
        windows.append({"account_id": a, "gap_before": before[a]["gap"], "gap_after": graded[a]["gap"] if a in graded else None,
                        "lot_events": events, "cause": cause, "kind": "RULE"})

    # ---- controls (S3 reads only)
    # 1. the rules off for the four accounts gives round 24's gaps back
    real_unrealized, real_restate = aal.unrealized_rows, aal._custodian_restatement

    def unrealized_off(*args, **kwargs):
        out = real_unrealized(*args, **kwargs)
        for r in out:
            if r["basis_source"] == aal.BASIS_WASH:
                r["cost_basis"], r["unrealized_gain"] = r["custodian_cost_basis"], round(r["unrealized_gain"] - r["_disallowed"], 6)
                r["basis_source"], r["_disallowed"] = aal.BASIS_CUSTODIAN, 0.0
        return out

    aal.unrealized_rows, aal._custodian_restatement = unrealized_off, lambda *a, **k: None
    try:
        off_tables, _ = aal.compute_local(s3, days, four, workers=12)
    finally:
        aal.unrealized_rows, aal._custodian_restatement = real_unrealized, real_restate
    off_rows, off_graded = grade(off_tables, days)
    rules_off = {a: {"gap": off_graded[a]["gap"] if a in off_graded else None, "round_24_gap": before[a]["gap"]} for a in four}
    # 2. the cash-paid basis the rule measures from equals the custodian's own original cost on every lot that carries a disallowed loss
    src = ard.source_entry(ard.load_declaration(), ard.declared_sources(ard.load_declaration())[0])
    pad = int(src.get("account_id_zero_pad") or 0)
    keep = set(accounts)
    cols = ["account_id", "cost_basis_unamortized", "original_cost_basis", "disallowed_loss_amount"]
    carrying, equal = 0, 0
    for table in aal.LOT_SOURCE["unrealized"]["tables"]:
        f = aal.read_day(s3, src, table, days[-1], columns=cols)
        if f is None:
            continue
        f = f[f["account_id"].astype(str).str.strip().str.zfill(pad).isin(keep)]
        for cb, oc, dl in zip(f["cost_basis_unamortized"], f["original_cost_basis"], f["disallowed_loss_amount"]):
            dl, cb, oc = aal._num(dl), aal._num(cb), aal._num(oc)
            if dl is not None and abs(dl) > aal.CENT / 2:
                carrying += 1
                equal += 1 if cb is not None and oc is not None and abs(cb - dl - oc) <= aal.CENT / 2 else 0

    out = {
        "task_order": "IRPT_DASHBD.TO-DB-b-39", "worker": "0.9.0_WK_IRPT_DASHBD~22", "window": "%s..%s" % (days[0], days[-1]),
        "producer": {"method_version": aal.METHOD_VERSION, "schema_version": aal.SCHEMA_VERSION, "leg_lag_days": aal.LEG_LAG_DAYS},
        "windows": windows,
        "regrade": {"graded": len(graded), "passed": len(passed), "failed": len(failed), "tolerance": TOLERANCE,
                    "pass_rule": "the window gap is within one cent (0.01), as in rounds 23 and 24", "failures": failures,
                    "failures_by_class": dict(sorted(counts.items())), "round_24": {
                        "graded": r24["regrade"]["graded"], "passed": r24["regrade"]["passed"], "failed": r24["regrade"]["failed"],
                        "failures_by_class": r24["regrade"]["failures_by_class"]},
                    "new_failures_against_round_24": new_failures, "windows_with_a_larger_gap_than_round_24": worse,
                    "same_91_accounts_as_round_23": len(graded) == rec["window_identity"]["accounts_graded"]},
        "rule_audit": {
            "basis_source_unrealized_rows": dict(Counter(r["basis_source"] for r in tables[aal.TABLE_UNREALIZED])),
            "basis_source_realized_rows": dict(Counter(r["basis_source"] for r in tables[aal.TABLE_REALIZED])),
            "unrealized_rows_with_an_absent_disallowed_figure": sum(r["_disallowed_absent"] for r in tables[aal.TABLE_UNREALIZED]),
            "reselections": inkind["reselections"], "unmatched": inkind["unmatched"],
            "matched_arrivals": len(inkind["matched_arrivals"]), "matched_departures": len(inkind["matched_departures"]),
            "relots": len(inkind["relots"])},
        "controls": {"rules_off_for_the_four": rules_off,
                     "last_day_lots_carrying_a_disallowed_loss": {"lots": carrying, "cash_paid_equals_basis_less_loss": equal,
                                                                  "day": days[-1], "accounts": len(keep)}},
    }
    OUT.write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    print("graded %d passed %d failed %d %s new %s" % (len(graded), len(passed), len(failed), dict(counts), new_failures))
    for w in windows:
        print(w["account_id"], w["gap_before"], "->", w["gap_after"], w["kind"], len(w["lot_events"]), "events")
    print("rules off", rules_off, "controls", carrying, equal)
    print("audit", out["rule_audit"])


if __name__ == "__main__":
    main()
