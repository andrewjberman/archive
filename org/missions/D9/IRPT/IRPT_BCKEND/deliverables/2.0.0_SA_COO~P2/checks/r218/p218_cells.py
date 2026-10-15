"""IRPT_BCKEND workstream ~PJ round 1 (issuer 2.0.0_SA_COO~P2) -- the checks of two READ cells that measure the served DELTA of the two ~PH builds.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB218-1  IB-pr-580  the exemption ALONE, per firm: the same candidate gated with and without the absent_at_source evidence, the served DELTA the exemption itself moves, the persistence on the next fire, the conditions that remain
    AC1  the method and the identity: base commit, read date, both firms, the candidate and served days, the builder, the claim measured
    AC2  the arithmetic per firm: the node and account counts with and without agree with the exemption alone, no other node changed, no amount added, the gate outcomes and conditions consistent, the second fire exempts again
    AC3  notes, the six counters 0, no long digit run (no id)
  IB218-2  IB-pr-581  the split adjustment on the 49 Financial channel, before and after, over the custodian's split days: the account-days moved, the implausible returns before and after
    AC1  the method and the identity: base commit, read date, the split days (trading days, 2026-04-21 among them), the claim measured
    AC2  the arithmetic: account-days run, changed, those holding a split security, the securities adjusted and ratio-absent, the status moves and the returns at or below -50 percent before and after
    AC3  notes, the six counters 0, no long digit run (no id)
"""
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC1 = D + "0.9.0_WK_IRPT_BCKEND~422/IB218-1_exemption_delta.json"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~423/IB218-2_split_delta.json"
FIRMS = ("49financial", "cottonwood")
OUTCOMES = ("REFUSED", "PUBLISHED")
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def iso(x, what):
    if not isinstance(x, str) or not re.fullmatch(r"\d{4}-\d\d-\d\d", x):
        fail("%s must be an ISO date" % what)
    try:
        return dt.date.fromisoformat(x)
    except ValueError:
        fail("%s is not a real date" % what)


def count(x, what):
    if not is_int(x) or x < 0:
        fail("%s must be a count (an integer, 0 or more)" % what)
    return x


def calendar():
    f = P6.ROOT / "lib" / "trading_calendar.py"
    if not f.is_file():
        fail("no lib/trading_calendar.py in the tree")
    spec = importlib.util.spec_from_file_location("tcal_p218", str(f))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def identity(r):
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be 40 hex")
    iso(r.get("read_date"), "read_date")
    text(r.get("method"), 120, "method")
    if r.get("claim") != "measured":
        fail("claim must read measured (a dry run over the live pinned inputs)")


def side(s, what):
    if not isinstance(s, dict):
        fail("%s must be an object" % what)
    if s.get("outcome") not in OUTCOMES:
        fail("%s.outcome must be one of %s" % (what, OUTCOMES))
    conds = s.get("conditions")
    if not isinstance(conds, list) or not all(isinstance(c, str) and c for c in conds):
        fail("%s.conditions must be a list of condition names" % what)
    if (s["outcome"] == "PUBLISHED") != (len(conds) == 0):
        fail("%s: PUBLISHED reads with no condition and REFUSED with at least one" % what)
    return count(s.get("node_count"), what + ".node_count"), count(s.get("account_count"), what + ".account_count")


def ac1_exemption(r):
    identity(r)
    firms = r.get("firms")
    if not isinstance(firms, dict) or sorted(firms) != sorted(FIRMS):
        fail("firms must hold exactly %s" % (FIRMS,))
    for f in FIRMS:
        e = firms[f]
        iso(e.get("candidate_day"), f + ".candidate_day")
        iso(e.get("served_day"), f + ".served_day")
        text(e.get("builder"), 8, f + ".builder")
    low = r["method"].lower()
    if "without" not in low or "with " not in low and "with the" not in low:
        fail("the method must state both runs, WITH and WITHOUT the evidence provider")
    print("OK: identity and method; firms %s" % sorted(firms))


