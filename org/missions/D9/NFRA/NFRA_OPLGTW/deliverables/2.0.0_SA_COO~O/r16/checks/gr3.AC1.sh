#!/usr/bin/env bash
# OPLGTW OG-gr-3 AC1 (CTO round-15 analysis R9): the three named tests in tests/test_schwab_grain_r9.py pass, and the
# existing grain/semantics suites stay green -- query.py DATASET_GRAINS and datasets.json grain_fields carry R9's grain
# (dim_position + quantity_settled_unsettled + quantity_cash_settled; dim_asset + security_description_line_1),
# semantics.py accepts them at import, and a planted collision refuses paging.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r16_gr3_audit_$$.jsonl"
pytest_named tests/test_schwab_grain_r9.py test_oggr3_ac01 test_oggr3_ac02 test_oggr3_ac03; r1=$?
out=$(cd "$GW" && timeout 200 python -m pytest tests/test_schwab_semantics.py tests/test_schwab_query.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r2=$?
echo "semantics+query suites rc=$r2 ($(printf '%s\n' "$out" | tail -1))"
restore_audit; rm -f "$AUDIT_PATH"
[ "$r1" = 0 ] && [ "$r2" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
