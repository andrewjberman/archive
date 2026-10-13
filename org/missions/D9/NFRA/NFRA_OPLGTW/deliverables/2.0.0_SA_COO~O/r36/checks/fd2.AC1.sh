#!/usr/bin/env bash
# OPLGTW OG-fd-2 AC1 (round-36 E2, row Z-S100): run_sweep persists its DLQ drain dict into the backfill-status section it
# writes, for the mirror families and for schwab. Named tests: test_fd2_ac01 (tests/test_mirror_conversion.py) and
# test_fd2_ac02 (tests/test_schwab_runtime.py); both whole suites pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
S=data/assets/scripts/silver
o1=$(cd "$S" && timeout 110 python -m pytest tests/test_mirror_conversion.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r1=$?
o2=$(cd "$S" && timeout 110 python -m pytest tests/test_schwab_runtime.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r2=$?
p=0
printf '%s\n' "$o1" | grep -qE '::test_fd2_ac01(\[.*\])? PASSED' && p=$((p+1))
printf '%s\n' "$o2" | grep -qE '::test_fd2_ac02(\[.*\])? PASSED' && p=$((p+1))
echo "mirror rc=$r1; schwab rc=$r2; named tests passed $p of 2"
[ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$p" = 2 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
