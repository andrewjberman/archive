#!/usr/bin/env bash
# MP-k-1 AC2 (the seam, against BOTH real neighbours): (1) over the verbatim capture, _compute('open') reads every box
# 'published' with open == that box's captured OPEN row count and scanned_at from its scan.json; (2) the request body the
# POST writes is APPLIED by the REAL consumer -- .tools/open-calls-scan.py apply_requests(), loaded from the repo, run
# with an in-memory store and a recording close() -- and its close() receives the call_id and ruled_by 'andrew'.
#   test_real_capture_calls
#   test_request_accepted_by_open_calls_scan
. "$(dirname "$0")/_root.sh"
named_pytest "calls seams" tests/test_admin_fabric_calls.py test_real_capture_calls test_request_accepted_by_open_calls_scan
