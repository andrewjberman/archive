#!/usr/bin/env bash
# MX-t-8 AC3 (FWD-2 parity, offline half; the live side-by-side is the close run's): the named test passes, nothing failed.
#   test_parity_with_served_object   (difference) for the mdpf family (amended to row W3-S11: the 3 tools catalog_gate resolves), the
#                                    tool's figure and as-of date for one fixture equal the served object's own figure and
#                                    as-of date, while the same fixture with its date shifted by one day reports the mismatch
. "$(dirname "$0")/_root.sh"
if pytest_named tests/test_portal_index.py test_parity_with_served_object; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
