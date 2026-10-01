#!/usr/bin/env bash
# OPLGTW OG-tr-1 AC2 (NEVER-2 + NARROW, from the committed record): the ledger entry for slug
# nfra-oplgtw-taxsma-route-release is committed and its sentinel gone; the manifest's opal-gateway deployed_commit ships
# ONLY the Tax route files (app/taxsma_workbook.py, app/server.py, app/config.py, tests/test_taxsma_workbook.py) plus
# deploy-to-ec2.sh; /ms_ingest.py unshipped.
. "$(dirname "$0")/_root.sh"
SLUG="nfra-oplgtw-taxsma-route-release"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('previous_deployed_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); p=$(printf '%s\n' "$out" | sed -n 2p)
allowed=$(printf '%s\n' "$GW/app/taxsma_workbook.py" "$GW/app/server.py" "$GW/app/config.py" "$GW/tests/test_taxsma_workbook.py" "$GW/deploy-to-ec2.sh" | sort -u)
shipped=$( [ "$p" != NONE ] && git diff --name-only "$p" "$c" -- "$GW" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
nf=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
ms=$(printf '%s\n' "$shipped" | grep -c "app/ms_ingest.py$")
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; deployed=$c previous=$p; gateway files shipped $nship, outside the Tax set $nf; ms_ingest.py shipped $ms"
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$ms" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
