# 0.9.0_WK_NFRA_MCPORTAL~14 on NFRA_MCPORTAL.TO-MP-z-2

- Built the Gateway page, getGatewayBreakdown, the /gateway route, the sidebar entry and public/routes.json in mcportal commit 6fbd25e (branch wk-NFRA_MCPORTAL-gw-14-mcportal over bc37107). Not pushed.
- z2.AC1.sh and z2.AC2.sh both RESULT: PASS exit=0 after the commit.
- Control: with "/gateway" deleted from public/routes.json on disk, `bun test src/pages/gateway` read 5 pass 1 fail; restored, mcportal status clean.
- Note: deleting the /gateway Route from App.tsx alone does not fail the drift test, because the test (as the order specifies) unions the PAGES paths, and /gateway is in PAGES.
