"""GS-e-2 AC1 (FWD-7, CTO ruling R3): the live read, run BY the site-Z lane on site Z's own tree. A control check: it
passes wherever round 1's tools have arrived and no seat-home copy of a NFRA_GATSCP order exists.

Arm 1: this box's tree has round 1's scoped tree check (`check --staged --act` prints ACT SCOPE).
Arm 2: this box's tree has box-sync's read-only grade (`box-sync.sh grade HEAD HEAD~1` prints a grade line).
Arm 3: no file under org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ names NFRA_GATSCP (the order was run from the
  mission tree with no seat-home copy or pointer).
The box name is printed (AGENTBUS_DEVICE), so the record says which tree was read.
"""
import os
import sys

from r2_common import ACT_ROW, ROOT, finish, git_bash, run, tail

box = os.environ.get("AGENTBUS_DEVICE", "UNKNOWN")
rc1, out1 = run([sys.executable, ".tools/missions-tree-index.py", "check", "--staged", "--act", ACT_ROW], None)
rc2, out2 = run([git_bash(), ".tools/box-sync.sh", "grade", "HEAD", "HEAD~1"], None, timeout=110)
seat_home = os.path.join(ROOT, "org", "tier2_senior", "0.7.0_AE_CloudOps", "task_orders")
copies = sorted(f for f in (os.listdir(seat_home) if os.path.isdir(seat_home) else []) if "NFRA_GATSCP" in f)
arms = [
    ("scoped-tree-check-present", rc1 in (0, 1) and "ACT SCOPE:" in out1, "box=%s rc=%s :: %s" % (box, rc1, tail(out1, 2))),
    ("box-sync-grade-present", rc2 in (0, 1) and "box-sync: grade" in out2, "rc=%s :: %s" % (rc2, tail(out2, 2))),
    ("no-seat-home-copy", not copies, "copies=%s" % copies),
]
sys.exit(finish("GS-E2-SITEZ", arms))
