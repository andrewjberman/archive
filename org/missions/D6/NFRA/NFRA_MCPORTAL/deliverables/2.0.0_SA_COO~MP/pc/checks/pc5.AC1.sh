#!/usr/bin/env bash
# MP-pc-5 AC1 (NEVER-2 + a NARROW release, read at HEAD): the entry for slug nfra-mcportal-pc-release is committed, its
# sentinel is gone and deploy_ledger.py does not list it; services.opal-gateway deployed_commit descends from
# previous_deployed_commit, and the gateway app/tests files that differ between the two are ONLY PC's set
# (admin_fabric_gitstate.py, admin_people.py, admin_api.py and their tests); mcportal_commit's tree holds src/pages/people/
# and its public/routes.json lists /people.
. "$(dirname "$0")/_root.sh"
SLUG="nfra-mcportal-pc-release"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
l=$(timeout 60 python .tools/deploy_ledger.py list 2>&1); listed=$(printf '%s\n' "$l" | grep -c -- "$SLUG"); den=$(printf '%s\n' "$l" | grep -m1 'SCAN DENOMINATOR' || echo "(no denominator)")
read -r DEP PREV MCP < <(python -c "import json;g=json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'];print(g.get('deployed_commit',''),g.get('previous_deployed_commit',''),g.get('mcportal_commit',''))" | tr -d '\r')
desc=no; [ -n "$DEP" ] && [ -n "$PREV" ] && git merge-base --is-ancestor "$PREV" "$DEP" 2>/dev/null && desc=yes
allow='^infra/aws/ec2/opal-gateway/(app/admin_fabric_gitstate\.py|app/admin_people\.py|app/admin_api\.py|tests/test_admin_fabric_gitstate\.py|tests/test_admin_people\.py)$'
files=$(git diff --name-only "$PREV" "$DEP" -- infra/aws/ec2/opal-gateway/app infra/aws/ec2/opal-gateway/tests 2>&1)
n=$(printf '%s\n' "$files" | grep -c . ); out=$(printf '%s\n' "$files" | grep -cvE "$allow")
MC="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/mcportal"
git -C "$MC" rev-parse --git-dir >/dev/null 2>&1 || { echo "mcportal repo unreadable at $MC"; echo "RESULT: FAIL"; exit 1; }
[ -n "$MCP" ] && git -C "$MC" cat-file -e "$MCP^{commit}" 2>/dev/null || { echo "mcportal_commit '$MCP' absent from $MC"; echo "RESULT: FAIL"; exit 1; }
pp=$(git -C "$MC" ls-tree -d --name-only "$MCP" src/pages/people | grep -c people)
rj=$(git -C "$MC" show "$MCP:public/routes.json" 2>/dev/null | python -c "import json,sys;print('yes' if '/people' in json.load(sys.stdin)['paths'] else 'no')" 2>/dev/null | tr -d '\r')
echo "entry files at HEAD=$entry; sentinel=$sent; listed OPEN/HELD=$listed; $den"
echo "deployed=$DEP previous=$PREV descends=$desc; gateway app/tests files changed=$n, outside PC's set=$out; mcportal_commit=$MCP people page=$pp routes.json lists /people=${rj:-no}"
printf '%s\n' "$files" | grep -vE "$allow" | sed 's/^/  OUTSIDE: /'
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR' \
   && [ "$desc" = yes ] && [ "$n" -ge 3 ] && [ "$out" = 0 ] && [ "$pp" = 1 ] && [ "$rj" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
