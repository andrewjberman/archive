"""AMGT_RESAPP round 78 -- AMGT-bb-22, the divergence score reads the dispersion fields Bloomberg serves.

  python r78_bb22.py --crit AC1|AC2 --where local

The probe of 2026-10-07 15:17Z by AMGT_CORPUS (evidence r40_ap10_probe_BA_20261007.txt @e3579e3693, msg 31085): Bloomberg
refuses BEST_CPS_STANDARD_DEV, BEST_CPS_AVG, BEST_EPS_STANDARD_DEV and BEST_EPS_AVG as invalid fields and returns
BEST_CPS_STDDEV, BEST_EPS_STDDEV, BEST_CPS_NUMEST and BEST_EPS_NUMEST. The mean is BEST_CPS / BEST_EPS.

AC1 (build) lib/research/scores/divergence.py:
  C1 CFPS_FIELDS is (BEST_CPS_STDDEV, BEST_CPS, BEST_CPS_NUMEST) and EPS_FIELDS is (BEST_EPS_STDDEV, BEST_EPS, BEST_EPS_NUMEST);
  C2 none of the four refused names remains in any .py under lib/research/scores/ or in lib/research/api/tests/test_score_modules.py.
AC2 (bound) the score tests pass: lib/research/scores/tests/ and lib/research/api/tests/test_score_modules.py.
Verdict: R78 BB22 <crit> SERVED: YES|NO (exit 0|1). Reads the tree only.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

REFUSED = ("BEST_CPS_STANDARD_DEV", "BEST_CPS_AVG", "BEST_EPS_STANDARD_DEV", "BEST_EPS_AVG")
WANT_CFPS = ("BEST_CPS_STDDEV", "BEST_CPS", "BEST_CPS_NUMEST")
WANT_EPS = ("BEST_EPS_STDDEV", "BEST_EPS", "BEST_EPS_NUMEST")


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def ac1(root):
    from lib.research.scores import divergence

    results = []
    ok1 = tuple(divergence.CFPS_FIELDS) == WANT_CFPS and tuple(divergence.EPS_FIELDS) == WANT_EPS
    results.append(ok1)
    print("%s C1 the two field lists are the served names %s %s" % ("PASS" if ok1 else "FAIL", tuple(divergence.CFPS_FIELDS),
                                                                   tuple(divergence.EPS_FIELDS)))
    files = [os.path.join(root, "lib", "research", "api", "tests", "test_score_modules.py")]
    for base, _dirs, names in os.walk(os.path.join(root, "lib", "research", "scores")):
        files += [os.path.join(base, n) for n in names if n.endswith(".py")]
    hits = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        n = sum(text.count(w) for w in REFUSED)
        if n:
            hits.append((os.path.relpath(path, root).replace(os.sep, "/"), n))
    ok2 = not hits
    results.append(ok2)
    print("%s C2 no refused name remains files read %d, with a refused name %d %s" % ("PASS" if ok2 else "FAIL", len(files),
                                                                                  len(hits), hits[:4]))
    ok = all(results)
    print("R78 BB22 AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac2(root):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "lib/research/scores/tests", "lib/research/api/tests/test_score_modules.py"],
                       cwd=root, capture_output=True, text=True, env=dict(os.environ, PYTHONPATH=root))
    last = [ln for ln in p.stdout.splitlines() if ln.strip()][-1:] or [""]
    ok = p.returncode == 0
    print("%s B1 the score tests pass rc=%d %s" % ("PASS" if ok else "FAIL", p.returncode, last[0][:120]))
    print("R78 BB22 AC2 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    root = _root()
    sys.path.insert(0, root)
    return ac1(root) if a.crit == "AC1" else ac2(root)


if __name__ == "__main__":
    sys.exit(main())
