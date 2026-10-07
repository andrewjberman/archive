#!/usr/bin/env bash
# OPLGTW OG-rl-12 AC2 (the row on the SERVED gateway): RL12_ALLOW.json, attested by the host's own SSM output
# (`RL12_DIGEST <sha256>` of its body), records through the INSTALLED code: the scoped concierge is admitted for
# opal_data_refresh_status and still denied a tool nothing names; its consent scope count is unchanged (9); the tool
# count is unchanged (66); the overlay holds one more row than before; grants_written 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL12_ALLOW.json"
[ -f "$F" ] || { echo "RL12_ALLOW.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r26/checks/rl12_attest.py" "$(native "$F")" RL12_DIGEST "$c" | tr -d '\r'); rc=$?
echo "concierge admitted for the status tool on the served release, nothing else widened: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
