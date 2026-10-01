#!/usr/bin/env bash
# OPLGTW OG-pr-1 AC3 (EXERCISED): the gateway HOST, under its own role, reads gateway/principals/rosters and it holds
# one master-admin pair and >=1 write-capable pairs (shape only, no value printed); NEVER-2 is closed at HEAD.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
SLUG="nfra-oplgtw-gateway-read-secrets"; INST="i-07dccb1615503ac99"; ok=1
params=$(python "$(native "$H/_pr_hostcmd.py")" | tr -d '\r')
id=$(aws ssm send-command --instance-ids "$INST" --document-name AWS-RunShellScript --region us-east-1 \
  --parameters "$params" --query Command.CommandId --output text | tr -d '\r')
echo "ssm command $id"
st=""
for _ in $(seq 1 20); do
  st=$(aws ssm get-command-invocation --command-id "$id" --instance-id "$INST" --region us-east-1 --query Status --output text 2>&1 | tr -d '\r')
  case "$st" in Success|Failed|Cancelled|TimedOut) break;; esac; sleep 3
done
out=$(aws ssm get-command-invocation --command-id "$id" --instance-id "$INST" --region us-east-1 --query StandardOutputContent --output text | tr -d '\r')
echo "host read status=$st; $out"
printf '%s\n' "$out" | grep -qE "^ROSTERS master 1 write [1-9][0-9]* all-pairs True$" || ok=0
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
echo "ledger entry files at HEAD=$entry; sentinel at HEAD=$sent"
{ [ "$entry" -ge 1 ] && [ "$sent" = no ]; } || ok=0
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
