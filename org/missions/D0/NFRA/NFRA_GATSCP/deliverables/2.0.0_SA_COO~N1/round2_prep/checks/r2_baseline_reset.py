"""GS-e-4 AC1 (FWD-2): deliberately resetting the known-errors list stays a refusal, even in a commit that stages
nothing but the baseline file.

Plant (private index only): the corpus baseline loses its first tuple.
Arm 1 (the reset act): the row gate with STAGED = the baseline file -> rc 1.
Arm 2 (the difference control): the row gate with STAGED = another project's untouched channel document -> rc 0, and
  the failure the dropped tuple uncovers prints STANDING with its own project (it is not this act's defect).
"""
import json
import re
import shutil
import sys

from r2_common import ACT_DOC, BASELINE, ROOT, finish, index_text, plant, run, standing, tail, temp_index

d, env = temp_index()
try:
    data = json.loads(index_text(BASELINE))
    dropped = data["tuples"][0]
    data["tuples"] = data["tuples"][1:]
    plant(env, BASELINE, json.dumps(data, indent=2) + "\n")
    m = re.match(r"org/(?:surprise_channel/([^/]+)/|missions/[^/]+/[^/]+/([^/]+)/)", dropped[0])
    owner = (m.group(1) or m.group(2)) if m else "?"
    env["ROOT"] = ROOT
    env.pop("SURPRISE_ROW_OVERRIDE", None)
    gate = [sys.executable, ".tools/surprise-row-gate.py"]
    rc1, out1 = run(gate, dict(env, STAGED=BASELINE))
    rc2, out2 = run(gate, dict(env, STAGED=ACT_DOC))
    arms = [
        ("reset-refused", rc1 == 1, "rc=%s :: %s" % (rc1, tail(out1, 4))),
        ("bystander-standing", rc2 == 0 and standing(out2, owner),
         "rc=%s standing_%s=%s :: %s" % (rc2, owner, standing(out2, owner), tail(out2, 3))),
    ]
    sys.exit(finish("GS-E4-RESET", arms))
finally:
    shutil.rmtree(d, ignore_errors=True)
