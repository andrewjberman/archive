#!/usr/bin/env bash
# OPLGTW OG-rl-1 AC3 (CTO ruling R4, row Z-S24): the template SHIPPED (manifest deployed_commit at HEAD) reads both
# principal rosters host-side from gateway/principals/rosters, no longer requires them from the deploying shell, still
# renders MASTER_ADMIN_PRINCIPALS and WRITE_CAPABLE_PRINCIPALS with equal %s and argument counts, carries no GUID, and
# parses (bash -n).
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
live=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
echo "deployed_commit (manifest at HEAD): $live"
T=$(mktemp -d)
MSYS_NO_PATHCONV=1 git show "$live:$GW/deploy-to-ec2.sh" > "$T/deploy-to-ec2.sh" || { echo "shipped template unreadable"; echo "RESULT: FAIL"; exit 1; }
timeout 60 python "$(native "$H/_pr.py")" template "$(native "$T/deploy-to-ec2.sh")" 2>&1 | tr -d '\r'; r=$?
rm -rf "$T"; exit $r
