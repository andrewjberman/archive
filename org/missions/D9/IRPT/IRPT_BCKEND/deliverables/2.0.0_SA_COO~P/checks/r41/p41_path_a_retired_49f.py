"""Round 41 (IRPT_BCKEND ~P, CTO batch 201, P-6) -- PATH A no longer composes 49 Financial: a 49F Performance request (fresh or a
retained reopen) is refused by a NAMED retirement under the existing UNSUPPORTED_OPERATION code; Inflection and Cottonwood are
unchanged.

Usage: python <this file> <repo_root> <criterion_id>
  IB41-1-AC1  infra/aws/lambda/investor-reporting/performance/retained.py, imported: COMPOSED_FIRMS does not contain
              tenants._CANONICAL_49F and still contains _CANONICAL_INF and _CANONICAL_COT; a class whose name contains "Retired"
              subclasses ProviderPathNotComposed. Then performance/tests/test_path_a_retired_49f.py names "49", "Retired" and
              "UNSUPPORTED_OPERATION", and at least 3 of its tests pass, 0 failed.
  IB41-1-AC2  the whole performance suite: at least 249 pass (246 at the base, 2026-10-03, plus 3), 0 failed.
Bounded at 110 s per pytest. Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

P = "infra/aws/lambda/investor-reporting/performance/"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB41"))
        sys.exit(1)

    def pytest(target, floor):
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                               cwd=str(root), capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("pytest exceeded 110 s on %s" % target)
        out = (r.stdout or "") + (r.stderr or "")
        bad = re.search(r"(\d+) (failed|error)", out)
        p = re.search(r"(\d+) passed", out)
        if bad or not p or int(p.group(1)) < floor:
            fail("%s: %s (floor %d)" % (target, bad.group(0) if bad else (p.group(0) if p else out[-200:]), floor))
        return int(p.group(1))

    if cid == "IB41-1-AC1":
        probe = ("import sys; sys.path[:0]=[%r, %r, %r]\n"
                 "import retained, tenants\n"
                 "c = set(retained.COMPOSED_FIRMS)\n"
                 "ret = [n for n in dir(retained) if 'Retired' in n and isinstance(getattr(retained, n), type) "
                 "and issubclass(getattr(retained, n), retained.ProviderPathNotComposed)]\n"
                 "print('49F' if tenants._CANONICAL_49F in c else 'no49F', 'INF' if tenants._CANONICAL_INF in c else 'noINF', "
                 "'COT' if tenants._CANONICAL_COT in c else 'noCOT', 'RET=' + ','.join(ret))\n"
                 % (str(root / P), str(root / "infra/aws/lambda/investor-reporting/reports"), str(root)))
        r = subprocess.run([sys.executable, "-c", probe], cwd=str(root / P), capture_output=True, text=True, timeout=110)
        out = (r.stdout or "").strip()
        if r.returncode != 0:
            fail("cannot import retained.py: %s" % (r.stderr or "")[-300:])
        if not out.startswith("no49F INF COT") or "RET=" not in out or out.endswith("RET="):
            fail("composition or retirement class wrong: %s" % out)
        t = root / (P + "tests/test_path_a_retired_49f.py")
        if not t.is_file():
            fail("no performance/tests/test_path_a_retired_49f.py")
        src = t.read_text(encoding="utf-8")
        for w in ("49", "Retired", "UNSUPPORTED_OPERATION"):
            if w not in src:
                fail("the test never names %r" % w)
        n = pytest(P + "tests/test_path_a_retired_49f.py", 3)
        print("OK: %s; retirement tests %d passed" % (out, n))
    elif cid == "IB41-1-AC2":
        n = pytest(P + "tests", 249)
        print("OK: performance suite %d passed, 0 failed" % n)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
