"""GS-e-5 AC1 (FWD-4): one project's generated index entry is composed from its STAGED tree row, alone.

`python .tools/missions-tree-index.py derive --staged --only <CODE> --stdout` prints the JSON the generated
org/projects/<CODE>.json must hold, composed from the index's copy of that project's project.json; it writes no file.
Arm 1 (unchanged): equals the committed org/projects/NFRA_GATSCP.json (parsed).
Arm 2 (the difference): with the row's dep_stage changed in the private index, the printed entry carries the new value.
Arm 3 (refusal): with dep_stage off its enum, rc 1 (the entry cannot be made, so the commit is refused with a reason).
The working-tree copy of org/projects/NFRA_GATSCP.json is byte-identical before and after.
"""
import hashlib
import json
import os
import re
import shutil
import sys

from r2_common import ACT_ROW, ROOT, finish, index_text, plant, run, tail, temp_index

CODE = "NFRA_GATSCP"
FLAT = "org/projects/%s.json" % CODE


def digest():
    with open(os.path.join(ROOT, FLAT), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def parsed(out):
    s, e = out.find("{"), out.rfind("}")
    try:
        return json.loads(out[s:e + 1]) if s >= 0 and e > s else None
    except ValueError:
        return None


before = digest()
tool = [sys.executable, ".tools/missions-tree-index.py", "derive", "--staged", "--only", CODE, "--stdout"]
dirs = []
try:
    d0, e0 = temp_index()
    dirs.append(d0)
    rc0, out0 = run(tool, e0)
    committed = json.loads(index_text(FLAT))
    row = index_text(ACT_ROW)
    cur = re.search(r'"dep_stage"\s*:\s*"([^"]*)"', row).group(1)
    new = "DECOMP" if cur != "DECOMP" else "EXECUTING"
    d1, e1 = temp_index()
    dirs.append(d1)
    plant(e1, ACT_ROW, re.sub(r'("dep_stage"\s*:\s*")[^"]*(")', r"\g<1>%s\g<2>" % new, row, count=1))
    rc1, out1 = run(tool, e1)
    d2, e2 = temp_index()
    dirs.append(d2)
    plant(e2, ACT_ROW, re.sub(r'("dep_stage"\s*:\s*")[^"]*(")', r"\g<1>NOT_A_STAGE\g<2>", row, count=1))
    rc2, out2 = run(tool, e2)
    p0, p1 = parsed(out0), parsed(out1)
    arms = [
        ("unchanged-equals-committed", rc0 == 0 and p0 == committed, "rc=%s equal=%s :: %s" % (rc0, p0 == committed, tail(out0, 2))),
        ("staged-change-carried", rc1 == 0 and isinstance(p1, dict) and p1.get("dep_stage") == new,
         "rc=%s dep_stage=%s expected=%s" % (rc1, (p1 or {}).get("dep_stage") if isinstance(p1, dict) else None, new)),
        ("bad-row-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2, 2))),
        ("worktree-untouched", digest() == before, "sha256 same=%s" % (digest() == before)),
    ]
    sys.exit(finish("GS-E5-DERIVE", arms))
finally:
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
