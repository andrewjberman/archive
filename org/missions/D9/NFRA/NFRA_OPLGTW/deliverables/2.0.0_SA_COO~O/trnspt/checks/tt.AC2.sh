#!/usr/bin/env bash
# OPLGTW OG-tt-1 AC2 (APPLIED and EXERCISED): the live https listener carries exactly one rule with the Tax path, exactly
# /ms/taxsma-workbook, forward; an unauthenticated GET there reaches the gateway (not the sign-in); an unknown /ms path
# and / still meet the sign-in; /ms/sites still 401 from the app; NEVER-2 closed.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
SLUG="nfra-oplgtw-taxsma-alb-rule"; ok=1; T=$(mktemp -d)
lb=$(aws elbv2 describe-load-balancers --names opal-gateway --region us-east-1 --query 'LoadBalancers[0].LoadBalancerArn' --output text | tr -d '\r')
ls=$(aws elbv2 describe-listeners --load-balancer-arn "$lb" --region us-east-1 --query 'Listeners[?Port==`443`].ListenerArn | [0]' --output text | tr -d '\r')
aws elbv2 describe-rules --listener-arn "$ls" --region us-east-1 --output json > "$T/rules.json"; echo "describe-rules rc=$?"
timeout 60 python "$(native "$H/_tt_probe.py")" > "$T/probe.json"; echo "probe rc=$?"
timeout 60 python "$(native "$H/_tt.py")" live "$(native "$T/rules.json")" "$(native "$T/probe.json")" 2>&1 | tr -d '\r' | sed '$d'
timeout 60 python "$(native "$H/_tt.py")" live "$(native "$T/rules.json")" "$(native "$T/probe.json")" >/dev/null 2>&1 || ok=0
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
echo "ledger entry files at HEAD=$entry; sentinel at HEAD=$sent"
{ [ "$entry" -ge 1 ] && [ "$sent" = no ]; } || ok=0
rm -rf "$T"
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
