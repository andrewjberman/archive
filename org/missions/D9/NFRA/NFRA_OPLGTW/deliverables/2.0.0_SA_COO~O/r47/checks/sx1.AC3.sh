#!/usr/bin/env bash
# OPLGTW OG-sx-1 AC3 (round 47): the worker's new test file tests/test_og_sx1.py passes and the existing tests of the five touched modules still pass
# (the Cottonwood adapter via test_og_cl4 and test_og_en4, family_depth via test_og_cd1 and test_og_cd2, the opal_portal status and send tests, the identity-scope, min-tier and classification tests that import the integrations).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_sx1.py tests/test_og_cl4.py tests/test_og_en4.py tests/test_og_cd1.py tests/test_og_cd2.py tests/test_opal_portal_status_displayed_date.py tests/test_opal_portal_status_id_shape.py tests/test_opal_portal_send_split.py tests/test_opal_portal_dedupe_content.py tests/test_tool_classification_composition.py tests/test_min_tier_gate.py tests/test_identity_scope.py
rc=$?; restore_audit
exit $rc
