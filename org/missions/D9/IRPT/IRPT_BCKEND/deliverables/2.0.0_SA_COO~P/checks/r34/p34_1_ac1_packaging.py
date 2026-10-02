"""IB34-1-AC1 -- G1 + G2 (CTO batch 175): the export function packages the Analysis contract, and every function that stages the
render grant module also stages the owner reader and the repository it imports.

Reads infra/aws/lambda/ci/lambda-source-map.json at the worktree. Grades:
  1. irpt-export-render stages docs/contracts/investor-reporting/v1/AnalysisReport.schema.json and ExportBundle.schema.json, each
     packaged as irpt_contracts/<name>, and the pinned blob of each equals HEAD's blob of that path.
  2. EVERY function whose staged_from or files names _render_identity/grant.py also stages _render_identity/report_owner.py
     (packaged beside grant.py: same directory as grant.py's packaged_as) and reports/repository.py; every one of those three
     pinned blobs equals HEAD's.
  3. infra/aws/lambda/ci/test_render_ports_packaging.py exists and `python -m pytest -q` on it passes at least 2 tests, 0 failed.
Usage: python <this file> <repo_root>
"""
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
B = "infra/aws/lambda/investor-reporting/"
DOCS = "docs/contracts/investor-reporting/v1/"
GRANT, OWNER, REPO = B + "_render_identity/grant.py", B + "_render_identity/report_owner.py", B + "reports/repository.py"
TEST = "infra/aws/lambda/ci/test_render_ports_packaging.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB34-1-AC1 FAIL")
    sys.exit(1)


def blob(root, ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=str(root), capture_output=True)
    if r.returncode != 0:
        fail("git show %s:%s failed" % (ref, path))
    return hashlib.sha256(r.stdout).hexdigest()


def staged(entry):
    return {s["repo_path"]: s for s in entry.get("staged_from", [])}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    fns = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"]
    exp = staged(fns.get("irpt-export-render") or fail("no irpt-export-render entry"))
    for name in ("AnalysisReport.schema.json", "ExportBundle.schema.json"):
        s = exp.get(DOCS + name)
        if s is None:
            fail("irpt-export-render does not stage %s" % (DOCS + name))
        if s.get("packaged_as") != "irpt_contracts/" + name:
            fail("%s packaged_as %r, want irpt_contracts/%s" % (name, s.get("packaged_as"), name))
        if blob(root, s["pin"], s["repo_path"]) != blob(root, "HEAD", s["repo_path"]):
            fail("irpt-export-render's %s pin %s is not HEAD's blob" % (name, s["pin"][:10]))
    n = 0
    for fn, entry in fns.items():
        st = staged(entry)
        names = set(st) | set(entry.get("files", []))
        if GRANT not in names:
            continue
        n += 1
        for need in (GRANT, OWNER, REPO):
            s = st.get(need)
            if s is None:
                fail("%s stages grant.py but not %s" % (fn, need))
            if blob(root, s["pin"], need) != blob(root, "HEAD", need):
                fail("%s pins %s at %s, not HEAD's blob" % (fn, need, s["pin"][:10]))
        if posixpath.dirname(st[OWNER].get("packaged_as", "")) != posixpath.dirname(st[GRANT].get("packaged_as", "")):
            fail("%s packages report_owner.py apart from grant.py" % fn)
    if n == 0:
        fail("no function stages grant.py (the census is empty)")
    t = root / TEST
    if not t.is_file():
        fail("no %s" % TEST)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST],
                       cwd=str(root), capture_output=True, text=True, timeout=110)
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad or not passed or int(passed.group(1)) < 2:
        fail("packaging test: %s" % (bad.group(0) if bad else out.strip()[-200:]))
    print("OK: export stages both contracts at HEAD; %d grant-staging function(s) stage report_owner + repository at HEAD; "
          "packaging test %s" % (n, passed.group(0)))
    print("IB34-1-AC1 PASS")


if __name__ == "__main__":
    main()