def ac2_exemption(r):
    for f in FIRMS:
        e = (r.get("firms") or {}).get(f) or {}
        wn, wa = side(e.get("without"), f + ".without")
        yn, ya = side(e.get("with"), f + ".with")
        ex = e.get("exemption_alone") or {}
        added_n, added_a = count(ex.get("nodes_added"), f + ".nodes_added"), count(ex.get("accounts_added"), f + ".accounts_added")
        if yn != wn + added_n or ya != wa + added_a:
            fail("%s: the counts with must equal the counts without plus the exemption alone (nodes %d+%d vs %d, accounts %d+%d vs %d)" % (f, wn, added_n, yn, wa, added_a, ya))
        if ex.get("other_nodes_changed") != 0:
            fail("%s: other_nodes_changed must be 0 (the exemption alone adds the listed node and moves no other node)" % f)
        if ex.get("amount_added_usd") != 0:
            fail("%s: amount_added_usd must be 0 (the listed account shows no amount as current)" % f)
        n_ex = count(e["with"].get("exempted_accounts"), f + ".with.exempted_accounts")
        if added_a != n_ex or added_n != n_ex:
            fail("%s: each exempted account adds exactly one account node (exempted %d, nodes added %d, accounts added %d)" % (f, n_ex, added_n, added_a))
        if "account_lost" in e["with"]["conditions"] and n_ex > 0:
            fail("%s: with the exemption an exempted account must not still refuse as account_lost" % f)
        if n_ex > 0 and "account_lost" not in e["without"]["conditions"]:
            fail("%s: an exemption that applied must have been an account_lost refusal without it" % f)
        if n_ex == 0 and (added_n != 0 or e["with"]["conditions"] != e["without"]["conditions"]):
            fail("%s: with no exempted account the two runs must be identical" % f)
        if n_ex > 0:
            fad = e["with"].get("first_absent_day")
            if fad is not None:
                iso(fad, f + ".with.first_absent_day")
            if not isinstance(e["with"].get("since_bound_reached"), bool):
                fail("%s.with.since_bound_reached must be a boolean" % f)
            s2 = e.get("second_fire") or {}
            if s2.get("exempt_again") is not True or s2.get("outcome_account_lost") is not False:
                fail("%s: the second fire (the listed snapshot served, the same candidate) must exempt the account again and not refuse it as account_lost" % f)
    print("OK: the exemption alone moves exactly its listed nodes; counts and conditions agree")


def ac1_split(r):
    identity(r)
    days = r.get("split_days")
    if not isinstance(days, list) or len(days) < 1 or days != sorted(days) or len(set(days)) != len(days):
        fail("split_days must be a sorted list of distinct ISO dates")
    cal = calendar()
    for d in days:
        if not cal.is_trading_day(iso(d, "split_days entry")):
            fail("split day %s is not a trading day" % d)
    if "2026-04-21" not in days:
        fail("split_days must include 2026-04-21 (the 6-for-1 day the ruling names)")
    if r.get("firm_scope") != "49financial":
        fail("firm_scope must read 49financial (the only channel with a split declaration)")
    text(r.get("method"), 120, "method")
    low = r["method"].lower()
    if "before" not in low or "after" not in low:
        fail("the method must state both runs, BEFORE and AFTER the adjustment")
    print("OK: %d split days, 2026-04-21 included" % len(days))


def ac2_split(r):
    t = r.get("totals") or {}
    run, changed = count(t.get("account_days_run"), "account_days_run"), count(t.get("account_days_changed"), "account_days_changed")
    held = count(t.get("account_days_holding_a_split_security"), "account_days_holding_a_split_security")
    if not (0 < run and changed <= held <= run):
        fail("account_days_changed must not exceed those holding a split security, which must not exceed those run (run %d, held %d, changed %d)" % (run, held, changed))
    adj, absent = count(t.get("securities_adjusted"), "securities_adjusted"), count(t.get("securities_ratio_absent"), "securities_ratio_absent")
    if adj + absent < 1:
        fail("at least one split security-day must be adjusted or ratio-absent")
    b, a = count(t.get("at_or_below_minus_50pct_before"), "at_or_below_minus_50pct_before"), count(t.get("at_or_below_minus_50pct_after"), "at_or_below_minus_50pct_after")
    if a > b:
        fail("returns at or below -50 percent must not rise with the adjustment (before %d, after %d)" % (b, a))
    moves = t.get("status_moves")
    if not isinstance(moves, dict) or not all(isinstance(k, str) and is_int(v) and v >= 0 for k, v in moves.items()):
        fail("status_moves must map 'FROM->TO' to a count")
    if sum(moves.values()) > run:
        fail("status moves cannot exceed the account-days run")
    if not isinstance(r.get("per_day"), list) or len(r["per_day"]) != len(r.get("split_days") or []):
        fail("per_day must hold one entry per split day")
    if sum(count(d.get("account_days_changed"), "per_day.account_days_changed") for d in r["per_day"]) != changed:
        fail("the per-day changed counts must sum to the total")
    d21 = [d for d in r["per_day"] if d.get("day") == "2026-04-21"]
    if len(d21) != 1 or d21[0]["account_days_changed"] < 1:
        fail("2026-04-21 must appear once with at least one account-day changed")
    print("OK: %d account-days run, %d changed; -50 percent returns %d before, %d after" % (run, changed, b, a))


def ac3(r):
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or any(not isinstance(n, str) or len(n) < 30 for n in notes):
        fail("notes needs at least three lines of 30+ characters (what each fact rests on, what was not read)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes, counters, no long digit run")


CHECKS = {
    "IB218-1-AC1": lambda: ac1_exemption(load(REC1)), "IB218-1-AC2": lambda: ac2_exemption(load(REC1)), "IB218-1-AC3": lambda: ac3(load(REC1)),
    "IB218-2-AC1": lambda: ac1_split(load(REC2)), "IB218-2-AC2": lambda: ac2_split(load(REC2)), "IB218-2-AC3": lambda: ac3(load(REC2)),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p218_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
