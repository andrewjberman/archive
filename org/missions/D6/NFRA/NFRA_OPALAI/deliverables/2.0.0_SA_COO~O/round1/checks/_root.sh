#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_OPALAI round-1 check: cd to the PARENT worktree root, never the nested opal_ai.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: every check captures `out=$(cmd | tr -d CR); rc=$?` -- without it rc is tr's exit status (always 0),
# so an rc criterion could never read the command's own exit (rows NFRA_OPALAI-Z-W3-S1, -Z-W6-S1).
set -o pipefail
# The commit this round was cut at: the parent-side BEFORE state for content-equality reads.
OA_BASE="0070f8a7ef"
