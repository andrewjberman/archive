"""IRPT_BCKEND round 54 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the r54 release census tooling (CTO half condition 2):
a BUILD_ONLY mode for build-and-upload.sh, and a census that diffs a built zip against the live bundle member by member and
attributes every changed member.

Usage: python <this file> <repo_root> <criterion_id>
  IB54-1-AC1  infra/aws/lambda/ci/tests/test_build_only.sh exits 0 and prints at least 3 PASS lines (BUILD_ONLY=1 builds the zip,
              makes no aws call and leaves the source map unchanged). Base: FAIL (no test).
  IB54-1-AC2  the census tests (TESTS) pass, at least 5, naming RIDER, attributed, added, removed and changed. Base: FAIL.
  IB54-1-AC3  a GUARD: the worker's own commits since base touch only the grant and nothing under infra/aws/terraform/ or
              lambda-source-map.json. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "f58728dde1"
CI = "infra/aws/lambda/ci"
W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~126/"
TESTS = W + "tests/test_release_census.py"
AUTHOR = "0.9.0_WK_IRPT_BCKEND~126"
WORDS = ("RIDER", "attributed", "added", "removed", "changed")
GRANT = (CI + "/build-and-upload.sh", CI + "/tests/", W, "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-323.")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv  # a bare "bash" resolves to WSL on this host

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB54-1"))
        sys.exit(1)

    if cid == "IB54-1-AC1":
        t = root / CI / "tests" / "test_build_only.sh"
        if not t.is_file():
            fail("no %s" % t)
        r = subprocess.run(bash_argv(str(t)), cwd=str(root), capture_output=True, text=True, timeout=900)
        out = (r.stdout or "") + (r.stderr or "")
        n = len(re.findall(r"^PASS", out, re.M))
        print(out[-600:])
        if r.returncode or n < 3:
            fail("rc %d, %d PASS lines" % (r.returncode, n))
        print("OK: %d PASS lines" % n)
    elif cid == "IB54-1-AC2":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        missing = [w for w in WORDS if w not in src]
        if missing:
            fail("the tests never name %s" % missing)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(t)], cwd=str(root),
                           capture_output=True, text=True, timeout=600)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
        m = re.search(r"(\d+) passed", out)
        if r.returncode or not m or int(m.group(1)) < 5:
            fail("pytest: %s" % out[-400:])
        print("OK: %s census tests passed" % m.group(1))
    elif cid == "IB54-1-AC3":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if c.startswith("infra/aws/terraform/") or c.endswith("lambda-source-map.json")
               or not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
