"""IRPT_BCKEND round 74 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- check of cell IB-pr-360 (row S381: the export build's
ADHC_DRIFTD.002 parity limb flags backfill_covered_account_ids.py, an operator tool in the export source dir that no member imports).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB74-1-AC1  the ADHC_DRIFTD.002 rule, applied exactly as infra/aws/lambda/ci/build-and-upload.sh applies it (top-level *.py in the
              source dir; skip __pycache__, *.pyc, test_*.py, *_test.py; every remaining base name must be in the UNION of files[]
              across every function whose source_dir is this one), finds 0 extras for infra/aws/lambda/investor-reporting/export;
              AND export/tests/test_backfill_covered_account_ids.py passes; AND the tool still runs its --help from its new home.
              Base: FAIL (1 extra: backfill_covered_account_ids.py).
  IB74-G-168  A GUARD: worker ~168's commits touch only its grant. Base: PASS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "8be1d0b344"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
SRC = "infra/aws/lambda/investor-reporting/export"
GRANT = (SRC + "/backfill_covered_account_ids.py", SRC + "/tools/", SRC + "/tests/test_backfill_covered_account_ids.py",
         P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-360.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~168/")


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB74"))
        sys.exit(1)

    if cid == "IB74-1-AC1":
        m = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))
        fs = m.get("functions", m)
        union = set()
        for v in fs.values():
            if isinstance(v, dict) and v.get("source_dir", "").rstrip("/") == SRC:
                union.update(v.get("files", []))
        extras = []
        for f in sorted((root / SRC).glob("*.py")):
            b = f.name
            if b.startswith("test_") or b.endswith("_test.py"):
                continue
            if b not in union:
                extras.append(b)
        if extras:
            fail("ADHC_DRIFTD.002 rule finds %d extra(s) in %s: %s" % (len(extras), SRC, extras))
        tools = sorted((root / SRC / "tools").glob("backfill_covered_account_ids.py")) if (root / SRC / "tools").is_dir() else []
        if not tools:
            fail("the back-fill tool is not at %s/tools/backfill_covered_account_ids.py" % SRC)
        rc, out = _run([sys.executable, str(tools[0]), "--help"], root / SRC)
        if rc or "--dry-run" not in out:
            fail("the tool's --help from its new home: rc %d %s" % (rc, _last(out)))
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_backfill_covered_account_ids.py"],
                       root / SRC)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("back-fill tests: %s" % last)
        print("OK: 0 parity extras over %d union members; tool --help rc 0; tests %s" % (len(union), last))
    elif cid == "IB74-G-168":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~168", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~168's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
