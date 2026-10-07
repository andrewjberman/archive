"""AMGT_RESAPP round 77 -- AMGT-ba-13: production code no longer names a worker's deliverables folder (row Z-W37-S2).

  --crit AC1 --where local

AC1 (build, with its control):
    C1 no production .py file under lib/ names "0.9.0_WK_AMGT_RESAPP~" (tests, conftest.py and test_*.py are not
       production; 19 files at the cut);
    C2 the two packaging scripts under infra/aws/terraform/harvest/ (build-and-upload-scoped-amgt.sh and
       lambda_src/build_zip.py) no longer name one either (3 lines at the cut);
    C3 CONTROL: the production files under integrations/bloomberg/ that name one are exactly the five listed at the cut
       -- Andrew's no-modify order stands, so that list neither shrinks nor grows.
(AC2 is the worker's own equal_reads.py; see the order.)
Verdict: R77 BA13 AC1 SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import os
import sys

NEEDLE = "0.9.0_WK_AMGT_RESAPP~"
BLOOMBERG_AT_CUT = [
    "integrations/bloomberg/auth/bbg_credentials.py",
    "integrations/bloomberg/research/build_unit_map.py",
    "integrations/bloomberg/research/derive_fye_fixed.py",
    "integrations/bloomberg/research/price_axis_pull.py",
    "integrations/bloomberg/research/pull_baba_daily_px.py",
]
PACKAGING = [
    "infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh",
    "infra/aws/terraform/harvest/lambda_src/build_zip.py",
]


def _production_py(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("tests", "__pycache__", "node_modules", ".git")]
        for name in files:
            if name.endswith(".py") and not name.startswith("test_") and name != "conftest.py":
                yield os.path.join(base, name).replace("\\", "/")


def _names(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return sum(1 for line in handle if NEEDLE in line)
    except OSError:
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1",), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    lib_hits = {p: _names(p) for p in _production_py("lib")}
    lib_hits = {p: n for p, n in lib_hits.items() if n}
    print(f"   lib/: {len(lib_hits)} production file(s), {sum(lib_hits.values())} line(s) name a worker folder")
    for path in sorted(lib_hits):
        print(f"      {path}: {lib_hits[path]}")
    clause("C1 no production file under lib/ names a worker folder", not lib_hits, f"{len(lib_hits)} file(s)")
    pack = {p: _names(p) for p in PACKAGING}
    print(f"   packaging: {pack}")
    clause("C2 the two packaging scripts name none", not any(pack.values()), f"{sum(pack.values())} line(s)")
    bbg = sorted(p for p in _production_py("integrations/bloomberg") if _names(p))
    clause("C3 control: the integrations/bloomberg list is the five at the cut", bbg == BLOOMBERG_AT_CUT,
           f"{len(bbg)} file(s) {[p for p in bbg if p not in BLOOMBERG_AT_CUT] or ''}")
    yes = bool(ok) and all(ok)
    print(f"R77 BA13 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
