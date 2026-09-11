#!/usr/bin/env bash
# Run each .tools/tests/*.py standalone (they are scripts, not pytest modules:
# test_fabric_check_classify.py raises SystemExit at import, which collects the
# WHOLE directory to zero under pytest). Print the denominator either way.
cd "$(dirname "$0")/../../../../../../.."  || exit 9
PASS=0; FAIL=0; TOTAL=0; FAILED=""
for t in .tools/tests/*.py; do
  TOTAL=$((TOTAL+1))
  if timeout 180 python "$t" >/dev/null 2>&1; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); FAILED="$FAILED $t"; fi
done
echo "TOOLS-TESTS: $PASS PASS / $FAIL FAIL of $TOTAL total (.tools/tests/*.py, run standalone)"
[ -n "$FAILED" ] && { echo "FAILED FILES:"; for f in $FAILED; do echo "  $f"; done; }
exit 0
