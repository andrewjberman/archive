#!/usr/bin/env bash
# MP-x-4 AC2 (the release is NARROW, read from the manifest at HEAD): services.opal-gateway deployed_commit descends from
# previous_deployed_commit; the gateway files that differ between the two are ONLY MP-x-1's three app files (and its test,
# which never ships but may ride the release branch); mcportal_commit is d60b4e0 or a descendant of it in the mcportal repo.
. "$(dirname "$0")/_root.sh"
read -r DEP PREV MCP < <(python -c "import json;g=json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'];print(g.get('deployed_commit',''),g.get('previous_deployed_commit',''),g.get('mcportal_commit',''))" | tr -d '\r')
desc=no; [ -n "$DEP" ] && [ -n "$PREV" ] && git merge-base --is-ancestor "$PREV" "$DEP" 2>/dev/null && desc=yes
allow='^infra/aws/ec2/opal-gateway/(app/admin_fabric\.py|app/admin_api\.py|app/refs/fabric_boxes\.json|tests/test_admin_fabric\.py)$'
files=$(git diff --name-only "$PREV" "$DEP" -- infra/aws/ec2/opal-gateway/app infra/aws/ec2/opal-gateway/tests 2>&1)
n=$(printf '%s\n' "$files" | grep -c . ); out=$(printf '%s\n' "$files" | grep -cvE "$allow")
# Row Z-S28: resolve the mcportal repo from the MAIN worktree (a linked worktree has no nested checkout), and fail LOUD
# when it is unreadable or lacks the commit, never as a silent "no".
MC="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/mcportal"
git -C "$MC" rev-parse --git-dir >/dev/null 2>&1 || { echo "mcportal repo unreadable at $MC"; echo "RESULT: FAIL"; exit 1; }
[ -z "$MCP" ] || git -C "$MC" cat-file -e "$MCP^{commit}" 2>/dev/null || { echo "mcportal_commit $MCP absent from $MC"; echo "RESULT: FAIL"; exit 1; }
mok=no; [ -n "$MCP" ] && git -C "$MC" merge-base --is-ancestor d60b4e0 "$MCP" && mok=yes
echo "deployed=$DEP previous=$PREV descends=$desc; gateway app/tests files changed=$n, outside MP-x-1's set=$out; mcportal_commit=$MCP contains d60b4e0=$mok"
printf '%s\n' "$files" | grep -vE "$allow" | sed 's/^/  OUTSIDE: /'
if [ "$desc" = yes ] && [ "$n" -ge 2 ] && [ "$out" = 0 ] && [ "$mok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
