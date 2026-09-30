#!/usr/bin/env bash
# MP-a-2 AC1 (NEVER-2): the deploy's entry for slug nfra-mcportal-r3-writer-apply is COMMITTED at HEAD, its sentinel is
# gone, and deploy_ledger.py's OPEN/HELD scan does not list it.
. "$(dirname "$0")/_root.sh"
SLUG="nfra-mcportal-r3-writer-apply"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
l=$(timeout 60 python .tools/deploy_ledger.py list 2>&1); listed=$(printf '%s\n' "$l" | grep -c -- "$SLUG"); den=$(printf '%s\n' "$l" | grep -m1 'SCAN DENOMINATOR' || echo "(no denominator)")
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; listed OPEN/HELD=$listed; $den"
if [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
