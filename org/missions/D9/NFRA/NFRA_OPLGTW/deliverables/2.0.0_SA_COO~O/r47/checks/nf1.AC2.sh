#!/usr/bin/env bash
# OPLGTW OG-nf-1 AC2 (round 47): the worker's new test file tests/test_og_nf1.py passes and the existing news tests still pass
# (test_og_gt8 carries one red at the live ref, test_oggt8_ac03_deploy_stages_lib, and is not in the set).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_nf1.py tests/test_og_nw1.py tests/test_og_nw2.py tests/test_og_en5.py
rc=$?; restore_audit
exit $rc
