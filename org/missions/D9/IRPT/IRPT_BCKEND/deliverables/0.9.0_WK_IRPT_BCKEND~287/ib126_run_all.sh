#!/usr/bin/env bash
# IB126 (worker 0.9.0_WK_IRPT_BCKEND~287, IRPT_BCKEND.TO-IB-pr-428): re-runs every capture and rebuilds the outputs.
# READ ONLY, LOCAL ONLY: existing handler tests with in-memory fakes; no AWS call, no live request. Run from anywhere.
# Each capture runs one existing test UNALTERED under ib126_capture_plugin.py (it only records the envelope the handler returned).
set -u
R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
D="$R/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~287"
IR="$R/infra/aws/lambda/investor-reporting"
A="$R/.scratch/answers"
mkdir -p "$A"
rm -f "$A"/*.json

cap() {  # cap <test dir> <wrap> <op> <out> <match|-> <pythonpath> <pytest target>
  local dir="$1" wrap="$2" op="$3" out="$4" match="$5" pp="$6" target="$7"
  echo "--- $op ($out)"
  if [ "$match" = "-" ]; then
    ( cd "$IR/$dir" && IB126_WRAP="$wrap" IB126_OP="$op" IB126_OUT="$A/$out" PYTHONPATH="$pp" \
        timeout 120 python -m pytest -q -p no:cacheprovider -p ib126_capture_plugin "$target" 2>&1 | tail -3 )
  else
    ( cd "$IR/$dir" && IB126_WRAP="$wrap" IB126_OP="$op" IB126_MATCH="$match" IB126_OUT="$A/$out" PYTHONPATH="$pp" \
        timeout 120 python -m pytest -q -p no:cacheprovider -p ib126_capture_plugin "$target" 2>&1 | tail -3 )
  fi
}

cap directory/tests entry.ENTRY.handle directory-browse directory-browse.json 'data.next_cursor=null' "$D" \
    "test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable"
cap ops/tests call analysis-request-history analysis-request-history.json - "$D" \
    "test_owned_entry.py::test_actual_entry_current_owner_serves_typed_data_without_custody_input[history]"
cap intake/tests sys:served.Entry.handle analysis-input-upload analysis-input-upload.normalized.json 'data.state="NORMALIZED"' "$D" \
    "test_deferred_resolution.py::test_resident_resolves_through_the_broker_to_the_12_03_frozen_input"
cap reports/tests sys:served.Entry.handle analysis-input-upload analysis-input-upload.json - "$D" \
    "test_generate_installed.py::test_the_upload_route_publishes_resolving_and_sends_one_message"
cap export/tests entry.lambda_handler custody-report-persist custody-report-persist.json - "$D" \
    "test_custody_writer_composed.py::test_guarded_or_scheduled_a_verified_opal_caller_persists_through_the_entry"
cap export/tests entry.lambda_handler custody-report-read custody-report-read.json - "$D;$IR/export/tests" \
    "$D/ib126_custody_read_probe.py"
cap ycharts/generate/tests sys:served.Entry.handle comparison-catalogue comparison-catalogue.json - "$D" \
    "test_comparison_catalogue.py::test_the_read_rides_the_entrys_guard_and_tenant_check"

echo "--- tests that exercise the nullable alternatives at payload level (run unaltered, no capture)"
( cd "$IR/ops/tests" && timeout 120 python -m pytest -q -p no:cacheprovider test_history_row_client.py 2>&1 | tail -1 )
( cd "$IR/ycharts/generate/tests" && timeout 120 python -m pytest -q -p no:cacheprovider test_comparison_catalogue.py 2>&1 | tail -1 )

cd "$R" || exit 1
python "$D/ib126_make_facts.py"
python "$D/ib126_pin_read.py" . > /dev/null && echo "OK: ib126_source_map_pins.json written"
python "$D/ib126_compare.py" .
