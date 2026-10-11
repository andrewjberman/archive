#!/usr/bin/env bash
# OPLGTW OG-ap-8 AC1 (OG-mu-1's grant, halves COO @34bf3d67a4 + CTO @e0ca80f880): ledger nfra-oplgtw-mu1-put-policy is CLOSED
# at HEAD with its sentinel gone. The targeted plan before the apply (W/ap8_plan_target.txt + .rc) read exactly
# 1 add 0 change 0 destroy at rc=0, the one address being aws_iam_role_policy.market_update_gateway_put. The re-plan after
# (W/ap8_replan.txt + .rc) read 0/0/0 at rc=0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; slug=nfra-oplgtw-mu1-put-policy; H="$(dirname "$0")/_tfplan.py"
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
python "$H" "$(native "$W/ap8_plan_target.txt")" "$(native "$W/ap8_plan_target.rc")" 1 0 0 aws_iam_role_policy.market_update_gateway_put; p1=$?
python "$H" "$(native "$W/ap8_replan.txt")" "$(native "$W/ap8_replan.rc")" 0 0 0; p2=$?
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$p1" = 0 ] && [ "$p2" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
