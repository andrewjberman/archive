"""GS-e-6 AC2 (FWD-6): the tree hook's close gate reads only staged bytes (structural; the hook is exercised by the
issuer's real ROUND_CLOSE commit of round 2).

Arm 1: close_gate() calls round-close-check.py with --staged.
Arm 2: close_gate() has no working-tree fallback for dep_stage (no read of "$ROOT/$p").
"""
import os
import re
import sys

from r2_common import ROOT, finish

with open(os.path.join(ROOT, ".tools", "git-hooks", "missions-tree-check.sh"), encoding="utf-8") as fh:
    src = fh.read()
m = re.search(r"(?ms)^close_gate\(\)\s*\{(.*?)^\}", src)
body = m.group(1) if m else ""
staged = bool(re.search(r"round-close-check\.py[^\n]*--staged", body))
fallback = '"$ROOT/$p"' in body
arms = [
    ("close-gate-passes-staged", bool(m) and staged, "function_found=%s staged=%s" % (bool(m), staged)),
    ("no-worktree-fallback", bool(m) and not fallback, "worktree_fallback_present=%s" % fallback),
]
sys.exit(finish("GS-E6-HOOK", arms))
