# PRESERVED BY 2.0.0_SA_COO~G AT THE DRAIN OF LGIC_ENFORCE.TO-EN-s-32-r6, UNMODIFIED BELOW THIS HEADER.
# ORIGIN: cmp_instruments.py of worktree .worktrees/wk-lgic-enforce-6-1, authored by 0.9.0_WK_LGIC_ENFORCE~1, NEVER COMMITTED
#   and about to be deleted with that worktree.
# WHY: DISARM_SWEEP_R6.json's own denominators.instrument field cites ".scratch/measure_armed.py" as the
#   SECOND, deliberately different reader whose agreement with check_en_r6.py's armed_population() is the
#   cell's corroboration claim. An untracked instrument makes that claim UNVERIFIABLE the moment the
#   worktree is removed -- the record would cite an instrument nobody can run.
# NOT CLAIMED: that this seat has re-run or reviewed the logic below. It is preserved VERBATIM as evidence,
#   and its own sha1 under git hash-object is recorded in the commit that adds it.
# THIS COPY IS NOT ON ANY EXECUTION PATH. No criterion invokes it.
#!/usr/bin/env python3
"""Drive the CHECKER's own armed_population() and compare it to my re-derivation.

Reads the fixed input as a module; edits nothing.
"""
import importlib.util
import json
import os
import sys

REPO = sys.argv[1]
CHK = os.path.join(
    REPO, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "deliverables",
    "2.0.0_SA_COO~G", "fixed_inputs", "r6", "check_en_r6.py")

spec = importlib.util.spec_from_file_location("check_en_r6", CHK)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

still, closed, note = mod.armed_population()
print("CHECKER armed_population(): " + note)
counts = {}
for o in still.values():
    counts[o] = counts.get(o, 0) + 1
print("CHECKER owners: %s" % json.dumps(counts, sort_keys=True))

mine = json.load(open(os.path.join(REPO, ".scratch", "armed_start.json"), encoding="utf-8"))
print("MINE occurrences=%d distinct=%d armed=%d closed=%d still=%d"
      % (mine["occurrences"], mine["distinct_ids"], mine["armed_ids"],
         len(mine["closed"]), len(mine["still_armed_owners"])))
print("MINE owners: %s" % json.dumps(mine["owner_counts"], sort_keys=True))

a = set(still)
b = set(mine["still_armed_owners"])
print("STILL-ARMED SET IDENTICAL: %s" % (a == b))
print("only in checker: %s" % sorted(a - b))
print("only in mine: %s" % sorted(b - a))
dis = [k for k in sorted(a & b) if still[k] != mine["still_armed_owners"][k]]
print("owner disagreements: %s" % dis)

# where does the occurrence count differ? compare per-document row tallies.
chk_pairs = mod.channel_rows()
per = {}
for doc, r in chk_pairs:
    per[doc] = per.get(doc, 0) + 1
print("CHECKER per-document rows: %s" % json.dumps(per, sort_keys=True))
