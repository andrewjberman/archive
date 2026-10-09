"""GS-t-1 AC1: the corpus pass refuses a NEW failure only inside the act's documents.

Plant: a NEW schema failure in the bystander's channel document (private index only).
Arm 1 (bystander): --act <a different project's document>  -> rc 0, a STANDING <bystander> line.
Arm 2 (own, the difference control): --act <the planted document> -> rc 1, exactly as today.
"""
import shutil
import sys

from r1_common import ACT_DOC, BYSTANDER, BYSTANDER_DOC, finish, plant_channel_failure, run, standing, tail, temp_index

d, env = temp_index()
try:
    plant_channel_failure(env)
    tool = ".tools/surprise-corpus-validate.py"
    rc1, out1 = run([sys.executable, tool, "--act", ACT_DOC], env)
    rc2, out2 = run([sys.executable, tool, "--act", BYSTANDER_DOC], env)
    arms = [
        ("bystander-lands", rc1 == 0 and standing(out1), "rc=%s standing_%s=%s :: %s" % (rc1, BYSTANDER, standing(out1), tail(out1))),
        ("own-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2))),
    ]
    sys.exit(finish("GS-T1-SCOPE", arms))
finally:
    shutil.rmtree(d, ignore_errors=True)
