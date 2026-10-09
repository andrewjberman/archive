#!/usr/bin/env bash
# OPLGTW OG-rl-15 AC3 (the 13-month grant write, CTO ruling msg 32087): RL15_GRANTS.json, attested by the host's own SSM
# output (`RL15G_DIGEST <sha256>` of its body): exactly 2 principals changed (Andrew's and Alyssa's), the field changed is
# calendar_months only, both at 13, 0 other principals changed, the prior reach recorded for both keys, and a 13-month
# availability read under the new grant returns at least one available date.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43/RL15_GRANTS.json"
[ -f "$F" ] || { echo "RL15_GRANTS.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/rl15_attest.py" "$(native "$F")" RL15G_DIGEST "$c" | tr -d '\r'); rc=$?
echo "13-month grants: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
