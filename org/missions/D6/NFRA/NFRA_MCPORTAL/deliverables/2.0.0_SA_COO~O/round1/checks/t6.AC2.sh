#!/usr/bin/env bash
# MP-t-6 AC2 (the release record, C3): EC2_MANIFEST.json at HEAD records an opal-gateway deploy whose deployed_commit
# CONTAINS app/owner_gate.py and app/admin_grants.py, and a mcportal_commit that is a real commit of the mcportal repo.
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('mcportal_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); m=$(printf '%s\n' "$out" | sed -n 2p)
g=0; for f in app/owner_gate.py app/admin_grants.py; do git cat-file -e "$c:infra/aws/ec2/opal-gateway/$f" 2>/dev/null && g=$((g+1)); done
mc=no; [ "$m" != NONE ] && git -C mcportal cat-file -e "$m^{commit}" 2>/dev/null && mc=yes
echo "deployed_commit=$c carries the gate+handlers $g of 2; mcportal_commit=$m resolves in mcportal=$mc"
if [ "$g" = 2 ] && [ "$mc" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
