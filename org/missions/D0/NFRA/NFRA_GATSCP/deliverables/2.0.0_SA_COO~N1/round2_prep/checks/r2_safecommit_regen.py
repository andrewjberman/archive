"""GS-e-5 AC2 (FWD-4): safe-commit regenerates the generated index entry inside the commit act (structural; the seam is
exercised by the issuer's real ROUND_CLOSE commit of round 2, made with no manual derive).

Arm 1: safe-commit.sh calls `missions-tree-index.py derive --staged --only` BEFORE the line that sets IN_SCOPE from
  `git diff --cached --name-only`, so the regenerated entry is inside every later gate's act.
Arm 2: within 40 lines after that call, the regenerated org/projects path is appended to PATHSPEC (the land step
  carries only PATHSPEC) and a REFUSED message names a regeneration failure.
"""
import os
import re
import sys

from r2_common import ROOT, finish

with open(os.path.join(ROOT, ".tools", "safe-commit.sh"), encoding="utf-8") as fh:
    lines = fh.read().splitlines()
call = next((i for i, ln in enumerate(lines) if "missions-tree-index.py" in ln and "--staged" in ln and "--only" in ln
             and "derive" in ln and not ln.lstrip().startswith("#")), None)
scope = next((i for i, ln in enumerate(lines) if re.match(r'\s*IN_SCOPE="\$\(git diff --cached --name-only', ln)), None)
window = lines[call:call + 40] if call is not None else []
appended = any("PATHSPEC+=(" in ln for ln in window)
refused = any("REFUSED" in ln and "regenerat" in ln.lower() for ln in window)
arms = [
    ("regen-before-in-scope", call is not None and scope is not None and call < scope,
     "call_line=%s in_scope_line=%s" % (None if call is None else call + 1, None if scope is None else scope + 1)),
    ("pathspec-and-refusal", appended and refused, "pathspec_append=%s refusal_message=%s" % (appended, refused)),
]
sys.exit(finish("GS-E5-SAFECOMMIT", arms))
