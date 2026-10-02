#!/usr/bin/env bash
# MX-s-18 AC1 (Z-W24-S4/S5, CTO 3a): the BD runner's own sentinel check -- a MEASURED has_data_rows=0 transactions
# (PERIOD) sidecar yields the sentinel; a 0-row SNAPSHOT table still withholds; 'OK: bronze sentinel emitted' prints
# only after a head_object reads the sentinel back. Named tests, offline (stubbed S3).
. "$(dirname "$0")/_root.sh"
T=infra/aws/lambda/bd-pipeline/bd-49f-runner/tests/test_runner_sentinel.py
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$T" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_period_empty_window_emits_sentinel test_snapshot_zero_rows_withholds test_ok_line_only_after_head_object_readback; do
  printf '%s\n' "$out" | grep -E "^PASSED [^ ]*::$t( |$)" >/dev/null && p=$((p+1)); done
echo "pytest rc=$rc; named tests passed $p of 3"; [ "$p" = 3 ] || rc=1
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
