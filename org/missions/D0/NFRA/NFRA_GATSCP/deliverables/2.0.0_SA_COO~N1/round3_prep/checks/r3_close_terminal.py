"""GS-f-3 AC1 (row D1-S9; ruling R3): round-close-check reads an order's terminal state and its judgment flag as the order
declares them, on real rounds (no plant).

Arm 1 (the build): LGIC_BLANKFIX round 12 -- its one order TO-BF-aa-1 reads `<status>complete -- landed by ...</status>`
  and carries a `judgment="true"` criterion -> PROOFS complete=1 and ROUND-CLOSE judgment=1 (the base reads complete=0,
  judgment=0).
Arm 2 (the control, R3's proof): LGIC_BLANKFIX round 13 -> orders=3 judgment=1, unchanged.
Arm 3 (the control, R3's proof): DSGN_AMGTV1 round 65 -> orders=1 judgment=1.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import finish, run, tail  # noqa: E402


def read(project, rnd):
    rc, out = run([sys.executable, ".tools/round-close-check.py", "--project", project, "--round", str(rnd)], None, timeout=110)
    comp = re.findall(r"PROOFS mode=\S+ complete=(\d+)", out)
    orders = re.findall(r"ROUND-CLOSE .*? orders=(\d+) judgment=(\d+)", out)
    return rc, (int(comp[-1]) if comp else None), (tuple(int(x) for x in orders[-1]) if orders else None), out


rc1, c1, o1, out1 = read("LGIC_BLANKFIX", 12)
rc2, c2, o2, out2 = read("LGIC_BLANKFIX", 13)
rc3, c3, o3, out3 = read("DSGN_AMGTV1", 65)
arms = [
    ("aa-1-read-terminal-with-judgment", c1 == 1 and o1 is not None and o1[1] == 1,
     "complete=%s orders,judgment=%s :: %s" % (c1, o1, tail(out1, 1))),
    ("lgic-r13-unchanged", o2 == (3, 1), "orders,judgment=%s" % (o2,)),
    ("dsgn-r65-judgment-read", o3 is not None and o3[1] >= 1, "orders,judgment=%s" % (o3,)),
]
sys.exit(finish("GS-F3-CLOSE", arms))
