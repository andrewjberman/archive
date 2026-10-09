"""GS-t-2 AC2: the commit hook (missions-tree-check.sh, the tree check's real caller) grades the staged bytes,
scoped to the act.

Plant: the bystander's tree row drifts in the private index only.
Arm 1 (bystander): staged list = this project's row -> exit 0, a STANDING <bystander> line.
Arm 2 (own, the difference control): staged list = the bystander's row -> exit 1. A hook that reads the
working tree sees no drift and exits 0 here.
"""
import shutil
import sys

from r1_common import (ACT_ROW, BYSTANDER, BYSTANDER_ROW, ROOT, finish, git_bash, plant_row_drift, run, standing, tail,
                       temp_index)

d, env = temp_index()
try:
    plant_row_drift(env)
    env["PRECOMP_REPO_ROOT"] = ROOT
    hook = [git_bash(), ".tools/git-hooks/missions-tree-check.sh"]
    rc1, out1 = run(hook, dict(env, OWNED_PATHS_STAGED_FILES=ACT_ROW))
    rc2, out2 = run(hook, dict(env, OWNED_PATHS_STAGED_FILES=BYSTANDER_ROW))
    arms = [
        ("bystander-lands", rc1 == 0 and standing(out1), "rc=%s standing_%s=%s :: %s" % (rc1, BYSTANDER, standing(out1), tail(out1))),
        ("own-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2))),
    ]
    sys.exit(finish("GS-T2-HOOK", arms))
finally:
    shutil.rmtree(d, ignore_errors=True)
