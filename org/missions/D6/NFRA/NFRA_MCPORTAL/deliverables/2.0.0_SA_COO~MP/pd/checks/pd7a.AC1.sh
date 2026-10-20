#!/usr/bin/env bash
# MP-pd-7 AC1 (Act A only, AMENDMENT A2; the NEVER-2 ledger): the release's deploy-ledger entry nfra-mcportal-pd-release is CLOSED at HEAD
# with every leg proven, its sentinel org/critical_paths/.open_deploys/nfra-mcportal-pd-release.json is absent at HEAD, and it is not
# listed OPEN or HELD by deploy_ledger.py.
. "$(dirname "$0")/_root.sh"
CM=org/critical_paths/change_management
ent=$(ls $CM/*nfra-mcportal-pd-release* 2>/dev/null | tail -1)
n=$(ls $CM/*nfra-mcportal-pd-release* 2>/dev/null | wc -l)
sent=no; [ -f org/critical_paths/.open_deploys/nfra-mcportal-pd-release.json ] && sent=yes
closed=no; [ -n "$ent" ] && grep -q -E 'Status:\*\* CLOSED' "$ent" && closed=yes
open=$(python .tools/deploy_ledger.py check 2>&1 | tr -d '\r' | grep -c 'nfra-mcportal-pd-release')
echo "entry files at HEAD=$n; closed=$closed; sentinel=$sent; listed OPEN/HELD=$open"
if [ "$n" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = no ] && [ "$open" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
