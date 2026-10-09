#!/usr/bin/env bash
# MP-s-1 AC2 (the seam, against the REAL store's shapes): over the verbatim capture, _compute() reads all four boxes
# 'recorded', each box's state equals the CP2.3-G rule applied in the test to that box's captured latest.json, and
# trunk.head is the newest latest.json's trunk_head[:12] with claim 'inferred'.
#   test_real_capture_gitstate
. "$(dirname "$0")/_root.sh"
named_pytest "gitstate real capture" tests/test_admin_fabric_gitstate.py test_real_capture_gitstate
