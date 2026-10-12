#!/usr/bin/env bash
# OPLGTW OG-ap-11 AC1 (OG-fd-1's schwab deploy, NEVER-2): ledger nfra-oplgtw-fd1-schwab-drain is CLOSED at HEAD with its sentinel
# gone. The LIVE opal-assets-silver-schwab CodeSha256 equals the build recorded in W/ap11_build.json {"code_sha256",
# "prior_code_sha256"} and differs from the prior. The pre-deploy record-shape read W/ap11_record_shape.json shows a live DLQ
# on-failure record carries requestContext.functionArn, read without consuming it (COO half condition C).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; slug=nfra-oplgtw-fd1-schwab-drain
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
want=NONE; prior=NONE
[ -f "$W/ap11_build.json" ] && read -r want prior <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('code_sha256','NONE'),d.get('prior_code_sha256','NONE'))" "$(native "$W/ap11_build.json")" | tr -d '\r')"
errf=$(mktemp); live=$(bash .tools/aws lambda get-function-configuration --function-name opal-assets-silver-schwab --region us-east-1 --query CodeSha256 --output text 2>"$errf" | tr -d '\r\n'); lrc=$?
[ "$lrc" = 0 ] && [ -n "$live" ] || { echo "live read FAILED rc=$lrc: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }; rm -f "$errf"
shape=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print('yes' if d.get('functionArn_present') is True and d.get('read_nondestructive') is True else 'no')" "$(native "$W/ap11_record_shape.json")" 2>/dev/null | tr -d '\r'); shape=${shape:-absent}
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
echo "live CodeSha256 equals the recorded build: $([ "$live" = "$want" ] && echo yes || echo no); differs from the prior: $([ "$live" != "$prior" ] && echo yes || echo no); live record carries functionArn: $shape"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$want" != NONE ] && [ "$live" = "$want" ] && [ "$live" != "$prior" ] && [ "$shape" = yes ] \
  && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
