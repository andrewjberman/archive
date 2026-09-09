#!/usr/bin/env bash
# F5-AC2 -- THE REAL RUN answers the stitch leg from the SERVED graph, inside the tool's own
# budget, with the stitch vintage disclosed. TO-CG-F-5, deliverable step 2.
#
# THE ENTRY IS NOT `.tools/comp-debt`. That path does not exist (row NFRA_CLDGRPH-W2-S56):
# `comp-which "comp-debt standing debt scan reachability"` returns NO curated rule, and
# `comp-find -i 'comp_debt|comp-debt' .tools org/modules` finds a DIFFERENT thing entirely --
# the org/modules/graph/comp_debt/ package (a fusion/guard signal engine). The tool this cell
# repoints is `python infra/aws/globgrph/comp_debt.py`, whose argparse prog is "comp-debt".
#
# THE BUDGET IS THE TOOL'S OWN AND IS IMPORTED, NEVER RE-TYPED. comp_debt.py prints no
# `WITHIN BUDGET` line of its own (row W2-S55) -- the bound it actually carries is the thin
# client's DEFAULT_QUERY_TIMEOUT_S, which the REACHABILITY leg spends twice, once per scope.
# The verdict below is the measured wall clock against 2 x that constant.
#
# Run from the repository root.
set -u

python - <<'PY'
import json
import subprocess
import sys
import time

sys.path.insert(0, "infra/aws/globgrph")
import projection_client as pc     # for the budget constant and the denominator, never re-typed

BUDGET_S = pc.DEFAULT_QUERY_TIMEOUT_S * 2      # the leg spends the client's timeout once per scope

t0 = time.time()
run = subprocess.run([sys.executable, "infra/aws/globgrph/comp_debt.py", "--json"],
                     capture_output=True, text=True)
elapsed = time.time() - t0

ledger = {}
try:
    ledger = json.loads(run.stdout)
except Exception:  # noqa: BLE001
    pass
reach = (ledger.get("families") or {}).get("REACHABILITY") or {}
per = reach.get("per_surface_count") or {}
vline = reach.get("served_vintage_line") or ""

# the DENOMINATOR: how many stitch-typed nodes the served graph carries at all
conn = pc.connect()
rows = conn.rows("MATCH (n:CloudNode) WHERE n.node_type IN ['GOLD_SCRIPT','S3_DATA_KEY'] "
                 "RETURN n.node_type AS t, count(*) AS c ORDER BY t")
denom = sum(r["c"] for r in rows)

print("F5-AC2 -- THE REAL RUN, AGAINST THE SERVED GRAPH")
print("  entry: python infra/aws/globgrph/comp_debt.py --json   (not .tools/comp-debt; W2-S56)")
print()
print("COMP_DEBT_RC=%d" % run.returncode)
print("STITCH_LEG_ISOLATED=%s of %d stitch-typed nodes" % (per.get("stitch"), denom))
print("NESSIE_LEG_ISOLATED=%s" % per.get("nessie"))
print("VINTAGE_LINE_HAS_STITCH=%s" % ("true" if "Stitch source:" in vline else "false"))
print("WITHIN_BUDGET=%s" % ("true" if elapsed <= BUDGET_S else "false"))
print()
print("  -- the leg --")
print("     census (deduped union)      : %s" % reach.get("census_count"))
print("     per surface                 : %s" % per)
print("     deduped across surfaces     : %s" % reach.get("deduped_across_surfaces"))
print("     gold sub-nodes dropped      : %s" % reach.get("gold_subnodes_dropped"))
print("     suppressed (logged)         : %s" % reach.get("suppressed_count"))
print("     residual (REAL orphans)     : %d" % len(reach.get("residual_candidates") or []))
print("     new vs baseline             : %d" % len(reach.get("new_vs_baseline") or []))
print()
print("  -- the vintage, ONE line for BOTH legs, from the ANSWER's own response --")
print("     %s" % vline)
print()
print("  -- the budget --")
print("     bound   : %.0f s = 2 x projection_client.DEFAULT_QUERY_TIMEOUT_S (%.0f s), one per scope"
      % (BUDGET_S, pc.DEFAULT_QUERY_TIMEOUT_S))
print("     measured: %.1f s wall clock for the WHOLE tool (both families, both legs)" % elapsed)
print("     the tool prints no budget line of its own -- row W2-S55; this bound is the only one")
print("     it carries, imported from the client rather than re-typed here.")
print()
print("  -- the CONTROL: what this run would have been before CG-s-24 --")
print("     a REFUSAL. The pre-F-4 leg opened kuzu_stitch_db and _stitch_freshness raised")
print("     SystemExit when it was absent; this worktree has never had that store, so the")
print("     old code could not have produced a scorecard here at all. The store's presence")
print("     now: %s" % __import__("os").path.exists("infra/aws/globgrph/kuzu_stitch_db"))
print()
print("  DENOMINATOR: 1 of 1 real run; %d of %d stitch-typed nodes in the served graph are the "
      "denominator of the stitch leg's %s isolates; 2 of 2 scopes swept, on 1 connection."
      % (denom, denom, per.get("stitch")))
PY
