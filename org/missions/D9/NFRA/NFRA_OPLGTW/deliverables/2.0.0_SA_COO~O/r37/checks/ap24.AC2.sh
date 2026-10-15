#!/usr/bin/env bash
# OPLGTW OG-ap-24 AC2 (round-37 GRANTS-BATCH, PHASE B): the ledger is CLOSED with its sentinel gone, and W/GR_APPLIED.json names six roles live and the invoke policy live; the roles are RE-READ from IAM here.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-grants-ap24
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=0; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/GR_APPLIED.json" ] || { echo "GR_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
live=0; for r in gateway-blackdiamond-read-role gateway-cot-blackdiamond-read-role gateway-inf-orion-read-role gateway-inf-eclipse-read-role gateway-cot-commonwealth-read-role gateway-smartx-read-role; do
  aws iam get-role --role-name "$r" --query 'Role.RoleName' --output text 2>/dev/null | tr -d '\r' | grep -qx "$r" && live=$((live+1)); done
inv=$(python -c "import json,sys;print('yes' if json.load(open(sys.argv[1],encoding='utf-8')).get('invoke_policy_live') is True else 'no')" "$(native "$W/GR_APPLIED.json")" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; roles live in IAM $live of 6; invoke policy live $inv"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$live" = 6 ] && [ "$inv" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
