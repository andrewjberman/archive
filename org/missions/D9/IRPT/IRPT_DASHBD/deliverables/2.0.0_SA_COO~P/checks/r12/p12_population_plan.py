"""IRPT_DASHBD round 12 (workstream B, issuer 2.0.0_SA_COO~P) -- E3 / P-5 build: the ONE Black Diamond population pull's script
and its OFFLINE plan (Andrew-direct ~22:0xZ 2026-10-04 card 2, record 66f1e98e98). No vendor call in this cell.

Usage: python <this file> <repo_root> <criterion_id>
  DB12-1-AC1  the plan file (PLAN) exists, was built with DRY_RUN=1, and records: accounts_total (the 49 Financial population
              read from the served gold), mapped and unmapped counts with every unmapped account carrying a reason,
              requests (one per mapped account with at least one gap-free segment of MIN_DAYS or more), vendor_calls == 0,
              and the word 66f1e98e98. Base: FAIL (no plan).
  DB12-1-AC2  the script's refusal tests (TESTS) pass, at least 4, naming: pull without --go, pull with a plan whose hash
              differs, pull when a pull record already exists (no second pull), and pull without the CTO shape ruling file.
              Base: FAIL (no tests).
  DB12-1-AC3  a GUARD: the worker's own commits since base touch only IRPT_DASHBD paths and no file under
              surprise-channel/remediations/. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "681c49eeeb"
W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/"
PLAN = W + "BD_POPULATION_PLAN_E3.json"
TESTS = W + "tests/test_bd_population_pull_e3.py"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~6"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB12-1"))
        sys.exit(1)

    if cid == "DB12-1-AC1":
        p = root / PLAN
        if not p.is_file():
            fail("no %s" % PLAN)
        plan = json.loads(p.read_bytes().decode("utf-8"))
        for k in ("accounts_total", "mapped", "unmapped", "requests", "vendor_calls", "dry_run", "word"):
            if k not in plan:
                fail("plan lacks %r" % k)
        if str(plan["dry_run"]) not in ("1", "True", "true"):
            fail("plan not built with DRY_RUN=1 (%r)" % plan["dry_run"])
        if plan["vendor_calls"] != 0:
            fail("vendor_calls %r" % plan["vendor_calls"])
        if "66f1e98e98" not in str(plan["word"]):
            fail("word %r" % plan["word"])
        un = plan["unmapped"] if isinstance(plan["unmapped"], list) else []
        if any(not str(u.get("reason") or "").strip() for u in un):
            fail("an unmapped account carries no reason")
        n_un = len(un) if isinstance(plan["unmapped"], list) else plan["unmapped"]
        n_map = plan["mapped"] if isinstance(plan["mapped"], int) else len(plan["mapped"])
        if plan["accounts_total"] <= 0 or n_map + n_un != plan["accounts_total"]:
            fail("accounts_total %r != mapped %r + unmapped %r" % (plan["accounts_total"], n_map, n_un))
        if not (0 < plan["requests"] <= n_map):
            fail("requests %r outside 1..mapped %r" % (plan["requests"], n_map))
        print("OK: population %d, mapped %d, unmapped %d (each with a reason), requests %d, vendor_calls 0" % (
            plan["accounts_total"], n_map, n_un, plan["requests"]))
    elif cid == "DB12-1-AC2":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        for w in ("--go", "hash", "second", "ruling"):
            if w not in src:
                fail("the tests never name %r" % w)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(t)], cwd=str(root), capture_output=True,
                           text=True, timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        m = re.search(r"(\d+) passed", out)
        if r.returncode or not m or int(m.group(1)) < 4:
            fail("pytest: %s" % out[-400:])
        print("OK: %s refusal tests passed" % m.group(1))
    elif cid == "DB12-1-AC3":
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
