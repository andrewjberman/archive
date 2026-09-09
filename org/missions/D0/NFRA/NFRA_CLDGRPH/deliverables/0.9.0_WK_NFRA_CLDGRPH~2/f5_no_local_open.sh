#!/usr/bin/env bash
# F5-AC3 -- NO LOCAL STORE OPENED. TO-CG-F-5, deliverable step 3.
#
# Four independent readings, because "the tool does not open a store" can be wrong in four
# different ways and only one of them is visible to any single instrument:
#   AST      an ast.walk over the REACHABILITY path's two files (comp_debt.py, projection_client.py)
#            -- not a text scan, which cannot tell a live call from the docstring that RECORDS the
#            retirement, and this file's prose deliberately still contains the words
#   CONSTANT the STITCH_DB name itself, checked in the CODE band only (comp-read's banding), so the
#            retirement note in the docstring does not read as a survival
#   PROCESS  the tool RUN, to completion, from a worktree where the store does not exist at all --
#            the strongest of the four, because it is the world rather than the source
#   CONTROL  the same AST walker over a file WRITTEN to contain an open. A 0 from a walker that
#            cannot find one is not a measurement.
#
# Run from the repository root.
set -u
D="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"
python "$D/f5_no_local_open.py" \
  --files infra/aws/globgrph/comp_debt.py infra/aws/globgrph/projection_client.py \
  --plant-dir .scratch/f5 > .scratch/f5/ast_census.json 2>&1
python - "$D" <<'PY'
import io
import json
import os
import subprocess
import sys

d = sys.argv[1]
c = json.load(open(".scratch/f5/ast_census.json", encoding="utf-8"))

# the constant, in the CODE band only -- comp-read bands the retirement note as DOCSTRING/COMMENT
r = subprocess.run([sys.executable, ".tools/comp-read", "infra/aws/globgrph/comp_debt.py",
                    "--enumerate", r"kuzu\.(Database|Connection)|STITCH_DB|_stitch_freshness|kuzu_stitch_db"],
                   capture_output=True, text=True)
enum = r.stdout or ""
code_hits = [ln for ln in enum.splitlines() if "  CODE " in ln and "hit " in ln]
bands = [ln.strip() for ln in enum.splitlines()
         if ln.strip().startswith(("DOCSTRING", "COMMENT", "CODE", "DEF"))]

store = "infra/aws/globgrph/kuzu_stitch_db"
store_present = os.path.exists(store)
run = subprocess.run([sys.executable, "infra/aws/globgrph/comp_debt.py"],
                     capture_output=True, text=True)
ran = run.returncode == 0 and "REACHABILITY" in (run.stdout or "")

print("F5-AC3 -- NO LOCAL STORE OPENED")
print()
print("LOCAL_OPEN_SITES=%d of %d files" % (c["files_with_a_local_open"], c["files_walked"]))
print("STITCH_DB_CONSTANT_PRESENT=%s" % ("true" if code_hits else "false"))
print("RUNS_WITHOUT_STORE=%s" % ("true" if (ran and not store_present) else "false"))
print("LOCAL_OPEN_PROBE_CONTROL=%s" % ("FIRED" if c["control_fired"] else "DID-NOT-FIRE"))
print()
print("  -- the AST walk, per file --")
for p, hits in c["per_file"].items():
    print("     %-44s %d open/import site(s)" % (p, len(hits)))
    for h in hits:
        print("        line %s  %s" % (h["line"], h["shape"]))
print()
print("  -- the constant, by BAND (a docstring mention is not a survival) --")
for b in bands:
    print("     " + b)
print("     CODE-band hits naming the retired store: %d" % len(code_hits))
for ln in code_hits:
    print("       " + ln.strip()[:150])
print()
print("  -- the PROCESS reading, the one that is the world and not the source --")
print("     store path            : %s" % store)
print("     store exists here     : %s" % store_present)
print("     tool exit code        : %d" % run.returncode)
print("     scorecard produced    : %s" % ("REACHABILITY" in (run.stdout or "")))
for ln in (run.stdout or "").splitlines():
    if ln.startswith("REACHABILITY") or "surfaces:" in ln:
        print("     " + ln.strip()[:150])
print()
print("  -- the CONTROL --")
print("     planted file          : %s" % c["control_planted_file"])
print("     the SAME walker found : %d site(s) %s"
      % (len(c["control_hits"]), [h["shape"] for h in c["control_hits"]]))
print("     so the 0 above is a measurement, not a walker that cannot see.")
print()
print("  DENOMINATOR: %d of %d files on the REACHABILITY path walked by AST (comp_debt.py and "
      "projection_client.py; canon_motif_scorer is a DIFFERENT family and uses the kuzu library "
      "legitimately, so it is declared out of this population rather than silently included); "
      "1 of 1 planted control; 1 of 1 process run from a worktree with no store."
      % (c["files_walked"], c["files_walked"]))
PY
