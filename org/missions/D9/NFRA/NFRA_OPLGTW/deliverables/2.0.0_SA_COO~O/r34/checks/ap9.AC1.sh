#!/usr/bin/env bash
# OPLGTW OG-ap-9 AC1 (OG-gw-1's apply, halves COO @88926383b1 + CTO @bef54b9b62): ledger nfra-oplgtw-grant-writer-rebuild is
# CLOSED at HEAD with its sentinel gone. The fresh targeted plan at the act (W/ap9_plan_target.txt + .rc) read 0/1/0 at rc=0
# on aws_lambda_function.mcportal_grant_writer only. The re-plan after (W/ap9_replan.txt + .rc) read 0/0/0 at rc=0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; slug=nfra-oplgtw-grant-writer-rebuild; H="$(dirname "$0")/_tfplan.py"
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
python "$H" "$(native "$W/ap9_plan_target.txt")" "$(native "$W/ap9_plan_target.rc")" 0 1 0 aws_lambda_function.mcportal_grant_writer; p1=$?
python "$H" "$(native "$W/ap9_replan.txt")" "$(native "$W/ap9_replan.rc")" 0 0 0; p2=$?
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$p1" = 0 ] && [ "$p2" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
