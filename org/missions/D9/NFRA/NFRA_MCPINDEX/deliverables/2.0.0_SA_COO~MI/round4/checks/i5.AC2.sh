#!/usr/bin/env bash
# MX-i-5 AC2 (as amended A1): the committed PLAN_MX-i-5.txt changes exactly the rules whose DEAD_PROOF verdict is DEAD
# -- 'Plan: 0 to add, N to change, 0 to destroy' with N = the number of DEAD verdicts, every change an
# aws_cloudwatch_event_rule.
. "$(dirname "$0")/_root.sh"
F=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/DEAD_PROOF_MX-i-5.md 2>/dev/null | head -1)
[ -n "$F" ] || { echo "DEAD_PROOF_MX-i-5.md absent"; echo "RESULT: FAIL"; exit 1; }
verdict() { awk -v h="## $1" 'index($0,h)==1{f=1;next} /^## /{if(f)exit} f' "$F" | sed -n 's/^VERDICT: \([A-Z]*\).*/\1/p' | head -1; }
P=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/PLAN_MX-i-5.txt 2>/dev/null | head -1)
[ -n "$P" ] || { echo "PLAN_MX-i-5.txt absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for r in bd-allocation-pipeline-trigger bd-realized-pipeline-trigger bd-transaction-pipeline-trigger bd-unrealized-pipeline-trigger; do [ "$(verdict "$r")" = DEAD ] && n=$((n+1)); done
plan=$(grep -cE "Plan: 0 to add, $n to change, 0 to destroy" "$P")
chg=$(grep -E '^ *# .* will be (updated in-place|created|destroyed|replaced)' "$P"); c=$(printf '%s\n' "$chg" | grep -c .); rules=$(printf '%s\n' "$chg" | grep -cE '# aws_cloudwatch_event_rule\.')
echo "DEAD verdicts $n; plan summary 'Plan: 0 to add, $n to change, 0 to destroy' present=$plan; changed resources $c, of which aws_cloudwatch_event_rule $rules"
if [ "$n" -ge 1 ] && [ "$plan" -ge 1 ] && [ "$c" = "$n" ] && [ "$rules" = "$n" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
