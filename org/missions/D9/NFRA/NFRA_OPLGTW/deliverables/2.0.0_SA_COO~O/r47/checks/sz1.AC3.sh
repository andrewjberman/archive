#!/usr/bin/env bash
# OPLGTW OG-sz-1 AC3 (round 47): the worker's new test file tests/test_og_sz1.py passes and the 16 existing test files that exercise harvest_typed, the portal_index
# integration and opal_discover still pass (137 tests at the base).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_sz1.py tests/test_og_gt0.py tests/test_og_gt5.py tests/test_og_gt6.py tests/test_portal_index.py tests/test_opal_discover.py tests/test_discover_echo.py tests/test_og_en9.py tests/test_og_en22.py tests/test_og_pt2.py tests/test_og_pt5.py tests/test_og_et1.py tests/test_positioning_extension.py tests/test_query_v0_tool.py tests/test_ce3_parts_absent_wording.py tests/test_firm_catalog_visibility.py tests/test_internal_role_routing.py
rc=$?; restore_audit
exit $rc
