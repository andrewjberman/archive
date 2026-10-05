"""IRPT_BCKEND round 51 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the ONE repair cell over the LOCAL part of E1's non-BLOCKING
remainder (decomposition section 42 / 45): rows S220, S282, W62-S1, S241, S297, S298, W101-S14, W101-S16.

Usage: python <this file> <repo_root> <criterion_id>
  IB51-1-AC1  every named suite passes with 0 failed: the S220 census, the S282 installed-schema test, W62-S1's
              test_submit_async.py run ALONE from export/, the holdings-performance, performance and export suites, and the CI
              shell tests (test_sha_handoff.sh plus any new tests/test_*.sh). Base: FAIL (S220 6 failed, S282 1 failed, W62-S1
              1 failed alone).
  IB51-1-AC2  each of the eight row ids is named in a test file added or changed since base. Base: FAIL.
  IB51-1-AC3  a GUARD: the worker's own commits since base touch only the grant (investor-reporting code and tests named
              by the order, infra/aws/lambda/ci/build-and-upload.sh and ci/tests/, the worker's deliverables, the channel and
              the order) and nothing under infra/aws/terraform/. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "0c3bc53717"
IR = "infra/aws/lambda/investor-reporting"
CI = "infra/aws/lambda/ci"
AUTHOR = "0.9.0_WK_IRPT_BCKEND~123"
ROWS = ("S220", "S282", "W62-S1", "S241", "S297", "S298", "W101-S14", "W101-S16")
SUITES = [  # (cwd relative to root, pytest target)
    (IR, "_authz/tests/test_unguarded_census.py"),
    (IR, "reports/tests/test_generate_installed.py"),
    (IR + "/export", "tests/test_submit_async.py"),
    (IR + "/holdings-performance", "tests/"),
    (IR + "/performance", "tests/"),
    (IR + "/export", "tests/"),
    (IR, "_authz/tests/"),
]
GRANT = (IR + "/_authz/", IR + "/reports/tests/", IR + "/export/", IR + "/holdings-performance/", IR + "/performance/",
         CI + "/build-and-upload.sh", CI + "/tests/", "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~123/",
         "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-320.")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv  # a bare "bash" resolves to WSL on this host

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB51-1"))
        sys.exit(1)

    if cid == "IB51-1-AC1":
        bad = []
        for cwd, target in SUITES:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], cwd=str(root / cwd),
                               capture_output=True, text=True, timeout=900)
            out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
            last = [ln for ln in out.splitlines() if ln.strip()][-1:] or ["(no output)"]
            print("%s :: %s -> rc %d :: %s" % (cwd, target, r.returncode, last[0]))
            if r.returncode or re.search(r"\d+ (failed|error)", last[0]):
                bad.append("%s/%s" % (cwd, target))
        for sh in sorted((root / CI / "tests").glob("test_*.sh")):
            r = subprocess.run(bash_argv(str(sh)), cwd=str(root), capture_output=True, text=True, timeout=600)
            print("%s -> rc %d" % (sh.name, r.returncode))
            if r.returncode:
                bad.append(sh.name)
        if bad:
            fail("failing: %s" % bad)
        print("OK: %d pytest suites and the CI shell tests pass" % len(SUITES))
    elif cid == "IB51-1-AC2":
        r = subprocess.run(["git", "diff", "--name-only", BASE, "HEAD", "--", IR, CI + "/tests"], cwd=str(root),
                           capture_output=True)
        tests = [ln for ln in r.stdout.decode("utf-8").splitlines() if "/tests/" in ln and (root / ln).is_file()]
        text = "\n".join((root / t).read_bytes().decode("utf-8", "replace") for t in tests)
        missing = [rid for rid in ROWS if not re.search(r"(?<![A-Z0-9-])%s(?![0-9])" % re.escape(rid), text)]
        if missing:
            fail("rows not named in any test changed since base (%d test files): %s" % (len(tests), missing))
        print("OK: all %d rows named across %d changed test file(s)" % (len(ROWS), len(tests)))
    elif cid == "IB51-1-AC3":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if c.startswith("infra/aws/terraform/") or not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
