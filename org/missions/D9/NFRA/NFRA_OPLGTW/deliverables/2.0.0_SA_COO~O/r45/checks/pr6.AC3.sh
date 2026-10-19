#!/usr/bin/env bash
# OPLGTW OG-pr-6 AC3 (round 45): the existing audit tests and the new test file pass together in both orders with the same count.
# The set: tests/test_audit_bytes_principal.py tests/test_audit_lake_key_stamp.py tests/test_audit_rivalfunds_args.py tests/test_og_en10.py tests/test_og_pr6.py (the new file).
# A thin call of the shared both-orders check (r38/checks/_bothorders.sh, which keeps the forward text since OG-en-33).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/_bothorders.sh pr6set tests/test_audit_bytes_principal.py tests/test_audit_lake_key_stamp.py tests/test_audit_rivalfunds_args.py tests/test_og_en10.py tests/test_og_pr6.py
exit $?
