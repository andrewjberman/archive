#!/usr/bin/env bash
# OPLGTW OG-bf-1 AC4 (amendment A1, ruling Y of the CTO half @f9b1f1fd31): the 49F gold dispatcher's accelerator branch
# SKIPS a qualified completion record whose date is not the production T-1. Four named tests in
# infra/aws/lambda/opal-assets/tests/test_advi_49f_gold_dispatch_dategate.py, offline (EC2, SSM and S3 mocked):
#   (01) a qualified record dated an earlier trading day returns dispatched false with the ruled skip_reason, and NO
#        EC2 or SSM call is made;
#   (02) a qualified record dated the production T-1 (from lib/trading_calendar.py as packaged) dispatches as today;
#   (03) a calendar that cannot be read SKIPS (never dispatches);
#   (04) a non-qualified record still SKIPS on the qualified check first (OG-m-2a unchanged), and a floor (scheduled)
#        event never reaches the date gate.
# And the existing tests/test_advi_49f_gold_dispatch_remedy.py passes whole, none of its tests removed or renamed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
T="infra/aws/lambda/opal-assets/tests"
BASE="94fa98a229"
ok=1
out=$(timeout 100 python -m pytest "$T/test_advi_49f_gold_dispatch_dategate.py" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ogbf1y_ac01 test_ogbf1y_ac02 test_ogbf1y_ac03 test_ogbf1y_ac04; do printf '%s\n' "$out" | grep -E "(::|\.)$t(\[.*\])? PASSED|$t \(.*\) \.\.\. ok" >/dev/null && p=$((p+1)); done
echo "dategate: pytest rc=$rc; named tests passed $p of 4"
[ "$rc" = 0 ] && [ "$p" = 4 ] || ok=0
f="$T/test_advi_49f_gold_dispatch_remedy.py"
out2=$(timeout 100 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc2=$?
was=$(MSYS_NO_PATHCONV=1 git show "$BASE:$f" | grep -cE '^\s*def test_')
now=$(grep -cE '^\s*def test_' "$f")
gone=$(MSYS_NO_PATHCONV=1 git show "$BASE:$f" | grep -oE 'def test_[A-Za-z0-9_]+' | sed 's/^def //' | while read -r t; do grep -qE "def $t\b" "$f" || echo "$t"; done | grep -c .)
echo "remedy: pytest rc=$rc2 ($(printf '%s\n' "$out2" | grep -E 'passed|failed' | tail -1)); test functions at the cut $was, now $now, removed or renamed $gone"
[ "$rc2" = 0 ] && [ "$gone" = 0 ] && [ "$now" -ge "$was" ] && [ "$was" -gt 0 ] || ok=0
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
