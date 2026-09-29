#!/usr/bin/env bash
# OPLGTW OG-t-2 AC2 (the NARROW release, read from the committed record): EC2_MANIFEST.json at HEAD records an opal-gateway
# deployed_commit that DESCENDS from its previous_deployed_commit; whose gateway-tree difference touches ONLY files
# the round-2 build cells' commits changed (authors = $OG_T2_AUTHORS, default the build slot ~12);
# and whose app/tier.py reads no email roster (MASTER_ADMIN_EMAILS absent).
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('previous_deployed_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); p=$(printf '%s\n' "$out" | sed -n 2p)
desc=no; [ "$p" != NONE ] && git merge-base --is-ancestor "$p" "$c" 2>/dev/null && desc=yes
OG_T2_AUTHORS="${OG_T2_AUTHORS:-0.9.0_WK_NFRA_OPLGTW~12}"   # the build slot: OG-t-1, OG-u-1, OG-u-2
allowed=$(for a in $OG_T2_AUTHORS; do git log --format=%H --author="$a <" HEAD -- "$GW"; done | while read h; do git show --name-only --format= "$h" -- "$GW"; done | sort -u)
shipped=$( [ "$p" != NONE ] && git diff --name-only "$p" "$c" -- "$GW" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
foreign=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed" | grep .)); nf=$(printf '%s\n' "$foreign" | grep -c .)
g=$(git show "$c:$GW/app/tier.py" 2>/dev/null | grep -c "MASTER_ADMIN_EMAILS"); t=$(git show "$c:$GW/app/tier.py" 2>/dev/null | grep -c .)
[ "$nf" != 0 ] && printf '%s\n' "$foreign" | sed 's/^/  foreign: /'
echo "deployed_commit=$c previous=$p descends=$desc; gateway files shipped $nship, outside the build cells' set $nf; tier.py lines $t, email roster reads $g"
if [ "$desc" = yes ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "${t:-0}" -ge 1 ] && [ "$g" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
