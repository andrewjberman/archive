"""IRPT_DASHBD round 17 (workstream B, issuer 2.0.0_SA_COO~P) -- E2 / P-5: the 0.35 pp tie-out of the 49 Financial served total
return against Black Diamond's own performancePeriod return over the full landed population (CTO round-15 analysis E2; PRD
C-TIEOUT). Zero vendor calls.

Usage: python <this file> <repo_root> <criterion_id>
  DB17-1-AC1  RECORD exists and reconciles: `segments_planned` equals the plan's segment count; graded + not_gradable ==
              segments_planned; within_tolerance + outside_tolerance == graded; tolerance_pp == 0.35; every outside segment
              carries a `reason` from the closed set (FLOW_TIMING, MISSING_PRICE, INCOME_DATE, COVERAGE_DAYS, UNEXPLAINED); every
              not_gradable segment carries a `why`; `vendor_calls` == 0. Base: FAIL (no record).
  DB17-1-AC2  the record names its inputs with denominators: the bronze prefix and its object count (5252), the served 49F
              series location and the account count it covers, and the plan path; its tests pass (at least 4, naming
              tolerance, reason and not_gradable). Base: FAIL.
  DB17-1-AC3  a GUARD: the worker's own commits touch only its grant. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "1b30e3b6d6"
W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~12/"
RECORD = W + "TIEOUT_49F_BD_POPULATION_E2.json"
TESTS = W + "tests/test_tieout_e2.py"
PLAN = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/BD_POPULATION_PLAN_E3.json"
REASONS = {"FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED"}
AUTHOR = "0.9.0_WK_IRPT_DASHBD~12"
GRANT = (W, "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-26.")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB17-1"))
        sys.exit(1)

    if cid == "DB17-1-AC1":
        p = root / RECORD
        if not p.is_file():
            fail("no %s" % RECORD)
        r = json.loads(p.read_bytes().decode("utf-8"))
        plan = json.loads((root / PLAN).read_bytes().decode("utf-8"))
        want = sum(len(x.get("segments") or []) for x in plan.get("request_list") or [])
        c = r.get("counts") or {}
        if r.get("vendor_calls") != 0:
            fail("vendor_calls %r" % r.get("vendor_calls"))
        if float(r.get("tolerance_pp", -1)) != 0.35:
            fail("tolerance_pp %r" % r.get("tolerance_pp"))
        if c.get("segments_planned") != want:
            fail("segments_planned %r, the plan holds %d" % (c.get("segments_planned"), want))
        if c.get("graded", -1) + c.get("not_gradable", -1) != want:
            fail("graded + not_gradable != %d" % want)
        if c.get("within_tolerance", -1) + c.get("outside_tolerance", -1) != c.get("graded"):
            fail("within + outside != graded")
        outs = [s for s in r.get("segments") or [] if s.get("verdict") == "OUTSIDE"]
        if len(outs) != c.get("outside_tolerance"):
            fail("%d OUTSIDE segment rows, counts say %r" % (len(outs), c.get("outside_tolerance")))
        bad = [s for s in outs if s.get("reason") not in REASONS]
        if bad:
            fail("%d outside segments lack a reason from the closed set" % len(bad))
        ng = [s for s in r.get("segments") or [] if s.get("verdict") == "NOT_GRADABLE" and not s.get("why")]
        if ng:
            fail("%d not_gradable segments lack a why" % len(ng))
        print("OK: %d planned = %d graded + %d not gradable; %d within, %d outside 0.35 pp" % (
            want, c["graded"], c["not_gradable"], c["within_tolerance"], c["outside_tolerance"]))
    elif cid == "DB17-1-AC2":
        p = root / RECORD
        if not p.is_file():
            fail("no %s" % RECORD)
        inp = json.loads(p.read_bytes().decode("utf-8")).get("inputs") or {}
        if inp.get("bronze_object_count") != 5252 or not inp.get("bronze_prefix"):
            fail("bronze input %r" % {k: inp.get(k) for k in ("bronze_prefix", "bronze_object_count")})
        if not inp.get("served_series") or not inp.get("served_accounts"):
            fail("served series not named with its account count")
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        for w in ("tolerance", "reason", "not_gradable"):
            if w not in src:
                fail("tests never name %r" % w)
        rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(t)], cwd=str(root),
                            capture_output=True, text=True, timeout=600)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
        m = re.search(r"(\d+) passed", out)
        if rr.returncode or not m or int(m.group(1)) < 4:
            fail("pytest: %s" % out[-300:])
        print("OK: inputs named; %s tests passed" % m.group(1))
    elif cid == "DB17-1-AC3":
        rr = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                            cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in rr.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
