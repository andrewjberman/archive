#!/usr/bin/env bash
# OPLGTW OG-rr-2 AC1 (round-37, CTO ruling @8b9adcbd8d s3 cell 2, msg 34906): the commit-time naming gate checks name_rulings.json rows' ruling_ref.
# The gate's self-test is green and carries four ruling_ref arms:
#   (1) a present ruling_ref that does NOT resolve -> REFUSE; (2) a resolving ruling_ref -> RULED/admitted; (3) a row ADDED in the staged diff with no ruling_ref -> REFUSE;
#   (4) a legacy row (present at HEAD, no ruling_ref) -> grade unchanged (not refused).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(timeout 115 python .tools/naming-gate.py --self-test 2>&1 | tr -d '\r'); rc=$?
pass=$(printf '%s\n' "$out" | grep -c '^NAMING-GATE-SELF-TEST: PASS')
a1=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm ruling-ref refuse-unresolved: .*REFUSE.*: ok$')
a2=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm ruling-ref admit-resolved: .*: ok$')
a3=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm ruling-ref refuse-new-row-no-ref: .*REFUSE.*: ok$')
a4=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm ruling-ref legacy-row-unchanged: .*: ok$')
fails=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm .*: (FAIL|MISMATCH)')
echo "gate self-test: rc=$rc; PASS lines $pass (want 1); ruling-ref arms refuse-unresolved $a1, admit-resolved $a2, refuse-new-row-no-ref $a3, legacy-row-unchanged $a4 (want 1 or more each); failing arms $fails (want 0)"
[ "$rc" = 0 ] && [ "$pass" = 1 ] && [ "$a1" -ge 1 ] && [ "$a2" -ge 1 ] && [ "$a3" -ge 1 ] && [ "$a4" -ge 1 ] && [ "$fails" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
