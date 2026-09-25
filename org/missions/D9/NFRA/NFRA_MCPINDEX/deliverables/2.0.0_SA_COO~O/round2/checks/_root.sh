#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPINDEX round-2 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: every check captures `out=$(cmd | tr -d CR); rc=$?` -- without it rc is tr's exit status (always 0),
# so an rc criterion could never read the command's own exit (rows NFRA_OPALAI-Z-W3-S1, -Z-W6-S1).
set -o pipefail
# Put a path in the form the native (Windows) python accepts.
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }
GW="infra/aws/ec2/opal-gateway"
# Named pytest tests in one gateway test file: pytest_named <file> <test>... -> prints the summary line; returns 0 on PASS.
pytest_named() {
  f="$1"; shift; n=$#
  [ -f "$GW/$f" ] || { echo "$GW/$f absent"; return 1; }
  out=$(cd "$GW" && timeout 110 python -m pytest "$f" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  p=0; for t in "$@"; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
  failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
  echo "pytest rc=$rc; named tests passed $p of $n; failed/error lines $failed"
  [ "$rc" = 0 ] && [ "$p" = "$n" ] && [ "$failed" = 0 ]
}
