# Session log -- 0.9.0_WK_NFRA_MCPORTAL~13 on NFRA_MCPORTAL.TO-MP-z-1

- Grounded: worktree C:/tmp/mp-gw-13, branch wk-NFRA_MCPORTAL-gw-13 over 233e78932a; org/ and .tools/ present.
- Built app/admin_gateway_breakdown.py and tests/test_admin_gateway_breakdown.py (code commit 0de6cfb834, test fix 28a7ff1904).
- Premise found false: the email rosters do not set a person's tier (config.py:320-323, tier.resolve_tier). Row NFRA_MCPORTAL-Z-W13-S1.
- Mutation control: with identity_scope.check, data_entitlement.tool_denial or blocklist.enforce removed from _admits, the seam test failed each time (1 failed, 8 passed); restored, 9 passed.
- AC1 and AC2 both PASS exit=0 after the print fix (an earlier AC2 read 1 of 2 because a debug print split the PASSED line; fixed in 28a7ff1904).
