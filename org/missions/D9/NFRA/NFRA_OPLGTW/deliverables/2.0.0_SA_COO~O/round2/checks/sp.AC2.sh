#!/usr/bin/env bash
# OPLGTW OG-s-1 AC2 (the NARROW release, read from the committed record): EC2_MANIFEST.json at HEAD records an
# opal-gateway deployed_commit that DESCENDS from its previous_deployed_commit; the gateway-tree difference between them
# is EXACTLY one file, deploy-to-ec2.sh; and that commit's .env template (the printf near :196) carries the key
# SPRINT_VIEW_ALLOWED_EMAILS= exactly once. Prints counts only, never an address.
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('previous_deployed_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); p=$(printf '%s\n' "$out" | sed -n 2p)
desc=no; [ "$p" != NONE ] && git merge-base --is-ancestor "$p" "$c" 2>/dev/null && desc=yes
shipped=$( [ "$p" != NONE ] && git diff --name-only "$p" "$c" -- "$GW" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
only=no; [ "$nship" = 1 ] && [ "$shipped" = "$GW/deploy-to-ec2.sh" ] && only=yes
k=$(git show "$c:$GW/deploy-to-ec2.sh" 2>/dev/null | grep -o 'SPRINT_VIEW_ALLOWED_EMAILS=' | wc -l | tr -d ' ')
echo "deployed_commit=$c previous=$p descends=$desc; gateway files shipped $nship, only deploy-to-ec2.sh=$only; template key occurrences=$k"
if [ "$desc" = yes ] && [ "$only" = yes ] && [ "$k" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
