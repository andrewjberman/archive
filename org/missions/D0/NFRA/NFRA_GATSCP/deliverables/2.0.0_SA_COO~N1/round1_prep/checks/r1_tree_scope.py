"""GS-t-2 AC1: the tree check reads the STAGED bytes and refuses only a violation in a project the act touches.

Plant: the bystander's tree row changes dep_stage in the private index only (its generated index is not
regenerated, so the staged estate carries an INDEX drift for the bystander). The working tree is untouched.
Arm 1 (bystander): check --staged --act <this project's row> -> rc 0, a STANDING <bystander> line.
Arm 2 (own, the difference control): check --staged --act <the bystander's row> -> rc 1.
"""
import shutil
import sys

from r1_common import ACT_ROW, BYSTANDER, BYSTANDER_ROW, finish, plant_row_drift, run, standing, tail, temp_index

d, env = temp_index()
try:
    plant_row_drift(env)
    tool = ".tools/missions-tree-index.py"
    rc1, out1 = run([sys.executable, tool, "check", "--staged", "--act", ACT_ROW], env)
    rc2, out2 = run([sys.executable, tool, "check", "--staged", "--act", BYSTANDER_ROW], env)
    arms = [
        ("bystander-lands", rc1 == 0 and standing(out1), "rc=%s standing_%s=%s :: %s" % (rc1, BYSTANDER, standing(out1), tail(out1))),
        ("own-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2))),
    ]
    sys.exit(finish("GS-T2-SCOPE", arms))
finally:
    shutil.rmtree(d, ignore_errors=True)
