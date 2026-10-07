#!/usr/bin/env bash
# OPLGTW OG-rl-11 AC3 (NFRA_OPALAI OA-f-14 on the SERVED gateway (CTO msg 30365): an UNSCOPED identity's consent scopes are unchanged (17);
# the scoped identity's are 8, or 9 under a Tax binding, a subset of the 17; its silent acquire still returns a token;
# every Graph probe its allowlisted tools need answers 200 with the narrowed token (SharePoint site resolve among
# them); the three host identity keys were read before GO.)
# RL11_SCOPES.json is attested by the host's own SSM output (`RL11C_DIGEST <sha256>` of its body).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL11_SCOPES.json"
[ -f "$F" ] || { echo "RL11_SCOPES.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r25/checks/_attest.py" "$(native "$F")" RL11C_DIGEST "$c" scopes | tr -d '\r'); rc=$?
echo "scoped consent narrowed and still working, unscoped unchanged, identity keys read: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
