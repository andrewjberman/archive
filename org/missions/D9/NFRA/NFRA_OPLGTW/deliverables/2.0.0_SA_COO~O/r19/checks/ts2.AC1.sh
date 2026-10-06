#!/usr/bin/env bash
# OPLGTW OG-ts-2 AC1 (rows Z-W22-S9/S10, CTO round-18 analysis s.4 item 1): each of the three files runs GREEN in its own
# process -- tests/test_principal_cutover.py (ROUTE_CLASS classifies /yearinreview and /yearinreview/),
# tests/test_data_entitlement_guard.py (the route census), tests/test_schwab_host_inputs.py (51 keys; the build_package
# call on CLOUD's signature). The S9 pair leaves r17/Q7_SUITE_BASELINE.txt at the drain (an issuer act; that file is
# in the issuer's own lane).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r19_ts2_audit_$$.jsonl"
res=""; allok=1
for f in tests/test_principal_cutover.py tests/test_data_entitlement_guard.py tests/test_schwab_host_inputs.py; do
  o=$(cd "$GW" && timeout 400 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  s=$(printf '%s\n' "$o" | grep -E '[0-9]+ (passed|failed|error)' | tail -1)
  res="$res $(basename "$f") rc=$rc [$s];"; [ "$rc" = 0 ] || allok=0
done
restore_audit; rm -f "$AUDIT_PATH"
echo "own-process runs:$res"
[ "$allok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
