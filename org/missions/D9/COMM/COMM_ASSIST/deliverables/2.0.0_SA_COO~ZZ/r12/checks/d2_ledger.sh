#!/usr/bin/env bash
# COMM_ASSIST CA-d-2 AC2 (round 12, NEVER-2): the mail deploy's ledger is committed CLOSED at HEAD with its sentinel gone.
R="$(git rev-parse --show-toplevel)" || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$R" || exit 9
slug=comm-assist-r12-mail-deploy
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
