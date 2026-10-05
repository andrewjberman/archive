"""IRPT_DASHBD round 16 (workstream B, issuer 2.0.0_SA_COO~P) -- the concurrent BD runner must never stop silently: relaunch 2
ended ~10:27Z with `complete: true, aborted: null` while 2,384 accounts were never requested, because worker threads died on an
uncaught http.client.RemoteDisconnected raised on the bearer-mint path.

Usage: python <this file> <repo_root> <criterion_id>
  DB16-1-AC1  the runner's tests pass, at least 3 NEW tests naming mint, crash and complete: a transport error on the mint is
              retried once and a second failure aborts the run with a reason; a worker's unexpected exception aborts the run
              and records the in-flight account; `complete` is true only when the queue is empty and nothing aborted. The
              existing tests still pass. Base: FAIL.
  DB16-1-AC2  a GUARD: the worker's commits touch only its grant. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "e8564f6a18"
W8 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~8/"
TESTS = W8 + "tests/test_bd_population_concurrent_e3.py"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~11"
GRANT = (W8 + "bd_population_concurrent_e3.py", W8 + "tests/", "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~11/",
         "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-25.")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB16-1"))
        sys.exit(1)

    if cid == "DB16-1-AC1":
        t = root / TESTS
        src = t.read_bytes().decode("utf-8")
        names = re.findall(r"def (test_\w+)", src)
        new = [n for n in names if re.search(r"mint|crash|complete", n)]
        if len([n for n in new if "mint" in n]) < 1 or len([n for n in new if "crash" in n]) < 1 or len([n for n in new if "complete" in n]) < 1:
            fail("tests naming mint, crash and complete not all present: %s" % new)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(t)], cwd=str(root),
                           capture_output=True, text=True, timeout=900)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
        last = ([ln for ln in out.splitlines() if ln.strip()] or ["(no output)"])[-1]
        if r.returncode or re.search(r"\d+ (failed|error)", last):
            fail("pytest: %s" % last)
        print("OK: %s; new tests %s" % (last, new))
    elif cid == "DB16-1-AC2":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
