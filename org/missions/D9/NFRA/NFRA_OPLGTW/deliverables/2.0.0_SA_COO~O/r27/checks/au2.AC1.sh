#!/usr/bin/env bash
# OPLGTW OG-au-2 AC1 (round-24 analysis, ruling on row Z-S64): the rivalfunds routes record which page was served.
# Four named tests in tests/test_audit_rivalfunds_args.py: (01) a rivalfunds_view record keeps day, route and fund;
# (02) NEGATIVE CONTROL: an arg outside those three (verdict, days, any other key) is absent from the record;
# (03) each 200 answer of the page, audit, archive and chart handlers writes bytes equal to the body's length;
# (04) every rivalfunds_view record carries a route, one of page, audit, archive, chart.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r27_au2_audit_$$.jsonl"
pytest_named tests/test_audit_rivalfunds_args.py test_ogau2_ac01 test_ogau2_ac02 test_ogau2_ac03 test_ogau2_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
