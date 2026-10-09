#!/usr/bin/env bash
# OPLGTW OG-ap-5 AC1 (OG-pn-1 Phase B, NEVER-2): ledger nfra-oplgtw-og-pn-1-converter is committed CLOSED at HEAD with its
# sentinel gone, and the LIVE opal-assets-silver-schwab CodeSha256 equals the built hash the applier recorded in
# W/ap5_build.json ({"code_sha256", "prior_code_sha256", "prior_artifact_version"}) and differs from the prior.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
slug=nfra-oplgtw-og-pn-1-converter
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap5_build.json"
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
want=NONE; prior=NONE
[ -f "$REC" ] && read -r want prior <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('code_sha256','NONE'),d.get('prior_code_sha256','NONE'))" "$(native "$REC")" | tr -d '\r')"
live=$(.tools/aws lambda get-function-configuration --function-name opal-assets-silver-schwab --region us-east-1 --query CodeSha256 --output text | tr -d '\r')
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
echo "live CodeSha256 equals the recorded build: $([ "$live" = "$want" ] && echo yes || echo no); differs from the prior: $([ "$live" != "$prior" ] && echo yes || echo no)"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$want" != NONE ] && [ "$live" = "$want" ] && [ "$live" != "$prior" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
