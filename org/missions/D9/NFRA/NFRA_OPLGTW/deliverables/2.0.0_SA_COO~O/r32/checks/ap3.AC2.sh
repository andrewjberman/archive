#!/usr/bin/env bash
# OPLGTW OG-ap-3 AC2 (r29 apply, NEVER-2): both ledgers of the act are committed CLOSED at HEAD with their sentinels gone --
# nfra-oplgtw-r29-commassist-secret-grant (the secret + the one policy line) and nfra-oplgtw-gateway-release-r29 (the
# gateway deploy).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
ok=1
for slug in nfra-oplgtw-r29-commassist-secret-grant nfra-oplgtw-gateway-release-r29; do
  entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
  sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
  echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
  [ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] || ok=0
done
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
