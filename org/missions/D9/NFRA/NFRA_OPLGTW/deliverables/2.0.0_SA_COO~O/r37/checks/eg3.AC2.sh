#!/usr/bin/env bash
# OPLGTW OG-eg-3 AC2 (round-37 HARVEST-RETIRE, PRD v3.11): the three runner ledgers are CLOSED at HEAD with their sentinels gone; the two earlier ones read SUPERSEDED;
# the proof records the FIRSTREC and WINDOW legs as NOT-EXERCISED.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/EG3_PROOF.json" ] || { echo "EG3_PROOF.json absent"; echo "RESULT: FAIL"; exit 1; }
closed=0; sent=0; sup=0
for slug in nfra-oplgtw-harvest-runner-retire nfra-oplgtw-harvest-runner-silver-cache nfra-oplgtw-harvest-runner-sa; do
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  if [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED'; then closed=$((closed+1)); fi
  sent=$((sent + $(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)))
  if [ "$slug" != nfra-oplgtw-harvest-runner-retire ] && [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qi 'SUPERSEDED'; then sup=$((sup+1)); fi
done
legs=$(python - "$(native "$W/EG3_PROOF.json")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("yes" if d.get("firstrec_not_exercised") is True and d.get("window_not_exercised") is True and d.get("state") == "Disabled" else "no")
PY
)
legs=$(printf '%s' "$legs" | tr -d '\r')
echo "ledgers closed $closed of 3; sentinels at HEAD $sent; superseded closes $sup of 2; proof legs not-exercised $legs"
[ "$closed" = 3 ] && [ "$sent" = 0 ] && [ "$sup" = 2 ] && [ "$legs" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
