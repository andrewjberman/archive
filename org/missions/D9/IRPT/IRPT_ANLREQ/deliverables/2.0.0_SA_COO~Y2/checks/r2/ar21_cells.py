"""IRPT_ANLREQ round 2 (workstream ~Y, issuer 2.0.0_SA_COO~Y2) -- checks of cell AR-y-21 (the release packet of AR-y-11: staged rows re-pinned
so the served functions carry the ticket binding and the contract that admits it; rows IRPT_ANLREQ-D2-W1-S2, CTO round-1 analysis release 1).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Read-only: source map, git blobs, and a BUILD_ONLY of each function (no upload).

  AR21-y-AC1  every staged row named below carries a pin whose blob equals HEAD's blob of the same repo_path, and its sha256 equals that
              blob's sha256: irpt-status submission.py + acceptance.py (+ ops/entry.py + ops/owned_report.py, AMENDMENT 3); irpt-ycharts-generate
              contracts/AnalysisSubmissionRequest.schema.json. Base at AMENDMENT 3: FAIL (2 of 5 lag).
  AR21-y-AC2  no staged commit ships split, for BOTH functions (checks/r73/cochange_closure.py irpt-status and irpt-ycharts-generate).
  AR21-y-AC3  every imported name resolves in BOTH built zips (BUILD_ONLY, then checks/r71/symbol_closure.py on each).
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROWS = [
    ("irpt-status", "infra/aws/lambda/investor-reporting/ycharts/generate/submission.py"),
    ("irpt-status", "infra/aws/lambda/investor-reporting/ycharts/generate/acceptance.py"),
    ("irpt-ycharts-generate", "docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json"),
    # AMENDMENT 3 (issuer 2026-10-09 ~08:3xZ): AR-y-22's reader ships only if irpt-status stages these at its drain (@75650bef27).
    ("irpt-status", "infra/aws/lambda/investor-reporting/ops/entry.py"),
    ("irpt-status", "infra/aws/lambda/investor-reporting/ops/owned_report.py"),
]
FUNCTIONS = ("irpt-status", "irpt-ycharts-generate")
Y2 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks"


def git(root, *args):
    return subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, check=True).stdout


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "AR21"))
        sys.exit(1)

    if cid not in ("AR21-y-AC1", "AR21-y-AC2", "AR21-y-AC3"):
        fail("unknown criterion %r" % cid)
    if cid == "AR21-y-AC1":
        fns = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))["functions"]
        bad = 0
        for fn, path in ROWS:
            rows = [r for r in (fns[fn].get("staged_from") or []) if r.get("repo_path") == path]
            if len(rows) != 1:
                fail("%s: %d staged row(s) for %s" % (fn, len(rows), path))
            r = rows[0]
            head = git(root, "show", "HEAD:" + path)
            at_pin = git(root, "show", "%s:%s" % (r["pin"], path))
            sha = hashlib.sha256(at_pin).hexdigest()
            ok = at_pin == head and r.get("sha256") == sha
            print("%s %s %s pin=%s sha_ok=%s" % ("OK" if ok else "LAG", fn, path, r["pin"][:10], r.get("sha256") == sha))
            bad += not ok
        print("denominator: %d row(s), %d lagging" % (len(ROWS), bad))
        if bad:
            fail("%d staged row(s) lag HEAD" % bad)
    elif cid == "AR21-y-AC2":
        for fn in FUNCTIONS:
            out = subprocess.run([sys.executable, str(root / Y2 / "r73/cochange_closure.py"), fn], cwd=str(root),
                                 capture_output=True, text=True)
            last = [ln for ln in out.stdout.splitlines() if ln.startswith("cochange_closure")]
            print(fn, " | ".join(last))
            if out.returncode != 0 or not last or not last[-1].endswith("PASS"):
                fail("%s co-change closure did not PASS" % fn)
    else:
        for fn in FUNCTIONS:
            b = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", fn], cwd=str(root),
                               capture_output=True, text=True, env=dict(os.environ, BUILD_ONLY="1"))
            line = [ln for ln in (b.stdout + b.stderr).splitlines() if ln.startswith("BUILD_ONLY:")]
            if not line:
                fail("%s: no BUILD_ONLY line (rc %d)" % (fn, b.returncode))
            zip_path = line[-1].split()[1]
            if os.name == "nt" and zip_path.startswith("/tmp/"):
                zip_path = subprocess.run(["cygpath", "-w", zip_path], capture_output=True, text=True).stdout.strip()
            s = subprocess.run([sys.executable, str(root / Y2 / "r71/symbol_closure.py"), zip_path], capture_output=True, text=True)
            tail = [ln for ln in s.stdout.splitlines() if ln.startswith("symbol_closure")]
            print(fn, " | ".join(tail))
            if s.returncode != 0:
                fail("%s symbol closure FAIL" % fn)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
