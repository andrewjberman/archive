#!/usr/bin/env bash
# MX-i-5 AC3 (as amended A1): DEAD_PROOF_MX-i-5.md has one '## <rule>' section per leg, each with a VERDICT: DEAD|LIVE
# line and FIRST_FAILING:/LAST_NON_FAILING: lines; a DEAD section also has OUTPUT_SINCE_LAST_NON_FAILING: 0 and a
# per-step table in which no step writes live output (STEP lines, each 'STEP <n> | ... | writes since: 0').
. "$(dirname "$0")/_root.sh"
F=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/DEAD_PROOF_MX-i-5.md 2>/dev/null | head -1)
[ -n "$F" ] || { echo "DEAD_PROOF_MX-i-5.md absent"; echo "RESULT: FAIL"; exit 1; }
ok=0
for r in bd-allocation-pipeline-trigger bd-realized-pipeline-trigger bd-transaction-pipeline-trigger bd-unrealized-pipeline-trigger; do sec=$(awk -v h="## $r" 'index($0,h)==1{f=1;next} /^## /{if(f)exit} f' "$F"); v=$(printf '%s\n' "$sec" | sed -n 's/^VERDICT: \([A-Z]*\).*/\1/p' | head -1)
  base=0; printf '%s\n' "$sec" | grep -q '^FIRST_FAILING:' && printf '%s\n' "$sec" | grep -q '^LAST_NON_FAILING:' && base=1
  good=0
  if [ "$base" = 1 ] && [ "$v" = LIVE ]; then good=1; fi
  if [ "$base" = 1 ] && [ "$v" = DEAD ]; then s=$(printf '%s\n' "$sec" | grep -c '^STEP '); w=$(printf '%s\n' "$sec" | grep '^STEP ' | grep -vcE 'writes since: 0( |$)')
    printf '%s\n' "$sec" | grep -qE '^OUTPUT_SINCE_LAST_NON_FAILING: 0( |$)' && [ "$s" -ge 1 ] && [ "$w" = 0 ] && good=1; fi
  echo "  $r: verdict=${v:-NONE} complete=$good"; ok=$((ok+good)); done
echo "dead-proof sections complete $ok of 4"
if [ "$ok" = 4 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
