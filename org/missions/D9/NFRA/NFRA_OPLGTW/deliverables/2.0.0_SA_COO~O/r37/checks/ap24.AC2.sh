#!/usr/bin/env bash
# OPLGTW OG-ap-24 AC2 (round-37 GRANTS-BATCH, PHASE B): the ledger is CLOSED with its sentinel gone, and W/GR_APPLIED.json names six roles live; the roles are RE-READ from IAM here.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-grants-ap24
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=0; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/GR_APPLIED.json" ] || { echo "GR_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
live=0; for r in gateway-49f-blackdiamond-read-role gateway-cot-blackdiamond-read-role gateway-inf-orion-read-role gateway-inf-eclipse-read-role gateway-cot-commonwealth-read-role gateway-smartx-read-role; do
  aws iam get-role --role-name "$r" --query 'Role.RoleName' --output text 2>/dev/null | tr -d '\r' | grep -qx "$r" && live=$((live+1)); done
# policy live: each of the six roles carries exactly one inline policy, RE-READ from IAM (list-role-policies is live; terraform state show is a stale cache, row Z-S157), and W/GR_APPLIED.json records _policy_live true.
pol=0; for r in gateway-49f-blackdiamond-read-role gateway-cot-blackdiamond-read-role gateway-inf-orion-read-role gateway-inf-eclipse-read-role gateway-cot-commonwealth-read-role gateway-smartx-read-role; do
  [ "$(aws iam list-role-policies --role-name "$r" --query 'length(PolicyNames)' --output text 2>/dev/null | tr -d '')" = 1 ] && pol=$((pol+1)); done
rec=$(python -c "import json,sys;print('true' if json.load(open(sys.argv[1],encoding='utf-8')).get('_policy_live') is True else 'false')" "$(native "$W/GR_APPLIED.json")" | tr -d '')
plive=no; [ "$pol" = 6 ] && [ "$rec" = true ] && plive=yes
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; roles live in IAM $live of 6;  policy live $plive"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$live" = 6 ] && [ "$plive" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
