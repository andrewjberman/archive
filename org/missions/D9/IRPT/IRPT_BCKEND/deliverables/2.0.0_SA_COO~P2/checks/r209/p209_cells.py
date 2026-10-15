"""IRPT_BCKEND workstream ~PC round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: row D2-S158, why Cottonwood's served holdings are stale (CTO msg 8020).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB209-1  IB-pr-569  Cottonwood's newest accepted holdings publication is 2026-10-08; later candidates were refused on ONE condition, account_lost count 1
    AC1  the refusals: the served date, the refused candidate dates (trading days after it, recomputed against the calendar), the one condition, and where the account is lost (served yes, candidate no, the source partition per date)
    AC2  the cause, whether it clears on its own, and the acceptance path read in the publisher's code (file and line verified at HEAD), the owner and the other firms' refusal state
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
REC = D + "0.9.0_WK_IRPT_BCKEND~412/IB209-1_s158_read.json"
CLAIMS = ("measured", "inferred", "absent")
CAUSES = ("terminated_or_closed_account", "source_data_gap", "mapping_break", "directory_exclusion", "candidate_filter", "other")
FIRMS = ("49financial", "inflection")
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
    spec = importlib.util.spec_from_file_location("tcal_p209", str(f))
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


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    cal = calendar()
    rd = iso(r.get("read_date"), "read_date")
    sv = r.get("served") or {}
    if sv.get("firm") != "cottonwood":
        fail("served.firm must be cottonwood")
    served = iso(sv.get("business_date"), "served.business_date")
    rf = r.get("refusals") or {}
    dates = rf.get("refused_dates")
    if not isinstance(dates, list) or not dates or dates != sorted(set(dates)):
        fail("refusals.refused_dates must be a sorted unique list of ISO dates")
    for x in dates:
        d = iso(x, "refused date")
        if not (served < d <= rd) or not cal.is_trading_day(d):
            fail("refused date %s must be a trading day after the served date and not after the read date" % x)
    if rf.get("first_refused_candidate_date") != dates[0] or rf.get("condition") != "account_lost" or rf.get("lost_count") != 1:
        fail("first_refused_candidate_date must be the first refused date; the one condition is account_lost with lost_count 1")
    if not is_int(rf.get("refusal_records_read")) or rf["refusal_records_read"] < 1:
        fail("refusals.refusal_records_read must be a count of at least 1")
    la = r.get("lost_account") or {}
    if la.get("present_in_served") is not True or la.get("absent_in_candidates") is not True or la.get("claim") not in CLAIMS:
        fail("lost_account: present_in_served true, absent_in_candidates true and a claim (%s)" % "|".join(CLAIMS))
    chk = la.get("source_partition_checks")
    if not isinstance(chk, list) or len(chk) < 2:
        fail("lost_account.source_partition_checks needs at least two dates")
    for x in chk:
        iso(x.get("date"), "source check date")
        if not isinstance(x.get("listed_in_source"), bool):
            fail("each source check needs listed_in_source as a boolean")
    dm = la.get("directory_mark")
    if not isinstance(dm, dict) or not isinstance(dm.get("found"), bool):
        fail("lost_account.directory_mark needs found as a boolean")
    text(dm.get("note"), 20, "lost_account.directory_mark.note (class only, never the account)")
    print("OK: %d refused candidate dates, one condition, the lost account located against the source" % len(dates))


def c2():
    r = load(REC)
    cz = r.get("cause") or {}
    if cz.get("class") not in CAUSES or cz.get("claim") not in CLAIMS:
        fail("cause needs class (%s) and claim (%s)" % ("|".join(CAUSES), "|".join(CLAIMS)))
    text(cz.get("statement"), 60, "cause.statement")
    ev = cz.get("evidence")
    if not isinstance(ev, list) or len(ev) < 2 or not all(isinstance(x, str) and len(x) >= 30 for x in ev):
        fail("cause.evidence needs at least two lines of 30+ characters")
    sc = r.get("self_clears") or {}
    if sc.get("claim") not in CLAIMS:
        fail("self_clears needs a claim")
    text(sc.get("statement"), 40, "self_clears.statement")
    ap = r.get("acceptance_path") or {}
    site(ap.get("guard"), "acceptance_path.guard")
    if "account_lost" not in ap["guard"]["identifier"]:
        fail("acceptance_path.guard must name the account_lost condition")
    mech = ap.get("override_mechanisms")
    if not isinstance(mech, list) or not mech:
        fail("acceptance_path.override_mechanisms needs at least one mechanism read in the code (a bypass, an exemption, a closed-account exclusion)")
    for i, m in enumerate(mech):
        site(m, "acceptance_path.override_mechanisms[%d]" % i)
    text(ap.get("owner"), 20, "acceptance_path.owner")
    text(ap.get("recommended_path"), 40, "acceptance_path.recommended_path")
    of = r.get("other_firms")
    if not isinstance(of, dict) or sorted(of) != sorted(FIRMS):
        fail("other_firms must hold %s" % ", ".join(FIRMS))
    for k, v in of.items():
        iso(v.get("served_business_date"), k + ".served_business_date")
        if not isinstance(v.get("refusal_record_present"), bool):
            fail("%s: refusal_record_present must be a boolean" % k)
    print("OK: the cause, whether it clears, the acceptance path read in the code, the other firms")


def c3():
    r = load(REC)
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters (what each fact rests on, the objects read counted, what was not read)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes, counters 0, no long digit run")


CHECKS = {"IB209-1-AC1": c1, "IB209-1-AC2": c2, "IB209-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p209_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
