#!/usr/bin/env bash
# MX-r-3 AC2 (the NARROW release, R-8, read from the committed record): EC2_MANIFEST.json at HEAD records an opal-gateway
# deployed_commit that DESCENDS from the previous_deployed_commit it also records; whose gateway-tree difference from that
# previous commit touches ONLY files NFRA_MCPINDEX's own commits changed (authors 0.9.0_WK_NFRA_MCPINDEX~<n>, reachable
# from HEAD); and which carries the two new integrations (app/integrations/opal_discover/, app/integrations/portal_index/).
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('previous_deployed_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); p=$(printf '%s\n' "$out" | sed -n 2p)
desc=no; [ "$p" != NONE ] && git merge-base --is-ancestor "$p" "$c" 2>/dev/null && desc=yes
allowed=$(git log --format=%H --author='0.9.0_WK_NFRA_MCPINDEX~' HEAD -- "$GW" | while read h; do git show --name-only --format= "$h" -- "$GW"; done | sort -u)
shipped=$( [ "$p" != NONE ] && git diff --name-only "$p" "$c" -- "$GW" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
foreign=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed" | grep .)); nf=$(printf '%s\n' "$foreign" | grep -c .)
g=0; for d in app/integrations/opal_discover app/integrations/portal_index; do git cat-file -e "$c:$GW/$d" 2>/dev/null && g=$((g+1)); done
[ "$nf" != 0 ] && printf '%s\n' "$foreign" | sed 's/^/  foreign: /'
echo "deployed_commit=$c previous=$p descends=$desc; gateway files shipped $nship, outside NFRA_MCPINDEX's set $nf; new integrations carried $g of 2"
if [ "$desc" = yes ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$g" = 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
