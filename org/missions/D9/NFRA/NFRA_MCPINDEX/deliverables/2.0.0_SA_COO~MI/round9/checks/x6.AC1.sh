#!/usr/bin/env bash
# MX-x-6 AC1 (row Z-W29-S1, round-8 analysis E3): the catalog emitter takes its census dir from the checkout it runs in
# by default, and REFUSES a --census-dir outside that checkout (a planted foreign dir is refused, nothing written).
# The two named tests in workflows/atom_decomposition/tests/test_emit_declared_inputs.py, read from pytest's -rA summary.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
F=workflows/atom_decomposition/tests/test_emit_declared_inputs.py
T1=test_census_dir_outside_checkout_refused
T2=test_census_dir_default_is_this_checkout
out=$(timeout 110 python -m pytest "$F" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in $T1 $T2; do printf '%s\n' "$out" | grep -E "^PASSED [^ ]*::$t( |$)" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
echo "pytest rc=$rc; named tests passed $p of 2; failed/error tests $failed"
if [ "$rc" = 0 ] && [ "$p" = 2 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
