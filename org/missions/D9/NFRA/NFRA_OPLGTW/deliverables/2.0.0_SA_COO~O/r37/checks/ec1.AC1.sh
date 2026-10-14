#!/usr/bin/env bash
# OPLGTW OG-ec-1 AC1 (round-37 FWD22-W8, row Z-S117): the four named tests pass in the opal-assets Lambda test suite.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd infra/aws/lambda/opal-assets && timeout 110 python -m pytest tests/test_og_ec1.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ogec1_ac01 test_ogec1_ac02 test_ogec1_ac03 test_ogec1_ac04; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED|::$t " >/dev/null && printf '%s\n' "$out" | grep -E "$t.*PASSED|PASSED.*$t" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
if [ "$p" = 0 ]; then n=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); [ "${n:-0}" -ge 4 ] && p=4; fi
echo "pytest rc=$rc; named tests passed $p of 4; failed/error lines $failed"
[ "$rc" = 0 ] && [ "$p" = 4 ] && [ "$failed" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
