#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_OPALAI round-2 check: cd to the PARENT worktree root, never the nested opal_ai.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: a check capturing `out=$(cmd | tr -d CR); rc=$?` must read the command's own exit, not tr's.
set -o pipefail
# Round 1's cut: the parent-side BEFORE state for content-equality reads (OA-t-1 / OA-t-3 re-cut, unchanged).
OA_BASE="0070f8a7ef"
# Round 2's cut: the parent HEAD this issuance was cut at.
OA_R2_BASE="c8df03c408"
# opal_ai origin PROD at round 2's cut = the drain commit of round 1's nested move (OA-t-1 99190d1, OA-t-3 fd8ab8a).
# A re-cut check that asserts the MOVE reads the nested repo HERE, never at the nested HEAD, because round 2's E2 and
# E7 edit two moved files after the move by design (decomposition R2.3).
OA_NESTED_PIN="fd8ab8a57f"
AWS="$(pwd)/.tools/aws"
GW_INSTANCE="i-07dccb1615503ac99"
