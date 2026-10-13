#!/usr/bin/env bash
# MP-n-4 AC1 (NEVER-2 + a NARROW release, read at HEAD): the entry for slug nfra-mcportal-c17r2-release is committed, its
# sentinel is gone and deploy_ledger.py does not list it; services.opal-gateway deployed_commit descends from
# previous_deployed_commit, and the gateway app/tests files that differ between the two are ONLY
# app/admin_fabric_gitstate.py and tests/test_admin_fabric_gitstate.py.
. "$(dirname "$0")/../../cp2/checks/_root.sh"
SLUG="nfra-mcportal-c17r2-release"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
l=$(timeout 60 python .tools/deploy_ledger.py list 2>&1); listed=$(printf '%s\n' "$l" | grep -c -- "$SLUG"); den=$(printf '%s\n' "$l" | grep -m1 'SCAN DENOMINATOR' || echo "(no denominator)")
read -r DEP PREV < <(python -c "import json;g=json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'];print(g.get('deployed_commit',''),g.get('previous_deployed_commit',''))" | tr -d '\r')
desc=no; [ -n "$DEP" ] && [ -n "$PREV" ] && git merge-base --is-ancestor "$PREV" "$DEP" 2>/dev/null && desc=yes
allow='^infra/aws/ec2/opal-gateway/(app/admin_fabric_gitstate\.py|tests/test_admin_fabric_gitstate\.py)$'
files=$(git diff --name-only "$PREV" "$DEP" -- infra/aws/ec2/opal-gateway/app infra/aws/ec2/opal-gateway/tests 2>&1)
n=$(printf '%s\n' "$files" | grep -c . ); out=$(printf '%s\n' "$files" | grep -cvE "$allow")
echo "entry files at HEAD=$entry; sentinel=$sent; listed OPEN/HELD=$listed; $den"
echo "deployed=$DEP previous=$PREV descends=$desc; gateway app/tests files changed=$n, outside the C17R2 set=$out"
printf '%s\n' "$files" | grep -vE "$allow" | sed 's/^/  OUTSIDE: /'
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR' \
   && [ "$desc" = yes ] && [ "$n" -ge 1 ] && [ "$out" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
