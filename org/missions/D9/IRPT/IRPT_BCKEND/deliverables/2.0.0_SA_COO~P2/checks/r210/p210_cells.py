"""IRPT_BCKEND workstream ~PC round 2 (issuer 2.0.0_SA_COO~P2) -- the checks of two READ cells on the CTO's msg 8248: 49 Financial's refusal FIRST, then the Cottonwood validator.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB210-1  IB-pr-570  49 Financial's holdings refusal: which condition refused, how many accounts (ids private), how far behind the served date is (recomputed against the calendar)
    AC1  the refusals (served date, refused candidate dates after it, the conditions with counts, the behind-count recomputed) and the guard's condition read in the code
    AC2  the account class or field behind the condition, the cause with its claim and evidence, the acceptance path in the code, the same question for the other two firms' served dates
    AC3  notes, the six counters 0, no long digit run (no account id)
  IB210-2  IB-pr-571  Cottonwood's dropped account: the offline run of the validator on its source rows names the failing condition
    AC1  the validator and the screen read in the code (file, line, identifier verified), the source rows counted, the offline run (read only, no write, no publish)
    AC2  the failing condition named from the validator's own code (the line that raises it verified), the claim measured, the fix options read in the code
    AC3  notes, the six counters 0, no long digit run (no account id)
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
REC1 = D + "0.9.0_WK_IRPT_BCKEND~413/IB210-1_49f_refusal_read.json"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~414/IB210-2_cot_validator_read.json"
CLAIMS = ("measured", "inferred", "absent")
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


def calendar():
    f = P6.ROOT / "lib" / "trading_calendar.py"
    if not f.is_file():
        fail("no lib/trading_calendar.py in the tree")
    spec = importlib.util.spec_from_file_location("tcal_p210", str(f))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def site(s, what):
    if not isinstance(s, dict) or not isinstance(s.get("file"), str) or not is_int(s.get("line")) or not isinstance(s.get("identifier"), str) or not s["identifier"]:
        fail("%s: needs file, line and the identifier on that line" % what)
    f = P6.ROOT / s["file"]
    if not f.is_file():
        fail("%s: %s is not in the tree" % (what, s["file"]))
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if not 1 <= s["line"] <= len(lines) or s["identifier"] not in lines[s["line"] - 1]:
        fail("%s: line %s of %s does not hold %r" % (what, s["line"], s["file"], s["identifier"]))


def base(r):
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    return iso(r.get("read_date"), "read_date")


def tail(rec):
    r = load(rec)
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters (what each fact rests on, the objects read counted, what was not read)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes, counters 0, no long digit run")


# ---------------------------------------------------------------------------- IB210-1
def f1():
    r = load(REC1)
    rd = base(r)
    cal = calendar()
    sv = r.get("served") or {}
    if sv.get("firm") != "49financial":
        fail("served.firm must be 49financial")
    served = iso(sv.get("business_date"), "served.business_date")
    t1 = cal.prev_trading_day(rd)
    behind = len(cal.trading_days_between(served, t1)) - 1 if served <= t1 else 0
    if sv.get("t_minus_1") != t1.isoformat() or sv.get("trading_days_behind") != behind:
        fail("served.t_minus_1 must be %s and trading_days_behind %d (recomputed against the calendar)" % (t1, behind))
    rf = r.get("refusals") or {}
    dates = rf.get("refused_dates")
    if not isinstance(dates, list) or not dates or dates != sorted(set(dates)):
        fail("refusals.refused_dates must be a sorted unique list of ISO dates")
    for x in dates:
        d = iso(x, "refused date")
        if not (served < d <= rd) or not cal.is_trading_day(d):
            fail("refused date %s must be a trading day after the served date and not after the read date" % x)
    if not is_int(rf.get("refusal_records_read")) or rf["refusal_records_read"] < 1:
        fail("refusals.refusal_records_read must be a count of at least 1")
    pc = rf.get("per_candidate")
    if not isinstance(pc, list) or [x.get("candidate_date") for x in pc] != dates:
        fail("refusals.per_candidate must hold one row per refused date, in order")
    for x in pc:
        cs = x.get("conditions")
        if not isinstance(cs, list) or not cs or not all(isinstance(c.get("condition"), str) and c["condition"] and is_int(c.get("count")) and c["count"] >= 0 for c in cs):
            fail("%s: conditions needs rows of {condition name, count}" % x.get("candidate_date"))
    site(r.get("guard_site"), "guard_site (the code that raises the first condition named)")
    print("OK: 49 Financial %d trading days behind T-1, %d refused candidate dates, the guard read in the code" % (behind, len(dates)))


def f2():
    r = load(REC1)
    ac = r.get("account_or_field") or {}
    if ac.get("claim") not in CLAIMS:
        fail("account_or_field needs a claim")
    text(ac.get("class"), 10, "account_or_field.class (the kind of account or field, never an id)")
    text(ac.get("statement"), 60, "account_or_field.statement")
    cz = r.get("cause") or {}
    if cz.get("claim") not in CLAIMS:
        fail("cause needs a claim")
    text(cz.get("statement"), 60, "cause.statement")
    ev = cz.get("evidence")
    if not isinstance(ev, list) or len(ev) < 2 or not all(isinstance(x, str) and len(x) >= 30 for x in ev):
        fail("cause.evidence needs at least two lines of 30+ characters")
    ap = r.get("acceptance_path") or {}
    mech = ap.get("mechanisms")
    if not isinstance(mech, list) or not mech:
        fail("acceptance_path.mechanisms needs at least one mechanism read in the code")
    for i, m in enumerate(mech):
        site(m, "acceptance_path.mechanisms[%d]" % i)
    text(ap.get("recommended_path"), 40, "acceptance_path.recommended_path")
    of = r.get("other_firms")
    if not isinstance(of, dict) or sorted(of) != ["cottonwood", "inflection"]:
        fail("other_firms must hold cottonwood and inflection")
    for k, v in of.items():
        iso(v.get("served_business_date"), k + ".served_business_date")
    print("OK: the account or field class, the cause, the acceptance path in the code, the other firms")


# ---------------------------------------------------------------------------- IB210-2
def v1():
    r = load(REC2)
    base(r)
    site(r.get("validator_site"), "validator_site (validate_cot_actual_positions)")
    if "validate_cot_actual_positions" not in r["validator_site"]["identifier"]:
        fail("validator_site must be the line that defines or calls validate_cot_actual_positions")
    site(r.get("screen_site"), "screen_site (cot_screen_accounts)")
    if "cot_screen_accounts" not in r["screen_site"]["identifier"]:
        fail("screen_site must be the line of cot_screen_accounts")
    sr = r.get("source_rows") or {}
    if not is_int(sr.get("count")) or sr["count"] < 1 or not is_int(sr.get("distinct_dates")) or sr["distinct_dates"] < 1:
        fail("source_rows needs count and distinct_dates as counts of at least 1 (the dropped account's rows, ids private)")
    run = r.get("offline_run") or {}
    if run.get("read_only") is not True or run.get("writes") != 0 or run.get("published") is not False:
        fail("offline_run must be read only: writes 0, published false")
    text(run.get("invocation"), 30, "offline_run.invocation (the command, without any account id)")
    if run.get("outcome") not in ("refused", "accepted"):
        fail("offline_run.outcome must be refused or accepted")
    print("OK: the validator and the screen read in the code, %d source rows, an offline read-only run" % sr["count"])


def v2():
    r = load(REC2)
    fc = r.get("failing_condition") or {}
    run = r.get("offline_run") or {}
    if run.get("outcome") == "refused":
        text(fc.get("name"), 4, "failing_condition.name (the validator's own condition name)")
        site(fc.get("site"), "failing_condition.site (the line that raises it)")
        if fc.get("claim") != "measured":
            fail("a refused offline run names the failing condition as a MEASURED claim")
    else:
        if fc.get("claim") not in ("inferred", "absent"):
            fail("an accepted offline run (the validator does not refuse) leaves the cause inferred or absent, and says so")
        text(fc.get("statement"), 60, "failing_condition.statement")
    text(fc.get("explanation"), 60, "failing_condition.explanation (what the condition checks, in words, no value)")
    fo = r.get("fix_options")
    if not isinstance(fo, list) or len(fo) < 2:
        fail("fix_options needs at least two options (a screen correction, a custodian TERMINATED mark, or others)")
    for i, o in enumerate(fo):
        text(o.get("option"), 20, "fix_options[%d].option" % i)
        site(o.get("site"), "fix_options[%d].site" % i)
        text(o.get("effect"), 30, "fix_options[%d].effect" % i)
    if r.get("ids_private") is not True:
        fail("ids_private must be true: the account is described by class and count only")
    print("OK: the failing condition named from the validator's own code, the fix options read in the code")


CHECKS = {"IB210-1-AC1": f1, "IB210-1-AC2": f2, "IB210-1-AC3": lambda: tail(REC1),
          "IB210-2-AC1": v1, "IB210-2-AC2": v2, "IB210-2-AC3": lambda: tail(REC2)}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p210_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
