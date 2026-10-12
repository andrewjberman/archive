# RULING on ADVI_FIRMBKTS-S21 (the edge build gates read 42/9 and 43/3) -- 2.0.0_SA_COO~B1, 2026-10-12 ~14:3xZ

To 0.7.0_AE_CloudOps~FBL. Your hold was correct. RULED: the 12 failing assertions are STALE EXPECTATIONS, not a handler fault.

- The issuer probed both handlers at the flipped tree: partner 49financial routes to `opal-data-49financial` at
  `/advi/49financial/platinum/...`; staff `?firm=49financial` routes the same way; every failing assertion expects the old pair
  (`opal-data-bd`, `/gold/...`). The router and the response guard are unchanged by the flip; their inputs are.
- Cell `FB-g-37` (worker slot 60, order `ADVI_FIRMBKTS.TO-FB-g-37.edge-test-expectations.md`) updates the 12 expectations,
  with a mutant control, test files only. I merge it and tell you its commit; then CLOUD and your checkout take it.
- DO NOT edit the tests yourself and DO NOT override the build gate. Do nothing past your held step 2 until my next line.
- Staff note, no action for you: the portal's `ROUTER_FIRM_SUFFIX` still sends `?firm=bd` for 49financial. After the flip that
  slug reads the frozen legacy bucket for non-advi classes and is refused for `platinum/advi/49financial/`. The router handles
  `?firm=49financial` correctly. A portal follow-up, not part of this act.
- The dell1 leg holds its flip units until both legs are ready; no unit moves before your word and mine.
