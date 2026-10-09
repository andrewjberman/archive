"""GS-t-1 AC3: the corpus pass reads its BASELINE from the graded index, not the working tree (C-BYTES).

Plant: the baseline file in the private index loses its first tuple; the working tree copy is untouched.
Arm (no --act, today's whole-corpus mode): rc 1 and a NEW line for the dropped tuple's row id. A pass that
reads the baseline from the working tree sees no change and returns 0.
"""
import json
import shutil
import sys

from r1_common import BASELINE, finish, index_text, plant, run, tail, temp_index

d, env = temp_index()
try:
    data = json.loads(index_text(BASELINE))
    key = next(k for k, v in data.items() if isinstance(v, list) and v and isinstance(v[0], list))
    dropped = data[key][0]
    data[key] = data[key][1:]
    plant(env, BASELINE, json.dumps(data, indent=2) + "\n")
    rc, out = run([sys.executable, ".tools/surprise-corpus-validate.py"], env)
    row_id = str(dropped[1])
    seen = any(ln.strip().startswith("NEW") and row_id in ln for ln in out.splitlines())
    arms = [("index-baseline-read", rc == 1 and seen, "rc=%s new_line_for_%s=%s :: %s" % (rc, row_id, seen, tail(out)))]
    sys.exit(finish("GS-T1-BYTES", arms))
finally:
    shutil.rmtree(d, ignore_errors=True)
