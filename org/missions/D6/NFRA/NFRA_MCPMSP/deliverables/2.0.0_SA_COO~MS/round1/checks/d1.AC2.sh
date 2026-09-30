#!/usr/bin/env bash
# MS-d-1 AC2 (the NARROW release, read from the committed record): EC2_MANIFEST.json at HEAD records an opal-gateway
# deployed_commit that descends from the deployed_commit the manifest held just before its last change (PREV); whose
# gateway-tree difference from PREV touches ONLY NFRA_MCPMSP's files (MS-t-1's and MS-t-5's written files plus the
# app/admin_api.py hookup and MS-d-1's own deploy-to-ec2.sh .env line); and which carries app/tenant_registry.py, app/firm_role.py and app/admin_tenants.py.
. "$(dirname "$0")/_root.sh"
M="infra/aws/ec2/EC2_MANIFEST.json"
mf() { git show "$1:$M" 2>/dev/null | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" 2>/dev/null | tr -d '\r'; }
last=$(git log -n1 --format=%H -- "$M")
c=$(mf HEAD); prev=$(mf "${last}^")
desc=no; [ -n "$prev" ] && git merge-base --is-ancestor "$prev" "$c" 2>/dev/null && desc=yes
allowed=$(printf '%s\n' "$G/app/tenant_registry.py" "$G/app/firm_role.py" "$G/app/asker_scope.py" "$G/app/audit.py" "$G/app/config.py" \
  "$G/tests/test_mcpmsp_asker_firm.py" "$G/app/admin_tenants.py" "$G/tests/test_admin_tenants.py" "$G/app/admin_api.py" \
  "$G/deploy-to-ec2.sh" | sort -u)
shipped=$(git diff --name-only "$prev" "$c" -- "$G" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
foreign=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed"))
nf=$(printf '%s\n' "$foreign" | grep -c .)
g=0; for f in app/tenant_registry.py app/firm_role.py app/admin_tenants.py; do git cat-file -e "$c:$G/$f" 2>/dev/null && g=$((g+1)); done
[ "$nf" != 0 ] && printf '%s\n' "$foreign" | sed 's/^/  foreign: /'
echo "deployed_commit=$c prev=$prev descends=$desc; gateway files shipped $nship, outside NFRA_MCPMSP's set $nf; carries the three new modules $g of 3"
if [ "$desc" = yes ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$g" = 3 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
