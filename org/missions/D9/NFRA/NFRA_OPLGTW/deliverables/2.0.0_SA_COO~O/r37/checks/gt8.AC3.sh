#!/usr/bin/env bash
# OPLGTW OG-gt-8 AC3 (round-37, FWD-22): the worker's own test file exists with 2+ tests, and it passes together with the
# suites of the two modules this cell edits (harvest_identity -> test_og_gt1; news_typed -> test_og_nw1) plus the shared layer.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
[ -f "$GW/tests/test_og_gt8.py" ] || { echo "$GW/tests/test_og_gt8.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$GW" && timeout 115 python -m pytest tests/test_og_gt8.py tests/test_og_gt1.py tests/test_og_gt0.py tests/test_og_nw1.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
tail -3 <<<"$out" | grep -E "passed|failed|error" | tail -1
n8=$(grep -cE '^\s*def test_' "$GW/tests/test_og_gt8.py" | tr -d '\r')
failed=$(grep -cE ' FAILED| ERROR' <<<"$out")
restore_audit
echo "pytest rc=$rc; tests defined in test_og_gt8.py $n8 (want 2+); failed/error lines $failed"
[ "$rc" = 0 ] && [ "$n8" -ge 2 ] && [ "$failed" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
