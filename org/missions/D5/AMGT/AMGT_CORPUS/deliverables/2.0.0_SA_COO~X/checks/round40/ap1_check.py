"""AMGT_CORPUS round 40, CRPS-ap-1 -- FWD-14's printed line is four named counts and their sum (round-39 analysis ruling 1).
Issuer's file. Read-only, offline: it calls the REAL `backlog._print_fence14_line` on two hand-built documents.

  python ap1_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap1 build <b>/1 control <c>/2`.
  build    one folder in each of the four classes, folders_read 4: the first printed line is exactly
           `fence14 resolved 1 ambiguous 1 empty-or-workbook-only 1 unresolved-with-reason 1 sum 4 folders_read 4`
           and the function returns True.
  control  c1  the same four records with folders_read 5 (one folder unaccounted for): the function returns False;
           c2  the fourth-class folder is still printed by name on its own line (folder, state, reason).
"""
import contextlib
import io
import sys

from lib.research.corpus import backlog

NEVER = sorted(backlog.NEVER_PROSE_REASONS)[0]
OTHER_STATE = "UNRESOLVED"
assert OTHER_STATE not in (backlog.STATE_RESOLVED, backlog.STATE_AMBIGUOUS)

RECORDS = [
    {"folder": "Resolved Co", "state": backlog.STATE_RESOLVED, "never_prose_reason": None, "disposition_reason": None},
    {"folder": "Ambiguous Co", "state": backlog.STATE_AMBIGUOUS, "never_prose_reason": None, "disposition_reason": None},
    {"folder": "Workbook Co", "state": backlog.STATE_RESOLVED, "never_prose_reason": NEVER, "disposition_reason": None},
    {"folder": "Unresolved Co", "state": OTHER_STATE, "never_prose_reason": None, "disposition_reason": "no ticker stated"},
]
WANT = "fence14 resolved 1 ambiguous 1 empty-or-workbook-only 1 unresolved-with-reason 1 sum 4 folders_read 4"


def run(folders_read):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = backlog._print_fence14_line({"folders_read": folders_read, "records": RECORDS})
    return ok, buf.getvalue().splitlines()


ok4, out4 = run(4)
ok5, _out5 = run(5)
build = 1 if (out4 and out4[0] == WANT and ok4 is True) else 0
c1 = 1 if ok5 is False else 0
c2 = 1 if any("Unresolved Co" in line and OTHER_STATE in line and "no ticker stated" in line for line in out4[1:]) else 0
print("first line: %s" % (out4[0] if out4 else "<none>"))
print("ap1 build %d/1 control %d/2" % (build, c1 + c2))
sys.exit(0)
