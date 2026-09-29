#!/usr/bin/env bash
# MX-i-5 AC2 (R-15 (b)): the committed saved-plan text PLAN_MX-i-5.txt (worker deliverables) reads 'Plan: 0 to add, 4 to change, 0 to destroy' and every resource it changes is one of the 4 named aws_cloudwatch_event_rule resources.
. "$(dirname "$0")/_root.sh"
F=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/PLAN_MX-i-5.txt 2>/dev/null | head -1)
[ -n "$F" ] || { echo "PLAN_MX-i-5.txt absent"; echo "RESULT: FAIL"; exit 1; }
plan=$(grep -cE 'Plan: 0 to add, 4 to change, 0 to destroy' "$F")
chg=$(grep -E '^ *# .* will be (updated in-place|created|destroyed|replaced)' "$F")
n=$(printf '%s\n' "$chg" | grep -c .); rules=$(printf '%s\n' "$chg" | grep -cE '# aws_cloudwatch_event_rule\.')
echo "plan file $F: summary line present=$plan; changed resources $n, of which aws_cloudwatch_event_rule $rules"
rc=1; [ "$plan" -ge 1 ] && [ "$n" = 4 ] && [ "$rules" = 4 ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
