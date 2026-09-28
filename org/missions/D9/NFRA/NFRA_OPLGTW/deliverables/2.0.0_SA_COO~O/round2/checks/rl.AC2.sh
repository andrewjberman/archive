#!/usr/bin/env bash
# OPLGTW OG-e-2 AC2 (the NARROW release, read from the committed record): EC2_MANIFEST.json at HEAD records an opal-gateway
# deployed_commit that DESCENDS from its previous_deployed_commit; whose gateway-tree difference touches ONLY files
# OG-e-1's commits changed (author 0.9.0_WK_NFRA_OPLGTW~7); and whose app/data_entitlement.py carries email_denial.
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('previous_deployed_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); p=$(printf '%s\n' "$out" | sed -n 2p)
desc=no; [ "$p" != NONE ] && git merge-base --is-ancestor "$p" "$c" 2>/dev/null && desc=yes
allowed=$(git log --format=%H --author='0.9.0_WK_NFRA_OPLGTW~7 <' HEAD -- "$GW" | while read h; do git show --name-only --format= "$h" -- "$GW"; done | sort -u)
shipped=$( [ "$p" != NONE ] && git diff --name-only "$p" "$c" -- "$GW" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
foreign=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed" | grep .)); nf=$(printf '%s\n' "$foreign" | grep -c .)
g=$(git show "$c:$GW/app/data_entitlement.py" 2>/dev/null | grep -c "def email_denial")
[ "$nf" != 0 ] && printf '%s\n' "$foreign" | sed 's/^/  foreign: /'
echo "deployed_commit=$c previous=$p descends=$desc; gateway files shipped $nship, outside OG-e-1's set $nf; email_denial carried $g"
if [ "$desc" = yes ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$g" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
