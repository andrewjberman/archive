#!/usr/bin/env bash
# OPLGTW OG-rl-3 AC3 (NEVER-2 + NARROW, from the committed record): the ledger entry for slug
# nfra-oplgtw-gateway-release-r13 is committed and its sentinel gone; the manifest's deployed_commit descends from
# 3a7d6a7dc8 and ships only the named release files (app/audit.py, app/tools.py, tests/test_audit_bytes_principal.py,
# deploy-to-ec2.sh, deploy/NFRA_OPLGTW_CONTRACT.json, tests/test_schwab_host_inputs.py, and app/taxsma_workbook.py ONLY
# as MDPF_TAXSMA's sha-verified bytes); app/ms_ingest.py unshipped.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
SLUG="nfra-oplgtw-gateway-release-r13"; LIVE0="3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
desc=no; [ "$c" != "$LIVE0" ] && git merge-base --is-ancestor "$LIVE0" "$c" 2>/dev/null && desc=yes
allowed=$(printf '%s\n' app/audit.py app/tools.py tests/test_audit_bytes_principal.py deploy-to-ec2.sh deploy/NFRA_OPLGTW_CONTRACT.json tests/test_schwab_host_inputs.py app/taxsma_workbook.py | sed "s|^|$GW/|" | sort -u)
shipped=$( [ "$desc" = yes ] && git diff --name-only "$LIVE0" "$c" -- "$GW" | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
nf=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
ms=$(printf '%s\n' "$shipped" | grep -c "app/ms_ingest.py$"); tx=$(printf '%s\n' "$shipped" | grep -c "app/taxsma_workbook.py$")
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; deployed=$c descends from 3a7d6a7dc8=$desc; gateway files shipped $nship, outside the release set $nf; ms_ingest.py shipped $ms; taxsma_workbook.py shipped $tx"
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$desc" = yes ] && [ "$nship" -ge 3 ] && [ "$nf" = 0 ] && [ "$ms" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
