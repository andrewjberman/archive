#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPINDEX round-14 check: cd to the PARENT worktree root, never a nested repo.
# Round-14 copy of the round-13 battery (pytest_named reads the -rA summary, row Z-W3-S12).
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: every check captures `out=$(cmd | tr -d CR); rc=$?` -- without it rc is tr's exit status (always 0).
set -o pipefail
# Put a path in the form the native (Windows) python accepts.
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }
GW="infra/aws/ec2/opal-gateway"
# Named pytest tests in one gateway test file: pytest_named <file> <test>... -> prints the summary line; returns 0 on PASS.
# Z-W3-S12: under -v, output a test prints through capsys.disabled() lands between `::name` and its verdict, so a
# per-line `::name PASSED` grep misses it. The verdicts are read from pytest's -rA short summary instead, where each
# test's verdict and node id always share one line: `PASSED <file>::<name>` / `FAILED <file>::<name> - ...`.
pytest_named() {
  f="$1"; shift; n=$#
  [ -f "$GW/$f" ] || { echo "$GW/$f absent"; return 1; }
  out=$(cd "$GW" && timeout 300 python -m pytest "$f" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  p=0; for t in "$@"; do printf '%s\n' "$out" | grep -E "^PASSED [^ ]*::$t(\[.*\])?( |$)" >/dev/null && p=$((p+1)); done
  failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
  names=$(printf '%s\n' "$out" | sed -n -E 's/^(FAILED|ERROR) [^ ]*::([^ ]*).*/\2/p' | tr '\n' ' ')
  echo "pytest rc=$rc; named tests passed $p of $n; failed/error tests $failed${names:+ ($names)}"
  [ "$rc" = 0 ] && [ "$p" = "$n" ] && [ "$failed" = 0 ]
}
