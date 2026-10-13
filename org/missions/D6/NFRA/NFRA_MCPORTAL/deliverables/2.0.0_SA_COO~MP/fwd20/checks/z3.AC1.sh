#!/usr/bin/env bash
# MP-z-3 AC1 (row Z-S41, CTO ruling msg 33519; decomposition GW.4): tests/test_dashboard_deep_links.py passes with
# 0 failed and each named test PASSES:
#   test_each_listed_route_serves_index_to_owner     every path in a planted routes.json -> 200 index.html for the owner
#   test_listed_route_refuses_non_owner              a listed path, no identity / wrong identity -> 401 / 403, no body
#   test_unknown_path_still_404                      a path not in routes.json -> 404, as today
#   test_missing_routes_file_serves_root_only        no or unreadable routes.json -> "/" serves, "/control-plane" 404s
#   test_existing_routes_keep_their_endpoint         /health, /assets/x, /api/admin/whoami, /mcp, /sprint resolve to
#                                                    the same endpoint as before the change (the app's route table)
#   test_bare_mcp_post_still_redirects               AMENDMENT 1: POST /mcp and DELETE /mcp -> 307 to /mcp/, never 405
#   test_unknown_path_any_method_404                 AMENDMENT 1: POST / PUT /no-such-page -> 404, never 405
#   AMENDMENT 2: the file must not pollute a suite that runs AFTER it in the same process -- co-run
#   tests/test_dashboard_deep_links.py FIRST, then test_owner_gate.py, test_admin_grants.py, test_admin_refusals.py:
#   0 failed (the issuer measured 7 failed in that order at ed6ccbcfc5; each file alone passes).
. "$(dirname "$0")/_root.sh"
co=$(cd "$GW" && timeout 110 python -m pytest tests/test_dashboard_deep_links.py tests/test_owner_gate.py tests/test_admin_grants.py tests/test_admin_refusals.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '' | tail -1)
cof=$(printf '%s' "$co" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); cof=${cof:-0}
echo "co-run (deep links first): $co"
[ -f "$GW/tests/test_dashboard_deep_links.py" ] && [ "$cof" != 0 ] && { echo "co-run failed=$cof"; echo "RESULT: FAIL"; exit 1; }
named_pytest "deep-link tests" tests/test_dashboard_deep_links.py test_each_listed_route_serves_index_to_owner test_listed_route_refuses_non_owner test_unknown_path_still_404 test_missing_routes_file_serves_root_only test_existing_routes_keep_their_endpoint test_bare_mcp_post_still_redirects test_unknown_path_any_method_404
