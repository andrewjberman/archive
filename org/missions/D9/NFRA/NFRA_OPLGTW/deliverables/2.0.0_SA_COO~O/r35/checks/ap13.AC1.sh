#!/usr/bin/env bash
# OPLGTW OG-ap-13 AC1 (OG-tb-1's pair, COO condition B): ledger nfra-oplgtw-tb1-bearer-narrow CLOSED at HEAD, sentinel gone;
# the LIVE default version of cloudops-dell-agent-platform-secrets-policy has Sid ReadPlatformKeys with 30 ARNs, none of them
# gateway/teams/bearer; simulate cloudops-dell1-agent-user on the bearer ARN reads implicitDeny, and on one kept ARN reads allowed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
slug=nfra-oplgtw-tb1-bearer-narrow
P=arn:aws:iam::313476888478:policy/cloudops-dell-agent-platform-secrets-policy
B=arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/teams/bearer-93ZHiU
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
errf=$(mktemp)
ver=$(MSYS_NO_PATHCONV=1 bash .tools/aws iam get-policy --policy-arn "$P" --query Policy.DefaultVersionId --output text 2>"$errf" | tr -d '\r\n')
[ -n "$ver" ] || { echo "policy read FAILED: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }
doc=$(mktemp)
MSYS_NO_PATHCONV=1 bash .tools/aws iam get-policy-version --policy-arn "$P" --version-id "$ver" --query PolicyVersion.Document --output json >"$doc" 2>"$errf"
read -r n hasb keep <<<"$(python - "$(native "$doc")" "$B" <<'PY' | tr -d '\r'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
st = [s for s in d.get("Statement", []) if s.get("Sid") == "ReadPlatformKeys"]
r = st[0].get("Resource", []) if st else []
r = [r] if isinstance(r, str) else r
print(len(r), "yes" if sys.argv[2] in r else "no", (r[0] if r else "NONE"))
PY
)"
rm -f "$doc"
uarn=$(bash .tools/aws iam get-user --user-name cloudops-dell1-agent-user --query User.Arn --output text 2>"$errf" | tr -d '\r\n')
simb=$(MSYS_NO_PATHCONV=1 bash .tools/aws iam simulate-principal-policy --policy-source-arn "$uarn" --action-names secretsmanager:GetSecretValue --resource-arns "$B" --query 'EvaluationResults[0].EvalDecision' --output text 2>"$errf" | tr -d '\r\n')
simk=$(MSYS_NO_PATHCONV=1 bash .tools/aws iam simulate-principal-policy --policy-source-arn "$uarn" --action-names secretsmanager:GetSecretValue --resource-arns "$keep" --query 'EvaluationResults[0].EvalDecision' --output text 2>"$errf" | tr -d '\r\n')
[ -n "$simb" ] && [ -n "$simk" ] || { echo "simulate FAILED: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }; rm -f "$errf"
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
echo "default version $ver: ReadPlatformKeys ARNs $n (want 30); bearer listed: $hasb"
echo "simulate dell1 on bearer: $simb (want implicitDeny); on kept ARN: $simk (want allowed)"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$n" = 30 ] && [ "$hasb" = no ] && [ "$simb" = implicitDeny ] && [ "$simk" = allowed ] \
  && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
