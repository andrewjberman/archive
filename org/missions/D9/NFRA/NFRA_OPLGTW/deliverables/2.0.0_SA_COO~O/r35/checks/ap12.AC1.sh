#!/usr/bin/env bash
# OPLGTW OG-ap-12 AC1 (row Z-S97, both halves signed): ledger nfra-oplgtw-ap12-dlq-visibility is CLOSED at HEAD with its
# sentinel gone; a live simulate of opal-assets-silver-schwab-role for sqs:ChangeMessageVisibility on the silver DLQ reads
# allowed; the LIVE opal-assets-silver-schwab CodeSha256 equals the OG-ap-11 build (W/ap11_build.json code_sha256).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; slug=nfra-oplgtw-ap12-dlq-visibility
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
want=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('code_sha256','NONE'))" "$(native "$W/ap11_build.json")" | tr -d '\r')
errf=$(mktemp)
live=$(bash .tools/aws lambda get-function-configuration --function-name opal-assets-silver-schwab --region us-east-1 --query CodeSha256 --output text 2>"$errf" | tr -d '\r\n'); lrc=$?
[ "$lrc" = 0 ] && [ -n "$live" ] || { echo "live code read FAILED rc=$lrc: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }
q=$(bash .tools/aws sqs get-queue-url --queue-name opal-assets-silver-dlq --region us-east-1 --query QueueUrl --output text 2>"$errf" | tr -d '\r\n')
qarn=$(bash .tools/aws sqs get-queue-attributes --queue-url "$q" --attribute-names QueueArn --region us-east-1 --query Attributes.QueueArn --output text 2>"$errf" | tr -d '\r\n')
rarn=$(bash .tools/aws iam get-role --role-name opal-assets-silver-schwab-role --query Role.Arn --output text 2>"$errf" | tr -d '\r\n')
[ -n "$qarn" ] && [ -n "$rarn" ] || { echo "arn read FAILED: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }
sim=$(MSYS_NO_PATHCONV=1 bash .tools/aws iam simulate-principal-policy --policy-source-arn "$rarn" --action-names sqs:ChangeMessageVisibility --resource-arns "$qarn" --query 'EvaluationResults[0].EvalDecision' --output text 2>"$errf" | tr -d '\r\n')
[ -n "$sim" ] || { echo "simulate FAILED: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }; rm -f "$errf"
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
echo "simulate schwab-role sqs:ChangeMessageVisibility on $qarn: $sim"
echo "live CodeSha256 equals the OG-ap-11 build: $([ "$live" = "$want" ] && echo yes || echo no)"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$sim" = allowed ] && [ "$want" != NONE ] && [ "$live" = "$want" ] \
  && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
