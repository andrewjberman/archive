"""AMGT_RESAPP round 77 -- AMGT-ba-15 (the identity grading read and the ONE PAGER precedence). Issuer checks.

  python r77_ba15.py --crit AC1|AC2|AC3 [--where local]

AC1 (build)  lib.research.identity.covered_keyed.grade(crosswalk_document, coverage_document, corpus_records):
             the denominator is the coverage list's records; keyed N of M is printed; a record the served crosswalk
             does not key resolves ONLY through a CORPUS record for the same folder; every residual is named with a
             reason. Control: a folder CORPUS does not hold stays UNRESOLVED.
AC2 (build)  covered_keyed.run() on the SERVED crosswalk, the coverage list and CORPUS's registered keys
             (read-only pool and library reads, no vendor call): denominator 89, keyed + residual = 89.
AC3 (build)  lib.research.identity.one_pager_precedence: the workbook with the newer stored modified date is read;
             the other is listed as superseded, with its date, on the same line.
"""
import argparse
import importlib
import os
import sys
import tempfile
import time

OK = []


def clause(label, ok, detail=""):
    OK.append(bool(ok))
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))


def load(name):
    try:
        return importlib.import_module(name), None
    except Exception as err:  # noqa: BLE001 -- the base has no module
        return None, "%s: %s" % (type(err).__name__, err)


def rec(folder, key):
    return {"security_key": key, "resolution": "MEASURED" if key else "UNRESOLVED",
            "source_row": {"folder": folder}}


def ac1():
    mod, err = load("lib.research.identity.covered_keyed")
    clause("C0 lib.research.identity.covered_keyed imports", mod is not None, err or "")
    if mod is None:
        return
    coverage = {"names": [{"folder": f} for f in ("Alpha AAA US", "Beta BBB US", "Gamma GGG LN", "Delta DDD FP")]}
    crosswalk = {"records": [rec("Alpha AAA US", "AAA_US_Equity"), rec("Beta BBB US", "BBB_US_Equity"),
                             rec(None, "ZZZ_US_Equity")]}
    corpus = [{"folder": "Gamma GGG LN", "security_key": "GGG_LN_Equity"},
              {"folder": "Unrelated UUU US", "security_key": "UUU_US_Equity"}]
    out = mod.grade(crosswalk, coverage, corpus)
    clause("C1 the denominator is the coverage list (4), never the crosswalk's record count",
           (out or {}).get("denominator") == 4, "got %s" % (out or {}).get("denominator"))
    clause("C2 keyed 3 of 4: two from the served crosswalk, one resolved through CORPUS's record for the folder",
           (out or {}).get("keyed") == 3, "got %s" % (out or {}).get("keyed"))
    residual = (out or {}).get("residual") or []
    clause("C3 control: the folder CORPUS does not hold stays UNRESOLVED, named with its reason",
           len(residual) == 1 and residual[0].get("folder") == "Delta DDD FP" and bool(residual[0].get("reason")),
           str(residual)[:160])
    none = mod.grade(crosswalk, coverage, None)
    clause("C4 with CORPUS unread, nothing is resolved through it and the read says so",
           (none or {}).get("keyed") == 2 and len((none or {}).get("residual") or []) == 2,
           "keyed %s residual %s" % ((none or {}).get("keyed"), len((none or {}).get("residual") or [])))


def ac2():
    mod, err = load("lib.research.identity.covered_keyed")
    clause("C0 lib.research.identity.covered_keyed imports", mod is not None, err or "")
    if mod is None:
        return
    out = mod.run()
    den, keyed, residual = (out or {}).get("denominator"), (out or {}).get("keyed"), (out or {}).get("residual") or []
    print("   keyed %s of %s; residual %s; crosswalk %s; corpus %s"
          % (keyed, den, len(residual), (out or {}).get("crosswalk_loaded_from"), (out or {}).get("corpus")))
    clause("C1 the denominator is the 89 covered records", den == 89, "got %s" % den)
    clause("C2 keyed + residual = the denominator, and keyed is 33 or more",
           isinstance(keyed, int) and keyed >= 33 and keyed + len(residual) == den, "keyed %s" % keyed)
    clause("C3 every residual is named with a reason",
           all(r.get("folder") and r.get("reason") for r in residual), "%d residual" % len(residual))


def ac3():
    mod, err = load("lib.research.identity.one_pager_precedence")
    clause("C0 lib.research.identity.one_pager_precedence imports", mod is not None, err or "")
    if mod is None:
        return
    with tempfile.TemporaryDirectory() as d:
        old = os.path.join(d, "ACME ONE PAGER 2025 11 02_v1.xlsx")
        new = os.path.join(d, "ACME ONE PAGER 2026 01 27_v2.xlsx")
        for p in (old, new):
            open(p, "wb").close()
        now = time.time()
        os.utime(new, (now - 86400 * 10, now - 86400 * 10))   # the NEWER-named file is the OLDER stored one
        os.utime(old, (now - 86400 * 2, now - 86400 * 2))
        names = sorted(os.path.basename(p) for p in (old, new))
        ordered = mod.ordered(d, names)
        clause("C1 the workbook with the newer stored modified date is read first (not the name order)",
               list(ordered)[:1] == [os.path.basename(old)], str(ordered))
        line = mod.line("Acme ACME US", d, names)
        days = {time.strftime("%Y-%m-%d", f(now - 86400 * 10)) for f in (time.gmtime, time.localtime)}
        clause("C2 the other workbook is listed as superseded, with its date, on the same line",
               isinstance(line, str) and "\n" not in line and os.path.basename(new) in line
               and "superseded" in line.lower() and any(day in line for day in days), str(line)[:200])
        one = mod.ordered(d, [os.path.basename(old)])
        clause("C3 one workbook is returned as it is", list(one) == [os.path.basename(old)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    {"AC1": ac1, "AC2": ac2, "AC3": ac3}[a.crit]()
    ok = bool(OK) and all(OK)
    print("R77 BA15 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
