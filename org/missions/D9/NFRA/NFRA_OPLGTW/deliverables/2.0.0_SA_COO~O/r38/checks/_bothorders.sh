#!/usr/bin/env bash
# OPLGTW generic both-orders check (round 41): the named gateway test files pass together, forward and reversed, with the same count.
# Usage: _bothorders.sh <label> <test file under infra/aws/ec2/opal-gateway/>...   (at least two files)
# Prints "<label> forward: passed N; failed F" and "<label> reverse: passed M; failed G" and RESULT: PASS only if F=G=0, N>=1 and N=M.
# Round 44 (OG-en-33, row Z-S399): env BOTHORDERS_PYTEST is the runner (default "python -m pytest -q -p no:cacheprovider"), called unquoted so a multi-word runner works;
#   env BOTHORDERS_OUT receives <label>.forward.txt and <label>.reverse.txt = the FULL runner output of each order (colour codes and CR stripped; default a fresh mktemp dir).
#   An order whose last line carries no "N passed" prints "<label> <order>: NO PASS LINE; saved <path>" and the last 15 lines of that file, and the verdict is FAIL.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
label="$1"; shift
[ -n "$label" ] && [ "$#" -ge 2 ] || { echo "usage: _bothorders.sh <label> <file> <file>..."; echo "RESULT: FAIL"; exit 2; }
GW=infra/aws/ec2/opal-gateway
BOTHORDERS_PYTEST="${BOTHORDERS_PYTEST:-python -m pytest -q -p no:cacheprovider}"
OUT="${BOTHORDERS_OUT:-$(mktemp -d)}"; mkdir -p "$OUT"
# run <order> <file>...: the full text goes to $OUT/<label>.<order>.txt; prints its last line (the N passed / N failed parse reads that line).
run() {
  local order="$1"; shift; local f="$OUT/${label}.${order}.txt"
  ( cd "$GW" && timeout 280 $BOTHORDERS_PYTEST "$@" ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | tr -d '\r' > "$f"
  tail -1 "$f"
}
fwd_args=("$@"); rev_args=(); for ((i=$#; i>=1; i--)); do rev_args+=("${!i}"); done
fwd=$(run forward "${fwd_args[@]}"); rev=$(run reverse "${rev_args[@]}")
pf=$(printf '%s' "$fwd" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); ff=$(printf '%s' "$fwd" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
pr=$(printf '%s' "$rev" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); fr=$(printf '%s' "$rev" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
echo "${label} forward: passed ${pf:-0}; failed ${ff:-0}"
echo "${label} reverse: passed ${pr:-0}; failed ${fr:-0}"
np=0
for o in forward reverse; do
  if [ "$o" = forward ]; then last="$fwd"; else last="$rev"; fi
  if ! printf '%s' "$last" | grep -qE '[0-9]+ passed'; then
    np=1; echo "${label} ${o}: NO PASS LINE; saved $OUT/${label}.${o}.txt"; tail -15 "$OUT/${label}.${o}.txt"
  fi
done
restore_audit
[ "$np" = 0 ] && [ "${ff:-0}" = 0 ] && [ "${fr:-0}" = 0 ] && [ "${pf:-0}" -ge 1 ] && [ "${pr:-0}" -ge 1 ] && [ "${pf:-0}" = "${pr:-0}" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
