#!/usr/bin/env bash
# MP-z-3 AC1 (row Z-S41, CTO ruling msg 33519; decomposition GW.4): tests/test_dashboard_deep_links.py passes with
# 0 failed and each named test PASSES:
#   test_each_listed_route_serves_index_to_owner     every path in a planted routes.json -> 200 index.html for the owner
#   test_listed_route_refuses_non_owner              a listed path, no identity / wrong identity -> 401 / 403, no body
#   test_unknown_path_still_404                      a path not in routes.json -> 404, as today
#   test_missing_routes_file_serves_root_only        no or unreadable routes.json -> "/" serves, "/control-plane" 404s
#   test_existing_routes_keep_their_endpoint         /health, /assets/x, /api/admin/whoami, /mcp, /sprint resolve to
#                                                    the same endpoint as before the change (the app's route table)
. "$(dirname "$0")/_root.sh"
named_pytest "deep-link tests" tests/test_dashboard_deep_links.py test_each_listed_route_serves_index_to_owner test_listed_route_refuses_non_owner test_unknown_path_still_404 test_missing_routes_file_serves_root_only test_existing_routes_keep_their_endpoint
