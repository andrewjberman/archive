#!/usr/bin/env bash
# MP-pf-9 AC1 (a BUNDLE-ONLY release, read at HEAD; CTO msg 34980 (b), row Z-S64): the entry for slug nfra-mcportal-pf-bundle-release is committed, its sentinel is gone and deploy_ledger.py does not list it OPEN or HELD;
# EC2_MANIFEST services.opal-gateway mcportal_commit is c66ca82952c01575968d16cc736cdabe36606572 and descends from 090b9cdc85 (read in the mcportal repo); deployed_commit differs from previous_deployed_commit; and NO gateway file
# differs between the two (git diff --name-only previous deployed -- infra/aws/ec2/opal-gateway is EMPTY: the release moved the bundle and nothing else).
. "$(dirname "$0")/../../pc/checks/_root.sh"
SLUG="nfra-mcportal-pf-bundle-release"; WANT=c66ca82952c01575968d16cc736cdabe36606572
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
l=$(timeout 60 python .tools/deploy_ledger.py list 2>&1); listed=$(printf '%s\n' "$l" | grep -c -- "$SLUG"); den=$(printf '%s\n' "$l" | grep -m1 'SCAN DENOMINATOR' || echo "(no denominator)")
read -r DEP PREV MCP < <(python -c "import json;g=json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'];print(g.get('deployed_commit',''),g.get('previous_deployed_commit',''),g.get('mcportal_commit',''))" | tr -d '\r')
MC="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/mcportal"
git -C "$MC" rev-parse --git-dir >/dev/null 2>&1 || { echo "mcportal repo unreadable at $MC"; echo "RESULT: FAIL"; exit 1; }
pin=no; [ "$MCP" = "$WANT" ] && pin=yes
desc=no; [ -n "$MCP" ] && git -C "$MC" merge-base --is-ancestor 090b9cdc85 "$MCP" 2>/dev/null && desc=yes
diffd=no; [ -n "$DEP" ] && [ -n "$PREV" ] && [ "$DEP" != "$PREV" ] && diffd=yes
n=-1; [ "$diffd" = yes ] && n=$(git diff --name-only "$PREV" "$DEP" -- infra/aws/ec2/opal-gateway 2>/dev/null | grep -c .)
echo "entry files at HEAD=$entry; sentinel=$sent; listed OPEN/HELD=$listed; $den"
echo "mcportal_commit=${MCP:0:12} is c66ca82952: $pin; descends from 090b9cdc85: $desc; deployed=${DEP:0:12} previous=${PREV:0:12} differ: $diffd; gateway files changed between them=$n"
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR' && [ "$pin" = yes ] && [ "$desc" = yes ] && [ "$diffd" = yes ] && [ "$n" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
