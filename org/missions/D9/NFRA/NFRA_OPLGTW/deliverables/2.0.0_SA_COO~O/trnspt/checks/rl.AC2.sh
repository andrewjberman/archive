#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-rl-1 AC2 (NEVER-2 + NARROW, from the committed record): the ledger entry for slug
# nfra-oplgtw-trnspt-deps-release is committed and its sentinel gone; the manifest's opal-gateway deployed_commit ships
# only gateway files that the TRNSPT-DEPS build slots (~15, ~16) changed, plus deploy-to-ec2.sh; /ms/* is unchanged.
. "$(dirname "$0")/_root.sh"
SLUG="nfra-oplgtw-trnspt-deps-release"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('previous_deployed_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); p=$(printf '%s\n' "$out" | sed -n 2p)
allowed=$( { for a in "0.9.0_WK_NFRA_OPLGTW~15" "0.9.0_WK_NFRA_OPLGTW~16"; do git log --format=%H --author="$a <" HEAD -- "$GW"; done \
  | while read h; do git show --name-only --format= "$h" -- "$GW"; done; echo "$GW/deploy-to-ec2.sh"; } | grep . | sort -u)
shipped=$( [ "$p" != NONE ] && git diff --name-only "$p" "$c" -- "$GW" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
nf=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
ms=$(printf '%s\n' "$shipped" | grep -c "app/ms_ingest.py$")
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; deployed=$c previous=$p; gateway files shipped $nship, outside the build slots' set $nf; ms_ingest.py shipped $ms"
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$ms" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
