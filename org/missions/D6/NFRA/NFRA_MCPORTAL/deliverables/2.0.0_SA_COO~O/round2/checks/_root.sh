#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPORTAL round-2 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: every check captures `out=$(cmd | tr -d CR); rc=$?` -- without it rc is tr's exit status (always 0),
# so an rc criterion could never read the command's own exit (rows NFRA_OPALAI-Z-W3-S1, -Z-W6-S1).
set -o pipefail
# The grant writer's staged build: build_package.py --out <zip> builds the zip and exits 0 (MP-b-1).
MPW_DIR="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
# Put a path in the form the native (Windows) python accepts.
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }
