#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPORTAL round-4 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: `out=$(cmd | tr -d CR); rc=$?` must read the command's own exit (rows NFRA_OPALAI-Z-W3-S1, -Z-W6-S1).
set -o pipefail
GW="infra/aws/ec2/opal-gateway"
