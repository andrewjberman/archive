#!/usr/bin/env bash
# OPLGTW OG-lg-1 AC2: nothing around /login regresses -- tests/test_principal_cutover.py (ROUTE_CLASS),
# tests/test_data_entitlement_guard.py (route census), tests/test_browser_oidc.py and tests/test_login_admit_r24.py each
# run GREEN in their own process, and the whole schwab set still runs in ONE process with 0 errors and nothing beyond the
# baseline (r18/checks/ti2.AC1.sh PASS).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r20_lg1b_audit_$$.jsonl"
res=""; allok=1
for f in tests/test_principal_cutover.py tests/test_data_entitlement_guard.py tests/test_browser_oidc.py tests/test_login_admit_r24.py; do
  o=$(cd "$GW" && timeout 400 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  s=$(printf '%s\n' "$o" | grep -E '[0-9]+ (passed|failed|error)' | tail -1)
  res="$res $(basename "$f") rc=$rc [$s];"; [ "$rc" = 0 ] || allok=0
done
restore_audit; rm -f "$AUDIT_PATH"
t=no; bash "$(dirname "$0")/../../r18/checks/ti2.AC1.sh" >/dev/null 2>&1 && t=yes
echo "own-process runs:$res one-process schwab floor (ti2.AC1) $t"
[ "$allok" = 1 ] && [ "$t" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
