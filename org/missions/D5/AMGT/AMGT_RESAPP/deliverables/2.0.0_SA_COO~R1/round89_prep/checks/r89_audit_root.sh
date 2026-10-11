#!/usr/bin/env bash
# AMGT_RESAPP round-89 PREP -- AMGT_RESAPP-S4: the mass-deletion gate's audit row lands in the SHARED tree.
#
#   bash r89_audit_root.sh [--hook <path to mass-deletion-check.sh>]      (default: .tools/git-hooks/ of the cwd's repo)
#
# `.tools/git-hooks/mass-deletion-check.sh` takes ROOT from `git rev-parse --show-toplevel` and `_audit()` appends to
# "$ROOT/$AUDIT_LOG", so a verdict written from a LINKED worktree dies with the worktree. `.tools/safe-commit.sh:177` already
# resolves its audit root through `--git-common-dir`; the gate adopts that for the audit path only.
#
# Built in a THROWAWAY repository under mktemp (no real tree is touched):
#    A1 a mass deletion committed from a linked worktree (warn mode): after the worktree is REMOVED the row is in the MAIN
#       tree's org/mass-deletion-audit.log.
#    A2 the same deletion in block mode: exit 1, and a BLOCKED row in the main tree's log (the verdict is unchanged).
#    A3 control: the same deletion run from the main worktree itself leaves its row in the main tree (unchanged).
# Verdict: R89 AUDIT ROOT: YES|NO (exit 0|1). At the base (2026-10-11) A1 and A2's row check FAIL, A3 PASS.
set -u
HOOK=""
if [ "${1:-}" = "--hook" ]; then HOOK="${2:-}"; fi
if [ -z "$HOOK" ]; then HOOK="$(git rev-parse --show-toplevel)/.tools/git-hooks/mass-deletion-check.sh"; fi
[ -f "$HOOK" ] || { echo "ERROR: hook not found: $HOOK"; exit 2; }
HOOK="$(cd "$(dirname "$HOOK")" && pwd)/$(basename "$HOOK")"

T="$(mktemp -d "${TMPDIR:-/tmp}/r89_audit_XXXXXX")"
M="$T/main"
mkdir -p "$M" && cd "$M" || exit 2
git init -q . && git config user.name r89 && git config user.email r89@opal.agent
for i in 1 2 3 4 5; do echo "f$i" > "f$i.txt"; done
git add -A && git commit -q -m seed
git branch -q wtb
git worktree add -q "$T/wt" wtb
MSG="$T/msg.txt"; echo "mass deletion probe" > "$MSG"
LOG="org/mass-deletion-audit.log"
PASSED=0; TOTAL=0
say() { TOTAL=$((TOTAL+1)); if [ "$1" = "1" ]; then PASSED=$((PASSED+1)); echo "PASS $2"; else echo "FAIL $2"; fi; }

# A1/A2 -- from the linked worktree.
cd "$T/wt" && git rm -q f1.txt f2.txt f3.txt f4.txt
MASS_DELETE_THRESHOLD=2 MASS_DELETE_MODE=warn bash "$HOOK" "$MSG" >/dev/null 2>&1; RC_WARN=$?
MASS_DELETE_THRESHOLD=2 MASS_DELETE_MODE=block bash "$HOOK" "$MSG" >/dev/null 2>&1; RC_BLOCK=$?
cd "$M" && git worktree remove --force "$T/wt"
ROW_WARN=0; ROW_BLOCK=0
[ -f "$M/$LOG" ] && ROW_WARN=$(grep -c ' WARNED ' "$M/$LOG" || true)
[ -f "$M/$LOG" ] && ROW_BLOCK=$(grep -c ' BLOCKED ' "$M/$LOG" || true)
echo "   linked worktree: warn rc=$RC_WARN block rc=$RC_BLOCK | main-tree rows after removal: WARNED=$ROW_WARN BLOCKED=$ROW_BLOCK"
if [ "$RC_WARN" = "0" ] && [ "$ROW_WARN" -ge 1 ]; then say 1 "A1 warn-mode verdict from a linked worktree leaves its row in the shared tree after the worktree is removed"
else say 0 "A1 warn-mode verdict from a linked worktree leaves its row in the shared tree after the worktree is removed"; fi
if [ "$RC_BLOCK" = "1" ] && [ "$ROW_BLOCK" -ge 1 ]; then say 1 "A2 block-mode: exit 1 and a BLOCKED row in the shared tree"
else say 0 "A2 block-mode: exit 1 and a BLOCKED row in the shared tree"; fi

# A3 -- control: the main worktree itself.
cd "$M" && rm -f "$LOG" && git rm -q f1.txt f2.txt f3.txt f4.txt
MASS_DELETE_THRESHOLD=2 MASS_DELETE_MODE=warn bash "$HOOK" "$MSG" >/dev/null 2>&1; RC_MAIN=$?
ROW_MAIN=0; [ -f "$M/$LOG" ] && ROW_MAIN=$(grep -c ' WARNED ' "$M/$LOG" || true)
echo "   main worktree: warn rc=$RC_MAIN rows WARNED=$ROW_MAIN"
if [ "$RC_MAIN" = "0" ] && [ "$ROW_MAIN" -ge 1 ]; then say 1 "A3 control: a deletion from the main worktree leaves its row in the main tree"
else say 0 "A3 control: a deletion from the main worktree leaves its row in the main tree"; fi

cd "$T/.." 2>/dev/null; rm -rf "$T"
if [ "$PASSED" = "$TOTAL" ]; then echo "R89 AUDIT ROOT: YES"; exit 0; fi
echo "R89 AUDIT ROOT: NO"; exit 1
