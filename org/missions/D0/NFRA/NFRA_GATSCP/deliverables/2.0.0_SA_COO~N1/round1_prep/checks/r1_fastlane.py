"""GS-t-3 AC2: safe-merge.sh's fast lane (a drain that lands by commit-tree, so no commit hook fires) runs the same
scoped tree check box-sync runs, and the script's own self-test stays green.

Arm 1: the body of _sm_fast_lane() invokes missions-tree-index.py with --staged and --act (structural; the fast
  lane cannot be driven without landing a merge, and its seam is exercised by the issuer's one real run at close).
Arm 2: bash .tools/safe-merge.sh --self-test exits 0.
"""
import os
import re
import sys

from r1_common import ROOT, finish, git_bash, run, tail

with open(os.path.join(ROOT, ".tools", "safe-merge.sh"), encoding="utf-8") as fh:
    src = fh.read()
m = re.search(r"(?ms)^_sm_fast_lane\s*\(\)\s*\{(.*?)^\}", src)
body = m.group(1) if m else ""
wired = bool(body) and "missions-tree-index.py" in body and "--staged" in body and "--act" in body
rc, out = run([git_bash(), ".tools/safe-merge.sh", "--self-test"], None)
arms = [
    ("fast-lane-runs-scoped-tree-check", wired, "function_found=%s wired=%s" % (bool(m), wired)),
    ("self-test-green", rc == 0, "rc=%s :: %s" % (rc, tail(out, 3))),
]
sys.exit(finish("GS-T3-FASTLANE", arms))
