"""AMGT_RESAPP round 78 -- AMGT-bb-15: the rot signal gets a home its own module owns (row AMGT_RESAPP-Z-W279-S2; CTO
round-77 ruling 14).

  --crit AC1|AC2|AC3 --where local

At the base `lib/research/freshness/build_view.py` finds the signal with ROT_SIGNAL_GLOB, a glob over every worker's
deliverables folder. The one file it matches is WORKER_COPY below. No store is read and nothing is deployed.

AC1 (build; FAILS at the base):
    C1 build_view no longer names a worker folder: no ROT_SIGNAL_GLOB attribute, no `glob.glob(` call, and no line
       naming both `deliverables` and `rot_signal.json`;
    C2 `lib.research.lists.rot.SIGNAL_HOME` is a path inside lib/research/lists/, the file is there, its bytes equal
       the worker folder's file, and the worker folder's file is still there (copied, never moved);
    C3 `build_view.find_rot_signal_path()` answers that home;
    C4 the absence arm: with `rot.SIGNAL_HOME` pointed at a file that does not exist, `find_rot_signal_path()` answers
       None and the rendered line is build_view.NO_ROT_SIGNAL.
AC2 (build; FAILS at the base): lib/research/freshness/tests/test_rot_home.py holds a test named
    test_the_view_reads_the_signal_from_its_home, and that file and lib/research/lists/tests/test_rot.py both pass.
AC3 (bound; PASSES at the base and after): the line the view renders from the stored signal is the same text as at the
    cut (LINE below), so the move changes where the signal is read from and not what the view says.
Verdict: R78 BB15 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

VIEW = "lib/research/freshness/build_view.py"
WORKER_COPY = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~5/lists/rot_signal.json"
NEW_TEST = "lib/research/freshness/tests/test_rot_home.py"
OLD_TEST = "lib/research/lists/tests/test_rot.py"
TEST_NAME = "test_the_view_reads_the_signal_from_its_home"
LINE = ("publishers: not stale (0/2 stale, reviewed 2026-09-10T22:42Z) | "
        "social_accounts: not stale (0/267 stale, reviewed 2026-09-10T22:42Z)")


def _bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    if a.crit == "AC2":
        text = open(NEW_TEST, encoding="utf-8").read() if os.path.isfile(NEW_TEST) else ""
        clause("C1 the test file holds %s" % TEST_NAME, ("def %s(" % TEST_NAME) in text, NEW_TEST)
        if not text:
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", NEW_TEST,
                            OLD_TEST], capture_output=True, timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C2 both test files pass", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               "rc=%d" % p.returncode)
        return verdict(a, ok)

    from lib.research.freshness import build_view
    from lib.research.lists import rot

    if a.crit == "AC3":
        path = build_view.find_rot_signal_path()
        line = build_view.render_rot_signal(build_view.load_rot_data(path))
        print("   read from %s" % (str(path).replace("\\", "/") if path else None))
        print("   %s" % line)
        clause("C1 the view renders the same line as at the cut", line == LINE)
        return verdict(a, ok)

    source = open(VIEW, encoding="utf-8").read()
    named = [ln.strip()[:90] for ln in source.splitlines() if "deliverables" in ln and "rot_signal.json" in ln]
    clause("C1 build_view names no worker folder for the signal",
           not hasattr(build_view, "ROT_SIGNAL_GLOB") and not re.search(r"\bglob\.glob\(", source) and not named,
           "ROT_SIGNAL_GLOB %s; glob call %s; lines %s" % (hasattr(build_view, "ROT_SIGNAL_GLOB"),
                                                           bool(re.search(r"\bglob\.glob\(", source)), named))
    home = getattr(rot, "SIGNAL_HOME", None)
    if not home:
        clause("C2 rot.SIGNAL_HOME exists", False, "absent")
        return verdict(a, ok)
    home = os.path.abspath(str(home))
    lists_dir = os.path.dirname(os.path.abspath(rot.__file__))
    inside = os.path.normcase(home).startswith(os.path.normcase(lists_dir) + os.sep)
    clause("C2 the home is inside lib/research/lists/ and holds a copy of the worker folder's file",
           inside and os.path.isfile(home) and os.path.isfile(WORKER_COPY) and _bytes(home) == _bytes(WORKER_COPY),
           "%s; worker copy still there %s" % (os.path.relpath(home).replace("\\", "/"), os.path.isfile(WORKER_COPY)))
    found = build_view.find_rot_signal_path()
    clause("C3 the view finds the signal at its home",
           found is not None and os.path.normcase(os.path.abspath(str(found))) == os.path.normcase(home), str(found))
    real = rot.SIGNAL_HOME
    rot.SIGNAL_HOME = type(real)(os.path.join(lists_dir, "data", "r78_no_such_signal.json"))
    try:
        gone = build_view.find_rot_signal_path()
        line = build_view.render_rot_signal(build_view.load_rot_data(gone))
    finally:
        rot.SIGNAL_HOME = real
    clause("C4 an absent signal reads as no signal", gone is None and line == build_view.NO_ROT_SIGNAL, repr(line))
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB15 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
