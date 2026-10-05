"""IRPT_DASHBD round 14 (workstream B, issuer 2.0.0_SA_COO~P) -- E3 concurrent completion (CTO batches 249 and 250): the same ONE
Black Diamond pull, finished over the complement by concurrent workers on one shared bearer. No vendor call in this cell.

Usage: python <this file> <repo_root> <criterion_id>
  DB14-1-AC1  the concurrent-completion tests (TESTS) pass, at least 8, naming: shared bearer, ramp, 429, FAILED, sweep,
              consecutive, --go, denominators. Base: FAIL (no tests).
  DB14-1-AC2  the offline concurrent plan (CPLAN) is the run's whole input: built with DRY_RUN=1 and vendor_calls 0; counts
              reconcile (requests_planned == 5252, landed + complement == requests_planned, landed >= 144, complement ==
              len(complement_accounts), no complement account landed); and its `ruling` object carries the batch 249/250
              parameters (workers_start 2, workers_max 6, ramp_after_s 600, aggregate_rps 2, retries_per_call 1,
              consecutive_failures_abort 3, failed_cap 105). Base: FAIL.
  DB14-1-AC3  a GUARD: the worker's own commits since base touch only IRPT_DASHBD paths and no file under
              surprise-channel/remediations/. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "0b6a5aff58"
W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~8/"
TESTS = W + "tests/test_bd_population_concurrent_e3.py"
CPLAN = W + "BD_POPULATION_CONCURRENT_PLAN_E3.json"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~8"
WORDS = ("shared bearer", "ramp", "429", "FAILED", "sweep", "consecutive", "--go", "denominators")
RULING = {"workers_start": 2, "workers_max": 6, "ramp_after_s": 600, "aggregate_rps": 2, "retries_per_call": 1,
          "consecutive_failures_abort": 3, "failed_cap": 105}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB14-1"))
        sys.exit(1)

    if cid == "DB14-1-AC1":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        for w in WORDS:
            if w not in src:
                fail("the tests never name %r" % w)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(t)], cwd=str(root), capture_output=True,
                           text=True, timeout=600)
        out = (r.stdout or "") + (r.stderr or "")
        m = re.search(r"(\d+) passed", out)
        if r.returncode or not m or int(m.group(1)) < 8:
            fail("pytest: %s" % out[-400:])
        print("OK: %s concurrent-completion tests passed" % m.group(1))
    elif cid == "DB14-1-AC2":
        p = root / CPLAN
        if not p.is_file():
            fail("no %s" % CPLAN)
        c = json.loads(p.read_bytes().decode("utf-8"))
        for k in ("requests_planned", "landed", "complement", "complement_accounts", "landed_accounts", "vendor_calls",
                  "dry_run", "ruling"):
            if k not in c:
                fail("concurrent plan lacks %r" % k)
        if str(c["dry_run"]) not in ("1", "True", "true") or c["vendor_calls"] != 0:
            fail("not built dry (dry_run %r, vendor_calls %r)" % (c["dry_run"], c["vendor_calls"]))
        if c["requests_planned"] != 5252 or c["landed"] + c["complement"] != c["requests_planned"] or c["landed"] < 144:
            fail("counts do not reconcile: planned %r landed %r complement %r" % (c["requests_planned"], c["landed"], c["complement"]))
        if c["complement"] != len(c["complement_accounts"]) or set(c["complement_accounts"]) & set(c["landed_accounts"]):
            fail("complement list wrong or overlaps the landed set")
        bad = {k: c["ruling"].get(k) for k, v in RULING.items() if c["ruling"].get(k) != v}
        if bad:
            fail("ruling parameters differ from batches 249/250: %s" % bad)
        print("OK: planned %d = landed %d + complement %d; dry, 0 vendor calls; ruling parameters match"
              % (c["requests_planned"], c["landed"], c["complement"]))
    elif cid == "DB14-1-AC3":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if "/surprise-channel/remediations/" in c or not c.startswith("org/missions/D9/IRPT/IRPT_DASHBD/")]
        if bad:
            fail("out-of-bounds changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside IRPT_DASHBD" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
