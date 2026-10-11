#!/usr/bin/env bash
# AMGT_RESAPP round-90 PREP -- the mass-deletion gate's merge exemption fires in a LINKED worktree.
#
#   bash r90_merge_head.sh [--hook <path to mass-deletion-check.sh>]      (default: .tools/git-hooks/ of the cwd's repo)
#
# `.tools/git-hooks/mass-deletion-check.sh` exempts a merge commit by testing "$ROOT/.git/MERGE_HEAD" (and CHERRY_PICK_HEAD).
# In a LINKED worktree `$ROOT/.git` is a FILE and the merge state lives under <common>/worktrees/<name>/, so the test never
# fires there and a legitimate merge that brings a deletion is gated like a hand-made mass deletion. The fix resolves the
# path with `git rev-parse --git-path MERGE_HEAD` (git's own resolver, the family of nn-4's --git-common-dir).
#
# Built in a THROWAWAY repository under mktemp (no real tree is touched). The hook is run with threshold 2, block mode:
#    B1 a MERGE in a linked worktree whose merged branch deletes 4 files: exit 0 and NO BLOCKED row.
#    B2 control: a NON-merge deletion of 4 files in the SAME linked worktree is still gated: exit 1 and a BLOCKED row.
#    B3 control: the same merge in the MAIN worktree stays exempt: exit 0.
# Verdict: R90 MERGE HEAD: YES|NO (exit 0|1). At the base (2026-10-11) B1 FAILs, B2 and B3 PASS.
set -u
HOOK=""
if [ "${1:-}" = "--hook" ]; then HOOK="${2:-}"; fi
if [ -z "$HOOK" ]; then HOOK="$(git rev-parse --show-toplevel)/.tools/git-hooks/mass-deletion-check.sh"; fi
[ -f "$HOOK" ] || { echo "ERROR: hook not found: $HOOK"; exit 2; }
HOOK="$(cd "$(dirname "$HOOK")" && pwd)/$(basename "$HOOK")"

T="$(mktemp -d "${TMPDIR:-/tmp}/r90_mh_XXXXXX")"
M="$T/main"
mkdir -p "$M" && cd "$M" || exit 2
git init -q . && git config user.name r90 && git config user.email r90@opal.agent
git checkout -q -b trunk 2>/dev/null || true
for i in 1 2 3 4 5; do echo "f$i" > "f$i.txt"; done
git add -A && git commit -q -m seed
git branch -q side && git checkout -q side
git rm -q f1.txt f2.txt f3.txt f4.txt && git commit -q -m "side deletes four"
git checkout -q trunk
git branch -q wtb
git worktree add -q "$T/wt" wtb
( cd "$T/wt" && echo g > g.txt && git add g.txt && git commit -q -m "wtb own commit" )
MSG="$T/msg.txt"; echo "merge probe" > "$MSG"
LOG="org/mass-deletion-audit.log"
PASSED=0; TOTAL=0
say() { TOTAL=$((TOTAL+1)); if [ "$1" = "1" ]; then PASSED=$((PASSED+1)); echo "PASS $2"; else echo "FAIL $2"; fi; }
blocked_rows() { if [ -f "$M/$LOG" ]; then grep -c ' BLOCKED ' "$M/$LOG" || true; else echo 0; fi; }

# B1 -- a merge in the linked worktree.
cd "$T/wt" || exit 2
git merge -q --no-commit --no-ff side >/dev/null 2>&1
MH="$(git rev-parse --git-path MERGE_HEAD)"
IN_MERGE=0; [ -f "$MH" ] && IN_MERGE=1
STAGED_DEL="$(git diff --cached --diff-filter=D --name-only | grep -c . || true)"
MASS_DELETE_THRESHOLD=2 MASS_DELETE_MODE=block bash "$HOOK" "$MSG" >/dev/null 2>&1; RC_MERGE=$?
ROWS_AFTER_B1="$(blocked_rows)"
echo "   linked worktree merge: MERGE_HEAD present=$IN_MERGE staged deletions=$STAGED_DEL hook rc=$RC_MERGE BLOCKED rows=$ROWS_AFTER_B1"
if [ "$IN_MERGE" = "1" ] && [ "$STAGED_DEL" -ge 3 ] && [ "$RC_MERGE" = "0" ] && [ "$ROWS_AFTER_B1" = "0" ]; then
  say 1 "B1 a merge in a linked worktree that brings deletions is exempt: exit 0, no BLOCKED row"
else
  say 0 "B1 a merge in a linked worktree that brings deletions is exempt: exit 0, no BLOCKED row"
fi
git merge --abort >/dev/null 2>&1 || git reset -q --hard >/dev/null 2>&1

# B2 -- control: a non-merge mass deletion in the same linked worktree is still gated.
cd "$T/wt" || exit 2
git rm -q f1.txt f2.txt f3.txt f4.txt
MASS_DELETE_THRESHOLD=2 MASS_DELETE_MODE=block bash "$HOOK" "$MSG" >/dev/null 2>&1; RC_DEL=$?
ROWS_AFTER_B2="$(blocked_rows)"
echo "   linked worktree plain deletion: hook rc=$RC_DEL BLOCKED rows=$ROWS_AFTER_B2"
if [ "$RC_DEL" = "1" ] && [ "$ROWS_AFTER_B2" -gt "$ROWS_AFTER_B1" ]; then
  say 1 "B2 control: a non-merge mass deletion in the linked worktree is still BLOCKED (exit 1, a NEW row written)"
else
  say 0 "B2 control: a non-merge mass deletion in the linked worktree is still BLOCKED (exit 1, a NEW row written)"
fi
git reset -q --hard >/dev/null 2>&1

# B3 -- control: the same merge in the main worktree stays exempt.
cd "$M" || exit 2
git merge -q --no-commit --no-ff side >/dev/null 2>&1
MASS_DELETE_THRESHOLD=2 MASS_DELETE_MODE=block bash "$HOOK" "$MSG" >/dev/null 2>&1; RC_MAIN=$?
echo "   main worktree merge: hook rc=$RC_MAIN"
if [ "$RC_MAIN" = "0" ]; then say 1 "B3 control: a merge in the main worktree stays exempt (exit 0)"
else say 0 "B3 control: a merge in the main worktree stays exempt (exit 0)"; fi

cd "$T/.." 2>/dev/null || cd /
rm -rf "$T"
if [ "$PASSED" = "$TOTAL" ]; then echo "R90 MERGE HEAD: YES ($PASSED of $TOTAL)"; exit 0; fi
echo "R90 MERGE HEAD: NO ($PASSED of $TOTAL)"; exit 1
