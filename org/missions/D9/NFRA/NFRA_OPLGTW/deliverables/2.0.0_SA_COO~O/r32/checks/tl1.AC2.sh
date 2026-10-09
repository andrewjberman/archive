#!/usr/bin/env bash
# OPLGTW OG-tl-1 AC2 (on the SERVED gateway): TL1_READ.json, attested by the host's own SSM output (`TL1_DIGEST <sha256>`
# of its body): served_release equals EC2_MANIFEST's deployed_commit at HEAD, installed code, TRANSCRIPT_MEETING_ALLOWLIST
# holds exactly the 4 ids of meeting_allowlist.json (count + sha256 of the sorted ids), and it is the only .env value changed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~48/TL1_READ.json"
[ -f "$F" ] || { echo "TL1_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/rl15_attest.py" "$(native "$F")" TL1_DIGEST "$c" | tr -d '\r'); rc=$?
echo "transcript allowlist served: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
