#!/usr/bin/env bash
# OA-e-3 AC1 (NEVER-2 on the WORLD act): the change-management entry for slug nfra-opalai-r2-asker-switch-on-gateway is COMMITTED at HEAD, its
# .open_deploys sentinel is gone at HEAD, and deploy_ledger.py's OPEN/HELD scan does not list it.
. "$(dirname "$0")/_root.sh"
SLUG="nfra-opalai-r2-asker-switch-on-gateway"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
lst=$(timeout 60 python .tools/deploy_ledger.py list 2>&1 | tr -d '\r')
listed=$(printf '%s\n' "$lst" | grep -c -- "$SLUG")
den=$(grep -m1 'SCAN DENOMINATOR' <<< "$lst"); [ -n "$den" ] || den="(no denominator line)"
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; listed OPEN/HELD=$listed; $den"
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
