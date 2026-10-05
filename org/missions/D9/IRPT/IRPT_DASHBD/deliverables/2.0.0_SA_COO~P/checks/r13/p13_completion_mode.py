"""IRPT_DASHBD round 13 (workstream B, issuer 2.0.0_SA_COO~P) -- E3 completion mode (CTO batch 248): the same ONE Black
Diamond pull, finished over the accounts not yet answered, re-minting the bearer before it expires. No vendor call in this cell.

Usage: python <this file> <repo_root> <criterion_id>
  DB13-1-AC1  the completion tests (TESTS) pass, at least 5, naming: complement, landed, re-mint, denominators, --go. Base:
              FAIL (no tests).
  DB13-1-AC2  the offline completion plan (CPLAN) exists, built with DRY_RUN=1 and vendor_calls 0, and its counts reconcile:
              requests_planned == 5252, landed + complement == requests_planned, landed >= 19 (read from S3 under
              pull=20261004), complement == len(complement_accounts), and no complement account is a landed one. Base: FAIL.
  DB13-1-AC3  a GUARD: the worker's own commits since base touch only IRPT_DASHBD paths and no file under
              surprise-channel/remediations/. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "0dc80bec30"
W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~7/"
TESTS = W + "tests/test_bd_population_complete_e3.py"
CPLAN = W + "BD_POPULATION_COMPLETION_PLAN_E3.json"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~7"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB13-1"))
        sys.exit(1)

    if cid == "DB13-1-AC1":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        for w in ("complement", "landed", "re-mint", "denominators", "--go"):
            if w not in src:
                fail("the tests never name %r" % w)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(t)], cwd=str(root), capture_output=True,
                           text=True, timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        m = re.search(r"(\d+) passed", out)
        if r.returncode or not m or int(m.group(1)) < 5:
            fail("pytest: %s" % out[-400:])
        print("OK: %s completion tests passed" % m.group(1))
    elif cid == "DB13-1-AC2":
        p = root / CPLAN
        if not p.is_file():
            fail("no %s" % CPLAN)
        c = json.loads(p.read_bytes().decode("utf-8"))
        for k in ("requests_planned", "landed", "complement", "complement_accounts", "landed_accounts", "vendor_calls", "dry_run"):
            if k not in c:
                fail("completion plan lacks %r" % k)
        if str(c["dry_run"]) not in ("1", "True", "true") or c["vendor_calls"] != 0:
            fail("not built dry (dry_run %r, vendor_calls %r)" % (c["dry_run"], c["vendor_calls"]))
        if c["requests_planned"] != 5252 or c["landed"] + c["complement"] != c["requests_planned"] or c["landed"] < 19:
            fail("counts do not reconcile: planned %r landed %r complement %r" % (c["requests_planned"], c["landed"], c["complement"]))
        if c["complement"] != len(c["complement_accounts"]) or set(c["complement_accounts"]) & set(c["landed_accounts"]):
            fail("complement list wrong or overlaps the landed set")
        print("OK: planned %d = landed %d + complement %d; dry, 0 vendor calls" % (c["requests_planned"], c["landed"], c["complement"]))
    elif cid == "DB13-1-AC3":
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
