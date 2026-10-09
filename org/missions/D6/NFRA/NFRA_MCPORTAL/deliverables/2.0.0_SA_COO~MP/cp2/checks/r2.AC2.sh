#!/usr/bin/env bash
# MP-r-2 AC2 (the release is NARROW, read from the manifest at HEAD): services.opal-gateway deployed_commit descends from
# previous_deployed_commit; the gateway app/tests files that differ between the two are ONLY CP2's set (the three handler
# modules, the rule file, admin_api.py's route lines, the three tests); mcportal_commit contains d60b4e0 (MP-x-2) and its
# tree holds src/pages/open-calls/ (MP-p-2).
. "$(dirname "$0")/_root.sh"
read -r DEP PREV MCP < <(python -c "import json;g=json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'];print(g.get('deployed_commit',''),g.get('previous_deployed_commit',''),g.get('mcportal_commit',''))" | tr -d '\r')
desc=no; [ -n "$DEP" ] && [ -n "$PREV" ] && git merge-base --is-ancestor "$PREV" "$DEP" 2>/dev/null && desc=yes
allow='^infra/aws/ec2/opal-gateway/(app/admin_fabric_(overlap|gitstate|calls)\.py|app/admin_api\.py|app/refs/overlap_rules\.json|tests/test_admin_fabric_(overlap|gitstate|calls)\.py)$'
files=$(git diff --name-only "$PREV" "$DEP" -- infra/aws/ec2/opal-gateway/app infra/aws/ec2/opal-gateway/tests 2>&1)
n=$(printf '%s\n' "$files" | grep -c . ); out=$(printf '%s\n' "$files" | grep -cvE "$allow")
mok=no; [ -n "$MCP" ] && git -C mcportal merge-base --is-ancestor d60b4e0 "$MCP" 2>/dev/null && mok=yes
oc=0; [ -n "$MCP" ] && oc=$(git -C mcportal ls-tree -d --name-only "$MCP" src/pages/open-calls 2>/dev/null | grep -c open-calls)
echo "deployed=$DEP previous=$PREV descends=$desc; gateway app/tests files changed=$n, outside CP2's set=$out; mcportal_commit=$MCP contains d60b4e0=$mok, has src/pages/open-calls=$oc"
printf '%s\n' "$files" | grep -vE "$allow" | sed 's/^/  OUTSIDE: /'
if [ "$desc" = yes ] && [ "$n" -ge 4 ] && [ "$out" = 0 ] && [ "$mok" = yes ] && [ "$oc" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
