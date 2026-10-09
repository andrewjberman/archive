"""GS-e-1 AC1 (FWD-5, CTO ruling R1): a box sync SHOWS the standing defects it carries, as information, and says
"N standing" -- "0 standing" included -- never nothing.

Commits (plumbing only, unreferenced):
  B0 = HEAD + the bystander's row drift + a NEW schema failure in the bystander's channel (two standing defects)
  X, Y   = B0 + two DIFFERENT probe files       -> the graded path set is EMPTY (the round-1 SKIP case, row D1-S3)
  X0, Y0 = HEAD + two different probe files     -> empty graded set, no placed defect (the box's organic count n0)
  X1, Y1 = HEAD + the same drift + two probes   -> both sides changed the bystander's row: in the graded set
Arm 1: grade X0 Y0 -> rc 0 and one line `box-sync: <n0> standing`.
Arm 2: grade X Y   -> rc 0, `box-sync: <n0+2> standing`, and STANDING lines naming the bystander.
Arm 3 (the negative arm, P1): grade X1 Y1 -> rc 1 (a defect the sync itself introduces still refuses).
"""
import re
import sys

from r2_common import BYSTANDER, build, cleanup, finish, git, git_bash, run, standing, tail

LINE = re.compile(r"(?m)^box-sync: (\d+) standing\b")


def count(out):
    m = LINE.findall(out)
    return int(m[-1]) if m else None


try:
    head = git(["rev-parse", "HEAD"]).stdout.strip()
    b0 = build(head, drift=True, channel=True, tag="B0")
    x = build(b0, probe="sx", tag="X")
    y = build(b0, probe="sy", tag="Y")
    x0 = build(head, probe="s0x", tag="X0")
    y0 = build(head, probe="s0y", tag="Y0")
    x1 = build(head, drift=True, probe="s1x", tag="X1")
    y1 = build(head, drift=True, probe="s1y", tag="Y1")
    bs = [git_bash(), ".tools/box-sync.sh", "grade"]
    rc0, out0 = run(bs + [x0, y0], None, timeout=110)
    rc1, out1 = run(bs + [x, y], None, timeout=110)
    rc2, out2 = run(bs + [x1, y1], None, timeout=110)
    n0, n1 = count(out0), count(out1)
    arms = [
        ("clean-sync-says-count", rc0 == 0 and n0 is not None, "rc=%s count=%s :: %s" % (rc0, n0, tail(out0, 3))),
        ("sync-shows-standing", rc1 == 0 and n0 is not None and n1 == n0 + 2 and standing(out1),
         "rc=%s count=%s expected=%s standing_%s=%s :: %s" % (rc1, n1, None if n0 is None else n0 + 2, BYSTANDER,
                                                             standing(out1), tail(out1, 4))),
        ("own-defect-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2, 3))),
    ]
    sys.exit(finish("GS-E1-SYNC", arms))
finally:
    cleanup()
