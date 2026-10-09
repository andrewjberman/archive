"""GS-t-1 AC2: the row gate (the corpus pass's real caller) lands a commit beside another project's NEW failure.

Plant: a NEW schema failure in the bystander's channel document (private index only).
Arm 1 (bystander): STAGED = a different project's channel document -> rc 0, a STANDING <bystander> line.
Arm 2 (own, the difference control): STAGED = the planted document -> rc 1.
"""
import shutil
import sys

from r1_common import ACT_DOC, BYSTANDER, BYSTANDER_DOC, ROOT, finish, plant_channel_failure, run, standing, tail, temp_index

d, env = temp_index()
try:
    plant_channel_failure(env)
    env["ROOT"] = ROOT
    env.pop("SURPRISE_ROW_OVERRIDE", None)
    gate = ".tools/surprise-row-gate.py"
    e1 = dict(env, STAGED=ACT_DOC)
    rc1, out1 = run([sys.executable, gate], e1)
    e2 = dict(env, STAGED=BYSTANDER_DOC)
    rc2, out2 = run([sys.executable, gate], e2)
    arms = [
        ("bystander-lands", rc1 == 0 and standing(out1), "rc=%s standing_%s=%s :: %s" % (rc1, BYSTANDER, standing(out1), tail(out1))),
        ("own-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2))),
    ]
    sys.exit(finish("GS-T1-ROWGATE", arms))
finally:
    shutil.rmtree(d, ignore_errors=True)
