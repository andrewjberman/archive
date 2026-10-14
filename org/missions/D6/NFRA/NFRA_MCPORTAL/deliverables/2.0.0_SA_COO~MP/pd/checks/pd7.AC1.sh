#!/usr/bin/env bash
# MP-pd-7 AC1 (F2 live; the NEVER-2 ledger): the release's deploy-ledger entry nfra-mcportal-pd-release is CLOSED at HEAD with
# every leg proven, its sentinel org/critical_paths/.open_deploys/nfra-mcportal-pd-release.json is absent at HEAD, it is not
# listed OPEN or HELD by deploy_ledger.py, the gateway release descends from the live base the GO named, and the gateway
# diff against that base names only the order's files (outside the F2 set = 0). The base is read from the GO file.
. "$(dirname "$0")/_root.sh"
CM=org/critical_paths/change_management
ent=$(ls $CM/*nfra-mcportal-pd-release* 2>/dev/null | tail -1)
n=$(ls $CM/*nfra-mcportal-pd-release* 2>/dev/null | wc -l)
sent=no; [ -f org/critical_paths/.open_deploys/nfra-mcportal-pd-release.json ] && sent=yes
closed=no; [ -n "$ent" ] && grep -q -E 'Status:\*\* CLOSED' "$ent" && closed=yes
open=$(python .tools/deploy_ledger.py check 2>&1 | tr -d '\r' | grep -c 'nfra-mcportal-pd-release')
GO="$PDD/2.0.0_SA_COO~MP/pd/GO_MP-pd-7.md"
base=$(grep -oE 'LIVE_BASE=[0-9a-f]{10,40}' "$GO" 2>/dev/null | head -1 | cut -d= -f2)
desc=no; outside=n/a
if [ -n "$base" ]; then
  git merge-base --is-ancestor "$base" HEAD 2>/dev/null && desc=yes
  outside=$(git diff --name-only "$base" HEAD -- infra/aws/ec2/opal-gateway 2>/dev/null | grep -v -E '^infra/aws/ec2/opal-gateway/(app/admin_api\.py|app/admin_people\.py|app/admin_people_access\.py|tests/test_admin_people\.py|tests/test_admin_people_access\.py)$' | wc -l)
fi
echo "entry files at HEAD=$n; closed=$closed; sentinel=$sent; listed OPEN/HELD=$open; base=${base:-none}; descends=$desc; outside the F2 set=$outside"
if [ "$n" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = no ] && [ "$open" = 0 ] && [ "$desc" = yes ] && [ "$outside" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
