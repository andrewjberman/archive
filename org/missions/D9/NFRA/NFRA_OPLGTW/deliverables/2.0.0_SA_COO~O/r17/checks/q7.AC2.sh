#!/usr/bin/env bash
# OPLGTW OG-q-7 AC2: the two placeholder guards are RETIRED (integration.py carries 0 `_asset_policy is None` lines; at
# the cut it carried 2, prepare_download and export_query), every download path calls sem.qualify_asset_plan (count of
# call sites >= 3: query, prepare_download, export_query), and the rest of the schwab test files add NO failure beyond
# the r17 baseline (r17/Q7_SUITE_BASELINE.txt), each FILE run in its own process (the one-process class is OG-ti-1's).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
I="$GW/app/integrations/schwab/integration.py"
g=$(grep -c '_asset_policy is None' "$I")
q=$(grep -c 'qualify_asset_plan(' "$I")
B="$(cd "$(dirname "$0")/.." && pwd)/Q7_SUITE_BASELINE.txt"
export AUDIT_PATH="${TMP:-/tmp}/og_r17_q7b_audit_$$.jsonl"
fails=""
for f in $(cd "$GW" && ls tests/test_schwab_*.py); do
  o=$(cd "$GW" && timeout 300 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r')
  fails="$fails
$(printf '%s\n' "$o" | sed -n 's/^\(FAILED\|ERROR\) \([^ ]*\).*/\2/p')"
done
restore_audit; rm -f "$AUDIT_PATH"
newids=$(printf '%s\n' "$fails" | tr '\\' '/' | grep . | sort -u | grep -vxF -f <(grep -v '^#' "$B" | grep .))
new=$(printf '%s\n' "$newids" | grep -c .)
echo "guards '_asset_policy is None' $g (want 0); qualify_asset_plan call sites $q (want >= 3); failures beyond baseline $new $(printf '%s ' $newids)"
[ "$g" = 0 ] && [ "$q" -ge 3 ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
