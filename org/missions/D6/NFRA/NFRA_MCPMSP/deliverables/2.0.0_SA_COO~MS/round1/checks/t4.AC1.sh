#!/usr/bin/env bash
# MS-t-4 AC1 (the built behaviour, on fixtures): opal_ai/opal/runtime-msp/record/test_ship_run.py passes with nothing
# failed and each named test PASSES: a dry run writes nothing; the planned keys sit under the builder's address
# s3://opal-data-assets/gateway/<firm>/bronze/msp_runs/<date>/<run_id>/; only the audit rows inside the window AND of the
# calling identity are shipped; and the record carries firm, advisor_oid and run_id tags.
. "$(dirname "$0")/_root.sh"
if pytest_named "opal_ai/opal/runtime-msp/record/test_ship_run.py" 1 \
  test_dry_run_writes_nothing test_keys_under_builder_address \
  test_audit_rows_filtered_to_window_and_identity test_record_tagged_firm_advisor_run; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
