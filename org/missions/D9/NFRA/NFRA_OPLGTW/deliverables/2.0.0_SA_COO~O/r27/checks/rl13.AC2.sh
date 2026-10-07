#!/usr/bin/env bash
# OPLGTW OG-rl-13 AC2 (the two cells on the SERVED gateway): RL13_READ.json, attested by the host's own SSM output
# (`RL13_DIGEST <sha256>` of its body), records through the INSTALLED code: the status tool, called through the dispatch
# wrapper as the scoped concierge, answers OK with a displayed_date equal to the served manifest's generated_at; a
# rivalfunds page request writes an audit record whose kept args are exactly day and route and whose bytes equal the
# page served; a chart 404 keeps day, fund and route; no other arg is kept; tools 66; consent 9; grants_written 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL13_READ.json"
[ -f "$F" ] || { echo "RL13_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r27/checks/rl13_attest.py" "$(native "$F")" RL13_DIGEST "$c" | tr -d '\r'); rc=$?
echo "status date and audit args on the served release: $line"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
