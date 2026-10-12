"""IRPT_BCKEND round 146 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD order, nothing served:
  IB146-1  IB-pr-450  the second witness's guard (PRD v0.40 and v0.41, both signed) as one pure function with its tests:
                      data/assets/scripts/gold/irpt_reporting/second_witness_guard.py :: second_witness_grades(bars, t) -> bool

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no module).
  IB146-1-AC1  the module's own test file passes under pytest.
  IB146-1-AC2  the issuer's cases, run here against the function: a moved bar grades; an unmoved bar does not; a bar inside the
               tolerance does not; no bar on the day does not; NO BAR ON THE CALENDAR'S PRIOR TRADING DAY does not, even where
               an earlier row exists and differs (the v0.41 sentence); a Monday is compared with the Friday before it.
  IB146-1-AC3  nothing served: no file under data/ or infra/ other than the module's own test imports or names the module.
"""
import datetime as dt
import importlib.util
import subprocess
import sys
from pathlib import Path

MOD = "data/assets/scripts/gold/irpt_reporting/second_witness_guard.py"
TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_second_witness_guard.py"
D = dt.date


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB146"))
        sys.exit(1)

    if not (root / MOD).is_file():
        fail("no %s" % MOD)
    if cid == "IB146-1-AC1":
        if not (root / TEST).is_file():
            fail("no %s" % TEST)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(root / TEST)], cwd=str(root),
                           capture_output=True, text=True, timeout=110)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        if r.returncode != 0 or " passed" not in tail or "failed" in tail:
            fail("pytest rc=%d: %s" % (r.returncode, tail[:160]))
        print("OK: %s" % tail[:120])
    elif cid == "IB146-1-AC2":
        sys.path.insert(0, str(root))
        spec = importlib.util.spec_from_file_location("second_witness_guard", str(root / MOD))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        g = m.second_witness_grades
        fri0, mon, tue, wed, thu = D(2026, 10, 2), D(2026, 10, 5), D(2026, 10, 6), D(2026, 10, 7), D(2026, 10, 8)
        cases = [
            ("a moved bar grades", {mon: 10.00, tue: 10.05}, tue, True),
            ("an unmoved bar does not", {mon: 10.00, tue: 10.00}, tue, False),
            ("a bar inside relative 1e-4 does not", {mon: 100.00, tue: 100.005}, tue, False),
            ("a bar just outside relative 1e-4 grades", {mon: 100.00, tue: 100.02}, tue, True),
            ("no bar on the day does not", {mon: 10.00}, tue, False),
            ("no bar on the prior trading day does not, though an earlier row differs", {mon: 10.00, wed: 10.40}, wed, False),
            ("no bar on the prior trading day does not, with a later day present", {mon: 10.00, wed: 10.40, thu: 10.50}, wed, False),
            ("a Monday is compared with the Friday before it: moved", {fri0: 10.00, mon: 10.10}, mon, True),
            ("a Monday is compared with the Friday before it: unmoved", {fri0: 10.00, mon: 10.00}, mon, False),
            ("an empty series does not", {}, tue, False),
        ]
        bad = []
        for name, bars, t, want in cases:
            got = g(bars, t)
            if got is not want:
                bad.append("%s: want %r, got %r" % (name, want, got))
        if bad:
            fail("; ".join(bad)[:600])
        print("OK: %d of %d issuer cases read as expected" % (len(cases), len(cases)))
    elif cid == "IB146-1-AC3":
        hits = []
        for top in ("data", "infra"):
            for f in (root / top).rglob("*.py"):
                rel = f.relative_to(root).as_posix()
                if rel in (MOD, TEST) or "__pycache__" in rel:
                    continue
                try:
                    if "second_witness_guard" in f.read_text(encoding="utf-8", errors="replace"):
                        hits.append(rel)
                except OSError:
                    continue
        if hits:
            fail("the module is named outside its own test: %s" % ", ".join(hits[:5]))
        print("OK: no file under data/ or infra/ other than the module's test names it: nothing served")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
