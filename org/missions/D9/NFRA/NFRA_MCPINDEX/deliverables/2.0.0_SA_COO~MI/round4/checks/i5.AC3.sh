#!/usr/bin/env bash
# MX-i-5 AC3 (R-15 (c)): DEAD_PROOF_MX-i-5.md (worker deliverables) has one section '## <rule>' per dead leg, each with FIRST_FAILING:, LAST_NON_FAILING: and OUTPUT_SINCE_LAST_NON_FAILING: 0 lines.
. "$(dirname "$0")/_root.sh"
F=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/DEAD_PROOF_MX-i-5.md 2>/dev/null | head -1)
[ -n "$F" ] || { echo "DEAD_PROOF_MX-i-5.md absent"; echo "RESULT: FAIL"; exit 1; }
ok=0; for r in bd-allocation-pipeline-trigger bd-realized-pipeline-trigger bd-transaction-pipeline-trigger bd-unrealized-pipeline-trigger; do sec=$(awk -v h="## $r" 'index($0,h)==1{f=1;next} /^## /{if(f)exit} f' "$F")
  if printf '%s\n' "$sec" | grep -q '^FIRST_FAILING:' && printf '%s\n' "$sec" | grep -q '^LAST_NON_FAILING:' && printf '%s\n' "$sec" | grep -qE '^OUTPUT_SINCE_LAST_NON_FAILING: 0( |$)'; then ok=$((ok+1)); else echo "  $r: section missing or incomplete"; fi; done
echo "dead-proof sections complete $ok of 4"
rc=1; [ "$ok" = 4 ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
