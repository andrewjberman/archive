#!/usr/bin/env bash
# OPLGTW OG-rl-5 AC2 (NEVER-2 + NARROW + FLOOR): the ledger entry for nfra-oplgtw-gateway-release-r16 is committed and its
# sentinel gone; the manifest's deployed_commit descends from af2d762970 and ships ONLY query.py, datasets.json and
# tests/test_schwab_grain_r9.py; and the regression floor holds -- rl4.AC1 (the .env shape) and ht.AC2 (/hx/teams served).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
SLUG="nfra-oplgtw-gateway-release-r16"; LIVE0="af2d7629702528c050860314a7867d8ea0cecfbf"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
desc=no; [ "$c" != "$LIVE0" ] && git merge-base --is-ancestor "$LIVE0" "$c" 2>/dev/null && desc=yes
S="$GW/app/integrations/schwab"
allowed=$(printf '%s\n' "$S/query.py" "$S/datasets.json" "$GW/tests/test_schwab_grain_r9.py" | sort -u)
shipped=$( [ "$desc" = yes ] && git diff --name-only "$LIVE0" "$c" -- "$GW" | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
nf=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; deployed=${c:0:10} descends from af2d762970=$desc; gateway files shipped $nship, outside the release set $nf"
f1=no; bash "$D/r14/checks/rl4.AC1.sh" >/dev/null 2>&1 && f1=yes
f2=no; bash "$D/hxteams/checks/ht.AC2.sh" >/dev/null 2>&1 && f2=yes
echo "floor: rl4.AC1 $f1; ht.AC2 $f2"
[ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$desc" = yes ] && [ "$nship" -ge 2 ] && [ "$nf" = 0 ] && [ "$f1" = yes ] && [ "$f2" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
