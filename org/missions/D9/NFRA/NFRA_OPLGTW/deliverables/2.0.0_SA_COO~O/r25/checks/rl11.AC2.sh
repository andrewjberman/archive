#!/usr/bin/env bash
# OPLGTW OG-rl-11 AC2 (R33 on the SERVED gateway: the tool count moved 65 -> 66; the read-only status tool answered for a known
# execution id with a terminal status; the real-send path waits at most 60 s in the call; no confirm=True was run.)
# RL11_SEND.json is attested by the host's own SSM output (`RL11S_DIGEST <sha256>` of its body).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL11_SEND.json"
[ -f "$F" ] || { echo "RL11_SEND.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r25/checks/_attest.py" "$(native "$F")" RL11S_DIGEST "$c" send | tr -d '\r'); rc=$?
echo "send split served (66 tools, status tool OK, inline wait <= 60 s, no real send run): $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
