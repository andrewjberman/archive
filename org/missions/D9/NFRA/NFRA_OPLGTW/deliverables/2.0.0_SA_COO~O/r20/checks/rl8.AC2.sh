#!/usr/bin/env bash
# OPLGTW OG-rl-8 AC2 (NEVER-2 + DRAIN-BACK + FLOOR): the ledger entry for nfra-oplgtw-gateway-release-r20 is committed
# and its sentinel gone; the manifest's deployed_commit descends from cf4b036e62; after the drain-back CLOUD equals live
# for the gateway tree (R16); the floor holds -- rl4.AC1 (51-name baseline) and ht.AC2 (51 keys).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
SLUG="nfra-oplgtw-gateway-release-r20"; LIVE0="cf4b036e62b5074600086e1d670dc3c6bdab004f"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
desc=no; [ "$c" != "$LIVE0" ] && git merge-base --is-ancestor "$LIVE0" "$c" 2>/dev/null && desc=yes
ndiff=$(git diff --name-only "$c" HEAD -- "$GW" | grep -c .)
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; deployed=${c:0:10} descends from cf4b036e62=$desc; gateway files differing live..CLOUD after drain-back $ndiff"
f1=no; RL4_ENV_KEYS_BASELINE="$D/r17/ENV_KEYS_R17B.txt" bash "$D/r14/checks/rl4.AC1.sh" >/dev/null 2>&1 && f1=yes
f2=no; HT_ENV_KEYS_COUNT=51 bash "$D/hxteams/checks/ht.AC2.sh" >/dev/null 2>&1 && f2=yes
echo "floor: rl4.AC1 $f1; ht.AC2 $f2"
[ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$desc" = yes ] && [ "$ndiff" = 0 ] && [ "$f1" = yes ] && [ "$f2" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
