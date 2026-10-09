#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPORTAL workstream-CP2 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: `out=$(cmd | tr -d CR); rc=$?` must read the command's own exit (rows NFRA_OPALAI-Z-W3-S1, -Z-W6-S1).
set -o pipefail
GW="infra/aws/ec2/opal-gateway"
CAP="org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/fixtures/s3_capture_20261009T0728Z.json"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99

# named_pytest <label> <test file under $GW> <name>... -- runs the file once; PASS needs 0 failed and every name PASSED.
named_pytest() {
  local label="$1" tf="$2"; shift 2
  local want=$# n=0 t out tail failed
  [ -f "$GW/$tf" ] || { echo "$GW/$tf absent"; echo "RESULT: FAIL"; exit 1; }
  out=$(cd "$GW" && timeout 110 python -m pytest "$tf" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
  for t in "$@"; do printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
  tail=$(printf '%s\n' "$out" | tail -1)
  failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
  echo "$label: $tail; named tests PASSED $n of $want"
  if [ "$n" = "$want" ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
  echo "RESULT: FAIL"; exit 1
}

# ssm_run <params.json> -> sets $SSM_ST (status) and $SSM_OUT (stdout). One command, polled up to ~60 s.
ssm_run() {
  local cid st i
  cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$1")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
  st=""; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
  SSM_ST="${st:-NONE}"; SSM_CID="${cid:-NONE}"
  SSM_OUT=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
}
