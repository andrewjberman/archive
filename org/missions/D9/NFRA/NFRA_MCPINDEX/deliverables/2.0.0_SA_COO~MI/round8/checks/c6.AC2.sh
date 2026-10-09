#!/usr/bin/env bash
# MX-c-6 AC2 (C1, the ONE writer): need entries are validated by the emitter's own schema. Three named tests in
# workflows/atom_decomposition/tests/test_catalog_need_entries.py prove the refusals (a GAP need with no owner, a
# PARTIAL vendor need with no live_error, a status outside the enum), and the emitter's existing test files still pass.
. "$(dirname "$0")/_root.sh"
T=workflows/atom_decomposition/tests
[ -f "$T/test_catalog_need_entries.py" ] || { echo "$T/test_catalog_need_entries.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 200 python -m pytest "$T/test_catalog_need_entries.py" "$T/test_catalog_silver_entries.py" "$T/test_emit_declared_inputs.py" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_gap_need_without_owner_is_refused test_partial_vendor_need_without_live_error_is_refused test_need_status_outside_the_enum_is_refused; do
  printf '%s\n' "$out" | grep -E "^PASSED [^ ]*::$t( |$)" >/dev/null && p=$((p+1)); done
f=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
echo "pytest rc=$rc; named tests passed $p of 3; failed/error tests $f"
if [ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$f" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
