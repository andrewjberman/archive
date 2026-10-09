#!/usr/bin/env bash
# MS-s-2 AC1 (the built behaviour, with its difference control): .tools/tests/test_safe_apply_scoped_gates.sh, run
# against the working .tools/safe-apply.sh, prints "PASS: <arm>" for each of the six arms and "RESULT: PASS"; and the
# SAME test run against the base bytes (safe-apply.sh at $SA_BASE, passed via SAFE_APPLY_UNDER_TEST) does NOT pass all
# six -- the arms discriminate this cell's change.
. "$(dirname "$0")/_root.sh"
T=".tools/tests/test_safe_apply_scoped_gates.sh"
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
ARMS="tagauthz_targeted_grades_own_plan tagauthz_targeted_refuses_own_plan tombstone_targeted_grades_own_plan tombstone_targeted_refuses_own_plan planfile_stages_read_given_planfile unscoped_apply_unchanged"
count() { n=0; for a in $ARMS; do printf '%s\n' "$1" | grep -qE "^PASS:? *$a\b" && n=$((n+1)); done; echo $n; }
new=$(SAFE_APPLY_UNDER_TEST=".tools/safe-apply.sh" timeout 55 bash "$T" 2>&1 | tr -d '\r')
B="$(mktemp "${TMPDIR:-/tmp}/safe_apply_base.XXXXXX.sh")"
git show "$SA_BASE":.tools/safe-apply.sh > "$B"
old=$(SAFE_APPLY_UNDER_TEST="$B" timeout 55 bash "$T" 2>&1 | tr -d '\r'); rm -f "$B"
nn=$(count "$new"); no=$(count "$old")
fin=$(printf '%s\n' "$new" | grep -c '^RESULT: PASS')
echo "working safe-apply: arms PASS $nn of 6, final RESULT: PASS lines=$fin; base safe-apply ($SA_BASE): arms PASS $no of 6"
if [ "$nn" = 6 ] && [ "$fin" -ge 1 ] && [ "$no" -lt 6 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
