#!/usr/bin/env bash
# OPLGTW OG-fd-1 AC2 (A1, row Z-W58-S1): the Schwab Lambda's own drain_dlq (data/assets/scripts/silver/schwab_runtime.py) is
# per-family too. Named test in data/assets/scripts/silver/tests/test_schwab_runtime.py:
# - test_fd1_ac04: a planted non-schwab message survives the schwab sweep (visibility reset, not deleted, not reported);
#   a schwab message is drained and reported; an unattributable one is never deleted.
# The whole test_schwab_runtime suite passes, and test_mirror_conversion still passes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
S=data/assets/scripts/silver
out=$(cd "$S" && timeout 110 python -m pytest tests/test_schwab_runtime.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; printf '%s\n' "$out" | grep -E "::test_fd1_ac04(\[.*\])? PASSED" >/dev/null && p=1
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
out2=$(cd "$S" && timeout 110 python -m pytest tests/test_mirror_conversion.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc2=$?
echo "test_schwab_runtime.py: pytest rc=$rc; named test passed $p of 1; failed/error lines $failed"
echo "test_mirror_conversion.py: pytest rc=$rc2"
[ "$rc" = 0 ] && [ "$p" = 1 ] && [ "$failed" = 0 ] && [ "$rc2" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
