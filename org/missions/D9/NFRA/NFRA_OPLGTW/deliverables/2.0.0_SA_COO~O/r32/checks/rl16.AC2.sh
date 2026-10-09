#!/usr/bin/env bash
# OPLGTW OG-rl-16 AC2 (E2 .xlsx on the SERVED gateway, packet E2 section 7): RL16_READ.json, attested by the host's own
# SSM output (`E2_DIGEST <sha256>` of its body): served_release == EC2_MANIFEST deployed_commit at HEAD; the tool is
# listed, not SAFE, class write_files; one refused call on a bad quarter wrote nothing; the host's fee_statement root
# equals address(); the .pptx pair's root is absent.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~51/RL16_READ.json"
[ -f "$F" ] || { echo "RL16_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/rl15_attest.py" "$(native "$F")" E2_DIGEST "$c" | tr -d '\r'); rc=$?
echo "E2 served: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
