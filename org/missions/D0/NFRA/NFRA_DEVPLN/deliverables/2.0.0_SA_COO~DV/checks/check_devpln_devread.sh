#!/usr/bin/env bash
# org/missions/D0/NFRA/NFRA_DEVPLN/deliverables/2.0.0_SA_COO~DV/checks/check_devpln_devread.sh -- NFRA_DEVPLN cell DP-c-1 independent denominator
# (issuer-authored; the worker only runs it). Runs the read, then compares its counts with git read directly.
# Usage: check_devpln_devread.sh <portal-repo-path>   (run from the workspace or worktree root)
# Last line: DEVREAD-COUNTS-MATCH t=<n> a=<a> u=<u>   |   DEVREAD-COUNTS-MISMATCH ...
set -u
REPO="${1:-portal}"
OUT="$(python .tools/portal-dev-approval-read.py --portal "$REPO" 2>&1)" || { echo "DEVREAD-COUNTS-MISMATCH tool-rc-nonzero"; exit 1; }
LAST="$(printf '%s\n' "$OUT" | tail -1)"
t="$(printf '%s' "$LAST" | grep -o -E 'first_parent_commits=[0-9]+' | cut -d= -f2)"
a="$(printf '%s' "$LAST" | grep -o -E ' approved=[0-9]+' | cut -d= -f2)"
u="$(printf '%s' "$LAST" | grep -o -E ' unapproved=[0-9]+' | cut -d= -f2)"
since="$(printf '%s' "$LAST" | grep -o -E 'since=[0-9a-f]+' | cut -d= -f2)"
ref="$(printf '%s' "$LAST" | grep -o -E 'ref=[^ ]+' | cut -d= -f2)"
if [ -z "$t" ] || [ -z "$a" ] || [ -z "$u" ] || [ -z "$since" ] || [ -z "$ref" ]; then
  echo "DEVREAD-COUNTS-MISMATCH unparsed-last-line:$LAST"; exit 1
fi
g="$(git -C "$REPO" rev-list --first-parent --count "$since..$ref" 2>&1)" || { echo "DEVREAD-COUNTS-MISMATCH git-unreadable:$g"; exit 1; }
lines="$(printf '%s\n' "$OUT" | grep -c '^DEV-COMMIT ')"
if [ "$t" = "$g" ] && [ "$((a + u))" = "$t" ] && [ "$lines" = "$t" ]; then
  echo "DEVREAD-COUNTS-MATCH t=$t a=$a u=$u"; exit 0
fi
echo "DEVREAD-COUNTS-MISMATCH tool_t=$t git_t=$g a=$a u=$u commit_lines=$lines"; exit 1
