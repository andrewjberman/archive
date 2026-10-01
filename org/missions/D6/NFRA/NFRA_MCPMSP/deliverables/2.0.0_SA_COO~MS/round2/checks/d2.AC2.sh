#!/usr/bin/env bash
# MS-d-2 AC2 (the NARROW release, from the committed record): EC2_MANIFEST.json at HEAD records an opal-gateway
# deployed_commit that descends from the deployed_commit the manifest held just before that value was set (PREV); whose
# gateway-tree difference from PREV touches ONLY round 2's files; and which carries app/internal_role.py,
# app/sender_gate.py and app/admin_refusals.py.
. "$(dirname "$0")/_root.sh"
M="infra/aws/ec2/EC2_MANIFEST.json"
mf() { git show "$1:$M" 2>/dev/null | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" 2>/dev/null | tr -d '\r'; }
c=$(mf HEAD); prev=""
# PREV = the value just before c was first set: walk the manifest's commits newest first to the first one reading != c
# (robust to a later edit of another service's entry).
for h in $(git log -n 40 --format=%H -- "$M"); do v=$(mf "$h"); [ "$v" != "$c" ] && { prev="$v"; break; }; done
desc=no; [ -n "$prev" ] && git merge-base --is-ancestor "$prev" "$c" 2>/dev/null && desc=yes
allowed=$(printf '%s\n' app/internal_role.py app/query_v0.py app/sender_gate.py app/asker_scope.py app/audit.py app/admin_refusals.py \
  app/admin_api.py deploy-to-ec2.sh tests/test_mcpmsp_internal_role.py tests/test_mcpmsp_sender_gate.py tests/test_admin_refusals.py \
  tests/run_release_suites.sh | sed "s#^#$G/#" | sort -u)
shipped=$(git diff --name-only "$prev" "$c" -- "$G" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
foreign=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed")); nf=$(printf '%s\n' "$foreign" | grep -c .)
g=0; for f in app/internal_role.py app/sender_gate.py app/admin_refusals.py; do git cat-file -e "$c:$G/$f" 2>/dev/null && g=$((g+1)); done
[ "$nf" != 0 ] && printf '%s\n' "$foreign" | sed 's/^/  foreign: /'
echo "deployed_commit=$c prev=$prev descends=$desc; gateway files shipped $nship, outside round 2's set $nf; carries the three new modules $g of 3"
if [ "$desc" = yes ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$g" = 3 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
