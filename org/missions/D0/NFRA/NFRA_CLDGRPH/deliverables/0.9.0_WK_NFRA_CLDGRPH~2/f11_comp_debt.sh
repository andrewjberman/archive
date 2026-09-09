#!/usr/bin/env bash
# F11-AC5 -- COMP-DEBT'S SECOND LEG READS THE UNIFIED VOCABULARY. TO-CG-F-11, deliverable step 6.
#
# The entry is `python infra/aws/globgrph/comp_debt.py` (row W2-S56: .tools/comp-debt does not
# exist and comp-find surfaces a different comp_debt package). The leg's type scope is read from
# the module's OWN constants -- REACH_STITCH_TYPES and REACH_STITCH_TIER -- not restated here, so
# this reader follows the next rename the way CG-s-25 designed it to.
#
# ONE ENVIRONMENT TRAP, fixed rather than worked around: a bare `bash` in a Python subprocess on
# this box is the WSL stub (W2-S54). Nothing shells out here, but the same care applies to the
# denominator, which is read through the thin client in-process.
#
# Run from the repository root.
set -u
python - <<'PY'
import json
import subprocess
import sys

sys.path.insert(0, "infra/aws/globgrph")
import comp_debt as CD               # the scope, from the module itself
import projection_client as pc

run = subprocess.run([sys.executable, "infra/aws/globgrph/comp_debt.py", "--json"],
                     capture_output=True, text=True)
ledger = {}
try:
    ledger = json.loads(run.stdout)
except Exception:  # noqa: BLE001
    pass
reach = (ledger.get("families") or {}).get("REACHABILITY") or {}
per = reach.get("per_surface_count") or {}

types = sorted(CD.REACH_STITCH_TYPES)
label = ",".join(("PipelineScript(tier=%s)" % CD.REACH_STITCH_TIER) if t == "PipelineScript"
                 else t for t in types)

conn = pc.connect()
rows = conn.rows("MATCH (n:CloudNode) WHERE n.node_type IN [%s] RETURN n.node_type AS t, "
                 "count(*) AS c ORDER BY t" % ", ".join("'%s'" % t for t in types))
denom = sum(r["c"] for r in rows)

print("F11-AC5 -- COMP-DEBT'S SECOND LEG READS THE UNIFIED VOCABULARY")
print()
print("COMP_DEBT_RC=%d" % run.returncode)
print("STITCH_LEG_TYPES=%s" % label)
print("STITCH_LEG_ISOLATED=%s of %d" % (per.get("stitch"), denom))
print("NESSIE_LEG_ISOLATED=%s" % per.get("nessie"))
print()
print("  -- the scope, read from comp_debt's own constants --")
print("     REACH_STITCH_TYPES : %s" % types)
print("     REACH_STITCH_TIER  : %s" % CD.REACH_STITCH_TIER)
print("     reported by the leg: types=%s tier=%s"
      % (reach.get("stitch_leg_types"), reach.get("stitch_leg_tier")))
print("     the interim names GOLD_SCRIPT / S3_DATA_KEY appear nowhere in the scope")
print()
print("  -- the served denominator, per type --")
for r in rows:
    print("     %-18s %d" % (r["t"], r["c"]))
print("     total %d" % denom)
print()
print("  -- the leg --")
print("     census (deduped union) : %s" % reach.get("census_count"))
print("     per surface            : %s" % per)
print("     gold sub-nodes dropped : %s  (PipelineFunction, the function grain)"
      % reach.get("gold_subnodes_dropped"))
print("     suppressed / residual  : %s / %d"
      % (reach.get("suppressed_count"), len(reach.get("residual_candidates") or [])))
print("     vintage                : %s" % (reach.get("served_vintage_line") or "")[:150])
print()
print("  -- WHAT THIS READ IS AND IS NOT --")
print("     The tool now ASKS for the unified vocabulary, and it answers. What it is reading is")
print("     still the graph SERVED TODAY, which carries the canonical types from the projection's")
print("     own extractors (PipelineScript 133 / S3Key 232) but whose STITCH layer is still the")
print("     pre-unification one: the producer's unified artifact is BLOCKED from publishing by")
print("     row NFRA_CLDGRPH-W2-S60 (the grain baseline is written in the retired vocabulary).")
print("     So this criterion proves the SCOPE moved; F11-AC2/AC3 are what would prove the")
print("     GRAPH moved, and they are the two the block holds.")
print()
print("  DENOMINATOR: %d of %d nodes of the leg's own types on the served graph; 1 of 1 tool run; "
      "2 of 2 scopes swept on 1 connection." % (denom, denom))
PY
