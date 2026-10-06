#!/usr/bin/env bash
# OPLGTW OG-ga-1 AC3 (LEDGER): the change-management entry for nfra-oplgtw-ga1-grant-write is committed and its sentinel gone.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
SLUG="nfra-oplgtw-ga1-grant-write"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent"
[ "$entry" -ge 1 ] && [ "$sent" = no ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
