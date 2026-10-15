"""IRPT_BCKEND workstream ~PE round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell on the CTO's msg 8256: 49 Financial's candidate screen, run offline on the lost ACTIVE account's source rows.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB212-1  IB-pr-573  49 Financial's candidate screen run OFFLINE on the lost ACTIVE account's source rows names the failing condition
    AC1  the screen and the validator read in the code (file, line, identifier verified), the source rows counted, the offline run (read only, no write, no publish, performed)
    AC2  the failing condition named from the code (the line that raises it verified, a measured claim) or the run's acceptance said in words; whether it is the SAME condition Cottonwood's IB-pr-571 found; the fix options read in the code
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
REC2 = D + "0.9.0_WK_IRPT_BCKEND~416/IB212-1_49f_screen_offline_read.json"
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


# ---------------------------------------------------------------------------- IB212-1

def v1():
    r = load(REC2)
    base(r)
    site(r.get("validator_site"), "validator_site (the 49 Financial candidate validator)")
    site(r.get("screen_site"), "screen_site (the 49 Financial candidate screen that drops accounts)")
    sr = r.get("source_rows") or {}
    if not is_int(sr.get("count")) or sr["count"] < 1 or not is_int(sr.get("distinct_dates")) or sr["distinct_dates"] < 1:
        fail("source_rows needs count and distinct_dates as counts of at least 1 (the dropped account's rows, ids private)")
    run = r.get("offline_run") or {}
    if run.get("performed") is not True:
        fail("offline_run.performed must be true: the validator was RUN offline on the account's rows (a record that did not run it is not graded)")
    if run.get("read_only") is not True or run.get("writes") != 0 or run.get("published") is not False:
        fail("offline_run must be read only: writes 0, published false")
    text(run.get("invocation"), 30, "offline_run.invocation (the command, without any account id)")
    if run.get("outcome") not in ("refused", "accepted"):
        fail("offline_run.outcome must be refused or accepted")
    print("OK: the validator and the screen read in the code, %d source rows, an offline read-only run" % sr["count"])


def v2():
    r = load(REC2)
    if not is_int((r.get("source_rows") or {}).get("count")) or r["source_rows"]["count"] < 1 or (r.get("offline_run") or {}).get("performed") is not True:
        fail("the offline run must have been performed on at least one source row before a condition is named or ruled out")
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
    sc = r.get("same_as_cottonwood") or {}
    if not isinstance(sc.get("same"), bool) or sc.get("claim") not in CLAIMS:
        fail("same_as_cottonwood needs same (boolean) and a claim")
    text(sc.get("statement"), 60, "same_as_cottonwood.statement (compare with the IB-pr-571 record when it exists; say what was and was not compared)")
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


CHECKS = {"IB212-1-AC1": v1, "IB212-1-AC2": v2, "IB212-1-AC3": lambda: tail(REC2)}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p212_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
