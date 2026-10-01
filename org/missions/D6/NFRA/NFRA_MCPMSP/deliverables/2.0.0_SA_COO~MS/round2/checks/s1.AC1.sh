#!/usr/bin/env bash
# MS-s-1 AC1 (the built behaviour, with its difference control): .tools/tests/test_safe_apply_targeted.sh, run against
# the working .tools/safe-apply.sh, prints "PASS: <arm>" for each of the five arms and "RESULT: PASS"; and the SAME test
# run against the base bytes (safe-apply.sh at 0af3c52597, the last commit to touch it before this round, passed via
# SAFE_APPLY_UNDER_TEST) does NOT pass all five -- the arms discriminate the ruling's change.
. "$(dirname "$0")/_root.sh"
T=".tools/tests/test_safe_apply_targeted.sh"
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
ARMS="targeted_plan_carries_caller_args targeted_out_of_pattern_refuses_enforce planfile_apply_grades_given_planfile untargeted_apply_unchanged targeted_unrenderable_refuses_enforce"
count() { n=0; for a in $ARMS; do printf '%s\n' "$1" | grep -qE "^PASS:? *$a\b" && n=$((n+1)); done; echo $n; }
new=$(SAFE_APPLY_UNDER_TEST=".tools/safe-apply.sh" timeout 110 bash "$T" 2>&1 | tr -d '\r')
B="$(mktemp "${TMPDIR:-/tmp}/safe_apply_base.XXXXXX.sh")"
git show 0af3c52597:.tools/safe-apply.sh > "$B"
old=$(SAFE_APPLY_UNDER_TEST="$B" timeout 110 bash "$T" 2>&1 | tr -d '\r'); rm -f "$B"
nn=$(count "$new"); no=$(count "$old")
fin=$(printf '%s\n' "$new" | grep -c '^RESULT: PASS')
echo "working safe-apply: arms PASS $nn of 5, final RESULT: PASS lines=$fin; base safe-apply (0af3c52597): arms PASS $no of 5"
if [ "$nn" = 5 ] && [ "$fin" -ge 1 ] && [ "$no" -lt 5 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
