#!/usr/bin/env bash
# OPLGTW OG-ap-9 AC2 (the session-free read-back, COO half condition B): the LIVE mcportal-grant-writer CodeSha256 (read now)
# equals the build recorded in W/ap9_build.json {"code_sha256"} and differs from the prior ZyYCPPyP5CV53eZP+UJHIgAjq834J4OsvePgmS6k8rI=.
# W/ap9_parse.json, from the DEPLOYED package's own parse_scope, reads deployed_accepts_13 true and prior_accepts_13 false
# (the negative control).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; PRIOR="ZyYCPPyP5CV53eZP+UJHIgAjq834J4OsvePgmS6k8rI="
[ -f "$W/ap9_build.json" ] && [ -f "$W/ap9_parse.json" ] || { echo "ap9_build.json or ap9_parse.json absent"; echo "RESULT: FAIL"; exit 1; }
built=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('code_sha256',''))" "$(native "$W/ap9_build.json")" | tr -d '\r')
# row Z-S93: the function is mcportal-grant-writer-lambda (mcportal_grant_writer.tf:128); the first cut named a function
# that does not exist and captured the error INTO the compared value. stderr now goes to its own file and a non-zero read FAILS.
errf=$(mktemp); live=$(bash .tools/aws lambda get-function-configuration --function-name mcportal-grant-writer-lambda --query CodeSha256 --output text 2>"$errf" | tr -d '\r\n'); lrc=$?
[ "$lrc" = 0 ] && [ -n "$live" ] || { echo "live read FAILED rc=$lrc: $(head -c 200 "$errf")"; rm -f "$errf"; echo "RESULT: FAIL"; exit 1; }
rm -f "$errf"
read -r d13 p13 <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('deployed_accepts_13'),d.get('prior_accepts_13'))" "$(native "$W/ap9_parse.json")" | tr -d '\r')"
echo "live CodeSha256 equals the build: $([ -n "$built" ] && [ "$live" = "$built" ] && echo yes || echo no); differs from the prior: $([ "$live" != "$PRIOR" ] && echo yes || echo no)"
echo "deployed package accepts calendar_months 13: $d13; prior package accepts it: $p13 (want False)"
[ -n "$built" ] && [ "$live" = "$built" ] && [ "$live" != "$PRIOR" ] && [ "$d13" = True ] && [ "$p13" = False ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
