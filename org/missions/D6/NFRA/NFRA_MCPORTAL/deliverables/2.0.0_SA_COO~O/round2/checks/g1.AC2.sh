#!/usr/bin/env bash
# MP-g-1 AC2 (E6's read, R-4): the two named history tests pass, nothing failed.
#   test_changes_reads_writer_table_across_principals  GET /api/admin/changes with NO parameters returns the writer table's
#                                                      items for two different principals, newest first
#   test_changes_table_unreachable_is_503              an unreachable changes table answers 503 with a reason, never a crash
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_admin_round2.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_changes_reads_writer_table_across_principals test_changes_table_unreachable_is_503; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 2; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 2 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
