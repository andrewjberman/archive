#!/usr/bin/env bash
# OA-t-6 AC2 (the release record): EC2_MANIFEST.json at HEAD records an opal-gateway deploy AFTER the round's cut, by
# this cell's worker, whose deployed_commit is a commit that CONTAINS app/asker_scope.py (the build OA-t-5 merged).
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('deployed_at','NONE')); print(s.get('deployed_by','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); at=$(printf '%s\n' "$out" | sed -n 2p); by=$(printf '%s\n' "$out" | sed -n 3p)
has=no; git cat-file -e "$c:infra/aws/ec2/opal-gateway/app/asker_scope.py" 2>/dev/null && has=yes
after=no; [ "$at" \> "2026-09-24T21:00:00Z" ] && after=yes
echo "deployed_commit=$c deployed_at=$at deployed_by=$by; commit contains asker_scope.py=$has; after the cut=$after"
if [ "$has" = yes ] && [ "$after" = yes ] && printf '%s' "$by" | grep -q '^0\.9\.0_WK_NFRA_OPALAI~'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
