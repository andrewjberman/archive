#!/usr/bin/env bash
# OPLGTW OG-ng-2 AC1 (round-37, XA-20261016T034740Z-28da): the gate's self-test is green and carries the three name_rulings arms:
#   (1) a none_owed row admits its own (name, type) pair; (2) a planted carrier with NO row still REFUSEs; (3) the same name under another type is not admitted.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(timeout 115 python .tools/naming-gate.py --self-test 2>&1 | tr -d '\r'); rc=$?
pass=$(printf '%s\n' "$out" | grep -c '^NAMING-GATE-SELF-TEST: PASS')
arm1=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm name-rulings admit: .*: ok$')
arm2=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm name-rulings control no-row: .*REFUSE.*: ok$')
arm3=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm name-rulings control other-type: .*REFUSE.*: ok$')
fails=$(printf '%s\n' "$out" | grep -cE '^SELF-TEST arm .*: (FAIL|MISMATCH)')
echo "gate self-test: rc=$rc; PASS lines $pass (want 1); name-rulings arms admit $arm1, no-row control $arm2, other-type control $arm3 (want 1 or more each); failing arms $fails (want 0)"
[ "$rc" = 0 ] && [ "$pass" = 1 ] && [ "$arm1" -ge 1 ] && [ "$arm2" -ge 1 ] && [ "$arm3" -ge 1 ] && [ "$fails" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
