#!/usr/bin/env bash
# COMM_ASSIST CA-d-2 AC2 (round 12, NEVER-2): every ledger of the mail deploy is committed CLOSED at HEAD with its sentinel gone.
# Two slugs: comm-assist-r12-mail-deploy (the first Phase B, closed not-applied on Branch B, row Z-S3) and
# comm-assist-r12-mail-deploy-2 (the re-issued Phase B on the pinned build). Checking only the first would PASS while the second,
# the live act, is still open -- so BOTH are required (issuer fix, 2026-10-09 ~18:1xZ).
R="$(git rev-parse --show-toplevel)" || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$R" || exit 9
ok=1
for slug in comm-assist-r12-mail-deploy comm-assist-r12-mail-deploy-2; do
  entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
  sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
  echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
  [ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] || ok=0
done
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
