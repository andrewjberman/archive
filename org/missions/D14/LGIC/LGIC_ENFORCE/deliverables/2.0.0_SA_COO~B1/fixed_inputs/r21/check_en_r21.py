"""LGIC_ENFORCE round 21 -- the issuer's fixed checks, one subcommand per criterion (2.0.0_SA_COO~B1).

Run from the root of the worktree under test:  python <this file> <arm>
Each arm prints exactly one PASS-* or FAIL-* verdict line last, and exits 0 only on PASS.

  unit        EN-aa-1  lib/tests/test_opal_lgctfm.py passes whole under pytest (rc 0, no failure).
  failclosed  EN-aa-1  a sparse worktree WITHOUT LEGACY_SERVED_PATHS.json: `opal_lgctfm.py walk` exits non-zero, prints
                       `MISSING INPUT <that path>`, and writes no contract; the same walk in THIS checkout completes (rc 0,
                       contract.json written). The two arms run in one invocation.
  pattern     EN-aa-2  the commit gate on the planted S152 commit (a09b284984, branch qa/lgic-enforce-r20-s12) prints a
                       NAMING line for `investor-reporting/directory` and its summary is never `0 graded`; the hand-typed
                       control literal is still graded.
  scope       EN-aa-3  lib/tests/test_opal_naming_scope.py prints SCOPE-TEST ok=True.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
LEGACY_REL = "org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json"
WALK = ["walk", "--subject", "cottonwood", "--seed", "opal-data-assets/cottonwood/"]
S152_COMMIT = "a09b284984"
PLANTED = "investor-reporting/directory"
SPARSE = ["/lib/", "/infra/", "/.tools/", "/org/standards/", "/org/missions/D14/LGIC/", "!/" + LEGACY_REL]


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def run(args, cwd=ROOT, timeout=600):
    p = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout)
    out = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, out.replace("\r\n", "\n")


def arm_failclosed():
    need(os.path.isfile(os.path.join(ROOT, LEGACY_REL)), "this checkout lacks %s: the full-checkout arm cannot run" % LEGACY_REL)
    tmp = tempfile.mkdtemp(prefix="r21-sparse-")
    wt = os.path.join(tmp, "wt")
    try:
        rc, out = run(["git", "worktree", "add", "--no-checkout", "--detach", wt, "HEAD"])
        need(rc == 0, "could not add the sparse worktree: %s" % out[-300:])
        rc, out = run(["git", "sparse-checkout", "set", "--no-cone"] + SPARSE, cwd=wt)
        need(rc == 0, "sparse-checkout set failed: %s" % out[-300:])
        rc, out = run(["git", "checkout"], cwd=wt, timeout=900)
        need(rc == 0, "sparse checkout failed: %s" % out[-300:])
        need(not os.path.exists(os.path.join(wt, LEGACY_REL)), "the sparse worktree still carries %s" % LEGACY_REL)
        need(os.path.isfile(os.path.join(wt, "lib", "opal_lgctfm.py")), "the sparse worktree lacks lib/opal_lgctfm.py")
        sp_out = os.path.join(tmp, "sparse_out")
        rc_s, out_s = run([sys.executable, "lib/opal_lgctfm.py"] + WALK + ["--out", sp_out], cwd=wt, timeout=600)
        print("sparse: rc=%d last=%r" % (rc_s, (out_s.strip().splitlines() or [""])[-1][:200]))
        need(rc_s != 0, "the sparse walk exited 0 without %s: it fails OPEN" % LEGACY_REL)
        need(re.search(r"MISSING INPUT \S*%s" % re.escape(LEGACY_REL.split("/")[-1]), out_s),
             "the sparse walk did not print MISSING INPUT naming %s (rc=%d): %s" % (LEGACY_REL, rc_s, out_s[-300:]))
        need(not os.path.exists(os.path.join(sp_out, "contract.json")), "the sparse walk wrote a contract.json (verdict rows)")
    finally:
        run(["git", "worktree", "remove", "--force", wt])
        shutil.rmtree(tmp, ignore_errors=True)
    full_out = tempfile.mkdtemp(prefix="r21-full-")
    try:
        rc_f, out_f = run([sys.executable, "lib/opal_lgctfm.py"] + WALK + ["--out", full_out], timeout=900)
        print("full: rc=%d last=%r" % (rc_f, (out_f.strip().splitlines() or [""])[-1][:200]))
        need(rc_f == 0 and os.path.isfile(os.path.join(full_out, "contract.json")),
             "the full-checkout walk did not complete (rc=%d): %s" % (rc_f, out_f[-300:]))
        need("MISSING INPUT" not in out_f, "the full-checkout walk printed MISSING INPUT")
    finally:
        shutil.rmtree(full_out, ignore_errors=True)
    return "PASS-R21-FAILCLOSED"


CONTROL_FIXTURE = """diff --git a/infra/aws/terraform/zz-r21-control/main.tf b/infra/aws/terraform/zz-r21-control/main.tf
new file mode 100644
--- /dev/null
+++ b/infra/aws/terraform/zz-r21-control/main.tf
@@ -0,0 +1,3 @@
+resource "aws_iam_role" "probe" {
+  name = "zz-probe-scheduler-role-typed"
+}
"""


def _gate_on(text):
    with tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False, encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    try:
        return run([sys.executable, ".tools/naming-gate.py", "--diff", fh.name], timeout=300)
    finally:
        os.unlink(fh.name)


def arm_pattern():
    rc, diff = run(["git", "show", "--format=", S152_COMMIT])
    need(rc == 0 and PLANTED in diff, "the planted commit %s is not readable or does not add %r" % (S152_COMMIT, PLANTED))
    rc, out = _gate_on(diff)
    summ = re.search(r"^NAMING-GATE: (PASS|WARN|REFUSE) (\d+) graded", out, re.M)
    need(summ is not None, "no NAMING-GATE summary line (rc=%d)" % rc)
    line = re.search(r"^NAMING \S+ \S*probe\.py:\d+ %s\b.*$" % re.escape(PLANTED), out, re.M)
    print("planted: %s | %s" % (line.group(0) if line else "NO GRADE LINE", summ.group(0)))
    need(line is not None, "the gate printed no NAMING line for the planted PATTERN name %r" % PLANTED)
    need(int(summ.group(2)) >= 1, "the gate summary reads 0 graded")
    rc, out = _gate_on(CONTROL_FIXTURE)
    need(re.search(r"^NAMING \S+ \S*zz-r21-control/main.tf:\d+ zz-probe-scheduler-role-typed\b", out, re.M),
         "control: the hand-typed literal is no longer graded")
    return "PASS-R21-PATTERN"


def arm_scope():
    rc, out = run([sys.executable, "lib/tests/test_opal_naming_scope.py"], timeout=900)
    last = (out.strip().splitlines() or [""])[-1]
    print("scope: rc=%d %s" % (rc, last))
    need(last.startswith("SCOPE-TEST ok=True"), "the scope test does not read ok=True: %s" % last)
    return "PASS-R21-SCOPE"


def arm_unit():
    rc, out = run([sys.executable, "-m", "pytest", "lib/tests/test_opal_lgctfm.py", "-q", "-p", "no:cacheprovider"], timeout=900)
    last = (out.strip().splitlines() or [""])[-1]
    print("unit: rc=%d %s" % (rc, re.sub(r"\x1b\[[0-9;]*m", "", last)))
    need(rc == 0 and " passed" in last and "failed" not in last and "error" not in last,
         "the engine's test file does not pass whole")
    return "PASS-R21-UNIT"


ARMS = {"failclosed": arm_failclosed, "pattern": arm_pattern, "scope": arm_scope, "unit": arm_unit}


def main():
    arm = sys.argv[1] if len(sys.argv) > 1 else ""
    if arm not in ARMS:
        print("usage: check_en_r21.py {%s}" % ",".join(sorted(ARMS)))
        return 2
    try:
        verdict = ARMS[arm]()
    except Fail as exc:
        print("FAIL-R21-%s: %s" % (arm.upper(), exc))
        return 1
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
