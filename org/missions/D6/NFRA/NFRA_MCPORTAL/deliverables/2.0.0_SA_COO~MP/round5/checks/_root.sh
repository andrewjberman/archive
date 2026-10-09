#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPORTAL round-5 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
set -o pipefail
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
# ssm_run <params.json> -> sets $SSM_ST (status) and $SSM_OUT (stdout). One command, polled up to ~60 s.
ssm_run() {
  local cid st i
  cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$1")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
  st=""; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
  SSM_ST="${st:-NONE}"; SSM_CID="${cid:-NONE}"
  SSM_OUT=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
}
