"""AMGT_RESAPP round 78 -- AMGT-bb-14: the pull driver gives a missing library its own stop word (row
AMGT_RESAPP-Z-S366; CTO round-77 ruling 14).

  --crit AC1|AC2|AC3 --where local
  --stamp                              print the AC3 stamp of the tree as it stands (the issuer's, at the cut)

NO Bloomberg call is made by this check: every boundary is a fake, and the three real reads of the driver
(`vehicle_ran_today`, `terminal_healthy`, `_load_blp_client`) are replaced by recorders before `main` is called.

AC1 (build; FAILS at the base) on integrations/bloomberg/research/research_pulls.py:
    C1 EXIT holds NO_BLOOMBERG_LIBRARY = 6 and the four older words keep their codes (0, 3, 4, 5);
    C2 `library_importable(module="blpapi")` exists and answers a bool: False for a module that does not exist, True
       for one that does;
    C3 `run(..., library=lambda: False)` on fakes stops NO_BLOOMBERG_LIBRARY with 0 calls and 0 writes, and neither the
       vehicle read nor the health read was made (it is decided before any other read);
    C4 the controls: with `library=lambda: True` the three names are pulled; with `library` left out the run is as
       today; a Terminal that does not answer still stops TERMINAL_DOWN, so the two words stay distinct;
    C5 the command line: with the library reported missing, `run segments --probe "AMD US Equity"` returns 6, prints
       `stopped NO_BLOOMBERG_LIBRARY` and a line naming this interpreter's path, and makes no vehicle read, no health
       read and no load of the Bloomberg client.
AC2 (build; FAILS at the base): integrations/bloomberg/research/tests/test_research_pulls.py holds a test named
    test_missing_library_stops_before_any_call and the whole file passes.
AC3 (bound; PASSES at the base and after): under integrations/bloomberg/ only the two files of this cell differ from
    the tree at the cut -- every other tracked file's blob is the one stamped below, no file was added or removed, and
    nothing else there is modified or untracked in the working tree.
Verdict: R78 BB14 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import os
import subprocess
import sys

DRIVER = "integrations/bloomberg/research/research_pulls.py"
TEST = "integrations/bloomberg/research/tests/test_research_pulls.py"
TEST_NAME = "test_missing_library_stops_before_any_call"
WORD, CODE = "NO_BLOOMBERG_LIBRARY", 6
OLD = {"OK": 0, "CAPACITY": 3, "VEHICLE_NOT_RUN": 4, "TERMINAL_DOWN": 5}
N3 = ["BA US Equity", "AMD US Equity", "ASML NA Equity"]
# sha256 over `git ls-files -s -- integrations/bloomberg` minus the two files of this cell, at the base this was cut on.
STAMP = "002e8c2034aba7d635fb082f04e096487abcc3697798011b0b1e35ecf626e81f"


class FakeBlp:
    def __init__(self):
        self.calls = []

    def reference_data(self, securities, fields, **_kw):
        self.calls.append(list(securities))
        return {s: {f: "x" for f in fields} for s in securities}


def _git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, timeout=120).stdout.decode("utf-8", "replace")


def tree_stamp():
    lines = [ln for ln in _git("ls-files", "-s", "--", "integrations/bloomberg").splitlines()
             if ln.split("\t", 1)[-1] not in (DRIVER, TEST)]
    return hashlib.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest(), len(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"))
    ap.add_argument("--where", choices=("local",), default="local")
    ap.add_argument("--stamp", action="store_true")
    a = ap.parse_args()
    if a.stamp:
        print("%s over %d files" % tree_stamp())
        return 0
    if not a.crit:
        ap.error("--crit is required")
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    if a.crit == "AC3":
        stamp, count = tree_stamp()
        clause("C1 every other tracked file under integrations/bloomberg is the one at the cut", stamp == STAMP,
               "%d files; stamp %s" % (count, stamp[:16]))
        dirty = [ln for ln in _git("status", "--porcelain", "--", "integrations/bloomberg").splitlines()
                 if ln[3:].strip().strip('"') not in (DRIVER, TEST)]
        clause("C2 nothing else there is modified or untracked", not dirty, "%d other path(s) %s" % (len(dirty), dirty[:4]))
        return verdict(a, ok)

    if a.crit == "AC2":
        text = open(TEST, encoding="utf-8").read() if os.path.isfile(TEST) else ""
        clause("C1 the test file holds %s" % TEST_NAME, ("def %s(" % TEST_NAME) in text)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST],
                           capture_output=True, timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C2 every case in the file passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               "rc=%d" % p.returncode)
        return verdict(a, ok)

    from integrations.bloomberg.research import research_pulls as rp

    clause("C1 EXIT holds the new word at 6 and the four older codes", rp.EXIT.get(WORD) == CODE
           and all(rp.EXIT.get(k) == v for k, v in OLD.items()) and len(rp.EXIT) == 5, str(rp.EXIT))
    probe = getattr(rp, "library_importable", None)
    if not callable(probe):
        clause("C2 library_importable exists", False, "absent")
        return verdict(a, ok)
    clause("C2 library_importable answers a bool either way",
           probe("r78_no_such_library_zz") is False and probe("json") is True)

    seen = []

    def go(**kw):
        blp, writes = FakeBlp(), []
        res = rp.run("segments", list(N3), blp, lambda *w: writes.append(w),
                     vehicle_ran=lambda: seen.append("vehicle") or True,
                     health=lambda: seen.append("health") or kw.pop("healthy", True), **kw)
        return res, blp, writes

    try:
        res, blp, writes = go(library=lambda: False)
        clause("C3 a missing library stops before any other read", res.get("stopped") == WORD and blp.calls == []
               and writes == [] and seen == [] and res.get("calls") == 0, "stopped %r reads %s" % (res.get("stopped"), seen))
        r1, b1, _w = go(library=lambda: True)
        r2, b2, _w = go()
        blp3, writes3 = FakeBlp(), []
        r3 = rp.run("segments", list(N3), blp3, lambda *w: writes3.append(w), vehicle_ran=lambda: True,
                    health=lambda: False, library=lambda: True)
        clause("C4 the controls: present pulls, omitted is as today, a silent Terminal is still TERMINAL_DOWN",
               r1.get("stopped") is None and r1.get("pulled") == 3 and len(b1.calls) == 3 and r2.get("stopped") is None
               and r2.get("pulled") == 3 and r3.get("stopped") == "TERMINAL_DOWN" and blp3.calls == [],
               "%r %r %r" % (r1.get("stopped"), r2.get("stopped"), r3.get("stopped")))
    except TypeError as err:
        clause("C3 run takes the library read", False, str(err))
        return verdict(a, ok)

    touched = []
    rp.library_importable = lambda *_a, **_k: False
    rp.vehicle_ran_today = lambda: touched.append("vehicle") or True
    rp.terminal_healthy = lambda: touched.append("health") or True
    rp._load_blp_client = lambda: touched.append("client")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = rp.main(["run", "segments", "--probe", "AMD US Equity"])
    printed = buf.getvalue()
    print("   " + printed.strip().replace("\n", "\n   "))
    clause("C5 the command line returns 6, says why, names the interpreter and reads nothing else",
           code == CODE and ("stopped %s" % WORD) in printed and sys.executable in printed and touched == [],
           "exit %r other reads %s" % (code, touched))
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB14 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
