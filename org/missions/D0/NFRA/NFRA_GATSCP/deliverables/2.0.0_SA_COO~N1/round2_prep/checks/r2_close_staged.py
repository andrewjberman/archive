"""GS-e-6 AC1 (FWD-6): round-close-check grades what the commit carries (--staged), not the working tree.

Plant (private index only): round 1's GS-t-1 proof instance is removed from the index; the working-tree file stays.
Arm 1 (no plant, --staged): PROOFS proof_ok=3 proof_bad=0.
Arm 2 (plant, --staged): fewer than 3 proofs read ok (the instance the index lacks is not graded as present).
Arm 3 (plant, no --staged, the difference control): proof_ok=3 -- the working tree still has it, which is the read
  FWD-6 retires from the commit path.
"""
import re
import shutil
import sys

from r2_common import finish, git, run, tail, temp_index

INST = ("org/missions/D0/NFRA/NFRA_GATSCP/deliverables/0.9.0_WK_NFRA_GATSCP~1/"
        "NFRA_GATSCP.TO-GS-t-1.corpus-pass-scoped-to-the-act.proof_of_spec.json")


def ok_count(out):
    m = re.findall(r"proof_ok=(\d+)", out)
    return int(m[-1]) if m else None


tool = [sys.executable, ".tools/round-close-check.py", "--project", "NFRA_GATSCP", "--round", "1"]
dirs = []
try:
    d0, e0 = temp_index()
    dirs.append(d0)
    rc0, out0 = run(tool + ["--staged"], e0)
    d1, e1 = temp_index()
    dirs.append(d1)
    r = git(["rm", "--cached", "-q", "--", INST], env=e1)
    rc1, out1 = run(tool + ["--staged"], e1)
    rc2, out2 = run(tool, e1)
    k0, k1, k2 = ok_count(out0), ok_count(out1), ok_count(out2)
    arms = [
        ("staged-clean-3-ok", k0 == 3, "rc=%s proof_ok=%s :: %s" % (rc0, k0, tail(out0, 2))),
        ("staged-plant-graded", r.returncode == 0 and k1 is not None and k1 < 3,
         "rm_rc=%s rc=%s proof_ok=%s :: %s" % (r.returncode, rc1, k1, tail(out1, 2))),
        ("worktree-read-differs", k2 == 3, "rc=%s proof_ok=%s (worktree read, the control)" % (rc2, k2)),
    ]
    sys.exit(finish("GS-E6-CLOSE", arms))
finally:
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
