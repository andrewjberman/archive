#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPORTAL workstream-PC round-2 check (decomposition v10): the round-1 helpers
# (cd to the PARENT worktree root, named_pytest for the gateway tests, ssm_run) plus the Lambda and tools helpers.
. "$(dirname "$0")/../../pc/checks/_root.sh"
LAM="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
PDD="org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables"

# named_pytest_in <label> <dir from the root> <test file under that dir> <name>...
# PASS needs 0 failed/error in the run's last line and every named test PASSED. The tail line is printed.
named_pytest_in() {
  local label="$1" dir="$2" tf="$3"; shift 3
  local want=$# n=0 t out tail failed
  [ -f "$dir/$tf" ] || { echo "$dir/$tf absent"; echo "RESULT: FAIL"; exit 1; }
  out=$(cd "$dir" && timeout 115 python -m pytest "$tf" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
  for t in "$@"; do printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
  tail=$(printf '%s\n' "$out" | tail -1)
  failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
  echo "$label: $tail; named tests PASSED $n of $want"
  if [ "$n" = "$want" ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
  echo "RESULT: FAIL"; exit 1
}
