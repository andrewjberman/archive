"""GS-t-3 AC1: a box-sync merge is graded by the tree check on the MERGED bytes, scoped to what the merge changes.

Commits are built with plumbing only (a private index, commit-tree); no ref moves and no working tree changes.
  B0 = HEAD + the bystander's row drift (a standing defect already on the box)
  X  = B0 + a new file in this project's tree     Y = B0 + another new file in this project's tree
  X1 = HEAD + the same drift + a new file          Y1 = HEAD + the same drift + another new file
Arm 1 (bystander): box-sync.sh grade X Y -> rc 0 and a STANDING <bystander> line (the drift sits in the merge
  base, so it is outside the merge's graded path set).
Arm 2 (own, the difference control): box-sync.sh grade X1 Y1 -> rc 1 (both sides changed the bystander's row, so
  the row is inside the graded path set, box-sync's existing definition at grade_merge).
`grade` is read-only: it lands nothing and moves no ref.
"""
import shutil
import sys

from r1_common import BYSTANDER, finish, git, git_bash, plant, plant_row_drift, run, standing, tail, temp_index

PROBE = "org/missions/D0/NFRA/NFRA_GATSCP/deliverables/2.0.0_SA_COO~N1/round1_prep/probe_%s.md"


def commit(parent, env, msg):
    tree = git(["write-tree"], env=env).stdout.strip()
    return git(["commit-tree", tree, "-p", parent, "-m", msg]).stdout.strip()


dirs = []


def build(parent, drift, probe):
    """A commit on `parent`, optionally carrying the bystander's drift, optionally adding one probe file."""
    d, env = temp_index()
    dirs.append(d)
    git(["read-tree", parent], env=env)
    if drift:
        plant_row_drift(env)
    if probe:
        plant(env, PROBE % probe, "probe %s\n" % probe)
    return commit(parent, env, "probe %s" % (probe or "B0: bystander drift"))


try:
    head = git(["rev-parse", "HEAD"]).stdout.strip()
    b0 = build(head, True, None)
    x = build(b0, False, "x")
    y = build(b0, False, "y")
    x1 = build(head, True, "x1")
    y1 = build(head, True, "y1")
    if not all([b0, x, y, x1, y1]):
        raise SystemExit("ERROR: could not build probe commits")
    bs = [git_bash(), ".tools/box-sync.sh", "grade"]
    rc1, out1 = run(bs + [x, y], None)
    rc2, out2 = run(bs + [x1, y1], None)
    arms = [
        ("bystander-lands", rc1 == 0 and standing(out1), "rc=%s standing_%s=%s :: %s" % (rc1, BYSTANDER, standing(out1), tail(out1))),
        ("own-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2))),
    ]
    sys.exit(finish("GS-T3-BOXSYNC", arms))
finally:
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
