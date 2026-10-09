"""GS-t-2 AC3: missions-tree-index.py --self-test stays green, every arm passing, and it carries arms for the new
--staged/--act behaviour (at least one arm line naming --staged and one naming --act or STANDING).

A control check at the base for the green half (38/38 PASS, rc 0); the arm half is the build.
"""
import re
import sys

from r1_common import finish, run, tail

rc, out = run([sys.executable, ".tools/missions-tree-index.py", "--self-test"], None)
m = re.search(r"--self-test:\s*(\d+)/(\d+)\s+PASS", out)
green = rc == 0 and bool(m) and m.group(1) == m.group(2)
arm_lines = [ln for ln in out.splitlines() if ln.strip().startswith("PASS")]
staged_arm = any("--staged" in ln for ln in arm_lines)
act_arm = any(("--act" in ln) or ("STANDING" in ln) for ln in arm_lines)
arms = [
    ("self-test-green", green, "rc=%s summary=%s :: %s" % (rc, m.group(0) if m else None, tail(out, 2))),
    ("has-staged-and-act-arms", staged_arm and act_arm, "staged_arm=%s act_arm=%s" % (staged_arm, act_arm)),
]
sys.exit(finish("GS-T2-SELFTEST", arms))
