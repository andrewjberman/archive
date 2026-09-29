#!/usr/bin/env bash
# OPLGTW OG-m-2 AC1 (E11 remedy, CTO msg 26305 option (a)): the dispatcher grades the chain log's terminal line, not SSM
# stdout cut at 24,000 chars; an S3 accelerator event dispatches only on a qualified marker; the floor reads no marker;
# nothing ever dispatches twice. 6 named tests, synthetic events, stubbed clients.
. "$(dirname "$0")/_root.sh"
T="infra/aws/lambda/opal-assets/tests/test_advi_49f_gold_dispatch_remedy.py"
[ -f "$T" ] || { echo "$T absent; named tests passed 0 of 6"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$T" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
n=0; p=0
for t in test_chain_log_ok_classifies_ok_once test_chain_log_abort_classifies_abort test_missing_chain_log_is_unknown_and_says_so \
  test_incomplete_marker_does_not_dispatch test_qualified_marker_dispatches_once test_floor_event_reads_no_marker; do
  n=$((n+1)); printf '%s\n' "$out" | grep -E "::$t PASSED" >/dev/null && p=$((p+1))
done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of $n; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = "$n" ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
