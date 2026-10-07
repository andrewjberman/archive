#!/usr/bin/env bash
# OPLGTW OG-rl-14 AC2 (the audit-lake key on the SERVED gateway): RL14_READ.json, attested by the host's own SSM output
# (`RL14_DIGEST <sha256>` of its body), records through the INSTALLED code, with NO object written to the lake: the
# key builder gives a record that has no `ts` a key whose time part is non-empty and whose day equals that time's day;
# a record that carries `ts` gets the key shape it had before; the builder changes no record; tools 66; consent 9.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL14_READ.json"
[ -f "$F" ] || { echo "RL14_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r29/checks/rl14_attest.py" "$(native "$F")" RL14_DIGEST "$c" | tr -d '\r'); rc=$?
echo "audit-lake key stamp on the served release: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
