#!/usr/bin/env bash
# MP-o-1 AC2 (the seam, against the REAL store's shapes): over the verbatim capture
# deliverables/2.0.0_SA_COO~MP/cp2/fixtures/s3_capture_20261009T0728Z.json, served by a fake client, _compute(hours) answers with
# every overlap holding >=2 roster boxes, the capture's INFRA overlap rated above every APPEND overlap, and deploys 'read'
# for all four boxes with open == the count of OPEN/HELD-SOVEREIGN-GATED entries computed in the test from the capture.
#   test_real_capture_overlap
. "$(dirname "$0")/_root.sh"
named_pytest "overlap real capture" tests/test_admin_fabric_overlap.py test_real_capture_overlap
