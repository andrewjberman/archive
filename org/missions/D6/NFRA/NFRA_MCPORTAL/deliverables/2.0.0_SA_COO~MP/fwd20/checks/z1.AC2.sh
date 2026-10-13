#!/usr/bin/env bash
# MP-z-1 AC2 (the seam against the REAL neighbours: the dispatch chain and the live server's registry; GW.0 item 2, GW.3):
#   test_holders_match_the_dispatch_chain   for each planted candidate (a master admin, a write-capable address, a scoped
#                                           identity, a profiled principal with an active grant, a blocklisted address,
#                                           and the population row) the tools the breakdown lists it as holding EQUAL the
#                                           tools the gateway's own chain admits for it. Difference control inside the same
#                                           test: blocklisting the write-capable address moves BOTH sides to empty.
#   test_real_server_tool_inventory         the real `app.tools.mcp` registered list (with the integrations the test
#                                           enables): every tool appears in exactly one channel and the channel count is
#                                           1 + the number of active integrations
. "$(dirname "$0")/_root.sh"
named_pytest "breakdown seam" tests/test_admin_gateway_breakdown.py test_holders_match_the_dispatch_chain test_real_server_tool_inventory
