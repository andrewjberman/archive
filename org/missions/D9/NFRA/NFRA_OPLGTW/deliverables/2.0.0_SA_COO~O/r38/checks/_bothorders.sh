#!/usr/bin/env bash
# OPLGTW generic both-orders check (round 41): the named gateway test files pass together, forward and reversed, with the same count.
# Usage: _bothorders.sh <label> <test file under infra/aws/ec2/opal-gateway/>...   (at least two files)
# Prints "<label> forward: passed N; failed F" and "<label> reverse: passed M; failed G" and RESULT: PASS only if F=G=0, N>=1 and N=M.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
label="$1"; shift
[ -n "$label" ] && [ "$#" -ge 2 ] || { echo "usage: _bothorders.sh <label> <file> <file>..."; echo "RESULT: FAIL"; exit 2; }
GW=infra/aws/ec2/opal-gateway
run() {
  ( cd "$GW" && timeout 280 python -m pytest -q -p no:cacheprovider "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | tail -1 )
}
fwd_args=("$@"); rev_args=(); for ((i=$#; i>=1; i--)); do rev_args+=("${!i}"); done
fwd=$(run "${fwd_args[@]}"); rev=$(run "${rev_args[@]}")
pf=$(printf '%s' "$fwd" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); ff=$(printf '%s' "$fwd" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
pr=$(printf '%s' "$rev" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); fr=$(printf '%s' "$rev" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
echo "${label} forward: passed ${pf:-0}; failed ${ff:-0}"
echo "${label} reverse: passed ${pr:-0}; failed ${fr:-0}"
restore_audit
[ "${ff:-0}" = 0 ] && [ "${fr:-0}" = 0 ] && [ "${pf:-0}" -ge 1 ] && [ "${pr:-0}" -ge 1 ] && [ "${pf:-0}" = "${pr:-0}" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
