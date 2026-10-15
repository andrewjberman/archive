"""IRPT_BCKEND workstream ~PF round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: how Cottonwood's one EMPTY-at-the-source account is accepted as closed (CTO msg 8263).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB213-1  IB-pr-574  the directory's TERMINATED mark: who writes it, its shape, the precedent, the guard's reading, and an OFFLINE guard run with the mark applied to the one account
    AC1  the mark's writer and shape read in the code (file, line, identifier verified), the guard's reading of it, and the precedent (the TERMINATED entries already in Cottonwood's directory, counted)
    AC2  the evidence the pair binds to: the one account, the zero-position source dates (trading days, at least three) and the first date it is accepted from
    AC3  the offline guard run with the mark applied (performed, read only, no write, no publish): the account lists as closed and not refused, the candidate would publish, every other node unchanged (counted); the rollback; notes, counters 0, no long digit run
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
REC = D + "0.9.0_WK_IRPT_BCKEND~417/IB213-1_terminated_mark_read.json"
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
    spec = importlib.util.spec_from_file_location("tcal_p213", str(f))
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
    iso(r.get("read_date"), "read_date")
    mk = r.get("mark") or {}
    site(mk.get("writer_site"), "mark.writer_site (the code that writes a directory entry's status)")
    site(mk.get("guard_reading_site"), "mark.guard_reading_site (closed_account_ids or the line that reads TERMINATED)")
    text(mk.get("shape"), 40, "mark.shape (the fields of a directory entry that carry the status and its date, no account id)")
    text(mk.get("owner"), 20, "mark.owner (who writes the directory: the seat, function or schedule)")
    pr = mk.get("precedent") or {}
    if not is_int(pr.get("terminated_entries_in_cottonwood")) or pr["terminated_entries_in_cottonwood"] < 0 or not is_int(pr.get("directory_entries")) or pr["directory_entries"] < 1:
        fail("mark.precedent needs terminated_entries_in_cottonwood and directory_entries as counts")
    if pr.get("claim") not in CLAIMS:
        fail("mark.precedent needs a claim")
    text(pr.get("how_set"), 40, "mark.precedent.how_set (how an existing TERMINATED entry came to carry the mark)")
    print("OK: the mark's writer, shape, owner and precedent read; the guard's reading verified")


def c2():
    r = load(REC)
    cal = calendar()
    ev = r.get("evidence") or {}
    if ev.get("accounts") != 1:
        fail("evidence.accounts must be 1 (the pair is bound to the one account; its id stays private)")
    dates = ev.get("zero_position_dates")
    if not isinstance(dates, list) or len(dates) < 3 or dates != sorted(set(dates)):
        fail("evidence.zero_position_dates must be a sorted unique list of at least three dates")
    rd = iso(r.get("read_date"), "read_date")
    for x in dates:
        d = iso(x, "zero position date")
        if not cal.is_trading_day(d) or d > rd:
            fail("zero position date %s must be a trading day not after the read date" % x)
    if ev.get("positions_on_those_dates") != 0:
        fail("evidence.positions_on_those_dates must be 0: the source itself reports zero positions")
    if ev.get("first_accept_date") != dates[0]:
        fail("evidence.first_accept_date must be the first zero-position date")
    if ev.get("claim") != "measured":
        fail("the evidence is read from the source rows: claim measured")
    text(ev.get("statement"), 60, "evidence.statement (the source rows' dates and zero position counts, in words, no id)")
    print("OK: one account, %d zero-position trading dates, accepted from %s" % (len(dates), dates[0]))


def c3():
    r = load(REC)
    og = r.get("offline_guard") or {}
    if og.get("performed") is not True or og.get("read_only") is not True or og.get("writes") != 0 or og.get("published") is not False:
        fail("offline_guard must be performed, read only, 0 writes, not published")
    text(og.get("invocation"), 30, "offline_guard.invocation (the command, no account id)")
    if og.get("account_listed_as") != "closed_accounts_not_refused" or og.get("outcome") not in ("PUBLISHED", "WOULD_PUBLISH"):
        fail("with the mark applied the account must list as closed_accounts_not_refused and the outcome PUBLISHED or WOULD_PUBLISH")
    if not is_int(og.get("nodes_changed_other_than_the_account")) or og["nodes_changed_other_than_the_account"] != 0:
        fail("every other node must be unchanged: nodes_changed_other_than_the_account 0")
    if not is_int(og.get("accounts_leaving")) or og["accounts_leaving"] != 1:
        fail("accounts_leaving must be 1")
    rb = r.get("rollback") or {}
    text(rb.get("statement"), 40, "rollback.statement (the prior accepted publication and how it returns)")
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the offline guard run lists the account closed and not refused, every other node unchanged")


CHECKS = {"IB213-1-AC1": c1, "IB213-1-AC2": c2, "IB213-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p213_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
