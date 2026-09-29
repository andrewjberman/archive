#!/usr/bin/env bash
# MX-i-5 AC1 (R-15 as amended A1): every one of the 4 legs is in the LIVE state its per-document verdict requires --
# VERDICT DEAD -> its EventBridge rule reads DISABLED; VERDICT LIVE -> it still reads ENABLED -- and the REST leg
# bd-asset-dim-pipeline-trigger still reads ENABLED (the negative control).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
F=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/DEAD_PROOF_MX-i-5.md 2>/dev/null | head -1)
[ -n "$F" ] || { echo "DEAD_PROOF_MX-i-5.md absent"; echo "RESULT: FAIL"; exit 1; }
verdict() { awk -v h="## $1" 'index($0,h)==1{f=1;next} /^## /{if(f)exit} f' "$F" | sed -n 's/^VERDICT: \([A-Z]*\).*/\1/p' | head -1; }
ok=0; dead=0
for r in bd-allocation-pipeline-trigger bd-realized-pipeline-trigger bd-transaction-pipeline-trigger bd-unrealized-pipeline-trigger; do v=$(verdict "$r"); s=$(timeout 40 "$AWS" events describe-rule --name "$r" --query State --output text 2>&1 | tr -d '\r')
  want=""; [ "$v" = DEAD ] && want=DISABLED; [ "$v" = LIVE ] && want=ENABLED; [ "$v" = DEAD ] && dead=$((dead+1))
  echo "  $r: verdict=${v:-NONE} live=$s want=${want:-?}"; [ -n "$want" ] && [ "$s" = "$want" ] && ok=$((ok+1)); done
c=$(timeout 40 "$AWS" events describe-rule --name bd-asset-dim-pipeline-trigger --query State --output text 2>&1 | tr -d '\r')
echo "legs in their verdict state $ok of 4 (DEAD verdicts: $dead); negative control bd-asset-dim-pipeline-trigger=$c"
if [ "$ok" = 4 ] && [ "$c" = ENABLED ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
