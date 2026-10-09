#!/usr/bin/env bash
# OPLGTW OG-rl-15 AC2 (release r29 on the SERVED gateway): RL15_READ.json, attested by the host's own SSM output
# (`RL15_DIGEST <sha256>` of its body), read through the INSTALLED code: opal_asker_query SAFE with no write class and 0
# registered tools unclassified (R54); the refresh/code send gate present in oauth_as (R50); calendar_months max 13 and
# contract 1.4 (PRD v2.0 item 4); the mail domain table holds exactly the signed entries (v1.9); 0 concierge refresh
# families revoked since the deploy (row Z-S67's disarm read); 0 grants written by the read.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43/RL15_READ.json"
[ -f "$F" ] || { echo "RL15_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/rl15_attest.py" "$(native "$F")" RL15_DIGEST "$c" | tr -d '\r'); rc=$?
echo "r29 served content: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
