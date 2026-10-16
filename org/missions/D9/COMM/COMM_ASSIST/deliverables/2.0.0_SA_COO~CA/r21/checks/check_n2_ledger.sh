#!/usr/bin/env bash
# COMM_ASSIST round 21 CA-n-2 AC3 (NEVER-2): the deploy's ledger comm-assist-r21-threads-deploy is committed CLOSED at HEAD and its
# sentinel is gone.
#   bash org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r21/checks/check_n2_ledger.sh
R="$(git rev-parse --show-toplevel)" || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$R" || exit 9
slug=comm-assist-r21-threads-deploy
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
