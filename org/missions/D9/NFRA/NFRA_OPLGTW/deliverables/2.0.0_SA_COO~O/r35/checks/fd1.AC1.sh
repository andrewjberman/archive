#!/usr/bin/env bash
# OPLGTW OG-fd-1 AC1 (round-35 E1, row Z-S91): the per-family DLQ drain. Named tests in
# data/assets/scripts/silver/tests/test_mirror_conversion.py:
# - test_fd1_ac01: a planted message of family A survives family B's sweep (visibility reset, not deleted) and is
#   absent from B's report;
# - test_fd1_ac02: A's own sweep then drains it and reports it;
# - test_fd1_ac03: a message whose family cannot be read is left in the queue and reported as unattributed, never
#   deleted.
# The whole test_mirror_conversion suite passes. The packaged Lambda copies are build snapshots (measured at the cut: 0 of 4
# equal to the source, eclipse -358 lines), so packaging belongs to the apply's never-widen ask, not to this criterion.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
S=data/assets/scripts/silver
out=$(cd "$S" && timeout 110 python -m pytest tests/test_mirror_conversion.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_fd1_ac01 test_fd1_ac02 test_fd1_ac03; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "test_mirror_conversion.py: pytest rc=$rc; named tests passed $p of 3; failed/error lines $failed"
[ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$failed" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
