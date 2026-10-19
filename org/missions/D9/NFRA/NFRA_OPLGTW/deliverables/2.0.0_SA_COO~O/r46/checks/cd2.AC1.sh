#!/usr/bin/env bash
# OPLGTW OG-cd-2 AC1 (round 46; the CTO's round-45 analysis A1, item 3): the family_depth route is mounted in app/admin_api.py BEHIND the owner gate.
# The three named tests in tests/test_og_cd2.py pass together: test_ogcd2_ac01 (the route /gateway/families, GET, is in admin_api.routes and its endpoint is NOT the bare family_depth.families),
# test_ogcd2_ac02 (no identity header -> 401, a verified non-owner -> 403, and family_depth.read is called by neither), test_ogcd2_ac03 (the owner -> 200 and the body equals the stubbed read()).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_cd2.py test_ogcd2_ac01 test_ogcd2_ac02 test_ogcd2_ac03
rc=$?; restore_audit
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
