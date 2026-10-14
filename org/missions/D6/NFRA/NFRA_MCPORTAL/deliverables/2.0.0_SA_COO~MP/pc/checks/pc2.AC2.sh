#!/usr/bin/env bash
# MP-pc-2 AC2 (THE SEAM, C15; decomposition PC.3 "what a person holds"): in one planted world, each person's tools from
# GET /api/admin/people EQUAL the tools the breakdown's holder rows list for that person, with a difference control in the
# same test (blocklisting one person empties BOTH sides for it); and against the real server's registered tools every
# tool a person is listed holding is a tool the live server registers.
#   test_person_holdings_equal_breakdown_holders
#   test_real_server_people_inventory
. "$(dirname "$0")/_root.sh"
named_pytest "people seam" tests/test_admin_people.py test_person_holdings_equal_breakdown_holders test_real_server_people_inventory
