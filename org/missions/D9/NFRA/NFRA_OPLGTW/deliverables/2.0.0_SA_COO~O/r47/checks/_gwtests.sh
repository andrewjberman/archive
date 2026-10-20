#!/usr/bin/env bash
# _gwtests.sh -- sourced by the round-47 test criteria. gwtests <new-test-file> <neighbour-test-file>...
# Runs the worker's NEW test file and its neighbours (existing tests that import the touched modules) in the gateway folder under `python3 -I -m pytest`.
# Passes when the new file exists and passes 100 percent, every neighbour passes, except the one carried red: test_ogz1_ac08 (a route-set pin that already
# fails at the live ref). Prints: new file: N passed, F failed; neighbours: N passed, failed names [..].
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
gwtests() (
  newf="$1"; shift
  cd "$GW" || { echo "ERROR: gateway folder absent"; return 9; }
  if [ ! -f "$newf" ]; then echo "new test file $newf: absent"; echo "RESULT: FAIL"; return 1; fi
  nout=$(timeout 200 python3 -I -m pytest "$newf" -q -rf --color=no -p no:cacheprovider 2>&1 | tr -d '\r')
  np=$(printf '%s\n' "$nout" | grep -oE '[0-9]+ passed' | tail -1 | grep -oE '[0-9]+'); nf=$(printf '%s\n' "$nout" | grep -oE '[0-9]+ (failed|error)' | tail -1 | grep -oE '[0-9]+')
  echo "new file $newf: ${np:-0} passed, ${nf:-0} failed"
  fail=""; pass=0
  if [ "$#" -gt 0 ]; then
    out=$(timeout 280 python3 -I -m pytest "$@" -q -rf --color=no -p no:cacheprovider 2>&1 | tr -d '\r')
    pass=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | tail -1 | grep -oE '[0-9]+')
    fail=$(printf '%s\n' "$out" | grep -E '^(FAILED|ERROR) ' | sed -E 's/^(FAILED|ERROR) [^:]*::([A-Za-z0-9_]+).*/\2/' | sort -u | grep -v '^test_ogz1_ac08$' | paste -sd, -)
  fi
  echo "neighbours ($#): ${pass:-0} passed, failed names [${fail}] (allowed: test_ogz1_ac08 only)"
  if [ -n "$np" ] && [ "${np:-0}" -ge 1 ] && [ "${nf:-0}" = 0 ] && [ -z "$fail" ]; then echo "RESULT: PASS"; return 0; fi
  echo "RESULT: FAIL"; return 1
)
